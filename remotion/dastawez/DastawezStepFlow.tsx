import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";

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
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
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
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 5,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const bottomSpring = spring({ frame, fps, delay: 18, config: { damping: 12, stiffness: 100 } });

  const defaultSteps: StepItem[] = [
    { step: 1, title: "आधिकारिक पोर्टल खोलें", desc: `${domain} पर जाकर रजिस्ट्रेशन विकल्प चुनें` },
    { step: 2, title: "e-KYC व फॉर्म भरें", desc: "आधार OTP और ज़रूरी दस्तावेज़ विवरण सबमिट करें" },
    { step: 3, title: "पावती रसीद प्राप्त करें", desc: "आवेदन रसीद डाउनलोड कर स्टेटस ट्रैक करें" },
  ];

  const rawSteps = applicationSteps || steps || defaultSteps;
  const flowSteps = rawSteps.slice(0, 3);

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
          urgencyBadge="ऑनलाइन आवेदन प्रक्रिया"
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="आवेदन कैसे करें?"
        />
      </div>

      {/* 2. Floating 3-Step Process Ribbon */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 28,
          flex: 1,
          marginTop: 30,
          marginBottom: 30,
          alignItems: "center",
        }}
      >
        {flowSteps.map((s, idx) => {
          const stepSpring = spring({
            frame,
            fps,
            delay: 6 + idx * 5,
            config: { damping: 12, stiffness: 110 },
          });

          return (
            <div
              key={idx}
              style={{
                transform: `translateY(${(1 - stepSpring) * 35}px) scale(${stepSpring})`,
                opacity: stepSpring,
                background: "rgba(11, 17, 32, 0.88)",
                backdropFilter: "blur(24px)",
                WebkitBackdropFilter: "blur(24px)",
                border: "2px solid rgba(56, 189, 248, 0.4)",
                borderRadius: 24,
                padding: "32px 28px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                height: 260,
                boxShadow: "0 20px 50px rgba(0, 0, 0, 0.65), 0 0 20px rgba(56, 189, 248, 0.15)",
                boxSizing: "border-box",
              }}
            >
              <div>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
                  <span
                    style={{
                      background: "linear-gradient(135deg, #0284c7, #2563eb)",
                      color: "#ffffff",
                      fontSize: 14,
                      fontWeight: 900,
                      padding: "6px 14px",
                      borderRadius: 10,
                      letterSpacing: 0.8,
                    }}
                  >
                    चरण {idx + 1}
                  </span>
                  <span style={{ fontSize: 24 }}>{idx === 0 ? "🌐" : idx === 1 ? "📝" : "📄"}</span>
                </div>

                <div style={{ fontSize: 24, fontWeight: 900, color: "#f8fafc", lineHeight: 1.25, marginBottom: 10 }}>
                  {s.title}
                </div>

                <div style={{ fontSize: 16, fontWeight: 600, color: "#94a3b8", lineHeight: 1.45 }}>
                  {s.desc}
                </div>
              </div>

              <div
                style={{
                  fontSize: 12,
                  color: "#38bdf8",
                  fontWeight: 800,
                  borderTop: "1px solid rgba(255, 255, 255, 0.1)",
                  paddingTop: 10,
                }}
              >
                ✔ आधिकारिक पोर्टल पर उपलब्ध
              </div>
            </div>
          );
        })}
      </div>

      {/* 3. Floating Official Portal Link Ribbon */}
      <div
        style={{
          transform: `translateY(${(1 - bottomSpring) * 20}px)`,
          opacity: bottomSpring,
          background: "rgba(15, 23, 42, 0.92)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1.5px solid rgba(99, 102, 241, 0.5)",
          borderRadius: 20,
          padding: "16px 36px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: "0 14px 40px rgba(0, 0, 0, 0.55)",
          marginBottom: 50,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <span style={{ fontSize: 22 }}>👉</span>
          <div>
            <div style={{ fontSize: 12, fontWeight: 800, color: "#a5b4fc", textTransform: "uppercase" }}>
              आधिकारिक पोर्टल वेबसाइट (OFFICIAL PORTAL)
            </div>
            <div style={{ fontSize: 22, fontWeight: 900, color: "#38bdf8" }}>
              https://{domain}
            </div>
          </div>
        </div>

        <div
          style={{
            background: "rgba(16, 185, 129, 0.2)",
            border: "1px solid rgba(16, 185, 129, 0.6)",
            color: "#6ee7b7",
            padding: "8px 20px",
            borderRadius: 14,
            fontSize: 14,
            fontWeight: 800,
          }}
        >
          ✅ 100% निःशुल्क ऑनलाइन आवेदन
        </div>
      </div>
    </div>
  );
};
