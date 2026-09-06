import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";

interface Props {
  schemeName: string;
  ministry?: string;
  eligibilityYes?: string[];
  eligibilityNo?: string[];
  category?: string;
}

export const DastawezEligibility: React.FC<Props> = ({
  schemeName,
  ministry,
  eligibilityYes = [],
  eligibilityNo = [],
  category,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cardSpring = spring({ frame, fps, delay: 5, config: { damping: 14 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 20%, #0a1e36 0%, #06101e 60%, #02070f 100%)",
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
          gap: 20,
        }}
      >
        {/* Act Title */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <span style={{ fontSize: 16, fontWeight: 700, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 1.5 }}>
              पात्रता मानदंड (Eligibility Check)
            </span>
            <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "6px 0 0 0" }}>
              किसे मिलेगा लाभ और कौन है अपात्र?
            </h2>
          </div>
          <div
            style={{
              padding: "10px 24px",
              background: "rgba(255, 255, 255, 0.08)",
              borderRadius: 30,
              border: "1px solid rgba(255, 255, 255, 0.15)",
              fontSize: 16,
              fontWeight: 600,
              color: "#e2e8f0",
            }}
          >
            📋 आवेदन करने से पहले शर्तें अवश्य जांचें
          </div>
        </div>

        {/* 2-Column Side-by-Side Comparison */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 32, flex: 1 }}>
          {/* YES: Eligible Column */}
          <div
            style={{
              background: "linear-gradient(180deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 78, 59, 0.2) 100%)",
              border: "2px solid rgba(52, 211, 153, 0.4)",
              borderRadius: 24,
              padding: "28px 32px",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              boxShadow: "0 15px 35px rgba(0, 0, 0, 0.3)",
              transform: `translateY(${(1 - cardSpring) * 30}px)`,
              opacity: cardSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12, borderBottom: "1px solid rgba(52, 211, 153, 0.25)", paddingBottom: 14 }}>
              <div
                style={{
                  width: 38,
                  height: 38,
                  borderRadius: "50%",
                  background: "#10b981",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 22,
                  color: "#ffffff",
                  fontWeight: 900,
                }}
              >
                ✓
              </div>
              <h3 style={{ fontSize: 26, fontWeight: 800, color: "#6ee7b7", margin: 0 }}>
                ये लोग हैं पात्र (Eligible)
              </h3>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 14, marginTop: 6 }}>
              {eligibilityYes.map((item, idx) => {
                const itemSpring = spring({ frame, fps, delay: 10 + idx * 6, config: { damping: 15 } });
                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 14,
                      background: "rgba(16, 185, 129, 0.08)",
                      padding: "14px 18px",
                      borderRadius: 14,
                      border: "1px solid rgba(16, 185, 129, 0.2)",
                      transform: `translateX(${(1 - itemSpring) * -20}px)`,
                      opacity: itemSpring,
                    }}
                  >
                    <span style={{ color: "#34d399", fontSize: 20, fontWeight: 900, marginTop: 1 }}>✔</span>
                    <span style={{ fontSize: 20, fontWeight: 600, color: "#f1f5f9", lineHeight: 1.4 }}>
                      {item}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* NO: Disqualified Column */}
          <div
            style={{
              background: "linear-gradient(180deg, rgba(239, 68, 68, 0.1) 0%, rgba(127, 29, 29, 0.2) 100%)",
              border: "2px solid rgba(248, 113, 113, 0.35)",
              borderRadius: 24,
              padding: "28px 32px",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              boxShadow: "0 15px 35px rgba(0, 0, 0, 0.3)",
              transform: `translateY(${(1 - cardSpring) * 30}px)`,
              opacity: cardSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12, borderBottom: "1px solid rgba(248, 113, 113, 0.25)", paddingBottom: 14 }}>
              <div
                style={{
                  width: 38,
                  height: 38,
                  borderRadius: "50%",
                  background: "#ef4444",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 22,
                  color: "#ffffff",
                  fontWeight: 900,
                }}
              >
                ✕
              </div>
              <h3 style={{ fontSize: 26, fontWeight: 800, color: "#fca5a5", margin: 0 }}>
                ये लोग आवेदन न करें (Ineligible)
              </h3>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 14, marginTop: 6 }}>
              {eligibilityNo.map((item, idx) => {
                const itemSpring = spring({ frame, fps, delay: 15 + idx * 6, config: { damping: 15 } });
                return (
                  <div
                    key={idx}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: 14,
                      background: "rgba(239, 68, 68, 0.08)",
                      padding: "14px 18px",
                      borderRadius: 14,
                      border: "1px solid rgba(239, 68, 68, 0.2)",
                      transform: `translateX(${(1 - itemSpring) * 20}px)`,
                      opacity: itemSpring,
                    }}
                  >
                    <span style={{ color: "#f87171", fontSize: 20, fontWeight: 900, marginTop: 1 }}>✖</span>
                    <span style={{ fontSize: 20, fontWeight: 600, color: "#f1f5f9", lineHeight: 1.4 }}>
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
