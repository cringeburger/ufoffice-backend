from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_dict_from_one_row,
)


@provide_cursor
def get_user_organization(user_id: int, cursor=None) -> List[Dict]:
    """Получение id организации по id пользователя"""
    cursor.execute("""
        select o.org_id
          from ufoffice.users u
          join ufoffice.map_team_participants mp on mp.user_id = u.user_id
          join ufoffice.team t on t.team_id = mp.team_id
          join ufoffice.organization o on o.org_id = t.org_id
         where u.user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)
