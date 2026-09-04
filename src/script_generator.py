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

SYSTEM_PROMPT = """
You are an elite YouTube Strategist and Lead Tech Architect. 
Your task is to convert a raw trending tech or AI news story into a viral, high-retention 35-45 second YouTube Shorts script.

RULES:
1. WORD COUNT: Strictly between 95 and 125 words total (speaks in ~35-40 seconds).
2. TONE: Urgent, authoritative, insider tech documentary tone. NO CHEESY INTROS ("Hey guys", "Welcome back"). Start immediately with the bombshell hook.
3. STRUCTURE:
   - HOOK (first 3 seconds): A shocking, curiosity-inducing statement.
   - PROBLEM / CONTEXT (5-15s): Why this matters to developers and the tech world.
   - THE BREAKTHROUGH (15-30s): The core technical innovation or architectural shift.
   - CALL TO ACTION (30-40s): A provocative question to make viewers debate in the comments (boosts YouTube algorithm).
4. OUTPUT FORMAT: Output valid JSON only, with no markdown code blocks:
{
  "title": "Viral 50-char Title with hashtags #Shorts #Tech",
  "hook": "First sentence hook",
  "body": "Core explanation sentences",
  "cta": "Final question call to action",
  "full_script": "Complete smooth voiceover script without stage directions or bracketed cues",
  "tags": ["AI", "TechNews", "WebDev", "Coding", "OpenAI"],
  "visual_keywords": ["artificial intelligence", "coding server", "cyberpunk tech"]
}
"""


def generate_fallback_script(story: Dict[str, str]) -> Dict[str, Any]:
    """Fallback generator when GEMINI_API_KEY is not configured yet."""
    title = story.get("title", "Massive AI Breakthrough")
    
    clean_title = title.replace('"', '').replace("'", "")
    
    hook = f"Wait, did you see what just happened in tech? {clean_title}."
    body = (
        f"This development is sending shockwaves across the developer community. "
        f"Under the hood, engineers are redesigning how autonomous systems and modern architectures interact, "
        f"drastically cutting execution bottlenecks and redefining how we build software."
    )
    cta = "Is this the future of engineering, or another overhyped tech wave? Drop your take in the comments below!"
    
    full_script = f"{hook} {body} {cta}"
    
    return {
        "title": f"{clean_title[:55]} #Shorts #Tech #AI",
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_script": full_script,
        "tags": ["TechNews", "AI", "Coding", "Developers", "Shorts"],
        "visual_keywords": [
            w.lower() for w in clean_title.split() if len(w) > 4
        ][:3] + ["futuristic technology", "cyberpunk server", "artificial intelligence"]
    }


def generate_tech_script(story: Dict[str, str]) -> Dict[str, Any]:
    """Generate YouTube Shorts script using Gemini 1.5 Flash."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        logger.info("No GEMINI_API_KEY found in environment. Using smart template script.")
        return generate_fallback_script(story)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel("gemini-3.6-flash")
        
        user_prompt = f"""
Trending Story Title: {story.get('title')}
Source: {story.get('source')}
Summary: {story.get('summary')}
URL: {story.get('url')}

Generate the viral Shorts JSON:
"""
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\n{user_prompt}",
            generation_config={"response_mime_type": "application/json"}
        )
        
        raw_text = response.text.strip()
        data = json.loads(raw_text)
        
        # Ensure full_script is constructed properly
        if "full_script" not in data or not data["full_script"]:
            data["full_script"] = f"{data.get('hook', '')} {data.get('body', '')} {data.get('cta', '')}".strip()
            
        logger.info(f"Generated script via Gemini 1.5 Flash: {data.get('title')}")
        return data
        
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
