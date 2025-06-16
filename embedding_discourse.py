import json
from collections import defaultdict
from datetime import datetime

# === CONFIGURATION ===
INPUT_FILE = "discourse_posts.json"
OUTPUT_FILE = "embedding_discourse_data.json"
CHUNK_SIZE = 500  # characters per chunk

# === CHUNKING FUNCTION ===
def chunk_text(text, size=CHUNK_SIZE):
    return [text[i:i + size] for i in range(0, len(text), size)]

# === LOAD POSTS ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    posts = json.load(f)

# === GROUP POSTS BY TOPIC ===
topics = defaultdict(list)
for post in posts:
    topics[post["topic_id"]].append(post)

# === PROCESS EACH TOPIC ===
output_data = []

for topic_id, topic_posts in topics.items():
    topic_posts.sort(key=lambda x: x["post_number"])
    combined_text = "\n\n".join(post["content"].strip() for post in topic_posts if post["content"].strip())
    post_numbers = [post["post_number"] for post in topic_posts]
    root_post_number = min(post_numbers)
    topic_title = topic_posts[0]["topic_title"]
    original_url = topic_posts[0]["url"]
    downloaded_at = max(post["updated_at"] for post in topic_posts)

    filename = f"topic_{topic_id}.json"

    chunks = chunk_text(combined_text)
    for chunk in chunks:
        output_data.append({
            "topic_id": topic_id,
            "topic_title": topic_title,
            "root_post_number": root_post_number,
            "post_numbers": post_numbers,
            "combined_text": combined_text,
            "chunk": chunk.strip(),
            "title": topic_title,
            "filename": filename,
            "original_url": original_url,
            "downloaded_at": downloaded_at
        })

# === WRITE OUTPUT JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"✅ Created {OUTPUT_FILE} with {len(output_data)} chunks.")
