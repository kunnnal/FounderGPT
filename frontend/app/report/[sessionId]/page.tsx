"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { WarRoomResults } from "@/components/WarRoomResults";
import { getSession } from "@/lib/api";
import type { WarRoomResponse } from "@/lib/types";

type ReportPageProps = {
  params: {
    sessionId: string;
  };
};

export default function ReportPage({ params }: ReportPageProps) {
  const [session, setSession] = useState<WarRoomResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadSession() {
      setError(null);
      setIsLoading(true);
      try {
        const response = await getSession(params.sessionId);
        if (active) {
          setSession(response);
        }
      } catch (caughtError) {
        if (active) {
          setError(
            caughtError instanceof Error
              ? caughtError.message
              : "The session could not be loaded.",
          );
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    loadSession();

    return () => {
      active = false;
    };
  }, [params.sessionId]);

  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-card">
          <p className="hero-badge">Decision Report</p>
          <h1>Review a saved founder session.</h1>
          <p>
            This route reopens the stored war-room response using the session
            identifier from the backend memory store.
          </p>
          <div className="hero-actions">
            <Link className="button secondary" href="/war-room">
              Back to war room
            </Link>
          </div>
        </div>
      </section>

      {isLoading ? (
        <div className="empty-state">Loading report...</div>
      ) : null}
      {error ? <div className="empty-state">{error}</div> : null}
      {session ? <WarRoomResults session={session} /> : null}
    </main>
  );
}

