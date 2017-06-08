import sys
import json
import time, threading

sys.path.append('..')
from slurm.slurm import Slurm


def run_test():
	a = ['python', 'accumulation.py']
	a = json.dumps(a)
	test_slurm = Slurm('srun', a)
	for i in range(0, 1000):
		test_slurm.test_run()

if __name__ == '__main__':
	start_time = time.time()
	t1 = threading.Thread(target=run_test)
	t2 = threading.Thread(target=run_test)
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	end_time = time.time()
	print ("run time = %f" % (end_time - start_time))