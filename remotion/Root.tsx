import React from "react";
import { Composition, Still } from "remotion";
import { TechShow } from "./TechShow";
import { TechShowProps } from "./types";
import { Thumbnail, ThumbnailProps } from "./Thumbnail";
import { DastawezShow } from "./dastawez/DastawezShow";
import { DastawezShowProps } from "./dastawez/types";
import { DastawezThumbnail, DastawezThumbnailProps } from "./dastawez/DastawezThumbnail";

const defaultProps: TechShowProps = {
  title: "High-IQ Tech Explainer",
  duration: 60,
  audio_path: "",
  ambient_path: "",
  scenes: [
    {
      dialogue: "In modern computing, the most catastrophic failures begin with a single overlooked assumption.",
      layout_type: "fullscreen_broll",
      chapter_id: 1,
      chapter_title: "The Impossible Paradox",
      chapter_subtitle: "The Mathematical Limit",
      start: 0,
      end: 4,
    },
    {
      dialogue: "According to reports, infrastructure was severely impacted.",
      layout_type: "splitscreen_article",
      chapter_id: 1,
      chapter_title: "Cold Open Roast",
      chapter_subtitle: "The Billion Dollar Blunder",
      article_source: "FINANCIAL TIMES",
      article_headline: "MASSIVE INFRASTRUCTURE COLLAPSE REPORTED",
      article_quote: "Engineers confirmed manual overrides bypassed critical safety gates.",
      start: 4,
      end: 12,
    },
    {
      dialogue: "Notice the damage scale.",
      layout_type: "splitscreen_stat",
      chapter_id: 1,
      chapter_title: "Cold Open Roast",
      chapter_subtitle: "The Billion Dollar Blunder",
      stat_number: "$1.2 BILLION",
      stat_label: "ESTIMATED INCIDENT LOSS",
      stat_context: "Single Friday deployment failure caused widespread outage.",
      stat_change: "+340% SURPLUS RISK",
      start: 12,
      end: 20,
    },
    {
      dialogue: "Management reaction was predictable.",
      layout_type: "meme_reaction",
      chapter_id: 1,
      chapter_title: "Cold Open Roast",
      chapter_subtitle: "The Billion Dollar Blunder",
      meme_punchline: "THIS IS FINE",
      start: 20,
      end: 28,
    },
    {
      dialogue: "Remember to test your software before prod tests you.",
      layout_type: "fullscreen_broll",
      chapter_id: 1,
      chapter_title: "Cold Open Roast",
      chapter_subtitle: "The Billion Dollar Blunder",
      start: 28,
      end: 60,
    },
  ],
  word_timings: [],
  phrases: [],
};

const defaultThumbProps: ThumbnailProps = {
  category: "AEROSPACE FORENSICS",
  hookTitle: "THE 64-BIT",
  hookHighlight: "GLITCH",
  subtitle: "How a single 10-line software shortcut destroyed a $500,000,000 rocket in 37 seconds.",
  badge: "⚠️ MISSION STATUS: CRITICAL DETONATION",
  accentColor: "#00f0ff",
};

const defaultDastawezProps: DastawezShowProps = {
  title: "आयुष्मान भारत योजना 2026",
  scheme_id: "ayushman_senior_citizen_2026",
  category: "स्वास्थ्य एवं परिवार कल्याण मंत्रालय",
  scenes: [
    {
      scene_id: 1,
      act_name: "योजना परिचय एवं लाभ",
      dialogue: "नमस्कार, iDastawez पर आपका स्वागत है।",
      layout_type: "scheme_overview",
      scheme_name: "आयुष्मान भारत - वरिष्ठ नागरिक ₹5 लाख मुफ्त इलाज योजना",
      ministry: "स्वास्थ्य एवं परिवार कल्याण मंत्रालय (MoHFW)",
      benefit_highlight: "₹5,00,000 प्रति वर्ष मुफ्त इलाज",
      latest_update: "केंद्रीय कैबिनेट द्वारा 70 वर्ष से अधिक आयु के सभी बुजुर्गों के लिए नया आयुष्मान कार्ड जारी।",
      portal_url: "https://beneficiary.nha.gov.in",
      urgency_badge: "ताज़ा घोषणा 2026",
      duration_seconds: 10,
      duration_frames_30fps: 300,
    },
  ],
};

const defaultDastawezThumbProps: DastawezThumbnailProps = {
  scheme_name: "आयुष्मान भारत वरिष्ठ नागरिक योजना 2026",
  big_benefit: "₹5,00,000 मुफ्त इलाज",
  urgency_badge: "70+ बुजुर्गों के लिए नया नियम",
  portal_name: "beneficiary.nha.gov.in",
  helpline: "14555",
  rule_change_badge: "100% आधिकारिक फैसला",
};

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="TechShowLandscape"
        component={TechShow}
        durationInFrames={30 * 60}
        fps={30}
        width={1920}
        height={1080}
        calculateMetadata={async ({ props }) => {
          const durationSec = (props as TechShowProps).duration || 60;
          return {
            durationInFrames: Math.max(30, Math.ceil(durationSec * 30)),
            props,
          };
        }}
        defaultProps={defaultProps}
      />
      <Still
        id="ThumbnailLandscape"
        component={Thumbnail}
        width={1280}
        height={720}
        defaultProps={defaultThumbProps}
      />

      {/* iDastawez Compositions */}
      <Composition
        id="DastawezLandscape"
        component={DastawezShow}
        durationInFrames={30 * 210}
        fps={30}
        width={1920}
        height={1080}
        calculateMetadata={async ({ props }) => {
          const dastawezProps = props as DastawezShowProps;
          const totalFrames = (dastawezProps.scenes || []).reduce(
            (acc, sc) => acc + (sc.duration_frames_30fps || Math.round((sc.duration_seconds || 5) * 30)),
            0
          );
          return {
            durationInFrames: Math.max(90, totalFrames || 300),
            props,
          };
        }}
        defaultProps={defaultDastawezProps}
      />
      <Still
        id="DastawezThumbnail"
        component={DastawezThumbnail}
        width={1280}
        height={720}
        defaultProps={defaultDastawezThumbProps}
      />
    </>
  );
};
