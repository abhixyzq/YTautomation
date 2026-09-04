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


def upload_short_to_youtube(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    privacy_status: str = "public"
) -> Optional[str]:
    """
    Upload a video file as a YouTube Short.
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

    # 3. Rich SEO Description with Call-To-Action for Algorithm Boost
    seo_description = f"""{clean_title}

{description.strip()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 What's your take on this? Let us know in the comments below!
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
    return video_url


if __name__ == "__main__":
    print("YouTube uploader module loaded successfully.")
