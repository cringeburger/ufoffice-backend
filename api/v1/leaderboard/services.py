from typing import List, Dict

from . import postgres


def get_leaderboard(user_id: int, only_place: bool) -> List[Dict]:
    """Получение списка лидеров по организации пользователя"""
    return postgres.get_leaderboard(
        user_id=user_id,
        only_place=only_place,
    )
