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

---

## Step 4 — POST /api/read with validation

### Q: What is a Pydantic model and how does FastAPI use it?
A: A class subclassing `BaseModel` that declares fields with types
(`event: str`, `thought: str`). When a route takes it as a parameter, FastAPI
parses the request JSON into it and validates types automatically, returning
422 if the body doesn't match — no manual parsing needed.
Tag: concept

### Q: Difference between a 400 and a 422 in this endpoint?
A: 422 is FastAPI/Pydantic rejecting a body of the wrong *shape* (missing field,
wrong type) automatically. 400 is our own rule for a body that's the right shape
but semantically invalid (present but empty/whitespace text).
Tag: learning

### Q: Why check `.strip()` when Pydantic already validated the fields?
A: Pydantic confirms the fields exist and are strings, but `""` or `"   "` are
valid strings. The empty-check is a business rule the type system can't express,
so we enforce it in the handler and raise `HTTPException(400)`.
Tag: learning

### Q: How do you raise an error with a specific status code in FastAPI?
A: `raise HTTPException(status_code=..., detail=...)`. FastAPI turns it into a
JSON response `{"detail": ...}` with that status, instead of crashing.
Tag: concept

### Q: Why build/test the endpoint's validation before adding the AI call?
A: It isolates concerns — you prove request parsing, validation, and status
codes work on their own. When the Anthropic call is added next, any new failure
is clearly from that piece, not the plumbing.
Tag: interview

---

## Step 5 — Load API key + create Anthropic client

### Q: What does `python-dotenv` / `load_dotenv()` do?
A: It reads key=value pairs from a `.env` file and loads them into
`os.environ` at startup, so code can read secrets/config via
`os.environ.get(...)` without hardcoding them in source.
Tag: concept

### Q: Why keep the API key in `.env` and git-ignore it instead of in the code?
A: Secrets in source get committed and leak (especially in public repos).
`.env` keeps the key on the machine only; each environment supplies its own, and
the file is git-ignored so it never enters version control.
Tag: interview

### Q: Why create the `Anthropic()` client once at module load instead of inside the handler?
A: The client is reusable and can hold connection pooling/config. Creating it
once avoids rebuilding it on every request, which is wasteful. Handlers just use
the shared `client`.
Tag: learning

### Q: Does creating the Anthropic client with a bad/placeholder key fail immediately?
A: No — constructing the client just stores the key. Authentication is only
checked when you actually make an API call, which is why this piece is safe to
add before wiring the real request.
Tag: learning

---

## Step 6 — System prompt + the Claude call

### Q: What is the "system prompt" vs the "user message" in a Claude call?
A: The system prompt sets the model's role and rules for the whole conversation
(here: how to analyze the thought and the exact JSON to return). The user
message is the specific input (the event + thought). System = instructions,
user = data.
Tag: concept

### Q: What are the key parameters of `client.messages.create(...)`?
A: `model` (which Claude version), `max_tokens` (cap on the reply length),
`system` (the instructions), and `messages` (the conversation list of
role/content items). It returns a message whose `content` is a list of blocks.
Tag: concept

### Q: Why does `message.content[0].text` get the reply, not just `message`?
A: A response's `content` is a list of typed blocks (text, tool use, etc.). For
a plain text answer the first block is a text block, so `.text` on it is the
actual string the model wrote.
Tag: learning

### Q: Why return the raw model text first instead of parsing immediately?
A: To see exactly what the model produces before trusting it. That revealed
Claude wraps its JSON in ```json fences despite being told not to — which
justifies the next piece: stripping fences before `json.loads`.
Tag: interview

---

## Step 7 — Strip fences + parse JSON

### Q: What does `json.loads()` do?
A: It parses a JSON-formatted *string* into a Python object (a `dict`/`list`).
"loads" = "load string". The reverse, `json.dumps()`, turns a Python object
back into a JSON string.
Tag: concept

### Q: Why must the ``` fences be removed before `json.loads()`?
A: `json.loads` expects the string to be pure JSON. The backtick fence lines
(```json … ```) are not valid JSON, so parsing would raise a
`JSONDecodeError`. Stripping them leaves only the object to parse.
Tag: learning

### Q: How does the fence-stripping code work?
A: If the text starts with ```` ``` ````, `split("\n", 1)[-1]` drops the first
line (the opening fence), and `rsplit("```", 1)[0]` drops everything from the
final ```` ``` ````. `.strip()` cleans up whitespace. If there are no fences it
leaves the text untouched.
Tag: learning

### Q: Once `read()` returns a Python dict, how does the client get JSON?
A: FastAPI automatically serializes the returned dict to a JSON HTTP response
(with the right content-type). So returning `reading` (a dict) sends structured
JSON to the caller — no manual `json.dumps` needed.
Tag: concept

### Q: What's still fragile about this parsing step right now?
A: If the model ever returns non-JSON or malformed JSON, `json.loads` raises and
crashes the request. That's why the next piece wraps it in try/except to return
a clean 500 instead.
Tag: interview

---

## Step 8 — Error handling (try/except → 500)

### Q: How does try/except work in Python?
A: Code in the `try` block runs normally; if it raises an exception, execution
jumps to the matching `except` block instead of crashing. It lets you handle
failure paths deliberately.
Tag: concept

### Q: Why is the 400 validation kept OUTSIDE the try/except?
A: The 400 is a deliberate rejection of bad input, not an unexpected error. If it
were inside the `try`, the broad `except Exception` would catch it and wrongly
convert it into a 500. Keeping it outside preserves the correct status.
Tag: interview

### Q: What kinds of failures does the try/except here catch?
A: Anything in the Claude call or parsing — a bad/expired API key, a network
error, an Anthropic outage, or a reply that isn't valid JSON
(`JSONDecodeError`). All become one clean 500.
Tag: learning

### Q: Why return a generic message instead of the raw exception to the user?
A: Raw exceptions can leak internal details (stack traces, keys, implementation)
and read as scary. A calm, generic message is safer and on-brand; the real error
can still be logged server-side for debugging.
Tag: interview

### Q: Trade-off of catching broad `except Exception` vs specific exceptions?
A: Broad catching is simple and guarantees no crash, but hides which failure
happened and can mask bugs. Specific excepts (e.g. `JSONDecodeError`, API
errors) give clearer handling/messages at the cost of more code. For one small
endpoint, broad is acceptable.
Tag: learning

---

## Step 9 — CORS

### Q: What is the Same-Origin Policy and what counts as an "origin"?
A: A browser security rule: JS from one origin can't read responses from a
different origin by default. An origin = scheme + host + port
(`http://localhost:5173`), so a different port alone makes it cross-origin.
Tag: concept

### Q: What is CORS and how does the server "allow" a cross-origin request?
A: CORS (Cross-Origin Resource Sharing) lets a server opt in by sending
`Access-Control-Allow-Origin` (and related) headers naming which origins/methods
are permitted. The browser reads those headers and allows or blocks the JS.
Tag: concept

### Q: What does `app.add_middleware(CORSMiddleware, ...)` do in FastAPI?
A: Middleware wraps every request/response. `CORSMiddleware` automatically adds
the correct CORS headers (and answers preflight OPTIONS requests) based on the
allowed origins/methods/headers you configure.
Tag: learning

### Q: Why did the app work through the Vite proxy without CORS, but still add it?
A: The dev proxy makes browser calls look same-origin (all via :5173), so CORS
wasn't triggered. Adding it lets the backend be called directly and is required
in production where frontend and backend are truly different origins.
Tag: interview

### Q: Why restrict `allow_origins` to a specific origin instead of `*`?
A: `*` allows any site to call your API from a browser. Naming only the trusted
frontend origin is a least-privilege security choice that limits who can invoke
it cross-origin.
Tag: interview








