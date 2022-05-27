from fastapi import status
from fastapi.responses import JSONResponse
from functools import wraps
from typing import Any, Dict, List, Tuple

import logging
import psycopg2

from .constants import APIResponseStatus
from .settings import DATABASE_CONNECT_DICT


# TODO логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_pg_connection(conn_attrs: dict = DATABASE_CONNECT_DICT):
    """Получение подключения к БД postgres"""
    return psycopg2.connect(
        user=conn_attrs['USER'],
        password=conn_attrs['PASSWORD'],
        host=conn_attrs['HOST'],
        port=conn_attrs['PORT'],
        dbname=conn_attrs['NAME'],
        connect_timeout=30,
    )


def provide_cursor(func, conn_attrs: dict = DATABASE_CONNECT_DICT):
    """Декоратор для передачи курсора (postgres) в вызываемую функцию"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'cursor' in kwargs:
            return func(*args, **kwargs)
        else:
            conn = get_pg_connection(conn_attrs=conn_attrs)

            conn.autocommit = kwargs.get('autocommit', True)

            with conn.cursor() as cursor:
                func_result = func(*args, cursor=cursor, **kwargs)
                return func_result

    return wrapper


def create_dict_from_one_row(row: Tuple[Any], cursor_description: Tuple[Any]) -> dict:
    """Преобразование строки-ответа БД к словарю"""
    if row is None:
        return dict()

    columns = [col[0].lower() for col in cursor_description]

    return dict(zip(columns, row))


def create_list_from_all_rows(rows: List[Tuple[Any]], cursor_description: Tuple[Any]) -> List[Dict]:
    """Преобразование строк-ответа БД к списку словарей"""
    if rows is None:
        return list()

    columns = [col[0].lower() for col in cursor_description]

    rows_list: list(dict) = []
    for row in rows:
        rows_list.append(dict(zip(columns, row)))
    return rows_list


def make_response(status_name=APIResponseStatus.SUCCESS, status_code=status.HTTP_200_OK, payload=None, message=None):
    """Подготовка JsonResponse для API"""
    
    data = {
        'status': status_name,
        'status_code': status_code,
        'message': message,
        'payload': payload
    }
    
    try:
        logger.info(f'Запрос с payload = {payload}')
        return JSONResponse(content=data, status_code=status_code)
    except Exception as e:
        logger.error(f'Ошибка ответа: {str(e)}\nВыходные данные: {data}')
        return {
            'status': APIResponseStatus.ERROR,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': str(e),
            'payload': None
        }
