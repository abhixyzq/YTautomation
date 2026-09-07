import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

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

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.02], {
    extrapolateRight: "clamp",
  });

  const beat1Spring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 110 } });
  const beat2Spring = spring({ frame, fps, delay: 14, config: { damping: 14, stiffness: 95 } });
  const beat3Spring = spring({ frame, fps, delay: 28, config: { damping: 14, stiffness: 95 } });

  const activeSteps = applicationSteps || steps || [
    { step: 1, title: "आधिकारिक पोर्टल खोलें", desc: "पोर्टल पर जाकर नया पंजीकरण या लॉगिन विकल्प चुनें।" },
    { step: 2, title: "आधार e-KYC सत्यापन", desc: "आधार नंबर और मोबाइल OTP द्वारा ऑनलाइन सत्यापन पूरा करें।" },
    { step: 3, title: "फॉर्म एवं दस्तावेज सबमिट", desc: "पात्रता विवरण दर्ज करें और आवश्यक कागजात अपलोड करें।" },
    { step: 4, title: "रसीद एवं स्टेटस चेक", desc: "सफलतापूर्वक सबमिट होने के बाद अपनी आवेदन रसीद सुरक्षित रख लें।" },
  ];

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  // Determine active step based on frame progression
  const activeStepIdx = Math.min(activeSteps.length - 1, Math.floor(frame / 50));

  const imgPath = visualMedia?.official_image_path || officialImagePath;
  const imgTitle = visualMedia?.official_image_title || officialImageTitle;
  const vidPath = visualMedia?.broll_video_path || brollVideoPath;
  const mediaAttr = visualMedia?.attribution || attribution;

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Full-Screen Container */}
      <div
        style={{
          position: "absolute",
          top: 36,
          bottom: 104,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Sleek Integrated Top Meta-Bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateY(${(1 - beat1Spring) * -14}px)`,
            opacity: beat1Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                background: "rgba(255, 255, 255, 0.94)",
                padding: "6px 14px",
                borderRadius: 12,
                border: "1px solid rgba(2, 132, 199, 0.25)",
                boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
              }}
            >
              <div
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: 6,
                  background: "linear-gradient(135deg, #ea580c, #f97316)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#fff",
                  fontWeight: 900,
                  fontSize: 13,
                }}
              >
                द
              </div>
              <span style={{ fontSize: 15, fontWeight: 900, color: "#0f172a" }}>@iDastawez</span>
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                background: "rgba(238, 242, 255, 0.95)",
                border: "1px solid rgba(99, 102, 241, 0.3)",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
                color: "#3730a3",
              }}
            >
              <span>🏛️</span>
              <span>{domain}</span>
            </div>

            <div
              style={{
                background: "rgba(2, 132, 199, 0.12)",
                border: "1px solid rgba(2, 132, 199, 0.3)",
                color: "#0369a1",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
              }}
            >
              💻 ऑनलाइन आवेदन चरण 2026
            </div>
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(255, 255, 255, 0.94)",
              padding: "6px 16px",
              borderRadius: 12,
              border: "1px solid rgba(2, 132, 199, 0.2)",
              boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
            }}
          >
            <span style={{ fontSize: 13, fontWeight: 900, color: "#0284c7" }}>
              भाग {currentActIndex}/{totalActs}
            </span>
            <span style={{ fontSize: 12, color: "#94a3b8" }}>•</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#334155" }}>
              आवेदन प्रक्रिया (Step-by-Step Flow)
            </span>
          </div>
        </div>

        {/* Browser Mockup Header Bar */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.95)",
            border: "1px solid rgba(203, 213, 225, 0.8)",
            borderRadius: 16,
            padding: "10px 20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 6px 20px rgba(15, 23, 42, 0.04)",
            marginTop: 8,
            marginBottom: 8,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#ef4444" }} />
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#f59e0b" }} />
            <div style={{ width: 12, height: 12, borderRadius: "50%", background: "#10b981" }} />
          </div>

          <div
            style={{
              background: "rgba(241, 245, 249, 0.95)",
              border: "1px solid rgba(203, 213, 225, 0.7)",
              borderRadius: 10,
              padding: "5px 18px",
              display: "flex",
              alignItems: "center",
              gap: 8,
              minWidth: 420,
              justifyContent: "center",
            }}
          >
            <span style={{ fontSize: 13 }}>🔒</span>
            <span style={{ fontSize: 13, fontWeight: 800, color: "#0369a1" }}>
              https://{domain}
            </span>
            <span style={{ fontSize: 10, fontWeight: 900, background: "#d1fae5", color: "#065f46", padding: "1px 6px", borderRadius: 4 }}>
              SECURE
            </span>
          </div>

          <div style={{ fontSize: 12, fontWeight: 800, color: "#64748b" }}>
            100% ऑनलाइन नागरिक पोर्टल
          </div>
        </div>

        {/* Grid: 4 Step Cards across Left/Center + Dedicated Visual Media Card on Right */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.9fr 0.9fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Left Column: 4 Progressive Step Cards */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
            {activeSteps.slice(0, 4).map((item, idx) => {
              const isCurrent = idx === activeStepIdx;
              const isCompleted = idx < activeStepIdx;

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
                      : "1.5px solid rgba(226, 232, 240, 0.9)",
                    borderRadius: 20,
                    padding: "20px 20px",
                    boxShadow: isCurrent
                      ? "0 16px 36px rgba(2, 132, 199, 0.16), 0 0 16px rgba(2, 132, 199, 0.1)"
                      : "0 8px 24px rgba(15, 23, 42, 0.05)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    transition: "all 0.3s ease",
                  }}
                >
                  <div>
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
                      <div
                        style={{
                          width: 38,
                          height: 38,
                          borderRadius: 10,
                          background: isCurrent
                            ? "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)"
                            : isCompleted
                            ? "linear-gradient(135deg, #059669 0%, #10b981 100%)"
                            : "rgba(241, 245, 249, 0.9)",
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          fontSize: 16,
                          fontWeight: 900,
                          color: isCurrent || isCompleted ? "#ffffff" : "#64748b",
                          boxShadow: isCurrent ? "0 4px 12px rgba(2, 132, 199, 0.3)" : "none",
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

                    <div style={{ fontSize: 20, fontWeight: 800, color: "#0f172a", lineHeight: 1.35 }}>
                      {item.title}
                    </div>

                    <div style={{ fontSize: 15, fontWeight: 600, color: "#475569", lineHeight: 1.45, marginTop: 8 }}>
                      {item.desc}
                    </div>
                  </div>

                  <div
                    style={{
                      height: 4,
                      borderRadius: 2,
                      background: isCurrent ? "#0284c7" : isCompleted ? "#10b981" : "rgba(226, 232, 240, 0.8)",
                      marginTop: 12,
                    }}
                  />
                </div>
              );
            })}
          </div>

          {/* Right Column: Dedicated Visual Media Card (Portal Walkthrough Video or Document Photo) */}
          <DastawezMediaCard
            imagePath={imgPath}
            videoPath={vidPath}
            title={imgTitle || "डिजिटल आवेदन एवं पोर्टल प्रक्रिया"}
            attribution={mediaAttr || "Wikimedia / Govt Source"}
            badgeLabel="🎥 पोर्टल लाइव प्रोसेस"
            mediaType="video"
            style={{
              height: "100%",
            }}
            fallbackIcon="💻"
            fallbackTitle="आधिकारिक डिजिटल सेवा पोर्टल"
          />
        </div>

        {/* Bottom Directive Bar */}
        <div
          style={{
            marginTop: 14,
            background: "rgba(255, 255, 255, 0.94)",
            backdropFilter: "blur(16px)",
            border: "1.5px solid rgba(2, 132, 199, 0.25)",
            borderRadius: 16,
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 8px 24px rgba(15, 23, 42, 0.05)",
            transform: `translateY(${(1 - beat3Spring) * 10}px)`,
            opacity: beat3Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 18 }}>💡</span>
            <span style={{ fontSize: 15, fontWeight: 800, color: "#0f172a" }}>
              ऑनलाइन फॉर्म सबमिट करने के बाद अपना एप्लीकेशन आईडी व पावती रसीद (Acknowledgement Receipt) सुरक्षित डाउनलोड करें।
            </span>
          </div>

          <div
            style={{
              background: "#eff6ff",
              border: "1px solid #bfdbfe",
              padding: "4px 12px",
              borderRadius: 8,
              fontSize: 12,
              fontWeight: 800,
              color: "#1d4ed8",
            }}
          >
            ✓ 100% ऑनलाइन प्रक्रिया
          </div>
        </div>
      </div>
    </div>
  );
};
