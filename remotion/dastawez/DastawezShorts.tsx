import React from "react";
import {
  Audio,
  Video,
  Img,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { Phrase, WordTiming } from "./types";
import { resolveMediaSrc } from "./DastawezShow";

export interface DastawezShortsProps {
  title?: string;
  badge_text?: string;
  badge_bg_color?: string;
  badge_border_color?: string;
  headline?: string;
  portal_domain?: string;
  ministry?: string;
  audio_path?: string;
  duration_seconds?: number;
  phrases?: Phrase[];
  broll_video_path?: string;
  official_image_path?: string;
}

export const DastawezShorts: React.FC<DastawezShortsProps> = ({
  title = "सरकारी योजना नया नियम 2026",
  badge_text = "SARKARI ALERT // OFFICIAL UPDATE",
  badge_bg_color = "rgba(225, 29, 72, 0.92)",
  badge_border_color = "rgba(255, 120, 150, 0.9)",
  headline = "राशन कार्ड e-KYC नया नियम 2026",
  portal_domain = "nfsa.gov.in",
  ministry = "उपभोक्ता मामले एवं खाद्य विभाग",
  audio_path,
  duration_seconds = 40,
  phrases = [],
  broll_video_path,
  official_image_path,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentTime = frame / fps;

  const resolvedAudio = resolveMediaSrc(audio_path);
  const resolvedBroll = resolveMediaSrc(broll_video_path);
  const resolvedImg = resolveMediaSrc(official_image_path);

  // Slow Ken Burns zoom across timeline
  const zoom = interpolate(frame, [0, durationInFrames], [1.0, 1.08], {
    extrapolateRight: "clamp",
  });

  // Entrance spring for top UI cards
  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120 },
  });

  // Active phrase finder for word-by-word subtitles
  const activePhrase = phrases.find(
    (p) => p.start <= currentTime && currentTime <= p.end + 0.08
  );

  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        background: "#0b1120",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif",
      }}
    >
      {/* 1. Fullscreen B-Roll Video / Image with continuous zoom */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `scale(${zoom})`,
          transformOrigin: "center center",
        }}
      >
        {resolvedBroll ? (
          <Video
            src={resolvedBroll}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
            loop
          />
        ) : resolvedImg ? (
          <Img
            src={resolvedImg}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              background: "radial-gradient(ellipse at 50% 30%, #1e293b 0%, #0f172a 60%, #020617 100%)",
            }}
          />
        )}
      </div>

      {/* 2. Dark Cinematic Vignette & Readability Gradient */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(180deg, rgba(11, 17, 32, 0.78) 0%, rgba(11, 17, 32, 0.35) 40%, rgba(11, 17, 32, 0.65) 75%, rgba(11, 17, 32, 0.95) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 3. Top Alert Category Pill */}
      <div
        style={{
          position: "absolute",
          top: 110,
          left: 60,
          transform: `translateY(${(1 - enterSpring) * -30}px)`,
          opacity: enterSpring,
          display: "flex",
          alignItems: "center",
          gap: 12,
          background: badge_bg_color,
          border: `2px solid ${badge_border_color}`,
          borderRadius: 20,
          padding: "10px 24px",
          boxShadow: "0 8px 24px rgba(225, 29, 72, 0.35)",
        }}
      >
        <div
          style={{
            width: 12,
            height: 12,
            borderRadius: "50%",
            background: "#ffffff",
            boxShadow: "0 0 10px #ffffff",
          }}
        />
        <span
          style={{
            fontSize: 26,
            fontWeight: 900,
            color: "#ffffff",
            letterSpacing: 1.2,
            textTransform: "uppercase",
          }}
        >
          {badge_text.replace(/^[●•\s]+/, "")}
        </span>
      </div>

      {/* 4. Glassmorphic Headline & Verification Card */}
      <div
        style={{
          position: "absolute",
          top: 185,
          left: 60,
          right: 60,
          transform: `translateY(${(1 - enterSpring) * -20}px)`,
          opacity: enterSpring,
          background: "rgba(15, 23, 42, 0.88)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: "2px solid rgba(56, 189, 248, 0.5)",
          borderRadius: 28,
          padding: "26px 32px",
          boxShadow: "0 18px 45px rgba(0, 0, 0, 0.45)",
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        <div
          style={{
            fontSize: 42,
            fontWeight: 900,
            color: "#ffffff",
            lineHeight: 1.25,
            textShadow: "0 2px 8px rgba(0, 0, 0, 0.6)",
          }}
        >
          {headline}
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10,
            fontSize: 22,
            color: "#93c5fd",
            fontWeight: 700,
          }}
        >
          <span style={{ color: "#38bdf8" }}>🏛️ {ministry}</span>
          <span style={{ opacity: 0.6 }}>•</span>
          <span style={{ color: "#facc15" }}>🌐 {portal_domain}</span>
        </div>
      </div>

      {/* 5. Word-by-Word Bouncing Highlight Captions (Center/Lower Safe Area) */}
      {activePhrase && activePhrase.words && (
        <div
          style={{
            position: "absolute",
            top: 1140,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            pointerEvents: "none",
            zIndex: 90,
          }}
        >
          <div
            style={{
              background: "rgba(10, 15, 26, 0.88)",
              backdropFilter: "blur(18px)",
              WebkitBackdropFilter: "blur(18px)",
              border: "2px solid rgba(250, 204, 21, 0.7)",
              borderRadius: 24,
              padding: "16px 36px",
              display: "flex",
              flexWrap: "wrap",
              gap: 14,
              justifyContent: "center",
              alignItems: "center",
              maxWidth: 960,
              boxShadow: "0 14px 40px rgba(0, 0, 0, 0.6)",
            }}
          >
            {activePhrase.words.map((w, idx) => {
              const isSpoken = w.start <= currentTime && currentTime <= w.end + 0.08;
              const color = isSpoken ? "#facc15" : "#ffffff";
              const scale = isSpoken ? 1.15 : 1.0;
              const weight = isSpoken ? 900 : 700;
              const textShadow = isSpoken
                ? "0 0 16px rgba(250, 204, 21, 0.6)"
                : "0 2px 4px rgba(0, 0, 0, 0.8)";

              return (
                <span
                  key={idx}
                  style={{
                    fontSize: 48,
                    fontWeight: weight,
                    color,
                    textShadow,
                    transform: `scale(${scale})`,
                    display: "inline-block",
                    transition: "all 0.06s ease-out",
                  }}
                >
                  {w.word}
                </span>
              );
            })}
          </div>
        </div>
      )}

      {/* 6. Subtle Channel Branding (Bottom Safe Zone) */}
      <div
        style={{
          position: "absolute",
          bottom: 120,
          left: 60,
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: "rgba(15, 23, 42, 0.85)",
          border: "1px solid rgba(56, 189, 248, 0.4)",
          borderRadius: 16,
          padding: "8px 20px",
        }}
      >
        <div
          style={{
            width: 10,
            height: 10,
            borderRadius: "50%",
            background: "#ef4444",
            boxShadow: "0 0 8px #ef4444",
          }}
        />
        <span
          style={{
            fontSize: 22,
            fontWeight: 800,
            color: "#ffffff",
            letterSpacing: 0.8,
          }}
        >
          @iDastawez
        </span>
      </div>

      {/* Audio Element */}
      {resolvedAudio && <Audio src={resolvedAudio} volume={1.0} />}
    </div>
  );
};
