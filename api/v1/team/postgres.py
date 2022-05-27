from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_list_from_all_rows,
    create_dict_from_one_row,
)
# noinspection PyUnresolvedReferences
from ..learning.postgres import get_user_skills


@provide_cursor
def get_user_team_info(user_id: int, cursor=None) -> List[Dict]:
    """Получение команды пользователя"""
    cursor.execute("""
        select us.user_fio "name",
               pr.profession_name proffesion,
               us.user_image img,
               us.user_mail mail,
               us.user_phone phone,
               us.user_vk vk,
               us.user_tg tg ,
               us.user_facebook fb,
               coalesce((
                    select t.task_name
                    from ufoffice.fct_task t
                    join ufoffice.map_user_tasks ut
                     on ut.user_id = us.user_id
                    and ut.task_id = t.task_id
                  where t.end_dt > now()
                  limit 1), 'Нет задач'
               ) curr_task,
               to_char((select t.end_dt
                  from ufoffice.fct_task t
                  join ufoffice.map_user_tasks ut
                    on ut.user_id = us.user_id
                   and ut.task_id = t.task_id
                 where t.end_dt > now()
                 limit 1
               ), 'dd.MM.yyyy') end_dt,
               (row_number() over())-1 as position_usr,
               us.user_rating,
               us.user_id,
               team.team_name
          from ufoffice.users us
          join ufoffice.map_team_participants team_p
            on team_p.user_id = %(user_id)s
          join ufoffice.team team
            on team.team_id = team_p.team_id
          join ufoffice.dim_profession pr
            on pr.profession_id = us.profession_id
         where us.user_id in (
            select team_p1.user_id
              from ufoffice.map_team_participants team_p1
             where team_p1.team_id = team.team_id)
         order by (row_number() over())-1;
    """, dict(user_id=user_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def get_user_team_name(user_id: int, cursor=None) -> Dict:
    """Получение названия команды пользователя"""
    cursor.execute("""
        select team.team_name
          from ufoffice.users us
          join ufoffice.map_team_participants opt
            on opt.user_id = us.user_id
          join ufoffice.team team
            on team.team_id = opt.team_id
         where us.user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def get_user_team_short_info(user_id: int, cursor=None) -> List[Dict]:
    """Получение короткого списка команды пользователя"""
    cursor.execute("""
        select us.user_fio,
               pr.profession_name,
               us.user_id
          from ufoffice.users us
          join ufoffice.dim_profession pr
            on pr.profession_id = us.profession_id
          join ufoffice.map_team_participants team
            on team.user_id = us.user_id
         where us.user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)
