class StaticKeys():
    # python configure
    PYTHON_SECTION = 'PYTHON'
    PYTHON_PATH = 'python_path'
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

class JOB_TYPE():
    NORMAL_JOB = 0
    HTC_JOB = 1
    OTHER_JOB = 2

class JOB_STATE():
    SUBMITED = 0
    WAITTINT = 1
    RUNNING = 2
    SUCCESS = 3
    FAIL = 4
    PEND = 5
    CANCEL = 6
    SUBMIT_ERROR = -1

    STATE_DESCRIPTION = {SUBMITED: "This Job Has Been Submited", 
                         WAITTINT: "This Job Is Waitting In Queue", 
                         RUNNING: "This Job Is Running", 
                         SUCCESS: "This Job Has Been Finished Successfully",
                         FAIL: "This Job Has Been Finished Fail",
                         PEND: "This Job is Pendding",
                         CANCEL: "This Job Has Been Canceled",
                         SUBMIT_ERROR: "This Job Submits Fail"}

    STATE_DESCRIPTION2 = {SUBMITED: "Submited", 
                         WAITTINT: "Waitting", 
                         RUNNING: "Running", 
                         SUCCESS: "Success",
                         FAIL: "Fail",
                         PEND: "Pendding",
                         CANCEL: "Cancel",
                         SUBMIT_ERROR: "Submit Fail"}

class TASK_STATE():
    SUBMITED = 0
    WAITTINT = 1
    RUNNING = 2
    SUCCESS = 3
    FAIL = 4
    PEND = 5
    CANCEL = 6
    RETRY = 7
    SUBMIT_ERROR = -1

    STATE_DESCRIPTION = {SUBMITED: "This Task Has Been Submited", 
                         WAITTINT: "This Task Is Waitting In Queue", 
                         RUNNING: "This Task Is Running", 
                         SUCCESS: "This Task Has Been Finished Successfully",
                         FAIL: "This Task Has Been Finished Fail",
                         PEND: "This Task is Pendding",
                         CANCEL: "This Task Has Been Canceled",
                         RETRY: "This Task Will Be Retrying",
                         SUBMIT_ERROR: "This Task Submits Fail"}

    STATE_DESCRIPTION2 = {SUBMITED: "Submited", 
                         WAITTINT: "Waitting", 
                         RUNNING: "Running", 
                         SUCCESS: "Success",
                         FAIL: "Fail",
                         PEND: "Pendding",
                         CANCEL: "Cancel",
                         RETRY: "Retrying",
                         SUBMIT_ERROR: "Submit Fail"}