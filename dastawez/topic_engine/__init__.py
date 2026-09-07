"""
iDastawez Topic Discovery & Verification Engine
Multi-Feed Pipeline:
SarkariResult (#1) + OnlineUpdateSTM (#2) + Govt Ministries + SSC/UPSC/RRB
+ Google Trends + YouTube Search -> Multi-Factor Scorer -> Official Verifier -> Evidence Pack
"""

import re
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


def resolve_target_scheme(target_input: str, force: bool = False) -> Dict[str, Any]:
    """
    Resolves any user-provided scheme string:
    1. Exact or prefix ID match in VERIFIED_GOVT_SCHEMES
    2. Substring match in VERIFIED_GOVT_SCHEMES
    3. Match across live candidates from SarkariResult / OnlineUpdateSTM
    4. Ad-hoc candidate synthesis for any arbitrary government topic or query
    """
    clean_input = str(target_input or "").strip()
    if not clean_input:
        return discover_daily_top_topic(filter_covered=not force)

    # 1. Exact ID match
    matching = [s for s in VERIFIED_GOVT_SCHEMES if s["id"] == clean_input]
    if matching:
        from dastawez.latest_tracker import enrich_and_prioritize_schemes
        return enrich_and_prioritize_schemes(matching, filter_covered=not force)[0]

    # 2. Substring in verified schemes
    lower_in = clean_input.lower()
    matching = [
        s for s in VERIFIED_GOVT_SCHEMES 
        if lower_in in s["id"].lower() 
        or lower_in in s.get("scheme_name_hi", "").lower() 
        or lower_in in s.get("title", "").lower()
    ]
    if matching:
        from dastawez.latest_tracker import enrich_and_prioritize_schemes
        return enrich_and_prioritize_schemes(matching, filter_covered=not force)[0]

    # 3. Live search in scraped feeds
    try:
        from dastawez.topic_engine.scorer import collect_all_candidates
        candidates = collect_all_candidates()
        in_words = [w for w in re.split(r"[\s/|\-_]+", lower_in) if len(w) > 2]
        for c in candidates:
            c_title = (c.get("title", "") + " " + c.get("raw_title", "")).lower()
            if in_words and all(w in c_title for w in in_words[:2]):
                verified = verify_topic_official_source(c)
                if verified.get("is_valid"):
                    logger.info(f"Target matched live feed topic: {verified['title']}")
                    return build_evidence_pack(verified)
    except Exception as e:
        logger.debug(f"Candidate match error: {e}")

    # 4. Ad-hoc dynamic candidate creation
    logger.info(f"Synthesizing targeted topic evidence pack for: '{clean_input}'")
    ad_hoc_candidate = {
        "title": clean_input,
        "raw_title": clean_input,
        "source": "Targeted Topic",
        "url": "https://india.gov.in",
        "category": "targeted_topic",
        "is_urgent": True,
        "base_score": 100
    }
    verified = verify_topic_official_source(ad_hoc_candidate)
    return build_evidence_pack(verified)


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
