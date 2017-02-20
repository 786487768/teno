#include <stdio.h>
#include <stdint.h>

typedef enum{
    TASK_LAUNCHING = 0,   /* Launch thread is running*/
    TASK_WAITING,         /* Launch thread complete and task in queue*/
    TASK_RUNNING,         /* Consumer is executing*/
    TASK_SUCCESS,         /* Task finish successfully*/
    TASK_FAIL,            /* Task fail*/
    TASK_PENDDING,        /* Task is Pendding */
    TASK_CANCEL,          /* Task is cancelled*/
    TASK_INIT = 100       /* Task's initial state*/
} task_state_t;

typedef enum{
    NORMAL_TASK = 0,      /* normal task */
    HTC_TASK,             /* htc task */
    OTHER_TASK            /* other task */
} task_type_t;

typedef struct{
    uint32_t task_id;
    char *task_exec;
    char *task_argv;
    char *workdir;
    int uid;
    FILE *ifile;
    FILE *ofile;
    FILE *efile;
    FILE *cfile;
    task_state_t state;
}task_t;

extern void task_init(task_t **task);