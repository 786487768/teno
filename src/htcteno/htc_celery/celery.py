from __future__ import absolute_import, unicode_literals

import os
import json
import redis
from celery import Celery, Task

master_port = os.getenv("HTCTENO_PORT", 6379)
master_host = os.getenv("HTCTENO_HOST", None)
if not master_host:
    raise Exception("Error: No HTCTENO_HOST SET")

masterip = "%s:%s" % (master_host, master_port)

app = Celery('htc_celery',
             broker="redis://" + masterip,
             backend="redis://" + masterip,
             include=['htc_celery.tasks'])

app.conf.update(
    result_expires=3600,
    #    result_serializer = "pickle" ,
    #    accept_content = ['pickle' , 'json']
)


if __name__ == '__main__':
    app.start()
