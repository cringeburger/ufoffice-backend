from datetime import date
from typing import List, Dict

from . import postgres


def get_user_tasks(user_id: int) -> List[Dict]:
    """Получение списка задач команды пользователя"""
    users_list = postgres.get_user_team_short_info(user_id=user_id)
    
    for user in users_list:
        user_tasks = postgres.get_user_tasks(user['user_id'])
        user['tasks'] = user_tasks

    return users_list


def update_task_status(task_id: int, task_status_name: str) -> None:
    """Обновление статуса задачи"""
    postgres.update_task_status(
        task_id=task_id,
        task_status_name=task_status_name
    )


def create_task(
    task_name: str,
    task_desc: str,
    end_dt: date,
    ach_pts: int,
    user_id: int,
) -> None:
    """Создание задачи"""
    postgres.add_task(
        task_name=task_name,
        task_desc=task_desc,
        end_dt=end_dt,
        ach_pts=ach_pts,
        user_id=user_id,
    )


# TODO получение досок пользователя

# TODO добавление досок пользователя
