from pydantic import BaseModel
from typing import Callable, Dict, Optional


class AttachmentModel(BaseModel):
    """Класс 'модель вложения'"""
    user_id: int
    parent_id: int
    # attachment_tab_name: Optional[str]
    payload : Optional[Dict]


class FileResponseModel(BaseModel):
    """Класс 'модель ответа для файла'"""
    file_type: str
    file_name: str
    file_path: Optional[str]
    document: Optional[Callable]
    mime_type: Optional[str]
    content: Optional[str]
