"""
iDastawez - Natural Conversational Hinglish Script Generator
Transforms complex government directives into clear, engaging, conversational
explainer scripts. Zero bureaucratic robotic cadence. Zero Hindi+English duplicate reading.
Crystal-clear pronunciation for iDastawez.
"""

import sys
import os
import re
import json
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def clean_for_speech(text: str) -> str:
    """Strips parenthetical notes, acronym duplicates, and formatting symbols from spoken dialogue."""
    if not text:
        return ""
    # Remove any parenthetical notes/acronyms/translations like (PMGKAY), (MoHFW), (ट्यूशन फीस व भत्ता)
    # This prevents the voiceover from reading both Hindi and English back-to-back.
    cleaned = re.sub(r"\s*\([^)]*\)", "", text)
    # Remove formatting artifacts
    cleaned = re.sub(r"['\"`]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def clean_news_headline(headline: Optional[str]) -> str:
    """Extracts only the core Hindi headline, removing trailing English slugs and publisher names."""
    if not headline:
        return ""
    # Strip after " - " if followed by English characters
    h = re.split(r'\s+-\s+[a-zA-Z]{3,}', headline)[0].strip()
    # Strip parenthetical English
    h = clean_for_speech(h)
    # Strip trailing publisher dashes
    h = re.sub(r"\s*-\s*(Jagran|Amar Ujala|Bhaskar|Livemint|NDTV|Aaj Tak|Prabhat Khabar).*$", "", h, flags=re.IGNORECASE).strip()
    return h


def generate_dastawez_script(scheme: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a natural, human, conversational Hinglish explainer script.
    Zero robotic feel. Simple, everyday spoken language that ordinary citizens understand effortlessly.
    """
    name_raw = scheme.get("scheme_name_hi", "")
    name_clean = clean_for_speech(name_raw)
    ministry_clean = clean_for_speech(scheme.get("ministry", "संबंधित सरकारी विभाग"))
    benefit_clean = clean_for_speech(scheme.get("benefit_amount", scheme.get("benefit_summary", "सरकारी लाभ")))
    portal = scheme.get("portal_url", "")
    portal_domain = scheme.get("official_portal_domain", portal.replace("https://", "").replace("http://", "").split("/")[0])
    helpline = scheme.get("helpline", "1967")
    warning_clean = clean_for_speech(scheme.get("official_warning", "किसी भी दलाल को कोई शुल्क न दें।"))
    what_changed_data = scheme.get("what_changed", {})
    topic_type = scheme.get("topic_type", "benefit_scheme")

    evidence_data = {
        "ministry": scheme.get("ministry"),
        "notification_ref": scheme.get("notification_ref", "MoRD/PMAY-G/Phase-2/2026"),
        "portal_url": portal,
        "official_portal_domain": portal_domain,
        "last_verified_date": scheme.get("last_verified_date", "सितंबर 2026"),
        "source_citation": scheme.get("source_citation", f"{ministry_clean} आधिकारिक निर्देश"),
        "helpline": helpline
    }

    # Clean headline for natural inclusion
    raw_news = scheme.get("latest_news_headline")
    cleaned_news = clean_news_headline(raw_news)
    news_dialogue_hook = f"ताज़ा अपडेट के अनुसार—{cleaned_news}। " if cleaned_news else ""

    # Common Source Verification Dialogue (Natural, human, not robotic)
    source_dialogue = (
        f"इस पूरी जानकारी की पुष्टि आप आधिकारिक सरकारी पोर्टल {portal_domain} पर जाकर खुद भी कर सकते हैं। "
        f"यह पूरा अपडेट {ministry_clean} के आधिकारिक निर्देशों पर आधारित है। "
        f"किसी भी सरकारी नियम की सही और सटीक जानकारी के लिए हमेशा सरकारी डोमेन जीओवी डॉट इन पर ही भरोसा करें। "
        f"सच्ची और निष्पक्ष नागरिक जानकारी के लिए आई दस्तावेज़ को सब्सक्राइब ज़रूर करें। धन्यवाद, जय हिन्द!"
    )

    # Dynamic Contextual Subject Hook and Consequence
    if "पैन" in name_clean:
        topic_hook = "अगर आपके पास पैन कार्ड है या आप बैंक खाता और वित्तीय लेन-देन करते हैं"
        consequence = "आपका पैन कार्ड निष्क्रिय हो सकता है और बैंक या टैक्स से जुड़े काम रुक सकते हैं"
    elif "राशन" in name_clean:
        topic_hook = "अगर आपके परिवार में राशन कार्ड है या आप सरकारी राशन योजना का लाभ लेते हैं"
        consequence = "आपका राशन कार्ड अस्थाई रूप से ब्लॉक हो सकता है"
    elif "किसान" in name_clean:
        topic_hook = "अगर आप पीएम किसान सम्मान निधि योजना के लाभार्थी किसान हैं"
        consequence = "आपकी अगली किस्त का पैसा खाते में आने से रुक सकता है"
    elif "स्कॉलरशिप" in name_clean:
        topic_hook = "अगर आप सरकारी छात्रवृत्ति या स्कॉलरशिप के लिए आवेदन करने वाले हैं"
        consequence = "आपकी छात्रवृत्ति का आवेदन रुक सकता है"
    elif "आयुष्मान" in name_clean:
        topic_hook = "अगर आपके परिवार में वरिष्ठ नागरिक हैं या आप मुफ्त इलाज योजना से जुड़े हैं"
        consequence = "मुफ्त इलाज के नए कार्ड का लाभ मिलने में रुकावट आ सकती है"
    else:
        topic_hook = f"अगर आप {name_clean} से जुड़े हैं या इसका लाभ लेते हैं"
        consequence = "सरकारी सेवा या लाभ मिलने में रुकावट आ सकती है"

    scenes = []

    if topic_type == "regulatory_deadline":
        # 1. Overview Hook (Conversational, direct, human)
        act1_dialogue = (
            f"हेलो दोस्तों, आई दस्तावेज़ पर आपका स्वागत है। "
            f"{topic_hook}, तो सरकार का एक बहुत बड़ा और ज़रूरी नया अपडेट आया है। "
            f"{news_dialogue_hook}"
            f"सरकार ने सभी संबंधित नागरिकों के लिए यह प्रक्रिया पूरी करना ज़रूरी कर दिया है, ताकि आपका {benefit_clean} बिना किसी रुकावट के लगातार मिलता रहे। "
            f"आज के वीडियो में हम बहुत आसान भाषा में समझेंगे कि नया नियम क्या है, लास्ट डेट कब तक है, और आपको क्या करना होगा।"
        )
        scenes.append({
            "scene_id": 1,
            "act_name": "अधिसूचना एवं महत्व",
            "dialogue": act1_dialogue,
            "layout_type": "overview",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "benefit_highlight": benefit_clean,
            "latest_update": clean_for_speech(scheme.get("latest_official_update", "")),
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "urgency_badge": "ज़रूरी सूचना: अंतिम तिथि / e-KYC अनिवार्य",
            "evidence": evidence_data
        })

        # 2. What Changed (Clear before vs after)
        old_rule_clean = clean_for_speech(what_changed_data.get("old_rule", ""))
        new_rule_clean = clean_for_speech(what_changed_data.get("new_rule", ""))
        deadline_clean = clean_for_speech(what_changed_data.get("deadline", ""))

        act2_dialogue = (
            f"अब सबसे पहले यह समझ लेते हैं कि नियम में आख़िर क्या बड़ा बदलाव हुआ है। "
            f"पहले नियम यह था कि {old_rule_clean} "
            f"लेकिन अब नए सरकारी नियम के तहत, {new_rule_clean} "
            f"लास्ट डेट को लेकर साफ़ निर्देश है कि {deadline_clean}। "
            f"अगर आपने तय समय में यह प्रक्रिया पूरी नहीं करवाई, तो {consequence}।"
        )
        scenes.append({
            "scene_id": 2,
            "act_name": "नियम में क्या बदला",
            "dialogue": act2_dialogue,
            "layout_type": "what_changed",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "what_changed": what_changed_data,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 3. Who is Affected (Eligibility & Requirement)
        yes_items = [clean_for_speech(x) for x in scheme.get("eligibility_yes", [])]
        no_items = [clean_for_speech(x) for x in scheme.get("eligibility_no", [])]
        yes_str = "। इसके अलावा, ".join(yes_items[:3])
        no_str = "। वहीं दूसरी ओर, ".join(no_items[:2])

        act3_dialogue = (
            f"अब बात करते हैं कि यह नियम किन लोगों पर लागू होता है: {yes_str}। "
            f"और किन्हें इससे बाहर रखा गया है: {no_str}। "
            f"इसलिए अगर आप पूरी तरह पात्र हैं, तो इस वेरिफिकेशन में बिल्कुल भी देरी न करें।"
        )
        scenes.append({
            "scene_id": 3,
            "act_name": "पात्रता एवं अनिवार्यता",
            "dialogue": act3_dialogue,
            "layout_type": "eligibility_card",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "eligibility_yes": yes_items,
            "eligibility_no": no_items,
            "evidence": evidence_data
        })

        # 4. Step-by-Step Action (Simple, conversational step progression)
        steps = scheme.get("application_steps", [])
        step_phrases = []
        step_ordinals = ["पहला स्टेप", "दूसरा स्टेप", "तीसरा स्टेप", "चौथा स्टेप"]
        for idx, s in enumerate(steps[:4]):
            ord_name = step_ordinals[idx] if idx < len(step_ordinals) else f"स्टेप {idx+1}"
            s_title = clean_for_speech(s.get("title", ""))
            s_desc = clean_for_speech(s.get("desc", ""))
            step_phrases.append(f"{ord_name}—{s_title}, यानी {s_desc}")

        act4_dialogue = (
            f"अब देखते हैं कि आपको यह प्रक्रिया कैसे पूरी करनी है। "
            f"{' '.join(step_phrases)} "
            f"प्रक्रिया पूरी होने के बाद आधिकारिक पोर्टल पर अपना स्टेटस ज़रूर चेक कर लें कि आपका आवेदन या वेरिफिकेशन कम्प्लीट हुआ है या नहीं।"
        )
        scenes.append({
            "scene_id": 4,
            "act_name": "ऑनलाइन सत्यापन प्रक्रिया",
            "dialogue": act4_dialogue,
            "layout_type": "step_by_step_flow",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "application_steps": steps,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 5. Fraud Alert & Helpline
        act5_dialogue = (
            f"यहाँ पर एक बहुत ज़रूरी सावधानी का ध्यान रखें: {warning_clean} "
            f"यह पूरी सरकारी प्रक्रिया मुफ़्त होती है। किसी भी व्यक्ति को इसके लिए पैसे न दें, "
            f"और अनजान मैसेज में आए किसी भी फर्जी लिंक पर क्लिक न करें। "
            f"अगर आपको कोई भी समस्या आती है, तो आधिकारिक हेल्पलाइन {helpline} पर सीधे कॉल करके मदद ले सकते हैं।"
        )
        scenes.append({
            "scene_id": 5,
            "act_name": "सावधानी व हेल्पलाइन",
            "dialogue": act5_dialogue,
            "layout_type": "official_alert",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "warning": warning_clean,
            "evidence": evidence_data
        })

        # 6. Source Verification
        scenes.append({
            "scene_id": 6,
            "act_name": "आधिकारिक स्रोत सत्यापन",
            "dialogue": source_dialogue,
            "layout_type": "source_verification",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "evidence": evidence_data
        })

    else:
        # BENEFIT SCHEME (Ayushman, PM-Kisan, PMAY, SSY, NSP)
        # 1. Overview Hook (Friendly, clear, direct)
        act1_dialogue = (
            f"हेलो दोस्तों, आई दस्तावेज़ पर आपका स्वागत है। "
            f"आज हम बात कर रहे हैं {ministry_clean} द्वारा चलाई जा रही {name_clean} के बारे में। "
            f"{news_dialogue_hook}"
            f"इस योजना के तहत पात्र नागरिकों को {benefit_clean} का सीधा लाभ दिया जा रहा है। "
            f"{clean_for_speech(scheme.get('latest_official_update', ''))} "
            f"आज के वीडियो में हम बहुत आसान भाषा में समझेंगे कि इस योजना का लाभ किन्हें मिलेगा, कौन से दस्तावेज़ चाहिए, और अप्लाई कैसे करना है।"
        )
        scenes.append({
            "scene_id": 1,
            "act_name": "योजना परिचय एवं मुख्य लाभ",
            "dialogue": act1_dialogue,
            "layout_type": "overview",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "benefit_highlight": benefit_clean,
            "latest_update": clean_for_speech(scheme.get("latest_official_update", "")),
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "urgency_badge": "ताज़ा अपडेट: नई सरकारी घोषणा",
            "evidence": evidence_data
        })

        # 2. Eligibility
        yes_items = [clean_for_speech(x) for x in scheme.get("eligibility_yes", [])]
        no_items = [clean_for_speech(x) for x in scheme.get("eligibility_no", [])]
        yes_str = "। इसके अलावा, ".join(yes_items[:3])
        no_str = "। वहीं दूसरी तरफ, ".join(no_items[:2])

        act2_dialogue = (
            f"सबसे पहले पात्रता के नियम समझ लेते हैं कि किन्हें लाभ मिलेगा: {yes_str}। "
            f"अब यह भी जान लीजिए कि कौन लोग इसमें पात्र नहीं हैं: {no_str}। "
            f"अगर आप इन शर्तों को पूरा करते हैं, तो आपका आवेदन आसानी से स्वीकृत हो जाएगा।"
        )
        scenes.append({
            "scene_id": 2,
            "act_name": "पात्रता",
            "dialogue": act2_dialogue,
            "layout_type": "eligibility_card",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "eligibility_yes": yes_items,
            "eligibility_no": no_items,
            "evidence": evidence_data
        })

        # 3. Documents Checklist
        doc_items = [clean_for_speech(x) for x in scheme.get("documents_required", [])]
        docs_str = "। इसके साथ ही, ".join(doc_items[:4])
        act3_dialogue = (
            f"आवेदन के लिए आपको कौन-कौन से ज़रूरी दस्तावेज़ चाहिए, ध्यान से देख लें: {docs_str}। "
            f"खास बात यह ध्यान रखें कि आपका आधार कार्ड चालू मोबाइल नंबर से जुड़ा होना चाहिए, "
            f"और बैंक खाते में डीबीटी यानी प्रत्यक्ष लाभ अंतरण सक्रिय होना ज़रूरी है ताकि पैसा सीधे आपके खाते में आए।"
        )
        scenes.append({
            "scene_id": 3,
            "act_name": "आवश्यक दस्तावेज़",
            "dialogue": act3_dialogue,
            "layout_type": "documents_checklist",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "documents": doc_items,
            "bank_note": "आधार-डीबीटी सक्रिय बैंक खाता अनिवार्य",
            "evidence": evidence_data
        })

        # 4. Step-by-Step Application
        steps = scheme.get("application_steps", [])
        step_phrases = []
        step_ordinals = ["पहला स्टेप", "दूसरा स्टेप", "तीसरा स्टेप", "चौथा स्टेप"]
        for idx, s in enumerate(steps[:4]):
            ord_name = step_ordinals[idx] if idx < len(step_ordinals) else f"स्टेप {idx+1}"
            s_title = clean_for_speech(s.get("title", ""))
            s_desc = clean_for_speech(s.get("desc", ""))
            step_phrases.append(f"{ord_name}—{s_title}, जिसमें {s_desc}")

        act4_dialogue = (
            f"अब देखते हैं कि आवेदन की ऑनलाइन प्रक्रिया क्या है। "
            f"{' '.join(step_phrases)} "
            f"फॉर्म सफलतापूर्वक सबमिट होने के बाद अपना रसीद नंबर या एप्लिकेशन आईडी सुरक्षित ज़रूर रख लें।"
        )
        scenes.append({
            "scene_id": 4,
            "act_name": "आवेदन प्रक्रिया",
            "dialogue": act4_dialogue,
            "layout_type": "step_by_step_flow",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "application_steps": steps,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "evidence": evidence_data
        })

        # 5. Fraud Alert & Helpline
        act5_dialogue = (
            f"एक बहुत ज़रूरी बात का ध्यान रखें: {warning_clean} "
            f"किसी भी बिचौलिए या साइबर कैफे वाले को फालतू पैसे न दें। "
            f"अगर आपको कोई भी दिक्कत आती है, तो आधिकारिक राष्ट्रीय हेल्पलाइन {helpline} पर कॉल करके सीधे मदद पा सकते हैं।"
        )
        scenes.append({
            "scene_id": 5,
            "act_name": "सावधानी व हेल्पलाइन",
            "dialogue": act5_dialogue,
            "layout_type": "official_alert",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "warning": warning_clean,
            "evidence": evidence_data
        })

        # 6. Source Verification
        scenes.append({
            "scene_id": 6,
            "act_name": "आधिकारिक स्रोत सत्यापन",
            "dialogue": source_dialogue,
            "layout_type": "source_verification",
            "scheme_name": name_clean,
            "ministry": ministry_clean,
            "portal_url": portal,
            "official_portal_domain": portal_domain,
            "helpline": helpline,
            "evidence": evidence_data
        })

    # SEO metadata
    meta_title = f"{name_clean} 2026: {benefit_clean} | New Rules & Online Apply"
    meta_description = (
        f"{name_clean} 2026 के नए नियम, पात्रता, आवश्यक दस्तावेज और ऑनलाइन आवेदन की पूरी जानकारी। "
        f"आधिकारिक पोर्टल {portal_domain} पर कैसे करें सत्यापन। "
        f"हेल्पलाइन: {helpline}। सच्ची और प्रामाणिक नागरिक जानकारी के लिए @iDastawez को सब्सक्राइब करें।"
    )

    return {
        "title": meta_title,
        "description": meta_description,
        "category": scheme.get("category", "नागरिक कल्याण"),
        "scheme_id": scheme.get("id"),
        "scenes": scenes
    }
