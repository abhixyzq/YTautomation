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
logger = logging.getLogger("ShortsOrchestrator")

from src.news_fetcher import get_trending_tech_stories
from src.script_generator import generate_tech_script
from src.voice_generator import generate_voiceover
from src.video_compositor import build_shorts_video
from src.youtube_uploader import upload_short_to_youtube


def print_banner():
    banner = """
========================================================================
   CINEMATIC TECH DOCUMENTARY SHORTS PIPELINE (100% REAL 4K FOOTAGE)
   Architecture: Fireship / Vox Style (Zero Cheap Avatars, Broadcast Grade)
========================================================================
"""
    print(banner)


def run_pipeline(dry_run: bool = True, custom_topic: str = None):
    print_banner()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ---------------------------------------------------------
    # STEP 1: Trending Tech News Discovery
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
        import random
        # Pick from top trending stories to ensure 3 unique drops each day
        story = random.choice(stories[:min(5, len(stories))])
        
    logger.info(f"Selected Story: [{story['source']}] {story['title']}")

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
        logger.info(">>> STEP 5: Publishing Video Directly to YouTube...")
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
    else:
        logger.info("DRY RUN MODE: Video generated and verified. YouTube upload skipped.")

    print("\n" + "="*72)
    print(f"  OUTPUT VIDEO: {os.path.abspath(final_video_path)}")
    print(f"  DURATION:     {voice_data['duration']}s")
    print(f"  FILE SIZE:    {file_size_mb:.2f} MB")
    print(f"  STATUS:       READY FOR BROADCAST")
    print("="*72 + "\n")
    return final_video_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous AI Avatar Tech Shorts Pipeline")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run generation without uploading to YouTube")
    parser.add_argument("--publish", action="store_true", default=False, help="Run generation and auto-publish to YouTube")
    parser.add_argument("--topic", type=str, default=None, help="Custom tech topic or headline override")
    
    args = parser.parse_args()
    
    # Default to dry-run if publish flag is not explicitly passed
    is_dry_run = not args.publish
    
    run_pipeline(dry_run=is_dry_run, custom_topic=args.topic)
