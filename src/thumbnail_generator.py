"""
High-CTR Automated Thumbnail Generator for Deep-Dive Tech Investigations (1280x720)
Style: Veritasium, Lemmino, and Think School.
Renders clickbait-free, high-contrast, curiosity-driven thumbnails with CAD wireframes
and bold typography using Remotion Still.
"""

import os
import json
import shutil
import logging
import subprocess
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

CURATED_THUMBNAIL_PRESETS: Dict[str, Dict[str, str]] = {
    "ariane5_integer_overflow_catastrophe": {
        "category": "AEROSPACE FORENSICS",
        "hookTitle": "THE 64-BIT",
        "hookHighlight": "GLITCH",
        "subtitle": "How 10 lines of code destroyed a $500,000,000 rocket in 37 seconds.",
        "badge": "⚠️ MISSION STATUS: CRITICAL DETONATION",
        "accentColor": "#00f0ff"
    },
    "quantum_encryption_apocalypse": {
        "category": "QUANTUM & CRYPTOGRAPHY",
        "hookTitle": "RSA IS",
        "hookHighlight": "BROKEN",
        "subtitle": "What happens when Shor's algorithm cracks global bank encryption?",
        "badge": "⚡ 10^30 YEARS -> 8 HOURS",
        "accentColor": "#c084fc"
    },
    "asml_extreme_ultraviolet_miracle": {
        "category": "NANOSCALE PHYSICS",
        "hookTitle": "MOLTEN TIN AT",
        "hookHighlight": "200,000 MPH",
        "subtitle": "The $200M Dutch machine that humanity needs to print 2nm microchips.",
        "badge": "🔬 13.5 NM WAVELENGTH // VACUUM",
        "accentColor": "#00f0ff"
    },
    "agi_mathematical_impossibility": {
        "category": "MATHEMATICS & COMPUTATION",
        "hookTitle": "AGI IS",
        "hookHighlight": "IMPOSSIBLE",
        "subtitle": "The mathematical limits of computation: why Turing and Gödel were right.",
        "badge": "🧠 RECURSIVE MODEL COLLAPSE",
        "accentColor": "#fbbf24"
    },
    "undersea_internet_chokepoint": {
        "category": "INVISIBLE INFRASTRUCTURE",
        "hookTitle": "THE 500",
        "hookHighlight": "THREADS",
        "subtitle": "Why 99% of global internet traffic travels through glass on the ocean floor.",
        "badge": "🌐 4 CABLES CUT // 25% TRAFFIC LOST",
        "accentColor": "#00f0ff"
    },
    "crowdstrike_kernel_crash_autopsy": {
        "category": "OPERATING SYSTEMS",
        "hookTitle": "THE NULL",
        "hookHighlight": "POINTER",
        "subtitle": "How a single ring-zero channel file froze 8.5 million machines worldwide.",
        "badge": "🛑 8,500,000 BLUE SCREENS",
        "accentColor": "#ef4444"
    },
    "stuxnet_physics_of_cyberwar": {
        "category": "CYBER WARFARE",
        "hookTitle": "CODE THAT DESTROYS",
        "hookHighlight": "STEEL",
        "subtitle": "The world's first digital weapon that crossed from bits into physical atoms.",
        "badge": "💣 1,000 CENTRIFUGES SHATTERED",
        "accentColor": "#ef4444"
    }
}


def build_thumbnail_props(story: Dict[str, Any]) -> Dict[str, str]:
    """Generates high-contrast thumbnail props for a given story."""
    story_id = story.get("id", "")
    if story_id in CURATED_THUMBNAIL_PRESETS:
        return CURATED_THUMBNAIL_PRESETS[story_id]

    title = story.get("title", "The Engineering Paradox").strip()
    words = title.split()

    # Create punchy 3-4 word title hook
    if len(words) >= 3:
        hook_title = " ".join(words[:2]).upper()
        hook_highlight = words[2].upper()
    else:
        hook_title = "THE HIDDEN"
        hook_highlight = words[0].upper() if words else "GLITCH"

    category = story.get("category", "DEEP TECHNOLOGY").upper()
    subtitle = story.get("core_paradox", story.get("summary", title))
    if len(subtitle) > 85:
        subtitle = subtitle[:82] + "..."

    return {
        "category": category,
        "hookTitle": hook_title,
        "hookHighlight": hook_highlight,
        "subtitle": subtitle,
        "badge": "⚡ VERIFIED INVESTIGATION",
        "accentColor": "#00f0ff"
    }


def generate_episode_thumbnail(
    story: Dict[str, Any],
    output_path: str = "output/thumbnail.jpg"
) -> Optional[str]:
    """
    Renders 1280x720 YouTube thumbnail via Remotion Still.
    Returns the absolute path of the generated JPEG.
    """
    npx_cmd = shutil.which("npx")
    if not npx_cmd:
        logger.warning("npx not found on system PATH. Cannot render Remotion thumbnail.")
        return None

    props = build_thumbnail_props(story)

    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    props_path = os.path.join(temp_dir, "thumb_props.json")

    with open(props_path, "w", encoding="utf-8") as f:
        json.dump(props, f, indent=2)

    out_abs = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)

    cmd = [
        "npx", "remotion", "still",
        "remotion/index.ts",
        "ThumbnailLandscape",
        out_abs,
        f"--props={props_path}",
        "--public-dir=public"
    ]

    logger.info(f"Rendering 1280x720 Thumbnail via Remotion: {' '.join(cmd)}")
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if res.returncode == 0 and os.path.exists(out_abs) and os.path.getsize(out_abs) > 500:
            size_kb = os.path.getsize(out_abs) / 1024
            logger.info(f"Thumbnail rendered successfully: {out_abs} ({size_kb:.1f} KB)")
            return out_abs
        else:
            logger.warning(
                f"Remotion thumbnail render failed (code {res.returncode}):\n{res.stderr[:600]}"
            )
            return None
    except Exception as e:
        logger.warning(f"Error rendering thumbnail: {e}")
        return None


if __name__ == "__main__":
    test_story = {
        "id": "ariane5_integer_overflow_catastrophe",
        "title": "How a 64-bit Number Destroyed a $500 Million Rocket in 37 Seconds",
        "category": "Engineering Catastrophes & Glitches"
    }
    thumb = generate_episode_thumbnail(test_story, "output/test_thumbnail_ariane5.jpg")
    print(f"Test thumbnail: {thumb}")
