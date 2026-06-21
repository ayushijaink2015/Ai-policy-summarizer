import { useEffect, useState } from "react";
import { getSummaries } from "../services/api";

export default function HistoryPage() {
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSummaries() {
      setLoading(true);
      setError("");

      try {
        const response = await getSummaries();
        setSummaries(response || []);
      } catch (err) {
        console.error("Failed to load summaries:", err);
        setError("Unable to fetch summary history.");
      } finally {
        setLoading(false);
      }
    }

    fetchSummaries();
  }, []);

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8 rounded-3xl bg-white p-8 shadow-xl shadow-slate-200">
          <h1 className="text-3xl font-semibold text-slate-900 sm:text-4xl">Summary History</h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-500 sm:text-base">
            Review previously generated policy summaries with status and creation timestamps.
          </p>
        </div>

        {loading ? (
          <div className="rounded-3xl bg-white p-10 text-center shadow-lg shadow-slate-200">
            <div className="mx-auto mb-6 h-14 w-14 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />
            <p className="text-base font-medium text-slate-700">Loading summaries...</p>
          </div>
        ) : error ? (
          <div className="rounded-3xl bg-white p-8 text-center text-red-700 shadow-lg shadow-slate-200">
            {error}
          </div>
        ) : summaries.length === 0 ? (
          <div className="rounded-3xl bg-white p-10 text-center text-slate-700 shadow-lg shadow-slate-200">
            No summaries found.
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {summaries.map((item) => (
              <div
                key={item.id || `${item.filename}-${item.created_at}`}
                className="rounded-3xl bg-white p-6 shadow-lg shadow-slate-200 transition hover:-translate-y-0.5 hover:shadow-xl"
              >
                <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                  <div>
                    <h2 className="text-lg font-semibold text-slate-900 truncate">{item.filename}</h2>
                    <p className="mt-1 text-sm text-slate-500">{item.created_at}</p>
                  </div>
                  <span
                    className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${
                      item.status === "completed"
                        ? "bg-emerald-100 text-emerald-700"
                        : "bg-rose-100 text-rose-700"
                    }`}
                  >
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
