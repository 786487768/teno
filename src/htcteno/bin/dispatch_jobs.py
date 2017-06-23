#!/usr/bin/env python
import os
import sys
import json
import redis
import threading
from os.path import isfile, join
sys.path.append('..')

from htc_celery.tasks import run_command

global dispatcher

def dispatch_tasks(begin, end):
    print("%s All tasks dispach begin" % (os.getpid))
    for index in range(begin, end):
        if dispatcher._input_dir != None:
            input_file_path = dispatcher._input_files_path[index]
            output_file_path = dispatcher._output_files_path[index]
            cmd = "%s %s >%s" % (
                    dispatcher._exec_program, input_file_path, output_file_path)
        else:
            output_file_path = join(dispatcher._output_dir, str(index))
            cmd = "%s >%s" % (dispatcher._exec_program, output_file_path)
        print(cmd)
        result = run_command.delay(cmd)
    print("%s All tasks dispach done" % (os.getpid))


class Dispatcher():

    task_nums = None
    _input_dir = None
    _output_dir = None
    _input_files_path = None
    _output_files_path = None
    _exec_program = None

    def __init__(self, host, port):
        self.redis_instance = redis.Redis(host=host, port=port)

    def set_info(self):
        # get setting from redis
        setting = json.loads(self.redis_instance.get(
            'htcteno_setting').decode('UTF-8'))
        self._exec_program = setting.get('exec')
        self._input_dir = setting.get('input')
        self._output_dir = setting.get('output')
        self.task_nums = int(setting.get('task_nums'))
        # get input file and output file
        if self._input_dir != None:
            input_files = [i for i in os.listdir(
                self._input_dir) if isfile(join(self._input_dir, i))]
            self._output_files_path = [
                join(self._output_dir, o) for o in input_files]
            self._input_files_path = [join(self._input_dir, i) for i in input_files]

        self.redis_instance.set('task_nums', self.task_nums)


if __name__ == '__main__':
    print("run dispatch_jos.py")
    redis_host = sys.argv[1]
    redis_port = sys.argv[2]
    dispatcher = Dispatcher(redis_host, redis_port)
    dispatcher.set_info()
    task_nums_per = dispatcher.task_nums // 5
    for i in range(5):
        begin_task = i * task_nums_per
        end_task = begin_task + task_nums_per
        print (begin_task, end_task)
        t = threading.Thread(target=dispatch_tasks, args=(begin_task, end_task, ))
        t.start()
        t.join()
    print("done dispatch_jos.py")
