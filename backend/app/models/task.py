from sqlalchemy import Column, Integer, String, Date, Float, Enum
from app.database import Base
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "pendiente"
    IN_PROGRESS = "en progreso"
    COMPLETED = "completada"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    description = Column(String)
    duration = Column(Float) # Duración en horas
    tags = Column(String) # Guardado como string separado por comas
    status = Column(String, default=TaskStatus.PENDING)
