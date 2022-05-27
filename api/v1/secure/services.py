from typing import Dict, Optional

from . import postgres


def user_login(login: str, password: str) -> Optional[Dict]:
    """Выполнение проверки логина и пароля"""
    response = postgres.user_login(
        login=login,
        password=password,
    )

    if response:
        return response
