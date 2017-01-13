#!/bin/bash
SLURM_NNODES=1
HTCTENO_HOME=/home/ll/code/teno/src/htcteno
HTCTENO_PYTHON_PATH=${HTCTENO_HOME}/bin
export PATH=$HTCTENO_PYTHON_PATH:$PATH
export PYTHONPATH=$HTCTENO_HOME
# run this main shell on the head node .
REDIS_PATH=$1
REDIS_HOST=$2
REDIS_PORT=$3
CELERY_PATH=$4
SETTINTS=$5
export HTCTENO_HOST=${REDIS_HOST}
export HTCTENO_PORT=${REDIS_PORT}
# run redis-server
nohup ${REDIS_PATH} &> log.redis &

# set settings to redis
set_configure.py ${REDIS_HOST} ${REDIS_PORT} ${SETTINTS} &> log.setting &
# run worker
srun ${CELERY_PATH} -A htc_celery worker -l info &> log.worker &
# dispatch jobs
dispatch_jobs.py ${REDIS_HOST} ${REDIS_PORT} &> log.run &
# monitor the status of the task and clean server when task is finished
monitor.py ${REDIS_HOST} ${REDIS_PORT}
echo "task has been finished"
sleep 10

