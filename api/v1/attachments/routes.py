from fastapi import (
    APIRouter,
    File,
    Form,
    status,
    UploadFile,
)

from . import models
from . import services
from ..middleware.utils import make_response


attachment_router = APIRouter(
    prefix='/attachment',
    tags=['attachment'],
)


@attachment_router.get("/")
def get_folder_resource(user_id: int, folder_id: int = 1):
    """Маршрут получения папок организации пользователя"""
    payload = services.get_folder_resource_info(
        user_id=user_id,
        folder_id=folder_id,
    )

    return make_response(
        payload=payload,
        message='Список ресурсов папки'
    )


@attachment_router.post("/")
def create_folder(folder: models.CreateFolderModel):
    """Маршрут создания папки"""
    services.create_folder(
        user_id=folder.user_id,
        parent_folder_id=folder.parent_folder_id,
        folder_name=folder.folder_name,
    )

    return make_response(
        message='Папка успешно создана',
    )


@attachment_router.post("/upload")
async def file_upload(
    user_id: int = Form(...),
    parent_folder_id: int = Form(...),
    resource_type: str = Form(...),
    file: UploadFile = File(...),
):
    """Маршрут загрузки файла"""
    uploaded = await services.upload_attachment(
        file=file,
        user_id=user_id,
        folder_id=parent_folder_id,
        file_type=resource_type,
    )

    if uploaded:
        return make_response(
                message='Ошибка загрузки файла',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    else:        
        return make_response(
                message='Файл успешно загружен',
            )
