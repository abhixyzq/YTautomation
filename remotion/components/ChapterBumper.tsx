import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface ChapterBumperProps {
  chapterNo: number;
  chapterTitle: string;
  subtitle: string;
}

export const ChapterBumper: React.FC<ChapterBumperProps> = ({
  chapterNo,
  chapterTitle,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring physics for entrance
  const cardScale = spring({
    frame,
    fps,
    config: { damping: 14, mass: 0.6, stiffness: 120 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], { extrapolateRight: "clamp" });
  const glowPulse = Math.sin(frame / 6) * 10 + 20;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#070b14",
        backgroundImage: `
          linear-gradient(to right, rgba(0, 235, 255, 0.05) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(0, 235, 255, 0.05) 1px, transparent 1px)
        `,
        backgroundSize: "80px 80px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Center Radial Glow */}
      <div
        style={{
          position: "absolute",
          width: 900,
          height: 600,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0, 229, 255, 0.12) 0%, rgba(225, 29, 72, 0.08) 40%, transparent 70%)",
          filter: "blur(60px)",
        }}
      />

      {/* Main Bumper Content Card with Spring Physics */}
      <div
        style={{
          transform: `scale(${cardScale})`,
          opacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          zIndex: 2,
        }}
      >
        {/* Chapter Pill Badge */}
        <div
          style={{
            background: "linear-gradient(135deg, #e11d48 0%, #be123c 100%)",
            border: "2px solid #fda4af",
            boxShadow: `0 0 ${glowPulse}px rgba(225, 29, 72, 0.6)`,
            borderRadius: "16px",
            padding: "10px 28px",
            color: "#ffffff",
            fontSize: "24px",
            fontWeight: 800,
            letterSpacing: "3px",
            textTransform: "uppercase",
            marginBottom: "28px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <span style={{ color: "#ffffff", fontSize: "20px" }}>●</span>
          CHAPTER {String(chapterNo).padStart(2, "0")} OF 05
        </div>

        {/* Title */}
        <h1
          style={{
            margin: 0,
            fontSize: "76px",
            fontWeight: 900,
            color: "#ffffff",
            letterSpacing: "4px",
            textTransform: "uppercase",
            textAlign: "center",
            textShadow: "0 10px 30px rgba(0, 0, 0, 0.9), 0 0 40px rgba(0, 235, 255, 0.3)",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {chapterTitle}
        </h1>

        {/* Neon Accent Divider Bar */}
        <div
          style={{
            width: "500px",
            height: "4px",
            background: "linear-gradient(90deg, transparent, #00e5ff, transparent)",
            boxShadow: "0 0 20px #00e5ff",
            margin: "24px 0",
          }}
        />

        {/* Subtitle */}
        <h2
          style={{
            margin: 0,
            fontSize: "34px",
            fontWeight: 700,
            color: "#fbbf24",
            letterSpacing: "2px",
            textTransform: "uppercase",
            textAlign: "center",
            textShadow: "0 4px 15px rgba(0,0,0,0.8)",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {subtitle}
        </h2>
      </div>
    </div>
  );
};
