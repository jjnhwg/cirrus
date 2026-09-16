import { useState } from "react";

type View = "input" | "loading" | "result";

export default function App() {
  const [view, setView] = useState<View>("input");
  const [event, setEvent] = useState("");
  const [thought, setThought] = useState("");

  const canSubmit = event.trim().length > 0 && thought.trim().length > 0;

  function handleSubmit() {
    if (!canSubmit) return;
    // API call to the FastAPI backend is wired up in a later step.
    setView("loading");
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-[600px] flex-col justify-center px-6 py-16">
      {view === "input" && (
        <section className="flex flex-col gap-8">
          <div className="flex flex-col gap-3">
            <label htmlFor="event" className="text-sm text-warmgrey">
              What happened?
            </label>
            <textarea
              id="event"
              value={event}
              onChange={(e) => setEvent(e.target.value)}
              placeholder="She mentioned a trip she took before we met."
              rows={3}
              className="w-full resize-none rounded-2xl border border-pale bg-white/60 p-4 text-ink transition-colors duration-700 placeholder:text-warmgrey/60 focus:border-sky focus:outline-none"
            />
          </div>

          <div className="flex flex-col gap-3">
            <label htmlFor="thought" className="text-sm text-warmgrey">
              What did you tell yourself about it?
            </label>
            <textarea
              id="thought"
              value={thought}
              onChange={(e) => setThought(e.target.value)}
              placeholder="I'm never going to see her the same way."
              rows={3}
              className="w-full resize-none rounded-2xl border border-pale bg-white/60 p-4 text-ink transition-colors duration-700 placeholder:text-warmgrey/60 focus:border-sky focus:outline-none"
            />
          </div>

          <button
            type="button"
            onClick={handleSubmit}
            disabled={!canSubmit}
            className="self-start rounded-full bg-deep px-8 py-3 text-offwhite transition-all duration-700 hover:bg-ink disabled:cursor-not-allowed disabled:bg-pale disabled:text-warmgrey"
          >
            Let it pass
          </button>
        </section>
      )}

      {view === "loading" && (
        <section className="flex flex-col items-center gap-6 text-warmgrey">
          <p className="text-sm">Reading…</p>
        </section>
      )}

      {view === "result" && (
        <section className="flex flex-col gap-6">
          <p className="text-warmgrey">Result view coming next.</p>
        </section>
      )}
    </main>
  );
}
