import type { FailureRisk } from "@/lib/types";

type RiskMatrixProps = {
  risks: FailureRisk[];
};

export function RiskMatrix({ risks }: RiskMatrixProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Risk</p>
          <h2 className="section-title">Top failure risks</h2>
        </div>
      </div>
      <div className="risk-grid">
        {risks.map((risk) => (
          <article className="risk-item" key={risk.risk}>
            <strong>{risk.risk}</strong>
            <div className="risk-meta">
              <span>{risk.probability}% probability</span>
              <span>{risk.severity} severity</span>
            </div>
            <p className="muted">{risk.mitigation}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

