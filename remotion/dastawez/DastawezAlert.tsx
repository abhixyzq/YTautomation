import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

interface DastawezAlertProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  warning?: string;
  dosAndDonts?: string[];
  category?: string;
  evidence?: EvidenceMetadata;
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
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
  dosAndDonts,
  category,
  evidence,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 6,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.02], {
    extrapolateRight: "clamp",
  });

  const beat1Spring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 110 } });
  const beat2Spring = spring({ frame, fps, delay: 14, config: { damping: 14, stiffness: 95 } });
  const beat3Spring = spring({ frame, fps, delay: 28, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const alertMessage =
    warning ||
    "यह पूरी सरकारी प्रक्रिया 100% निःशुल्क है। किसी भी साइबर कैफे वाले या बिचौलिए को कोई अवैध शुल्क न दें।";

  const phone = helpline || "1967 / 1800-1800-150";

  const securityPoints =
    dosAndDonts && dosAndDonts.length > 0
      ? dosAndDonts
      : [
          "अपना आधार OTP या बैंक पासवर्ड किसी अनजान व्यक्ति को न दें।",
          "अवैध पैसे मांगने पर सीधे हेल्पलाइन पर तुरंत शिकायत दर्ज करें।",
          "अनधिकृत APK फाइल्स या संदिग्ध मैसेज लिंक पर क्लिक न करें।",
        ];

  const imgPath = visualMedia?.official_image_path || officialImagePath;
  const imgTitle = visualMedia?.official_image_title || officialImageTitle;
  const vidPath = visualMedia?.broll_video_path || brollVideoPath;
  const mediaAttr = visualMedia?.attribution || attribution;

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Full-Screen Container */}
      <div
        style={{
          position: "absolute",
          top: 36,
          bottom: 104,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Sleek Integrated Top Meta-Bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateY(${(1 - beat1Spring) * -14}px)`,
            opacity: beat1Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                background: "rgba(255, 255, 255, 0.94)",
                padding: "6px 14px",
                borderRadius: 12,
                border: "1px solid rgba(2, 132, 199, 0.25)",
                boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
              }}
            >
              <div
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: 6,
                  background: "linear-gradient(135deg, #ea580c, #f97316)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#fff",
                  fontWeight: 900,
                  fontSize: 13,
                }}
              >
                द
              </div>
              <span style={{ fontSize: 15, fontWeight: 900, color: "#0f172a" }}>@iDastawez</span>
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                background: "rgba(238, 242, 255, 0.95)",
                border: "1px solid rgba(99, 102, 241, 0.3)",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
                color: "#3730a3",
              }}
            >
              <span>🏛️</span>
              <span>{domain}</span>
            </div>

            <div
              style={{
                background: "linear-gradient(135deg, #ea580c, #dc2626)",
                color: "#ffffff",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
                boxShadow: "0 2px 8px rgba(234, 88, 12, 0.3)",
              }}
            >
              🛡️ नागरिक सुरक्षा व हेल्पलाइन
            </div>
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(255, 255, 255, 0.94)",
              padding: "6px 16px",
              borderRadius: 12,
              border: "1px solid rgba(2, 132, 199, 0.2)",
              boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
            }}
          >
            <span style={{ fontSize: 13, fontWeight: 900, color: "#0284c7" }}>
              भाग {currentActIndex}/{totalActs}
            </span>
            <span style={{ fontSize: 12, color: "#94a3b8" }}>•</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#334155" }}>
              सावधानी व आधिकारिक हेल्पलाइन
            </span>
          </div>
        </div>

        {/* Section Headline */}
        <div
          style={{
            marginTop: 10,
            marginBottom: 10,
            transform: `translateY(${(1 - beat1Spring) * 12}px)`,
            opacity: beat1Spring,
          }}
        >
          <h1
            style={{
              fontSize: 38,
              fontWeight: 900,
              lineHeight: 1.25,
              color: "#0f172a",
              margin: 0,
              letterSpacing: "-0.5px",
            }}
          >
            धोखाधड़ी से बचें एवं किसी भी समस्या पर यहाँ संपर्क करें
          </h1>
        </div>

        {/* 4-Card Security Dashboard Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.1fr 1.1fr 1fr 1.05fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Card 1: Fraud Alert (Saffron / Rose Glass) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 247, 237, 0.94) 100%)",
              border: "2px solid rgba(249, 115, 22, 0.5)",
              borderRadius: 22,
              padding: "24px 24px",
              boxShadow: "0 16px 40px rgba(249, 115, 22, 0.08)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  background: "#ffedd5",
                  color: "#c2410c",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>⚠️</span>
                <span>साइबर फ्रॉड व अवैध वसूली चेतावनी</span>
              </div>

              <div
                style={{
                  fontSize: 22,
                  fontWeight: 800,
                  color: "#7c2d12",
                  lineHeight: 1.45,
                  marginTop: 14,
                }}
              >
                {alertMessage}
              </div>
            </div>

            <div
              style={{
                background: "rgba(255, 255, 255, 0.9)",
                border: "1px solid rgba(249, 115, 22, 0.3)",
                padding: "10px 14px",
                borderRadius: 12,
                display: "flex",
                alignItems: "center",
                gap: 10,
              }}
            >
              <span style={{ fontSize: 20 }}>🚫</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: "#9a3412" }}>
                अज्ञात APK फाइल्स व गैर-सरकारी लिंक्स से सावधान रहें
              </span>
            </div>
          </div>

          {/* Card 2: Official Helpline Dialer (Emerald Green Glass) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.94) 100%)",
              border: "2.5px solid rgba(16, 185, 129, 0.6)",
              borderRadius: 22,
              padding: "24px 24px",
              boxShadow: "0 16px 40px rgba(16, 185, 129, 0.1)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span
                  style={{
                    background: "#d1fae5",
                    color: "#047857",
                    fontSize: 12,
                    fontWeight: 900,
                    padding: "4px 12px",
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
                    padding: "3px 8px",
                    borderRadius: 6,
                  }}
                >
                  टोल-फ्री
                </span>
              </div>

              {/* Dialer Large Number Block */}
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.95)",
                  border: "1.5px solid rgba(16, 185, 129, 0.35)",
                  borderRadius: 16,
                  padding: "16px 18px",
                  display: "flex",
                  alignItems: "center",
                  gap: 14,
                  marginTop: 16,
                }}
              >
                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 12,
                    background: "linear-gradient(135deg, #059669 0%, #10b981 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 24,
                    color: "#ffffff",
                    boxShadow: "0 4px 12px rgba(16, 185, 129, 0.3)",
                  }}
                >
                  📞
                </div>
                <div>
                  <div style={{ fontSize: 11, fontWeight: 800, color: "#065f46", textTransform: "uppercase" }}>
                    सीधे सहायता हेतु डायल करें
                  </div>
                  <div style={{ fontSize: 26, fontWeight: 900, color: "#064e3b", letterSpacing: 0.5 }}>
                    {phone}
                  </div>
                </div>
              </div>
            </div>

            <div
              style={{
                fontSize: 12,
                fontWeight: 700,
                color: "#059669",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>✓</span> भारत सरकार द्वारा अधिकृत नागरिक सहायता डेस्क
            </div>
          </div>

          {/* Card 3: Citizen Security Checklist (Sky Blue Glass) */}
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              border: "1.5px solid rgba(2, 132, 199, 0.3)",
              borderRadius: 22,
              padding: "24px 22px",
              boxShadow: "0 14px 34px rgba(15, 23, 42, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  background: "rgba(2, 132, 199, 0.12)",
                  color: "#0284c7",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>🛡️</span>
                <span>नागरिक सुरक्षा नियम</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
                {securityPoints.map((pt, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 8,
                      background: "#f8fafc",
                      border: "1px solid #e2e8f0",
                      padding: "8px 12px",
                      borderRadius: 10,
                    }}
                  >
                    <span style={{ color: "#0284c7", fontWeight: 900, fontSize: 14 }}>•</span>
                    <span style={{ fontSize: 13, fontWeight: 700, color: "#1e293b", lineHeight: 1.35 }}>
                      {pt}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                background: "#eff6ff",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 700,
                color: "#1d4ed8",
                textAlign: "center",
              }}
            >
              100% सुरक्षित नागरिक अधिकार
            </div>
          </div>

          {/* Card 4: Dedicated Visual Media Card */}
          <DastawezMediaCard
            imagePath={imgPath}
            videoPath={vidPath}
            title={imgTitle || "नागरिक सहायता एवं सुरक्षा व्यवस्था"}
            attribution={mediaAttr || "Wikimedia / Govt Source"}
            badgeLabel="🛡️ हेल्पलाइन दृश्य"
            mediaType="video"
            style={{
              height: "100%",
            }}
            fallbackIcon="📞"
            fallbackTitle="राष्ट्रीय नागरिक सहायता डेस्क"
          />
        </div>

        {/* Bottom Safety Guarantee Bar */}
        <div
          style={{
            marginTop: 14,
            background: "rgba(255, 255, 255, 0.94)",
            backdropFilter: "blur(16px)",
            border: "1.5px solid rgba(2, 132, 199, 0.25)",
            borderRadius: 16,
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 8px 24px rgba(15, 23, 42, 0.05)",
            transform: `translateY(${(1 - beat3Spring) * 10}px)`,
            opacity: beat3Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 18 }}>🔒</span>
            <span style={{ fontSize: 15, fontWeight: 800, color: "#0f172a" }}>
              हमेशा केवल आधिकारिक सरकारी पोर्टल{" "}
              <span style={{ color: "#0284c7", fontWeight: 900 }}>https://{domain}</span> पर ही अपनी व्यक्तिगत जानकारी दर्ज करें।
            </span>
          </div>

          <div
            style={{
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              padding: "4px 12px",
              borderRadius: 8,
              fontSize: 12,
              fontWeight: 800,
              color: "#1d4ed8",
            }}
          >
            सुरक्षित नागरिक सेवा
          </div>
        </div>
      </div>
    </div>
  );
};
