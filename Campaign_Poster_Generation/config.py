import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# LLM for prompt engineering (free via OpenRouter)
TEXT_MODEL = "google/gemma-4-26b-a4b-it:free"

# Image generation — uses Hugging Face free Inference API
HF_IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell"

# Output
CAMPAIGNS_DIR = "campaigns"
HISTORY_FILE = os.path.join(CAMPAIGNS_DIR, "history.json")

# Regeneration style modifiers
STYLE_MODIFIERS = {
    "1": ("premium", "luxury aesthetic, gold accents, elegant typography, dark rich background, high-end feel"),
    "2": ("festive", "vibrant festive decorations, bright colors, celebratory elements, traditional motifs"),
    "3": ("minimal", "clean minimalist design, white space, simple typography, subtle color palette"),
    "4": ("modern", "contemporary design, bold geometric shapes, trendy color gradients, sleek layout"),
    "5": ("warm", "warm cozy lighting, earthy tones, inviting atmosphere, soft textures"),
}
