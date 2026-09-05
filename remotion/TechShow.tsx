import React from "react";
import { Audio, staticFile, useCurrentFrame, useVideoConfig, Sequence } from "remotion";
import { TechShowProps, Scene } from "./types";
import { ChapterBumper } from "./components/ChapterBumper";
import { ArticleCard } from "./components/ArticleCard";
import { StatMetricCard } from "./components/StatMetricCard";
import { MemeReaction } from "./components/MemeReaction";
import { CinematicBroll } from "./components/CinematicBroll";
import { KineticCaptions } from "./components/KineticCaptions";

const SFX_MAP: Record<string, string> = {
  bruh: "assets/audio/bruh.wav",
  windows_error: "assets/audio/windows_error.wav",
  vine_boom: "assets/audio/vine_boom.wav",
  pop: "assets/audio/pop_click.wav",
  whoosh: "assets/audio/whoosh.wav",
  record_scratch: "assets/audio/record_scratch.wav",
};

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

export const TechShow: React.FC<TechShowProps> = ({
  scenes = [],
  audio_path,
  ambient_path,
  phrases = [],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Locate active scene
  let activeScene: Scene | undefined = scenes.find(
    (sc) => sc.start <= currentTime && currentTime <= sc.end
  );

  if (!activeScene && scenes.length > 0) {
    if (currentTime >= scenes[scenes.length - 1].end) {
      activeScene = scenes[scenes.length - 1];
    } else {
      activeScene = scenes[0];
    }
  }

  const layoutType = activeScene?.layout_type || "fullscreen_broll";
  const resolvedBroll = resolveMediaSrc(activeScene?.broll_path);
  const resolvedMeme = resolveMediaSrc(activeScene?.meme_path);
  const resolvedAudio = resolveMediaSrc(audio_path);
  const resolvedAmbient = resolveMediaSrc(ambient_path);

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        backgroundColor: "#070b14",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* 1. Dynamic Layout Rendering */}
      {layoutType === "chapter_bumper" && (
        <ChapterBumper
          chapterNo={activeScene?.chapter_id || 1}
          chapterTitle={activeScene?.chapter_title || "CHAPTER"}
          subtitle={activeScene?.chapter_subtitle || ""}
        />
      )}

      {layoutType === "splitscreen_article" && (
        <ArticleCard
          brollPath={resolvedBroll}
          source={activeScene?.article_source}
          headline={activeScene?.article_headline}
          quote={activeScene?.article_quote}
        />
      )}

      {layoutType === "splitscreen_stat" && (
        <StatMetricCard
          brollPath={resolvedBroll}
          statNumber={activeScene?.stat_number}
          statLabel={activeScene?.stat_label}
          statContext={activeScene?.stat_context}
          statChange={activeScene?.stat_change}
        />
      )}

      {layoutType === "meme_reaction" && (
        <MemeReaction
          memePath={resolvedMeme}
          punchline={activeScene?.meme_punchline}
        />
      )}

      {layoutType === "fullscreen_broll" && (
        <CinematicBroll brollPath={resolvedBroll} />
      )}

      {/* 2. Kinetic Captions Overlay (Lower third, outside bumper cards) */}
      {layoutType !== "chapter_bumper" && (
        <KineticCaptions phrases={phrases} currentTime={currentTime} />
      )}

      {/* 3. Audio Tracks */}
      {resolvedAudio && <Audio src={resolvedAudio} />}
      {resolvedAmbient && <Audio src={resolvedAmbient} volume={0.12} loop />}

      {/* 4. Situational SFX triggers */}
      {scenes.map((sc, idx) => {
        const sfxKey = sc.sfx || (sc.layout_type === "chapter_bumper" ? "whoosh" : undefined);
        if (!sfxKey || !SFX_MAP[sfxKey]) return null;
        const sfxSrc = resolveMediaSrc(SFX_MAP[sfxKey]);
        if (!sfxSrc) return null;
        const startFrame = Math.max(0, Math.round(sc.start * fps));
        return (
          <Sequence key={`sfx-${idx}`} from={startFrame} durationInFrames={fps * 3}>
            <Audio src={sfxSrc} volume={0.35} />
          </Sequence>
        );
      })}
    </div>
  );
};
