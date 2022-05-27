from fastapi import APIRouter

from . import models
from . import services
from ..middleware.utils import make_response


notes_router = APIRouter(
    prefix='/notes',
    tags=['notes'],
)


@notes_router.get("/")
def get_user_notes(user_id: int, quantity: int = 1000):
    """Маршрут получения заметок пользователя"""
    payload = services.get_user_notes(
        user_id=user_id,
        quantity=quantity,
    )

    return make_response(
        payload=payload,
        message='Список заметок пользователя'
    )


@notes_router.post("/")
def create_note(note: models.CreateNoteModel):
    """Маршрут создания заметки"""
    services.create_note(
        user_id=note.user_id,
        header=note.note_header,
        body=note.note_body,
    )

    return make_response(
        message='Заметка успешно создана',
    )


@notes_router.patch("/")
def update_note(note: models.UpdateNoteModel):
    """Маршрут создания заметки"""
    services.update_note(
        note_id=note.note_id,
        header=note.note_header,
        body=note.note_body,
    )

    return make_response(
        message=f'Заметка с id = {note.note_id} успешно изменена',
    )


@notes_router.delete("/{note_id}")
def delete_note(note_id: int):
    """Маршрут удаления заметки"""
    services.delete_note(note_id=note_id)

    return make_response(
        message=f'Заметка с id = {note_id} успешна удалена',
    )
