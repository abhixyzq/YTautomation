"""
Cinematic Tech Documentary Shorts Compositor (Fireship / Vox Style)
100% Real Footage, Zero Cheap Avatars, Ultra-High Retention:
- Dynamic 4K/HD Tech B-roll video switching every 2.8 - 3.5 seconds
- Cinematic Whoosh SFX on scene transitions
- Ambient Cyberpunk Drone background music (-20dB)
- Glassmorphic Breaking Tech Headline Card
- Floating Syntax-Highlighted Code IDE overlay during deep-dives
- Viral Word-by-Word Bouncing Highlight Captions
- Dark Cinematic Edge Vignette for Broadcast Polish
"""

import os
import sys
import re
import math
import logging
from typing import Dict, Any, List, Optional
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

from src.caption_engine import CaptionRenderer, group_words_into_phrases
from src.broll_downloader import get_curated_broll_clips
from src.meme_engine import pick_story_theme, get_story_meme_package, render_meme_punchline_frame
from src.script_generator import build_semantic_storyboard

logger = logging.getLogger(__name__)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

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


def get_dynamic_badge_meta(story: Any) -> tuple:
    """
    Returns (badge_text, bg_color, border_color) tailored to the breaking story topic.
    """
    if isinstance(story, dict):
        title_upper = story.get("title", "").upper()
        source_upper = story.get("source", "").upper()
    else:
        title_upper = str(story).upper()
        source_upper = ""

    if "OPENAI" in title_upper or "GPT" in title_upper:
        return ("● OPENAI CONFIDENTIAL", (16, 185, 129, 235), (110, 231, 183))  # Emerald Green
    elif "GOOGLE" in title_upper or "GEMINI" in title_upper or "DEEPMIND" in title_upper:
        return ("● GOOGLE AI RADAR", (37, 99, 235, 235), (147, 197, 253))      # Google Royal Blue
    elif "NVIDIA" in title_upper or "GPU" in title_upper or "CHIP" in title_upper:
        return ("● HARDWARE WAR", (101, 163, 13, 235), (190, 242, 100))        # Nvidia Lime
    elif "META" in title_upper or "LLAMA" in title_upper or "ZUCK" in title_upper:
        return ("● OPEN SOURCE LEAK", (124, 58, 237, 235), (196, 181, 253))    # Meta Purple
    elif any(k in title_upper for k in ["LEAK", "EXPOSED", "SECRET", "SCANDAL", "SHOCK", "DISASTER"]):
        return ("● BREAKING INTEL", (225, 29, 72, 235), (255, 120, 150))       # Crimson Warning
    elif "HACKER NEWS" in source_upper:
        return ("● SILICON VALLEY RADAR", (234, 88, 12, 235), (253, 186, 116)) # HN Orange
    elif "REDDIT" in source_upper:
        return ("● DEV COMMUNITY TREND", (220, 38, 38, 235), (254, 202, 202))  # Reddit Red
    else:
        return ("● BREAKING TECH RADAR", (225, 29, 72, 235), (255, 120, 150))   # Tech Crimson


class CinematicDocumentaryEngine:
    def __init__(self, scenes: List[Dict[str, Any]], width: int = WIDTH, height: int = HEIGHT):
        self.width = width
        self.height = height
        self.scenes = scenes
        
        # Load VideoFileClips for scenes that have broll paths
        for sc in self.scenes:
            path = sc.get("clip_path")
            if path and os.path.exists(path):
                try:
                    sc["clip"] = VideoFileClip(path)
                except Exception as e:
                    logger.warning(f"Failed to load B-roll clip {path}: {e}")
                    sc["clip"] = None
            else:
                sc["clip"] = None

        self.font_title = ImageFont.truetype(FONT_PATH_BOLD, 48) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_badge = ImageFont.truetype(FONT_PATH_BOLD, 26) if FONT_PATH_BOLD else ImageFont.load_default()
        self.font_code = ImageFont.truetype(FONT_PATH_CODE, 30) if FONT_PATH_CODE else ImageFont.load_default()
        self.font_code_small = ImageFont.truetype(FONT_PATH_CODE, 24) if FONT_PATH_CODE else ImageFont.load_default()

        # Pre-compute a smooth cinematic vignette
        self.vignette = self._generate_cinematic_vignette()

    def _generate_cinematic_vignette(self) -> Image.Image:
        """Create a soft dark radial vignette and vertical top/bottom gradient overlay."""
        vig = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(vig)
        
        # Dark gradient top (y: 0 to 450) to make headline pop
        for y in range(450):
            alpha = int(210 * (1.0 - (y / 450.0)))
            draw.line([(0, y), (self.width, y)], fill=(0, 0, 0, alpha))
            
        # Dark gradient bottom (y: 1100 to 1920) to make captions and footer pop
        for y in range(1100, self.height):
            progress = (y - 1100) / (self.height - 1100)
            alpha = int(220 * progress)
            draw.line([(0, y), (self.width, y)], fill=(0, 0, 0, alpha))
            
        return vig

    def render_code_card_frame(self, scene: Dict[str, Any], t: float) -> Image.Image:
        """Render a sleek Fireship-style VS Code editor scene with syntax highlighting."""
        bg = Image.new("RGB", (self.width, self.height), (12, 16, 24))
        draw = ImageDraw.Draw(bg)
        
        # Subtle dark cyber grid
        for y in range(0, self.height, 60):
            draw.line([(0, y), (self.width, y)], fill=(20, 26, 38), width=1)

        # VS Code Window
        win_x0, win_y0, win_x1, win_y1 = 50, 480, 1030, 1260
        glow_col = (86, 156, 214)  # VS Code Blue
        draw.rounded_rectangle([win_x0 - 2, win_y0 - 2, win_x1 + 2, win_y1 + 2], radius=18, fill=None, outline=glow_col, width=2)
        draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y1], radius=16, fill=(28, 32, 42))

        # Window Header
        header_h = 60
        draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y0 + header_h], radius=16, fill=(20, 24, 32))
        draw.ellipse([win_x0 + 25, win_y0 + 22, win_x0 + 41, win_y0 + 38], fill=(255, 95, 87))
        draw.ellipse([win_x0 + 52, win_y0 + 22, win_x0 + 68, win_y0 + 38], fill=(254, 188, 46))
        draw.ellipse([win_x0 + 79, win_y0 + 22, win_x0 + 95, win_y0 + 38], fill=(40, 200, 64))
        draw.text((win_x0 + 130, win_y0 + 16), "production_hotfix.py", font=self.font_code_small, fill=(210, 220, 235))

        # Gutter Divider
        gutter_w = 75
        draw.line([(win_x0 + gutter_w, win_y0 + header_h), (win_x0 + gutter_w, win_y1)], fill=(42, 48, 62), width=1)

        snippet = scene.get("code_snippet", "def test_in_prod():\n    return 'LGTM 🚀'")
        lines = snippet.split("\n")
        code_y = win_y0 + header_h + 30
        for l_num, line in enumerate(lines, 1):
            draw.text((win_x0 + 18, code_y), f"{l_num:2d}", font=self.font_code, fill=(90, 100, 120))
            x_pos = win_x0 + gutter_w + 25
            for tok in line.split(" "):
                tok_clean = tok.strip("():,[]{}")
                col = (220, 220, 220)
                if tok_clean in ["def", "import", "from", "return", "class", "async", "await", "if", "else", "for", "in", "fn", "let", "mut"]:
                    col = (86, 156, 214)  # Keyword blue
                elif tok.startswith("#") or tok.startswith("//"):
                    col = (106, 153, 85)  # Comment green
                elif "'" in tok or '"' in tok:
                    col = (206, 145, 120) # String coral
                elif any(c.isdigit() for c in tok):
                    col = (181, 206, 168) # Number lime
                elif "(" in tok:
                    col = (220, 220, 170) # Func gold
                draw.text((x_pos, code_y), tok + " ", font=self.font_code, fill=col)
                tok_bbox = draw.textbbox((0, 0), tok + " ", font=self.font_code)
                x_pos += (tok_bbox[2] - tok_bbox[0])
            code_y += 50

        # Blinking Cursor
        if int(t * 2) % 2 == 0:
            draw.rectangle([win_x0 + gutter_w + 28, code_y, win_x0 + gutter_w + 42, code_y + 34], fill=(86, 156, 214))

        return bg

    def render_terminal_card_frame(self, scene: Dict[str, Any], t: float) -> Image.Image:
        """Render a retro/cyber hacker terminal CLI window."""
        bg = Image.new("RGB", (self.width, self.height), (10, 14, 18))
        draw = ImageDraw.Draw(bg)

        for y in range(0, self.height, 60):
            draw.line([(0, y), (self.width, y)], fill=(16, 24, 30), width=1)

        win_x0, win_y0, win_x1, win_y1 = 50, 480, 1030, 1260
        neon_green = (0, 255, 136)
        draw.rounded_rectangle([win_x0 - 2, win_y0 - 2, win_x1 + 2, win_y1 + 2], radius=18, fill=None, outline=neon_green, width=2)
        draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y1], radius=16, fill=(12, 18, 22))

        header_h = 60
        draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y0 + header_h], radius=16, fill=(18, 26, 32))
        draw.ellipse([win_x0 + 25, win_y0 + 22, win_x0 + 41, win_y0 + 38], fill=(255, 95, 87))
        draw.ellipse([win_x0 + 52, win_y0 + 22, win_x0 + 68, win_y0 + 38], fill=(254, 188, 46))
        draw.ellipse([win_x0 + 79, win_y0 + 22, win_x0 + 95, win_y0 + 38], fill=(40, 200, 64))
        draw.text((win_x0 + 130, win_y0 + 16), "bash — 80x24 — ⚡ SSH ROOT", font=self.font_code_small, fill=(0, 235, 255))

        cmd_text = scene.get("terminal_cmd", "$ ./execute_override.sh\n> [OK] Connected to agent network...")
        lines = cmd_text.split("\n")
        term_y = win_y0 + header_h + 35
        for line in lines:
            col = neon_green if line.startswith("$") else (0, 230, 255) if line.startswith(">") else (220, 235, 245)
            draw.text((win_x0 + 35, term_y), line, font=self.font_code, fill=col)
            term_y += 50

        if int(t * 3) % 2 == 0:
            draw.rectangle([win_x0 + 35, term_y, win_x0 + 52, term_y + 32], fill=neon_green)

        return bg

    def get_scene_frame(self, t: float) -> Image.Image:
        """Get scaled, non-repeating frame based on the active storyboard scene."""
        if not self.scenes:
            # Fallback cyber canvas
            bg = Image.new("RGB", (self.width, self.height), (10, 15, 26))
            d = ImageDraw.Draw(bg)
            for y in range(0, self.height, 60):
                d.line([(0, y), (self.width, y)], fill=(20, 30, 50), width=1)
            return bg

        # Locate active scene
        active_scene = self.scenes[0]
        for sc in self.scenes:
            if sc["start"] <= t <= sc["end"]:
                active_scene = sc
                break
        if t > self.scenes[-1]["end"]:
            active_scene = self.scenes[-1]

        v_type = active_scene.get("visual_type", "broll")

        if v_type == "code_card":
            return self.render_code_card_frame(active_scene, t)
        elif v_type == "terminal":
            return self.render_terminal_card_frame(active_scene, t)
        elif v_type == "broll" and active_scene.get("clip"):
            clip = active_scene["clip"]
            scene_duration = max(active_scene["end"] - active_scene["start"], 1.0)
            local_t = min(max(t - active_scene["start"], 0.0), clip.duration - 0.05)
            raw_frame = clip.get_frame(local_t)
            frame_img = Image.fromarray(raw_frame)

            # Continuous Ken Burns slow-zoom across scene duration
            progress = (t - active_scene["start"]) / scene_duration
            zoom_factor = 1.0 + 0.06 * min(max(progress, 0.0), 1.0)
            target_w = int(self.width * zoom_factor)
            target_h = int(self.height * zoom_factor)

            scale_w = target_w / frame_img.width
            scale_h = target_h / frame_img.height
            scale = max(scale_w, scale_h)
            new_w = int(frame_img.width * scale)
            new_h = int(frame_img.height * scale)

            resized = frame_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
            left = (new_w - self.width) // 2
            top = (new_h - self.height) // 2
            return resized.crop((left, top, left + self.width, top + self.height))
        else:
            # Fallback to code card
            return self.render_code_card_frame(active_scene, t)

    def render_overlay_ui(self, t: float, story: Any, total_duration: float) -> Image.Image:
        """Render floating glassmorphic news card with dynamic story-specific category badge."""
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        story_title = story.get("title", "BREAKING TECH") if isinstance(story, dict) else str(story)

        # 1. Top Live Dynamic Category Pill (Customized by Story Topic)
        badge_text, bg_col, border_col = get_dynamic_badge_meta(story)
        badge_bbox = draw.textbbox((0, 0), badge_text, font=self.font_badge)
        badge_w = (badge_bbox[2] - badge_bbox[0]) + 52
        draw.rounded_rectangle([70, 130, 70 + badge_w, 185], radius=14, fill=bg_col, outline=border_col, width=2)
        draw.text((96, 142), badge_text, font=self.font_badge, fill=(255, 255, 255))

        # 2. Glassmorphic Headline Box (Top)
        headline = story_title.replace("#Shorts", "").replace("#Tech", "").replace("#AI", "").strip()
        words = headline.split()
        lines = []
        curr_line = []
        for w in words:
            curr_line.append(w)
            bbox = draw.textbbox((0, 0), " ".join(curr_line), font=self.font_title)
            if (bbox[2] - bbox[0]) > 840:
                curr_line.pop()
                lines.append(" ".join(curr_line))
                curr_line = [w]
        if curr_line:
            lines.append(" ".join(curr_line))
        lines = lines[:3]

        card_h = len(lines) * 62 + 45
        draw.rounded_rectangle(
            [60, 210, 1020, 210 + card_h],
            radius=20,
            fill=(10, 15, 28, 210),  # Dark glass backing
            outline=(0, 235, 255, 160),
            width=3
        )
        line_y = 232
        for line in lines:
            draw.text((92, line_y), line, font=self.font_title, fill=(255, 255, 255))
            line_y += 62

        return overlay


def build_shorts_video(
    story: Dict[str, Any],
    voice_data: Dict[str, Any],
    output_path: str = "output/tech_short.mp4",
    fps: int = FPS
) -> str:
    """Build and export the final 1080x1920 YouTube Shorts MP4 with multi-clip B-roll and SFX."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio_path = voice_data["audio_path"]
    total_duration = voice_data["duration"]
    word_timings = voice_data["word_timings"]

    # -----------------------------------------------------------------
    # STORYBOARD SCENE SETUP: 1-to-1 Narrative Matching, Zero-Repeat B-Roll
    # -----------------------------------------------------------------
    storyboard = story.get("storyboard")
    if not storyboard or not isinstance(storyboard, list) or len(storyboard) < 4:
        storyboard = build_semantic_storyboard(story.get("title", ""), story.get("full_script", ""))

    num_scenes = len(storyboard)
    scene_dur = total_duration / num_scenes
    
    # Collect queries for broll scenes
    broll_queries = [sc.get("visual_query", "artificial intelligence technology") for sc in storyboard if sc.get("visual_type") == "broll"]
    logger.info(f">>> Fetching {len(broll_queries)} unique non-repeating B-roll clips for storyboard...")
    unique_broll_paths = get_curated_broll_clips(broll_queries, count=len(broll_queries))

    scenes_data = []
    broll_idx = 0
    for i, sc in enumerate(storyboard):
        sc_start = i * scene_dur
        sc_end = (i + 1) * scene_dur
        v_type = sc.get("visual_type", "broll")
        clip_path = None
        if v_type == "broll":
            if broll_idx < len(unique_broll_paths):
                clip_path = unique_broll_paths[broll_idx]
                broll_idx += 1
            else:
                # If no more unique broll clips, convert to code card or terminal so we NEVER repeat a video!
                v_type = "code_card" if i % 2 == 0 else "terminal"

        scenes_data.append({
            "start": sc_start,
            "end": sc_end,
            "visual_type": v_type,
            "clip_path": clip_path,
            "code_snippet": sc.get("code_snippet", "def optimize():\n    return 'Testing in Prod 🚀'"),
            "terminal_cmd": sc.get("terminal_cmd", "$ curl -X POST https://api.internal/v1/leak\n> [INFO] Connection established."),
            "visual_query": sc.get("visual_query", "")
        })

    logger.info(f"Compositing {num_scenes}-Scene Fireship Video: {total_duration:.1f}s at {WIDTH}x{HEIGHT} (Zero Video Loop)...")
    theme_key, theme = pick_story_theme(story)
    meme_pkg = get_story_meme_package(story, total_duration)
    if meme_pkg:
        logger.info(f"Loaded Fireship Meme Pop: {meme_pkg['punchline']} ({meme_pkg['start_time']}s - {meme_pkg['end_time']}s)")

    doc_engine = CinematicDocumentaryEngine(scenes_data, WIDTH, HEIGHT)
    caption_renderer = CaptionRenderer(WIDTH, HEIGHT)
    phrases = group_words_into_phrases(word_timings)

    transition_cuts = [sc["start"] for sc in scenes_data if sc["start"] > 0.5]

    # Frame generator function
    def make_frame(t):
        # 1. Scaled, Ken-Burns animated 4K B-roll background or Code/Terminal Scene
        frame_base = doc_engine.get_scene_frame(t).convert("RGBA")

        # 2. Cinematic vignette and top/bottom gradient overlay
        frame_base.alpha_composite(doc_engine.vignette)

        # 3. Glassmorphic Breaking Tech Headline Card & Dynamic Story Badge
        ui_overlay = doc_engine.render_overlay_ui(t, story, total_duration)
        frame_base.alpha_composite(ui_overlay)

        # 4. Fireship Contextual Meme Card Pop
        if meme_pkg:
            meme_overlay = render_meme_punchline_frame(meme_pkg, t, WIDTH, HEIGHT, doc_engine.font_title)
            if meme_overlay:
                frame_base.alpha_composite(meme_overlay)

        # 5. High-retention active word-by-word subtitles
        active_phrase = None
        for p in phrases:
            if p["start"] <= t <= p["end"]:
                active_phrase = p
                break
        if not active_phrase and phrases and t < phrases[-1]["end"]:
            active_phrase = min(phrases, key=lambda p: abs(p["start"] - t))

        if active_phrase:
            caption_overlay = caption_renderer.render_caption_frame(active_phrase, t)
            frame_base.alpha_composite(caption_overlay)

        return np.array(frame_base.convert("RGB"))

    # Build Video Clip
    video_clip = VideoClip(make_frame, duration=total_duration)

    # -----------------------------------------------------------------
    # AUDIO MIXING: Neural Voice + Ambient Cyberpunk Music + Whoosh SFX
    # -----------------------------------------------------------------
    logger.info("Mixing audio track: Voiceover + Ambient Cyberpunk Bed + Transition SFX...")
    speech_audio = AudioFileClip(audio_path)
    audio_layers = [speech_audio]

    # Ambient Music Bed
    ambient_path = "assets/audio/ambient_tech.wav"
    if os.path.exists(ambient_path):
        try:
            ambient_clip = AudioFileClip(ambient_path).subclipped(0, total_duration).with_volume_scaled(0.14)
            audio_layers.append(ambient_clip)
        except Exception as e:
            logger.warning(f"Could not load ambient audio: {e}")

    # Whoosh Transition Sound Effects on every scene cut and at 0.0s hook
    whoosh_path = "assets/audio/whoosh.wav"
    if os.path.exists(whoosh_path):
        try:
            # Opening audio impact to stop scroll immediately
            intro_whoosh = AudioFileClip(whoosh_path).with_start(0.0).with_volume_scaled(0.35)
            audio_layers.append(intro_whoosh)

            for cut_time in transition_cuts:
                if cut_time < total_duration - 1.0:
                    w_clip = AudioFileClip(whoosh_path).with_start(cut_time).with_volume_scaled(0.28)
                    audio_layers.append(w_clip)
        except Exception as e:
            logger.warning(f"Could not load whoosh SFX: {e}")

    # -----------------------------------------------------------------
    # CONTEXTUAL EAR-CANDY SFX: Digital Chimes on Numbers, UI Pops on Leaks / Code Cards
    # -----------------------------------------------------------------
    chirp_path = "assets/audio/digital_chirp.wav"
    pop_path = "assets/audio/pop_click.wav"
    last_sfx_time = 0.6
    min_sfx_gap = 2.8

    # Trigger audio chime when a code card or terminal scene begins!
    for sc in scenes_data:
        sc_t = sc["start"]
        if sc["visual_type"] in ["code_card", "terminal"] and sc_t > 1.0:
            if os.path.exists(chirp_path) and sc_t - last_sfx_time >= min_sfx_gap:
                try:
                    sc_sfx = AudioFileClip(chirp_path).with_start(sc_t).with_volume_scaled(0.22)
                    audio_layers.append(sc_sfx)
                    last_sfx_time = sc_t
                except Exception:
                    pass

    NUMERIC_KEYWORDS = {"BILLION", "MILLION", "PERCENT", "DOLLARS", "COST", "PRICING", "HUNDRED", "THOUSAND"}
    SHOCK_KEYWORDS = {"LEAKED", "SECRET", "EXPOSED", "SHOCK", "DISASTER", "HACKED", "CRAZY", "INSANE"}

    for item in word_timings:
        w_raw = item["word"].upper()
        w_clean = re.sub(r'[^A-Z0-9%]', '', w_raw)
        w_time = item["start"]

        if w_time - last_sfx_time < min_sfx_gap or w_time >= total_duration - 1.0:
            continue

        # 1. Numbers / Percentages / Stats -> High-tech digital chime
        has_digit = any(char.isdigit() for char in w_clean) or "%" in w_clean or w_clean in NUMERIC_KEYWORDS
        if has_digit and os.path.exists(chirp_path):
            try:
                ch_clip = AudioFileClip(chirp_path).with_start(w_time).with_volume_scaled(0.18)
                audio_layers.append(ch_clip)
                last_sfx_time = w_time
                continue
            except Exception as e:
                logger.warning(f"Could not load chirp SFX: {e}")

        # 2. Shock / Leak Words -> UI Pop Click
        if (w_clean in SHOCK_KEYWORDS or "LEAK" in w_clean) and os.path.exists(pop_path):
            try:
                pop_clip = AudioFileClip(pop_path).with_start(w_time).with_volume_scaled(0.22)
                audio_layers.append(pop_clip)
                last_sfx_time = w_time
            except Exception as e:
                logger.warning(f"Could not load pop SFX: {e}")

    # 3. Fireship Meme Pop-in Audio Trigger
    if meme_pkg and os.path.exists(pop_path):
        try:
            meme_sfx = AudioFileClip(pop_path).with_start(meme_pkg["start_time"]).with_volume_scaled(0.30)
            audio_layers.append(meme_sfx)
        except Exception:
            pass

    final_audio = CompositeAudioClip(audio_layers)
    video_clip = video_clip.with_audio(final_audio)

    # Render with libx264 fast preset
    video_clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        ffmpeg_params=["-crf", "22", "-pix_fmt", "yuv420p"],
        threads=4
    )

    # Close clips to free resources
    for c in doc_engine.broll_clips:
        try:
            c.close()
        except Exception:
            pass

    logger.info(f"OUTSTANDING Short generated successfully at: {output_path}")
    return output_path


if __name__ == "__main__":
    from src.voice_generator import generate_voiceover
    test_story = {
        "title": "Discovery of a new OpenAI agent message board",
        "visual_keywords": ["artificial intelligence", "coding terminal"]
    }
    sample_text = "Wait, did you see what just happened in tech? Discovery of a new OpenAI agent message board. Engineers are stunned."
    voice = generate_voiceover(sample_text)
    out = build_shorts_video(test_story, voice, output_path="temp/test_doc_short.mp4")
    print("Test documentary video generated:", out)
