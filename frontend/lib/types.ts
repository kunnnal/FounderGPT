export type Stage = "idea" | "validation" | "mvp" | "pilot" | "growth";

export type FounderProfileInput = {
  name: string;
  role: string;
  years_experience: number;
  domain_expertise: string;
  previous_startup_exits: number;
  technical_strength: number;
  go_to_market_strength: number;
};

export type WarRoomRequest = {
  startup_name: string;
  one_line_pitch: string;
  problem: string;
  solution: string;
  target_customer: string;
  business_model: string;
  market_context: string;
  stage: Stage;
  traction_summary: string;
  monthly_revenue: number;
  monthly_burn: number;
  runway_months: number;
  team_size: number;
  founder: FounderProfileInput;
};

export type Citation = {
  source: string;
  title: string;
  snippet: string;
};

export type AgentFinding = {
  agent: string;
  focus_area: string;
  verdict: string;
  confidence: number;
  summary: string;
  strengths: string[];
  concerns: string[];
  next_steps: string[];
  citations: Citation[];
};

export type DebateTurn = {
  speaker: string;
  counterparty: string;
  stance: string;
  message: string;
};

export type ScoreCard = {
  market: number;
  product: number;
  execution: number;
  financial: number;
  defensibility: number;
  overall: number;
  readiness_stage: string;
};

export type FailureRisk = {
  risk: string;
  probability: number;
  severity: string;
  mitigation: string;
};

export type ScenarioResult = {
  name: string;
  assumption: string;
  outcome: string;
  impact_score: number;
};

export type Recommendation = {
  decision: string;
  confidence: number;
  rationale: string;
  milestones: string[];
  investor_readiness: string;
};

export type WarRoomResponse = {
  session_id: string;
  created_at: string;
  request: WarRoomRequest;
  executive_summary: string;
  routing: string[];
  agent_findings: AgentFinding[];
  debate: DebateTurn[];
  scorecard: ScoreCard;
  failure_risks: FailureRisk[];
  scenarios: ScenarioResult[];
  recommendation: Recommendation;
  citations: Citation[];
};

export type DemoPayload = {
  request: WarRoomRequest;
  notes: string[];
};

