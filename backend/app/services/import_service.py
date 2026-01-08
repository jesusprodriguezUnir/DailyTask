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
            # Formato: YYYY-MM-DD;Descripción;Duración;Tags;Estado
            parts = line.split(";")
            if len(parts) >= 3:
                task_date = datetime.strptime(parts[0].strip(), "%Y-%m-%d").date()
                description = parts[1].strip()
                duration = float(parts[2].strip())
                tags = parts[3].strip() if len(parts) > 3 else ""
                status = parts[4].strip() if len(parts) > 4 else "pendiente"
                
                tasks.append(TaskCreate(
                    date=task_date,
                    description=description,
                    duration=duration,
                    tags=tags,
                    status=status
                ))
        except Exception as e:
            print(f"Error parseando línea: {line} - {e}")
            continue
    return tasks
