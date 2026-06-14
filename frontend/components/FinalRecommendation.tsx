import type { Recommendation } from "@/lib/types";

type FinalRecommendationProps = {
  recommendation: Recommendation;
  executiveSummary: string;
};

export function FinalRecommendation({
  recommendation,
  executiveSummary,
}: FinalRecommendationProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Decision</p>
          <h2 className="section-title">{recommendation.decision}</h2>
        </div>
        <div className="summary-card">
          <div className="muted">Confidence</div>
          <div className="metric-value">{recommendation.confidence}</div>
        </div>
      </div>
      <p>{executiveSummary}</p>
      <p className="muted">{recommendation.rationale}</p>
      <div className="summary-grid">
        <article className="summary-card">
          <strong>Milestones</strong>
          <ul className="list">
            {recommendation.milestones.map((milestone) => (
              <li key={milestone}>{milestone}</li>
            ))}
          </ul>
        </article>
        <article className="summary-card">
          <strong>Investor readiness</strong>
          <p className="muted">{recommendation.investor_readiness}</p>
        </article>
      </div>
    </section>
  );
}

