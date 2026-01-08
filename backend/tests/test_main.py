from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de DailyTask 2026"}

def test_read_tasks_no_key():
    response = client.get("/tasks/")
    assert response.status_code == 403

def test_create_task():
    headers = {"X-API-KEY": "daily-task-secret-key-2026"}
    task_data = {
        "date": "2026-01-08",
        "description": "Test Task",
        "start_time": "09:00",
        "end_time": "10:00",
        "duration": 1.0,
        "category": "Daily",
        "tags": "test",
        "status": "pendiente"
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Task"
    assert data["category"] == "Daily"

def test_download_template():
    response = client.get("/tasks/template/download")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_report_pdf():
    headers = {"X-API-KEY": "daily-task-secret-key-2026"}
    response = client.get("/report/pdf", headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
