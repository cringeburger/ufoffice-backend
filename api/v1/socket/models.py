from pydantic import BaseModel


class RegisterValidator(BaseModel):
    """Класс регистрация сокета"""
    user_fio: str
