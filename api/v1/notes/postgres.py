from typing import List, Dict

from ..middleware.utils import (
    provide_cursor,
    create_list_from_all_rows,
)


@provide_cursor
def get_user_notes(user_id: int, quantity: int, cursor=None) -> List[Dict]:
    """Получение заметок пользователя"""
    cursor.execute("""
        select nt.note_header,
               nt.note_body,
               nt.note_id
          from ufoffice.fct_notes nt
         where nt.user_id = %(user_id)s
         limit %(quantity)s;
    """, dict(
            user_id=user_id,
            quantity=quantity,
        )
    )

    return create_list_from_all_rows(cursor.fetchall(), cursor.description)


@provide_cursor
def create_note(user_id: int, header: str, body: str, cursor=None) -> None:
    """Создание заметки"""
    cursor.execute("""
        insert into ufoffice.fct_notes (note_header, note_body, user_id)
             values (%(header)s, %(body)s, %(user_id)s);
    """, dict(
            header=header,
            body=body,
            user_id=user_id,
        )
    )


@provide_cursor
def update_note(note_id: int, header: str, body: str, cursor=None) -> None:
    """Обновление заметки"""
    cursor.execute("""
        update ufoffice.fct_notes
           set note_body = %(body)s,
               updated_dttm = now(),
               note_header = %(header)s
         where note_id = %(note_id)s;
    """, dict(
        header=header,
        body=body,
        note_id=note_id,
        )
    )


@provide_cursor
def delete_note(note_id: int, cursor=None) -> None:
    """Удаление заметки"""
    cursor.execute("""
        delete from ufoffice.fct_notes
         where note_id = %(note_id)s;
    """, dict(note_id=note_id)
    )
