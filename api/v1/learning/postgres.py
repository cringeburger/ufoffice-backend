from typing import Dict, List

from ..middleware.utils import (
    create_list_from_all_rows,
    provide_cursor,
)


@provide_cursor
def get_user_skills(user_id: int, cursor=None) -> List[Dict]:
    """Получения списка навыков пользователя"""
    cursor.execute("""
        select sk.skill_img,
               case when sk.skill_name is null then 'Нет навыков'
                    else sk.skill_name
               end as skill_name
          from ufoffice.users us
          left join ufoffice.fct_user_skills usk on usk.user_id = us.user_id
          left join ufoffice.dim_skill sk on sk.skill_id = usk.skill_id
         where us.user_id = %(user_id)s;
    """, dict(user_id=user_id)
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


# TODO получение курсов

# TODO создание курсов
