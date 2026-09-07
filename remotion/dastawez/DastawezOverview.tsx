import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig, Img, Video } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezTopHud } from "./DastawezTopHud";
import { resolveMediaSrc } from "./DastawezShow";

interface DastawezOverviewProps {
  schemeName: string;
  ministry?: string;
  benefitHighlight?: string;
  latestUpdate?: string;
  portalUrl?: string;
  officialPortalDomain?: string;
  urgencyBadge?: string;
  category?: string;
  evidence?: EvidenceMetadata;
  officialImagePath?: string;
  officialImageTitle?: string;
  attribution?: string;
  brollVideoPath?: string;
  visualMedia?: SceneVisualMedia;
  currentActIndex?: number;
  totalActs?: number;
}

export const DastawezOverview: React.FC<DastawezOverviewProps> = ({
  schemeName,
  ministry,
  benefitHighlight = "सरकारी सहायता एवं लाभ",
  latestUpdate,
  portalUrl,
  officialPortalDomain,
  urgencyBadge,
  category,
  evidence,
  officialImagePath,
  officialImageTitle,
  attribution,
  brollVideoPath,
  visualMedia,
  currentActIndex = 1,
  totalActs = 6,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "india.gov.in");

  const hudSpring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 120 } });
  const cardSpring = spring({ frame, fps, delay: 10, config: { damping: 12, stiffness: 100 } });
  const mediaSpring = spring({ frame, fps, delay: 18, config: { damping: 13, stiffness: 100 } });

  const resolvedImg = resolveMediaSrc(visualMedia?.official_image_path || officialImagePath);
  const resolvedVid = resolveMediaSrc(visualMedia?.broll_video_path || brollVideoPath);
  const imgTitle = visualMedia?.official_image_title || officialImageTitle || "आधिकारिक रिकॉर्ड";
  const mediaAttr = visualMedia?.attribution || attribution || "भारत सरकार (Public Domain)";

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
      {/* 1. Sleek Top Meta HUD Bar */}
      <div style={{ transform: `translateY(${(1 - hudSpring) * -20}px)`, opacity: hudSpring }}>
        <DastawezTopHud
          schemeName={schemeName}
          domain={domain}
          urgencyBadge={urgencyBadge}
          ministry={ministry}
          actIndex={currentActIndex}
          totalActs={totalActs}
          actTitle="योजना परिचय एवं मुख्य लाभ"
        />
      </div>

      {/* 2. Floating Center-HUD Grid (Left: Hero Benefit Card, Right: Official Visual Card) */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.25fr 1fr",
          gap: 36,
          alignItems: "center",
          flex: 1,
          marginTop: 20,
          marginBottom: 60,
        }}
      >
        {/* Left: Floating Hero Benefit Card */}
        <div
          style={{
            transform: `translateY(${(1 - cardSpring) * 30}px)`,
            opacity: cardSpring,
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid rgba(56, 189, 248, 0.4)",
            borderRadius: 28,
            padding: "36px 40px",
            boxShadow: "0 24px 60px rgba(0, 0, 0, 0.65), 0 0 30px rgba(56, 189, 248, 0.15)",
            display: "flex",
            flexDirection: "column",
            gap: 20,
          }}
        >
          {/* Tag Pill */}
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span
              style={{
                background: "rgba(16, 185, 129, 0.2)",
                border: "1.5px solid rgba(16, 185, 129, 0.6)",
                color: "#34d399",
                fontSize: 14,
                fontWeight: 900,
                padding: "6px 14px",
                borderRadius: 12,
                letterSpacing: 0.8,
                textTransform: "uppercase",
              }}
            >
              💰 मुख्य लाभ / सहायता राशि
            </span>
          </div>

          {/* Glowing Big Metric */}
          <div
            style={{
              fontSize: 54,
              fontWeight: 900,
              lineHeight: 1.1,
              background: "linear-gradient(135deg, #34d399 0%, #38bdf8 50%, #ffffff 100%)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              filter: "drop-shadow(0 4px 16px rgba(52, 211, 153, 0.35))",
            }}
          >
            {benefitHighlight}
          </div>

          {/* Scheme Name Banner */}
          <div
            style={{
              fontSize: 26,
              fontWeight: 800,
              color: "#f1f5f9",
              lineHeight: 1.35,
            }}
          >
            {schemeName}
          </div>

          {/* Action Chips */}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12, marginTop: 6 }}>
            <div
              style={{
                background: "rgba(30, 41, 59, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                padding: "8px 16px",
                borderRadius: 14,
                fontSize: 14,
                fontWeight: 700,
                color: "#93c5fd",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>🌐</span>
              <span>ऑनलाइन आवेदन प्रणाली</span>
            </div>
            <div
              style={{
                background: "rgba(30, 41, 59, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                padding: "8px 16px",
                borderRadius: 14,
                fontSize: 14,
                fontWeight: 700,
                color: "#86efac",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>✅</span>
              <span>100% निःशुल्क प्रक्रिया</span>
            </div>
            <div
              style={{
                background: "rgba(30, 41, 59, 0.8)",
                border: "1px solid rgba(255, 255, 255, 0.15)",
                padding: "8px 16px",
                borderRadius: 14,
                fontSize: 14,
                fontWeight: 700,
                color: "#fde047",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>⚠️</span>
              <span>दलालों से सावधान</span>
            </div>
          </div>
        </div>

        {/* Right: Floating Official Visual / Photo Card */}
        <div
          style={{
            transform: `translateY(${(1 - mediaSpring) * 30}px)`,
            opacity: mediaSpring,
            background: "rgba(11, 17, 32, 0.88)",
            backdropFilter: "blur(24px)",
            WebkitBackdropFilter: "blur(24px)",
            border: "2px solid rgba(99, 102, 241, 0.4)",
            borderRadius: 28,
            overflow: "hidden",
            boxShadow: "0 24px 60px rgba(0, 0, 0, 0.65)",
            height: 380,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* Media Header */}
          <div
            style={{
              padding: "12px 20px",
              background: "rgba(15, 23, 42, 0.9)",
              borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ fontSize: 16 }}>🏛️</span>
              <span style={{ fontSize: 13, fontWeight: 800, color: "#cbd5e1" }}>
                आधिकारिक सरकारी अभिलेख
              </span>
            </div>
            <span
              style={{
                fontSize: 11,
                fontWeight: 700,
                color: "#38bdf8",
                background: "rgba(56, 189, 248, 0.15)",
                padding: "3px 8px",
                borderRadius: 6,
              }}
            >
              सत्यापित
            </span>
          </div>

          {/* Media Body */}
          <div style={{ flex: 1, position: "relative", overflow: "hidden" }}>
            {resolvedImg ? (
              <Img
                src={resolvedImg}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            ) : resolvedVid ? (
              <Video
                src={resolvedVid}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
                loop
                muted
              />
            ) : (
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "radial-gradient(ellipse at 50% 50%, #1e293b, #0f172a)",
                  color: "#64748b",
                  fontSize: 16,
                  fontWeight: 700,
                }}
              >
                भारत सरकार आधिकारिक पोर्टल अभिलेख
              </div>
            )}
          </div>

          {/* Attribution Footer */}
          <div
            style={{
              padding: "10px 20px",
              background: "rgba(15, 23, 42, 0.95)",
              borderTop: "1px solid rgba(255, 255, 255, 0.08)",
              fontSize: 12,
              color: "#94a3b8",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", maxWidth: "70%" }}>
              {imgTitle}
            </span>
            <span style={{ color: "#64748b", fontSize: 11 }}>{mediaAttr}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
