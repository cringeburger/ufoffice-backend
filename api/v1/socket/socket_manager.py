import logging

from fastapi import WebSocket
from typing import Dict

from ..chat.postgres import create_message


# TODO логгер
logger = logging.getLogger(__name__)


class SocketManager:
    """Менеджер сокетов"""
    def __init__(self):
        self.active_connections: Dict[int: WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_fio: str):
        """Соединение пользователя"""
        await websocket.accept()
        self.active_connections[client_fio] = websocket
        logger.info(f'Соединился пользователь {client_fio}, сокет: {self.active_connections[client_fio]}')

    def disconnect(self, client_fio: str):
        """Отсоединение пользователя"""
        self.active_connections.pop(client_fio)

    async def send_personal_message(self, message: Dict):
        """Отправка личного сообщения (с записью в БД)"""
        for connection in self.active_connections.values():
            if connection.query_params._dict['user_fio'] == message['to_user']:
                await connection.send_json(message)

        create_message(
            from_user_fio=message['from_user'],
            to_user_fio=message['to_user'],
            message=message['message_text'],
        )

        logger.debug(f'Сообщение {message["message_text"]} для {message["to_user"]} от {message["from_user"]}')
