from __future__ import absolute_import, unicode_literals

import os
import signal
from subprocess import PIPE, Popen
from htc_celery.HtcTask import HtcTask
from htc_celery.celery import app


class ExceptionReturn (Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(base=HtcTask, bind=True, autoretry_for=(Exception,), track_started=True, max_retries=3, default_retry_delay=1)
def run_command(self, command, env=None, timeout=600):
    args = ["bash", "-c", "-l", command]
    try:
        p = Popen(args, stdout=PIPE, stderr=PIPE)
    except OSError as ex:
        raise self.retry(exc=ex)
    output = ""
    error = ""
    retcode = 0
    signal.alarm(timeout)
    try:
        (output, error) = p.communicate()
        retcode = p.poll()
        signal.alarm(0)  # reset the alarm
    except Exception as exc:
        raise exc
    run_command.get_redis_instance.lpush('compelete_list', 1)
    return [retcode]
