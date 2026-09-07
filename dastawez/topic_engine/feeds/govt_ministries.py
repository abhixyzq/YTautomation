"""
iDastawez Topic Engine - Govt Ministries Feed
Direct official releases from Press Information Bureau (PIB), MyGov,
and official verified central ministries (MoHFW, DFPD, Agriculture, Finance, MeitY).
"""

import re
import ssl
import logging
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any

from dastawez.topics import VERIFIED_GOVT_SCHEMES

logger = logging.getLogger("topic_engine.ministries")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[Govt Ministries Feed] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

PIB_RSS_URL = "https://pib.gov.in/RssMain.aspx?ModId=6"


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_govt_ministries_feed(max_items: int = 10) -> List[Dict[str, Any]]:
    """
    Combines live PIB RSS press releases with verified central government scheme registries.
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    ministry_items = []

    # 1. Live PIB Press Releases (Cabinet Decisions, Schemes, Orders)
    try:
        req = urllib.request.Request(PIB_RSS_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()
        root = ET.fromstring(data)
        items = root.findall(".//item")
        for it in items[:8]:
            title = it.find("title").text if it.find("title") is not None else ""
            link = it.find("link").text if it.find("link") is not None else ""
            pub_date = it.find("pubDate").text if it.find("pubDate") is not None else ""
            desc = it.find("description").text if it.find("description") is not None else ""

            if not title or len(title) < 10:
                continue

            # Only keep citizen welfare, scheme, or regulatory press releases
            if re.search(r"(cabinet|scheme|yojana|ration|kisan|health|ayushman|pension|portal|guidelines|approval)", title, re.IGNORECASE):
                ministry_items.append({
                    "title": title.strip(),
                    "url": link.strip(),
                    "source": "PIB (Press Information Bureau)",
                    "category": "केंद्रीय कैबिनेट व मंत्रालय प्रेस विज्ञप्ति",
                    "base_score": 38,
                    "is_urgent": bool(re.search(r"(deadline|extended|last date|approval)", title, re.IGNORECASE)),
                    "is_new": True,
                    "published_at": pub_date or datetime.now().isoformat(),
                    "description": (desc or "")[:200],
                    "raw_text": title
                })
    except Exception as e:
        logger.warning(f"Could not fetch PIB RSS: {e}")

    # 2. Verified Knowledge Base of Central Schemes (as steady fallback)
    for sc in VERIFIED_GOVT_SCHEMES:
        ministry_items.append({
            "title": sc["scheme_name_hi"],
            "url": sc.get("portal_url", f"https://{sc.get('official_portal_domain', 'gov.in')}"),
            "source": "Govt Ministries Registry",
            "category": sc.get("category", "सरकारी योजनाएं एवं नागरिक सेवाएं"),
            "base_score": 35,
            "is_urgent": bool(sc.get("urgency_badge")),
            "is_new": False,
            "published_at": datetime.now().isoformat(),
            "description": sc.get("latest_official_update", ""),
            "raw_text": f"{sc['scheme_name_hi']} {sc.get('ministry', '')}",
            "scheme_data": sc
        })

    logger.info(f"Govt Ministries Feed: Loaded {len(ministry_items)} official ministry items.")
    return ministry_items[:max_items]


if __name__ == "__main__":
    items = fetch_govt_ministries_feed(5)
    print(f"Fetched {len(items)} items from Govt Ministries:")
    for idx, it in enumerate(items):
        print(f"{idx+1}. [{it['category']}] {it['title']}")
