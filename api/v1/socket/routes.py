from fastapi import (
    APIRouter,
    Response,
)

from . import models


socket_router = APIRouter(
    prefix='/socket',
    tags=['socket'],
)


@socket_router.post("/register")
def register_socket_user(user: models.RegisterValidator, response: Response):
    """Регистрация сокета пользователя"""
    response.set_cookie(key='X-Authorization', value=user.user_fio)
    return {'cookie': f'X-Authorization={user.user_fio}'}
