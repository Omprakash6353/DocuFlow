from fastapi.testclient import TestClient
from fastapi_service.main import app

client = TestClient(app)

def test_workflow_action_approve():
    response = client.post(
        "/workflow/action/",
        json={"document_id": 1, "action": "approve", "actor": 1, "comment": "ok"},
        headers={"api-token": "supersecret123"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
