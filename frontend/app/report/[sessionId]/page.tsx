type ReportPageProps = {
  params: {
    sessionId: string;
  };
};

export default function ReportPage({ params }: ReportPageProps) {
  return (
    <main>
      <h1>Decision Report</h1>
      <p>Session: {params.sessionId}</p>
    </main>
  );
}

