"""
iDastawez Topic Engine - Multi-Factor Scorer & Anti-Duplication Engine
Aggregates candidate topics from 6 feeds, calculates composite engagement/urgency scores,
and enforces strict deduplication against history.json.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

from dastawez.history_tracker import is_topic_covered
from dastawez.topic_engine.feeds.sarkari_result import fetch_sarkari_result_feed
from dastawez.topic_engine.feeds.online_update_stm import fetch_online_update_stm_feed
from dastawez.topic_engine.feeds.govt_ministries import fetch_govt_ministries_feed
from dastawez.topic_engine.feeds.recruitment_boards import fetch_recruitment_boards_feed
from dastawez.topic_engine.feeds.google_trends import fetch_google_trends_feed, get_trends_similarity_score
from dastawez.topic_engine.feeds.youtube_search import fetch_youtube_search_trends, get_youtube_intent_score

logger = logging.getLogger("topic_engine.scorer")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[Topic Scorer] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


def collect_all_candidates() -> List[Dict[str, Any]]:
    """
    Ingests raw candidate items from all 4 primary content feeds.
    """
    candidates = []

    # 1. Sarkari Result (Priority #1)
    sarkari_items = fetch_sarkari_result_feed(max_items=20)
    candidates.extend(sarkari_items)

    # 2. Online Update STM (Priority #2)
    stm_items = fetch_online_update_stm_feed(max_items=15)
    candidates.extend(stm_items)

    # 3. Govt Ministries & PIB
    ministry_items = fetch_govt_ministries_feed(max_items=10)
    candidates.extend(ministry_items)

    # 4. Recruitment Boards (SSC/UPSC/RRB/NTA)
    board_items = fetch_recruitment_boards_feed(max_items=10)
    candidates.extend(board_items)

    return candidates


def score_and_rank_topics(filter_covered: bool = True) -> List[Dict[str, Any]]:
    """
    Ranks all candidate topics based on the multi-factor scoring formula:
    Score = SourceBase (30-55) + UrgencyBoost (+20) + YouTubeBoost (+25) + TrendsBoost (+20) - DuplicationPenalty
    """
    logger.info("Starting Multi-Feed Candidate Ingestion & Scoring...")
    candidates = collect_all_candidates()

    # Ingest search volume signals (Feeds 5 & 6)
    yt_queries = fetch_youtube_search_trends()
    google_trends = fetch_google_trends_feed()

    scored_topics = []
    seen_normalized = set()

    for item in candidates:
        title = item.get("title", "")
        if not title:
            continue

        # Normalization check to prevent near-identical titles across feeds
        norm_title = re.sub(r"[^\w\s]", "", title).strip().lower()
        norm_title = re.sub(r"\s+", " ", norm_title)
        if norm_title in seen_normalized:
            continue
        seen_normalized.add(norm_title)

        # 1. Source Base Score
        base = item.get("base_score", 30)

        # 2. Urgency & Deadline Boost
        urgency_boost = 0
        if item.get("is_urgent") or re.search(r"(last date|अंतिम तिथि|deadline|e-kyc|ekyc|extended)", title, re.IGNORECASE):
            urgency_boost = 20

        # 3. YouTube Citizen Search Intent Boost
        yt_boost = get_youtube_intent_score(title, yt_queries)

        # 4. Google Trends Spikes Boost
        trends_boost = get_trends_similarity_score(title, google_trends)

        # 5. Anti-Duplication History Check
        duplication_penalty = 0
        is_dup = is_topic_covered(topic_id=title, topic_title=title, cooldown_days=45)
        if is_dup:
            duplication_penalty = 1000
            logger.info(f"Topic '{title}' was recently covered in history. Penalized by -1000.")

        total_score = base + urgency_boost + yt_boost + trends_boost - duplication_penalty

        scored_item = dict(item)
        scored_item["score"] = total_score
        scored_item["score_breakdown"] = {
            "source_base": base,
            "urgency_boost": urgency_boost,
            "youtube_boost": yt_boost,
            "trends_boost": trends_boost,
            "duplication_penalty": duplication_penalty,
            "is_duplicate": is_dup,
        }

        if filter_covered and is_dup:
            continue

        scored_topics.append(scored_item)

    # Sort descending by total score
    scored_topics.sort(key=lambda x: x["score"], reverse=True)
    logger.info(f"Scoring Complete: Ranked {len(scored_topics)} active candidate topics.")
    return scored_topics


if __name__ == "__main__":
    ranked = score_and_rank_topics(filter_covered=False)
    print(f"\nTop 10 Scored Topics:")
    for idx, t in enumerate(ranked[:10]):
        sb = t["score_breakdown"]
        dup_marker = " [DUPLICATE]" if sb["is_duplicate"] else ""
        print(f"{idx+1}. [{t['score']} pts]{dup_marker} ({t['source']}) {t['title']}")
        print(f"    Breakdown: Base {sb['source_base']} | Urgency +{sb['urgency_boost']} | YT +{sb['youtube_boost']} | Trends +{sb['trends_boost']}")
