import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";
import { EvidenceMetadata } from "./types";

interface DastawezAlertProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  warning?: string;
  category?: string;
  evidence?: EvidenceMetadata;
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
  category,
  evidence,
  currentActIndex = 5,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.03], {
    extrapolateRight: "clamp",
  });

  const entrance = spring({ frame, fps, delay: 4, config: { damping: 14, stiffness: 100 } });
  const card1Spring = spring({ frame, fps, delay: 10, config: { damping: 14 } });
  const card2Spring = spring({ frame, fps, delay: 40, config: { damping: 14 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 25%, #18090d 0%, #0c0507 60%, #050203 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Subtle Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "radial-gradient(rgba(239, 68, 68, 0.1) 1px, transparent 1px), radial-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
          backgroundSize: "40px 40px, 80px 80px",
          pointerEvents: "none",
          opacity: 0.6,
        }}
      />

      <DastawezHeader
        ministry={ministry}
        category={category}
        schemeName={schemeName}
        currentActIndex={currentActIndex}
        totalActs={totalActs}
        actTitle="सावधानी व हेल्पलाइन"
        portalDomain={domain}
      />

      <div
        style={{
          position: "absolute",
          top: 145,
          bottom: 110,
          left: 64,
          right: 64,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: 22,
          transform: `scale(${cameraScale})`,
        }}
      >
        {/* Header Badge */}
        <div style={{ transform: `translateY(${(1 - entrance) * 20}px)`, opacity: entrance }}>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(220, 38, 38, 0.15)",
              border: "1px solid rgba(239, 68, 68, 0.5)",
              padding: "6px 18px",
              borderRadius: 100,
              width: "fit-content",
            }}
          >
            <span style={{ fontSize: 15, fontWeight: 800, color: "#f87171", letterSpacing: 0.6 }}>
              नागरिक सुरक्षा एडवाइजरी | CITIZEN FRAUD CAUTION
            </span>
          </div>
          <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "6px 0 0 0" }}>
            फर्जी वेबसाइटों एवं दलालों से कैसे बचें?
          </h2>
        </div>

        {/* Two-Column Layout: Warning vs Helpline */}
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 28, marginTop: 4 }}>
          {/* Card 1: Official Warning Box */}
          <div
            style={{
              background: "rgba(24, 12, 16, 0.9)",
              border: "2px solid rgba(239, 68, 68, 0.6)",
              borderRadius: 22,
              padding: "28px 32px",
              boxShadow: "0 16px 45px rgba(0, 0, 0, 0.6), 0 0 20px rgba(239, 68, 68, 0.15)",
              display: "flex",
              flexDirection: "column",
              gap: 16,
              transform: `translateX(${(1 - card1Spring) * -30}px)`,
              opacity: card1Spring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontSize: 26 }}>⚠️</span>
              <div style={{ fontSize: 16, fontWeight: 800, color: "#f87171", textTransform: "uppercase" }}>
                महत्वपूर्ण सरकारी चेतावनी
              </div>
            </div>

            <div style={{ fontSize: 23, fontWeight: 700, color: "#ffffff", lineHeight: 1.5 }}>
              {warning || "किसी भी अनधिकृत लिंक या साइबर दलाल को व्यक्तिगत दस्तावेज व अवैध फीस न दें।"}
            </div>

            <div
              style={{
                background: "rgba(15, 23, 42, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: 12,
                padding: "14px 18px",
                fontSize: 15,
                color: "#cbd5e1",
                lineHeight: 1.5,
              }}
            >
              🔒 <strong>सुरक्षा नियम:</strong> सरकारी योजनाओं में ऑनलाइन आवेदन सदैव <strong>.gov.in</strong> या <strong>.nic.in</strong> पोर्टल पर ही होता है। किसी भी .com / .org / .xyz लिंक पर भरोसा न करें।
            </div>
          </div>

          {/* Card 2: Official National Helpline */}
          <div
            style={{
              background: "rgba(10, 18, 36, 0.88)",
              border: "1px solid rgba(59, 130, 246, 0.4)",
              borderRadius: 22,
              padding: "28px 32px",
              boxShadow: "0 16px 45px rgba(0, 0, 0, 0.6)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              gap: 18,
              transform: `translateX(${(1 - card2Spring) * 30}px)`,
              opacity: card2Spring,
            }}
          >
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
                सत्यापित राष्ट्रीय हेल्पलाइन
              </div>
              <div
                style={{
                  fontSize: 36,
                  fontWeight: 900,
                  color: "#38bdf8",
                  marginTop: 10,
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                }}
              >
                <span>📞</span>
                <span>{helpline || "1800-11-0001"}</span>
              </div>
              <div style={{ fontSize: 14, color: "#94a3b8", marginTop: 6 }}>
                सोमवार से शनिवार (कार्यदिवस) में सीधे संपर्क करें
              </div>
            </div>

            <div
              style={{
                background: "rgba(15, 23, 42, 0.7)",
                border: "1px solid rgba(255, 255, 255, 0.1)",
                borderRadius: 12,
                padding: "12px 18px",
                display: "flex",
                alignItems: "center",
                gap: 10,
              }}
            >
              <span style={{ fontSize: 18 }}>🌐</span>
              <span style={{ fontSize: 15, fontWeight: 700, color: "#ffffff" }}>
                पोर्टल: {domain}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
