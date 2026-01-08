# DailyTask 2026 📌

Aplicación completa para el control de tareas diarias diseñada para el año 2026.

## 🚀 Arquitectura
- **Backend**: FastAPI + SQLAlchemy (SQLite) + FPDF2 (PDF).
- **Frontend**: Streamlit.
- **Seguridad**: Autenticación por `X-API-KEY`.

## 🛠️ Instalación Local

1. Instalar dependencias:
   ```bash
   pip install -r backend/requirements.txt
   pip install -r frontend/requirements.txt
   ```

2. Ejecutar Backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. Ejecutar Frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

## 🐳 Docker
Para levantar todo el entorno:
```bash
docker-compose up --build
```

## 📄 Formato de Importación TXT
Crea un archivo `.txt` con el siguiente formato (uno por línea):
`YYYY-MM-DD;Descripción;Duración;Etiquetas;Estado`

Ejemplo:
`2026-01-08;Reunión de inicio de proyecto;1.5;planificación;completada`

## 🔒 API Externa
Puedes insertar tareas desde aplicaciones como **n8n** enviando un POST a `/tasks/` con el header `X-API-KEY`.
