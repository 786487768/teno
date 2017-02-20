/*
 * Producer - Teno System Common Tools 
 *
 * Connect with kafka and produce command messages to kafka
 */

 #include <ctype.h>
 #include <signal.h>
 #include <unistd.h>
 #include <stdlib.h>
 #include <syslog.h>
 #include <time.h>
 #include <sys/time.h>
 #include <getopt.h>
 #include <string.h>
 #include <mysql.h>

 #include "rdkafka.h"   /* for Kafka driver */
 #include "src/common/task.h"
 #include "src/common/cJSON.h"
 #include "src/common/teno_db.h"
 /* produce messages to kafka*/
 extern void produce_message(char *buf, MYSQL *mysql);