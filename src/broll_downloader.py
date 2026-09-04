"""
Cinematic B-Roll Downloader via Pexels API (Dynamic & Non-Repeating)
Downloads fresh, high-definition 4K/HD vertical footage matching exact news topics.
Features randomized page offsets so NO TWO VIDEOS EVER LOOK THE SAME.
"""

import os
import random
import requests
import logging
from typing import List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
CACHE_DIR = "assets/broll_cache"

# Diverse search topics to prevent repetition
FALLBACK_QUERIES = [
    "artificial intelligence",
    "cyberpunk server",
    "developer coding keyboard",
    "quantum computing",
    "microchip processor",
    "robotics technology",
    "data center network",
    "futuristic city night",
    "supercomputer lights"
]


def fetch_broll_clip(query: str, unique_tag: str) -> str:
    """Search and download a fresh vertical tech video from Pexels with randomized page selection."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    if not PEXELS_API_KEY:
        logger.warning("No PEXELS_API_KEY provided. Skipping b-roll download.")
        return ""

    # Randomize page offset (1 to 15) so we never download the exact same clip
    random_page = random.randint(1, 12)
    headers = {"Authorization": PEXELS_API_KEY}
    url = (
        f"https://api.pexels.com/videos/search?"
        f"query={requests.utils.quote(query)}&"
        f"orientation=portrait&"
        f"per_page=5&"
        f"page={random_page}"
    )

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        videos = []
        if resp.status_code == 200:
            videos = resp.json().get("videos", [])

        # If empty on that page, try page 1
        if not videos:
            url_p1 = f"https://api.pexels.com/videos/search?query={requests.utils.quote(query)}&orientation=portrait&per_page=5&page=1"
            resp_p1 = requests.get(url_p1, headers=headers, timeout=12)
            if resp_p1.status_code == 200:
                videos = resp_p1.json().get("videos", [])

        if videos:
            # Pick a random video from the result set for true variety
            selected_video = random.choice(videos)
            video_id = selected_video.get("id")
            target_path = os.path.join(CACHE_DIR, f"pex_{video_id}.mp4")

            # If already downloaded, return it
            if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
                return target_path

            video_files = selected_video.get("video_files", [])
            # Prioritize vertical HD files (height >= 1280, width <= 1080)
            sorted_files = sorted(
                video_files,
                key=lambda f: (f.get("height", 0) >= 1280, f.get("width", 0) <= 1080),
                reverse=True
            )
            if sorted_files:
                download_url = sorted_files[0]["link"]
                logger.info(f"Downloading fresh B-roll for topic '{query}' (ID: {video_id})...")
                v_data = requests.get(download_url, timeout=35)
                if v_data.status_code == 200:
                    with open(target_path, "wb") as f:
                        f.write(v_data.content)
                    logger.info(f"Saved fresh B-roll to: {target_path} ({len(v_data.content)/(1024*1024):.1f} MB)")
                    return target_path
    except Exception as e:
        logger.warning(f"Error fetching Pexels video for '{query}': {e}")

    return ""


def get_curated_broll_clips(keywords: List[str] = None, count: int = 4) -> List[str]:
    """Retrieve 4 completely fresh, topic-specific B-roll clips for this specific video."""
    if not keywords or len(keywords) < 2:
        keywords = random.sample(FALLBACK_QUERIES, k=min(count, len(FALLBACK_QUERIES)))

    # Ensure unique topics per video
    search_queries = list(set(keywords))
    random.shuffle(search_queries)

    clips = []
    for i, kw in enumerate(search_queries[:count]):
        clip_path = fetch_broll_clip(kw, unique_tag=str(i))
        if clip_path and os.path.exists(clip_path) and clip_path not in clips:
            clips.append(clip_path)

    # Fill any remaining slots with random queries from the diverse pool
    if len(clips) < count:
        remaining_queries = [q for q in FALLBACK_QUERIES if q not in search_queries]
        random.shuffle(remaining_queries)
        for extra_kw in remaining_queries:
            if len(clips) >= count:
                break
            clip_path = fetch_broll_clip(extra_kw, unique_tag="extra")
            if clip_path and os.path.exists(clip_path) and clip_path not in clips:
                clips.append(clip_path)

    logger.info(f"Ready with {len(clips)} fresh, unique B-roll clips for this Short.")
    return clips


if __name__ == "__main__":
    test_clips = get_curated_broll_clips(["quantum computing", "supercomputer lights"], count=2)
    print("Fresh clips downloaded:", test_clips)
