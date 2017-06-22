# coding=utf-8
#!/usr/bin/env python

import os
import sys
import json
from os.path import isfile, isdir, join, dirname
from subprocess import Popen, PIPE
from getopt import getopt, GetoptError
sys.path.append('..')
sys.path.append('../..')

#  from slurm.slurm import Slurm
from utils.static_keys import StaticKeys, JOB_TYPE, TASK_STATE
from utils.parse_configure import parse_all_configure
# from torm.handle_tasks import insert_task, update_slurm_id, update_task_state


def _usage():
    print ('''usage:      htcrun [exec] <exec argvs>
            -C      configure file
            -I      input dir
            -O      output dir
            -h      help''')
    exit(1)
if __name__ == '__main__':
    try:
        opts, argvs = getopt(sys.argv[1:], "C:I:n:N:O:h",
                             ['configure=',
                              'input=',
                              'tasks=',
                              'nodes=',
                              'output=',
                              'help'])
    except GetoptError:
        _usage()

    if len(argvs) == 0:
        print("please appoint executable program")
        _usage()
    else:
        exec_program = argvs
    print(exec_program)
    if not isfile(exec_program[0]):
        print("exec is not exist")
        exit(2)
    task_nums = None
    node_nums = None
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
        elif opt in ('-n', '--tasks'):
            task_nums = arg
        elif opt in ('-N', '--nodes'):
            node_nums = arg
        elif opt in ('-O', '--output'):
            output_dir = arg
        else:
            _usage()
    # init node nums
    if node_nums == None:
        node_nums = 1
    # init task nums
    if input_dir:
        input_files = [i for i in os.listdir(input_dir) if
                       os.path.isfile(join(input_dir, i))]
        task_nums = len(input_files)
    elif task_nums == None:
        task_nums = 1
    else:
        pass
    # create output dir
    if output_dir:
        if not isdir(output_dir):
            os.mkdir(output_dir)
    else:
        output_dir = join(os.getcwd(), 'output')
        if not isdir(output_dir):
            os.mkdir(output_dir)

    # get configure info, for example redis、celery、python
    configure_info = parse_all_configure(configure_file)
    print(configure_info)
    # redis host is definited when the task will be startup in current version
    redis_host = configure_info.get(StaticKeys.REDIS_HOST)
    redis_port = configure_info.get(StaticKeys.REDIS_PORT)
    redis_path = configure_info.get(StaticKeys.REDIS_PATH)
    python_path = configure_info.get(StaticKeys.PYTHON_PATH)
    celery_path = configure_info.get(StaticKeys.CELERY_PATH)
    htcteno_home = dirname(os.getcwd())
    # create a new task
    # userid
    user = os.getuid()
    # command info
    job_command_args = ' '.join(exec_program)
    job_command = "%s -I %s -O %s" % (job_command_args, input_dir, output_dir)
    '''
    task_id = insert_task(user, TASK_TYPE.HTC_TASK, TASK_STATE.SUBMITED, \
            redis_host, redis_port, task_nums, job_command)
    if task_id == None:
        print ("task submit fail")
        # 作业信息插入失败
        update_task_state(task_id, TASK_STATE.SUBMIT_ERROR)
        exit(3)
    '''
    setting = {}
    setting['job_id'] = 0
    setting['exec'] = job_command_args
    setting['input'] = input_dir
    setting['output'] = output_dir
    setting['node_nums'] = node_nums
    setting['task_nums'] = task_nums
    settings = json.dumps(setting).encode('utf-8')
    print(setting)
    print(python_path, redis_path, htcteno_home, celery_path)
    slurm_argvs = ['sbatch', '-N', node_nums, 'run.sh',
                   redis_path, redis_host, redis_port, celery_path,
                   python_path, htcteno_home, settings]
    try:
        p = Popen(slurm_argvs, stdout=PIPE, stderr=PIPE)
        (output, error) = p.communicate()
        print(output, error)
    except Exception:
        print("sbatch failed")
        # 开启进程执行slurm命令失败
        # update_task_state(task_id, TASK_STATE.SUBMIT_ERROR)

    if error:
        print(error)
        # 作业提交至slurm的过程中出错
        # update_task_state(task_id, TASK_STATE.SUBMIT_ERROR)
    else:
        print("your job has been started")
        slurm_id = output.decode('UTF-8').strip().split(' ')[-1]
        # 作业成功提交至slurm作业队列中
        # update_task_state(task_id, TASK_STATE.WAITTINT)
        # 根据slurm返回的信息更新作业信息
        # update_slurm_id(task_id, slurm_id)
