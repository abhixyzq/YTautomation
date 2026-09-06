"""
Long-Form Tech Documentary & Satire Compositor (16:9 Landscape 1920x1080)
Style: John Oliver / Jon Stewart meets Fireship & Vox.
Master-tier, broadcast-grade landscape compositor featuring 5 distinct dynamic layouts:
1. chapter_bumper: Cinematic chapter title cards with sub-bass impact
2. fullscreen_broll: 4K landscape footage with Ken-Burns slow pan & broadcast chyrons
3. splitscreen_article: Left 45% video + Right 55% floating 3D newspaper/tweet quote card
4. splitscreen_code: Left 45% video + Right 55% Dark VS Code IDE window with syntax highlighting
5. meme_reaction: Centered GIPHY moving video clip with Gaussian blur & punchline banner

Includes multi-track audio scoring, landscape word-by-word captions, and YouTube chapter markers.
"""

import os
import sys
import re
import math
import json
import shutil
import subprocess
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import imageio_ffmpeg
from moviepy import (
    AudioFileClip,
    VideoFileClip,
    CompositeAudioClip,
    VideoClip
)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.broll_downloader import fetch_broll_clip, get_curated_broll_clips
from src.giphy_fetcher import search_giphy_meme_clip
from src.meme_engine import render_cinematic_meme_scene, prepare_meme_scene_data, LOCAL_REAL_MEMES

logger = logging.getLogger(__name__)

WIDTH = 1920
HEIGHT = 1080
FPS = 30

def _normalize_rel_path(p: Optional[str]) -> str:
    if not p:
        return ""
    abs_p = os.path.abspath(p)
    ws_root = os.path.abspath(os.getcwd())
    if abs_p.startswith(ws_root):
        return os.path.relpath(abs_p, ws_root).replace("\\", "/")
    return p.replace("\\", "/")


def render_remotion_video(props_dict: Dict[str, Any], output_path: str) -> bool:
    """Renders broadcast video using Remotion (React + CSS Motion Graphics)."""
    npx_cmd = shutil.which("npx")
    if not npx_cmd:
        logger.warning("npx not found on system PATH. Skipping Remotion render.")
        return False

    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    public_dir = os.path.join(os.getcwd(), "public")
    os.makedirs(public_dir, exist_ok=True)

    # 1. Sync narration audio into public/ directory for Remotion static server
    audio_path = props_dict.get("audio_path")
    if audio_path and os.path.exists(audio_path):
        target_audio = os.path.join(public_dir, audio_path)
        os.makedirs(os.path.dirname(target_audio), exist_ok=True)
        try:
            shutil.copy2(audio_path, target_audio)
        except Exception as e:
            logger.warning(f"Could not copy audio to public dir: {e}")

    # 2. Sync only active B-roll / media clips for this episode into public/
    for sc in props_dict.get("scenes", []):
        bp = sc.get("broll_path")
        if bp and os.path.exists(bp):
            target_bp = os.path.join(public_dir, bp)
            if not os.path.exists(target_bp):
                os.makedirs(os.path.dirname(target_bp), exist_ok=True)
                try:
                    shutil.copy2(bp, target_bp)
                except Exception:
                    pass

    props_path = os.path.join(temp_dir, "remotion_props.json")

    with open(props_path, "w", encoding="utf-8") as f:
        json.dump(props_dict, f, indent=2)

    out_abs = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(out_abs), exist_ok=True)

    cmd = [
        "npx", "remotion", "render",
        "remotion/index.ts",
        "TechShowLandscape",
        out_abs,
        f"--props={props_path}",
        "--public-dir=public",
        "--concurrency=4"
    ]

    logger.info(f"Invoking Remotion render: {' '.join(cmd)}")
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if res.returncode == 0 and os.path.exists(out_abs) and os.path.getsize(out_abs) > 1000:
            logger.info(f"Remotion render completed successfully: {out_abs} ({os.path.getsize(out_abs) / (1024*1024):.2f} MB)")
            return True
        else:
            logger.warning(f"Remotion render failed with code {res.returncode}.\nStderr: {res.stderr[:800]}\nStdout: {res.stdout[:800]}")
            return False
    except Exception as e:
        logger.warning(f"Remotion render exception: {e}")
        return False

def _find_font(candidates: List[str]) -> Optional[str]:
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

FONT_PATH_BOLD = _find_font([
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
])
FONT_PATH_REG = _find_font([
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
])
FONT_PATH_CODE = _find_font([
    "C:/Windows/Fonts/consola.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
])


class VSCodeRenderer:
    """Renders an ultra-realistic, syntax-highlighted Dark VS Code IDE Window."""
    def __init__(self, font_code_path: Optional[str] = FONT_PATH_CODE):
        self.font_code = ImageFont.truetype(font_code_path, 26) if font_code_path else ImageFont.load_default()
        self.font_small = ImageFont.truetype(font_code_path, 20) if font_code_path else ImageFont.load_default()
        self.font_tab = ImageFont.truetype(FONT_PATH_BOLD, 20) if FONT_PATH_BOLD else ImageFont.load_default()

        # Syntax Token Colors
        self.COLOR_KEYWORD = (197, 134, 192)   # Purple #c586c0
        self.COLOR_FUNC = (220, 220, 170)      # Yellow #dcdcaa
        self.COLOR_STRING = (206, 145, 120)    # Orange #ce9178
        self.COLOR_COMMENT = (106, 153, 85)    # Green #6a9955
        self.COLOR_NUMBER = (181, 206, 168)    # Light Green #b5cea8
        self.COLOR_DEFAULT = (220, 220, 220)   # Light Gray
        self.COLOR_LINENUM = (110, 118, 129)   # Gutter Gray

    def tokenize_line(self, line: str) -> List[Tuple[str, Tuple[int, int, int]]]:
        """Simple tokenizer for syntax coloring Python/JS/C code."""
        tokens = []
        # Check comment
        comment_idx = line.find("#") if "#" in line else line.find("//")
        if comment_idx != -1:
            code_part = line[:comment_idx]
            comment_part = line[comment_idx:]
        else:
            code_part = line
            comment_part = ""

        # Tokenize code part with regex
        pattern = re.compile(
            r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'  # Strings
            r'\b(def|async|await|while|for|return|if|else|elif|import|from|class|try|except|raise|with|as)\b|'  # Keywords
            r'\b(\d+)\b|'  # Numbers
            r'\b([a-zA-Z_]\w*)(?=\s*\()|'  # Function calls
            r'([a-zA-Z_]\w*|[^\s\w]+|\s+)'  # Identifiers / symbols / whitespace
        )
        for match in pattern.finditer(code_part):
            s_str, kw, num, fn, other = match.groups()
            if s_str:
                tokens.append((s_str, self.COLOR_STRING))
            elif kw:
                tokens.append((kw, self.COLOR_KEYWORD))
            elif num:
                tokens.append((num, self.COLOR_NUMBER))
            elif fn:
                tokens.append((fn, self.COLOR_FUNC))
            elif other:
                tokens.append((other, self.COLOR_DEFAULT))

        if comment_part:
            tokens.append((comment_part, self.COLOR_COMMENT))

        return tokens

    def render_ide_card(
        self,
        width: int,
        height: int,
        filename: str = "cluster_fault.py",
        code_text: str = "",
        error_line: int = 4
    ) -> Image.Image:
        """Render a standalone 3D dark VS Code window."""
        card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)

        # Outer IDE Container (Dark Charcoal with sleek border)
        draw.rounded_rectangle(
            [0, 0, width, height],
            radius=18,
            fill=(30, 30, 30, 248),
            outline=(0, 220, 255, 140),
            width=2
        )

        # macOS Traffic Lights Bar (Top)
        bar_h = 56
        draw.rounded_rectangle([0, 0, width, bar_h], radius=18, fill=(37, 37, 38, 255))
        draw.rectangle([0, bar_h - 18, width, bar_h], fill=(37, 37, 38, 255)) # Square bottom edge
        draw.line([(0, bar_h), (width, bar_h)], fill=(50, 50, 52), width=1)

        # Traffic Lights
        draw.ellipse([24, 20, 40, 36], fill=(255, 95, 87))    # Red
        draw.ellipse([48, 20, 64, 36], fill=(254, 188, 46))   # Yellow
        draw.ellipse([72, 20, 88, 36], fill=(40, 201, 64))    # Green

        # Active File Tab
        tab_w = 260
        tab_x = 110
        draw.rectangle([tab_x, 10, tab_x + tab_w, bar_h], fill=(30, 30, 30))
        draw.line([(tab_x, 10), (tab_x + tab_w, 10)], fill=(0, 122, 204), width=3) # Blue active line
        draw.text((tab_x + 36, 18), f"📄 {filename}", font=self.font_tab, fill=(240, 240, 240))

        # Status indicator right
        draw.text((width - 180, 20), "UTF-8  •  Python", font=self.font_small, fill=(150, 150, 150))

        # Code Editor Canvas
        gutter_w = 70
        draw.rectangle([0, bar_h, gutter_w, height], fill=(33, 33, 33, 255))
        draw.line([(gutter_w, bar_h), (gutter_w, height)], fill=(45, 45, 48), width=1)

        lines = code_text.strip().split("\n")
        start_y = bar_h + 24
        line_height = 38

        for idx, line in enumerate(lines[:18]):
            curr_y = start_y + (idx * line_height)
            line_no = idx + 1

            # Gutter Line Number
            draw.text((22, curr_y), f"{line_no:2d}", font=self.font_code, fill=self.COLOR_LINENUM)

            # Highlight buggy line background
            if line_no == error_line or "FIXME" in line or "TODO" in line or "drop_all" in line:
                draw.rectangle([gutter_w + 4, curr_y - 4, width - 20, curr_y + line_height - 6], fill=(255, 60, 60, 45))

            # Syntax Tokens
            tokens = self.tokenize_line(line)
            cursor_x = gutter_w + 24
            for text, color in tokens:
                draw.text((cursor_x, curr_y), text, font=self.font_code, fill=color)
                bbox = draw.textbbox((0, 0), text, font=self.font_code)
                cursor_x += (bbox[2] - bbox[0])

            # Red squiggly line under error line
            if line_no == error_line or "FIXME" in line or "TODO" in line:
                squiggle_y = curr_y + 30
                for sx in range(gutter_w + 24, min(cursor_x, width - 30), 6):
                    draw.line([(sx, squiggle_y), (sx + 3, squiggle_y + 3), (sx + 6, squiggle_y)], fill=(255, 75, 75), width=2)

        # Bottom IDE Status Bar
        status_h = 32
        draw.rounded_rectangle([0, height - status_h, width, height], radius=18, fill=(0, 122, 204, 255))
        draw.rectangle([0, height - status_h, width, height - status_h + 10], fill=(0, 122, 204, 255))
        draw.text((24, height - status_h + 6), "⚡ main*  •  0 errors, 1 catastrophic warning", font=self.font_small, fill=(255, 255, 255))

        return card


class ArticleCardRenderer:
    """Renders a floating 3D Newspaper / Investigative Media Card."""
    def __init__(self):
        self.font_source = ImageFont.truetype(FONT_PATH_BOLD, 22) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_headline = ImageFont.truetype(FONT_PATH_BOLD, 36) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_quote = ImageFont.truetype(FONT_PATH_REG, 28) if FONT_PATH_REG else ImageFont.load_default()
        self.font_footer = ImageFont.truetype(FONT_PATH_REG, 20) if FONT_PATH_REG else ImageFont.load_default()

    def render_article_card(
        self,
        width: int,
        height: int,
        headline: str,
        quote: str,
        source: str = "FINANCIAL TIMES"
    ) -> Image.Image:
        card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)

        # Card Container (Modern high-contrast dark card with glowing border)
        draw.rounded_rectangle(
            [0, 0, width, height],
            radius=20,
            fill=(14, 20, 36, 245),
            outline=(255, 180, 0, 180),
            width=2
        )

        # Header Pill Badge (Source)
        source_badge = f"● {source.upper()}"
        bbox = draw.textbbox((0, 0), source_badge, font=self.font_source)
        badge_w = (bbox[2] - bbox[0]) + 40
        draw.rounded_rectangle([40, 36, 40 + badge_w, 82], radius=12, fill=(225, 29, 72, 235), outline=(255, 120, 150), width=2)
        draw.text((60, 48), source_badge, font=self.font_source, fill=(255, 255, 255))

        # Date / Classification Tag (Dynamically right-aligned with safe 45px margin)
        tag_text = "INVESTIGATIVE INTEL"
        tag_bb = draw.textbbox((0, 0), tag_text, font=self.font_source)
        tag_w = tag_bb[2] - tag_bb[0]
        draw.text((width - tag_w - 45, 50), tag_text, font=self.font_source, fill=(160, 175, 200))

        # Headline
        words = headline.split()
        lines = []
        curr = []
        for w in words:
            curr.append(w)
            bb = draw.textbbox((0, 0), " ".join(curr), font=self.font_headline)
            if (bb[2] - bb[0]) > (width - 100):
                curr.pop()
                lines.append(" ".join(curr))
                curr = [w]
        if curr:
            lines.append(" ".join(curr))
        lines = lines[:3]

        curr_y = 115
        for line in lines:
            draw.text((42, curr_y), line, font=self.font_headline, fill=(255, 255, 255))
            curr_y += 48

        # Divider line
        curr_y += 15
        draw.line([(40, curr_y), (width - 40, curr_y)], fill=(50, 65, 95), width=2)
        curr_y += 30

        # Quote Box (Highlight callout with glowing left accent bar)
        quote_h = min(height - curr_y - 90, 320)
        draw.rounded_rectangle(
            [40, curr_y, width - 40, curr_y + quote_h],
            radius=14,
            fill=(22, 30, 54, 255),
            outline=(80, 100, 145),
            width=1
        )
        # Left Amber Accent Bar
        draw.rounded_rectangle([40, curr_y, 52, curr_y + quote_h], radius=6, fill=(255, 215, 0))

        # Quotation Mark Icon
        draw.text((68, curr_y + 16), "“", font=self.font_headline, fill=(255, 215, 0))

        # Quote Text
        q_words = quote.split()
        q_lines = []
        curr = []
        for w in q_words:
            curr.append(w)
            bb = draw.textbbox((0, 0), " ".join(curr), font=self.font_quote)
            if (bb[2] - bb[0]) > (width - 160):
                curr.pop()
                q_lines.append(" ".join(curr))
                curr = [w]
        if curr:
            q_lines.append(" ".join(curr))

        qy = curr_y + 55
        for qline in q_lines[:5]:
            # Highlight background for keywords
            draw.text((70, qy), qline, font=self.font_quote, fill=(255, 240, 180))
            qy += 40

        # Card Footer
        draw.text((45, height - 52), "VERIFIED SOURCE  •  CONFIDENTIAL LEAK ARCHIVE", font=self.font_footer, fill=(120, 140, 175))

        return card


class ChapterBumperRenderer:
    """Renders high-impact episodic chapter intro title cards."""
    def __init__(self):
        self.font_huge = ImageFont.truetype(FONT_PATH_BOLD, 74) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_sub = ImageFont.truetype(FONT_PATH_BOLD, 36) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_pill = ImageFont.truetype(FONT_PATH_BOLD, 26) if FONT_PATH_BOLD else ImageFont.load_default()

    def render_bumper(
        self,
        width: int,
        height: int,
        chapter_no: int,
        chapter_title: str,
        subtitle: str,
        progress: float = 0.0
    ) -> Image.Image:
        img = Image.new("RGB", (width, height), (8, 12, 22))
        draw = ImageDraw.Draw(img)

        # Subtle dark cyber grid
        for x in range(0, width, 80):
            draw.line([(x, 0), (x, height)], fill=(16, 24, 40), width=1)
        for y in range(0, height, 80):
            draw.line([(0, y), (width, y)], fill=(16, 24, 40), width=1)

        # Center Radial Glow
        center_x, center_y = width // 2, height // 2

        # Chapter Pill Badge
        badge_text = f"● CHAPTER {chapter_no:02d} OF 05"
        bb = draw.textbbox((0, 0), badge_text, font=self.font_pill)
        bw = (bb[2] - bb[0]) + 56
        bx = (width - bw) // 2
        draw.rounded_rectangle([bx, center_y - 170, bx + bw, center_y - 116], radius=16, fill=(225, 29, 72, 235), outline=(255, 120, 150), width=2)
        draw.text((bx + 28, center_y - 156), badge_text, font=self.font_pill, fill=(255, 255, 255))

        # Title (Upper case, bold, centered with word-wrapping to prevent screen edge cutoff)
        t_clean = chapter_title.upper()
        t_words = t_clean.split()
        t_lines = []
        curr_t = []
        for w in t_words:
            curr_t.append(w)
            bb = draw.textbbox((0, 0), " ".join(curr_t), font=self.font_huge)
            if (bb[2] - bb[0]) > (width - 160):
                curr_t.pop()
                if curr_t:
                    t_lines.append(" ".join(curr_t))
                curr_t = [w]
        if curr_t:
            t_lines.append(" ".join(curr_t))
        if not t_lines:
            t_lines = [t_clean]

        line_h = 80
        total_th = len(t_lines) * line_h
        start_ty = center_y - (total_th // 2) - 25

        max_line_w = 0
        for idx, tline in enumerate(t_lines):
            t_bb = draw.textbbox((0, 0), tline, font=self.font_huge)
            t_w = t_bb[2] - t_bb[0]
            max_line_w = max(max_line_w, t_w)
            tx = max(40, (width - t_w) // 2)
            draw.text((tx, start_ty + (idx * line_h)), tline, font=self.font_huge, fill=(255, 255, 255))

        # Cyan / Gold Accent Line
        lw = min(max_line_w + 80, width - 400)
        lx = (width - lw) // 2
        line_y = start_ty + total_th + 15
        draw.line([(lx, line_y), (lx + lw, line_y)], fill=(0, 229, 255), width=4)

        # Subtitle
        s_clean = subtitle.upper()
        s_bb = draw.textbbox((0, 0), s_clean, font=self.font_sub)
        s_w = s_bb[2] - s_bb[0]
        sx = max(40, (width - s_w) // 2)
        draw.text((sx, line_y + 25), s_clean, font=self.font_sub, fill=(255, 215, 0))

        return img


class LongCaptionRenderer:
    """16:9 Landscape Captions in the lower third with active word highlighting."""
    def __init__(self):
        self.font = ImageFont.truetype(FONT_PATH_BOLD, 36) if FONT_PATH_BOLD else ImageFont.load_default()

    def render_caption_frame(self, phrase: Dict[str, Any], current_time: float, width: int = WIDTH, height: int = HEIGHT) -> Image.Image:
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        words = phrase.get("words", [])
        if not words:
            return overlay

        # Calculate word bounding boxes
        word_data = []
        space_w = draw.textbbox((0, 0), " ", font=self.font)[2]
        total_w = 0

        for w_item in words:
            w_text = w_item["word"].strip()
            if not w_text:
                continue
            bb = draw.textbbox((0, 0), w_text, font=self.font)
            ww = bb[2] - bb[0]
            word_data.append((w_item, w_text, ww))
            total_w += ww + space_w

        if not word_data:
            return overlay

        total_w -= space_w
        start_x = (width - total_w) // 2
        y_pos = height - 130

        # Background Pill Backing
        draw.rounded_rectangle(
            [start_x - 30, y_pos - 14, start_x + total_w + 30, y_pos + 52],
            radius=16,
            fill=(10, 15, 26, 215),
            outline=(0, 235, 255, 120),
            width=2
        )

        curr_x = start_x
        for w_item, w_text, ww in word_data:
            is_active = w_item["start"] <= current_time <= w_item["end"]
            text_color = (255, 235, 0) if is_active else (255, 255, 255)

            # Drop shadow
            draw.text((curr_x + 2, y_pos + 2), w_text, font=self.font, fill=(0, 0, 0, 220))
            draw.text((curr_x, y_pos), w_text, font=self.font, fill=text_color)
            curr_x += ww + space_w

        return overlay


def build_long_video(
    script_data: Dict[str, Any],
    voice_data: Dict[str, Any],
    output_path: str,
    width: int = WIDTH,
    height: int = HEIGHT
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Master Compositor for 16:9 Landscape Episodic Tech Shows.
    Returns (final_video_path, youtube_chapters_metadata).
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    total_duration = voice_data["duration"]
    audio_path = voice_data["audio_path"]
    word_timings = voice_data["word_timings"]

    logger.info(f"Compositing 16:9 Landscape Long Video ({width}x{height}) at {FPS} FPS | Duration: {total_duration:.1f}s")

    # Group words into phrases for captions (approx 4-6 words per phrase)
    phrases = []
    curr_phrase_words = []
    for w in word_timings:
        curr_phrase_words.append(w)
        if len(curr_phrase_words) >= 5 or w["word"].endswith((".", "!", "?", ",")):
            phrases.append({
                "words": curr_phrase_words,
                "start": curr_phrase_words[0]["start"],
                "end": curr_phrase_words[-1]["end"]
            })
            curr_phrase_words = []
    if curr_phrase_words:
        phrases.append({
            "words": curr_phrase_words,
            "start": curr_phrase_words[0]["start"],
            "end": curr_phrase_words[-1]["end"]
        })

    # Flatten all scenes across chapters and compute their start/end timestamps
    chapters = script_data.get("chapters", [])
    if not chapters:
        logger.error("No chapters found in script_data.")
        return "", []

    all_scenes = []
    for ch in chapters:
        ch_id = ch.get("chapter_id", 1)
        ch_title = ch.get("chapter_title", "Chapter")
        ch_sub = ch.get("subtitle", "")
        for sc in ch.get("scenes", []):
            sc_copy = dict(sc)
            sc_copy["chapter_id"] = ch_id
            sc_copy["chapter_title"] = ch_title
            sc_copy["chapter_subtitle"] = ch_sub
            all_scenes.append(sc_copy)

    if not all_scenes:
        logger.error("No scenes found across chapters.")
        return "", []

    # Map words/dialogue to scene durations
    # Distribute total_duration proportionally by dialogue word count
    total_words = sum(max(len(sc.get("dialogue", "").split()), 4) for sc in all_scenes)
    curr_time = 0.0
    for sc in all_scenes:
        sc_words = max(len(sc.get("dialogue", "").split()), 4)
        sc_duration = (sc_words / total_words) * total_duration
        sc["start"] = curr_time
        sc["end"] = curr_time + sc_duration
        curr_time += sc_duration

    # Track Chapter Markers for YouTube Description
    youtube_chapters = []
    seen_chapters = set()
    for sc in all_scenes:
        cid = sc["chapter_id"]
        if cid not in seen_chapters:
            seen_chapters.add(cid)
            m = int(sc["start"] // 60)
            s = int(sc["start"] % 60)
            stamp = f"{m:02d}:{s:02d}"
            youtube_chapters.append({
                "chapter_id": cid,
                "timestamp": stamp,
                "title": f"{sc['chapter_title']}: {sc['chapter_subtitle']}",
                "start_seconds": sc["start"]
            })

    # 1. Normalize scene layouts and fill defaults for all high-IQ explainer layouts
    for sc in all_scenes:
        l_type = sc.get("layout_type", "fullscreen_broll")
        # Direct video start: convert any chapter_bumper to fullscreen_broll with cinematic visuals
        if l_type == "chapter_bumper":
            sc["layout_type"] = "fullscreen_broll"
            l_type = "fullscreen_broll"

        if l_type == "splitscreen_code":
            sc["layout_type"] = "blueprint_schematic"
            l_type = "blueprint_schematic"

        if l_type == "splitscreen_stat":
            if not sc.get("stat_number"):
                sc["stat_number"] = "99.999%"
            if not sc.get("stat_label"):
                sc["stat_label"] = "THEORETICAL RELIABILITY"
            if not sc.get("stat_context"):
                sc["stat_context"] = sc.get("dialogue", "Systemic threshold breached under real-world conditions.")
            if not sc.get("stat_change"):
                sc["stat_change"] = "CASCADE THRESHOLD"

        elif l_type == "blueprint_schematic":
            if not sc.get("schematic_title"):
                sc["schematic_title"] = sc.get("article_headline", "SYSTEM ARCHITECTURE & CONSTRAINTS")
            if not sc.get("schematic_tag"):
                sc["schematic_tag"] = "SPEC // CAD-RECONSTRUCTION"
            if not sc.get("schematic_specs"):
                sc["schematic_specs"] = [
                    {"label": "CLOCK SPEED", "value": "4.85 GHz"},
                    {"label": "QUANTUM TOLERANCE", "value": "±0.002 nm"},
                    {"label": "DATA THROUGHPUT", "value": "1.24 TB/s"},
                    {"label": "CRITICAL RISK", "value": "CRITICAL THRESHOLD"}
                ]

        elif l_type == "kinetic_flowchart":
            if not sc.get("flowchart_title"):
                sc["flowchart_title"] = "CAUSAL LOGIC CHAIN"
            if not sc.get("flowchart_steps"):
                sc["flowchart_steps"] = [
                    {"step": 1, "label": "Initial Sensor Discrepancy", "detail": "Telemetry exceeds buffer allocation", "status": "normal"},
                    {"step": 2, "label": "Uncaught Arithmetic Overflow", "detail": "64-bit float cast to 16-bit integer", "status": "active"},
                    {"step": 3, "label": "Inertial Processor Shutdown", "detail": "Primary and backup CPUs enter dead halt", "status": "critical"},
                    {"step": 4, "label": "Diagnostic Data into Thrusters", "detail": "Rocket swivels nozzles 90 degrees at Mach 2", "status": "critical"}
                ]

        elif l_type == "visual_analogy":
            if not sc.get("analogy_title"):
                sc["analogy_title"] = "THE PHYSICAL ANALOGY"
            if not sc.get("concept_name"):
                sc["concept_name"] = "THE ABSTRACT CODE"
            if not sc.get("concept_desc"):
                sc["concept_desc"] = "Complex mathematical algorithm running in isolated memory."
            if not sc.get("analogy_name"):
                sc["analogy_name"] = "REAL-WORLD METAPHOR"
            if not sc.get("analogy_desc"):
                sc["analogy_desc"] = "Pouring a gallon of water into a pint glass with no overflow sensor."
            if not sc.get("takeaway"):
                sc["takeaway"] = "When software ignores physical boundaries, failure is inevitable."

        elif l_type == "data_timeline_matrix":
            if not sc.get("timeline_title"):
                sc["timeline_title"] = "CHRONOLOGICAL FORENSIC TIMELINE"
            if not sc.get("timeline_events"):
                sc["timeline_events"] = [
                    {"time_label": "T - 00:00", "title": "System Launch", "desc": "All primary and secondary telemetry reporting green.", "severity": "info"},
                    {"time_label": "T + 36.7s", "title": "Primary Unit Halt", "desc": "Arithmetic overflow in horizontal alignment CPU.", "severity": "warning"},
                    {"time_label": "T + 37.2s", "title": "Backup Duplicate Crash", "desc": "Identical legacy routine causes identical shutdown.", "severity": "critical"},
                    {"time_label": "T + 39.0s", "title": "Self-Destruct Sequence", "desc": "Aerodynamic shear triggers automatic mission termination.", "severity": "critical"}
                ]

    # 2. Pre-fetch & cache media assets (B-roll & Memes)
    used_broll_ids = set()
    for sc in all_scenes:
        l_type = sc.get("layout_type", "fullscreen_broll")
        query = sc.get("broll_query") or "quantum physics artificial intelligence server technology"
        if l_type in [
            "fullscreen_broll", "splitscreen_article", "splitscreen_stat",
            "chapter_bumper", "blueprint_schematic", "kinetic_flowchart",
            "visual_analogy", "data_timeline_matrix"
        ]:
            clip_p = fetch_broll_clip(query, orientation="landscape", exclude_ids=used_broll_ids)
            sc["broll_path"] = clip_p
        elif l_type == "meme_reaction":
            m_query = sc.get("meme_query", "michael jordan stop it")
            meme_p = search_giphy_meme_clip(m_query)
            if not meme_p or not os.path.exists(meme_p):
                fallback_entry = LOCAL_REAL_MEMES.get("JORDAN", LOCAL_REAL_MEMES["DEFAULT"])
                meme_p = fallback_entry[0]
            sc["meme_path"] = meme_p

    # 3. ATTEMPT REMOTION (REACT 18 + CSS) MOTION GRAPHICS ENGINE FIRST
    ambient_path = "assets/audio/ambient_tech.wav"
    remotion_scenes = []
    for sc in all_scenes:
        remotion_scenes.append({
            "dialogue": sc.get("dialogue", ""),
            "layout_type": sc.get("layout_type", "fullscreen_broll"),
            "broll_path": _normalize_rel_path(sc.get("broll_path")),
            "meme_path": _normalize_rel_path(sc.get("meme_path")),
            "meme_punchline": sc.get("meme_punchline", "THIS IS FINE"),
            "article_headline": sc.get("article_headline", "CRITICAL TECH BREAKTHROUGH"),
            "article_quote": sc.get("article_quote", "Cascading shifts detected across modern computing."),
            "article_source": sc.get("article_source", "WIRED"),
            "stat_number": sc.get("stat_number", "99.999%"),
            "stat_label": sc.get("stat_label", "ESTIMATED INCIDENT LOSS"),
            "stat_context": sc.get("stat_context", sc.get("dialogue", "Critical systems impacted across multiple cloud regions.")),
            "stat_change": sc.get("stat_change", "+340% SURPLUS RISK"),

            # 1. Blueprint Schematic
            "schematic_title": sc.get("schematic_title"),
            "schematic_tag": sc.get("schematic_tag"),
            "schematic_specs": sc.get("schematic_specs"),

            # 2. Kinetic Flowchart
            "flowchart_title": sc.get("flowchart_title"),
            "flowchart_steps": sc.get("flowchart_steps"),

            # 3. Visual Analogy
            "analogy_title": sc.get("analogy_title"),
            "concept_name": sc.get("concept_name"),
            "concept_desc": sc.get("concept_desc"),
            "analogy_name": sc.get("analogy_name"),
            "analogy_desc": sc.get("analogy_desc"),
            "takeaway": sc.get("takeaway"),

            # 4. Data Timeline Matrix
            "timeline_title": sc.get("timeline_title"),
            "timeline_events": sc.get("timeline_events"),

            "chapter_id": sc.get("chapter_id", 1),
            "chapter_title": sc.get("chapter_title", "CHAPTER"),
            "chapter_subtitle": sc.get("chapter_subtitle", ""),
            "start": sc.get("start", 0.0),
            "end": sc.get("end", 0.0),
            "sfx": sc.get("sfx")
        })

    remotion_props = {
        "title": script_data.get("title", script_data.get("topic", "Tech Documentary")),
        "duration": total_duration,
        "audio_path": _normalize_rel_path(audio_path),
        "ambient_path": _normalize_rel_path(ambient_path) if os.path.exists(ambient_path) else "",
        "scenes": remotion_scenes,
        "word_timings": word_timings,
        "phrases": phrases
    }

    logger.info("Attempting rendering with Remotion (React + CSS Motion Graphics)...")
    if render_remotion_video(remotion_props, output_path):
        logger.info(f"Remotion rendered episodic landscape video successfully: {output_path}")
        return output_path, youtube_chapters

    logger.warning("Remotion rendering unavailable or failed. Falling back to MoviePy engine...")

    # 4. FALLBACK: MoviePy In-Memory VideoClip Rendering
    for sc in all_scenes:
        if sc.get("broll_path") and os.path.exists(sc["broll_path"]):
            try:
                sc["video_clip"] = VideoFileClip(sc["broll_path"])
            except Exception as e:
                logger.warning(f"Failed to load landscape B-roll {sc['broll_path']}: {e}")
                sc["video_clip"] = None
        elif sc.get("meme_path") and os.path.exists(sc["meme_path"]):
            try:
                sc["video_clip"] = VideoFileClip(sc["meme_path"])
            except Exception as e:
                logger.warning(f"Failed to load meme clip {sc['meme_path']}: {e}")
                sc["video_clip"] = None
        else:
            sc["video_clip"] = None

    # Instantiate specialized layout renderers
    vscode_engine = VSCodeRenderer()
    article_engine = ArticleCardRenderer()
    bumper_engine = ChapterBumperRenderer()
    caption_engine = LongCaptionRenderer()

    # Pre-render static card elements where appropriate to optimize frame loop
    for sc in all_scenes:
        l_type = sc.get("layout_type")
        if l_type == "splitscreen_article":
            sc["rendered_card"] = article_engine.render_article_card(
                width=980,
                height=860,
                headline=sc.get("article_headline", "CRITICAL SYSTEM INSTABILITY REPORTED"),
                quote=sc.get("article_quote", "Cascading failures reported across multiple availability zones."),
                source=sc.get("article_source", "FINANCIAL TIMES")
            )
        elif l_type == "splitscreen_stat":
            sc["rendered_card"] = article_engine.render_article_card(
                width=980,
                height=860,
                headline=sc.get("stat_label", "CRITICAL METRIC LOSS"),
                quote=f"{sc.get('stat_number', '$1.2B')} — {sc.get('stat_context', 'Severe production outage.')}",
                source="METRICS REPORT"
            )

    # Frame generator function
    def make_frame(t: float) -> np.ndarray:
        # Locate active scene
        active_scene = all_scenes[0]
        for sc in all_scenes:
            if sc["start"] <= t <= sc["end"]:
                active_scene = sc
                break
        if t > all_scenes[-1]["end"]:
            active_scene = all_scenes[-1]

        l_type = active_scene.get("layout_type", "fullscreen_broll")
        sc_start = active_scene["start"]
        sc_dur = max(active_scene["end"] - sc_start, 1.0)
        local_t = min(max(t - sc_start, 0.0), sc_dur)

        # -------------------------------------------------------------
        # LAYOUT 1: CHAPTER BUMPER
        # -------------------------------------------------------------
        if l_type == "chapter_bumper":
            progress = local_t / sc_dur
            frame_img = bumper_engine.render_bumper(
                width=width,
                height=height,
                chapter_no=active_scene.get("chapter_id", 1),
                chapter_title=active_scene.get("chapter_title", "CHAPTER"),
                subtitle=active_scene.get("chapter_subtitle", ""),
                progress=progress
            )
            return np.array(frame_img)

        # -------------------------------------------------------------
        # LAYOUT 2: MEME REACTION (GIPHY)
        # -------------------------------------------------------------
        elif l_type == "meme_reaction":
            # Dark blurred cyber canvas
            canvas = Image.new("RGBA", (width, height), (12, 16, 28, 255))
            draw = ImageDraw.Draw(canvas)

            # Draw background grid
            for x in range(0, width, 90):
                draw.line([(x, 0), (x, height)], fill=(20, 28, 48), width=1)
            for y in range(0, height, 90):
                draw.line([(0, y), (width, y)], fill=(20, 28, 48), width=1)

            # Center Meme Video Frame
            clip = active_scene.get("video_clip")
            if clip:
                m_t = local_t % clip.duration
                raw_f = clip.get_frame(m_t)
                meme_frame = Image.fromarray(raw_f)

                # Scale to ~960x680 maintaining aspect ratio
                mw = 960
                mh = int(meme_frame.height * (mw / meme_frame.width))
                if mh > 680:
                    mh = 680
                    mw = int(meme_frame.width * (mh / meme_frame.height))
                meme_resized = meme_frame.resize((mw, mh), Image.Resampling.BILINEAR)

                # Center on canvas with sleek border
                mx = (width - mw) // 2
                my = (height - mh) // 2 - 40
                draw.rounded_rectangle([mx - 6, my - 6, mx + mw + 6, my + mh + 6], radius=14, fill=(0, 235, 255, 180))
                canvas.paste(meme_resized, (mx, my))

            # Punchline Banner
            punchline = active_scene.get("meme_punchline", "THIS IS FINE").upper()
            font_banner = ImageFont.truetype(FONT_PATH_BOLD, 42) if FONT_PATH_BOLD else ImageFont.load_default()
            bb = draw.textbbox((0, 0), punchline, font=font_banner)
            bw = (bb[2] - bb[0]) + 60
            bx = (width - bw) // 2
            by = height - 210
            draw.rounded_rectangle([bx, by, bx + bw, by + 68], radius=16, fill=(255, 215, 0, 245), outline=(0, 0, 0), width=3)
            draw.text((bx + 30, by + 12), punchline, font=font_banner, fill=(0, 0, 0))

            frame_base = canvas

        # -------------------------------------------------------------
        # LAYOUT 3 & 4: SPLITSCREEN (ARTICLE & STAT/CODE)
        # -------------------------------------------------------------
        elif l_type in ["splitscreen_article", "splitscreen_stat", "splitscreen_code"]:
            canvas = Image.new("RGBA", (width, height), (10, 14, 24, 255))
            draw = ImageDraw.Draw(canvas)

            # Left Pane (0 to 880px): 16:9 Video Footage
            left_w = 880
            clip = active_scene.get("video_clip")
            if clip:
                v_t = local_t % clip.duration
                raw_f = clip.get_frame(v_t)
                v_img = Image.fromarray(raw_f)
                scale = max(left_w / v_img.width, height / v_img.height)
                nw, nh = int(v_img.width * scale), int(v_img.height * scale)
                v_resized = v_img.resize((nw, nh), Image.Resampling.BILINEAR)
                v_cropped = v_resized.crop(((nw - left_w) // 2, (nh - height) // 2, (nw - left_w) // 2 + left_w, (nh - height) // 2 + height))
                canvas.paste(v_cropped, (0, 0))
            else:
                draw.rectangle([0, 0, left_w, height], fill=(16, 22, 38))

            # Vertical Neon Separator Line
            draw.line([(left_w, 0), (left_w, height)], fill=(0, 220, 255, 180), width=3)

            # Right Pane (880px to 1920px): Floating 3D Card
            card = active_scene.get("rendered_card")
            if card:
                card_x = left_w + 35
                card_y = (height - card.height) // 2
                canvas.alpha_composite(card, (card_x, card_y))

            frame_base = canvas

        # -------------------------------------------------------------
        # LAYOUT 5: FULLSCREEN B-ROLL (CINEMATIC 4K)
        # -------------------------------------------------------------
        else:
            clip = active_scene.get("video_clip")
            if clip:
                v_t = local_t % clip.duration
                raw_f = clip.get_frame(v_t)
                v_img = Image.fromarray(raw_f)

                # Slow Ken Burns Zoom (1.0 to 1.05)
                zoom = 1.0 + 0.05 * (local_t / sc_dur)
                zw, zh = int(width * zoom), int(height * zoom)
                scale = max(zw / v_img.width, zh / v_img.height)
                nw, nh = int(v_img.width * scale), int(v_img.height * scale)
                v_resized = v_img.resize((nw, nh), Image.Resampling.BILINEAR)
                frame_base = v_resized.crop(((nw - width) // 2, (nh - height) // 2, (nw - width) // 2 + width, (nh - height) // 2 + height)).convert("RGBA")
            else:
                frame_base = Image.new("RGBA", (width, height), (14, 18, 30, 255))

            draw = ImageDraw.Draw(frame_base)

            # Top & Bottom Subtle Broadcast Vignette Gradients
            for y in range(160):
                alpha = int(180 * (1.0 - (y / 160.0)))
                draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
            for y in range(height - 180, height):
                progress = (y - (height - 180)) / 180.0
                alpha = int(210 * progress)
                draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

            # Top-Left Broadcast Live Pill (Dynamically sized with high-IQ investigative branding)
            badge_text = "● FORENSIC INVESTIGATION"
            font_badge = ImageFont.truetype(FONT_PATH_BOLD, 20) if FONT_PATH_BOLD else ImageFont.load_default()
            b_bb = draw.textbbox((0, 0), badge_text, font=font_badge)
            b_w = (b_bb[2] - b_bb[0]) + 44
            draw.rounded_rectangle([50, 40, 50 + b_w, 85], radius=12, fill=(225, 29, 72, 230), outline=(255, 120, 150), width=2)
            draw.text((72, 52), badge_text, font=font_badge, fill=(255, 255, 255))

        # -------------------------------------------------------------
        # CAPTIONS OVERLAY (Lower-Third, only outside bumper cards)
        # -------------------------------------------------------------
        if l_type != "chapter_bumper":
            active_phrase = None
            for p in phrases:
                if p["start"] <= t <= p["end"]:
                    active_phrase = p
                    break
            if active_phrase:
                caption_overlay = caption_engine.render_caption_frame(active_phrase, t, width, height)
                frame_base.alpha_composite(caption_overlay)

        return np.array(frame_base.convert("RGB"))

    # Build MoviePy VideoClip
    video_clip = VideoClip(make_frame, duration=total_duration)

    # -----------------------------------------------------------------
    # MULTI-TRACK AUDIO MIXING (Voiceover + Looped Ambient + SFX)
    # -----------------------------------------------------------------
    logger.info("Mixing Multi-Track Audio: Speech + Looped Ambient Bed + Transition Whooshes + Meme Hits...")
    speech_clip = AudioFileClip(audio_path)
    audio_layers = [speech_clip]

    # Looped Ambient Music Bed
    ambient_path = "assets/audio/ambient_tech.wav"
    if os.path.exists(ambient_path):
        try:
            # Loop ambient clip to match total_duration
            amb_base = AudioFileClip(ambient_path)
            amb_dur = amb_base.duration
            repeats = math.ceil(total_duration / amb_dur)
            sub_clips = []
            for i in range(repeats):
                st = i * amb_dur
                dur = min(amb_dur, total_duration - st)
                if dur > 0.1:
                    c = AudioFileClip(ambient_path).subclipped(0, dur).with_start(st).with_volume_scaled(0.12)
                    sub_clips.append(c)
            audio_layers.extend(sub_clips)
        except Exception as e:
            logger.warning(f"Could not mix ambient audio bed: {e}")

    # Whoosh SFX at Chapter Boundaries & Scene Transitions
    whoosh_path = "assets/audio/whoosh.wav"
    if os.path.exists(whoosh_path):
        try:
            for sc in all_scenes:
                if sc.get("layout_type") == "chapter_bumper" and sc["start"] < total_duration - 0.5:
                    w_clip = AudioFileClip(whoosh_path).with_start(sc["start"]).with_volume_scaled(0.35)
                    audio_layers.append(w_clip)
        except Exception as e:
            logger.warning(f"Could not mix whoosh SFX: {e}")

    # Situational Meme SFX (Bruh, Windows Error, Vine Boom, Pop)
    sfx_map = {
        "bruh": "assets/audio/bruh.wav",
        "windows_error": "assets/audio/windows_error.wav",
        "vine_boom": "assets/audio/vine_boom.wav",
        "pop": "assets/audio/pop_click.wav",
        "whoosh": "assets/audio/whoosh.wav"
    }
    for sc in all_scenes:
        sfx_tag = sc.get("sfx")
        if sfx_tag and sfx_tag in sfx_map:
            p = sfx_map[sfx_tag]
            if os.path.exists(p) and sc["start"] < total_duration - 0.5:
                try:
                    vol = 0.40 if sfx_tag in ["bruh", "vine_boom"] else 0.32
                    sfx_clip = AudioFileClip(p).with_start(sc["start"]).with_volume_scaled(vol)
                    audio_layers.append(sfx_clip)
                except Exception as e:
                    logger.warning(f"Could not load SFX {p}: {e}")

    # Final Audio Track Composite
    final_audio = CompositeAudioClip(audio_layers)
    video_with_audio = video_clip.with_audio(final_audio)

    # Export Broadcast MP4
    logger.info(f"Rendering 16:9 MP4 to {output_path}...")
    video_with_audio.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        ffmpeg_params=["-crf", "22", "-pix_fmt", "yuv420p"],
        logger=None
    )

    # Close resources
    try:
        video_with_audio.close()
        for sc in all_scenes:
            if sc.get("video_clip"):
                sc["video_clip"].close()
    except Exception:
        pass

    logger.info(f"Broadcast 16:9 Long Video rendered successfully: {output_path}")
    return output_path, youtube_chapters


if __name__ == "__main__":
    print("Long compositor module loaded.")
