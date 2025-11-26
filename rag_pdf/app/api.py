from fastapi import FastAPI, UploadFile
from app.pdf_processor import process_pdf
from app.vector_store import create_vector_store
from app.rag_pipeline import get_rag_pipeline
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
print("GROQ KEY CHECK:", os.getenv("GROQ_API_KEY"))


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    pdf_id = str(uuid.uuid4())
    pdf_path = f"{UPLOAD_DIR}/{pdf_id}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    chunks = process_pdf(pdf_path)
    create_vector_store(chunks, pdf_id)

    return {"message": "PDF processed successfully", "pdf_id": pdf_id}

from pydantic import BaseModel

class AskRequest(BaseModel):
    pdf_id: str
    question: str

@app.post("/ask-pdf")
async def ask_pdf(req: AskRequest):
    chain = get_rag_pipeline(req.pdf_id)
    answer = chain.invoke({"question": req.question})   
    return {"answer": answer}


