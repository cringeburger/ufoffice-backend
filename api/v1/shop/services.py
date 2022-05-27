import logging
import os

from fastapi import UploadFile
from typing import List, Dict, Optional

from . import postgres


logger = logging.getLogger(__name__)


def get_user_items(user_id: int) -> List[Dict]:
    """Получение предметов магазина пользователя"""
    org_id_dict = postgres.get_user_organization(user_id=user_id)
    host = os.environ['HOST']
    port = os.environ['PORT']

    return postgres.get_shop_items(
        org_id=org_id_dict['org_id'],
        host=host,
        port=port,
    )


async def create_item(
    file: UploadFile,
    user_id: int,
    item_name: str,
    price: int,
) -> Optional[str]:
    """Создание предмета"""
    try:
        org_id_dict = postgres.get_user_organization(user_id=user_id)
        
        file_full_path = f'{os.environ["PYTHON_AD"]}/static/org_{org_id_dict["org_id"]}/shop/{file.filename}'
        db_path = f'static/org_{org_id_dict["org_id"]}/shop/'

        contents = await file.read()
        with open(file_full_path, 'wb') as creating_image:
            creating_image.write(contents)

        doc_id_dict = postgres.create_item_attachment(
            user_id=user_id,
            document_name=file.filename,
            img_path=db_path,
        )

        postgres.create_item(
            item_name=item_name,
            price=price,
            org_id=org_id_dict['org_id'],
            document_id=doc_id_dict['document_id'],
        )
    except Exception as e:
        logger.debug(f'Ошибка загрузки файла: {e}')
        return 'Ошибка загрузки файла'


def delete_item(item_id: int) -> None:
    """Удаление предмета"""
    postgres.delete_item(
        item_id=item_id,
    )


def purchase_item(item_id: int, user_id: int) -> Optional[str]:
    """Покупка предмета"""
    user_info = postgres.get_user_info(user_id=user_id)
    item_price = postgres.item_price_info(item_id)

    if user_info['points'] < item_price['price']:
        return 'Недостаточно баллов'

    postgres.purchase_item(user_id=user_id, item_id=item_id)
    postgres.update_user_point(user_id=user_id, points=0-item_price['price'])
