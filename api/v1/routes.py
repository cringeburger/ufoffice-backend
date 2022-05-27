from fastapi import APIRouter

from .attachments.routes import attachment_router
from .chat.routes import chat_router
from .files.routes import file_router
from .leaderboard.routes import leaderboard_router
from .secure.routes import login_router
from .notes.routes import notes_router
from .shop.routes import shop_router
from .socket.routes import socket_router
from .tasks.routes import task_router
from .team.routes import team_router


api_router = APIRouter(
    prefix="/v1"
)

api_router.include_router(attachment_router)
api_router.include_router(chat_router)
api_router.include_router(file_router)
api_router.include_router(leaderboard_router)
api_router.include_router(login_router)
api_router.include_router(notes_router)
api_router.include_router(shop_router)
api_router.include_router(socket_router)
api_router.include_router(task_router)
api_router.include_router(team_router)
