from sqlalchemy import Column, Integer, String, Date, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
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
    start_time = Column(String, nullable=True) # Formato HH:MM
    end_time = Column(String, nullable=True)   # Formato HH:MM
    duration = Column(Float) # Duración calculada en horas
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = Column(String, nullable=True) # Mantenemos el campo string temporalmente para compatibilidad o lo quitamos
    tags = Column(String) # Guardado como string separado por comas
    status = Column(String, default=TaskStatus.PENDING)

    category_rel = relationship("Category", back_populates="tasks")
