#include <stdio.h>

/*
 * log levels, logging will occur at or below the selected level
 * QUIET disable logging completely.
 */
typedef enum {
	LOG_LEVEL_QUIET = 0,
	LOG_LEVEL_FATAL,
	LOG_LEVEL_ERROR,
	LOG_LEVEL_INFO,
	LOG_LEVEL_DEBUG,
	LOG_LEVEL_DEBUG2,
	LOG_LEVEL_END
}	log_level_t;

/*
 * the following log a message to the log facility at the appropriate level:
 *
 * Messages do not need a newline!
 *
 * args are printf style with the following exceptions:
 * %m expands to strerror(errno)
 * %M expand to time stamp, format is configuration dependent
 * %t expands to strftime("%x %X") [ locally preferred short date/time ]
 * %T expands to rfc2822 date time  [ "dd, Mon yyyy hh:mm:ss GMT offset" ]
 */

/* fatal() exits program
 * error() returns TENO_ERROR
 */
void	fatal(const char *, ...) __attribute__ ((format (printf, 1, 2)));
int		error(const char *, ...) __attribute__ ((format (printf, 1, 2)));
void	info(const char *, ...) __attribute__ ((format (printf, 1, 2)));
void	debug(const char *, ...) __attribute__ ((format (printf, 1, 2)));
void	debug2(const char *, ...) __attribute__ ((format (printf, 1, 2)));