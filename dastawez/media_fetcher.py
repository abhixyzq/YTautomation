"""
iDastawez Media & Visual Asset Engine
Integrates:
1. Wikimedia Commons — 100% Free & Open (No API Key). Authentic Indian Government buildings,
   Parliament, Ashoka emblems, Ration distribution, AIIMS hospitals, Indian currency, Farmer fields.
2. Pexels — HD 1080p/4K Cinematic Landscape B-Roll video clips (Office, documents, typing, banking).
3. Pixabay / Unsplash — Fallback generic stock photos and video footage.

All assets are automatically downloaded, optimized, cached, and synchronized into Remotion's public/ folder.
"""

import os
import re
import random
import shutil
import logging
import requests
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("dastawez.media")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[iDastawez Media] %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "").strip()
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "").strip()

MEDIA_CACHE_DIR = "assets/dastawez_media"
BROLL_CACHE_DIR = "assets/broll_cache"

os.makedirs(MEDIA_CACHE_DIR, exist_ok=True)
os.makedirs(BROLL_CACHE_DIR, exist_ok=True)


# =====================================================================
# 1. WIKIMEDIA COMMONS (100% Free, Public Domain & CC Govt Imagery)
# =====================================================================

def fetch_wikimedia_image(
    query: str, 
    fallback_queries: Optional[List[str]] = None,
    public_dest_dir: str = "public/dastawez_media"
) -> Optional[Dict[str, str]]:
    """
    Searches Wikimedia Commons API for high-resolution authentic government/official photos.
    No API Key required. Public Domain & CC-BY compliant.
    """
    queries = [query] + (fallback_queries or [])
    headers = {"User-Agent": "iDastawez-Explainer-Bot/1.0 (https://github.com/abhixyzq/YTautomation; contact@idastawez.org)"}
    
    for q in queries:
        try:
            api_url = (
                f"https://commons.wikimedia.org/w/api.php?"
                f"action=query&format=json&generator=search&"
                f"gsrnamespace=6&gsrsearch={requests.utils.quote(q)}&"
                f"gsrlimit=8&prop=imageinfo&iiprop=url|mime|size|extmetadata"
            )
            resp = requests.get(api_url, headers=headers, timeout=12)
            if resp.status_code != 200:
                continue

            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            
            for pid, page_info in pages.items():
                title = page_info.get("title", "")
                imageinfo = page_info.get("imageinfo", [])
                if not imageinfo:
                    continue
                
                info = imageinfo[0]
                mime = info.get("mime", "").lower()
                img_url = info.get("url")
                width = info.get("width", 0)
                
                # Must be a photo (JPEG/PNG) and reasonable resolution
                if not img_url or not ("image/jpeg" in mime or "image/png" in mime):
                    continue
                if width and width < 600:
                    continue
                
                # Sanitize filename
                clean_name = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", title.replace("File:", ""))
                local_cache_path = os.path.join(MEDIA_CACHE_DIR, clean_name)

                # Download if not cached
                if not (os.path.exists(local_cache_path) and os.path.getsize(local_cache_path) > 10000):
                    logger.info(f"Downloading Wikimedia Commons image for '{q}': {clean_name}...")
                    img_resp = requests.get(img_url, headers=headers, timeout=25)
                    if img_resp.status_code == 200:
                        with open(local_cache_path, "wb") as f:
                            f.write(img_resp.content)
                    else:
                        continue

                # Sync to Remotion public/ directory
                os.makedirs(public_dest_dir, exist_ok=True)
                public_filename = f"wiki_{clean_name}"
                public_file_path = os.path.join(public_dest_dir, public_filename)
                shutil.copy2(local_cache_path, public_file_path)

                return {
                    "local_path": local_cache_path,
                    "public_path": f"dastawez_media/{public_filename}",
                    "source_url": img_url,
                    "attribution": "Wikimedia Commons (Public Domain / CC)",
                    "title": title.replace("File:", "").replace(".jpg", "").replace(".png", "")
                }
        except Exception as e:
            logger.warning(f"Error querying Wikimedia Commons for '{q}': {e}")

    return None


# =====================================================================
# 2. PEXELS 1080p LANDSCAPE B-ROLL VIDEO FETCHER
# =====================================================================

def fetch_pexels_broll(
    query: str,
    orientation: str = "landscape",
    public_dest_dir: str = "public/dastawez_broll"
) -> Optional[Dict[str, str]]:
    """
    Downloads royalty-free 1080p horizontal B-roll footage from Pexels API.
    Used for subtle animated ambient background layers in Remotion.
    """
    if not PEXELS_API_KEY:
        logger.info("No PEXELS_API_KEY detected. Skipping B-roll download.")
        return None

    clean_query = query.replace('"', '').replace("'", "").strip()
    headers = {"Authorization": PEXELS_API_KEY}
    random_page = random.randint(1, 4)
    url = (
        f"https://api.pexels.com/videos/search?"
        f"query={requests.utils.quote(clean_query)}&"
        f"orientation={orientation}&"
        f"per_page=6&"
        f"page={random_page}"
    )

    try:
        resp = requests.get(url, headers=headers, timeout=12)
        videos = []
        if resp.status_code == 200:
            videos = resp.json().get("videos", [])
        
        if not videos:
            # Fallback to page 1
            resp_p1 = requests.get(
                f"https://api.pexels.com/videos/search?query={requests.utils.quote(clean_query)}&orientation={orientation}&per_page=6&page=1",
                headers=headers, timeout=12
            )
            if resp_p1.status_code == 200:
                videos = resp_p1.json().get("videos", [])

        if videos:
            selected_video = random.choice(videos)
            vid_id = str(selected_video.get("id"))
            local_cache_path = os.path.join(BROLL_CACHE_DIR, f"pex_landscape_{vid_id}.mp4")

            if not (os.path.exists(local_cache_path) and os.path.getsize(local_cache_path) > 100000):
                # Prioritize horizontal 1080p
                video_files = selected_video.get("video_files", [])
                sorted_files = sorted(
                    video_files,
                    key=lambda f: (f.get("width", 0) >= 1920, f.get("width", 0) >= 1280),
                    reverse=True
                )
                if sorted_files:
                    dl_url = sorted_files[0]["link"]
                    logger.info(f"Downloading 1080p landscape B-roll for '{query}' (ID: {vid_id})...")
                    v_data = requests.get(dl_url, timeout=35)
                    if v_data.status_code == 200:
                        with open(local_cache_path, "wb") as f:
                            f.write(v_data.content)

            if os.path.exists(local_cache_path):
                # Sync to Remotion public/ directory
                os.makedirs(public_dest_dir, exist_ok=True)
                public_filename = f"broll_{vid_id}.mp4"
                public_file_path = os.path.join(public_dest_dir, public_filename)
                if not os.path.exists(public_file_path):
                    shutil.copy2(local_cache_path, public_file_path)

                return {
                    "local_path": local_cache_path,
                    "public_path": f"dastawez_broll/{public_filename}",
                    "source": "Pexels (Free Commercial Use)",
                    "id": vid_id
                }
    except Exception as e:
        logger.warning(f"Error fetching Pexels video for '{query}': {e}")

    return None


# =====================================================================
# 3. PIXABAY VIDEO & PHOTO FETCHER (FALLBACK)
# =====================================================================

def fetch_pixabay_asset(
    query: str,
    asset_type: str = "video",
    public_dest_dir: str = "public/dastawez_broll"
) -> Optional[Dict[str, str]]:
    """
    Queries Pixabay API for free stock videos/photos if PIXABAY_API_KEY is configured.
    """
    if not PIXABAY_API_KEY:
        return None

    clean_query = requests.utils.quote(query.strip())
    try:
        if asset_type == "video":
            url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={clean_query}&video_type=film&per_page=5"
            resp = requests.get(url, timeout=12).json()
            hits = resp.get("hits", [])
            if hits:
                item = random.choice(hits)
                vid_url = item.get("videos", {}).get("medium", {}).get("url") or item.get("videos", {}).get("large", {}).get("url")
                vid_id = str(item.get("id"))
                if vid_url:
                    local_path = os.path.join(BROLL_CACHE_DIR, f"pix_{vid_id}.mp4")
                    if not os.path.exists(local_path):
                        v_data = requests.get(vid_url, timeout=30).content
                        with open(local_path, "wb") as f:
                            f.write(v_data)
                    
                    os.makedirs(public_dest_dir, exist_ok=True)
                    pub_name = f"pix_broll_{vid_id}.mp4"
                    shutil.copy2(local_path, os.path.join(public_dest_dir, pub_name))
                    return {"public_path": f"dastawez_broll/{pub_name}", "source": "Pixabay"}
    except Exception as e:
        logger.warning(f"Pixabay fetch error: {e}")
    return None


# =====================================================================
# 4. HIGH-LEVEL TOPIC VISUAL BUNDLE GENERATOR
# =====================================================================

TOPIC_VISUAL_MAP: Dict[str, Dict[str, Any]] = {
    "pan": {
        "wiki_queries": ["Income Tax Department India", "North Block New Delhi", "Aadhaar authentication India"],
        "broll_queries": ["laptop office typing", "digital banking computer", "documents paperwork"]
    },
    "ration": {
        "wiki_queries": ["Public Distribution System India ration", "Food Corporation of India", "Indian wheat grain godown"],
        "broll_queries": ["grain harvest India", "store market retail", "supermarket counter"]
    },
    "kisan": {
        "wiki_queries": ["Indian farmer agriculture", "Krishi Bhavan New Delhi", "wheat crop tractor India"],
        "broll_queries": ["farmer agriculture green field", "rural farm nature", "tractor field"]
    },
    "scholarship": {
        "wiki_queries": ["Indian students classroom", "University library India", "Ministry of Education India"],
        "broll_queries": ["student studying classroom", "writing notes pen", "college library students"]
    },
    "ayushman": {
        "wiki_queries": ["All India Institute of Medical Sciences", "Indian doctor hospital", "senior citizen health India"],
        "broll_queries": ["hospital corridor doctor", "medical health stethoscope", "doctor healthcare clinic"]
    },
    "awas": {
        "wiki_queries": ["Pradhan Mantri Awas Yojana house", "Indian brick house rural", "Nirman Bhavan New Delhi"],
        "broll_queries": ["house construction building", "architect blueprint desk", "modern home keys"]
    },
    "shram": {
        "wiki_queries": ["Indian construction worker", "Ministry of Labour and Employment India", "Indian artisan craft"],
        "broll_queries": ["construction worker safety", "industrial workshop machine", "blue collar workers"]
    },
    "sukanya": {
        "wiki_queries": ["Indian school girl child", "Post office India savings", "Banknote of India rupee"],
        "broll_queries": ["family smiling children", "piggy bank savings coin", "girl student studying"]
    }
}


def get_topic_visual_bundle(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Automatically discovers and provisions verified photos and 1080p B-roll
    tailored to the selected government scheme.
    """
    scheme_name = scheme.get("scheme_name_hi", "") + " " + scheme.get("id", "")
    matched_key = "default"

    if "पैन" in scheme_name or "pan" in scheme_name:
        matched_key = "pan"
    elif "राशन" in scheme_name or "ration" in scheme_name:
        matched_key = "ration"
    elif "किसान" in scheme_name or "kisan" in scheme_name:
        matched_key = "kisan"
    elif "स्कॉलरशिप" in scheme_name or "scholarship" in scheme_name:
        matched_key = "scholarship"
    elif "आयुष्मान" in scheme_name or "ayushman" in scheme_name:
        matched_key = "ayushman"
    elif "आवास" in scheme_name or "awas" in scheme_name:
        matched_key = "awas"
    elif "श्रम" in scheme_name or "shram" in scheme_name:
        matched_key = "shram"
    elif "सुकन्या" in scheme_name or "sukanya" in scheme_name:
        matched_key = "sukanya"

    config = TOPIC_VISUAL_MAP.get(matched_key, {
        "wiki_queries": ["Parliament House India", "Government of India building New Delhi", "Rashtrapati Bhavan New Delhi"],
        "broll_queries": ["office paperwork desk", "official signature document", "government office computer"]
    })

    # 1. Fetch authentic photo from Wikimedia Commons (100% Free, Public Domain/CC)
    wiki_asset = fetch_wikimedia_image(
        query=config["wiki_queries"][0],
        fallback_queries=config["wiki_queries"][1:]
    )

    # 2. Fetch 1080p landscape B-roll from Pexels or Pixabay
    broll_asset = None
    for bq in config["broll_queries"]:
        broll_asset = fetch_pexels_broll(bq, orientation="landscape")
        if broll_asset:
            break

    if not broll_asset:
        for bq in config["broll_queries"]:
            broll_asset = fetch_pixabay_asset(bq, asset_type="video")
            if broll_asset:
                break

    return {
        "official_image": wiki_asset,
        "broll_video": broll_asset,
        "topic_tag": matched_key
    }


if __name__ == "__main__":
    from dastawez.topics import VERIFIED_GOVT_SCHEMES
    sample = VERIFIED_GOVT_SCHEMES[0]  # Ayushman
    print(f"Testing visual asset fetcher for: {sample['scheme_name_hi']}...")
    bundle = get_topic_visual_bundle(sample)
    print("\nVisual Bundle Result:")
    print("Official Photo:", bundle["official_image"])
    print("Cinematic B-Roll:", bundle["broll_video"])
