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
        top: 28,
        left: 64,
        right: 64,
        height: 74,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 28px",
        background: "rgba(255, 255, 255, 0.92)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        borderRadius: 20,
        border: "1px solid rgba(226, 232, 240, 0.95)",
        boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08), 0 2px 6px rgba(15, 23, 42, 0.03)",
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
              width: 44,
              height: 44,
              borderRadius: 12,
              background: "linear-gradient(135deg, #1d4ed8 0%, #2563eb 60%, #0284c7 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 900,
              fontSize: 20,
              color: "#ffffff",
              boxShadow: "0 4px 14px rgba(37, 99, 235, 0.35)",
              position: "relative",
            }}
          >
            iD
            <span
              style={{
                position: "absolute",
                top: -2,
                right: -2,
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: "#f97316",
                border: "2px solid #ffffff",
              }}
            />
          </div>
          <div>
            <div style={{ fontSize: 20, fontWeight: 900, color: "#0f172a", letterSpacing: 0.2 }}>
              iDastawez
            </div>
            <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", letterSpacing: 0.5, textTransform: "uppercase" }}>
              नागरिक सूचना एवं सरकारी नियम
            </div>
          </div>
        </div>

        {/* Vertical Divider */}
        <div style={{ width: 1, height: 28, background: "rgba(203, 213, 225, 0.8)" }} />

        {/* Official Portal Chip */}
        {portalDomain && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(2, 132, 199, 0.08)",
              border: "1px solid rgba(2, 132, 199, 0.25)",
              borderRadius: 10,
              padding: "5px 14px",
            }}
          >
            <span style={{ fontSize: 13 }}>🏛️</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#0369a1" }}>
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
                    ? "#0284c7"
                    : isCompleted
                    ? "#10b981"
                    : "rgba(203, 213, 225, 0.7)",
                  boxShadow: isCurrent ? "0 2px 8px rgba(2, 132, 199, 0.4)" : "none",
                  transition: "all 0.3s ease",
                }}
              />
            );
          })}
        </div>

        {/* Current Act Tag */}
        <div
          style={{
            background: "rgba(241, 245, 249, 0.95)",
            border: "1px solid rgba(203, 213, 225, 0.9)",
            borderRadius: 10,
            padding: "5px 14px",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span style={{ fontSize: 12, fontWeight: 800, color: "#0284c7" }}>
            भाग {currentActIndex}/{totalActs}
          </span>
          {actTitle && (
            <span style={{ fontSize: 13, fontWeight: 700, color: "#1e293b" }}>
              {actTitle}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
