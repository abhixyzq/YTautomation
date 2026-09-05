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


from PIL import Image, ImageDraw, ImageFont, ImageFilter


def get_story_meme_package(
    story: Dict[str, Any], 
    meme_scene: Optional[Dict[str, Any]] = None, 
    total_duration: float = 40.0
) -> Optional[Dict[str, Any]]:
    """
    Selects the most hilarious contextual meme, clean ASCII punchline text, and exact trigger metadata.
    """
    scene_text = ""
    if meme_scene:
        scene_text = (meme_scene.get("visual_query", "") + " " + meme_scene.get("narration_part", "")).upper()
    
    story_text = (story.get("title", "") + " " + story.get("summary", "")).upper()
    combined_text = (scene_text + " " + story_text).strip()
    
    meme_file = None
    punchline = None
    logo_file = None
    border_col = (255, 69, 0)  # default fire orange

    # Detect Company Logo
    if "OPENAI" in combined_text or "GPT" in combined_text:
        logo_file = "assets/memes/logo_openai.png"
    elif "GOOGLE" in combined_text or "GEMINI" in combined_text:
        logo_file = "assets/memes/logo_google.png"
    elif "MICROSOFT" in combined_text or "WINDOWS" in combined_text:
        logo_file = "assets/memes/logo_microsoft.png"
    elif "CROWDSTRIKE" in combined_text:
        logo_file = "assets/memes/logo_crowdstrike.png"

    # Contextual Meme Selection (Clean ASCII punchlines with ZERO glyph box issues)
    if any(k in combined_text for k in ["THIS_IS_FINE", "FINE", "BUG", "PROBLEM", "ERROR", "FIRE", "ISSUES"]):
        meme_file = "assets/memes/this_is_fine.png"
        punchline = "THIS IS FINE"
        border_col = (255, 120, 30)
    elif any(k in combined_text for k in ["ELMO", "CRASH", "OUTAGE", "DOWN", "BROKE", "CHAOS", "DESTROY", "UNHINGED"]):
        meme_file = "assets/memes/elmo_chaos.png"
        punchline = "PRODUCTION DOWN"
        border_col = (255, 50, 50)
    elif any(k in combined_text for k in ["STONKS", "PRICE", "PRICING", "EXPENSIVE", "BILLION", "MILLION", "COST", "DOLLARS"]):
        meme_file = "assets/memes/stonks_money.png"
        punchline = "STONKS"
        border_col = (52, 211, 153)
    elif any(k in combined_text for k in ["DISASTER", "PRODUCTION", "DEPLOY", "RELEASE", "SHIPPED", "PUSH"]):
        meme_file = "assets/memes/disaster_girl.png"
        punchline = "GIT PUSH --FORCE"
        border_col = (244, 63, 94)
    elif any(k in combined_text for k in ["FRY", "SUSPICIOUS", "SECRET", "LEAK", "EXPOSED", "ILLEGAL"]):
        meme_file = "assets/memes/suspicious_fry.png"
        punchline = "NOT SURE IF LEGAL"
        border_col = (250, 204, 21)
    elif any(k in combined_text for k in ["SPONGE", "MOCK", "PROMISE", "CLAIM", "FAKE", "EXCUSE", "OVERHYPED"]):
        meme_file = "assets/memes/mocking_sponge.png"
        punchline = "tEcH iNnOvAtIoN"
        border_col = (0, 230, 255)
    elif any(k in combined_text for k in ["ROLLSAFE", "GENIUS", "TRICK", "HACK", "OPTIMIZE", "BRAIN", "BYPASS"]):
        meme_file = "assets/memes/smart_rollsafe.png"
        punchline = "BIG BRAIN DEV"
        border_col = (168, 85, 247)
    else:
        # Evergreen fallback
        meme_file = "assets/memes/this_is_fine.png"
        punchline = "REAL MEN TEST IN PROD"
        border_col = (255, 90, 30)

    if not meme_file or not os.path.exists(meme_file):
        return None

    # Determine default timing if not passed in scene
    start_time = meme_scene.get("start", max(total_duration * 0.38, 8.0)) if meme_scene else max(total_duration * 0.38, 8.0)
    end_time = meme_scene.get("end", min(start_time + 2.4, total_duration - 4.0)) if meme_scene else min(start_time + 2.4, total_duration - 4.0)

    return {
        "meme_path": meme_file,
        "punchline": punchline,
        "border_col": border_col,
        "logo_path": logo_file if (logo_file and os.path.exists(logo_file)) else None,
        "start_time": round(start_time, 2),
        "end_time": round(end_time, 2)
    }


def prepare_meme_scene_data(meme_pkg: Dict[str, Any], width: int, height: int) -> Dict[str, Any]:
    """
    Precomputes and caches blurred background and image scaling for 30 FPS rendering speed.
    """
    meme_path = meme_pkg["meme_path"]
    meme_raw = Image.open(meme_path).convert("RGBA")
    
    # Pre-generate Gaussian blurred ambient backdrop
    bg_blur = meme_raw.resize((width, height), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(32))
    dark_scrim = Image.new("RGBA", (width, height), (0, 0, 0, 180))
    bg_blur.alpha_composite(dark_scrim)
    
    base_w = int(width * 0.82)
    aspect = meme_raw.height / max(meme_raw.width, 1)
    base_h = int(base_w * aspect)

    logo_img = None
    if meme_pkg.get("logo_path") and os.path.exists(meme_pkg["logo_path"]):
        try:
            raw_l = Image.open(meme_pkg["logo_path"]).convert("RGBA")
            logo_img = raw_l.resize((120, 120), Image.Resampling.BILINEAR)
        except Exception:
            logo_img = None

    return {
        "bg_blur": bg_blur,
        "meme_raw": meme_raw,
        "base_w": base_w,
        "base_h": base_h,
        "border_col": meme_pkg.get("border_col", (255, 90, 30)),
        "punchline": meme_pkg.get("punchline", "THIS IS FINE"),
        "logo_img": logo_img
    }


def render_cinematic_meme_scene(
    meme_data: Dict[str, Any],
    t_local: float,
    scene_duration: float,
    width: int,
    height: int,
    font_bold: ImageFont.ImageFont
) -> Image.Image:
    """
    Renders a full-frame vertical Fireship meme scene with:
    - Ambient blurred background
    - Smooth Ken-Burns punch zoom (1.0 to 1.07 scale)
    - High-contrast punchline banner card
    - Glowing theme border and optional company badge
    """
    frame = meme_data["bg_blur"].copy()
    draw = ImageDraw.Draw(frame)

    dur = max(scene_duration, 0.8)
    progress = min(max(t_local / dur, 0.0), 1.0)
    
    # Ken-Burns slow dramatic punch zoom
    scale = 1.0 + 0.07 * progress
    target_w = int(meme_data["base_w"] * scale)
    target_h = int(meme_data["base_h"] * scale)

    meme_scaled = meme_data["meme_raw"].resize((target_w, target_h), Image.Resampling.BILINEAR)
    card_x = (width - target_w) // 2
    card_y = int(height * 0.44) - (target_h // 2)

    # Neon accent border & dark card backing
    border_col = meme_data.get("border_col", (255, 90, 30))
    draw.rounded_rectangle(
        [card_x - 8, card_y - 8, card_x + target_w + 8, card_y + target_h + 8],
        radius=22,
        fill=(10, 15, 25, 230),
        outline=border_col,
        width=4
    )
    frame.paste(meme_scaled, (card_x, card_y), meme_scaled)

    # Company sticker badge on top-right
    if meme_data.get("logo_img"):
        l_img = meme_data["logo_img"]
        lw, lh = l_img.size
        lx = card_x + target_w - (lw // 2) - 15
        ly = card_y - (lh // 2) + 15
        frame.paste(l_img, (lx, ly), l_img)

    # High-impact uppercase Punchline Banner Card (Fireship Style)
    punchline = meme_data.get("punchline", "THIS IS FINE")
    bbox = draw.textbbox((0, 0), punchline, font=font_bold)
    text_w = bbox[2] - bbox[0]
    text_x = (width - text_w) // 2
    text_y = card_y - 95
    if text_y < 280:
        text_y = card_y + target_h + 30

    draw.rounded_rectangle(
        [text_x - 24, text_y - 10, text_x + text_w + 24, text_y + 68],
        radius=16,
        fill=(5, 8, 15, 245),
        outline=(255, 255, 255, 200),
        width=3
    )
    draw.text(
        (text_x, text_y), 
        punchline, 
        font=font_bold, 
        fill=(255, 255, 255), 
        stroke_fill=(0, 0, 0), 
        stroke_width=4
    )

    return frame.convert("RGB")

