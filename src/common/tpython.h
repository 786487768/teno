#include <stdio.h>
#include <Python.h>

/* import module*/
extern PyObject *
import_name(const char *modname, const char *symbol);

/* compute the pow of num*/
extern double 
call_func(PyObject *func, double x, double y);

/* get result */
extern int
get_task_result(PyObject *func, const char *exec, const char *argv, 
                    char **exec_result, char **error);
