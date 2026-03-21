from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from backend.rag_pipeline import ingest_pdf, get_answer
from backend.utils import get_all_pdfs, faiss_index_exists, ensure_folders

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    language: str = "auto"

class AnswerResponse(BaseModel):
    answer: str
    source: str = "university documents"

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    ensure_folders()

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    save_path = os.path.join("data", file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks = ingest_pdf(save_path)
        return {
            "message": f"Successfully uploaded and ingested '{file.filename}'",
            "chunks_created": chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    if not faiss_index_exists():
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Please upload a university PDF first."
        )

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer = get_answer(request.question, request.language)
        return AnswerResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

@router.get("/documents")
def list_documents():
    pdfs = get_all_pdfs()
    filenames = [os.path.basename(p) for p in pdfs]
    return {
        "total": len(filenames),
        "documents": filenames
    }