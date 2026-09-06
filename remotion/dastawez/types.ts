export interface DastawezScene {
  scene_id: number;
  act_name: string;
  dialogue: string;
  layout_type: "scheme_overview" | "eligibility_card" | "documents_checklist" | "step_by_step_flow" | "official_alert";
  scheme_name: string;
  ministry?: string;
  benefit_highlight?: string;
  latest_update?: string;
  portal_url?: string;
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
  audio_path?: string;
  duration_seconds: number;
  duration_frames_30fps: number;
}

export interface DastawezShowProps {
  title: string;
  scheme_id: string;
  category: string;
  scenes: DastawezScene[];
  ambient_audio_path?: string;
}
