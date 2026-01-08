from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import date
import os
import tempfile

from app.database import engine, Base, get_db
from app.models import task as task_models
from app.schemas import task as task_schemas
from app.crud import task as task_crud
from app.core.security import get_api_key
from app.core.config import settings
from app.services.pdf_service import generate_tasks_pdf
from app.services.import_service import parse_txt_tasks

# Crear tablas
task_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de DailyTask 2026"}

@app.get("/tasks/", response_model=List[task_schemas.Task], dependencies=[Depends(get_api_key)])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    start_date: date = None, 
    end_date: date = None, 
    db: Session = Depends(get_db)
):
    tasks = task_crud.get_tasks(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    return tasks

@app.post("/tasks/", response_model=task_schemas.Task, dependencies=[Depends(get_api_key)])
def create_task(task: task_schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_task(db=db, task=task)

@app.get("/tasks/{task_id}", response_model=task_schemas.Task, dependencies=[Depends(get_api_key)])
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.put("/tasks/{task_id}", response_model=task_schemas.Task, dependencies=[Depends(get_api_key)])
def update_task(task_id: int, task: task_schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.delete("/tasks/{task_id}", dependencies=[Depends(get_api_key)])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = task_crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}

@app.get("/report/pdf", dependencies=[Depends(get_api_key)])
def get_report_pdf(
    start_date: date = Query(None), 
    end_date: date = Query(None), 
    db: Session = Depends(get_db)
):
    tasks = task_crud.get_tasks(db, start_date=start_date, end_date=end_date)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        generate_tasks_pdf(tasks, tmp.name)
        return FileResponse(tmp.name, filename=f"reporte_tareas_{date.today()}.pdf")

@app.post("/tasks/import", dependencies=[Depends(get_api_key)])
async def import_tasks(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    tasks_to_create = parse_txt_tasks(content.decode("utf-8"))
    created_tasks = []
    for task in tasks_to_create:
        created_tasks.append(task_crud.create_task(db, task))
    return {"message": f"Se importaron {len(created_tasks)} tareas exitosamente"}

@app.post("/tasks/duplicate", dependencies=[Depends(get_api_key)])
def duplicate_tasks(request: task_schemas.TaskDuplicate, db: Session = Depends(get_db)):
    tasks = task_crud.duplicate_tasks(db, source_date=request.source_date, target_date=request.target_date)
    return {"message": f"Se duplicaron {len(tasks)} tareas de {request.source_date} a {request.target_date}"}

@app.post("/tasks/{task_id}/duplicate", response_model=task_schemas.Task, dependencies=[Depends(get_api_key)])
def duplicate_single_task(task_id: int, request: task_schemas.TaskSingleDuplicate, db: Session = Depends(get_db)):
    db_task = task_crud.duplicate_single_task(db, task_id=task_id, target_date=request.target_date)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_task

@app.get("/tasks/template/download")
def download_template():
    template_content = (
        "# Formato: Fecha;Descripción;Hora Inicio;Hora Fin;Categoría (Opcional);Etiquetas;Estado\n"
        "2026-01-08;Reunión de desarrollo;09:00;10:30;Reunion Desarrollo;técnico,daily;completada\n"
        "2026-01-08;Sprint Planning;11:00;12:00;Planning;gestión;pendiente\n"
        "2026-01-08;Reunión con Cliente Alpha;15:00;16:00;Reunion con Cliente;ventas;en progreso\n"
    )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(template_content.encode("utf-8"))
        return FileResponse(tmp.name, filename="plantilla_tareas_2026.txt")
