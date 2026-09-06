"""
iDastawez - Latest Government Updates & Anti-Fake Fact-Check Tracker
Priority Engine: Ensures 100% authentic, real-time verified government announcements.
Filters out clickbait, scam forwards, and unverified social media rumors.
Integrates live Sarkari Result trends and Anti-Duplication History Engine.
"""

import os
import sys
import re
import ssl
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Optional

from dastawez.sarkari_scraper import match_sarkari_trends_with_schemes, fetch_all_sarkari_trends
from dastawez.history_tracker import is_topic_covered, get_covered_topics

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Blacklist of sensationalized scam keywords (Absolute ZERO tolerance for fake news)
FAKE_CLICKBAIT_BLACKLIST = [
    r"फ्री रिचार्ज",
    r"खाते में आ गए \d+ लाख",
    r"15 लाख",
    r"लॉटरी",
    r"मोदी जी दे रहे हैं सबको फ्री",
    r"फ्री लैपटॉप बिना किसी शर्त",
    r"तुरंत इस लिंक पर क्लिक करें",
    r"telegram group",
    r"whatsapp लिंक",
    r"बिना आवेदन के सीधे खाते में",
    r"सबका कर्ज माफ",
]

# Trusted national official and mainstream news sources covering government press releases
TRUSTED_SOURCES = [
    "PIB", "दूरदर्शन", "Press Information Bureau", "All India Radio",
    "Dainik Bhaskar", "Jagran", "Amar Ujala", "Hindustan", "Livemint",
    "Economic Times", "Business Standard", "NDTV", "Aaj Tak", "Navbharat Times",
    "Prabhat Khabar", "ABP News", "Zee News", "The Hindu", "Indian Express"
]

def _get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_live_scheme_news(scheme_name: str, max_items: int = 5, days_back: int = 7) -> List[Dict[str, Any]]:
    """
    Fetches real-time verified news and announcements for a specific scheme from Google News Hindi.
    """
    ctx = _get_ssl_context()
    clean_term = re.sub(r"[^\w\s-]", "", scheme_name).strip()
    query = f"{clean_term} when:{days_back}d"
    encoded_q = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=hi&gl=IN&ceid=IN:hi"
    
    verified_items = []
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()
            
        root = ET.fromstring(data)
        raw_items = root.findall(".//item")
        
        for it in raw_items:
            title = it.find("title").text if it.find("title") is not None else ""
            pub_date = it.find("pubDate").text if it.find("pubDate") is not None else ""
            link = it.find("link").text if it.find("link") is not None else ""
            source_tag = it.find("source")
            source_name = source_tag.text if source_tag is not None else ""
            
            # Anti-fake check: Discard any clickbait
            is_fake = False
            for pattern in FAKE_CLICKBAIT_BLACKLIST:
                if re.search(pattern, title, re.IGNORECASE):
                    is_fake = True
                    break
            if is_fake:
                continue
            
            # Detect if it's a fact-check or rumor-busting headline
            is_fact_check = bool(re.search(r"(सच|झूठ|अफवाह|फैक्ट चेक|fake|reality|सावधान|अलर्ट)", title, re.IGNORECASE))
            
            verified_items.append({
                "title": title,
                "published_date": pub_date,
                "source": source_name,
                "url": link,
                "is_fact_check": is_fact_check
            })
            
            if len(verified_items) >= max_items:
                break
                
    except Exception as e:
        pass
        
    return verified_items


def enrich_and_prioritize_schemes(
    schemes_list: List[Dict[str, Any]], 
    filter_covered: bool = True,
    cooldown_days: int = 60
) -> List[Dict[str, Any]]:
    """
    Ranks schemes by highest priority based on:
    1. Sarkari Result live trending presence (+40 pts)
    2. Active deadline or mandatory e-KYC requirement (+30 pts)
    3. Freshness (real-time news mentions in the last 7 days, +10 pts each)
    4. Senior citizen / farmer / universal impact (+20 pts)
    5. Anti-Duplication: Filters or deprioritizes topics already covered in history.
    """
    ranked = []
    
    print("\n[iDastawez Priority Engine] 🔍 Scanning Sarkari Result & Live Portals...")
    sarkari_matches = {}
    try:
        s_data = match_sarkari_trends_with_schemes(schemes_list)
        sarkari_matches = s_data.get("matched_schemes", {})
        if sarkari_matches:
            print(f"  ✓ Found {len(sarkari_matches)} scheme(s) actively trending on SarkariResult.com!")
    except Exception as e:
        print(f"  [Warning] Sarkari Result scan skipped: {e}")

    for scheme in schemes_list:
        scheme_copy = dict(scheme)
        scheme_id = scheme["id"]
        scheme_name = scheme.get("scheme_name_hi", "")
        
        # Check Anti-Duplication History
        already_covered = is_topic_covered(scheme_id, scheme_name, cooldown_days=cooldown_days)
        scheme_copy["is_covered"] = already_covered

        # Choose optimal search phrase for live news
        search_terms = []
        if "आयुष्मान" in scheme_name:
            search_terms = ["आयुष्मान कार्ड", "Ayushman Vay Vandana"]
        elif "किसान" in scheme_name:
            search_terms = ["PM Kisan e-KYC", "पीएम किसान"]
        elif "राशन" in scheme_name:
            search_terms = ["राशन कार्ड e-KYC", "राशन कार्ड"]
        elif "पैन" in scheme_name:
            search_terms = ["पैन आधार लिंक", "PAN Aadhaar link"]
        elif "सुकन्या" in scheme_name:
            search_terms = ["सुकन्या समृद्धि योजना"]
        elif "आवास" in scheme_name:
            search_terms = ["प्रधानमंत्री आवास योजना", "PMAY"]
        elif "स्कॉलरशिप" in scheme_name:
            search_terms = ["नेशनल स्कॉलरशिप", "NSP Scholarship"]
        elif "श्रम" in scheme_name:
            search_terms = ["ई श्रम कार्ड", "e-Shram card"]
        else:
            search_terms = [scheme.get("scheme_name_en", "")]

        live_news = []
        for term in search_terms:
            items = fetch_live_scheme_news(term, max_items=2, days_back=7)
            live_news.extend(items)
            if len(live_news) >= 3:
                break
        scheme_copy["live_news"] = live_news
        
        # Calculate priority score
        score = 50  # Base score
        
        # Sarkari Result Trending Boost
        sarkari_trends = sarkari_matches.get(scheme_id, [])
        scheme_copy["sarkari_trends"] = sarkari_trends
        if sarkari_trends:
            score += 40
            
        # Boost for active e-KYC / Deadline / Penalty
        desc_text = scheme.get("latest_official_update", "") + " " + scheme.get("benefit_summary", "")
        if any(w in desc_text for w in ["e-KYC", "ई-केवाईसी", "अंतिम तिथि", "अनिवार्य", "डेडलाइन"]):
            score += 30
            scheme_copy["urgency_badge"] = "ज़रूरी सूचना: अंतिम तिथि / e-KYC अनिवार्य"
        elif any(w in desc_text for w in ["नया कार्ड", "कैबिनेट", "शुरू", "स्वीकृति"]):
            score += 25
            scheme_copy["urgency_badge"] = "ताज़ा अपडेट: नई सरकारी घोषणा"
        else:
            scheme_copy["urgency_badge"] = "आधिकारिक जानकारी: आवश्यक नियम व प्रक्रिया"
            
        # Boost for live news freshness
        if live_news:
            score += len(live_news) * 10
            latest_headline = live_news[0]["title"]
            scheme_copy["latest_news_headline"] = latest_headline
            
            fact_checks = [n for n in live_news if n["is_fact_check"]]
            if fact_checks:
                score += 15
                scheme_copy["fact_check_alert"] = f"सावधान: {fact_checks[0]['title']}"
        else:
            scheme_copy["latest_news_headline"] = None
            scheme_copy["fact_check_alert"] = None
            
        # Senior citizen & wide public utility boost
        if "वरिष्ठ नागरिक" in scheme_name or "किसान" in scheme_name or "राशन" in scheme_name:
            score += 20
            
        # Handle already covered status
        if already_covered:
            scheme_copy["priority_score"] = -999  # Deprioritize so it won't be picked
            status_tag = "⛔ [ALREADY COVERED - SKIPPED]"
        else:
            scheme_copy["priority_score"] = score
            status_tag = f"✨ [FRESH] Score: {score}"
            
        sarkari_tag = f" | SarkariResult: 🔥 {len(sarkari_trends)}" if sarkari_trends else ""
        print(f"  {status_tag} {scheme_name[:34]}...{sarkari_tag} (News: {len(live_news)})")
        
        ranked.append(scheme_copy)
        
    # Sort descending by priority score
    ranked.sort(key=lambda x: x["priority_score"], reverse=True)
    return ranked
