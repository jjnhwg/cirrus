# Flashcards

Spaced-repetition style notes for Cirrus. Grouped loosely by build step.

---

## Step 1 — Scaffold + Input state

### Q: What is the Next.js App Router and how does the file system define routes?
A: In the App Router, folders under `app/` become URL routes and a `page.tsx`
inside a folder is the page for that route. `app/page.tsx` is the site root
`/`. `layout.tsx` wraps every page below it. No manual route config needed.
Tag: concept

### Q: What's the difference between a Server Component and a Client Component in Next.js?
A: Components are Server Components by default (rendered on the server, no
browser JS, can't use state/effects). Adding `"use client"` at the top makes it
a Client Component that ships JS and can use `useState`, event handlers, etc.
`Home()` needs `"use client"` because it tracks textarea state.
Tag: concept

### Q: Why is `canSubmit` derived on each render instead of stored in state?
A: It's fully computed from `event` and `thought`. Storing it separately would
risk it going stale or out of sync. Derived values should be recomputed, not
duplicated in state.
Tag: learning

### Q: Why scaffold Next.js manually instead of using `create-next-app`?
A: `create-next-app` refuses to run in a non-empty folder (we already had
`prompt.md`, `.git`, etc.), and doing it by hand shows exactly what each config
file (`tsconfig`, `postcss.config`, `next.config`) is responsible for.
Tag: learning

### Q: How does Tailwind v4 get wired into the project?
A: A single `@import "tailwindcss";` in `globals.css`, plus the
`@tailwindcss/postcss` plugin in `postcss.config.mjs`. The theme (custom sky
colors) is declared with `@theme inline` in CSS — no `tailwind.config.js`
needed in v4.
Tag: concept

### Q: A recruiter asks how you kept the UI calm and on-brand. What do you say?
A: I defined a constrained sky palette as CSS variables (pale blues, warm
greys, off-white, no pure black) and exposed them to Tailwind via `@theme`, so
every component pulls from the same tokens. Transitions are all long
(~700ms) by default to match the "let the thought drift past" concept.
Tag: interview

### Q: Why disable the submit button until both fields have text?
A: It's a boundary check at the UI level — it prevents sending an incomplete
"moment" to the model and gives the user a clear signal that both halves
(the event and their interpretation) matter to the reading.
Tag: interview

---

## Step 2 — `/api/read` route

### Q: What is a Next.js Route Handler and how do you make one?
A: A file named `route.ts` inside `app/api/.../` that exports functions named
after HTTP verbs (`GET`, `POST`, …). Exporting `POST` creates a POST endpoint
at that folder's path. It runs on the server, so secrets like API keys are safe
there.
Tag: concept

### Q: Why must the Anthropic call live in an API route instead of the browser?
A: The API key must never ship to the client. Route Handlers run server-side,
so `process.env.ANTHROPIC_API_KEY` stays on the server and is never exposed in
network responses or bundled JS.
Tag: interview

### Q: Why strip ``` fences from the model's reply before `JSON.parse`?
A: LLMs often wrap JSON in a markdown code block (```json … ```) even when told
not to. `JSON.parse` would throw on those backticks, so we remove them first to
make parsing robust.
Tag: learning

### Q: How does `.env.local` work in Next.js and why is it git-ignored?
A: Next.js auto-loads `.env.local` into `process.env` on the server. It holds
secrets (the API key), so it's git-ignored to keep credentials out of version
control. Each developer supplies their own.
Tag: concept

### Q: Why wrap the whole handler in try/catch and return a 500 with a plain message?
A: Many things can fail — a bad key, a network blip, an unparseable reply. One
try/catch turns all of them into a single calm, user-facing error instead of a
crash or a leaked stack trace, which is both safer and on-brand.
Tag: interview

---

## Step 3 — Python (FastAPI) backend, piece 1

### Q: Why move the backend to a separate Python service instead of a Next.js route?
A: It splits the app into a frontend (Next.js) and an independent API (FastAPI)
that can be developed, run, and deployed on its own. The frontend just calls it
over HTTP. Trade-off: more moving parts (two servers, CORS) vs. clearer
separation and using Python's ecosystem.
Tag: interview

### Q: What is a Python virtual environment (venv) and why use one per project?
A: An isolated folder (`.venv`) with its own Python and installed packages, so
each project's dependencies don't collide with other projects or the system
Python. You `activate` it before installing or running.
Tag: concept

### Q: What does FastAPI give you out of the box?
A: An ASGI web framework with routing via decorators (`@app.get(...)`),
automatic JSON serialization of returned dicts, request validation (via
Pydantic), and interactive docs at `/docs`. Great fit for a single JSON API.
Tag: concept

### Q: What is uvicorn and why do you need it to run FastAPI?
A: FastAPI defines the app but doesn't serve HTTP itself. uvicorn is an ASGI
server that actually listens on a port and runs the app (`uvicorn main:app`).
Tag: learning

### Q: Why start the backend with just a `/health` endpoint?
A: It's the smallest possible proof the server boots and responds, before
adding any real logic. Health checks are also standard in production for load
balancers/monitoring to know a service is alive.
Tag: learning


