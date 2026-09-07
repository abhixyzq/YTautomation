import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";

interface DastawezAlertProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  warning?: string;
  dosAndDonts?: string[];
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

export const DastawezAlert: React.FC<DastawezAlertProps> = ({
  schemeName,
  ministry,
  portalUrl,
  officialPortalDomain,
  helpline,
  warning,
  dosAndDonts,
  category,
  evidence,
  visualMedia,
  officialImagePath,
  officialImageTitle,
  brollVideoPath,
  attribution,
  currentActIndex = 6,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const cardSpring = spring({ frame, fps, delay: 10, config: { damping: 12, stiffness: 100 } });
  const subSpring = spring({ frame, fps, delay: 18, config: { damping: 12, stiffness: 100 } });

  const alertMessage =
    warning ||
    "यह पूरी सरकारी प्रक्रिया 100% निःशुल्क है। किसी भी साइबर कैफे या बिचौलिए को कोई अवैध शुल्क न दें।";

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
          urgencyBadge="आधिकारिक सतर्कता एवं निर्देश"
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="सावधानी व आधिकारिक सत्यापन"
        />
      </div>

      {/* 2. Floating Cyber Alert & Official Verification Card */}
      <div
        style={{
          transform: `translateY(${(1 - cardSpring) * 30}px)`,
          opacity: cardSpring,
          background: "rgba(11, 17, 32, 0.9)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          border: "2px solid rgba(225, 29, 72, 0.5)",
          borderRadius: 28,
          padding: "36px 44px",
          display: "flex",
          flexDirection: "column",
          gap: 20,
          boxShadow: "0 24px 60px rgba(0, 0, 0, 0.7), 0 0 30px rgba(225, 29, 72, 0.2)",
          marginTop: 20,
          marginBottom: 20,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: 16,
              background: "linear-gradient(135deg, #e11d48, #be123c)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 26,
              boxShadow: "0 4px 16px rgba(225, 29, 72, 0.4)",
            }}
          >
            🛡️
          </div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 900, color: "#fda4af", textTransform: "uppercase", letterSpacing: 0.8 }}>
              आधिकारिक जन-हित चेतावनी
            </div>
            <div style={{ fontSize: 28, fontWeight: 900, color: "#ffffff" }}>
              साइबर फ्रॉड व अवैध दलालों से सावधान रहें
            </div>
          </div>
        </div>

        <div style={{ fontSize: 20, fontWeight: 700, color: "#e2e8f0", lineHeight: 1.5 }}>
          {alertMessage}
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 20, flexWrap: "wrap", marginTop: 8 }}>
          <div
            style={{
              background: "rgba(30, 41, 59, 0.8)",
              border: "1px solid rgba(56, 189, 248, 0.4)",
              padding: "10px 18px",
              borderRadius: 14,
              fontSize: 15,
              fontWeight: 800,
              color: "#38bdf8",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span>🌐 केवल सरकारी पोर्टल:</span>
            <span>https://{domain}</span>
          </div>

          <div
            style={{
              background: "rgba(30, 41, 59, 0.8)",
              border: "1px solid rgba(52, 211, 153, 0.4)",
              padding: "10px 18px",
              borderRadius: 14,
              fontSize: 15,
              fontWeight: 800,
              color: "#34d399",
              display: "flex",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span>📞 राष्ट्रीय हेल्पलाइन:</span>
            <span>{helpline || "1947 / 1800-xxx-xxxx"}</span>
          </div>
        </div>
      </div>

      {/* 3. Floating Subscribe Call to Action Ribbon */}
      <div
        style={{
          transform: `translateY(${(1 - subSpring) * 20}px)`,
          opacity: subSpring,
          background: "linear-gradient(90deg, rgba(14, 165, 233, 0.25) 0%, rgba(15, 23, 42, 0.92) 25%, rgba(15, 23, 42, 0.92) 75%, rgba(14, 165, 233, 0.25) 100%)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "1.5px solid rgba(56, 189, 248, 0.5)",
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
          <span style={{ fontSize: 24 }}>🔔</span>
          <div>
            <div style={{ fontSize: 13, fontWeight: 800, color: "#38bdf8", textTransform: "uppercase" }}>
              सरकारी योजनाओं की 100% सटीक व प्रमाणिक जानकारी
            </div>
            <div style={{ fontSize: 20, fontWeight: 900, color: "#ffffff" }}>
              @iDastawez को अभी सब्सक्राइब करें
            </div>
          </div>
        </div>

        <div
          style={{
            background: "linear-gradient(135deg, #e11d48, #f43f5e)",
            color: "#ffffff",
            padding: "10px 24px",
            borderRadius: 14,
            fontSize: 16,
            fontWeight: 900,
            boxShadow: "0 4px 16px rgba(225, 29, 72, 0.4)",
            display: "flex",
            alignItems: "center",
            gap: 8,
          }}
        >
          <span>SUBSCRIBE</span>
          <span>▶</span>
        </div>
      </div>
    </div>
  );
};
