import UploadForm from "../components/UploadForm";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="w-full rounded-[2rem] bg-white/95 shadow-2xl shadow-indigo-900/20 backdrop-blur-xl ring-1 ring-white/10 lg:p-12">
          <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
            <div className="space-y-6 px-6 py-8 lg:px-10">
              <div className="inline-flex rounded-full bg-indigo-100/90 px-4 py-2 text-sm font-semibold text-indigo-700 shadow-sm shadow-indigo-300/20 ring-1 ring-indigo-100">
                AI Policy Summarizer
              </div>

              <div className="space-y-4">
                <h1 className="text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
                  Simplify government policies using AI
                </h1>
                <p className="max-w-xl text-base leading-8 text-slate-600 sm:text-lg">
                  Upload any PDF policy document and get a concise, readable summary instantly. Built with modern AI workflows for fast policy understanding.
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-3xl border border-slate-200/80 bg-gradient-to-br from-slate-50 via-white to-indigo-50 p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg hover:shadow-indigo-300/20">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-indigo-700">Fast uploads</p>
                  <p className="mt-2 text-sm text-slate-600">Drop PDFs and generate summaries in seconds.</p>
                </div>
                <div className="rounded-3xl border border-slate-200/80 bg-gradient-to-br from-slate-50 via-white to-indigo-50 p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-lg hover:shadow-indigo-300/20">
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-indigo-700">AI-powered clarity</p>
                  <p className="mt-2 text-sm text-slate-600">Turn dense policy text into easy-to-read summaries.</p>
                </div>
              </div>
            </div>

            <div className="mx-auto max-w-xl px-6 pb-8 pt-6 sm:px-8 lg:px-10">
              <div className="rounded-[1.75rem] border border-slate-200/80 bg-slate-950/95 p-8 shadow-2xl shadow-slate-950/20 ring-1 ring-white/10 backdrop-blur-xl">
                <div className="mb-6 rounded-3xl bg-gradient-to-r from-indigo-500 via-blue-500 to-sky-500 p-1 shadow-lg shadow-indigo-500/20">
                  <div className="rounded-3xl bg-slate-950 px-5 py-4 text-center text-white">
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-200">Upload your policy</p>
                    <h2 className="mt-2 text-2xl font-semibold">Start with a PDF</h2>
                  </div>
                </div>
                <div className="rounded-3xl bg-slate-900/95 px-5 py-6 shadow-inner shadow-slate-950/10">
                  <UploadForm />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
