from pydantic import BaseModel
from datetime import date
from typing import Optional, List
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pendiente"
    IN_PROGRESS = "en progreso"
    COMPLETED = "completada"

class TaskBase(BaseModel):
    date: date
    description: str
    duration: float
    tags: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    date: Optional[date] = None
    description: Optional[str] = None
    duration: Optional[float] = None
    tags: Optional[str] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
