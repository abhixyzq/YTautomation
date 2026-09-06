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
  documents?: string[];
  bank_note?: string;
  application_steps?: Array<{
    step: number;
    title: string;
    desc: string;
  }>;
  what_changed?: WhatChangedData;
  evidence?: EvidenceMetadata;
  audio_path?: string;
  visual_media?: {
    broll_video_path?: string;
    official_image_path?: string;
    official_image_title?: string;
    attribution?: string;
  };
  duration_seconds: number;
  duration_frames_30fps: number;
  phrases?: Phrase[];
  word_timings?: WordTiming[];
}

export interface DastawezShowProps {
  title: string;
  scheme_id: string;
  category: string;
  scenes: DastawezScene[];
  ambient_audio_path?: string;
  evidence?: EvidenceMetadata;
  visual_media?: {
    broll_video_path?: string;
    official_image_path?: string;
    official_image_title?: string;
    attribution?: string;
  };
}

export interface DastawezThumbnailProps {
  scheme_name: string;
  big_benefit: string;
  urgency_badge?: string;
  portal_name?: string;
  helpline?: string;
  rule_change_badge?: string;
}

