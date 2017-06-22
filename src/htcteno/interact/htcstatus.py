import sys
sys.path.append('..')

from torm.entity import Tasks
from utils.static_keys import TASK_STATE
from torm.handle_tasks import get_task_info_by_id
from torm.handle_jobs import get_success_jobs_num_by_task_id, \
    get_fail_jobs_num_by_task_id

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" Please input Job ID ")
        exit(1)

    task_id = sys.argv[1]
    task_info = get_task_info_by_id(task_id)
    if task_info:
        total_jobs = task_info.total_jobs
        state = TASK_STATE.STATE_DESCRIPTION2[task_info.state]
        success_jobs_num = get_success_jobs_num_by_task_id(task_id)
        fail_jobs_num = get_fail_jobs_num_by_task_id(task_id)
        running_jobs_num = total_jobs - success_jobs_num - fail_jobs_num
        print("%5s %10s %8s %8s %8s %8s" % ('id', 'state', 'total', 'success',
                                            'fail', 'run'))
        print("%5s %10s %8s %8s %8s %8s" % (task_id, state, total_jobs, success_jobs_num,
                                            fail_jobs_num, running_jobs_num))
    else:
        print(" error task id ")
