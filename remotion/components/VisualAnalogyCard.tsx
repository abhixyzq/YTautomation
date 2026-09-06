import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface VisualAnalogyCardProps {
  analogyTitle?: string;
  conceptName?: string;
  conceptDesc?: string;
  analogyName?: string;
  analogyDesc?: string;
  takeaway?: string;
}

export const VisualAnalogyCard: React.FC<VisualAnalogyCardProps> = ({
  analogyTitle = "INTUITIVE ANALOGY // THE FIRST PRINCIPLE",
  conceptName = "QUANTUM SUPERPOSITION",
  conceptDesc = "A qubit exists in an infinite continuum of 0 and 1 simultaneously until an observer collapses the wave function.",
  analogyName = "A SPINNING COIN IN MID-AIR",
  analogyDesc = "While spinning in the air, the coin is neither Heads nor Tails—it is 100% of both possibilities until it hits the table.",
  takeaway = "Quantum power comes from calculating all possibilities during the spin, not after the landing.",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const entrance = spring({ frame, fps, config: { damping: 14, stiffness: 95 } });
  const pulse = 0.85 + Math.sin(frame / 10) * 0.15;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#050711",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "50px 80px 40px",
        overflow: "hidden",
        fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
      }}
    >
      {/* Background Gradients */}
      <div
        style={{
          position: "absolute",
          top: "-20%",
          left: "20%",
          width: "600px",
          height: "600px",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0, 240, 255, 0.08) 0%, transparent 60%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "-20%",
          right: "20%",
          width: "600px",
          height: "600px",
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, transparent 60%)",
        }}
      />

      {/* Header Banner */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${entrance})`,
          opacity: entrance,
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            fontWeight: 800,
            color: "#a855f7",
            letterSpacing: "2px",
            textTransform: "uppercase",
            marginBottom: 6,
            background: "rgba(168, 85, 247, 0.12)",
            padding: "4px 14px",
            borderRadius: "99px",
            border: "1px solid rgba(168, 85, 247, 0.3)",
          }}
        >
          {analogyTitle}
        </div>
        <div
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#ffffff",
            letterSpacing: "-0.5px",
            textTransform: "uppercase",
            textShadow: "0 4px 20px rgba(168, 85, 247, 0.3)",
          }}
        >
          THE PHYSICAL MENTAL MODEL
        </div>
      </div>

      {/* Center Split: Abstract vs Real-World Metaphor */}
      <div
        style={{
          display: "flex",
          alignItems: "stretch",
          justifyContent: "center",
          gap: 30,
          width: "100%",
          maxWidth: "1500px",
          position: "relative",
          zIndex: 2,
        }}
      >
        {/* Left Card: The Abstract Tech Concept */}
        <div
          style={{
            flex: 1,
            background: "rgba(10, 18, 36, 0.75)",
            backdropFilter: "blur(20px)",
            border: "2px solid rgba(0, 240, 255, 0.35)",
            borderRadius: "24px",
            padding: "36px 32px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: `0 0 ${25 * pulse}px rgba(0, 240, 255, 0.2), 0 20px 50px rgba(0,0,0,0.5)`,
            transform: `translateX(${(1 - entrance) * -40}px)`,
            opacity: entrance,
          }}
        >
          <div>
            <div
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 12,
                fontWeight: 800,
                color: "#00f0ff",
                letterSpacing: "1px",
                marginBottom: 10,
              }}
            >
              [ABSTRACT TECHNICAL MECHANISM]
            </div>
            <div
              style={{
                fontSize: 28,
                fontWeight: 800,
                color: "#ffffff",
                lineHeight: 1.2,
                marginBottom: 16,
              }}
            >
              {conceptName}
            </div>
            <div
              style={{
                fontSize: 16,
                fontWeight: 500,
                color: "#94a3b8",
                lineHeight: 1.6,
              }}
            >
              {conceptDesc}
            </div>
          </div>
          <div
            style={{
              marginTop: 20,
              paddingTop: 16,
              borderTop: "1px solid rgba(255,255,255,0.08)",
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 12,
              color: "#38bdf8",
            }}
          >
            <span>⚡ MATHEMATICAL PARADOX</span>
          </div>
        </div>

        {/* Center Equals Badge */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            position: "relative",
          }}
        >
          <div
            style={{
              width: "60px",
              height: "60px",
              borderRadius: "50%",
              background: "linear-gradient(135deg, #00f0ff, #a855f7)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "#050811",
              fontSize: 24,
              fontWeight: 900,
              boxShadow: "0 0 30px rgba(0, 240, 255, 0.5)",
              transform: `scale(${entrance})`,
            }}
          >
            ≈
          </div>
        </div>

        {/* Right Card: The Real-World Physical Analogy */}
        <div
          style={{
            flex: 1,
            background: "rgba(22, 12, 38, 0.75)",
            backdropFilter: "blur(20px)",
            border: "2px solid rgba(168, 85, 247, 0.45)",
            borderRadius: "24px",
            padding: "36px 32px",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            boxShadow: `0 0 ${25 * pulse}px rgba(168, 85, 247, 0.2), 0 20px 50px rgba(0,0,0,0.5)`,
            transform: `translateX(${(1 - entrance) * 40}px)`,
            opacity: entrance,
          }}
        >
          <div>
            <div
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 12,
                fontWeight: 800,
                color: "#c084fc",
                letterSpacing: "1px",
                marginBottom: 10,
              }}
            >
              [INTUITIVE PHYSICAL METAPHOR]
            </div>
            <div
              style={{
                fontSize: 28,
                fontWeight: 800,
                color: "#ffffff",
                lineHeight: 1.2,
                marginBottom: 16,
              }}
            >
              {analogyName}
            </div>
            <div
              style={{
                fontSize: 16,
                fontWeight: 500,
                color: "#cbd5e1",
                lineHeight: 1.6,
              }}
            >
              {analogyDesc}
            </div>
          </div>
          <div
            style={{
              marginTop: 20,
              paddingTop: 16,
              borderTop: "1px solid rgba(255,255,255,0.08)",
              display: "flex",
              alignItems: "center",
              gap: 8,
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 12,
              color: "#c084fc",
            }}
          >
            <span>💡 REAL-WORLD INTUITION</span>
          </div>
        </div>
      </div>

      {/* Bottom Takeaway Insight Banner */}
      <div
        style={{
          width: "100%",
          maxWidth: "1500px",
          background: "rgba(0, 240, 255, 0.08)",
          border: "1px solid rgba(0, 240, 255, 0.3)",
          borderRadius: "14px",
          padding: "14px 24px",
          display: "flex",
          alignItems: "center",
          gap: 14,
          transform: `translateY(${(1 - entrance) * 20}px)`,
          opacity: entrance,
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 11,
            fontWeight: 800,
            color: "#00f0ff",
            background: "rgba(0, 240, 255, 0.2)",
            padding: "4px 8px",
            borderRadius: "6px",
            letterSpacing: "1px",
          }}
        >
          CORE INSIGHT
        </div>
        <div
          style={{
            fontSize: 15,
            fontWeight: 700,
            color: "#ffffff",
            lineHeight: 1.3,
          }}
        >
          {takeaway}
        </div>
      </div>
    </div>
  );
};
