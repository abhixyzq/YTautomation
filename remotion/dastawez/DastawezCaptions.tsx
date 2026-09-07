import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { Phrase, WordTiming } from "./types";

interface DastawezCaptionsProps {
  phrases?: Phrase[];
  currentTime?: number;
}

export const DastawezCaptions: React.FC<DastawezCaptionsProps> = ({
  phrases = [],
  currentTime,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const effectiveTime = currentTime !== undefined ? currentTime : frame / fps;

  if (!phrases || phrases.length === 0) {
    return null;
  }

  // Find active phrase based on current time
  const activePhrase = phrases.find(
    (p) => p.start <= effectiveTime && effectiveTime <= p.end
  );

  if (!activePhrase || !activePhrase.words || activePhrase.words.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        bottom: 20,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 90,
      }}
    >
      {/* Luminous Frosted Dark Glass Pill with High-Contrast Typography */}
      <div
        style={{
          background: "rgba(11, 17, 32, 0.96)",
          border: "1.5px solid rgba(56, 189, 248, 0.35)",
          boxShadow: "0 16px 42px rgba(0, 0, 0, 0.65), 0 0 20px rgba(56, 189, 248, 0.15)",
          borderRadius: 24,
          padding: "12px 34px",
          display: "flex",
          flexDirection: "row",
          gap: 14,
          alignItems: "center",
          maxWidth: 1400,
        }}
      >
        {/* GovTech Blue CC Badge */}
        <div
          style={{
            background: "linear-gradient(135deg, #0284c7, #2563eb)",
            borderRadius: 8,
            padding: "4px 10px",
            fontSize: 13,
            fontWeight: 900,
            color: "#ffffff",
            letterSpacing: 1,
            boxShadow: "0 2px 10px rgba(2, 132, 199, 0.4)",
          }}
        >
          CC
        </div>

        {/* Phrase Words with Clean Spoken Emphasis */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
          {activePhrase.words.map((w, idx) => {
            const isSpoken = w.start <= effectiveTime && effectiveTime <= w.end;
            const color = isSpoken ? "#facc15" : "#e2e8f0";
            const scale = isSpoken ? 1.08 : 1.0;
            const weight = isSpoken ? 900 : 700;
            const textShadow = isSpoken
              ? "0 0 18px rgba(250, 204, 21, 0.65)"
              : "none";

            return (
              <span
                key={idx}
                style={{
                  fontSize: 28,
                  fontWeight: weight,
                  color,
                  textShadow,
                  transform: `scale(${scale})`,
                  display: "inline-block",
                  fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif",
                  transition: "all 0.08s ease-out",
                  letterSpacing: 0.3,
                  background: isSpoken ? "rgba(250, 204, 21, 0.16)" : "transparent",
                  padding: isSpoken ? "2px 8px" : "0px",
                  borderRadius: 6,
                }}
              >
                {w.word}
              </span>
            );
          })}
        </div>
      </div>
    </div>
  );
};
