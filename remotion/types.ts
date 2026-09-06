export interface WordTiming {
  word: string;
  start: number;
  end: number;
}

export interface Phrase {
  words: WordTiming[];
  start: number;
  end: number;
}

export interface Scene {
  dialogue: string;
  layout_type:
    | "chapter_bumper"
    | "fullscreen_broll"
    | "splitscreen_article"
    | "splitscreen_stat"
    | "blueprint_schematic"
    | "kinetic_flowchart"
    | "visual_analogy"
    | "data_timeline_matrix"
    | "meme_reaction";
  broll_path?: string;
  meme_path?: string;
  meme_punchline?: string;
  article_headline?: string;
  article_quote?: string;
  article_source?: string;
  stat_number?: string;
  stat_label?: string;
  stat_context?: string;
  stat_change?: string;

  // 1. Blueprint Schematic (CAD technical wireframe & specs)
  schematic_title?: string;
  schematic_tag?: string;
  schematic_specs?: Array<{ label: string; value: string }>;

  // 2. Kinetic Flowchart (Veritasium logic chain)
  flowchart_title?: string;
  flowchart_steps?: Array<{ step: number; label: string; detail?: string; status?: "normal" | "active" | "critical" }>;

  // 3. Visual Analogy (Think School split card)
  analogy_title?: string;
  concept_name?: string;
  concept_desc?: string;
  analogy_name?: string;
  analogy_desc?: string;
  takeaway?: string;

  // 4. Data Timeline Matrix (Lemmino chronological autopsy)
  timeline_title?: string;
  timeline_events?: Array<{ time_label: string; title: string; desc: string; severity?: "info" | "warning" | "critical" }>;

  chapter_id: number;
  chapter_title: string;
  chapter_subtitle: string;
  start: number;
  end: number;
  sfx?: string;
}

export interface Chapter {
  chapter_id: number;
  chapter_title: string;
  subtitle: string;
  scenes: Scene[];
}

export interface TechShowProps {
  title: string;
  duration: number;
  audio_path: string;
  ambient_path?: string;
  scenes: Scene[];
  word_timings: WordTiming[];
  phrases?: Phrase[];
}
