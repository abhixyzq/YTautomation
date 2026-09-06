"""
iDastawez - Dedicated YouTube Uploader
Uses YouTube Data API v3 (Google Cloud OAuth 2.0).
Keeps @iDastawez credentials in 'token_dastawez.json' isolated from other channels.
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Full YouTube management and upload scope
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

TOKEN_FILE = "token_dastawez.json"
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")


def get_dastawez_youtube_service():
    """
    Authenticate and return an authorized YouTube Data API service instance for @iDastawez.
    Uses 'token_dastawez.json' so it never conflicts with tech channel credentials.
    """
    creds = None

    # 1. Check cached token for @iDastawez
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            logger.warning(f"Failed to load cached {TOKEN_FILE}: {e}")

    # 2. Refresh or trigger initial browser OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired YouTube OAuth token for @iDastawez...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CLIENT_SECRET_FILE):
                logger.error(
                    f"'{CLIENT_SECRET_FILE}' not found!\n"
                    "Make sure 'client_secret.json' is present in the workspace root."
                )
                return None

            print("\n" + "="*70)
            print("🔑 Connecting YouTube Account for @iDastawez...")
            print("Opening browser for 1-time Google Login.")
            print("IMPORTANT: Select your Google account and choose '@iDastawez' channel.")
            print("="*70 + "\n")

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future unattended runs
        with open(TOKEN_FILE, "w", encoding="utf-8") as token_out:
            token_out.write(creds.to_json())
            logger.info(f"Saved @iDastawez OAuth credentials to {TOKEN_FILE}.")

    service = build("youtube", "v3", credentials=creds)
    return service


def verify_connected_channel() -> Optional[Dict[str, Any]]:
    """
    Checks and displays details of the currently authorized YouTube channel.
    """
    service = get_dastawez_youtube_service()
    if not service:
        return None

    try:
        req = service.channels().list(part="snippet,statistics", mine=True)
        res = req.execute()
        items = res.get("items", [])
        if not items:
            logger.warning("No channel found for authenticated credentials.")
            return None

        channel = items[0]
        snippet = channel.get("snippet", {})
        title = snippet.get("title")
        custom_url = snippet.get("customUrl", "")
        ch_id = channel.get("id")
        
        print("\n" + "="*60)
        print("✅ YOUTUBE CHANNEL CONNECTED SUCCESSFULLY!")
        print(f"📺 Channel Name:   {title}")
        print(f"🔗 Handle / URL:   {custom_url or '@' + title}")
        print(f"🆔 Channel ID:     {ch_id}")
        print("="*60 + "\n")
        return {
            "channel_title": title,
            "custom_url": custom_url,
            "channel_id": ch_id
        }
    except Exception as e:
        logger.error(f"Failed to query channel details: {e}")
        return None


def upload_dastawez_long_video(
    video_path: str,
    title: str,
    description: str,
    tags: list = None,
    thumbnail_path: str = None,
    privacy_status: str = "public",
    first_comment: str = None
) -> Optional[str]:
    """
    Uploads a verified government explainer video to @iDastawez:
    - 1080p long video format
    - Custom 1280x720 thumbnail
    - Category 27 (Education / Citizen Information)
    - Pinned first comment with official helpline & portal
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    youtube = get_dastawez_youtube_service()
    if not youtube:
        logger.warning(f"Skipping upload. Video ready locally at: {video_path}")
        return None

    # Title cleanup (max 100 chars for YouTube)
    clean_title = title.strip()[:100]

    # Hindi & Scheme SEO tags
    default_dastawez_tags = [
        "iDastawez", "Sarkari Yojana 2026", "Government Schemes India",
        "eKYC Online", "Aadhaar Card", "Ration Card", "PM Kisan",
        "Ayushman Bharat", "Sarkari Form Apply", "Official Notification"
    ]
    if tags:
        combined_tags = list(dict.fromkeys(tags + default_dastawez_tags))[:30]
    else:
        combined_tags = default_dastawez_tags

    body = {
        "snippet": {
            "title": clean_title,
            "description": description.strip(),
            "tags": combined_tags,
            "categoryId": "27",  # 27 = Education / Public Information
            "defaultLanguage": "hi",
            "defaultAudioLanguage": "hi"
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

    logger.info(f"Uploading '{clean_title}' to @iDastawez as [{privacy_status.upper()}]...")
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
    logger.info(f"🎉 VIDEO UPLOADED SUCCESSFULLY! Watch URL: {video_url}")

    # Set Custom 1280x720 Thumbnail
    if thumbnail_path and os.path.exists(thumbnail_path):
        try:
            logger.info(f"Uploading custom thumbnail from: {thumbnail_path}...")
            mime = "image/png" if thumbnail_path.endswith(".png") else "image/jpeg"
            thumb_media = MediaFileUpload(thumbnail_path, mimetype=mime)
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=thumb_media
            ).execute()
            logger.info("✓ Custom 1280x720 thumbnail applied successfully!")
        except Exception as e:
            logger.warning(f"Could not set custom thumbnail (Verify phone on YouTube Studio): {e}")

    # Post first pinned discussion & helpline comment
    if first_comment:
        try:
            comment_body = {
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": first_comment
                        }
                    }
                }
            }
            youtube.commentThreads().insert(part="snippet", body=comment_body).execute()
            logger.info("✓ Pinned official comment posted successfully!")
        except Exception as e:
            logger.info(f"Comment note: {e}")

    return video_url


if __name__ == "__main__":
    verify_connected_channel()
