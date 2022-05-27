from typing import List, Dict

from . import postgres


def get_user_notes(user_id: int, quantity: int) -> List[Dict]:
    """Получение заметок пользователя"""
    return postgres.get_user_notes(
        user_id=user_id,
        quantity=quantity,
    )


def create_note(user_id: int, header: str, body: str) -> None:
    """Создание заметки"""
    postgres.create_note(
        user_id=user_id,
        header=header,
        body=body,
    )


def update_note(note_id: int, header: str, body: str) -> None:
    """Обновление заметки"""
    postgres.update_note(
        note_id=note_id,
        header=header,
        body=body,
    )


def delete_note(note_id: int) -> None:
    """Удаление заметки"""
    postgres.delete_note(
        note_id=note_id,
    )
