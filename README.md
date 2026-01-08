# DailyTask 2026 📌

![DailyTask Logo](DailiTask.png)

Aplicación completa para el control de tareas diarias diseñada para el año 2026.

## 🚀 Arquitectura
- **Backend**: FastAPI + SQLAlchemy (SQLite) + FPDF2 (PDF).
- **Frontend**: Streamlit + Streamlit-Calendar (FullCalendar 6).
- **Seguridad**: Autenticación por `X-API-KEY`.

## 🌟 Características Principales
- **Vista de Calendario Interactiva**: Gestión visual de tareas por día, semana y mes.
- **Registro Rápido**: Selección de rangos horarios directamente en el calendario para auto-completar el registro.
- **Categorización**: Clasificación por tipos de reunión o trabajo con códigos de colores.
- **Reportes Profesionales**: Generación de reportes PDF filtrados por fecha.
- **Importación Inteligente**: Procesamiento masivo de tareas desde archivos de texto.

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
`Fecha;Descripción;Hora Inicio;Hora Fin;Categoría (Opcional);Etiquetas;Estado`

Ejemplo:
`2026-01-08;Reunión de desarrollo;09:00;10:30;Reunion Desarrollo;técnico,daily;completada`

> **Tip**: Puedes descargar una plantilla de ejemplo directamente desde la barra lateral de la aplicación.

## 🔒 API Externa
Puedes insertar tareas desde aplicaciones como **n8n** enviando un POST a `/tasks/` con el header `X-API-KEY`.
