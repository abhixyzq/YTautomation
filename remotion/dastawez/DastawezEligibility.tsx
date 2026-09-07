import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";

interface DastawezEligibilityProps {
  schemeName: string;
  ministry?: string;
  eligibilityYes?: string[];
  eligibilityNo?: string[];
  priorityGroups?: string[];
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

export const DastawezEligibility: React.FC<DastawezEligibilityProps> = ({
  schemeName,
  ministry,
  eligibilityYes = [],
  eligibilityNo = [],
  priorityGroups = [],
  category,
  evidence,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 3,
  totalActs = 6,
  portalUrl,
  officialPortalDomain,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const yesSpring = spring({ frame, fps, delay: 10, config: { damping: 12, stiffness: 100 } });
  const noSpring = spring({ frame, fps, delay: 18, config: { damping: 12, stiffness: 100 } });

  const yesList =
    eligibilityYes.length > 0
      ? eligibilityYes.slice(0, 3)
      : ["पात्र ग्रामीण एवं शहरी नागरिक", "राशन कार्ड / बीपीएल परिवार", "18 वर्ष या अधिक आयु वर्ग"];
  const noList =
    eligibilityNo.length > 0
      ? eligibilityNo.slice(0, 2)
      : ["सरकारी कर्मचारी या आयकरदाता (Taxpayer)", "अपूर्ण दस्तावेज या असत्यापित बैंक खाता"];

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
          urgencyBadge="पात्रता एवं शर्तें"
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="किन्हें मिलेगा लाभ?"
        />
      </div>

      {/* 2. Floating Eligibility Split Columns */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.15fr 1fr",
          gap: 36,
          alignItems: "stretch",
          flex: 1,
          marginTop: 24,
          marginBottom: 40,
        }}
      >
        {/* Left: Eligible List (Glowing Emerald Glass) */}
        <div
          style={{
            transform: `translateY(${(1 - yesSpring) * 30}px)`,
            opacity: yesSpring,
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid rgba(16, 185, 129, 0.5)",
            borderRadius: 24,
            padding: "32px 36px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: "0 24px 60px rgba(0, 0, 0, 0.65), 0 0 30px rgba(16, 185, 129, 0.15)",
          }}
        >
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
              <span
                style={{
                  background: "rgba(16, 185, 129, 0.2)",
                  border: "1px solid rgba(16, 185, 129, 0.6)",
                  color: "#6ee7b7",
                  fontSize: 14,
                  fontWeight: 900,
                  padding: "6px 14px",
                  borderRadius: 12,
                  letterSpacing: 0.8,
                }}
              >
                ✅ कौन-कौन पात्र हैं? (ELIGIBLE)
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {yesList.map((item, idx) => (
                <div
                  key={idx}
                  style={{
                    background: "rgba(30, 41, 59, 0.75)",
                    border: "1px solid rgba(16, 185, 129, 0.3)",
                    padding: "14px 20px",
                    borderRadius: 14,
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    fontSize: 20,
                    fontWeight: 700,
                    color: "#f8fafc",
                  }}
                >
                  <span style={{ color: "#34d399", fontSize: 22 }}>✔</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div
            style={{
              fontSize: 13,
              color: "#34d399",
              borderTop: "1px solid rgba(16, 185, 129, 0.2)",
              paddingTop: 12,
              marginTop: 16,
              fontWeight: 700,
            }}
          >
            📌 100% सरकारी दिशा-निर्देशों के अनुसार सत्यापन
          </div>
        </div>

        {/* Right: Ineligible List (Amber/Red Glass) */}
        <div
          style={{
            transform: `translateY(${(1 - noSpring) * 30}px)`,
            opacity: noSpring,
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "1.5px solid rgba(244, 63, 94, 0.4)",
            borderRadius: 24,
            padding: "32px 36px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: "0 20px 50px rgba(0, 0, 0, 0.6)",
          }}
        >
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
              <span
                style={{
                  background: "rgba(244, 63, 94, 0.2)",
                  border: "1px solid rgba(244, 63, 94, 0.6)",
                  color: "#fda4af",
                  fontSize: 14,
                  fontWeight: 900,
                  padding: "6px 14px",
                  borderRadius: 12,
                  letterSpacing: 0.8,
                }}
              >
                ❌ किन्हें लाभ नहीं मिलेगा? (EXCLUDED)
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {noList.map((item, idx) => (
                <div
                  key={idx}
                  style={{
                    background: "rgba(30, 41, 59, 0.75)",
                    border: "1px solid rgba(244, 63, 94, 0.3)",
                    padding: "14px 20px",
                    borderRadius: 14,
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    fontSize: 20,
                    fontWeight: 700,
                    color: "#e2e8f0",
                  }}
                >
                  <span style={{ color: "#f43f5e", fontSize: 22 }}>✖</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div
            style={{
              fontSize: 13,
              color: "#fca5a5",
              borderTop: "1px solid rgba(244, 63, 94, 0.2)",
              paddingTop: 12,
              marginTop: 16,
              fontWeight: 700,
            }}
          >
            ⚠️ अपात्र पाए जाने पर फॉर्म स्वतः निरस्त होगा
          </div>
        </div>
      </div>
    </div>
  );
};
