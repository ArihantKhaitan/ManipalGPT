from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import uvicorn

from rag_system import RAGSystem
from data_collector import DataCollector

load_dotenv()

# Initialize RAG system
rag_system = RAGSystem()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RAG system on startup"""
    print("Initializing RAG system...")
    try:
        if not rag_system.is_initialized():
            print("Knowledge base not found. Collecting data...")
            collector = DataCollector()
            collector.collect_all_data()
            rag_system.initialize()
        else:
            # Just load the existing collection
            rag_system.collection = rag_system.client.get_or_create_collection("manipal_knowledge")
            rag_system.initialized = True
        print("RAG system ready!")
    except Exception as e:
        print(f"Warning: Could not initialize RAG system: {e}")
        print("System will use fallback responses. You can rebuild the knowledge base later.")
    yield
    # Cleanup code can go here if needed

app = FastAPI(
    title="Manipal AI Chat API", 
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3004", "http://127.0.0.1:3004"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Manipal AI Chat API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "initialized": rag_system.is_initialized()}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get response from RAG system
        result = rag_system.query(request.message.strip())
        
        return ChatResponse(
            response=result["answer"],
            sources=result.get("sources", []),
            timestamp=result.get("timestamp", "")
        )
    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/api/rebuild-knowledge-base")
async def rebuild_knowledge_base():
    """Rebuild the knowledge base from collected data"""
    try:
        collector = DataCollector()
        collector.collect_all_data()
        rag_system.initialize()
        return {"message": "Knowledge base rebuilt successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rebuilding knowledge base: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

