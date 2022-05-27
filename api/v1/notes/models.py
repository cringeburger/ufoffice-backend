from pydantic import BaseModel
from typing import Optional


class CreateNoteModel(BaseModel):
    """Класс 'Модель создания заметки'"""
    user_id: int
    note_header: Optional[str]
    note_body: str


class UpdateNoteModel(BaseModel):
    """Класс 'Модель обновления заметки'"""
    note_id: int
    note_header: Optional[str]
    note_body: str
