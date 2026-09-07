"""
iDastawez Topic Discovery & Verification Engine
Multi-Feed Pipeline:
SarkariResult (#1) + OnlineUpdateSTM (#2) + Govt Ministries + SSC/UPSC/RRB
+ Google Trends + YouTube Search -> Multi-Factor Scorer -> Official Verifier -> Evidence Pack
"""

import logging
from typing import Dict, Any, List, Optional

from dastawez.topic_engine.scorer import score_and_rank_topics
from dastawez.topic_engine.verifier import verify_topic_official_source
from dastawez.topic_engine.evidence_pack import build_evidence_pack
from dastawez.topics import VERIFIED_GOVT_SCHEMES

logger = logging.getLogger("topic_engine")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[iDastawez Topic Engine] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


def discover_daily_top_topic(filter_covered: bool = True) -> Dict[str, Any]:
    """
    Executes the complete multi-feed topic discovery pipeline:
    1. Ingests and scores topics across all 6 primary and secondary feeds.
    2. Enforces anti-duplication against history.json.
    3. Validates against official source (.gov.in / zero fake clickbait).
    4. Packages the winning topic into a complete standard Evidence Pack.
    """
    logger.info("Executing Multi-Feed Topic Discovery...")
    ranked_candidates = score_and_rank_topics(filter_covered=filter_covered)

    if not ranked_candidates:
        logger.warning("No candidates found in live feeds. Falling back to primary verified scheme.")
        return VERIFIED_GOVT_SCHEMES[0]

    # Find the highest-ranked topic that passes official verification
    for candidate in ranked_candidates:
        verified = verify_topic_official_source(candidate)
        if verified.get("is_valid"):
            logger.info("=" * 65)
            logger.info(f"🏆 TOPIC SELECTED: {verified['title']}")
            logger.info(f"   Source: {verified.get('source')} (Score: {candidate.get('score')} pts)")
            logger.info(f"   Official Authority: {verified.get('ministry')}")
            logger.info(f"   Official Domain: {verified.get('official_portal_domain')}")
            logger.info("=" * 65)

            # Build and return complete Evidence Pack
            evidence_pack = build_evidence_pack(verified)
            return evidence_pack

    logger.warning("No live candidates passed verification. Using default verified registry.")
    return VERIFIED_GOVT_SCHEMES[0]


def get_ranked_topics_overview(limit: int = 10, filter_covered: bool = True) -> List[Dict[str, Any]]:
    """
    Returns an overview of the top ranked topics for reporting and dashboard visibility.
    """
    ranked = score_and_rank_topics(filter_covered=filter_covered)
    overview = []
    for item in ranked[:limit]:
        verified = verify_topic_official_source(item)
        overview.append({
            "title": item["title"],
            "score": item["score"],
            "source": item["source"],
            "category": item["category"],
            "is_urgent": item.get("is_urgent", False),
            "is_valid": verified.get("is_valid", False),
            "official_domain": verified.get("official_portal_domain"),
            "score_breakdown": item.get("score_breakdown", {})
        })
    return overview


if __name__ == "__main__":
    top = discover_daily_top_topic(filter_covered=True)
    print("\nSelected Daily Scheme:")
    print("Title:", top["scheme_name_hi"])
    print("Ministry:", top["ministry"])
    print("Portal:", top["portal_url"])
    print("Ref:", top["notification_ref"])
