#include <mysql.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "src/common/tools.h"
#include "src/common/teno_error.h"

/* Establish connection with Mysql */
extern int 
connector_init(MYSQL *mysql, const char *user, const char *pwd, const char *db);

/* Terminate the connection with Mysql */
extern void 
connector_terminate(MYSQL *mysql);

/* Insert task info to mysql */
extern int 
insert_task(MYSQL *mysql, int user, 
                short task_type, short state, char* command);

/* Query task state */
extern int 
qurey_state(MYSQL *mysql, int task_id);

/* Update task state */
extern int 
update_state(MYSQL *mysql, int task_id, short state);