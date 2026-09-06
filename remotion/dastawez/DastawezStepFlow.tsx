import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface StepItem {
  step: number;
  title: string;
  desc: string;
}

interface DastawezStepFlowProps {
  schemeName: string;
  ministry?: string;
  applicationSteps?: StepItem[];
  steps?: StepItem[];
  portalUrl?: string;
  officialPortalDomain?: string;
  category?: string;
  evidence?: EvidenceMetadata;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezStepFlow: React.FC<DastawezStepFlowProps> = ({
  schemeName,
  ministry,
  applicationSteps,
  steps,
  portalUrl,
  officialPortalDomain,
  category,
  evidence,
  currentActIndex = 4,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.03], {
    extrapolateRight: "clamp",
  });

  const entrance = spring({ frame, fps, delay: 4, config: { damping: 14, stiffness: 100 } });

  const activeSteps = applicationSteps || steps || [];
  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  // Determine active step based on frame progression
  const activeStepIdx = Math.min(activeSteps.length - 1, Math.floor(frame / 60));

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
        actTitle="आवेदन प्रक्रिया (Step-by-Step)"
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
          gap: 24,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Header Title */}
        <div style={{ transform: `translateY(${(1 - entrance) * 20}px)`, opacity: entrance }}>
          <div style={{ fontSize: 15, fontWeight: 800, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 1 }}>
            आधिकारिक पोर्टल गाइड 2026
          </div>
          <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "4px 0 0 0" }}>
            घर बैठे आवेदन व सत्यापन का आसान तरीका
          </h2>
        </div>

        {/* 4-Step Flow Grid */}
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${activeSteps.length}, 1fr)`, gap: 20, position: "relative" }}>
          {activeSteps.map((st, idx) => {
            const stepDelay = 8 + idx * 16;
            const stepSpring = spring({ frame, fps, delay: stepDelay, config: { damping: 14 } });
            const isActive = idx === activeStepIdx;
            const isDone = idx < activeStepIdx;

            return (
              <div
                key={idx}
                style={{
                  background: isActive
                    ? "linear-gradient(145deg, rgba(30, 58, 138, 0.5) 0%, rgba(10, 18, 36, 0.95) 100%)"
                    : "rgba(10, 18, 36, 0.75)",
                  border: isActive
                    ? "2px solid rgba(59, 130, 246, 0.9)"
                    : "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: 20,
                  padding: "24px 22px",
                  boxShadow: isActive
                    ? "0 14px 40px rgba(0,0,0,0.7), 0 0 22px rgba(37, 99, 235, 0.3)"
                    : "0 8px 25px rgba(0,0,0,0.4)",
                  display: "flex",
                  flexDirection: "column",
                  gap: 12,
                  transform: `scale(${isActive ? 1.03 : 1.0}) translateY(${(1 - stepSpring) * 20}px)`,
                  opacity: stepSpring,
                  transition: "all 0.3s ease",
                }}
              >
                {/* Step Badge */}
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div
                    style={{
                      background: isActive ? "#2563eb" : isDone ? "#10b981" : "rgba(255, 255, 255, 0.1)",
                      borderRadius: 10,
                      padding: "4px 14px",
                      fontSize: 14,
                      fontWeight: 900,
                      color: "#ffffff",
                    }}
                  >
                    कदम {st.step}
                  </div>
                  {isActive && (
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#38bdf8", boxShadow: "0 0 8px #38bdf8" }} />
                  )}
                </div>

                <div style={{ fontSize: 21, fontWeight: 800, color: "#ffffff", lineHeight: 1.3 }}>
                  {st.title}
                </div>

                <div style={{ fontSize: 16, color: "#cbd5e1", lineHeight: 1.5 }}>
                  {st.desc}
                </div>
              </div>
            );
          })}
        </div>

        {/* Official Portal Direction Note */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(255, 255, 255, 0.1)",
            borderRadius: 16,
            padding: "16px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ fontSize: 22 }}>🔒</span>
            <div style={{ fontSize: 16, fontWeight: 700, color: "#e2e8f0" }}>
              आधिकारिक पोर्टल: <strong style={{ color: "#38bdf8" }}>{domain}</strong> पर ही सुरक्षित आवेदन करें।
            </div>
          </div>
          <div
            style={{
              background: "rgba(34, 197, 94, 0.15)",
              border: "1px solid rgba(34, 197, 94, 0.5)",
              borderRadius: 8,
              padding: "6px 14px",
              fontSize: 13,
              fontWeight: 800,
              color: "#4ade80",
            }}
          >
            फ्री ऑनलाइन प्रक्रिया
          </div>
        </div>
      </div>
    </div>
  );
};
