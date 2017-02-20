#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include "src/common/tools.h"
/* get current time format 2017-2-15 4:19:30*/
extern void 
get_current_datetime(char *buf, int size)
{
    time_t t;
    struct tm *tmp;

    time(&t);
    tmp = localtime(&t);
    if(strftime(buf, size, "%F %X", tmp) == 0)
        printf("buffer size %d is too small\n", size);
}
