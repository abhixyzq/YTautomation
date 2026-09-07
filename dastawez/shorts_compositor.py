"""
iDastawez - 9:16 Cinematic Civic-Tech Shorts Compositor
Builds 1080x1920 (9:16) ultra-high retention vertical YouTube Shorts for @iDastawez:
- Dynamic Top Alert Badge (e.g. '● SARKARI ALERT // DEADLINE', '● RATION CARD // NEW RULES')
- Glassmorphic Headline & Verification Card (Govt Ministry + Official Portal Domain)
- Dynamic B-Roll video switching every 3.0 - 3.8 seconds with Ken Burns zoom
- Hindi Word-by-Word Bouncing Highlight Captions (Mangal Bold font with neon-yellow active highlight)
- Cinematic Whoosh SFX on scene transitions + Ambient background music (-22dB)
"""

import os
import sys
import re
import math
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

from src.broll_downloader import fetch_broll_clip
from dastawez.voice_generator import clean_hindi_for_tts

logger = logging.getLogger("dastawez.shorts_compositor")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[iDastawez Compositor] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Font Candidates
FONT_HINDI_BOLD = None
FONT_HINDI_REG = None
for candidate in ["C:/Windows/Fonts/mangalb.ttf", "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]:
    if os.path.exists(candidate):
        FONT_HINDI_BOLD = candidate
        break

for candidate in ["C:/Windows/Fonts/mangal.ttf", "C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf"]:
    if os.path.exists(candidate):
        FONT_HINDI_REG = candidate
        break


class HindiShortsCaptionRenderer:
    """
    Renders word-by-word active highlight subtitles for Devanagari Hindi
    with screen-safe margins and high-contrast dark backing.
    """
    def __init__(self, width: int = 1080, height: int = 1920, base_font_size: int = 58):
        self.width = width
        self.height = height
        self.base_font_size = base_font_size
        self.max_allowed_width = width - 140  # 70px safe margin

    def _get_font(self, size: int):
        if FONT_HINDI_BOLD:
            return ImageFont.truetype(FONT_HINDI_BOLD, size)
        return ImageFont.load_default()

    def render_caption_frame(self, current_phrase: Dict[str, Any], current_time: float) -> Image.Image:
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        words = current_phrase.get("words", [])
        if not words:
            return overlay

        font = self._get_font(self.base_font_size)
        space_w = draw.textbbox((0, 0), " ", font=font)[2]

        word_widths = []
        for w in words:
            wt = w["word"]
            bbox = draw.textbbox((0, 0), wt, font=font)
            word_widths.append(bbox[2] - bbox[0])

        total_w = sum(word_widths) + max(0, len(words) - 1) * space_w

        # Scale down if exceeds safe width
        if total_w > self.max_allowed_width:
            scale = self.max_allowed_width / max(total_w, 1)
            new_size = max(int(self.base_font_size * scale), 36)
            font = self._get_font(new_size)
            space_w = draw.textbbox((0, 0), " ", font=font)[2]
            word_widths = []
            for w in words:
                bbox = draw.textbbox((0, 0), w["word"], font=font)
                word_widths.append(bbox[2] - bbox[0])
            total_w = sum(word_widths) + max(0, len(words) - 1) * space_w

        # Center horizontally at middle-lower area (Y=1150)
        start_x = (self.width - total_w) // 2
        y_pos = 1150
        pill_h = 90
        pad_x = 24

        # Dark contrast backing pill
        draw.rounded_rectangle(
            [start_x - pad_x, y_pos - 10, start_x + total_w + pad_x, y_pos + pill_h],
            radius=18,
            fill=(10, 15, 26, 210),
            outline=(255, 230, 0, 180),
            width=2
        )

        curr_x = start_x
        for i, w in enumerate(words):
            wt = w["word"]
            is_active = w["start"] <= current_time <= w["end"] + 0.08
            
            # Active word gets vibrant yellow #FFE600, others clean white
            fill_color = (255, 230, 0, 255) if is_active else (255, 255, 255, 230)
            
            # Drop shadow
            draw.text((curr_x + 2, y_pos + 12), wt, font=font, fill=(0, 0, 0, 220))
            # Main text
            draw.text((curr_x, y_pos + 10), wt, font=font, fill=fill_color)

            curr_x += word_widths[i] + space_w

        return overlay


class DastawezShortsEngine:
    def __init__(self, scenes_data: List[Dict[str, Any]], width: int = WIDTH, height: int = HEIGHT):
        self.scenes = scenes_data
        self.width = width
        self.height = height
        self.font_badge = ImageFont.truetype(FONT_HINDI_BOLD, 28) if FONT_HINDI_BOLD else ImageFont.load_default()
        self.font_title = ImageFont.truetype(FONT_HINDI_BOLD, 46) if FONT_HINDI_BOLD else ImageFont.load_default()
        self.font_meta = ImageFont.truetype(FONT_HINDI_REG, 26) if FONT_HINDI_REG else ImageFont.load_default()

    def get_background_frame(self, t: float) -> Image.Image:
        # Locate active scene
        active_scene = self.scenes[0]
        for sc in self.scenes:
            if sc["start"] <= t <= sc["end"]:
                active_scene = sc
                break
        if t > self.scenes[-1]["end"]:
            active_scene = self.scenes[-1]

        clip = active_scene.get("clip")
        if clip:
            try:
                scene_duration = max(active_scene["end"] - active_scene["start"], 1.0)
                local_t = min(max(t - active_scene["start"], 0.0), clip.duration - 0.05)
                raw_frame = clip.get_frame(local_t)
                frame_img = Image.fromarray(raw_frame)

                # Ken Burns subtle zoom
                progress = (t - active_scene["start"]) / scene_duration
                zoom_factor = 1.0 + 0.05 * min(max(progress, 0.0), 1.0)
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
                cropped = resized.crop((left, top, left + self.width, top + self.height))
                return cropped
            except Exception as e:
                logger.warning(f"Error rendering broll frame: {e}")

        # Fallback Civic-Tech background (Sleek deep navy gradient with grid)
        bg = Image.new("RGB", (self.width, self.height), (12, 18, 32))
        d = ImageDraw.Draw(bg)
        for y in range(0, self.height, 50):
            d.line([(0, y), (self.width, y)], fill=(20, 32, 54), width=1)
        for x in range(0, self.width, 50):
            d.line([(x, 0), (x, self.height)], fill=(20, 32, 54), width=1)
        return bg

    def render_overlay_ui(self, t: float, script_data: Dict[str, Any]) -> Image.Image:
        """Render floating civic card with dynamic alert badge and verified portal metadata."""
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 1. Top Dynamic Alert Pill (Vector Circle Dot + Bold Text)
        badge_text = script_data.get("badge_text", "SARKARI ALERT // OFFICIAL UPDATE")
        bg_col = script_data.get("badge_bg_color", (225, 29, 72, 235))
        border_col = script_data.get("badge_border_color", (255, 120, 150))

        clean_badge = re.sub(r'^[●•\s]+', '', badge_text).strip()
        badge_bbox = draw.textbbox((0, 0), clean_badge, font=self.font_badge)
        text_w = badge_bbox[2] - badge_bbox[0]
        badge_w = text_w + 72

        draw.rounded_rectangle([70, 130, 70 + badge_w, 185], radius=14, fill=bg_col, outline=border_col, width=2)
        # Vector pulsating live dot
        draw.ellipse([92, 150, 106, 164], fill=(255, 255, 255))
        draw.text((118, 142), clean_badge, font=self.font_badge, fill=(255, 255, 255))

        # 2. Glassmorphic Headline Card
        headline_raw = script_data.get("headline", script_data.get("title", ""))
        headline_clean = clean_hindi_for_tts(headline_raw)
        words = headline_clean.split()
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
        lines = lines[:2]

        card_h = len(lines) * 60 + 85
        draw.rounded_rectangle(
            [60, 210, 1020, 210 + card_h],
            radius=20,
            fill=(10, 16, 30, 225),  # Dark civic glass
            outline=(37, 99, 235, 190),
            width=3
        )

        # Draw headline text
        line_y = 235
        for line in lines:
            draw.text((85, line_y), line, font=self.font_title, fill=(255, 255, 255))
            line_y += 58

        # Portal & Ministry verification tag at bottom of card
        portal_domain = script_data.get("portal_domain", "india.gov.in")
        ministry = script_data.get("ministry", "भारत सरकार")
        clean_ministry = re.sub(r'[^\w\s\u0900-\u097F-]', '', ministry).strip()
        meta_tag = f"GOVT: {clean_ministry[:26]}  |  PORTAL: {portal_domain}"
        draw.text((85, line_y + 8), meta_tag, font=self.font_meta, fill=(147, 197, 253))

        # 3. Subtle bottom channel branding
        draw.rounded_rectangle([70, 1810, 290, 1860], radius=12, fill=(15, 23, 42, 210), outline=(56, 189, 248, 140), width=1)
        draw.ellipse([88, 1830, 98, 1840], fill=(239, 68, 68))
        draw.text((108, 1823), "@iDastawez", font=self.font_meta, fill=(255, 255, 255))

        return overlay


def align_storyboard_to_word_timings(
    storyboard: List[Dict[str, Any]], 
    word_timings: List[Dict[str, Any]], 
    total_duration: float
) -> List[Dict[str, Any]]:
    """
    Intelligently synchronizes each storyboard scene's start & end timestamp
    to the exact spoken Hindi words from edge-tts voiceover.
    """
    if not storyboard:
        return []
        
    num_scenes = len(storyboard)
    if not word_timings:
        dur = total_duration / max(num_scenes, 1)
        for i, sc in enumerate(storyboard):
            sc["start"] = round(i * dur, 2)
            sc["end"] = round((i + 1) * dur, 2)
        return storyboard

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

    # Ensure contiguous timeline boundaries from 0.0 to total_duration
    for i in range(len(storyboard)):
        if i == 0:
            storyboard[i]["start"] = 0.0
        else:
            storyboard[i]["start"] = storyboard[i - 1]["end"]
        if i == len(storyboard) - 1:
            storyboard[i]["end"] = round(total_duration, 2)

    return storyboard


def build_dastawez_shorts_video(
    script_data: Dict[str, Any],
    voice_data: Dict[str, Any],
    output_path: str = "output/dastawez_short.mp4",
    fps: int = FPS
) -> str:
    """
    Builds and exports 1080x1920 vertical YouTube Short for @iDastawez
    with 100% topic-matched semantic B-roll, dynamic subtitles & audio sync.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    audio_path = voice_data["audio_path"]
    total_duration = voice_data["duration"]
    phrases = voice_data.get("phrases", [])
    word_timings = voice_data.get("word_timings", [])

    # -------------------------------------------------------------
    # 1. STORYBOARD & TOPIC-ALIGNED SCENE SETUP
    # -------------------------------------------------------------
    storyboard = script_data.get("storyboard")
    if not storyboard or not isinstance(storyboard, list) or len(storyboard) < 3:
        from dastawez.shorts_script_generator import build_dastawez_storyboard
        storyboard = build_dastawez_storyboard(scheme=script_data.get("scheme", {}), script_data=script_data)

    # Align each scene cut to spoken sentence boundaries
    storyboard = align_storyboard_to_word_timings(storyboard, word_timings, total_duration)

    scenes_data = []
    loaded_clips = []
    transition_cuts = []
    used_clip_ids = set()

    logger.info(f"Compositing {len(storyboard)} topic-aligned visual scenes for {total_duration:.1f}s Short...")

    for i, sc in enumerate(storyboard):
        sc_start = sc["start"]
        sc_end = sc["end"]
        if sc_start > 0:
            transition_cuts.append(sc_start)

        query = sc.get("visual_query", "official government document")
        logger.info(f"  [Scene {i+1}/{len(storyboard)}] ({sc_start:.1f}s - {sc_end:.1f}s): Query='{query}' | Text='{sc.get('narration_part', '')[:40]}...'")

        # Download or retrieve vertical portrait B-roll from Pexels with zero repetitions
        clip_path = fetch_broll_clip(query=query, unique_tag=f"dastawez_{i}", exclude_ids=used_clip_ids, orientation="portrait")
        
        # If query didn't return a video, try fallback query
        if not clip_path or not os.path.exists(clip_path):
            fallback_query = "official government document stamp"
            clip_path = fetch_broll_clip(query=fallback_query, unique_tag=f"dastawez_fb_{i}", exclude_ids=used_clip_ids, orientation="portrait")

        clip = None
        if clip_path and os.path.exists(clip_path):
            try:
                raw_clip = VideoFileClip(clip_path)
                req_dur = sc_end - sc_start + 1.0
                if raw_clip.duration < req_dur:
                    loop_count = int(math.ceil(req_dur / max(raw_clip.duration, 0.5)))
                    from moviepy import concatenate_videoclips
                    clip = concatenate_videoclips([raw_clip] * loop_count)
                else:
                    clip = raw_clip
                loaded_clips.append(clip)
            except Exception as e:
                logger.warning(f"Failed to load clip {clip_path}: {e}")
                clip = None

        scenes_data.append({
            "start": sc_start,
            "end": sc_end,
            "clip": clip,
            "query": query,
            "narration_part": sc.get("narration_part", "")
        })

    engine = DastawezShortsEngine(scenes_data=scenes_data, width=WIDTH, height=HEIGHT)
    caption_renderer = HindiShortsCaptionRenderer(width=WIDTH, height=HEIGHT)

    # -------------------------------------------------------------
    # 2. FRAME GENERATOR
    # -------------------------------------------------------------
    def make_frame(t):
        # Base background with Ken Burns zoom
        bg_img = engine.get_background_frame(t)
        frame_base = bg_img.convert("RGBA")

        # Overlay UI (Badge + Headline + Portal card + Branding)
        ui_overlay = engine.render_overlay_ui(t, script_data)
        frame_base.alpha_composite(ui_overlay)

        # Active Subtitles
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

    video_clip = VideoClip(make_frame, duration=total_duration)

    # -------------------------------------------------------------
    # 3. AUDIO MIXING: Voiceover + Subtle BGM + Whoosh SFX
    # -------------------------------------------------------------
    logger.info("Mixing audio track: Voiceover + Whoosh SFX + Subtle BGM...")
    speech_audio = AudioFileClip(audio_path)
    audio_layers = [speech_audio]

    # Whoosh transitions
    whoosh_path = "assets/audio/whoosh.wav"
    if os.path.exists(whoosh_path):
        try:
            intro_whoosh = AudioFileClip(whoosh_path).with_start(0.0).with_volume_scaled(0.32)
            audio_layers.append(intro_whoosh)
            for cut_time in transition_cuts:
                if cut_time < total_duration - 0.8:
                    w_clip = AudioFileClip(whoosh_path).with_start(cut_time).with_volume_scaled(0.24)
                    audio_layers.append(w_clip)
        except Exception as e:
            logger.warning(f"Could not load whoosh SFX: {e}")

    # Ambient Music Bed
    ambient_path = "assets/audio/ambient_tech.wav"
    if os.path.exists(ambient_path):
        try:
            raw_ambient = AudioFileClip(ambient_path)
            if raw_ambient.duration < total_duration:
                from moviepy import concatenate_audioclips
                loops = int(math.ceil(total_duration / max(raw_ambient.duration, 1.0))) + 1
                ambient_clip = concatenate_audioclips([raw_ambient] * loops).subclipped(0, total_duration).with_volume_scaled(0.10)
            else:
                ambient_clip = raw_ambient.subclipped(0, total_duration).with_volume_scaled(0.10)
            audio_layers.append(ambient_clip)
        except Exception as e:
            logger.warning(f"Could not load ambient music: {e}")

    final_audio = CompositeAudioClip(audio_layers)
    video_clip = video_clip.with_audio(final_audio)

    # -------------------------------------------------------------
    # 4. RENDER TO MP4
    # -------------------------------------------------------------
    logger.info(f"Rendering 1080x1920 Short video to: {output_path}...")
    video_clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        ffmpeg_params=["-crf", "22", "-pix_fmt", "yuv420p"],
        threads=4
    )

    # Free clip resources
    for c in loaded_clips:
        try:
            c.close()
        except Exception:
            pass

    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    logger.info(f"✓ iDastawez Short rendered successfully: {output_path} ({file_size_mb:.2f} MB)")
    return output_path


if __name__ == "__main__":
    from dastawez.topics import VERIFIED_GOVT_SCHEMES
    from dastawez.shorts_script_generator import generate_shorts_script
    from dastawez.voice_generator import generate_shorts_voiceover

    test_scheme = VERIFIED_GOVT_SCHEMES[0]
    test_script = generate_shorts_script(test_scheme)
    test_voice = generate_shorts_voiceover(test_script["full_script"], "temp/test_dastawez_short_voice.mp3")
    
    out_file = "output/test_dastawez_short.mp4"
    build_dastawez_shorts_video(test_script, test_voice, out_file)
    print("Test video built at:", out_file)
