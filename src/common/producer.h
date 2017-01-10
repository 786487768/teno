/*
 * producer - x system common tools
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

 #include "rdkafka.h"   /* for Kafka driver */

 /* produce messages to kafka*/
 extern void produce_message(char *buf);