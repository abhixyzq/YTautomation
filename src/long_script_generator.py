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
import time
import random
import logging
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

CANDIDATE_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
    "gemini-pro-latest",
]

CHAPTER_SCHEME = [
    {
        "id": 1,
        "title": "Act 1: The Paradox",
        "subtitle": "The Impossible Premise",
        "bg_track": "dark_investigation",
        "ratio": 0.20  # ~20% of time
    },
    {
        "id": 2,
        "title": "Act 2: First Principles",
        "subtitle": "Deconstruction & Visual Analogy",
        "bg_track": "synth_code",
        "ratio": 0.30  # ~30% of time
    },
    {
        "id": 3,
        "title": "Act 3: The Breaking Point",
        "subtitle": "Forensic Autopsy & Catastrophe",
        "bg_track": "broadcast_news",
        "ratio": 0.30  # ~30% of time
    },
    {
        "id": 4,
        "title": "Act 4: The Paradigm Shift",
        "subtitle": "The Uncomfortable Reality",
        "bg_track": "cinematic_outro",
        "ratio": 0.20  # ~20% of time
    }
]


def build_system_prompt(duration_minutes: int, target_words: int, language: str = "en") -> str:
    is_hindi = language.lower() in ("hi", "hindi", "dastawez")
    
    lang_directive = """
LANGUAGE & SCRIPT RULES (HINDI DEVANAGARI):
- Write the ENTIRE spoken script (all "dialogue" fields, chapter titles, subtitles, summary, cta_question) in fluent, intellectual, engaging HINDI (हिन्दी - Devanagari script).
- Style: Think School / Dhruv Rathee / Discovery Science Hindi commentary.
- International technical words (e.g. 'सॉफ्टवेयर', 'रॉकेट', 'इंजीनियरिंग', 'सिस्टम', 'आर्किटेक्चर', '64-बिट', 'एल्गोरिदम') can be used naturally in Devanagari.
- CRITICAL: All visual queries ("broll_query", search terms) MUST ALWAYS BE IN ENGLISH so visual search engines (Pexels, stock footage) find the correct 4K clips!
""" if is_hindi else """
LANGUAGE: Fluent, intellectual, captivating English (in the style of Veritasium, Lemmino, Johnny Harris).
"""

    return f"""
You are the lead science & technology documentary essayist (in the style of Veritasium, Lemmino, Johnny Harris, and Think School).
Your mission is to produce a masterclass {duration_minutes}-minute video essay script (approximately {target_words} words).
The narrative must leave the audience breathless, elevating their understanding of technology, physics, and engineering.

{lang_directive}

ABSOLUTE PRIORITIES:
1. INTELLECTUAL MAGNETISM (HIGH-IQ STORYTELLING):
   - Hook the viewer with a mind-bending contradiction or shocking scientific reality.
   - Do NOT use cheap jokes, memes, slang, or generic tech filler.
   - Every minute must deliver dense, fascinating, first-principles insight that viewers will quote to their friends.
2. 4-ACT INQUIRY STRUCTURE:
   - Act 1: The Impossible Paradox (Establish the contradiction, the stakes, why conventional wisdom is wrong).
   - Act 2: First Principles & Visual Analogy (Deconstruct the physics/math/code into intuitive real-world metaphors).
   - Act 3: The Breaking Point / Forensic Autopsy (The historic catastrophe, timeline of events, the cascading chain of failures).
   - Act 4: The Paradigm Shift & Uncomfortable Reality (The philosophical conclusion, systemic fragility, provocative open question).
3. VISUAL STORYBOARD LAYOUTS (MUST USE RICH VISUAL METAPHORS):
   - 'fullscreen_broll': 16:9 4K archival, laboratory, or cinematic footage with lower-third kinetic captions.
   - 'blueprint_schematic': CAD technical wireframe blueprint with telemetry parameters.
   - 'kinetic_flowchart': Step-by-step causal logic chain (Step 1 -> Step 2 -> Step 3).
   - 'visual_analogy': Split card comparing abstract tech vs real-world physical metaphor with takeaway.
   - 'data_timeline_matrix': Chronological timeline autopsy of the disaster/breakthrough with severity badges.
   - 'splitscreen_stat': 3D metric counter with context and percentage change.
   - 'splitscreen_article': Floating verified source citation / declassified document.
   (IMPORTANT: Do NOT generate full-screen chapter bumper cards or title card pauses. The video must start DIRECTLY at 00:00 with immersive footage and narrative visuals).

OUTPUT STRICT JSON ONLY (no markdown backticks, no trailing commas):
{{
  "title": "Compelling Title in Question or Paradox Format",
  "duration_target_minutes": {duration_minutes},
  "summary": "2-sentence documentary synopsis",
  "tags": ["Technology", "Engineering", "Physics", "ComputerScience", "DeepDive"],
  "cta_question": "A philosophical or engineering dilemma for the comments",
  "chapters": [
    {{
      "chapter_id": 1,
      "chapter_title": "The Paradox",
      "subtitle": "The Impossible Premise",
      "scenes": [
        {{
          "dialogue": "Spoken narration opening the paradox...",
          "layout_type": "fullscreen_broll",
          "broll_query": "deep space dark telemetry glowing grid",
          "sfx": "whoosh"
        }},
        {{
          "dialogue": "Spoken narration detailing the shocking reality...",
          "layout_type": "blueprint_schematic",
          "broll_query": "quantum computer gold wiring cryogenic chamber",
          "schematic_title": "QUANTUM CRYPTOGRAPHY TELEMETRY",
          "schematic_tag": "SPEC // QUANTUM-GATE-TOPOLOGY",
          "schematic_specs": [
            {{"label": "KEY LENGTH", "value": "2048-BIT RSA"}},
            {{"label": "CLASSICAL SEARCH", "value": "10^30 YEARS"}},
            {{"label": "SHOR'S ALGORITHM", "value": "8.4 HOURS"}},
            {{"label": "SYSTEMIC RISK", "value": "CRITICAL 100%"}}
          ],
          "sfx": "pop"
        }},
        {{
          "dialogue": "Spoken narration deconstructing the concept...",
          "layout_type": "visual_analogy",
          "analogy_title": "THE CRYPTOGRAPHIC METAPHOR",
          "concept_name": "PRIME FACTORIZATION",
          "concept_desc": "Multiplying two 300-digit primes takes milliseconds. Finding them back takes universe lifespans.",
          "analogy_name": "THE COLOR-MIXING VAULT",
          "analogy_desc": "Mixing two paint drops into brown is trivial. Separating the exact drops back out is impossible.",
          "takeaway": "Quantum computers don't unmix the paint—they test every photon state simultaneously.",
          "sfx": "none"
        }},
        {{
          "dialogue": "Spoken narration walking through the breakdown...",
          "layout_type": "kinetic_flowchart",
          "flowchart_title": "THE CASCADING MEMORY OVERFLOW",
          "flowchart_steps": [
            {{"step": 1, "label": "Horizontal Velocity Surge", "detail": "Value exceeds 32,767 integer boundary", "status": "normal"}},
            {{"step": 2, "label": "64-bit to 16-bit Cast", "detail": "Software lacks arithmetic overflow trap", "status": "active"}},
            {{"step": 3, "label": "Inertial Processor Halt", "detail": "Primary and backup units crash simultaneously", "status": "critical"}},
            {{"step": 4, "label": "Diagnostic Data into Nozzles", "detail": "Rocket swivels engines 90 degrees at Mach 2", "status": "critical"}}
          ],
          "sfx": "whoosh"
        }},
        {{
          "dialogue": "Spoken narration forensic timeline...",
          "layout_type": "data_timeline_matrix",
          "timeline_title": "FLIGHT 501 DISASTER TIMELINE",
          "timeline_events": [
            {{"time_label": "T+00.0s", "title": "Nominal Liftoff", "desc": "Twin solid rocket boosters ignite from Kourou", "severity": "info"}},
            {{"time_label": "T+36.7s", "title": "Guidance Computer Crash", "desc": "Both inertial reference units shut down", "severity": "warning"}},
            {{"time_label": "T+37.2s", "title": "Engine Swivel Hardover", "desc": "Aerodynamic shear rips boosters from main tank", "severity": "critical"}},
            {{"time_label": "T+39.0s", "title": "Automatic Self-Destruct", "desc": "500 million dollar payload detonated in atmosphere", "severity": "critical"}}
          ],
          "sfx": "pop"
        }},
        {{
          "dialogue": "Spoken narration highlighting scale...",
          "layout_type": "splitscreen_stat",
          "broll_query": "supercomputer processing data server room",
          "stat_number": "$500,000,000",
          "stat_label": "HARDWARE LOSS IN 37 SECONDS",
          "stat_context": "The most expensive software bug in human aerospace history.",
          "stat_change": "100% MISSION FAILURE",
          "sfx": "pop"
        }}
      ]
    }}
  ]
}}
"""


def generate_procedural_long_script(story: Dict[str, Any], duration_minutes: int, language: str = "en") -> Dict[str, Any]:
    """
    Bulletproof procedural long-form script generator matching the 4-Act Mind-Bending Visual Explainer format.
    Generates high-IQ scientific inquiry, physical analogies, CAD blueprints, and forensic timelines
    in both English (techByAbhi) and Hindi Devanagari (iDastawez).
    """
    is_hindi = language.lower() in ("hi", "hindi", "dastawez")
    title = story.get("title", "The Engineering Paradox That Broke Modern Computing")
    category = story.get("category", "Science & Deep Technology")
    core_paradox = story.get("core_paradox", "What appears mathematically secure or physically stable collapses under edge-case conditions.")
    inciting_incident = story.get("inciting_incident", "A single overlooked flaw triggered an unprecedented systemic failure.")
    real_world_analogy = story.get("real_world_analogy", "Pouring a gallon of water into a pint glass—the boundary conditions were never validated.")
    catastrophe_case_study = story.get("catastrophe_case_study", "The primary and secondary fail-safes executed contradictory instructions.")
    paradigm_shift = story.get("paradigm_shift", "Complexity is the enemy of reliability. When technology controls physical systems, assumptions are fatal.")

    # Narrative scaling factor
    mult = max(1, round(duration_minutes / 3.0))
    chapters = []

    if is_hindi:
        # =============================================================
        # HINDI DEVANAGARI NARRATIVE (iDastawez)
        # =============================================================
        # Act 1
        act1_scenes = [
            {
                "dialogue": f"इस तकनीकी पहेली को समझने के लिए, हमें उस विरोधाभास से शुरुआत करनी होगी जिसने आधुनिक विज्ञान को हिलाकर रख दिया: {title}।",
                "layout_type": "fullscreen_broll",
                "broll_query": "deep space dark telemetry glowing grid",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"इस पूरी समस्या की जड़ हैरान करने वाली है: {core_paradox}",
                "layout_type": "blueprint_schematic",
                "broll_query": "quantum supercomputer cryogenic gold wiring",
                "schematic_title": "SYSTEM ARCHITECTURE // बुनियादी ढांचा",
                "schematic_tag": "TELEMETRY // बुनियादी नियम",
                "schematic_specs": [
                    {"label": "PRIMARY DOMAIN", "value": category.upper()[:20]},
                    {"label": "THEORETICAL LIMIT", "value": "O(N!) HARDNESS"},
                    {"label": "SYSTEMIC TOLERANCE", "value": "±0.0001%"},
                    {"label": "OBSERVED RISK", "value": "CRITICAL THRESHOLD"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "सालों तक दुनिया भर के इंजीनियरों और शोधकर्ताओं ने इस सिस्टम को अचूक माना। लेकिन जब इस पर चरम दबाव डाला गया, तो पूरी सुरक्षा प्रणाली चरमरा गई।",
                "layout_type": "splitscreen_stat",
                "broll_query": "server rack data center fiber optic glowing",
                "stat_number": "99.999%",
                "stat_label": "THEORETICAL RELIABILITY",
                "stat_context": "सिस्टम पूरी तरह सुरक्षित माना गया जब तक कि सीमाएं नहीं टूटीं।",
                "stat_change": "CASCADE FAILURE",
                "sfx": "pop"
            },
            {
                "dialogue": f"यह कोई साधारण दुर्घटना नहीं थी—यह सैद्धांतिक गणित और वास्तविक भौतिकी के बीच की अनिवार्य टक्कर थी: {inciting_incident}",
                "layout_type": "fullscreen_broll",
                "broll_query": "laboratory microscope semiconductor silicon wafer",
                "sfx": "none"
            }
        ]
        if mult > 1:
            act1_scenes.append({
                "dialogue": "यह समझने के लिए कि सब गलत दिशा में क्यों देख रहे थे, हमें इस सिस्टम को इसके बुनियादी परमाणुओं तक डिकोड करना होगा।",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic data telemetry particle wave abstract",
                "sfx": "whoosh"
            })

        chapters.append({
            "chapter_id": 1,
            "chapter_title": "अध्याय 1: असंभव विरोधाभास (The Paradox)",
            "subtitle": "असंभव पहेली",
            "scenes": act1_scenes
        })

        # Act 2
        act2_scenes = [
            {
                "dialogue": "जब जटिल तकनीक हमें उलझाती है, तो उसका समाधान भारी-भरकम शब्दों में नहीं, बल्कि एक सटीक भौतिक उदाहरण में छिपा होता है।",
                "layout_type": "fullscreen_broll",
                "broll_query": "cinematic physics lab laser beam optics",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"जरा इस उदाहरण पर विचार कीजिए: {real_world_analogy}",
                "layout_type": "visual_analogy",
                "analogy_title": "THE PHYSICAL ANALOGY // भौतिक उदाहरण",
                "concept_name": "THE ABSTRACT ALGORITHM",
                "concept_desc": "सिलिकॉन चिप्स के अंदर चलने वाली जटिल गणितीय गणनाएं।",
                "analogy_name": "THE REAL-WORLD METAPHOR",
                "analogy_desc": real_world_analogy,
                "takeaway": "जब सॉफ्टवेयर प्रकृति के भौतिक नियमों को भूल जाता है, तो तबाही अनिवार्य हो जाती है।",
                "sfx": "pop"
            },
            {
                "dialogue": "ध्यान से देखिए इस छिपे हुए जाल को। गणित की दुनिया में संख्याएं अनंत और संपूर्ण होती हैं, लेकिन असली सिलिकॉन चिप में हर बाइट इलेक्ट्रॉनों की भौतिक हलचल पर टिकी होती है।",
                "layout_type": "blueprint_schematic",
                "broll_query": "integrated circuit microchip electron microscope",
                "schematic_title": "THERMODYNAMIC BOUNDARY MAP",
                "schematic_tag": "PHYSICS // हार्डवेयर सीमाएं",
                "schematic_specs": [
                    {"label": "BIT REGISTER DEPTH", "value": "64-BIT IEEE-754"},
                    {"label": "FLOATING OVERFLOW", "value": "> 32,767 LIMIT"},
                    {"label": "ENERGY DISSIPATION", "value": "10^-21 JOULES/BIT"},
                    {"label": "QUANTUM TUNNELING", "value": "ACTIVE RISK"}
                ],
                "sfx": "none"
            },
            {
                "dialogue": "हार्डवेयर की सीमाओं को नजरअंदाज करके, इंजीनियरों ने मान लिया था कि सॉफ्टवेयर भौतिक नियमों से परे है। यह भ्रम पहले बड़े परीक्षण तक ही टिक सका।",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic cleanroom engineer wearing hazmat suit silicon fab",
                "sfx": "none"
            }
        ]
        if mult > 1:
            act2_scenes.append({
                "dialogue": "इस बग को सबसे खतरनाक यह बात बनाती थी कि 100 में से 99 बार सिस्टम पूरी तरह सही चलता था। यह सिर्फ तभी फटा जब कई अप्रत्याशित घटनाएं एक साथ घटीं।",
                "layout_type": "splitscreen_stat",
                "broll_query": "supercomputer server nodes flashing green blue",
                "stat_number": "1 IN 10^9",
                "stat_label": "CRITICAL ANOMALY PROBABILITY",
                "stat_context": "अरबों ऑपरेशंस प्रति सेकंड की गति पर, यह दुर्लभ बग हर कुछ मिनट में आ सकता है।",
                "stat_change": "100% INEVITABLE",
                "sfx": "pop"
            })

        chapters.append({
            "chapter_id": 2,
            "chapter_title": "अध्याय 2: बुनियादी सिद्धांत (First Principles)",
            "subtitle": "भौतिक उदाहरण और विश्लेषण",
            "scenes": act2_scenes
        })

        # Act 3
        act3_scenes = [
            {
                "dialogue": "और फिर आया वह ऐतिहासिक निर्णायक मोड़, जब सभी सुरक्षा प्रणालियाँ एक साथ ताश के पत्तों की तरह ढह गईं।",
                "layout_type": "fullscreen_broll",
                "broll_query": "dark industrial telemetry warning lights flashing red",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"विफलता की वैज्ञानिक पड़ताल से जो खुलासा हुआ, उसने पूरी दुनिया को हिलाकर रख दिया: {catastrophe_case_study}",
                "layout_type": "kinetic_flowchart",
                "flowchart_title": "FORENSIC CAUSAL LOGIC CHAIN // विफलता की श्रृंखला",
                "flowchart_steps": [
                    {"step": 1, "label": "Initial Sensor Discrepancy", "detail": "सेंसर डेटा ने मेमोरी सीमा को पार किया", "status": "normal"},
                    {"step": 2, "label": "Uncaught Exception", "detail": "सेफ्टी रूटीन सीपीयू समय बचाने के लिए बंद थी", "status": "active"},
                    {"step": 3, "label": "Diagnostic Data as Command", "detail": "एरर डेटा को सिस्टम ने कमांड समझ लिया", "status": "critical"},
                    {"step": 4, "label": "Complete Structural Catastrophe", "detail": "चरम भौतिक दबाव में सिस्टम पूरी तरह क्रैश हुआ", "status": "critical"}
                ],
                "sfx": "whoosh"
            },
            {
                "dialogue": "जब जांचकर्ताओं ने पूरे घटनाक्रम का सेकंड-दर-सेकंड विश्लेषण किया, तो पता चला कि हर बैकअप सिस्टम डोमिनोज़ की तरह एक के बाद एक फेल होता चला गया।",
                "layout_type": "data_timeline_matrix",
                "timeline_title": "CHRONOLOGICAL FORENSIC TIMELINE",
                "timeline_events": [
                    {"time_label": "T - 00:00", "title": "सिस्टम लॉन्च", "desc": "सभी प्राथमिक और बैकअप सेंसर पूरी तरह सामान्य थे।", "severity": "info"},
                    {"time_label": "T + 36.7s", "title": "प्राइमरी यूनिट क्रैश", "desc": "मेमोरी ओवरफ्लो के कारण मुख्य सीपीयू बंद हुआ।", "severity": "warning"},
                    {"time_label": "T + 37.2s", "title": "बैकअप यूनिट डुप्लीकेट क्रैश", "desc": "वही पुराना कोड बैकअप कंप्यूटर को भी ले डूबा।", "severity": "critical"},
                    {"time_label": "T + 39.0s", "title": "पूर्ण विखंडन", "desc": "चरम दबाव में सिस्टम ने खुद को नष्ट कर लिया।", "severity": "critical"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "आर्थिक और तकनीकी नुकसान अभूतपूर्व था। लेकिन सबसे चौंकाने वाली बात यह थी कि कोड टूटा नहीं था—बल्कि कोड ने बिल्कुल वही किया जो उसे प्रोग्राम किया गया था।",
                "layout_type": "splitscreen_article",
                "broll_query": "investigation declassified report document paper",
                "article_headline": "OFFICIAL INQUIRY BOARD DISCLOSES FINDINGS",
                "article_quote": "यह विफलता किसी हार्डवेयर खराबी से नहीं, बल्कि सॉफ्टवेयर आवश्यकताओं की गलत धारणाओं से हुई।",
                "article_source": "INDEPENDENT INQUIRY BOARD",
                "sfx": "pop"
            }
        ]
        if mult > 1:
            act3_scenes.append({
                "dialogue": "सुरक्षा कोड की सिर्फ एक साधारण लाइन इस पूरे विनाश को रोक सकती थी। लेकिन उस जांच को जानबूझकर छोड़ दिया गया था।",
                "layout_type": "fullscreen_broll",
                "broll_query": "dark server rack glowing blue orange cinematic",
                "sfx": "none"
            })

        chapters.append({
            "chapter_id": 3,
            "chapter_title": "अध्याय 3: महाविनाश का मोड़ (The Breaking Point)",
            "subtitle": "पोस्टमार्टम और विफलता की श्रृंखला",
            "scenes": act3_scenes
        })

        # Act 4
        act4_scenes = [
            {
                "dialogue": "यह महाविनाश हमारी आधुनिक दुनिया को चलाने वाले डिजिटल ढांचे के बारे में क्या उजागर करता है?",
                "layout_type": "fullscreen_broll",
                "broll_query": "earth from orbit night glowing city lights digital network",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"इस पूरे विश्लेषण का सबसे बड़ा और क्रांतिकारी निष्कर्ष यह है: {paradigm_shift}",
                "layout_type": "blueprint_schematic",
                "broll_query": "abstract futuristic geometric matrix holographic cube",
                "schematic_title": "THE PARADIGM SHIFT ARCHITECTURE",
                "schematic_tag": "SYNTHESIS // भविष्य का सबक",
                "schematic_specs": [
                    {"label": "CORE TAKEAWAY", "value": "सुरक्षा > गति"},
                    {"label": "SYSTEMIC LATENCY", "value": "शून्य सहनशीलता"},
                    {"label": "HUMAN LIMIT", "value": "जटिलता की सीमा"},
                    {"label": "NEW PARADIGM", "value": "कड़ा सत्यापन"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "जैसे-जैसे हमारी सभ्यता बैंकिंग, विमानन, पावर ग्रिड और एआई को लाखों लाइनों के कोड पर टिका रही है, हमें खुद से एक असहज सवाल पूछना होगा।",
                "layout_type": "fullscreen_broll",
                "broll_query": "modern mega city skyline night traffic time lapse cinematic",
                "sfx": "none"
            },
            {
                "dialogue": "अगर एक अनदेखी मानवीय धारणा अरबों डॉलर के सिस्टम को मिनटों में ध्वस्त कर सकती है, तो हमारी मौजूदा तकनीक में अगला बड़ा झटका कहाँ लगेगा? अपनी राय नीचे कमेंट्स में बताएं और सब्सक्राइब करें @iDastawez को अगली गहरी वैज्ञानिक पड़ताल के लिए।",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic studio end screen abstract particle waves",
                "sfx": "whoosh"
            }
        ]

        chapters.append({
            "chapter_id": 4,
            "chapter_title": "अध्याय 4: तकनीकी क्रांति और सबक (The Paradigm Shift)",
            "subtitle": "एक कड़वा सच",
            "scenes": act4_scenes
        })

        summary_text = f"{title} का एक विस्तृत वैज्ञानिक और तकनीकी विश्लेषण: बुनियादी सिद्धांतों का विश्लेषण, वास्तविक उदाहरण, और इंजीनियरिंग की चरम सीमाएँ।"
        cta_text = "अगर एक छोटी सी धारणा इतने बड़े सिस्टम को क्रैश कर सकती है, तो आज की कौन सी आधुनिक तकनीक सबसे ज्यादा खतरे में है? अपनी राय नीचे कमेंट्स में बताएं! 👇"

    else:
        # =============================================================
        # ENGLISH NARRATIVE (techByAbhi)
        # =============================================================
        act1_scenes = [
            {
                "dialogue": f"To understand {title.lower()}, we must begin with a contradiction that modern science took decades to confront.",
                "layout_type": "fullscreen_broll",
                "broll_query": "deep space dark telemetry glowing grid",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"At its core, the problem seems deceptively simple: {core_paradox}",
                "layout_type": "blueprint_schematic",
                "broll_query": "quantum supercomputer cryogenic gold wiring",
                "schematic_title": "SYSTEM ARCHITECTURE & CONSTRAINTS",
                "schematic_tag": "TELEMETRY // FIRST-PRINCIPLES",
                "schematic_specs": [
                    {"label": "PRIMARY DOMAIN", "value": category.upper()[:20]},
                    {"label": "THEORETICAL LIMIT", "value": "O(N!) HARDNESS"},
                    {"label": "SYSTEMIC TOLERANCE", "value": "±0.0001%"},
                    {"label": "OBSERVED RISK", "value": "CRITICAL THRESHOLD"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "For years, standard textbooks and enterprise architectures took this foundation for granted. Yet when pushed to the mathematical edge, the entire framework begins to fracture.",
                "layout_type": "splitscreen_stat",
                "broll_query": "server rack data center fiber optic glowing",
                "stat_number": "99.999%",
                "stat_label": "THEORETICAL RELIABILITY ASSUMED",
                "stat_context": "Assumptions held until physical edge-case constraints were breached.",
                "stat_change": "CASCADE FAILURE",
                "sfx": "pop"
            },
            {
                "dialogue": f"The inciting event was neither an accident nor malice—it was the inevitable collision between theoretical equations and physical reality: {inciting_incident}",
                "layout_type": "fullscreen_broll",
                "broll_query": "laboratory microscope semiconductor silicon wafer",
                "sfx": "none"
            }
        ]
        if mult > 1:
            act1_scenes.append({
                "dialogue": "To see why everyone was looking in the wrong direction, we have to deconstruct this system down to its atomic components.",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic data telemetry particle wave abstract",
                "sfx": "whoosh"
            })

        chapters.append({
            "chapter_id": 1,
            "chapter_title": "Act 1: The Paradox",
            "subtitle": "The Impossible Premise",
            "scenes": act1_scenes
        })

        act2_scenes = [
            {
                "dialogue": "When complex technology confuses us, the solution is never more jargon—it is finding the right physical analogy.",
                "layout_type": "fullscreen_broll",
                "broll_query": "cinematic physics lab laser beam optics",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"Consider this mental model: {real_world_analogy}",
                "layout_type": "visual_analogy",
                "analogy_title": "THE PHYSICAL ANALOGY",
                "concept_name": "THE ABSTRACT ALGORITHM",
                "concept_desc": "High-dimensional mathematical operations running inside isolated silicon registers.",
                "analogy_name": "THE REAL-WORLD COUNTERPART",
                "analogy_desc": real_world_analogy,
                "takeaway": "When software forgets the physical laws of its container, disaster is mathematically guaranteed.",
                "sfx": "pop"
            },
            {
                "dialogue": "Notice the subtle trap. In abstract mathematics, numbers are infinite and flawless. In real silicon and physical hardware, every byte is an arrangement of trapped electrons subject to thermodynamic entropy.",
                "layout_type": "blueprint_schematic",
                "broll_query": "integrated circuit microchip electron microscope",
                "schematic_title": "THERMODYNAMIC BOUNDARY MAP",
                "schematic_tag": "PHYSICS // HARDWARE-ABSTRACTION",
                "schematic_specs": [
                    {"label": "BIT REGISTER DEPTH", "value": "64-BIT IEEE-754"},
                    {"label": "FLOATING OVERFLOW", "value": "> 32,767 LIMIT"},
                    {"label": "ENERGY DISSIPATION", "value": "10^-21 JOULES/BIT"},
                    {"label": "QUANTUM TUNNELING", "value": "ACTIVE RISK"}
                ],
                "sfx": "none"
            },
            {
                "dialogue": "By abstracting away the hardware, generations of engineers convinced themselves that software exists outside the laws of nature. That illusion lasted until the first catastrophic test.",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic cleanroom engineer wearing hazmat suit silicon fab",
                "sfx": "none"
            }
        ]
        if mult > 1:
            act2_scenes.append({
                "dialogue": "What made this flaw so insidious is that in 99 out of 100 simulations, the system performed flawlessly. The failure mode only triggered when multiple asynchronous variables aligned.",
                "layout_type": "splitscreen_stat",
                "broll_query": "supercomputer server nodes flashing green blue",
                "stat_number": "1 IN 10^9",
                "stat_label": "CRITICAL ANOMALY PROBABILITY",
                "stat_context": "At modern computing scales, a one-in-a-billion bug strikes every 14 seconds.",
                "stat_change": "100% INEVITABLE",
                "sfx": "pop"
            })

        chapters.append({
            "chapter_id": 2,
            "chapter_title": "Act 2: First Principles",
            "subtitle": "Deconstruction & Visual Analogy",
            "scenes": act2_scenes
        })

        act3_scenes = [
            {
                "dialogue": "Theory is mathematically pristine, but when pushed to its operational limit, even the most rigorously tested system meets its breaking point.",
                "layout_type": "fullscreen_broll",
                "broll_query": "dark industrial telemetry warning lights flashing red",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"Here is the exact forensic chain of failure: {catastrophe_case_study}",
                "layout_type": "kinetic_flowchart",
                "flowchart_title": "FORENSIC CAUSAL LOGIC CHAIN",
                "flowchart_steps": [
                    {"step": 1, "label": "Initial Sensor Discrepancy", "detail": "Telemetry exceeds buffer allocation during peak load", "status": "normal"},
                    {"step": 2, "label": "Uncaught Exception", "detail": "Protection routine disabled to save 80 microseconds of CPU time", "status": "active"},
                    {"step": 3, "label": "Diagnostic Data Interpreted as Command", "detail": "Error dump bits routed directly to physical actuators", "status": "critical"},
                    {"step": 4, "label": "Complete Structural Catastrophe", "detail": "Aerodynamic and physical stress exceeds design threshold", "status": "critical"}
                ],
                "sfx": "whoosh"
            },
            {
                "dialogue": "When investigators reconstructed the telemetry millisecond by millisecond, they uncovered a timeline where every safeguard failed in domino succession.",
                "layout_type": "data_timeline_matrix",
                "timeline_title": "CHRONOLOGICAL FORENSIC TIMELINE",
                "timeline_events": [
                    {"time_label": "T - 00:00", "title": "System Nominal Launch", "desc": "All primary and redundant telemetry reporting green.", "severity": "info"},
                    {"time_label": "T + 36.7s", "title": "Primary Unit Hardware Halt", "desc": "Arithmetic overflow in alignment calculation halts CPU.", "severity": "warning"},
                    {"time_label": "T + 37.2s", "title": "Backup Unit Duplicate Crash", "desc": "Identical legacy code causes identical fault in backup.", "severity": "critical"},
                    {"time_label": "T + 39.0s", "title": "Total Structural Disintegration", "desc": "Actuators pivot to maximum angle; mission terminated.", "severity": "critical"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "The financial and technological wreckage was immense. But the most horrifying finding was not that the code was broken—it was that the code did exactly what it was programmed to do.",
                "layout_type": "splitscreen_article",
                "broll_query": "investigation declassified report document paper",
                "article_headline": "OFFICIAL INQUIRY BOARD DISCLOSES STRUCTURAL FINDINGS",
                "article_quote": "The failure was not caused by a random hardware malfunction, but by a systemic flaw in the specification of software requirements.",
                "article_source": "INDEPENDENT INQUIRY BOARD",
                "sfx": "pop"
            }
        ]
        if mult > 1:
            act3_scenes.append({
                "dialogue": "A simple assertion check—a single line of defensive code—would have prevented the entire collapse. But that check was deliberately omitted.",
                "layout_type": "fullscreen_broll",
                "broll_query": "dark server rack glowing blue orange cinematic",
                "sfx": "none"
            })

        chapters.append({
            "chapter_id": 3,
            "chapter_title": "Act 3: The Breaking Point",
            "subtitle": "Forensic Autopsy & Catastrophe",
            "scenes": act3_scenes
        })

        act4_scenes = [
            {
                "dialogue": "What does this catastrophe reveal about the fragile technological web supporting our modern world?",
                "layout_type": "fullscreen_broll",
                "broll_query": "earth from orbit night glowing city lights digital network",
                "sfx": "whoosh"
            },
            {
                "dialogue": f"The fundamental takeaway reshapes our understanding: {paradigm_shift}",
                "layout_type": "blueprint_schematic",
                "broll_query": "abstract futuristic geometric matrix holographic cube",
                "schematic_title": "THE PARADIGM SHIFT ARCHITECTURE",
                "schematic_tag": "SYNTHESIS // FUTURE-HORIZONS",
                "schematic_specs": [
                    {"label": "CORE TAKEAWAY", "value": "VERIFICATION OVER SPEED"},
                    {"label": "SYSTEMIC LATENCY", "value": "ZERO TOLERANCE"},
                    {"label": "HUMAN COGNITIVE LIMIT", "value": "O(COMPLEXITY)"},
                    {"label": "NEW PARADIGM", "value": "FORMAL PROOF DESIGN"}
                ],
                "sfx": "pop"
            },
            {
                "dialogue": "As our civilization connects banking, aviation, energy grids, and autonomous intelligence to millions of lines of recursive code, we must ask ourselves an uncomfortable question.",
                "layout_type": "fullscreen_broll",
                "broll_query": "modern mega city skyline night traffic time lapse cinematic",
                "sfx": "none"
            },
            {
                "dialogue": f"If an invisible assumption can bring down a half-billion-dollar system in seconds, which foundational assumption in our current technology will break next? Share your perspective in the comments below, and subscribe for our next deep dive into the hidden machinery of our world.",
                "layout_type": "fullscreen_broll",
                "broll_query": "futuristic studio end screen abstract particle waves",
                "sfx": "whoosh"
            }
        ]

        chapters.append({
            "chapter_id": 4,
            "chapter_title": "Act 4: The Paradigm Shift",
            "subtitle": "The Uncomfortable Reality",
            "scenes": act4_scenes
        })

        summary_text = f"A forensic, mind-bending investigation into {title}: deconstructing first principles, physical analogies, and the catastrophic limits of human engineering."
        cta_text = f"If a single latent mathematical assumption can collapse this system, what modern tech assumption is most vulnerable today? Debate below! 👇"

    # Compute full narrative text
    all_sentences = []
    for ch in chapters:
        for sc in ch["scenes"]:
            all_sentences.append(sc["dialogue"])
    full_script = " ".join(all_sentences)

    return {
        "title": title,
        "duration_target_minutes": duration_minutes,
        "summary": summary_text,
        "tags": ["Engineering", "Science", "Physics", "ComputerScience", "DeepDive", "TechnologyExplained"],
        "cta_question": cta_text,
        "chapters": chapters,
        "full_script": full_script
    }


def generate_long_form_script(story: Dict[str, Any], duration_minutes: int = 12, language: str = "en") -> Dict[str, Any]:
    """
    Generate 4-Act Mind-Bending Visual Explainer script via Gemini with multi-model cascade,
    Hindi Devanagari support, rate limit backoff retries, and automatic procedural fallback.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    target_words = int(duration_minutes * 145)

    if not api_key:
        logger.info("No GEMINI_API_KEY found. Generating procedural 4-Act deep-dive script...")
        return generate_procedural_long_script(story, duration_minutes, language=language)

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key, transport='rest')

        sys_prompt = build_system_prompt(duration_minutes, target_words, language=language)
        user_prompt = f"""
TOPIC TO ADAPT INTO A MIND-BENDING VISUAL EXPLAINER (VERITASIUM / LEMMINO / THINK SCHOOL STYLE):
Title: {story.get('title')}
Category: {story.get('category', 'Science & Deep Technology')}
Core Paradox: {story.get('core_paradox', story.get('summary', story.get('title')))}
Real-World Analogy: {story.get('real_world_analogy', 'Deconstruct using an everyday physical metaphor')}
Catastrophe / Breaking Point: {story.get('catastrophe_case_study', 'The engineering breakdown and causal chain')}
Paradigm Shift: {story.get('paradigm_shift', 'The broader systemic reality check')}

Target Duration: {duration_minutes} minutes ({target_words} spoken words across 4 investigative acts).
Strictly return valid JSON adhering to the specified schema with all 4 acts and rich multi-layout storyboard scenes.
"""
        for model_name in CANDIDATE_MODELS:
            for attempt in range(2):
                try:
                    logger.info(f"Generating 4-Act Deep Dive script via Gemini model: {model_name} (attempt {attempt+1})...")
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        f"{sys_prompt}\n\n{user_prompt}",
                        generation_config={"response_mime_type": "application/json"}
                    )
                    raw = response.text.strip()
                    data = json.loads(raw)

                    # Validate and normalize chapter/act structure
                    ch_list = data.get("chapters") or data.get("acts")
                    if ch_list and isinstance(ch_list, list) and len(ch_list) >= 2:
                        data["chapters"] = ch_list
                        # Stitch full_script if not present
                        if "full_script" not in data or not data["full_script"]:
                            all_dialogue = []
                            for ch in data["chapters"]:
                                for sc in ch.get("scenes", []):
                                    if "dialogue" in sc:
                                        all_dialogue.append(sc["dialogue"])
                            data["full_script"] = " ".join(all_dialogue)

                        word_count = len(data["full_script"].split())
                        logger.info(f"Successfully generated {len(data['chapters'])}-act script via {model_name} ({word_count} words).")
                        return data
                    else:
                        logger.warning(f"Model {model_name} returned insufficient chapter structure. Trying next...")
                        break
                except Exception as m_err:
                    err_str = str(m_err)
                    if ("429" in err_str or "quota" in err_str.lower()) and attempt == 0:
                        logger.info(f"Model {model_name} hit rate limit (429). Waiting 8.5s for quota window before retry...")
                        time.sleep(8.5)
                        continue
                    logger.warning(f"Model {model_name} error: {m_err}. Trying next model...")
                    break

        logger.warning("All Gemini candidate models failed. Using procedural 4-Act explainer generator.")
        return generate_procedural_long_script(story, duration_minutes, language=language)

    except Exception as e:
        logger.warning(f"Error in Gemini long script generation: {e}. Using procedural script.")
        return generate_procedural_long_script(story, duration_minutes, language=language)


if __name__ == "__main__":
    test_story = {
        "title": "Massive Cloud Kernel Driver Outage Grounds Airline Flights",
        "source": "Hacker News",
        "summary": "An untested Friday patch with null-pointer dereference crashed 8 million corporate machines."
    }
    res = generate_long_form_script(test_story, duration_minutes=3, language="hi")
    print("\n--- GENERATED LONG SCRIPT (HINDI) ---")
    print("Title:", res["title"])
    print("Chapters:", len(res["chapters"]))
    for ch in res["chapters"]:
        print(f" > Chapter {ch.get('chapter_id')}: {ch.get('chapter_title')} ({len(ch.get('scenes', []))} scenes)")
    print("Total Words:", len(res["full_script"].split()))
    print("Sample Dialogue:", res["chapters"][0]["scenes"][0]["dialogue"])
