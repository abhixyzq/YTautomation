import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface DastawezHeaderProps {
  ministry?: string;
  category?: string;
  schemeName?: string;
  currentActIndex?: number;
  totalActs?: number;
  actTitle?: string;
  portalDomain?: string;
}

export const DastawezHeader: React.FC<DastawezHeaderProps> = ({
  ministry,
  category,
  currentActIndex = 1,
  totalActs = 6,
  actTitle,
  portalDomain,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 100 },
  });

  const opacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 30,
        left: 64,
        right: 64,
        height: 76,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 28px",
        background: "rgba(7, 13, 26, 0.88)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        borderRadius: 18,
        border: "1px solid rgba(59, 130, 246, 0.28)",
        boxShadow: "0 12px 30px rgba(0, 0, 0, 0.6)",
        transform: `translateY(${(1 - entrance) * -30}px)`,
        opacity,
        zIndex: 50,
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Left: Brand Identity & Verified Source Badge */}
      <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          {/* Logo Monogram */}
          <div
            style={{
              width: 42,
              height: 42,
              borderRadius: 10,
              background: "linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #38bdf8 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 900,
              fontSize: 20,
              color: "#ffffff",
              boxShadow: "0 0 15px rgba(37, 99, 235, 0.4)",
            }}
          >
            iD
          </div>
          <div>
            <div style={{ fontSize: 19, fontWeight: 900, color: "#ffffff", letterSpacing: 0.5 }}>
              iDastawez
            </div>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8", letterSpacing: 0.4, textTransform: "uppercase" }}>
              नागरिक सूचना एवं सरकारी नियम
            </div>
          </div>
        </div>

        {/* Vertical Divider */}
        <div style={{ width: 1, height: 28, background: "rgba(255, 255, 255, 0.15)" }} />

        {/* Official Portal Chip */}
        {portalDomain && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(37, 99, 235, 0.15)",
              border: "1px solid rgba(59, 130, 246, 0.4)",
              borderRadius: 8,
              padding: "4px 12px",
            }}
          >
            <span style={{ fontSize: 12 }}>🌐</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#93c5fd" }}>
              {portalDomain}
            </span>
          </div>
        )}
      </div>

      {/* Right: Adaptive Chapter Progress Tracker */}
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        {/* Chapter Steps Track */}
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          {Array.from({ length: totalActs }).map((_, idx) => {
            const actNum = idx + 1;
            const isCompleted = actNum < currentActIndex;
            const isCurrent = actNum === currentActIndex;

            return (
              <div
                key={idx}
                style={{
                  width: isCurrent ? 28 : 10,
                  height: 8,
                  borderRadius: 4,
                  background: isCurrent
                    ? "#38bdf8"
                    : isCompleted
                    ? "#2563eb"
                    : "rgba(255, 255, 255, 0.15)",
                  boxShadow: isCurrent ? "0 0 10px rgba(56, 189, 248, 0.8)" : "none",
                  transition: "all 0.3s ease",
                }}
              />
            );
          })}
        </div>

        {/* Current Act Tag */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.8)",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: 8,
            padding: "5px 14px",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span style={{ fontSize: 12, fontWeight: 800, color: "#38bdf8" }}>
            भाग {currentActIndex}/{totalActs}
          </span>
          {actTitle && (
            <span style={{ fontSize: 13, fontWeight: 700, color: "#f8fafc" }}>
              {actTitle}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
