#include <stdio.h>
#include "src/common/tpython.h"

extern PyObject *
import_name(const char *modname, const char *symbol){
    PyObject *u_name, *module;
    u_name = PyUnicode_FromString(modname);
    module = PyImport_Import(u_name);
    Py_DECREF(u_name);
    return PyObject_GetAttrString(module, symbol);
}

extern double
call_func(PyObject *func, double x, double y){
    PyObject *args;
    PyObject *kwargs;
    PyObject *result = 0;
    double retval;

    /* Make sure own thr GIL */
    PyGILState_STATE state = PyGILState_Ensure();

    /* Verify the func is a proper callable */
    if(!PyCallable_Check(func)){
        fprintf(stderr, "call_func: expected a callable\n");
        goto fail;
    }
    /* Biuld arguments */
    args = Py_BuildValue("dd", x, y);
    kwargs = NULL;

    /* Call the function */
    result = PyObject_Call(func, args, kwargs);
    Py_DECREF(args);
    Py_XDECREF(kwargs);

    /* Check for python exception */
    if(PyErr_Occurred()){
        PyErr_Print();
        goto fail;
    }

    /* Vertify the result is a float object */
    if(!PyFloat_Check(result)){
        fprintf(stderr, "call_func: callable didn't return a float\n");
        goto fail;
    }

    /* Create the return value */
    retval = PyFloat_AsDouble(result);
    Py_DECREF(result);

    /* Restore previous GIL state and return */
    PyGILState_Release(state);
    return retval;

fail:
    Py_DECREF(result);
    PyGILState_Release(state);
    exit(8);

}

extern char *
get_task_result(PyObject *func, const char *exec, const char *argv){
    PyObject *args;
    PyObject *kwargs;
    PyObject *result = 0;
    char *retval;

    /* Make sure own thr GIL */
    PyGILState_STATE state = PyGILState_Ensure();

    /* Verify the func is a proper callable */
    if(!PyCallable_Check(func)){
        fprintf(stderr, "call_func: expected a callable\n");
        goto fail;
    }
    /* Biuld arguments */
    args = Py_BuildValue("ss", exec, argv);
    kwargs = NULL;

    /* Call the function */
    result = PyObject_Call(func, args, kwargs);
    Py_DECREF(args);
    Py_XDECREF(kwargs);

    /* Check for python exception */
    if(PyErr_Occurred()){
        PyErr_Print();
        goto fail;
    }

    /* Vertify the result is a Unicode object */
    if(!PyBytes_Check(result)){
        fprintf(stderr, "call_func: callable didn't return a normal result\n");
        goto fail;
    }

    /* Create the return value */
    retval = PyBytes_AsString(result);
    Py_DECREF(result);

    /* Restore previous GIL state and return */
    PyGILState_Release(state);
    return retval;

fail:
    Py_DECREF(result);
    PyGILState_Release(state);
    exit(8);
}