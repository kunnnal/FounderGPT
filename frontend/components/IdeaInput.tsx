import type { FounderProfileInput, WarRoomRequest } from "@/lib/types";

type IdeaInputProps = {
  value: WarRoomRequest;
  onFieldChange: (
    field: keyof Omit<WarRoomRequest, "founder">,
    nextValue: string | number,
  ) => void;
  onFounderFieldChange: (
    field: keyof FounderProfileInput,
    nextValue: string | number,
  ) => void;
  onLoadDemo: () => void;
  onSubmit: () => void;
  isSubmitting: boolean;
  isLoadingDemo: boolean;
  error?: string | null;
};

const stageOptions: Array<WarRoomRequest["stage"]> = [
  "idea",
  "validation",
  "mvp",
  "pilot",
  "growth",
];

export function IdeaInput({
  value,
  onFieldChange,
  onFounderFieldChange,
  onLoadDemo,
  onSubmit,
  isSubmitting,
  isLoadingDemo,
  error,
}: IdeaInputProps) {
  return (
    <section className="card">
      <div className="section-head">
        <div>
          <p className="pill">Founder Intake</p>
          <h2 className="section-title">Describe the startup clearly</h2>
        </div>
        <div className="action-row">
          <button
            className="button secondary"
            onClick={onLoadDemo}
            type="button"
            disabled={isLoadingDemo}
          >
            {isLoadingDemo ? "Loading demo..." : "Load demo"}
          </button>
          <button
            className="button"
            onClick={onSubmit}
            type="button"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Running war room..." : "Run war room"}
          </button>
        </div>
      </div>

      <div className="form-grid">
        <div className="field">
          <label htmlFor="startup_name">Startup name</label>
          <input
            className="input"
            id="startup_name"
            value={value.startup_name}
            onChange={(event) =>
              onFieldChange("startup_name", event.target.value)
            }
          />
        </div>
        <div className="field">
          <label htmlFor="stage">Stage</label>
          <select
            className="select"
            id="stage"
            value={value.stage}
            onChange={(event) => onFieldChange("stage", event.target.value)}
          >
            {stageOptions.map((stage) => (
              <option key={stage} value={stage}>
                {stage}
              </option>
            ))}
          </select>
        </div>

        <div className="field-wide">
          <label htmlFor="one_line_pitch">One-line pitch</label>
          <textarea
            className="textarea"
            id="one_line_pitch"
            value={value.one_line_pitch}
            onChange={(event) =>
              onFieldChange("one_line_pitch", event.target.value)
            }
          />
        </div>

        <div className="field-wide">
          <label htmlFor="problem">Problem</label>
          <textarea
            className="textarea"
            id="problem"
            value={value.problem}
            onChange={(event) => onFieldChange("problem", event.target.value)}
          />
        </div>

        <div className="field-wide">
          <label htmlFor="solution">Solution</label>
          <textarea
            className="textarea"
            id="solution"
            value={value.solution}
            onChange={(event) => onFieldChange("solution", event.target.value)}
          />
        </div>

        <div className="field-wide">
          <label htmlFor="target_customer">Target customer</label>
          <textarea
            className="textarea"
            id="target_customer"
            value={value.target_customer}
            onChange={(event) =>
              onFieldChange("target_customer", event.target.value)
            }
          />
        </div>

        <div className="field-wide">
          <label htmlFor="business_model">Business model</label>
          <textarea
            className="textarea"
            id="business_model"
            value={value.business_model}
            onChange={(event) =>
              onFieldChange("business_model", event.target.value)
            }
          />
        </div>

        <div className="field-wide">
          <label htmlFor="market_context">Market context</label>
          <textarea
            className="textarea"
            id="market_context"
            value={value.market_context}
            onChange={(event) =>
              onFieldChange("market_context", event.target.value)
            }
          />
        </div>

        <div className="field-wide">
          <label htmlFor="traction_summary">Traction summary</label>
          <textarea
            className="textarea"
            id="traction_summary"
            value={value.traction_summary}
            onChange={(event) =>
              onFieldChange("traction_summary", event.target.value)
            }
          />
        </div>

        <div className="field">
          <label htmlFor="monthly_revenue">Monthly revenue</label>
          <input
            className="input"
            id="monthly_revenue"
            type="number"
            value={value.monthly_revenue}
            onChange={(event) =>
              onFieldChange("monthly_revenue", Number(event.target.value))
            }
          />
        </div>
        <div className="field">
          <label htmlFor="monthly_burn">Monthly burn</label>
          <input
            className="input"
            id="monthly_burn"
            type="number"
            value={value.monthly_burn}
            onChange={(event) =>
              onFieldChange("monthly_burn", Number(event.target.value))
            }
          />
        </div>
        <div className="field">
          <label htmlFor="runway_months">Runway months</label>
          <input
            className="input"
            id="runway_months"
            type="number"
            value={value.runway_months}
            onChange={(event) =>
              onFieldChange("runway_months", Number(event.target.value))
            }
          />
        </div>
        <div className="field">
          <label htmlFor="team_size">Team size</label>
          <input
            className="input"
            id="team_size"
            type="number"
            value={value.team_size}
            onChange={(event) =>
              onFieldChange("team_size", Number(event.target.value))
            }
          />
        </div>

        <div className="field">
          <label htmlFor="founder_name">Founder name</label>
          <input
            className="input"
            id="founder_name"
            value={value.founder.name}
            onChange={(event) =>
              onFounderFieldChange("name", event.target.value)
            }
          />
        </div>
        <div className="field">
          <label htmlFor="founder_role">Role</label>
          <input
            className="input"
            id="founder_role"
            value={value.founder.role}
            onChange={(event) =>
              onFounderFieldChange("role", event.target.value)
            }
          />
        </div>
        <div className="field">
          <label htmlFor="years_experience">Years experience</label>
          <input
            className="input"
            id="years_experience"
            type="number"
            value={value.founder.years_experience}
            onChange={(event) =>
              onFounderFieldChange(
                "years_experience",
                Number(event.target.value),
              )
            }
          />
        </div>
        <div className="field">
          <label htmlFor="previous_startup_exits">Previous exits</label>
          <input
            className="input"
            id="previous_startup_exits"
            type="number"
            value={value.founder.previous_startup_exits}
            onChange={(event) =>
              onFounderFieldChange(
                "previous_startup_exits",
                Number(event.target.value),
              )
            }
          />
        </div>
        <div className="field">
          <label htmlFor="technical_strength">Technical strength /10</label>
          <input
            className="input"
            id="technical_strength"
            type="number"
            min={1}
            max={10}
            value={value.founder.technical_strength}
            onChange={(event) =>
              onFounderFieldChange(
                "technical_strength",
                Number(event.target.value),
              )
            }
          />
        </div>
        <div className="field">
          <label htmlFor="go_to_market_strength">GTM strength /10</label>
          <input
            className="input"
            id="go_to_market_strength"
            type="number"
            min={1}
            max={10}
            value={value.founder.go_to_market_strength}
            onChange={(event) =>
              onFounderFieldChange(
                "go_to_market_strength",
                Number(event.target.value),
              )
            }
          />
        </div>
        <div className="field-wide">
          <label htmlFor="domain_expertise">Domain expertise</label>
          <textarea
            className="textarea"
            id="domain_expertise"
            value={value.founder.domain_expertise}
            onChange={(event) =>
              onFounderFieldChange("domain_expertise", event.target.value)
            }
          />
        </div>
      </div>

      {error ? <p className="error">{error}</p> : null}
    </section>
  );
}

