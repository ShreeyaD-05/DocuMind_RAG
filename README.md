# DocuMind — AI Document Intelligence

DocuMind is a full-stack RAG (Retrieval-Augmented Generation) application that lets you upload documents and chat with them using AI. Powered by Groq LLM and local vector search via FAISS.

---

## Features

- Upload PDF, TXT, and MD files
- Ask questions and get answers grounded in your documents
- Summarize entire documents or specific sections
- Source citations with every answer
- Fast inference via Groq API (llama-3.3-70b-versatile)
- Local embeddings via sentence-transformers (no external embedding API needed)
- Fully containerized with Docker

---

## Tech Stack

| Layer | Technology |
|-----------|--------------------------------------|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | FastAPI, Python 3.11 |
| LLM | Groq API (llama-3.3-70b-versatile) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB | FAISS (local) |
| Container | Docker + Docker Compose |

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/documind.git
cd documind
```

### 2. Set up environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run

**Windows** — just double-click:
```
start_documind.bat
```

**Or manually:**
```bash
docker-compose up --build -d
```

Then open: [http://localhost:3000](http://localhost:3000)

> First run takes a few minutes to build. Every run after is fast (uses cached images).

---

## Project Structure

```
documind/
├── backend/
│   ├── app.py                  # FastAPI entry point
│   ├── routes/
│   │   ├── upload.py           # Document upload & indexing
│   │   └── query.py            # RAG query endpoint
│   ├── services/
│   │   ├── rag_pipeline.py     # Groq LLM integration
│   │   ├── embedding_service.py# Local sentence-transformers
│   │   ├── vector_store.py     # FAISS index management
│   │   └── document_loader.py  # PDF/TXT/MD parser
│   ├── utils/
│   │   └── text_splitter.py    # Chunking logic
│   ├── models/schemas.py       # Pydantic models
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/         # React UI components
│   │   ├── api/client.js       # Axios API client
│   │   └── App.jsx
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── start_documind.bat          # One-click Windows launcher
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|--------------|--------------------------|
| POST | `/upload` | Upload and index a document |
| POST | `/query` | Ask a question |
| GET | `/documents` | List indexed documents |
| GET | `/health` | Health check |
| DELETE | `/clear` | Clear all documents |

API docs available at: [http://localhost:8001/docs](http://localhost:8001/docs)

---

## Environment Variables

See `backend/.env.example` for all options.

| Variable | Description | Default |
|----------------------|--------------------------------------|-------------------------------|
| `GROQ_API_KEY` | Your Groq API key | required |
| `GROQ_MODEL` | Groq model to use | llama-3.3-70b-versatile |
| `EMBEDDING_MODEL` | HuggingFace embedding model | all-MiniLM-L6-v2 |
| `CHUNK_SIZE` | Text chunk size | 400 |
| `CHUNK_OVERLAP` | Chunk overlap | 50 |
| `TOP_K` | Top chunks to retrieve | 3 |

