import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";

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

const DOC_ICONS = ["🪪", "🏦", "📱", "📸", "📄", "🏠"];

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

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const bottomSpring = spring({ frame, fps, delay: 20, config: { damping: 12, stiffness: 100 } });

  const rawDocs = documents.length > 0 ? documents : ["आधार कार्ड (Aadhaar)", "बैंक पासबुक (DBT सक्रिय)", "सक्रिय मोबाइल नंबर", "पासपोर्ट साइज फोटो"];
  const docList = rawDocs.slice(0, 4);

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
          urgencyBadge="ज़रूरी दस्तावेज़ चेकलिस्ट"
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="आवेदन हेतु क्या-क्या चाहिए?"
        />
      </div>

      {/* 2. Floating 3D/Glass Document Card Grid (High Screenshot Value) */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 28,
          flex: 1,
          marginTop: 20,
          marginBottom: 20,
          alignItems: "center",
        }}
      >
        {docList.map((doc, idx) => {
          const itemSpring = spring({
            frame,
            fps,
            delay: 6 + idx * 4,
            config: { damping: 12, stiffness: 110 },
          });

          return (
            <div
              key={idx}
              style={{
                transform: `translateY(${(1 - itemSpring) * 30}px) scale(${itemSpring})`,
                opacity: itemSpring,
                background: "rgba(11, 17, 32, 0.96)",
                border: "2px solid rgba(56, 189, 248, 0.4)",
                borderRadius: 24,
                padding: "24px 28px",
                display: "flex",
                alignItems: "center",
                gap: 20,
                boxShadow: "0 20px 50px rgba(0, 0, 0, 0.65), 0 0 20px rgba(56, 189, 248, 0.15)",
              }}
            >
              {/* Icon Container */}
              <div
                style={{
                  width: 64,
                  height: 64,
                  borderRadius: 18,
                  background: "linear-gradient(135deg, rgba(56, 189, 248, 0.25), rgba(37, 99, 235, 0.35))",
                  border: "1.5px solid rgba(56, 189, 248, 0.6)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 32,
                  boxShadow: "0 6px 16px rgba(0, 0, 0, 0.3)",
                }}
              >
                {DOC_ICONS[idx % DOC_ICONS.length]}
              </div>

              {/* Doc Info */}
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 800, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 0.8 }}>
                  दस्तावेज़ क्रमांक {idx + 1}
                </div>
                <div style={{ fontSize: 24, fontWeight: 900, color: "#f8fafc", lineHeight: 1.25, marginTop: 4 }}>
                  {doc}
                </div>
                <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 4 }}>
                  मूल प्रति एवं स्व-प्रमाणित छायाप्रति
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* 3. Floating Screenshot Advice & Bank Note Ribbon */}
      <div
        style={{
          transform: `translateY(${(1 - bottomSpring) * 20}px)`,
          opacity: bottomSpring,
          background: "rgba(15, 23, 42, 0.96)",
          border: "1.5px solid rgba(52, 211, 153, 0.5)",
          borderRadius: 20,
          padding: "16px 32px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: "0 14px 40px rgba(0, 0, 0, 0.55)",
          marginBottom: 50,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <span
            style={{
              background: "rgba(52, 211, 153, 0.2)",
              color: "#34d399",
              padding: "6px 14px",
              borderRadius: 10,
              fontSize: 14,
              fontWeight: 900,
            }}
          >
            📸 स्क्रीनशॉट ले लें
          </span>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9" }}>
            {bankNote || "बैंक खाते में आधार लिंक और DBT (Direct Benefit Transfer) सक्रिय होना अनिवार्य है।"}
          </span>
        </div>

        <div style={{ fontSize: 13, fontWeight: 800, color: "#94a3b8" }}>
          🏛️ @iDastawez वेरीफाइड
        </div>
      </div>
    </div>
  );
};
