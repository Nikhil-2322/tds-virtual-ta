import json
from pathlib import Path

# === CONFIGURATION ===
METADATA_FILE = "metadata.json"
MARKDOWN_DIR = "tds_pages_md"  # directory where .md files are stored
OUTPUT_FILE = "embedding_md_data.json"
CHUNK_SIZE = 500  # size of each text chunk (in characters)

# === LOAD METADATA ===
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# === CHUNKING FUNCTION ===
def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i + size] for i in range(0, len(text), size)]

# === PROCESS EACH MARKDOWN FILE ===
output_data = []

for entry in metadata:
    filename = entry["filename"]
    original_url = entry["original_url"]

    filepath = Path(MARKDOWN_DIR) / filename
    if not filepath.exists():
        print(f"❌ File not found: {filename}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_text(content)
    for chunk in chunks:
        output_data.append({
            "chunk": chunk.strip(),
            "original_url": original_url
        })

# === WRITE OUTPUT JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"✅ Created {OUTPUT_FILE} with {len(output_data)} chunks.")
