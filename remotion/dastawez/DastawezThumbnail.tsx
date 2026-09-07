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
        background: "radial-gradient(ellipse at 50% 25%, #e0f2fe 0%, #f8fafc 60%, #f1f5f9 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "44px 54px",
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
          height: 7,
          background: "linear-gradient(90deg, #ea580c 0%, #ea580c 33.3%, #ffffff 33.3%, #ffffff 66.6%, #10b981 66.6%, #10b981 100%)",
        }}
      />

      {/* Header Badges */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        {/* Brand */}
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 14,
              background: "linear-gradient(135deg, #ea580c 0%, #f97316 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: 900,
              fontSize: 26,
              color: "#ffffff",
              boxShadow: "0 4px 12px rgba(234, 88, 12, 0.35)",
            }}
          >
            द
          </div>
          <div>
            <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a", letterSpacing: -0.5 }}>
              @iDastawez
            </span>
            <span style={{ fontSize: 13, display: "block", color: "#64748b", fontWeight: 700 }}>
              Official Citizen Portal Guide
            </span>
          </div>
        </div>

        {/* Urgency Pill */}
        <div
          style={{
            background: "linear-gradient(135deg, #ea580c 0%, #dc2626 100%)",
            color: "#ffffff",
            fontSize: 18,
            fontWeight: 900,
            padding: "8px 22px",
            borderRadius: 30,
            boxShadow: "0 4px 18px rgba(234, 88, 12, 0.35)",
            letterSpacing: 0.5,
          }}
        >
          🚨 {rule_change_badge}
        </div>
      </div>

      {/* Center Punch: Giant Bold Benefit & Scheme on Luminous Glass Card */}
      <div
        style={{
          background: "rgba(255, 255, 255, 0.94)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          border: "1.5px solid rgba(2, 132, 199, 0.3)",
          borderRadius: 24,
          padding: "32px 42px",
          boxShadow: "0 20px 48px rgba(15, 23, 42, 0.08), 0 4px 16px rgba(2, 132, 199, 0.06)",
          display: "flex",
          flexDirection: "column",
          gap: 14,
        }}
      >
        {/* Top Urgency Category Tag */}
        <div
          style={{
            background: "#eff6ff",
            border: "1.5px solid #3b82f6",
            padding: "6px 18px",
            borderRadius: 10,
            width: "fit-content",
            fontSize: 20,
            fontWeight: 800,
            color: "#1d4ed8",
          }}
        >
          {urgency_badge}
        </div>

        {/* Giant Main Benefit */}
        <h1
          style={{
            fontSize: 70,
            fontWeight: 900,
            lineHeight: 1.1,
            color: "#0f172a",
            margin: 0,
            letterSpacing: -1,
          }}
        >
          {big_benefit}
        </h1>

        {/* Scheme Name Subtitle */}
        <div
          style={{
            fontSize: 30,
            fontWeight: 800,
            color: "#334155",
            lineHeight: 1.3,
            maxWidth: 1050,
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
          background: "rgba(255, 255, 255, 0.92)",
          backdropFilter: "blur(16px)",
          borderRadius: 18,
          padding: "14px 28px",
          border: "1px solid rgba(2, 132, 199, 0.25)",
          boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 16, color: "#64748b", fontWeight: 700 }}>आधिकारिक पोर्टल:</span>
          <span style={{ fontSize: 20, color: "#0284c7", fontWeight: 800 }}>{portal_name}</span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 16, color: "#64748b", fontWeight: 700 }}>हेल्पलाइन:</span>
          <span style={{ fontSize: 22, color: "#059669", fontWeight: 900 }}>📞 {helpline}</span>
        </div>
      </div>
    </div>
  );
};
