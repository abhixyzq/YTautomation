import React from "react";
import { interpolate, useCurrentFrame, Video } from "remotion";

interface CinematicBrollProps {
  brollPath?: string;
  badgeText?: string;
}

export const CinematicBroll: React.FC<CinematicBrollProps> = ({
  brollPath,
  badgeText = "● SPECIAL REPORT: TECH SATIRE",
}) => {
  const frame = useCurrentFrame();

  // Smooth continuous Ken Burns pan & zoom
  const zoom = 1.0 + (frame / 400) * 0.06;
  const panX = Math.sin(frame / 120) * 15;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#070b14",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* 4K Video Background */}
      {brollPath ? (
        <Video
          src={brollPath}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${zoom}) translateX(${panX}px)`,
          }}
        />
      ) : (
        <div style={{ width: "100%", height: "100%", background: "#0f172a" }} />
      )}

      {/* Top Gradient Vignette */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "160px",
          background: "linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, transparent 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Bottom Gradient Vignette for Subtitles */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "220px",
          background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Top-Left Broadcast Live Bug */}
      <div
        style={{
          position: "absolute",
          top: "40px",
          left: "50px",
          background: "linear-gradient(135deg, #e11d48, #be123c)",
          border: "1.5px solid #fda4af",
          borderRadius: "12px",
          padding: "8px 24px",
          color: "#ffffff",
          fontSize: "18px",
          fontWeight: 800,
          letterSpacing: "2px",
          textTransform: "uppercase",
          boxShadow: "0 6px 20px rgba(0, 0, 0, 0.6)",
        }}
      >
        {badgeText}
      </div>
    </div>
  );
};
