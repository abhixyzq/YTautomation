"""
Autonomous AI Avatar Tech Shorts Pipeline - Master Orchestrator
100% Free & Automated.

Usage:
  python main.py --dry-run             # Generates video locally without uploading
  python main.py --publish             # Generates video and publishes to YouTube
  python main.py --topic "Your Topic"  # Generates a video on a specific topic
"""

import os
import sys
import argparse
import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Orchestrator")

from src.news_fetcher import (
    get_trending_tech_stories,
    filter_previously_published_stories,
    mark_story_as_published
)
from src.script_generator import generate_tech_script
from src.long_script_generator import generate_long_form_script
from src.voice_generator import generate_voiceover
from src.video_compositor import build_shorts_video
from src.long_compositor import build_long_video
from src.youtube_uploader import upload_short_to_youtube, upload_long_video_to_youtube
from src.instagram_uploader import upload_reel_to_instagram


def print_banner(mode: str = "short"):
    if mode == "long":
        banner = """
========================================================================
   MIND-BENDING VISUAL EXPLAINER & DEEP DIVE (16:9 BROADCAST 1080P)
   Architecture: Veritasium + Lemmino + Think School (High-IQ Deep Dives)
========================================================================
"""
    else:
        banner = """
========================================================================
   CINEMATIC TECH DOCUMENTARY SHORTS PIPELINE (100% REAL 4K FOOTAGE)
   Architecture: Fireship / Vox Style (Zero Cheap Avatars, Broadcast Grade)
========================================================================
"""
    print(banner)


def run_pipeline(dry_run: bool = True, custom_topic: str = None):
    print_banner(mode="short")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ---------------------------------------------------------
    # STEP 1: Trending Tech News Discovery & Duplicate Prevention
    # ---------------------------------------------------------
    logger.info(">>> STEP 1: Scanning Hacker News, Reddit, and RSS for Trending Tech...")
    if custom_topic:
        story = {
            "title": custom_topic,
            "source": "Custom User Topic",
            "summary": custom_topic,
            "url": "https://news.ycombinator.com"
        }
    else:
        stories = get_trending_tech_stories()
        if not stories:
            logger.error("No tech stories available. Exiting.")
            return None

        # Filter out stories covered in previous runs (48h - 7d duplicate prevention)
        fresh_stories = filter_previously_published_stories(stories)
        if not fresh_stories:
            logger.warning("All top trending stories have been recently published! Falling back to full pool.")
            fresh_stories = stories

        import random
        # Pick from top fresh trending stories to guarantee variety across daily drops
        story = random.choice(fresh_stories[:min(5, len(fresh_stories))])
        
    logger.info(f"Selected Fresh Story: [{story['source']}] {story['title']}")

    # ---------------------------------------------------------
    # STEP 2: Script Generation (Gemini 1.5 Flash Free Tier)
    # ---------------------------------------------------------
    logger.info(">>> STEP 2: Generating Viral 35-45s Tech Script via Gemini...")
    script_data = generate_tech_script(story)
    logger.info(f"Video Title: {script_data['title']}")
    logger.info(f"Hook: {script_data.get('hook', '')}")
    logger.info(f"Full Script: {script_data['full_script']}")

    # ---------------------------------------------------------
    # STEP 3: Neural Voice Synthesis (edge-tts)
    # ---------------------------------------------------------
    logger.info(">>> STEP 3: Synthesizing Studio Neural Audio via edge-tts...")
    audio_temp_path = f"temp/speech_{timestamp}.mp3"
    voice_data = generate_voiceover(
        text=script_data["full_script"],
        output_path=audio_temp_path
    )
    logger.info(f"Voiceover Ready: {voice_data['duration']}s | Words: {len(voice_data['word_timings'])}")

    # ---------------------------------------------------------
    # STEP 4: Video Compositing (Cyber Canvas + Avatar + Captions)
    # ---------------------------------------------------------
    logger.info(">>> STEP 4: Compositing 1080x1920 Vertical Short at 30 FPS...")
    output_filename = f"output/Short_{timestamp}.mp4"
    final_video_path = build_shorts_video(
        story=script_data,
        voice_data=voice_data,
        output_path=output_filename
    )
    
    file_size_mb = os.path.getsize(final_video_path) / (1024 * 1024)
    logger.info(f"Video Render Complete! Path: {final_video_path} ({file_size_mb:.2f} MB)")

    # ---------------------------------------------------------
    # STEP 5: YouTube Publishing
    # ---------------------------------------------------------
    if not dry_run:
        logger.info(">>> STEP 5A: Publishing Video Directly to YouTube...")
        publish_mode = os.getenv("PUBLISH_MODE", "PUBLIC")
        video_url = upload_short_to_youtube(
            video_path=final_video_path,
            title=script_data["title"],
            description=f"{script_data.get('hook', '')}\n\n{script_data.get('body', '')}\n\n{script_data.get('cta', '')}",
            tags=script_data.get("tags", ["Shorts", "Tech", "AI"]),
            privacy_status=publish_mode,
            comment_text=script_data.get("cta")
        )
        if video_url:
            logger.info(f"MISSION ACCOMPLISHED! YouTube Video URL: {video_url}")
        else:
            logger.info(f"Video saved locally at {final_video_path}. Add client_secret.json to enable auto-upload.")

        # ---------------------------------------------------------
        # STEP 5B: Instagram Reels Publishing (Optional, Auto-Detected)
        # ---------------------------------------------------------
        logger.info(">>> STEP 5B: Checking Instagram Reels Publishing...")
        ig_url = upload_reel_to_instagram(
            video_path=final_video_path,
            title=script_data["title"],
            description=f"{script_data.get('hook', '')}\n\n{script_data.get('body', '')}\n\n{script_data.get('cta', '')}",
            tags=script_data.get("tags", ["Shorts", "Tech", "AI"]),
            comment_text=script_data.get("cta")
        )
        if ig_url:
            logger.info(f"MISSION ACCOMPLISHED! Instagram Reel Live: {ig_url}")
    else:
        logger.info("DRY RUN MODE: Video generated and verified. YouTube and Instagram uploads skipped.")

    # Record story to history to prevent repeat uploads across daily drops
    mark_story_as_published(story)

    print("\n" + "="*72)
    print(f"  OUTPUT VIDEO: {os.path.abspath(final_video_path)}")
    print(f"  DURATION:     {voice_data['duration']}s")
    print(f"  FILE SIZE:    {file_size_mb:.2f} MB")
    print(f"  STATUS:       READY FOR BROADCAST")
    print("="*72 + "\n")
    return final_video_path


def run_long_pipeline(duration: int = 12, dry_run: bool = True, custom_topic: str = None):
    """
    Episodic 16:9 Landscape Long-Form Satire & Deep Dive Pipeline (1920x1080).
    5 Dynamic Chapters, Multi-Track Audio Scoring, Clickable YouTube Timestamps.
    """
    print_banner(mode="long")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # ---------------------------------------------------------
    # STEP 1: Deep-Dive Topic Selection & Mystery Sourcing
    # ---------------------------------------------------------
    logger.info(">>> STEP 1: Sourcing Mind-Bending Deep-Dive Mystery for 16:9 Episode...")
    from src.deep_dive_topics import get_deep_dive_topic, CURATED_MYSTERIES
    if custom_topic:
        matched = next((m for m in CURATED_MYSTERIES if custom_topic.lower() in m["title"].lower()), None)
        if matched:
            story = matched
        else:
            story = {
                "title": custom_topic,
                "category": "Science & Deep Technology",
                "core_paradox": f"The hidden engineering reality behind {custom_topic}.",
                "real_world_analogy": "An everyday physical metaphor that makes this complex system instantly intuitive.",
                "catastrophe_case_study": f"The critical breaking point of {custom_topic} when pushed to its limits.",
                "paradigm_shift": f"How {custom_topic} fundamentally alters our understanding of technology.",
                "url": "https://en.wikipedia.org",
                "source": "Deep Dive Inquiry"
            }
    else:
        from src.news_fetcher import load_published_history
        history = load_published_history()
        published_titles = [h.get("title", "") for h in history]
        story = get_deep_dive_topic(previously_published=published_titles)

    logger.info(f"Mind-Bending Topic: [{story.get('category', 'Engineering')}] {story.get('title')}")

    # ---------------------------------------------------------
    # STEP 2: 4-Act High-IQ Explainer Script Generation
    # ---------------------------------------------------------
    logger.info(f">>> STEP 2: Generating {duration}-Minute 4-Act Explainer Script via Gemini...")
    script_data = generate_long_form_script(story, duration_minutes=duration)
    logger.info(f"Episode Title: {script_data['title']}")
    logger.info(f"Total Acts: {len(script_data.get('chapters', []))}")

    # ---------------------------------------------------------
    # STEP 3: Studio Neural Voice Synthesis
    # ---------------------------------------------------------
    logger.info(">>> STEP 3: Synthesizing Full Narration Audio via edge-tts...")
    audio_temp_path = f"temp/long_speech_{timestamp}.mp3"
    voice_data = generate_voiceover(
        text=script_data["full_script"],
        output_path=audio_temp_path
    )
    logger.info(f"Audio Synthesized: {voice_data['duration']:.1f}s | Words: {len(voice_data['word_timings'])}")

    # ---------------------------------------------------------
    # STEP 4: 1920x1080 Landscape Video Compositing
    # ---------------------------------------------------------
    logger.info(">>> STEP 4: Compositing 16:9 Landscape Video (Mind-Bending Visual Explainer)...")
    output_filename = f"output/Episode_{timestamp}.mp4"
    final_video_path, chapters_meta = build_long_video(
        script_data=script_data,
        voice_data=voice_data,
        output_path=output_filename,
        width=1920,
        height=1080
    )

    file_size_mb = os.path.getsize(final_video_path) / (1024 * 1024)
    logger.info(f"Long-Form Render Complete! Path: {final_video_path} ({file_size_mb:.2f} MB)")

    # ---------------------------------------------------------
    # STEP 4B: Automated High-CTR Thumbnail Generation (1280x720)
    # ---------------------------------------------------------
    logger.info(">>> STEP 4B: Generating 1280x720 High-CTR Thumbnail via Remotion...")
    from src.thumbnail_generator import generate_episode_thumbnail
    thumbnail_filename = f"output/Thumbnail_{timestamp}.jpg"
    final_thumbnail_path = generate_episode_thumbnail(story, thumbnail_filename)
    if final_thumbnail_path and os.path.exists(final_thumbnail_path):
        thumb_size_kb = os.path.getsize(final_thumbnail_path) / 1024
        logger.info(f"High-CTR Thumbnail Ready: {final_thumbnail_path} ({thumb_size_kb:.1f} KB)")
    else:
        final_thumbnail_path = None
        logger.warning("Could not generate custom thumbnail; YouTube default will be used.")

    # ---------------------------------------------------------
    # STEP 5: YouTube Long Video Publishing with Timestamps & Thumbnail
    # ---------------------------------------------------------
    if not dry_run:
        logger.info(">>> STEP 5: Publishing 16:9 Episode to YouTube with Clickable Chapters & Thumbnail...")
        publish_mode = os.getenv("PUBLISH_MODE", "PUBLIC")
        video_url = upload_long_video_to_youtube(
            video_path=final_video_path,
            title=script_data["title"],
            description=script_data.get("summary", script_data["title"]),
            chapters=chapters_meta,
            tags=script_data.get("tags", ["TechNews", "Coding", "SoftwareEngineering"]),
            privacy_status=publish_mode,
            comment_text=script_data.get("cta_question"),
            thumbnail_path=final_thumbnail_path
        )
        if video_url:
            logger.info(f"BROADCAST LIVE ON YOUTUBE: {video_url}")
        else:
            logger.info(f"Video saved locally at {final_video_path}.")
    else:
        logger.info("DRY RUN MODE: Episode generated locally. YouTube upload skipped.")

    mark_story_as_published(story)

    print("\n" + "="*72)
    print(f"  OUTPUT EPISODE:   {os.path.abspath(final_video_path)}")
    if final_thumbnail_path:
        print(f"  OUTPUT THUMBNAIL: {os.path.abspath(final_thumbnail_path)}")
    print(f"  RESOLUTION:       1920x1080 (16:9 Landscape)")
    print(f"  DURATION:         {voice_data['duration']:.1f}s")
    print(f"  FILE SIZE:        {file_size_mb:.2f} MB")
    print(f"  CHAPTERS:         {len(chapters_meta)} Timestamps Created")
    print("="*72 + "\n")
    return final_video_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Tech Video Pipeline (Shorts & Long Shows)")
    parser.add_argument("--mode", choices=["short", "long"], default="short", help="Video mode: 'short' (9:16 vertical) or 'long' (16:9 horizontal)")
    parser.add_argument("--duration", type=int, default=12, help="Target duration in minutes for long mode (default: 12)")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run generation without uploading to YouTube")
    parser.add_argument("--publish", action="store_true", default=False, help="Run generation and auto-publish to YouTube")
    parser.add_argument("--topic", type=str, default=None, help="Custom tech topic or headline override")
    
    args = parser.parse_args()
    
    # Default to dry-run if publish flag is not explicitly passed
    is_dry_run = not args.publish

    if args.mode == "long":
        run_long_pipeline(duration=args.duration, dry_run=is_dry_run, custom_topic=args.topic)
    else:
        run_pipeline(dry_run=is_dry_run, custom_topic=args.topic)
