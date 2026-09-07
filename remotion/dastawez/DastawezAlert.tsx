import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface DastawezAlertProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  warning?: string;
  category?: string;
  evidence?: EvidenceMetadata;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezAlert: React.FC<DastawezAlertProps> = ({
  schemeName,
  ministry,
  portalUrl,
  officialPortalDomain,
  helpline,
  warning,
  category,
  evidence,
  currentActIndex = 5,
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

  const alertMessage =
    warning ||
    "यह पूरी सरकारी प्रक्रिया 100% निःशुल्क है। किसी भी साइबर कैफे वाले या बिचौलिए को कोई अवैध शुल्क न दें।";

  const phone = helpline || "1800-180-1961 / 1967";

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
        actTitle="सावधानी व आधिकारिक हेल्पलाइन"
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
              background: "rgba(234, 88, 12, 0.12)",
              border: "1px solid rgba(234, 88, 12, 0.35)",
              color: "#c2410c",
              fontSize: 14,
              fontWeight: 800,
              padding: "6px 18px",
              borderRadius: 100,
              textTransform: "uppercase",
              letterSpacing: 0.6,
            }}
          >
            🛡️ नागरिक सुरक्षा व चेतावनी
          </span>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a" }}>
            धोखाधड़ी से बचें एवं किसी भी समस्या पर यहाँ संपर्क करें
          </span>
        </div>

        {/* 2-Column Alert & Dialer Stage */}
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 26 }}>
          {/* Left Card: Fraud Alert & Caution (Warm Saffron Glass) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 247, 237, 0.92) 100%)",
              border: "2px solid rgba(249, 115, 22, 0.5)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 45px rgba(249, 115, 22, 0.1)",
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
                    background: "#ffedd5",
                    color: "#c2410c",
                    fontSize: 13,
                    fontWeight: 800,
                    padding: "5px 14px",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span>⚠️</span> महत्वपूर्ण आधिकारिक चेतावनी
                </span>
                <span style={{ fontSize: 12, fontWeight: 700, color: "#ea580c" }}>
                  (साइबर फ्रॉड से बचाव)
                </span>
              </div>

              <div style={{ fontSize: 23, fontWeight: 800, color: "#7c2d12", lineHeight: 1.45 }}>
                {alertMessage}
              </div>
            </div>

            {/* Zero Fee Guarantee Box */}
            <div
              style={{
                background: "rgba(255, 255, 255, 0.9)",
                border: "1px solid rgba(249, 115, 22, 0.25)",
                borderRadius: 14,
                padding: "12px 18px",
                display: "flex",
                alignItems: "center",
                gap: 12,
              }}
            >
              <span style={{ fontSize: 22 }}>🚫</span>
              <span style={{ fontSize: 14, fontWeight: 700, color: "#9a3412" }}>
                अनजान व्हाट्सएप मैसेज या एसएमएस में आए किसी भी अनधिकृत APK या लिंक पर क्लिक न करें।
              </span>
            </div>
          </div>

          {/* Right Card: Official Helpline Dialer (Emerald Green Glass) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.92) 100%)",
              border: "2.5px solid rgba(16, 185, 129, 0.6)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 16px 45px rgba(16, 185, 129, 0.12), 0 0 25px rgba(16, 185, 129, 0.08)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 18,
              transform: `translateX(${(1 - card2Spring) * 25}px)`,
              opacity: card2Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
                <span
                  style={{
                    background: "#d1fae5",
                    color: "#047857",
                    fontSize: 13,
                    fontWeight: 800,
                    padding: "5px 14px",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span>📞</span> राष्ट्रीय आधिकारिक हेल्पलाइन
                </span>
                <span
                  style={{
                    background: "#10b981",
                    color: "#ffffff",
                    fontSize: 11,
                    fontWeight: 800,
                    padding: "3px 10px",
                    borderRadius: 6,
                  }}
                >
                  टोल-फ्री 100% मुफ्त
                </span>
              </div>

              {/* Dialer Large Number Block */}
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.95)",
                  border: "1.5px solid rgba(16, 185, 129, 0.35)",
                  borderRadius: 16,
                  padding: "16px 20px",
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  marginTop: 10,
                }}
              >
                <div
                  style={{
                    width: 52,
                    height: 52,
                    borderRadius: 14,
                    background: "linear-gradient(135deg, #059669 0%, #10b981 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 26,
                    color: "#ffffff",
                    boxShadow: "0 4px 14px rgba(16, 185, 129, 0.35)",
                  }}
                >
                  📞
                </div>
                <div>
                  <div style={{ fontSize: 11, fontWeight: 800, color: "#065f46", textTransform: "uppercase" }}>
                    सीधे सहायता हेतु कॉल करें
                  </div>
                  <div style={{ fontSize: 30, fontWeight: 900, color: "#064e3b", letterSpacing: 0.5 }}>
                    {phone}
                  </div>
                </div>
              </div>
            </div>

            {/* Ministry Support Desk Pill */}
            <div
              style={{
                fontSize: 13,
                fontWeight: 700,
                color: "#059669",
                display: "flex",
                alignItems: "center",
                gap: 8,
              }}
            >
              <span>✓</span> भारत सरकार द्वारा अधिकृत नागरिक सहायता केंद्र (Customer Care Desk)
            </div>
          </div>
        </div>

        {/* Bottom Safety Guarantee Bar */}
        <div
          style={{
            background: "rgba(239, 246, 255, 0.95)",
            border: "1px solid rgba(59, 130, 246, 0.3)",
            borderRadius: 14,
            padding: "12px 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 16 }}>🔒</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: "#1e40af" }}>
              हमेशा केवल आधिकारिक सरकारी पोर्टल {domain} पर ही अपनी व्यक्तिगत जानकारी दर्ज करें।
            </span>
          </div>
          <span style={{ fontSize: 12, fontWeight: 800, color: "#0284c7" }}>
            सुरक्षित नागरिक सेवा
          </span>
        </div>
      </div>
    </div>
  );
};
