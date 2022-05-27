from typing import Dict, Optional

from .hash import hash_check
from ..middleware.utils import (
    create_list_from_all_rows,
    provide_cursor,
)


@provide_cursor
def user_login(login: str, password: str, cursor=None) -> Optional[Dict]:
    """Вход"""
    cursor.execute("""
        select u.username, 
               u.user_password, 
               u.user_id,
               u.user_fio,
               u.user_image,
               ur.user_role_sysname,
               p.profession_name
          from ufoffice.users u
          join ufoffice.dim_user_role ur
            on ur.user_role_id = u.user_role_id
          join ufoffice.dim_profession p on p.profession_id = u.profession_id
    """
    )

    data = create_list_from_all_rows(cursor.fetchall(), cursor.description)

    for item in data:
        if login.lower() == item['username'] and hash_check(item['user_password'], password):
            return {
                'login': item['username'],
                'token': str(item['user_id']),
                'role': item['user_role_sysname'],
                'user_fio': item['user_fio'],
                'user_image': item['user_image'],
                'profession_name': item['profession_name'],
            }
