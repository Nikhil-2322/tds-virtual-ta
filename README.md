<<<<<<< HEAD
# tds-virtual-ta
TDS Virtual TA is a semantic search assistant for IITM's Tools for Data Science course. It uses OCR, FAISS, and AIPipe embeddings to answer queries from scraped content. Supports text/image input via API and integrates with Promptfoo for evaluation.
=======

# 🧠 TDS Virtual Teaching Assistant (`tds-virtual-ta`)

## 📌 Introduction

**TDS Virtual TA** is an intelligent question-answering assistant built specifically for the *Tools for Data Science (TDS)* course offered by IITM. This assistant is designed to help students by answering questions based on the course's official discussion forum and lecture notes. It understands natural language queries and can even extract and interpret text from screenshots.

This project uses:
- ✅ **Semantic search with FAISS**
- ✅ **AI Pipe for state-of-the-art text embeddings**
- ✅ **Tesseract OCR** for image understanding
- ✅ **FastAPI** for a lightweight REST API backend

It supports both **text-based** and **image-based** queries.

---

## 🕸️ 1. Scraping the Knowledge Base

We collect content from two trusted sources:

### a. Discourse Forum

```bash
python discourse_downloader_single.py
```
- Source: [TDS Discourse Forum](https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34)  
- Output: `discourse_posts.json`

### b. Markdown Pages (S. Anand)

```bash
python website_downloader_full.py
```
- Source: [S. Anand's TDS Notes](https://tds.s-anand.net/#/2025-01/)
- Output: `metadata.json`

---

## 🧠 2. Embedding the Content

Using **AI Pipe**, we convert text to vector embeddings.

### a. Discourse Embeddings

```bash
python embedding_discourse.py
```
➡️ Output: `embedding_discourse_data.json`

### b. Markdown Embeddings

```bash
python embedding_metadata.py
```
➡️ Output: `embedding_md_data.json`

### c. Combine Embeddings

```bash
python combine_embeddings.py
```
➡️ Output: `combined_embedding_data.json`

---

## 🧱 3. FAISS Index Building

```bash
python build_faiss_index.py
```
- Loads all embeddings
- Builds a FAISS similarity index
- Output: `faiss_index.idx`

---

## 🔍 4. Core Search Logic (`query.py`)

- Extracts text via OCR from base64 images (if present)
- Combines question + OCR result
- Gets vector embeddings using AI Pipe
- Performs semantic similarity search
- Returns best matched text and source links

---

## 🚀 5. Running the API (`main.py`)

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### POST `/api/`

#### JSON Payload
```json
{
  "question": "What is the cost of TTS?",
  "image": "<optional base64 image string>"
}
```

---

## 🧪 6. How to Test

### a. Text Query

```bash
curl -X POST http://0.0.0.0:8000/api/   -H "Content-Type: application/json"   -d '{"question": "What is the cost of TTS?"}'
```

### b. With Screenshot Image (OCR)

```bash
curl -X POST http://0.0.0.0:8000/api/   -H "Content-Type: application/json"   -d '{"question": "What does this say?", "image": "'$(base64 -w0 image.png)'"}'
```

---

## 📊 7. Evaluate Your Application with Promptfoo

### Step 1: Set API URL

Open the file:

```
project-tds-virtual-ta-promptfoo.yaml
```

Replace the line:

```yaml
providers[0].config.url: "http://localhost:8000/api/"
```

...with your actual URL if needed.

### Step 2: Run the Evaluation

```bash
npx -y promptfoo eval --config project-tds-virtual-ta-promptfoo.yaml
```

Promptfoo will test realistic student questions and check your API’s answers.

---

## 📦 Project Summary

| Task                        | Output File                           |
|-----------------------------|----------------------------------------|
| Discourse scraping          | `discourse_posts.json`                 |
| Markdown scraping           | `metadata.json`                        |
| Embedding generation        | `embedding_*.json`                     |
| Combined embeddings         | `combined_embedding_data.json`         |
| FAISS index                 | `faiss_index.idx`                      |
| Semantic QA logic           | `query.py`                             |
| API endpoint                | `main.py`                              |
| API tests                   | `test.yaml`                            |
| Promptfoo eval config       | `project-tds-virtual-ta-promptfoo.yaml`|

---

## 🛠 Requirements

```bash
pip install -r requirements.txt
```

OCR needs Tesseract:

```bash
sudo apt install tesseract-ocr
```

---

## ✅ Example Output

```json
{
  "answer": "📌 Context:
...
❓ Your Question:
What is the cost of TTS?

💡 This is a mock answer...",
  "links": [
    {"url": "https://tds.s-anand.net/#/llm-speech", "text": "Source"},
    ...
  ]
}
```
## 👥 Credits

Developed by: *Nikhil Yadav* (IIT Madras - B.S. Data Science, IIIT Kota - B.Tech CSE)

Powered by:

- [FastAPI](https://fastapi.tiangolo.com/)
- [SentenceTransformers](https://www.sbert.net/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [AIPipe Proxy](https://aipipe.org)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Discourse](https://discourse.onlinedegree.iitm.ac.in)
>>>>>>> 6f6db1e (Initial commit: TDS Virtual TA with OCR and semantic search)
