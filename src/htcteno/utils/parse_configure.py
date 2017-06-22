import os
import configparser
from utils.static_keys import StaticKeys


def parse_all_configure(configure_file=None):
    configure_info = {}
    if configure_file:
        if not os.path.isfile(configure_file):
            raise IOError
        config = configparser.ConfigParser()
        config.read(configure_file)
        if StaticKeys.PYTHON_SECTION in config.sections():
            python_info = config[StaticKeys.PYTHON_SECTION]
            configure_info[StaticKeys.PYTHON_PATH] = python_info.get(
                StaticKeys.PYTHON_PATH)
        if StaticKeys.CELERY_SECTION in config.sections():
            celery_info = config[StaticKeys.CELERY_SECTION]
            configure_info[StaticKeys.CELERY_PATH] = celery_info.get(
                StaticKeys.CELERY_PATH)
        if StaticKeys.REDIS_SECTION in config.sections():
            redis_info = config[StaticKeys.REDIS_SECTION]
            configure_info[StaticKeys.REDIS_PATH] = redis_info.get(
                StaticKeys.REDIS_PATH)
            if os.getenv('HOSTNAME'):
                configure_info[StaticKeys.REDIS_HOST] = os.getenv('HOSTNAME')
            else:
                configure_info[StaticKeys.REDIS_HOST] = redis_info.get(
                    StaticKeys.REDIS_HOST)
            configure_info[StaticKeys.REDIS_PORT] = redis_info.get(
                StaticKeys.REDIS_PORT)
        if StaticKeys.MYSQL_SECTION in config.sections():
            mysql_info = config[StaticKeys.MYSQL_SECTION]
            configure_info[StaticKeys.MYSQL_HOST] = mysql_info.get(
                StaticKeys.MYSQL_HOST)
            configure_info[StaticKeys.MYSQL_PORT] = mysql_info.get(
                StaticKeys.MYSQL_PORT)
            configure_info[StaticKeys.MYSQL_DATABASE] = mysql_info.get(
                StaticKeys.MYSQL_DATABASE)

    configure_info = _check_celery_configure(configure_info)
    configure_info = _check_redis_configure(configure_info)
    return configure_info


def parse_mysql_configure(configure_file=None):
    configure_info = {}
    if configure_file:
        if not os.path.isfile(configure_file):
            raise IOError
        config = configparser.ConfigParser()
        config.read(configure_file)
        if StaticKeys.MYSQL_SECTION in config.sections():
            mysql_info = config[StaticKeys.MYSQL_SECTION]
            configure_info[StaticKeys.MYSQL_HOST] = mysql_info.get(
                StaticKeys.MYSQL_HOST)
            configure_info[StaticKeys.MYSQL_PORT] = mysql_info.get(
                StaticKeys.MYSQL_PORT)
    configure_info = _check_mysql_configure(configure_info)
    return configure_info


def _check_celery_configure(configure_info):
    if not configure_info.get(StaticKeys.CELERY_PATH):
        configure_info[StaticKeys.CELERY_PATH] = StaticKeys.DEFAULT_CELERY_PATH
    return configure_info


def _check_redis_configure(configure_info):
    if not configure_info.get(StaticKeys.REDIS_PATH):
        configure_info[StaticKeys.REDIS_PATH] = StaticKeys.DEFAULT_REDIS_PATH
    if not configure_info.get(StaticKeys.REDIS_HOST):
        configure_info[StaticKeys.REDIS_HOST] = StaticKeys.DEFAULT_REDIS_HOST
    if not configure_info.get(StaticKeys.REDIS_PORT):
        configure_info[StaticKeys.REDIS_PORT] = StaticKeys.DEFAULT_REDIS_PORT
    return configure_info


def _check_mysql_configure(configure_info):
    if not configure_info.get(StaticKeys.MYSQL_HOST):
        configure_info[StaticKeys.MYSQL_HOST] = StaticKeys.DEFAULT_MYSQL_HOST
    if not configure_info.get(StaticKeys.MYSQL_PORT):
        configure_info[StaticKeys.MYSQL_PORT] = StaticKeys.DEFAULT_MYSQL_PORT
    if not configure_info.get(StaticKeys.MYSQL_USER):
        configure_info[StaticKeys.MYSQL_USER] = StaticKeys.DEFAULT_MYSQL_USER
    if not configure_info.get(StaticKeys.MYSQL_PASSWORD):
        configure_info[
            StaticKeys.MYSQL_PASSWORD] = StaticKeys.DEFAULT_MYSQL_PASSWORD
    if not configure_info.get(StaticKeys.MYSQL_DATABASE):
        configure_info[
            StaticKeys.MYSQL_DATABASE] = StaticKeys.DEFAULT_MYSQL_DATABASE
    return configure_info
