# Methods

A running log of every **backend** function, API route handler, and server-side
helper added to Cirrus. Frontend/UI code (React components, hooks, client event
handlers) is intentionally not logged here. Newest entries appended at the
bottom.

---

## `health()`

- **File:**
- **Summary:**
- **Input:**
- **Output:**
- **User flow:**


## how the anthropic api sdk works 


## `read()` — `POST /api/read`

- **File:** - backend/main.py
- **Summary:** - when a user submits their thoughts the read makes sure 
there is an event an a thought
- **Input:** - the event and thought body from the pydantic model 
- **Output:** - the event and the thoguht 
- **User flow:**. - user submits an event and thought

> Changed (step 6): added the Claude call — output is no longer the echoed
> event/thought, it's now the model's raw text reply (`{"raw": ...}`). Update
> your Summary/Output to reflect that.
