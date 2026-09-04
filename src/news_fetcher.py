"""
Trending Tech News Fetcher
Fetches real-time trending tech, AI, and developer news from Hacker News, Reddit, and RSS feeds.
100% Free - No API keys required.
"""

import requests
import feedparser
import logging
from typing import List, Dict

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


if __name__ == "__main__":
    stories = get_trending_tech_stories()
    for i, story in enumerate(stories[:3], 1):
        print(f"{i}. [{story['source']}] {story['title']}")
