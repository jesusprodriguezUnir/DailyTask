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
        response = httpx.get(f"{BASE_URL}/tasks/", headers=self.headers, params=params)
        return response.json()

    def create_task(self, task_data):
        response = httpx.post(f"{BASE_URL}/tasks/", headers=self.headers, json=task_data)
        return response.json()

    def delete_task(self, task_id):
        response = httpx.delete(f"{BASE_URL}/tasks/{task_id}", headers=self.headers)
        return response.json()

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
