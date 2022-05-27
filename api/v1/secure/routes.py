from fastapi import APIRouter, status

from . import models
from . import services
from ..middleware.utils import make_response, APIResponseStatus


login_router = APIRouter(
    prefix='/login',
    tags=['login'],
)


@login_router.post("/")
async def user_login(data: models.UserLoginModel):
    """Маршрут для входа"""
    payload = services.user_login(
        login=data.login,
        password=data.password,
    )

    if payload:
        return make_response(
            payload=payload,
            message='Вход произведен успешно',
        )
    else:
        return make_response(
            message='Логин или пароль неверны',
            status_name=APIResponseStatus.ERROR,
            status_code=status.HTTP_400_BAD_REQUEST,
        )