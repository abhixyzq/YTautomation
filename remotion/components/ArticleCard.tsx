import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Video } from "remotion";

interface ArticleCardProps {
  brollPath?: string;
  source?: string;
  headline?: string;
  quote?: string;
}

export const ArticleCard: React.FC<ArticleCardProps> = ({
  brollPath,
  source = "INVESTIGATIVE DISCLOSURE",
  headline = "UNPRECEDENTED TECH INFRASTRUCTURE ANOMALY REPORTED",
  quote = "Engineering telemetry reveals cascading failures triggered by manual overrides.",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 3D Card Spring Entrance
  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 13, mass: 0.7, stiffness: 100 },
  });

  const cardRotateY = interpolate(cardSpring, [0, 1], [-12, 0]);
  const cardTranslateX = interpolate(cardSpring, [0, 1], [60, 0]);
  const cardOpacity = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: "clamp" });

  // Ken Burns zoom on left B-roll
  const brollZoom = 1.0 + (frame / 300) * 0.05;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#070b14",
        display: "flex",
        flexDirection: "row",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Left 45% Pane: 16:9 Video Footage */}
      <div
        style={{
          width: "48%",
          height: "100%",
          position: "relative",
          overflow: "hidden",
          borderRight: "3px solid rgba(0, 229, 255, 0.4)",
          boxShadow: "10px 0 30px rgba(0,0,0,0.8)",
        }}
      >
        {brollPath ? (
          <Video
            src={brollPath}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${brollZoom})`,
            }}
          />
        ) : (
          <div style={{ width: "100%", height: "100%", background: "#0f172a" }} />
        )}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to right, transparent 60%, rgba(7, 11, 20, 0.7) 100%)",
          }}
        />
      </div>

      {/* Right 52% Pane: 3D Frosted Glass Article Card */}
      <div
        style={{
          width: "52%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px",
          perspective: "1200px",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            width: "100%",
            maxHeight: "92%",
            background: "rgba(13, 20, 36, 0.85)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid rgba(251, 191, 36, 0.6)",
            boxShadow: "0 20px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(251, 191, 36, 0.2)",
            borderRadius: "24px",
            padding: "36px 42px",
            display: "flex",
            flexDirection: "column",
            gap: "20px",
            transform: `translateX(${cardTranslateX}px) rotateY(${cardRotateY}deg)`,
            opacity: cardOpacity,
            boxSizing: "border-box",
          }}
        >
          {/* Header Badge */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div
              style={{
                background: "linear-gradient(135deg, #e11d48, #be123c)",
                border: "1px solid #fecdd3",
                borderRadius: "12px",
                padding: "8px 20px",
                color: "#ffffff",
                fontSize: "18px",
                fontWeight: 800,
                letterSpacing: "2px",
                textTransform: "uppercase",
              }}
            >
              ● {source}
            </div>
            <div style={{ color: "#94a3b8", fontSize: "16px", fontWeight: 600, letterSpacing: "1px" }}>
              VERIFIED ARCHIVE
            </div>
          </div>

          {/* Headline */}
          <h2
            style={{
              margin: 0,
              fontSize: "36px",
              fontWeight: 800,
              color: "#ffffff",
              lineHeight: 1.25,
              fontFamily: "system-ui, -apple-system, sans-serif",
              letterSpacing: "0.5px",
            }}
          >
            {headline}
          </h2>

          <div style={{ width: "100%", height: "1px", background: "rgba(148, 163, 184, 0.2)" }} />

          {/* Quote Callout Box */}
          <div
            style={{
              background: "rgba(22, 33, 62, 0.9)",
              border: "1px solid rgba(251, 191, 36, 0.4)",
              borderRadius: "16px",
              padding: "24px 28px",
              position: "relative",
              borderLeft: "6px solid #fbbf24",
            }}
          >
            <div style={{ color: "#fbbf24", fontSize: "40px", lineHeight: "20px", fontWeight: 900 }}>“</div>
            <p
              style={{
                margin: "10px 0 0 0",
                fontSize: "26px",
                fontWeight: 500,
                color: "#fef08a",
                lineHeight: 1.4,
                fontStyle: "italic",
                fontFamily: "system-ui, -apple-system, sans-serif",
              }}
            >
              {quote}
            </p>
          </div>

          {/* Footer */}
          <div style={{ color: "#64748b", fontSize: "16px", fontWeight: 600, letterSpacing: "1px" }}>
            SILICON VALLEY BUREAU  •  INTERNAL TELEMETRY DISCLOSURE
          </div>
        </div>
      </div>
    </div>
  );
};
