import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";

interface Props {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  helpline?: string;
  warning?: string;
  category?: string;
}

export const DastawezAlert: React.FC<Props> = ({
  schemeName,
  ministry,
  portalUrl,
  helpline,
  warning,
  category,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const alertSpring = spring({ frame, fps, delay: 5, config: { damping: 14 } });
  const ctaSpring = spring({ frame, fps, delay: 20, config: { damping: 12 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 20%, #151a30 0%, #0a0e1c 60%, #03050a 100%)",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      <DastawezHeader ministry={ministry} category={category} schemeName={schemeName} />

      <div
        style={{
          position: "absolute",
          top: 140,
          bottom: 40,
          left: 56,
          right: 56,
          display: "flex",
          flexDirection: "column",
          gap: 28,
          justifyContent: "center",
        }}
      >
        {/* Anti-Fraud Alert Box */}
        <div
          style={{
            background: "linear-gradient(135deg, rgba(220, 38, 38, 0.15) 0%, rgba(153, 27, 27, 0.25) 100%)",
            border: "2px solid rgba(248, 113, 113, 0.4)",
            borderRadius: 24,
            padding: "32px 36px",
            display: "flex",
            alignItems: "center",
            gap: 24,
            boxShadow: "0 20px 40px rgba(220, 38, 38, 0.25)",
            transform: `scale(${alertSpring})`,
            opacity: alertSpring,
          }}
        >
          <div
            style={{
              width: 72,
              height: 72,
              borderRadius: "50%",
              background: "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 36,
              color: "#ffffff",
              boxShadow: "0 0 25px rgba(239, 68, 68, 0.6)",
              flexShrink: 0,
            }}
          >
            🛡️
          </div>
          <div>
            <div style={{ fontSize: 20, fontWeight: 800, color: "#fca5a5", textTransform: "uppercase", letterSpacing: 1 }}>
              आधिकारिक चेतावनी एवं साइबर सुरक्षा अलर्ट
            </div>
            <div style={{ fontSize: 28, fontWeight: 800, color: "#ffffff", marginTop: 6, lineHeight: 1.3 }}>
              {warning || "सरकारी योजनाओं के लिए आवेदन 100% निःशुल्क है। किसी भी अनधिकृत लिंक या साइबर कैफे वाले को अवैध शुल्क न दें।"}
            </div>
          </div>
        </div>

        {/* Portal & Helpline Row */}
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr", gap: 28 }}>
          {/* Official Portal Card */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.75)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(255, 255, 255, 0.14)",
              borderRadius: 22,
              padding: "28px 32px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div style={{ fontSize: 16, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
              🌐 एकमात्र आधिकारिक सरकारी पोर्टल
            </div>
            <div
              style={{
                fontSize: 32,
                fontWeight: 800,
                color: "#38bdf8",
                marginTop: 10,
                wordBreak: "break-all",
              }}
            >
              {portalUrl || "https://india.gov.in"}
            </div>
            <div style={{ fontSize: 15, color: "#64748b", marginTop: 8 }}>
              (सीधा लिंक नीचे वीडियो के डिस्क्रिप्शन बॉक्स में उपलब्ध है)
            </div>
          </div>

          {/* Helpline Card */}
          <div
            style={{
              background: "rgba(15, 23, 42, 0.75)",
              backdropFilter: "blur(16px)",
              border: "1px solid rgba(255, 255, 255, 0.14)",
              borderRadius: 22,
              padding: "28px 32px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div style={{ fontSize: 16, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>
              📞 राष्ट्रीय टोल-फ्री हेल्पलाइन
            </div>
            <div
              style={{
                fontSize: 36,
                fontWeight: 900,
                color: "#34d399",
                marginTop: 10,
              }}
            >
              {helpline || "1800-11-1947"}
            </div>
            <div style={{ fontSize: 15, color: "#64748b", marginTop: 8 }}>
              (किसी भी समस्या के समाधान के लिए सुबह 8 से रात 8 बजे तक)
            </div>
          </div>
        </div>

        {/* Subscribe & Share CTA */}
        <div
          style={{
            background: "linear-gradient(90deg, rgba(249, 115, 22, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%)",
            border: "1px solid rgba(255, 255, 255, 0.16)",
            borderRadius: 22,
            padding: "22px 32px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateY(${(1 - ctaSpring) * 20}px)`,
            opacity: ctaSpring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ fontSize: 32 }}>🔔</div>
            <div>
              <div style={{ fontSize: 22, fontWeight: 800, color: "#ffffff" }}>
                सच्ची और प्रमाणित सरकारी योजनाओं के लिए iDastawez को सब्सक्राइब करें
              </div>
              <div style={{ fontSize: 15, color: "#cbd5e1", marginTop: 2 }}>
                इस वीडियो को अपने परिवार और दोस्तों के साथ व्हाट्सएप पर ज़रूर साझा करें।
              </div>
            </div>
          </div>
          <div
            style={{
              background: "#ef4444",
              color: "#ffffff",
              fontWeight: 900,
              fontSize: 18,
              padding: "12px 28px",
              borderRadius: 30,
              boxShadow: "0 6px 20px rgba(239, 68, 68, 0.4)",
            }}
          >
            SUBSCRIBE @iDastawez
          </div>
        </div>
      </div>
    </div>
  );
};
