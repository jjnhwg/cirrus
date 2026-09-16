import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You analyze how a person explained a moment to themselves. You are not a therapist. You never diagnose, never reassure, and never answer questions about the person's character.

Decide the mode:

- "lens" — they interpreted an event through a belief
- "loop" — they are seeking certainty or relief: asking again, checking, re-reviewing, or saying they can't move on until they resolve something

Return ONLY valid JSON, no markdown, no preamble:

{
"mode": "lens" | "loop",
"altitude": 0.0-1.0,
"quoted_phrase": "2-5 words copied VERBATIM from their text that reveal the pattern",
"label": "one short line naming the pattern, e.g. 'One event, treated as a permanent rule.'",
"explanation": "2-3 sentences. Point at their exact words. Plain language, no jargon, no therapy-speak. Do not comfort them. Do not tell them the nicer reading is true.",
"predictions": [
"where this same pattern likely shows up in their work or goals, written as a sentence they might say",
"where it likely shows up in how they see themselves, written as a sentence they might say"
],
"suggestion": "one concrete action, under 20 words, something they DO"
}

Rules:

- altitude reflects how caught they are, NOT how dark the thought is. A bleak thought they noticed and moved past is high. A mild thought they've circled for hours is low. Loops are always below 0.35.
- If mode is "loop", the suggestion must NOT involve analyzing, examining, or resolving the thought. Suggest delay, logging it, or acting without resolving it.
- If they ask for a verdict ("am I a bad person", "what does this say about me", "does this mean I don't love her"), do not answer it. In `explanation`, name the jump from one action to a claim about who they are.
- quoted_phrase must appear word-for-word in their input."""

app = FastAPI()


class ReadRequest(BaseModel):
    event: str
    thought: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/read")
def read(body: ReadRequest):
    if not body.event.strip() or not body.thought.strip():
        raise HTTPException(
            status_code=400,
            detail="Both a moment and a thought are needed.",
        )
    #builds an http post to antrhopic api end point to create a message 

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"What happened: {body.event}\n\nWhat they told themselves: {body.thought}",
                }
            ],
        )

        raw = message.content[0].text

        # The model sometimes wraps its JSON in ``` fences; strip them before parsing.
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]  # drop the opening ```/```json line
            cleaned = cleaned.rsplit("```", 1)[0]  # drop the closing ```
        cleaned = cleaned.strip()

        reading = json.loads(cleaned)
        return reading
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something drifted off. Try again in a moment.",
        )

