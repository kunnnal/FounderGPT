import type { ScoreCard as ScoreCardType } from "@/lib/types";

type ScoreCardProps = {
  scorecard: ScoreCardType;
};

const metrics = [
  { key: "market", label: "Market" },
  { key: "product", label: "Product" },
  { key: "execution", label: "Execution" },
  { key: "financial", label: "Financial" },
  { key: "defensibility", label: "Defensibility" },
] as const;

export function ScoreCard({ scorecard }: ScoreCardProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Readiness</p>
          <h2 className="section-title">Scorecard</h2>
        </div>
        <div className="summary-card">
          <div className="muted">Recommended stage</div>
          <div className="metric-value">{scorecard.readiness_stage}</div>
        </div>
      </div>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="muted">Overall score</div>
          <div className="metric-value">{scorecard.overall}</div>
        </div>
        <div className="metric-card">
          <div className="muted">Best next use</div>
          <div className="metric-value">Founder demo</div>
        </div>
      </div>

      {metrics.map((metric) => (
        <div className="score-row" key={metric.key}>
          <div className="score-label">
            <span>{metric.label}</span>
            <span>{scorecard[metric.key]}</span>
          </div>
          <div className="score-track">
            <div
              className="score-fill"
              style={{ width: `${scorecard[metric.key]}%` }}
            />
          </div>
        </div>
      ))}
    </section>
  );
}

