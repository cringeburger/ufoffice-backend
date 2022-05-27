from typing import List, Dict

from . import postgres


def get_user_team_info(user_id: int) -> List[Dict]:
    """Получение команды пользователя"""
    user_team_list = postgres.get_user_team_info(user_id=user_id)

    for user in user_team_list:
        user['skills'] = postgres.get_user_skills(user['user_id'])

    return user_team_list


def get_user_team_name(user_id: int) -> None:
    """Получение названия команды пользователя"""
    return postgres.get_user_team_name(user_id=user_id)
