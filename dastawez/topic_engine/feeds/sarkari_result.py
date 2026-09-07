"""
iDastawez Topic Engine - Sarkari Result Feed (Priority #1)
Scrapes https://www.sarkariresult.com/ for real-time trending government schemes,
recruitment notifications, e-KYC updates, admit cards, and certificates.
"""

import re
import ssl
import logging
import urllib.request
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import bs4
except ImportError:
    bs4 = None

logger = logging.getLogger("topic_engine.sarkari")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[SarkariResult Feed] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

SARKARI_RESULT_URL = "https://www.sarkariresult.com/"


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_sarkari_result_feed(max_items: int = 15) -> List[Dict[str, Any]]:
    """
    Fetches real-time topics from SarkariResult.com.
    Prioritizes 'Important' (schemes, e-KYC, certificates) followed by 'Latest Jobs' & 'Admit Card'.
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "hi,en-US,en;q=0.9",
    }

    try:
        req = urllib.request.Request(SARKARI_RESULT_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        logger.warning(f"Failed to fetch SarkariResult homepage: {e}")
        return []

    if not bs4:
        logger.warning("BeautifulSoup not installed. Falling back to regex parsing.")
        return _parse_sarkari_regex(html, max_items)

    soup = bs4.BeautifulSoup(html, "html.parser")
    feed_items = []

    # Target key sections on SarkariResult
    category_map = {
        "important": ("Important Schemes & Services", 55),
        "latest jobs": ("Latest Government Jobs", 50),
        "certificate verification": ("Certificate Verification", 48),
        "admit card": ("Admit Card / Exam Update", 45),
        "admission": ("Central / State Admission", 42),
    }

    for p in soup.find_all(["p", "div"]):
        header_text = p.get_text(strip=True).lower()
        matched_cat = None
        base_priority = 50

        for key, (cat_label, prio) in category_map.items():
            if key in header_text and len(header_text) < 35:
                matched_cat = cat_label
                base_priority = prio
                break

        if matched_cat:
            ul = p.find_next("ul")
            if not ul:
                continue
            for li in ul.find_all("li"):
                a = li.find("a")
                if not a:
                    continue
                title = a.get_text(strip=True)
                href = a.get("href", "").strip()
                if not title or len(title) < 6:
                    continue

                if href and not href.startswith("http"):
                    href = urllib.parse.urljoin(SARKARI_RESULT_URL, href)

                # Check urgency keywords
                is_urgent = bool(re.search(r"(last date|अंतिम तिथि|extended|deadline|closing|today|last chance)", title, re.IGNORECASE))
                is_new = bool(re.search(r"(online form|apply online|शुरू|new|declared|out)", title, re.IGNORECASE))

                feed_items.append({
                    "title": title,
                    "url": href,
                    "source": "Sarkari Result",
                    "category": matched_cat,
                    "base_score": base_priority,
                    "is_urgent": is_urgent,
                    "is_new": is_new,
                    "published_at": datetime.now().isoformat(),
                    "raw_text": f"{title} {matched_cat}"
                })

    # Deduplicate within feed
    unique_items = []
    seen_titles = set()
    for it in feed_items:
        clean_t = re.sub(r"\s+", " ", it["title"]).strip().lower()
        if clean_t not in seen_titles:
            seen_titles.add(clean_t)
            unique_items.append(it)

    logger.info(f"SarkariResult Feed: Extracted {len(unique_items)} unique live topics.")
    return unique_items[:max_items]


def _parse_sarkari_regex(html: str, max_items: int) -> List[Dict[str, Any]]:
    pattern = r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.IGNORECASE)
    items = []
    seen = set()

    for href, raw_title in matches:
        title = re.sub(r'<[^>]+>', '', raw_title).strip()
        if len(title) > 12 and "sarkari" in href.lower():
            if title.lower() not in seen:
                seen.add(title.lower())
                items.append({
                    "title": title,
                    "url": href,
                    "source": "Sarkari Result",
                    "category": "Sarkari Update",
                    "base_score": 50,
                    "is_urgent": bool(re.search(r"(last date|अंतिम तिथि|deadline)", title, re.IGNORECASE)),
                    "is_new": bool(re.search(r"(apply online|new|online form)", title, re.IGNORECASE)),
                    "published_at": datetime.now().isoformat(),
                    "raw_text": title
                })
        if len(items) >= max_items:
            break
    return items


if __name__ == "__main__":
    items = fetch_sarkari_result_feed(10)
    print(f"Fetched {len(items)} items from SarkariResult:")
    for idx, it in enumerate(items):
        print(f"{idx+1}. [{it['category']}] (Score: {it['base_score']}) {it['title']}")
