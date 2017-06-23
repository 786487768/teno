import os
import sys
import json
import redis
sys.path.append('../..')

from celery import Task
# from torm.handle_jobs import insert_job
from utils.static_keys import TASK_STATE


class HtcTask(Task):
    _redis_instance = None
    def __init__(self):
        # get teno system id
    '''
        setting = json.loads(self.backend.client.get(
            'htcteno_setting').decode('UTF-8'))
        self.teno_id = setting.get('task_id')
    '''

    @property
    def get_redis_instance(self):
        if self._redis_instance is None:
            master_port = os.getenv("HTCTENO_PORT", 6379)
            master_host = os.getenv("HTCTENO_HOST", 'localhost')
            self._redis_instance = redis.Redis(host=master_host, port=master_port)
        return self._redis_instance

    '''
    def on_success(self, retval, task_id, args, kwargs):
        # task_info = {'task_id': task_id,
        #             'retval': retval,}
        self.backend.client.lpush('success_list', task_id)
        self.backend.client.hdel('thht_id_pd', task_id)
        key = 'celery-task-meta-%s' % task_id
        self.backend.client.delete(key)
        # insert success job to mysql

        task_info = json.loads(self.backend.client.hget( \
                'thht_id_info', task_id).decode('UTF-8'))
        insert_job(self.teno_id, task_id, TASK_STATE.SUCCESS, \
                task_info.get('task_cmd'))


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_error_info = {'task_id': task_id, 'exc': str(exc)}
        self.backend.client.lpush('fail_list', json.dumps(
            task_error_info))  # == hkeys('fail_log')
        self.backend.client.hdel('thht_id_pd',  task_id)
        #self.backend.client.hmset( 'thht_id_pd' , { rest.task_id : 'F' })
        self.logError(exc, task_id, args, kwargs, einfo)
        key = 'celery-task-meta-%s' % task_id
        self.backend.client.delete(key)
        # insert fail job to mysql

        task_info = json.loads(self.backend.client.hget( \
                'thht_id_info', task_id).decode('UTF-8'))
        insert_job(self.teno_id, task_id, TASK_STATE.FAIL, \
                task_info.get('task_cmd'))


    def on_retry(self, exc, task_id, args, kwargs, einfo):
        pass
        num = self.backend.client.lpush('retry_list', task_id)
        # TO-DO exc may be huge , need to check !
        self.backend.client.hincrby('thht_exc_log',  exc)
        # TO-DO if log_retry , not safty , may need a lot of mem !
        self.logError(exc, task_id, args, kwargs, einfo)

    def logError(self, exc, task_id, args, kwargs, einfo):
        err_info = {
            'task_id': task_id,
            'exc': str(exc),
            #'einfo' : einfo ,
            'date': time.time(),
            'host': self.request.hostname,
        }
        self.backend.client.lpush('err_log', json.dumps(err_info))
    '''
