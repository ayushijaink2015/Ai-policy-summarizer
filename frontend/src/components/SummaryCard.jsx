import React from 'react';

export default function SummaryCard({ summary }) {
  if (!summary) {
    return <div>No summary available</div>;
  }

  return (
    <div className="summary-card">
      <h2>Summary</h2>
      <p>{summary}</p>
    </div>
  );
}
