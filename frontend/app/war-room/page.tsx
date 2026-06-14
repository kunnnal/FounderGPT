"use client";

import Link from "next/link";
import { startTransition, useState } from "react";

import { IdeaInput } from "@/components/IdeaInput";
import { WarRoomResults } from "@/components/WarRoomResults";
import { analyzeWarRoom, getDemoRequest } from "@/lib/api";
import { defaultWarRoomRequest } from "@/lib/defaults";
import type { FounderProfileInput, WarRoomRequest, WarRoomResponse } from "@/lib/types";

export default function WarRoomPage() {
  const [request, setRequest] = useState<WarRoomRequest>(defaultWarRoomRequest);
  const [result, setResult] = useState<WarRoomResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingDemo, setIsLoadingDemo] = useState(false);

  function updateField(
    field: keyof Omit<WarRoomRequest, "founder">,
    nextValue: string | number,
  ) {
    setRequest((current) => ({
      ...current,
      [field]: nextValue,
    }));
  }

  function updateFounderField(
    field: keyof FounderProfileInput,
    nextValue: string | number,
  ) {
    setRequest((current) => ({
      ...current,
      founder: {
        ...current.founder,
        [field]: nextValue,
      },
    }));
  }

  async function handleRunAnalysis() {
    setError(null);
    setIsSubmitting(true);
    try {
      const response = await analyzeWarRoom(request);
      startTransition(() => {
        setResult(response);
      });
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "The war room request failed.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleLoadDemo() {
    setError(null);
    setIsLoadingDemo(true);
    try {
      const payload = await getDemoRequest();
      setRequest(payload.request);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Demo payload could not be loaded.",
      );
    } finally {
      setIsLoadingDemo(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-card">
          <p className="hero-badge">War Room</p>
          <h1>Run the founder idea through specialist agents.</h1>
          <p>
            Start with the demo payload or replace it with your own idea. The
            backend will generate a structured decision report with scores,
            risks, and next steps.
          </p>
          <div className="hero-actions">
            <Link className="button secondary" href="/">
              Back home
            </Link>
          </div>
        </div>
      </section>

      <div style={{ maxWidth: 840, margin: "0 auto", width: "100%" }}>
        <IdeaInput
          value={request}
          onFieldChange={updateField}
          onFounderFieldChange={updateFounderField}
          onLoadDemo={handleLoadDemo}
          onSubmit={handleRunAnalysis}
          isSubmitting={isSubmitting}
          isLoadingDemo={isLoadingDemo}
          error={error}
        />
      </div>

      <section className="stack" style={{ marginTop: 24 }}>
        {result ? (
          <WarRoomResults session={result} />
        ) : (
          <div className="empty-state">
            Run the war room to generate a full founder report. The result will
            appear here and can be reopened on the report route.
          </div>
        )}
      </section>

      <div className="grid-two" style={{ gridTemplateColumns: "1fr 1fr", borderTop: "1px solid var(--border)", paddingTop: 32, marginTop: 48 }}>
        <article style={{ padding: "12px 0" }}>
          <p className="pill">Valuation Engine</p>
          <h2 className="section-title">Comprehensive Insights</h2>
          <ul className="list">
            <li>Readiness Index: Computes a standardized venture readiness score across core business variables.</li>
            <li>Risk Forecasting: Predicts execution bottlenecks, financial runaways, and target segment errors.</li>
            <li>Scenario Stress Tests: Employs heuristic-based simulations to evaluate business model durability.</li>
          </ul>
        </article>
        <article style={{ padding: "12px 0" }}>
          <p className="pill">Methodology</p>
          <h2 className="section-title">Analysis Pipeline</h2>
          <ul className="list">
            <li>Multi-Role Assessment: Reviews ideas across market, finance, GTM, and compliance domains.</li>
            <li>Debated Synthesis: Simulates a timeline debate to reconcile agent findings and uncover bias.</li>
            <li>Actionable Roadmap: Packages the output into next steps, milestones, and investor reports.</li>
          </ul>
        </article>
      </div>
    </main>
  );
}

