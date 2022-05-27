import os

from ...api.v1.middleware.constants import StringEnumBase


class AppConfig(StringEnumBase):
    STATIC_FILES_PATH = '/static'


env_variables = {
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'postgres',
    'DB_HOST': 'localhost',
    'DB_PORT': '5432',
    'DB_NAME': 'ufoffice',
}

def apply_env():
    for var_key, var_val in env_variables.items():
        if os.getenv(var_key) is None:
            os.environ[var_key] = var_val

apply_env()
