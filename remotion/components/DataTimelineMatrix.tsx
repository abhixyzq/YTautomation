import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

interface TimelineEvent {
  time_label: string;
  title: string;
  desc: string;
  severity?: "info" | "warning" | "critical";
}

interface DataTimelineMatrixProps {
  timelineTitle?: string;
  events?: TimelineEvent[];
}

export const DataTimelineMatrix: React.FC<DataTimelineMatrixProps> = ({
  timelineTitle = "CHRONOLOGICAL AUTOPSY OF THE EVENT",
  events = [
    { time_label: "00:00:00", title: "Lift-Off Confirmed", desc: "Engine telemetry nominal. Velocity reaching Mach 1.2.", severity: "info" },
    { time_label: "00:00:36", title: "Internal Float Overflow", desc: "Primary SRI guidance computer downcasts 64-bit value to 16-bit int.", severity: "warning" },
    { time_label: "00:00:37", title: "Erroneous Nozzle Deflection", desc: "Computer interprets debug crash codes as angle corrections.", severity: "critical" },
    { time_label: "00:00:39", title: "Structural Disintegration", desc: "Aerodynamic stress triggers emergency flight termination system.", severity: "critical" },
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleSpring = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  const pulse = 0.85 + Math.sin(frame / 8) * 0.15;

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        backgroundColor: "#050812",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "50px 90px 45px",
        overflow: "hidden",
        fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
      }}
    >
      {/* Background Grid Lines */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px)
          `,
          backgroundSize: "60px 60px",
          opacity: 0.6,
        }}
      />

      {/* Header */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `scale(${titleSpring})`,
          opacity: titleSpring,
          zIndex: 2,
        }}
      >
        <div
          style={{
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 12,
            fontWeight: 800,
            color: "#f59e0b",
            letterSpacing: "2px",
            textTransform: "uppercase",
            marginBottom: 6,
            background: "rgba(245, 158, 11, 0.12)",
            padding: "4px 14px",
            borderRadius: "99px",
            border: "1px solid rgba(245, 158, 11, 0.3)",
          }}
        >
          INVESTIGATIVE FORENSICS // TIMELINE
        </div>
        <div
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#ffffff",
            letterSpacing: "-0.5px",
            textTransform: "uppercase",
            textShadow: "0 4px 20px rgba(245, 158, 11, 0.3)",
          }}
        >
          {timelineTitle}
        </div>
      </div>

      {/* Timeline Chain Grid */}
      <div
        style={{
          display: "flex",
          alignItems: "stretch",
          justifyContent: "center",
          gap: 20,
          width: "100%",
          maxWidth: "1550px",
          position: "relative",
          zIndex: 2,
        }}
      >
        {events.map((ev, idx) => {
          const itemSpring = spring({
            frame: frame - idx * 7,
            fps,
            config: { damping: 14, stiffness: 95 },
          });

          const isCrit = ev.severity === "critical";
          const isWarn = ev.severity === "warning";

          let badgeColor = "#00f0ff";
          let borderColor = "rgba(0, 240, 255, 0.3)";
          if (isCrit) {
            badgeColor = "#ef4444";
            borderColor = "rgba(239, 68, 68, 0.4)";
          } else if (isWarn) {
            badgeColor = "#f59e0b";
            borderColor = "rgba(245, 158, 11, 0.4)";
          }

          return (
            <div
              key={idx}
              style={{
                flex: 1,
                background: "rgba(10, 16, 32, 0.8)",
                backdropFilter: "blur(20px)",
                border: `1.5px solid ${borderColor}`,
                borderRadius: "20px",
                padding: "24px 20px",
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                boxShadow: isCrit
                  ? `0 0 ${25 * pulse}px rgba(239, 68, 68, 0.25)`
                  : "0 10px 30px rgba(0,0,0,0.5)",
                transform: `translateY(${(1 - itemSpring) * 30}px)`,
                opacity: Math.max(0, itemSpring),
              }}
            >
              <div>
                {/* Time Indicator Badge */}
                <div
                  style={{
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 13,
                    fontWeight: 800,
                    color: badgeColor,
                    letterSpacing: "1px",
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    marginBottom: 12,
                  }}
                >
                  <span
                    style={{
                      width: 8,
                      height: 8,
                      borderRadius: "50%",
                      backgroundColor: badgeColor,
                      boxShadow: `0 0 10px ${badgeColor}`,
                    }}
                  />
                  <span>{ev.time_label.startsWith("T") ? ev.time_label : `T + ${ev.time_label}`}</span>
                </div>

                {/* Event Headline */}
                <div
                  style={{
                    fontSize: 20,
                    fontWeight: 800,
                    color: "#ffffff",
                    lineHeight: 1.3,
                    marginBottom: 10,
                  }}
                >
                  {ev.title}
                </div>

                {/* Technical Forensic Detail */}
                <div
                  style={{
                    fontSize: 13,
                    fontWeight: 500,
                    color: "#94a3b8",
                    lineHeight: 1.55,
                  }}
                >
                  {ev.desc}
                </div>
              </div>

              {/* Status Classification Label */}
              <div
                style={{
                  marginTop: 16,
                  paddingTop: 12,
                  borderTop: "1px solid rgba(255,255,255,0.07)",
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 11,
                  fontWeight: 700,
                  color: badgeColor,
                  textTransform: "uppercase",
                  letterSpacing: "0.5px",
                }}
              >
                ● STATUS: {ev.severity || "NOMINAL"}
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer System Indicator */}
      <div
        style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 11,
          color: "rgba(255, 255, 255, 0.4)",
          letterSpacing: "1px",
          zIndex: 2,
        }}
      >
        DOCUMENTARY EVIDENCE LOG // VERIFIED FLIGHT TELEMETRY
      </div>
    </div>
  );
};
