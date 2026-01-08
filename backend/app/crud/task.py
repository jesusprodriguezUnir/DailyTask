from sqlalchemy.orm import Session, joinedload
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from datetime import date

def get_task(db: Session, task_id: int):
    return db.query(Task).options(joinedload(Task.category_rel)).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100, start_date: date = None, end_date: date = None):
    query = db.query(Task).options(joinedload(Task.category_rel))
    if start_date:
        query = query.filter(Task.date >= start_date)
    if end_date:
        query = query.filter(Task.date <= end_date)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate):
    task_data = task.model_dump()
    # Si tenemos un nombre de categoría pero no un ID, intentamos enlazarlo
    if task_data.get("category") and not task_data.get("category_id"):
        from app.models.category import Category
        cat = db.query(Category).filter(Category.name == task_data["category"]).first()
        if cat:
            task_data["category_id"] = cat.id
            
    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        update_data = task.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def duplicate_tasks(db: Session, source_date: date, target_date: date):
    tasks = db.query(Task).filter(Task.date == source_date).all()
    duplicated_tasks = []
    for task in tasks:
        # Creamos una copia del objeto Task, quitando el id y cambiando la fecha
        new_task_data = {
            "date": target_date,
            "description": task.description,
            "start_time": task.start_time,
            "end_time": task.end_time,
            "duration": task.duration,
            "category_id": task.category_id,
            "category": task.category,
            "tags": task.tags,
            "status": "pendiente" # Al duplicar, las tareas vuelven a estar pendientes
        }
        db_task = Task(**new_task_data)
        db.add(db_task)
        duplicated_tasks.append(db_task)
    
    db.commit()
    for task in duplicated_tasks:
        db.refresh(task)
    return duplicated_tasks

def duplicate_single_task(db: Session, task_id: int, target_date: date):
    original_task = db.query(Task).filter(Task.id == task_id).first()
    if not original_task:
        return None
    
    new_task_data = {
        "date": target_date,
        "description": original_task.description,
        "start_time": original_task.start_time,
        "end_time": original_task.end_time,
        "duration": original_task.duration,
        "category_id": original_task.category_id,
        "category": original_task.category,
        "tags": original_task.tags,
        "status": "pendiente" # Siempre pendiente al duplicar
    }
    db_task = Task(**new_task_data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
