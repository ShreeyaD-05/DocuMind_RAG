import requests
import os
from config import (
    OPENROUTER_API_KEY, OPENROUTER_BASE_URL, TEXT_MODEL, CAMPAIGNS_DIR
)

OR_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://campaign-poster-gen.local",
    "X-Title": "Campaign Poster Generator",
}


def build_image_prompt(campaign: dict, style_modifier: str = "") -> str:
    """Use free LLM via OpenRouter to build a rich image generation prompt."""
    style_note = f"\nAdditional style direction: {style_modifier}" if style_modifier else ""

    user_message = f"""You are an expert marketing designer and prompt engineer.
Convert the following restaurant campaign details into a detailed, vivid image generation prompt for a marketing poster.

Campaign Details:
- Festival/Occasion: {campaign['festival']}
- Offer/Campaign: {campaign['offer']}
- Target Audience: {campaign['target_audience']}
- Duration: {campaign['duration']} days (starting {campaign['start_date']})
- Restaurant Name: {campaign['restaurant_name']}{style_note}

Rules:
- Output ONLY the image prompt, no explanation
- Make it visually descriptive: lighting, colors, composition, mood, food elements
- Include the offer text naturally in the scene description
- Keep it under 200 words
- Style: professional marketing poster, high quality, photorealistic"""

    payload = {
        "model": TEXT_MODEL,
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.8,
    }

    response = requests.post(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        headers=OR_HEADERS,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def generate_poster(image_prompt: str, filename: str) -> str:
    """Generate image via Pollinations.ai (completely free, no API key needed)."""
    os.makedirs(CAMPAIGNS_DIR, exist_ok=True)
    output_path = os.path.join(CAMPAIGNS_DIR, filename)

    # Pollinations free image API — no auth required
    import urllib.parse
    encoded = urllib.parse.quote(image_prompt[:500])
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true"

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path
