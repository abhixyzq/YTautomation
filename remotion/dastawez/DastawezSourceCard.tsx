import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

interface DastawezSourceCardProps {
  schemeName: string;
  ministry?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  helpline?: string;
  evidence?: EvidenceMetadata;
  category?: string;
  visualMedia?: SceneVisualMedia;
  officialImagePath?: string;
  officialImageTitle?: string;
  brollVideoPath?: string;
  attribution?: string;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezSourceCard: React.FC<DastawezSourceCardProps> = ({
  schemeName,
  ministry,
  portalUrl,
  officialPortalDomain,
  helpline = "1967 / 1800-180-2087",
  evidence,
  category = "नागरिक अधिकार",
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

  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.02], {
    extrapolateRight: "clamp",
  });

  const card1Spring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 100 } });
  const card2Spring = spring({ frame, fps, delay: 8, config: { damping: 14, stiffness: 100 } });
  const card3Spring = spring({ frame, fps, delay: 14, config: { damping: 14, stiffness: 100 } });
  const card4Spring = spring({ frame, fps, delay: 20, config: { damping: 14, stiffness: 100 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const ministryName = evidence?.ministry || ministry || "भारत सरकार (Government of India)";
  const notifRef = evidence?.notification_ref || "सार्वजनिक परिपत्र / राजपत्र 2026";
  const verifiedDate = evidence?.last_verified_date || "सितंबर 2026";
  const citationText =
    evidence?.source_citation ||
    `भारत सरकार के आधिकारिक पोर्टल ${domain} तथा शासकीय अधिसूचना से संकलित व पुष्ट जानकारी।`;

  const helplineNumber = evidence?.helpline || helpline;

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
      {/* Full-Screen Container without bulky Navbar */}
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
        {/* Sleek Top Inline Meta-Bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            background: "rgba(255, 255, 255, 0.85)",
            backdropFilter: "blur(16px)",
            WebkitBackdropFilter: "blur(16px)",
            border: "1px solid rgba(226, 232, 240, 0.9)",
            borderRadius: 14,
            padding: "8px 20px",
            boxShadow: "0 4px 20px rgba(15, 23, 42, 0.04)",
          }}
        >
          {/* Left: Brand Monogram + Scheme Title + Domain */}
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <div
              style={{
                width: 32,
                height: 32,
                borderRadius: 8,
                background: "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: 900,
                fontSize: 14,
                color: "#ffffff",
                letterSpacing: -0.5,
              }}
            >
              iD
            </div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 8 }}>
              <span style={{ fontSize: 16, fontWeight: 900, color: "#0f172a" }}>
                {schemeName}
              </span>
              <span style={{ fontSize: 13, fontWeight: 600, color: "#64748b" }}>
                • {ministryName}
              </span>
            </div>
            <div
              style={{
                background: "rgba(2, 132, 199, 0.08)",
                border: "1px solid rgba(2, 132, 199, 0.25)",
                padding: "3px 10px",
                borderRadius: 6,
                fontSize: 11,
                fontWeight: 700,
                color: "#0369a1",
                fontFamily: "monospace",
              }}
            >
              🌐 {domain}
            </div>
          </div>

          {/* Right: Category Pill + Scene Tracker + Source Tag */}
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div
              style={{
                background: "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                border: "1px solid #cbd5e1",
                color: "#334155",
                fontSize: 11,
                fontWeight: 800,
                padding: "4px 12px",
                borderRadius: 100,
                textTransform: "uppercase",
              }}
            >
              {category}
            </div>
            <div
              style={{
                background: "rgba(30, 41, 59, 0.06)",
                color: "#0f172a",
                fontSize: 11,
                fontWeight: 800,
                padding: "4px 10px",
                borderRadius: 6,
              }}
            >
              अंक {currentActIndex} / {totalActs}
            </div>
            <div
              style={{
                background: "rgba(2, 132, 199, 0.1)",
                border: "1px solid rgba(2, 132, 199, 0.3)",
                color: "#0369a1",
                fontSize: 11,
                fontWeight: 800,
                padding: "4px 12px",
                borderRadius: 100,
                display: "flex",
                alignItems: "center",
                gap: 5,
              }}
            >
              <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#0284c7" }} />
              🏛️ शासकीय स्रोत व प्रमाण
            </div>
          </div>
        </div>

        {/* Section Heading Banner */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            margin: "12px 0 6px 0",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span
              style={{
                background: "linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%)",
                color: "#ffffff",
                fontSize: 12,
                fontWeight: 800,
                padding: "5px 14px",
                borderRadius: 8,
                letterSpacing: 0.5,
              }}
            >
              अंतिम सारांश व सत्यापन
            </span>
            <h2
              style={{
                fontSize: 26,
                fontWeight: 900,
                color: "#0f172a",
                letterSpacing: -0.5,
                margin: 0,
              }}
            >
              आधिकारिक स्रोत, राजपत्र परिपत्र व नागरिक सहायता निर्देश
            </h2>
          </div>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b" }}>
            तथ्य सत्यापन माह: <strong style={{ color: "#0284c7" }}>{verifiedDate}</strong>
          </div>
        </div>

        {/* 4-Card Balanced 2x2 Grid (Filling 1808px x ~690px) */}
        <div
          style={{
            flex: 1,
            maxHeight: 690,
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gridTemplateRows: "1fr 1fr",
            gap: 16,
          }}
        >
          {/* Card 1: Official Gazette & Ministry Circular Evidence */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(240, 249, 255, 0.94) 100%)",
              border: "1.5px solid rgba(2, 132, 199, 0.35)",
              borderRadius: 20,
              padding: "22px 26px",
              boxShadow: "0 10px 30px rgba(2, 132, 199, 0.08)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              transform: `scale(${card1Spring})`,
              opacity: card1Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <div
                    style={{
                      width: 28,
                      height: 28,
                      borderRadius: 6,
                      background: "#e0f2fe",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 14,
                    }}
                  >
                    📜
                  </div>
                  <span style={{ fontSize: 13, fontWeight: 800, color: "#0369a1", textTransform: "uppercase" }}>
                    शासकीय राजपत्र प्रमाण
                  </span>
                </div>
                <span style={{ fontSize: 11, fontWeight: 700, color: "#059669", background: "#d1fae5", padding: "3px 10px", borderRadius: 100 }}>
                  ✓ अभिलेख प्रमाणित
                </span>
              </div>

              <div style={{ fontSize: 18, fontWeight: 800, color: "#0f172a", lineHeight: 1.4, marginBottom: 12 }}>
                {citationText}
              </div>

              {/* Notification Reference Box */}
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.92)",
                  border: "1px solid rgba(2, 132, 199, 0.2)",
                  borderRadius: 10,
                  padding: "10px 14px",
                }}
              >
                <div style={{ fontSize: 10, fontWeight: 800, color: "#64748b", textTransform: "uppercase" }}>
                  अधिसूचना / परिपत्र संदर्भ संख्या
                </div>
                <div
                  style={{
                    fontSize: 14,
                    fontWeight: 800,
                    color: "#1d4ed8",
                    marginTop: 2,
                    fontFamily: "monospace",
                    letterSpacing: 0.5,
                  }}
                >
                  {notifRef}
                </div>
              </div>
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                fontSize: 12,
                fontWeight: 700,
                color: "#059669",
                background: "rgba(16, 185, 129, 0.08)",
                padding: "8px 12px",
                borderRadius: 8,
              }}
            >
              <span>🏛️</span>
              <span>केवल भारत सरकार के .gov.in या .nic.in डोमेन से ही नियमों की पुष्टि करें।</span>
            </div>
          </div>

          {/* Card 2: Dedicated DastawezMediaCard (Govt Authority / Portal Visual) */}
          <div
            style={{
              borderRadius: 20,
              overflow: "hidden",
              boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
              transform: `scale(${card2Spring})`,
              opacity: card2Spring,
            }}
          >
            <DastawezMediaCard
              imagePath={officialImagePath || visualMedia?.official_image_path}
              videoPath={brollVideoPath || visualMedia?.broll_video_path}
              title={officialImageTitle || visualMedia?.official_image_title || "संसद व केंद्रीय मंत्रालय सार्वजनिक संदर्भ"}
              attribution={attribution || visualMedia?.attribution || "सार्वजनिक शासकीय अभिलेख"}
              badgeLabel="🏛️ अधिकृत संदर्भ"
              style={{
                width: "100%",
                height: "100%",
                borderRadius: 20,
              }}
              fallbackIcon="🏛️"
              fallbackTitle="भारत सरकार आधिकारिक पोर्टल अभिलेख"
            />
          </div>

          {/* Card 3: 3-Point Citizen Self-Verification Checklist */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.94) 100%)",
              border: "1.5px solid rgba(226, 232, 240, 0.9)",
              borderRadius: 20,
              padding: "20px 24px",
              boxShadow: "0 10px 30px rgba(15, 23, 42, 0.04)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              transform: `scale(${card3Spring})`,
              opacity: card3Spring,
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
              <div
                style={{
                  width: 28,
                  height: 28,
                  borderRadius: 6,
                  background: "#e0f2fe",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 14,
                }}
              >
                🔍
              </div>
              <span style={{ fontSize: 13, fontWeight: 800, color: "#0f172a", textTransform: "uppercase" }}>
                3-बिंदु नागरिक स्व-सत्यापन मार्गदर्शिका
              </span>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {/* Point 1 */}
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 10,
                  background: "rgba(255, 255, 255, 0.8)",
                  border: "1px solid rgba(226, 232, 240, 0.8)",
                  borderRadius: 10,
                  padding: "8px 12px",
                }}
              >
                <span style={{ color: "#0284c7", fontWeight: 900, fontSize: 14 }}>1.</span>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#1e293b", lineHeight: 1.35 }}>
                  <strong>आधिकारिक पोर्टल:</strong> केवल <code>https://{domain}</code> पर जाकर मूल परिपत्र व नियम डाउनलोड करें।
                </div>
              </div>

              {/* Point 2 */}
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 10,
                  background: "rgba(255, 255, 255, 0.8)",
                  border: "1px solid rgba(226, 232, 240, 0.8)",
                  borderRadius: 10,
                  padding: "8px 12px",
                }}
              >
                <span style={{ color: "#0284c7", fontWeight: 900, fontSize: 14 }}>2.</span>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#1e293b", lineHeight: 1.35 }}>
                  <strong>टोल-फ्री हेल्पलाइन:</strong> किसी भी समस्या पर सीधे <code>{helplineNumber}</code> पर संपर्क करें।
                </div>
              </div>

              {/* Point 3 */}
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 10,
                  background: "rgba(255, 255, 255, 0.8)",
                  border: "1px solid rgba(226, 232, 240, 0.8)",
                  borderRadius: 10,
                  padding: "8px 12px",
                }}
              >
                <span style={{ color: "#0284c7", fontWeight: 900, fontSize: 14 }}>3.</span>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#1e293b", lineHeight: 1.35 }}>
                  <strong>अधिकृत केंद्र:</strong> ग्राम पंचायत या कॉमन सर्विस सेंटर (CSC) से ही ई-केवाईसी व आवेदन रसीद लें।
                </div>
              </div>
            </div>

            <div style={{ fontSize: 11, color: "#64748b", fontWeight: 600 }}>
              🛡️ किसी भी अनाधिकृत व्हाट्सएप या टेलीग्राम लिंक पर अपनी निजी जानकारी साझा न करें।
            </div>
          </div>

          {/* Card 4: Branded Subscribe CTA Card (@iDastawez) */}
          <div
            style={{
              background: "linear-gradient(145deg, rgba(255, 255, 255, 0.98) 0%, rgba(254, 242, 242, 0.94) 100%)",
              border: "1.5px solid rgba(254, 202, 202, 0.8)",
              borderRadius: 20,
              padding: "20px 24px",
              boxShadow: "0 10px 30px rgba(220, 38, 38, 0.05)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              transform: `scale(${card4Spring})`,
              opacity: card4Spring,
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: 10,
                      background: "linear-gradient(135deg, #1d4ed8 0%, #0284c7 100%)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: 900,
                      fontSize: 16,
                      color: "#ffffff",
                    }}
                  >
                    iD
                  </div>
                  <div>
                    <div style={{ fontSize: 18, fontWeight: 900, color: "#0f172a" }}>
                      @iDastawez
                    </div>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b" }}>
                      सच्ची और निष्पक्ष नागरिक जानकारी
                    </div>
                  </div>
                </div>
                <div
                  style={{
                    background: "#fee2e2",
                    color: "#dc2626",
                    fontSize: 11,
                    fontWeight: 800,
                    padding: "3px 8px",
                    borderRadius: 6,
                  }}
                >
                  YouTube
                </div>
              </div>

              {/* YouTube Subscribe Mock Button */}
              <div
                style={{
                  background: "#dc2626",
                  color: "#ffffff",
                  borderRadius: 12,
                  padding: "11px 18px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 10,
                  fontSize: 15,
                  fontWeight: 900,
                  boxShadow: "0 6px 20px rgba(220, 38, 38, 0.3)",
                }}
              >
                <span>🔔</span> अभी SUBSCRIBE करें
              </div>

              <div style={{ fontSize: 12, color: "#475569", fontWeight: 600, lineHeight: 1.45, marginTop: 10 }}>
                सरकारी योजनाओं, नए परिपत्रों और नागरिक अधिकारों की निष्पक्ष व सरल जानकारी के लिए चैनल को सब्सक्राइब करें।
              </div>
            </div>

            <div style={{ fontSize: 10, color: "#94a3b8", fontWeight: 600, lineHeight: 1.3 }}>
              अस्वीकरण: iDastawez एक निष्पक्ष नागरिक सूचना मंच है जो सरकारी पोर्टलों पर उपलब्ध सार्वजनिक नियमों को सरल भाषा में प्रस्तुत करता है।
            </div>
          </div>
        </div>

        {/* Full-Width Bottom Official Portal & Jai Hind Directive Bar */}
        <div
          style={{
            background: "rgba(255, 255, 255, 0.95)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
            border: "1px solid rgba(226, 232, 240, 0.9)",
            borderRadius: 12,
            padding: "9px 20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 4px 14px rgba(15, 23, 42, 0.04)",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 15 }}>🌐</span>
            <span style={{ fontSize: 13, fontWeight: 800, color: "#0369a1" }}>
              आधिकारिक पोर्टल लिंक: https://{domain}
            </span>
          </div>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#64748b" }}>
            🛡️ सार्वजनिक जनहित में जारी — किसी अनधिकृत एजेंट को शुल्क न दें
          </div>
          <span style={{ fontSize: 13, fontWeight: 900, color: "#059669" }}>
            धन्यवाद, जय हिन्द! 🇮🇳
          </span>
        </div>
      </div>
    </div>
  );
};
