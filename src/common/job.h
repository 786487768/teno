#include <stdio.h>
#include <stdint.h>

typedef enum{
	JOB_INIT= 0,		/* Job's initial state*/
	JOB_LAUNCHING,		/* Launch thread is running*/
	JOB_WAITING,		/* Launch thread complete and job in queue*/
	JOB_RUNNING,		/* Consumer is executing*/
	JOB_SUCCESS,		/* Job finish successfully*/
	JOB_CANCEL,			/* Job is cancelled*/
	JOB_FAIL			/* Job fail*/
} job_state_t;

typedef struct{
	uint32_t job_id;
	char *job_cmd;
	char *job_argv;
	char *workdir;
	int uid;
	FILE *ifile;
	FILE *ofile;
	FILE *efile;
	FILE *cfile;
	job_state_t state;
}job_t;

extern void job_init(job_t **job);