import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

interface DastawezEligibilityProps {
  schemeName: string;
  ministry?: string;
  eligibilityYes?: string[];
  eligibilityNo?: string[];
  priorityGroups?: string[];
  category?: string;
  evidence?: EvidenceMetadata;
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
  currentActIndex?: number;
  totalActs?: number;
  portalUrl?: string;
  officialPortalDomain?: string;
}

export const DastawezEligibility: React.FC<DastawezEligibilityProps> = ({
  schemeName,
  ministry,
  eligibilityYes = [],
  eligibilityNo = [],
  priorityGroups = [],
  category,
  evidence,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 3,
  totalActs = 6,
  portalUrl,
  officialPortalDomain,
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

  const yesList =
    eligibilityYes.length > 0
      ? eligibilityYes
      : ["राष्ट्रीय खाद्य सुरक्षा (NFSA) राशन कार्डधारक", "सभी पंजीकृत परिवार व पात्र नागरिक"];
  const noList =
    eligibilityNo.length > 0
      ? eligibilityNo
      : ["फर्जी या अपात्र यूनिट्स / मृतक सदस्य", "चार पहिया वाहन या इनकम टैक्स देने वाले परिवार"];
  const priorityList =
    priorityGroups.length > 0
      ? priorityGroups
      : ["वरिष्ठ नागरिक (70+ आयु वर्ग)", "महिला मुखिया व अंत्योदय (AAY) परिवार", "दिव्यांगजन एवं अत्यंत पिछड़े वर्ग"];

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
                background: "rgba(16, 185, 129, 0.12)",
                border: "1px solid rgba(16, 185, 129, 0.35)",
                color: "#047857",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
              }}
            >
              📋 पात्रता मानदंड 2026
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
              पात्रता मानदंड (Eligibility Criteria)
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
            कौन-कौन पात्र हैं और किन्हें इस योजना से बाहर रखा गया है?
          </h1>
        </div>

        {/* 4-Card Multi-Column Matrix Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.15fr 1fr 1.05fr 1.15fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Card 1: Eligible Citizens (Mint / Emerald Glass) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.94) 100%)",
              border: "2px solid rgba(16, 185, 129, 0.5)",
              borderRadius: 22,
              padding: "22px 24px",
              boxShadow: "0 14px 36px rgba(16, 185, 129, 0.08)",
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
                  <span>✓</span> पूरी तरह पात्र नागरिक
                </span>
                <span style={{ fontSize: 11, fontWeight: 800, color: "#059669" }}>स्वीकृत</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
                {yesList.map((item, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 10,
                      background: "rgba(255, 255, 255, 0.85)",
                      border: "1px solid rgba(16, 185, 129, 0.25)",
                      padding: "10px 14px",
                      borderRadius: 12,
                    }}
                  >
                    <span style={{ color: "#059669", fontWeight: 900, fontSize: 16 }}>✓</span>
                    <span style={{ fontSize: 16, fontWeight: 700, color: "#0f172a", lineHeight: 1.35 }}>
                      {item}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                background: "rgba(16, 185, 129, 0.12)",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 800,
                color: "#047857",
                textAlign: "center",
              }}
            >
              शत-प्रतिशत प्रत्यक्ष लाभ (100% Direct Entitlement)
            </div>
          </div>

          {/* Card 2: Priority Groups & Special Concessions (Sky Blue Glass) */}
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              border: "1.5px solid rgba(2, 132, 199, 0.3)",
              borderRadius: 22,
              padding: "22px 24px",
              boxShadow: "0 14px 34px rgba(15, 23, 42, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span
                  style={{
                    background: "rgba(2, 132, 199, 0.12)",
                    color: "#0284c7",
                    fontSize: 12,
                    fontWeight: 900,
                    padding: "4px 12px",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span>⭐</span> विशेष प्राथमिकता समूह
                </span>
                <span style={{ fontSize: 11, fontWeight: 800, color: "#0284c7" }}>प्राथमिकता</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
                {priorityList.map((item, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 10,
                      background: "#f0f9ff",
                      border: "1px solid #bae6fd",
                      padding: "10px 14px",
                      borderRadius: 12,
                    }}
                  >
                    <span style={{ color: "#0284c7", fontWeight: 900, fontSize: 16 }}>★</span>
                    <span style={{ fontSize: 15, fontWeight: 700, color: "#0369a1", lineHeight: 1.35 }}>
                      {item}
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
              विशेष काउंटर / त्वरित सत्यापन सुविधा
            </div>
          </div>

          {/* Card 3: Ineligible / Excluded (Warm Saffron / Rose Glass) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.98) 0%, rgba(254, 242, 242, 0.94) 100%)",
              border: "2px solid rgba(248, 113, 113, 0.45)",
              borderRadius: 22,
              padding: "22px 24px",
              boxShadow: "0 14px 36px rgba(239, 68, 68, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                <span
                  style={{
                    background: "#fee2e2",
                    color: "#b91c1c",
                    fontSize: 12,
                    fontWeight: 900,
                    padding: "4px 12px",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  <span>✕</span> अपात्र / बहिष्कृत श्रेणी
                </span>
                <span style={{ fontSize: 11, fontWeight: 800, color: "#b91c1c" }}>अस्वीकृत</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
                {noList.map((item, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 10,
                      background: "rgba(255, 255, 255, 0.85)",
                      border: "1px solid rgba(248, 113, 113, 0.25)",
                      padding: "10px 14px",
                      borderRadius: 12,
                    }}
                  >
                    <span style={{ color: "#dc2626", fontWeight: 900, fontSize: 16 }}>✕</span>
                    <span style={{ fontSize: 16, fontWeight: 700, color: "#334155", lineHeight: 1.35 }}>
                      {item}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div
              style={{
                background: "#fee2e2",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 800,
                color: "#991b1b",
                textAlign: "center",
              }}
            >
              गलत जानकारी देने पर दंड व वसूली संभव
            </div>
          </div>

          {/* Card 4: Dedicated Visual Media Card */}
          <DastawezMediaCard
            imagePath={imgPath}
            videoPath={vidPath}
            title={imgTitle || "नागरिक पात्रता एवं फील्ड रिकॉर्ड"}
            attribution={mediaAttr || "Wikimedia / Govt Source"}
            badgeLabel="👥 नागरिक पात्रता दृश्य"
            mediaType="image"
            style={{
              height: "100%",
            }}
            fallbackIcon="📋"
            fallbackTitle="आधिकारिक पात्रता सत्यापन रिकॉर्ड"
          />
        </div>

        {/* Bottom Full-Width Directive Bar */}
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
            <span style={{ fontSize: 18 }}>ℹ️</span>
            <span style={{ fontSize: 15, fontWeight: 800, color: "#0f172a" }}>
              यदि आप इन शर्तों को पूरा करते हैं, तो आधिकारिक पोर्टल{" "}
              <span style={{ color: "#0284c7", fontWeight: 900 }}>https://{domain}</span> पर तत्काल अपनी पात्रता की जांच करें।
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
            100% आधिकारिक मापदंड
          </div>
        </div>
      </div>
    </div>
  );
};
