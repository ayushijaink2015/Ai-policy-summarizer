import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/70 bg-slate-950/95 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="text-lg font-semibold text-white">
          AI Policy Summarizer
        </Link>

        <nav className="flex items-center gap-3">
          <Link
            to="/"
            className="rounded-full bg-slate-900/90 px-4 py-2 text-sm font-medium text-slate-100 transition hover:bg-slate-800"
          >
            Home
          </Link>
          <Link
            to="/history"
            className="rounded-full bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-indigo-500"
          >
            History
          </Link>
        </nav>
      </div>
    </header>
  );
}
