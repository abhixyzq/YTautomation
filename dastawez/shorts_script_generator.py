"""
iDastawez - 9:16 Viral Shorts Script Generator
Crafts 35-45 second ultra-punchy, high-retention Hindi scripts for @iDastawez.
Follows the proven 4-beat structure:
1. Hook (0-3s): Stop-the-scroll psychological urgency.
2. Crisis / Rule Change (3-15s): What changed, new rules, or deadlines.
3. Action & Documents (15-32s): Required documents & exact steps to apply.
4. Official Portal & CTA (32-42s): Verification at .gov.in and subscribe @iDastawez.
"""

import sys
import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

logger = logging.getLogger("dastawez.shorts_script")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[iDastawez Shorts Script] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()


def clean_hindi_text(text: str) -> str:
    """Strips parenthetical notes, duplicate English acronyms, and formatting artifacts."""
    if not text:
        return ""
    # Remove parenthetical translations/acronyms like (PMGKAY), (Ration Card Copy)
    text = re.sub(r"\s*\([^)]*\)", "", text)
    # Strip markdown symbols
    text = re.sub(r"[\*#`_]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_dynamic_badge(scheme: Dict[str, Any]) -> tuple:
    """
    Returns (badge_text, bg_color_rgba, border_color_rgb) for the top pill.
    """
    title_text = scheme.get("scheme_name_hi", "") + " " + scheme.get("title", "")
    urgency = scheme.get("urgency_badge", "")
    topic_type = scheme.get("topic_type", "")

    if any(k in title_text for k in ["e-KYC", "eKYC", "केवाईसी", "अंतिम तिथि", "लास्ट डेट", "डेडलाइन"]) or "DEADLINE" in urgency:
        return ("● SARKARI ALERT // e-KYC DEADLINE", (225, 29, 72, 235), (255, 120, 150))  # Crimson
    elif any(k in title_text for k in ["राशन", "राशन कार्ड", "मुफ्त अनाज", "अन्न योजना"]):
        return ("● RATION CARD // NEW RULES 2026", (234, 88, 12, 235), (253, 186, 116))  # Orange
    elif any(k in title_text for k in ["आवेदन शुरू", "ऑनलाइन फॉर्म", "भर्ती", "रिजल्ट", "एडमिट कार्ड"]):
        return ("● SARKARI RESULT // LIVE UPDATE", (37, 99, 235, 235), (147, 197, 253))  # Royal Blue
    elif any(k in title_text for k in ["पेंशन", "किसान", "सम्मान निधि", "किस्त", "लाभ"]):
        return ("● YOJANA UPDATE // DIRECT BENEFIT", (16, 185, 129, 235), (110, 231, 183))  # Emerald Green
    else:
        return ("● GOVT DIRECTIVE // OFFICIAL ALERT", (220, 38, 38, 235), (254, 202, 202))


def generate_fallback_shorts_script(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Algorithmic zero-fail template generator when Gemini API is offline.
    Produces a crisp 35-45s script in natural spoken Hindi.
    """
    name_hi = clean_hindi_text(scheme.get("scheme_name_hi", scheme.get("title", "सरकारी योजना 2026")))
    ministry = clean_hindi_text(scheme.get("ministry", "संबंधित सरकारी विभाग"))
    portal_url = scheme.get("portal_url", "https://india.gov.in")
    portal_domain = scheme.get("official_portal_domain", portal_url.replace("https://", "").replace("http://", "").split("/")[0])
    benefit = clean_hindi_text(scheme.get("benefit_amount", scheme.get("benefit_summary", "सरकारी सहायता")))

    what_changed = scheme.get("what_changed", {})
    deadline = what_changed.get("deadline", "समय पर पूरा करना अनिवार्य है")
    new_rule = what_changed.get("new_rule", "नया नियम लागू कर दिया गया है")

    docs = scheme.get("documents_required", ["आधार कार्ड", "राशन कार्ड या बैंक पासबुक", "मोबाइल नंबर"])
    docs_str = " और ".join(clean_hindi_text(d) for d in docs[:3])

    # 1. Hook
    if "राशन" in name_hi:
        hook = "अगर आपके परिवार के पास राशन कार्ड है, तो ये एक जरूरी काम तुरंत निपटा लें वरना मुफ्त राशन बंद हो सकता है!"
        crisis = f"सरकार ने राशन कार्ड के लिए नया नियम लागू कर दिया है। अब परिवार के हर एक सदस्य का सत्यापन अनिवार्य है, और {deadline}।"
        action = f"इसके लिए आपको सिर्फ {docs_str} की ज़रूरत होगी। अपने नजदीकी राशन डीलर या CSC केंद्र पर जाकर e-KYC पूरा करें। इसके लिए कोई भी सरकारी फीस नहीं लगती।"
    elif "किसान" in name_hi:
        hook = "पीएम किसान की अगली किस्त को लेकर सरकार ने नया अलर्ट जारी किया है!"
        crisis = f"अगर आपने अभी तक बैंक खाते में आधार और NPCI लिंक नहीं कराया है, तो अगली किस्त खाते में नहीं आएगी। {deadline}।"
        action = f"अपने नजदीकी बैंक शाखा या पोस्ट ऑफिस जाकर DBT सक्रिय करवाएं। दस्तावेज़ में सिर्फ {docs_str} चाहिए।"
    else:
        hook = f"अगर आप {name_hi} का लाभ लेना चाहते हैं, तो सरकार का ये नया अपडेट ध्यान से सुनिए!"
        crisis = f"{ministry} ने नए दिशा-निर्देश जारी किए हैं। {new_rule}।"
        action = f"पात्र नागरिक {docs_str} के साथ तुरंत आवेदन कर सकते हैं। इसके लिए किसी भी दलाल को पैसे देने की ज़रूरत नहीं है।"

    cta = f"पूरी सूची और ऑनलाइन स्टेटस चेक करने के लिए आधिकारिक पोर्टल {portal_domain} पर जाएं। सरकारी योजनाओं की 100% सही जानकारी के लिए iDastawez को अभी सब्सक्राइब करें!"

    full_script = f"{hook} {crisis} {action} {cta}"

    badge_text, bg_col, border_col = get_dynamic_badge(scheme)

    clean_short_title = re.sub(r"[^\w\s\u0900-\u097F-]", "", name_hi).strip()
    if len(clean_short_title) > 50:
        clean_short_title = clean_short_title[:50]

    base_script_data = {
        "title": f"{clean_short_title} 2026: नया नियम व e-KYC | #Shorts #iDastawez",
        "hook": hook,
        "crisis": crisis,
        "action": action,
        "cta": cta,
        "full_script": full_script,
        "badge_text": badge_text,
        "badge_bg_color": bg_col,
        "badge_border_color": border_col,
        "headline": name_hi,
        "portal_domain": portal_domain,
        "ministry": ministry,
        "benefit": benefit,
        "tags": [
            "Shorts",
            "iDastawez",
            "SarkariYojana",
            "Yojana2026",
            "GovernmentSchemes",
            "eKYC",
            "OnlineApply",
            "SarkariUpdate"
        ]
    }

    base_script_data["storyboard"] = build_dastawez_storyboard(scheme, base_script_data)
    base_script_data["broll_queries"] = [sc["visual_query"] for sc in base_script_data["storyboard"]]
    base_script_data["scheme"] = scheme
    return base_script_data


def get_contextual_queries(scheme: Dict[str, Any]) -> Dict[str, List[str]]:
    """Returns scheme-specific, high-yield Pexels search queries."""
    text = (scheme.get("scheme_name_hi", "") + " " + scheme.get("title", "") + " " + scheme.get("id", "")).lower()

    if any(k in text for k in ["राशन", "ration", "अनाज", "खाद्य", "nfsa", "अन्न"]):
        return {
            "hook": ["wheat grain food distribution", "supermarket rice store", "flour bags food grocery"],
            "rules": ["biometric fingerprint scanner", "official government document stamp"],
            "docs": ["identity card verification", "aadhaar biometric authentication"],
            "portal": ["laptop computer typing website", "happy indian family eating"]
        }
    elif any(k in text for k in ["किसान", "kisan", "कृषि", "खेती", "फसल", "tractor", "सम्मान निधि"]):
        return {
            "hook": ["indian farmer tractor field", "wheat crop harvest green field"],
            "rules": ["counting money rupees cash", "bank official desk"],
            "docs": ["farmer hands soil agriculture", "biometric fingerprint scanner"],
            "portal": ["rural farm nature sunrise", "laptop mobile online check"]
        }
    elif any(k in text for k in ["स्कॉलरशिप", "scholarship", "छात्र", "शिक्षा", "college", "student", "ecss"]):
        return {
            "hook": ["college students classroom studying", "young student writing exam"],
            "rules": ["university library books students", "degree certificate document"],
            "docs": ["school girl studying notebook", "filling paperwork application"],
            "portal": ["graduate smiling success celebration", "laptop typing website"]
        }
    elif any(k in text for k in ["आवास", "awas", "मकान", "घर", "शौचालय", "toilet", "निर्माण"]):
        return {
            "hook": ["brick wall construction worker", "house building construction site"],
            "rules": ["architect blueprint house desk", "counting cash money bank"],
            "docs": ["construction tools building bricks", "official property documents"],
            "portal": ["happy family new home keys", "modern house exterior"]
        }
    elif any(k in text for k in ["आयुष्मान", "ayushman", "इलाज", "स्वास्थ्य", "hospital", "doctor", "दवा"]):
        return {
            "hook": ["hospital doctor patient clinic", "doctor stethoscope medical checkup"],
            "rules": ["senior citizen healthcare hospital", "medicine pills pharmacy counter"],
            "docs": ["hospital reception counter", "biometric card verification"],
            "portal": ["healthy smiling family home", "modern hospital building"]
        }
    elif any(k in text for k in ["पैन", "pan", "आधार", "aadhaar", "bank", "बैंक", "खाता", "dbt", "npci"]):
        return {
            "hook": ["credit card banking transaction", "counting money cash counter"],
            "rules": ["official legal paperwork signature", "laptop cyber security office"],
            "docs": ["biometric fingerprint scanner", "identity card verification"],
            "portal": ["mobile banking smartphone app", "laptop typing website desk"]
        }
    else:
        return {
            "hook": ["indian citizen government office", "crowd indian citizens street"],
            "rules": ["official government document stamp", "computer office desk typing"],
            "docs": ["fingerprint biometric scanner", "paperwork signing desk"],
            "portal": ["laptop typing website online", "happy indian citizens smiling"]
        }


def build_dastawez_storyboard(scheme: Dict[str, Any], script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Builds an authentic, 6 to 9 scene storyboard mapping each spoken Hindi sentence
    directly to 100% relevant, topic-matched B-roll queries (Tech-channel quality).
    """
    q_map = get_contextual_queries(scheme)
    full_script = script_data.get("full_script", "").strip()
    
    # Split into discrete sentences
    raw_sentences = [s.strip() for s in re.split(r'[।\.\!\?\n]+', full_script) if len(s.strip()) > 6]
    
    # Fallback if sentence splitting is empty
    if not raw_sentences:
        raw_sentences = [
            script_data.get("hook", ""),
            script_data.get("crisis", ""),
            script_data.get("action", ""),
            script_data.get("cta", "")
        ]
        raw_sentences = [s for s in raw_sentences if s]

    storyboard = []
    used_queries = set()

    for idx, sentence in enumerate(raw_sentences):
        s_lower = sentence.lower()
        selected_query = None

        # 1. RATION / FOOD / GRAIN KEYWORDS
        if any(w in s_lower for w in ["राशन", "अनाज", "गेहूं", "चावल", "खाद्य", "कोटा", "nfsa", "मुफ्त राशन", "राशन कार्ड"]):
            candidates = ["wheat grain food distribution", "supermarket grocery food", "supermarket rice store"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 2. BIOMETRIC / e-KYC / FINGERPRINT KEYWORDS
        elif any(w in s_lower for w in ["बायोमेट्रिक", "kyc", "ekyc", "ई-केवाईसी", "फिंगरप्रिंट", "सत्यापन", "अंगूठा", "otp", "ओटीपी"]):
            candidates = ["biometric fingerprint scanner", "thumb impression scanning", "biometric card verification"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 3. FARMER / CROPS / FIELD / TRACTOR KEYWORDS
        elif any(w in s_lower for w in ["किसान", "खेती", "कृषि", "ट्रैक्टर", "फसल", "खेत", "खाद", "यूरिया", "भू-सत्यापन", "खतौनी"]):
            candidates = ["indian farmer tractor field", "wheat crop harvest field", "farmer hands soil agriculture"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 4. CASH / BANK / MONEY / DBT / FEE / INSTALLMENT KEYWORDS
        elif any(w in s_lower for w in ["किस्त", "खाता", "रुपये", "पैसा", "बैंक", "फीस", "मुफ्त", "dbt", "npci", "पैसे", "लाख", "हजार"]):
            candidates = ["counting money cash", "bank official desk counter", "atm cash machine"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 5. CSC / SERVICE CENTER / DEALER / SHOP
        elif any(w in s_lower for w in ["csc", "केंद्र", "डीलर", "दुकान", "कैफे", "शाखा", "कार्यालय", "काउंटर"]):
            candidates = ["customer service desk counter", "cyber cafe computer typing", "government office desk"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 6. OFFICIAL DOCUMENTS / AADHAAR / PAN / ID CARD
        elif any(w in s_lower for w in ["आधार", "aadhaar", "pan", "पैन", "दस्तावेज़", "कागजात", "पहचान", "कार्ड"]):
            candidates = ["identity card verification", "official government document stamp", "paperwork signing desk"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 7. PORTAL / ONLINE WEBSITE / SMARTPHONE / DOWNLOAD
        elif any(w in s_lower for w in ["पोर्टल", "portal", "वेबसाइट", "gov.in", "ऑनलाइन", "स्टेटस", "चेक", "डाउनलोड", "लिंक"]):
            candidates = ["laptop typing website", "smartphone mobile app scroll", "computer typing screen"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 8. HEALTH / DOCTOR / HOSPITAL / MEDICINE
        elif any(w in s_lower for w in ["अस्पताल", "डॉक्टर", "इलाज", "दवा", "मरीज", "स्वास्थ्य", "आयुष्मान", "बीमारी", "क्लिनिक"]):
            candidates = ["hospital doctor clinic", "doctor stethoscope checkup", "pharmacy medicine counter"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 9. HOUSING / BRICK / HOME / CONSTRUCTION
        elif any(w in s_lower for w in ["मकान", "घर", "दीवार", "ईंट", "निर्माण", "शौचालय", "आवास", "छत"]):
            candidates = ["brick wall construction worker", "house building construction", "modern home keys"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 10. STUDENTS / EDUCATION / COLLEGE / EXAM
        elif any(w in s_lower for w in ["छात्र", "पढ़ाई", "स्कूल", "कॉलेज", "परीक्षा", "विद्यार्थी", "स्कॉलरशिप"]):
            candidates = ["college students classroom", "student writing exam notebook", "university library books"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 11. SUBSCRIBE / IDASTAWEZ / CITIZEN FAMILY / GOOD NEWS
        elif any(w in s_lower for w in ["सब्सक्राइब", "idastawez", "परिवार", "खुशखबरी", "नागरिक", "शेयर"]):
            candidates = ["happy indian family", "happy rural citizens smiling", "indian citizen government office"]
            for c in candidates:
                if c not in used_queries:
                    selected_query = c
                    break
            if not selected_query:
                selected_query = candidates[0]

        # 12. Contextual Scheme Fallback if no specific keyword triggered
        if not selected_query:
            if idx == 0:
                selected_query = q_map["hook"][0]
            elif idx == len(raw_sentences) - 1:
                selected_query = q_map["portal"][0]
            elif idx < len(raw_sentences) // 2:
                selected_query = q_map["rules"][idx % len(q_map["rules"])]
            else:
                selected_query = q_map["docs"][idx % len(q_map["docs"])]

        used_queries.add(selected_query)
        storyboard.append({
            "scene_id": idx + 1,
            "beat": f"scene_{idx + 1}",
            "narration_part": sentence,
            "visual_query": selected_query
        })

    return storyboard


def generate_shorts_script(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main generator: Uses Gemini 1.5 Flash if API key is configured;
    falls back gracefully to robust algorithmic templates.
    """
    fallback_data = generate_fallback_shorts_script(scheme)

    if not GEMINI_API_KEY:
        logger.info("GEMINI_API_KEY not configured. Using high-retention fallback Hindi Shorts script.")
        return fallback_data

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        
        candidate_models = ["gemini-flash-latest", "gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-1.5-pro"]
        model = None
        for m in candidate_models:
            try:
                model = genai.GenerativeModel(m)
                break
            except Exception:
                continue
        if not model:
            model = genai.GenerativeModel("gemini-flash-latest")

        scheme_summary = json.dumps({
            "name": scheme.get("scheme_name_hi", scheme.get("title")),
            "ministry": scheme.get("ministry"),
            "benefit": scheme.get("benefit_amount", scheme.get("benefit_summary")),
            "portal": scheme.get("portal_url"),
            "what_changed": scheme.get("what_changed"),
            "documents": scheme.get("documents_required", []),
            "urgent": scheme.get("urgency_badge")
        }, ensure_ascii=False)

        prompt = f"""You are the head scriptwriter for '@iDastawez', India's premier civic-tech YouTube channel.
Write a VIRAL 35-45 second Hindi YouTube Short script about this government announcement:
{scheme_summary}

RULES FOR 100% MAXIMUM VIEWER RETENTION:
1. Spoken Language: Natural, conversational Hindi (Hinglish spoken style like a sharp news anchor).
2. NO bureaucratic robot language. Speak directly to the viewer ("अगर आपके पास राशन कार्ड है...").
3. DO NOT read parenthetical English translations or acronym repetitions.
4. Total length MUST be between 85 and 110 words so it speaks in exactly 38-44 seconds.
5. Structure:
   - "hook" (15-20 words): Irresistible urgency or warning in the first 3 seconds.
   - "crisis" (25-30 words): What changed, new rules, or deadline.
   - "action" (30-35 words): What exact documents to carry and where to go (CSC, dealer, or portal).
   - "cta" (15-20 words): Direct them to the official .gov.in portal domain and tell them to subscribe to @iDastawez.

Return STRICT JSON matching this schema:
{{
  "title": "High CTR YouTube Shorts Title (under 60 chars) | #Shorts #iDastawez",
  "hook": "Spoken hook text",
  "crisis": "Spoken crisis/rule text",
  "action": "Spoken action steps and documents text",
  "cta": "Spoken portal and subscribe call to action",
  "full_script": "All 4 parts merged into continuous dialogue",
  "headline": "Short scheme headline for card (under 35 chars)",
  "broll_queries": ["query1", "query2", "query3"]
}}
"""
        resp = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json", "temperature": 0.3}
        )
        data = json.loads(resp.text)
        
        # Blend with fallback metadata
        data["badge_text"] = fallback_data["badge_text"]
        data["badge_bg_color"] = fallback_data["badge_bg_color"]
        data["badge_border_color"] = fallback_data["badge_border_color"]
        data["portal_domain"] = fallback_data["portal_domain"]
        data["ministry"] = fallback_data["ministry"]
        data["benefit"] = fallback_data["benefit"]
        data["tags"] = fallback_data["tags"]

        # Ensure full_script is constructed if missing
        if not data.get("full_script"):
            data["full_script"] = f"{data.get('hook', '')} {data.get('crisis', '')} {data.get('action', '')} {data.get('cta', '')}".strip()

        data["storyboard"] = build_dastawez_storyboard(scheme, data)
        data["broll_queries"] = [sc["visual_query"] for sc in data["storyboard"]]
        data["scheme"] = scheme

        logger.info(f"Generated viral Hindi Shorts script via Gemini: '{data.get('title')}'")
        return data

    except Exception as e:
        logger.warning(f"Gemini script generation error: {e}. Using verified algorithmic script.")
        return fallback_data


if __name__ == "__main__":
    from dastawez.topics import VERIFIED_GOVT_SCHEMES
    sample = VERIFIED_GOVT_SCHEMES[0]
    script = generate_shorts_script(sample)
    print("\n--- SHORTS SCRIPT PREVIEW ---")
    print("Title:", script["title"])
    print("Full Script:\n", script["full_script"])
    print("Badge:", script["badge_text"])
