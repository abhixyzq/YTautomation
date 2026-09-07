"""
iDastawez Topic Engine - SSC / UPSC / RRB / NTA Feed
Dedicated tracker for national recruitment bodies and examination authorities:
Staff Selection Commission (SSC), Union Public Service Commission (UPSC),
Railway Recruitment Boards (RRB), and National Testing Agency (NTA).
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Any

from dastawez.topic_engine.feeds.sarkari_result import fetch_sarkari_result_feed

logger = logging.getLogger("topic_engine.boards")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[Recruitment Boards Feed] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

TARGET_BOARDS = {
    "ssc": ("कर्मचारी चयन आयोग (SSC)", "ssc.gov.in", 32),
    "upsc": ("संघ लोक सेवा आयोग (UPSC)", "upsc.gov.in", 32),
    "railway": ("रेलवे भर्ती बोर्ड (RRB)", "rrbcdg.gov.in", 34),
    "rrb": ("रेलवे भर्ती बोर्ड (RRB)", "rrbcdg.gov.in", 34),
    "nta": ("नेशनल टेस्टिंग एजेंसी (NTA)", "nta.ac.in", 30),
    "ibps": ("इंस्टीट्यूट ऑफ बैंकिंग पर्सनेल (IBPS)", "ibps.in", 28),
}


def fetch_recruitment_boards_feed(max_items: int = 10) -> List[Dict[str, Any]]:
    """
    Filters and formats high-priority recruitment and exam notifications
    specifically issued by SSC, UPSC, RRB, and NTA.
    """
    raw_sarkari = fetch_sarkari_result_feed(max_items=30)
    board_items = []
    seen = set()

    for item in raw_sarkari:
        title = item.get("title", "")
        title_lower = title.lower()

        matched_board = None
        for key, (board_name, domain, prio) in TARGET_BOARDS.items():
            if re.search(rf"\b{key}\b", title_lower):
                matched_board = (board_name, domain, prio)
                break

        if matched_board and title_lower not in seen:
            seen.add(title_lower)
            board_name, domain, prio = matched_board
            score = prio
            if item.get("is_urgent"):
                score += 8
            if item.get("is_new"):
                score += 5

            board_items.append({
                "title": title,
                "url": item.get("url", f"https://{domain}"),
                "source": f"Recruitment Board ({board_name})",
                "category": f"भर्ती परीक्षा: {board_name}",
                "base_score": score,
                "is_urgent": item.get("is_urgent", False),
                "is_new": item.get("is_new", False),
                "published_at": item.get("published_at", datetime.now().isoformat()),
                "official_portal_domain": domain,
                "raw_text": f"{title} {board_name}"
            })

    logger.info(f"Recruitment Boards Feed: Filtered {len(board_items)} board notifications.")
    return board_items[:max_items]


if __name__ == "__main__":
    items = fetch_recruitment_boards_feed(5)
    print(f"Fetched {len(items)} items from Recruitment Boards:")
    for idx, it in enumerate(items):
        print(f"{idx+1}. [{it['category']}] (Score: {it['base_score']}) {it['title']}")
