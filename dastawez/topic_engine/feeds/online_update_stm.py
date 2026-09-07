"""
iDastawez Topic Engine - Online Update STM Feed (Priority #2)
Scrapes https://onlineupdatestm.in/ for real-time trending citizen schemes,
Bihar & Central government yojanas, student credit cards, scholarships, and smart PDS updates.
"""

import re
import ssl
import logging
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger("topic_engine.onlineupdatestm")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[OnlineUpdateSTM Feed] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

STM_FEEDS = [
    ("https://onlineupdatestm.in/category/sarkari-yojana/feed/", "Sarkari Yojana", 45),
    ("https://onlineupdatestm.in/feed/", "Latest Portal Updates", 40),
    ("https://onlineupdatestm.in/category/scholarship/feed/", "Scholarship & Education", 38),
]


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_online_update_stm_feed(max_items: int = 15) -> List[Dict[str, Any]]:
    """
    Fetches trending citizen schemes and updates from OnlineUpdateSTM RSS feeds.
    Extracts titles, descriptions, links, and publication dates.
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "hi,en-US,en;q=0.9",
    }

    all_items = []
    seen_titles = set()

    for feed_url, default_cat, base_prio in STM_FEEDS:
        try:
            req = urllib.request.Request(feed_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                data = resp.read()

            root = ET.fromstring(data)
            items = root.findall(".//item")
            for it in items:
                title_elem = it.find("title")
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                link_elem = it.find("link")
                link = link_elem.text.strip() if link_elem is not None and link_elem.text else ""
                pubdate_elem = it.find("pubDate")
                pub_date = pubdate_elem.text.strip() if pubdate_elem is not None and pubdate_elem.text else ""
                desc_elem = it.find("description")
                raw_desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                clean_desc = re.sub(r"<[^>]+>", "", raw_desc).strip()

                if not title or len(title) < 8:
                    continue

                # Deduplicate by normalized title
                norm_title = re.sub(r"\s+", " ", title).strip().lower()
                if norm_title in seen_titles:
                    continue
                seen_titles.add(norm_title)

                is_urgent = bool(re.search(r"(last date|अंतिम तिथि|extended|deadline|closing|today|जल्दी करे|आवेदन शुरू)", title, re.IGNORECASE))
                is_new = bool(re.search(r"(online apply|आवेदन शुरू|जारी|new|out|घोषित|शुरू)", title, re.IGNORECASE))

                # Boost score if it mentions major welfare keywords (eKYC, PDS, Loan, Pension)
                score = base_prio
                if re.search(r"(ekyc|e-kyc|राशन|pds|लोन|पेंशन|स्कॉलरशिप|scholarship|pm |योजना)", title, re.IGNORECASE):
                    score += 5

                all_items.append({
                    "title": title,
                    "url": link,
                    "source": "Online Update STM",
                    "category": default_cat,
                    "base_score": score,
                    "is_urgent": is_urgent,
                    "is_new": is_new,
                    "published_at": pub_date or datetime.now().isoformat(),
                    "description": clean_desc[:250],
                    "raw_text": f"{title} {clean_desc[:120]}"
                })

        except Exception as e:
            logger.warning(f"Error reading OnlineUpdateSTM feed {feed_url}: {e}")

    # Sort by base score descending
    all_items.sort(key=lambda x: x["base_score"], reverse=True)
    logger.info(f"OnlineUpdateSTM Feed: Extracted {len(all_items)} unique scheme topics.")
    return all_items[:max_items]


if __name__ == "__main__":
    items = fetch_online_update_stm_feed(10)
    print(f"Fetched {len(items)} items from OnlineUpdateSTM:")
    for idx, it in enumerate(items):
        print(f"{idx+1}. [{it['category']}] (Score: {it['base_score']}) {it['title']}")
