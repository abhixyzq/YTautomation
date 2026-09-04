# 🚀 Autonomous AI Avatar Tech Shorts Pipeline (100% Free)

An end-to-end, zero-cost, fully autonomous pipeline for generating high-retention 9:16 YouTube Shorts on trending tech and artificial intelligence news.

---

## 💎 Key Features
- **100% Free & Unlimited:** No HeyGen subscriptions, no ElevenLabs character limits, no watermarks.
- **Hardware-Optimized:** Custom-built for integrated graphics (Intel Iris Xe) and Windows.
- **Trending News Ingestion:** Auto-scrapes Hacker News, Reddit (`r/technology`, `r/artificial`), and TechCrunch RSS feeds.
- **Gemini 1.5 Flash:** Free tier (15 requests/minute) for generating viral 35-45 second hooks and high-retention scripts.
- **Neural Voiceover:** `edge-tts` Microsoft Neural Voice (`en-US-ChristopherNeural` - authoritative tech documentary tone).
- **Audio-Reactive AI Presenter:** Animated tech host bubble with neon glow, sinusoidal breathing motion, and live status badge.
- **Dynamic Captions:** High-contrast viral subtitles with word-by-word active highlights (Hormozi/MrBeast style).
- **Direct YouTube Upload:** Uploads as public or draft YouTube Shorts with `#Shorts #Tech #AI` metadata via YouTube Data API v3.
- **Automation Ready:** Includes `run_daily.bat` and `scheduler_setup.ps1` to publish 2x daily (9:00 AM & 6:00 PM).

---

## 📁 Project Structure

```
automate/
├── assets/
│   └── avatar_host.jpg       # High-authority AI presenter portrait
├── src/
│   ├── news_fetcher.py       # Scrapes top trending tech news
│   ├── script_generator.py   # Gemini 1.5 Flash viral script engine
│   ├── voice_generator.py    # edge-tts neural audio & timestamping
│   ├── avatar_engine.py      # Audio-reactive animated presenter bubble
│   ├── caption_engine.py     # Word-level highlighted subtitles
│   ├── video_compositor.py   # 1080x1920 9:16 video renderer
│   └── youtube_uploader.py   # YouTube Data API v3 publisher
├── output/                   # Rendered YouTube Shorts MP4s
├── temp/                     # Audio clips and intermediate frames
├── .env.example              # Configuration template
├── main.py                   # Master orchestrator
├── run_daily.bat             # 1-click execution batch file
├── scheduler_setup.ps1       # Windows Task Scheduler automated setup
└── requirements.txt          # Python dependencies
```

---

## ⚡ Quick Start

### 1. Test Run Locally (Dry Run)
Test the entire pipeline without uploading to YouTube:
```powershell
python main.py --dry-run
```
Your final video will be generated and saved in the `output/` folder!

### 2. Custom Topic Run
To make a video on a specific tech headline:
```powershell
python main.py --topic "DeepSeek V3 Open Source Model Outperforms GPT-4"
```

### 3. Add Google Gemini API Key ($0 Free)
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API Key** and create a free key (no credit card required).
3. Open `.env` and set:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   ```

### 4. Enable YouTube Auto-Upload ($0 Free)
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable **YouTube Data API v3**.
3. Go to **Credentials** > **Create Credentials** > **OAuth Client ID**.
4. Application type: **Desktop App**.
5. Click **Download JSON**, rename it to `client_secret.json`, and place it in this project folder.
6. The first time you run `python main.py --publish`, a browser window will open asking you to sign in with your YouTube account. It saves `token.json` locally so subsequent runs are 100% automated and silent!

---

## 🕒 Setting Up Automated 2x Daily Execution

To run automatically at 9:00 AM and 6:00 PM every day:
1. Open PowerShell as Administrator.
2. Run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scheduler_setup.ps1
   ```
This registers the tasks in Windows Task Scheduler to execute `run_daily.bat` autonomously.
