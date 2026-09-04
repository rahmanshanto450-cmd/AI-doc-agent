
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import FastAPI, File, UploadFile
from rag.ingest import ingest_pdf
from rag.pipeline import ask_question

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = FastAPI(
    title="AI Doc Agent",
    description="AI-powered document question answering API",
    version="1.0.0",
)

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Question to ask about the document",
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask")
def ask(request: QuestionRequest):
    result = ask_question(request.question)

    return {
        "answer": result["answer"],
        "sources": [
            {
                "page": document.metadata.get("page_label", "Unknown"),
                "content": document.page_content,
            }
            for document in result["sources"]
        ],
   }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF and add its contents to the vector database.
    """

    file_path = DATA_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    ingest_pdf(str(file_path))

    return {
        "message": "PDF uploaded and processed successfully",
        "filename": file.filename,
    }