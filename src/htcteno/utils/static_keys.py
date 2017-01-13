class StaticKeys():
    # celery configure
    CELERY_SECTION = 'CELERY'
    CELERY_PATH = 'celery_path'
    # redis configure
    REDIS_SECTION = 'REDIS'
    REDIS_HOST = 'redis_host'
    REDIS_PORT = 'redis_port'
    REDIS_PATH = 'redis_path'
    # mysql configure
    MYSQL_CONF_PATH = ""
    MYSQL_SECTION = 'MYSQL'
    MYSQL_USER = 'mysql_user'
    MYSQL_PASSWORD = 'mysql_password'
    MYSQL_HOST = 'mysql_host'
    MYSQL_PORT = 'mysql_port'
    MYSQL_DATABASE = 'mysql_database'
    # default configure
    DEFAULT_CELERY_PATH = "/usr/local/bin/celery"

    DEFAULT_REDIS_PATH = "/usr/bin/redis-server"
    DEFAULT_REDIS_HOST = 'localhost'
    DEFAULT_REDIS_PORT = '6379'

    DEFAULT_MYSQL_USER = 'll'
    DEFAULT_MYSQL_PASSWORD = '816543'
    DEFAULT_MYSQL_HOST = 'localhost'
    DEFAULT_MYSQL_PORT = '3306'
    DEFAULT_MYSQL_DATABASE = 'tasks_info'

class TASK_TYPE():
    NORMAL_TASK = 0
    HTC_TASK = 1
    OTHER_TASK = 2
    
class TASK_STATE():
    SUBMITED = 0
    WAITTINT = 1
    RUNNING = 2
    SUCCESS = 3
    FAIL = 4
    PEND = 5
    CANCEL = 6
    SUBMIT_ERROR = -1

    STATE_DESCRIPTION = {SUBMITED: "Your Job Has Been Submited", 
                         WAITTINT: "Your Job Is Waitting In Queue", 
                         RUNNING: "Your Job Is Running", 
                         SUCCESS: "Your Job Has Been Finished Successfully",
                         FAIL: "Your Job Has Been Finished Fail",
                         PEND: "Your Job is Pendding",
                         CANCEL: "Your Job Has Been Canceled",
                         SUBMIT_ERROR: "Your Job Occured Submit Error"}

    STATE_DESCRIPTION2 = {SUBMITED: "Submited", 
                         WAITTINT: "Waitting", 
                         RUNNING: "Running", 
                         SUCCESS: "Success",
                         FAIL: "Fail",
                         PEND: "Pendding",
                         CANCEL: "Cancel",
                         SUBMIT_ERROR: "Submit Error"}