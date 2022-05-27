import os

from ...api.v1.middleware.constants import StringEnumBase


class AppConfig(StringEnumBase):
    STATIC_FILES_PATH = '/static'
