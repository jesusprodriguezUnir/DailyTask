from __future__ import annotations
from pydantic import BaseModel
import datetime
from typing import Optional, List
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pendiente"
    IN_PROGRESS = "en progreso"
    COMPLETED = "completada"

class TaskBase(BaseModel):
    date: datetime.date
    description: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: float
    category: Optional[str] = None
    tags: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    date: Optional[datetime.date] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskDuplicate(BaseModel):
    source_date: datetime.date
    target_date: datetime.date

class TaskSingleDuplicate(BaseModel):
    target_date: datetime.date

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
