# 🎓 AI-Powered University Helpdesk — NIST University

An intelligent RAG-based chatbot that answers student queries about NIST University Berhampur using university documents. Supports English, Hindi, and Odia languages.

🌐 **Live Demo:** https://ai-university.streamlit.app

## 🚀 Demo
![Helpdesk Demo](docs/architecture.png)

## 🛠️ Tech Stack
- **LLM** — Groq (llama-3.3-70b-versatile)
- **RAG Framework** — LangChain
- **Vector Database** — FAISS
- **Embeddings** — HuggingFace (all-MiniLM-L6-v2)
- **Backend** — FastAPI + Uvicorn
- **Frontend** — Streamlit
- **Language Detection** — langdetect

## 💡 Features
- Ask questions about admissions, fees, hostel, placements, exams
- Upload any university PDF and get instant answers
- Multilingual support — English, Hindi, Odia
- Auto language detection
- REST API backend with Swagger docs at /docs
- Powered by Groq API (fast cloud LLM)

## 🏗️ Architecture
```
Student Question → Streamlit UI → FastAPI → RAG Pipeline → FAISS Search → Ollama LLM → Answer
```

## ⚙️ How to Run

### 1. Clone the repo
```bash
git clone https://github.com/Rani2025-tech/ai-university-helpdesk.git
cd ai-university-helpdesk
```

### 2. Create virtual environment
```bash
python -m venv rag_env
rag_env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```env
GROQ_API_KEY=your_groq_api_key_here
FAISS_INDEX_PATH=faiss_index
ADMIN_PASSWORD=your_admin_password
```

### 5. Start FastAPI backend
```bash
python -m uvicorn backend.main:app --reload
```

### 6. Start Streamlit frontend
```bash
streamlit run frontend/app.py
```

### 7. Open browser
```bash
streamlit run frontend/app.py
```

### 8. Open browser
```
https://ai-university.streamlit.app
```

## 📁 Project Structure
```
ai-university-helpdesk/
├── backend/
│   ├── main.py          # FastAPI app
│   ├── routes.py        # API endpoints
│   ├── rag_pipeline.py  # RAG logic
│   └── utils.py         # Helper functions
├── frontend/
│   └── app.py           # Streamlit UI
├── data/                # University PDFs
├── docs/                # Architecture diagram
├── .env                 # Config (not uploaded)
├── requirements.txt
└── README.md
```

## 🎯 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Check server status |
| POST | /api/upload | Upload university PDF |
| POST | /api/ask | Ask a question |
| GET | /api/documents | List uploaded PDFs |

## 👨‍💻 Built By
RANI NAYAK — NIST University Berhampur
```

Press `Ctrl + S`.

---

**Step 3 — update `requirements.txt`** — open it and replace with:
```
fastapi
uvicorn
streamlit
langchain
langchain-community
langchain-ollama
langchain-huggingface
faiss-cpu
pypdf
python-dotenv
requests
python-multipart
sentence-transformers
langdetect
reportlab
beautifulsoup4
