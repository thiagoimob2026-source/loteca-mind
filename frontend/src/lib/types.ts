/* ===== TypeScript Interfaces for Loteca Mind ===== */

export interface TeamData {
  name: string;
  abbreviation: string;
  xg_accumulated: number;
  vertical_passes_avg: number;
  box_entries_avg: number;
  counter_attack_efficiency: number;
  clean_sheet_rate: number;
  form_last_5: string[];
  clutch_factor?: number;
}

export interface ContextData {
  momentum: "on_fire" | "stable" | "crisis" | "new_coach";
  coach_change_days: number | null;
  var_incidents_last_5: number;
  ex_players_in_opponent: number;
  away_resilience: number;
  consecutive_losses: number;
  is_six_pointer: boolean;
  recent_news_sentiment: number;
}

export interface MatchData {
  id: number;
  round_number: number;
  competition: string;
  home_team: TeamData;
  away_team: TeamData;
  home_context: ContextData;
  away_context: ContextData;
  venue: string;
  kickoff_time: string | null;
  head_to_head: { home_wins: number; draws: number; away_wins: number };
  is_verified?: boolean;
}

export interface FusionResult {
  match_id: number;
  home_team: string;
  away_team: string;
  home_win_prob: number;
  draw_prob: number;
  away_win_prob: number;
  reason_score: number;
  emotion_score: number;
  overall_confidence: number;
  suggested_column: "1" | "X" | "2";
  key_factors: string[];
  emotional_factors: string[];
  zebra_alert: boolean;
  zebra_insight: string | null;
  home_temperature: "on_fire" | "stable" | "cold";
  away_temperature: "on_fire" | "stable" | "cold";
  clutch_factor: number;
  deep_analysis: string | null;
  latest_news_summary?: string | null;
  is_verified?: boolean;
}

export interface TicketSuggestion {
  match_id: number;
  home_team: string;
  away_team: string;
  columns: string[];
  bet_type: "simples" | "duplo" | "triplo";
  confidence: number;
  reason_score: number;
  emotion_score: number;
}

export interface StrategistOutput {
  suggestions: TicketSuggestion[];
  total_combinations: number;
  ticket_cost: number;
  target_budget: number;
  doubles_count: number;
  triples_count: number;
  expected_roi: number | null;
}

export interface LotecaPrediction {
  round_number: number;
  competition: string;
  fusions: FusionResult[];
  strategy: StrategistOutput;
  zebra_hunter_verdict: string | null;
  deep_analysis: string;
  generated_at: string;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  display_name: string;
  avatar_url: string | null;
  total_points: number;
  accuracy_rate: number;
  badges_count: number;
  tier: string;
}

export interface Badge {
  type: string;
  name: string;
  description: string;
  icon: string;
  earned_at: string | null;
}

export interface MatchesResponse {
  round_number: number;
  competition: string;
  total_matches: number;
  matches: MatchData[];
}

export interface LeaderboardResponse {
  total_users: number;
  entries: LeaderboardEntry[];
}
