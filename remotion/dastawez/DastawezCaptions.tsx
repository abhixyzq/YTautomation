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
        bottom: 50,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 90,
      }}
    >
      {/* Frosted Dark Glass Pill with High-Contrast Typography */}
      <div
        style={{
          background: "rgba(6, 11, 22, 0.92)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1px solid rgba(59, 130, 246, 0.4)",
          boxShadow: "0 12px 36px rgba(0, 0, 0, 0.8), 0 0 20px rgba(37, 99, 235, 0.2)",
          borderRadius: 20,
          padding: "12px 32px",
          display: "flex",
          flexDirection: "row",
          gap: 14,
          alignItems: "center",
          maxWidth: 1400,
        }}
      >
        {/* Subtle CC Badge */}
        <div
          style={{
            background: "rgba(37, 99, 235, 0.25)",
            border: "1px solid rgba(59, 130, 246, 0.6)",
            borderRadius: 6,
            padding: "2px 8px",
            fontSize: 13,
            fontWeight: 800,
            color: "#60a5fa",
            letterSpacing: 1,
          }}
        >
          CC
        </div>

        {/* Phrase Words with Clean Active Emphasis */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
          {activePhrase.words.map((w, idx) => {
            const isSpoken = w.start <= effectiveTime && effectiveTime <= w.end;
            const color = isSpoken ? "#fde047" : "#ffffff";
            const scale = isSpoken ? 1.05 : 1.0;
            const weight = isSpoken ? 800 : 700;
            const textShadow = isSpoken
              ? "0 0 16px rgba(253, 224, 71, 0.6)"
              : "0 2px 6px rgba(0, 0, 0, 0.8)";

            return (
              <span
                key={idx}
                style={{
                  fontSize: 32,
                  fontWeight: weight,
                  color,
                  textShadow,
                  transform: `scale(${scale})`,
                  display: "inline-block",
                  fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                  transition: "all 0.08s ease-out",
                  letterSpacing: 0.3,
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
