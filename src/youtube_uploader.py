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
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")


def resolve_token_file(channel: str = "tech", token_file: Optional[str] = None) -> str:
    """Resolve token file path based on selected target channel with seamless fallback."""
    if token_file:
        return token_file
    if channel.lower() in ("dastawez", "idastawez", "hindi"):
        dastawez_token = os.getenv("YOUTUBE_TOKEN_DASTAWEZ_FILE", "token_dastawez.json")
        if os.path.exists(dastawez_token) and os.path.getsize(dastawez_token) > 10:
            return dastawez_token
        # Graceful fallback: If separate dastawez token is missing, use default token.json
        general_token = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")
        if os.path.exists(general_token) and os.path.getsize(general_token) > 10:
            logger.info(f"Target token '{dastawez_token}' not found. Using channel token '{general_token}'.")
            return general_token
        return dastawez_token
    return os.getenv("YOUTUBE_TOKEN_FILE", "token.json")


def get_youtube_service(channel: str = "tech", token_file: Optional[str] = None):
    """Authenticate and return an authorized YouTube Data API service instance for specified channel."""
    target_token_file = resolve_token_file(channel, token_file)
    creds = None
    
    # 1. Check if token file already exists (saved session)
    if os.path.exists(target_token_file):
        try:
            creds = Credentials.from_authorized_user_file(target_token_file)
        except Exception as e:
            logger.warning(f"Failed to load cached token ({target_token_file}): {e}")

    # 2. If credentials exist but expired, attempt refresh
    if creds and creds.expired and creds.refresh_token:
        logger.info(f"Refreshing expired YouTube OAuth token for [{channel.upper()}] ({target_token_file})...")
        try:
            creds.refresh(Request())
        except Exception as e:
            logger.error(
                f"❌ Failed to refresh YouTube OAuth token: {e}\n"
                "👉 This usually happens because Google Cloud OAuth Consent Screen is in 'Testing' mode (expires in 7 days),\n"
                "   or the token was revoked.\n"
                "👉 Solution: Set OAuth Consent Screen to 'In production' (Publish App) and generate a new token using 'python generate_token.py'."
            )
            creds = None

    # 3. If still no valid credentials, handle interactive authentication or CI failure
    if not creds or not creds.valid:
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

        # If running in GitHub Actions / CI, interactive browser auth is impossible
        if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
            logger.error(
                f"❌ YouTube authentication failed in GitHub Actions!\n"
                f"The token in '{target_token_file}' is invalid or expired ('invalid_grant').\n"
                "-------------------------------------------------------------------------\n"
                "HOW TO FIX THIS:\n"
                "1. Set Google Cloud OAuth status to 'In production' (Publish App) to prevent 7-day expiration:\n"
                "   https://console.cloud.google.com/apis/credentials/consent?project=youtubeautomation-507613\n"
                "2. Run 'python generate_token.py' on your local computer to generate a fresh token.\n"
                "3. Update GitHub Secret 'TOKEN_JSON' (or 'TOKEN_DASTAWEZ_JSON') at:\n"
                "   https://github.com/abhixyzq/YTautomation/settings/secrets/actions\n"
                "-------------------------------------------------------------------------"
            )
            return None

        logger.info(f"Initiating browser OAuth authentication for YouTube [{channel.upper()}]...")
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

        # Save credentials for future unattended runs
        if creds and creds.valid:
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

