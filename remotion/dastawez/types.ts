export interface WordTiming {
  word: string;
  start: number;
  end: number;
}

export interface Phrase {
  phrase_text: string;
  start: number;
  end: number;
  words: WordTiming[];
}

export interface EvidenceMetadata {
  ministry?: string;
  notification_ref?: string;
  portal_url?: string;
  official_portal_domain?: string;
  last_verified_date?: string;
  source_citation?: string;
  helpline?: string;
}

export interface WhatChangedData {
  old_rule?: string;
  new_rule?: string;
  deadline?: string;
}

export interface SceneVisualMedia {
  broll_video_path?: string;
  official_image_path?: string;
  official_image_title?: string;
  attribution?: string;
  media_type?: "image" | "video";
  badge_label?: string;
  background_clips?: BackgroundClip[];
}

export interface DastawezScene {
  scene_id: number;
  act_name: string;
  dialogue: string;
  layout_type:
    | "overview"
    | "scheme_overview"
    | "what_changed"
    | "eligibility_card"
    | "documents_checklist"
    | "step_by_step_flow"
    | "official_alert"
    | "source_verification";
  scheme_name: string;
  ministry?: string;
  benefit_highlight?: string;
  latest_update?: string;
  portal_url?: string;
  official_portal_domain?: string;
  helpline?: string;
  warning?: string;
  urgency_badge?: string;
  eligibility_yes?: string[];
  eligibility_no?: string[];
  target_groups?: string[];
  priority_groups?: string[];
  guidelines?: string[];
  dos_and_donts?: string[];
  verification_checklist?: string[];
  documents?: string[];
  bank_note?: string;
  application_steps?: Array<{
    step: number;
    title: string;
    desc: string;
  }>;
  what_changed?: WhatChangedData;
  why_changed?: string;
  evidence?: EvidenceMetadata;
  audio_path?: string;
  visual_media?: SceneVisualMedia;
  duration_seconds: number;
  duration_frames_30fps: number;
  phrases?: Phrase[];
  word_timings?: WordTiming[];
  hero_stat?: string;
  hero_badge?: string;
  action_chips?: string[];
}

export interface DastawezShowProps {
  title: string;
  scheme_id: string;
  category: string;
  scenes: DastawezScene[];
  ambient_audio_path?: string;
  evidence?: EvidenceMetadata;
  visual_media?: SceneVisualMedia;
}

export interface DastawezThumbnailProps {
  scheme_name: string;
  big_benefit: string;
  urgency_badge?: string;
  portal_name?: string;
  helpline?: string;
  rule_change_badge?: string;
}

export interface BackgroundClip {
  start: number;
  end: number;
  video_path?: string;
  image_path?: string;
  query?: string;
  narration_part?: string;
}

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
  background_clips?: BackgroundClip[];
  broll_video_path?: string;
  official_image_path?: string;
}


