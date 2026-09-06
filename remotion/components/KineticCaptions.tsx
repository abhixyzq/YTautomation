import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Phrase, WordTiming } from "../types";

interface KineticCaptionsProps {
  phrases?: Phrase[];
  currentTime: number;
}

export const KineticCaptions: React.FC<KineticCaptionsProps> = ({
  phrases = [],
  currentTime,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Find active phrase
  const activePhrase = phrases.find(
    (p) => p.start <= currentTime && currentTime <= p.end
  );

  if (!activePhrase || !activePhrase.words.length) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        bottom: "80px",
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        pointerEvents: "none",
        zIndex: 50,
      }}
    >
      {/* Frosted Glass Subtitle Pill */}
      <div
        style={{
          background: "rgba(10, 15, 26, 0.88)",
          backdropFilter: "blur(16px)",
          WebkitBackdropFilter: "blur(16px)",
          border: "2px solid rgba(0, 235, 255, 0.4)",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 235, 255, 0.2)",
          borderRadius: "18px",
          padding: "14px 34px",
          display: "flex",
          flexDirection: "row",
          gap: "14px",
          alignItems: "center",
        }}
      >
        {activePhrase.words.map((w, idx) => {
          const isActive = w.start <= currentTime && currentTime <= w.end;
          const wordFrame = Math.max(0, Math.floor((currentTime - w.start) * fps));
          
          const wordSpring = isActive
            ? spring({
                frame: wordFrame,
                fps,
                config: { damping: 10, mass: 0.4, stiffness: 180 },
              })
            : 1;

          const scale = isActive ? 1.0 + wordSpring * 0.18 : 1.0;
          const color = isActive ? "#fef08a" : "#ffffff";
          const textShadow = isActive
            ? "0 0 20px rgba(254, 240, 138, 0.8), 0 2px 8px rgba(0,0,0,0.9)"
            : "0 2px 6px rgba(0, 0, 0, 0.8)";

          return (
            <span
              key={idx}
              style={{
                fontSize: "34px",
                fontWeight: 800,
                color,
                textShadow,
                transform: `scale(${scale})`,
                display: "inline-block",
                fontFamily: "system-ui, -apple-system, sans-serif",
                letterSpacing: "0.5px",
              }}
            >
              {w.word.toUpperCase()}
            </span>
          );
        })}
      </div>
    </div>
  );
};
