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

  const entrance = spring({
    frame,
    fps,
    delay: 4,
    config: { damping: 14, stiffness: 100 },
  });

  // Timed sequential micro-states:
  // Beat 1: Old Rule (frame 10+)
  const oldRuleSpring = spring({
    frame,
    fps,
    delay: 10,
    config: { damping: 14, stiffness: 90 },
  });

  // Beat 2: New Rule (frame 35+)
  const newRuleSpring = spring({
    frame,
    fps,
    delay: 35,
    config: { damping: 14, stiffness: 90 },
  });

  // Beat 3: Deadline Box (frame 70+)
  const deadlineSpring = spring({
    frame,
    fps,
    delay: 70,
    config: { damping: 14, stiffness: 95 },
  });

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
        background: "radial-gradient(circle at 50% 25%, #081329 0%, #050a14 60%, #02050a 100%)",
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

      {/* Top Header */}
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="नियम में क्या बदलाव हुआ"
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
          transform: `scale(${interpolate(frame, [0, 900], [1.0, 1.03], { extrapolateRight: "clamp" })})`,
        }}
      >
        {/* Section Badge */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 12,
            background: "rgba(220, 38, 38, 0.12)",
            border: "1px solid rgba(239, 68, 68, 0.4)",
            padding: "8px 22px",
            borderRadius: 100,
            width: "fit-content",
            transform: `translateY(${(1 - entrance) * -20}px)`,
            opacity: entrance,
          }}
        >
          <span style={{ fontSize: 16, fontWeight: 800, color: "#f87171", letterSpacing: 0.8 }}>
            आधिकारिक संशोधन 2026 | OFFICIAL REGULATORY UPDATE
          </span>
        </div>

        {/* Title */}
        <h1
          style={{
            fontSize: 46,
            fontWeight: 900,
            color: "#ffffff",
            margin: 0,
            lineHeight: 1.25,
            textShadow: "0 4px 20px rgba(0, 0, 0, 0.6)",
            transform: `translateY(${(1 - entrance) * 20}px)`,
            opacity: entrance,
          }}
        >
          पहले क्या नियम था vs अब नया नियम क्या है?
        </h1>

        {/* Side-by-Side Comparison Matrix */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.2fr", gap: 28 }}>
          {/* Left: Old Rule Card (Muted, Slate) */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.75)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              borderRadius: 22,
              padding: "26px 30px",
              boxShadow: "0 14px 35px rgba(0, 0, 0, 0.5)",
              display: "flex",
              flexDirection: "column",
              gap: 14,
              transform: `translateX(${(1 - oldRuleSpring) * -30}px)`,
              opacity: oldRuleSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div
                style={{
                  background: "rgba(148, 163, 184, 0.2)",
                  borderRadius: 8,
                  padding: "4px 12px",
                  fontSize: 14,
                  fontWeight: 800,
                  color: "#94a3b8",
                }}
              >
                पहले की व्यवस्था (OLD RULE)
              </div>
            </div>
            <div style={{ fontSize: 22, fontWeight: 700, color: "#cbd5e1", lineHeight: 1.5 }}>
              {oldRule}
            </div>
            <div style={{ fontSize: 14, color: "#64748b", marginTop: "auto" }}>
              * पूर्व में लागू नियमों के अनुसार
            </div>
          </div>

          {/* Right: New Official Rule (Vibrant Cobalt Blue & Stark White) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(30, 58, 138, 0.35) 0%, rgba(10, 18, 36, 0.9) 100%)",
              border: "2px solid rgba(59, 130, 246, 0.65)",
              borderRadius: 22,
              padding: "26px 30px",
              boxShadow: "0 18px 45px rgba(0, 0, 0, 0.7), 0 0 25px rgba(37, 99, 235, 0.25)",
              display: "flex",
              flexDirection: "column",
              gap: 14,
              transform: `translateX(${(1 - newRuleSpring) * 30}px)`,
              opacity: newRuleSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div
                style={{
                  background: "rgba(37, 99, 235, 0.3)",
                  border: "1px solid rgba(59, 130, 246, 0.8)",
                  borderRadius: 8,
                  padding: "4px 14px",
                  fontSize: 14,
                  fontWeight: 900,
                  color: "#60a5fa",
                }}
              >
                ✓ नया आधिकारिक नियम 2026 (NEW DIRECTIVE)
              </div>
            </div>
            <div style={{ fontSize: 25, fontWeight: 800, color: "#ffffff", lineHeight: 1.5 }}>
              {newRule}
            </div>
            <div style={{ fontSize: 14, color: "#93c5fd", marginTop: "auto", fontWeight: 600 }}>
              * आधिकारिक मंत्रालय अधिसूचना अनुसार लागू
            </div>
          </div>
        </div>

        {/* Bottom Urgency & Deadline Banner */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.9)",
            borderLeft: "6px solid #ef4444",
            borderTop: "1px solid rgba(255, 255, 255, 0.1)",
            borderRight: "1px solid rgba(255, 255, 255, 0.1)",
            borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: "0 18px 18px 0",
            padding: "18px 28px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateY(${(1 - deadlineSpring) * 20}px)`,
            opacity: deadlineSpring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <span style={{ fontSize: 26 }}>⏳</span>
            <div>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#f87171", textTransform: "uppercase" }}>
                कार्रवाई एवं समयसीमा (DEADLINE)
              </div>
              <div style={{ fontSize: 20, fontWeight: 800, color: "#ffffff", marginTop: 2 }}>
                {deadline}
              </div>
            </div>
          </div>
          <div
            style={{
              background: "rgba(220, 38, 38, 0.2)",
              border: "1px solid rgba(239, 68, 68, 0.5)",
              borderRadius: 10,
              padding: "6px 16px",
              fontSize: 14,
              fontWeight: 800,
              color: "#fca5a5",
            }}
          >
            लापरवाही न बरतें
          </div>
        </div>
      </div>
    </div>
  );
};
