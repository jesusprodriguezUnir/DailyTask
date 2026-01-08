import sqlite3
import os

db_path = "backend/daily_tasks.db"

if not os.path.exists(db_path):
    print(f"Base de datos no encontrada en {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Intentar añadir la columna category_id a tasks
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN category_id INTEGER REFERENCES categories(id)")
            print("Columna 'category_id' añadida exitosamente a la tabla 'tasks'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("La columna 'category_id' ya existe.")
            else:
                raise e
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error durante la migración manual: {e}")
