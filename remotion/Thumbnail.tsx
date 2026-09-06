import React from "react";

export interface ThumbnailProps {
  category?: string;
  hookTitle?: string;
  hookHighlight?: string;
  subtitle?: string;
  badge?: string;
  accentColor?: string;
}

export const Thumbnail: React.FC<ThumbnailProps> = ({
  category = "AEROSPACE FORENSICS",
  hookTitle = "THE 64-BIT",
  hookHighlight = "GLITCH",
  subtitle = "How a single 10-line software shortcut destroyed a $500,000,000 rocket in 37 seconds.",
  badge = "⚠️ MISSION STATUS: CRITICAL DETONATION",
  accentColor = "#00f0ff",
}) => {
  return (
    <div
      style={{
        width: 1280,
        height: 720,
        position: "relative",
        backgroundColor: "#030712",
        overflow: "hidden",
        fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
        display: "flex",
      }}
    >
      {/* 1. Background Cinematic Blueprint Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(0, 240, 255, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.08) 1px, transparent 1px)
          `,
          backgroundSize: "48px 48px",
        }}
      />

      {/* 2. Deep Blue Ambient Glow Orbs */}
      <div
        style={{
          position: "absolute",
          top: "10%",
          left: "8%",
          width: 500,
          height: 500,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(0, 240, 255, 0.22) 0%, transparent 70%)",
          filter: "blur(60px)",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: "10%",
          right: "15%",
          width: 450,
          height: 450,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(168, 85, 247, 0.2) 0%, transparent 70%)",
          filter: "blur(70px)",
        }}
      />

      {/* 3. Left Anchor: 3D CAD Hologram Wireframe */}
      <div
        style={{
          width: 560,
          height: 720,
          position: "relative",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* Outer Circular Compass Reticle */}
        <div
          style={{
            position: "absolute",
            width: 420,
            height: 420,
            borderRadius: "50%",
            border: "1.5px dashed rgba(0, 240, 255, 0.4)",
          }}
        />
        <div
          style={{
            position: "absolute",
            width: 470,
            height: 470,
            borderRadius: "50%",
            border: "1px solid rgba(0, 240, 255, 0.15)",
          }}
        />

        {/* Outer Hexagon Matrix */}
        <div
          style={{
            position: "absolute",
            width: 320,
            height: 320,
            borderRadius: 36,
            border: "3px solid #00f0ff",
            boxShadow: "0 0 35px rgba(0, 240, 255, 0.6), inset 0 0 35px rgba(0, 240, 255, 0.2)",
            transform: "rotate(25deg)",
          }}
        />

        {/* Counter-Rotated Core Hologram Square */}
        <div
          style={{
            position: "absolute",
            width: 230,
            height: 230,
            borderRadius: 24,
            border: "3px solid #c084fc",
            boxShadow: "0 0 45px rgba(192, 132, 252, 0.7), inset 0 0 25px rgba(192, 132, 252, 0.3)",
            transform: "rotate(-20deg)",
          }}
        />

        {/* High-Energy Glowing Core Sphere */}
        <div
          style={{
            width: 90,
            height: 90,
            borderRadius: "50%",
            background: "radial-gradient(circle, #ffffff 0%, #00f0ff 50%, #0284c7 100%)",
            boxShadow: "0 0 60px #00f0ff, 0 0 110px rgba(0, 240, 255, 0.9)",
          }}
        />

        {/* Telemetry Coordinate Vectors */}
        <div
          style={{
            position: "absolute",
            top: 70,
            left: 50,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 13,
            color: "rgba(0, 240, 255, 0.8)",
            letterSpacing: "1.5px",
          }}
        >
          SYS-SPEC // 64-BIT IEEE-754
        </div>
        <div
          style={{
            position: "absolute",
            bottom: 70,
            left: 50,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            color: "rgba(255, 255, 255, 0.6)",
            letterSpacing: "1.5px",
          }}
        >
          VECTOR [36.7s // MAX-Q FLIGHT]
        </div>
      </div>

      {/* 4. Right Side: Massive Typography & Curiosity Hook */}
      <div
        style={{
          flex: 1,
          height: 720,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          paddingRight: 80,
          paddingLeft: 20,
          zIndex: 10,
        }}
      >
        {/* Category Pill Badge */}
        <div style={{ marginBottom: 24 }}>
          <span
            style={{
              display: "inline-block",
              padding: "8px 20px",
              borderRadius: 30,
              backgroundColor: "rgba(0, 240, 255, 0.12)",
              border: `1.5px solid ${accentColor}`,
              color: accentColor,
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 14,
              fontWeight: 800,
              letterSpacing: "2.5px",
              boxShadow: `0 0 20px rgba(0, 240, 255, 0.25)`,
            }}
          >
            ● {category.toUpperCase()}
          </span>
        </div>

        {/* Primary 3-4 Word Hook Title */}
        <h1
          style={{
            margin: 0,
            fontSize: 78,
            fontWeight: 900,
            lineHeight: 1.05,
            letterSpacing: "-2px",
            color: "#ffffff",
            textTransform: "uppercase",
            textShadow: "0 6px 30px rgba(0, 0, 0, 0.9)",
          }}
        >
          {hookTitle} <br />
          <span
            style={{
              color: "#fbbf24",
              textShadow: "0 0 35px rgba(251, 191, 36, 0.6)",
            }}
          >
            {hookHighlight}
          </span>
        </h1>

        {/* Curiosity Gap Subtitle */}
        <p
          style={{
            marginTop: 24,
            marginBottom: 32,
            fontSize: 22,
            fontWeight: 500,
            lineHeight: 1.4,
            color: "#cbd5e1",
            maxWidth: 580,
            textShadow: "0 2px 10px rgba(0, 0, 0, 0.8)",
          }}
        >
          {subtitle}
        </p>

        {/* Hazard / Telemetry Badge */}
        <div>
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 10,
              padding: "10px 22px",
              borderRadius: 14,
              backgroundColor: "rgba(239, 68, 68, 0.15)",
              border: "1.5px solid rgba(239, 68, 68, 0.6)",
              color: "#fca5a5",
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 14,
              fontWeight: 700,
              letterSpacing: "1px",
              boxShadow: "0 0 25px rgba(239, 68, 68, 0.2)",
            }}
          >
            {badge}
          </div>
        </div>
      </div>

      {/* 5. Subtle Edge Vignette Border */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          border: "4px solid rgba(0, 240, 255, 0.3)",
          pointerEvents: "none",
        }}
      />
    </div>
  );
};
