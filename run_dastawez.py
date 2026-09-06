"""
iDastawez - Main CLI Runner for Daily Government Explainer Videos
Run:
  python run_dastawez.py --list                 # Show all schemes ranked by priority & live news
  python run_dastawez.py --dry-run              # Generate script, audio & thumbnail for today's #1 topic
  python run_dastawez.py --render               # Render full 1080p video for today's #1 topic
  python run_dastawez.py --scheme ayushman_senior_citizen_2026 --render  # Target specific scheme
"""

import sys
import argparse
from dastawez.topics import VERIFIED_GOVT_SCHEMES
from dastawez.latest_tracker import enrich_and_prioritize_schemes
from dastawez.compositor import build_daily_dastawez_video

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="iDastawez Daily Video Automation Engine")
    parser.add_argument("--scheme", "-s", type=str, default=None, help="Target specific scheme ID")
    parser.add_argument("--render", action="store_true", help="Render full 1080p MP4 video")
    parser.add_argument("--dry-run", action="store_true", help="Generate script, voiceover and thumbnail only")
    parser.add_argument("--list", "-l", action="store_true", help="List all schemes ranked by real-time priority")

    args = parser.parse_args()

    if args.list:
        print("\n" + "="*75)
        print("🇮🇳 iDastawez - CURRENT LIVE GOVERNMENT UPDATES & SCHEMES PRIORITY RANKING")
        print("="*75)
        ranked = enrich_and_prioritize_schemes(VERIFIED_GOVT_SCHEMES)
        for i, s in enumerate(ranked, 1):
            print(f"\n#{i} [Score: {s['priority_score']}] {s['scheme_name_hi']}")
            print(f"    ID: {s['id']}")
            print(f"    विभाग: {s['ministry']}")
            print(f"    पोर्टल: {s['portal_url']}")
            print(f"    स्थिति/बैज: {s.get('urgency_badge')}")
            if s.get("latest_news_headline"):
                print(f"    ताज़ा खबर: {s['latest_news_headline']}")
        print("\n" + "="*75)
        return

    # If neither --render nor --dry-run is passed, default to dry-run (safe mode)
    render_video = args.render and not args.dry_run

    build_daily_dastawez_video(
        target_scheme_id=args.scheme,
        render_video=render_video,
        render_thumbnail=True
    )


if __name__ == "__main__":
    main()
