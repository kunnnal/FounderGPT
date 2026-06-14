import Link from "next/link";

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-card">
          <h1>Pressure-test a startup idea with a multi-agent war room.</h1>
          <p>
            FounderGPT turns one startup brief into specialist analysis, debate,
            scoring, failure risks, simulations, and a founder-facing
            recommendation.
          </p>
          <div className="hero-actions">
            <Link className="button" href="/war-room">
              Open war room
            </Link>
            <a className="button secondary" href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
              Explore API Docs
            </a>
          </div>
        </div>
        <div className="grid-two">
          <article className="card">
            <p className="pill">Core Capabilities</p>
            <h2 className="section-title">Advanced Decision Architecture</h2>
            <ul className="list">
              <li>Deploys specialist agents to analyze GTM, product scope, financial viability, and compliance.</li>
              <li>Runs interactive cross-agent debates to surface hidden assumptions and groupthink risks.</li>
              <li>Synthesizes conflicting feedback into actionable milestones and next steps.</li>
            </ul>
          </article>
          <article className="card">
            <p className="pill">Assessment Flow</p>
            <h2 className="section-title">Intelligent Simulation Suite</h2>
            <ul className="list">
              <li>Stress-test custom startup profiles or launch pre-loaded demo scenarios instantly.</li>
              <li>Access saved analytical briefs with session persistence on standalone reports.</li>
              <li>Run full-spectrum checks in seconds to evaluate venture defensibility.</li>
            </ul>
          </article>
        </div>
      </section>
    </main>
  );
}

