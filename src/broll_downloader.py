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


def fetch_broll_clip(query: str, unique_tag: str = "", exclude_ids: set = None, orientation: str = "portrait") -> str:
    """Search and download a fresh tech video from Pexels with randomized page selection."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    if exclude_ids is None:
        exclude_ids = set()
    
    if not PEXELS_API_KEY:
        logger.warning("No PEXELS_API_KEY provided. Skipping b-roll download.")
        return ""

    # Clean query for Pexels search
    clean_query = query.replace('"', '').replace("'", "").strip()
    if len(clean_query.split()) > 4:
        clean_query = " ".join(clean_query.split()[:3])

    # Randomize page offset (1 to 6) for high variety
    random_page = random.randint(1, 6)
    headers = {"Authorization": PEXELS_API_KEY}
    url = (
        f"https://api.pexels.com/videos/search?"
        f"query={requests.utils.quote(clean_query)}&"
        f"orientation={orientation}&"
        f"per_page=8&"
        f"page={random_page}"
    )

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        videos = []
        if resp.status_code == 200:
            videos = resp.json().get("videos", [])

        # If empty on that page, try page 1
        if not videos:
            url_p1 = f"https://api.pexels.com/videos/search?query={requests.utils.quote(clean_query)}&orientation={orientation}&per_page=8&page=1"
            resp_p1 = requests.get(url_p1, headers=headers, timeout=12)
            if resp_p1.status_code == 200:
                videos = resp_p1.json().get("videos", [])

        if videos:
            # Filter out videos that are already used
            eligible_videos = [v for v in videos if str(v.get("id")) not in exclude_ids]
            if not eligible_videos:
                eligible_videos = videos

            selected_video = random.choice(eligible_videos)
            video_id = str(selected_video.get("id"))
            exclude_ids.add(video_id)
            target_path = os.path.join(CACHE_DIR, f"pex_{orientation}_{video_id}.mp4")

            # If already downloaded and valid, return it
            if os.path.exists(target_path) and os.path.getsize(target_path) > 100000:
                return target_path

            video_files = selected_video.get("video_files", [])
            if orientation == "landscape":
                # Prioritize horizontal 1080p/4K files (width >= 1920, height >= 1080)
                sorted_files = sorted(
                    video_files,
                    key=lambda f: (f.get("width", 0) >= 1920, f.get("width", 0) >= 1280),
                    reverse=True
                )
            else:
                # Prioritize vertical HD files (height >= 1280, width <= 1080)
                sorted_files = sorted(
                    video_files,
                    key=lambda f: (f.get("height", 0) >= 1280, f.get("width", 0) <= 1080),
                    reverse=True
                )
            if sorted_files:
                download_url = sorted_files[0]["link"]
                logger.info(f"Downloading fresh {orientation} B-roll for scene '{query}' (ID: {video_id})...")
                v_data = requests.get(download_url, timeout=35)
                if v_data.status_code == 200:
                    with open(target_path, "wb") as f:
                        f.write(v_data.content)
                    logger.info(f"Saved fresh B-roll to: {target_path} ({len(v_data.content)/(1024*1024):.1f} MB)")
                    return target_path
    except Exception as e:
        logger.warning(f"Error fetching Pexels video for '{query}': {e}")

    return ""


def get_curated_broll_clips(keywords: List[str] = None, count: int = 8, orientation: str = "portrait") -> List[str]:
    """Retrieve unique, non-repeating B-roll clips matched to the storyboard."""
    if not keywords or len(keywords) < 2:
        keywords = random.sample(FALLBACK_QUERIES, k=min(count, len(FALLBACK_QUERIES)))

    clips = []
    used_ids = set()

    for i, kw in enumerate(keywords):
        if len(clips) >= count:
            break
        clip_path = fetch_broll_clip(kw, unique_tag=str(i), exclude_ids=used_ids, orientation=orientation)
        if clip_path and os.path.exists(clip_path) and clip_path not in clips:
            clips.append(clip_path)

    # Fill any remaining slots with varied tech queries so zero clips repeat
    if len(clips) < count:
        remaining_queries = [q for q in FALLBACK_QUERIES if q not in keywords]
        random.shuffle(remaining_queries)
        for extra_kw in remaining_queries:
            if len(clips) >= count:
                break
            clip_path = fetch_broll_clip(extra_kw, unique_tag="extra", exclude_ids=used_ids, orientation=orientation)
            if clip_path and os.path.exists(clip_path) and clip_path not in clips:
                clips.append(clip_path)

    # If still need more, pick cached clips matching orientation
    if len(clips) < count and os.path.exists(CACHE_DIR):
        prefix = f"pex_{orientation}_" if orientation == "landscape" else "pex_"
        cached_files = [os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR) if f.startswith(prefix) and f.endswith(".mp4")]
        random.shuffle(cached_files)
        for c_file in cached_files:
            if len(clips) >= count:
                break
            if c_file not in clips and os.path.getsize(c_file) > 100000:
                clips.append(c_file)

    logger.info(f"Ready with {len(clips)} {orientation} B-roll clips (Zero Repeat).")
    return clips


if __name__ == "__main__":
    test_clips = get_curated_broll_clips(["quantum computing", "supercomputer lights"], count=2)
    print("Fresh clips downloaded:", test_clips)
