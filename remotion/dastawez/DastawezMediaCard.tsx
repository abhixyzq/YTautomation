import React from "react";
import { Img, OffthreadVideo } from "remotion";
import { resolveMediaSrc } from "./DastawezShow";

interface DastawezMediaCardProps {
  imagePath?: string;
  videoPath?: string;
  title?: string;
  attribution?: string;
  badgeLabel?: string;
  mediaType?: "image" | "video";
  style?: React.CSSProperties;
  fallbackIcon?: string;
  fallbackTitle?: string;
}

export const DastawezMediaCard: React.FC<DastawezMediaCardProps> = ({
  imagePath,
  videoPath,
  title = "आधिकारिक नागरिक सूचना रिकॉर्ड",
  attribution = "सार्वजनिक स्रोत / अधिकृत पोर्टल",
  badgeLabel = "🏛 आधिकारिक विजुअल",
  mediaType = "image",
  style = {},
  fallbackIcon = "🏛",
  fallbackTitle = "भारत सरकार आधिकारिक पोर्टल अभिलेख",
}) => {
  const resolvedImg = resolveMediaSrc(imagePath);
  const resolvedVideo = resolveMediaSrc(videoPath);

  const hasVideo = Boolean(resolvedVideo);
  const hasImage = Boolean(resolvedImg);

  // Determine whether to play video or show image
  const showVideo = (mediaType === "video" && hasVideo) || (hasVideo && !hasImage);

  return (
    <div
      style={{
        position: "relative",
        borderRadius: 20,
        overflow: "hidden",
        border: "1.5px solid rgba(2, 132, 199, 0.35)",
        boxShadow: "0 16px 36px rgba(15, 23, 42, 0.1), 0 4px 12px rgba(2, 132, 199, 0.08)",
        background: "linear-gradient(135deg, rgba(241, 245, 249, 0.95), rgba(224, 242, 254, 0.8))",
        display: "flex",
        flexDirection: "column",
        ...style,
      }}
    >
      {/* Top Floating Badge */}
      <div
        style={{
          position: "absolute",
          top: 12,
          left: 14,
          zIndex: 10,
          background: "rgba(15, 23, 42, 0.94)",
          color: "#ffffff",
          fontSize: 12,
          fontWeight: 800,
          padding: "4px 12px",
          borderRadius: 20,
          border: "1px solid rgba(255, 255, 255, 0.2)",
          display: "flex",
          alignItems: "center",
          gap: 6,
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.2)",
        }}
      >
        <span>{showVideo ? "🎥" : "📸"}</span>
        <span>{badgeLabel}</span>
      </div>

      {/* Main Visual Display */}
      <div style={{ flex: 1, width: "100%", position: "relative", overflow: "hidden" }}>
        {showVideo ? (
          <OffthreadVideo
            src={resolvedVideo!}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : hasImage ? (
          <Img
            src={resolvedImg!}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          /* High-Tech Fallback Vector Graphic Frame */
          <div
            style={{
              width: "100%",
              height: "100%",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              background: "radial-gradient(ellipse at 50% 40%, #e0f2fe 0%, #f1f5f9 100%)",
              padding: 24,
              boxSizing: "border-box",
              textAlign: "center",
            }}
          >
            <div
              style={{
                width: 64,
                height: 64,
                borderRadius: 18,
                background: "linear-gradient(135deg, #1d4ed8, #0284c7)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 32,
                color: "#ffffff",
                marginBottom: 12,
                boxShadow: "0 8px 20px rgba(2, 132, 199, 0.25)",
              }}
            >
              {fallbackIcon}
            </div>
            <div style={{ fontSize: 16, fontWeight: 800, color: "#0f172a", maxWidth: 280 }}>
              {fallbackTitle}
            </div>
            <div style={{ fontSize: 13, color: "#64748b", marginTop: 4 }}>
              राष्ट्रीय सूचना विज्ञान केंद्र (NIC) / Gov.in नेटवर्क
            </div>
          </div>
        )}
      </div>

      {/* Bottom Integrated Frosted Glass Caption Bar */}
      <div
        style={{
          background: "#ffffff",
          borderTop: "1px solid rgba(2, 132, 199, 0.2)",
          padding: "8px 16px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 5,
        }}
      >
        <div
          style={{
            fontSize: 12,
            fontWeight: 800,
            color: "#0f172a",
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
            maxWidth: 320,
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 11,
            color: "#0284c7",
            fontWeight: 700,
            background: "rgba(2, 132, 199, 0.08)",
            padding: "2px 8px",
            borderRadius: 6,
            whiteSpace: "nowrap",
          }}
        >
          {attribution}
        </div>
      </div>
    </div>
  );
};
