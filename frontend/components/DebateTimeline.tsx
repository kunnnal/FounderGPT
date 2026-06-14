import type { DebateTurn } from "@/lib/types";

type DebateTimelineProps = {
  debate: DebateTurn[];
};

export function DebateTimeline({ debate }: DebateTimelineProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Debate</p>
          <h2 className="section-title">How the agents challenged each other</h2>
        </div>
      </div>
      <div className="timeline">
        {debate.map((turn, index) => (
          <article className="timeline-item" key={`${turn.speaker}-${index}`}>
            <strong>
              {turn.speaker} to {turn.counterparty} · {turn.stance}
            </strong>
            <p className="muted">{turn.message}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

