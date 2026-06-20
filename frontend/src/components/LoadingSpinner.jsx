export default function LoadingSpinner() {
  return (
    <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-xl shadow-slate-200">
      <div className="flex flex-col items-center gap-6 text-center">
        <div className="h-20 w-20 rounded-full border-4 border-blue-100 border-t-blue-500 animate-spin" />
        <div>
          <p className="text-lg font-semibold text-slate-900">Generating summary...</p>
          <p className="mt-2 text-sm text-slate-500">
            Please wait while we analyze your document.
          </p>
        </div>
      </div>
    </div>
  );
}
