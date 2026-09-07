import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Img } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface DastawezOverviewProps {
  schemeName: string;
  ministry?: string;
  benefitHighlight?: string;
  latestUpdate?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  urgencyBadge?: string;
  category?: string;
  evidence?: EvidenceMetadata;
  officialImagePath?: string;
  officialImageTitle?: string;
  attribution?: string;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezOverview: React.FC<DastawezOverviewProps> = ({
  schemeName,
  ministry,
  benefitHighlight,
  latestUpdate,
  portalUrl,
  officialPortalDomain,
  urgencyBadge,
  category,
  evidence,
  officialImagePath,
  officialImageTitle,
  attribution,
  currentActIndex = 1,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Subtle Ken Burns motion
  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.025], {
    extrapolateRight: "clamp",
  });

  // Micro-beats:
  const beat1Spring = spring({ frame, fps, delay: 4, config: { damping: 14, stiffness: 100 } });
  const beat2Spring = spring({ frame, fps, delay: 20, config: { damping: 14, stiffness: 90 } });
  const beat3Spring = spring({ frame, fps, delay: 45, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Top Header */}
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="अधिसूचना एवं मुख्य बिंदु"
        portalDomain={domain}
      />

      {/* Main Content Stage */}
      <div
        style={{
          position: "absolute",
          top: 130,
          bottom: 110,
          left: 64,
          right: 64,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 20,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Top Badges Row */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            transform: `translateY(${(1 - beat1Spring) * -16}px)`,
            opacity: beat1Spring,
          }}
        >
          {/* Saffron Urgency Badge */}
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              background: "rgba(255, 247, 237, 0.95)",
              border: "1px solid rgba(249, 115, 22, 0.4)",
              padding: "7px 20px",
              borderRadius: 100,
              boxShadow: "0 4px 12px rgba(249, 115, 22, 0.12)",
            }}
          >
            <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#ea580c", boxShadow: "0 0 8px #f97316" }} />
            <span style={{ fontSize: 15, fontWeight: 800, color: "#c2410c", letterSpacing: 0.3 }}>
              {urgencyBadge || "ताज़ा सरकारी अधिसूचना 2026"}
            </span>
          </div>

          {/* Ministry Badge */}
          {ministry && (
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 8,
                background: "rgba(239, 246, 255, 0.95)",
                border: "1px solid rgba(59, 130, 246, 0.3)",
                padding: "7px 18px",
                borderRadius: 100,
              }}
            >
              <span style={{ fontSize: 13 }}>🏛️</span>
              <span style={{ fontSize: 14, fontWeight: 700, color: "#1d4ed8" }}>
                {ministry}
              </span>
            </div>
          )}
        </div>

        {/* Scheme Master Title */}
        <h1
          style={{
            fontSize: 48,
            fontWeight: 900,
            lineHeight: 1.24,
            color: "#0f172a",
            margin: 0,
            maxWidth: 1650,
            letterSpacing: "-0.5px",
            textShadow: "0 2px 10px rgba(0, 0, 0, 0.05)",
            transform: `translateY(${(1 - beat1Spring) * 16}px)`,
            opacity: beat1Spring,
          }}
        >
          {schemeName}
        </h1>

        {/* 2-Column Broadcast Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.1fr", gap: 26, marginTop: 4 }}>
          {/* Left Column: Big Benefit Card */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 253, 244, 0.9) 100%)",
              border: "2px solid rgba(16, 185, 129, 0.5)",
              borderRadius: 24,
              padding: "26px 30px",
              boxShadow: "0 18px 45px rgba(15, 23, 42, 0.08), 0 0 20px rgba(16, 185, 129, 0.1)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 16,
              transform: `translateX(${(1 - beat2Spring) * -25}px)`,
              opacity: beat2Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span
                  style={{
                    background: "rgba(16, 185, 129, 0.15)",
                    color: "#059669",
                    padding: "4px 12px",
                    borderRadius: 8,
                    fontSize: 13,
                    fontWeight: 800,
                    textTransform: "uppercase",
                    letterSpacing: 0.8,
                  }}
                >
                  निर्धारित आर्थिक सहायता / मुख्य लाभ
                </span>
              </div>
              <div
                style={{
                  fontSize: 38,
                  fontWeight: 900,
                  color: "#064e3b",
                  lineHeight: 1.25,
                  marginTop: 14,
                }}
              >
                {benefitHighlight || "सीधा लाभ बैंक खाते में (DBT)"}
              </div>
            </div>

            {/* Direct Benefit Transfer Pill */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                background: "rgba(255, 255, 255, 0.8)",
                border: "1px solid rgba(16, 185, 129, 0.25)",
                padding: "10px 16px",
                borderRadius: 12,
              }}
            >
              <span style={{ fontSize: 18 }}>⚡</span>
              <span style={{ fontSize: 14, fontWeight: 700, color: "#047857" }}>
                100% सरकारी सब्सिडी / DBT योजना | कोई बिचौलिया नहीं
              </span>
            </div>
          </div>

          {/* Right Column: Authentic Image + Latest Directive Card */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - beat3Spring) * 25}px)`,
              opacity: beat3Spring,
            }}
          >
            {/* Authentic Wikimedia Photo Frame */}
            {officialImagePath ? (
              <div
                style={{
                  position: "relative",
                  borderRadius: 20,
                  overflow: "hidden",
                  border: "1px solid rgba(186, 230, 253, 0.8)",
                  height: 155,
                  boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
                  background: "#e2e8f0",
                }}
              >
                <Img
                  src={officialImagePath}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                  }}
                />
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    background: "linear-gradient(180deg, transparent 40%, rgba(15, 23, 42, 0.85) 100%)",
                  }}
                />
                <div
                  style={{
                    position: "absolute",
                    bottom: 8,
                    left: 14,
                    right: 14,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                  }}
                >
                  <span style={{ fontSize: 13, color: "#ffffff", fontWeight: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "75%" }}>
                    🏛️ {officialImageTitle || "आधिकारिक संदर्भ दृश्य"}
                  </span>
                  <span style={{ fontSize: 11, color: "#cbd5e1", fontWeight: 600, background: "rgba(0,0,0,0.4)", padding: "2px 8px", borderRadius: 4 }}>
                    {attribution || "Wikimedia Commons"}
                  </span>
                </div>
              </div>
            ) : null}

            {/* Directive Quote Card */}
            <div
              style={{
                background: "rgba(255, 255, 255, 0.94)",
                border: "1px solid rgba(226, 232, 240, 0.9)",
                borderRadius: 20,
                padding: "20px 24px",
                boxShadow: "0 12px 30px rgba(15, 23, 42, 0.06)",
                display: "flex",
                flexDirection: "column",
                gap: 12,
              }}
            >
              <div style={{ fontSize: 13, fontWeight: 800, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.8 }}>
                नवीनतम सरकारी निर्देश एवं अद्यतन
              </div>
              <div style={{ fontSize: 20, fontWeight: 700, color: "#1e293b", lineHeight: 1.5 }}>
                {latestUpdate || "आधिकारिक सार्वजनिक दिशा-निर्देश जारी किए गए हैं।"}
              </div>

              {/* Verified Portal Confirmation Pill */}
              <div
                style={{
                  background: "rgba(239, 246, 255, 0.9)",
                  border: "1px solid rgba(59, 130, 246, 0.25)",
                  borderRadius: 10,
                  padding: "8px 14px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ fontSize: 15 }}>🌐</span>
                  <span style={{ fontSize: 14, fontWeight: 700, color: "#1d4ed8" }}>
                    आधिकारिक पोर्टल: {domain}
                  </span>
                </div>
                <span style={{ fontSize: 12, color: "#059669", fontWeight: 700 }}>
                  ✓ सत्यापित सरकारी डोमेन
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
