import sys
import os

# Añadir el directorio raíz del backend al path para poder importar la 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.category import Category
from app.models.task import Task # Importar Task para que SQLAlchemy pueda resolver la relación
from app.crud.category import create_category
from app.schemas.category import CategoryCreate

def seed():
    # Asegurar que las tablas existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        initial_categories = [
            {"name": "Daily", "color": "#4CAF50"},
            {"name": "Reunion Desarrollo", "color": "#2196F3"},
            {"name": "Reunion con Pablo", "color": "#9C27B0"},
            {"name": "Reunion con Cesar", "color": "#673AB7"},
            {"name": "Reunion con Cliente", "color": "#FF9800"},
            {"name": "Planning", "color": "#E91E63"},
            {"name": "Sin Categoría", "color": "#9E9E9E"}
        ]
        
        for cat_data in initial_categories:
            # Comprobar si ya existe
            exists = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not exists:
                create_category(db, CategoryCreate(**cat_data))
                print(f"Creada categoría: {cat_data['name']}")
            else:
                print(f"La categoría ya existe: {cat_data['name']}")
                
    finally:
        db.close()

if __name__ == "__main__":
    seed()
    print("Inicialización de categorías completada.")
