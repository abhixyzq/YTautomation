import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

interface DastawezChecklistProps {
  schemeName: string;
  ministry?: string;
  documents?: string[];
  bankNote?: string;
  category?: string;
  evidence?: EvidenceMetadata;
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
  currentActIndex?: number;
  totalActs?: number;
  portalUrl?: string;
  officialPortalDomain?: string;
}

export const DastawezChecklist: React.FC<DastawezChecklistProps> = ({
  schemeName,
  ministry,
  documents = [],
  bankNote,
  category,
  evidence,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 4,
  totalActs = 6,
  portalUrl,
  officialPortalDomain,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.02], {
    extrapolateRight: "clamp",
  });

  const beat1Spring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 110 } });
  const beat2Spring = spring({ frame, fps, delay: 14, config: { damping: 14, stiffness: 95 } });
  const beat3Spring = spring({ frame, fps, delay: 28, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const docList =
    documents.length > 0
      ? documents
      : [
          "मूल आधार कार्ड (चालू मोबाइल नंबर से लिंक)",
          "सक्रिय बैंक खाता पासबुक (आधार-डीबीटी लिंक)",
          "आय, जाति एवं निवास प्रमाण पत्र (यदि लागू हो)",
          "राशन कार्ड / वर्तमान लाभार्थी पहचान पत्र",
        ];

  // Highlight active doc progressively
  const activeDocIdx = Math.min(docList.length - 1, Math.floor(frame / 60));
  const docIcons = ["🪪", "🏦", "📄", "📜"];

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
              📂 दस्तावेज़ सत्यापन सूची 2026
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
              ज़रूरी दस्तावेज़ चेकलिस्ट
            </span>
          </div>
        </div>

        {/* Section Headline */}
        <div
          style={{
            marginTop: 10,
            marginBottom: 10,
            transform: `translateY(${(1 - beat1Spring) * 12}px)`,
            opacity: beat1Spring,
          }}
        >
          <h1
            style={{
              fontSize: 38,
              fontWeight: 900,
              lineHeight: 1.25,
              color: "#0f172a",
              margin: 0,
              letterSpacing: "-0.5px",
            }}
          >
            आवेदन व सत्यापन करने से पहले ये कागजात तैयार रखें
          </h1>
        </div>

        {/* Multi-Card Grid: 4 Docs Grid on Left + Rules & Visual Media on Right */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.65fr 1fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Left Column: 4 Document Cards in 2x2 Grid */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            {docList.slice(0, 4).map((doc, idx) => {
              const isActive = idx === activeDocIdx;

              return (
                <div
                  key={idx}
                  style={{
                    background: isActive
                      ? "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(239, 246, 255, 0.95) 100%)"
                      : "rgba(255, 255, 255, 0.92)",
                    border: isActive
                      ? "2.5px solid #0284c7"
                      : "1.5px solid rgba(226, 232, 240, 0.9)",
                    borderRadius: 20,
                    padding: "20px 22px",
                    boxShadow: isActive
                      ? "0 14px 35px rgba(2, 132, 199, 0.16), 0 0 16px rgba(2, 132, 199, 0.1)"
                      : "0 8px 24px rgba(15, 23, 42, 0.05)",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-between",
                    transition: "all 0.3s ease",
                  }}
                >
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <div
                      style={{
                        width: 44,
                        height: 44,
                        borderRadius: 12,
                        background: isActive
                          ? "linear-gradient(135deg, #1d4ed8, #0284c7)"
                          : "rgba(241, 245, 249, 0.9)",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 22,
                        color: isActive ? "#ffffff" : "#475569",
                        boxShadow: isActive ? "0 4px 12px rgba(2, 132, 199, 0.3)" : "none",
                      }}
                    >
                      {docIcons[idx % docIcons.length]}
                    </div>
                    <span
                      style={{
                        background: isActive ? "#dbeafe" : "#f1f5f9",
                        color: isActive ? "#1e40af" : "#64748b",
                        fontSize: 11,
                        fontWeight: 800,
                        padding: "3px 10px",
                        borderRadius: 6,
                        textTransform: "uppercase",
                      }}
                    >
                      दस्तावेज़ #{idx + 1}
                    </span>
                  </div>

                  <div style={{ fontSize: 21, fontWeight: 800, color: "#0f172a", lineHeight: 1.35, marginTop: 12 }}>
                    {doc}
                  </div>

                  <div
                    style={{
                      marginTop: 10,
                      fontSize: 12,
                      fontWeight: 700,
                      color: isActive ? "#0284c7" : "#64748b",
                      display: "flex",
                      alignItems: "center",
                      gap: 6,
                    }}
                  >
                    <span>✓</span>
                    <span>ओरिजिनल व स्व-हस्ताक्षरित प्रति अनिवार्य</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right Column: Guidelines Card + Dedicated Visual Media Card */}
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {/* Rules & Attestation Card */}
            <div
              style={{
                background: "rgba(255, 255, 255, 0.94)",
                border: "1.5px solid rgba(2, 132, 199, 0.25)",
                borderRadius: 20,
                padding: "16px 20px",
                boxShadow: "0 10px 24px rgba(15, 23, 42, 0.05)",
                display: "flex",
                flexDirection: "column",
                gap: 8,
              }}
            >
              <div style={{ fontSize: 12, fontWeight: 900, color: "#0284c7", textTransform: "uppercase" }}>
                📑 दस्तावेज़ अपलोड नियम (Upload Guidelines)
              </div>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#1e293b", lineHeight: 1.4 }}>
                • सभी स्कैन प्रतियां स्पष्ट और पठनीय (Clear PDF/JPEG) होनी चाहिए।<br />
                • आधार से लिंक मोबाइल पर OTP सत्यापन सुनिश्चित करें।
              </div>
            </div>

            {/* Dedicated Visual Media Card */}
            <DastawezMediaCard
              imagePath={imgPath}
              videoPath={vidPath}
              title={imgTitle || "आधिकारिक दस्तावेज़ सत्यापन केंद्र"}
              attribution={mediaAttr || "Wikimedia / Govt Source"}
              badgeLabel="📑 दस्तावेज़ सत्यापन दृश्य"
              mediaType="image"
              style={{
                flex: 1,
              }}
              fallbackIcon="📂"
              fallbackTitle="सरकारी दस्तावेज़ सत्यापन अभिलेख"
            />
          </div>
        </div>

        {/* Bottom Direct Benefit Transfer (DBT) Note Banner */}
        <div
          style={{
            marginTop: 14,
            background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.94) 100%)",
            border: "1.5px solid rgba(16, 185, 129, 0.45)",
            borderRadius: 16,
            padding: "14px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 8px 24px rgba(16, 185, 129, 0.08)",
            transform: `translateY(${(1 - beat3Spring) * 10}px)`,
            opacity: beat3Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 22 }}>⚡</span>
            <div>
              <span style={{ fontSize: 13, fontWeight: 800, color: "#065f46", textTransform: "uppercase" }}>
                महत्वपूर्ण बैंकिंग निर्देश:
              </span>
              <span style={{ fontSize: 15, fontWeight: 700, color: "#047857", marginLeft: 8 }}>
                {bankNote || "आधार-डीबीटी सक्रिय बैंक खाता अनिवार्य है, ताकि सरकारी सहायता बिना किसी रुकावट सीधे पहुंचे।"}
              </span>
            </div>
          </div>

          <div
            style={{
              background: "#d1fae5",
              color: "#047857",
              fontSize: 12,
              fontWeight: 800,
              padding: "4px 12px",
              borderRadius: 6,
            }}
          >
            100% DBT लिंक
          </div>
        </div>
      </div>
    </div>
  );
};
