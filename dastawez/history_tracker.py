"""
iDastawez - Episode History & Anti-Duplication Engine
Guarantees that topics are never repeated. Tracks all rendered & uploaded episodes.
"""

import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HISTORY_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "history.json")
)


def _ensure_history_dir():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)


def load_history() -> Dict[str, Any]:
    """Loads the history database. Returns empty struct if file doesn't exist."""
    _ensure_history_dir()
    if not os.path.exists(HISTORY_FILE):
        return {"version": 1, "published_episodes": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[History Engine Warning] Failed to read history: {e}")
        return {"version": 1, "published_episodes": []}


def save_history(data: Dict[str, Any]):
    """Saves updated history to disk atomically."""
    _ensure_history_dir()
    temp_file = HISTORY_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    os.rename(temp_file, HISTORY_FILE)


def normalize_title(title: str) -> str:
    """Normalizes Hindi/English text for robust duplicate comparison."""
    if not title:
        return ""
    # Remove dates, years, punctuation, and extra whitespace
    t = re.sub(r"\b202\d\b", "", title)
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def is_topic_covered(topic_id: str, topic_title: str = "", cooldown_days: int = 60) -> bool:
    """
    Checks if a topic or closely matching title was covered within cooldown_days.
    If cooldown_days <= 0, considers all recorded history permanently.
    """
    history = load_history()
    episodes = history.get("published_episodes", [])
    if not episodes:
        return False

    now = datetime.now(timezone.utc)
    norm_incoming_title = normalize_title(topic_title)

    for ep in episodes:
        # Match by ID
        matched_id = (ep.get("scheme_id") == topic_id or ep.get("id") == topic_id)
        
        # Match by normalized title similarity
        matched_title = False
        if norm_incoming_title:
            past_title = normalize_title(ep.get("scheme_name", ""))
            if norm_incoming_title in past_title or past_title in norm_incoming_title:
                matched_title = True

        if matched_id or matched_title:
            if cooldown_days <= 0:
                return True
            # Check cooldown duration
            pub_str = ep.get("published_at")
            if not pub_str:
                return True
            try:
                pub_dt = datetime.fromisoformat(pub_str)
                if pub_dt.tzinfo is None:
                    pub_dt = pub_dt.replace(tzinfo=timezone.utc)
                if (now - pub_dt).days < cooldown_days:
                    return True
            except Exception:
                return True

    return False


def record_topic_published(
    scheme_id: str,
    scheme_name: str,
    episode_folder: str,
    youtube_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Records a completed/published episode into history so it is never repeated.
    """
    history = load_history()
    episodes = history.setdefault("published_episodes", [])
    
    # Avoid duplicate entry in history file itself
    for ep in episodes:
        if ep.get("scheme_id") == scheme_id and ep.get("episode_folder") == episode_folder:
            return

    new_entry = {
        "scheme_id": scheme_id,
        "scheme_name": scheme_name,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "episode_folder": episode_folder,
        "youtube_id": youtube_id,
        "metadata": metadata or {}
    }
    episodes.append(new_entry)
    save_history(history)
    print(f"[History Engine] ✓ Topic permanently logged to anti-duplication registry: {scheme_name}")


def get_covered_topics() -> List[Dict[str, Any]]:
    """Returns all covered episodes with dates and IDs."""
    history = load_history()
    return history.get("published_episodes", [])
