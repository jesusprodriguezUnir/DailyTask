import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "daily-task-secret-key-2026")

class APIClient:
    def __init__(self):
        self.headers = {"X-API-KEY": API_KEY}

    def get_tasks(self, start_date=None, end_date=None):
        params = {}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        try:
            response = httpx.get(f"{BASE_URL}/tasks/", headers=self.headers, params=params)
            if response.status_code != 200:
                print(f"Error API {response.status_code}: {response.text}")
                return []
            return response.json()
        except Exception as e:
            print(f"Error al obtener tareas: {e}")
            return []

    def create_task(self, task_data):
        try:
            response = httpx.post(f"{BASE_URL}/tasks/", headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al crear tarea: {e}")
            return {"error": str(e)}

    def update_task(self, task_id, task_data):
        try:
            response = httpx.put(f"{BASE_URL}/tasks/{task_id}", headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al actualizar tarea: {e}")
            return {"error": str(e)}

    def delete_task(self, task_id):
        try:
            response = httpx.delete(f"{BASE_URL}/tasks/{task_id}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al eliminar tarea: {e}")
            return {"error": str(e)}

    def get_pdf_report(self, start_date=None, end_date=None):
        params = {}
        if start_date: params["start_date"] = start_date
        if end_date: params["end_date"] = end_date
        response = httpx.get(f"{BASE_URL}/report/pdf", headers=self.headers, params=params)
        return response.content

    def import_tasks(self, file_content):
        files = {"file": ("tasks.txt", file_content)}
        response = httpx.post(f"{BASE_URL}/tasks/import", headers=self.headers, files=files)
        return response.json()

    def download_template(self):
        response = httpx.get(f"{BASE_URL}/tasks/template/download", headers=self.headers)
        return response.content
