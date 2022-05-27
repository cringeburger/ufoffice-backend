from datetime import date
from pydantic import BaseModel


class CreateTaskModel(BaseModel):
    """'Класс 'Модель создания задачи"""
    task_name: str
    task_desc: str
    end_dt: date
    ach_pts: int
    user_id: int


class UpdateTaskStatusModel(BaseModel):
    """'Класс 'Модель обновления статуса задачи"""
    task_id: int
    task_status_name: str
