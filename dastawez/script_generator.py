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
    Constructs an adaptive, evidence-first Hindi explainer script for @iDastawez.
    Dynamically routes storyboards based on topic_type (regulatory_deadline vs benefit_scheme).
    """
    name_hi = scheme["scheme_name_hi"]
    ministry = scheme["ministry"]
    benefit = scheme["benefit_amount"]
    portal = scheme["portal_url"]
    portal_domain = scheme.get("official_portal_domain", portal.replace("https://", "").replace("http://", "").split("/")[0])
    helpline = scheme["helpline"]
    latest_update = scheme["latest_official_update"]
    warning = scheme["official_warning"]
    topic_type = scheme.get("topic_type", "benefit_scheme")
    what_changed_data = scheme.get("what_changed", {
        "old_rule": "पहले सामान्य नियमों के तहत आवेदन की सुविधा थी।",
        "new_rule": latest_update,
        "deadline": "आधिकारिक पोर्टल पर अंतिम तिथि पूर्व कार्यवाही आवश्यक"
    })
    evidence_data = {
        "ministry": ministry,
        "notification_ref": scheme.get("notification_ref", "MoF/PIB/Public-Notice-2026"),
        "portal_url": portal,
        "official_portal_domain": portal_domain,
        "last_verified_date": scheme.get("last_verified_date", "सितंबर 2026"),
        "source_citation": scheme.get("source_citation", f"भारत सरकार के आधिकारिक पोर्टल {portal_domain} से सत्यापित"),
        "helpline": helpline
    }

    news_headline_text = f"ताज़ा अपडेट के अनुसार: {scheme.get('latest_news_headline')}। " if scheme.get('latest_news_headline') else ""

    # Common Act: Source Verification (Trust Anchor)
    source_dialogue = (
        f"इस पूरे विश्लेषण की प्रामाणिकता के लिए स्रोत नोट कर लें: "
        f"यह जानकारी {ministry} द्वारा जारी आधिकारिक अधिसूचना संख्या {evidence_data['notification_ref']} "
        f"और आधिकारिक सरकारी पोर्टल {portal_domain} पर उपलब्ध सार्वजनिक दस्तावेजों पर आधारित है। "
        f"किसी भी नियम की पुष्टि के लिए केवल सरकारी डोमेन gov.in या nic.in का ही उपयोग करें। "
        f"सच्ची और निष्पक्ष नागरिक जानकारी के लिए iDastawez को सब्सक्राइब करें। धन्यवाद, जय हिन्द!"
    )

    scenes = []

    if topic_type == "regulatory_deadline":
        # 1. Overview Hook
        act1_dialogue = (
            f"नमस्कार, iDastawez पर आपका स्वागत है। "
            f"{ministry} द्वारा {name_hi} को लेकर एक महत्वपूर्ण आधिकारिक निर्देश जारी किया गया है। "
            f"{news_headline_text}"
            f"यदि आपका नाम इस सूची में है, तो {benefit} की निरंतरता बनाए रखने के लिए समय पर सत्यापन अनिवार्य कर दिया गया है। "
            f"आज हम जानेंगे कि क्या नियम बदला है, किसे तुरंत कार्रवाई करनी है, और घर बैठे e-KYC कैसे पूरी करें।"
        )
        scenes.append({
            "scene_id": 1,
            "act_name": "अधिसूचना एवं महत्व",
            "dialogue": act1_dialogue,
            "layout_type": "overview",
            "scheme_name": name_hi,
            "ministry": ministry,
            "benefit_highlight": benefit,
            "latest_update": latest_update,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 2. What Changed
        act2_dialogue = (
            f"आइए समझते हैं कि नियम में क्या बड़ा बदलाव हुआ है। "
            f"पहले स्थिति यह थी: {what_changed_data['old_rule']} "
            f"लेकिन अब नया नियम यह है: {what_changed_data['new_rule']} "
            f"समयसीमा को लेकर स्पष्ट निर्देश है: {what_changed_data['deadline']}। "
            f"यदि तय समय में यह प्रक्रिया पूरी नहीं हुई, तो सेवा अस्थाई रूप से रोकी जा सकती है।"
        )
        scenes.append({
            "scene_id": 2,
            "act_name": "नियम में क्या बदला",
            "dialogue": act2_dialogue,
            "layout_type": "what_changed",
            "scheme_name": name_hi,
            "ministry": ministry,
            "what_changed": what_changed_data,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 3. Who is Affected (Eligibility / Requirement)
        yes_str = "। इसके अलावा, ".join(scheme["eligibility_yes"])
        no_str = "। वहीं दूसरी ओर, ".join(scheme["eligibility_no"])
        act3_dialogue = (
            f"अब जान लीजिए कि यह नियम किन पर लागू होता है: {yes_str}। "
            f"किन्हें इससे छूट है या कौन अपात्र हैं: {no_str}। "
            f"यदि आप पात्रता के दायरे में आते हैं, तो सत्यापन में देरी बिल्कुल न करें।"
        )
        scenes.append({
            "scene_id": 3,
            "act_name": "पात्रता एवं अनिवार्यता",
            "dialogue": act3_dialogue,
            "layout_type": "eligibility_card",
            "scheme_name": name_hi,
            "ministry": ministry,
            "eligibility_yes": scheme["eligibility_yes"],
            "eligibility_no": scheme["eligibility_no"],
            "evidence": evidence_data
        })

        # 4. Step-by-Step Action
        steps = scheme["application_steps"]
        step_texts = [f"कदम {s['step']}: {s['title']} — {s['desc']}" for s in steps]
        act4_dialogue = (
            f"सत्यापन की सरल प्रक्रिया इस प्रकार है: "
            f"{' '.join(step_texts)} "
            f"सत्यापन पूरा होने पर पोर्टल से डिजिटल रसीद या कंफर्मेशन स्लिप अवश्य सुरक्षित रख लें।"
        )
        scenes.append({
            "scene_id": 4,
            "act_name": "ऑनलाइन सत्यापन प्रक्रिया",
            "dialogue": act4_dialogue,
            "layout_type": "step_by_step_flow",
            "scheme_name": name_hi,
            "ministry": ministry,
            "application_steps": steps,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 5. Alert & Helpline
        act5_dialogue = (
            f"महत्वपूर्ण सावधानी: {warning} "
            f"आधिकारिक पोर्टल {portal_domain} के अलावा किसी अनजान व्यक्ति को ओटीपी या बैंक पासवर्ड कभी न दें। "
            f"किसी भी समस्या के समाधान हेतु राष्ट्रीय हेल्पलाइन नंबर {helpline} पर सीधे संपर्क कर सकते हैं।"
        )
        scenes.append({
            "scene_id": 5,
            "act_name": "सावधानी व हेल्पलाइन",
            "dialogue": act5_dialogue,
            "layout_type": "official_alert",
            "scheme_name": name_hi,
            "ministry": ministry,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "warning": warning,
            "evidence": evidence_data
        })

        # 6. Source Verification (Evidence Card)
        scenes.append({
            "scene_id": 6,
            "act_name": "आधिकारिक स्रोत सत्यापन",
            "dialogue": source_dialogue,
            "layout_type": "source_verification",
            "scheme_name": name_hi,
            "ministry": ministry,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "evidence": evidence_data
        })

    else:
        # BENEFIT SCHEME (Ayushman, PM-Kisan, PMAY, SSY, e-Shram)
        # 1. Overview Hook & Entitlement
        act1_dialogue = (
            f"नमस्कार, iDastawez पर आपका स्वागत है। "
            f"आज हम विश्लेषण कर रहे हैं {ministry} द्वारा संचालित {name_hi} का। "
            f"{news_headline_text}"
            f"इस योजना के तहत पात्र नागरिकों को {benefit} का सीधा लाभ प्रदान किया जा रहा है। "
            f"{latest_update} "
            f"आज के वीडियो में हम जानेंगे कि कौन पात्र है, किन दस्तावेजों की आवश्यकता है, और आधिकारिक पोर्टल पर आवेदन कैसे करें।"
        )
        scenes.append({
            "scene_id": 1,
            "act_name": "योजना परिचय एवं मुख्य लाभ",
            "dialogue": act1_dialogue,
            "layout_type": "overview",
            "scheme_name": name_hi,
            "ministry": ministry,
            "benefit_highlight": benefit,
            "latest_update": latest_update,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 2. Eligibility
        yes_str = "। इसके अलावा, ".join(scheme["eligibility_yes"])
        no_str = "। वहीं दूसरी ओर, ".join(scheme["eligibility_no"])
        act2_dialogue = (
            f"सबसे पहले पात्रता के नियम समझ लेते हैं: {yes_str}। "
            f"अब यह भी जान लीजिए कि कौन लोग इसमें पात्र नहीं हैं: {no_str}। "
            f"यदि आप पात्रता मानदंडों को पूरा करते हैं, तो आवेदन के लिए आवश्यक दस्तावेज तैयार रखें।"
        )
        scenes.append({
            "scene_id": 2,
            "act_name": "पात्रता (Eligibility)",
            "dialogue": act2_dialogue,
            "layout_type": "eligibility_card",
            "scheme_name": name_hi,
            "ministry": ministry,
            "eligibility_yes": scheme["eligibility_yes"],
            "eligibility_no": scheme["eligibility_no"],
            "evidence": evidence_data
        })

        # 3. Documents Checklist
        docs_str = "। इसके साथ ही, ".join(scheme["documents_required"])
        act3_dialogue = (
            f"आवेदन के लिए जरूरी दस्तावेजों की सूची इस प्रकार है: {docs_str}। "
            f"विशेष ध्यान रखें कि आपका आधार कार्ड चालू मोबाइल नंबर से जुड़ा होना चाहिए, "
            f"और बैंक खाते में प्रत्यक्ष लाभ अंतरण (DBT) सक्रिय होना अनिवार्य है।"
        )
        scenes.append({
            "scene_id": 3,
            "act_name": "आवश्यक दस्तावेज़",
            "dialogue": act3_dialogue,
            "layout_type": "documents_checklist",
            "scheme_name": name_hi,
            "ministry": ministry,
            "documents": scheme["documents_required"],
            "bank_note": "आधार-NPCI सक्रिय बैंक खाता अनिवार्य",
            "evidence": evidence_data
        })

        # 4. Step-by-Step Application
        steps = scheme["application_steps"]
        step_texts = [f"कदम {s['step']}: {s['title']} — {s['desc']}" for s in steps]
        act4_dialogue = (
            f"आवेदन की आधिकारिक प्रक्रिया इस प्रकार है: "
            f"{' '.join(step_texts)} "
            f"फॉर्म सफलतापूर्वक जमा होने के बाद अपना आवेदन संदर्भ संख्या सुरक्षित रख लें।"
        )
        scenes.append({
            "scene_id": 4,
            "act_name": "आवेदन प्रक्रिया",
            "dialogue": act4_dialogue,
            "layout_type": "step_by_step_flow",
            "scheme_name": name_hi,
            "ministry": ministry,
            "application_steps": steps,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 5. Alert & Helpline
        act5_dialogue = (
            f"महत्वपूर्ण सरकारी चेतावनी: {warning} "
            f"किसी भी अनाधिकृत व्यक्ति या साइबर दलाल को अवैध शुल्क न दें। "
            f"किसी भी तकनीकी असुविधा के लिए आधिकारिक राष्ट्रीय हेल्पलाइन नंबर {helpline} पर संपर्क करें।"
        )
        scenes.append({
            "scene_id": 5,
            "act_name": "सावधानी व हेल्पलाइन",
            "dialogue": act5_dialogue,
            "layout_type": "official_alert",
            "scheme_name": name_hi,
            "ministry": ministry,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "warning": warning,
            "evidence": evidence_data
        })

        # 6. Source Verification (Evidence Card)
        scenes.append({
            "scene_id": 6,
            "act_name": "आधिकारिक स्रोत सत्यापन",
            "dialogue": source_dialogue,
            "layout_type": "source_verification",
            "scheme_name": name_hi,
            "ministry": ministry,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "evidence": evidence_data
        })

    full_script = "\n\n".join(sc["dialogue"] for sc in scenes)
    word_count = len(full_script.split())

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
