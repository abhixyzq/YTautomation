import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Video } from "remotion";

interface MemeReactionProps {
  memePath?: string;
  punchline?: string;
}

export const MemeReaction: React.FC<MemeReactionProps> = ({
  memePath,
  punchline = "THIS IS FINE",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Bouncy Spring Pop-In Physics
  const popSpring = spring({
    frame,
    fps,
    config: { damping: 10, mass: 0.5, stiffness: 140 },
  });

  const bannerSpring = spring({
    frame: frame - 6,
    fps,
    config: { damping: 12, mass: 0.5, stiffness: 120 },
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#070b14",
        backgroundImage: `
          linear-gradient(to right, rgba(0, 235, 255, 0.04) 1px, transparent 1px),
          linear-gradient(to bottom, rgba(0, 235, 255, 0.04) 1px, transparent 1px)
        `,
        backgroundSize: "70px 70px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          transform: `scale(${popSpring})`,
          borderRadius: "20px",
          border: "4px solid #00e5ff",
          boxShadow: "0 0 50px rgba(0, 229, 255, 0.5), 0 20px 60px rgba(0,0,0,0.9)",
          overflow: "hidden",
          width: "960px",
          height: "620px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#000000",
        }}
      >
        {memePath ? (
          <Video
            src={memePath}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          <div style={{
            width: "100%",
            height: "100%",
            background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: "24px",
          }}>
            <div style={{ fontSize: "80px" }}>💀</div>
            <div style={{ color: "#94a3b8", fontSize: "24px", fontWeight: 700, letterSpacing: "2px", textTransform: "uppercase" }}>MEME UNAVAILABLE</div>
          </div>
        )}
      </div>

      {/* Punchline Banner with Spring Pop */}
      <div
        style={{
          transform: `scale(${Math.max(0, bannerSpring)})`,
          marginTop: "32px",
          background: "linear-gradient(135deg, #fbbf24, #f59e0b)",
          border: "3px solid #000000",
          boxShadow: "0 10px 35px rgba(0, 0, 0, 0.8), 0 0 25px rgba(251, 191, 36, 0.5)",
          borderRadius: "16px",
          padding: "14px 44px",
          color: "#000000",
          fontSize: "36px",
          fontWeight: 900,
          letterSpacing: "2px",
          textTransform: "uppercase",
          fontFamily: "system-ui, -apple-system, sans-serif",
          textAlign: "center",
        }}
      >
        {punchline}
      </div>
    </div>
  );
};
