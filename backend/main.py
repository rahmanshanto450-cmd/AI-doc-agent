
from fastapi import FastAPI
from pydantic import BaseModel

from rag.pipeline import ask_question


app = FastAPI(
    title="AI Doc Agent",
    description="AI-powered document question answering API",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str


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