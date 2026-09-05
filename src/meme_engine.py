"""
Dynamic Meme & Aesthetic Engine (Fireship Style)
Provides:
- 4 Unique Visual Themes (Cyberpunk Neon, Fireship Dark, Matrix Terminal, Corporate Sarcasm)
- Contextual Meme Selection (Elmo in fire, This Is Fine dog, Stonks, Fry, Disaster Girl)
- Tech Logo Superimposition (OpenAI, Google, Microsoft, CrowdStrike)
- High-Impact Punchline Card Generator
"""

import os
import re
import random
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

# Curated visual themes to make each video look distinctly unique
THEMES = {
    "fireship_dark": {
        "name": "Fireship Dark (Sarcasm / Outages)",
        "accent": (255, 69, 0),             # Fire Orange
        "pill_bg": (18, 12, 10, 225),
        "pill_border": (255, 90, 30, 180),
        "active_text": (255, 120, 40, 255),
        "vignette_alpha": 230,
        "badge_bg": (225, 29, 72, 235),
    },
    "cyberpunk_neon": {
        "name": "Cyberpunk Neon (AI / Breakthroughs)",
        "accent": (0, 240, 255),            # Electric Cyan
        "pill_bg": (8, 14, 25, 220),
        "pill_border": (0, 240, 255, 160),
        "active_text": (255, 230, 0, 255),
        "vignette_alpha": 210,
        "badge_bg": (37, 99, 235, 235),
    },
    "matrix_terminal": {
        "name": "Matrix Terminal (Hacks / Protocols)",
        "accent": (16, 185, 129),           # Emerald Matrix Green
        "pill_bg": (6, 18, 12, 230),
        "pill_border": (52, 211, 153, 180),
        "active_text": (52, 211, 153, 255),
        "vignette_alpha": 240,
        "badge_bg": (16, 185, 129, 235),
    },
    "corporate_sarcasm": {
        "name": "Corporate Sarcasm (Money / Drama / Big Tech)",
        "accent": (244, 63, 94),            # Rose / Crimson
        "pill_bg": (20, 12, 24, 225),
        "pill_border": (251, 113, 133, 180),
        "active_text": (250, 204, 21, 255),
        "vignette_alpha": 220,
        "badge_bg": (234, 88, 12, 235),
    }
}


def pick_story_theme(story: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Determine visual aesthetic theme based on story content."""
    text = (story.get("title", "") + " " + story.get("summary", "")).upper()
    
    if any(k in text for k in ["CRASH", "OUTAGE", "DOWN", "CROWDSTRIKE", "BUG", "FAIL", "WINDOWS"]):
        theme_key = "fireship_dark"
    elif any(k in text for k in ["PROTOCOL", "REVERSE", "HACK", "SECURITY", "LINUX", "EXPLOIT", "LEAK"]):
        theme_key = "matrix_terminal"
    elif any(k in text for k in ["PRICE", "PRICING", "EXPENSIVE", "BILLION", "LAWSUIT", "DOLLARS", "COST"]):
        theme_key = "corporate_sarcasm"
    else:
        # Default to vibrant cyberpunk AI theme or rotate
        theme_key = "cyberpunk_neon"
        
    return theme_key, THEMES[theme_key]


def get_story_meme_package(story: Dict[str, Any], total_duration: float) -> Optional[Dict[str, Any]]:
    """
    Selects the most hilarious contextual meme, punchline text, and exact trigger timestamp.
    """
    text = (story.get("title", "") + " " + story.get("summary", "")).upper()
    
    meme_file = None
    punchline = None
    logo_file = None

    # Detect Company Logo
    if "OPENAI" in text or "GPT" in text:
        logo_file = "assets/memes/logo_openai.png"
    elif "GOOGLE" in text or "GEMINI" in text:
        logo_file = "assets/memes/logo_google.png"
    elif "MICROSOFT" in text or "WINDOWS" in text:
        logo_file = "assets/memes/logo_microsoft.png"
    elif "CROWDSTRIKE" in text:
        logo_file = "assets/memes/logo_crowdstrike.png"

    # Contextual Meme Selection
    if any(k in text for k in ["CRASH", "OUTAGE", "DOWN", "BROKE", "CHAOS", "DESTROY"]):
        meme_file = "assets/memes/elmo_chaos.png"
        punchline = "PRODUCTION DOWN 🔥"
    elif any(k in text for k in ["BUG", "PROBLEM", "ERROR", "FIRE", "ISSUES"]):
        meme_file = "assets/memes/this_is_fine.png"
        punchline = "THIS IS FINE ☕"
    elif any(k in text for k in ["PRICE", "PRICING", "EXPENSIVE", "BILLION", "MILLION", "COST", "DOLLARS"]):
        meme_file = "assets/memes/stonks_money.png"
        punchline = "STONKS 📈💸"
    elif any(k in text for k in ["PRODUCTION", "DEPLOY", "RELEASE", "SHIPPED", "PUSH"]):
        meme_file = "assets/memes/disaster_girl.png"
        punchline = "GIT PUSH --FORCE 😈"
    elif any(k in text for k in ["SECRET", "LEAK", "SUSPICIOUS", "EXPOSED", "ILLEGAL"]):
        meme_file = "assets/memes/suspicious_fry.png"
        punchline = "NOT SURE IF LEGAL 🧐"
    elif any(k in text for k in ["PROMISE", "CLAIM", "FAKE", "EXCUSE", "OVERHYPED"]):
        meme_file = "assets/memes/mocking_sponge.png"
        punchline = "tEcH iNnOvAtIoN 🤡"
    elif any(k in text for k in ["GENIUS", "TRICK", "HACK", "OPTIMIZE", "BRAIN", "BYPASS"]):
        meme_file = "assets/memes/smart_rollsafe.png"
        punchline = "BIG BRAIN DEV 🧠"
    else:
        # Evergreen fallback
        meme_file = "assets/memes/elmo_chaos.png"
        punchline = "REAL MEN TEST IN PROD 🚀"

    if not meme_file or not os.path.exists(meme_file):
        return None

    # Time window: triggers around the climax of the Short (e.g. 11.5s to 14.5s)
    start_time = max(total_duration * 0.38, 8.0)
    end_time = min(start_time + 2.8, total_duration - 4.0)

    return {
        "meme_path": meme_file,
        "punchline": punchline,
        "logo_path": logo_file if (logo_file and os.path.exists(logo_file)) else None,
        "start_time": round(start_time, 2),
        "end_time": round(end_time, 2)
    }


def render_meme_punchline_frame(
    meme_pkg: Dict[str, Any],
    t: float,
    width: int,
    height: int,
    font_bold: ImageFont.ImageFont
) -> Optional[Image.Image]:
    """
    Renders a centered Fireship-style meme punchline card with smooth pop-in animation.
    """
    if not meme_pkg:
        return None

    start = meme_pkg["start_time"]
    end = meme_pkg["end_time"]
    if not (start <= t <= end):
        return None

    # Pop-in scale factor for the first 0.15 seconds
    dt = t - start
    scale = min(1.0, dt / 0.15) if dt < 0.15 else 1.0

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Dark backdrop scrim to make the meme pop out
    scrim = Image.new("RGBA", (width, height), (0, 0, 0, int(150 * scale)))
    overlay.alpha_composite(scrim)

    # 2. Load and scale meme image
    try:
        meme_raw = Image.open(meme_pkg["meme_path"]).convert("RGBA")
        target_meme_w = int(680 * scale)
        aspect = meme_raw.height / max(meme_raw.width, 1)
        target_meme_h = int(target_meme_w * aspect)

        meme_resized = meme_raw.resize((target_meme_w, target_meme_h), Image.Resampling.BILINEAR)

        # Draw card container
        card_x = (width - target_meme_w) // 2
        card_y = int(height * 0.40) - (target_meme_h // 2)

        # Drop shadow / border
        draw.rounded_rectangle(
            [card_x - 12, card_y - 12, card_x + target_meme_w + 12, card_y + target_meme_h + 12],
            radius=24,
            fill=(10, 15, 25, 240),
            outline=(255, 69, 0, 220),
            width=4
        )

        overlay.paste(meme_resized, (card_x, card_y), meme_resized)

        # Optional Company Logo sticker on top-right of the meme card
        if meme_pkg.get("logo_path"):
            try:
                logo_raw = Image.open(meme_pkg["logo_path"]).convert("RGBA")
                logo_size = int(120 * scale)
                logo_resized = logo_raw.resize((logo_size, logo_size), Image.Resampling.BILINEAR)
                logo_x = card_x + target_meme_w - (logo_size // 2) - 20
                logo_y = card_y - (logo_size // 2) + 20
                overlay.paste(logo_resized, (logo_x, logo_y), logo_resized)
            except Exception:
                pass

        # 3. Big Bold Punchline Text (Fireship Style) above the meme
        punchline = meme_pkg["punchline"]
        bbox = draw.textbbox((0, 0), punchline, font=font_bold)
        text_w = bbox[2] - bbox[0]
        text_x = (width - text_w) // 2
        text_y = card_y - 110

        # Draw dark contrast backing for punchline text
        draw.rounded_rectangle(
            [text_x - 24, text_y - 10, text_x + text_w + 24, text_y + 75],
            radius=16,
            fill=(0, 0, 0, 230),
            outline=(255, 255, 255, 180),
            width=3
        )
        draw.text((text_x, text_y), punchline, font=font_bold, fill=(255, 255, 255), stroke_fill=(0, 0, 0), stroke_width=4)

    except Exception as e:
        pass

    return overlay
