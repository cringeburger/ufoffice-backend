import mimetypes

from json import dumps
from typing import Optional

from . import models
from . import postgres


def get_document(document_id: int) -> Optional[models.FileResponseModel]:
    """Получение документа"""
    document_type_dict =  postgres.get_document_type(document_id=document_id)

    if not document_type_dict:
        return

    filepath_dict = postgres.get_document_path(document_id=document_id)

    if document_type_dict['document_type_name'] != 'portal_document':
        
        def iterfile():
            with open(filepath_dict['filepath'], mode='rb') as file:
                yield from file

        return models.FileResponseModel(
            file_type='file',
            file_name=filepath_dict['document_name'],
            file_path=filepath_dict['filepath'],
            document=iterfile,
            mime_type=str(mimetypes.MimeTypes().guess_type(filepath_dict['filepath'])[0]),
        )

    else:
        with open(filepath_dict['filepath'], mode='r', encoding='utf-8') as file:
            json = file.read()

        return models.FileResponseModel(
            file_type='portal_document',
            file_name=filepath_dict['document_name'],
            content=dumps(json),
        )
