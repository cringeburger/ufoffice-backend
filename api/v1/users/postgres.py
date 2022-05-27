from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_dict_from_one_row,
)


@provide_cursor
def get_user_info(user_id: int, cursor=None) -> Dict:
    """Получение данных пользователя"""
    cursor.execute("""
        select user_fio,
               user_image,
               points
          from ufoffice.users
         where user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_dict_from_one_row(cursor.fetchone(), cursor.description)


@provide_cursor
def update_user_point(user_id: int, points: int, cursor=None) -> None:
    """Получение данных пользователя"""
    cursor.execute("""
        update ufoffice.users
        set points = points + %(points)s
         where user_id = %(user_id)s;
    """, dict(
            user_id=user_id,
            points=points,
        )
    )
