import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Load text
with open("data/flipkart_raw_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunking
def chunk_text(text, size=400):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

chunks = chunk_text(text)

with open("chunks/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

# Embedding
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

# Qdrant
client = QdrantClient(":memory:")

client.recreate_collection(
    collection_name="flipkart",
    vectors_config={"size": 384, "distance": "Cosine"}
)

points = [
    {"id": i, "vector": embeddings[i].tolist(), "payload": {"text": chunks[i]}}
    for i in range(len(chunks))
]

client.upsert("flipkart", points)

print("✅ Data embedded and stored in Qdrant")