"""
iDastawez Topic Engine - Google Trends Feed
Monitors real-time search volume spikes in India via Google Trends RSS.
Provides instant search interest boosts to matching citizen and government topics.
"""

import ssl
import logging
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

logger = logging.getLogger("topic_engine.trends")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[Google Trends] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

GOOGLE_TRENDS_IN_URL = "https://trends.google.com/trending/rss?geo=IN"


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_google_trends_feed() -> List[Dict[str, Any]]:
    """
    Fetches real-time daily trending search terms in India from Google Trends RSS.
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "hi,en-US,en;q=0.9",
    }

    trends = []
    try:
        req = urllib.request.Request(GOOGLE_TRENDS_IN_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()

        root = ET.fromstring(data)
        items = root.findall(".//item")
        for it in items:
            title = it.find("title").text if it.find("title") is not None else ""
            approx_elem = it.find("{https://trends.google.com/trending/rss}approx_traffic")
            traffic = approx_elem.text if approx_elem is not None else "100+"

            if title:
                trends.append({
                    "query": title.strip(),
                    "traffic": traffic,
                    "source": "Google Trends (India)"
                })
        logger.info(f"Google Trends: Loaded {len(trends)} trending terms.")
    except Exception as e:
        logger.warning(f"Failed to fetch Google Trends IN: {e}")

    return trends


def get_trends_similarity_score(topic_title: str, trends_list: List[Dict[str, Any]]) -> int:
    """
    Returns a score boost (+15 to +25) if the topic matches active Google Trends queries.
    """
    if not topic_title or not trends_list:
        return 0

    title_lower = topic_title.lower()
    for tr in trends_list:
        query_lower = tr.get("query", "").lower()
        if len(query_lower) >= 3 and query_lower in title_lower:
            logger.info(f"Google Trends Match! '{query_lower}' found in '{topic_title}' (+20 pts)")
            return 20
        # Also check reverse (if title words match query)
        words = [w for w in title_lower.split() if len(w) > 3]
        for w in words:
            if w in query_lower:
                return 15

    return 0


if __name__ == "__main__":
    trends = fetch_google_trends_feed()
    print(f"Loaded {len(trends)} Google Trends:")
    for tr in trends[:5]:
        print(f" - {tr['query']} ({tr['traffic']})")
