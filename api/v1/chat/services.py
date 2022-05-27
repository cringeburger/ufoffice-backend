from typing import List, Dict

from . import postgres


def get_user_dialogs(user_id: int) -> List[Dict]:
    """Получение диалогов пользователя"""
    return postgres.get_user_dialogs(user_id=user_id)


def create_message(from_user_id: int, to_user_id: int, message: str) -> None:
    """Создание сообщения"""
    postgres.create_message(
        from_user_fio=from_user_id,
        to_user_fio=to_user_id,
        message=message,
    )


def get_dialog_messages(from_user_id: int, to_user_id: int, quantity: int):
    """Получение истории диалога"""
    to_user_dict = postgres.get_user_info(user_id=to_user_id)
    messages = postgres.get_dialog_messages(
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        quantity=quantity,
    )

    payload = {
        'to': to_user_dict['user_fio'],
        'img': to_user_dict['user_image'],
        'messages': messages
    }

    return payload
