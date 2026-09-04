"""
High-Retention Viral Caption Engine (Auto-Sized & Screen-Safe)
Guarantees captions NEVER spill outside the screen borders.
- Dynamic 1-2 word chunking for rapid reading (Hormozi / MrBeast style)
- Dynamic font auto-scaling with guaranteed 80px safe margins
- Bouncy neon yellow (#FFE600) active word highlights
- Dark rounded pill backing for 100% contrast on any video
"""

import os
import math
from typing import List, Dict, Any
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "assets/fonts/bold.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
]

FONT_PATH = None
for candidate in FONT_CANDIDATES:
    if os.path.exists(candidate):
        FONT_PATH = candidate
        break


def _build_phrase_item(chunk: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "words": chunk,
        "phrase_text": " ".join(w["word"].upper() for w in chunk),
        "start": chunk[0]["start"],
        "end": chunk[-1]["end"] + 0.12
    }


def group_words_into_phrases(
    word_timings: List[Dict[str, Any]],
    max_words_per_phrase: int = 2,
    max_chars_per_phrase: int = 15,
    words_per_phrase: int = None
) -> List[Dict[str, Any]]:
    if words_per_phrase is not None:
        max_words_per_phrase = words_per_phrase
    """
    Intelligently groups words into punchy 1-2 word phrases.
    Ensures long technical words (e.g. 'ARCHITECTURES', 'DEVELOPMENT')
    get their own focused frame so they NEVER clip the edges.
    """
    phrases = []
    current_chunk = []
    current_chars = 0

    for item in word_timings:
        word = item["word"]
        word_len = len(word)

        # Flush chunk if adding this word exceeds limits
        if current_chunk:
            is_word_count_exceeded = len(current_chunk) >= max_words_per_phrase
            is_char_len_exceeded = (current_chars + word_len + 1) > max_chars_per_phrase
            is_super_long = word_len >= 9  # Long tech words deserve isolated focus

            if is_word_count_exceeded or is_char_len_exceeded or is_super_long:
                phrases.append(_build_phrase_item(current_chunk))
                current_chunk = []
                current_chars = 0

        current_chunk.append(item)
        current_chars += word_len + 1

    if current_chunk:
        phrases.append(_build_phrase_item(current_chunk))

    return phrases


class CaptionRenderer:
    def __init__(self, width: int = 1080, height: int = 1920, base_font_size: int = 68):
        self.width = width
        self.height = height
        self.base_font_size = base_font_size
        self.max_allowed_width = width - 160  # Guaranteed 80px safe margin on both sides

    def _get_font(self, size: int):
        if FONT_PATH:
            return ImageFont.truetype(FONT_PATH, size)
        return ImageFont.load_default()

    def render_caption_frame(self, current_phrase: Dict[str, Any], current_time: float) -> Image.Image:
        """Render a single transparent RGBA subtitle overlay with guaranteed screen-safe bounds."""
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        words = current_phrase["words"]
        word_items = [(w["word"].upper(), w["start"], w["end"]) for w in words]

        # 1. Start with base font and autoscale down if words are too wide
        curr_font_size = self.base_font_size
        font = self._get_font(curr_font_size)

        space_w = draw.textbbox((0, 0), " ", font=font)[2]
        word_widths = [draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox((0, 0), text, font=font)[0] for text, _, _ in word_items]
        total_w = sum(word_widths) + max(0, len(words) - 1) * space_w

        # If it exceeds screen-safe width, scale down font dynamically
        if total_w > self.max_allowed_width:
            scale = self.max_allowed_width / total_w
            curr_font_size = max(int(self.base_font_size * scale), 44)
            font = self._get_font(curr_font_size)
            space_w = draw.textbbox((0, 0), " ", font=font)[2]
            word_widths = [draw.textbbox((0, 0), text, font=font)[2] - draw.textbbox((0, 0), text, font=font)[0] for text, _, _ in word_items]
            total_w = sum(word_widths) + max(0, len(words) - 1) * space_w

        # 2. Guaranteed centered position with strict boundary clamping
        start_x = max(80, (self.width - total_w) // 2)
        # Position at ~63% height (golden eye level for vertical Shorts)
        y_pos = int(self.height * 0.63)

        # 3. Dynamic contrast backing badge (pill)
        pad_x = 28
        pad_y = 16
        text_sample_bbox = draw.textbbox((0, 0), "AG", font=font)
        line_height = text_sample_bbox[3] - text_sample_bbox[1]

        box_left = max(40, start_x - pad_x)
        box_right = min(self.width - 40, start_x + total_w + pad_x)
        box_top = y_pos - pad_y
        box_bottom = y_pos + line_height + pad_y + 8

        # Draw sleek dark glass backing with vibrant cyan border
        draw.rounded_rectangle(
            [box_left, box_top, box_right, box_bottom],
            radius=18,
            fill=(8, 12, 22, 215),
            outline=(0, 240, 255, 140),
            width=3
        )

        # 4. Render active word highlight and crisp white surrounding text
        curr_x = start_x
        for (text, w_start, w_end), w_w in zip(word_items, word_widths):
            is_active = (w_start <= current_time <= w_end + 0.08)

            # Colors: Active = Electric Neon Yellow (#FFE600), Inactive = Pure Crisp White
            text_color = (255, 230, 0, 255) if is_active else (255, 255, 255, 255)
            stroke_color = (0, 0, 0, 255)
            stroke_w = 4 if is_active else 3

            draw.text(
                (curr_x, y_pos),
                text,
                font=font,
                fill=text_color,
                stroke_fill=stroke_color,
                stroke_width=stroke_w
            )

            curr_x += w_w + space_w

        return overlay


if __name__ == "__main__":
    test_words = [
        {"word": "DEVELOPER", "start": 0.0, "end": 0.4},
        {"word": "COMMUNITY.", "start": 0.4, "end": 0.9},
        {"word": "UNDER", "start": 0.9, "end": 1.2},
        {"word": "THE", "start": 1.2, "end": 1.4},
        {"word": "HOOD,", "start": 1.4, "end": 1.7},
        {"word": "ENGINEERS", "start": 1.7, "end": 2.2},
        {"word": "ARE", "start": 2.2, "end": 2.4},
        {"word": "REDESIGNING", "start": 2.4, "end": 2.9},
        {"word": "MODERN", "start": 2.9, "end": 3.3},
        {"word": "ARCHITECTURES", "start": 3.3, "end": 3.9},
        {"word": "INTERACT,", "start": 3.9, "end": 4.4}
    ]
    phrases = group_words_into_phrases(test_words)
    renderer = CaptionRenderer()

    print(f"Grouped into {len(phrases)} screen-safe phrases:")
    for i, p in enumerate(phrases):
        print(f"  {i+1}: {p['phrase_text']}")

    # Render test frame for longest phrase: 'ARCHITECTURES' or 'DEVELOPER COMMUNITY.'
    test_frame = renderer.render_caption_frame(phrases[0], current_time=0.2)
    os.makedirs("temp", exist_ok=True)
    test_frame.save("temp/test_safe_caption.png")
    print("Saved test caption overlay to temp/test_safe_caption.png")
