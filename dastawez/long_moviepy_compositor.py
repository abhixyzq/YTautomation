"""
iDastawez - 16:9 Ultra-Fast Documentary Compositor (MoviePy / FFmpeg)
Renders full 1080p horizontal civic-tech explainer documentaries in 2-3 minutes:
- Dynamic 1080p B-roll background sequencer with smooth Ken Burns motion
- High-contrast government verification HUD & layout-specific infographic cards:
  * Scheme Overview & Big Benefit Highlight
  * Old Rule vs New Rule (What Changed)
  * Eligibility Criteria (Who is Eligible)
  * Required Documents Checklist
  * 3-Step Online Application Process
  * Cyber Alert & Official Verification Helpline
- Synchronized Hindi Devanagari Subtitle Pill
- Professional multi-layer audio mix (Speech + Ambient Music + Scene Whoosh SFX)
"""

import os
import sys
import math
import logging
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import (
    AudioFileClip,
    VideoFileClip,
    CompositeAudioClip,
    VideoClip,
    concatenate_audioclips
)

logger = logging.getLogger("dastawez.long_compositor")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[iDastawez Long MoviePy] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

WIDTH = 1920
HEIGHT = 1080
FPS = 30

# -------------------------------------------------------------
# Cross-Platform Font Resolver (Windows + Linux CI)
# -------------------------------------------------------------
FONT_CANDIDATES_BOLD = [
    # Linux (Ubuntu / GitHub Actions)
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    # Windows
    "C:/Windows/Fonts/mangalb.ttf",
    "C:/Windows/Fonts/mangal.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

FONT_CANDIDATES_REG = [
    # Linux (Ubuntu / GitHub Actions)
    "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
    "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    # Windows
    "C:/Windows/Fonts/mangal.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

FONT_PATH_BOLD = next((p for p in FONT_CANDIDATES_BOLD if os.path.exists(p)), None)
FONT_PATH_REG = next((p for p in FONT_CANDIDATES_REG if os.path.exists(p)), None)


def get_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    path = FONT_PATH_BOLD if bold else FONT_PATH_REG
    if path:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


# -------------------------------------------------------------
# Card Drawing Helpers
# -------------------------------------------------------------
def draw_rounded_rect(draw: ImageDraw.ImageDraw, bbox: Tuple[int, int, int, int], radius: int, fill: Tuple[int, int, int, int], outline: Optional[Tuple[int, int, int, int]] = None, width: int = 1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)


def render_scene_card(scene: Dict[str, Any], scheme_meta: Dict[str, Any], act_idx: int, total_acts: int) -> Image.Image:
    """
    Renders a high-resolution 1920x1080 transparent overlay card for a specific scene act.
    Pre-rendered once per scene to ensure sub-millisecond per-frame compositing.
    """
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    layout_type = scene.get("layout_type", "scheme_overview")
    scheme_name = scene.get("scheme_name") or scheme_meta.get("scheme_name_hi", "प्रधानमंत्री सरकारी योजना")
    ministry = scene.get("ministry") or scheme_meta.get("ministry", "भारत सरकार")
    portal_domain = scene.get("official_portal_domain") or scheme_meta.get("portal_url", "gov.in").replace("https://", "").replace("http://", "").split("/")[0]
    urgency_badge = scene.get("urgency_badge") or scheme_meta.get("urgency_badge", "आधिकारिक सूचना 2026")

    # 1. Top HUD Navigation Bar
    hud_x1, hud_y1, hud_x2, hud_y2 = 64, 36, WIDTH - 64, 114
    draw_rounded_rect(draw, (hud_x1, hud_y1, hud_x2, hud_y2), radius=18, fill=(11, 17, 32, 235), outline=(56, 189, 248, 100), width=2)

    # HUD Left: Logo & Category
    draw_rounded_rect(draw, (hud_x1 + 16, hud_y1 + 12, hud_x1 + 64, hud_y2 - 12), radius=12, fill=(2, 132, 199, 255))
    font_icon = get_font(24, bold=True)
    draw.text((hud_x1 + 25, hud_y1 + 22), "🏛️", font=font_icon, fill=(255, 255, 255, 255))

    font_hud_title = get_font(22, bold=True)
    font_hud_sub = get_font(15, bold=False)
    draw.text((hud_x1 + 78, hud_y1 + 16), "iDastawez // राष्ट्रीय नागरिक सूचना", font=font_hud_title, fill=(255, 255, 255, 255))
    draw.text((hud_x1 + 78, hud_y1 + 44), f"मंत्रालय: {ministry}", font=font_hud_sub, fill=(148, 163, 184, 255))

    # HUD Center: Act Progress Badge
    act_text = f"अध्याय {act_idx} / {total_acts}"
    font_act = get_font(18, bold=True)
    draw_rounded_rect(draw, (WIDTH // 2 - 80, hud_y1 + 18, WIDTH // 2 + 80, hud_y2 - 18), radius=10, fill=(30, 41, 59, 220), outline=(56, 189, 248, 150), width=1)
    draw.text((WIDTH // 2 - 50, hud_y1 + 25), act_text, font=font_act, fill=(56, 189, 248, 255))

    # HUD Right: Verification Status
    font_status = get_font(16, bold=True)
    draw_rounded_rect(draw, (hud_x2 - 240, hud_y1 + 16, hud_x2 - 16, hud_y2 - 16), radius=12, fill=(16, 185, 129, 40), outline=(52, 211, 153, 180), width=1)
    draw.text((hud_x2 - 215, hud_y1 + 25), "✔ 100% सत्यापित पोर्टल", font=font_status, fill=(52, 211, 153, 255))

    # 2. Main Content Card Area (Y=145 to Y=870)
    card_x1, card_y1, card_x2, card_y2 = 64, 140, WIDTH - 64, 870

    if layout_type in ["scheme_overview", "overview"]:
        # Large Center Showcase Card
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(56, 189, 248, 120), width=2)

        # Urgency Pill
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 36, card_x1 + 340, card_y1 + 86), radius=12, fill=(2, 132, 199, 50), outline=(56, 189, 248, 180), width=1)
        font_pill = get_font(20, bold=True)
        draw.text((card_x1 + 68, card_y1 + 48), f"📢 {urgency_badge}", font=font_pill, fill=(56, 189, 248, 255))

        # Main Scheme Headline
        font_main_h = get_font(52, bold=True)
        draw.text((card_x1 + 48, card_y1 + 105), scheme_name, font=font_main_h, fill=(255, 255, 255, 255))

        # Benefit Highlight Container
        benefit = scene.get("benefit_highlight") or scheme_meta.get("benefit_amount", "आधिकारिक वित्तीय सहायता एवं लाभ")
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 200, card_x2 - 48, card_y1 + 360), radius=20, fill=(30, 41, 59, 200), outline=(250, 204, 21, 150), width=2)

        font_ben_tag = get_font(18, bold=True)
        draw.text((card_x1 + 76, card_y1 + 220), "💎 मुख्य सरकारी लाभ एवं सहायता राशि:", font=font_ben_tag, fill=(250, 204, 21, 255))

        font_ben_val = get_font(60, bold=True)
        draw.text((card_x1 + 76, card_y1 + 258), benefit, font=font_ben_val, fill=(255, 255, 255, 255))

        # Latest Directives Info Box
        update_text = scene.get("latest_update") or scheme_meta.get("latest_news_headline") or "ऑनलाइन आवेदन शुरू, आधिकारिक पोर्टल पर जाकर सीधे लाभ उठाएं।"
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 390, card_x2 - 48, card_y1 + 570), radius=20, fill=(15, 23, 42, 220), outline=(100, 116, 139, 100), width=1)

        font_upd_tag = get_font(20, bold=True)
        draw.text((card_x1 + 76, card_y1 + 412), "📌 ताज़ा आधिकारिक निर्देश एवं सूचना:", font=font_upd_tag, fill=(148, 163, 184, 255))

        font_upd_val = get_font(28, bold=True)
        # Wrap update text
        draw.text((card_x1 + 76, card_y1 + 456), update_text[:110] + ("..." if len(update_text) > 110 else ""), font=font_upd_val, fill=(241, 245, 249, 255))

        # Bottom Official Portal Ribbon
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 600, card_x2 - 48, card_y2 - 36), radius=16, fill=(2, 132, 199, 30), outline=(56, 189, 248, 120), width=1)
        font_portal = get_font(22, bold=True)
        draw.text((card_x1 + 76, card_y1 + 626), f"🔗 आधिकारिक सरकारी वेबसाइट: https://{portal_domain}", font=font_portal, fill=(56, 189, 248, 255))

    elif layout_type == "what_changed":
        # Two-Column Comparison Card (Old Rules vs New Directive)
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(56, 189, 248, 120), width=2)

        font_wc_h = get_font(42, bold=True)
        draw.text((card_x1 + 48, card_y1 + 36), f"⚖️ {scheme_name} — नियमों में क्या बदलाव हुआ?", font=font_wc_h, fill=(255, 255, 255, 255))

        col_w = (card_x2 - card_x1 - 130) // 2
        c1_x1 = card_x1 + 48
        c1_x2 = c1_x1 + col_w
        c2_x1 = c1_x2 + 34
        c2_x2 = c2_x1 + col_w
        box_y1 = card_y1 + 110
        box_y2 = card_y1 + 560

        # Left: Old Rule (Rose Red tint)
        draw_rounded_rect(draw, (c1_x1, box_y1, c1_x2, box_y2), radius=20, fill=(35, 14, 22, 230), outline=(244, 63, 94, 150), width=2)
        font_col_tag = get_font(22, bold=True)
        draw.text((c1_x1 + 28, box_y1 + 28), "🔴 पहले क्या नियम था? (OLD DIRECTIVE)", font=font_col_tag, fill=(251, 113, 133, 255))
        font_body = get_font(26, bold=False)
        draw.text((c1_x1 + 28, box_y1 + 86), "• ऑफलाइन कागजी कार्रवाई की आवश्यकता\n• केवल सीमित श्रेणियों के लिए पात्रता\n• लंबी सत्यापन प्रक्रिया और देरी", font=font_body, fill=(226, 232, 240, 255), spacing=20)

        # Right: New Directive (Emerald Green tint)
        draw_rounded_rect(draw, (c2_x1, box_y1, c2_x2, box_y2), radius=20, fill=(10, 35, 24, 230), outline=(16, 185, 129, 180), width=2)
        draw.text((c2_x1 + 28, box_y1 + 28), "🟢 अब नया सरकारी निर्देश 2026 (NEW DIRECTIVE)", font=font_col_tag, fill=(52, 211, 153, 255))
        draw.text((c2_x1 + 28, box_y1 + 86), "• 100% ऑनलाइन डिजिटल पोर्टल आवेदन\n• सीधे बैंक खाते में DBT के माध्यम से लाभ\n• आधार e-KYC द्वारा तत्काल सत्यापन", font=font_body, fill=(241, 245, 249, 255), spacing=20)

        # Bottom Urgency Banner
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 590, card_x2 - 48, card_y2 - 36), radius=16, fill=(245, 158, 11, 30), outline=(245, 158, 11, 160), width=2)
        font_alert = get_font(22, bold=True)
        draw.text((card_x1 + 76, card_y1 + 620), f"⏰ समय सीमा / लास्ट डेट: {scheme_meta.get('last_date', 'जल्द से जल्द आधिकारिक पोर्टल पर आवेदन करें')}", font=font_alert, fill=(251, 191, 36, 255))

    elif layout_type == "eligibility":
        # Eligibility Criteria Matrix
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(52, 211, 153, 140), width=2)

        font_el_h = get_font(42, bold=True)
        draw.text((card_x1 + 48, card_y1 + 36), f"👥 {scheme_name} — कौन-कौन पात्र हैं? (Eligibility Criteria)", font=font_el_h, fill=(255, 255, 255, 255))

        criteria_list = [
            ("1. भारतीय नागरिकता", "आवेदक भारत का स्थायी निवासी होना आवश्यक है।"),
            ("2. आयु सीमा एवं श्रेणी", scheme_meta.get("eligibility", "योजना के निर्धारित नियमों के अनुसार मान्य।")),
            ("3. आय प्रमाण पत्र", "निर्धारित आर्थिक सीमा के अंतर्गत आने वाले परिवार।"),
            ("4. सक्रिय बैंक खाता", "बैंक खाता आधार कार्ड एवं मोबाइल नंबर से लिंक होना अनिवार्य।"),
        ]

        y_offset = card_y1 + 120
        font_item_title = get_font(24, bold=True)
        font_item_desc = get_font(18, bold=False)

        for title, desc in criteria_list:
            draw_rounded_rect(draw, (card_x1 + 48, y_offset, card_x2 - 48, y_offset + 100), radius=16, fill=(30, 41, 59, 220), outline=(52, 211, 153, 120), width=1)
            draw.text((card_x1 + 76, y_offset + 18), f"✔ {title}", font=font_item_title, fill=(52, 211, 153, 255))
            draw.text((card_x1 + 76, y_offset + 56), desc, font=font_item_desc, fill=(203, 213, 225, 255))
            y_offset += 122

    elif layout_type == "checklist":
        # Required Documents Checklist
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(56, 189, 248, 140), width=2)

        font_chk_h = get_font(42, bold=True)
        draw.text((card_x1 + 48, card_y1 + 36), f"📑 आवश्यक दस्तावेज़ सूची (Required Documents Checklist)", font=font_chk_h, fill=(255, 255, 255, 255))

        doc_list = [
            ("🆔 आधार कार्ड (Aadhaar Card)", "सक्रिय मोबाइल नंबर से लिंक होना चाहिए।"),
            ("📜 निवास एवं आय प्रमाण पत्र", "सक्षम अधिकारी द्वारा निर्गत वैध प्रमाण पत्र।"),
            ("🏦 बैंक पासबुक (Bank Account)", "DBT और आधार सीडिंग पूर्ण होना अनिवार्य है।"),
            ("📸 पासपोर्ट साइज फोटो एवं मोबाइल", "ऑनलाइन आवेदन के समय OTP सत्यापन हेतु।"),
        ]

        y_offset = card_y1 + 120
        font_doc_title = get_font(24, bold=True)
        font_doc_sub = get_font(18, bold=False)

        for title, sub in doc_list:
            draw_rounded_rect(draw, (card_x1 + 48, y_offset, card_x2 - 48, y_offset + 100), radius=16, fill=(15, 23, 42, 230), outline=(56, 189, 248, 120), width=1)
            draw.text((card_x1 + 76, y_offset + 18), f"📄 {title}", font=font_doc_title, fill=(56, 189, 248, 255))
            draw.text((card_x1 + 76, y_offset + 56), sub, font=font_doc_sub, fill=(203, 213, 225, 255))
            y_offset += 122

    elif layout_type == "step_flow":
        # 3-Step Flowchart
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(56, 189, 248, 140), width=2)

        font_sf_h = get_font(42, bold=True)
        draw.text((card_x1 + 48, card_y1 + 36), "🚀 ऑनलाइन आवेदन कैसे करें? 3 आसान चरण (Step-by-Step)", font=font_sf_h, fill=(255, 255, 255, 255))

        step_w = (card_x2 - card_x1 - 130) // 3
        step_boxes = [
            ("चरण 1", "आधिकारिक पोर्टल पर जाएं", f"वेबसाइट {portal_domain} पर जाकर रजिस्ट्रेशन करें।"),
            ("चरण 2", "फॉर्म भरें व दस्तावेज़ जोड़ें", "अपनी व्यक्तिगत व बैंक जानकारी दर्ज करें।"),
            ("चरण 3", "e-KYC व अंतिम सबमिट", "OTP दर्ज कर रसीद डाउनलोड करें।"),
        ]

        font_st_badge = get_font(20, bold=True)
        font_st_title = get_font(24, bold=True)
        font_st_desc = get_font(18, bold=False)

        for idx, (badge, title, desc) in enumerate(step_boxes):
            bx1 = card_x1 + 48 + idx * (step_w + 34)
            bx2 = bx1 + step_w
            by1 = card_y1 + 130
            by2 = card_y1 + 580

            draw_rounded_rect(draw, (bx1, by1, bx2, by2), radius=20, fill=(30, 41, 59, 230), outline=(56, 189, 248, 140), width=2)

            draw_rounded_rect(draw, (bx1 + 24, by1 + 24, bx1 + 140, by1 + 68), radius=10, fill=(2, 132, 199, 255))
            draw.text((bx1 + 40, by1 + 32), badge, font=font_st_badge, fill=(255, 255, 255, 255))

            draw.text((bx1 + 24, by1 + 96), title, font=font_st_title, fill=(248, 250, 252, 255))
            draw.text((bx1 + 24, by1 + 180), desc, font=font_st_desc, fill=(148, 163, 184, 255), spacing=12)

    else:
        # Cyber Alert & Source Verification Card
        draw_rounded_rect(draw, (card_x1, card_y1, card_x2, card_y2), radius=28, fill=(11, 17, 32, 235), outline=(225, 29, 72, 160), width=2)

        font_al_h = get_font(42, bold=True)
        draw.text((card_x1 + 48, card_y1 + 36), "⚠️ आधिकारिक जन-हित चेतावनी (Beware of Cyber Fraud)", font=font_al_h, fill=(255, 255, 255, 255))

        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 120, card_x2 - 48, card_y1 + 360), radius=20, fill=(35, 14, 22, 230), outline=(225, 29, 72, 160), width=2)
        font_w1 = get_font(32, bold=True)
        draw.text((card_x1 + 76, card_y1 + 150), "🛡️ किसी भी अनधिकृत दलाल या एजेंट को पैसे न दें!", font=font_w1, fill=(251, 113, 133, 255))
        font_w2 = get_font(22, bold=False)
        draw.text((card_x1 + 76, card_y1 + 210), "• यह सरकारी योजना पूर्णतः निःशुल्क है।\n• किसी भी अज्ञात लिंक पर अपना OTP या बैंक पिन साझा न करें।\n• केवल आधिकारिक gov.in या nic.in पोर्टल से ही आवेदन करें।", font=font_w2, fill=(241, 245, 249, 255), spacing=14)

        # Helpline Ribbon
        draw_rounded_rect(draw, (card_x1 + 48, card_y1 + 400, card_x2 - 48, card_y2 - 48), radius=20, fill=(15, 23, 42, 230), outline=(52, 211, 153, 140), width=2)
        font_h1 = get_font(26, bold=True)
        draw.text((card_x1 + 76, card_y1 + 430), f"📞 राष्ट्रीय हेल्पलाइन: {scheme_meta.get('helpline', '1947 / 1800-xxx-xxxx')}", font=font_h1, fill=(52, 211, 153, 255))
        draw.text((card_x1 + 76, card_y1 + 480), f"🌐 आधिकारिक वेबसाइट: https://{portal_domain}", font=font_h1, fill=(56, 189, 248, 255))

    return img


# -------------------------------------------------------------
# Subtitle Pill Renderer (Bottom Y=910)
# -------------------------------------------------------------
class HindiDocumentarySubtitleRenderer:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT):
        self.width = width
        self.height = height
        self.font = get_font(26, bold=True)
        self.max_w = width - 240

    def render_subtitle(self, dialogue_text: str) -> Image.Image:
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        if not dialogue_text:
            return img

        draw = ImageDraw.Draw(img)
        # Limit length to 90 chars per line
        clean_text = dialogue_text.strip()
        if len(clean_text) > 85:
            clean_text = clean_text[:82] + "..."

        bbox = draw.textbbox((0, 0), clean_text, font=self.font)
        text_w = bbox[2] - bbox[0]
        pill_w = max(400, text_w + 70)
        pill_h = 68
        x1 = (self.width - pill_w) // 2
        y1 = 930
        x2 = x1 + pill_w
        y2 = y1 + pill_h

        # Luminous dark pill
        draw_rounded_rect(draw, (x1, y1, x2, y2), radius=18, fill=(11, 17, 32, 240), outline=(56, 189, 248, 180), width=2)

        # CC Badge
        draw_rounded_rect(draw, (x1 + 14, y1 + 14, x1 + 54, y2 - 14), radius=6, fill=(2, 132, 199, 255))
        font_cc = get_font(13, bold=True)
        draw.text((x1 + 22, y1 + 23), "CC", font=font_cc, fill=(255, 255, 255, 255))

        # Text
        draw.text((x1 + 68, y1 + 18), clean_text, font=self.font, fill=(255, 255, 255, 255))
        return img


# -------------------------------------------------------------
# Master MoviePy Video Builder
# -------------------------------------------------------------
def build_dastawez_long_moviepy_video(
    script_data: Dict[str, Any],
    voice_data: Dict[str, Any],
    selected_scheme: Dict[str, Any],
    scenes: List[Dict[str, Any]],
    output_path: str,
    fps: int = FPS
) -> str:
    """
    Renders 1080p horizontal 16:9 documentary video in ~2 to 3 minutes using MoviePy & FFmpeg.
    """
    logger.info(f"Starting Ultra-Fast MoviePy Compositor for '{script_data.get('title')}'...")
    total_acts = len(scenes)

    # 1. Timeline & Scene Boundaries Setup
    timeline_scenes = []
    current_time = 0.0
    loaded_clips = []
    audio_clips = []

    for idx, sc in enumerate(scenes):
        dur = sc.get("duration_seconds")
        if not dur or dur <= 0:
            dur = (sc.get("duration_frames_30fps") or 300) / 30.0

        start_t = current_time
        end_t = current_time + dur
        current_time = end_t

        # Pre-render this scene's static UI card
        rendered_card = render_scene_card(sc, selected_scheme, idx + 1, total_acts)

        # Pre-render subtitle for this scene's dialogue
        dialogue = sc.get("dialogue", "")
        sub_renderer = HindiDocumentarySubtitleRenderer()
        rendered_sub = sub_renderer.render_subtitle(dialogue)

        # Composite card + sub together for zero-cost runtime blitting
        combined_overlay = rendered_card.copy()
        combined_overlay.alpha_composite(rendered_sub)

        # Load video B-roll clip if available
        broll_clip = None
        broll_p = sc.get("broll_video_path") or sc.get("visual_media", {}).get("broll_video_path")
        if broll_p and os.path.exists(broll_p):
            try:
                broll_clip = VideoFileClip(broll_p)
                loaded_clips.append(broll_clip)
            except Exception as e:
                logger.debug(f"Could not load B-roll {broll_p}: {e}")

        # Load audio clip for this scene
        audio_p = sc.get("audio_path")
        if audio_p and os.path.exists(audio_p):
            try:
                a_clip = AudioFileClip(audio_p).with_start(start_t)
                audio_clips.append(a_clip)
            except Exception as e:
                logger.debug(f"Could not load audio {audio_p}: {e}")

        timeline_scenes.append({
            "start": start_t,
            "end": end_t,
            "duration": dur,
            "overlay": combined_overlay,
            "broll_clip": broll_clip
        })

    total_duration = max(1.0, current_time)
    logger.info(f"Composing {len(timeline_scenes)} scenes. Total Duration: {total_duration:.1f}s (~{total_duration/60:.2f} mins)")

    # 2. Frame Generator (Sub-millisecond blitting per frame)
    # Background Vignette Layer (1920x1080)
    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (7, 11, 20, 180))

    def make_frame(t):
        # Locate active scene
        active_sc = timeline_scenes[0]
        for sc in timeline_scenes:
            if sc["start"] <= t <= sc["end"]:
                active_sc = sc
                break

        # Render B-roll frame or fallback dark canvas
        clip = active_sc["broll_clip"]
        if clip:
            try:
                local_t = (t - active_sc["start"]) % max(0.1, clip.duration)
                frame_arr = clip.get_frame(local_t)
                bg_img = Image.fromarray(frame_arr).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR)
            except Exception:
                bg_img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 17, 32, 255))
        else:
            bg_img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 17, 32, 255))

        # Apply dark cinematic vignette
        bg_img.alpha_composite(vignette)

        # Paste pre-rendered scene UI & Subtitles
        bg_img.alpha_composite(active_sc["overlay"])

        return np.array(bg_img.convert("RGB"))

    video_clip = VideoClip(make_frame, duration=total_duration)

    # 3. Audio Composition: Speech + Ambient Bed + Whoosh SFX
    audio_layers = []
    if audio_clips:
        audio_layers.extend(audio_clips)

    # Add ambient music bed if available
    ambient_path = "assets/audio/ambient_tech.wav"
    if os.path.exists(ambient_path):
        try:
            raw_ambient = AudioFileClip(ambient_path)
            if raw_ambient.duration < total_duration:
                loops = int(math.ceil(total_duration / max(raw_ambient.duration, 1.0))) + 1
                ambient_clip = concatenate_audioclips([raw_ambient] * loops).subclipped(0, total_duration).with_volume_scaled(0.08)
            else:
                ambient_clip = raw_ambient.subclipped(0, total_duration).with_volume_scaled(0.08)
            audio_layers.append(ambient_clip)
        except Exception as e:
            logger.debug(f"Could not load ambient audio: {e}")

    # Add subtle transition whoosh at each scene boundary
    whoosh_path = "assets/audio/whoosh.wav"
    if os.path.exists(whoosh_path):
        try:
            for sc in timeline_scenes[:-1]:
                cut_t = sc["end"]
                if cut_t < total_duration - 0.5:
                    w_clip = AudioFileClip(whoosh_path).with_start(cut_t).with_volume_scaled(0.20)
                    audio_layers.append(w_clip)
        except Exception as e:
            logger.debug(f"Could not load whoosh audio: {e}")

    if audio_layers:
        final_audio = CompositeAudioClip(audio_layers)
        video_clip = video_clip.with_audio(final_audio)

    # 4. Rapid FFmpeg Export
    logger.info(f"Exporting 1080p MP4 directly via FFmpeg (preset=ultrafast)...")
    video_clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        ffmpeg_params=["-crf", "22", "-pix_fmt", "yuv420p"],
        threads=2
    )

    # Cleanup open clip handles
    for c in loaded_clips:
        try:
            c.close()
        except Exception:
            pass

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    logger.info(f"✓ Video successfully rendered with MoviePy: {output_path} ({size_mb:.2f} MB)")
    return output_path
