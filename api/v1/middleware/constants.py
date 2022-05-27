from enum import Enum


class StringEnumBase(str, Enum):
    """Базовый Enum класс для перечислений строк"""
    def __str__(self):
        return self.value


class NumberEnumBase(int, Enum):
    """Базовый Enum класс для перечислений числовых констант"""
    def __str__(self):
        return str(self.value)


class APIResponseStatus(StringEnumBase):
    """Статусы ответа API"""
    ERROR = 'error'
    SUCCESS = 'success'
