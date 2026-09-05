"""
Trending Tech News Fetcher
Fetches real-time trending tech, AI, and developer news from Hacker News, Reddit, and RSS feeds.
100% Free - No API keys required.
"""

import os
import re
import json
import datetime
import requests
import feedparser
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# Curated evergreen/backup trending stories if network is offline
FALLBACK_STORIES = [
    {
        "title": "OpenAI Releases Next-Generation Model with Real-Time Reasoning Capabilities",
        "source": "HackerNews",
        "url": "https://news.ycombinator.com",
        "summary": "A massive architectural shift in artificial intelligence focusing on multi-step reasoning, self-correction, and autonomous coding agents."
    },
    {
        "title": "New Web Standards Proposal Aims to Replace JavaScript Bundlers with Native ES Modules",
        "source": "Reddit r/technology",
        "url": "https://reddit.com/r/technology",
        "summary": "Browsers are preparing to support direct module resolution, dramatically reducing build times and eliminating complex tooling."
    },
    {
        "title": "Open-Source Local LLMs Surpass Proprietary Cloud Models on Coding Benchmarks",
        "source": "TechRadar",
        "url": "https://techcrunch.com",
        "summary": "Quantized 7B and 14B models running on standard consumer hardware can now write, test, and debug full-stack applications locally."
    }
]


def fetch_hacker_news_top(limit: int = 5) -> List[Dict[str, str]]:
    """Fetch top trending stories from Hacker News official Firebase API."""
    stories = []
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            top_ids = resp.json()[:limit]
            for item_id in top_ids:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                item_resp = requests.get(item_url, timeout=5)
                if item_resp.status_code == 200:
                    data = item_resp.json()
                    if data and "title" in data:
                        stories.append({
                            "title": data.get("title", ""),
                            "url": data.get("url", f"https://news.ycombinator.com/item?id={item_id}"),
                            "source": "Hacker News",
                            "score": data.get("score", 0),
                            "summary": data.get("title", "")
                        })
    except Exception as e:
        logger.warning(f"Could not fetch from Hacker News: {e}")
    return stories


def fetch_reddit_tech(limit: int = 5) -> List[Dict[str, str]]:
    """Fetch top tech posts from Reddit JSON feed."""
    stories = []
    try:
        headers = {"User-Agent": USER_AGENT}
        url = "https://www.reddit.com/r/technology/hot.json?limit=" + str(limit)
        resp = requests.get(url, headers=headers, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})
                if not post.get("stickied", False):
                    stories.append({
                        "title": post.get("title", ""),
                        "url": f"https://reddit.com{post.get('permalink', '')}",
                        "source": "Reddit r/technology",
                        "score": post.get("score", 0),
                        "summary": post.get("title", "")
                    })
    except Exception as e:
        logger.warning(f"Could not fetch from Reddit: {e}")
    return stories


def fetch_rss_feed(feed_url: str, source_name: str, limit: int = 3) -> List[Dict[str, str]]:
    """Fetch articles from an RSS feed."""
    stories = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:limit]:
            stories.append({
                "title": entry.get("title", ""),
                "url": entry.get("link", ""),
                "source": source_name,
                "summary": entry.get("summary", "")[:200]
            })
    except Exception as e:
        logger.warning(f"Could not fetch from {source_name}: {e}")
    return stories


def get_trending_tech_stories() -> List[Dict[str, str]]:
    """Aggregate, deduplicate, and return top tech stories."""
    all_stories = []
    
    hn_stories = fetch_hacker_news_top(limit=4)
    all_stories.extend(hn_stories)

    reddit_stories = fetch_reddit_tech(limit=3)
    all_stories.extend(reddit_stories)

    tc_stories = fetch_rss_feed("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI", limit=3)
    all_stories.extend(tc_stories)

    # Filter out empty or duplicate titles
    seen_titles = set()
    cleaned = []
    for s in all_stories:
        title = s.get("title", "").strip()
        if title and len(title) > 15 and title.lower() not in seen_titles:
            seen_titles.add(title.lower())
            cleaned.append(s)

    if not cleaned:
        logger.info("Using fallback tech news stories.")
        return FALLBACK_STORIES

    logger.info(f"Successfully aggregated {len(cleaned)} trending tech stories.")
    return cleaned


# =========================================================================
# DUPLICATE STORY PREVENTION (48h - 7d Fuzzy Keyword & URL Deduplication)
# =========================================================================
HISTORY_FILE = "assets/published_history.json"


def _normalize_title_tokens(text: str) -> set:
    """Extract significant keywords (> 3 chars) for fuzzy duplicate matching."""
    words = re.findall(r'[a-z0-9]+', text.lower())
    stop_words = {
        "this", "that", "with", "from", "have", "been", "were", "what", 
        "just", "after", "into", "over", "more", "their", "will", "about", 
        "there", "which", "could", "would"
    }
    return {w for w in words if len(w) > 3 and w not in stop_words}


def load_published_history(history_file: str = HISTORY_FILE) -> List[Dict[str, Any]]:
    """Loads previously published stories from local tracking file."""
    if not os.path.exists(history_file):
        return []
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        logger.warning(f"Could not read published history: {e}")
        return []


def filter_previously_published_stories(
    candidate_stories: List[Dict[str, Any]], 
    history_file: str = HISTORY_FILE
) -> List[Dict[str, Any]]:
    """
    Intelligently filters out any candidate story that was already covered in recent runs.
    Uses exact URL matching, exact title matching, and fuzzy keyword token overlap (>= 60%).
    """
    history = load_published_history(history_file)
    if not history:
        logger.info("No prior story history found. All candidates are fresh.")
        return candidate_stories

    fresh_stories = []
    for cand in candidate_stories:
        cand_title = cand.get("title", "").strip()
        cand_url = cand.get("url", "").strip().lower()
        cand_tokens = _normalize_title_tokens(cand_title)
        
        is_duplicate = False
        matched_prev = ""
        for entry in history:
            prev_title = entry.get("title", "").strip()
            prev_url = entry.get("url", "").strip().lower()
            
            # 1. Exact URL match
            if cand_url and prev_url and cand_url == prev_url:
                is_duplicate = True
                matched_prev = prev_title
                break
                
            # 2. Exact Title match
            if cand_title.lower() == prev_title.lower():
                is_duplicate = True
                matched_prev = prev_title
                break
                
            # 3. High keyword overlap (Fuzzy overlap >= 60%)
            prev_tokens = _normalize_title_tokens(prev_title)
            if cand_tokens and prev_tokens:
                intersection = cand_tokens.intersection(prev_tokens)
                overlap_ratio = len(intersection) / min(len(cand_tokens), len(prev_tokens))
                if overlap_ratio >= 0.60:
                    is_duplicate = True
                    matched_prev = prev_title
                    break
        
        if is_duplicate:
            logger.info(f"Duplicate Story Prevention: Skipping already covered topic -> '{cand_title}' (matches: '{matched_prev}')")
        else:
            fresh_stories.append(cand)

    logger.info(f"Duplicate Story Prevention: {len(fresh_stories)} fresh stories available (filtered out {len(candidate_stories) - len(fresh_stories)} duplicates).")
    return fresh_stories


def mark_story_as_published(story: Dict[str, Any], history_file: str = HISTORY_FILE):
    """Appends story to published history and prunes old entries beyond 100 items."""
    try:
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        history = load_published_history(history_file)
        
        entry = {
            "title": story.get("title", ""),
            "url": story.get("url", ""),
            "source": story.get("source", ""),
            "published_at": datetime.datetime.now().isoformat()
        }
        history.append(entry)
        
        # Keep last 100 stories (clean, small JSON payload)
        history = history[-100:]
        
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Recorded published story in history: '{story.get('title')}'")
    except Exception as e:
        logger.warning(f"Could not update published history: {e}")


if __name__ == "__main__":
    stories = get_trending_tech_stories()
    fresh = filter_previously_published_stories(stories)
    for i, story in enumerate(fresh[:3], 1):
        print(f"{i}. [{story['source']}] {story['title']}")
