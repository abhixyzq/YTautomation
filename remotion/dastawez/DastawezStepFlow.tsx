import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";

interface StepItem {
  step: number;
  title: string;
  desc: string;
}

interface Props {
  schemeName: string;
  ministry?: string;
  steps?: StepItem[];
  portalUrl?: string;
  category?: string;
}

export const DastawezStepFlow: React.FC<Props> = ({
  schemeName,
  ministry,
  steps = [],
  portalUrl,
  category,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 20%, #0c2038 0%, #06101c 60%, #01060b 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      <DastawezHeader ministry={ministry} category={category} schemeName={schemeName} />

      <div
        style={{
          position: "absolute",
          top: 140,
          bottom: 40,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          gap: 24,
        }}
      >
        {/* Title */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <span style={{ fontSize: 16, fontWeight: 700, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 1.5 }}>
              ऑनलाइन आवेदन प्रक्रिया (Step-by-Step Guide)
            </span>
            <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "6px 0 0 0" }}>
              घर बैठे मोबाइल से कैसे करें आवेदन या e-KYC?
            </h2>
          </div>
          {portalUrl && (
            <div
              style={{
                padding: "10px 24px",
                background: "rgba(56, 189, 248, 0.15)",
                borderRadius: 30,
                border: "1px solid rgba(56, 189, 248, 0.35)",
                fontSize: 16,
                fontWeight: 700,
                color: "#38bdf8",
              }}
            >
              🌐 {portalUrl}
            </div>
          )}
        </div>

        {/* 4-Step Horizontal Pipeline */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: 20,
            flex: 1,
            alignItems: "stretch",
          }}
        >
          {steps.map((s, idx) => {
            const stepSpring = spring({ frame, fps, delay: 8 + idx * 8, config: { damping: 14 } });
            return (
              <div
                key={idx}
                style={{
                  background: "rgba(15, 23, 42, 0.8)",
                  backdropFilter: "blur(16px)",
                  border: "1px solid rgba(255, 255, 255, 0.14)",
                  borderRadius: 22,
                  padding: "28px 24px",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  boxShadow: "0 15px 35px rgba(0, 0, 0, 0.35)",
                  transform: `translateY(${(1 - stepSpring) * 30}px)`,
                  opacity: stepSpring,
                  position: "relative",
                }}
              >
                {/* Step Pill */}
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div
                    style={{
                      background: "linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)",
                      color: "#ffffff",
                      fontWeight: 900,
                      fontSize: 16,
                      padding: "6px 16px",
                      borderRadius: 20,
                      boxShadow: "0 4px 12px rgba(14, 165, 233, 0.4)",
                    }}
                  >
                    STEP 0{s.step}
                  </div>
                  <span style={{ fontSize: 22, opacity: 0.7 }}>➔</span>
                </div>

                {/* Step Title & Desc */}
                <div style={{ marginTop: 20, flex: 1 }}>
                  <h3
                    style={{
                      fontSize: 24,
                      fontWeight: 800,
                      color: "#ffffff",
                      margin: "0 0 12px 0",
                      lineHeight: 1.3,
                    }}
                  >
                    {s.title}
                  </h3>
                  <p
                    style={{
                      fontSize: 17,
                      fontWeight: 500,
                      color: "#cbd5e1",
                      lineHeight: 1.5,
                      margin: 0,
                    }}
                  >
                    {s.desc}
                  </p>
                </div>

                {/* Status Indicator */}
                <div
                  style={{
                    marginTop: 20,
                    paddingTop: 16,
                    borderTop: "1px solid rgba(255, 255, 255, 0.1)",
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    fontSize: 14,
                    color: "#38bdf8",
                    fontWeight: 600,
                  }}
                >
                  <span>✓ निःशुल्क एवं सुरक्षित</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
