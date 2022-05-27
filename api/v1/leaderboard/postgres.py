from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_list_from_all_rows,
)


@provide_cursor
def get_leaderboard(user_id: int, only_place: bool, cursor=None) -> List[Dict]:
    """Получение списка лидеров по организации пользователя или места пользователя в списке"""
    where_expr = f'where t.user_id = {user_id}' if only_place else ''
    
    cursor.execute("""
        with org as (
            select org.org_id
              from ufoffice.users us
              join ufoffice.map_team_participants mt on mt.user_id = us.user_id
              join ufoffice.team t on t.team_id = mt.team_id
              join ufoffice.organization org on org.org_id = t.org_id
             where us.user_id = %(user_id)s
        ),
        users as (
            select us.*
              from ufoffice.team t
              join ufoffice.map_team_participants mt on mt.team_id = t.team_id 
              join ufoffice.users us on mt.user_id = us.user_id
             where t.org_id = (select org_id from org)
        )
        select row_number() over() as position, t.name, t.rating
          from (
            select user_id,
                   user_fio as name,
                   user_rating rating
              from users
             order by user_rating desc
        ) t
    """ + where_expr, dict(user_id=user_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)
