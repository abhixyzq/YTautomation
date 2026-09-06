"""
iDastawez - Studio Neural Hindi Voice Generator
Uses Microsoft Edge Neural TTS (hi-IN-MadhurNeural / hi-IN-SwaraNeural).
100% Free, Zero Cost, Studio Quality Hindi Pronunciation with Natural Cadence.
"""

import os
import sys
import re
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Default Voice: Madhur (Clear, Authoritative, News anchor tone)
DEFAULT_HINDI_VOICE = "hi-IN-MadhurNeural"
DEFAULT_RATE = "+0%"  # Neutral rate for maximum clarity and comprehension
DEFAULT_PITCH = "+0Hz"


def clean_hindi_for_tts(text: str) -> str:
    """
    Normalizes symbols, acronyms, and numbers into phonetically clear Hindi words
    so edge-tts pronounces them flawlessly without stuttering.
    """
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Acronym phonetic expansions in Devanagari
    acronym_map = [
        (r"\be-KYC\b", "ई-केवाईसी"),
        (r"\bE-KYC\b", "ई-केवाईसी"),
        (r"\beKYC\b", "ई-केवाईसी"),
        (r"\bOTP\b", "ओटीपी"),
        (r"\bDBT\b", "डीबीटी"),
        (r"\bNPCI\b", "एनपीसीआई"),
        (r"\bPAN\b", "पैन"),
        (r"\bPDF\b", "पीडीएफ"),
        (r"\bSMS\b", "एसएमएस"),
        (r"\bNSP\b", "एनएसपी"),
        (r"\bOTR\b", "ओटीआर"),
        (r"\bPMAY\b", "पीएम आवास योजना"),
        (r"\bCGHS\b", "सीजीएचएस"),
        (r"\bECHS\b", "ईसीएचएस"),
        (r"\bCSC\b", "सीएससी केंद्र"),
        (r"\bURL\b", "वेबसाइट लिंक"),
        (r"\bID\b", "आईडी"),
    ]
    for pattern, repl in acronym_map:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # Convert common Rupee representations
    text = re.sub(r"₹\s*5,00,000", "पाँच लाख रुपये", text)
    text = re.sub(r"₹\s*6,000", "छह हज़ार रुपये", text)
    text = re.sub(r"₹\s*2,000", "दो हज़ार रुपये", text)
    text = re.sub(r"₹\s*10,000", "दस हज़ार रुपये", text)
    text = re.sub(r"₹\s*1,000", "एक हज़ार रुपये", text)
    text = re.sub(r"₹\s*(\d+)", r"\1 रुपये", text)

    # Convert percentages
    text = re.sub(r"(\d+)%", r"\1 प्रतिशत", text)

    # Ensure natural micro-pauses after transitions
    text = text.replace("—", ", ")
    text = text.replace("--", ", ")
    text = text.replace(":", " -")

    return text


async def _generate_audio_file(
    text: str, 
    output_audio_path: str, 
    voice: str = DEFAULT_HINDI_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> float:
    """
    Generates an MP3 file for the provided Hindi text and returns duration in seconds.
    """
    cleaned_text = clean_hindi_for_tts(text)
    communicate = edge_tts.Communicate(cleaned_text, voice=voice, rate=rate, pitch=pitch)
    
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    await communicate.save(output_audio_path)
    
    # Calculate duration using ffprobe or mutagen/pydub or simple estimate
    duration = 0.0
    try:
        import mutagen.mp3
        audio = mutagen.mp3.MP3(output_audio_path)
        duration = audio.info.length
    except Exception:
        # Fallback to ffprobe
        import subprocess
        try:
            cmd = [
                "ffprobe", "-v", "error", "-show_entries",
                "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                output_audio_path
            ]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            duration = float(result.stdout.strip())
        except Exception:
            # Fallback estimate: ~2.6 words per second in Hindi
            words = len(cleaned_text.split())
            duration = words / 2.6
            
    return duration


def generate_scene_voiceovers(
    script_data: Dict[str, Any], 
    output_dir: str, 
    voice: str = DEFAULT_HINDI_VOICE
) -> Dict[str, Any]:
    """
    Generates studio neural voiceovers for each scene in the script.
    Saves individual MP3 files and returns scene metadata with exact durations.
    """
    os.makedirs(output_dir, exist_ok=True)
    scenes = script_data.get("scenes", [])
    
    print(f"\n[iDastawez Voice Engine] Generating neural Hindi audio with {voice}...")
    
    enriched_scenes = []
    total_duration = 0.0
    
    async def process_all_scenes():
        nonlocal total_duration
        for scene in scenes:
            scene_id = scene["scene_id"]
            audio_filename = f"scene_{scene_id}.mp3"
            audio_path = os.path.join(output_dir, audio_filename)
            dialogue = scene["dialogue"]
            
            duration = await _generate_audio_file(dialogue, audio_path, voice=voice)
            total_duration += duration
            
            enriched = dict(scene)
            enriched["audio_file"] = audio_filename
            enriched["audio_path"] = os.path.abspath(audio_path).replace("\\", "/")
            enriched["duration_seconds"] = round(duration, 2)
            enriched["duration_frames_30fps"] = int(round(duration * 30))
            enriched_scenes.append(enriched)
            
            print(f"  ✓ Scene {scene_id} [{scene['act_name']}]: {round(duration, 1)}s ({len(dialogue.split())} words)")

    asyncio.run(process_all_scenes())
    
    result = dict(script_data)
    result["scenes"] = enriched_scenes
    result["total_audio_duration_seconds"] = round(total_duration, 2)
    result["voice_used"] = voice
    
    # Also save metadata JSON alongside the audio
    meta_path = os.path.join(output_dir, "voice_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"[iDastawez Voice Engine] Generated {len(enriched_scenes)} scenes. Total Duration: {round(total_duration / 60, 2)} minutes.")
    return result


if __name__ == "__main__":
    from dastawez.topics import VERIFIED_GOVT_SCHEMES
    from dastawez.script_generator import generate_dastawez_script
    
    sample_scheme = VERIFIED_GOVT_SCHEMES[0]  # Ayushman Bharat 70+
    sample_script = generate_dastawez_script(sample_scheme)
    
    test_output_dir = os.path.abspath("./output/dastawez_test_voice")
    voice_res = generate_scene_voiceovers(sample_script, test_output_dir)
    print("\nVoice Generation Complete! Metadata saved to:", test_output_dir)
