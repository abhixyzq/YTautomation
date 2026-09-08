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
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")


def resolve_token_file(channel: str = "tech", token_file: Optional[str] = None) -> str:
    """Resolve token file path based on selected target channel."""
    if token_file:
        return token_file
    if channel.lower() in ("dastawez", "idastawez", "hindi"):
        return os.getenv("YOUTUBE_TOKEN_DASTAWEZ_FILE", "token_dastawez.json")
    return os.getenv("YOUTUBE_TOKEN_FILE", "token.json")


def get_youtube_service(channel: str = "tech", token_file: Optional[str] = None):
    """Authenticate and return an authorized YouTube Data API service instance for specified channel."""
    target_token_file = resolve_token_file(channel, token_file)
    creds = None
    
    # 1. Check if token file already exists (saved session)
    if os.path.exists(target_token_file):
        try:
            creds = Credentials.from_authorized_user_file(target_token_file, SCOPES)
        except Exception as e:
            logger.warning(f"Failed to load cached token ({target_token_file}): {e}")

    # 2. If no valid credentials, refresh or initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info(f"Refreshing expired YouTube OAuth token for [{channel.upper()}] ({target_token_file})...")
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
            
            logger.info(f"Initiating browser OAuth authentication for YouTube [{channel.upper()}]...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future unattended runs
        with open(target_token_file, "w") as token:
            token.write(creds.to_json())
            logger.info(f"Saved YouTube OAuth credentials to {target_token_file}.")

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
    comment_text: str = None,
    channel: str = "tech",
    token_file: Optional[str] = None,
    story: Optional[dict] = None,
    language: Optional[str] = None
) -> Optional[str]:
    """
    Upload a video file as a YouTube Short to the specified channel with algorithm-optimized SEO.
    Returns the uploaded YouTube Video URL.
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    youtube = get_youtube_service(channel=channel, token_file=token_file)
    if not youtube:
        logger.warning(f"Skipping upload. Video rendered and ready locally at: {video_path}")
        return None

    from src.seo_engine import generate_shorts_seo

    # 1. Generate Algorithm-Optimized Shorts SEO Metadata
    resolved_lang = language or ("hi" if channel.lower() in ("dastawez", "idastawez", "hindi") else "en")
    seo_meta = generate_shorts_seo(
        story=story or {"title": title, "summary": description, "cta": comment_text},
        raw_title=title,
        description=description,
        channel=channel,
        language=resolved_lang
    )
    final_title = seo_meta["title"]
    seo_description = seo_meta["description"]
    combined_tags = tags or seo_meta["tags"]
    pinned_prompt = comment_text or seo_meta["pinned_comment"]

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

    logger.info(f"Uploading '{final_title}' (Short) to YouTube [{channel.upper()}] as [{privacy_status.upper()}]...")
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
    logger.info(f"SUCCESS! Short live at: {video_url}")

    # 2. Attempt to post first engagement comment
    post_first_comment(youtube, video_id, pinned_prompt)

    return video_url


def upload_long_video_to_youtube(
    video_path: str,
    title: str,
    description: str,
    chapters: list = None,
    tags: list = None,
    privacy_status: str = "public",
    comment_text: str = None,
    thumbnail_path: str = None,
    channel: str = "tech",
    token_file: Optional[str] = None,
    story: Optional[dict] = None,
    language: Optional[str] = None
) -> Optional[str]:
    """
    Upload a 16:9 horizontal long video to YouTube with 5-layer SEO metadata architecture,
    clickable chapters / timestamps for Google Key Moments, and custom thumbnail.
    Returns the uploaded YouTube Video URL.
    """
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None

    youtube = get_youtube_service(channel=channel, token_file=token_file)
    if not youtube:
        logger.warning(f"Skipping upload. Video rendered and ready locally at: {video_path}")
        return None

    from src.seo_engine import generate_masterclass_seo

    # 1. Generate 5-Layer Masterclass SEO Metadata
    resolved_lang = language or ("hi" if channel.lower() in ("dastawez", "idastawez", "hindi") else "en")
    seo_meta = generate_masterclass_seo(
        story=story or {"title": title, "summary": description, "cta_question": comment_text},
        chapters=chapters,
        channel=channel,
        language=resolved_lang
    )

    final_title = seo_meta["title"]
    seo_description = seo_meta["description"]
    pinned_prompt = comment_text or seo_meta["pinned_comment"]
    
    # Merge custom tags with high-performance SEO tags
    if tags:
        combined_tags = list(dict.fromkeys(seo_meta["tags"] + tags))[:25]
    else:
        combined_tags = seo_meta["tags"]

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

