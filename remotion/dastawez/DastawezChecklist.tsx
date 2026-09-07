import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface DastawezChecklistProps {
  schemeName: string;
  ministry?: string;
  documents?: string[];
  bankNote?: string;
  category?: string;
  evidence?: EvidenceMetadata;
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
  currentActIndex = 3,
  totalActs = 6,
  portalUrl,
  officialPortalDomain,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.025], {
    extrapolateRight: "clamp",
  });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const docList = documents.length > 0 ? documents : [
    "मूल आधार कार्ड (चालू मोबाइल नंबर से लिंक)",
    "सक्रिय बैंक खाता पासबुक (आधार-डीबीटी लिंक)",
    "आय एवं निवास प्रमाण पत्र (यदि लागू हो)",
    "पासपोर्ट साइज ताज़ा फोटो व हस्ताक्षर",
  ];

  // Progressive document spotlight: cycle every 55 frames
  const activeDocIdx = Math.min(docList.length - 1, Math.floor(frame / 55));

  const docIcons = ["🪪", "🏦", "📄", "📸", "📝"];

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
        actTitle="ज़रूरी दस्तावेज़ चेकलिस्ट (Required Documents)"
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
        {/* Section Heading Pill */}
        <div style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
          <span
            style={{
              background: "rgba(2, 132, 199, 0.1)",
              border: "1px solid rgba(2, 132, 199, 0.35)",
              color: "#0369a1",
              fontSize: 14,
              fontWeight: 800,
              padding: "6px 18px",
              borderRadius: 100,
              textTransform: "uppercase",
              letterSpacing: 0.6,
            }}
          >
            📂 दस्तावेज़ सत्यापन सूची 2026
          </span>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a" }}>
            आवेदन करने से पहले ये कागजात तैयार रखें
          </span>
        </div>

        {/* 2x2 Grid of Document Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
          {docList.slice(0, 4).map((doc, idx) => {
            const isActive = idx === activeDocIdx;
            const docSpring = spring({ frame, fps, delay: 5 + idx * 8, config: { damping: 14, stiffness: 90 } });

            return (
              <div
                key={idx}
                style={{
                  background: isActive
                    ? "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(239, 246, 255, 0.95) 100%)"
                    : "rgba(255, 255, 255, 0.92)",
                  border: isActive
                    ? "2px solid #0284c7"
                    : "1px solid rgba(226, 232, 240, 0.9)",
                  borderRadius: 20,
                  padding: "20px 24px",
                  boxShadow: isActive
                    ? "0 14px 35px rgba(2, 132, 199, 0.18), 0 0 15px rgba(2, 132, 199, 0.1)"
                    : "0 8px 24px rgba(15, 23, 42, 0.05)",
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  transform: `translateY(${(1 - docSpring) * 20}px)`,
                  opacity: docSpring,
                  transition: "all 0.3s ease",
                }}
              >
                {/* Icon Container */}
                <div
                  style={{
                    width: 52,
                    height: 52,
                    borderRadius: 14,
                    background: isActive
                      ? "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)"
                      : "rgba(241, 245, 249, 0.9)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 24,
                    color: isActive ? "#ffffff" : "#475569",
                    boxShadow: isActive ? "0 4px 14px rgba(2, 132, 199, 0.35)" : "none",
                    flexShrink: 0,
                  }}
                >
                  {docIcons[idx % docIcons.length]}
                </div>

                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                    <span style={{ fontSize: 12, fontWeight: 800, color: isActive ? "#0284c7" : "#64748b", textTransform: "uppercase" }}>
                      कागजात #{idx + 1}
                    </span>
                    {isActive && (
                      <span
                        style={{
                          background: "#dbeafe",
                          color: "#1e40af",
                          fontSize: 10,
                          fontWeight: 800,
                          padding: "2px 8px",
                          borderRadius: 4,
                        }}
                      >
                        अनिवार्य
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#0f172a", lineHeight: 1.35 }}>
                    {doc}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom Direct Benefit Transfer (DBT) Note Banner */}
        <div
          style={{
            background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.94) 100%)",
            border: "1.5px solid rgba(16, 185, 129, 0.45)",
            borderRadius: 16,
            padding: "14px 22px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 10px 25px rgba(16, 185, 129, 0.08)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 22 }}>⚡</span>
            <div>
              <span style={{ fontSize: 13, fontWeight: 800, color: "#065f46", textTransform: "uppercase", letterSpacing: 0.6 }}>
                महत्वपूर्ण बैंकिंग निर्देश:
              </span>
              <span style={{ fontSize: 15, fontWeight: 700, color: "#047857", marginLeft: 8 }}>
                {bankNote || "आधार-डीबीटी सक्रिय बैंक खाता अनिवार्य है, ताकि सरकारी सहायता बिना किसी रुकावट सीधे पहुंचे।"}
              </span>
            </div>
          </div>
          <span
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
          </span>
        </div>
      </div>
    </div>
  );
};
