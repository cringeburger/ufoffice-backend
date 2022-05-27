from fastapi import APIRouter

from . import services
from ..middleware.utils import make_response


leaderboard_router = APIRouter(
    prefix='/leaderboard',
    tags=['leaderboard'],
)


@leaderboard_router.get("/")
def get_leaderboard(user_id: int, only_place: bool = False):
    """Маршрут получения списка лидеров по организации пользователя или места в списке"""
    payload = services.get_leaderboard(
        user_id=user_id,
        only_place=only_place,
    )

    return make_response(
        payload=payload,
        message='Список лидеров'
    )
