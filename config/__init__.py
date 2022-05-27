import os


app_env = os.getenv('APP_ENV')

if app_env == 'LOCAL':
    from .environment import local
    APP_CONFIG = local.AppConfig

elif app_env == 'TEST':
    from .environment import test
    APP_CONFIG = test.AppConfig

elif app_env == 'PROD':
    from .environment import prod
    APP_CONFIG = prod.AppConfig
