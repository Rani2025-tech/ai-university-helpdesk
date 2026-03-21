from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from backend.utils import ensure_folders

app = FastAPI(
    title="AI University Helpdesk",
    description="RAG-based chatbot for university queries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_folders()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Welcome to AI University Helpdesk",
        "docs": "Visit /docs to see all API endpoints"
    }