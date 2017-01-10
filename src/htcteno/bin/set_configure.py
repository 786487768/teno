#!/usr/bin/env python
import sys
import json
import redis

if __name__ == '__main__':
    print ("run set_configure.py")
    redis_host = sys.argv[1]
    redis_port = sys.argv[2]
    # shell.sh call .py argv problem
    configure = sys.argv[3:]
    setting = ''.join(configure)
    setting = json.loads(setting)
    r = redis.Redis(host=redis_host, port=redis_port)
    if not r.set('htcteno_setting', json.dumps(setting)):
        print ("setting configure error")