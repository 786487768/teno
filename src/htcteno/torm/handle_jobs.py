import sys
import datetime
sys.path.append('..')
sys.path.append('../..')
from htcteno import session
from torm.entity import Jobs
from utils.static_keys import TASK_STATE

def insert_job(task_id, celery_id, state, command):
    " Create new job for the task_id "
    end_time = datetime.datetime.now()
    job = Jobs(task_id=task_id, celery_id=celery_id, \
                end_time=end_time, state=state, command=command)
    session.add(job)
    session.commit()

def update_state(job_id, state):
    " Update job state "
    job = session.query(Jobs).filter_by(id=job_id).first()
    job.state = state

    session.commit()

def get_success_jobs_num_by_task_id(task_id):
    " Get success jobs number by task id "
    success_jobs_number = session.query(Jobs).filter_by(task_id=task_id, \
            state=TASK_STATE.SUCCESS).count()
    return success_jobs_number

def get_fail_jobs_num_by_task_id(task_id):
    " Get fail jobs number by task id "
    fail_jobs_number = session.query(Jobs).filter_by(task_id=task_id, \
            state=TASK_STATE.FAIL).count()
    return fail_jobs_number