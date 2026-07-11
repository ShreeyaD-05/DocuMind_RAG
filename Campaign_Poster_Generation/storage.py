import json
import os
from datetime import datetime
from config import HISTORY_FILE, CAMPAIGNS_DIR


def _load_history() -> list:
    os.makedirs(CAMPAIGNS_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def _save_history(history: list):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_campaign(campaign: dict, image_prompt: str, image_path: str, style: str = "original") -> str:
    history = _load_history()

    # Group variations under same campaign_id
    campaign_id = campaign.get("campaign_id") or f"camp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    campaign["campaign_id"] = campaign_id

    entry = {
        "campaign_id": campaign_id,
        "timestamp": datetime.now().isoformat(),
        "style": style,
        "inputs": campaign,
        "generated_prompt": image_prompt,
        "image_path": image_path,
    }

    history.append(entry)
    _save_history(history)
    return campaign_id


def get_campaign_history() -> list:
    return _load_history()


def get_campaign_by_id(campaign_id: str) -> list:
    history = _load_history()
    return [e for e in history if e["campaign_id"] == campaign_id]
