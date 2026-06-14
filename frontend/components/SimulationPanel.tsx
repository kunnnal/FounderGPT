import type { ScenarioResult } from "@/lib/types";

type SimulationPanelProps = {
  scenarios: ScenarioResult[];
};

export function SimulationPanel({ scenarios }: SimulationPanelProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Simulation</p>
          <h2 className="section-title">What-if scenarios</h2>
        </div>
      </div>
      <div className="scenario-grid">
        {scenarios.map((scenario) => (
          <article className="scenario-card" key={scenario.name}>
            <strong>{scenario.name}</strong>
            <p className="muted">{scenario.assumption}</p>
            <p>{scenario.outcome}</p>
            <div className="pill">Impact {scenario.impact_score}</div>
          </article>
        ))}
      </div>
    </section>
  );
}

