import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from datetime import datetime
import requests
import re

class RAGSystem:
    def __init__(self):
        self.data_dir = Path("data")
        self.chroma_dir = Path("chroma_db")
        self.chroma_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_dir),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            self.embedding_model = None
            
        self.collection = None
        self.initialized = False
        
    def is_initialized(self) -> bool:
        """Check if the knowledge base is initialized"""
        if self.chroma_dir.exists() and any(self.chroma_dir.iterdir()):
            try:
                collection = self.client.get_or_create_collection("manipal_knowledge")
                return collection.count() > 0
            except:
                return False
        return False
        
    def initialize(self):
        """Initialize the RAG system by loading data into vector database"""
        if not self.embedding_model:
            print("Embedding model not available. Using fallback...")
            self.initialized = False
            return False
            
        print("Initializing RAG system...")
        
        try:
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="manipal_knowledge",
                metadata={"description": "Manipal Institute of Technology Knowledge Base"}
            )
            
            # Clear existing data if rebuilding
            if self.collection.count() > 0:
                print("Clearing existing data for fresh build...")
                try:
                    self.client.delete_collection("manipal_knowledge")
                except:
                    pass
                self.collection = self.client.create_collection(
                    name="manipal_knowledge",
                    metadata={"description": "Manipal Institute of Technology Knowledge Base"}
                )
            
            # Load and process all data files
            data_files = [
                "official_info.json",
                "courses.json",
                "hostels.json",
                "fees.json",
                "facilities.json",
                "admissions.json"
            ]
            
            documents = []
            metadatas = []
            ids = []
            
            for file_name in data_files:
                file_path = self.data_dir / file_name
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        processed = self._process_json_data(data, file_name.replace(".json", ""))
                        for i, doc in enumerate(processed):
                            documents.append(doc["text"])
                            metadatas.append(doc["metadata"])
                            ids.append(f"{file_name}_{i}")
            
            if documents:
                # Generate embeddings
                print(f"Generating embeddings for {len(documents)} documents...")
                embeddings = self.embedding_model.encode(documents, show_progress_bar=True).tolist()
                
                # Add to ChromaDB in batches to avoid memory issues
                batch_size = 100
                for i in range(0, len(documents), batch_size):
                    batch_docs = documents[i:i+batch_size]
                    batch_embeddings = embeddings[i:i+batch_size]
                    batch_metas = metadatas[i:i+batch_size]
                    batch_ids = ids[i:i+batch_size]
                    
                    self.collection.add(
                        embeddings=batch_embeddings,
                        documents=batch_docs,
                        metadatas=batch_metas,
                        ids=batch_ids
                    )
                
                print(f"Added {len(documents)} documents to knowledge base")
                self.initialized = True
                return True
            else:
                print("No documents to add to knowledge base")
                self.initialized = False
                return False
        except Exception as e:
            print(f"Error initializing RAG system: {e}")
            self.initialized = False
            return False
            
    def _process_json_data(self, data: Dict, source: str) -> List[Dict]:
        """Process JSON data into text chunks with metadata"""
        chunks = []
        
        def extract_text(obj: any, prefix: str = "", depth: int = 0) -> List[str]:
            """Recursively extract text from JSON structure"""
            texts = []
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_text = key.replace("_", " ").title()
                    if isinstance(value, (dict, list)):
                        texts.extend(extract_text(value, f"{prefix} {key_text}", depth + 1))
                    else:
                        texts.append(f"{prefix} {key_text}: {value}")
            elif isinstance(obj, list):
                for item in obj:
                    if isinstance(item, (dict, list)):
                        texts.extend(extract_text(item, prefix, depth + 1))
                    else:
                        texts.append(f"{prefix}: {item}")
            else:
                texts.append(f"{prefix}: {obj}")
            return texts
        
        # Convert JSON to readable text
        text_parts = extract_text(data)
        full_text = " ".join(text_parts)
        
        # Split into chunks (simple splitting by sentences)
        sentences = full_text.split(". ")
        current_chunk = []
        current_length = 0
        chunk_size = 400  # Smaller chunks for better retrieval
        
        for sentence in sentences:
            if current_length + len(sentence) > chunk_size and current_chunk:
                chunk_text = ". ".join(current_chunk) + "."
                chunks.append({
                    "text": chunk_text,
                    "metadata": {"source": source, "type": "structured_data"}
                })
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence)
        
        # Add remaining chunk
        if current_chunk:
            chunk_text = ". ".join(current_chunk) + "."
            chunks.append({
                "text": chunk_text,
                "metadata": {"source": source, "type": "structured_data"}
            })
        
        return chunks
        
    def query(self, question: str, top_k: int = 8) -> Dict:
        """Query the RAG system"""
        if not self.initialized or not self.collection:
            # Fallback to rule-based responses
            return self._fallback_response(question)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([question]).tolist()[0]
            
            # Search similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Extract relevant context
            contexts = results["documents"][0] if results["documents"] else []
            sources = results["metadatas"][0] if results["metadatas"] else []
            
            # Generate response using LLM
            answer = self._generate_response(question, contexts)
            
            return {
                "answer": answer,
                "sources": [s.get("source", "unknown") for s in sources],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error in RAG query: {e}")
            return self._fallback_response(question)
            
    def _generate_response(self, question: str, contexts: List[str]) -> str:
        """Generate response using improved prompt and context"""
        # Combine contexts intelligently
        context_text = "\n\n".join(contexts[:5])  # Use top 5 contexts
        
        # Create improved, more conversational prompt
        prompt = f"""You are a friendly and knowledgeable AI assistant for Manipal Institute of Technology (MIT), Manipal. 
You provide detailed, accurate, and helpful answers about the college.

CONTEXT INFORMATION:
{context_text}

USER QUESTION: {question}

INSTRUCTIONS:
1. Answer the question naturally and conversationally, like ChatGPT
2. Use the context information provided above to give accurate, detailed answers
3. If the context contains relevant information, use it to provide comprehensive answers
4. Structure your answer clearly with proper paragraphs
5. If the context doesn't fully answer the question, provide the best answer you can based on the context and mention that for more details, they can contact the college
6. Be friendly, professional, and helpful
7. Format numbers, fees, and important details clearly
8. If asked about something not in the context, politely say you don't have that specific information but offer to help with related topics

ANSWER:"""
        
        # Try Hugging Face Inference API first
        try:
            return self._call_huggingface_api(prompt, question, contexts)
        except Exception as e:
            print(f"Hugging Face API error: {e}")
            # Fallback to improved rule-based generation
            return self._improved_rule_based_response(question, contexts)
            
    def _call_huggingface_api(self, prompt: str, question: str, contexts: List[str]) -> str:
        """Call Hugging Face Inference API with better model"""
        # Try using a better free model
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"}
        
        # If no API key, use improved rule-based
        if not os.getenv('HUGGINGFACE_API_KEY'):
            return self._improved_rule_based_response(question, contexts)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        answer = result[0]["generated_text"].strip()
                        # Clean up the answer
                        answer = re.sub(r'^ANSWER:\s*', '', answer, flags=re.IGNORECASE)
                        if answer:
                            return answer
            return self._improved_rule_based_response(question, contexts)
        except Exception as e:
            print(f"API call error: {e}")
            return self._improved_rule_based_response(question, contexts)
            
    def _improved_rule_based_response(self, question: str, contexts: List[str]) -> str:
        """Generate improved, more natural responses using context"""
        question_lower = question.lower()
        
        # Extract and organize relevant information from contexts
        relevant_sections = []
        all_info = {}
        
        for context in contexts:
            # Extract key information
            sentences = context.split(". ")
            for sentence in sentences:
                sentence_clean = sentence.strip()
                if not sentence_clean:
                    continue
                
                sentence_lower = sentence_clean.lower()
                # Categorize information
                if any(word in question_lower for word in sentence_lower.split()):
                    relevant_sections.append(sentence_clean)
                
                # Extract structured data
                if ":" in sentence_clean:
                    parts = sentence_clean.split(":", 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower()
                        value = parts[1].strip()
                        if key not in all_info:
                            all_info[key] = []
                        all_info[key].append(value)
        
        # Build comprehensive answer
        if relevant_sections:
            # Remove duplicates while preserving order
            seen = set()
            unique_sections = []
            for section in relevant_sections:
                if section not in seen:
                    seen.add(section)
                    unique_sections.append(section)
            
            # Combine into natural answer
            answer_parts = []
            
            # Start with most relevant sentence
            if unique_sections:
                main_answer = unique_sections[0]
                answer_parts.append(main_answer)
                
                # Add supporting details
                for section in unique_sections[1:6]:  # Limit to 5 additional sections
                    if section != main_answer and len(section) > 20:
                        answer_parts.append(section)
                
                answer = ". ".join(answer_parts)
                
                # Ensure proper ending
                if not answer.endswith((".", "!", "?")):
                    answer += "."
                
                # Add helpful closing if appropriate
                if len(answer_parts) > 1:
                    answer += " If you need more specific information, feel free to ask or contact the admissions office."
                
                return answer
        
        # Fallback to keyword-based responses with more detail
        return self._detailed_fallback_response(question_lower, all_info)
        
    def _detailed_fallback_response(self, question_lower: str, info_dict: Dict) -> str:
        """Generate detailed fallback responses"""
        
        if any(word in question_lower for word in ["course", "program", "degree", "b.tech", "m.tech"]):
            response = "Manipal Institute of Technology (MIT) offers a wide range of programs:\n\n"
            response += "**Undergraduate Programs (B.Tech):**\n"
            response += "• Computer Science & Engineering\n"
            response += "• Information Technology\n"
            response += "• Electronics & Communication Engineering\n"
            response += "• Mechanical Engineering\n"
            response += "• Civil Engineering\n"
            response += "• Electrical & Electronics Engineering\n"
            response += "• Aerospace Engineering\n"
            response += "• Chemical Engineering\n\n"
            response += "**Postgraduate Programs (M.Tech & MBA):**\n"
            response += "• Various M.Tech specializations in engineering fields\n"
            response += "• MBA program\n\n"
            response += "The duration for B.Tech is 4 years and M.Tech is 2 years. "
            response += "Admissions are based on MET (Manipal Entrance Test) or JEE Main scores for B.Tech programs. "
            response += "For detailed information about specific courses, eligibility criteria, and admission requirements, "
            response += "I'd recommend visiting the official MIT Manipal website or contacting the admissions office."
            return response
        
        if any(word in question_lower for word in ["fee", "cost", "price", "tuition", "money"]):
            response = "Here's the fee structure at MIT Manipal:\n\n"
            response += "**B.Tech Programs:**\n"
            response += "• Annual tuition: ₹4,00,000 - ₹5,00,000 per year\n"
            response += "• Total 4-year cost: ₹16,00,000 - ₹20,00,000\n\n"
            response += "**M.Tech Programs:**\n"
            response += "• Annual tuition: ₹2,00,000 - ₹3,00,000 per year\n\n"
            response += "**MBA Program:**\n"
            response += "• Annual tuition: ₹5,00,000 - ₹7,00,000 per year\n\n"
            response += "**Additional Costs:**\n"
            response += "• Admission fee (one-time): ₹50,000 - ₹1,00,000\n"
            response += "• Security deposit (refundable): ₹25,000 - ₹50,000\n"
            response += "• Hostel fees: ₹80,000 - ₹1,70,000 per year (depending on accommodation type)\n"
            response += "• Medical insurance: ₹5,000 - ₹10,000 per year\n\n"
            response += "**Financial Aid:**\n"
            response += "MIT Manipal offers various scholarships including merit-based scholarships (up to 50% fee waiver based on MET/JEE rank), "
            response += "sports quota scholarships, need-based financial aid, and alumni scholarships. "
            response += "Education loans and EMI options are also available."
            return response
        
        if any(word in question_lower for word in ["hostel", "accommodation", "mess", "room", "living"]):
            response = "MIT Manipal provides comprehensive hostel facilities:\n\n"
            response += "**Boys Hostels:**\n"
            response += "• Non-AC Double Occupancy: ₹80,000 - ₹90,000/year\n"
            response += "• AC Double Occupancy: ₹1,20,000 - ₹1,40,000/year\n"
            response += "• Non-AC Single Occupancy: ₹1,50,000 - ₹1,70,000/year\n\n"
            response += "**Girls Hostels:**\n"
            response += "• Non-AC Double Occupancy: ₹80,000 - ₹90,000/year\n"
            response += "• AC Double Occupancy: ₹1,20,000 - ₹1,40,000/year\n\n"
            response += "**Facilities:** All hostels include Wi-Fi, common rooms, laundry services, mess facilities, and 24/7 security.\n\n"
            response += "**Mess Timings:**\n"
            response += "• Breakfast: 7:00 AM - 9:00 AM\n"
            response += "• Lunch: 12:00 PM - 2:00 PM\n"
            response += "• Snacks: 4:00 PM - 6:00 PM\n"
            response += "• Dinner: 7:00 PM - 9:00 PM\n\n"
            response += "Mess fees are included in the hostel fees, and both vegetarian and non-vegetarian options are available."
            return response
        
        if any(word in question_lower for word in ["admission", "apply", "entrance", "met", "jee", "how to"]):
            response = "**Admission Process for MIT Manipal:**\n\n"
            response += "**Entrance Exams Accepted:**\n"
            response += "• MET (Manipal Entrance Test) - conducted by MAHE\n"
            response += "• JEE Main - for B.Tech programs\n"
            response += "• GATE - for M.Tech programs (minimum 50 percentile)\n\n"
            response += "**Application Steps:**\n"
            response += "1. Register online on the official MIT Manipal website\n"
            response += "2. Fill out the application form\n"
            response += "3. Pay application fee (₹600 - ₹2,000)\n"
            response += "4. Appear for entrance exam (if applicable)\n"
            response += "5. Participate in counseling and seat allocation\n"
            response += "6. Complete document verification and fee payment\n\n"
            response += "**Important Dates:**\n"
            response += "• Application usually starts: October-November\n"
            response += "• Application deadline: March-April\n"
            response += "• Exam date: April-May\n"
            response += "• Results: May-June\n"
            response += "• Counseling: June-July\n"
            response += "• Admission: July-August\n\n"
            response += "**Contact:**\n"
            response += "Admissions Office: +91 820 292 2400\n"
            response += "Email: admissions@manipal.edu\n"
            response += "Website: https://manipal.edu/mit"
            return response
        
        if any(word in question_lower for word in ["library", "book", "study", "resource"]):
            response = "The Knowledge Resource Centre (Library) at MIT Manipal is a comprehensive facility:\n\n"
            response += "**Collection:**\n"
            response += "• Books: 300,000+\n"
            response += "• Journals: 1,500+\n"
            response += "• E-books: 50,000+\n"
            response += "• Digital databases: Access to IEEE, ACM, Springer, and more\n\n"
            response += "**Operating Hours:**\n"
            response += "• Weekdays: 8:00 AM - 10:00 PM\n"
            response += "• Saturday: 9:00 AM - 6:00 PM\n"
            response += "• Sunday: 10:00 AM - 6:00 PM\n\n"
            response += "**Services:**\n"
            response += "• Book lending (maximum 5 books for 15 days)\n"
            response += "• 24/7 digital library access\n"
            response += "• Study room booking\n"
            response += "• Research assistance\n"
            response += "• Printing and scanning facilities"
            return response
        
        if any(word in question_lower for word in ["facility", "campus", "lab", "sports", "cafeteria"]):
            response = "MIT Manipal offers extensive campus facilities:\n\n"
            response += "**Library:** Knowledge Resource Centre with 300,000+ books and digital resources\n\n"
            response += "**Laboratories:** Multiple well-equipped computer labs, engineering labs, and advanced research facilities\n\n"
            response += "**Sports Facilities:**\n"
            response += "• Indoor: Basketball, Badminton, Table Tennis, Gym, Squash\n"
            response += "• Outdoor: Cricket, Football, Tennis, Volleyball, Athletics\n"
            response += "• Sports complex with courts, fields, and gymnasium\n\n"
            response += "**Cafeterias:** Multiple food courts serving Indian, Chinese, Continental, and Fast Food (7 AM - 10 PM)\n\n"
            response += "**Medical:** Campus health center with doctors and 24/7 ambulance service\n\n"
            response += "**Technology:** Campus-wide high-speed Wi-Fi available 24/7\n\n"
            response += "**Transportation:** Regular bus service within campus and to nearby areas"
            return response
        
        # General helpful response
        response = "I'm here to help you with information about MIT Manipal! I can provide details about:\n\n"
        response += "• Academic programs (B.Tech, M.Tech, MBA)\n"
        response += "• Fee structure and scholarships\n"
        response += "• Hostel facilities and accommodation\n"
        response += "• Admission process and requirements\n"
        response += "• Campus facilities (library, labs, sports, cafeterias)\n"
        response += "• Campus life and activities\n\n"
        response += "What specific information would you like to know? Feel free to ask me anything about MIT Manipal!"
        return response
        
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when RAG system is not initialized"""
        answer = self._detailed_fallback_response(question.lower(), {})
        return {
            "answer": answer,
            "sources": ["general_knowledge"],
            "timestamp": datetime.now().isoformat()
        }
