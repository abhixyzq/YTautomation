import React from "react";

export interface DastawezThumbnailProps {
  scheme_name: string;
  big_benefit: string;
  urgency_badge: string;
  portal_name: string;
  helpline: string;
  rule_change_badge?: string;
}

export const DastawezThumbnail: React.FC<DastawezThumbnailProps> = ({
  scheme_name = "आयुष्मान भारत योजना",
  big_benefit = "₹5,00,000 मुफ्त इलाज",
  urgency_badge = "70+ वरिष्ठ नागरिक नया नियम",
  portal_name = "beneficiary.nha.gov.in",
  helpline = "14555",
  rule_change_badge = "आधिकारिक घोषणा",
}) => {
  return (
    <div
      style={{
        width: 1280,
        height: 720,
        background: "radial-gradient(circle at 75% 25%, #0f2d4e 0%, #081526 50%, #030812 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "48px 56px",
        boxSizing: "border-box",
      }}
    >
      {/* Tricolor Accent Stripe at Top */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 8,
          background: "linear-gradient(90deg, #f97316 0%, #f97316 33.3%, #ffffff 33.3%, #ffffff 66.6%, #10b981 66.6%, #10b981 100%)",
        }}
      />

      {/* Header Badges */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        {/* Brand */}
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 46,
              height: 46,
              borderRadius: 12,
              background: "linear-gradient(135deg, #f97316 0%, #10b981 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 900,
              fontSize: 24,
              color: "#ffffff",
            }}
          >
            द
          </div>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#ffffff", letterSpacing: -0.5 }}>
            @iDastawez
          </span>
        </div>

        {/* Urgency Pill */}
        <div
          style={{
            background: "#dc2626",
            color: "#ffffff",
            fontSize: 20,
            fontWeight: 900,
            padding: "8px 24px",
            borderRadius: 30,
            boxShadow: "0 0 25px rgba(220, 38, 38, 0.7)",
            letterSpacing: 0.5,
          }}
        >
          🚨 {rule_change_badge}
        </div>
      </div>

      {/* Center Punch: Giant Bold Benefit & Scheme */}
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {/* Top Urgency Category Tag */}
        <div
          style={{
            background: "rgba(249, 115, 22, 0.2)",
            border: "2px solid #f97316",
            padding: "8px 22px",
            borderRadius: 12,
            width: "fit-content",
            fontSize: 22,
            fontWeight: 800,
            color: "#fb923c",
          }}
        >
          {urgency_badge}
        </div>

        {/* Giant Main Benefit */}
        <h1
          style={{
            fontSize: 78,
            fontWeight: 900,
            lineHeight: 1.1,
            color: "#fde047",
            margin: 0,
            textShadow: "0 4px 30px rgba(253, 224, 71, 0.4), 0 8px 40px rgba(0, 0, 0, 0.9)",
          }}
        >
          {big_benefit}
        </h1>

        {/* Scheme Name Subtitle */}
        <div
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#ffffff",
            lineHeight: 1.3,
            maxWidth: 1000,
          }}
        >
          {scheme_name}
        </div>
      </div>

      {/* Bottom Footer Info Bar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: "rgba(15, 23, 42, 0.8)",
          backdropFilter: "blur(12px)",
          borderRadius: 16,
          padding: "16px 28px",
          border: "1px solid rgba(255, 255, 255, 0.12)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 16, color: "#94a3b8", fontWeight: 600 }}>आधिकारिक पोर्टल:</span>
          <span style={{ fontSize: 20, color: "#38bdf8", fontWeight: 800 }}>{portal_name}</span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 16, color: "#94a3b8", fontWeight: 600 }}>हेल्पलाइन:</span>
          <span style={{ fontSize: 22, color: "#34d399", fontWeight: 900 }}>📞 {helpline}</span>
        </div>
      </div>
    </div>
  );
};
