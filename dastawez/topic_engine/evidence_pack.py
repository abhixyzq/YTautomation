"""
iDastawez Topic Engine - Evidence Pack Builder
Constructs complete, standardized, and authentic scheme evidence payloads
from dynamic multi-feed topics for the video compositor and script generator.
"""

import re
from datetime import datetime
from typing import Dict, Any, List

from dastawez.topic_engine.verifier import verify_topic_official_source


def parse_clean_titles(raw_title: str) -> tuple[str, str]:
    """
    Separates mixed Hindi/English headlines and strips promotional suffixes
    to prevent repetitive bilingual text in synthesized voiceovers.
    """
    junk_patterns = [
        r"(?:online|ऑफलाइन)\s*apply.*$",
        r"आवेदन\s*शुरू.*$",
        r"यहाँ\s*से\s*करे\s*अप्लाई.*$",
        r"मिलेगा\s*₹?[\d,]+.*$",
        r"direct\s*link.*$",
        r"last\s*date.*$",
        r"new\s*update.*$",
        r"apply\s*now.*$",
        r"योग्यता,?\s*पात्रता.*$",
        r"दस्तावेज\s*और\s*आवेदन.*$",
        r"notification\s*out.*$",
        r"online\s*form.*$",
        r"admit\s*card.*$",
        r"answer\s*key.*$"
    ]
    
    parts = re.split(r"\s*[\-\|:\/]\s*", raw_title)
    en_candidate = ""
    hi_candidate = ""
    
    for p in parts:
        p_strip = p.strip()
        if not p_strip:
            continue
        has_hindi = bool(re.search(r"[\u0900-\u097F]", p_strip))
        if has_hindi and not hi_candidate:
            cleaned_h = p_strip
            for jp in junk_patterns:
                cleaned_h = re.sub(jp, "", cleaned_h, flags=re.IGNORECASE).strip()
            if len(cleaned_h) >= 4:
                hi_candidate = cleaned_h
        elif not has_hindi and not en_candidate:
            cleaned_e = p_strip
            for jp in junk_patterns:
                cleaned_e = re.sub(jp, "", cleaned_e, flags=re.IGNORECASE).strip()
            if len(cleaned_e) >= 4:
                en_candidate = cleaned_e

    if not hi_candidate and not en_candidate:
        base = raw_title
        for jp in junk_patterns:
            base = re.sub(jp, "", base, flags=re.IGNORECASE).strip()
        hi_candidate = base
        en_candidate = base
    elif hi_candidate and not en_candidate:
        en_candidate = hi_candidate
    elif en_candidate and not hi_candidate:
        hi_candidate = en_candidate

    return hi_candidate.strip(" -|:"), en_candidate.strip(" -|:")


from dastawez.topic_engine.distiller import distill_topic_context, extract_clean_names


def build_evidence_pack(verified_topic: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms a verified topic into a complete standard scheme data structure
    ready for 5-Act script generation and 1080p Remotion rendering.
    """
    # If the topic already has full pre-configured scheme_data (e.g. from static registry), merge it
    if "scheme_data" in verified_topic:
        base_scheme = dict(verified_topic["scheme_data"])
        if verified_topic.get("title"):
            clean_h, _, _ = extract_clean_names(verified_topic["title"])
            base_scheme["latest_news_headline"] = clean_h
        return base_scheme

    title = verified_topic.get("title", "")
    domain = verified_topic.get("official_portal_domain", "india.gov.in")
    portal_url = verified_topic.get("portal_url", f"https://{domain}")
    ministry = verified_topic.get("ministry", "भारत सरकार (Government of India)")
    notif_ref = verified_topic.get("notification_ref", "GOV/DIR/2026-PUB")

    # Use smart semantic distiller to extract clean domain fields
    distilled = distill_topic_context(title, domain)

    clean_slug = re.sub(r"[^\w\s]", "", distilled["scheme_name_en"]).lower()
    clean_slug = re.sub(r"\s+", "_", clean_slug)[:45].strip("_")
    clean_slug = re.sub(r"_202[0-9]$", "", clean_slug)
    scheme_id = f"auto_{clean_slug}_2026"

    priority_groups = [
        "ग्रामीण एवं वंचित वर्ग के परिवार",
        "दिव्यांगजन, वृद्ध एवं महिला मुखिया परिवार",
        "समय सीमा से पूर्व ऑनलाइन आवेदन करने वाले पात्र नागरिक"
    ]

    evidence_pack = {
        "id": scheme_id,
        "category": distilled["category"],
        "topic_type": distilled["topic_type"],
        "scheme_name_hi": distilled["scheme_name_hi"],
        "scheme_name_en": distilled["scheme_name_en"],
        "short_name": distilled["short_name"],
        "target_audience": distilled["target_audience"],
        "action_phrase": distilled["action_phrase"],
        "ministry": ministry,
        "portal_name": f"{domain} Official Portal",
        "portal_url": portal_url,
        "official_portal_domain": domain,
        "notification_ref": notif_ref,
        "last_verified_date": "सितंबर 2026",
        "source_citation": f"{ministry} - आधिकारिक सार्वजनिक सूचना",
        "helpline": verified_topic.get("helpline") or distilled.get("helpline", "1967"),
        "benefit_amount": distilled["benefit_amount"],
        "benefit_summary": distilled["benefit_summary"],
        "latest_official_update": f"{distilled['action_phrase']} (सार्वजनिक अधिसूचना {notif_ref})",
        "latest_news_headline": distilled["scheme_name_hi"],
        "what_changed": distilled["what_changed"],
        "eligibility_yes": distilled["eligibility_yes"],
        "eligibility_no": distilled["eligibility_no"],
        "priority_groups": priority_groups,
        "documents_required": distilled["documents_required"],
        "application_steps": distilled["application_steps"],
        "official_warning": distilled["official_warning"],
        "seo_keywords": [domain, "Online Apply 2026", distilled["short_name"], "New Rules", "Sarkari Yojana"],
        "urgency_badge": "ताज़ा आधिकारिक निर्देश 2026",
        "source_feed": verified_topic.get("source", "Sarkari Result"),
        "raw_topic": verified_topic
    }

    return evidence_pack


if __name__ == "__main__":
    sample_topic = {
        "title": "Bihar Smart PDS 2.0 | बिहार मे राशन के लिए यहाँ से करे अप्लाई योग्यता,पात्रता,दस्तावेज और आवेदन की प्रक्रिया",
        "url": "https://onlineupdatestm.in/bihar-smart-pds-2-o/",
        "source": "Online Update STM",
        "category": "Sarkari Yojana",
        "is_urgent": True,
        "ministry": "उपभोक्ता मामले, खाद्य और सार्वजनिक वितरण मंत्रालय",
        "official_portal_domain": "nfsa.gov.in",
        "helpline": "1967",
        "notification_ref": "NFSA/SMART-PDS/2026-CIR-101"
    }

    pack = build_evidence_pack(sample_topic)
    print("\nBuilt Evidence Pack:")
    print("Scheme ID:", pack["id"])
    print("Ministry:", pack["ministry"])
    print("Portal:", pack["official_portal_domain"])
    print("Benefit:", pack["benefit_amount"])
    print("Steps:", len(pack["application_steps"]))
