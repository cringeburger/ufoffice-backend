from fastapi import APIRouter

from . import services
from ..middleware.utils import make_response


chat_router = APIRouter(
    prefix='/messenger',
    tags=['messenger'],
)


@chat_router.get("/")
def get_user_dialogs(user_id: int):
    """Маршрут получения диалогов пользователя"""
    payload = services.get_user_dialogs(user_id=user_id)

    return make_response(
        payload=payload,
        message='Список диалогов пользователя'
    )


@chat_router.get("/history")
def get_user_dialogs(from_user_id: int, to_user_id: int, quantity: int = 20):
    """Маршрут получения истории диалога"""
    payload = services.get_dialog_messages(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        quantity=quantity,
    )

    return make_response(
        payload=payload,
        message='Список диалогов пользователя'
    )
