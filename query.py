import pickle
import faiss
import numpy as np
import requests
from PIL import Image
import pytesseract
import io
import base64
import os
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()
AIPIPE_TOKEN = os.getenv("AIPIPE_API_KEY")
AIPIPE_EMBEDDING_ENDPOINT = os.getenv("AIPIPE_API_URL", "https://aipipe.org/openai/v1/embeddings")
AIPIPE_COMPLETION_ENDPOINT = os.getenv("AIPIPE_COMPLETION_URL", "https://aipipe.org/openai/v1/chat/completions")
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
INDEX_FILE = "faiss_index.idx"

# === Load FAISS index and metadata ===
def load_index_and_metadata(filepath):
    with open(filepath, "rb") as f:
        saved = pickle.load(f)
    index = faiss.deserialize_index(saved["faiss_index"])
    metadata = pickle.loads(saved["metadata"])
    return index, metadata

index, metadata = load_index_and_metadata(INDEX_FILE)

# === OCR extraction ===
def extract_text_from_base64_image(base64_str: str) -> str:
    try:
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return ""

# === Get embedding from AI Pipe ===
def get_embedding(text: str):
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text.replace("\n", " ")
    }
    response = requests.post(AIPIPE_EMBEDDING_ENDPOINT, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"AI Pipe Error {response.status_code}: {response.text}")
    
    return np.array(response.json()["data"][0]["embedding"], dtype="float32")

# === Semantic search ===
def retrieve(query: str, index, metadata: dict, k=5):
    query_vec = get_embedding(query).reshape(1, -1)
    D, I = index.search(query_vec, k)
    return [metadata[idx] for idx in I[0] if idx in metadata]

# === Generate LLM-based response ===
def generate_llm_answer(context_str: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {AIPIPE_TOKEN}",
        "Content-Type": "application/json"
    }
    prompt = f"""You are a helpful assistant for the TDS course.
Answer the question using the provided context. If the answer is not available, say you don't know.

Context:
{context_str}

Question:
{question}
"""
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(AIPIPE_COMPLETION_ENDPOINT, headers=headers, json=payload)

    if response.status_code != 200:
        return "⚠️ Sorry, something went wrong while generating the answer."

    return response.json()["choices"][0]["message"]["content"].strip()

# === Final answer logic ===
def answer_question(question: str, image_base64: str = None):
    if image_base64:
        ocr_text = extract_text_from_base64_image(image_base64)
        if ocr_text:
            print(f"🖼️ OCR extracted: {ocr_text}")
            question += "\n" + ocr_text

    results = retrieve(question, index, metadata)
    if not results:
        return {
            "answer": "⚠️ Sorry, I couldn't find relevant information.",
            "links": []
        }

    context_chunks = []
    links = []

    for r in results:
        text = r.get("combined_text") or r.get("chunk") or ""
        context_chunks.append(text.strip())
        if r.get("original_url"):
            links.append({
                "url": r["original_url"],
                "text": r.get("title", "Source")
            })

    context_str = "\n---\n".join(context_chunks)
    llm_answer = generate_llm_answer(context_str, question)

    return {
        "answer": llm_answer,
        "links": links
    }
