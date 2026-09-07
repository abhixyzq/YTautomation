import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { EvidenceMetadata, SceneVisualMedia } from "./types";
import { DastawezMediaCard } from "./DastawezMediaCard";

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
  benefitHighlight,
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

  // Subtle broadcast camera creep
  const cameraScale = interpolate(frame, [0, 900], [1.0, 1.02], {
    extrapolateRight: "clamp",
  });

  const beat1Spring = spring({ frame, fps, delay: 2, config: { damping: 14, stiffness: 110 } });
  const beat2Spring = spring({ frame, fps, delay: 15, config: { damping: 14, stiffness: 95 } });
  const beat3Spring = spring({ frame, fps, delay: 28, config: { damping: 14, stiffness: 95 } });

  const domain =
    officialPortalDomain ||
    (portalUrl ? portalUrl.replace("https://", "").replace("http://", "").split("/")[0] : "gov.in");

  const imgPath = visualMedia?.official_image_path || officialImagePath;
  const imgTitle = visualMedia?.official_image_title || officialImageTitle;
  const vidPath = visualMedia?.broll_video_path || brollVideoPath;
  const mediaAttr = visualMedia?.attribution || attribution;

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      }}
    >
      {/* Full-Screen Content Container (Smart Space Utilization: Top 36px to Bottom 96px) */}
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
        {/* Sleek Integrated Top Meta-Bar (Replaces bulky navbar) */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            transform: `translateY(${(1 - beat1Spring) * -14}px)`,
            opacity: beat1Spring,
          }}
        >
          {/* Left: Brand Monogram + Portal Domain + Urgency Badge */}
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                background: "rgba(255, 255, 255, 0.94)",
                padding: "6px 14px",
                borderRadius: 12,
                border: "1px solid rgba(2, 132, 199, 0.25)",
                boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
              }}
            >
              <div
                style={{
                  width: 24,
                  height: 24,
                  borderRadius: 6,
                  background: "linear-gradient(135deg, #ea580c, #f97316)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#fff",
                  fontWeight: 900,
                  fontSize: 13,
                }}
              >
                द
              </div>
              <span style={{ fontSize: 15, fontWeight: 900, color: "#0f172a" }}>@iDastawez</span>
            </div>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
                background: "rgba(238, 242, 255, 0.95)",
                border: "1px solid rgba(99, 102, 241, 0.3)",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
                color: "#3730a3",
              }}
            >
              <span>🏛️</span>
              <span>{domain}</span>
            </div>

            <div
              style={{
                background: "linear-gradient(135deg, #ea580c, #f97316)",
                color: "#ffffff",
                padding: "6px 14px",
                borderRadius: 12,
                fontSize: 13,
                fontWeight: 800,
                boxShadow: "0 2px 8px rgba(234, 88, 12, 0.3)",
              }}
            >
              🚨 {urgencyBadge || "ताज़ा सरकारी अधिसूचना 2026"}
            </div>

            {ministry && (
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.9)",
                  border: "1px solid rgba(2, 132, 199, 0.2)",
                  padding: "6px 14px",
                  borderRadius: 12,
                  fontSize: 13,
                  fontWeight: 700,
                  color: "#0369a1",
                }}
              >
                {ministry}
              </div>
            )}
          </div>

          {/* Right: Step Indicator */}
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              background: "rgba(255, 255, 255, 0.94)",
              padding: "6px 16px",
              borderRadius: 12,
              border: "1px solid rgba(2, 132, 199, 0.2)",
              boxShadow: "0 4px 12px rgba(15, 23, 42, 0.05)",
            }}
          >
            <span style={{ fontSize: 13, fontWeight: 900, color: "#0284c7" }}>
              भाग {currentActIndex}/{totalActs}
            </span>
            <span style={{ fontSize: 12, color: "#94a3b8" }}>•</span>
            <span style={{ fontSize: 13, fontWeight: 700, color: "#334155" }}>
              अधिसूचना एवं मुख्य बिंदु
            </span>
          </div>
        </div>

        {/* Master Scheme Title (Clear, Punchy, Full Width) */}
        <div
          style={{
            marginTop: 10,
            marginBottom: 10,
            transform: `translateY(${(1 - beat1Spring) * 12}px)`,
            opacity: beat1Spring,
          }}
        >
          <h1
            style={{
              fontSize: 44,
              fontWeight: 900,
              lineHeight: 1.2,
              color: "#0f172a",
              margin: 0,
              letterSpacing: "-0.5px",
            }}
          >
            {schemeName}
          </h1>
        </div>

        {/* 4-Card High-Density Broadcast Grid (Utilizing Full Canvas Width & Height) */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1.2fr 1fr 1fr 1.15fr",
            gap: 20,
            flex: 1,
            maxHeight: 570,
            transform: `translateY(${(1 - beat2Spring) * 16}px)`,
            opacity: beat2Spring,
          }}
        >
          {/* Card 1: Primary Benefit & Financial Aid Card (Luminous Emerald) */}
          <div
            style={{
              background: "linear-gradient(150deg, rgba(255, 255, 255, 0.96) 0%, rgba(240, 253, 244, 0.94) 100%)",
              border: "2px solid rgba(16, 185, 129, 0.5)",
              borderRadius: 22,
              padding: "24px 26px",
              boxShadow: "0 18px 40px rgba(15, 23, 42, 0.08), 0 0 16px rgba(16, 185, 129, 0.12)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  background: "rgba(16, 185, 129, 0.15)",
                  color: "#059669",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                  textTransform: "uppercase",
                }}
              >
                <span>💰</span>
                <span>निर्धारित लाभ / आर्थिक सहायता</span>
              </div>

              <div
                style={{
                  fontSize: 34,
                  fontWeight: 900,
                  color: "#064e3b",
                  lineHeight: 1.25,
                  marginTop: 14,
                  letterSpacing: -0.5,
                }}
              >
                {benefitHighlight || "सीधा लाभ बैंक खाते में (DBT Transfer)"}
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              <div
                style={{
                  background: "rgba(255, 255, 255, 0.9)",
                  border: "1px solid rgba(16, 185, 129, 0.3)",
                  padding: "8px 12px",
                  borderRadius: 10,
                  fontSize: 13,
                  fontWeight: 700,
                  color: "#047857",
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <span>⚡</span>
                <span>100% सरकारी सब्सिडी | कोई बिचौलिया नहीं</span>
              </div>
              <div
                style={{
                  background: "rgba(238, 242, 255, 0.9)",
                  border: "1px solid rgba(99, 102, 241, 0.25)",
                  padding: "8px 12px",
                  borderRadius: 10,
                  fontSize: 12,
                  fontWeight: 700,
                  color: "#3730a3",
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                }}
              >
                <span>🏦</span>
                <span>Aadhaar Seeding / NPCI डायरेक्ट क्रेडिट</span>
              </div>
            </div>
          </div>

          {/* Card 2: Official Gazette Directive & Rule Change Card */}
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              border: "1.5px solid rgba(2, 132, 199, 0.3)",
              borderRadius: 22,
              padding: "24px 24px",
              boxShadow: "0 14px 34px rgba(15, 23, 42, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  background: "rgba(2, 132, 199, 0.12)",
                  color: "#0284c7",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>📑</span>
                <span>नवीनतम सरकारी निर्देश 2026</span>
              </div>

              <div
                style={{
                  fontSize: 20,
                  fontWeight: 800,
                  color: "#1e293b",
                  lineHeight: 1.45,
                  marginTop: 14,
                }}
              >
                {latestUpdate || "योजना के नियमों में ताजा संशोधन जारी किया गया है।"}
              </div>
            </div>

            <div
              style={{
                background: "rgba(248, 250, 252, 0.95)",
                border: "1px solid rgba(203, 213, 225, 0.8)",
                padding: "10px 14px",
                borderRadius: 10,
                fontSize: 12,
                color: "#475569",
                fontWeight: 600,
              }}
            >
              <div style={{ fontWeight: 800, color: "#0f172a" }}>राजपत्र संदर्भ:</div>
              <div>{evidence?.notification_ref || "GOI-PUBLIC-NOTIF-2026"}</div>
            </div>
          </div>

          {/* Card 3: Target Beneficiaries & Scope Card */}
          <div
            style={{
              background: "rgba(255, 255, 255, 0.95)",
              border: "1.5px solid rgba(14, 165, 233, 0.3)",
              borderRadius: 22,
              padding: "24px 24px",
              boxShadow: "0 14px 34px rgba(15, 23, 42, 0.06)",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
            }}
          >
            <div>
              <div
                style={{
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  background: "rgba(249, 115, 22, 0.12)",
                  color: "#c2410c",
                  padding: "4px 12px",
                  borderRadius: 8,
                  fontSize: 12,
                  fontWeight: 900,
                  letterSpacing: 0.5,
                }}
              >
                <span>👥</span>
                <span>लक्षित लाभार्थी एवं क्षेत्र</span>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10, marginTop: 14 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ color: "#059669", fontWeight: 900 }}>✓</span>
                  <span style={{ fontSize: 16, fontWeight: 700, color: "#1e293b" }}>
                    पात्र परिवार एवं व्यक्तिगत कार्डधारक
                  </span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ color: "#059669", fontWeight: 900 }}>✓</span>
                  <span style={{ fontSize: 16, fontWeight: 700, color: "#1e293b" }}>
                    सभी राज्यों एवं केंद्र शासित प्रदेशों में प्रभावी
                  </span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <span style={{ color: "#059669", fontWeight: 900 }}>✓</span>
                  <span style={{ fontSize: 16, fontWeight: 700, color: "#1e293b" }}>
                    समयबद्ध सत्यापन प्रक्रिया अनिवार्य
                  </span>
                </div>
              </div>
            </div>

            <div
              style={{
                background: "#eff6ff",
                border: "1px solid #bfdbfe",
                padding: "8px 12px",
                borderRadius: 10,
                fontSize: 12,
                fontWeight: 700,
                color: "#1d4ed8",
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <span>🔒</span>
              <span>अधिकृत पहचान पत्र द्वारा सत्यापन</span>
            </div>
          </div>

          {/* Card 4: Dedicated Visual Media Card (Authentic Photo / Looping Video Frame) */}
          <DastawezMediaCard
            imagePath={imgPath}
            videoPath={vidPath}
            title={imgTitle || "आधिकारिक प्रशासनिक संदर्भ"}
            attribution={mediaAttr || "Wikimedia / Govt Source"}
            badgeLabel="🏛 आधिकारिक संदर्भ दृश्य"
            mediaType="image"
            style={{
              height: "100%",
            }}
            fallbackIcon="🏛️"
            fallbackTitle="भारत सरकार आधिकारिक पोर्टल अभिलेख"
          />
        </div>

        {/* Bottom Full-Width Action Directive Strip */}
        <div
          style={{
            marginTop: 14,
            background: "rgba(255, 255, 255, 0.94)",
            backdropFilter: "blur(16px)",
            border: "1.5px solid rgba(2, 132, 199, 0.25)",
            borderRadius: 16,
            padding: "12px 24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 8px 24px rgba(15, 23, 42, 0.05)",
            transform: `translateY(${(1 - beat3Spring) * 10}px)`,
            opacity: beat3Spring,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <span style={{ fontSize: 18 }}>💡</span>
            <span style={{ fontSize: 15, fontWeight: 800, color: "#0f172a" }}>
              नागरिक सहायता निर्देश: योजना की पूर्ण जानकारी व ऑनलाइन आवेदन केवल आधिकारिक पोर्टल{" "}
              <span style={{ color: "#0284c7", fontWeight: 900 }}>https://{domain}</span> से ही करें।
            </span>
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              background: "rgba(16, 185, 129, 0.12)",
              border: "1px solid rgba(16, 185, 129, 0.4)",
              padding: "4px 12px",
              borderRadius: 8,
              fontSize: 12,
              fontWeight: 800,
              color: "#047857",
            }}
          >
            <span>✓</span>
            <span>100% निःशुल्क सेवा</span>
          </div>
        </div>
      </div>
    </div>
  );
};
