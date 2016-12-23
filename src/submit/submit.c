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

static void _usage(char *process_name);

int main(int argc, char **argv){

    job_t *job;
    int opt, i;
    char *job_argv = NULL;
    char *input_file = NULL;
    char *output_file = NULL;
    char *error_file = NULL;
    char *conf_file = NULL;
    
    cJSON *message = cJSON_CreateObject();

    job_init(&job);

    if(job == NULL)
        printf("error\n");
    while((opt = getopt(argc, argv, "a:c:e:i:o:w:h")) != -1){
        switch(opt){
            case 'a':
                job->job_argv = optarg;
                break;
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
            default:
                _usage(argv[0]);
                exit(1);
        }
    }

    if(argc <= 1 || optind >= argc){
        _usage(argv[0]);
        exit(1);
    }
    job->uid = getuid();
    job->job_cmd = *(argv + optind);
    cJSON_AddStringToObject(message, "cmd", job->job_cmd);
    if(job->job_argv == NULL)
        cJSON_AddStringToObject(message, "argv", "");
    else
        cJSON_AddStringToObject(message, "argv", job->job_argv);
    cJSON_AddNumberToObject(message, "uid", job->uid);
    char *out = cJSON_Print(message);
    printf("%s\n", out);


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