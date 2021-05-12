# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# -*- coding: utf-8 -*-
'''This module implements a task class called :class:`PythonTask`, which is
able to execute arbitrary Python code (in the form of a function call) when
requested to do so. This is extra useful because functions wrapped in
:class:`PythonTask` can receive the scheduling environment as an additional
parameter, which makes it possible to write code that depends on the results of
previous tasks.

:class:`PythonTask` objects
---------------------------

Creating a :class:`PythonTask` is very simple. Let us define a function that
returns a constant value:

    >>> def func():
    ...   return 42

We can wrap the function in a :class:`PythonTask` as follows:

    >>> task = PythonTask('answer', func)  # 'answer' is the task name

We can then execute the task by passing an empty environment (dictionary) and
an empty :class:`~.Config` to the :meth:`PythonTask.do` method:

    >>> task.do(env={}, config=None)
    42

Note that :meth:`PythonTask.do` simply returns the result of the wrapped
function. For the sake of illustration, our function returns an integer;
however, if you want to use :class:`PythonTask` in a :class:`~.DepGraph`, your
wrapped function will need to return an `(env_up, status)` pair, like the other
tasks.

.. note::

    Exceptions raised by the wrapped function are not caught by the task (they
    should be caught by the scheduler, though).

Calling a function without any arguments is not very restrictive per se.
Say you want to call a function of two arguments:

    >>> def add(x, y):
    ...   return x + y

If you have your arguments lying around at the time you construct your task,
then you may do something like

    >>> x, y = 5, 3
    >>> task_add = PythonTask('add', lambda: add(x, y))
    >>> task_add.do(env={}, config=None)
    8

Essentially, you construct a trampoline: the lambda takes no arguments, but it
captures `x` and `y` from the surrounding scope and passes them to the
:func:`!add` function. This works, but due to the way Python handles captured
variables, it may bring a few surprises:

    >>> x, y = 5, 3
    >>> task_add = PythonTask('add', lambda: add(x, y))
    >>> x, y = 1, 2
    >>> task_add.do(env={}, config=None)  # this still returns 8, right?
    3
    >>> # WAT

So, unless you know what you are doing, it is better to avoid this surprising
behaviour and use the `args` argument to :class:`PythonTask`:

    >>> x, y = 5, 3
    >>> task_add = PythonTask('add', add, args=(x, y))
    >>> task_add.do(env={}, config=None)
    8

There is also a `kwargs` argument that can be used to pass keyword arguments:

    >>> task_add = PythonTask('add', add, kwargs={'x': x, 'y': y})
    >>> task_add.do(env={}, config=None)
    8


Passing arguments via the environment
-------------------------------------

Sometimes your function requires some arguments, but the arguments themselves
are not available (e.g. they haven't been computed yet) by the time you create
your :class:`PythonTask`. For this purpose, :class:`PythonTask` provides an
additional feature that allows the called function to query the task
environment and retrieve any additional information from there.

The mechanism is simple: the environment is passed to the wrapped function as a
keyword argument. The keyword can be specified by the user using the
`env_kwarg` argument to the :class:`PythonTask` constructor.

As a simple example, consider the following function:

    >>> def goodnight(*, some_dict):
    ...   number = some_dict['number']
    ...   return 'Goodnight, ' + ('ding'*number)

You can wrap it in a :class:`PythonTask` as follows:

    >>> task_gnight = PythonTask('goodnight', goodnight, env_kwarg='some_dict')

and this is how it works:

    >>> env = {'number': 8}
    >>> task_gnight.do(env, config=None)
    'Goodnight, dingdingdingdingdingdingdingding'

Passing arguments via the environment: a more complex example
-------------------------------------------------------------

As an illustration of a more complex scenario, we will now implement a set of
:class:`PythonTask` objects to calculate the Pascal's triangle. In plain
Python, the code to print all the rows up to the n-th would look something like
this:

    >>> import numpy as np
    >>> def pascal(n):
    ...   res = np.zeros((n, n), dtype=int)
    ...   res[:, 0] = 1
    ...   res[0, :] = 1
    ...   for i in range(2, n):
    ...     for j in range(1, i):
    ...       res[i-j, j] = res[i-j-1, j] + res[i-j, j-1]
    ...   return res
    >>> direct_pascal = pascal(8)
    >>> print(direct_pascal)
    [[ 1  1  1  1  1  1  1  1]
     [ 1  2  3  4  5  6  7  0]
     [ 1  3  6 10 15 21  0  0]
     [ 1  4 10 20 35  0  0  0]
     [ 1  5 15 35  0  0  0  0]
     [ 1  6 21  0  0  0  0  0]
     [ 1  7  0  0  0  0  0  0]
     [ 1  0  0  0  0  0  0  0]]

The logic is that each matrix element (except for those in the first
row/column) is the sum of the element above and the element on the left.

In order to compute Pascal's triangle using :class:`PythonTask` objects, we
first need to decide on a strategy. We decide to use a :class:`PythonTask` per
matrix element. We also have to choose a strategy for naming the tasks, because
the content of the environment is indexed by the task name. So we decide to
call ``'(i, j)'`` the task that computes element `(i, j)`.

Armed with these conventions, we can write the function that computes element
`(i, j)`:

    >>> from valjean.cosette.task import TaskStatus
    >>> def compute(name, i, j, *, env):
    ...   if i == 0 or j == 0:
    ...     env_up = {name: {'result': 1}}
    ...     return env_up, TaskStatus.DONE
    ...   left = str((i-1, j))
    ...   above = str((i, j-1))
    ...   left_result = env[left]['result']
    ...   above_result = env[above]['result']
    ...   result = left_result + above_result
    ...   env_up = {name: {'result': result}}
    ...   return env_up, TaskStatus.DONE

Note that we have to return an environment update and a status.  Now we
construct the tasks and assemble them into a dependency dictionary:

    >>> deps = {}
    >>> name_to_task = {}
    >>> n = 8
    >>> for k in range(n):
    ...   # k is the index of the row in the triange
    ...   # i and j index the matrix element, so k = i + j
    ...   for i in range(k+1):
    ...     j = k - i
    ...     task_name = str((i, j))
    ...     task = PythonTask(task_name, compute, args=(task_name, i, j),
    ...                       env_kwarg='env')
    ...     name_to_task[task_name] = task
    ...     deps[task] = set()
    ...     if i > 0:
    ...       index_left = str((i-1, j))
    ...       deps[task].add(name_to_task[index_left])
    ...     if j > 0:
    ...       index_above = str((i, j-1))
    ...       deps[task].add(name_to_task[index_above])

We can then import :class:`~.DepGraph` and :class:`~.Scheduler` and execute the
dependency graph:

    >>> from valjean.cosette.depgraph import DepGraph
    >>> graph = DepGraph.from_dependency_dictionary(deps)
    >>> from valjean.cosette.scheduler import Scheduler
    >>> scheduler = Scheduler(hard_graph=graph)
    >>> final_env = scheduler.schedule()

And now we can extract the results from the final environment:

    >>> pythontask_pascal = np.zeros_like(direct_pascal)
    >>> for k in range(n):
    ...   for i in range(k+1):
    ...     j = k - i
    ...     task_name = str((i, j))
    ...     pythontask_pascal[i, j] = final_env[task_name]['result']
    >>> print(pythontask_pascal)
    [[ 1  1  1  1  1  1  1  1]
     [ 1  2  3  4  5  6  7  0]
     [ 1  3  6 10 15 21  0  0]
     [ 1  4 10 20 35  0  0  0]
     [ 1  5 15 35  0  0  0  0]
     [ 1  6 21  0  0  0  0  0]
     [ 1  7  0  0  0  0  0  0]
     [ 1  0  0  0  0  0  0  0]]
    >>> np.all(pythontask_pascal == direct_pascal)
    True

Passing arguments via the configuration
---------------------------------------

The function wrapped in a :class:`PythonTask` can also inspect the global
`valjean` configuration object. This may be useful to retrieve global settings
for paths, for instance. Like the environment, you can specify that the
configuration should be passed to the wrapped function as a keyword argument.
The keyword is specified by the `config_kwarg` parameter to the
:class:`PythonTask` constructor. For example:

    >>> from valjean.config import Config
    >>> def print_output_dir(*, config):
    ...     print(config.query('path', 'output-root'))
    >>> task = PythonTask('output-dir', print_output_dir,
    ...                   config_kwarg='config')
    >>> config = Config()
    >>> task.do(env={}, config=config)
    /.../output


Module API
----------
'''

import copy
from .task import Task, TaskStatus
from .. import LOGGER


class TaskException(Exception):
    '''An exception that can be raised by any functions wrapped in
    :class:`PythonTask`. It causes the task to fail. A reason can be specified
    in the constructor.'''

    def __init__(self, reason='unknown'):
        '''Construct a :class:`TaskException`.

        :param str reason: why this exception was raised.'''
        super().__init__()
        self.because = reason


class PythonTask(Task):
    '''Task that executes specified Python code.'''

    def __init__(self, name, func, *, args=None, kwargs=None,
                 env_kwarg=None, config_kwarg=None, deps=None, soft_deps=None):
        '''Initialize the task with a function, a tuple of arguments and a
        dictionary of kwargs.

        :param str name: The name of the task.
        :param func: A function to be executed.
        :param tuple args: A tuple of positional arguments to `func`, or `None`
                           if none are required.
        :param dict kwargs: A dictionary of keyword arguments to `func`, or
                            `None` if none are required.
        :param str env_kwarg: The name of the keyword argument that will be
                              used to pass the environment to the function, or
                              `None` if the environment should not be passed.
        :param str config_kwarg: The name of the keyword argument that will be
                                 used to pass the config to the function, or
                                 `None` if the config should not be passed.
        :param deps: If this task depends on other tasks (and valjean cannot
                     automatically discover this), pass them (as a list) to the
                     `deps` parameter.
        :type deps: None or collection of :class:`~.Task` objects.
        :param soft_deps: If this task has a soft dependency on other tasks
                          (and valjean cannot automatically discover this),
                          pass them (as a list) to the `soft_deps` parameter.
        :type soft_deps: None or collection of :class:`~.Task` objects.
        '''
        super().__init__(name=name, deps=deps, soft_deps=soft_deps)
        self.func = func
        self.args = copy.deepcopy(args) if args is not None else ()
        self.kwargs = copy.deepcopy(kwargs) if kwargs is not None else {}
        self.env_kwarg = env_kwarg
        self.config_kwarg = config_kwarg

    def do(self, env, config):
        '''Execute the function.

        :param env: The environment. It will be passed to the executed function
                    as the `env_kwarg` keyword, if specified.
        :param config: The config. It will be passed to the executed function
                       as the `config_kwarg` keyword, if specified.
        '''
        from types import MappingProxyType
        LOGGER.debug('PythonTask %r runs', self.name)
        if self.env_kwarg is not None:
            # wrap the environment in MappingProxyType, so that self.func
            # cannot modify it
            self.kwargs[self.env_kwarg] = MappingProxyType(env)
        if self.config_kwarg is not None:
            self.kwargs[self.config_kwarg] = config
        try:
            # here result is actually an (env_up, status) tuple
            result = self.func(*self.args, **self.kwargs)
        except TaskException as task_exc:
            env_up = {self.name: {'why': task_exc.because}}
            return env_up, TaskStatus.FAILED
        return result
