from datetime import date
from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_list_from_all_rows,
)
# noinspection PyUnresolvedReferences
from ..team.postgres import get_user_team_short_info


@provide_cursor
def get_user_tasks(user_id: int, cursor=None) -> List[Dict]:
    """Получение названия команды пользователя"""
    cursor.execute("""
        select ts.task_name,
               to_char(ts.create_dttm, 'dd.mm.yyyy') start_dt,
               to_char(ts.end_dt, 'dd.mm.yyyy') end_dt,
               coalesce(ts.ach_pts, 0) ach_pts,
               ts.task_desc,
               tst.task_status_sysname,
               ts.task_id,
               us.user_id
          from ufoffice.users us
          join ufoffice.map_user_tasks ust
            on ust.user_id = us.user_id
          join ufoffice.fct_task ts
            on ts.task_id = ust.task_id
          join ufoffice.dim_task_status_name tst
            on ts.task_status_name_id  = tst.task_status_name_id 
         where us.user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def add_task(
    task_name: str,
    task_desc: str,
    end_dt: date,
    ach_pts: int,
    user_id: int,
    cursor=None
) -> None:
    """Добавление задачи"""
    cursor.execute("""
        begin;
            insert into ufoffice.fct_task (task_name, task_desc, end_dt, ach_pts, task_status_name_id)
            values (%(task_name)s, %(task_desc)s, %(end_dt)s, %(ach_pts)s, 1);
            
            insert into ufoffice.map_user_tasks (user_id, task_id)
            values (%(user_id)s, (select max(task_id) from ufoffice.fct_task));
        commit;
    """, dict(
            task_name=task_name,
            task_desc=task_desc,
            end_dt=end_dt,
            ach_pts=ach_pts,
            user_id=user_id
        )
    )


@provide_cursor
def update_task_status(task_id: int, task_status_name: str, cursor=None) -> None:
    """Изменение статуса задачи"""
    cursor.execute("""
        update ufoffice.fct_task
           set task_status_name_id = (select task_status_name_id
                                        from ufoffice.dim_task_status_name
                                       where task_status_sysname = %(task_status_name)s)
         where task_id = %(task_id)s;
    """, dict(
            task_id=task_id,
            task_status_name=task_status_name,
        )
    )

# TODO добавить доски для задач

# TODO получение досок пользователя

# TODO добавление досок пользователя
