from fastapi import (
    APIRouter,
    status,
)
from typing import Dict, List, Optional

from ..middleware.utils import make_response
from . import models
from . import services


shop_router = APIRouter(
    prefix='/learning',
    tags=['learning'],
)

# TODO получение обучалок

# TODO добавление обучалок

# TODO изменение обучалок ???
