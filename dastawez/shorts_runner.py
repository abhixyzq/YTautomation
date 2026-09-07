"""
iDastawez - Daily 9:16 Shorts Pipeline Orchestrator
Automates 35-45s vertical YouTube Shorts for @iDastawez:
1. Multi-Feed Real-Time Topic Discovery (SarkariResult + OnlineUpdateSTM)
2. Viral 4-beat Hindi Shorts Script (Gemini 1.5 Flash + verified fallback)
3. Studio Neural Hindi Speech (hi-IN-MadhurNeural with word timestamps)
4. 1080x1920 (9:16) Cinematic Compositor with B-roll, badges, and bouncing captions
5. YouTube Data API v3 Auto-Publishing isolated to 'token_dastawez.json'
6. Anti-Duplication History Engine logging
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dastawez.topics import VERIFIED_GOVT_SCHEMES
from dastawez.latest_tracker import enrich_and_prioritize_schemes
from dastawez.shorts_script_generator import generate_shorts_script
from dastawez.voice_generator import generate_shorts_voiceover
from dastawez.shorts_compositor import build_dastawez_shorts_video
from dastawez.history_tracker import record_topic_published, is_topic_covered

import shutil
import subprocess

logger = logging.getLogger("dastawez.shorts_runner")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[iDastawez Shorts Engine] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


def build_daily_dastawez_short(
    target_scheme_id: Optional[str] = None,
    output_base_dir: str = "./output/dastawez_episodes",
    render_video: bool = True,
    auto_upload: bool = False,
    privacy_status: str = "public",
    force: bool = False,
    engine: str = "remotion"
) -> Dict[str, Any]:
    """
    Executes the end-to-end daily Shorts pipeline for @iDastawez.
    """
    print("\n" + "="*72)
    print("🇮🇳 iDastawez - 9:16 CINEMATIC VIRAL SHORTS PIPELINE STARTING")
    print("="*72)

    # 1. Topic Selection
    if target_scheme_id:
        from dastawez.topic_engine import resolve_target_scheme
        selected_scheme = resolve_target_scheme(target_scheme_id, force=force)
    else:
        from dastawez.topic_engine import discover_daily_top_topic
        selected_scheme = discover_daily_top_topic(filter_covered=not force)

    scheme_id = selected_scheme["id"]
    today_str = datetime.now().strftime("%Y%m%d")
    episode_dir = os.path.abspath(os.path.join(output_base_dir, f"{today_str}_{scheme_id}_short"))
    os.makedirs(episode_dir, exist_ok=True)

    print(f"\n[Step 1] Selected Top Topic for Short: {selected_scheme.get('scheme_name_hi')}")
    print(f"         Priority Score: {selected_scheme.get('priority_score')}")
    print(f"         Urgency Badge:  {selected_scheme.get('urgency_badge')}")

    # 2. Viral Hindi Shorts Script Generation
    print("\n[Step 2] Generating 35-45s High-Retention Hindi Script...")
    script_data = generate_shorts_script(selected_scheme)
    script_data["scheme"] = selected_scheme
    script_path = os.path.join(episode_dir, "shorts_script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)

    print(f"         ✓ Title:       {script_data['title']}")
    print(f"         ✓ Hook:        {script_data.get('hook', '')}")
    print(f"         ✓ Full Script: {script_data['full_script']}")

    # 3. Studio Neural Voiceover with Word Timings
    print("\n[Step 3] Synthesizing Neural Hindi Voiceover via edge-tts...")
    audio_path = os.path.join(episode_dir, "shorts_audio.mp3")
    voice_data = generate_shorts_voiceover(
        text=script_data["full_script"],
        output_path=audio_path,
        rate="+3%"
    )
    print(f"         ✓ Voiceover Ready: {voice_data['duration']}s | Spoken Words: {len(voice_data['word_timings'])}")

    # 3.5 Prepare Remotion Props & Sync Audio to public/
    public_dir = os.path.abspath("public")
    public_audio_dir = os.path.join(public_dir, "dastawez_audio")
    os.makedirs(public_audio_dir, exist_ok=True)

    public_audio_filename = f"{today_str}_{scheme_id}_short.mp3"
    public_audio_dest = os.path.join(public_audio_dir, public_audio_filename)
    try:
        shutil.copy2(audio_path, public_audio_dest)
        rel_audio_path = f"dastawez_audio/{public_audio_filename}"
    except Exception as e:
        logger.warning(f"Could not copy audio to public dir: {e}")
        rel_audio_path = audio_path

    # Format badge colors for Remotion CSS
    bg_col = script_data.get("badge_bg_color", [220, 38, 38, 235])
    border_col = script_data.get("badge_border_color", [254, 202, 202])
    if isinstance(bg_col, (list, tuple)):
        badge_bg_str = f"rgba({bg_col[0]}, {bg_col[1]}, {bg_col[2]}, {round(bg_col[3]/255, 2) if len(bg_col) > 3 else 0.92})"
    else:
        badge_bg_str = str(bg_col)

    if isinstance(border_col, (list, tuple)):
        badge_border_str = f"rgba({border_col[0]}, {border_col[1]}, {border_col[2]}, 0.85)"
    else:
        badge_border_str = str(border_col)

    portal_domain = script_data.get("portal_domain", "india.gov.in")
    ministry = script_data.get("ministry", "भारत सरकार")

    official_image_path = None
    broll_video_path = None
    try:
        from dastawez.media_fetcher import get_topic_visual_bundle
        media_bundle = get_topic_visual_bundle(selected_scheme)
        if media_bundle.get("official_image"):
            official_image_path = media_bundle["official_image"].get("public_path")
        if media_bundle.get("broll_video"):
            broll_video_path = media_bundle["broll_video"].get("public_path")
    except Exception as e:
        logger.debug(f"Media fetch warning: {e}")

    remotion_props = {
        "title": script_data["title"],
        "badge_text": script_data.get("badge_text", "● SARKARI ALERT // OFFICIAL UPDATE"),
        "badge_bg_color": badge_bg_str,
        "badge_border_color": badge_border_str,
        "headline": script_data.get("headline", selected_scheme.get("scheme_name_hi")),
        "portal_domain": portal_domain,
        "ministry": ministry,
        "audio_path": rel_audio_path,
        "duration_seconds": voice_data.get("duration", 40),
        "phrases": voice_data.get("phrases", []),
        "official_image_path": official_image_path,
        "broll_video_path": broll_video_path
    }
    remotion_props_path = os.path.join(episode_dir, "remotion_shorts_props.json")
    with open(remotion_props_path, "w", encoding="utf-8") as f:
        json.dump(remotion_props, f, ensure_ascii=False, indent=2)

    # 4. 1080x1920 (9:16) Video Composition
    video_output_path = os.path.join(episode_dir, "final_short_1080p.mp4")
    if render_video:
        print(f"\n[Step 4] Compositing 1080x1920 Vertical Short ({engine} engine)...")
        if engine == "remotion":
            clean_props = remotion_props_path.replace("\\", "/")
            render_cmd = f'npx remotion render remotion/index.ts DastawezShorts "{video_output_path}" --props="{clean_props}" --public-dir=public --concurrency=2'
            try:
                print("         Executing Remotion 9:16 render...")
                subprocess.run(render_cmd, check=True, shell=True)
                if not os.path.exists(video_output_path) or os.path.getsize(video_output_path) < 1000:
                    raise RuntimeError("Remotion render did not create valid MP4")
                print(f"         ✓ Remotion Short rendered: {video_output_path}")
            except Exception as e:
                logger.warning(f"Remotion render error: {e}. Falling back to MoviePy compositor...")
                build_dastawez_shorts_video(
                    script_data=script_data,
                    voice_data=voice_data,
                    output_path=video_output_path
                )
        else:
            build_dastawez_shorts_video(
                script_data=script_data,
                voice_data=voice_data,
                output_path=video_output_path
            )
    else:
        print("\n[Step 4] (DRY-RUN MODE) Video render skipped. Script & Audio generated successfully.")

    # 5. YouTube Upload & Metadata Generation
    yt_url = None
    portal_domain = script_data.get("portal_domain", "india.gov.in")
    ministry = script_data.get("ministry", "भारत सरकार")
    description = (
        f"🇮🇳 {script_data['title']}\n\n"
        f"📌 आधिकारिक सरकारी पोर्टल (Official Portal):\n"
        f"👉 https://{portal_domain}\n\n"
        f"🏛️ विभाग: {ministry}\n\n"
        f"इस वीडियो में:\n"
        f"1️⃣ {script_data.get('crisis', '')}\n"
        f"2️⃣ {script_data.get('action', '')}\n\n"
        f"🔔 भारत सरकार की हर ताज़ा योजना, भर्ती और e-KYC की 100% सटीक जानकारी के लिए @iDastawez को अभी SUBSCRIBE करें!\n\n"
        f"#Shorts #iDastawez #SarkariYojana #Yojana2026 #GovernmentSchemes #eKYC"
    )

    first_comment = (
        f"📌 आधिकारिक पोर्टल लिंक: https://{portal_domain}\n"
        f"योजना से जुड़ी हर सही जानकारी के लिए @iDastawez को सब्सक्राइब करें!"
    )

    if auto_upload and render_video and os.path.exists(video_output_path):
        print("\n[Step 5] Auto-Uploading Short to @iDastawez via YouTube Data API...")
        from dastawez.youtube_uploader import upload_dastawez_short
        yt_url = upload_dastawez_short(
            video_path=video_output_path,
            title=script_data["title"],
            description=description,
            tags=script_data.get("tags", []),
            privacy_status=privacy_status,
            first_comment=first_comment
        )
        if yt_url:
            print(f"         🎉 SHORT LIVE ON YOUTUBE: {yt_url}")
    elif auto_upload:
        print("\n[Step 5] Upload requested but video file does not exist. (Dry run or render error).")
    else:
        print("\n[Step 5] Upload skipped. Use --upload to publish directly to @iDastawez.")

    # 6. Anti-Duplication History Engine
    record_topic_published(
        scheme_id=scheme_id,
        scheme_name=selected_scheme.get("scheme_name_hi", script_data["title"]),
        episode_folder=os.path.basename(episode_dir),
        youtube_id=yt_url.split("/")[-1] if yt_url else None,
        metadata={
            "format": "shorts_9x16",
            "title": script_data["title"],
            "portal_url": f"https://{portal_domain}",
            "ministry": ministry
        }
    )

    print("\n" + "="*72)
    print("✅ iDastawez SHORTS PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"📁 Artifacts Saved In: {episode_dir}")
    if os.path.exists(video_output_path):
        print(f"🎬 Video File:        {video_output_path}")
    print("="*72 + "\n")

    return {
        "scheme_id": scheme_id,
        "episode_dir": episode_dir,
        "video_path": video_output_path if os.path.exists(video_output_path) else None,
        "audio_path": audio_path,
        "youtube_url": yt_url
    }
