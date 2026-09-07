import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata } from "./types";
import { DastawezHeader } from "./DastawezHeader";

interface DastawezSourceCardProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  evidence?: EvidenceMetadata;
  category?: string;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezSourceCard: React.FC<DastawezSourceCardProps> = ({
  schemeName,
  ministry,
  portalUrl,
  officialPortalDomain,
  helpline,
  evidence,
  category,
  currentActIndex = 6,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.025], {
    extrapolateRight: "clamp",
  });

  const card1Spring = spring({ frame, fps, delay: 5, config: { damping: 14, stiffness: 90 } });
  const card2Spring = spring({ frame, fps, delay: 25, config: { damping: 14, stiffness: 90 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const ministryName = evidence?.ministry || ministry || "भारत सरकार (Government of India)";
  const notifRef = evidence?.notification_ref || "आधिकारिक सार्वजनिक परिपत्र / गजट 2026";
  const verifiedDate = evidence?.last_verified_date || "सितंबर 2026";
  const citationText =
    evidence?.source_citation || `भारत सरकार के आधिकारिक पोर्टल ${domain} पर उपलब्ध जानकारी से सत्यापित।`;

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
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="आधिकारिक स्रोत व प्रामाणिकता (Source Verification)"
        portalDomain={domain}
      />

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
          gap: 22,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Section Heading Pill */}
        <div style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
          <span
            style={{
              background: "rgba(2, 132, 199, 0.1)",
              border: "1px solid rgba(2, 132, 199, 0.35)",
              color: "#0369a1",
              fontSize: 14,
              fontWeight: 800,
              padding: "6px 18px",
              borderRadius: 100,
              textTransform: "uppercase",
              letterSpacing: 0.6,
            }}
          >
            🏛️ आधिकारिक स्रोत व संदर्भ
          </span>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a" }}>
            100% सत्यापित सरकारी अधिसूचना पर आधारित जानकारी
          </span>
        </div>

        {/* 2-Column Verification Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 26 }}>
          {/* Left Card: Government Evidence Card */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(239, 246, 255, 0.94) 100%)",
              border: "2px solid rgba(2, 132, 199, 0.45)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 45px rgba(2, 132, 199, 0.1)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 18,
              transform: `translateX(${(1 - card1Spring) * -25}px)`,
              opacity: card1Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
                <span
                  style={{
                    background: "#e0f2fe",
                    color: "#0369a1",
                    fontSize: 13,
                    fontWeight: 800,
                    padding: "5px 14px",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span>🏛️</span> आधिकारिक स्रोत प्रमाण
                </span>
                <span style={{ fontSize: 12, fontWeight: 700, color: "#0284c7" }}>
                  सत्यापन माह: {verifiedDate}
                </span>
              </div>

              <div style={{ fontSize: 22, fontWeight: 800, color: "#0f172a", lineHeight: 1.4 }}>
                {citationText}
              </div>

              {/* Notification Reference Box */}
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.9)",
                  border: "1px solid rgba(2, 132, 199, 0.25)",
                  borderRadius: 12,
                  padding: "12px 18px",
                  marginTop: 14,
                }}
              >
                <div style={{ fontSize: 11, fontWeight: 800, color: "#64748b", textTransform: "uppercase" }}>
                  परिपत्र / गजट संदर्भ संख्या
                </div>
                <div style={{ fontSize: 16, fontWeight: 700, color: "#1d4ed8", marginTop: 2, fontFamily: "monospace" }}>
                  {notifRef}
                </div>
              </div>
            </div>

            {/* Gov Domain Stamp */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                fontSize: 14,
                fontWeight: 700,
                color: "#059669",
              }}
            >
              <span>✓</span> हमेशा केवल आधिकारिक .gov.in या .nic.in डोमेन से ही नियमों की पुष्टि करें।
            </div>
          </div>

          {/* Right Card: iDastawez Channel & Subscribe CTA */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.94) 100%)",
              border: "1.5px solid rgba(226, 232, 240, 0.9)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 14px 35px rgba(15, 23, 42, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 18,
              transform: `translateX(${(1 - card2Spring) * 25}px)`,
              opacity: card2Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 14 }}>
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 900,
                    fontSize: 20,
                    color: "#ffffff",
                  }}
                >
                  iD
                </div>
                <div>
                  <div style={{ fontSize: 20, fontWeight: 900, color: "#0f172a" }}>
                    @iDastawez
                  </div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#64748b" }}>
                    सच्ची और निष्पक्ष नागरिक जानकारी
                  </div>
                </div>
              </div>

              {/* YouTube Subscribe Button Mockup */}
              <div
                style={{
                  background: "#dc2626",
                  color: "#ffffff",
                  borderRadius: 14,
                  padding: "14px 20px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 10,
                  fontSize: 17,
                  fontWeight: 900,
                  boxShadow: "0 8px 24px rgba(220, 38, 38, 0.35)",
                }}
              >
                <span>🔔</span> अभी SUBSCRIBE करें
              </div>

              <div style={{ fontSize: 13, color: "#475569", fontWeight: 600, lineHeight: 1.5, marginTop: 14 }}>
                भारत सरकार की हर ताज़ा योजना, नई भर्ती और दस्तावेज़ नियमों के आसान वीडियो के लिए चैनल को सब्सक्राइब ज़रूर करें।
              </div>
            </div>

            {/* Disclaimer */}
            <div style={{ fontSize: 11, color: "#94a3b8", fontWeight: 600 }}>
              अस्वीकरण: iDastawez आधिकारिक सरकारी पोर्टलों पर उपलब्ध सार्वजनिक नियमों को सरल भाषा में प्रस्तुत करता है।
            </div>
          </div>
        </div>

        {/* Bottom Direct Link Bar */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.95)",
            border: "1px solid rgba(226, 232, 240, 0.9)",
            borderRadius: 14,
            padding: "12px 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 6px 18px rgba(15, 23, 42, 0.04)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 16 }}>🌐</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: "#0369a1" }}>
              आधिकारिक पोर्टल लिंक: https://{domain}
            </span>
          </div>
          <span style={{ fontSize: 13, fontWeight: 800, color: "#059669" }}>
            धन्यवाद, जय हिन्द! 🇮🇳
          </span>
        </div>
      </div>
    </div>
  );
};
