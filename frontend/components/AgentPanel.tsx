import type { AgentFinding } from "@/lib/types";

type AgentPanelProps = {
  findings: AgentFinding[];
};

export function AgentPanel({ findings }: AgentPanelProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Agents</p>
          <h2 className="section-title">Specialist findings</h2>
        </div>
      </div>
      <div className="agent-grid">
        {findings.map((finding) => (
          <article className="agent-card" key={finding.agent}>
            <strong>
              {finding.agent.replace(/_/g, " ")} · {finding.verdict}
            </strong>
            <p className="muted">{finding.summary}</p>
            <ul className="list">
              {finding.strengths.slice(0, 2).map((point) => (
                <li key={`${finding.agent}-strength-${point}`}>{point}</li>
              ))}
            </ul>
            <ul className="list">
              {finding.concerns.slice(0, 2).map((point) => (
                <li key={`${finding.agent}-concern-${point}`}>{point}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}

