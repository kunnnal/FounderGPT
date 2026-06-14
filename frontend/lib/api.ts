import type { DemoPayload, WarRoomRequest, WarRoomResponse } from "@/lib/types";
import { defaultWarRoomRequest } from "./defaults";

export const API_BASE_URL = (() => {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }
  if (typeof window !== "undefined") {
    // Resolve hostname dynamically for local network/IP device testing
    const hostname = window.location.hostname;
    return `http://${hostname}:8000`;
  }
  return "http://localhost:8000";
})();

async function requestJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed.");
  }

  return (await response.json()) as T;
}

export async function getDemoRequest(): Promise<DemoPayload> {
  try {
    return await requestJson<DemoPayload>("/api/founder/demo");
  } catch (error) {
    console.warn("Backend not running. Falling back to local frontend mock data.", error);
    return {
      request: defaultWarRoomRequest,
      notes: [
        "Running in local frontend fallback mode.",
        "FastAPI backend is offline; simulation data is generated on the client."
      ]
    };
  }
}

export async function analyzeWarRoom(
  payload: WarRoomRequest,
): Promise<WarRoomResponse> {
  try {
    return await requestJson<WarRoomResponse>("/api/war-room/analyze", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  } catch (error) {
    console.warn("Backend not running. Generating client-side simulation report.", error);
    // Simulate minor network delay for feedback feel
    await new Promise((resolve) => setTimeout(resolve, 800));
    return generateLocalMockReport(payload);
  }
}

export async function getSession(sessionId: string): Promise<WarRoomResponse> {
  try {
    return await requestJson<WarRoomResponse>(`/api/war-room/sessions/${sessionId}`);
  } catch (error) {
    console.warn("Backend not running. Generating client-side session report.", error);
    return generateLocalMockReport(defaultWarRoomRequest, sessionId);
  }
}

function generateLocalMockReport(
  request: WarRoomRequest,
  sessionId?: string,
): WarRoomResponse {
  const sId = sessionId ?? `session_mock_${Math.random().toString(36).substring(2, 11)}`;
  const dateStr = new Date().toISOString();

  // Compute mock score based on request values
  const hasRevenue = request.monthly_revenue > 0;
  const isVague = request.one_line_pitch.length < 25;
  const burnRatio = request.monthly_burn / Math.max(1, request.monthly_revenue);

  const market = isVague ? 60 : 85;
  const product = Math.min(98, Math.max(30, request.founder.technical_strength * 10));
  const execution = Math.min(98, Math.max(30, request.founder.go_to_market_strength * 10));
  const financial = burnRatio > 4 ? 45 : 75;
  const defensibility = Math.min(95, 50 + (request.founder.years_experience * 3));

  const overall = Math.round((market + product + execution + financial + defensibility) / 5);
  const readiness_stage = overall > 80 ? "Pre-seed / Ready" : overall > 60 ? "Incubation" : "Ideation / Refinement Needed";

  return {
    session_id: sId,
    created_at: dateStr,
    request,
    executive_summary: `The venture proposal '${request.startup_name}' presents a ${readiness_stage.toLowerCase()} rating. The core priority is testing target client workflow integration to mitigate early support hurdles before accelerating GTM burn.`,
    routing: ["product", "gtm", "compliance", "finance", "risk"],
    agent_findings: [
      {
        agent: "product",
        focus_area: "MVP Scope",
        verdict: "APPROVED WITH CONDITIONS",
        confidence: 88,
        summary: `The core solution in '${request.startup_name}' is technically viable, but the MVP outline must be defended against feature creep to maintain speed.`,
        strengths: [
          "Directly addresses target client pain points.",
          "Lightweight profile minimises early development overhead."
        ],
        concerns: [
          "Messaging risks sounding overly broad without narrow wedge features.",
          "Requires custom metrics instrumentation to track client activation milestones."
        ],
        next_steps: [
          "Reduce the early outline to a single user journey.",
          "Instrument client activation monitoring from day one."
        ],
        citations: [
          {
            source: "MVP Strategy Library",
            title: "Wedge validation in early SaaS products",
            snippet: "Early SaaS systems succeed by proving high engagement on one single workflow."
          }
        ]
      },
      {
        agent: "gtm",
        focus_area: "Distribution and pricing",
        verdict: "CAUTION",
        confidence: 82,
        summary: "Distribution channel validation is the primary challenge. Outbound should be founder-led early on.",
        strengths: [
          "Subscription pricing models align with client scale milestones.",
          "GTM founder skills support outbound discovery conversations."
        ],
        concerns: [
          "Messaging can drift to generic efficiency claims if wedges aren't verified.",
          "High client acquisition friction expected if target segments are not narrowed."
        ],
        next_steps: [
          "Define a targeted outbound contact list of 30 initial partner accounts.",
          "Run early validation pilot feedback iterations before committing paid marketing burn."
        ],
        citations: []
      },
      {
        agent: "compliance",
        focus_area: "Automation and privacy controls",
        verdict: "STABLE",
        confidence: 90,
        summary: "Data handling scope is low-risk, but compliance controls should be set up early.",
        strengths: [
          "Avoids storing unnecessary personal user records in early data paths.",
          "Lightweight architecture simplifies logging integrations."
        ],
        concerns: [
          "Privacy guidelines apply as soon as client business workflows are processed.",
          "Requires explicit data logging boundaries prior to scaling partner access."
        ],
        next_steps: [
          "Document data retention schedules and access controls.",
          "Implement human review safeguards for automated recommendations."
        ],
        citations: []
      }
    ],
    debate: [
      {
        speaker: "product",
        counterparty: "gtm",
        stance: "CHALLENGE",
        message: "Adding custom features early to close deals will clutter the MVP and delay validation."
      },
      {
        speaker: "gtm",
        counterparty: "product",
        stance: "RECONCILE",
        message: "Agreed. We will prioritize design partners who can work with the core wedge workflow."
      }
    ],
    scorecard: {
      market,
      product,
      execution,
      financial,
      defensibility,
      overall,
      readiness_stage
    },
    failure_risks: [
      {
        risk: "Vague Wedge and Messaging Drift",
        probability: 65,
        severity: "HIGH",
        mitigation: "Focus GTM copy strictly on onboarding activation outcomes."
      },
      {
        risk: "Runway Pressure",
        probability: burnRatio > 3 ? 80 : 35,
        severity: "CRITICAL",
        mitigation: "Close paying pilots early to off-set burn rates."
      }
    ],
    scenarios: [
      {
        name: "Base Runway Burn",
        assumption: "Burn and revenue settings remain consistent.",
        outcome: `Runway will last approximately ${request.runway_months} months.`,
        impact_score: 80
      },
      {
        name: "Slow Pilot Onboarding",
        assumption: "Partner activation takes 3 months longer than expected.",
        outcome: "Venture burn compounds, decreasing runway limits by 30%.",
        impact_score: 55
      }
    ],
    recommendation: {
      decision: overall > 75 ? "INVESTMENT READY" : "PLANNING REFINEMENT REQUIRED",
      confidence: 85,
      rationale: `The solution solves a real bottleneck. The priority milestone is proving retention metrics quickly.`,
      milestones: [
        "Close 3 design partners on paying pilots.",
        "Reach an activation engagement rate above 40%."
      ],
      investor_readiness: "Venture is viable for early incubator review."
    },
    citations: []
  };
}
