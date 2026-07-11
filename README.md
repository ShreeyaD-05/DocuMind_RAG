# DocuMind RAG — AI Projects Collection

A collection of two production-ready Generative AI projects built with Python and Streamlit:

1. **Campaign Poster Generator** — AI-powered marketing poster creation for restaurants
2. **Company RAG Chatbot** — Retrieval-Augmented Generation chatbot for company knowledge

---

## Table of Contents

- [Project Overview](#project-overview)
- [Campaign Poster Generator](#-campaign-poster-generator)
  - [Architecture](#architecture)
  - [How It Works](#how-it-works)
  - [Setup & Run](#setup--run)
- [Company RAG Chatbot](#-company-rag-chatbot)
  - [Architecture](#architecture-1)
  - [How It Works](#how-it-works-1)
  - [Setup & Run](#setup--run-1)
- [Tech Stack](#tech-stack)

---

## Project Overview

```
DocuMind_RAG/
├── Campaign_Poster_Generation/     # Project 1: Poster Generator
│   ├── main.py                     # Streamlit UI
│   ├── generator.py                # LLM prompt builder + image generator
│   ├── config.py                   # API keys, models, style configs
│   ├── storage.py                  # Campaign history (JSON)
│   ├── requirements.txt
│   └── campaigns/                  # Generated posters saved here
│
└── company_rag_chatbot/            # Project 2: RAG Chatbot
    ├── app.py                      # Streamlit UI
    ├── scrape.py                   # Web scraper (BeautifulSoup)
    ├── embed_store.py              # Embedding + Qdrant vector store
    ├── rag_pipeline.py             # Retrieval + Gemini answer generation
    ├── requirements.txt
    ├── data/                       # Raw scraped text
    └── chunks/                     # Chunked JSON for embedding
```

---

## 🎨 Campaign Poster Generator

### Architecture

```
User Input (Streamlit UI)
        │
        ▼
┌───────────────────┐
│   config.py       │  ← API keys, style modifiers, model names
└───────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│   generator.py — build_image_prompt() │
│                                       │
│   Sends campaign details to           │
│   OpenRouter API (Gemma 4 LLM)        │
│   → Returns rich image prompt         │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────┐
│   generator.py — generate_poster()    │
│                                       │
│   Sends prompt to Pollinations.ai     │
│   (free, no API key needed)           │
│   → Downloads 1024×1024 PNG poster    │
└───────────────────────────────────────┘
        │
        ▼
┌───────────────────┐
│   storage.py      │  ← Saves campaign + prompt + image path to history.json
└───────────────────┘
        │
        ▼
   Preview in UI + Campaign History Panel
```

### How It Works

| Step | What Happens |
|------|-------------|
| 1 | User fills in restaurant name, festival, offer, audience, duration, start date |
| 2 | Selects a poster style (Original / Premium / Festive / Minimal / Modern / Warm) |
| 3 | Gemma 4 LLM (via OpenRouter) converts campaign details into a rich image prompt |
| 4 | Pollinations.ai generates a 1024×1024 marketing poster from the prompt |
| 5 | Poster is saved to `campaigns/` folder and shown in the UI |
| 6 | All campaigns are stored in `campaigns/history.json` with unique campaign IDs |

**Style Modifiers:**

| Style | Description |
|-------|-------------|
| Original | No modifier — pure LLM interpretation |
| Premium | Luxury aesthetic, gold accents, dark rich background |
| Festive | Vibrant colors, celebratory elements, traditional motifs |
| Minimal | Clean design, white space, subtle color palette |
| Modern | Bold geometric shapes, trendy gradients, sleek layout |
| Warm | Cozy lighting, earthy tones, inviting atmosphere |

### Setup & Run

#### Prerequisites
- Python 3.9+
- An [OpenRouter](https://openrouter.ai/) API key (free tier available)

#### Steps

```bash
# 1. Navigate to the project folder
cd Campaign_Poster_Generation

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install streamlit  # if not already installed

# 4. Create your .env file
```

Create a `.env` file in `Campaign_Poster_Generation/`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

```bash
# 5. Run the app
streamlit run main.py
```

Open your browser at `http://localhost:8501`

#### Get a free OpenRouter API key
1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to **Keys** → **Create Key**
4. Paste it in your `.env` file

---

## 🛒 Company RAG Chatbot

### Architecture

```
                    ┌─────────────────────────────┐
                    │        scrape.py             │
                    │  Scrapes Flipkart website    │
                    │  → saves flipkart_raw_text   │
                    └─────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────┐
                    │       embed_store.py         │
                    │                             │
                    │  1. Chunks text (400 words) │
                    │  2. Encodes with            │
                    │     all-MiniLM-L6-v2        │
                    │  3. Stores 384-dim vectors  │
                    │     in Qdrant (in-memory)   │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │       rag_pipeline.py        │
                    │                             │
                    │  retrieve_context():        │
                    │  • Embeds user query        │
                    │  • Cosine similarity search │
                    │  • Returns top-3 chunks     │
                    │                             │
                    │  generate_answer():         │
                    │  • Builds prompt with       │
                    │    retrieved context        │
                    │  • Calls Gemini Pro API     │
                    │  • Returns grounded answer  │
                    └─────────────┬───────────────┘
                                  │
                    ┌─────────────▼───────────────┐
                    │           app.py             │
                    │      Streamlit Chat UI       │
                    └─────────────────────────────┘
```

### How It Works

| Step | What Happens |
|------|-------------|
| 1 | `scrape.py` crawls Flipkart pages and saves raw text to `data/flipkart_raw_text.txt` |
| 2 | `embed_store.py` splits text into 400-word chunks, embeds them using `all-MiniLM-L6-v2`, and loads them into an in-memory Qdrant vector database |
| 3 | User asks a question in the Streamlit UI |
| 4 | The query is embedded and the top 3 most similar chunks are retrieved from Qdrant using cosine similarity |
| 5 | Retrieved chunks are injected into a prompt and sent to Gemini Pro |
| 6 | Gemini answers strictly from the provided context — no hallucination |

**RAG Flow:**
```
User Query → Embedding → Vector Search (Qdrant) → Top-K Chunks → Gemini Pro → Answer
```

### Setup & Run

#### Prerequisites
- Python 3.9+
- A [Google Gemini](https://aistudio.google.com/) API key (free tier available)

#### Steps

```bash
# 1. Navigate to the project folder
cd company_rag_chatbot

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

#### 4. Add your Gemini API key

Open `rag_pipeline.py` and replace:
```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```
with your actual key:
```python
genai.configure(api_key="your_actual_gemini_api_key")
```

#### Get a free Gemini API key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **Get API Key** → **Create API Key**

#### 5. Scrape the data

```bash
python scrape.py
```

This saves raw text to `data/flipkart_raw_text.txt`.

#### 6. Embed and store in Qdrant

```bash
python embed_store.py
```

This chunks the text, creates embeddings, and loads them into the in-memory vector store.

#### 7. Run the chatbot

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

> **Note:** Since Qdrant runs in-memory, you must run `embed_store.py` every time before starting the app. For persistence, switch to a local Qdrant instance.

---

## Tech Stack

| Technology | Used In | Purpose |
|------------|---------|---------|
| Streamlit | Both | Web UI framework |
| OpenRouter API | Campaign Poster | LLM gateway (Gemma 4) |
| Pollinations.ai | Campaign Poster | Free image generation |
| Google Gemini Pro | RAG Chatbot | Answer generation |
| Sentence Transformers | RAG Chatbot | Text embeddings (all-MiniLM-L6-v2) |
| Qdrant | RAG Chatbot | Vector similarity search |
| BeautifulSoup | RAG Chatbot | Web scraping |
| python-dotenv | Campaign Poster | Environment variable management |

---

## Notes

- The `.env` file is excluded from this repo — never commit API keys
- The `venv/` folders are excluded — always create your own virtual environment
- Campaign posters are saved locally in `campaigns/` and not tracked in git
- The RAG chatbot uses an in-memory vector store — re-run `embed_store.py` on each session start
