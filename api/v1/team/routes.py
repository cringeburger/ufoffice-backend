from fastapi import APIRouter

from . import services
from ..middleware.utils import make_response


team_router = APIRouter(
    prefix='/team',
    tags=['team'],
)


@team_router.get("/{user_id}/info")
def get_user_team_info(user_id: int):
    """Маршрут получения информации о команде пользователя"""
    payload = services.get_user_team_info(user_id=user_id)

    return make_response(
        payload=payload,
        message='Информация о команде пользователя'
    )


@team_router.get("/{user_id}/name")
def get_user_team_name(user_id: int):
    """Маршрут получения имени команды пользователя"""
    payload = services.get_user_team_name(user_id=user_id)

    return make_response(
        payload=payload,
        message='Имя команды пользователя'
    )
