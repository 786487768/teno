#!/usr/bin/env python

import os
import sys
import json
from os.path import isfile, isdir, join
from subprocess import Popen, PIPE
from getopt import getopt, GetoptError
sys.path.append('..')
sys.path.append('../..')

from slurm.slurm import Slurm
from utils.static_keys import StaticKeys, TASK_TYPE, TASK_STATE
from utils.parse_configure import parse_all_configure
from torm.handle_tasks import insert_task, update_slurm_id, update_task_state

def _usage():
    print ('''usage:      htcrun [exec] <exec argvs>
            -C      configure file
            -I      input dir
            -O      output dir
            -h      help''') 
    exit(1)
if __name__ == '__main__':
    try:
        opts, argvs = getopt(sys.argv[1:], "C:I:O:h", ['configure=', 'input=', 'output=', 'help'])
    except GetoptError:
        _usage()

    if len(argvs) == 0:
        print ("please appoint executable program")
        _usage()
    else:
        exec_program = argvs
    if not isfile(exec_program[0]):
        print ("exec is not exist")
        exit(2)
    input_dir = None
    output_dir = None
    configure_file = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            _usage()
        elif opt in ('-C', '--configure'):
            configure_file = arg
        elif opt in ('-I', '--input'):
            input_dir = arg
        elif opt in ('-O', '--output'):
            output_dir = arg
        else:
            _usage()

    if input_dir:
        if not isdir(input_dir):
            print ("input dir is not exist")
            exit(2)
    else:
        print ("please use -I to appoint input file dir")
        _usage()

    if output_dir:
        if not isdir(output_dir):
            os.mkdir(output_dir)
    else:
        output_dir = join(os.getcwd(), 'output')
        if not isdir(output_dir):
            os.mkdir(output_dir)

    # get configure info, for example redis、celery、python
    configure_info = parse_all_configure()
    redis_host = configure_info.get(StaticKeys.REDIS_HOST)
    redis_port = configure_info.get(StaticKeys.REDIS_PORT)
    redis_path = configure_info.get(StaticKeys.REDIS_PATH)
    python_path = configure_info.get(StaticKeys.PYTHON_PATH)
    celery_path = configure_info.get(StaticKeys.CELERY_PATH)
    # create a new task record
    user = os.getuid()
    input_files = [i for i in os.listdir(input_dir) if os.path.isfile(join(input_dir, i))]
    total_jobs = len(input_files)
    command = ' '.join(exec_program)
    command_all = "%s -I %s -O %s" %(command, input_dir, output_dir)
    task_id = insert_task(user, TASK_TYPE.HTC_TASK, TASK_STATE.SUBMITED, \
            redis_host, redis_port, total_jobs, command_all)
    if task_id == None:
        print ("task submit fail")
        exit(3)

    setting = {}
    setting['task_id'] = task_id
    setting['exec'] = command
    setting['input'] = input_dir
    setting['output'] = output_dir
    settings = json.dumps(setting).encode('utf-8')
    slurm_argvs = ['sbatch', 'run.sh', redis_path, redis_host, \
            redis_port, celery_path, python_path, settings]
    try:
        p = Popen(slurm_argvs, stdout=PIPE, stderr=PIPE)
        (output, error) = p.communicate()
        print (output, error)
    except Exception:
        print ("sbatch failed")
        update_task_state(task_id, TASK_STATE.SUBMIT_ERROR)

    if error:
        print (error)
        update_task_state(task_id, TASK_STATE.SUBMIT_ERROR) 
    else:
        slurm_id = output.decode('UTF-8').strip().split(' ')[-1]
        update_task_state(task_id, TASK_STATE.WAITTINT) 
        update_slurm_id(task_id, slurm_id)












