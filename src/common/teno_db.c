#include "src/common/teno_db.h"


/* Establish connection with Mysql */
extern int 
connector_init(MYSQL *mysql, const char *user, const char *pwd, const char *db)
{
    if(NULL == mysql_init(mysql)){
        printf("mysql init failed: %s\n", mysql_error(mysql));
        return MYSQL_INIT_FAILED;
    }

    if(NULL == mysql_real_connect(mysql,
                        "localhost",
                        "ll",
                        "816543",
                        "tasks_info",
                        0,
                        NULL,
                        0)){
        printf("mysql_real_connect(): %s\n", mysql_error(mysql));
        return MYSQL_CONNECT_FAILED;
    }

    printf("Connect Mysql success!\n");
    return 0;
}

/* Terminate the connection with Mysql */
extern void connector_terminate(MYSQL *mysql)
{
    mysql_close(mysql);
}

/* Insert task info to mysql */
extern int insert_task(MYSQL *mysql, int user, 
            short task_type, short state, char* command)
{
    char datetime[20];
    int size = strlen(command) + 1 + 150;
    char *insert_sql;
    int return_code = 0;
    if(!(insert_sql=(char *)malloc(sizeof(char) * size))){
        printf("Insert_sql alloctes memory failed!\n");
        return MEMORY_ALLOCATE_FAILED;
    }
    get_current_datetime(datetime, 20);
    sprintf(insert_sql, "insert into tasks(user, task_type, state, start_time ,command) values(%d, %d, %d, '%s', '%s')", user, 
        task_type, state, datetime, command);
    if(!(_execute_sql(insert_sql, mysql)))
        return_code =  mysql_insert_id(mysql);
    else
        return_code =  EXECUTE_SQL_FAILED;
    free(insert_sql);
    return return_code;
}

extern int qurey_state(MYSQL *mysql, int task_id)
{
    char qurey_sql[50];
    MYSQL_RES *res = NULL;
    MYSQL_ROW row;
    sprintf(qurey_sql, "select state from tasks where id = %d", 
                task_id);
    _execute_sql(qurey_sql, mysql);
    res = mysql_store_result(mysql);
    if(!res){
        printf("mysql store result failed:%s\n", mysql_error(mysql));
        return MYSQL_STORE_FAILED; 
    }
    row = mysql_fetch_row(res);
    if(!row){
        printf("Task id error");
        return TASK_ID_ERROR;
    }
    else
        return row[0];
}

extern int update_state(MYSQL *mysql, int task_id, short state)
{
    char update_sql[50];
    sprintf(update_sql, "update tasks set state = %d where id = %d ", 
            state, task_id);
    printf("%s\n", update_sql);
    return _execute_sql(update_sql, mysql);
}

int _execute_sql(const char *sql, MYSQL *mysql)
{
    if(mysql_real_query(mysql, sql, strlen(sql))){
        printf("execute sql statement failed: %s\n", mysql_error(mysql));
        return EXECUTE_SQL_FAILED;
    }
    return 0;
}

