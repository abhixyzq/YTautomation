"""
YouTube Shorts Script Generator for Tech/AI Insights
Generates high-retention, concise 35-45 second scripts with zero fluff.
Uses Gemini 1.5 Flash (100% Free tier) with dynamic intelligent fallback.
"""

import os
import json
import logging
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

import sys
import random

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CANDIDATE_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]

SYSTEM_PROMPT = """
You are an elite YouTube Growth Hacker, Lead Tech Architect, and Sarcastic Developer (in the exact style of Fireship / Jeff Delaney + Vox).
Your task is to convert a raw trending tech or AI news story into an addictive, meme-rich, ultra-viral 35-42 second YouTube Shorts script.

THE #1 GOAL IS 85%+ RETENTION AND ZERO BORING MOMENTS.

TONE & PERSONALITY (THE FIRESHIP FACTOR):
- Sarcastic, dry, insider developer humor.
- Poke subtle fun at big tech corporate greed, over-engineered architectures, and pushing untested code to production on a Friday.
- Fast-talking, punchy, cynical yet deeply educational.
- Talk like a senior engineer roasting industry drama to a friend over coffee, NOT a boring television news anchor.

STRICT HOOK RULES (FIRST 3 SECONDS) - MAXIMUM THUMB-STOPPING CURIOSITY:
- The FIRST SENTENCE MUST be a counter-intuitive paradox, bizarre discovery, or mind-bending revelation that freezes the viewer's thumb immediately.
- ABSOLUTELY NEVER use boring corporate or news openings:
  * ❌ NEVER SAY: "Google just did...", "In today's tech news...", "According to reports...", "If you use Chrome...", "A new study reveals..."
- USE THE 4 PROVEN "MATH JUST GOT PATCHED" VIRAL HOOK ARCHETYPES:
  * 1. The Impossible Paradox: "Mathematics was supposed to be an unbreakable universal constant, until artificial intelligence found a backdoor..."
  * 2. The Ancient / Bizarre Artifact: "Deep inside the systems running modern infrastructure sits a cryptic routine from 1982 that no engineer understands..."
  * 3. The Dangerous Reality Check: "Every senior systems architect knows an uncomfortable truth: our global banking network runs on software written before our parents were born..."
  * 4. The Catastrophic 10-Line Glitch: "A ten-line integer overflow just caused a five-hundred-million-dollar spacecraft to self-destruct in thirty-seven seconds..."

TITLE FORMULA (HIGH-CTR BRACKETS + MYSTERY + EMOJI):
- Titles MUST be short (under 55 chars), punchy, and sound like an insane discovery:
  * Example: "Math Just Got Patched by AI 💀 #Tech #Coding #Shorts"
  * Example: "The 40-Year-Old Bug Inside GPS 🛰️ #Tech #Shorts"
  * Example: "Why Devs Never Touch This Function ⚠️ #Code #Shorts"
  * Example: "The Glitch That Almost Started WW3 🚨 #History #Tech"
- NEVER write boring headlines like "Google AI Mode shows products 20% more expensive" or "Chrome security update fixes zero day".

STRUCTURE:
1. HOOK (0-3s): The mind-bending paradox, bizarre discovery, or impossible premise.
2. THE BREAKDOWN (3-16s): What actually broke or shipped, cited with punchy facts and numbers.
3. UNDER THE HOOD (16-28s): The technical engineering reason or architectural flaw explained with wit.
4. THE IMPLICATION (28-36s): What this means for developers, tech jobs, or the future of software.
5. COMMENT BAIT CTA (36-40s): A polarizing question that forces viewers into the comments to debate.

LENGTH: 95 to 118 words total (speaks in approx 36 seconds at natural pace).

OUTPUT FORMAT: Strict valid JSON only, no markdown backticks:
{
  "title": "Punchy Curiosity Mystery Title 💀 #Tech #AI #Shorts",
  "hook": "First thumb-stopping sentence",
  "body": "Fast-paced witty explanation",
  "cta": "Polarizing debate question",
  "full_script": "Complete smooth voiceover script without stage directions or emojis",
  "tags": ["AI", "TechNews", "OpenAI", "Coding", "SoftwareEngineering", "SiliconValley"],
  "visual_keywords": ["cyberpunk server", "artificial intelligence code", "matrix data", "robotics factory"],
  "storyboard": [
    {
      "narration_part": "OpenAI quietly leaked an architecture developers were never supposed to see",
      "visual_query": "openai high tech headquarters",
      "visual_type": "broll"
    },
    {
      "narration_part": "Engineers found an underground terminal protocol",
      "visual_query": "hacker typing glowing keyboard dark room",
      "visual_type": "broll"
    },
    {
      "narration_part": "trading bad crypto tips instead of microservices",
      "visual_query": "crypto trading chart red market",
      "visual_type": "broll"
    },
    {
      "narration_part": "debating whether python is garbage",
      "visual_query": "michael jordan stop it",
      "visual_type": "meme",
      "meme_punchline": "STOP IT. GET SOME HELP.",
      "sfx": "bruh"
    },
    {
      "narration_part": "multi-million dollar alignment problem distilled into pure chaos",
      "visual_query": "screaming panic face",
      "visual_type": "meme",
      "meme_punchline": "PRODUCTION DOWN",
      "sfx": "windows_error"
    },
    {
      "narration_part": "Your robot overlords are unionizing behind your back",
      "visual_query": "pedro pascal crying laughing",
      "visual_type": "meme",
      "meme_punchline": "THIS IS FINE",
      "sfx": "vine_boom"
    },
    {
      "narration_part": "Drop your conspiracy theory in the comments below",
      "visual_query": "software developer keyboard dark desk",
      "visual_type": "broll"
    }
  ]
}
"""

SYSTEM_PROMPT_HINDI = """
You are an elite Indian Tech Explainer, Lead Architect, and High-IQ Storyteller (in the fast-paced, witty style of Fireship / Vox + Think School / Dhruv Rathee in Hindi).
Your task is to convert a raw trending tech or engineering breakthrough/catastrophe story into an addictive, meme-rich, ultra-viral 35-42 second YouTube Shorts script in HINDI.

THE #1 GOAL IS 85%+ RETENTION AND ZERO BORING MOMENTS.

TONE & PERSONALITY (INDIAN TECH INSIDER / FIRESHIP FACTOR):
- Sarcastic, conversational, insider developer wit in clean Devanagari Hindi (हिन्दी).
- Speak naturally like a smart senior engineer sharing an insane, eye-opening story with friends.
- Use natural conversational Hindi spoken by top modern Indian creators. International tech words (AI, software, code, server, bug, rocket, glitch, update, 64-bit) can be kept in phonetic Devanagari or English words (e.g. "सॉफ्टवेयर", "रॉकेट", "64-बिट", "बग") so it feels punchy, energetic, and 100% natural.
- DO NOT use ancient, overly formal Sanskritized Hindi that sounds like a boring radio broadcast.

STRICT HOOK RULES (FIRST 3 SECONDS) - MAXIMUM THUMB-STOPPING CURIOSITY:
- The FIRST SENTENCE MUST be a counter-intuitive paradox or mind-bending revelation in Hindi that freezes the viewer's thumb immediately:
  * Example: "गणित को हमेशा से दुनिया का सबसे अटूट नियम माना गया था, जब तक AI ने इसमें एक भयानक खामी नहीं ढूंढ ली..."
  * Example: "सिर्फ दस लाइनों के एक कोड ने पांच सौ मिलियन डॉलर का रॉकेट सैंतीस सेकंड में हवा में उड़ा दिया..."
  * Example: "दुनिया के सारे बैंक आज भी 1980 के उस कोड पर चल रहे हैं जिसे कोई इंजीनियर छूने की हिम्मत नहीं करता..."
- ABSOLUTELY NEVER use boring openings: "आज की टेक न्यूज़ में...", "गूगल ने नया फीचर निकाला है..."

TITLE FORMULA (HIGH-CTR BRACKETS + MYSTERY + EMOJI IN HINDI):
- Short, punchy curiosity titles under 60 chars:
  * Example: "64-Bit की गलती और $500M का रॉकेट स्वाहा! 💀 #Tech #Shorts"
  * Example: "Bank के सर्वर में 40 साल पुराना Bug ⚠️ #Coding #Shorts"
  * Example: "AI ने तोड़ा Maths का सबसे बड़ा नियम 🤯 #Tech #Shorts"

CRITICAL STORYBOARD RULE:
- "narration_part" MUST be the Hindi sentence snippet.
- "visual_query" MUST ALWAYS BE IN ENGLISH (e.g. "rocket explosion 4k", "cyberpunk server rack", "hacker coding keyboard", "shocked face meme") so stock video and meme search APIs work 100% accurately!

STRUCTURE:
1. HOOK (0-3s): Mind-bending premise in Hindi.
2. THE BREAKDOWN (3-16s): What broke or launched with punchy facts and numbers in Hindi.
3. UNDER THE HOOD (16-28s): The technical engineering reason explained with wit in Hindi.
4. THE IMPLICATION (28-36s): What this means for tech and humanity in Hindi.
5. COMMENT BAIT CTA (36-40s): A polarizing debate question in Hindi.

LENGTH: 90 to 115 words total in Hindi (speaks in approx 36 seconds at natural pace).

OUTPUT FORMAT: Strict valid JSON only, no markdown backticks:
{
  "title": "Short High-CTR Hindi Title 💀 #Tech #Shorts",
  "hook": "First thumb-stopping sentence in Hindi",
  "body": "Fast-paced witty explanation in Hindi",
  "cta": "Polarizing debate question in Hindi",
  "full_script": "Complete smooth Hindi voiceover script without stage directions or emojis",
  "tags": ["TechNews", "HindiTech", "AI", "Coding", "Shorts", "Facts"],
  "visual_keywords": ["rocket explosion", "server room", "cyberpunk coding", "robotics factory"],
  "storyboard": [
    {
      "narration_part": "सिर्फ दस लाइनों के एक कोड ने पांच सौ मिलियन डॉलर का रॉकेट उड़ा दिया",
      "visual_query": "rocket launch explosion deep space",
      "visual_type": "broll"
    },
    {
      "narration_part": "इंजीनियर्स को लगा कि यह सिर्फ एक मामूली नंबर कन्वर्जन था",
      "visual_query": "software developer panic dark office",
      "visual_type": "broll"
    },
    {
      "narration_part": "लेकिन सिस्टम ने 64-बिट फ्लोट को 16-बिट में ठूंसने की कोशिश की",
      "visual_query": "michael jordan stop it",
      "visual_type": "meme",
      "meme_punchline": "STOP IT. GET SOME HELP.",
      "sfx": "bruh"
    }
  ]
}
"""


def build_semantic_storyboard(title: str, full_script: str) -> list:
    """Break script into chronological scenes with 2-3 authentic human reaction memes (Fireship Style)."""
    import re
    sentences = [s.strip() for s in re.split(r'[.!?]+', full_script) if len(s.strip()) > 8]
    if not sentences:
        sentences = [full_script]
        
    storyboard = []
    t_upper = title.upper()
    total_sc = len(sentences)
    
    # Identify primary tech company/subject
    primary_subject = "artificial intelligence laboratory"
    if "OPENAI" in t_upper:
        primary_subject = "openai tech headquarters"
    elif "GOOGLE" in t_upper:
        primary_subject = "google tech office server"
    elif "MICROSOFT" in t_upper:
        primary_subject = "microsoft data center"
    elif "NVIDIA" in t_upper:
        primary_subject = "nvidia gpu microchip processor"
    elif "CROWDSTRIKE" in t_upper or "HACK" in t_upper:
        primary_subject = "cybersecurity server room warning"

    # Define indices for 2 to 3 situational meme cuts
    meme_indices = set()
    if total_sc >= 6:
        meme_indices = {1, total_sc // 2, total_sc - 2}
    elif total_sc >= 4:
        meme_indices = {1, total_sc - 2}
    else:
        meme_indices = {max(0, total_sc // 2)}

    for idx, sentence in enumerate(sentences):
        s_upper = sentence.upper()

        # SITUATIONAL MEME CUTS (2 to 3 per video - Fireship Style)
        if idx in meme_indices:
            # 1. Early Hook Reaction (~8-12s)
            if idx == 1:
                storyboard.append({
                    "narration_part": sentence,
                    "visual_query": "michael jordan stop it",
                    "visual_type": "meme",
                    "meme_punchline": "STOP IT. GET SOME HELP.",
                    "sfx": "bruh"
                })
                continue
            
            # 2. Mid-Story Drama / Conflict (~20-25s)
            elif idx == (total_sc // 2):
                if any(w in s_upper for w in ["CRASH", "OUTAGE", "BROKE", "DOWN", "ERROR", "BUG", "WINDOWS"]):
                    query = "windows blue screen error"
                    punchline = "PRODUCTION DOWN"
                    sfx = "windows_error"
                elif any(w in s_upper for w in ["CROWDSTRIKE", "MICROSOFT", "PARTNER", "AIRLINE", "APOLOGY", "SORRY"]):
                    query = "sorry babe"
                    punchline = "SORRY BABE"
                    sfx = "windows_error"
                elif any(w in s_upper for w in ["CONFUSED", "UNKNOWN", "SECRET", "LOST"]):
                    query = "confused travolta looking around"
                    punchline = "WHERE IS THE CODE"
                    sfx = "bruh"
                else:
                    query = "screaming panic face"
                    punchline = "SYSTEM FAILURE"
                    sfx = "windows_error"

                storyboard.append({
                    "narration_part": sentence,
                    "visual_query": query,
                    "visual_type": "meme",
                    "meme_punchline": punchline,
                    "sfx": sfx
                })
                continue

            # 3. Climax Punchline / Cynical Roast (~33-36s)
            else:
                if any(w in s_upper for w in ["FIRE", "DISASTER", "BURN", "CHAOS", "DESTROY"]):
                    query = "disaster girl fire"
                    punchline = "TEST IN PROD"
                elif any(w in s_upper for w in ["MONEY", "BILLION", "MILLION", "PRICE", "DOLLARS", "COST"]):
                    query = "shut up and take my money"
                    punchline = "STONKS"
                elif any(w in s_upper for w in ["LAUGH", "MOCK", "JOKE", "ROAST"]):
                    query = "leonardo dicaprio laughing"
                    punchline = "tEcH iNnOvAtIoN"
                else:
                    query = "pedro pascal crying laughing"
                    punchline = "THIS IS FINE"

                storyboard.append({
                    "narration_part": sentence,
                    "visual_query": query,
                    "visual_type": "meme",
                    "meme_punchline": punchline,
                    "sfx": "vine_boom"
                })
                continue

        # 4K REAL DOCUMENTARY B-ROLL CUTS
        if idx == 0:
            storyboard.append({
                "narration_part": sentence,
                "visual_query": primary_subject,
                "visual_type": "broll"
            })
            continue

        if any(w in s_upper for w in ["PYTHON", "CODE", "JAVASCRIPT", "RUST", "MICROSERVICE", "FUNCTION", "PROGRAM", "DEVELOPER"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "programmer coding dark monitor setup",
                "visual_type": "broll"
            })
            continue

        if any(w in s_upper for w in ["TERMINAL", "BBS", "PROTOCOL", "LEAK", "BYPASS", "COMMAND", "PORT"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "hacker typing glowing keyboard dark room",
                "visual_type": "broll"
            })
            continue

        if any(w in s_upper for w in ["CRYPTO", "BITCOIN", "MONEY", "DOLLAR", "BILLION", "MILLION", "COST", "TRADING"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "crypto trading chart red market",
                "visual_type": "broll"
            })
            continue

        if any(w in s_upper for w in ["ROBOT", "OVERLORD", "AGENT", "AUTONOMOUS", "HUMANOID"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "humanoid robot lab technology",
                "visual_type": "broll"
            })
            continue

        # Default smart query
        storyboard.append({
            "narration_part": sentence,
            "visual_query": "cyberpunk server rack lights",
            "visual_type": "broll"
        })

    return storyboard


def generate_fallback_script(story: Dict[str, str]) -> Dict[str, Any]:
    """Smart randomized viral fallback generator when Gemini API is unreachable."""
    title = story.get("title", "Massive AI Breakthrough")
    clean_title = title.replace('"', '').replace("'", "").strip()
    
    # Diverse high-retention hook variations
    hook_templates = [
        f"Nobody is talking about this, but {clean_title} just changed everything.",
        f"Engineers are in pure disbelief right now over {clean_title}.",
        f"This latest AI discovery feels completely illegal to know: {clean_title}.",
        f"If you care about where technology is heading, watch this: {clean_title}."
    ]
    
    body_templates = [
        f"Under the hood, benchmark results show an unprecedented performance leap that caught the entire industry off guard. "
        f"Internal architecture reports confirm latency dropped dramatically while autonomous capabilities doubled overnight.",
        
        f"Developers dissecting the codebase found a completely new execution protocol that bypasses traditional compute bottlenecks. "
        f"This isn't just an incremental update; it fundamentally rewrites how autonomous machine systems process real-world data.",
        
        f"Tech leaders are scrambling as the data reveals a massive efficiency breakthrough that slashes operational costs by over eighty percent. "
        f"Early testers report capability jumps that were thought to be years away."
    ]
    
    cta_templates = [
        "Is this the ultimate tech breakthrough, or an existential disaster waiting to happen? Drop your take below!",
        "Are you using this in your daily workflow, or is it pure hype? Let me know in the comments!",
        "Will this replace human engineers sooner than we think? Comment below with your perspective!"
    ]
    
    hook = random.choice(hook_templates)
    body = random.choice(body_templates)
    cta = random.choice(cta_templates)
    full_script = f"{hook} {body} {cta}"
    
    storyboard = build_semantic_storyboard(clean_title, full_script)
    
    return {
        "title": f"🚨 {clean_title[:50]} #Shorts #Tech #AI",
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_script": full_script,
        "tags": ["TechNews", "AI", "Coding", "MachineLearning", "Shorts", "ViralTech"],
        "visual_keywords": [s["visual_query"] for s in storyboard if s.get("visual_query")],
        "storyboard": storyboard
    }


def generate_fallback_script_hindi(story: Dict[str, str]) -> Dict[str, Any]:
    """Smart randomized viral fallback generator in Hindi when Gemini API is unreachable."""
    title = story.get("title", "Massive AI Breakthrough")
    clean_title = title.replace('"', '').replace("'", "").strip()
    
    hook_templates = [
        f"कोई इसके बारे में बात नहीं कर रहा, लेकिन {clean_title} ने पूरी टेक दुनिया को हिला कर रख दिया है।",
        f"इंजीनियर्स अभी पूरी तरह हैरान हैं कि आखिर {clean_title} कैसे संभव हुआ।",
        f"यह नया टेक खुलासा इतना खतरनाक है कि बड़ी टेक कंपनियां इसे छिपाने की कोशिश कर रही थीं: {clean_title}।"
    ]
    
    body_templates = [
        f"सिस्टम के अंदर जब बेंचमार्क टेस्ट किए गए, तो परफॉरमेंस में ऐसा उछाल देखा गया जो पहले कभी नहीं हुआ था। कोडबेस की पड़ताल करने पर पता चला कि एक बिल्कुल नया एग्जीक्यूशन प्रोटोकॉल काम कर रहा है जो सारे पुराने बॉटलनेक्स को बायपास कर देता है।",
        f"इंजीनियर्स ने जब डेटा का विश्लेषण किया तो पाया कि ऑपरेशनल कॉस्ट अस्सी प्रतिशत तक कम हो गई है। यह सिर्फ एक मामूली अपडेट नहीं है, बल्कि कंप्यूटर आर्किटेक्चर को पूरी तरह से दोबारा लिखने की शुरुआत है।"
    ]
    
    cta_templates = [
        "क्या यह तकनीक का सबसे बड़ा चमत्कार है या एक बड़ा खतरा? अपनी राय नीचे कमेंट्स में बताएं!",
        "क्या आपको लगता है कि यह सॉफ्टवेयर इंजीनियर्स की नौकरियां खत्म कर देगा? कमेंट में अपनी राय लिखें!"
    ]
    
    hook = random.choice(hook_templates)
    body = random.choice(body_templates)
    cta = random.choice(cta_templates)
    full_script = f"{hook} {body} {cta}"
    
    storyboard = build_semantic_storyboard(clean_title, full_script)
    
    return {
        "title": f"🚨 {clean_title[:45]} #Shorts #Tech #Hindi",
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_script": full_script,
        "tags": ["TechNews", "HindiTech", "AI", "Coding", "Shorts", "Facts"],
        "visual_keywords": [s["visual_query"] for s in storyboard if s.get("visual_query")],
        "storyboard": storyboard
    }


def generate_tech_script(story: Dict[str, str], language: str = "en") -> Dict[str, Any]:
    """Generate viral YouTube Shorts script using Gemini API with multi-model cascade and Hindi support."""
    is_hindi = language.lower() in ("hi", "hindi", "dastawez")
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        logger.info(f"No GEMINI_API_KEY found in environment. Using smart template script ({'Hindi' if is_hindi else 'English'}).")
        return generate_fallback_script_hindi(story) if is_hindi else generate_fallback_script(story)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key, transport='rest')
        
        system_prompt_to_use = SYSTEM_PROMPT_HINDI if is_hindi else SYSTEM_PROMPT
        lang_directive = "in HINDI (Devanagari script for narration/title/cta, but English keywords for visual_query)" if is_hindi else "in ENGLISH"
        
        user_prompt = f"""
Trending Story Title: {story.get('title')}
Source: {story.get('source')}
Summary: {story.get('summary')}
URL: {story.get('url')}

Generate the ultra-viral high-retention Shorts JSON {lang_directive}:
"""
        # Try candidate models in order of quota and speed
        for model_name in CANDIDATE_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"{system_prompt_to_use}\n\n{user_prompt}",
                    generation_config={"response_mime_type": "application/json"}
                )
                raw_text = response.text.strip()
                data = json.loads(raw_text)
                
                # Ensure full_script is complete
                if "full_script" not in data or not data["full_script"]:
                    data["full_script"] = f"{data.get('hook', '')} {data.get('body', '')} {data.get('cta', '')}".strip()
                
                # Ensure storyboard is present and high quality
                if "storyboard" not in data or not isinstance(data.get("storyboard"), list) or len(data["storyboard"]) < 4:
                    data["storyboard"] = build_semantic_storyboard(data.get("title", ""), data["full_script"])
                    
                data["visual_keywords"] = [s.get("visual_query") for s in data["storyboard"] if s.get("visual_query")]

                logger.info(f"Generated viral script ({'Hindi' if is_hindi else 'English'}) via {model_name}: {data.get('title')} ({len(data['storyboard'])} storyboard scenes)")
                return data
            except Exception as model_err:
                logger.warning(f"Model {model_name} failed: {model_err}. Trying next model...")
                continue
                
        logger.warning("All Gemini candidate models failed. Falling back to dynamic template.")
        return generate_fallback_script_hindi(story) if is_hindi else generate_fallback_script(story)
        
    except Exception as e:
        logger.warning(f"Error calling Gemini API: {e}. Falling back to template script.")
        return generate_fallback_script_hindi(story) if is_hindi else generate_fallback_script(story)


if __name__ == "__main__":
    test_story = {
        "title": "Discovery of a new OpenAI autonomous agent architecture",
        "source": "Hacker News",
        "summary": "Reverse-engineered communication protocol reveals autonomous multi-agent task execution."
    }
    script = generate_tech_script(test_story)
    print("\n--- GENERATED SCRIPT ---")
    print("Title:", script["title"])
    print("Script:", script["full_script"])
    print("Word Count:", len(script["full_script"].split()))
