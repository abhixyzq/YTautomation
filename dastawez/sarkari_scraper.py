"""
iDastawez - Sarkari Result & Official Portals Live Trend Scraper
Discovers what is currently trending across India in government schemes,
recruitment deadlines, admit cards, certificates, and citizen portals.
"""

import sys
import ssl
import re
import urllib.request
import bs4
from typing import List, Dict, Any, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SARKARI_RESULT_URL = "https://www.sarkariresult.com/"


def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_all_sarkari_trends() -> Dict[str, List[Dict[str, Any]]]:
    """
    Scrapes SarkariResult.com and extracts trending items grouped by section:
    - 'Important' (Schemes, Voter ID, Scholarship, e-KYC, Certificates)
    - 'Latest Jobs' (Top Vacancies, Deadlines)
    - 'Certificate' (Degrees, TET Credentials)
    - 'Admit Card' (Major examinations)
    - 'Admission' (Central / State institutions)
    """
    ctx = _get_ssl_context()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "hi,en-US,en;q=0.9",
    }

    categorized_trends = {
        "Important": [],
        "Latest Jobs": [],
        "Certificate": [],
        "Admit Card": [],
        "Admission": []
    }

    try:
        req = urllib.request.Request(SARKARI_RESULT_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        soup = bs4.BeautifulSoup(html, "html.parser")

        # Find category header blocks
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)
            matched_cat = None
            text_lower = text.lower()
            
            if "job" in text_lower and len(text) < 25:
                matched_cat = "Latest Jobs"
            elif "important" in text_lower and len(text) < 25:
                matched_cat = "Important"
            elif "certificate" in text_lower and len(text) < 35:
                matched_cat = "Certificate"
            elif "admit" in text_lower and len(text) < 25:
                matched_cat = "Admit Card"
            elif "admission" in text_lower and len(text) < 25:
                matched_cat = "Admission"

            if matched_cat and matched_cat in categorized_trends:
                ul = p.find_next("ul")
                if ul:
                    items = ul.find_all("li")
                    for li in items:
                        a = li.find("a")
                        if not a:
                            continue
                        title = a.get_text(strip=True)
                        href = a.get("href", "").strip()
                        if not title or len(title) < 5:
                            continue

                        # Detect urgency / deadline hints
                        is_urgent = bool(re.search(r"(last date|अंतिम तिथि|extended|deadline|closing|today)", title, re.IGNORECASE))
                        is_new = bool(re.search(r"(online form|apply online|शुरू|new|declared)", title, re.IGNORECASE))

                        entry = {
                            "title": title,
                            "url": href,
                            "category": matched_cat,
                            "is_urgent": is_urgent,
                            "is_new": is_new,
                            "source": "SarkariResult.com"
                        }
                        
                        # Avoid duplicates in section
                        if not any(e["title"] == title for e in categorized_trends[matched_cat]):
                            categorized_trends[matched_cat].append(entry)

    except Exception as e:
        print(f"[Sarkari Scraper Warning] Failed to scrape {SARKARI_RESULT_URL}: {e}")

    return categorized_trends


def match_sarkari_trends_with_schemes(schemes_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Checks all verified government schemes against live Sarkari Result trends.
    Returns:
      - 'matched_schemes': list of schemes currently trending on Sarkari Result
      - 'raw_trends': all raw categorized trends
    """
    raw_trends = fetch_all_sarkari_trends()
    all_trend_titles = []
    for cat_items in raw_trends.values():
        for item in cat_items:
            all_trend_titles.append(item["title"].lower())

    enriched_matches = {}

    for scheme in schemes_list:
        scheme_id = scheme["id"]
        scheme_name_hi = scheme.get("scheme_name_hi", "").lower()
        scheme_name_en = scheme.get("scheme_name_en", "").lower()
        keywords = scheme.get("seo_keywords", [])

        matched_trend_items = []
        for cat, items in raw_trends.items():
            for item in items:
                title_lower = item["title"].lower()
                
                # Direct scheme name checks
                if "राशन" in scheme_name_hi and any(k in title_lower for k in ["ration", "राशन"]):
                    matched_trend_items.append(item)
                elif "किसान" in scheme_name_hi and any(k in title_lower for k in ["kisan", "pm kisan", "किसान"]):
                    matched_trend_items.append(item)
                elif "आयुष्मान" in scheme_name_hi and any(k in title_lower for k in ["ayushman", "आयुष्मान"]):
                    matched_trend_items.append(item)
                elif "स्कॉलरशिप" in scheme_name_hi and any(k in title_lower for k in ["scholarship", "स्कॉलरशिप"]):
                    matched_trend_items.append(item)
                elif "पैन" in scheme_name_hi and any(k in title_lower for k in ["pan", "aadhaar", "पैन"]):
                    matched_trend_items.append(item)
                elif "आवास" in scheme_name_hi and any(k in title_lower for k in ["awas", "आवास"]):
                    matched_trend_items.append(item)
                elif "श्रम" in scheme_name_hi and any(k in title_lower for k in ["shram", "श्रम"]):
                    matched_trend_items.append(item)
                elif "सुकन्या" in scheme_name_hi and any(k in title_lower for k in ["sukanya", "सुकन्या"]):
                    matched_trend_items.append(item)

        if matched_trend_items:
            enriched_matches[scheme_id] = matched_trend_items

    return {
        "matched_schemes": enriched_matches,
        "raw_trends": raw_trends
    }


if __name__ == "__main__":
    trends = fetch_all_sarkari_trends()
    print("\n" + "="*70)
    print("🇮🇳 SARKARI RESULT LIVE TRENDING OVERVIEW")
    print("="*70)
    for cat, items in trends.items():
        print(f"\n[{cat}] ({len(items)} items)")
        for it in items[:5]:
            urgent_tag = " 🔥 [URGENT/DEADLINE]" if it["is_urgent"] else ""
            print(f"  • {it['title']}{urgent_tag}")
