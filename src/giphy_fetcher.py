"""
GIPHY Meme & Reaction Clip Engine (Fireship Style)
Fetches authentic, viral moving reaction video clips (.mp4) directly from GIPHY.
Provides 100% realistic pop-culture memes (Michael Jordan, Pedro Pascal, Leonardo DiCaprio, etc.)
"""

import os
import re
import json
import logging
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

GIPHY_API_KEY = os.getenv("GIPHY_API_KEY", "Y8PSKU5ua4A75zQRA6EHOZ9FcAySv9U6")
CACHE_DIR = "assets/broll_cache"

# Curated high-retention search terms mapped to situational keywords
SITUATIONAL_GIPHY_MAP = {
    "STOP": "michael jordan stop it",
    "BUG": "windows blue screen error",
    "CRASH": "screaming panic face",
    "FIRE": "this is fine dog fire",
    "LAUGH": "leonardo dicaprio laughing",
    "CRY": "pedro pascal crying laughing",
    "DISASTER": "disaster girl fire",
    "MONEY": "shut up and take my money",
    "SORRY": "sorry babe",
    "CONFUSED": "confused travolta looking around",
    "HACK": "typing fast hacker green screen",
    "FACEPALM": "facepalm annoyed captain picard",
    "DUMB": "bruh moment reaction",
    "PROMISE": "clown applying makeup",
    "ROBOT": "mark zuckerberg robot stare"
}


def search_giphy_meme_clip(
    query: str,
    api_key: Optional[str] = None,
    target_dir: str = CACHE_DIR
) -> Optional[str]:
    """
    Searches GIPHY API for real moving reaction clips and returns local MP4 path.
    """
    key = api_key or GIPHY_API_KEY or os.getenv("GIPHY_API_KEY", "")
    if not key:
        logger.warning("GIPHY_API_KEY is not set; skipping GIPHY search.")
        return None

    os.makedirs(target_dir, exist_ok=True)
    clean_query = query.strip()
    
    # Safe cache filename
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', clean_query.lower())[:35]
    cache_path = os.path.join(target_dir, f"giphy_{safe_name}.mp4")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 10000:
        logger.info(f"Using cached GIPHY meme clip: {cache_path}")
        return cache_path

    url = (
        f"https://api.giphy.com/v1/gifs/search?"
        f"api_key={key}&q={urllib.parse.quote(clean_query)}&limit=5&rating=pg-13"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("data", [])
        if not items:
            logger.warning(f"No GIPHY memes found for query: '{clean_query}'")
            return None

        # Pick first item that has a working MP4
        mp4_url = None
        for item in items:
            imgs = item.get("images", {})
            # Prefer downsized or original mp4
            candidates = [
                imgs.get("downsized_small", {}).get("mp4"),
                imgs.get("original", {}).get("mp4"),
                imgs.get("fixed_height", {}).get("mp4"),
                imgs.get("looping", {}).get("mp4")
            ]
            for c in candidates:
                if c and c.startswith("http"):
                    mp4_url = c
                    break
            if mp4_url:
                break

        if not mp4_url:
            logger.warning(f"No MP4 found in GIPHY response for '{clean_query}'")
            return None

        logger.info(f"Downloading GIPHY MP4 for '{clean_query}' from: {mp4_url}")
        img_req = urllib.request.Request(mp4_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(img_req, timeout=12) as r, open(cache_path, "wb") as f:
            f.write(r.read())

        if os.path.exists(cache_path) and os.path.getsize(cache_path) > 5000:
            logger.info(f"Successfully saved GIPHY meme to: {cache_path} ({os.path.getsize(cache_path)} bytes)")
            return cache_path

    except Exception as e:
        logger.warning(f"Error fetching GIPHY meme for '{clean_query}': {e}")

    return None


def get_situational_giphy_query(text: str) -> str:
    """Map script context to the best viral real human reaction query."""
    t_up = text.upper()
    for trigger, query in SITUATIONAL_GIPHY_MAP.items():
        if trigger in t_up:
            return query
    
    # Generic viral fallback
    return "michael jordan stop it"
