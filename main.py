from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from query import answer_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image

@app.post("/api/")
def answer_api(request: QuestionRequest):
    try:
        result = answer_question(request.question, request.image)
        return {
            "answer": result["answer"],
            "links": result["links"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "TDS Virtual TA is running!"}
