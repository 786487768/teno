#!/bin/bash

## get config args
REDIS_PATH=$1
REDIS_HOST=$HOSTNAME
REDIS_PORT=$3
CELERY_PATH=$4
PYTHON_PATH=$5
HTCTENO_HOME=$6
SETTINGS=$7

HTCTENO_PYTHON_PATH=${HTCTENO_HOME}/bin
export PATH=$PYTHON_PATH:$HTCTENO_PYTHON_PATH:$PATH
export PYTHONPATH=$HTCTENO_HOME:$PYTHONPATH
# set htc teno head node
export HTCTENO_HOST=${REDIS_HOST}
export HTCTENO_PORT=${REDIS_PORT}
# run redis-server
nohup ${REDIS_PATH} &> log.redis
# run rabbitmq
nohup rabbitmq-server &> log.rabbitmq
is_startup=`ps -aux | grep 5672 | wc -l`
while (( $is_startup == 0 ))
do
	echo $is_startup
	sleep 3
	is_startup=`ps -aux | grep 5672 | wc -l`
	echo "wait rabbitmq startup"
done
# set rabbitmq user
rabbitmqctl add_user ll 816543 &> log.rabbitmq
rabbitmqctl set_user_tags ll consumer &> log.rabbitmq
rabbitmqctl set_permissions -p / ll "." "." ".*" &> log.rabbitmq
# set settings to redis
echo ${SETTINGS}
set_configure.py ${REDIS_HOST} ${REDIS_PORT} ${SETTINGS} &> log.setting
# run worker
echo $SLURM_NNODES
srun -N ${SLURM_NNODES} -n ${SLURM_NNODES} ${CELERY_PATH} -A htc_celery worker -l info &> log.worker.${HOSTNAME} &
# dispatch jobs
dispatch_jobs.py ${REDIS_HOST} ${REDIS_PORT} &> log.run
# monitor the status of the task and clean server when task is finished
monitor.py ${REDIS_HOST} ${REDIS_PORT} &> log.monitor
echo "task has been finished"