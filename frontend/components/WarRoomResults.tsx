import Link from "next/link";

import type { WarRoomResponse } from "@/lib/types";
import { AgentPanel } from "@/components/AgentPanel";
import { DebateTimeline } from "@/components/DebateTimeline";
import { FinalRecommendation } from "@/components/FinalRecommendation";
import { RiskMatrix } from "@/components/RiskMatrix";
import { ScoreCard } from "@/components/ScoreCard";
import { SimulationPanel } from "@/components/SimulationPanel";

type WarRoomResultsProps = {
  session: WarRoomResponse;
};

export function WarRoomResults({ session }: WarRoomResultsProps) {
  return (
    <section className="stack">
      <div className="status-row">
        <div className="pill">Session {session.session_id}</div>
        <Link className="inline-link" href={`/report/${session.session_id}`}>
          Open standalone report
        </Link>
      </div>
      <FinalRecommendation
        recommendation={session.recommendation}
        executiveSummary={session.executive_summary}
      />
      <ScoreCard scorecard={session.scorecard} />
      <div className="grid-two">
        <RiskMatrix risks={session.failure_risks} />
        <SimulationPanel scenarios={session.scenarios} />
      </div>
      <DebateTimeline debate={session.debate} />
      <AgentPanel findings={session.agent_findings} />
    </section>
  );
}
