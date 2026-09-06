import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface Props {
  ministry?: string;
  category?: string;
  schemeName?: string;
}

export const DastawezHeader: React.FC<Props> = ({ ministry, category }) => {
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
        top: 36,
        left: 56,
        right: 56,
        height: 80,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 32px",
        background: "rgba(10, 25, 47, 0.75)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        borderRadius: 20,
        border: "1px solid rgba(255, 255, 255, 0.12)",
        boxShadow: "0 10px 30px rgba(0, 0, 0, 0.4)",
        transform: `translateY(${(1 - entrance) * -30}px)`,
        opacity,
        zIndex: 50,
      }}
    >
      {/* Brand Identity */}
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div
          style={{
            width: 44,
            height: 44,
            borderRadius: 12,
            background: "linear-gradient(135deg, #f97316 0%, #ea580c 50%, #10b981 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 900,
            fontSize: 22,
            color: "#ffffff",
            boxShadow: "0 4px 15px rgba(249, 115, 22, 0.4)",
          }}
        >
          द
        </div>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span
            style={{
              fontSize: 24,
              fontWeight: 900,
              letterSpacing: -0.5,
              color: "#ffffff",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            @iDastawez
            <span
              style={{
                fontSize: 12,
                fontWeight: 700,
                color: "#f97316",
                background: "rgba(249, 115, 22, 0.15)",
                padding: "2px 8px",
                borderRadius: 6,
                border: "1px solid rgba(249, 115, 22, 0.3)",
              }}
            >
              OFFICIAL
            </span>
          </span>
          <span style={{ fontSize: 13, color: "#94a3b8", fontWeight: 500 }}>
            {category || "सरकारी योजनाएं एवं नागरिक सेवाएं"}
          </span>
        </div>
      </div>

      {/* Ministry Center Pill */}
      {ministry && (
        <div
          style={{
            padding: "8px 20px",
            background: "rgba(255, 255, 255, 0.06)",
            borderRadius: 30,
            border: "1px solid rgba(255, 255, 255, 0.1)",
            fontSize: 15,
            fontWeight: 600,
            color: "#e2e8f0",
            maxWidth: 500,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          🏛️ {ministry}
        </div>
      )}

      {/* Verified Status Pill */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: "rgba(16, 185, 129, 0.15)",
          padding: "8px 18px",
          borderRadius: 30,
          border: "1px solid rgba(16, 185, 129, 0.35)",
        }}
      >
        <div
          style={{
            width: 10,
            height: 10,
            borderRadius: "50%",
            background: "#10b981",
            boxShadow: "0 0 10px #10b981",
          }}
        />
        <span style={{ fontSize: 14, fontWeight: 700, color: "#34d399", letterSpacing: 0.2 }}>
          100% प्रमाणित सरकारी जानकारी
        </span>
      </div>
    </div>
  );
};
