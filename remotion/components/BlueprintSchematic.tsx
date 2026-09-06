import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface BlueprintSpec {
  label: string;
  value: string;
}

interface BlueprintSchematicProps {
  brollPath?: string;
  title?: string;
  tag?: string;
  specs?: BlueprintSpec[];
}

export const BlueprintSchematic: React.FC<BlueprintSchematicProps> = ({
  brollPath,
  title = "SYSTEM ARCHITECTURE SCHEMATIC",
  tag = "SPEC // CAD-RECONSTRUCTION",
  specs = [
    { label: "CLOCK SPEED", value: "4.85 GHz" },
    { label: "QUANTUM TOLERANCE", value: "±0.002 nm" },
    { label: "DATA THROUGHPUT", value: "1.24 TB/s" },
    { label: "CRITICAL FAILURE RISK", value: "99.4%" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrances
  const cardSpring = spring({ frame, fps, config: { damping: 14, stiffness: 95 } });
  const pulse = 0.85 + Math.sin(frame / 12) * 0.15;
  const gridPan = (frame / 2) % 40;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#050811",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "60px 80px",
        overflow: "hidden",
        fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
      }}
    >
      {/* 1. Background Cinematic Blueprint Grid */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(0, 240, 255, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.07) 1px, transparent 1px)
          `,
          backgroundSize: "40px 40px",
          backgroundPosition: `${gridPan}px ${gridPan}px`,
          opacity: 0.8,
        }}
      />

      {/* Crosshair accents at corners */}
      <div style={{ position: "absolute", top: 40, left: 40, color: "rgba(0,240,255,0.4)", fontFamily: "monospace", fontSize: 13 }}>
        + 37.7749° N, 122.4194° W [SCHEMATIC-SYS]
      </div>
      <div style={{ position: "absolute", bottom: 40, right: 40, color: "rgba(0,240,255,0.4)", fontFamily: "monospace", fontSize: 13 }}>
        CALIBRATION: ACTIVE // RES: 1080P
      </div>

      {/* 2. Left: Technical Wireframe & Geometry Hologram */}
      <div
        style={{
          width: "48%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
          zIndex: 2,
        }}
      >
        <div
          style={{
            width: "380px",
            height: "380px",
            borderRadius: "50%",
            border: "1px dashed rgba(0, 240, 255, 0.35)",
            position: "absolute",
            animation: "spin 20s linear infinite",
            transform: `scale(${cardSpring})`,
          }}
        />
        <div
          style={{
            width: "320px",
            height: "320px",
            borderRadius: "24px",
            border: "2px solid rgba(0, 240, 255, 0.6)",
            boxShadow: `0 0 ${25 * pulse}px rgba(0, 240, 255, 0.3), inset 0 0 30px rgba(0, 240, 255, 0.1)`,
            background: "rgba(10, 18, 36, 0.5)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexDirection: "column",
            gap: 16,
            transform: `scale(${cardSpring}) rotate(${(frame * 0.25) % 360}deg)`,
          }}
        >
          {/* Inner Geometric Wireframe Element */}
          <div
            style={{
              width: "160px",
              height: "160px",
              border: "1.5px solid #a855f7",
              transform: `rotate(${-(frame * 0.5) % 360}deg)`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 0 20px rgba(168, 85, 247, 0.4)",
            }}
          >
            <div
              style={{
                width: "80px",
                height: "80px",
                borderRadius: "50%",
                background: "radial-gradient(circle, #00f0ff 0%, transparent 70%)",
              }}
            />
          </div>
        </div>

        {/* Technical Callout Vector Arrow */}
        <div
          style={{
            position: "absolute",
            bottom: "8%",
            display: "flex",
            alignItems: "center",
            gap: 8,
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            color: "#00f0ff",
            letterSpacing: "1px",
            background: "rgba(0, 240, 255, 0.1)",
            padding: "6px 14px",
            borderRadius: "6px",
            border: "1px solid rgba(0, 240, 255, 0.3)",
          }}
        >
          <span>◀ COMPONENT TELEMETRY: REAL-TIME OVERLAY ▶</span>
        </div>
      </div>

      {/* 3. Right: Sleek Blueprint Dossier & Specifications */}
      <div
        style={{
          width: "48%",
          zIndex: 2,
          display: "flex",
          flexDirection: "column",
          gap: 18,
          transform: `translateY(${(1 - cardSpring) * 40}px)`,
          opacity: cardSpring,
        }}
      >
        {/* Document Classification Tag */}
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div
            style={{
              background: "rgba(0, 240, 255, 0.15)",
              border: "1px solid #00f0ff",
              color: "#00f0ff",
              fontSize: 11,
              fontWeight: 800,
              padding: "4px 10px",
              borderRadius: "4px",
              letterSpacing: "1.5px",
              fontFamily: "'JetBrains Mono', monospace",
            }}
          >
            {tag}
          </div>
          <div style={{ width: 40, height: 1, background: "rgba(0, 240, 255, 0.4)" }} />
        </div>

        {/* Headline / Title */}
        <div
          style={{
            fontSize: 36,
            fontWeight: 800,
            color: "#ffffff",
            lineHeight: 1.2,
            letterSpacing: "-0.5px",
            textTransform: "uppercase",
            textShadow: "0 4px 20px rgba(0, 240, 255, 0.25)",
          }}
        >
          {title}
        </div>

        {/* Specs Grid */}
        <div
          style={{
            background: "rgba(11, 19, 36, 0.75)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(0, 240, 255, 0.25)",
            borderRadius: "16px",
            padding: "20px 24px",
            display: "flex",
            flexDirection: "column",
            gap: 14,
            boxShadow: "0 20px 50px rgba(0, 0, 0, 0.6)",
          }}
        >
          {specs.map((item, idx) => (
            <div
              key={idx}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                paddingBottom: idx === specs.length - 1 ? 0 : 12,
                borderBottom: idx === specs.length - 1 ? "none" : "1px solid rgba(255, 255, 255, 0.07)",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div
                  style={{
                    width: 7,
                    height: 7,
                    borderRadius: "50%",
                    backgroundColor: idx % 2 === 0 ? "#00f0ff" : "#a855f7",
                    boxShadow: `0 0 8px ${idx % 2 === 0 ? "#00f0ff" : "#a855f7"}`,
                  }}
                />
                <span style={{ fontSize: 13, fontWeight: 700, color: "#94a3b8", letterSpacing: "0.5px" }}>
                  {item.label}
                </span>
              </div>
              <span
                style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 16,
                  fontWeight: 800,
                  color: "#f8fafc",
                }}
              >
                {item.value}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
