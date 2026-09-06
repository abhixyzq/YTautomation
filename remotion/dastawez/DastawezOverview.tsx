import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";

interface Props {
  schemeName: string;
  ministry?: string;
  benefitHighlight?: string;
  latestUpdate?: string;
  portalUrl?: string;
  urgencyBadge?: string;
  category?: string;
}

export const DastawezOverview: React.FC<Props> = ({
  schemeName,
  ministry,
  benefitHighlight,
  latestUpdate,
  portalUrl,
  urgencyBadge,
  category,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({ frame, fps, delay: 5, config: { damping: 14 } });
  const benefitSpring = spring({ frame, fps, delay: 15, config: { damping: 12, stiffness: 90 } });
  const updateSpring = spring({ frame, fps, delay: 25, config: { damping: 14 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 20%, #0f2b48 0%, #081426 60%, #030a14 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Top Header */}
      <DastawezHeader ministry={ministry} category={category} schemeName={schemeName} />

      {/* Main Content Layout */}
      <div
        style={{
          position: "absolute",
          top: 140,
          bottom: 40,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 28,
        }}
      >
        {/* Urgency / Category Pill */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: "linear-gradient(90deg, rgba(249, 115, 22, 0.25) 0%, rgba(249, 115, 22, 0.05) 100%)",
            borderLeft: "5px solid #f97316",
            padding: "10px 24px",
            borderRadius: "0 12px 12px 0",
            width: "fit-content",
            transform: `translateX(${(1 - titleSpring) * -40}px)`,
            opacity: titleSpring,
          }}
        >
          <span style={{ fontSize: 18, fontWeight: 800, color: "#fb923c", letterSpacing: 0.5 }}>
            {urgencyBadge || "📢 आधिकारिक सरकारी अधिसूचना 2026"}
          </span>
        </div>

        {/* Big Scheme Title */}
        <h1
          style={{
            fontSize: 58,
            fontWeight: 900,
            lineHeight: 1.25,
            color: "#ffffff",
            margin: 0,
            maxWidth: 1600,
            textShadow: "0 4px 20px rgba(0, 0, 0, 0.6)",
            transform: `translateY(${(1 - titleSpring) * 30}px)`,
            opacity: titleSpring,
          }}
        >
          {schemeName}
        </h1>

        {/* Two-Column Showcase: Benefit + Latest Official Decision */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.3fr", gap: 32, marginTop: 10 }}>
          {/* Benefit Card */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 78, 59, 0.25) 100%)",
              border: "2px solid rgba(52, 211, 153, 0.4)",
              borderRadius: 24,
              padding: "36px 32px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
              transform: `scale(${benefitSpring})`,
              opacity: benefitSpring,
            }}
          >
            <div>
              <div style={{ fontSize: 18, fontWeight: 700, color: "#6ee7b7", textTransform: "uppercase", letterSpacing: 1 }}>
                🎯 मुख्य लाभ / आर्थिक सहायता
              </div>
              <div
                style={{
                  fontSize: 50,
                  fontWeight: 900,
                  color: "#ffffff",
                  marginTop: 14,
                  lineHeight: 1.2,
                  textShadow: "0 0 30px rgba(52, 211, 153, 0.5)",
                }}
              >
                {benefitHighlight || "₹5,00,000 मुफ्त इलाज"}
              </div>
            </div>

            <div
              style={{
                marginTop: 24,
                display: "flex",
                alignItems: "center",
                gap: 12,
                fontSize: 18,
                color: "#a7f3d0",
                fontWeight: 600,
              }}
            >
              <span>🔒 100% DBT / सीधे अस्पताल में कैशलेस सुविधा</span>
            </div>
          </div>

          {/* Latest Decision / News Card */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.75)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(255, 255, 255, 0.14)",
              borderRadius: 24,
              padding: "36px 36px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              boxShadow: "0 20px 40px rgba(0, 0, 0, 0.4)",
              transform: `translateY(${(1 - updateSpring) * 30}px)`,
              opacity: updateSpring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#f97316" }} />
                <span style={{ fontSize: 16, fontWeight: 700, color: "#f97316", textTransform: "uppercase", letterSpacing: 1 }}>
                  ताज़ा आधिकारिक फैसला / कैबिनेट निर्देश
                </span>
              </div>
              <p
                style={{
                  fontSize: 26,
                  fontWeight: 600,
                  color: "#e2e8f0",
                  lineHeight: 1.5,
                  marginTop: 16,
                  marginBottom: 0,
                }}
              >
                {latestUpdate || "आधिकारिक पोर्टल पर नई गाइडलाइन जारी कर दी गई है। सभी पात्र नागरिक तुरंत अपना e-KYC पूरा करें।"}
              </p>
            </div>

            {/* Official Portal Pill */}
            {portalUrl && (
              <div
                style={{
                  marginTop: 20,
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 12,
                  background: "rgba(255, 255, 255, 0.06)",
                  padding: "10px 20px",
                  borderRadius: 14,
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  width: "fit-content",
                }}
              >
                <span style={{ fontSize: 16, color: "#94a3b8" }}>पोर्टल:</span>
                <span style={{ fontSize: 18, fontWeight: 700, color: "#38bdf8" }}>{portalUrl}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
