"""War room pipeline for the FounderGPT hackathon demo."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.agents import (
    run_compliance_agent,
    run_critic_agent,
    run_decision_agent,
    run_finance_agent,
    run_founder_profile_agent,
    run_gtm_agent,
    run_market_agent,
    run_planner_agent,
    run_product_agent,
    run_report_agent,
    run_risk_agent,
)
from app.engines.failure_prediction_engine import predict_failure_risks
from app.engines.readiness_engine import calculate_readiness_score
from app.engines.simulation_engine import run_simulations
from app.orchestration.debate_engine import build_debate
from app.orchestration.routing import build_routing_plan
from app.retrieval.foundry_iq_client import LocalKnowledgeBaseClient
from app.schemas.requests import FounderProfileInput, WarRoomRequest
from app.schemas.responses import Citation, WarRoomResponse
from app.schemas.state import WarRoomState
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WarRoomService:
    def __init__(self, knowledge_base: LocalKnowledgeBaseClient | None = None) -> None:
        self.knowledge_base = knowledge_base or LocalKnowledgeBaseClient()
        self.sessions: dict[str, WarRoomResponse] = {}

    def create_demo_request(self) -> WarRoomRequest:
        return WarRoomRequest(
            startup_name="OnboardPilot",
            one_line_pitch="AI onboarding coach for B2B SaaS teams that cuts time-to-value and support load.",
            problem=(
                "Mid-market B2B SaaS teams lose trial users and expansion revenue because onboarding is manual, "
                "implementation is slow, and customer success teams cannot personalize setup at scale."
            ),
            solution=(
                "An AI-guided onboarding workspace that maps product setup steps, nudges users toward first value, "
                "and gives customer success teams a playbook to reduce drop-off during implementation."
            ),
            target_customer="Series A to C B2B SaaS companies with sales-assisted onboarding and lean customer success teams.",
            business_model="SaaS subscription with pilot onboarding fee and recurring platform seats.",
            market_context=(
                "PLG and hybrid sales-led SaaS companies are under pressure to improve activation, expansion, and support efficiency."
            ),
            stage="mvp",
            traction_summary="Five design partners, two paying pilots, and an early 18 percent improvement in time-to-value.",
            monthly_revenue=4500,
            monthly_burn=18000,
            runway_months=10,
            team_size=3,
            founder=FounderProfileInput(
                name="Aarav Mehta",
                role="CEO and product lead",
                years_experience=9,
                domain_expertise="B2B SaaS onboarding, customer success, and product-led growth",
                previous_startup_exits=0,
                technical_strength=7,
                go_to_market_strength=8,
            ),
        )

    def run_analysis(self, request: WarRoomRequest) -> WarRoomResponse:
        routing = build_routing_plan(request)
        state = WarRoomState(request=request, routing=routing)

        specialist_findings = [
            run_planner_agent(request, self.knowledge_base),
            run_founder_profile_agent(request, self.knowledge_base),
            run_market_agent(request, self.knowledge_base),
            run_product_agent(request, self.knowledge_base),
            run_gtm_agent(request, self.knowledge_base),
            run_finance_agent(request, self.knowledge_base),
            run_risk_agent(request, self.knowledge_base),
            run_compliance_agent(request, self.knowledge_base),
        ]
        state.agent_findings.extend(specialist_findings)

        scorecard = calculate_readiness_score(request)
        failure_risks = predict_failure_risks(request, scorecard)
        scenarios = run_simulations(request, scorecard)

        critic_finding = run_critic_agent(request, scorecard, specialist_findings)
        decision_finding, recommendation = run_decision_agent(
            request,
            scorecard,
            failure_risks,
            self.knowledge_base,
        )
        report_finding, executive_summary = run_report_agent(
            request,
            scorecard,
            recommendation,
            specialist_findings + [critic_finding, decision_finding],
            failure_risks,
        )

        state.agent_findings.extend([critic_finding, decision_finding, report_finding])

        debate = build_debate(state.agent_findings, scorecard, recommendation)
        citations = _collect_citations(state.agent_findings)

        session_id = f"session_{uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc).isoformat()
        response = WarRoomResponse(
            session_id=session_id,
            created_at=created_at,
            request=request,
            executive_summary=executive_summary,
            routing=routing,
            agent_findings=state.agent_findings,
            debate=debate,
            scorecard=scorecard,
            failure_risks=failure_risks,
            scenarios=scenarios,
            recommendation=recommendation,
            citations=citations,
        )
        self.sessions[session_id] = response
        logger.info("Created FounderGPT session %s for %s", session_id, request.startup_name)
        return response

    def get_session(self, session_id: str) -> WarRoomResponse | None:
        return self.sessions.get(session_id)


def _collect_citations(agent_findings: list[object]) -> list[Citation]:
    seen: set[tuple[str, str]] = set()
    citations: list[Citation] = []
    for finding in agent_findings:
        for citation in finding.citations:
            key = (citation.source, citation.title)
            if key in seen:
                continue
            seen.add(key)
            citations.append(citation)
    return citations


_service = WarRoomService()


def get_war_room_service() -> WarRoomService:
    return _service

