from fastapi import (
    APIRouter,
    status,
)
from fastapi.responses import FileResponse, StreamingResponse

from ..middleware.utils import make_response
from . import services


file_router = APIRouter(
    prefix='/files',
    tags=['files'],
)


@file_router.get('/')
def file_show(resource_id: int, download: bool = False):
    """Маршрут показа или скачивания файла"""
    file = services.get_document(document_id=resource_id)

    if file:
        if file.file_type!= 'portal_document':
            if not download:
                return StreamingResponse(file.document(), media_type=file.mime_type)
            else:
                return FileResponse(file.file_path, media_type=file.mime_type, filename=file.file_name)
        else:
            return make_response(
                message='Содержимое внутреннего файла приложения',
                payload=file.content
            )    
    else:
        return make_response(
            message='Ресурс с запрошиваемым id не найден',
            status_code=404,
            status_name=status.HTTP_404_NOT_FOUND
        )
