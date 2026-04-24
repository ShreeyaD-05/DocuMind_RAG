FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install torch CPU-only first (small ~200MB vs 530MB GPU version)
RUN pip install --no-cache-dir torch==2.3.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

# Install remaining deps (torch already present, won't re-download)
RUN pip install --no-cache-dir \
    fastapi==0.111.0 \
    "uvicorn[standard]==0.29.0" \
    python-multipart==0.0.9 \
    python-dotenv==1.0.1 \
    pydantic==2.7.1 \
    pypdf==4.2.0 \
    faiss-cpu==1.8.0 \
    "numpy==1.26.4" \
    "openai>=1.52.0" \
    "sentence-transformers==2.7.0"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
