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

  const leftCardSpring = spring({ frame, fps, delay: 5, config: { damping: 14, stiffness: 90 } });
  const rightCardSpring = spring({ frame, fps, delay: 25, config: { damping: 14, stiffness: 90 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const yesList = eligibilityYes.length > 0 ? eligibilityYes : ["सभी पात्र भारतीय नागरिक", "निर्धारित नियमों के तहत पंजीकृत परिवार"];
  const noList = eligibilityNo.length > 0 ? eligibilityNo : ["अपात्र या गलत दस्तावेज वाले आवेदन", "अन्य समान सरकारी योजनाओं के लाभार्थी"];

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
        actTitle="पात्रता मानदंड (Eligibility Criteria)"
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
              background: "rgba(16, 185, 129, 0.12)",
              border: "1px solid rgba(16, 185, 129, 0.35)",
              color: "#059669",
              fontSize: 14,
              fontWeight: 800,
              padding: "6px 18px",
              borderRadius: 100,
              textTransform: "uppercase",
              letterSpacing: 0.6,
            }}
          >
            📋 पात्रता सूची
          </span>
          <span style={{ fontSize: 26, fontWeight: 900, color: "#0f172a" }}>
            कौन-कौन पात्र हैं और किन्हें इस योजना से बाहर रखा गया है?
          </span>
        </div>

        {/* Dual-Column Eligibility Matrix */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 26 }}>
          {/* Left: Eligible Citizens (Mint / Emerald Glass) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 253, 244, 0.92) 100%)",
              border: "2px solid rgba(16, 185, 129, 0.5)",
              borderRadius: 24,
              padding: "26px 30px",
              boxShadow: "0 14px 40px rgba(16, 185, 129, 0.08)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - leftCardSpring) * -25}px)`,
              opacity: leftCardSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span
                style={{
                  background: "#d1fae5",
                  color: "#047857",
                  fontSize: 13,
                  fontWeight: 800,
                  padding: "5px 14px",
                  borderRadius: 8,
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                }}
              >
                <span>✓</span> ये लोग पूरी तरह पात्र हैं
              </span>
              <span style={{ fontSize: 13, fontWeight: 700, color: "#059669" }}>
                स्वीकृत श्रेणी
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {yesList.map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 12,
                    background: "rgba(255, 255, 255, 0.8)",
                    border: "1px solid rgba(16, 185, 129, 0.25)",
                    padding: "12px 16px",
                    borderRadius: 14,
                  }}
                >
                  <span style={{ color: "#059669", fontWeight: 900, fontSize: 18, lineHeight: 1.2 }}>✓</span>
                  <span style={{ fontSize: 19, fontWeight: 700, color: "#0f172a", lineHeight: 1.4 }}>
                    {item}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Ineligible / Excluded (Warm Saffron / Amber Glass) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 247, 237, 0.92) 100%)",
              border: "2px solid rgba(249, 115, 22, 0.45)",
              borderRadius: 24,
              padding: "26px 30px",
              boxShadow: "0 14px 40px rgba(249, 115, 22, 0.08)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - rightCardSpring) * 25}px)`,
              opacity: rightCardSpring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <span
                style={{
                  background: "#ffedd5",
                  color: "#c2410c",
                  fontSize: 13,
                  fontWeight: 800,
                  padding: "5px 14px",
                  borderRadius: 8,
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                }}
              >
                <span>✕</span> किन्हें लाभ नहीं मिलेगा / अपात्र
              </span>
              <span style={{ fontSize: 13, fontWeight: 700, color: "#ea580c" }}>
                अस्वीकृत श्रेणी
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {noList.map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 12,
                    background: "rgba(255, 255, 255, 0.8)",
                    border: "1px solid rgba(249, 115, 22, 0.25)",
                    padding: "12px 16px",
                    borderRadius: 14,
                  }}
                >
                  <span style={{ color: "#ea580c", fontWeight: 900, fontSize: 18, lineHeight: 1.2 }}>✕</span>
                  <span style={{ fontSize: 19, fontWeight: 700, color: "#334155", lineHeight: 1.4 }}>
                    {item}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Bottom Verification Note Pill */}
        <div
          style={{
            background: "rgba(239, 246, 255, 0.95)",
            border: "1px solid rgba(59, 130, 246, 0.3)",
            borderRadius: 14,
            padding: "12px 20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 16 }}>ℹ️</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: "#1e40af" }}>
              यदि आप इन शर्तों को पूरा करते हैं, तो आधिकारिक पोर्टल {domain} पर तत्काल अपना आवेदन व e-KYC सत्यापन पूरा करें।
            </span>
          </div>
          <span style={{ fontSize: 12, fontWeight: 800, color: "#0284c7" }}>
            100% आधिकारिक मापदंड
          </span>
        </div>
      </div>
    </div>
  );
};
