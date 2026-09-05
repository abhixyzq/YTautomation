"""
Automated Instagram Reels Publisher (Meta Instagram Graph API)
Publishes 1080x1920 vertical video directly as Instagram Reels.
Supports direct binary streaming via Meta Resumable Upload Protocol (Zero public hosting needed).
"""

import os
import sys
import time
import json
import logging
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "").strip()
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "").strip()
GRAPH_API_VERSION = "v21.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def is_instagram_configured() -> bool:
    """Check if valid Instagram Graph API credentials exist in environment."""
    return bool(INSTAGRAM_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN)


def format_instagram_caption(
    title: str,
    description: str = "",
    tags: Optional[List[str]] = None,
    comment_prompt: Optional[str] = None
) -> str:
    """Formats high-converting viral Instagram caption with emojis and trending tech hashtags."""
    clean_title = title.replace("#Shorts", "").replace("#shorts", "").replace("#Tech", "").replace("#AI", "").strip()
    prompt = comment_prompt or "What's your take on this? Drop your thoughts below! 👇"
    
    default_ig_tags = [
        "#tech", "#technology", "#ai", "#artificialintelligence", 
        "#coding", "#developer", "#softwareengineer", "#programming", 
        "#webdevelopment", "#technews", "#viralreels", "#reelsindia", 
        "#techreels", "#siliconvalley", "#computerscience"
    ]
    
    custom_tags = []
    if tags:
        for t in tags:
            tag_clean = t.replace("#", "").strip().lower()
            if tag_clean and f"#{tag_clean}" not in default_ig_tags:
                custom_tags.append(f"#{tag_clean}")
                
    all_hashtags = " ".join((custom_tags[:8] + default_ig_tags)[:22])

    caption = f"""{clean_title} 🚀
.
💬 Question of the day:
{prompt}
.
{description.strip() if description else ''}
.
Follow for daily high-octane tech & AI intelligence ⚡
.
{all_hashtags}"""

    return caption.strip()


def upload_reel_to_instagram(
    video_path: str,
    title: str,
    description: str = "",
    tags: Optional[List[str]] = None,
    comment_text: Optional[str] = None
) -> Optional[str]:
    """
    Publishes an .mp4 video file directly to Instagram Reels using Meta's official Graph API.
    Uses Meta Resumable Upload protocol (streams binary bytes directly to Meta servers).
    """
    if not is_instagram_configured():
        logger.info("Instagram credentials not configured. Skipping Instagram upload.")
        logger.info("(To enable 100% automated Instagram Reels: Add INSTAGRAM_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN to .env)")
        return None

    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    file_size = os.path.getsize(video_path)
    logger.info(f">>> [INSTAGRAM] Preparing to publish Reel: {os.path.basename(video_path)} ({file_size / (1024*1024):.2f} MB)...")

    caption = format_instagram_caption(title, description, tags, comment_text)

    # -----------------------------------------------------------------
    # STEP 1: Initialize Resumable Container on Instagram Graph API
    # -----------------------------------------------------------------
    init_url = f"{GRAPH_API_BASE}/{INSTAGRAM_ACCOUNT_ID}/media"
    init_payload = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    try:
        resp = requests.post(init_url, data=init_payload, timeout=20)
        init_data = resp.json()
    except Exception as e:
        logger.error(f"[INSTAGRAM] Failed to connect to Meta Graph API: {e}")
        return None

    if "id" not in init_data or "uri" not in init_data:
        logger.error(f"[INSTAGRAM] Container initialization failed: {init_data}")
        return None

    container_id = init_data["id"]
    upload_uri = init_data["uri"]
    logger.info(f"[INSTAGRAM] Container initialized (ID: {container_id}). Uploading video binary...")

    # -----------------------------------------------------------------
    # STEP 2: Stream Raw Video Bytes to Meta Upload URI
    # -----------------------------------------------------------------
    headers = {
        "Authorization": f"OAuth {INSTAGRAM_ACCESS_TOKEN}",
        "offset": "0",
        "file_size": str(file_size),
        "Content-Type": "application/octet-stream"
    }

    try:
        with open(video_path, "rb") as f:
            video_bytes = f.read()

        upload_resp = requests.post(upload_uri, headers=headers, data=video_bytes, timeout=120)
        if upload_resp.status_code not in (200, 201):
            logger.error(f"[INSTAGRAM] Binary upload failed ({upload_resp.status_code}): {upload_resp.text}")
            return None
        logger.info("[INSTAGRAM] Binary stream accepted by Meta servers. Processing Reel container...")
    except Exception as e:
        logger.error(f"[INSTAGRAM] Error during video upload: {e}")
        return None

    # -----------------------------------------------------------------
    # STEP 3: Poll Container Status until Meta Finish Encoding
    # -----------------------------------------------------------------
    status_url = f"{GRAPH_API_BASE}/{container_id}"
    status_params = {
        "fields": "status_code,status",
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    max_retries = 24  # 24 * 5s = 2 minutes max
    is_ready = False
    for attempt in range(max_retries):
        time.sleep(5)
        try:
            st_resp = requests.get(status_url, params=status_params, timeout=15)
            st_data = st_resp.json()
            status_code = st_data.get("status_code", "").upper()
            logger.info(f"[INSTAGRAM] Encoding Status ({attempt+1}/{max_retries}): {status_code}")

            if status_code == "FINISHED":
                is_ready = True
                break
            elif status_code == "ERROR":
                logger.error(f"[INSTAGRAM] Container encoding failed: {st_data}")
                return None
        except Exception as e:
            logger.warning(f"[INSTAGRAM] Polling warning: {e}")

    if not is_ready:
        logger.error("[INSTAGRAM] Container processing timed out.")
        return None

    # -----------------------------------------------------------------
    # STEP 4: Publish the Reel Live to Instagram Feed
    # -----------------------------------------------------------------
    publish_url = f"{GRAPH_API_BASE}/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }

    try:
        pub_resp = requests.post(publish_url, data=publish_payload, timeout=30)
        pub_data = pub_resp.json()
    except Exception as e:
        logger.error(f"[INSTAGRAM] Media publish request failed: {e}")
        return None

    if "id" not in pub_data:
        logger.error(f"[INSTAGRAM] Failed to publish Reel: {pub_data}")
        return None

    media_id = pub_data["id"]
    
    # Retrieve public permalink URL
    permalink = None
    try:
        p_resp = requests.get(
            f"{GRAPH_API_BASE}/{media_id}", 
            params={"fields": "permalink", "access_token": INSTAGRAM_ACCESS_TOKEN},
            timeout=10
        )
        p_data = p_resp.json()
        permalink = p_data.get("permalink")
    except Exception:
        pass

    final_url = permalink or f"https://www.instagram.com/p/{media_id}/"
    logger.info(f"🎉 [INSTAGRAM] MISSION ACCOMPLISHED! Reel live at: {final_url}")
    return final_url


if __name__ == "__main__":
    configured = is_instagram_configured()
    print(f"Instagram Graph API Configured: {configured}")
    if not configured:
        print("Set INSTAGRAM_ACCOUNT_ID and INSTAGRAM_ACCESS_TOKEN in .env to enable.")
