import { useEffect, useState } from "react";
import { getSummaries } from "../services/api"; // Adjust path if needed

export default function HistoryPage() {
  const [summaries, setSummaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

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

  const filteredSummaries = summaries.filter((item) =>
    (item.filename || "")
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
  );

  return (
  <main className="min-h-screen bg-slate-100 px-4 py-10 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-6xl">
      {/* Header */}
      <div className="mb-8 rounded-3xl bg-white p-8 shadow-xl shadow-slate-200">
        <h1 className="text-3xl font-semibold text-slate-900 sm:text-4xl">
          Summary History
        </h1>
        <p className="mt-3 max-w-2xl text-sm text-slate-500 sm:text-base">
          Review previously generated policy summaries with status and creation
          timestamps.
        </p>
      </div>

      {/* Search Box */}
      {!loading && !error && summaries.length > 0 && (
        <input
          type="text"
          placeholder="🔍 Search by filename..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="mb-6 w-full rounded-xl border border-slate-300 bg-white p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      )}

      {/* Loading */}
      {loading ? (
        <div className="rounded-3xl bg-white p-10 text-center shadow-lg shadow-slate-200">
          <div className="mx-auto mb-6 h-14 w-14 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600"></div>
          <p className="text-base font-medium text-slate-700">
            Loading summaries...
          </p>
        </div>
      ) : error ? (
        /* Error */
        <div className="rounded-3xl bg-white p-8 text-center text-red-700 shadow-lg shadow-slate-200">
          {error}
        </div>
      ) : summaries.length === 0 ? (
        /* No summaries */
        <div className="rounded-3xl bg-white p-10 text-center text-slate-700 shadow-lg shadow-slate-200">
          No summaries found.
        </div>
      ) : filteredSummaries.length === 0 ? (
        /* Search returned nothing */
        <div className="rounded-3xl bg-white p-10 text-center text-slate-700 shadow-lg shadow-slate-200">
          No matching summaries found.
        </div>
      ) : (
        /* Summary Table */
        <div className="overflow-x-auto rounded-3xl bg-white shadow-lg shadow-slate-200">
          <table className="w-full">
            <thead className="bg-blue-600 text-white">
              <tr>
                <th className="p-4 text-left">Filename</th>
                <th className="p-4 text-left">Status</th>
                <th className="p-4 text-left">Created At</th>
              </tr>
            </thead>

            <tbody>
              {filteredSummaries.map((item) => (
                <tr
                  key={item.id}
                  className="border-b border-slate-200 hover:bg-slate-50"
                >
                  <td className="p-4">{item.filename}</td>

                  <td className="p-4">
                    <span
                      className={`rounded-full px-3 py-1 text-sm text-white ${
                        item.status === "completed"
                          ? "bg-green-500"
                          : "bg-red-500"
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>

                  <td className="p-4 text-slate-600">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  </main>
);
}