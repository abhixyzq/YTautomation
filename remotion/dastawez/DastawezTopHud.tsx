import React from "react";

interface DastawezTopHudProps {
  schemeName?: string;
  domain?: string;
  urgencyBadge?: string;
  ministry?: string;
  actIndex?: number;
  totalActs?: number;
  actTitle?: string;
}

export const DastawezTopHud: React.FC<DastawezTopHudProps> = ({
  schemeName,
  domain = "india.gov.in",
  urgencyBadge,
  ministry,
  actIndex = 1,
  totalActs = 6,
  actTitle = "अधिसूचना विवरण",
}) => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        width: "100%",
        padding: "4px 0",
      }}
    >
      {/* Left: Brand Monogram + Portal Domain + Urgency Badge + Ministry */}
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        {/* Brand Monogram */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: "rgba(11, 17, 32, 0.94)",
            padding: "8px 16px",
            borderRadius: 14,
            border: "1.5px solid rgba(56, 189, 248, 0.4)",
            boxShadow: "0 8px 24px rgba(0, 0, 0, 0.65)",
          }}
        >
          <div
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#38bdf8",
              boxShadow: "0 0 10px #38bdf8",
            }}
          />
          <span style={{ fontSize: 16, fontWeight: 900, color: "#f8fafc", letterSpacing: 0.5 }}>
            @iDastawez
          </span>
        </div>

        {/* Portal Domain */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: "rgba(11, 17, 32, 0.94)",
            padding: "8px 16px",
            borderRadius: 14,
            border: "1.5px solid rgba(99, 102, 241, 0.4)",
            color: "#c7d2fe",
            fontSize: 14,
            fontWeight: 800,
            boxShadow: "0 8px 24px rgba(0, 0, 0, 0.65)",
          }}
        >
          <span>🏛️</span>
          <span>{domain}</span>
        </div>

        {/* Urgency Badge */}
        {urgencyBadge && (
          <div
            style={{
              background: "linear-gradient(135deg, #e11d48, #f43f5e)",
              color: "#ffffff",
              padding: "8px 18px",
              borderRadius: 14,
              fontSize: 14,
              fontWeight: 900,
              letterSpacing: 0.5,
              boxShadow: "0 6px 20px rgba(225, 29, 72, 0.45)",
            }}
          >
            ● {urgencyBadge.replace(/^[●•\s]+/, "")}
          </div>
        )}

        {/* Ministry */}
        {ministry && (
          <div
            style={{
              background: "rgba(11, 17, 32, 0.92)",
              border: "1px solid rgba(255, 255, 255, 0.15)",
              padding: "8px 16px",
              borderRadius: 14,
              fontSize: 13,
              fontWeight: 700,
              color: "#94a3b8",
              boxShadow: "0 8px 24px rgba(0, 0, 0, 0.65)",
            }}
          >
            {ministry}
          </div>
        )}
      </div>

      {/* Right: Act Tracker */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: "rgba(11, 17, 32, 0.94)",
          padding: "8px 18px",
          borderRadius: 14,
          border: "1.5px solid rgba(56, 189, 248, 0.4)",
          boxShadow: "0 8px 24px rgba(0, 0, 0, 0.65)",
        }}
      >
        <span style={{ fontSize: 14, fontWeight: 900, color: "#38bdf8" }}>
          ACT {actIndex}/{totalActs}
        </span>
        <span style={{ fontSize: 14, color: "#64748b" }}>•</span>
        <span style={{ fontSize: 14, fontWeight: 800, color: "#e2e8f0" }}>{actTitle}</span>
      </div>
    </div>
  );
};
