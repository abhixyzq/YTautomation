import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface FlowStep {
  step: number;
  label: string;
  detail?: string;
  status?: "normal" | "active" | "critical";
}

interface KineticFlowchartProps {
  title?: string;
  steps?: FlowStep[];
}

export const KineticFlowchart: React.FC<KineticFlowchartProps> = ({
  title = "THE CASCADING LOGIC CHAIN",
  steps = [
    { step: 1, label: "Input Assertion", detail: "Assumed safe 64-bit float", status: "normal" },
    { step: 2, label: "Type Cast Shortcut", detail: "Downcasted to 16-bit integer", status: "normal" },
    { step: 3, label: "Arithmetic Overflow", detail: "Value > 32,767 at t+36s", status: "active" },
    { step: 4, label: "Total Rocket Self-Destruct", detail: "Guidance computers shut down", status: "critical" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const pulse = 0.8 + Math.sin(frame / 8) * 0.2;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#060912",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "50px 80px",
        overflow: "hidden",
        fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
      }}
    >
      {/* Background Radial Glow */}
      <div
        style={{
          position: "absolute",
          width: "900px",
          height: "900px",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0, 240, 255, 0.08) 0%, transparent 65%)",
          pointerEvents: "none",
        }}
      />

      {/* Header */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          marginBottom: 60,
          transform: `scale(${titleSpring})`,
          opacity: titleSpring,
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            fontWeight: 800,
            color: "#00f0ff",
            letterSpacing: "2px",
            textTransform: "uppercase",
            marginBottom: 8,
            background: "rgba(0, 240, 255, 0.12)",
            padding: "4px 14px",
            borderRadius: "99px",
            border: "1px solid rgba(0, 240, 255, 0.3)",
          }}
        >
          LOGICAL ARCHITECTURE // STEP-BY-STEP BREAKDOWN
        </div>
        <div
          style={{
            fontSize: 38,
            fontWeight: 800,
            color: "#ffffff",
            letterSpacing: "-0.5px",
            textTransform: "uppercase",
            textAlign: "center",
            textShadow: "0 4px 20px rgba(0, 240, 255, 0.3)",
          }}
        >
          {title}
        </div>
      </div>

      {/* Horizontal Step Sequence */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          maxWidth: "1600px",
          position: "relative",
          zIndex: 2,
        }}
      >
        {steps.map((st, idx) => {
          const stepSpring = spring({
            frame: frame - idx * 6,
            fps,
            config: { damping: 14, stiffness: 90 },
          });

          const isCritical = st.status === "critical";
          const isActive = st.status === "active";

          let borderColor = "rgba(255, 255, 255, 0.12)";
          let accentColor = "#94a3b8";
          let bgCard = "rgba(13, 21, 38, 0.7)";

          if (isCritical) {
            borderColor = "#ef4444";
            accentColor = "#ef4444";
            bgCard = "rgba(239, 68, 68, 0.12)";
          } else if (isActive) {
            borderColor = "#00f0ff";
            accentColor = "#00f0ff";
            bgCard = "rgba(0, 240, 255, 0.12)";
          }

          return (
            <React.Fragment key={idx}>
              {/* Step Node Card */}
              <div
                style={{
                  flex: 1,
                  background: bgCard,
                  backdropFilter: "blur(20px)",
                  border: `2px solid ${borderColor}`,
                  borderRadius: "20px",
                  padding: "24px 20px",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  textAlign: "center",
                  position: "relative",
                  transform: `scale(${Math.max(0.01, stepSpring)})`,
                  opacity: Math.max(0, stepSpring),
                  boxShadow: isActive
                    ? `0 0 ${30 * pulse}px rgba(0, 240, 255, 0.35)`
                    : isCritical
                    ? `0 0 ${30 * pulse}px rgba(239, 68, 68, 0.35)`
                    : "0 10px 30px rgba(0, 0, 0, 0.5)",
                }}
              >
                {/* Step Badge */}
                <div
                  style={{
                    width: "36px",
                    height: "36px",
                    borderRadius: "50%",
                    backgroundColor: accentColor,
                    color: "#050811",
                    fontWeight: 800,
                    fontSize: 16,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    marginBottom: 14,
                    boxShadow: `0 0 14px ${accentColor}`,
                  }}
                >
                  {st.step}
                </div>

                {/* Node Label */}
                <div
                  style={{
                    fontSize: 18,
                    fontWeight: 800,
                    color: "#ffffff",
                    lineHeight: 1.3,
                    marginBottom: 8,
                  }}
                >
                  {st.label}
                </div>

                {/* Node Detail */}
                {st.detail && (
                  <div
                    style={{
                      fontSize: 12.5,
                      fontWeight: 600,
                      color: "#94a3b8",
                      fontFamily: "'JetBrains Mono', monospace",
                      lineHeight: 1.4,
                    }}
                  >
                    {st.detail}
                  </div>
                )}
              </div>

              {/* Connecting Vector Arrow (Between nodes) */}
              {idx < steps.length - 1 && (
                <div
                  style={{
                    width: "48px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    position: "relative",
                  }}
                >
                  <div
                    style={{
                      height: "2px",
                      width: "100%",
                      background: "linear-gradient(90deg, rgba(0,240,255,0.4), rgba(0,240,255,0.9))",
                      boxShadow: "0 0 8px rgba(0,240,255,0.6)",
                    }}
                  />
                  <div
                    style={{
                      position: "absolute",
                      right: 0,
                      width: 0,
                      height: 0,
                      borderTop: "6px solid transparent",
                      borderBottom: "6px solid transparent",
                      borderLeft: "8px solid #00f0ff",
                    }}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
