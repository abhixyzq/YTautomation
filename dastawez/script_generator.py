"""
iDastawez - Professional Hindi Script Generator for Government Schemes & Updates.
Generates 3.5 to 4-minute structured, crystal-clear Hindi explainer scripts.
100% Authentic, Direct, and Trust-Focused.
"""

import os
import sys
import logging
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath("."))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def generate_dastawez_script(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Constructs a highly structured 3.5-minute authentic Hindi video script
    covering: Hook/Benefit -> Eligibility -> Documents Checklist -> Application Steps -> Official Alert.
    """
    name_hi = scheme["scheme_name_hi"]
    ministry = scheme["ministry"]
    benefit = scheme["benefit_amount"]
    portal = scheme["portal_url"]
    helpline = scheme["helpline"]
    latest_update = scheme["latest_official_update"]
    warning = scheme["official_warning"]

    # Act 1: Hook & Scheme Overview (00:00 - 00:35)
    news_headline_text = f"हाल ही में जारी ताज़ा रिपोर्ट के अनुसार: {scheme.get('latest_news_headline')}। " if scheme.get('latest_news_headline') else ""
    fact_check_text = f"सोशल मीडिया पर चल रही अफवाहों से सावधान रहें: {scheme.get('fact_check_alert')}। " if scheme.get('fact_check_alert') else ""

    act1_dialogue = (
        f"नमस्कार, iDastawez पर आपका स्वागत है। "
        f"सरकारी योजनाओं और आधिकारिक नियमों की सटीक जानकारी की श्रृंखला में आज का यह वीडियो बेहद महत्वपूर्ण है। "
        f"{news_headline_text}"
        f"{ministry} द्वारा {name_hi} को लेकर एक बड़ा आधिकारिक फैसला और निर्देश जारी किया गया है, "
        f"जिसके तहत पात्र नागरिकों को {benefit} का सीधा लाभ सुनिश्चित किया जा रहा है। "
        f"{latest_update} "
        f"आज हम जानेंगे कि इस योजना के लिए कौन पात्र है, किन दस्तावेज़ों की ज़रूरत होगी, "
        f"और आप आधिकारिक पोर्टल पर बिना किसी दलाल के घर बैठे कैसे आवेदन या e-KYC कर सकते हैं।"
    )

    # Act 2: Patrata - Kisko Milega aur Kisko Nahi (00:35 - 01:25)
    yes_points_str = "। इसके अलावा, ".join(scheme["eligibility_yes"])
    no_points_str = "। साथ ही, ".join(scheme["eligibility_no"])
    act2_dialogue = (
        f"सबसे पहले बात करते हैं सबसे ज़रूरी पहलू की — यानी पात्रता (Eligibility)। "
        f"अक्सर अधूरी जानकारी के कारण लोग गलत फॉर्म भर देते हैं और उनका आवेदन निरस्त हो जाता है। "
        f"ध्यान से सुनिए कि इस योजना के लिए कौन पात्र है: {yes_points_str}। "
        f"अब यह भी जान लीजिए कि कौन लोग इस योजना में आवेदन नहीं कर सकते ताकि आपका समय बर्बाद न हो: "
        f"{no_points_str}। "
        f"यदि आप इन सभी पात्रताओं को पूरा करते हैं, तो चलिए देखते हैं कि आवेदन के लिए आपके पास कौन से दस्तावेज़ तैयार होने चाहिए।"
    )

    # Act 3: Zaroori Dastawez Checklist (01:25 - 02:15)
    docs_str = "। दूसरा महत्वपूर्ण दस्तावेज़ है ".join(scheme["documents_required"])
    act3_dialogue = (
        f"दस्तावेज़ों की सूची को बहुत ध्यान से नोट कर लीजिए, क्योंकि ऑनलाइन पोर्टल पर यही कागज़ात अपलोड करने होंगे। "
        f"पहला सबसे अनिवार्य दस्तावेज़ है {docs_str}। "
        f"विशेष ध्यान रखें कि आपके आधार कार्ड में आपका चालू मोबाइल नंबर लिंक होना चाहिए, "
        f"क्योंकि ओटीपी सत्यापन के बिना फॉर्म आगे नहीं बढ़ेगा। "
        f"इसके अलावा, आपके बैंक खाते में एनपीसीआई और आधार सीडिंग एक्टिव होनी चाहिए, "
        f"ताकि सरकार द्वारा भेजी गई सहायता राशि बिना किसी रुकावट सीधे आपके खाते में क्रेडिट हो सके।"
    )

    # Act 4: Step-by-Step Online Apply / Portal Guide (02:15 - 03:20)
    steps = scheme["application_steps"]
    step_texts = []
    for s in steps:
        step_texts.append(f"स्टेप {s['step']}: {s['title']} — {s['desc']}")
    steps_dialogue = " ".join(step_texts)

    act4_dialogue = (
        f"अब बात करते हैं आवेदन की पूरी प्रक्रिया (Step-by-Step Online Process) की। "
        f"आपको किसी भी दलाल या एजेंट के पास जाने की आवश्यकता नहीं है, आप स्वयं अपने मोबाइल या कंप्यूटर से आवेदन कर सकते हैं। "
        f"{steps_dialogue} "
        f"जैसे ही आपका आवेदन सफलतापूर्वक जमा होगा, आपको स्क्रीन पर एक एप्लीकेशन रेफरेंस नंबर मिलेगा। "
        f"उस नंबर को सुरक्षित नोट कर लें, ताकि आप भविष्य में अपने आवेदन की स्थिति ट्रैक कर सकें।"
    )

    # Act 5: Official Alert & Help Desk (03:20 - 03:45)
    act5_dialogue = (
        f"अंत में सबसे महत्वपूर्ण आधिकारिक चेतावनी: {warning} "
        f"{fact_check_text}"
        f"इस योजना की एकमात्र आधिकारिक वेबसाइट है {portal}। "
        f"किसी भी फर्जी वेबसाइट या व्हाट्सएप लिंक पर अपनी निजी जानकारी साझा न करें। "
        f"यदि आपको आवेदन करने में कोई भी तकनीकी समस्या या संदेह हो, तो सरकार के राष्ट्रीय हेल्पलाइन नंबर {helpline} पर सीधे संपर्क कर सकते हैं। "
        f"इस आधिकारिक पोर्टल का सीधा लिंक हमने नीचे वीडियो के डिस्क्रिप्शन बॉक्स में दे दिया है। "
        f"अगर यह जानकारी आपको उपयोगी लगी हो, तो इस वीडियो को अपने परिवार और दोस्तों के साथ व्हाट्सएप पर ज़रूर शेयर करें, "
        f"और सरकारी योजनाओं की हर सच्ची व प्रमाणित अपडेट के लिए iDastawez को अभी सब्सक्राइब करें। धन्यवाद, जय हिन्द!"
    )

    full_script = f"{act1_dialogue}\n\n{act2_dialogue}\n\n{act3_dialogue}\n\n{act4_dialogue}\n\n{act5_dialogue}"
    word_count = len(full_script.split())

    # Build Structured Scene Storyboard for Remotion Hindi Infographics
    scenes = [
        {
            "scene_id": 1,
            "act_name": "योजना परिचय एवं लाभ",
            "dialogue": act1_dialogue,
            "layout_type": "scheme_overview",
            "scheme_name": name_hi,
            "ministry": ministry,
            "benefit_highlight": benefit,
            "latest_update": latest_update,
            "portal_url": portal
        },
        {
            "scene_id": 2,
            "act_name": "पात्रता (Eligibility)",
            "dialogue": act2_dialogue,
            "layout_type": "eligibility_card",
            "scheme_name": name_hi,
            "eligibility_yes": scheme["eligibility_yes"],
            "eligibility_no": scheme["eligibility_no"]
        },
        {
            "scene_id": 3,
            "act_name": "ज़रूरी दस्तावेज़ (Documents)",
            "dialogue": act3_dialogue,
            "layout_type": "documents_checklist",
            "scheme_name": name_hi,
            "documents": scheme["documents_required"],
            "bank_note": "आधार-NPCI सक्रिय बैंक खाता अनिवार्य"
        },
        {
            "scene_id": 4,
            "act_name": "आवेदन प्रक्रिया (Step-by-Step)",
            "dialogue": act4_dialogue,
            "layout_type": "step_by_step_flow",
            "scheme_name": name_hi,
            "ministry": ministry,
            "steps": scheme["application_steps"],
            "application_steps": scheme["application_steps"],
            "portal_url": portal
        },
        {
            "scene_id": 5,
            "act_name": "महत्वपूर्ण चेतावनी व हेल्पलाइन",
            "dialogue": act5_dialogue,
            "layout_type": "official_alert",
            "scheme_name": name_hi,
            "ministry": ministry,
            "portal_url": portal,
            "helpline": helpline,
            "warning": warning
        }
    ]

    # Generate High-CTR YouTube Title & Description
    yt_title = f"{scheme['scheme_name_en']} 2026: {scheme['benefit_amount']} | ऑनलाइन आवेदन व लिस्ट चेक करें"
    if len(yt_title) > 95:
        yt_title = f"{scheme['scheme_name_en'][:40]} 2026: {scheme['benefit_amount']} | Apply Online Guide"

    yt_description = f"""🇮🇳 {name_hi} - सम्पूर्ण जानकारी एवं ऑनलाइन आवेदन प्रक्रिया (2026)

📌 आधिकारिक पोर्टल (Official Portal Link):
👉 {portal}

📞 आधिकारिक राष्ट्रीय हेल्पलाइन नंबर: {helpline}
🏛️ संबंधित मंत्रालय: {ministry}

इस वीडियो में हमने विस्तार से बताया है:
1️⃣ {name_hi} क्या है और इसके तहत {benefit} का लाभ कैसे मिलेगा?
2️⃣ कौन-कौन से नागरिक इसके लिए पात्र हैं और कौन अपात्र हैं?
3️⃣ आवेदन करने के लिए कौन-कौन से ज़रूरी दस्तावेज़ (Documents) चाहिए?
4️⃣ मोबाइल से घर बैठे ऑनलाइन फॉर्म भरने और लिस्ट में नाम चेक करने का Step-by-Step तरीका।
5️⃣ महत्वपूर्ण आधिकारिक चेतावनी और दिशा-निर्देश।

🔔 भारत सरकार और राज्य सरकारों की हर ताज़ा योजना, भर्ती और दस्तावेज़ की 100% सटीक जानकारी के लिए @iDastawez को अभी SUBSCRIBE करें!

#iDastawez #{scheme['id']} #SarkariYojana2026 #GovernmentSchemes #OnlineApply #{scheme['category'].split()[0]}

⚠️ अस्वीकरण (Disclaimer):
iDastawez एक स्वतंत्र सूचनात्मक मंच है। हम केवल सरकार के आधिकारिक पोर्टलों ({portal}) पर उपलब्ध सार्वजनिक जानकारी को आम नागरिकों के लिए सरल भाषा में प्रस्तुत करते हैं। आवेदन करने से पहले आधिकारिक वेबसाइट पर नियमों की पुष्टि अवश्य करें।
"""

    return {
        "scheme_id": scheme["id"],
        "title": yt_title,
        "description": yt_description,
        "category": scheme["category"],
        "target_duration_seconds": 210,  # ~3.5 minutes
        "word_count": word_count,
        "full_script": full_script,
        "scenes": scenes,
        "seo_tags": scheme.get("seo_keywords", ["SarkariYojana", "GovernmentSchemes", "iDastawez"])
    }


if __name__ == "__main__":
    from dastawez.topics import get_scheme_by_id
    sample_scheme = get_scheme_by_id("ayushman_senior_citizen_2026")
    script = generate_dastawez_script(sample_scheme)
    print(f"Generated Script for: {script['title']}")
    print(f"Total Words: {script['word_count']} (~{script['word_count'] / 1.7:.1f} seconds of speech)")
    print(f"Total Acts/Scenes: {len(script['scenes'])}")
    print("\n--- SAMPLE ACT 1 SCRIPT ---")
    print(script["scenes"][0]["dialogue"][:250] + "...")
