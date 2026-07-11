from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(":memory:")

def retrieve_context(query, top_k=3):
    q_vector = model.encode(query).tolist()
    results = client.search("flipkart", q_vector, limit=top_k)
    return "\n".join([r.payload["text"] for r in results])

def generate_answer(query, context):
    prompt = f"""
You are a company information assistant.
Answer ONLY using the context below.
If not present, say "Information not available".

Context:
{context}

Question:
{query}
"""
    gemini = genai.GenerativeModel("gemini-pro")
    return gemini.generate_content(prompt).text