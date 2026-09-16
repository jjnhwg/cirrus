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
