import os
import time
import requests

BASE_URL = os.environ.get("ORCH_URL", "http://localhost:8000")
INGEST_URL = os.environ.get("INGEST_URL", "http://localhost:8003")
JIRA_URL = os.environ.get("JIRA_URL", "http://localhost:8005")


def main() -> None:
    doc = {
        "source": "local",
        "uri": "infra/db/seeds/sample.txt",
        "tenant_id": "tenant-1",
    }
    r = requests.post(f"{INGEST_URL}/v1/ingest", json=doc, timeout=30)
    r.raise_for_status()

    chat = {
        "session_id": "session-1",
        "message": "Summarize the sample content and include citations.",
        "tenant_id": "tenant-1",
        "user_id": "user-1",
    }
    r = requests.post(f"{BASE_URL}/v1/chat", json=chat, timeout=30)
    r.raise_for_status()
    data = r.json()
    assert "citations" in data, "missing citations"

    tool_req = {
        "session_id": "session-2",
        "message": "Create a high-risk Jira ticket.",
        "tenant_id": "tenant-1",
        "user_id": "user-1",
    }
    r = requests.post(f"{BASE_URL}/v1/chat", json=tool_req, timeout=30)
    r.raise_for_status()
    task = r.json()
    assert task.get("status") == "pending_approval"

    task_id = task["id"]
    r = requests.post(f"{BASE_URL}/v1/tasks/{task_id}/approve", json={"approved_by": "user-admin"}, timeout=30)
    r.raise_for_status()
    time.sleep(1)
    r = requests.get(f"{BASE_URL}/v1/tasks/{task_id}", timeout=30)
    r.raise_for_status()
    task = r.json()
    assert task.get("status") == "completed"

    r = requests.get(f"{JIRA_URL}/health", timeout=10)
    r.raise_for_status()

    print("Smoke test passed")


if __name__ == "__main__":
    main()
