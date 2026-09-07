import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { WhatChangedData, EvidenceMetadata } from "./types";
import { DastawezHeader } from "./DastawezHeader";

interface DastawezWhatChangedProps {
  schemeName: string;
  ministry?: string;
  whatChanged?: WhatChangedData;
  portalUrl?: string;
  officialPortalDomain?: string;
  evidence?: EvidenceMetadata;
  category?: string;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezWhatChanged: React.FC<DastawezWhatChangedProps> = ({
  schemeName,
  ministry,
  whatChanged,
  portalUrl,
  officialPortalDomain,
  evidence,
  category,
  currentActIndex = 2,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.025], {
    extrapolateRight: "clamp",
  });

  // Timed sequential reveals:
  const oldRuleSpring = spring({ frame, fps, delay: 5, config: { damping: 14, stiffness: 90 } });
  const newRuleSpring = spring({ frame, fps, delay: 25, config: { damping: 14, stiffness: 90 } });
  const deadlineSpring = spring({ frame, fps, delay: 50, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const oldRule = whatChanged?.old_rule || "पहले सामान्य नियमों के तहत सुविधा चालू थी।";
  const newRule = whatChanged?.new_rule || "नया सरकारी निर्देश जारी किया गया है।";
  const deadline = whatChanged?.deadline || "अंतिम तिथि से पूर्व सत्यापन आवश्यक";

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
        actTitle="नियम में क्या बदला (नया बनाम पुराना)"
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
          gap: 22,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Section Heading Pill */}
        <div style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
          <span
            style={{
              background: "rgba(2, 132, 199, 0.1)",
              border: "1px solid rgba(2, 132, 199, 0.3)",
              color: "#0369a1",
              fontSize: 14,
              fontWeight: 800,
              padding: "6px 18px",
              borderRadius: 100,
              textTransform: "uppercase",
              letterSpacing: 0.6,
            }}
          >
            ⚖️ नियमों में आधिकारिक बदलाव
          </span>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a" }}>
            पहले क्या था और अब क्या नया नियम लागू हुआ है?
          </span>
        </div>

        {/* Side-by-Side Comparison Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 26 }}>
          {/* Old Rule Card (Rose / Crimson Glass) */}
          <div
            style={{
              background: "rgba(254, 242, 242, 0.92)",
              border: "1.5px solid rgba(248, 113, 113, 0.4)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 14px 36px rgba(239, 68, 68, 0.06)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - oldRuleSpring) * -25}px)`,
              opacity: oldRuleSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span
                style={{
                  background: "#fee2e2",
                  color: "#b91c1c",
                  fontSize: 13,
                  fontWeight: 800,
                  padding: "5px 14px",
                  borderRadius: 8,
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                }}
              >
                <span>✕</span> पहले का पुराना नियम
              </span>
            </div>
            <div style={{ fontSize: 23, fontWeight: 700, color: "#334155", lineHeight: 1.5 }}>
              {oldRule}
            </div>
          </div>

          {/* New Rule Card (Mint / Emerald Glass) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.92) 100%)",
              border: "2.5px solid rgba(16, 185, 129, 0.6)",
              borderRadius: 24,
              padding: "28px 32px",
              boxShadow: "0 18px 45px rgba(16, 185, 129, 0.12), 0 0 25px rgba(16, 185, 129, 0.08)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - newRuleSpring) * 25}px)`,
              opacity: newRuleSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
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
                <span>✓</span> अब 2026 का नया नियम
              </span>
              <span style={{ fontSize: 12, fontWeight: 700, color: "#059669" }}>
                (लागू एवं अनिवार्य)
              </span>
            </div>
            <div style={{ fontSize: 24, fontWeight: 800, color: "#064e3b", lineHeight: 1.5 }}>
              {newRule}
            </div>
          </div>
        </div>

        {/* Bottom Saffron Deadline Banner */}
        <div
          style={{
            background: "rgba(255, 247, 237, 0.95)",
            border: "1.5px solid rgba(249, 115, 22, 0.45)",
            borderRadius: 20,
            padding: "18px 26px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 10px 30px rgba(249, 115, 22, 0.08)",
            transform: `translateY(${(1 - deadlineSpring) * 20}px)`,
            opacity: deadlineSpring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div
              style={{
                width: 44,
                height: 44,
                borderRadius: 12,
                background: "linear-gradient(135deg, #ea580c 0%, #f97316 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 22,
                color: "#ffffff",
                boxShadow: "0 4px 12px rgba(249, 115, 22, 0.3)",
              }}
            >
              ⏰
            </div>
            <div>
              <div style={{ fontSize: 12, fontWeight: 800, color: "#9a3412", textTransform: "uppercase", letterSpacing: 0.8 }}>
                अंतिम तिथि एवं जरूरी निर्देश (Official Deadline)
              </div>
              <div style={{ fontSize: 19, fontWeight: 800, color: "#7c2d12", marginTop: 2 }}>
                {deadline}
              </div>
            </div>
          </div>

          <div
            style={{
              background: "#ffffff",
              border: "1px solid rgba(249, 115, 22, 0.3)",
              padding: "8px 16px",
              borderRadius: 10,
              fontSize: 13,
              fontWeight: 700,
              color: "#ea580c",
            }}
          >
            समय पर पूरा न होने पर सेवा रुक सकती है
          </div>
        </div>
      </div>
    </div>
  );
};
