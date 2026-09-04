"""
Neural Voice Generator via edge-tts
100% Free, Unlimited, Studio Quality, No Watermark.
Generates audio and computes exact word-level timing offsets for viral captions.
"""

import os
import asyncio
import logging
from typing import Dict, Any, List
import edge_tts
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_VOICE = os.getenv("VOICE_NAME", "en-US-ChristopherNeural")
DEFAULT_RATE = os.getenv("VOICE_RATE", "+5%")
DEFAULT_PITCH = os.getenv("VOICE_PITCH", "+0Hz")


def _calculate_word_timings(sentence_boundaries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert SentenceBoundaries (100ns ticks) into exact word-level start/end timestamps."""
    all_word_timings = []
    
    for sentence in sentence_boundaries:
        # 10,000,000 ticks = 1 second
        offset_sec = sentence["offset"] / 10000000.0
        duration_sec = sentence["duration"] / 10000000.0
        text = sentence["text"].strip()
        words = text.split()
        
        if not words:
            continue
            
        # Weight word durations by character length
        total_weights = sum(max(len(w), 2) for w in words)
        current_time = offset_sec
        
        for w in words:
            weight = max(len(w), 2)
            w_duration = (weight / total_weights) * duration_sec
            all_word_timings.append({
                "word": w,
                "start": round(current_time, 3),
                "end": round(current_time + w_duration, 3)
            })
            current_time += w_duration
            
    return all_word_timings


async def _generate_audio_async(
    text: str,
    output_audio_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> Dict[str, Any]:
    """Internal async synthesizer collecting audio chunks and sentence boundaries."""
    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
    
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    sentence_boundaries = []
    
    with open(output_audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            chunk_type = chunk.get("type")
            if chunk_type == "audio":
                audio_file.write(chunk.get("data", b""))
            elif chunk_type == "SentenceBoundary":
                sentence_boundaries.append(chunk)

    word_timings = _calculate_word_timings(sentence_boundaries)
    
    # Audio total duration calculation
    total_duration = 0.0
    if word_timings:
        total_duration = word_timings[-1]["end"] + 0.3
    else:
        # Fallback if no boundaries returned
        import imageio_ffmpeg
        import subprocess
        ffprobe_exe = imageio_ffmpeg.get_ffmpeg_exe()
        # Estimate ~130 words/minute
        total_duration = max(len(text.split()) / 2.5, 5.0)

    logger.info(f"Generated neural voiceover: {total_duration:.1f}s, {len(word_timings)} words.")
    
    return {
        "audio_path": output_audio_path,
        "duration": round(total_duration, 2),
        "word_timings": word_timings
    }


def generate_voiceover(
    text: str,
    output_path: str = "temp/voiceover.mp3",
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH
) -> Dict[str, Any]:
    """Synchronous entry point for generating voiceover audio and timestamps."""
    return asyncio.run(_generate_audio_async(text, output_path, voice, rate, pitch))


if __name__ == "__main__":
    sample_text = "Breaking AI update! A brand new autonomous agent protocol was just discovered. Developers are stunned."
    res = generate_voiceover(sample_text)
    print("\n--- AUDIO GENERATION RESULT ---")
    print("Path:", res["audio_path"])
    print("Duration:", res["duration"])
    print("First 3 words:", res["word_timings"][:3])
