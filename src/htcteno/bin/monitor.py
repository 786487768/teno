#!/usr/bin/env python
import sys
import json
import time
import redis
from subprocess import Popen, PIPE
sys.path.append('../..')

# from htcteno import session


class Monitor():
    """ Monitor the status of jobs and clean resource after 
                task has been finished """

    def __init__(self, host, port):
        self.redis_instance = redis.Redis(host=host, port=port)
        setting = json.loads(self.redis_instance.get(
            'htcteno_setting').decode('UTF-8'))
        self.teno_id = setting.get('task_id')
        self.is_finished = False

    def wait(self):
        while 1:
            time.sleep(10)
            cln = self.redis_instance.llen('compelete_list')
            aln = int(self.redis_instance.get('task_nums'))
            if cln == aln:
                self.is_finished = True
                self._clean()
                break

    def _clean(self):
        kill_celery = ['bash', '-c', 'killall', '-9', 'celery']
        kill_redis_server = ['bash', '-c', 'killall', '-9', 'redis-server']
        Popen(kill_celery, stdout=PIPE, stderr=PIPE)
        Popen(kill_redis_server, stdout=PIPE, stderr=PIPE)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("monitor argv error")
    host, port = sys.argv[1], sys.argv[2]
    monitor = Monitor(host, port)
    monitor.wait()
