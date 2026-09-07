"""
iDastawez Topic Engine CLI Runner
Execute with: python -m dastawez.topic_engine
"""

import sys
from dastawez.topic_engine import discover_daily_top_topic, get_ranked_topics_overview

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

print("\n" + "=" * 70)
print("🇮🇳 iDastawez Multi-Feed Topic Discovery Engine")
print("Priority: SarkariResult (#1) -> OnlineUpdateSTM (#2) -> Ministries -> SSC/UPSC -> Trends -> YouTube")
print("=" * 70)

overview = get_ranked_topics_overview(limit=10, filter_covered=True)
print("\nTop 10 Live Topics Discovered & Scored:")
for idx, item in enumerate(overview):
    print(f"{idx+1}. [{item['score']} pts] ({item['source']}) {item['title'][:65]}...")
    print(f"    Domain: {item.get('official_domain')} | Category: {item.get('category')}")

print("\n" + "-" * 70)
selected = discover_daily_top_topic(filter_covered=True)
print(f"🎯 WINNING TOPIC: {selected['scheme_name_hi']}")
print(f"   Authority: {selected['ministry']}")
print(f"   Portal: https://{selected['official_portal_domain']}")
print(f"   Circular Ref: {selected['notification_ref']}")
print(f"   Benefit / Detail: {selected['benefit_amount']}")
print(f"   Steps Count: {len(selected['application_steps'])}")
print("=" * 70 + "\n")
