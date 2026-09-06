import React from "react";
import { Audio, staticFile, Sequence } from "remotion";
import { DastawezShowProps } from "./types";
import { DastawezOverview } from "./DastawezOverview";
import { DastawezEligibility } from "./DastawezEligibility";
import { DastawezChecklist } from "./DastawezChecklist";
import { DastawezStepFlow } from "./DastawezStepFlow";
import { DastawezAlert } from "./DastawezAlert";

export const resolveMediaSrc = (path?: string) => {
  if (!path) return undefined;
  if (path.startsWith("http://") || path.startsWith("https://") || path.startsWith("data:")) {
    return path;
  }
  const normalized = path.replace(/\\/g, "/");
  const marker = "/automate/";
  const idx = normalized.indexOf(marker);
  const rel = idx !== -1 ? normalized.substring(idx + marker.length) : normalized.replace(/^\/+/, "");
  try {
    return staticFile(rel);
  } catch (e) {
    return "/" + rel;
  }
};

export const DastawezShow: React.FC<DastawezShowProps> = ({
  category,
  scenes = [],
  ambient_audio_path,
}) => {
  const resolvedAmbient = resolveMediaSrc(ambient_audio_path);

  // Calculate cumulative start frames for each scene sequence
  let currentStartFrame = 0;
  const sequenceConfigs = scenes.map((sc) => {
    const startFrame = currentStartFrame;
    const durationFrames = sc.duration_frames_30fps || Math.round(sc.duration_seconds * 30);
    currentStartFrame += durationFrames;
    return {
      scene: sc,
      from: startFrame,
      durationInFrames: durationFrames,
    };
  });

  return (
    <div
      style={{
        width: 1920,
        height: 1080,
        background: "#030a14",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Background Ambient Audio */}
      {resolvedAmbient && (
        <Audio src={resolvedAmbient} volume={0.08} loop />
      )}

      {/* Sequential Scene Components and Synchronized Scene Voiceovers */}
      {sequenceConfigs.map(({ scene, from, durationInFrames }, idx) => {
        const resolvedSceneAudio = resolveMediaSrc(scene.audio_path);

        return (
          <Sequence
            key={idx}
            from={from}
            durationInFrames={durationInFrames}
            name={`Scene_${scene.scene_id}_${scene.act_name}`}
          >
            {/* Audio Voiceover for Scene */}
            {resolvedSceneAudio && (
              <Audio src={resolvedSceneAudio} volume={1.0} />
            )}

            {/* Visual Scene Infographics Layout */}
            {scene.layout_type === "scheme_overview" && (
              <DastawezOverview
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                benefitHighlight={scene.benefit_highlight}
                latestUpdate={scene.latest_update}
                portalUrl={scene.portal_url}
                urgencyBadge={scene.urgency_badge}
                category={category}
              />
            )}

            {scene.layout_type === "eligibility_card" && (
              <DastawezEligibility
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                eligibilityYes={scene.eligibility_yes}
                eligibilityNo={scene.eligibility_no}
                category={category}
              />
            )}

            {scene.layout_type === "documents_checklist" && (
              <DastawezChecklist
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                documents={scene.documents}
                bankNote={scene.bank_note}
                category={category}
              />
            )}

            {scene.layout_type === "step_by_step_flow" && (
              <DastawezStepFlow
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                steps={scene.application_steps || (scene as any).steps}
                portalUrl={scene.portal_url}
                category={category}
              />
            )}

            {scene.layout_type === "official_alert" && (
              <DastawezAlert
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                portalUrl={scene.portal_url}
                helpline={scene.helpline}
                warning={scene.warning}
                category={category}
              />
            )}
          </Sequence>
        );
      })}
    </div>
  );
};
