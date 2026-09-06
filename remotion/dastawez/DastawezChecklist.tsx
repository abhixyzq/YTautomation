import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";
import { DastawezHeader } from "./DastawezHeader";

interface Props {
  schemeName: string;
  ministry?: string;
  documents?: string[];
  bankNote?: string;
  category?: string;
}

export const DastawezChecklist: React.FC<Props> = ({
  schemeName,
  ministry,
  documents = [],
  bankNote,
  category,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const headerSpring = spring({ frame, fps, delay: 5, config: { damping: 14 } });
  const bannerSpring = spring({ frame, fps, delay: 25, config: { damping: 12 } });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 20%, #0c233c 0%, #06111e 60%, #01060d 100%)",
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
          gap: 22,
        }}
      >
        {/* Title */}
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <span style={{ fontSize: 16, fontWeight: 700, color: "#f59e0b", textTransform: "uppercase", letterSpacing: 1.5 }}>
              अनिवार्य कागज़ात (Mandatory Documents)
            </span>
            <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "6px 0 0 0" }}>
              आवेदन के लिए ज़रूरी दस्तावेज़ों की चेकलिस्ट
            </h2>
          </div>
          <div
            style={{
              padding: "10px 24px",
              background: "rgba(245, 158, 11, 0.15)",
              borderRadius: 30,
              border: "1px solid rgba(245, 158, 11, 0.35)",
              fontSize: 16,
              fontWeight: 700,
              color: "#fbbf24",
            }}
          >
            📁 स्पष्ट एवं वैध दस्तावेज़ ही अपलोड करें
          </div>
        </div>

        {/* Documents Cards Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: documents.length > 2 ? "1fr 1fr" : "1fr",
            gap: 20,
            flex: 1,
            alignContent: "start",
          }}
        >
          {documents.map((doc, idx) => {
            const docSpring = spring({ frame, fps, delay: 10 + idx * 7, config: { damping: 14 } });
            return (
              <div
                key={idx}
                style={{
                  background: "rgba(15, 23, 42, 0.8)",
                  backdropFilter: "blur(16px)",
                  border: "1px solid rgba(255, 255, 255, 0.14)",
                  borderRadius: 20,
                  padding: "24px 28px",
                  display: "flex",
                  alignItems: "center",
                  gap: 20,
                  boxShadow: "0 10px 25px rgba(0, 0, 0, 0.3)",
                  transform: `scale(${docSpring})`,
                  opacity: docSpring,
                }}
              >
                <div
                  style={{
                    width: 52,
                    height: 52,
                    borderRadius: 14,
                    background: "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 24,
                    color: "#ffffff",
                    fontWeight: 900,
                    boxShadow: "0 4px 15px rgba(59, 130, 246, 0.4)",
                  }}
                >
                  {idx + 1}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 22, fontWeight: 700, color: "#f8fafc", lineHeight: 1.35 }}>
                    {doc}
                  </div>
                  <div style={{ fontSize: 14, color: "#94a3b8", marginTop: 4, fontWeight: 500 }}>
                    सत्यापित डिजिटल कॉपी / ओरिजिनल दस्तावेज़
                  </div>
                </div>
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    background: "rgba(16, 185, 129, 0.2)",
                    border: "1px solid rgba(16, 185, 129, 0.5)",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    color: "#34d399",
                    fontWeight: 900,
                  }}
                >
                  ✓
                </div>
              </div>
            );
          })}
        </div>

        {/* Bank NPCI / DBT Warning Banner */}
        <div
          style={{
            background: "linear-gradient(90deg, rgba(234, 88, 12, 0.2) 0%, rgba(194, 65, 12, 0.1) 100%)",
            border: "2px solid rgba(249, 115, 22, 0.45)",
            borderRadius: 20,
            padding: "20px 28px",
            display: "flex",
            alignItems: "center",
            gap: 20,
            boxShadow: "0 10px 30px rgba(0, 0, 0, 0.4)",
            transform: `translateY(${(1 - bannerSpring) * 20}px)`,
            opacity: bannerSpring,
          }}
        >
          <div
            style={{
              fontSize: 32,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            ⚠️
          </div>
          <div>
            <div style={{ fontSize: 20, fontWeight: 800, color: "#fb923c" }}>
              विशेष ध्यान दें: बैंक खाता आधार से लिंक (NPCI DBT Seeding) होना आवश्यक है
            </div>
            <div style={{ fontSize: 16, color: "#fed7aa", marginTop: 4, fontWeight: 500 }}>
              {bankNote || "यदि आपका बैंक खाता NPCI से मैप नहीं है, तो सरकारी सहायता सीधे खाते में नहीं आ पाएगी। अपने बैंक में तुरंत e-KYC कराएं।"}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
