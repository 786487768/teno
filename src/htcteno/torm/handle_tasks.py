import sys
import datetime
sys.path.append('..')
sys.path.append('../..')
# from htcteno import session
from torm.entity import Tasks


def insert_task(user, task_type, state, redis_host,
                redis_port, total_jobs, command=None):
    " Create a new task and return task id"
    start_time = datetime.datetime.now()
    task = Tasks(user=user, task_type=task_type, state=state,
                 start_time=start_time, redis_host=redis_host,
                 redis_port=redis_port, total_jobs=total_jobs, command=command)
    session.add(task)
    insert_result = session.query(Tasks).filter_by(user=user,
                                                   start_time=start_time).order_by(Tasks.id.desc()).first()
    session.commit()
    if insert_result:
        return insert_result.id


def update_slurm_id(task_id, slurm_id):
    " After submit to slurm successfully, update task slurm_id"
    task = session.query(Tasks).filter_by(id=task_id).first()
    task.slurm_id = slurm_id
    session.commit()


def update_task_state(task_id, state):
    " update task state"
    task = session.query(Tasks).filter_by(id=task_id).first()
    task.state = state
    session.commit()


def get_task_info_by_id(task_id):
    task = session.query(Tasks).filter_by(id=task_id).first()
    return task
