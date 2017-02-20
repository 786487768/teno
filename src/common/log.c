
#include <errno.h>
#include <poll.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdarg.h>

#include "src/common/log.h"
#include "src/common/teno_error.h"

#  define LINEBUFSIZE 256

static int logfile_fd = 2;

static char *tstrfmt(const char *fmt, va_list ap);
static void log_msg(log_level_t level, const char *fmt, va_list args);

extern void 
fatal(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_msg(LOG_LEVEL_FATAL, fmt, ap);
    va_end(ap);

    exit(1);
}

extern int 
error(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_msg(LOG_LEVEL_ERROR, fmt, ap);
    va_end(ap);

    return TENO_ERROR;
}

extern void 
info(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_msg(LOG_LEVEL_INFO, fmt, ap);
    va_end(ap);
}

void debug(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_msg(LOG_LEVEL_DEBUG, fmt, ap);
    va_end(ap);
}

void debug2(const char *fmt, ...)
{
    va_list ap;

    va_start(ap, fmt);
    log_msg(LOG_LEVEL_DEBUG2, fmt, ap);
    va_end(ap);
}

static void
log_msg(log_level_t level, const char *fmt, va_list args)
{
    char *pfx = "";
    char *buf = NULL;

    switch(level){
        case LOG_LEVEL_FATAL:
            pfx = "fatal: ";
            break;
        case LOG_LEVEL_ERROR:
            pfx = "error: ";
            break;
        case LOG_LEVEL_INFO:
            pfx = "info: ";
            break;
        case LOG_LEVEL_DEBUG:
            pfx = "debug: ";
            break;
        case LOG_LEVEL_DEBUG2:
            pfx = "debug2: ";
            break;
        default:
            pfx = "internal error: ";
            break;
    }

    //buf = tstrfmt(fmt, args);
    fprintf(stderr, "%s\n", fmt);

}
/* return a heap allocated string formed from fmt and ap arglist
 * returned string is allocated with malloc, so must free with free.
 *
 * args are like printf, with the addition of the following format chars:
 * - %m expands to strerror(errno)
 * - %M expand to time stamp, format is configuration dependent
 * - %t expands to strftime("%x %X") [ locally preferred short date/time ]
 * - %T expands to rfc2822 date time  [ "dd, Mon yyyy hh:mm:ss GMT offset" ]
 *
 * simple format specifiers are handled explicitly to avoid calls to
 * vsnprintf and allow dynamic sizing of the message buffer. If a call
 * is made to vsnprintf, however, the message will be limited to 1024 bytes.
 * (inc. newline)
 *
 */
static char 
*tstrfmt(const char *fmt, va_list ap)
{
    char *buf = NULL;
    char *p = NULL;
    size_t len = (size_t)0;
    char tmp[LINEBUFSIZE];
    int unprocessed = 0;
    int long_long = 0;

    while(*fmt != '\0'){
        if((p = (char *)strchr(fmt, '%')) == NULL){
            xstrcat(buf, fmt);
        }
    }
}