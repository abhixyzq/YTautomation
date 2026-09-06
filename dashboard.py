"""
YT Automation Pipeline - Mobile Control Dashboard Server
Run: python dashboard.py
Then open http://<YOUR_LAPTOP_IP>:5000 on your phone (same WiFi)
"""

import os
import sys
import json
import subprocess
import threading
import datetime
import logging
from pathlib import Path
from flask import Flask, jsonify, request, render_template_string, Response, send_from_directory
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Dashboard")

app = Flask(__name__)

# ─────────────────────────────────────────────
# GLOBAL PIPELINE STATE
# ─────────────────────────────────────────────
pipeline_state = {
    "running": False,
    "mode": None,
    "topic": None,
    "duration": None,
    "started_at": None,
    "status": "idle",          # idle | running | done | error
    "last_result": None,
    "log_lines": [],
}
MAX_LOG_LINES = 200
_lock = threading.Lock()
_current_proc = None


def _log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    with _lock:
        pipeline_state["log_lines"].append(line)
        if len(pipeline_state["log_lines"]) > MAX_LOG_LINES:
            pipeline_state["log_lines"] = pipeline_state["log_lines"][-MAX_LOG_LINES:]
    logger.info(msg)


def run_pipeline_thread(mode: str, topic: str, duration: int, publish: bool):
    """Runs main.py in a subprocess and streams output to log_lines."""
    global _current_proc
    with _lock:
        pipeline_state["running"] = True
        pipeline_state["mode"] = mode
        pipeline_state["topic"] = topic
        pipeline_state["duration"] = duration
        pipeline_state["started_at"] = datetime.datetime.now().isoformat()
        pipeline_state["status"] = "running"
        pipeline_state["last_result"] = None

    cmd = [sys.executable, "main.py", "--mode", mode]
    if topic:
        cmd += ["--topic", topic]
    if mode == "long":
        cmd += ["--duration", str(duration)]
    if publish:
        cmd.append("--publish")
    else:
        cmd.append("--dry-run")

    _log(f"▶ Starting pipeline: {' '.join(cmd)}")

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.getcwd(),
            encoding="utf-8",
            errors="replace"
        )
        with _lock:
            _current_proc = proc

        for line in proc.stdout:
            _log(line.rstrip())
        proc.wait()
        if proc.returncode == 0:
            with _lock:
                pipeline_state["status"] = "done"
                pipeline_state["last_result"] = "success"
            _log("✅ Pipeline completed successfully!")
        elif proc.returncode == -15 or proc.returncode == 1:
            with _lock:
                pipeline_state["status"] = "idle"
                pipeline_state["last_result"] = "stopped by user"
            _log("⏹ Pipeline stopped by user.")
        else:
            with _lock:
                pipeline_state["status"] = "error"
                pipeline_state["last_result"] = f"exit code {proc.returncode}"
            _log(f"❌ Pipeline failed with exit code {proc.returncode}")
    except Exception as e:
        with _lock:
            pipeline_state["status"] = "error"
            pipeline_state["last_result"] = str(e)
        _log(f"❌ Exception: {e}")
    finally:
        with _lock:
            _current_proc = None
            pipeline_state["running"] = False


# ─────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    with _lock:
        state = dict(pipeline_state)
        state["log_lines"] = state["log_lines"][-50:]  # last 50 lines only
    # Count output files
    output_dir = Path("output")
    shorts = len(list(output_dir.glob("Short_*.mp4"))) if output_dir.exists() else 0
    episodes = len(list(output_dir.glob("Episode_*.mp4"))) if output_dir.exists() else 0
    state["total_shorts"] = shorts
    state["total_episodes"] = episodes

    # Published count
    history_file = Path("assets/published_history.json")
    pub_count = 0
    if history_file.exists():
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                pub_count = len(json.load(f))
        except Exception:
            pass
    state["total_published"] = pub_count

    # Network IP for convenient phone connection banner
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        state["local_ip"] = s.getsockname()[0]
        s.close()
    except Exception:
        state["local_ip"] = "localhost"

    return jsonify(state)


@app.route("/api/run", methods=["POST"])
def api_run():
    if pipeline_state["running"]:
        return jsonify({"error": "Pipeline already running!"}), 409

    data = request.get_json(force=True, silent=True) or {}
    mode = data.get("mode", "short")
    topic = data.get("topic", "").strip() or None
    duration = int(data.get("duration", 12))
    publish = bool(data.get("publish", False))

    if mode not in ("short", "long"):
        return jsonify({"error": "mode must be 'short' or 'long'"}), 400

    t = threading.Thread(
        target=run_pipeline_thread,
        args=(mode, topic, duration, publish),
        daemon=True
    )
    t.start()
    return jsonify({"status": "started", "mode": mode, "topic": topic, "publish": publish})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    global _current_proc
    with _lock:
        proc = _current_proc
    if proc and proc.poll() is None:
        try:
            import subprocess
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
            _log("🛑 Sent taskkill to pipeline process tree.")
            return jsonify({"status": "stopping", "message": "Pipeline terminated."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "No active pipeline running."})


@app.route("/output/<path:filename>")
def serve_output(filename):
    output_dir = Path("output").resolve()
    return send_from_directory(output_dir, filename)


@app.route("/api/history")
def api_history():
    history_file = Path("assets/published_history.json")
    if not history_file.exists():
        return jsonify([])
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(list(reversed(data[-50:])))  # newest first
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/outputs")
def api_outputs():
    output_dir = Path("output")
    if not output_dir.exists():
        return jsonify([])
    files = []
    for f in sorted(output_dir.glob("*.mp4"), reverse=True):
        files.append({
            "name": f.name,
            "size_mb": round(f.stat().st_size / (1024 * 1024), 1),
            "type": "short" if f.name.startswith("Short_") else "episode",
            "created": datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        })
    return jsonify(files[:30])


@app.route("/api/logs")
def api_logs():
    with _lock:
        lines = list(pipeline_state["log_lines"])
    return jsonify({"lines": lines})


@app.route("/api/logs/stream")
def api_logs_stream():
    """Server-Sent Events stream for real-time log tailing."""
    def generate():
        sent = 0
        while True:
            with _lock:
                lines = pipeline_state["log_lines"]
                new_lines = lines[sent:]
                sent = len(lines)
            for line in new_lines:
                yield f"data: {json.dumps(line)}\n\n"
            import time; time.sleep(0.8)
    return Response(generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/env")
def api_env():
    """Return masked env config for the Settings page."""
    def mask(val):
        if not val: return "❌ Not set"
        return val[:8] + "..." + val[-4:] if len(val) > 12 else "✅ Set"
    return jsonify({
        "GEMINI_API_KEY": mask(os.getenv("GEMINI_API_KEY", "")),
        "PEXELS_API_KEY": mask(os.getenv("PEXELS_API_KEY", "")),
        "GIPHY_API_KEY": mask(os.getenv("GIPHY_API_KEY", "")),
        "VOICE_NAME": os.getenv("VOICE_NAME", "en-US-BrianMultilingualNeural"),
        "PUBLISH_MODE": os.getenv("PUBLISH_MODE", "PUBLIC"),
        "LANGUAGE": os.getenv("LANGUAGE", "ENG"),
        "INSTAGRAM_ACCOUNT_ID": mask(os.getenv("INSTAGRAM_ACCOUNT_ID", "")),
        "INSTAGRAM_ACCESS_TOKEN": mask(os.getenv("INSTAGRAM_ACCESS_TOKEN", "")),
    })


# ─────────────────────────────────────────────
# SERVE THE SINGLE-PAGE MOBILE APP
# ─────────────────────────────────────────────

@app.route("/")
def index():
    html_path = Path(__file__).parent / "dashboard_ui" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "localhost"

    print("\n" + "="*60)
    print("  📱 YT AUTOMATION MOBILE DASHBOARD")
    print("="*60)
    print(f"  Local:   http://localhost:5000")
    print(f"  Network: http://{local_ip}:5000")
    print(f"  → Open the Network URL on your phone (same WiFi)")
    print("="*60 + "\n")

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
