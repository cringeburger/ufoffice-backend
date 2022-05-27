from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_list_from_all_rows,
)
# noinspection PyUnresolvedReferences
from ..users.postgres import get_user_info


@provide_cursor
def get_user_dialogs(user_id: int, cursor=None) -> List[Dict]:
    """Получение диалогов пользователя"""
    cursor.execute("""
        select u.user_id,
            (select from_user_id from ufoffice.fct_chat_history where note_id = max(ch.note_id)) last_message_owner,
            u.user_fio,
            u.user_image,
            coalesce((select message_text
                from ufoffice.fct_chat_history h
                where (h.from_user_id = %(user_id)s and h.to_user_id = u.user_id)
                    or (h.from_user_id = u.user_id and h.to_user_id = %(user_id)s)
                order by h.message_dttm desc
                limit 1
            ), 'Диалог пуст') last_message,
            to_char(max(ch.message_dttm), 'dd.mm.yyyy') last_message_date,
            to_char(max(ch.message_dttm), 'hh24:mi') last_message_time
        from ufoffice.map_team_participants tp
        join ufoffice.users u on u.user_id = tp.user_id and u.user_id <> %(user_id)s
        join ufoffice.team t on tp.team_id = t.team_id and t.team_id = (
            select t.team_id
            from ufoffice.team t
            join ufoffice.map_team_participants tp on t.team_id = tp.team_id
            where tp.user_id = %(user_id)s)
        left join ufoffice.fct_chat_history ch
                on (ch.from_user_id = %(user_id)s and ch.to_user_id = u.user_id)
                or (ch.from_user_id = u.user_id and ch.to_user_id = %(user_id)s)
                and ch.message_dttm = (select max(message_dttm)
                                         from ufoffice.fct_chat_history
                                        where from_user_id = %(user_id)s or to_user_id = %(user_id)s)
        group by u.user_id
        order by max(ch.message_dttm) desc nulls last, u.user_fio;
    """, dict(
            user_id=user_id,
        )
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def create_message(from_user_fio: str, to_user_fio: str, message: str, cursor=None) -> None:
    """Создание сообщения"""
    cursor.execute("""
        insert into ufoffice.fct_chat_history (from_user_id, to_user_id, message_text)
             values (
                (select user_id from ufoffice.users where user_fio = %(from_user_fio)s),
                (select user_id from ufoffice.users where user_fio = %(to_user_fio)s),
                %(message)s
             );
    """, dict(
            from_user_fio=from_user_fio,
            to_user_fio=to_user_fio,
            message=message,
        )
    )


@provide_cursor
def get_dialog_messages(from_user_id: int, to_user_id: int, quantity: int, cursor=None) -> None:
    """Получение истории диалога"""
    cursor.execute("""
        select from_us.user_fio,
               from_us.user_id,
               ch.message_text
          from ufoffice.fct_chat_history ch
          join ufoffice.users from_us on from_us.user_id = ch.from_user_id
          join ufoffice.users to_us on to_us.user_id = ch.to_user_id
         where (ch.from_user_id = %(from_user_id)s and ch.to_user_id = %(to_user_id)s)
               or (ch.from_user_id = %(to_user_id)s and ch.to_user_id = %(from_user_id)s)
         order by ch.message_dttm desc
         limit %(quantity)s;
    """, dict(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            quantity=quantity,
        )
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)
