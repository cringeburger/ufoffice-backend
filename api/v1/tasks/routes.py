from fastapi import APIRouter

from . import models
from . import services
from ..middleware.utils import make_response


task_router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
)


@task_router.get("/{user_id}")
def get_user_tasks(user_id: int):
    """Маршрут получения задач команды пользователя"""
    payload = services.get_user_tasks(user_id=user_id)

    return make_response(
        payload=payload,
        message='Информация о задачах команды пользователя'
    )


@task_router.post("/")
def create_task(task: models.CreateTaskModel):
    """Маршрут создания задачи"""
    services.create_task(
        task_name=task.task_name,
        task_desc=task.task_desc,
        end_dt=task.end_dt,
        ach_pts=task.ach_pts,
        user_id=task.user_id,
    )

    return make_response(
        message='Задача успешно создана',
    )


@task_router.patch("/")
def update_task_status(task_status: models.UpdateTaskStatusModel):
    """Маршрут обновления статуса задачи"""
    services.update_task_status(
        task_id=task_status.task_id,
        task_status_name=task_status.task_status_name,
    )

    return make_response(
        message=f'Статус задачи с id = {task_status.task_id} успешно изменен',
    )


# TODO получение досок пользователя

# TODO добавление досок пользователя
