/*
 * Submit - Teno System task Submit command
 */

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>

#include "src/common/log.h"
#include "src/common/producer.h"

static char *EXEC = "srun";
static void _usage(char *process_name);

int main(int argc, const char **argv){

    task_t *task;
    int opt, i;
    char *task_argv = NULL;
    char *input_file = NULL;
    char *output_file = NULL;
    char *error_file = NULL;
    char *conf_file = NULL;
    char *command = NULL;
    cJSON *message = cJSON_CreateObject();
    cJSON *argv_array = cJSON_CreateStringArray(argv + 1, argc - 1);

    int size = 0, task_id = -1;
    MYSQL mysql;

    task_init(&task);
    if(task == NULL)
        printf("error\n");
    if(connector_init(&mysql, "ll", "816543", "tasks_info"))
        return -1;
/*    while((opt = getopt(argc, argv, "a:c:e:i:o:w:h")) != -1){
        switch(opt){
            case 'c':
                if((task->cfile = fopen(optarg, "r")) == NULL)
                    error("configure file open fail");
                break;
            case 'e':
                if((task->efile = fopen(optarg, "a")) == NULL)
                    error("error file open fail");
                break;
            case 'i':
                if((task->ifile = fopen(optarg, "r")) == NULL)
                    error("input file open fail");
                break;
            case 'o':
                if((task->ofile = fopen(optarg, "a")) == NULL)
                    error("output file open fail");
                break;
            case 'w':
                task->workdir = optarg;
                break;
            case 'h':
                _usage(argv[0]);
                exit(1);
            default:
                printf("%s\n", optarg);
        }
    }

    if(argc <= 1 || optind >= argc){
        _usage(argv[0]);
        exit(1);
    }*/
    task->uid = getuid();
    task->task_exec = EXEC;

    task_argv = cJSON_Print(argv_array);
    size = strlen(task_argv) + strlen(task->task_exec) + 1;
    command = (char *)malloc(sizeof(char) * size);
    sprintf(command, "%s %s", task->task_exec, task_argv);
    task_id = insert_task(&mysql, task->uid, 0, TASK_LAUNCHING, command);
    printf("task id = %d\n", task_id);

    cJSON_AddNumberToObject(message, "task_id", task_id);
    cJSON_AddStringToObject(message, "exec", task->task_exec);
    cJSON_AddItemToObject(message, "argv", argv_array);
    cJSON_AddNumberToObject(message, "uid", task->uid);
    char *out = cJSON_Print(message);

    if(out)
        produce_message(out, &mysql);

    cJSON_Delete(message);
    connector_terminate(&mysql);
    free(out);
    return 0;
}

static void 
_usage(char *process_name){
    fprintf(stderr, 
        "Usage: %s [cmd/exec] <-a argv>)\n"
        "\n"
        "Options:\n"
        "   -c                 Conf file\n"
        "   -w                 Workdir\n"
        "   -i                 Inputfile\n"
        "   -o                 Outputfile\n"
        "\n"
        "\n"
        ,process_name);
}