import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { WhatChangedData, EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

interface DastawezWhatChangedProps {
  schemeName: string;
  ministry?: string;
  whatChanged?: WhatChangedData;
  whyChanged?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  evidence?: EvidenceMetadata;
  category?: string;
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezWhatChanged: React.FC<DastawezWhatChangedProps> = ({
  schemeName,
  ministry,
  whatChanged,
  whyChanged,
  portalUrl,
  officialPortalDomain,
  evidence,
  category,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 2,
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

  const oldRule = whatChanged?.old_rule || "पहले सामान्य नियमों के तहत सुविधा चालू थी।";
  const newRule = whatChanged?.new_rule || "नया सरकारी निर्देश जारी किया गया है।";
  const deadline = whatChanged?.deadline || "अंतिम तिथि से पूर्व सत्यापन आवश्यक";
  const reason = whyChanged || "फर्जी लाभार्थियों की रोकथाम और पात्र नागरिकों तक 100% शत-प्रतिशत लाभ पहुंचाने हेतु।";

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
      {/* Full-Screen Container (Top 36px to Bottom 96px) */}
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
          {/* Left: Brand + Official Portal */}
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
                background: "rgba(2, 132, 199, 0.12)",
                border: "1px solid rgba(2, 132, 199, 0.3)",
                color: "#0369a1",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
              }}
            >
              ⚖️ नियमों में आधिकारिक संशोधन
            </div>
          </div>

          {/* Right: Step Indicator */}
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
              नियमों में क्या बदला (नया बनाम पुराना)
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
            पहले क्या था और अब 2026 में क्या नया नियम लागू हुआ है?
          </h1>
        </div>

        {/* 4-Card Comparative Dashboard Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.1fr 1.2fr 1fr 1.15fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Card 1: Old Rule (Soft Red Glass) */}
          <div
            style={{
              background: "rgba(254, 242, 242, 0.95)",
              border: "1.5px solid rgba(248, 113, 113, 0.4)",
              borderRadius: 22,
              padding: "24px 24px",
              boxShadow: "0 14px 34px rgba(239, 68, 68, 0.06)",
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
                  background: "#fee2e2",
                  color: "#b91c1c",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>✕</span>
                <span>पहले का पुराना नियम (व्यवस्था)</span>
              </div>

              <div
                style={{
                  fontSize: 21,
                  fontWeight: 700,
                  color: "#334155",
                  lineHeight: 1.5,
                  marginTop: 14,
                }}
              >
                {oldRule}
              </div>
            </div>

            <div
              style={{
                background: "rgba(255, 255, 255, 0.85)",
                border: "1px solid rgba(248, 113, 113, 0.25)",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 700,
                color: "#991b1b",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>⚠️</span>
              <span>पूर्व व्यवस्था अब समाप्त / संशोधित</span>
            </div>
          </div>

          {/* Card 2: New 2026 Rule (Luminous Emerald Glass) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.94) 100%)",
              border: "2.5px solid rgba(16, 185, 129, 0.6)",
              borderRadius: 22,
              padding: "24px 26px",
              boxShadow: "0 18px 42px rgba(16, 185, 129, 0.12), 0 0 16px rgba(16, 185, 129, 0.1)",
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
                  background: "#d1fae5",
                  color: "#047857",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>✓</span>
                <span>अब 2026 का नया नियम (लागू)</span>
              </div>

              <div
                style={{
                  fontSize: 22,
                  fontWeight: 900,
                  color: "#064e3b",
                  lineHeight: 1.45,
                  marginTop: 14,
                }}
              >
                {newRule}
              </div>
            </div>

            <div
              style={{
                background: "rgba(255, 255, 255, 0.9)",
                border: "1px solid rgba(16, 185, 129, 0.3)",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 800,
                color: "#059669",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>🔒</span>
              <span>समयबद्ध सत्यापन अनिवार्य</span>
            </div>
          </div>

          {/* Card 3: Why It Changed (Royal Blue Glass) */}
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              border: "1.5px solid rgba(2, 132, 199, 0.3)",
              borderRadius: 22,
              padding: "24px 24px",
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
                <span>💡</span>
                <span>नियम बदलने का मुख्य कारण</span>
              </div>

              <div
                style={{
                  fontSize: 18,
                  fontWeight: 700,
                  color: "#1e293b",
                  lineHeight: 1.5,
                  marginTop: 14,
                }}
              >
                {reason}
              </div>
            </div>

            <div
              style={{
                background: "#f0f9ff",
                border: "1px solid #bae6fd",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 700,
                color: "#0369a1",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>⚡</span>
              <span>100% पारदर्शिता एवं डायरेक्ट ट्रांसफर</span>
            </div>
          </div>

          {/* Card 4: Dedicated Visual Media Card */}
          <DastawezMediaCard
            imagePath={imgPath}
            videoPath={vidPath}
            title={imgTitle || "सत्यापन एवं सरकारी प्रक्रिया"}
            attribution={mediaAttr || "Wikimedia / Govt Source"}
            badgeLabel="📸 नियम सत्यापन रिकॉर्ड"
            mediaType="image"
            style={{
              height: "100%",
            }}
            fallbackIcon="⚖️"
            fallbackTitle="आधिकारिक नियम संशोधन अभिलेख"
          />
        </div>

        {/* Bottom Saffron Deadline & Urgency Banner */}
        <div
          style={{
            marginTop: 14,
            background: "rgba(255, 247, 237, 0.96)",
            border: "1.5px solid rgba(249, 115, 22, 0.45)",
            borderRadius: 16,
            padding: "14px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 8px 24px rgba(249, 115, 22, 0.08)",
            transform: `translateY(${(1 - beat3Spring) * 10}px)`,
            opacity: beat3Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                background: "linear-gradient(135deg, #ea580c, #f97316)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 18,
                color: "#ffffff",
                boxShadow: "0 2px 8px rgba(234, 88, 12, 0.3)",
              }}
            >
              ⏰
            </div>
            <div>
              <div style={{ fontSize: 11, fontWeight: 800, color: "#9a3412", textTransform: "uppercase" }}>
                अंतिम तिथि एवं जरूरी निर्देश (OFFICIAL DEADLINE)
              </div>
              <div style={{ fontSize: 17, fontWeight: 800, color: "#7c2d12" }}>
                {deadline}
              </div>
            </div>
          </div>

          <div
            style={{
              background: "#ffffff",
              border: "1px solid rgba(249, 115, 22, 0.3)",
              padding: "6px 14px",
              borderRadius: 8,
              fontSize: 12,
              fontWeight: 700,
              color: "#ea580c",
            }}
          >
            समय पर सत्यापन न होने पर लाभ रुक सकता है
          </div>
        </div>
      </div>
    </div>
  );
};
