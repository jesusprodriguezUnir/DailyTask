from app.schemas.task import TaskCreate, TaskStatus
from datetime import datetime
from typing import List

def parse_txt_tasks(content: str) -> List[TaskCreate]:
    tasks = []
    lines = content.strip().split("\n")
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        try:
            # Formato: YYYY-MM-DD;Descripción;Inicio;Fin;Categoría;Tags;Estado
            parts = line.split(";")
            if len(parts) >= 4:
                task_date = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
                description = parts[1].strip()
                start_time = parts[2].strip()
                end_time = parts[3].strip()
                category = parts[4].strip() if len(parts) > 4 else None
                tags = parts[5].strip() if len(parts) > 5 else ""
                status = parts[6].strip() if len(parts) > 6 else "pendiente"
                
                # Calcular duración básica (en horas)
                duration = 0.0
                if start_time and end_time:
                    t1 = datetime.strptime(start_time, "%H:%M")
                    t2 = datetime.strptime(end_time, "%H:%M")
                    tdelta = t2 - t1
                    duration = tdelta.seconds / 3600.0

                tasks.append(TaskCreate(
                    date=task_date,
                    description=description,
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration,
                    category=category,
                    tags=tags,
                    status=status
                ))
        except Exception as e:
            print(f"Error parseando línea: {line} - {e}")
            continue
    return tasks
