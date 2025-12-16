from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import pathlib

# ---------------------------------------------------
# LOAD .env FROM DOCUFLOW ROOT
# ---------------------------------------------------
ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

print("DEBUG: Looking for .env at:", ENV_PATH)

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    print("WARNING: .env NOT FOUND!")

print("DEBUG: API_TOKEN after load =", os.getenv("API_TOKEN"))

app = FastAPI()

# ---------------------------------------------------
# Environment Variables
# ---------------------------------------------------
API_TOKEN = os.getenv("API_TOKEN", "DEFAULT_TOKEN")
print("DEBUG: API_TOKEN used by FastAPI =", API_TOKEN)


# ---------------------------------------------------
# Authentication Function
# ---------------------------------------------------
def verify_token(token: str):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")


# ---------------------------------------------------
# Request Models
# ---------------------------------------------------
class WorkflowStartRequest(BaseModel):
    document_id: int
    initiator: int
    approver: int


class WorkflowActionRequest(BaseModel):
    document_id: int
    action: str
    actor: int
    comment: str | None = None


# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.get("/health/")
def health():
    return {"status": "FastAPI service running"}


# ---------------------------------------------------
# WORKFLOW START (VALIDATION ONLY)
# ---------------------------------------------------
@app.post("/workflow/start/")
def workflow_start(data: WorkflowStartRequest, api_token: str = Header(None)):

    verify_token(api_token)

    return {
        "status": "ok",
        "assigned_to": data.approver,
        "message": "Workflow started successfully"
    }


# ---------------------------------------------------
# WORKFLOW ACTION (Approve / Reject)
# ---------------------------------------------------
@app.post("/workflow/action/")
def workflow_action(data: WorkflowActionRequest, api_token: str = Header(None)):

    verify_token(api_token)

    allowed_actions = ["approve", "reject"]
    if data.action not in allowed_actions:
        raise HTTPException(status_code=400, detail="Invalid action")

    # Map to Django-style workflow statuses
    mapped_status = {
        "approve": "approved",
        "reject": "rejected"
    }

    return {
        "status": mapped_status[data.action],
        "new_state": data.action,
        "comment": data.comment
    }