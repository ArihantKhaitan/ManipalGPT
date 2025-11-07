# ManipalGPT - AI Chatbot for MIT Manipal

An intelligent AI-powered chatbot designed specifically for Manipal Institute of Technology (MIT), Manipal. This application provides instant, ChatGPT-like answers to questions about courses, fees, hostels, facilities, admissions, and campus life.

![MIT Manipal AI Assistant](https://img.shields.io/badge/MIT-Manipal-orange?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

## ✨ Features

- **🤖 ChatGPT-like AI**: Advanced RAG (Retrieval Augmented Generation) system for natural, conversational responses
- **🎨 Premium Liquid Glass UI**: Beautiful minimalist design with glass morphism effects, orange/white/black theme
- **📚 Comprehensive Knowledge Base**: Detailed information about courses, fees, hostels, facilities, and admissions
- **⚡ Real-time Responses**: Fast and accurate answers with context-aware generation
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **🌙 Dark Mode**: Elegant dark theme with orange accents
- **🆓 Free & Open Source**: Uses free AI APIs and open-source technologies

## 🎯 What It Can Answer

- **Academic Programs**: B.Tech, M.Tech, MBA courses and specializations
- **Fee Structure**: Tuition fees, hostel fees, scholarships, and payment options
- **Hostel Information**: Accommodation types, facilities, mess timings, and rules
- **Campus Facilities**: Library, laboratories, sports, cafeterias, medical facilities
- **Admissions**: Entrance exams (MET, JEE Main, GATE), application process, important dates
- **Campus Life**: Events, activities, transportation, and student resources

## 📋 Prerequisites

- **Node.js** (v18 or higher) - For the frontend
- **Python** (v3.8 or higher) - For the backend
- **pip** - Python package manager
- **npm** or **yarn** - Node package manager

## 🚀 Quick Start

### Windows Users

#### Step 1: Setup Backend

1. Open Command Prompt or PowerShell
2. Navigate to the project directory:
   ```bash
   cd Manipal_gpt
   cd backend
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```
   
   Or double-click `start_backend.bat` from the project root.

   The backend will start on `http://localhost:8000`

#### Step 2: Setup Frontend

1. Open a **new** Command Prompt or PowerShell window
2. Navigate to the frontend directory:
   ```bash
   cd Manipal_gpt
   cd frontend
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```
   
   Or run directly with npx:
   ```bash
   npx next dev -p 3004
   ```
   
   Or double-click `start_frontend.bat` from the project root.

   The frontend will start on `http://localhost:3004`

#### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:3004
```

### Linux/Mac Users

#### Step 1: Setup Backend

```bash
cd Manipal_gpt/backend
pip install -r requirements.txt
python3 main.py
```

Or:
```bash
chmod +x start_backend.sh
./start_backend.sh
```

#### Step 2: Setup Frontend

Open a new terminal:
```bash
cd Manipal_gpt/frontend
npm install
npm run dev
```

Or run directly with npx:
```bash
cd Manipal_gpt/frontend
npx next dev -p 3004
```

Or:
```bash
chmod +x start_frontend.sh
./start_frontend.sh
```

#### Step 3: Access the Application

Open your web browser and navigate to:
```
http://localhost:3004
```

## 📝 First Run

On the first run, the backend will:
1. Collect data about Manipal Institute of Technology
2. Build a knowledge base using vector embeddings (this may take 2-5 minutes)
3. Start accepting chat requests

You'll see progress messages in the backend console. **Please be patient** - the initial setup downloads AI models and builds the knowledge base.

## 📁 Project Structure

```
Manipal_gpt/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main FastAPI application
│   ├── data_collector.py   # Data collection from various sources
│   ├── rag_system.py       # Advanced RAG system for AI responses
│   ├── requirements.txt    # Python dependencies
│   ├── data/               # Collected data (generated)
│   └── chroma_db/          # Vector database (generated)
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx    # Main chat interface (liquid glass UI)
│   │   │   ├── layout.tsx  # Root layout with Poppins font
│   │   │   ├── globals.css  # Global styles with liquid glass effects
│   │   │   └── api/        # Next.js API routes
│   │   └── components/     # UI components
│   ├── package.json        # Node dependencies
│   └── ...
│
├── start_backend.bat       # Windows backend startup script
├── start_frontend.bat      # Windows frontend startup script
├── start_backend.sh        # Linux/Mac backend startup script
├── start_frontend.sh       # Linux/Mac frontend startup script
└── README.md               # This file
```

## 🔧 Configuration

### Backend Configuration

Create a `.env` file in the `backend/` directory (optional):

```env
# Hugging Face API Key (optional - for better AI responses)
# Get your free API key from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=your_api_key_here

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
```

**Note**: The system works without an API key using rule-based responses, but an API key enables more natural, ChatGPT-like responses.

### Frontend Configuration

The frontend is configured to:
- Run on port **3004** (default)
- Connect to backend at `http://localhost:8000`
- Use **Poppins** font for better readability
- Feature **liquid glass** UI with orange/white/black theme

To change the backend URL, create a `.env.local` file in the `frontend/` directory:

```env
BACKEND_URL=http://your-backend-url:8000
```

## 🎨 UI Features

- **Liquid Glass Design**: Premium glass morphism effects with backdrop blur
- **Minimalist Layout**: Clean, uncluttered interface
- **Orange/White/Black Theme**: Manipal brand colors
- **Poppins Font**: Modern, readable typography
- **Smooth Animations**: Framer Motion powered transitions
- **Responsive Sidebar**: Collapsible navigation with quick actions
- **Message Bubbles**: Rounded, elegant chat bubbles with proper spacing
- **Auto-focus Input**: Cursor automatically focuses on input box
- **Stop Generation**: Button to stop AI response generation

## 📚 Knowledge Base

The system collects comprehensive information from various sources about:

- **Courses & Programs**: B.Tech, M.Tech, MBA programs with specializations
- **Fees**: Detailed tuition fees, hostel fees, scholarships, and payment options
- **Hostels**: Accommodation types, facilities, mess timings, and rules
- **Campus Facilities**: Library (300,000+ books), labs, sports, cafeterias, medical
- **Admissions**: Entrance exams (MET, JEE Main, GATE), application process, dates
- **Campus Life**: Events, activities, transportation, and student resources

### Rebuilding the Knowledge Base

To rebuild the knowledge base with updated data:

```bash
# Make a POST request to the rebuild endpoint
curl -X POST http://localhost:8000/api/rebuild-knowledge-base
```

Or visit the endpoint in your browser while the server is running.

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **ChromaDB** - Vector database for embeddings
- **Sentence Transformers** - For text embeddings (all-MiniLM-L6-v2)
- **Hugging Face API** - Free LLM API (optional, for better responses)
- **BeautifulSoup4** - Web scraping capabilities

### Frontend
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS 4** - Utility-first CSS
- **Framer Motion** - Smooth animations
- **Radix UI** - Accessible UI components
- **Poppins Font** - Modern typography
- **Lucide React** - Beautiful icons

## 🎯 AI Capabilities

### RAG System
- **Vector Search**: Semantic search using embeddings
- **Context Retrieval**: Top 8 most relevant contexts per query
- **Response Generation**: Natural, conversational responses
- **Fallback System**: Rule-based responses when API unavailable

### Response Quality
- **Comprehensive Answers**: Detailed, structured responses
- **Context-Aware**: Uses relevant information from knowledge base
- **Natural Language**: ChatGPT-like conversational tone
- **Source Attribution**: Tracks information sources

## 🔍 API Endpoints

### Backend API

- `GET /` - Health check
- `GET /health` - System status and initialization state
- `POST /api/chat` - Send a chat message
  ```json
  {
    "message": "What are the B.Tech courses available?"
  }
  ```
  Response:
  ```json
  {
    "response": "Manipal Institute of Technology offers various B.Tech programs...",
    "sources": ["courses", "official_info"],
    "timestamp": "2025-11-07T19:30:00"
  }
  ```
- `POST /api/rebuild-knowledge-base` - Rebuild the knowledge base

## 🐛 Troubleshooting

### Frontend Server Not Starting (Port 3004)

**If the server exits immediately or shows "site can't be reached":**

1. **Check if port 3004 is in use:**
   - Windows: `netstat -ano | findstr :3004`
   - Linux/Mac: `lsof -i :3004`
   - If in use, kill the process or use a different port

2. **Clear Next.js cache:**
   ```bash
   cd frontend
   rm -rf .next
   npm run dev
   ```

3. **Check for compilation errors:**
   ```bash
   cd frontend
   npm run build
   ```

4. **Reinstall dependencies:**
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run dev
   ```

5. **Verify Node.js version:** Must be 18 or higher
   ```bash
   node --version
   ```

### Backend Issues

- **ImportError with huggingface_hub**: If you see `cannot import name 'cached_download'`, the requirements.txt has the correct versions. Just run:
  ```bash
  cd backend
  pip install -r requirements.txt --upgrade
  ```

- **Port 8000 already in use**: Change the port in `backend/main.py` or stop the other service

- **Python not found**: Make sure Python 3.8+ is installed and added to PATH

- **Module not found**: Run `pip install -r requirements.txt --upgrade` again

- **Backend still downloading**: This is normal on first run! It can take 5-10 minutes to download models and build the knowledge base. Just wait for it to complete.

- **TensorFlow conflicts**: The requirements.txt uses compatible versions. If issues persist, try:
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt --no-cache-dir
  ```

### Connection Issues

- **Make sure both servers are running**: You need TWO terminal windows - one for backend, one for frontend
- **Check backend health**: Visit `http://localhost:8000/health` in your browser
- **Check frontend**: Visit `http://localhost:3004` in your browser
- **Check browser console**: Press F12 and check for errors in the Console tab
- **Verify CORS settings**: Backend should allow `http://localhost:3004`

### Slow Responses

- First-time initialization takes longer as it builds the knowledge base (5-10 minutes)
- Consider using a Hugging Face API key for faster/better responses
- Check your internet connection if using Hugging Face API
- The system uses rule-based responses without API key, which are still comprehensive

### Knowledge Base Not Updating

- Delete the `backend/chroma_db/` directory and restart the server
- Use the rebuild endpoint: `POST /api/rebuild-knowledge-base`
- Check that data files exist in `backend/data/` directory

## ✅ Verification

To verify everything is working:

1. **Backend health check**: Visit `http://localhost:8000/health`
   - Should return: `{"status": "healthy", "initialized": true}`

2. **Frontend**: Visit `http://localhost:3004`
   - Should show the chat interface with liquid glass UI

3. **Test a question**: Try asking:
   - "What courses are available at MIT Manipal?"
   - "Tell me about hostel facilities"
   - "What are the fees for B.Tech?"

## 🚀 Deployment

### Backend Deployment

The backend can be deployed on:
- **Heroku**: Use the Procfile included
- **Railway**: Connect your GitHub repo
- **Render**: Deploy from GitHub
- **AWS/GCP/Azure**: Use containerized deployment
- **PythonAnywhere**: Free hosting for Python apps

### Frontend Deployment

The frontend can be deployed on:
- **Vercel**: Recommended for Next.js (connect GitHub repo)
- **Netlify**: Deploy from GitHub
- **Any static hosting**: Build with `npm run build` and serve the `out` directory

### Environment Variables for Production

Make sure to set:
- `BACKEND_URL` in frontend `.env.local` pointing to your deployed backend
- `HUGGINGFACE_API_KEY` in backend `.env` for better responses

## 📝 Development

### Adding New Data Sources

Edit `backend/data_collector.py` to add new data sources:

```python
def collect_new_data(self):
    """Collect new data source"""
    data = {
        "new_topic": {
            "info": "Your data here"
        }
    }
    with open(self.data_dir / "new_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

Then add the file to the data_files list in `rag_system.py`.

### Customizing the AI Responses

Edit `backend/rag_system.py` to customize:
- Embedding model (currently `all-MiniLM-L6-v2`)
- LLM API endpoint
- Response generation logic
- Context retrieval strategy (top_k parameter)
- Prompt templates

### UI Customization

- **Chat Interface**: Edit `frontend/src/app/page.tsx`
- **Styling**: Edit `frontend/src/app/globals.css`
- **Components**: Modify files in `frontend/src/components/`
- **Font**: Change in `frontend/src/app/layout.tsx`
- **Colors**: Update CSS variables in `globals.css`

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the code comments for implementation details

## 🙏 Acknowledgments

- **Manipal Institute of Technology** for inspiration
- **Hugging Face** for free AI APIs and models
- **ChromaDB** for vector database
- **Next.js and FastAPI** communities
- **Open source contributors** who made this possible

## 📅 Version History

- **v1.1.0** - Enhanced UI and AI (Current)
  - Premium liquid glass UI with Poppins font
  - Improved AI response generation (ChatGPT-like)
  - Better context retrieval (top 8 results)
  - Enhanced fallback responses
  - Orange/white/black theme
  - Better spacing and layout

- **v1.0.0** - Initial release
  - Basic chat interface
  - Knowledge base for MIT Manipal
  - Course, fees, hostel, and facility information
  - Dark mode support
  - Responsive design

---

**Made with ❤️ for MIT Manipal students**

*Empowering students with instant access to college information through AI*
