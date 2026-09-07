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
      {/* Luminous Frosted Glass Pill with High-Contrast Typography */}
      <div
        style={{
          background: "rgba(255, 255, 255, 0.94)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          border: "1px solid rgba(2, 132, 199, 0.35)",
          boxShadow: "0 14px 38px rgba(15, 23, 42, 0.12), 0 4px 12px rgba(2, 132, 199, 0.08)",
          borderRadius: 24,
          padding: "12px 32px",
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
            background: "linear-gradient(135deg, #1d4ed8, #0284c7)",
            borderRadius: 8,
            padding: "4px 10px",
            fontSize: 13,
            fontWeight: 900,
            color: "#ffffff",
            letterSpacing: 1,
            boxShadow: "0 2px 8px rgba(29, 78, 216, 0.3)",
          }}
        >
          CC
        </div>

        {/* Phrase Words with Clean Spoken Emphasis */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, alignItems: "center" }}>
          {activePhrase.words.map((w, idx) => {
            const isSpoken = w.start <= effectiveTime && effectiveTime <= w.end;
            const color = isSpoken ? "#ea580c" : "#1e293b";
            const scale = isSpoken ? 1.08 : 1.0;
            const weight = isSpoken ? 900 : 700;
            const textShadow = isSpoken
              ? "0 2px 10px rgba(234, 88, 12, 0.25)"
              : "none";

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
                  background: isSpoken ? "rgba(255, 237, 213, 0.75)" : "transparent",
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
