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
from moviepy import VideoFileClip
from src.giphy_fetcher import search_giphy_meme_clip

# Curated local real-human fallback memes
LOCAL_REAL_MEMES = {
    "JORDAN": ("assets/memes/test_jordan.mp4", True, "STOP IT. GET SOME HELP."),
    "SORRY": ("assets/memes/thinking_about_other_women.jpg", False, "SORRY BABE"),
    "DISASTER": ("assets/memes/disaster_girl.png", False, "TEST IN PROD"),
    "LAUGH": ("assets/memes/laughing_leo.png", False, "tEcH iNnOvAtIoN"),
    "CRY": ("assets/memes/harold_pain.jpg", False, "THIS IS FINE"),
    "PASCAL": ("assets/memes/harold_pain.jpg", False, "THIS IS FINE"),
    "MONEY": ("assets/memes/getting_paid.png", False, "YOU GUYS GETTING PAID?"),
    "STONKS": ("assets/memes/stonks_money.png", False, "STONKS"),
    "FLEX": ("assets/memes/flex_tape_slap.png", False, "I SAID WE PROD TODAY"),
    "SAME": ("assets/memes/same_picture.jpg", False, "THEY'RE THE SAME PICTURE"),
    "DISTRACTED": ("assets/memes/distracted_boyfriend.jpg", False, "NEW JAVASCRIPT FRAMEWORK"),
    "GRAVE": ("assets/memes/grant_gustin_grave.png", False, "REST IN PEACE"),
    "CONSPIRACY": ("assets/memes/charlie_conspiracy.jpg", False, "CONNECTING THE NODES"),
    "CLOWN": ("assets/memes/clown_makeup.jpg", False, "CLOWN MOMENT"),
    "PABLO": ("assets/memes/pablo_escobar.jpg", False, "WAITING FOR CI/CD"),
    "SPIDERMAN": ("assets/memes/spiderman_pointing.jpg", False, "SPIDERMAN POINTING"),
    "DEFAULT": ("assets/memes/this_is_fine.png", False, "THIS IS FINE")
}


def get_story_meme_package(
    story: Dict[str, Any], 
    meme_scene: Optional[Dict[str, Any]] = None, 
    total_duration: float = 40.0
) -> Optional[Dict[str, Any]]:
    """
    Selects moving GIPHY MP4 reaction clip or high-definition real-human meme.
    """
    scene_text = ""
    target_query = ""
    custom_punchline = ""
    sfx_type = "vine_boom"

    if meme_scene:
        target_query = meme_scene.get("visual_query", "")
        custom_punchline = meme_scene.get("meme_punchline", "")
        sfx_type = meme_scene.get("sfx", "vine_boom")
        scene_text = (target_query + " " + meme_scene.get("narration_part", "")).upper()
    
    story_text = (story.get("title", "") + " " + story.get("summary", "")).upper()
    combined_text = (scene_text + " " + story_text).strip()
    
    logo_file = None
    border_col = (0, 230, 255)  # Default electric cyan

    # Detect Company Logo for face/corner stamping
    if "OPENAI" in combined_text or "GPT" in combined_text:
        logo_file = "assets/memes/logo_openai.png"
        border_col = (16, 185, 129)
    elif "GOOGLE" in combined_text or "GEMINI" in combined_text:
        logo_file = "assets/memes/logo_google.png"
        border_col = (66, 133, 244)
    elif "MICROSOFT" in combined_text or "WINDOWS" in combined_text:
        logo_file = "assets/memes/logo_microsoft.png"
        border_col = (0, 164, 239)
    elif "CROWDSTRIKE" in combined_text:
        logo_file = "assets/memes/logo_crowdstrike.png"
        border_col = (255, 50, 50)

    # 1. First priority: Try fetching real moving reaction video clip from GIPHY!
    is_video = False
    clip_path = None
    if target_query:
        giphy_mp4 = search_giphy_meme_clip(target_query)
        if giphy_mp4 and os.path.exists(giphy_mp4):
            is_video = True
            clip_path = giphy_mp4

    # 2. If GIPHY query didn't succeed, fallback to local authentic human memes
    punchline = custom_punchline
    fallback_img = "assets/memes/this_is_fine.png"
    if not clip_path:
        matched = False
        for key, (fpath, vid, default_p) in LOCAL_REAL_MEMES.items():
            if key in combined_text and os.path.exists(fpath):
                clip_path = fpath
                is_video = vid
                if not punchline:
                    punchline = default_p
                matched = True
                break
        if not matched:
            clip_path = fallback_img
            is_video = False
            if not punchline:
                punchline = "THIS IS FINE"

    start_time = meme_scene.get("start", max(total_duration * 0.38, 8.0)) if meme_scene else max(total_duration * 0.38, 8.0)
    end_time = meme_scene.get("end", min(start_time + 2.4, total_duration - 4.0)) if meme_scene else min(start_time + 2.4, total_duration - 4.0)

    return {
        "is_video": is_video,
        "clip_path": clip_path,
        "punchline": punchline.upper() if punchline else "THIS IS FINE",
        "border_col": border_col,
        "logo_path": logo_file if (logo_file and os.path.exists(logo_file)) else None,
        "sfx": sfx_type,
        "start_time": round(start_time, 2),
        "end_time": round(end_time, 2)
    }


def prepare_meme_scene_data(meme_pkg: Dict[str, Any], width: int, height: int) -> Dict[str, Any]:
    """
    Prepares video or image meme assets for 30 FPS rendering.
    """
    is_video = meme_pkg.get("is_video", False)
    clip_path = meme_pkg.get("clip_path", "")
    
    logo_img = None
    if meme_pkg.get("logo_path") and os.path.exists(meme_pkg["logo_path"]):
        try:
            raw_l = Image.open(meme_pkg["logo_path"]).convert("RGBA")
            logo_img = raw_l.resize((120, 120), Image.Resampling.BILINEAR)
        except Exception:
            logo_img = None

    if is_video and os.path.exists(clip_path):
        try:
            video_clip = VideoFileClip(clip_path)
            return {
                "is_video": True,
                "clip": video_clip,
                "punchline": meme_pkg.get("punchline", "THIS IS FINE"),
                "border_col": meme_pkg.get("border_col", (0, 230, 255)),
                "logo_img": logo_img
            }
        except Exception as e:
            logger.warning(f"Failed to load video meme clip {clip_path}: {e}")

    # Fallback to image
    meme_raw = Image.open(clip_path if os.path.exists(clip_path) else "assets/memes/this_is_fine.png").convert("RGBA")
    bg_blur = meme_raw.resize((width, height), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(35))
    dark_scrim = Image.new("RGBA", (width, height), (0, 0, 0, 185))
    bg_blur.alpha_composite(dark_scrim)

    base_w = int(width * 0.90)
    aspect = meme_raw.height / max(meme_raw.width, 1)
    base_h = int(base_w * aspect)

    return {
        "is_video": False,
        "bg_blur": bg_blur,
        "meme_raw": meme_raw,
        "base_w": base_w,
        "base_h": base_h,
        "punchline": meme_pkg.get("punchline", "THIS IS FINE"),
        "border_col": meme_pkg.get("border_col", (0, 230, 255)),
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
    Renders moving GIPHY reaction video or high-res real-human meme with:
    - Ambient blurred backdrop
    - Centered authentic reaction video
    - Fireship bold punchline header
    - Tech company logo badge
    """
    # 1. Moving GIPHY MP4 Video Reaction Clip
    if meme_data.get("is_video") and meme_data.get("clip"):
        clip = meme_data["clip"]
        clip_dur = max(clip.duration, 0.4)
        local_v_time = t_local % clip_dur
        raw_arr = clip.get_frame(local_v_time)
        frame_img = Image.fromarray(raw_arr).convert("RGBA")

        # Ambient backdrop blur from the current video frame
        bg = frame_img.resize((width, height), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(35))
        dark = Image.new("RGBA", (width, height), (0, 0, 0, 185))
        bg.alpha_composite(dark)
        draw = ImageDraw.Draw(bg)

        # Scale moving video to fill width cleanly (1000px wide)
        target_w = int(width * 0.92)
        aspect = frame_img.height / max(frame_img.width, 1)
        target_h = int(target_w * aspect)
        video_scaled = frame_img.resize((target_w, target_h), Image.Resampling.BILINEAR)

        card_x = (width - target_w) // 2
        card_y = int(height * 0.44) - (target_h // 2)

        border_col = meme_data.get("border_col", (0, 230, 255))
        draw.rounded_rectangle(
            [card_x - 4, card_y - 4, card_x + target_w + 4, card_y + target_h + 4],
            radius=16,
            fill=None,
            outline=border_col,
            width=3
        )
        bg.paste(video_scaled, (card_x, card_y), video_scaled)

        # Tech Logo sticker
        if meme_data.get("logo_img"):
            l_img = meme_data["logo_img"]
            lw, lh = l_img.size
            bg.paste(l_img, (card_x + target_w - lw - 10, card_y + 10), l_img)

        # Bold Fireship Punchline Header
        punchline = meme_data.get("punchline", "THIS IS FINE")
        bbox = draw.textbbox((0, 0), punchline, font=font_bold)
        pw = bbox[2] - bbox[0]
        px = (width - pw) // 2
        py = card_y - 90
        if py < 280:
            py = card_y + target_h + 25

        draw.rounded_rectangle(
            [px - 26, py - 10, px + pw + 26, py + 68],
            radius=16,
            fill=(5, 10, 18, 245),
            outline=(255, 255, 255, 210),
            width=3
        )
        draw.text(
            (px, py),
            punchline,
            font=font_bold,
            fill=(255, 255, 255),
            stroke_fill=(0, 0, 0),
            stroke_width=4
        )

        return bg.convert("RGB")

    # 2. Real Human Static Photo Meme with Ken-Burns Punch Zoom
    frame = meme_data["bg_blur"].copy()
    draw = ImageDraw.Draw(frame)

    dur = max(scene_duration, 0.8)
    progress = min(max(t_local / dur, 0.0), 1.0)
    scale = 1.0 + 0.06 * progress

    target_w = int(meme_data["base_w"] * scale)
    target_h = int(meme_data["base_h"] * scale)
    meme_scaled = meme_data["meme_raw"].resize((target_w, target_h), Image.Resampling.BILINEAR)

    card_x = (width - target_w) // 2
    card_y = int(height * 0.44) - (target_h // 2)

    border_col = meme_data.get("border_col", (0, 230, 255))
    draw.rounded_rectangle(
        [card_x - 4, card_y - 4, card_x + target_w + 4, card_y + target_h + 4],
        radius=18,
        fill=(10, 15, 25, 230),
        outline=border_col,
        width=3
    )
    frame.paste(meme_scaled, (card_x, card_y), meme_scaled)

    if meme_data.get("logo_img"):
        l_img = meme_data["logo_img"]
        lw, lh = l_img.size
        frame.paste(l_img, (card_x + target_w - lw - 10, card_y + 10), l_img)

    punchline = meme_data.get("punchline", "THIS IS FINE")
    bbox = draw.textbbox((0, 0), punchline, font=font_bold)
    pw = bbox[2] - bbox[0]
    px = (width - pw) // 2
    py = card_y - 90
    if py < 280:
        py = card_y + target_h + 25

    draw.rounded_rectangle(
        [px - 26, py - 10, px + pw + 26, py + 68],
        radius=16,
        fill=(5, 10, 18, 245),
        outline=(255, 255, 255, 210),
        width=3
    )
    draw.text(
        (px, py),
        punchline,
        font=font_bold,
        fill=(255, 255, 255),
        stroke_fill=(0, 0, 0),
        stroke_width=4
    )

    return frame.convert("RGB")

