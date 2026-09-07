"""
iDastawez Topic Engine - YouTube Search Autocomplete Feed
Tracks high-intent search phrases that millions of Indian citizens are typing into YouTube.
Gives a heavy viral relevance boost to topics aligning with live YouTube search volume.
"""

import json
import ssl
import logging
import urllib.parse
import urllib.request
from typing import List, Dict, Any, Set

logger = logging.getLogger("topic_engine.youtube")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[YouTube Search Feed] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

CITIZEN_SEARCH_SEEDS = [
    "sarkari yojana 2026",
    "online form 2026",
    "ekyc kaise kare",
    "ration card 2026",
    "pm kisan installment",
    "scholarship online form",
    "voter id card",
    "pan aadhar link",
    "ayushman card apply",
    "bihar yojana",
]


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_youtube_search_trends() -> List[str]:
    """
    Fetches real-time YouTube search autocomplete suggestions across all seed intents.
    Returns a unified deduplicated list of trending search phrases.
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "hi,en-US,en;q=0.9",
    }

    all_suggestions: Set[str] = set()

    for seed in CITIZEN_SEARCH_SEEDS:
        url = f"https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&q={urllib.parse.quote(seed)}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8, context=ctx) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")

            if raw.startswith("window.google.ac.h("):
                payload = raw[len("window.google.ac.h("):-1]
                data = json.loads(payload)
                suggestions = [item[0] for item in data[1]]
                all_suggestions.update(suggestions)
        except Exception as e:
            logger.warning(f"Error querying YouTube autocomplete for '{seed}': {e}")

    results = sorted(list(all_suggestions))
    logger.info(f"YouTube Search Feed: Discovered {len(results)} high-intent citizen queries.")
    return results


def get_youtube_intent_score(topic_title: str, yt_queries: List[str]) -> int:
    """
    Returns an algorithmic search intent boost (+15 to +25) if topic matches
    what citizens are actively searching on YouTube.
    """
    if not topic_title or not yt_queries:
        return 0

    title_lower = topic_title.lower()
    for q in yt_queries:
        q_lower = q.lower()
        # Direct substring match
        if len(q_lower) >= 5 and (q_lower in title_lower or title_lower in q_lower):
            logger.info(f"YouTube Search Match! '{q}' matches topic '{topic_title}' (+25 pts)")
            return 25

        # Key phrases match (e.g. 'ekyc', 'ration card', 'online form')
        token_matches = sum(1 for token in q_lower.split() if len(token) > 3 and token in title_lower)
        if token_matches >= 2:
            return 18

    return 0


if __name__ == "__main__":
    queries = fetch_youtube_search_trends()
    print(f"Sample YouTube Citizen Queries ({len(queries)} total):")
    for q in queries[:10]:
        print(f" - {q}")
