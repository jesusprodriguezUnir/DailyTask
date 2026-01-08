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
