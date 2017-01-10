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
from utils.static_keys import StaticKeys
from utils.parse_configure import parse_configure_file

def _usage():
    print ('''usage:      htcrun [exec] <exec argvs>
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

    # get configure info
    configure_info = parse_configure_file()
    redis_host = configure_info.get(StaticKeys.REDIS_HOST)
    redis_port = configure_info.get(StaticKeys.REDIS_PORT)
    redis_path = configure_info.get(StaticKeys.REDIS_PATH)
    celery_path = configure_info.get(StaticKeys.CELERY_PATH)

    setting = {}
    setting['exec'] = ' '.join(exec_program)
    setting['input'] = input_dir
    setting['output'] = output_dir
    settings = json.dumps(setting).encode('utf-8')
    print (type(settings))
    slurm_argvs = ['bash', 'run.sh', redis_path, redis_host, redis_port, celery_path, settings]

    try:
        p = Popen(slurm_argvs, stdout=PIPE, stderr=PIPE)
        (output, error) = p.communicate()
        print (output, error)
    except Exception:
        print ("sbatch failed")












