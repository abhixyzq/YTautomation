"""
Automated YouTube Shorts Publisher
Uses YouTube Data API v3 (Google Cloud OAuth 2.0).
Free quota: 10,000 units/day (Each upload is ~1,600 units = 5-6 uploads daily).
Supports persistent token caching so browser authentication is only needed once.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

# Scope required for uploading YouTube videos
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.json"
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")


def get_youtube_service():
    """Authenticate and return an authorized YouTube Data API service instance."""
    creds = None
    
    # 1. Check if token.json already exists (saved session)
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            logger.warning(f"Failed to load cached token: {e}")

    # 2. If no valid credentials, refresh or initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired YouTube OAuth token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                logger.error(
                    f"'{CLIENT_SECRET_FILE}' not found! "
                    "To enable auto-uploading to YouTube:\n"
                    "1. Visit https://console.cloud.google.com/\n"
                    "2. Enable 'YouTube Data API v3'\n"
                    "3. Go to Credentials -> Create Credentials -> OAuth Client ID (Desktop App)\n"
                    "4. Download the JSON and save as 'client_secret.json' in this folder."
                )
                return None
            
            logger.info("Initiating browser OAuth authentication for YouTube...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future unattended runs
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
            logger.info("Saved YouTube OAuth credentials to token.json.")

    return build("youtube", "v3", credentials=creds)


def post_first_comment(youtube, video_id: str, comment_text: str) -> bool:
    """
    Attempt to post the first engagement discussion comment via YouTube API.
    Handles scopes gracefully if token doesn't have youtube.force-ssl.
    """
    if not comment_text:
        return False
    try:
        body = {
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
        logger.info(f"Posting engagement question on video {video_id}...")
        youtube.commentThreads().insert(part="snippet", body=body).execute()
        logger.info("Successfully posted first engagement comment!")
        return True
    except Exception as e:
        logger.info(
            f"Comment note: {e}. (Engagement question is placed prominently at top of video description)."
        )
        return False


def upload_short_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy_status: str = "public",
    comment_text: str = None
) -> Optional[str]:
    """
    Upload a video file as a YouTube Short and post the initial engagement question.
    Returns the uploaded YouTube Video URL.
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    youtube = get_youtube_service()
    if not youtube:
        logger.warning(f"Skipping upload. Video rendered and ready locally at: {video_path}")
        return None

    # 1. High-CTR Title with mandatory #Shorts tag
    clean_title = title.replace("#Shorts", "").replace("#shorts", "").strip()
    final_title = f"{clean_title[:75]} #Shorts #Tech #AI"

    # 2. Comprehensive High-Volume Tags Matrix
    default_push_tags = [
        "Shorts", "Tech", "AI", "Artificial Intelligence", "TechNews",
        "Coding", "Software Engineering", "Web Development", "Developers",
        "Machine Learning", "Programming", "Tech Trends 2026"
    ]
    if tags:
        combined_tags = list(dict.fromkeys(tags + default_push_tags))[:25]
    else:
        combined_tags = default_push_tags

    pinned_prompt = comment_text or "What's your perspective on this? Drop your take below! 👇"

    # 3. Rich SEO Description with Call-To-Action & Pinned Question for Algorithm Boost
    seo_description = f"""💬 QUESTION OF THE DAY:
{pinned_prompt}
Drop your perspective in the comments below! 👇

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{clean_title}

{description.strip()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔔 Subscribe for daily cutting-edge tech and AI insights.

#Shorts #Tech #AI #ArtificialIntelligence #Coding #SoftwareEngineering #TechNews #WebDevelopment #Programming #TechTrends
"""

    body = {
        "snippet": {
            "title": final_title[:100],
            "description": seo_description.strip(),
            "tags": combined_tags,
            "categoryId": "28"  # 28 = Science & Technology
        },
        "status": {
            "privacyStatus": privacy_status.lower(),  # "public", "private", "unlisted"
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    logger.info(f"Uploading '{title}' to YouTube as [{privacy_status.upper()}]...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logger.info(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    logger.info(f"SUCCESS! Video live at: {video_url}")

    # 4. Attempt to post first engagement comment
    first_comment = f"👇 QUESTION OF THE DAY:\n{pinned_prompt}"
    post_first_comment(youtube, video_id, first_comment)

    return video_url


def upload_long_video_to_youtube(
    video_path: str,
    title: str,
    description: str,
    chapters: list = None,
    tags: list = None,
    privacy_status: str = "public",
    comment_text: str = None,
    thumbnail_path: str = None
) -> Optional[str]:
    """
    Upload a 16:9 horizontal long video to YouTube with clickable chapters / timestamps in description
    and high-CTR custom thumbnail.
    Returns the uploaded YouTube Video URL.
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    youtube = get_youtube_service()
    if not youtube:
        logger.warning(f"Skipping upload. Video rendered and ready locally at: {video_path}")
        return None

    # 1. Clean Title (No #Shorts tag for long videos)
    clean_title = title.replace("#Shorts", "").replace("#shorts", "").strip()
    final_title = f"{clean_title[:95]}"

    # 2. Comprehensive High-Volume Tags Matrix
    default_push_tags = [
        "Software Engineering", "Computer Science", "System Architecture",
        "Science Explainer", "Engineering Deep Dive", "Veritasium Style",
        "Deep Dive Documentary", "Physics", "Cybersecurity", "Tech 2026"
    ]
    if tags:
        combined_tags = list(dict.fromkeys(tags + default_push_tags))[:25]
    else:
        combined_tags = default_push_tags

    pinned_prompt = comment_text or "What was the worst outage you ever witnessed in production? Drop your take below! 👇"

    # 3. Format Clickable YouTube Chapter Markers
    chapters_text = ""
    if chapters:
        chapter_lines = []
        for ch in chapters:
            timestamp = ch.get("timestamp", "00:00")
            ch_title = ch.get("title", f"Chapter {ch.get('chapter_id', '')}")
            chapter_lines.append(f"{timestamp} - {ch_title}")
        chapters_text = "\n📌 CHAPTERS & TIMESTAMPS:\n" + "\n".join(chapter_lines) + "\n"

    # 4. Rich SEO Description
    seo_description = f"""💬 QUESTION OF THE DAY:
{pinned_prompt}
Drop your perspective in the comments below! 👇

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{clean_title}

{description.strip()}
{chapters_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔔 Subscribe for weekly deep dives, tech investigations, and developer satire.

#TechNews #SoftwareEngineering #SiliconValley #Coding #SystemArchitecture #AI #CloudComputing #Programming
"""

    body = {
        "snippet": {
            "title": final_title[:100],
            "description": seo_description.strip(),
            "tags": combined_tags,
            "categoryId": "28"  # 28 = Science & Technology
        },
        "status": {
            "privacyStatus": privacy_status.lower(),  # "public", "private", "unlisted"
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=-1,
        resumable=True,
        mimetype="video/mp4"
    )

    logger.info(f"Uploading '{final_title}' (Long Video) to YouTube as [{privacy_status.upper()}]...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            logger.info(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    logger.info(f"SUCCESS! Long-form video live at: {video_url}")

    # 5. Set Custom High-CTR Thumbnail
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            logger.info(f"Setting custom 1280x720 thumbnail for video {video_id}...")
            thumb_media = MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=thumb_media
            ).execute()
            logger.info("Custom high-CTR thumbnail uploaded successfully!")
        except Exception as e:
            logger.warning(
                f"Could not set custom thumbnail (check channel phone verification on YouTube Studio): {e}"
            )

    # 6. Post first pinned engagement comment
    first_comment = f"👇 QUESTION OF THE DAY:\n{pinned_prompt}"
    post_first_comment(youtube, video_id, first_comment)

    return video_url


if __name__ == "__main__":
    print("YouTube uploader module loaded successfully.")

