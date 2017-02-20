#include <stdio.h>
#include <malloc.h>

#include "src/common/task.h"
#include "src/common/log.h"


extern void
task_init(task_t **task)
{
    if((*task = (task_t *)malloc(sizeof(task_t))) == NULL)
        printf("task init fail\n");
    (*task)->task_id = -1;
    (*task)->task_exec = NULL;
    (*task)->task_argv = NULL;
    (*task)->workdir = NULL;
    (*task)->uid = 0;
    (*task)->ifile = stdin;
    (*task)->ofile = stdout;
    (*task)->efile = stderr;
    (*task)->cfile = NULL;
    (*task)->state = TASK_INIT;
}