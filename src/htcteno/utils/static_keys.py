class StaticKeys():
    CELERY_SECTION = 'CELERY'
    CELERY_PATH = 'celery_path'

    REDIS_SECTION = 'REDIS'
    REDIS_HOST = 'redis_host'
    REDIS_PORT = 'redis_port'
    REDIS_PATH = 'redis_path'

    DEFAULT_CELERY_PATH = "/usr/local/bin/celery"
    DEFAULT_REDIS_PATH = "/usr/bin/redis-server"
    DEFAULT_REDIS_HOST = 'localhost'
    DEFAULT_REDIS_PORT = '6379'