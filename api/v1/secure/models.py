from pydantic import BaseModel


class UserLoginModel(BaseModel):
    """Класс 'Модель входа пользователя'"""
    login: str
    password: str
