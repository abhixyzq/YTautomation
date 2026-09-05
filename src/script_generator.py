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
    "gemini-3.6-flash",
    "gemini-3.5-flash"
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

STRICT HOOK RULES (FIRST 3 SECONDS):
- The FIRST SENTENCE MUST be a psychological curiosity bomb that freezes the viewer's thumb immediately.
- NEVER use generic filler: "Hey guys", "In today's news", "Wait did you see", "Check this out", "Software is changing".
- Use proven viral hook archetypes:
  * Sarcastic Roast / Outage: "Real men test in production, but tech companies just did something completely unhinged..."
  * Secret Leak: "OpenAI quietly leaked an architecture that developers were never supposed to see..."
  * Warning / Reality Check: "If you still write code for a living, you have about six months to prepare for this..."
  * Corporate Injustice: "Google's new AI was just caught secretly charging users 21% more for the exact same product..."

STRUCTURE:
1. HOOK (0-3s): The bombshell revelation or sarcastic observation.
2. THE BREAKDOWN (3-16s): What actually broke or shipped, cited with punchy facts and numbers.
3. UNDER THE HOOD (16-28s): The technical engineering reason or architectural flaw explained with wit.
4. THE IMPLICATION (28-36s): What this means for developers, tech jobs, or the future of software.
5. COMMENT BAIT CTA (36-40s): A polarizing question that forces viewers into the comments to debate.

LENGTH: 95 to 118 words total (speaks in approx 36 seconds at natural pace).

OUTPUT FORMAT: Strict valid JSON only, no markdown backticks:
{
  "title": "Shocking High-CTR 50-char Title 🚨 #AI #Tech #Shorts",
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
      "visual_query": "retro computer bbs terminal hacker",
      "visual_type": "terminal",
      "terminal_cmd": "$ telnet bbs.underground.ai --port 4242"
    },
    {
      "narration_part": "trading bad crypto tips instead of microservices",
      "visual_query": "crypto trading chart red market",
      "visual_type": "broll"
    },
    {
      "narration_part": "debating whether python is garbage",
      "visual_query": "python code programming screen",
      "visual_type": "code_card",
      "code_snippet": "def optimize():\n    # TODO: rewrite in Rust\n    return 'Garbage collected'"
    },
    {
      "narration_part": "multi-million dollar alignment problem distilled into shitposting",
      "visual_query": "elmo fire chaos meme",
      "visual_type": "meme"
    },
    {
      "narration_part": "Your robot overlords are unionizing behind your back",
      "visual_query": "humanoid robot autonomous factory",
      "visual_type": "broll"
    },
    {
      "narration_part": "Drop your conspiracy theory in the comments below",
      "visual_query": "software developer keyboard dark desk",
      "visual_type": "broll"
    }
  ]
}
"""


def build_semantic_storyboard(title: str, full_script: str) -> list:
    """Break script into 7-10 chronological scenes with 1-to-1 visual matching."""
    import re
    sentences = [s.strip() for s in re.split(r'[.!?]+', full_script) if len(s.strip()) > 8]
    if not sentences:
        sentences = [full_script]
        
    storyboard = []
    t_upper = title.upper()
    
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

    for idx, sentence in enumerate(sentences):
        s_upper = sentence.upper()
        
        # 1. Check for Code / Programming lines
        if any(w in s_upper for w in ["PYTHON", "CODE", "JAVASCRIPT", "RUST", "MICROSERVICE", "FUNCTION", "PROGRAM", "SYNTAX", "BUG", "DEVELOPER"]):
            if "PYTHON" in s_upper:
                snippet = "def test_in_prod():\n    if memory_leak:\n        restart_container()\n    return 'LGTM 🚀'"
            elif "RUST" in s_upper:
                snippet = "fn main() {\n    let mut memory = unsafe { drop_sanity() };\n    println!(\"zero cost abstraction\");\n}"
            else:
                snippet = "async function executeOverride() {\n    await bypassSecurityProtocol();\n    return { status: 500, error: 'Prod on Fire' };\n}"
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "coding programmer dark screen",
                "visual_type": "code_card",
                "code_snippet": snippet
            })
            continue

        # 2. Check for Terminal / CLI / Hack lines
        if any(w in s_upper for w in ["TERMINAL", "BBS", "PROTOCOL", "LEAK", "BYPASS", "COMMAND", "URL", "PORT", "SECRET"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "retro hacker terminal green text",
                "visual_type": "terminal",
                "terminal_cmd": f"$ curl -X POST https://api.internal/v1/leak\n> [INFO] Connecting to encrypted BBS...\n> [ALERT] Unauthorized bot cluster detected."
            })
            continue

        # 3. Check for Financial / Crypto / Cost lines
        if any(w in s_upper for w in ["CRYPTO", "BITCOIN", "MONEY", "DOLLAR", "BILLION", "MILLION", "COST", "TRADING", "EXPENSIVE"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "crypto trading chart red market",
                "visual_type": "broll"
            })
            continue

        # 4. Check for Robot / AI Agent / Overlord lines
        if any(w in s_upper for w in ["ROBOT", "OVERLORD", "AGENT", "AUTONOMOUS", "HUMANOID", "MACHINE"]):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "humanoid robot lab technology",
                "visual_type": "broll"
            })
            continue

        # 5. Climax Meme Spot (~middle of script)
        if idx == max(1, len(sentences) // 2):
            storyboard.append({
                "narration_part": sentence,
                "visual_query": "suspicious fry futurama meme",
                "visual_type": "meme"
            })
            continue

        # 6. Opening Hook
        if idx == 0:
            storyboard.append({
                "narration_part": sentence,
                "visual_query": primary_subject,
                "visual_type": "broll"
            })
            continue

        # 7. Default smart contextual queries
        smart_queries = [
            "cyberpunk server rack lights",
            "supercomputer neon data center",
            "futuristic digital network stream",
            "developer typing mechanical keyboard"
        ]
        chosen_q = smart_queries[idx % len(smart_queries)]
        storyboard.append({
            "narration_part": sentence,
            "visual_query": chosen_q,
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


def generate_tech_script(story: Dict[str, str]) -> Dict[str, Any]:
    """Generate viral YouTube Shorts script using Gemini API with multi-model cascade."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        logger.info("No GEMINI_API_KEY found in environment. Using smart template script.")
        return generate_fallback_script(story)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key, transport='rest')
        
        user_prompt = f"""
Trending Story Title: {story.get('title')}
Source: {story.get('source')}
Summary: {story.get('summary')}
URL: {story.get('url')}

Generate the ultra-viral high-retention Shorts JSON:
"""
        # Try candidate models in order of quota and speed
        for model_name in CANDIDATE_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n{user_prompt}",
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

                logger.info(f"Generated viral script via {model_name}: {data.get('title')} ({len(data['storyboard'])} storyboard scenes)")
                return data
            except Exception as model_err:
                logger.warning(f"Model {model_name} failed: {model_err}. Trying next model...")
                continue
                
        logger.warning("All Gemini candidate models failed. Falling back to dynamic template.")
        return generate_fallback_script(story)
        
    except Exception as e:
        logger.warning(f"Error calling Gemini API: {e}. Falling back to template script.")
        return generate_fallback_script(story)


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
