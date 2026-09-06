"""
iDastawez - Master Video Compositor & Pipeline Orchestrator
Builds end-to-end authentic, verified Hindi long videos (3.5 - 4.5 minutes)
for @iDastawez (Indian Government Schemes, Yojanas & Citizen Services).
"""

import os
import sys
import json
import logging
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional

from dastawez.topics import VERIFIED_GOVT_SCHEMES
from dastawez.latest_tracker import enrich_and_prioritize_schemes
from dastawez.script_generator import generate_dastawez_script
from dastawez.voice_generator import generate_scene_voiceovers

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def build_daily_dastawez_video(
    target_scheme_id: Optional[str] = None,
    output_base_dir: str = "./output/dastawez_episodes",
    render_video: bool = True,
    render_thumbnail: bool = True,
    auto_upload: bool = False,
    privacy_status: str = "public",
) -> Dict[str, Any]:
    """
    Executes the complete daily episode pipeline:
    1. Scan & Prioritize latest verified official updates (Zero Fake News)
    2. Generate structured 5-Act Hindi explainer script
    3. Generate natural neural Hindi speech (hi-IN-MadhurNeural)
    4. Render Remotion 1080p landscape video & 1280x720 thumbnail
    5. Generate complete YouTube SEO metadata
    """
    print("\n" + "="*70)
    print("🇮🇳 iDastawez - Daily Government Explainer Pipeline Starting")
    print("="*70)

    # 1. Topic Selection & Real-Time Prioritization
    if target_scheme_id:
        matching = [s for s in VERIFIED_GOVT_SCHEMES if s["id"] == target_scheme_id]
        if not matching:
            raise ValueError(f"Scheme ID {target_scheme_id} not found in verified registry.")
        ranked_schemes = enrich_and_prioritize_schemes(matching)
        selected_scheme = ranked_schemes[0]
    else:
        # Automatic top-priority selection based on live news & active e-KYC deadlines
        ranked_schemes = enrich_and_prioritize_schemes(VERIFIED_GOVT_SCHEMES)
        selected_scheme = ranked_schemes[0]

    scheme_id = selected_scheme["id"]
    today_str = datetime.now().strftime("%Y%m%d")
    episode_dir = os.path.abspath(os.path.join(output_base_dir, f"{today_str}_{scheme_id}"))
    os.makedirs(episode_dir, exist_ok=True)

    print(f"\n[Step 1] Selected Top Priority Topic: {selected_scheme['scheme_name_hi']}")
    print(f"         Priority Score: {selected_scheme.get('priority_score')}")
    print(f"         Urgency Badge: {selected_scheme.get('urgency_badge')}")
    if selected_scheme.get("latest_news_headline"):
        print(f"         Live Report: {selected_scheme['latest_news_headline']}")

    # 2. Script Generation
    print("\n[Step 2] Generating 5-Act Authentic Hindi Script...")
    script_data = generate_dastawez_script(selected_scheme)
    script_path = os.path.join(episode_dir, "script_and_scenes.json")
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, ensure_ascii=False, indent=2)

    # 3. Neural Hindi Voice Generation (Edge-TTS hi-IN-MadhurNeural)
    print("\n[Step 3] Synthesizing Studio Neural Hindi Audio...")
    voice_dir = os.path.join(episode_dir, "audio")
    voice_data = generate_scene_voiceovers(script_data, voice_dir, voice="hi-IN-MadhurNeural")
    total_duration_sec = voice_data.get("total_audio_duration_seconds", 240)
    print(f"         Total Audio Duration: {round(total_duration_sec, 1)} seconds ({round(total_duration_sec/60, 2)} minutes)")

    # Prepare Remotion props file
    remotion_props = {
      "title": script_data["title"],
      "scheme_id": scheme_id,
      "category": selected_scheme.get("category", "सरकारी योजनाएं एवं नागरिक सेवाएं"),
      "scenes": voice_data["scenes"]
    }
    remotion_props_path = os.path.join(episode_dir, "remotion_props.json")
    with open(remotion_props_path, "w", encoding="utf-8") as f:
        json.dump(remotion_props, f, ensure_ascii=False, indent=2)

    # 4. Thumbnail Generation (1280x720)
    thumb_output_path = os.path.join(episode_dir, "thumbnail.png")
    if render_thumbnail:
        print("\n[Step 4] Rendering High-CTR 1280x720 Hindi Thumbnail...")
        thumb_props = {
            "scheme_name": selected_scheme["scheme_name_hi"],
            "big_benefit": selected_scheme["benefit_amount"],
            "urgency_badge": selected_scheme.get("urgency_badge", "100% आधिकारिक नियम"),
            "portal_name": selected_scheme["portal_url"].replace("https://", "").replace("http://", "").split("/")[0],
            "helpline": selected_scheme["helpline"],
            "rule_change_badge": "100% सरकारी फैसला"
        }
        thumb_props_path = os.path.join(episode_dir, "thumb_props.json")
        with open(thumb_props_path, "w", encoding="utf-8") as f:
            json.dump(thumb_props, f, ensure_ascii=False, indent=2)

        thumb_cmd = [
            "npx", "remotion", "still", "DastawezThumbnail",
            thumb_output_path,
            "--props", thumb_props_path.replace("\\", "/")
        ]
        try:
            subprocess.run(thumb_cmd, check=True, shell=True)
            print(f"         ✓ Thumbnail saved: {thumb_output_path}")
        except Exception as e:
            print(f"         [Thumbnail Warning] Render failed: {e}")

    # 5. Video Composition & Rendering (1920x1080 Landscape)
    video_output_path = os.path.join(episode_dir, "final_explainer_1080p.mp4")
    if render_video:
        print("\n[Step 5] Rendering Full 1080p Hindi Video with Remotion...")
        video_cmd = [
            "npx", "remotion", "render", "DastawezLandscape",
            video_output_path,
            "--props", remotion_props_path.replace("\\", "/"),
            "--concurrency", "2"
        ]
        try:
            print(f"         Executing Remotion render ({round(total_duration_sec, 1)}s)...")
            subprocess.run(video_cmd, check=True, shell=True)
            print(f"         ✓ Video successfully rendered: {video_output_path}")
        except Exception as e:
            print(f"         [Video Render Warning] Render failed: {e}")

    # 6. Save Complete YouTube Metadata Bundle
    yt_meta_path = os.path.join(episode_dir, "youtube_upload_metadata.json")
    yt_bundle = {
        "channel": "@iDastawez",
        "title": script_data["title"],
        "description": script_data["description"],
        "tags": selected_scheme.get("seo_keywords", []) + ["iDastawez", "SarkariYojana", "GovernmentSchemes"],
        "category_id": "27",  # Education / Citizen Info
        "privacy_status": "public",
        "thumbnail_path": thumb_output_path,
        "video_path": video_output_path,
        "created_at": datetime.now().isoformat(),
        "verified_scheme": selected_scheme
    }
    with open(yt_meta_path, "w", encoding="utf-8") as f:
        json.dump(yt_bundle, f, ensure_ascii=False, indent=2)

    # 7. Optional Automatic Upload to @iDastawez
    if auto_upload and os.path.exists(video_output_path):
        from dastawez.youtube_uploader import upload_dastawez_long_video
        print("\n[Step 6] Uploading directly to @iDastawez on YouTube...")
        first_comment = (
            f"📌 आधिकारिक पोर्टल: {selected_scheme['portal_url']}\n"
            f"📞 राष्ट्रीय हेल्पलाइन: {selected_scheme['helpline']}\n"
            f"⚠️ किसी भी दलाल को शुल्क न दें, यह योजना 100% निःशुल्क है।"
        )
        url = upload_dastawez_long_video(
            video_path=video_output_path,
            title=script_data["title"],
            description=script_data["description"],
            tags=yt_bundle["tags"],
            thumbnail_path=thumb_output_path if os.path.exists(thumb_output_path) else None,
            privacy_status=privacy_status,
            first_comment=first_comment
        )
        if url:
            yt_bundle["uploaded_url"] = url

    print("\n" + "="*70)
    print("🎉 iDastawez Episode Pipeline Completed Successfully!")
    print(f"📁 Artifacts Directory: {episode_dir}")
    print("="*70)
    return yt_bundle


if __name__ == "__main__":
    # Test dry run: prioritize and generate all scripts, voiceovers, metadata, and thumbnail
    build_daily_dastawez_video(render_video=False, render_thumbnail=True)
