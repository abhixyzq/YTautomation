"""
iDastawez - Studio Neural Hindi Voice Generator
Uses Microsoft Edge Neural TTS (hi-IN-MadhurNeural / hi-IN-SwaraNeural).
100% Free, Zero Cost, Studio Quality Hindi Pronunciation with Natural Cadence.
"""

import os
import sys
import re
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Default Voice: Madhur (Clear, Authoritative, News anchor tone)
DEFAULT_HINDI_VOICE = "hi-IN-MadhurNeural"
DEFAULT_RATE = "+0%"  # Neutral rate for maximum clarity and comprehension
DEFAULT_PITCH = "+0Hz"


HINDI_NUMBERS = {
    0: "शून्य", 1: "एक", 2: "दो", 3: "तीन", 4: "चार", 5: "पाँच",
    6: "छह", 7: "सात", 8: "आठ", 9: "नौ", 10: "दस",
    11: "ग्यारह", 12: "बारह", 13: "तेरह", 14: "चौदह", 15: "पंद्रह",
    16: "सोलह", 17: "सत्रह", 18: "अठारह", 19: "उन्नीस", 20: "बीस",
    21: "इक्कीस", 22: "बाइस", 23: "तेईस", 24: "चौबीस", 25: "पच्चीस",
    26: "छब्बीस", 27: "सत्ताईस", 28: "अट्ठाईस", 29: "उनतीस", 30: "तीस",
    31: "इकतीस", 32: "बत्तीस", 33: "तैंतीस", 34: "चौंतीस", 35: "पैंतीस",
    36: "छत्तीस", 37: "सैंतीस", 38: "अड़तीस", 39: "उनतालीस", 40: "चालीस",
    41: "इकतालीस", 42: "बयालीस", 43: "तैंतालीस", 44: "चवालीस", 45: "पैंतालीस",
    46: "छियालीस", 47: "सैंतालीस", 48: "अड़तालीस", 49: "उनचास", 50: "पचास",
    51: "इक्यावन", 52: "बावन", 53: "तिरपन", 54: "चौवन", 55: "पचपन",
    56: "छप्पन", 57: "सत्तावन", 58: "अट्ठावन", 59: "उनसठ", 60: "साठ",
    61: "इकसठ", 62: "बासठ", 63: "तैसठ", 64: "चौंसठ", 65: "पैंसठ",
    66: "छियासठ", 67: "सड़सठ", 68: "अड़सठ", 69: "उनहत्तर", 70: "सत्तर",
    71: "इकहत्तर", 72: "बहत्तर", 73: "तिहत्तर", 74: "चौहत्तर", 75: "पचहत्तर",
    76: "छिहत्तर", 77: "सतहत्तर", 78: "अठहत्तर", 79: "उन्यासी", 80: "अस्सी",
    81: "इक्यासी", 82: "बयासी", 83: "तिरासी", 84: "चौरासी", 85: "पचासी",
    86: "छियासी", 87: "सत्तासी", 88: "अठासी", 89: "नवासी", 90: "नब्बे",
    91: "इक्यानवे", 92: "बानवे", 93: "तिरानवे", 94: "चौरानवे", 95: "पंचानवे",
    96: "छियानवे", 97: "सत्तानवे", 98: "अट्ठानवे", 99: "निन्यानवे", 100: "सौ"
}


def number_to_hindi(n: int) -> str:
    """Converts an integer into natural spoken Hindi words."""
    if n in HINDI_NUMBERS:
        return HINDI_NUMBERS[n]
    if n < 0:
        return f"माइनस {number_to_hindi(abs(n))}"
    if n < 1000:
        hundreds = n // 100
        rem = n % 100
        res = f"{HINDI_NUMBERS.get(hundreds, str(hundreds))} सौ"
        if rem > 0:
            res += f" {number_to_hindi(rem)}"
        return res
    if n < 100000:
        thousands = n // 1000
        rem = n % 1000
        res = f"{number_to_hindi(thousands)} हज़ार"
        if rem > 0:
            res += f" {number_to_hindi(rem)}"
        return res
    if n < 10000000:
        lakhs = n // 100000
        rem = n % 100000
        res = f"{number_to_hindi(lakhs)} लाख"
        if rem > 0:
            res += f" {number_to_hindi(rem)}"
        return res
    crores = n // 10000000
    rem = n % 10000000
    res = f"{number_to_hindi(crores)} करोड़"
    if rem > 0:
        res += f" {number_to_hindi(rem)}"
    return res


def format_decimal_in_hindi(num_str: str) -> str:
    """Formats numbers like 6.5, 1.5, 2.5, 0.5 into natural colloquial Hindi."""
    try:
        val = float(num_str)
    except ValueError:
        return num_str

    if abs(val - 0.5) < 0.01:
        return "आधा"
    if abs(val - 1.5) < 0.01:
        return "डेढ़"
    if abs(val - 2.5) < 0.01:
        return "ढाई"
    if abs(val - 1.25) < 0.01:
        return "सवा"
    if abs(val - 1.75) < 0.01:
        return "पौने दो"

    int_part = int(val)
    frac_part = round(val - int_part, 2)

    if abs(frac_part - 0.5) < 0.01:
        int_hi = number_to_hindi(int_part)
        return f"साढ़े {int_hi}"

    if abs(frac_part - 0.25) < 0.01:
        int_hi = number_to_hindi(int_part)
        return f"सवा {int_hi}"

    if abs(frac_part - 0.75) < 0.01:
        next_hi = number_to_hindi(int_part + 1)
        return f"पौने {next_hi}"

    if frac_part == 0:
        return number_to_hindi(int_part)

    # General decimal e.g. 6.8 -> छह दशमलव आठ
    int_hi = number_to_hindi(int_part)
    frac_str = str(round(frac_part, 2)).split('.')[1]
    frac_hi = " ".join(HINDI_NUMBERS.get(int(d), d) for d in frac_str)
    return f"{int_hi} दशमलव {frac_hi}"


def clean_hindi_for_tts(text: str) -> str:
    """
    Normalizes symbols, currency notations (e.g. rs6.5 lakh, ₹ 6.5 लाख, ₹12,000),
    acronyms, examination terms, and numbers into phonetically clear Hindi words
    so edge-tts pronounces them flawlessly without stuttering or robotic cadence.
    """
    if not text:
        return ""

    # 1. Clean brand name pronunciation: iDastawez -> आई दस्तावेज़
    text = re.sub(r"@?iDastawez\b", "आई दस्तावेज़", text, flags=re.IGNORECASE)
    text = re.sub(r"\bi-Dastawez\b", "आई दस्तावेज़", text, flags=re.IGNORECASE)

    # 2. Strip parenthetical duplicates/acronyms like (PMGKAY), (Ration Card Copy), (MoHFW), (ट्यूशन फीस)
    # This prevents the TTS from awkwardly reading Hindi followed immediately by its English translation.
    text = re.sub(r"\s*\([^)]*\)", "", text)

    # 3. Clean any trailing English news slugs like " - bihar top news... - Jagran"
    text = re.split(r'\s+-\s+[a-zA-Z]{3,}', text)[0]

    # 4. Standardize years (e.g. 2024-2030) so edge-tts doesn't read twenty twenty six
    text = re.sub(r"\b2024\b", "दो हज़ार चौबीस", text)
    text = re.sub(r"\b2025\b", "दो हज़ार पच्चीस", text)
    text = re.sub(r"\b2026\b", "दो हज़ार छब्बीस", text)
    text = re.sub(r"\b2027\b", "दो हज़ार सत्ताईस", text)
    text = re.sub(r"\b2028\b", "दो हज़ार अट्ठाईस", text)
    text = re.sub(r"\b2030\b", "दो हज़ार तीस", text)

    # 5. Educational classes and age ranges
    text = re.sub(r"\b10th\b|\b10वीं\b", "दसवीं", text, flags=re.IGNORECASE)
    text = re.sub(r"\b12th\b|\b12वीं\b", "बारहवीं", text, flags=re.IGNORECASE)
    text = re.sub(r"\b8th\b|\b8वीं\b", "आठवीं", text, flags=re.IGNORECASE)
    text = re.sub(r"\b5th\b|\b5वीं\b", "पाँचवीं", text, flags=re.IGNORECASE)

    def age_repl(m):
        n1 = int(m.group(1))
        n2 = int(m.group(2))
        unit = m.group(3)
        return f"{number_to_hindi(n1)} से {number_to_hindi(n2)} {unit}"
    text = re.sub(r"\b(\d{1,2})\s*से\s*(\d{1,2})\s*(वर्ष|साल)\b", age_repl, text)

    # 6. Slashes between alternatives: "1967 / 1800" -> "1967 या 1800"
    def slash_num_repl(m):
        n1 = int(m.group(1))
        n2 = int(m.group(2))
        return f"{number_to_hindi(n1)} या {number_to_hindi(n2)}"
    text = re.sub(r"\b(\d+)\s*/\s*(\d+)\b", slash_num_repl, text)

    # 7. English Government, Banking, Exam, and Portal Terms (Longer phrases first)
    acronym_map = [
        # Multi-word phrases
        (r"\bpradhan\s*mantri\b", "प्रधानमंत्री"),
        (r"\bofficial\s+website\b", "ऑफिशियल वेबसाइट"),
        (r"\bdirect\s+link\b", "डायरेक्ट लिंक"),
        (r"\bsarkari\s+result\b", "सरकारी रिजल्ट"),
        (r"\bonline\s+apply\b", "ऑनलाइन आवेदन"),
        (r"\bapply\s+online\b", "ऑनलाइन आवेदन"),
        (r"\badmit\s+card\b", "एडमिट कार्ड"),
        (r"\bscore\s*card\b", "स्कोर कार्ड"),
        (r"\banswer\s+key\b", "उत्तर कुंजी"),
        (r"\blast\s+date\b", "अंतिम तारीख"),
        (r"\bration\s+card\b", "राशन कार्ड"),
        (r"\bvoter\s+id\b", "वोटर आईडी"),
        (r"\bbank\s+account\b", "बैंक खाता"),

        # Single word terms
        (r"\bcut[\s-]?off\b", "कटऑफ"),
        (r"\bresult\b", "रिजल्ट"),
        (r"\bnotification\b", "नोटिफिकेशन"),
        (r"\bportal\b", "पोर्टल"),
        (r"\bregistration\b", "रजिस्ट्रेशन"),
        (r"\blogin\b", "लॉगिन"),
        (r"\bdownload\b", "डाउनलोड"),
        (r"\beligibility\b", "पात्रता"),
        (r"\bsarkari\b", "सरकारी"),
        (r"\byojana\b", "योजना"),
        (r"\bgovt\.?\b", "सरकारी"),
        (r"\bstatus\b", "स्टेटस"),
        (r"\bupdate\b", "अपडेट"),
        (r"\bform\b", "फॉर्म"),
        (r"\bdeadline\b", "डेडलाइन"),
        (r"\bpassbook\b", "पासबुक"),
        (r"\binstallment\b", "किस्त"),
        (r"\bsubsidy\b", "सब्सिडी"),
        (r"\bfees?\b", "फीस"),
        (r"\blink\b", "लिंक"),
        (r"\bapply\b", "आवेदन"),
        (r"\baadhaar\b|\baadhar\b", "आधार"),
        (r"\bclerk\b", "क्लर्क"),
        (r"\bconstable\b", "कांस्टेबल"),

        # Acronyms & Agencies
        (r"\bUBI\b", "यूबीआई"),
        (r"\bSBI\b", "एसबीआई"),
        (r"\bPNB\b", "पीएनबी"),
        (r"\bBOB\b", "बीओबी"),
        (r"\bSSC\b", "एसएससी"),
        (r"\bUPSC\b", "यूपीएससी"),
        (r"\bRRB\b", "आरआरबी"),
        (r"\bNTA\b", "एनटीए"),
        (r"\bBPSC\b", "बीपीएससी"),
        (r"\bUPSSSC\b", "यूपी ट्रिपल एससी"),
        (r"\bCBSE\b", "सीबीएसई"),
        (r"\bCISF\b", "सीआईएसएफ"),
        (r"\bCRPF\b", "सीआरपीएफ"),
        (r"\bBSF\b", "बीएसएफ"),
        (r"\bITBP\b", "आईटीबीपी"),
        (r"\bCGL\b", "सीजीएल"),
        (r"\bCHSL\b", "सीएचएसएल"),
        (r"\bMTS\b", "एमटीएस"),
        (r"\bSO\b", "एसओ"),
        (r"\bPO\b", "पीओ"),
        (r"\bSI\b", "एसआई"),
        (r"\bGD\b", "जीडी"),
        (r"\be-?KYC\b", "ई-केवाईसी"),
        (r"\bOTP\b", "ओटीपी"),
        (r"\bDBT\b", "डीबीटी"),
        (r"\bNPCI\b", "एनपीसीआई"),
        (r"\bPAN\b", "पैन"),
        (r"\bPDF\b", "पीडीएफ"),
        (r"\bSMS\b", "एसएमएस"),
        (r"\bNSP\b", "एनएसपी"),
        (r"\bOTR\b", "ओटीआर"),
        (r"\bPMAY\b", "पीएम आवास योजना"),
        (r"\bCGHS\b", "सीजीएचएस"),
        (r"\bECHS\b", "ईसीएचएस"),
        (r"\bCSC\b", "सीएससी"),
        (r"\bURL\b", "वेबसाइट लिंक"),
        (r"\bID\b", "आईडी"),
        (r"\bPM\b", "पीएम"),
        (r"\bCM\b", "सीएम"),
        (r"\bgov\.in\b", "जीओवी डॉट इन"),
        (r"\bnic\.in\b", "एनआईसी डॉट इन"),
    ]
    for pattern, repl in acronym_map:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # 8. CURRENCY AND AMOUNTS (Fix for rs6.5 lakh, ₹ 6.5 लाख, ₹12,000)
    curr_prefix = r"(?:(?:₹|rs\.?|inr)\s*)?"

    # 8a. Lakhs with decimal or integer:
    # E.g. rs6.5 lakh, ₹ 6.5 लाख, 6.5 lakh, 1.5 lakh, 5 lakh
    def lakh_repl(m):
        num_str = m.group(1)
        spoken_amount = format_decimal_in_hindi(num_str) + " लाख रुपये "
        return spoken_amount

    text = re.sub(
        rf"{curr_prefix}(\d+(?:\.\d+)?)\s*(?:lakhs?|lacs?|लाख)(?:\s*(?:rupees?|रुपये|रुपया))?",
        lakh_repl,
        text,
        flags=re.IGNORECASE
    )

    # 8b. Crores with decimal or integer:
    # E.g. 1.5 crore, 10.5 crore, ₹ 2 crore
    def crore_repl(m):
        num_str = m.group(1)
        spoken_amount = format_decimal_in_hindi(num_str) + " करोड़ रुपये "
        return spoken_amount

    text = re.sub(
        rf"{curr_prefix}(\d+(?:\.\d+)?)\s*(?:crores?|cr|करोड़)(?:\s*(?:rupees?|रुपये|रुपया))?",
        crore_repl,
        text,
        flags=re.IGNORECASE
    )

    # 8c. Explicit currency prefixed numbers like ₹12,000, Rs. 50,000, Rs 12000, ₹ 5,00,000, ₹12,000/-
    def currency_num_repl(m):
        raw_num = m.group(1).replace(",", "")
        try:
            n = int(raw_num)
            return f"{number_to_hindi(n)} रुपये "
        except ValueError:
            return m.group(0)

    text = re.sub(
        r"(?:₹|rs\.?|inr)\s*(\d{1,3}(?:,\d{2,3})*|\d+)(?:\s*\/-\s*|\s*रुपये|\s*rupees)?\b",
        currency_num_repl,
        text,
        flags=re.IGNORECASE
    )

    # 8d. Standalone numbers followed by रुपये / rupees e.g. "12000 रुपये"
    def num_rupees_repl(m):
        raw_num = m.group(1).replace(",", "")
        try:
            n = int(raw_num)
            return f"{number_to_hindi(n)} रुपये "
        except ValueError:
            return m.group(0)

    text = re.sub(
        r"\b(\d{1,3}(?:,\d{2,3})*|\d+)\s*(?:रुपये|रुपया|rupees?)\b",
        num_rupees_repl,
        text,
        flags=re.IGNORECASE
    )

    # Clean multiple consecutive "रुपये"
    text = re.sub(r"(रुपये\s*)+रुपये", "रुपये", text)

    # 9. Percentages: 6.5% -> साढ़े छह प्रतिशत, 10% -> दस प्रतिशत
    def percent_repl(m):
        num_str = m.group(1)
        spoken = format_decimal_in_hindi(num_str)
        return f"{spoken} प्रतिशत"

    text = re.sub(r"(\d+(?:\.\d+)?)\s*%", percent_repl, text)

    # 10. Standalone decimals not caught above: 6.5 -> साढ़े छह
    def standalone_decimal_repl(m):
        num_str = m.group(1)
        return format_decimal_in_hindi(num_str)

    text = re.sub(r"\b(\d+\.\d+)\b", standalone_decimal_repl, text)

    # 11. Natural breath pauses & clean punctuation
    text = text.replace("—", ", ")
    text = text.replace("--", ", ")
    text = text.replace(":", " -")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _calculate_word_and_phrase_timings(
    sentence_boundaries: List[Dict[str, Any]], 
    cleaned_text: str
) -> Tuple[float, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Computes exact start and end timestamps for each spoken Hindi word
    and groups them into punchy 3-5 word subtitle phrases.
    """
    all_word_timings = []
    
    for sentence in sentence_boundaries:
        # 10,000,000 ticks = 1 second
        offset_sec = sentence["offset"] / 10000000.0
        duration_sec = sentence["duration"] / 10000000.0
        stext = sentence["text"].strip()
        words = stext.split()
        if not words:
            continue
            
        total_weights = sum(max(len(w), 2) for w in words)
        curr_t = offset_sec
        for w in words:
            weight = max(len(w), 2)
            w_duration = (weight / total_weights) * duration_sec
            all_word_timings.append({
                "word": w,
                "start": round(curr_t, 3),
                "end": round(curr_t + w_duration, 3)
            })
            curr_t += w_duration

    # Group words into clean 3-5 word phrases for subtitles
    phrases = []
    max_words_per_phrase = 4
    current_chunk = []
    for w_obj in all_word_timings:
        current_chunk.append(w_obj)
        if len(current_chunk) >= max_words_per_phrase or w_obj["word"].endswith(("।", "?", "!", ",")):
            phrases.append({
                "phrase_text": " ".join(w["word"] for w in current_chunk),
                "start": current_chunk[0]["start"],
                "end": round(current_chunk[-1]["end"] + 0.1, 3),
                "words": current_chunk
            })
            current_chunk = []
    if current_chunk:
        phrases.append({
            "phrase_text": " ".join(w["word"] for w in current_chunk),
            "start": current_chunk[0]["start"],
            "end": round(current_chunk[-1]["end"] + 0.1, 3),
            "words": current_chunk
        })

    # Total duration
    if all_word_timings:
        total_dur = all_word_timings[-1]["end"] + 0.3
    else:
        total_dur = max(len(cleaned_text.split()) / 2.6, 5.0)

    return round(total_dur, 2), all_word_timings, phrases


async def _generate_audio_file(
    text: str, 
    output_audio_path: str, 
    voice: str = DEFAULT_HINDI_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> Dict[str, Any]:
    """
    Generates an MP3 file via edge-tts stream and extracts exact word/phrase timestamps.
    """
    cleaned_text = clean_hindi_for_tts(text)
    communicate = edge_tts.Communicate(cleaned_text, voice=voice, rate=rate, pitch=pitch)
    
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    sentence_boundaries = []
    
    with open(output_audio_path, "wb") as f:
        async for chunk in communicate.stream():
            chunk_type = chunk.get("type")
            if chunk_type == "audio":
                f.write(chunk.get("data", b""))
            elif chunk_type == "SentenceBoundary":
                sentence_boundaries.append(chunk)

    duration, word_timings, phrases = _calculate_word_and_phrase_timings(sentence_boundaries, cleaned_text)
    
    # Verify file was written
    if not os.path.exists(output_audio_path) or os.path.getsize(output_audio_path) < 100:
        raise RuntimeError(f"Audio file synthesis failed: {output_audio_path}")
        
    return {
        "duration": duration,
        "word_timings": word_timings,
        "phrases": phrases
    }


def generate_scene_voiceovers(
    script_data: Dict[str, Any], 
    output_dir: str, 
    voice: str = DEFAULT_HINDI_VOICE
) -> Dict[str, Any]:
    """
    Generates studio neural voiceovers for each scene in the script.
    Saves individual MP3 files and returns scene metadata with exact durations,
    word timestamps, and subtitle phrase chunks.
    """
    os.makedirs(output_dir, exist_ok=True)
    scenes = script_data.get("scenes", [])
    
    print(f"\n[iDastawez Voice Engine] Generating neural Hindi audio with {voice}...")
    
    enriched_scenes = []
    total_duration = 0.0
    
    async def process_all_scenes():
        nonlocal total_duration
        for scene in scenes:
            scene_id = scene["scene_id"]
            audio_filename = f"scene_{scene_id}.mp3"
            audio_path = os.path.join(output_dir, audio_filename)
            dialogue = scene["dialogue"]
            
            res = await _generate_audio_file(dialogue, audio_path, voice=voice)
            dur = res["duration"]
            total_duration += dur
            
            enriched = dict(scene)
            enriched["audio_file"] = audio_filename
            enriched["audio_path"] = os.path.abspath(audio_path).replace("\\", "/")
            enriched["duration_seconds"] = dur
            enriched["duration_frames_30fps"] = int(round(dur * 30))
            enriched["phrases"] = res["phrases"]
            enriched["word_timings"] = res["word_timings"]
            enriched_scenes.append(enriched)
            
            print(f"  ✓ Scene {scene_id} [{scene['act_name']}]: {round(dur, 1)}s ({len(dialogue.split())} words, {len(res['phrases'])} caption phrases)")

    asyncio.run(process_all_scenes())
    
    result = dict(script_data)
    result["scenes"] = enriched_scenes
    result["total_audio_duration_seconds"] = round(total_duration, 2)
    result["voice_used"] = voice
    
    # Also save metadata JSON alongside the audio
    meta_path = os.path.join(output_dir, "voice_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"[iDastawez Voice Engine] Generated {len(enriched_scenes)} scenes. Total Duration: {round(total_duration / 60, 2)} minutes.")
    return result


def generate_shorts_voiceover(
    text: str,
    output_path: str,
    voice: str = DEFAULT_HINDI_VOICE,
    rate: str = "+3%",
    pitch: str = DEFAULT_PITCH
) -> Dict[str, Any]:
    """
    Generates single continuous studio neural Hindi voiceover for 9:16 Shorts
    and computes exact word-level timing offsets and punchy subtitle phrases.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    res = asyncio.run(_generate_audio_file(text, output_path, voice=voice, rate=rate, pitch=pitch))
    abs_path = os.path.abspath(output_path).replace("\\", "/")
    return {
        "audio_path": abs_path,
        "duration": res["duration"],
        "word_timings": res["word_timings"],
        "phrases": res["phrases"]
    }


if __name__ == "__main__":
    from dastawez.topics import VERIFIED_GOVT_SCHEMES
    from dastawez.script_generator import generate_dastawez_script
    
    sample_scheme = VERIFIED_GOVT_SCHEMES[0]  # Ayushman Bharat 70+
    sample_script = generate_dastawez_script(sample_scheme)
    
    test_output_dir = os.path.abspath("./output/dastawez_test_voice")
    voice_res = generate_scene_voiceovers(sample_script, test_output_dir)
    print("\nVoice Generation Complete! Metadata saved to:", test_output_dir)
