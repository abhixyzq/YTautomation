import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Video } from "remotion";

interface StatMetricCardProps {
  brollPath?: string;
  statNumber?: string;
  statLabel?: string;
  statContext?: string;
  statChange?: string;
}

export const StatMetricCard: React.FC<StatMetricCardProps> = ({
  brollPath,
  statNumber = "$1.2 BILLION",
  statLabel = "ESTIMATED INFRASTRUCTURE DAMAGE",
  statContext = "Total loss attributed to single untested Friday deployment loop.",
  statChange = "+340% SURPLUS RISK",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Spring scale entrance for the card
  const cardSpring = spring({
    frame,
    fps,
    config: { damping: 12, mass: 0.6, stiffness: 110 },
  });

  // Animated progress bar fill
  const barProgress = interpolate(frame, [10, 40], [0, 92], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

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
      {/* Left 48% Pane: 16:9 Footage */}
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

      {/* Right 52% Pane: 3D High-Impact Stat Infographic Card */}
      <div
        style={{
          width: "52%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "40px",
          boxSizing: "border-box",
        }}
      >
        <div
          style={{
            width: "100%",
            background: "rgba(12, 19, 36, 0.9)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid #00e5ff",
            boxShadow: "0 20px 60px rgba(0, 0, 0, 0.85), 0 0 40px rgba(0, 229, 255, 0.3)",
            borderRadius: "24px",
            padding: "40px",
            display: "flex",
            flexDirection: "column",
            gap: "24px",
            transform: `scale(${cardSpring})`,
            boxSizing: "border-box",
          }}
        >
          {/* Header Metric Badge */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div
              style={{
                background: "linear-gradient(135deg, #0284c7, #0369a1)",
                border: "1px solid #7dd3fc",
                borderRadius: "12px",
                padding: "8px 22px",
                color: "#ffffff",
                fontSize: "18px",
                fontWeight: 800,
                letterSpacing: "2px",
                textTransform: "uppercase",
              }}
            >
              ● CRITICAL IMPACT METRIC
            </div>
          {/* Change Badge - Red for risk/negative, Green for positive */}
            <div
              style={{
                background: statChange && (statChange.includes("GROWTH") || statChange.includes("GAIN") || statChange.includes("IMPROVEMENT") || statChange.includes("SAVED") || (statChange.startsWith("+") && !statChange.includes("RISK") && !statChange.includes("DOWNTIME") && !statChange.includes("SURPLUS")))
                  ? "rgba(34, 197, 94, 0.2)"
                  : "rgba(239, 68, 68, 0.2)",
                border: `1px solid ${statChange && (statChange.includes("GROWTH") || statChange.includes("GAIN") || statChange.includes("IMPROVEMENT") || statChange.includes("SAVED") || (statChange.startsWith("+") && !statChange.includes("RISK") && !statChange.includes("DOWNTIME") && !statChange.includes("SURPLUS")))
                  ? "#22c55e"
                  : "#ef4444"}`,
                borderRadius: "8px",
                padding: "6px 14px",
                color: statChange && (statChange.includes("GROWTH") || statChange.includes("GAIN") || statChange.includes("IMPROVEMENT") || statChange.includes("SAVED") || (statChange.startsWith("+") && !statChange.includes("RISK") && !statChange.includes("DOWNTIME") && !statChange.includes("SURPLUS")))
                  ? "#4ade80"
                  : "#f87171",
                fontSize: "16px",
                fontWeight: 700,
              }}
            >
              {statChange}
            </div>
          </div>

          {/* Big Stat Number */}
          <div
            style={{
              fontSize: "72px",
              fontWeight: 900,
              color: "#00e5ff",
              letterSpacing: "1px",
              textShadow: "0 0 35px rgba(0, 229, 255, 0.6)",
              fontFamily: "system-ui, -apple-system, sans-serif",
              lineHeight: 1.05,
            }}
          >
            {statNumber}
          </div>

          {/* Stat Label */}
          <div
            style={{
              fontSize: "22px",
              fontWeight: 800,
              color: "#ffffff",
              letterSpacing: "2px",
              textTransform: "uppercase",
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            {statLabel}
          </div>

          {/* Animated Glowing Progress Bar */}
          <div style={{ width: "100%", height: "14px", background: "rgba(30, 41, 59, 0.8)", borderRadius: "8px", overflow: "hidden", border: "1px solid rgba(0, 229, 255, 0.2)" }}>
            <div
              style={{
                width: `${barProgress}%`,
                height: "100%",
                background: "linear-gradient(90deg, #00e5ff, #e11d48)",
                boxShadow: "0 0 15px #00e5ff",
                borderRadius: "8px",
              }}
            />
          </div>

          {/* Satirical Context Box */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.9)",
              borderLeft: "5px solid #00e5ff",
              borderRadius: "12px",
              padding: "18px 22px",
              color: "#cbd5e1",
              fontSize: "22px",
              fontWeight: 500,
              lineHeight: 1.35,
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            {statContext}
          </div>
        </div>
      </div>
    </div>
  );
};
