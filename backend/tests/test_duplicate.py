from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)
API_KEY_HEADERS = {"X-API-KEY": "daily-task-secret-key-2026"}

def test_duplicate_tasks_success():
    # 1. Crear una tarea para el día de hoy
    source_date = date.today().isoformat()
    target_date = (date.today() + timedelta(days=1)).isoformat()
    
    task_data = {
        "date": source_date,
        "description": "Tarea a duplicar",
        "start_time": "10:00",
        "end_time": "11:00",
        "duration": 1.0,
        "category": "Daily",
        "tags": "test-dup",
        "status": "completada" # El original está completado
    }
    
    # Crear tarea original
    response_create = client.post("/tasks/", json=task_data, headers=API_KEY_HEADERS)
    assert response_create.status_code == 200
    
    # 2. Llamar al endpoint de duplicar
    duplicate_data = {
        "source_date": source_date,
        "target_date": target_date
    }
    response_dup = client.post("/tasks/duplicate", json=duplicate_data, headers=API_KEY_HEADERS)
    assert response_dup.status_code == 200
    assert "Se duplicaron" in response_dup.json()["message"]
    
    # 3. Verificar que la tarea duplicada existe en el destino y está pendiente
    response_get = client.get(f"/tasks/?start_date={target_date}&end_date={target_date}", headers=API_KEY_HEADERS)
    assert response_get.status_code == 200
    tasks = response_get.json()
    
    # Filtrar por descripción para estar seguros
    duplicated_tasks = [t for t in tasks if t["description"] == "Tarea a duplicar"]
    assert len(duplicated_tasks) >= 1
    assert duplicated_tasks[0]["date"] == target_date
    assert duplicated_tasks[0]["status"] == "pendiente" # Debe haber cambiado a pendiente

def test_duplicate_tasks_no_key():
    source_date = date.today().isoformat()
    target_date = (date.today() + timedelta(days=1)).isoformat()
    
    duplicate_data = {
        "source_date": source_date,
        "target_date": target_date
    }
    response = client.post("/tasks/duplicate", json=duplicate_data)
    assert response.status_code == 403

def test_duplicate_tasks_empty_day():
    # Intentar duplicar de un día que (probablemente) no tiene tareas
    source_date = "1999-01-01"
    target_date = "1999-01-02"
    
    duplicate_data = {
        "source_date": source_date,
        "target_date": target_date
    }
    response = client.post("/tasks/duplicate", json=duplicate_data, headers=API_KEY_HEADERS)
    assert response.status_code == 200
    assert "Se duplicaron 0 tareas" in response.json()["message"]

def test_duplicate_single_task():
    # 1. Crear tarea original
    task_data = {
        "date": "2026-01-10",
        "description": "Tarea Única",
        "start_time": "08:00",
        "end_time": "09:00",
        "duration": 1.0,
        "category": "Daily",
        "tags": "single-test",
        "status": "completada"
    }
    create_res = client.post("/tasks/", json=task_data, headers=API_KEY_HEADERS)
    task_id = create_res.json()["id"]
    
    # 2. Replicar a otra fecha
    target_date = "2026-01-15"
    dup_res = client.post(f"/tasks/{task_id}/duplicate", json={"target_date": target_date}, headers=API_KEY_HEADERS)
    
    assert dup_res.status_code == 200
    data = dup_res.json()
    assert data["date"] == target_date
    assert data["description"] == "Tarea Única"
    assert data["status"] == "pendiente"
    assert data["id"] != task_id
