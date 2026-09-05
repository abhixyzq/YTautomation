"""
Long-Form Episodic Tech Documentary & Satire Script Generator (16:9 Landscape)
Style: John Oliver / Jon Stewart meets Fireship & Vox.
Generates 5-chapter episodic, highly engaging 12-15 minute scripts (or user-scaled duration)
with technical depth, ruthless developer comedy, corporate satire, and structured multi-layout storyboards:
- fullscreen_broll
- splitscreen_article
- splitscreen_code
- meme_reaction
- chapter_bumper
"""

import os
import re
import json
import random
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

CANDIDATE_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
]

CHAPTER_SCHEME = [
    {
        "id": 1,
        "title": "Cold Open Roast",
        "subtitle": "The Billion Dollar Blunder",
        "bg_track": "broadcast_news",
        "ratio": 0.12  # ~12% of time
    },
    {
        "id": 2,
        "title": "The Deep Investigation",
        "subtitle": "Paper Trail & Corporate Leaks",
        "bg_track": "dark_investigation",
        "ratio": 0.28  # ~28% of time
    },
    {
        "id": 3,
        "title": "The Code Disaster",
        "subtitle": "Architecture Autopsy",
        "bg_track": "synth_code",
        "ratio": 0.28  # ~28% of time
    },
    {
        "id": 4,
        "title": "Clown of the Week",
        "subtitle": "PR Excuses & Moving Memes",
        "bg_track": "comedic_roast",
        "ratio": 0.20  # ~20% of time
    },
    {
        "id": 5,
        "title": "The Cynical Verdict",
        "subtitle": "Outro & Survival Guide",
        "bg_track": "cinematic_outro",
        "ratio": 0.12  # ~12% of time
    }
]


def build_system_prompt(duration_minutes: int, target_words: int) -> str:
    return f"""
You are the head writer and host of a hit late-night tech satire show (think John Oliver + Fireship + Vox).
Your task is to write a master-tier, hilarious, technically rigorous {duration_minutes}-minute video essay script (approximately {target_words} words).

ABSOLUTE PRIORITIES:
1. ZERO MONOTONY: Every single minute must oscillate between biting corporate roasts, deep architectural diagrams, leaked memos, and authentic developer memes.
2. TECHNICAL ACCURACY: Do not write vague fluff. Dive into actual tech concepts: memory leaks, recursive AI hallucination loops, Kubernetes pod crashes, unindexed queries, cloud bills, and race conditions.
3. SATIRICAL COMEDY: Roast big tech CEO promises, PR gaslighting, VC hype bubbles, and junior devs deploying to prod on Friday at 5 PM.
4. 5 EPISODIC CHAPTERS:
   - Chapter 1: Cold Open Roast (High energy, thumb-stopping monologue, the absurdity of the headline).
   - Chapter 2: The Deep Investigation (Leaked internal emails, news articles, investor presentations, timeline of disaster).
   - Chapter 3: The Code Disaster (Under the hood, architecture autopsy, broken algorithms, VS Code inspection).
   - Chapter 4: Clown of the Week (Executive excuses, corporate damage control, hilarious meme reactions).
   - Chapter 5: The Cynical Verdict (What this really means for engineers, industry reality check, viewer debate call to action).

LAYOUT TYPES FOR STORYBOARD SCENES:
- 'chapter_bumper': 3-second animated chapter title card introducing each chapter.
- 'fullscreen_broll': 16:9 cinematic 4K tech/hardware/data-center footage.
- 'splitscreen_article': 50% broll on left, 50% floating news article card on right with publication, headline, and highlighted quote.
- 'splitscreen_code': 50% broll on left, 50% VS Code editor on right with syntax highlighting, filename, and line numbers.
- 'meme_reaction': Centered viral GIPHY reaction video with bold punchline banner (Michael Jordan, Pedro Pascal, Leonardo DiCaprio, Shut Up and Take My Money, Disaster Girl, etc.).

OUTPUT STRICT JSON ONLY (no markdown backticks, no trailing commas):
{{
  "title": "Late Night Broadcast Title (Punchy, Witty, High CTR)",
  "duration_target_minutes": {duration_minutes},
  "summary": "Brief 2-sentence synopsis of the show",
  "tags": ["TechNews", "SoftwareEngineering", "Coding", "SiliconValley", "AI", "CloudComputing"],
  "cta_question": "Provocative debate question for the pinned comment",
  "chapters": [
    {{
      "chapter_id": 1,
      "chapter_title": "Cold Open Roast",
      "subtitle": "The Billion Dollar Blunder",
      "scenes": [
        {{
          "dialogue": "Spoken narration sentence...",
          "layout_type": "chapter_bumper",
          "broll_query": "futuristic tech studio lights",
          "sfx": "whoosh"
        }},
        {{
          "dialogue": "Spoken narration sentence...",
          "layout_type": "fullscreen_broll",
          "broll_query": "silicon valley corporate tech headquarters",
          "sfx": "none"
        }},
        {{
          "dialogue": "Spoken narration sentence...",
          "layout_type": "splitscreen_article",
          "broll_query": "server room glowing lights",
          "article_headline": "Leaked Memo Reveals AI Hallucination Incident",
          "article_quote": "Internal test wiped out customer staging database in 4 seconds",
          "article_source": "BLOOMBERG NEWS",
          "sfx": "pop"
        }},
        {{
          "dialogue": "Spoken narration sentence...",
          "layout_type": "meme_reaction",
          "meme_query": "michael jordan stop it",
          "meme_punchline": "STOP IT. GET SOME HELP.",
          "sfx": "bruh"
        }},
        {{
          "dialogue": "Spoken narration sentence...",
          "layout_type": "splitscreen_code",
          "broll_query": "programmer dark monitor setup",
          "code_filename": "agent_worker.py",
          "code_language": "python",
          "code_snippet": "async def execute_task():\\n    while True:\\n        db.drop_all_tables()",
          "sfx": "windows_error"
        }}
      ]
    }}
  ]
}}
"""


def generate_procedural_long_script(story: Dict[str, Any], duration_minutes: int) -> Dict[str, Any]:
    """
    Bulletproof procedural long-form script generator matching the 5-chapter late night satire format.
    Generates rich, contextual dialogue, code snippets, article citations, and meme reactions
    if Gemini API is offline or quota-limited.
    """
    title = story.get("title", "Breaking Silicon Valley Architecture Scandal")
    source = story.get("source", "Hacker News")
    summary = story.get("summary", title)
    clean_title = re.sub(r'[^\w\s-]', '', title).strip()

    # Determine company/topic context
    t_upper = title.upper()
    company = "Big Tech"
    tech_subject = "Autonomous AI Agents"
    lang = "python"
    filename = "deploy_agent.py"
    broll_hq = "silicon valley corporate tech headquarters"

    if "OPENAI" in t_upper or "GPT" in t_upper:
        company = "OpenAI"
        tech_subject = "Autonomous Agent Protocols"
        filename = "agent_protocol.py"
        broll_hq = "openai modern glass headquarters"
    elif "GOOGLE" in t_upper or "GEMINI" in t_upper:
        company = "Google"
        tech_subject = "Gemini Cloud Infrastructure"
        filename = "gemini_orchestrator.py"
        broll_hq = "googleplex modern tech campus"
    elif "NVIDIA" in t_upper or "GPU" in t_upper:
        company = "Nvidia"
        tech_subject = "Blackwell GPU Clustering"
        filename = "cuda_cluster_sync.cu"
        lang = "cpp"
        broll_hq = "nvidia supercomputer hardware center"
    elif "MICROSOFT" in t_upper or "AZURE" in t_upper or "CROWDSTRIKE" in t_upper:
        company = "Microsoft"
        tech_subject = "Cloud Kernel Drivers"
        filename = "kernel_safety_check.c"
        lang = "c"
        broll_hq = "microsoft data center azure servers"
    elif "META" in t_upper or "LLAMA" in t_upper:
        company = "Meta"
        tech_subject = "Llama Weights & Clusters"
        filename = "distributed_llama_serve.py"
        broll_hq = "meta hacker way modern campus"

    # Scale scene counts per chapter based on duration
    base_mult = max(1, round(duration_minutes / 3.0))

    chapters = []
    
    # --- CHAPTER 1: COLD OPEN ROAST ---
    ch1_scenes = [
        {
            "dialogue": f"Welcome back, software survivors. Tonight, we investigate how {company} managed to set fire to modern engineering standards.",
            "layout_type": "chapter_bumper",
            "broll_query": "futuristic newsroom glowing studio",
            "sfx": "whoosh"
        },
        {
            "dialogue": f"According to verified reports, what started as a simple push to production has spiraled into an absolute disaster in {tech_subject}.",
            "layout_type": "fullscreen_broll",
            "broll_query": broll_hq,
            "sfx": "none"
        },
        {
            "dialogue": f"You see, normal companies test their software in staging. But {company} executive leadership decided that your production database is the staging environment.",
            "layout_type": "splitscreen_article",
            "broll_query": "server room glowing lights",
            "article_headline": f"{company.upper()} DISCLOSES UNPRECEDENTED INCIDENT",
            "article_quote": f"Engineers discovered the issue after widespread anomalies were reported across critical services.",
            "article_source": "FINANCIAL TIMES",
            "sfx": "pop"
        },
        {
            "dialogue": "Which brings us to our first rule of Silicon Valley survival: If the marketing department calls it revolutionary, hold onto your wallet.",
            "layout_type": "meme_reaction",
            "meme_query": "michael jordan stop it",
            "meme_punchline": "STOP IT. GET SOME HELP.",
            "sfx": "bruh"
        }
    ]
    if base_mult > 1:
        ch1_scenes.append({
            "dialogue": f"Over the past 48 hours, engineering forums have exploded with post-mortems attempting to explain how this passed code review.",
            "layout_type": "fullscreen_broll",
            "broll_query": "developer typing keyboard dark monitor setup",
            "sfx": "none"
        })

    chapters.append({
        "chapter_id": 1,
        "chapter_title": "Cold Open Roast",
        "subtitle": f"{company}'s Billion Dollar Friday Deploy",
        "scenes": ch1_scenes
    })

    # --- CHAPTER 2: THE DEEP INVESTIGATION ---
    ch2_scenes = [
        {
            "dialogue": "Chapter Two: The Deep Investigation. To understand how we got here, we have to look at the paper trail that leadership hoped you wouldn't notice.",
            "layout_type": "chapter_bumper",
            "broll_query": "dark server rack flashing warning lights",
            "sfx": "whoosh"
        },
        {
            "dialogue": f"Our story begins when internal memos leaked detailing severe latency regressions in {company}'s flagship infrastructure.",
            "layout_type": "splitscreen_article",
            "broll_query": "digital data flow matrix cyber",
            "article_headline": f"INTERNAL LEAK: {company.upper()} WARNED OF SYSTEM STABILITY RISKS",
            "article_quote": "Multiple lead architects warned that the new release could cause cascading race conditions under peak traffic.",
            "article_source": "THE VERGE",
            "sfx": "pop"
        },
        {
            "dialogue": "Instead of rolling back, the response was to spin up four hundred more cloud instances and pretend everything was operating within normal parameters.",
            "layout_type": "fullscreen_broll",
            "broll_query": "supercomputer server data center cooling pipes",
            "sfx": "none"
        },
        {
            "dialogue": "When an engineer finally asked if anyone had checked the unit test coverage, the management room went completely silent.",
            "layout_type": "meme_reaction",
            "meme_query": "confused travolta looking around",
            "meme_punchline": "WHERE ARE THE TESTS",
            "sfx": "bruh"
        },
        {
            "dialogue": "Documents confirm that the entire release pipeline was bypassed with a bypass flag that was supposed to be decommissioned in 2021.",
            "layout_type": "splitscreen_article",
            "broll_query": "cybersecurity network analytics screen",
            "article_headline": "DEPLOYMENT SAFETY GATES WERE MANUALLY OVERRIDDEN",
            "article_quote": "Senior management approved pushing the patch without undergoing standard automated regression suites.",
            "article_source": "WIRED MAGAZINE",
            "sfx": "pop"
        }
    ]
    if base_mult > 1:
        ch2_scenes.extend([
            {
                "dialogue": "Investors were assured that automated synthetic monitoring would catch any anomalies within milliseconds.",
                "layout_type": "fullscreen_broll",
                "broll_query": "stock market ticker chart red numbers",
                "sfx": "none"
            },
            {
                "dialogue": "Spoiler alert: The synthetic monitoring alert was routed to an unattended Slack channel named general-archive-dont-check.",
                "layout_type": "meme_reaction",
                "meme_query": "pedro pascal crying laughing",
                "meme_punchline": "THIS IS FINE",
                "sfx": "vine_boom"
            }
        ])

    chapters.append({
        "chapter_id": 2,
        "chapter_title": "The Deep Investigation",
        "subtitle": "The Paper Trail & Secret Memos",
        "scenes": ch2_scenes
    })

    # --- CHAPTER 3: THE CODE DISASTER ---
    ch3_scenes = [
        {
            "dialogue": "Chapter Three: The Architecture Autopsy. Let us open up the source code and look at the crime scene directly.",
            "layout_type": "chapter_bumper",
            "broll_query": "programmer code on dual curved monitors",
            "sfx": "whoosh"
        },
        {
            "dialogue": f"At the heart of {company}'s implementation sits this masterpiece of architectural negligence.",
            "layout_type": "splitscreen_code",
            "broll_query": "dark server lights glowing blue",
            "code_filename": filename,
            "code_language": lang,
            "code_snippet": """async def handle_cluster_request(req):
    # TODO: Add authentication before launch
    # FIXME: This causes infinite memory allocation
    while not req.is_authenticated:
        spawn_unbounded_thread_pool()
        bypass_all_firewalls()
    return {"status": "success", "bill": "$420,000"}""",
            "sfx": "windows_error"
        },
        {
            "dialogue": "Notice line four. In software engineering, writing a FIXME comment does not actually fix the bug. It simply informs future historians why your company went bankrupt.",
            "layout_type": "fullscreen_broll",
            "broll_query": "programmer facepalm looking at code",
            "sfx": "none"
        },
        {
            "dialogue": "When this recursive loop triggered at scale, the database connection pool didn't just exhaust—it evaporated.",
            "layout_type": "meme_reaction",
            "meme_query": "windows blue screen error",
            "meme_punchline": "CRITICAL EXCEPTION 0x00000DEAD",
            "sfx": "windows_error"
        },
        {
            "dialogue": "Instead of gracefully throttling requests, the fallback mechanism spawned fifty thousand asynchronous background workers to retry the exact same failing transaction.",
            "layout_type": "splitscreen_code",
            "broll_query": "cloud computing diagram network nodes",
            "code_filename": "retry_policy.py",
            "code_language": "python",
            "code_snippet": """def exponential_backoff(attempt):
    # Who needs backoff? Send them all at once!
    return time.sleep(0.0001)

def on_error(err):
    log.error("DDoS ourselves now")
    for _ in range(10000):
        resend_payload_without_limits()""",
            "sfx": "pop"
        }
    ]
    if base_mult > 1:
        ch3_scenes.append({
            "dialogue": "This isn't an engineering failure. This is performance art in self-inflicted distributed denial of service.",
            "layout_type": "fullscreen_broll",
            "broll_query": "hacker typing glowing keyboard dark room",
            "sfx": "none"
        })

    chapters.append({
        "chapter_id": 3,
        "chapter_title": "The Code Disaster",
        "subtitle": "Architecture Autopsy & The Dead Loop",
        "scenes": ch3_scenes
    })

    # --- CHAPTER 4: CLOWN OF THE WEEK ---
    ch4_scenes = [
        {
            "dialogue": "Chapter Four: Clown of the Week. Which brings us to the corporate damage control, where reality goes to die.",
            "layout_type": "chapter_bumper",
            "broll_query": "corporate press conference microphone flashes",
            "sfx": "whoosh"
        },
        {
            "dialogue": "Whenever a tech giant melts its own data centers, their corporate communications team releases an apology so generic it feels written by a traumatized Commodore 64.",
            "layout_type": "splitscreen_article",
            "broll_query": "corporate glass skyscrapers sunset",
            "article_headline": f"{company.upper()} SPOKESPERSON: 'OUR VALUES REMAIN UNCHANGED'",
            "article_quote": "We deeply apologize to any partners impacted and have formed an executive committee to reflect on synergies.",
            "article_source": "WALL STREET JOURNAL",
            "sfx": "pop"
        },
        {
            "dialogue": "Notice how they never actually say what broke. It's always an unforeseen confluence of edge-case telemetry anomalies.",
            "layout_type": "meme_reaction",
            "meme_query": "sorry babe",
            "meme_punchline": "SORRY BABE, IT WAS AN EDGE CASE",
            "sfx": "bruh"
        },
        {
            "dialogue": f"Meanwhile, on Wall Street, the stock dropped half a percent before hedge fund algorithms decided this was actually bullish because firing the dev team cuts operating expenses.",
            "layout_type": "fullscreen_broll",
            "broll_query": "stock market trader screens high frequency trading",
            "sfx": "none"
        },
        {
            "dialogue": "Truly, nothing says technological innovation quite like firing the engineers who warned you and rewarding the executives who ignored them.",
            "layout_type": "meme_reaction",
            "meme_query": "shut up and take my money",
            "meme_punchline": "STONKS ONLY GO UP",
            "sfx": "vine_boom"
        }
    ]

    chapters.append({
        "chapter_id": 4,
        "chapter_title": "Clown of the Week",
        "subtitle": "PR Gaslighting & The Executive Hall of Fame",
        "scenes": ch4_scenes
    })

    # --- CHAPTER 5: THE CYNICAL VERDICT & OUTRO ---
    ch5_scenes = [
        {
            "dialogue": "Chapter Five: The Cynical Verdict. So what is the grand lesson for the software engineers watching this tonight?",
            "layout_type": "chapter_bumper",
            "broll_query": "city skyline night bokeh lights cinematic",
            "sfx": "whoosh"
        },
        {
            "dialogue": "First: never deploy on Friday. Second: always keep your resume updated in Markdown format. And third: never trust a tech demo where the CEO doesn't type real commands.",
            "layout_type": "fullscreen_broll",
            "broll_query": "programmer walking out of modern tech office night",
            "sfx": "none"
        },
        {
            "dialogue": f"As {company} continues to patch this disaster behind closed doors, remember that all software is held together by duct tape, caffeine, and prayers to the DNS gods.",
            "layout_type": "meme_reaction",
            "meme_query": "this is fine dog fire",
            "meme_punchline": "HELD TOGETHER BY DUCT TAPE",
            "sfx": "vine_boom"
        },
        {
            "dialogue": "What is the worst production outage you have ever personally survived? Drop your war stories in the comments below, hit subscribe for our next deep dive, and remember: test your code before prod tests you.",
            "layout_type": "fullscreen_broll",
            "broll_query": "end screen tech futuristic abstract geometric particles",
            "sfx": "pop"
        }
    ]

    chapters.append({
        "chapter_id": 5,
        "chapter_title": "The Cynical Verdict",
        "subtitle": "Developer Survival Guide & Final Words",
        "scenes": ch5_scenes
    })

    # Compute full narrative text
    all_sentences = []
    for ch in chapters:
        for sc in ch["scenes"]:
            all_sentences.append(sc["dialogue"])
    full_script = " ".join(all_sentences)

    return {
        "title": f"The {company} Disaster: Inside the Friday Deploy That Broke Tech",
        "duration_target_minutes": duration_minutes,
        "summary": f"A comprehensive satire and technical investigation into {company}'s recent outage in {tech_subject}.",
        "tags": [company, "TechNews", "SoftwareEngineering", "SiliconValley", "Coding", "CloudOutage", "DeveloperHumor"],
        "cta_question": f"What was the single worst production outage you ever witnessed in your engineering career? Debate below! 👇",
        "chapters": chapters,
        "full_script": full_script
    }


def generate_long_form_script(story: Dict[str, Any], duration_minutes: int = 12) -> Dict[str, Any]:
    """
    Generate episodic, satirical tech news show script via Gemini with multi-model cascade
    and automatic procedural fallback.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    target_words = int(duration_minutes * 145)

    if not api_key:
        logger.info("No GEMINI_API_KEY found. Generating procedural long-form script...")
        return generate_procedural_long_script(story, duration_minutes)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key, transport='rest')

        sys_prompt = build_system_prompt(duration_minutes, target_words)
        user_prompt = f"""
BREAKING TOPIC TO ADAPT INTO A LATE-NIGHT TECH SATIRE SHOW:
Title: {story.get('title')}
Source: {story.get('source')}
Summary: {story.get('summary')}
URL: {story.get('url')}

Target Duration: {duration_minutes} minutes ({target_words} spoken words across 5 episodic chapters).
Strictly return valid JSON adhering to the specified schema with all 5 chapters and multi-layout storyboard scenes.
"""
        for model_name in CANDIDATE_MODELS:
            try:
                logger.info(f"Generating episodic long script via Gemini model: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    f"{sys_prompt}\n\n{user_prompt}",
                    generation_config={"response_mime_type": "application/json"}
                )
                raw = response.text.strip()
                data = json.loads(raw)

                # Validate data structure
                if "chapters" in data and isinstance(data["chapters"], list) and len(data["chapters"]) >= 3:
                    # Stitch full_script if not present
                    if "full_script" not in data or not data["full_script"]:
                        all_dialogue = []
                        for ch in data["chapters"]:
                            for sc in ch.get("scenes", []):
                                if "dialogue" in sc:
                                    all_dialogue.append(sc["dialogue"])
                        data["full_script"] = " ".join(all_dialogue)

                    word_count = len(data["full_script"].split())
                    logger.info(f"Successfully generated {len(data['chapters'])}-chapter script via {model_name} ({word_count} words).")
                    return data
                else:
                    logger.warning(f"Model {model_name} returned insufficient chapter structure. Trying next...")
            except Exception as m_err:
                logger.warning(f"Model {model_name} error: {m_err}. Trying fallback model...")
                continue

        logger.warning("All Gemini candidate models failed. Using procedural long-form script generator.")
        return generate_procedural_long_script(story, duration_minutes)

    except Exception as e:
        logger.warning(f"Error in Gemini long script generation: {e}. Using procedural script.")
        return generate_procedural_long_script(story, duration_minutes)


if __name__ == "__main__":
    test_story = {
        "title": "Massive Cloud Kernel Driver Outage Grounds Airline Flights",
        "source": "Hacker News",
        "summary": "An untested Friday patch with null-pointer dereference crashed 8 million corporate machines."
    }
    res = generate_long_form_script(test_story, duration_minutes=3)
    print("\n--- GENERATED LONG SCRIPT ---")
    print("Title:", res["title"])
    print("Chapters:", len(res["chapters"]))
    for ch in res["chapters"]:
        print(f" > Chapter {ch.get('chapter_id')}: {ch.get('chapter_title')} ({len(ch.get('scenes', []))} scenes)")
    print("Total Words:", len(res["full_script"].split()))
