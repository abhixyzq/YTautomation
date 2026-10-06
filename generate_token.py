#!/usr/bin/env python3
"""
Interactive YouTube OAuth Token Generator
Generates a fresh token.json (or token_dastawez.json) for unattended automation & GitHub Actions.
"""

import os
import sys
import json
import argparse
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
CLIENT_SECRET_FILE = os.getenv("YOUTUBE_CLIENT_SECRET_FILE", "client_secret.json")


def main():
    parser = argparse.ArgumentParser(description="Generate YouTube OAuth token")
    parser.add_argument(
        "--channel",
        choices=["tech", "dastawez"],
        default="tech",
        help="Target channel token to generate ('tech' -> token.json, 'dastawez' -> token_dastawez.json)"
    )
    parser.add_argument(
        "--upload-only",
        action="store_true",
        help="Request only youtube.upload scope (recommended if force-ssl scope is not added in GCP consent screen)"
    )
    args = parser.parse_args()

    active_scopes = ["https://www.googleapis.com/auth/youtube.upload"] if args.upload_only else SCOPES
    target_file = "token_dastawez.json" if args.channel == "dastawez" else "token.json"
    secret_name = "TOKEN_DASTAWEZ_JSON" if args.channel == "dastawez" else "TOKEN_JSON"

    print("=" * 72)
    print(" 🔑 YOUTUBE OAUTH TOKEN GENERATOR")
    print(f" 🎯 Target File:        {target_file} (Channel: {args.channel.upper()})")
    print(f" 🔒 GitHub Secret Name: {secret_name}")
    print(f" 📜 Scopes:             {', '.join(active_scopes)}")
    print("=" * 72)

    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"\n❌ Error: '{CLIENT_SECRET_FILE}' was not found in the current directory!")
        print("Please ensure your Google Cloud OAuth client credentials JSON exists.")
        print("1. Visit https://console.cloud.google.com/apis/credentials")
        print("2. Create/Download an OAuth Client ID (Application type: Desktop App)")
        print(f"3. Save it as '{CLIENT_SECRET_FILE}' in this folder.")
        sys.exit(1)

    # Extract Project ID if available
    project_id = None
    try:
        with open(CLIENT_SECRET_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            client_info = data.get("installed", data.get("web", {}))
            project_id = client_info.get("project_id")
    except Exception:
        pass

    print("\n⚠️  IMPORTANT: WHY TOKENS EXPIRE AFTER 7 DAYS")
    print("------------------------------------------------------------------------")
    print("If your Google Cloud OAuth Consent Screen is in 'Testing' status,")
    print("Google automatically EXPIRES your refresh token after exactly 7 days,")
    print("causing the GitHub Actions error: 'invalid_grant: Token has been expired or revoked.'")
    print("\n👉 TO STOP 7-DAY EXPIRATION PERMANENTLY (Set to Production):")
    if project_id:
        print(f"   1. Open: https://console.cloud.google.com/apis/credentials/consent?project={project_id}")
    else:
        print("   1. Open: https://console.cloud.google.com/apis/credentials/consent")
    print("   2. Under 'Publishing status', click the 'PUBLISH APP' button and confirm.")
    print("   (Note: For personal use, you do NOT need Google App Verification.")
    print("    You just click 'Advanced' -> 'Go to App (unsafe)' during Google login once.)")
    print("------------------------------------------------------------------------\n")

    input("👉 Press ENTER to open your browser and sign in with your YouTube Google account...")

    print("\n🌐 Starting local authentication server & opening browser...")
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=active_scopes
    )
    # prompt='consent' and access_type='offline' ensure a long-lived refresh_token is returned
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

    # Verify credentials immediately with YouTube Data API
    print("\n⏳ Verifying token with YouTube API...")
    try:
        yt = build("youtube", "v3", credentials=creds)
        res = yt.channels().list(part="snippet", mine=True).execute()
        items = res.get("items", [])
        if items:
            channel_name = items[0]["snippet"]["title"]
            channel_id = items[0]["id"]
            print(f"✅ Authenticated successfully as channel: '{channel_name}' (ID: {channel_id})")
        else:
            print("✅ Authenticated successfully! (Valid Google Account)")
    except Exception as e:
        print(f"⚠️ Warning: Token generated, but channel info query returned: {e}")

    token_json_str = creds.to_json()

    # Save locally to file
    with open(target_file, "w", encoding="utf-8") as f:
        f.write(token_json_str)
    print(f"\n💾 Saved credentials locally to: {target_file}")

    # Attempt copy to Windows clipboard
    copied = False
    try:
        p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
        p.communicate(input=token_json_str.encode("utf-8"))
        if p.returncode == 0:
            copied = True
    except Exception:
        pass

    print("\n" + "=" * 72)
    print(f"🎉 SUCCESS! NEXT STEP: UPDATE GITHUB ACTIONS SECRET '{secret_name}'")
    print("=" * 72)
    if copied:
        print(f"📋 The entire content of '{target_file}' is ALREADY COPIED to your CLIPBOARD!")
    else:
        print(f"📋 Copy the entire contents of '{target_file}' from your project folder.")

    print("\n1. Go to your GitHub Repository Secrets page:")
    print("   👉 https://github.com/abhixyzq/YTautomation/settings/secrets/actions")
    print(f"2. Locate secret '{secret_name}' (click update, or 'New repository secret')")
    print("3. Paste the copied token JSON.")
    print("4. Click 'Update secret' (or 'Add secret').")
    print("5. Go to Actions tab and re-run the failed workflow!\n")
    print("=" * 72)


if __name__ == "__main__":
    main()
