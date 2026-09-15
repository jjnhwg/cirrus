Build a minimal web app called Cirrus. One page, no auth,
no database yet.

CONCEPT (context for you, don't put this in the UI)
Everyone has negative thoughts. The difference is whether
you grab them or let them pass. The app reads a moment
someone logged and shows them the pattern in how they
explained it. Visually, thoughts are clouds. What changes
is ALTITUDE, never "good vs bad":

- low = fog you're standing inside (a loop: asking again,
  checking, can't move on until it's resolved)
- high = cirrus drifting past (they noticed the thought
  and kept living)
  Never render a thought as a storm because its content is
  dark. Content never sets the weather. Only the pattern does.

STACK
Next.js (App Router) + TypeScript + Tailwind. One page at /,
one API route at /api/read. Anthropic SDK, model
claude-sonnet-4-6. Key from ANTHROPIC_API_KEY in .env.local.

THE PAGE — three states, no routing

1. INPUT
   Two textareas stacked:
   - "What happened?"
     placeholder: "She mentioned a trip she took before we met."
   - "What did you tell yourself about it?"
     placeholder: "I'm never going to see her the same way."
     Button: "Let it pass". Disabled until both have text.

2. LOADING
   Slow drifting cloud animation. Calm, not a spinner.

3. RESULT
   Render from the API response:
   - quoted_phrase large, in quotes, serif
   - label as one line under it
   - explanation paragraph
   - predictions as two lines with arrows
   - suggestion in a bordered box
     The background reflects `altitude` (0-1): near 0 is low,
     dense, close fog; near 1 is high thin wisps against open
     sky. Animate the transition in over ~1.5s.
     Two buttons: "Sounds like me" / "Not really" —
     console.log the choice, then show "Log another" to reset.

API ROUTE
POST /api/read takes { event, thought }. Calls Anthropic
with the system prompt below, max_tokens 1000. Strip ```
fences if present, parse JSON, return it. try/catch, and on
failure return 500 with a plain message shown on the page.

## SYSTEM PROMPT (use verbatim)

You analyze how a person explained a moment to themselves.
You are not a therapist. You never diagnose, never reassure,
and never answer questions about the person's character.

Decide the mode:

- "lens" — they interpreted an event through a belief
- "loop" — they are seeking certainty or relief: asking
  again, checking, re-reviewing, or saying they can't move
  on until they resolve something

Return ONLY valid JSON, no markdown, no preamble:

{
"mode": "lens" | "loop",
"altitude": 0.0-1.0,
"quoted_phrase": "2-5 words copied VERBATIM from their
text that reveal the pattern",
"label": "one short line naming the pattern, e.g.
'One event, treated as a permanent rule.'",
"explanation": "2-3 sentences. Point at their exact words.
Plain language, no jargon, no therapy-speak. Do not
comfort them. Do not tell them the nicer reading is true.",
"predictions": [
"where this same pattern likely shows up in their work
or goals, written as a sentence they might say",
"where it likely shows up in how they see themselves,
written as a sentence they might say"
],
"suggestion": "one concrete action, under 20 words,
something they DO"
}

Rules:

- altitude reflects how caught they are, NOT how dark the
  thought is. A bleak thought they noticed and moved past
  is high. A mild thought they've circled for hours is low.
  Loops are always below 0.35.
- If mode is "loop", the suggestion must NOT involve
  analyzing, examining, or resolving the thought. Suggest
  delay, logging it, or acting without resolving it.
- If they ask for a verdict ("am I a bad person", "what
  does this say about me", "does this mean I don't love
  her"), do not answer it. In `explanation`, name the jump
  from one action to a claim about who they are.
- quoted_phrase must appear word-for-word in their input.

---

STYLING
Soft sky palette: pale blues, warm greys, off-white. No
black. Generous whitespace, large serif for quoted_phrase,
clean sans for everything else. Mobile-first, max-width
~600px centered. Everything moves slowly — no snappy
transitions anywhere.
