import React from "react";
import { Composition } from "remotion";
import { TechShow } from "./TechShow";
import { TechShowProps } from "./types";

const defaultProps: TechShowProps = {
  title: "Silicon Valley Satire Show",
  duration: 60,
  audio_path: "",
  ambient_path: "",
  scenes: [
    {
      dialogue: "Welcome back, software survivors.",
      layout_type: "chapter_bumper",
      chapter_id: 1,
      chapter_title: "Cold Open Roast",
      chapter_subtitle: "The Billion Dollar Blunder",
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
    </>
  );
};
