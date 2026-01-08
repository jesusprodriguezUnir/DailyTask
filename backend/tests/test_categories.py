from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
API_KEY_HEADERS = {"X-API-KEY": "daily-task-secret-key-2026"}

def test_crud_categories():
    # 1. Crear categoría
    new_cat = {"name": "Test Category", "color": "#FF0000"}
    response = client.post("/categories/", json=new_cat, headers=API_KEY_HEADERS)
    assert response.status_code == 200
    cat_id = response.json()["id"]
    assert response.json()["name"] == "Test Category"

    # 2. Leer categorías
    response = client.get("/categories/", headers=API_KEY_HEADERS)
    assert response.status_code == 200
    categories = response.json()
    assert any(c["id"] == cat_id for c in categories)

    # 3. Editar categoría
    updated_cat = {"name": "Edited Category", "color": "#00FF00"}
    response = client.put(f"/categories/{cat_id}", json=updated_cat, headers=API_KEY_HEADERS)
    assert response.status_code == 200
    assert response.json()["name"] == "Edited Category"
    assert response.json()["color"] == "#00FF00"

    # 4. Borrar categoría
    response = client.delete(f"/categories/{cat_id}", headers=API_KEY_HEADERS)
    assert response.status_code == 200
    assert response.json()["message"] == "Categoría eliminada"

def test_task_with_category_relation():
    # 1. Crear categoría para la tarea
    cat_res = client.post("/categories/", json={"name": "Relational Cat", "color": "#123456"}, headers=API_KEY_HEADERS)
    cat_id = cat_res.json()["id"]

    # 2. Crear tarea enlazada
    task_data = {
        "date": "2026-01-20",
        "description": "Task with Category ID",
        "start_time": "12:00",
        "end_time": "13:00",
        "duration": 1.0,
        "category_id": cat_id,
        "tags": "test",
        "status": "pendiente"
    }
    task_res = client.post("/tasks/", json=task_data, headers=API_KEY_HEADERS)
    assert task_res.status_code == 200
    
    # 3. Verificar relación en el GET
    task_id = task_res.json()["id"]
    get_res = client.get(f"/tasks/{task_id}", headers=API_KEY_HEADERS)
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["category_rel"]["id"] == cat_id
    assert data["category_rel"]["name"] == "Relational Cat"

    # Limpieza
    client.delete(f"/tasks/{task_id}", headers=API_KEY_HEADERS)
    client.delete(f"/categories/{cat_id}", headers=API_KEY_HEADERS)
