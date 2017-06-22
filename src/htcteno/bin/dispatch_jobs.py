#!/usr/bin/env python
import os
import sys
import json
import redis
from os.path import isfile, join
sys.path.append('..')

from htc_celery.tasks import run_command


class Dispatcher():

    def __init__(self, host, port):
        self.redis_instance = redis.Redis(host=host, port=port)

    def run_jobs(self):
        # get setting from redis
        setting = json.loads(self.redis_instance.get(
            'htcteno_setting').decode('UTF-8'))
        exec_program = setting.get('exec')
        input_dir = setting.get('input')
        output_dir = setting.get('output')
        task_nums = int(setting.get('task_nums'))
        # get input file and output file
        if input_dir != None:
            input_files = [i for i in os.listdir(
                input_dir) if isfile(join(input_dir, i))]
            output_files_path = [join(output_dir, o) for o in input_files]
            input_files_path = [join(input_dir, i) for i in input_files]

        for index in range(task_nums):
            if input_dir != None:
                input_file_path = input_files_path[index]
                output_file_path = output_files_path[index]
                cmd = "%s %s >%s" % (
                    exec_program, input_file_path, output_file_path)
            else:
                output_file_path = join(output_dir, str(index))
                cmd = "%s >%s" % (exec_program, output_file_path)
            exec_program_name = exec_program.split(' ')[0]
            tname = "%s_%s" % (exec_program_name, index)
            print(cmd)
            result = run_command.delay(cmd)
            task_info = {}
            task_info['task_name'] = tname
            task_info['task_cmd'] = cmd
            task_info['task_id'] = result.task_id
            task_info = json.dumps(task_info)
            self.redis_instance.hmset('thht_id_name', {result.task_id: tname})
            self.redis_instance.hmset(
                'thht_id_info', {result.task_id: task_info})
            self.redis_instance.hmset('thht_name_id', {tname: result.task_id})
            self.redis_instance.hmset('thht_id_pd', {result.task_id: 'pd'})


if __name__ == '__main__':
    print("run dispatch_jos.py")
    redis_host = sys.argv[1]
    redis_port = sys.argv[2]
    dispatcher = Dispatcher(redis_host, redis_port)
    dispatcher.run_jobs()
