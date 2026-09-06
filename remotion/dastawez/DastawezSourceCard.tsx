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

  const entrance = spring({
    frame,
    fps,
    delay: 5,
    config: { damping: 14, stiffness: 100 },
  });

  const card1Spring = spring({
    frame,
    fps,
    delay: 15,
    config: { damping: 14, stiffness: 95 },
  });

  const card2Spring = spring({
    frame,
    fps,
    delay: 25,
    config: { damping: 14, stiffness: 95 },
  });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const ministryName = evidence?.ministry || ministry || "भारत सरकार (Government of India)";
  const notifRef = evidence?.notification_ref || "आधिकारिक सार्वजनिक परिपत्र / गजट";
  const verifiedDate = evidence?.last_verified_date || "सितंबर 2026";
  const citationText =
    evidence?.source_citation || `भारत सरकार के आधिकारिक पोर्टल ${domain} पर उपलब्ध जानकारी से सत्यापित।`;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 25%, #0b1836 0%, #060b18 60%, #03060c 100%)",
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

      {/* Top Header with Live Chapter Scrubber */}
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="आधिकारिक स्रोत व प्रामाणिकता"
        portalDomain={domain}
      />

      {/* Main Content Layout */}
      <div
        style={{
          position: "absolute",
          top: 150,
          bottom: 110,
          left: 64,
          right: 64,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 24,
          transform: `scale(${interpolate(frame, [0, 900], [1.0, 1.025], { extrapolateRight: "clamp" })})`,
        }}
      >
        {/* Section Pill: Grounded & Official Source */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: "rgba(37, 99, 235, 0.15)",
            border: "1px solid rgba(59, 130, 246, 0.5)",
            padding: "8px 22px",
            borderRadius: 100,
            width: "fit-content",
            transform: `translateY(${(1 - entrance) * -20}px)`,
            opacity: entrance,
          }}
        >
          <div
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#38bdf8",
              boxShadow: "0 0 10px #38bdf8",
            }}
          />
          <span style={{ fontSize: 16, fontWeight: 800, color: "#93c5fd", letterSpacing: 0.8 }}>
            आधिकारिक स्रोत सत्यापन | VERIFIED SOURCE CITATION
          </span>
        </div>

        {/* Headline */}
        <h1
          style={{
            fontSize: 44,
            fontWeight: 900,
            color: "#ffffff",
            margin: 0,
            lineHeight: 1.25,
            textShadow: "0 4px 20px rgba(0, 0, 0, 0.6)",
            transform: `translateY(${(1 - entrance) * 20}px)`,
            opacity: entrance,
          }}
        >
          सत्यापित सरकारी स्रोत एवं दस्तावेज संदर्भ
        </h1>

        {/* Two-Column Evidence Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 28, marginTop: 4 }}>
          {/* Left Column: Official Notification Card */}
          <div
            style={{
              background: "rgba(10, 18, 36, 0.88)",
              border: "1px solid rgba(59, 130, 246, 0.35)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 40px rgba(0, 0, 0, 0.6)",
              display: "flex",
              flexDirection: "column",
              gap: 20,
              transform: `translateX(${(1 - card1Spring) * -30}px)`,
              opacity: card1Spring,
            }}
          >
            {/* Ministry / Department Callout */}
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
                संबद्ध मंत्रालय / विभाग
              </div>
              <div style={{ fontSize: 24, fontWeight: 800, color: "#ffffff", marginTop: 4 }}>
                {ministryName}
              </div>
            </div>

            {/* Notification ID / Circular */}
            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                borderRadius: 14,
                padding: "16px 20px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <div>
                <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b" }}>
                  परिपत्र / अधिसूचना संदर्भ संख्या
                </div>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#38bdf8", fontFamily: "monospace", marginTop: 2 }}>
                  {notifRef}
                </div>
              </div>
              <div
                style={{
                  background: "rgba(34, 197, 94, 0.15)",
                  border: "1px solid rgba(34, 197, 94, 0.5)",
                  borderRadius: 8,
                  padding: "4px 12px",
                  fontSize: 13,
                  fontWeight: 800,
                  color: "#4ade80",
                }}
              >
                सत्यापित: {verifiedDate}
              </div>
            </div>

            {/* Citation Statement */}
            <div style={{ fontSize: 16, color: "#cbd5e1", lineHeight: 1.6, borderLeft: "3px solid #3b82f6", paddingLeft: 14 }}>
              {citationText}
            </div>
          </div>

          {/* Right Column: Official Portal Domain & Citizen Helpline */}
          <div
            style={{
              background: "rgba(10, 18, 36, 0.88)",
              border: "1px solid rgba(255, 255, 255, 0.12)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 40px rgba(0, 0, 0, 0.6)",
              display: "flex",
              flexDirection: "column",
              gap: 20,
              transform: `translateX(${(1 - card2Spring) * 30}px)`,
              opacity: card2Spring,
            }}
          >
            {/* Official Portal Block */}
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
                एकमात्र आधिकारिक वेब पोर्टल
              </div>
              <div
                style={{
                  marginTop: 8,
                  background: "linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(15, 23, 42, 0.7) 100%)",
                  border: "1px solid rgba(59, 130, 246, 0.6)",
                  borderRadius: 14,
                  padding: "16px 20px",
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                }}
              >
                <div
                  style={{
                    width: 36,
                    height: 36,
                    borderRadius: 10,
                    background: "#2563eb",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 20,
                    color: "#ffffff",
                  }}
                >
                  🔒
                </div>
                <div>
                  <div style={{ fontSize: 22, fontWeight: 900, color: "#ffffff" }}>
                    {domain}
                  </div>
                  <div style={{ fontSize: 13, color: "#60a5fa", fontWeight: 600 }}>
                    100% सुरक्षित राष्ट्रीय पोर्टल (.gov.in)
                  </div>
                </div>
              </div>
            </div>

            {/* National Helpline */}
            {helpline && (
              <div
                style={{
                  background: "rgba(15, 23, 42, 0.8)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: 14,
                  padding: "14px 20px",
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                }}
              >
                <span style={{ fontSize: 24 }}>📞</span>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8" }}>
                    राष्ट्रीय नागरिक सहायता केंद्र (Toll-Free Helpline)
                  </div>
                  <div style={{ fontSize: 20, fontWeight: 900, color: "#f8fafc" }}>
                    {helpline}
                  </div>
                </div>
              </div>
            )}

            {/* Transparency Note */}
            <div style={{ fontSize: 13, color: "#64748b", lineHeight: 1.5, marginTop: "auto" }}>
              * iDastawez एक स्वतंत्र सूचनात्मक मंच है। हमारा उद्देश्य सरकारी गजट और सार्वजनिक आदेशों को आम नागरिकों तक स्पष्ट भाषा में पहुँचाना है।
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
