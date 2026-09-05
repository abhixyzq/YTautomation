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
  layout_type: "chapter_bumper" | "fullscreen_broll" | "splitscreen_article" | "splitscreen_stat" | "meme_reaction";
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
