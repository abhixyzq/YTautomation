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
from src.meme_engine import (
    pick_story_theme, 
    get_story_meme_package, 
    prepare_meme_scene_data, 
    render_cinematic_meme_scene
)
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
            if sc.get("visual_type") == "broll" and path and os.path.exists(path):
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

    def get_scene_frame(self, t: float) -> Image.Image:
        """Get scaled, non-repeating frame from real 4K footage or cinematic meme scene."""
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

        # 1. Full-frame Fireship Meme Scene
        if active_scene.get("visual_type") == "meme" and active_scene.get("meme_data"):
            scene_duration = max(active_scene["end"] - active_scene["start"], 1.0)
            local_t = min(max(t - active_scene["start"], 0.0), scene_duration)
            return render_cinematic_meme_scene(
                active_scene["meme_data"],
                local_t,
                scene_duration,
                self.width,
                self.height,
                self.font_title
            )

        # 2. 4K Cinematic B-roll with continuous Ken Burns slow-zoom
        elif active_scene.get("clip"):
            clip = active_scene["clip"]
            scene_duration = max(active_scene["end"] - active_scene["start"], 1.0)
            local_t = min(max(t - active_scene["start"], 0.0), clip.duration - 0.05)
            raw_frame = clip.get_frame(local_t)
            frame_img = Image.fromarray(raw_frame)

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
            # Fallback sleek obsidian cyber canvas
            bg = Image.new("RGB", (self.width, self.height), (10, 15, 26))
            d = ImageDraw.Draw(bg)
            for y in range(0, self.height, 60):
                d.line([(0, y), (self.width, y)], fill=(20, 30, 50), width=1)
            return bg

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

        # 2. Glassmorphic Headline Box (Top) - strictly printable ASCII to guarantee no glyph boxes
        import re
        clean_headline = re.sub(r'#\w+', '', story_title)
        clean_headline = re.sub(r'[^\x20-\x7E]', '', clean_headline).strip()
        headline = " ".join(clean_headline.split())
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


def align_storyboard_to_word_timings(
    storyboard: List[Dict[str, Any]], 
    word_timings: List[Dict[str, Any]], 
    total_duration: float
) -> List[Dict[str, Any]]:
    """
    Intelligently synchronizes each storyboard scene's start & end timestamp
    to the exact spoken words from the voiceover.
    """
    if not word_timings or not storyboard:
        dur = total_duration / max(len(storyboard), 1)
        for i, sc in enumerate(storyboard):
            sc["start"] = round(i * dur, 2)
            sc["end"] = round((i + 1) * dur, 2)
        return storyboard

    num_scenes = len(storyboard)
    word_idx = 0
    total_words = len(word_timings)

    for i, sc in enumerate(storyboard):
        part_text = sc.get("narration_part", "")
        part_words = [w for w in part_text.split() if w]
        advance = max(len(part_words), 1)
        target_idx = min(word_idx + advance - 1, total_words - 1)
        
        sc_start = word_timings[word_idx]["start"] if word_idx < total_words else (i * total_duration / num_scenes)
        sc_end = word_timings[target_idx]["end"] if target_idx < total_words else ((i + 1) * total_duration / num_scenes)
        word_idx = min(target_idx + 1, total_words - 1)

        sc["start"] = round(sc_start, 2)
        sc["end"] = round(sc_end, 2)

    # Ensure contiguous boundaries across the timeline
    for i in range(len(storyboard)):
        if i == 0:
            storyboard[i]["start"] = 0.0
        else:
            storyboard[i]["start"] = storyboard[i - 1]["end"]
        if i == len(storyboard) - 1:
            storyboard[i]["end"] = round(total_duration, 2)

    return storyboard


def build_shorts_video(
    story: Dict[str, Any],
    voice_data: Dict[str, Any],
    output_path: str = "output/tech_short.mp4",
    fps: int = FPS
) -> str:
    """Build and export 1080x1920 YouTube Short with 100% real 4K documentary footage & synced Fireship meme cuts."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio_path = voice_data["audio_path"]
    total_duration = voice_data["duration"]
    word_timings = voice_data["word_timings"]

    # -----------------------------------------------------------------
    # STORYBOARD SCENE SETUP: Audio-Aligned Dialogue Cuts & Contextual Memes
    # -----------------------------------------------------------------
    storyboard = story.get("storyboard")
    if not storyboard or not isinstance(storyboard, list) or len(storyboard) < 4:
        storyboard = build_semantic_storyboard(story.get("title", ""), story.get("full_script", ""))

    # Align each scene to spoken sentence timestamps
    storyboard = align_storyboard_to_word_timings(storyboard, word_timings, total_duration)

    # Only fetch B-roll for non-meme scenes (memes never query Pexels!)
    broll_scenes = [sc for sc in storyboard if sc.get("visual_type") != "meme"]
    broll_queries = [sc.get("visual_query", "artificial intelligence technology") for sc in broll_scenes]
    logger.info(f">>> Fetching {len(broll_queries)} unique 4K/HD documentary B-roll clips for storyboard...")
    unique_broll_paths = get_curated_broll_clips(broll_queries, count=len(broll_queries))

    theme_key, theme = pick_story_theme(story)

    scenes_data = []
    broll_idx = 0
    for sc in storyboard:
        v_type = sc.get("visual_type", "broll")
        if v_type == "meme":
            meme_pkg = get_story_meme_package(story, sc, total_duration)
            meme_data = prepare_meme_scene_data(meme_pkg, WIDTH, HEIGHT) if meme_pkg else None
            scenes_data.append({
                "start": sc["start"],
                "end": sc["end"],
                "visual_type": "meme",
                "clip_path": None,
                "meme_pkg": meme_pkg,
                "meme_data": meme_data,
                "visual_query": sc.get("visual_query", "")
            })
            if meme_pkg:
                logger.info(f"Loaded Fireship Meme Scene: {meme_pkg['punchline']} ({sc['start']:.2f}s -> {sc['end']:.2f}s)")
        else:
            clip_path = unique_broll_paths[broll_idx % len(unique_broll_paths)] if unique_broll_paths else None
            broll_idx += 1
            scenes_data.append({
                "start": sc["start"],
                "end": sc["end"],
                "visual_type": "broll",
                "clip_path": clip_path,
                "visual_query": sc.get("visual_query", "")
            })

    num_scenes = len(scenes_data)
    logger.info(f"Compositing {num_scenes}-Scene 4K Documentary Short: {total_duration:.1f}s at {WIDTH}x{HEIGHT}...")

    doc_engine = CinematicDocumentaryEngine(scenes_data, WIDTH, HEIGHT)
    caption_renderer = CaptionRenderer(WIDTH, HEIGHT)
    phrases = group_words_into_phrases(word_timings)

    transition_cuts = [sc["start"] for sc in scenes_data if sc["start"] > 0.5]

    # Frame generator function
    def make_frame(t):
        # 1. Scaled, Ken-Burns animated 100% Real 4K B-roll or Full-Frame Meme background
        frame_base = doc_engine.get_scene_frame(t).convert("RGBA")

        # 2. Cinematic vignette and top/bottom gradient overlay
        frame_base.alpha_composite(doc_engine.vignette)

        # 3. Glassmorphic Breaking Tech Headline Card & Dynamic Story Badge
        ui_overlay = doc_engine.render_overlay_ui(t, story, total_duration)
        frame_base.alpha_composite(ui_overlay)

        # 4. High-retention active word-by-word subtitles
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
    # AUDIO MIXING: Neural Voice + Ambient Cyberpunk Bed + Transition SFX + Meme Boom
    # -----------------------------------------------------------------
    logger.info("Mixing audio track: Voiceover + Ambient Cyberpunk Bed + Transition SFX + Meme Punch...")
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
    # FIRESHIP MEME COMEDIC PUNCH AUDIO TRIGGERS (Situational Remotion Sound Effects)
    # -----------------------------------------------------------------
    sfx_map = {
        "windows_error": "assets/audio/windows_error.wav",
        "bruh": "assets/audio/bruh.wav",
        "vine_boom": "assets/audio/vine_boom.wav",
        "record_scratch": "assets/audio/record_scratch.wav",
        "whip": "assets/audio/whip.wav",
        "pop": "assets/audio/pop_click.wav"
    }
    fallback_meme_sfx = "assets/audio/vine_boom.wav" if os.path.exists("assets/audio/vine_boom.wav") else "assets/audio/pop_click.wav"

    for sc in scenes_data:
        if sc.get("visual_type") == "meme":
            sfx_tag = sc.get("meme_pkg", {}).get("sfx", "") if isinstance(sc.get("meme_pkg"), dict) else sc.get("sfx", "")
            target_sfx_path = sfx_map.get(sfx_tag, fallback_meme_sfx)
            if not os.path.exists(target_sfx_path):
                target_sfx_path = fallback_meme_sfx

            if os.path.exists(target_sfx_path):
                try:
                    vol = 0.42 if "bruh" in target_sfx_path else (0.35 if "windows" in target_sfx_path else 0.38)
                    meme_sfx = AudioFileClip(target_sfx_path).with_start(sc["start"]).with_volume_scaled(vol)
                    audio_layers.append(meme_sfx)
                    logger.info(f"Attached situational meme SFX [{sfx_tag} -> {os.path.basename(target_sfx_path)}] at {sc['start']:.2f}s")
                except Exception as e:
                    logger.warning(f"Could not load meme SFX {target_sfx_path}: {e}")

    # -----------------------------------------------------------------
    # CONTEXTUAL EAR-CANDY SFX: Digital Chimes on Numbers, UI Pops on Keywords
    # -----------------------------------------------------------------
    chirp_path = "assets/audio/digital_chirp.wav"
    pop_path = "assets/audio/pop_click.wav"
    last_sfx_time = 0.6
    min_sfx_gap = 2.8

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
    for sc in doc_engine.scenes:
        c = sc.get("clip")
        if c:
            try:
                c.close()
            except Exception:
                pass
        m_clip = sc.get("meme_data", {}).get("clip") if isinstance(sc.get("meme_data"), dict) else None
        if m_clip:
            try:
                m_clip.close()
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
