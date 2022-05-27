from fastapi import (
    APIRouter,
    File,
    status,
    UploadFile,
)

from . import services
from ..middleware.utils import make_response


shop_router = APIRouter(
    prefix='/shop',
    tags=['shop'],
)


@shop_router.get("/")
def get_shop_item(user_id: int):
    """Маршрут получения предметов магазина пользователя"""
    payload = services.get_user_items(
        user_id=user_id,
    )

    return make_response(
        payload=payload,
        message='Список предметов магазина пользователя'
    )


@shop_router.post("/")
async def create_item(
    user_id: int,
    item_name: str,
    price: int,
    file: UploadFile = File(...)
):
    """Маршрут создания предмета"""
    uploaded = await services.create_item(
        file=file,
        user_id=user_id,
        price=price,
        item_name=item_name,
    )

    if uploaded:
        return make_response(
                message='Ошибка загрузки файла',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    else:        
        return make_response(
                message='Предмет успешно создан',
            )


@shop_router.delete("/{item_id}")
def delete_item(item_id: int):
    """Маршрут удаления предмета"""
    services.delete_item(item_id=item_id)

    return make_response(
        message=f'Предмет с id = {item_id} успешно удален',
    )


@shop_router.post("/purchase")
def purchase_item(item_id: int, user_id: int):
    """Маршрут покупки предмета"""
    response = services.purchase_item(user_id=user_id, item_id=item_id)

    if not response:
        return make_response(
            message=f'Предмет с id = {item_id} успешно удален',
        )
    else:
        return make_response(
            message='Недостаточно баллов',
            status_code=status.HTTP_403_FORBIDDEN,
            status_name='error'
        )
