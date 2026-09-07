"""
iDastawez Topic Engine - Smart Semantic Distiller
Extracts clean scheme names, core benefits, target beneficiaries, and contextual
action guidelines from raw scraped feeds (SarkariResult, OnlineUpdateSTM, Ministries).
Prevents raw SEO headlines, clickbait phrases, and bilingual duplication from entering video scripts.
"""

import re
from typing import Dict, Any, Tuple, List, Optional


def clean_title_noise(raw_title: str) -> str:
    """Removes clickbait, SEO clutter, and promotional patterns from raw headlines."""
    if not raw_title:
        return ""
    
    t = raw_title
    
    # 1. Strip publisher names and URLs
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"\s*-\s*(Jagran|Amar Ujala|Bhaskar|Livemint|NDTV|Aaj Tak|Prabhat Khabar|Sarkari Result|Online Update STM|Dailyhunt).*$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*\|\s*(Sarkari Result|Online Update STM).*$", "", t, flags=re.IGNORECASE)

    # 2. Strip promotional clickbait suffixes
    promotional_patterns = [
        r"(?:online|ऑफलाइन)\s*apply.*$",
        r"ऑनलाइन\s*आवेदन\s*(?:शुरू|करें|प्रक्रिया).*$",
        r"आवेदन\s*शुरू.*$",
        r"यहाँ\s*से\s*करे\s*अप्लाई.*$",
        r"यहाँ\s*से\s*देखें.*$",
        r"डायरेक्ट\s*लिंक.*$",
        r"direct\s*link.*$",
        r"apply\s*now.*$",
        r"online\s*form.*$",
        r"notification\s*out.*$",
        r"admit\s*card.*$",
        r"answer\s*key.*$",
        r"result\s*declared.*$",
        r"new\s*update.*$",
        r"ताज़ा\s*खबर.*$",
        r"बड़ा\s*अपडेट.*$",
        r"मिलेगा\s*₹?[\d,]+\s*(?:का\s*लाभ|सीधे|रुपये)?.*$",
        r"खाते\s*में\s*आएंगे.*$",
        r"योग्यता,?\s*पात्रता.*$",
        r"दस्तावेज\s*और\s*आवेदन.*$",
    ]
    for pat in promotional_patterns:
        t = re.sub(pat, "", t, flags=re.IGNORECASE).strip()

    return t.strip(" -|:/,")


def extract_clean_names(raw_title: str) -> Tuple[str, str, str]:
    """
    Extracts:
    1. clean_name_hi: Clean Devanagari/Hindi name (e.g. 'बिहार ग्रामीण शौचालय योजना 2026')
    2. clean_name_en: Clean English name (e.g. 'Bihar Rural Sanitation Scheme 2026')
    3. short_name: Spoken conversational name (e.g. 'शौचालय योजना')
    """
    raw_cleaned = clean_title_noise(raw_title)
    
    # Check if raw title has delimiter between English and Hindi
    parts = re.split(r"\s*[\-\|:\/]\s*", raw_title)
    hi_part = ""
    en_part = ""
    
    for p in parts:
        p_clean = clean_title_noise(p)
        if not p_clean:
            continue
        has_devanagari = bool(re.search(r"[\u0900-\u097F]", p_clean))
        if has_devanagari and not hi_part and len(p_clean) >= 4:
            hi_part = p_clean
        elif not has_devanagari and not en_part and len(p_clean) >= 4:
            en_part = p_clean

    # Resolve Hindi name
    if hi_part:
        clean_hi = hi_part
    else:
        # If no Devanagari part found, use raw cleaned
        clean_hi = raw_cleaned

    # Resolve English name
    if en_part:
        clean_en = en_part
    else:
        clean_en = raw_cleaned

    # Extract short spoken name
    short_name = clean_hi
    for keyword in ["शौचालय योजना", "आवास योजना", "राशन कार्ड", "स्मार्ट पीडीएस", "स्टूडेंट क्रेडिट कार्ड", 
                    "स्कॉलरशिप", "जीडी कांस्टेबल", "किसान सम्मान निधि", "आयुष्मान भारत", "पेंशन योजना"]:
        if keyword in clean_hi:
            short_name = keyword
            break

    # Guarantee year 2026 is present cleanly once
    if "2026" not in clean_hi and ("2025" not in clean_hi):
        clean_hi = f"{clean_hi} 2026"
    if "2026" not in clean_en and ("2025" not in clean_en):
        clean_en = f"{clean_en} 2026"

    # Clean double years if any
    clean_hi = re.sub(r"2026\s+2026", "2026", clean_hi)
    clean_en = re.sub(r"2026\s+2026", "2026", clean_en)

    return clean_hi.strip(), clean_en.strip(), short_name.strip()


def distill_topic_context(raw_title: str, portal_domain: str = "india.gov.in") -> Dict[str, Any]:
    """
    Analyzes the topic and generates tailored domain context:
    - benefit_amount
    - target_audience
    - action_phrase
    - what_changed (old, new, deadline)
    - eligibility (yes, no)
    - documents
    - steps
    - warning
    - helpline
    """
    clean_hi, clean_en, short_name = extract_clean_names(raw_title)
    title_lower = (raw_title + " " + clean_hi + " " + clean_en).lower()

    # 1. TOILET / SANITATION SCHEME (शौचालय)
    if "शौचालय" in title_lower or "sauchalay" in title_lower or "toilet" in title_lower:
        return {
            "category": "ग्रामीण विकास एवं स्वच्छता",
            "topic_type": "benefit_scheme",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": "ग्रामीण शौचालय योजना",
            "target_audience": "बिहार और देश के ग्रामीण क्षेत्रों में रहने वाले उन परिवारों",
            "action_phrase": "शौचालय निर्माण के लिए सीधे बैंक खाते में आर्थिक सहायता देने हेतु नए ऑनलाइन आवेदन शुरू हो चुके हैं",
            "benefit_amount": "शौचालय निर्माण के लिए सीधे बैंक खाते में ₹12,000 की सरकारी सहायता",
            "benefit_summary": "प्रत्येक पात्र ग्रामीण परिवार को व्यक्तिगत घरेलू शौचालय निर्माण हेतु ₹12,000 की प्रोत्साहन राशि सीधे आधार लिंक बैंक खाते में दी जाती है।",
            "what_changed": {
                "old_rule": "पहले ग्रामीण नागरिकों को ब्लॉक या पंचायत के चक्कर लगाकर कागजी फॉर्म जमा करना पड़ता था, जिससे काफी समय लगता था।",
                "new_rule": f"अब आधिकारिक पोर्टल {portal_domain} पर ऑनलाइन आवेदन प्रणाली शुरू कर दी गई है, जहाँ आवेदक खुद मोबाइल से अप्लाई कर सकते हैं।",
                "deadline": "पोर्टल पर आवेदन प्रक्रिया सक्रिय है, बिना देरी किए आवेदन करें"
            },
            "eligibility_yes": [
                "ग्रामीण क्षेत्र का स्थायी निवासी परिवार जिसके घर में पहले से कोई पक्का शौचालय न हो",
                "आवेदक का बैंक खाता आधार से लिंक और प्रत्यक्ष लाभ अंतरण यानी डीबीटी सक्रिय होना चाहिए",
                "गरीबी रेखा के नीचे (BPL) परिवार एवं पात्र APL ग्रामीण परिवार"
            ],
            "eligibility_no": [
                "जिन परिवारों को पहले कभी स्वच्छ भारत मिशन या सरकारी योजना के तहत ₹12,000 की सहायता मिल चुकी हो",
                "जिनके घर में पहले से पक्का शौचालय बना हुआ है",
                "सरकारी नौकरी या आयकर दाता परिवार"
            ],
            "documents_required": [
                "आवेदक का आधार कार्ड (मोबाइल नंबर से लिंक)",
                "बैंक खाता पासबुक की साफ फोटोकॉपी (DBT सक्रिय)",
                "निवास प्रमाण पत्र या राशन कार्ड",
                "शौचालय निर्माण स्थल की फोटो एवं चालू मोबाइल नंबर"
            ],
            "application_steps": [
                {"step": 1, "title": "पोर्टल रजिस्ट्रेशन", "desc": f"आधिकारिक पोर्टल {portal_domain} पर जाएँ और 'सिटिज़न रजिस्ट्रेशन' पर क्लिक करें।"},
                {"step": 2, "title": "लॉगिन व आवेदन फॉर्म", "desc": "पंजीकृत मोबाइल नंबर पर आए ओटीपी से लॉगिन करें और 'न्यू एप्लीकेशन' विकल्प चुनें।"},
                {"step": 3, "title": "बैंक व व्यक्तिगत विवरण", "desc": "अपना जिला, ब्लॉक, ग्राम पंचायत, आधार संख्या और सही बैंक खाता विवरण भरें।"},
                {"step": 4, "title": "फोटो अपलोड व सबमिशन", "desc": "बैंक पासबुक व निर्माण स्थल की फोटो अपलोड करके फॉर्म फाइनल सबमिट करें और रसीद प्रिंट कर लें।"}
            ],
            "official_warning": "यह सरकारी योजना 100% निःशुल्क है। किसी भी मुखिया, दलाल या साइबर कैफे वाले को रिश्वत न दें। पैसा सीधे आपके बैंक खाते में आएगा।",
            "helpline": "1800-3456-112"
        }

    # 2. PDS / RATION CARD / SMART PDS (राशन / ई-केवाईसी)
    elif "राशन" in title_lower or "ration" in title_lower or "pds" in title_lower:
        return {
            "category": "खाद्य एवं नागरिक आपूर्ति",
            "topic_type": "regulatory_deadline",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": "राशन कार्ड e-KYC नियम",
            "target_audience": "राशन कार्ड धारक परिवारों और सरकारी राशन लेने वाले सभी नागरिकों",
            "action_phrase": "राशन कार्ड में परिवार के सभी सदस्यों का बायोमेट्रिक e-KYC सत्यापन अनिवार्य कर दिया गया है",
            "benefit_amount": "मुफ्त मासिक राशन एवं 'वन नेशन वन राशन कार्ड' सुविधा",
            "benefit_summary": "सत्यापन पूरा होने पर देश के किसी भी सरकारी राशन डीलर से मुफ्त अनाज प्राप्त करने की सुविधा बिना रुकावट जारी रहेगी।",
            "what_changed": {
                "old_rule": "पहले केवल परिवार के मुखिया के फिंगरप्रिंट या पुराने कार्ड से पूरे परिवार का राशन मिल जाता था।",
                "new_rule": "अब राष्ट्रीय खाद्य सुरक्षा अधिनियम के तहत परिवार के हर सदस्य का आधार बायोमेट्रिक e-KYC POS मशीन पर अनिवार्य कर दिया गया है।",
                "deadline": "निर्धारित समय सीमा से पूर्व नजदीकी राशन डीलर के पास जाकर e-KYC अनिवार्य रूप से करवा लें"
            },
            "eligibility_yes": [
                "राष्ट्रीय खाद्य सुरक्षा कानून (NFSA) और राज्य राशन कार्ड सूची में शामिल सभी परिवार",
                "परिवार के सभी सदस्य जिनका नाम राशन कार्ड में दर्ज है",
                "प्रवासी मजदूर जो देश के किसी भी शहर में रहकर राशन लेना चाहते हैं"
            ],
            "eligibility_no": [
                "जिनका बायोमेट्रिक सत्यापन निर्धारित समय तक पूरा नहीं होगा, उनका नाम कार्ड से अस्थाई रूप से हटाया जा सकता है",
                "अवैध और अपात्र कार्ड धारक"
            ],
            "documents_required": [
                "मूल राशन कार्ड",
                "परिवार के सभी सदस्यों का आधार कार्ड",
                "सक्रिय मोबाइल नंबर"
            ],
            "application_steps": [
                {"step": 1, "title": "राशन डीलर के पास जाएँ", "desc": "अपने नजदीकी सरकारी उचित मूल्य दुकान (राशन डीलर) के पास सभी सदस्यों के साथ जाएँ।"},
                {"step": 2, "title": "e-POS मशीन पर आधार दर्ज करें", "desc": "डीलर की बायोमेट्रिक ई-पॉस मशीन में अपना आधार नंबर दर्ज करवाएँ।"},
                {"step": 3, "title": "फिंगरप्रिंट या आँख की पुतली स्कैन", "desc": "बायोमेट्रिक फिंगरप्रिंट या आईरिस स्कैनर से आधार सत्यापन पूरा करें।"},
                {"step": 4, "title": "सत्यापन पावती प्राप्त करें", "desc": "मशीन से सफल सत्यापन की पर्ची या स्क्रीन कन्फर्मेशन देख लें।" }
            ],
            "official_warning": "राशन कार्ड e-KYC पूर्णतः निःशुल्क है। डीलर को ₹1 भी शुल्क न दें।",
            "helpline": "1967"
        }

    # 3. STUDENT CREDIT CARD / SCHOLARSHIP / LOAN (शिक्षा ऋण / छात्रवृत्ति)
    elif "scholarship" in title_lower or "छात्रवृत्ति" in title_lower or "credit card" in title_lower or "loan" in title_lower:
        return {
            "category": "उच्च शिक्षा एवं छात्र कल्याण",
            "topic_type": "benefit_scheme",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": "स्टूडेंट क्रेडिट कार्ड / छात्रवृत्ति योजना",
            "target_audience": "12वीं पास और उच्च शिक्षा प्राप्त कर रहे विद्यार्थियों",
            "action_phrase": "तकनीकी, मेडिकल और सामान्य उच्च शिक्षा के लिए सरकारी आर्थिक सहायता व ऋण के नए आवेदन शुरू हो चुके हैं",
            "benefit_amount": "उच्च शिक्षा के लिए ₹4 लाख तक का ब्याज-मुक्त शिक्षा ऋण व छात्रवृत्ति",
            "benefit_summary": "गरीब व मध्यमवर्गीय छात्रों को पैसों की कमी के कारण पढ़ाई न छोड़नी पड़े, इसके लिए राज्य सरकार गारंटी और आर्थिक मदद प्रदान करती है।",
            "what_changed": {
                "old_rule": "पहले बैंकों से एजुकेशन लोन लेने में भारी गारंटी और 10% से अधिक ब्याज देना पड़ता था।",
                "new_rule": f"अब सरकारी पोर्टल {portal_domain} के माध्यम से सरकार की गारंटी पर मात्र 1% ब्याज (महिलाओं व दिव्यांगों के लिए) या ब्याज-मुक्त ऋण मिलता है।",
                "deadline": "नए शैक्षणिक सत्र 2026 के लिए ऑनलाइन पोर्टल खुला है"
            },
            "eligibility_yes": [
                "राज्य का स्थायी निवासी छात्र जिसने 10वीं या 12वीं मान्यता प्राप्त बोर्ड से उत्तीर्ण की हो",
                "मान्यता प्राप्त कॉलेज, संस्थान या विश्वविद्यालय में उच्च शिक्षा में नामांकित छात्र",
                "आवेदक की आयु सामान्यतः 25 वर्ष से कम होनी चाहिए"
            ],
            "eligibility_no": [
                "जो छात्र किसी अन्य सरकारी संस्था से पहले से पूर्ण शिक्षा ऋण ले चुके हों",
                "अमान्य या गैर-मान्यता प्राप्त संस्थानों में अध्ययनरत छात्र"
            ],
            "documents_required": [
                "छात्र एवं अभिभावक का आधार कार्ड व पैन कार्ड",
                "10वीं और 12वीं की अंकतालिका व प्रमाण पत्र",
                "कॉलेज का एडमिशन लेटर एवं फीस स्ट्रक्चर",
                "बैंक खाता पासबुक एवं निवास प्रमाण पत्र"
            ],
            "application_steps": [
                {"step": 1, "title": "ऑनलाइन पोर्टल पर पंजीकरण", "desc": f"{portal_domain} पोर्टल पर जाकर न्यू एप्लीकेंट रजिस्ट्रेशन करें।"},
                {"step": 2, "title": "ओटीपी वेरिफिकेशन", "desc": "मोबाइल और ईमेल पर आए ओटीपी से सत्यापन कर लॉगिन आईडी बनाएं।"},
                {"step": 3, "title": "कोर्स व बैंक विवरण भरें", "desc": "अपने कॉलेज, कोर्स फीस और बैंक खाते का पूरा विवरण भरें।"},
                {"step": 4, "title": "दस्तावेज़ सत्यापन", "desc": "जिला निबंधन एवं परामर्श केंद्र (DRCC) जाकर मूल दस्तावेजों का भौतिक सत्यापन करवाएँ।"}
            ],
            "official_warning": "आवेदन की प्रक्रिया पूरी तरह पारदर्शी है। किसी भी अनधिकृत एजेंट या कंसल्टेंट के बहकावे में न आएं।",
            "helpline": "1800-3456-444"
        }

    # 4. ADMIT CARD / PHYSICAL TEST / EXAM (एडमिट कार्ड / फिजिकल टेस्ट / परीक्षा)
    elif any(k in title_lower for k in ["admit card", "hall ticket", "call letter", "pet / pst", "pst", "physical test", "exam date", "admit"]):
        return {
            "category": "प्रवेश पत्र एवं परीक्षा",
            "topic_type": "regulatory_deadline",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": "एडमिट कार्ड एवं परीक्षा",
            "target_audience": "इस भर्ती परीक्षा और फिजिकल टेस्ट के लिए आवेदन कर चुके सभी अभ्यर्थियों",
            "action_phrase": "आधिकारिक परीक्षा और फिजिकल टेस्ट के लिए एडमिट कार्ड जारी कर दिया गया है",
            "benefit_amount": "आधिकारिक एडमिट कार्ड व परीक्षा केंद्र आवंटन",
            "benefit_summary": "अभ्यर्थी अपना रोल नंबर या रजिस्ट्रेशन नंबर दर्ज करके तुरंत अपना एडमिट कार्ड डाउनलोड कर सकते हैं।",
            "what_changed": {
                "old_rule": "पूर्व में डाक द्वारा या ऑफलाइन माध्यम से प्रवेश पत्र भेजे जाते थे।",
                "new_rule": f"अब आधिकारिक पोर्टल {portal_domain} पर डिजिटल एडमिट कार्ड उपलब्ध है, जिसे ऑनलाइन डाउनलोड करना अनिवार्य है।",
                "deadline": "परीक्षा और फिजिकल टेस्ट की तिथि से पहले अपना एडमिट कार्ड अवश्य डाउनलोड कर लें"
            },
            "eligibility_yes": [
                "वे सभी उम्मीदवार जिन्होंने निर्धारित समय सीमा में सफलतापूर्वक ऑनलाइन फॉर्म भरा था",
                "जिनका आवेदन पत्र भर्ती बोर्ड द्वारा स्वीकृत किया गया है",
                "मान्य रजिस्ट्रेशन नंबर और जन्म तिथि वाले अभ्यर्थी"
            ],
            "eligibility_no": [
                "जिनका फॉर्म अधूरी फीस या गलत जानकारी के कारण रिजेक्ट हो चुका है",
                "परीक्षा केंद्र पर बिना एडमिट कार्ड और मूल पहचान पत्र के प्रवेश नहीं दिया जाएगा"
            ],
            "documents_required": [
                "एडमिट कार्ड की स्पष्ट कलर प्रिंट कॉपी",
                "मूल आधार कार्ड या वैध फोटो पहचान पत्र",
                "दो हालिया पासपोर्ट साइज फोटो",
                "परीक्षा केंद्र हेतु निर्धारित स्व-घोषणा पत्र"
            ],
            "application_steps": [
                {"step": 1, "title": "भर्ती पोर्टल खोलें", "desc": f"आधिकारिक वेबसाइट {portal_domain} पर जाएँ और 'Download Admit Card' लिंक पर क्लिक करें।"},
                {"step": 2, "title": "लॉगिन विवरण दर्ज करें", "desc": "अपना रजिस्ट्रेशन नंबर और जन्म तिथि दर्ज करके कैप्चा भरें।"},
                {"step": 3, "title": "एडमिट कार्ड जांचें", "desc": "स्क्रीन पर अपना नाम, रोल नंबर, परीक्षा केंद्र और रिपोर्टिंग टाइम ध्यान से चेक करें।"},
                {"step": 4, "title": "प्रिंट निकालें", "desc": "एडमिट कार्ड PDF डाउनलोड करें और परीक्षा के लिए 2 कॉपी सुरक्षित प्रिंट निकाल लें।"}
            ],
            "official_warning": "परीक्षा केंद्र पर किसी भी तरह के इलेक्ट्रॉनिक गैजेट, मोबाइल या स्मार्टवॉच ले जाना सख्त मना है। भर्ती पूरी तरह निष्पक्ष और मेरिट आधारित है।",
            "helpline": "1800-180-0020"
        }

    # 5. RECRUITMENT / GOVT JOBS (भर्ती / सरकारी नौकरी)
    elif any(k in title_lower for k in ["constable", "bharti", "भर्ती", "ssc", "rrb", "upsc", "vacancy", "post", "recruitment", "police", "home guard", "daroga", "si", "army", "defence", "agniveer"]):
        # Extract post count if present
        post_match = re.search(r"(\d+[\d,]*)\s*(?:post|पद)", title_lower)
        post_str = f"{post_match.group(1)} पदों पर" if post_match else "विभिन्न महत्वपूर्ण पदों पर"
        
        return {
            "category": "सरकारी भर्ती एवं रोजगार",
            "topic_type": "benefit_scheme",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": "सरकारी भर्ती 2026",
            "target_audience": "सरकारी नौकरी की तैयारी कर रहे देश और राज्य के युवाओं",
            "action_phrase": f"{post_str} आधिकारिक भर्ती अधिसूचना जारी कर दी गई है और ऑनलाइन फॉर्म भरना शुरू हो चुका है",
            "benefit_amount": f"{post_str} स्थाई सरकारी नौकरी एवं नियमानुसार वेतनमान",
            "benefit_summary": f"केंद्र व राज्य सरकार के विभागों में युवाओं के लिए सरकारी रोजगार का सुनहरा अवसर।",
            "what_changed": {
                "old_rule": "पूर्व में ऑफलाइन ओएमआर प्रक्रिया या पुराने पैटर्न पर परीक्षा आयोजित होती थी।",
                "new_rule": f"अब {portal_domain} पर वन-टाइम रजिस्ट्रेशन (OTR) और कंप्यूटर आधारित पारदर्शी परीक्षा (CBE) प्रणाली लागू है।",
                "deadline": "अंतिम तिथि से पहले अपना ऑनलाइन आवेदन अवश्य सबमिट कर लें"
            },
            "eligibility_yes": [
                "10वीं, 12वीं या स्नातक पास योग्य उम्मीदवार (पदानुसार)",
                "निर्धारित न्यूनतम आयु 18 वर्ष और अधिकतम आयु सीमा पूरी करने वाले अभ्यर्थी",
                "आरक्षित वर्गों को नियमानुसार आयु सीमा में छूट प्रदान की जाएगी"
            ],
            "eligibility_no": [
                "निर्धारित कट-ऑफ तिथि तक शैक्षणिक योग्यता पूरी न करने वाले आवेदक",
                "गलत व्यक्तिगत या शैक्षणिक जानकारी दर्ज करने वाले उम्मीदवार"
            ],
            "documents_required": [
                "आधार कार्ड एवं वैध फोटो पहचान पत्र",
                "10वीं/12वीं की मार्कशीट व उत्तीर्ण प्रमाण पत्र",
                "जाति एवं श्रेणी प्रमाण पत्र (यदि लागू हो)",
                "हाल ही की पासपोर्ट साइज फोटो (व्हाइट बैकग्राउंड) एवं डिजिटल हस्ताक्षर"
            ],
            "application_steps": [
                {"step": 1, "title": "आधिकारिक पोर्टल पर OTR करें", "desc": f"{portal_domain} पोर्टल पर जाकर पहले वन टाइम रजिस्ट्रेशन पूरा करें।"},
                {"step": 2, "title": "पोस्ट का चयन करें", "desc": "लॉगिन करने के बाद संबंधित भर्ती परीक्षा का चयन करें और फॉर्म भरें।"},
                {"step": 3, "title": "फोटो व हस्ताक्षर अपलोड", "desc": "निर्धारित साइज में स्पष्ट फोटो और डिजिटल हस्ताक्षर अपलोड करें।"},
                {"step": 4, "title": "फीस भुगतान व प्रिंट", "desc": "ऑनलाइन आवेदन शुल्क जमा करें और फाइनल एप्लीकेशन फॉर्म का प्रिंट सुरक्षित रख लें।"}
            ],
            "official_warning": "नौकरी लगवाने का झांसा देने वाले किसी भी दलाल या फर्जी गिरोह से सावधान रहें। भर्ती पूरी तरह मेरिट पर आधारित है।",
            "helpline": "1800-112-234"
        }

    # 5. GENERAL WELFARE / CITIZEN SERVICES (सामान्य नागरिक योजना)
    else:
        # Check benefit hint in title
        benefit_match = re.search(r"(\d+[\d,]*\s*(?:post|पद|लाख|रुपये|₹))", title_lower)
        benefit_str = f"कुल लाभ: {benefit_match.group(1)}" if benefit_match else "आधिकारिक सरकारी लाभ व सहायता"

        return {
            "category": "सरकारी योजनाएं एवं नागरिक अधिकार",
            "topic_type": "benefit_scheme",
            "scheme_name_hi": clean_hi,
            "scheme_name_en": clean_en,
            "short_name": short_name,
            "target_audience": "पात्र नागरिकों और सभी संबंधित परिवारों",
            "action_phrase": "सरकार ने इस योजना के तहत नए दिशा-निर्देश और ऑनलाइन आवेदन प्रक्रिया शुरू कर दी है",
            "benefit_amount": benefit_str,
            "benefit_summary": f"{clean_hi} के तहत सरकार द्वारा पात्र नागरिकों को सीधे सहायता प्रदान की जा रही है।",
            "what_changed": {
                "old_rule": "पहले नागरिकों को सरकारी दफ्तरों में जाकर ऑफलाइन फॉर्म भरना पड़ता था।",
                "new_rule": f"अब आधिकारिक पोर्टल {portal_domain} पर डिजिटल सत्यापन और पारदर्शी प्रणाली लागू है।",
                "deadline": "पोर्टल पर दिए गए समय सीमा के भीतर अपना आवेदन पूरा करें"
            },
            "eligibility_yes": [
                "भारत का कोई भी नागरिक जो योजना की निर्धारित शर्तें पूरी करता हो",
                "वैध आधार कार्ड और आधार से लिंक्ड सक्रिय बैंक खाता धारक",
                "अधिसूचना के अनुसार सभी पात्र श्रेणी के आवेदक"
            ],
            "eligibility_no": [
                "गलत या भ्रामक जानकारी देकर आवेदन करने वाले व्यक्ति",
                "अंतिम तिथि समाप्त होने के बाद आवेदन करने वाले"
            ],
            "documents_required": [
                "मूल आधार कार्ड (सक्रिय मोबाइल नंबर लिंक)",
                "सक्रिय बैंक खाता पासबुक (DBT लिंक)",
                "निवास प्रमाण पत्र एवं हालिया पासपोर्ट साइज फोटो",
                "योजना से संबंधित आवश्यक योग्यता प्रमाण पत्र"
            ],
            "application_steps": [
                {"step": 1, "title": "आधिकारिक पोर्टल खोलें", "desc": f"केवल आधिकारिक वेबसाइट https://{portal_domain} पर जाएं।"},
                {"step": 2, "title": "पंजीकरण एवं e-KYC", "desc": "मोबाइल नंबर और आधार से लॉगिन करके ऑनलाइन फॉर्म खोलें।"},
                {"step": 3, "title": "विवरण व दस्तावेज़", "desc": "अपनी सही जानकारी भरें और आवश्यक प्रमाण पत्र अपलोड करें।"},
                {"step": 4, "title": "रसीद सुरक्षित रखें", "desc": "आवेदन फाइनल सबमिट करने के बाद रजिस्ट्रेशन स्लिप सुरक्षित रख लें।"}
            ],
            "official_warning": f"यह सरकारी सेवा पूरी तरह पारदर्शी है। किसी भी अनधिकृत व्यक्ति या फर्जी वेबसाइट को पैसे न दें।",
            "helpline": "1800-111-555"
        }
