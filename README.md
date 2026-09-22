# 🚀 YTautomation: Autonomous Tech Video Pipeline

End-to-end automation for generating and publishing bilingual tech videos:
- **Shorts (9:16)** for rapid trend coverage
- **Long episodes (16:9)** for deep-dive explainers
- **English (@TechShow)** and **Hindi (@iDastawez)** channel flows

The project can run locally, but production publishing is designed around **GitHub Actions schedules**.

---

## ✨ What this repo does

- Fetches trending stories (Hacker News, Reddit, RSS) or uses a custom topic
- Generates script content with Gemini
- Creates neural narration (`edge-tts`)
- Renders:
  - vertical Shorts via Python compositor
  - landscape long episodes via Remotion + Python pipeline
- Auto-publishes to YouTube (and Instagram Reel for tech shorts when configured)
- Tracks published stories to avoid repeats (`assets/published_history.json`)

---

## 📁 Project structure

```text
/home/runner/work/YTautomation/YTautomation
├── assets/                    # audio, meme assets, avatar image, publish history
├── src/                       # pipeline modules (fetch, script, voice, render, upload)
├── remotion/                  # long-form visual/thumbnail components
├── .github/workflows/         # scheduled automation workflows
├── main.py                    # entry point
├── requirements.txt           # Python dependencies
├── package.json               # Remotion/Node dependencies
├── .env.example               # local environment template
└── scheduler_*.ps1, run_daily.bat
```

---

## ⚙️ Prerequisites

- Python **3.11+**
- Node.js **20+**
- FFmpeg available in PATH
- System fonts for Devanagari/Hindi rendering (for Hindi output)

---

## 🧪 Local setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Node dependencies (required for Remotion-based long visuals/thumbnails):
   ```bash
   npm ci
   ```

3. Create local env file:
   ```bash
   cp .env.example .env
   ```

4. Add credentials in `.env` as needed:
   - `GEMINI_API_KEY`
   - `PEXELS_API_KEY` (optional)
   - YouTube OAuth files (`client_secret.json`, token files) for publishing
   - Instagram keys only if using IG publishing

---

## ▶️ Usage

> By default, runs are dry-run unless `--publish` is passed.

### Short video (default mode)
```bash
python main.py --channel tech --dry-run
```

### Long episode
```bash
python main.py --mode long --channel tech --duration 12 --dry-run
```

### Hindi channel
```bash
python main.py --channel dastawez --mode short --publish
```

### Dual-channel run
```bash
python main.py --channel both --mode short --publish
```

### Custom topic
```bash
python main.py --mode long --channel tech --topic "AI chip war" --duration 10 --publish
```

### Key CLI options
- `--mode short|long`
- `--channel tech|dastawez|both`
- `--lang en|hi` (optional override)
- `--duration <minutes>` (long mode)
- `--topic "..."`
- `--publish` (otherwise dry-run behavior)

---

## 🤖 GitHub Actions automation

Primary workflows:
- `daily_shorts.yml` → tech shorts schedule + manual dispatch
- `daily_dastawez.yml` → Hindi shorts + long schedule + manual dispatch
- `weekly_episodes.yml` (named daily long episodes) → long-form episode automation

These workflows install dependencies, inject secrets, run `main.py`, and persist publish history updates.

---

## 🔐 Required GitHub Secrets (for CI publishing)

- `GEMINI_API_KEY`
- `PEXELS_API_KEY` (optional but recommended)
- `CLIENT_SECRET_JSON`
- `TOKEN_JSON`
- `TOKEN_DASTAWEZ_JSON` (or fallback behavior in workflows)
- `INSTAGRAM_ACCOUNT_ID` / `INSTAGRAM_ACCESS_TOKEN` (optional IG flow)

---

## 📝 Notes

- `run_daily.bat` is intentionally disabled for local laptop execution in the current setup.
- Windows scheduler scripts are present, but the active production path is GitHub Actions automation.
