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

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.025], {
    extrapolateRight: "clamp",
  });

  const activeSteps = applicationSteps || steps || [
    { step: 1, title: "आधिकारिक पोर्टल खोलें", desc: "पोर्टल पर जाकर नया पंजीकरण या लॉगिन विकल्प चुनें।" },
    { step: 2, title: "आधार e-KYC सत्यापन", desc: "आधार नंबर और मोबाइल OTP द्वारा ऑनलाइन सत्यापन पूरा करें।" },
    { step: 3, title: "फॉर्म एवं दस्तावेज सबमिट", desc: "पात्रता विवरण दर्ज करें और आवश्यक कागजात अपलोड करें।" },
    { step: 4, title: "रसीद एवं स्टेटस चेक", desc: "सफलतापूर्वक सबमिट होने के बाद अपनी आवेदन रसीद सुरक्षित रख लें।" },
  ];

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  // Determine active step based on frame progression (cycle every 50 frames)
  const activeStepIdx = Math.min(activeSteps.length - 1, Math.floor(frame / 50));

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
      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="आवेदन प्रक्रिया (Step-by-Step Guide)"
        portalDomain={domain}
      />

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
          gap: 20,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Browser Top Navigation Frame */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.95)",
            border: "1px solid rgba(226, 232, 240, 0.9)",
            borderRadius: 18,
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 6px 20px rgba(15, 23, 42, 0.05)",
          }}
        >
          {/* Traffic Light Dots */}
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#ef4444" }} />
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#f59e0b" }} />
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#10b981" }} />
          </div>

          {/* URL Search Box */}
          <div
            style={{
              background: "rgba(241, 245, 249, 0.95)",
              border: "1px solid rgba(203, 213, 225, 0.8)",
              borderRadius: 10,
              padding: "6px 20px",
              display: "flex",
              alignItems: "center",
              gap: 8,
              minWidth: 420,
              justifyContent: "center",
            }}
          >
            <span style={{ fontSize: 13 }}>🔒</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: "#0369a1" }}>
              https://{domain}
            </span>
            <span style={{ fontSize: 11, fontWeight: 800, background: "#d1fae5", color: "#065f46", padding: "2px 6px", borderRadius: 4 }}>
              SECURE
            </span>
          </div>

          <div style={{ fontSize: 13, fontWeight: 800, color: "#64748b" }}>
            पोर्टल आवेदन चरण
          </div>
        </div>

        {/* 4 Sequential Step Progression Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
          {activeSteps.slice(0, 4).map((item, idx) => {
            const isCurrent = idx === activeStepIdx;
            const isCompleted = idx < activeStepIdx;
            const stepSpring = spring({ frame, fps, delay: 5 + idx * 8, config: { damping: 14, stiffness: 90 } });

            return (
              <div
                key={idx}
                style={{
                  background: isCurrent
                    ? "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(239, 246, 255, 0.95) 100%)"
                    : "rgba(255, 255, 255, 0.92)",
                  border: isCurrent
                    ? "2.5px solid #0284c7"
                    : isCompleted
                    ? "1.5px solid rgba(16, 185, 129, 0.5)"
                    : "1px solid rgba(226, 232, 240, 0.9)",
                  borderRadius: 22,
                  padding: "24px 20px",
                  boxShadow: isCurrent
                    ? "0 16px 40px rgba(2, 132, 199, 0.18), 0 0 20px rgba(2, 132, 199, 0.1)"
                    : "0 8px 24px rgba(15, 23, 42, 0.05)",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  minHeight: 250,
                  transform: `translateY(${(1 - stepSpring) * 20}px)`,
                  opacity: stepSpring,
                  transition: "all 0.3s ease",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* Step Number Badge */}
                <div>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
                    <div
                      style={{
                        width: 42,
                        height: 42,
                        borderRadius: 12,
                        background: isCurrent
                          ? "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)"
                          : isCompleted
                          ? "linear-gradient(135deg, #059669 0%, #10b981 100%)"
                          : "rgba(241, 245, 249, 0.9)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 18,
                        fontWeight: 900,
                        color: isCurrent || isCompleted ? "#ffffff" : "#64748b",
                        boxShadow: isCurrent ? "0 4px 12px rgba(2, 132, 199, 0.35)" : "none",
                      }}
                    >
                      {isCompleted ? "✓" : idx + 1}
                    </div>

                    {isCurrent ? (
                      <span
                        style={{
                          background: "#e0f2fe",
                          color: "#0369a1",
                          fontSize: 11,
                          fontWeight: 800,
                          padding: "3px 10px",
                          borderRadius: 6,
                          textTransform: "uppercase",
                          letterSpacing: 0.5,
                        }}
                      >
                        सक्रिय चरण
                      </span>
                    ) : isCompleted ? (
                      <span
                        style={{
                          background: "#d1fae5",
                          color: "#047857",
                          fontSize: 11,
                          fontWeight: 800,
                          padding: "3px 8px",
                          borderRadius: 6,
                        }}
                      >
                        पूर्ण
                      </span>
                    ) : null}
                  </div>

                  {/* Step Title */}
                  <div style={{ fontSize: 20, fontWeight: 800, color: "#0f172a", lineHeight: 1.35 }}>
                    {item.title}
                  </div>

                  {/* Step Description */}
                  <div style={{ fontSize: 15, fontWeight: 600, color: "#475569", lineHeight: 1.5, marginTop: 10 }}>
                    {item.desc}
                  </div>
                </div>

                {/* Bottom Step Indicator Bar */}
                <div
                  style={{
                    height: 4,
                    borderRadius: 2,
                    background: isCurrent ? "#0284c7" : isCompleted ? "#10b981" : "rgba(226, 232, 240, 0.8)",
                    marginTop: 16,
                  }}
                />
              </div>
            );
          })}
        </div>

        {/* Bottom Safety Reminder Pill */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.95)",
            border: "1px solid rgba(226, 232, 240, 0.9)",
            borderRadius: 14,
            padding: "12px 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 6px 18px rgba(15, 23, 42, 0.04)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 16 }}>💡</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: "#1e293b" }}>
              ऑनलाइन फॉर्म सबमिट करने के बाद अपना एप्लीकेशन आईडी व पावती रसीद (Acknowledgement Receipt) सुरक्षित डाउनलोड करें।
            </span>
          </div>
          <span style={{ fontSize: 12, fontWeight: 800, color: "#059669" }}>
            ✓ 100% ऑनलाइन प्रक्रिया
          </span>
        </div>
      </div>
    </div>
  );
};
