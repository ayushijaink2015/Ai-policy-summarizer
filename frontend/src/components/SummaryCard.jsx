import React from 'react';

export default function SummaryCard({ filename, status, createdAt, summary }) {
  const statusStyles =
    status === 'completed'
      ? 'bg-emerald-100 text-emerald-700 ring-1 ring-emerald-200'
      : 'bg-rose-100 text-rose-700 ring-1 ring-rose-200';

  return (
    <article className="w-full max-w-3xl rounded-3xl bg-white p-6 shadow-lg shadow-slate-200 transition duration-300 hover:-translate-y-0.5 hover:shadow-xl sm:p-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-900 truncate">{filename}</h2>
          <p className="mt-1 text-sm text-slate-500">{createdAt}</p>
        </div>
        <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${statusStyles}`}>
          {status}
        </span>
      </div>

      <div className="mt-6 rounded-2xl bg-slate-50 p-5 text-slate-700 shadow-sm sm:p-6">
        <h3 className="mb-3 text-sm font-medium uppercase tracking-[0.18em] text-slate-500">Summary</h3>
        <p className="whitespace-pre-wrap break-words text-sm leading-7 text-slate-700">{summary}</p>
      </div>
    </article>
  );
}
