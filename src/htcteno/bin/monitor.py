#!/usr/bin/env python
import sys
import json
import redis
from subprocess import Popen, PIPE
sys.path.append('../..')

from htcteno import session

class Monitor():
    """ Monitor the status of jobs and clean resource after 
                task has been finished """
    def __init__(self, host, port):
        self.redis_instance = redis.Redis(host=host, port=port)
        setting = json.loads(self.redis_instance.get( \
                'htcteno_setting').decode('UTF-8'))
        self.teno_id = setting.get('task_id')
        self.is_finished = False

    def wait(self):
        while 1:
            sln = self.redis_instance.llen('success_list')
            fln = self.redis_instance.llen('fail_list')
            aln = self.redis_instance.hlen('thht_id_name')
            if sln + fln == aln:
                fail_list = self.redis_instance.lrange('fail_list', 0, fln)
                for fail_job in fail_list:
                    task_id = fail_job.get('task_job')
                    task_info = json.loads(self.redis_instance.hget( \
                        'thht_id_info', task_id).decode('UTF-8'))
                    print ("Total Jobs: %s Success Jobs: %s Fail Jobs: %s" \
                        % (aln, sln, fln))
                    print ("fail job:%s %s %s" %(task_id, task_info.get( \
                        'task_cmd'), fail_job.get('exc')))
                self.is_finished = True
                self._clean()
                break

    def _clean(self):
        kill_celery = ['bash', '-c', 'killall', '-9', 'celery']
        kill_redis_server = ['bash', '-c','killall', '-9', 'redis-server']
        Popen(kill_celery, stdout=PIPE, stderr=PIPE)
        Popen(kill_redis_server, stdout=PIPE, stderr=PIPE)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ("monitor argv error")
    host, port = sys.argv[1], sys.argv[2]
    monitor = Monitor(host, port)
    monitor.wait()


