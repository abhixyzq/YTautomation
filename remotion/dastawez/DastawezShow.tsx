import React from "react";
import { Audio, staticFile, Sequence } from "remotion";
import { DastawezShowProps } from "./types";
import { DastawezOverview } from "./DastawezOverview";
import { DastawezWhatChanged } from "./DastawezWhatChanged";
import { DastawezEligibility } from "./DastawezEligibility";
import { DastawezChecklist } from "./DastawezChecklist";
import { DastawezStepFlow } from "./DastawezStepFlow";
import { DastawezAlert } from "./DastawezAlert";
import { DastawezSourceCard } from "./DastawezSourceCard";
import { DastawezCaptions } from "./DastawezCaptions";

export const resolveMediaSrc = (path?: string) => {
  if (!path) return undefined;
  if (path.startsWith("http://") || path.startsWith("https://") || path.startsWith("data:")) {
    return path;
  }
  let normalized = path.replace(/\\/g, "/");

  // If path contains public/, strip everything up to public/
  const pubIdx = normalized.indexOf("/public/");
  if (pubIdx !== -1) {
    normalized = normalized.substring(pubIdx + "/public/".length);
  } else if (normalized.startsWith("public/")) {
    normalized = normalized.substring("public/".length);
  }

  // Also strip workspace marker if present
  const marker = "/automate/";
  const idx = normalized.indexOf(marker);
  if (idx !== -1) {
    normalized = normalized.substring(idx + marker.length);
  }

  const rel = normalized.replace(/^\/+/, "");
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
  evidence: globalEvidence,
}) => {
  const resolvedAmbient = resolveMediaSrc(ambient_audio_path);

  // Calculate cumulative start frames for each scene sequence
  let currentStartFrame = 0;
  const totalActs = scenes.length;
  const sequenceConfigs = scenes.map((sc, idx) => {
    const startFrame = currentStartFrame;
    const durationFrames = sc.duration_frames_30fps || Math.round((sc.duration_seconds || 5) * 30);
    currentStartFrame += durationFrames;
    return {
      scene: sc,
      from: startFrame,
      durationInFrames: durationFrames,
      actIndex: idx + 1,
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
      {sequenceConfigs.map(({ scene, from, durationInFrames, actIndex }, idx) => {
        const resolvedSceneAudio = resolveMediaSrc(scene.audio_path);
        const evidence = scene.evidence || globalEvidence;

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
            {(scene.layout_type === "scheme_overview" || scene.layout_type === "overview") && (
              <DastawezOverview
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                benefitHighlight={scene.benefit_highlight}
                latestUpdate={scene.latest_update}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                urgencyBadge={scene.urgency_badge}
                category={category}
                evidence={evidence}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "what_changed" && (
              <DastawezWhatChanged
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                whatChanged={scene.what_changed}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                evidence={evidence}
                category={category}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "eligibility_card" && (
              <DastawezEligibility
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                eligibilityYes={scene.eligibility_yes}
                eligibilityNo={scene.eligibility_no}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                category={category}
                evidence={evidence}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "documents_checklist" && (
              <DastawezChecklist
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                documents={scene.documents}
                bankNote={scene.bank_note}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                category={category}
                evidence={evidence}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "step_by_step_flow" && (
              <DastawezStepFlow
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                applicationSteps={scene.application_steps || (scene as any).steps}
                steps={scene.application_steps || (scene as any).steps}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                category={category}
                evidence={evidence}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "official_alert" && (
              <DastawezAlert
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                helpline={scene.helpline || evidence?.helpline}
                warning={scene.warning}
                category={category}
                evidence={evidence}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {scene.layout_type === "source_verification" && (
              <DastawezSourceCard
                schemeName={scene.scheme_name}
                ministry={scene.ministry}
                portalUrl={scene.portal_url}
                officialPortalDomain={scene.official_portal_domain || evidence?.official_portal_domain}
                helpline={scene.helpline || evidence?.helpline}
                evidence={evidence}
                category={category}
                currentActIndex={actIndex}
                totalActs={totalActs}
              />
            )}

            {/* Real-time Lower-Third Synchronized Captions */}
            <DastawezCaptions phrases={scene.phrases} />
          </Sequence>
        );
      })}
    </div>
  );
};
