from pydantic import BaseModel
from typing import Optional


class CreateFolderModel(BaseModel):
    """Класс 'Модель создания папки'"""
    user_id: int
    folder_name: Optional[str] = ''
    parent_folder_id: int


class CreateAttachmentModel(BaseModel):
    """
    Класс 'Модель создания файла'\n
    resource_type: `image`, `document`, `portal_document`
    """
    user_id: int
    parent_folder_id: int
    resource_type: str
