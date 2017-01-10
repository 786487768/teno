#include <stdio.h>
#include <malloc.h>

#include "src/common/job.h"
#include "src/common/log.h"


extern void
job_init(job_t **job)
{
    if((*job = (job_t *)malloc(sizeof(job_t))) == NULL)
        printf("job init fail\n");
    (*job)->job_id = -1;
    (*job)->job_exec = NULL;
    (*job)->job_argv = NULL;
    (*job)->workdir = NULL;
    (*job)->uid = 0;
    (*job)->ifile = stdin;
    (*job)->ofile = stdout;
    (*job)->efile = stderr;
    (*job)->cfile = NULL;
    (*job)->state = JOB_INIT;
}