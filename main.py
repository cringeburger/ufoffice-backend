import os
import uvicorn

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env') # TODO костыленция

from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from api import router
from api.v1.middleware.exceptions import LibraryValidationException
from api.v1.socket.socket_manager import SocketManager


app = FastAPI(
    title='UFOFFICE API',
    description='Апиха пажилая сучка', # TODO название
    version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://26.237.70.37:8080'], # TODO корс whitelist
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(router)

templates = Jinja2Templates(directory='templates')
socket_manager = SocketManager()


# TODO перенести в другой файл
@app.exception_handler(LibraryValidationException)
async def library_validation_exception_handler(request, exc: LibraryValidationException):
    """Обработчник ошибок валидации запросов"""
    return JSONResponse(content=exc.errors, status_code=400)


# TODO перенести в другой файл
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, user_fio: str):
    """Socket manager для сообщений"""
    sender = user_fio # websocket.cookies.get('X-Authorization')
    if sender:
        await socket_manager.connect(websocket, sender)
        try:
            while True:
                data = await websocket.receive_json()
                await socket_manager.send_personal_message(data)
        except WebSocketDisconnect:
            socket_manager.disconnect(sender)
            print(f'{sender} отвалился')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root"""
    return templates.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    # локальный запуск с .env 
    load_dotenv(dotenv_path='.env')

    uvicorn.run(
        "main:app",
        host=os.environ['HOST'],
        port=int(os.environ['PORT']),
        reload=True,
        debug=True,
    )
