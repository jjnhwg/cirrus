import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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

    # Placeholder — the Anthropic call is added in the next piece.
    return {"event": body.event, "thought": body.thought}

