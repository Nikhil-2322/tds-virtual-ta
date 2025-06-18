import json
import faiss
import numpy as np
import pickle
import requests

# === CONFIGURATION ===
AIPIPE_TOKEN = "<your-aipipe-token>"
AIPIPE_EMBEDDING_ENDPOINT = "<your-aipipe-embedding-url>"
EMBEDDING_MODEL = "text-embedding-3-small"

INPUT_JSON = "combined_embedding_data.json"
OUTPUT_INDEX = "faiss_index.idx"

# === Helper: Get embedding from AI Pipe ===
def get_embedding(text):
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
        raise Exception(f"Error code: {response.status_code} - {response.json()}")
    
    return response.json()["data"][0]["embedding"]

# === Load JSON ===
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# === Build FAISS index ===
embeddings = []
id_to_metadata = {}

print("🔄 Generating embeddings...")
for i, item in enumerate(data):
    try:
        emb = get_embedding(item["chunk"])
        embeddings.append(emb)
        id_to_metadata[i] = item
        print(f"✅ Embedded chunk {i+1}/{len(data)}")
    except Exception as e:
        print(f"❌ Error on item {i}: {e}")
        continue

# Convert to float32 matrix
embedding_matrix = np.array(embeddings).astype("float32")

# Create FAISS index
dim = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dim)
id_index = faiss.IndexIDMap(index)

ids = np.array(list(id_to_metadata.keys())).astype("int64")
id_index.add_with_ids(embedding_matrix, ids)

# Save index and metadata
faiss_binary = faiss.serialize_index(id_index)
metadata_binary = pickle.dumps(id_to_metadata)

with open(OUTPUT_INDEX, "wb") as f:
    pickle.dump({
        "faiss_index": faiss_binary,
        "metadata": metadata_binary
    }, f)

print(f"\n✅ FAISS index saved to `{OUTPUT_INDEX}` with {len(embeddings)} embeddings.")
