from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import traceback  # NEW
from query import answer_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

@app.post("/api/")
def answer_api(request: QuestionRequest):
    try:
        result = answer_question(request.question, request.image)
        return {
            "answer": result["answer"],
            "links": result["links"]
        }
    except Exception as e:
        print("Error during question answering:", e)
        traceback.print_exc()  # 👈 this logs full traceback
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "TDS Virtual TA is running!"}
