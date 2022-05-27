import logging
import os

from fastapi import UploadFile
from typing import List, Dict, Optional

from . import postgres


logger = logging.getLogger(__name__)


def get_folder_resource_info(user_id: int, folder_id: int) -> List[Dict]:
    """Получение ресурсов папки"""
    org_id_dict = postgres.get_user_organization(user_id=user_id)

    return postgres.get_folder_resource_info(
        folder_id=folder_id,
        org_id=org_id_dict['org_id'],
    )


def create_folder(user_id: int, parent_folder_id: int, folder_name: str = '') -> None:
    """Создание папки"""
    org_id_dict = postgres.get_user_organization(user_id=user_id)

    if folder_name.replace(' ', '') == '' or not folder_name:
        folder_name = postgres.select_folder_seq_nextval()['folder_name']

    folder_id_dict = postgres.create_folder(
        parent_folder_id=parent_folder_id,
        folder_name=folder_name,
        org_id=org_id_dict['org_id'],
    )

    folder_path_dict = postgres.get_folder_path(
        folder_id=folder_id_dict['folder_id'],
        org_id=org_id_dict['org_id'],
    )

    file_path = os.environ['PYTHON_AD'] + f'/static/org_{org_id_dict["org_id"]}{folder_path_dict["folder_path"]}'
    os.makedirs(file_path)


async def upload_attachment(
    file: Optional[UploadFile],
    user_id: int,
    folder_id: int,
    file_type: str,
) -> Optional[str]:
    """Загрузка вложений"""
    try:
        org_id_dict = postgres.get_user_organization(user_id=user_id)

        folder_path_dict = postgres.get_folder_path(
            folder_id=folder_id,
            org_id=org_id_dict['org_id'],
        )
        
        # file_name = file.filename if file else f'{json_text["payload"]["name"]}.json'
        file_full_path = f'{os.environ["PYTHON_AD"]}/static/org_{org_id_dict["org_id"]}{folder_path_dict["folder_path"]}{file.filename}' # noqa
        db_path = f'static/org_{org_id_dict["org_id"]}{folder_path_dict["folder_path"]}'

        contents = await file.read()
        with open(file_full_path, 'wb') as creating_file:
            creating_file.write(contents)

        document_id_dict = postgres.add_attachment_info(
            document_name=file.filename,
            document_path=db_path,
            document_type_name=file_type,
            user_id=user_id,
        )

        postgres.add_attachment_folder_mapping(
            folder_id=folder_id,
            document_id=document_id_dict['document_id']
        )
        
    except Exception as e:
        logger.debug(f'Ошибка загрузки файла: {e}')
        return 'Ошибка загрузки файла'
