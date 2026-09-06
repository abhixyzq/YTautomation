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

  // Gentle continuous Ken Burns camera push-in (eliminates static video feel)
  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.03], {
    extrapolateRight: "clamp",
  });

  // Timed Sequential Reveals (Every 5-12 seconds):
  // Beat 1: Ministry Announcement & Headline (0s+)
  const beat1Spring = spring({ frame, fps, delay: 5, config: { damping: 14, stiffness: 100 } });

  // Beat 2: Big Benefit / Entitlement Card (frame 35+)
  const beat2Spring = spring({ frame, fps, delay: 35, config: { damping: 14, stiffness: 90 } });

  // Beat 3: Latest Official Directive & Portal Anchor (frame 75+)
  const beat3Spring = spring({ frame, fps, delay: 75, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 25%, #0a1530 0%, #060b18 60%, #03050a 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Background Subtle Tech Blueprint Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "radial-gradient(rgba(59, 130, 246, 0.12) 1px, transparent 1px), radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px)",
          backgroundSize: "40px 40px, 80px 80px",
          pointerEvents: "none",
          opacity: 0.6,
        }}
      />

      {/* Top Header with Chapter Progress */}
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="अधिसूचना एवं मुख्य बिंदु"
        portalDomain={domain}
      />

      {/* Main Dynamic Viewport */}
      <div
        style={{
          position: "absolute",
          top: 145,
          bottom: 110,
          left: 64,
          right: 64,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 22,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Beat 1: Notification Badge & Ministry Tag */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: "rgba(37, 99, 235, 0.14)",
            border: "1px solid rgba(59, 130, 246, 0.5)",
            padding: "8px 22px",
            borderRadius: 100,
            width: "fit-content",
            transform: `translateY(${(1 - beat1Spring) * -20}px)`,
            opacity: beat1Spring,
          }}
        >
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: "#38bdf8", boxShadow: "0 0 8px #38bdf8" }} />
          <span style={{ fontSize: 16, fontWeight: 800, color: "#93c5fd", letterSpacing: 0.6 }}>
            {urgencyBadge || "आधिकारिक सरकारी अधिसूचना 2026"}
          </span>
        </div>

        {/* Scheme Title */}
        <h1
          style={{
            fontSize: 52,
            fontWeight: 900,
            lineHeight: 1.22,
            color: "#ffffff",
            margin: 0,
            maxWidth: 1600,
            textShadow: "0 4px 20px rgba(0, 0, 0, 0.7)",
            transform: `translateY(${(1 - beat1Spring) * 20}px)`,
            opacity: beat1Spring,
          }}
        >
          {schemeName}
        </h1>

        {/* Dynamic Two-Column Card Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.3fr", gap: 28, marginTop: 6 }}>
          {/* Beat 2: Big Benefit Reveal Card */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(30, 58, 138, 0.4) 0%, rgba(10, 18, 36, 0.9) 100%)",
              border: "2px solid rgba(59, 130, 246, 0.65)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 18px 45px rgba(0, 0, 0, 0.7), 0 0 25px rgba(37, 99, 235, 0.25)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 16,
              transform: `translateX(${(1 - beat2Spring) * -30}px)`,
              opacity: beat2Spring,
            }}
          >
            <div>
              <div style={{ fontSize: 14, fontWeight: 800, color: "#60a5fa", textTransform: "uppercase", letterSpacing: 1 }}>
                निर्धारित आर्थिक सहायता / मुख्य लाभ
              </div>
              <div
                style={{
                  fontSize: 40,
                  fontWeight: 900,
                  color: "#ffffff",
                  lineHeight: 1.25,
                  marginTop: 10,
                  textShadow: "0 2px 15px rgba(0,0,0,0.5)",
                }}
              >
                {benefitHighlight || "सीधा लाभ बैंक खाते में (DBT)"}
              </div>
              {officialImagePath && (
                <div
                  style={{
                    position: "relative",
                    borderRadius: 16,
                    overflow: "hidden",
                    border: "1px solid rgba(59, 130, 246, 0.45)",
                    height: 125,
                    marginTop: 14,
                    background: "#020617",
                  }}
                >
                  <Img
                    src={officialImagePath}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      opacity: 0.9,
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      background: "linear-gradient(180deg, transparent 30%, rgba(2, 6, 23, 0.92) 100%)",
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      bottom: 6,
                      left: 10,
                      right: 10,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <span style={{ fontSize: 11, color: "#93c5fd", fontWeight: 700, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "72%" }}>
                      🏛️ {officialImageTitle || "आधिकारिक संदर्भ दृश्य"}
                    </span>
                    <span style={{ fontSize: 10, color: "#94a3b8", fontWeight: 600 }}>
                      {attribution || "Wikimedia Commons"}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Beat 3: Latest Official Directive & Portal Anchor */}
          <div
            style={{
              background: "rgba(10, 18, 36, 0.85)",
              border: "1px solid rgba(255, 255, 255, 0.12)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 40px rgba(0, 0, 0, 0.6)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 16,
              transform: `translateX(${(1 - beat3Spring) * 30}px)`,
              opacity: beat3Spring,
            }}
          >
            <div>
              <div style={{ fontSize: 14, fontWeight: 800, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
                नवीनतम सरकारी निर्देश एवं अद्यतन
              </div>
              <div style={{ fontSize: 23, fontWeight: 700, color: "#f1f5f9", lineHeight: 1.5, marginTop: 8 }}>
                {latestUpdate || "आधिकारिक सार्वजनिक दिशा-निर्देश जारी किए गए हैं।"}
              </div>
            </div>

            {/* Official Domain Confirmation */}
            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(59, 130, 246, 0.3)",
                borderRadius: 12,
                padding: "12px 18px",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ fontSize: 18 }}>🏛️</span>
                <span style={{ fontSize: 15, fontWeight: 700, color: "#93c5fd" }}>
                  सत्यापित पोर्टल: {domain}
                </span>
              </div>
              <span style={{ fontSize: 13, color: "#64748b", fontWeight: 600 }}>
                सरकारी अधिकृत
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
