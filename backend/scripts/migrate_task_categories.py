import sys
import os

# Añadir el directorio raíz del backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal
from app.models.task import Task
from app.models.category import Category

def migrate_existing_tasks():
    db = SessionLocal()
    try:
        # 1. Obtener todas las categorías para mapear nombre -> id
        categories = db.query(Category).all()
        cat_map = {c.name.lower(): c.id for c in categories}
        
        # 2. Obtener tareas que tienen categoria en string pero no id
        tasks_to_fix = db.query(Task).filter(Task.category_id == None, Task.category != None).all()
        
        print(f"Encontradas {len(tasks_to_fix)} tareas para actualizar.")
        updated_count = 0
        
        for task in tasks_to_fix:
            cat_name = task.category.strip().lower()
            if cat_name in cat_map:
                task.category_id = cat_map[cat_name]
                updated_count += 1
        
        db.commit()
        print(f"Se han actualizado {updated_count} tareas con su respectivo category_id.")
                
    finally:
        db.close()

if __name__ == "__main__":
    migrate_existing_tasks()
