import os
import configparser
from utils.static_keys import StaticKeys

def parse_configure_file(configure_file=None):
    configure_info = {}
    if configure_file:
        if not os.path.isfile(configure_file):
            raise IOError
        config = configparser.ConfigParser()
        config.read(configure_file)
        if StaticKeys.CELERY_SECTION in config.sections():
            celery_info = config[StaticKeys.CELERY_SECTION]
            configure_info[StaticKeys.CELERY_PATH] = celery_info.get( \
                                StaticKeys.CELERY_PATH)
        if StaticKeys.REDIS_SECTION in config.sections():
            redis_info = config[StaticKeys.REDIS_SECTION]
            configure_info[StaticKeys.REDIS_PATH] = redis_info.get( \
                                StaticKeys.REDIS_PATH)
            if os.getenv('HOSTNAME'):
                configure_info[StaticKeys.REDIS_HOST] = os.getenv('HOSTNAME')
            else:
                configure_info[StaticKeys.REDIS_HOST] = redis_info.get( \
                                StaticKeys.REDIS_HOST)
            configure_info[StaticKeys.REDIS_PORT] = redis_info.get( \
                                StaticKeys.REDIS_PORT)

    configure_info = _check_configure(configure_info)
    return configure_info

def _check_configure(configure_info):
    if not configure_info.get(StaticKeys.CELERY_PATH):
        configure_info[StaticKeys.CELERY_PATH] = StaticKeys.DEFAULT_CELERY_PATH
    if not configure_info.get(StaticKeys.REDIS_PATH):
        configure_info[StaticKeys.REDIS_PATH] = StaticKeys.DEFAULT_REDIS_PATH
    if not configure_info.get(StaticKeys.REDIS_HOST):
        configure_info[StaticKeys.REDIS_HOST] = StaticKeys.DEFAULT_REDIS_HOST
    if not configure_info.get(StaticKeys.REDIS_PORT):
        configure_info[StaticKeys.REDIS_PORT] = StaticKeys.DEFAULT_REDIS_PORT
    return configure_info