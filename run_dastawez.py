"""
iDastawez - Main CLI Runner for Daily Government Explainer Videos
Run:
  python run_dastawez.py --trending             # Inspect live Sarkari Result trending updates & fresh status
  python run_dastawez.py --history              # View history of previously covered topics (no duplicates)
  python run_dastawez.py --list                 # Show all schemes ranked by priority & live news
  python run_dastawez.py --dry-run              # Generate script, audio & thumbnail for today's #1 topic
  python run_dastawez.py --render               # Render full 1080p video for today's #1 topic
  python run_dastawez.py --scheme <id> --render # Target specific scheme
  python run_dastawez.py --force                # Force render even if topic was covered previously
"""

import sys
import argparse
from dastawez.topics import VERIFIED_GOVT_SCHEMES
from dastawez.latest_tracker import enrich_and_prioritize_schemes
from dastawez.compositor import build_daily_dastawez_video
from dastawez.sarkari_scraper import fetch_all_sarkari_trends
from dastawez.history_tracker import get_covered_topics, is_topic_covered

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
    parser.add_argument("--trending", "-t", action="store_true", help="Inspect live Sarkari Result trending topics")
    parser.add_argument("--history", action="store_true", help="Show history of previously covered topics")
    parser.add_argument("--force", action="store_true", help="Allow rebuilding a topic even if previously covered")
    parser.add_argument("--connect-youtube", action="store_true", help="Authenticate and connect @iDastawez YouTube channel")
    parser.add_argument("--upload", action="store_true", help="Upload the rendered video directly to YouTube")
    parser.add_argument("--privacy", type=str, default="public", choices=["public", "unlisted", "private"], help="YouTube privacy status")

    args = parser.parse_args()

    if args.connect_youtube:
        from dastawez.youtube_uploader import verify_connected_channel
        print("\n[iDastawez] Verifying YouTube Connection for @iDastawez...")
        verify_connected_channel()
        return

    if args.history:
        print("\n" + "="*75)
        print("📜 iDastawez - PREVIOUSLY COVERED TOPICS (ANTI-DUPLICATION REGISTRY)")
        print("="*75)
        covered = get_covered_topics()
        if not covered:
            print("  (No topics logged in history yet. All topics are currently FRESH!)")
        else:
            for idx, item in enumerate(covered, 1):
                date_str = item.get("published_at", "")[:10]
                yt_link = f" (YouTube: {item['youtube_id']})" if item.get("youtube_id") else ""
                print(f"  #{idx} [{date_str}] {item.get('scheme_name', 'Unknown')}")
                print(f"       ID: {item.get('scheme_id')} | Folder: {item.get('episode_folder')}{yt_link}")
        print("="*75 + "\n")
        return

    if args.trending:
        print("\n" + "="*75)
        print("🇮🇳 SARKARI RESULT - LIVE TRENDING OVERVIEW & FRESHNESS STATUS")
        print("="*75)
        trends = fetch_all_sarkari_trends()
        for cat, items in trends.items():
            print(f"\n📂 [{cat.upper()}] ({len(items)} trending items)")
            for it in items[:6]:
                covered = is_topic_covered(it["title"], it["title"])
                status_tag = "⛔ [COVERED]" if covered else "✨ [FRESH]"
                urgent_tag = " 🔥 [URGENT/DEADLINE]" if it["is_urgent"] else ""
                print(f"  {status_tag} {it['title']}{urgent_tag}")
                print(f"       URL: {it['url']}")
        print("\n" + "="*75 + "\n")
        return

    if args.list:
        print("\n" + "="*75)
        print("🇮🇳 iDastawez - CURRENT LIVE GOVERNMENT UPDATES & SCHEMES PRIORITY RANKING")
        print("="*75)
        ranked = enrich_and_prioritize_schemes(VERIFIED_GOVT_SCHEMES, filter_covered=not args.force)
        for i, s in enumerate(ranked, 1):
            cov_status = "⛔ [ALREADY COVERED]" if s.get("is_covered") else "✨ [FRESH]"
            print(f"\n#{i} {cov_status} [Score: {s['priority_score']}] {s['scheme_name_hi']}")
            print(f"    ID: {s['id']}")
            print(f"    विभाग: {s['ministry']}")
            print(f"    पोर्टल: {s['portal_url']}")
            print(f"    स्थिति/बैज: {s.get('urgency_badge')}")
            if s.get("sarkari_trends"):
                print(f"    🔥 Sarkari Result Trending: {len(s['sarkari_trends'])} item(s) matched")
            if s.get("latest_news_headline"):
                print(f"    ताज़ा खबर: {s['latest_news_headline']}")
        print("\n" + "="*75)
        return

    # If --upload is requested, we must render the video
    render_video = args.render or args.upload
    if args.dry_run:
        render_video = False

    build_daily_dastawez_video(
        target_scheme_id=args.scheme,
        render_video=render_video,
        render_thumbnail=True,
        auto_upload=args.upload,
        privacy_status=args.privacy,
        force=args.force
    )


if __name__ == "__main__":
    main()
