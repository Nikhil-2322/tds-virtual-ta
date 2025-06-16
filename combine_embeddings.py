# combine_embeddings.py
import json

md_file = "embedding_md_data.json"
discourse_file = "embedding_discourse_data.json"
output_file = "combined_embedding_data.json"

# Load both
with open(md_file, "r", encoding="utf-8") as f:
    md_data = json.load(f)

with open(discourse_file, "r", encoding="utf-8") as f:
    discourse_data = json.load(f)

# Tag source
for item in md_data:
    item["source"] = "markdown"

for item in discourse_data:
    item["source"] = "discourse"

# Combine
combined = md_data + discourse_data

# Write to output
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined, f, indent=2, ensure_ascii=False)

print(f"✅ Combined {len(md_data)} markdown + {len(discourse_data)} discourse chunks into {output_file}")
