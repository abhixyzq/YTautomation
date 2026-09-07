import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { WhatChangedData, EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";

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

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const cardSpring = spring({ frame, fps, delay: 10, config: { damping: 12, stiffness: 100 } });
  const deadlineSpring = spring({ frame, fps, delay: 18, config: { damping: 12, stiffness: 100 } });

  const oldRule = whatChanged?.old_rule || "पहले सामान्य प्रक्रिया के तहत सुविधा उपलब्ध थी।";
  const newRule = whatChanged?.new_rule || "अब नए सरकारी आदेश के तहत ऑनलाइन सत्यापन और बायोमेट्रिक अनिवार्य कर दिया गया है।";
  const deadline = whatChanged?.deadline || "समय सीमा के भीतर प्रक्रिया पूर्ण करना आवश्यक";

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        padding: "36px 64px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        boxSizing: "border-box",
        pointerEvents: "none",
        zIndex: 10,
      }}
    >
      {/* 1. Top Meta HUD */}
      <div style={{ transform: `translateY(${(1 - hudSpring) * -20}px)`, opacity: hudSpring }}>
        <DastawezTopHud
          schemeName={schemeName}
          domain={domain}
          urgencyBadge="नया सरकारी नियम 2026"
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="नियम में क्या बदला?"
        />
      </div>

      {/* 2. Floating Split Comparison HUD */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1.15fr",
          gap: 36,
          alignItems: "stretch",
          flex: 1,
          marginTop: 24,
          marginBottom: 24,
          transform: `translateY(${(1 - cardSpring) * 30}px)`,
          opacity: cardSpring,
        }}
      >
        {/* Left: Old Rule Card (Muted Amber/Red Glass) */}
        <div
          style={{
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "1.5px solid rgba(244, 63, 94, 0.35)",
            borderRadius: 24,
            padding: "32px 36px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: "0 20px 50px rgba(0, 0, 0, 0.6)",
          }}
        >
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
              <span
                style={{
                  background: "rgba(244, 63, 94, 0.2)",
                  border: "1px solid rgba(244, 63, 94, 0.6)",
                  color: "#fda4af",
                  fontSize: 13,
                  fontWeight: 900,
                  padding: "5px 12px",
                  borderRadius: 10,
                  letterSpacing: 0.8,
                }}
              >
                🔴 पहले क्या नियम था
              </span>
            </div>
            <div
              style={{
                fontSize: 22,
                fontWeight: 700,
                color: "#cbd5e1",
                lineHeight: 1.5,
              }}
            >
              {oldRule}
            </div>
          </div>

          <div
            style={{
              fontSize: 13,
              color: "#64748b",
              borderTop: "1px solid rgba(255, 255, 255, 0.1)",
              paddingTop: 12,
              marginTop: 16,
            }}
          >
            ❌ पुरानी व्यवस्था अब अमान्य
          </div>
        </div>

        {/* Right: New Directive Card (Luminous Emerald/Cyan Glass) */}
        <div
          style={{
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid rgba(16, 185, 129, 0.5)",
            borderRadius: 24,
            padding: "32px 36px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: "0 24px 60px rgba(0, 0, 0, 0.65), 0 0 30px rgba(16, 185, 129, 0.15)",
          }}
        >
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
              <span
                style={{
                  background: "rgba(16, 185, 129, 0.2)",
                  border: "1px solid rgba(16, 185, 129, 0.6)",
                  color: "#6ee7b7",
                  fontSize: 13,
                  fontWeight: 900,
                  padding: "5px 12px",
                  borderRadius: 10,
                  letterSpacing: 0.8,
                }}
              >
                🟢 2026 में क्या बदला (नया नियम)
              </span>
            </div>
            <div
              style={{
                fontSize: 24,
                fontWeight: 800,
                color: "#f8fafc",
                lineHeight: 1.5,
              }}
            >
              {newRule}
            </div>
          </div>

          <div
            style={{
              fontSize: 14,
              fontWeight: 700,
              color: "#34d399",
              borderTop: "1px solid rgba(16, 185, 129, 0.2)",
              paddingTop: 12,
              marginTop: 16,
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span>✅</span>
            <span>नया आदेश आधिकारिक पोर्टल पर लागू</span>
          </div>
        </div>
      </div>

      {/* 3. Floating Deadline & Consequence HUD Ribbon */}
      <div
        style={{
          transform: `translateY(${(1 - deadlineSpring) * 20}px)`,
          opacity: deadlineSpring,
          background: "linear-gradient(90deg, rgba(225, 29, 72, 0.25) 0%, rgba(15, 23, 42, 0.92) 30%, rgba(15, 23, 42, 0.92) 70%, rgba(225, 29, 72, 0.25) 100%)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1.5px solid rgba(244, 63, 94, 0.5)",
          borderRadius: 20,
          padding: "16px 36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: "0 14px 40px rgba(0, 0, 0, 0.5)",
          marginBottom: 50,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <span style={{ fontSize: 24 }}>⏰</span>
          <div>
            <div style={{ fontSize: 12, fontWeight: 800, color: "#fca5a5", textTransform: "uppercase" }}>
              अंतिम तिथि / समय-सीमा (DEADLINE)
            </div>
            <div style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>
              {deadline}
            </div>
          </div>
        </div>

        <div
          style={{
            background: "rgba(225, 29, 72, 0.3)",
            border: "1px solid rgba(244, 63, 94, 0.6)",
            color: "#fecdd3",
            padding: "8px 20px",
            borderRadius: 14,
            fontSize: 14,
            fontWeight: 800,
          }}
        >
          ⚠️ लापरवाही पर सरकारी लाभ रोका जा सकता है
        </div>
      </div>
    </div>
  );
};
