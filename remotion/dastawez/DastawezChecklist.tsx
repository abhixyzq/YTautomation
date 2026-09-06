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

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.03], {
    extrapolateRight: "clamp",
  });

  const entrance = spring({ frame, fps, delay: 4, config: { damping: 14, stiffness: 100 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  // Progressive spotlight: determine which document is actively spoken based on frames
  // e.g. each document gets ~50 frames of active spotlight
  const activeDocIdx = Math.min(documents.length - 1, Math.floor(frame / 60));

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        background: "radial-gradient(circle at 50% 25%, #081329 0%, #050a14 60%, #02050a 100%)",
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
            "radial-gradient(rgba(59, 130, 246, 0.12) 1px, transparent 1px), radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px)",
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
        actTitle="ज़रूरी दस्तावेज़ (Documents)"
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
        {/* Header Block */}
        <div style={{ transform: `translateY(${(1 - entrance) * 20}px)`, opacity: entrance }}>
          <div style={{ fontSize: 15, fontWeight: 800, color: "#38bdf8", textTransform: "uppercase", letterSpacing: 1 }}>
            सत्यापित दस्तावेज़ चेकलिस्ट 2026
          </div>
          <h2 style={{ fontSize: 44, fontWeight: 900, color: "#ffffff", margin: "4px 0 0 0" }}>
            आवेदन हेतु अनिवार्य सरकारी कागजात
          </h2>
        </div>

        {/* Sequential Dynamic Document Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20 }}>
          {documents.map((doc, idx) => {
            const docDelay = 8 + idx * 18;
            const docSpring = spring({ frame, fps, delay: docDelay, config: { damping: 14 } });
            const isSpotlight = idx === activeDocIdx;

            return (
              <div
                key={idx}
                style={{
                  background: isSpotlight
                    ? "linear-gradient(145deg, rgba(30, 58, 138, 0.5) 0%, rgba(10, 18, 36, 0.95) 100%)"
                    : "rgba(10, 18, 36, 0.75)",
                  border: isSpotlight
                    ? "2px solid rgba(59, 130, 246, 0.9)"
                    : "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: 18,
                  padding: "20px 22px",
                  boxShadow: isSpotlight
                    ? "0 14px 40px rgba(0,0,0,0.7), 0 0 20px rgba(37, 99, 235, 0.3)"
                    : "0 8px 25px rgba(0,0,0,0.4)",
                  display: "flex",
                  flexDirection: "column",
                  gap: 12,
                  transform: `scale(${isSpotlight ? 1.03 : 1.0}) translateY(${(1 - docSpring) * 20}px)`,
                  opacity: docSpring,
                  transition: "all 0.3s ease",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <div
                    style={{
                      width: 32,
                      height: 32,
                      borderRadius: 8,
                      background: isSpotlight ? "#2563eb" : "rgba(255, 255, 255, 0.1)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 16,
                      fontWeight: 800,
                      color: "#ffffff",
                    }}
                  >
                    {idx + 1}
                  </div>
                  {isSpotlight && (
                    <div
                      style={{
                        background: "rgba(34, 197, 94, 0.2)",
                        border: "1px solid rgba(34, 197, 94, 0.6)",
                        borderRadius: 6,
                        padding: "2px 8px",
                        fontSize: 11,
                        fontWeight: 800,
                        color: "#4ade80",
                      }}
                    >
                      सक्रिय बिंदु
                    </div>
                  )}
                </div>

                <div style={{ fontSize: 18, fontWeight: 700, color: "#ffffff", lineHeight: 1.45 }}>
                  {doc}
                </div>
              </div>
            );
          })}
        </div>

        {/* Bank Aadhaar-NPCI Mandatory Alert Callout */}
        <div
          style={{
            background: "rgba(15, 23, 42, 0.85)",
            border: "1px solid rgba(59, 130, 246, 0.4)",
            borderRadius: 16,
            padding: "16px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ fontSize: 24 }}>💳</span>
            <div>
              <div style={{ fontSize: 13, fontWeight: 800, color: "#60a5fa", textTransform: "uppercase" }}>
                सीधा बैंक अंतरण (DBT) नियम
              </div>
              <div style={{ fontSize: 18, fontWeight: 700, color: "#f8fafc", marginTop: 2 }}>
                {bankNote || "बैंक खाते में आधार NPCI मैपिंग एवं एक्टिव DBT होना अनिवार्य है।"}
              </div>
            </div>
          </div>
          <div
            style={{
              background: "rgba(37, 99, 235, 0.2)",
              border: "1px solid rgba(59, 130, 246, 0.5)",
              borderRadius: 8,
              padding: "6px 14px",
              fontSize: 13,
              fontWeight: 800,
              color: "#93c5fd",
            }}
          >
            पैसा सीधे खाते में
          </div>
        </div>
      </div>
    </div>
  );
};
