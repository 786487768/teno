#include "src/common/tpython.h"

int main(){
    PyObject *pow_func;

    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('..')");
    pow_func = import_name("slurm.slurm", "run");
    printf("%s\n", get_task_result(pow_func, "srun", ""));
    Py_DECREF(pow_func);
    Py_Finalize();
    return 0;
}