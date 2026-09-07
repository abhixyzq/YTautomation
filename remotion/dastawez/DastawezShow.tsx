import React from "react";
import { Audio, OffthreadVideo, staticFile, Sequence, useCurrentFrame, interpolate } from "remotion";
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

const LongVideoBackgroundClipItem: React.FC<{
  videoSrc?: string;
  durationInFrames: number;
}> = ({ videoSrc, durationInFrames }) => {
  const frame = useCurrentFrame();

  // Subtle broadcast Ken Burns pan + zoom
  const zoom = interpolate(frame, [0, Math.max(1, durationInFrames)], [1.0, 1.05], {
    extrapolateRight: "clamp",
  });
  const panX = interpolate(frame, [0, Math.max(1, durationInFrames)], [0, -18], {
    extrapolateRight: "clamp",
  });

  // Smooth cross-fade transition
  const opacity = interpolate(frame, [0, 5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity,
        overflow: "hidden",
      }}
    >
      {videoSrc ? (
        <OffthreadVideo
          src={videoSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${zoom}) translateX(${panX}px)`,
            transformOrigin: "center center",
          }}
        />
      ) : (
        <div style={{ width: "100%", height: "100%", background: "#0b1120" }} />
      )}
    </div>
  );
};

export const DastawezShow: React.FC<DastawezShowProps> = ({
  category,
  scenes = [],
  ambient_audio_path,
  evidence: globalEvidence,
  visual_media,
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
        backgroundColor: "#070b14",
        position: "relative",
        overflow: "hidden",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans Devanagari', sans-serif",
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
        const sceneBroll = resolveMediaSrc(scene.visual_media?.broll_video_path || visual_media?.broll_video_path);
        const officialImg = resolveMediaSrc(scene.visual_media?.official_image_path || visual_media?.official_image_path);
        const officialImgTitle = scene.visual_media?.official_image_title || visual_media?.official_image_title;
        const officialImgAttr = scene.visual_media?.attribution || visual_media?.attribution;

        const backgroundClips = scene.visual_media?.background_clips || [];

        return (
          <Sequence
            key={idx}
            from={from}
            durationInFrames={durationInFrames}
            name={`Scene_${scene.scene_id}_${scene.act_name}`}
          >
            {/* 1. 100% Fullscreen Cinematic Dynamic B-Roll Video Sequencer */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                overflow: "hidden",
                zIndex: 0,
                backgroundColor: "#070b14",
              }}
            >
              {backgroundClips.length > 0 ? (
                backgroundClips.map((clip, clipIdx) => {
                  const clipFrom = Math.round(clip.start * 30);
                  const clipDur = Math.max(1, Math.round((clip.end - clip.start) * 30));
                  const clipSrc = resolveMediaSrc(clip.video_path);

                  return (
                    <Sequence
                      key={clipIdx}
                      from={clipFrom}
                      durationInFrames={clipDur}
                      layout="none"
                    >
                      <LongVideoBackgroundClipItem
                        videoSrc={clipSrc}
                        durationInFrames={clipDur}
                      />
                    </Sequence>
                  );
                })
              ) : (
                <LongVideoBackgroundClipItem
                  videoSrc={sceneBroll}
                  durationInFrames={durationInFrames}
                />
              )}

              {/* Cinematic Vignette Overlay (Ensures HUD widgets and subtitles pop with 100% clarity) */}
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background:
                    "linear-gradient(180deg, rgba(7, 11, 20, 0.78) 0%, rgba(7, 11, 20, 0.3) 30%, rgba(7, 11, 20, 0.45) 65%, rgba(7, 11, 20, 0.92) 100%)",
                  pointerEvents: "none",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  boxShadow: "inset 0 0 140px rgba(0, 0, 0, 0.8)",
                  pointerEvents: "none",
                }}
              />
            </div>

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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
                visualMedia={scene.visual_media || visual_media}
                officialImagePath={officialImg}
                officialImageTitle={officialImgTitle}
                brollVideoPath={sceneBroll}
                attribution={officialImgAttr}
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
