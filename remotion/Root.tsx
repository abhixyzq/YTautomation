import React from "react";
import { Composition, Still } from "remotion";
import { TechShow } from "./TechShow";
import { TechShowProps } from "./types";
import { Thumbnail, ThumbnailProps } from "./Thumbnail";

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
    </>
  );
};
