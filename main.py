from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from query import answer_question

app = FastAPI()

# ✅ Enable CORS for all origins (or restrict to specific domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to ["https://your-frontend.com"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define request schema
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64-encoded image (optional)

# ✅ API route to answer questions
@app.post("/api/")
def answer_api(request: QuestionRequest):
    try:
        print("📩 Received request:", request.dict())  # Log input
        result = answer_question(request.question, request.image)
        print("✅ Answer generated:", result)  # Log output
        return {
            "answer": result["answer"],
            "links": result["links"]
        }
    except Exception as e:
        print("❌ Internal Server Error:", str(e))  # Log error
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Root route to verify deployment
@app.get("/")
def read_root():
    return {"message": "TDS Virtual TA is running!"}
