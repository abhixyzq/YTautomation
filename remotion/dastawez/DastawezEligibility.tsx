import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface DastawezEligibilityProps {
  schemeName: string;
  ministry?: string;
  eligibilityYes?: string[];
  eligibilityNo?: string[];
  category?: string;
  evidence?: EvidenceMetadata;
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
  category,
  evidence,
  currentActIndex = 2,
  totalActs = 6,
  portalUrl,
  officialPortalDomain,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.03], {
    extrapolateRight: "clamp",
  });

  const entrance = spring({ frame, fps, delay: 4, config: { damping: 14, stiffness: 100 } });

  // Phase transition: around frame 70 (approx half-way through the first 30s)
  // Phase 1 (0 to 70): Focus on Eligible citizens (Blue/Green)
  // Phase 2 (70+): Shift focus to Disqualified/Ineligible (Red Alert)
  const isPhase2 = frame >= 70;

  const leftCardSpring = spring({ frame, fps, delay: 10, config: { damping: 14 } });
  const rightCardSpring = spring({ frame, fps, delay: 55, config: { damping: 14 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

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
      {/* Subtle Grid */}
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

      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="पात्रता मानदंड (Eligibility)"
        portalDomain={domain}
      />

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
          gap: 20,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Header Title Block */}
        <div style={{ transform: `translateY(${(1 - entrance) * 20}px)`, opacity: entrance }}>
          <div style={{ fontSize: 15, fontWeight: 800, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 1 }}>
            आधिकारिक पात्रता चेकलिस्ट 2026
          </div>
          <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "4px 0 0 0" }}>
            किसे मिलेगा लाभ और कौन है अपात्र?
          </h2>
        </div>

        {/* Two-Column Comparison Grid */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 28, marginTop: 4 }}>
          {/* Column 1: Eligible Citizens (Blue/Green Accents) */}
          <div
            style={{
              background: isPhase2 ? "rgba(10, 18, 36, 0.6)" : "rgba(10, 22, 46, 0.9)",
              border: isPhase2 ? "1px solid rgba(59, 130, 246, 0.3)" : "2px solid rgba(59, 130, 246, 0.8)",
              borderRadius: 22,
              padding: "24px 28px",
              boxShadow: isPhase2 ? "0 10px 30px rgba(0,0,0,0.4)" : "0 18px 45px rgba(0, 0, 0, 0.7), 0 0 25px rgba(37, 99, 235, 0.25)",
              display: "flex",
              flexDirection: "column",
              gap: 14,
              transform: `translateX(${(1 - leftCardSpring) * -30}px)`,
              opacity: leftCardSpring,
              transition: "all 0.4s ease",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div
                style={{
                  background: "rgba(34, 197, 94, 0.2)",
                  border: "1px solid rgba(34, 197, 94, 0.5)",
                  borderRadius: 8,
                  padding: "4px 14px",
                  fontSize: 14,
                  fontWeight: 900,
                  color: "#4ade80",
                }}
              >
                ✓ कौन आवेदन कर सकते हैं (ELIGIBLE)
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {eligibilityYes.map((item, idx) => {
                const itemDelay = 12 + idx * 14;
                const itemSpring = spring({ frame, fps, delay: itemDelay, config: { damping: 14 } });

                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 12,
                      background: "rgba(15, 23, 42, 0.6)",
                      border: "1px solid rgba(255, 255, 255, 0.08)",
                      borderRadius: 12,
                      padding: "10px 14px",
                      transform: `translateY(${(1 - itemSpring) * 15}px)`,
                      opacity: itemSpring,
                    }}
                  >
                    <span style={{ fontSize: 18, color: "#4ade80", marginTop: 2 }}>✓</span>
                    <span style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", lineHeight: 1.4 }}>
                      {item}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Column 2: Ineligible / Excluded (Stark Red Warning) */}
          <div
            style={{
              background: isPhase2 ? "rgba(26, 12, 16, 0.9)" : "rgba(15, 23, 42, 0.6)",
              border: isPhase2 ? "2px solid rgba(239, 68, 68, 0.8)" : "1px solid rgba(255, 255, 255, 0.1)",
              borderRadius: 22,
              padding: "24px 28px",
              boxShadow: isPhase2 ? "0 18px 45px rgba(0, 0, 0, 0.7), 0 0 25px rgba(239, 68, 68, 0.25)" : "0 10px 30px rgba(0,0,0,0.4)",
              display: "flex",
              flexDirection: "column",
              gap: 14,
              transform: `translateX(${(1 - rightCardSpring) * 30}px)`,
              opacity: rightCardSpring,
              transition: "all 0.4s ease",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div
                style={{
                  background: "rgba(239, 68, 68, 0.2)",
                  border: "1px solid rgba(239, 68, 68, 0.6)",
                  borderRadius: 8,
                  padding: "4px 14px",
                  fontSize: 14,
                  fontWeight: 900,
                  color: "#f87171",
                }}
              >
                ✕ कौन पात्र नहीं हैं (DISQUALIFIED)
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {eligibilityNo.map((item, idx) => {
                const itemDelay = 60 + idx * 14;
                const itemSpring = spring({ frame, fps, delay: itemDelay, config: { damping: 14 } });

                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 12,
                      background: "rgba(15, 23, 42, 0.6)",
                      border: "1px solid rgba(239, 68, 68, 0.2)",
                      borderRadius: 12,
                      padding: "10px 14px",
                      transform: `translateY(${(1 - itemSpring) * 15}px)`,
                      opacity: itemSpring,
                    }}
                  >
                    <span style={{ fontSize: 18, color: "#ef4444", marginTop: 2 }}>✕</span>
                    <span style={{ fontSize: 17, fontWeight: 700, color: "#f8fafc", lineHeight: 1.4 }}>
                      {item}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
