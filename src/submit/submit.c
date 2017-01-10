/*
 * x system command: submit
 */

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

#include "src/common/log.h"
#include "src/common/job.h"
#include "src/common/cJSON.h"
#include "src/common/producer.h"

static char *EXEC = "srun";
static void _usage(char *process_name);

int main(int argc, const char **argv){

    job_t *job;
    int opt, i;
    char *job_argv = NULL;
    char *input_file = NULL;
    char *output_file = NULL;
    char *error_file = NULL;
    char *conf_file = NULL;
    cJSON *message = cJSON_CreateObject();
    cJSON *argv_array = cJSON_CreateStringArray(argv + 1, argc - 1);
    cJSON *arg;
    job_init(&job);

    if(job == NULL)
        printf("error\n");
/*    while((opt = getopt(argc, argv, "a:c:e:i:o:w:h")) != -1){
        switch(opt){
            case 'c':
                if((job->cfile = fopen(optarg, "r")) == NULL)
                    error("configure file open fail");
                break;
            case 'e':
                if((job->efile = fopen(optarg, "a")) == NULL)
                    error("error file open fail");
                break;
            case 'i':
                if((job->ifile = fopen(optarg, "r")) == NULL)
                    error("input file open fail");
                break;
            case 'o':
                if((job->ofile = fopen(optarg, "a")) == NULL)
                    error("output file open fail");
                break;
            case 'w':
                job->workdir = optarg;
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
    job->uid = getuid();
    job->job_exec = EXEC;
    cJSON_AddStringToObject(message, "exec", job->job_exec);
    cJSON_AddItemToObject(message, "argv", argv_array);
    cJSON_AddNumberToObject(message, "uid", job->uid);
    char *out = cJSON_Print(message);
    printf("%s\n", out);

    produce_message(out);
    cJSON_Delete(message);
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