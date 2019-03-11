r'''This module provides a decorator that simplifies the integration of free
Python functions in the :mod:`valjean` dependency graph.


An example
==========

Let us consider the following simple function, that counts the number of
characters in a file:

    >>> def how_many_chars(filename):
    ...     return len(open(filename).read())

Suppose that we have a task that produces some text and we want to count the
number of characters in the output. For this example, we will take the task to
be:

    >>> from valjean.cosette.run import RunTask
    >>> cmd = ['echo', 'spam']
    >>> run_task = RunTask.from_cli('run_task', cmd)

This task will produce exactly five characters of standard output [#]_, but
assume we want to check this with our `how_many_chars` function. If the task is
part of a dependency graph, we cannot call `how_many_chars` until the task has
been executed, simply because its output (which is the input to
`how_many_chars`) does not exist until then.

The solution is to bridge the gap using an :class:`Use` object:

    >>> from valjean.cosette.use import Use
    >>> use_arg_echo = Use(func=how_many_chars, task=run_task, key='stdout')

:class:`Use` lifts the naked function `how_many_chars` into the world of
:mod:`valjean` dependency graphs. The `how_many_chars` function is wrapped in a
:class:`~.PythonTask` that can be retrieved with the :meth:`~.get_task`
method:

    >>> how_many_task = use_arg_echo.get_task()
    >>> from valjean.cosette.pythontask import PythonTask
    >>> isinstance(how_many_task, PythonTask)
    True

The `how_many_task` object is wired in such a way that it will retrieve the
value to its argument from the ``'stdout'`` key of `run_task`'s environment
section on execution. If `run_task` has not been executed at that point or it
has failed, then of course `how_many_task` will fail, too.  The dependency of
`how_many_task` on `run_task` is made explicit:

    >>> run_task in how_many_task.depends_on
    True

This allows :mod:`valjean` to seamlessly integrate the execution of
`how_many_task` in the dependency graph.  We can illustrate the relations
between the objects that we have created with the following diagram:

.. digraph:: depgraph
    :align: center

    compound=true;
    subgraph cluster_use {
        label="use_arg_echo: Use";
        func [label="how_many_chars: func" shape=diamond];
    }
    run_task [label="run_task: Task"];
    how_many_task [label="how_many_task: Task"]
    { rank=same run_task how_many_task }
    func -> how_many_task [label=" generates" style=dotted ltail=cluster_use];
    how_many_task -> run_task [label="depends on"];

Here we see that `use_arg_echo` has type :class:`Use` and contains the
`how_many_chars` function. Additionally, it generates `how_many_task`, which is
a :class:`~.Task` object that depends on `run_task`.


.. doctest:: cosette_use
    :hide:

    >>> from valjean.config import Config
    >>> config = Config(paths=[])

We can test that `how_many_task` works by manually executing `run_task` first
and passing the resulting environment to `how_many_task`:

    >>> from valjean.cosette.env import Env
    >>> env, status = run_task.do(env=Env(), config=config)
    >>> print(status)
    TaskStatus.DONE

Note that the environment now contains the name of the file written by
`run_task` in the ``'stdout'`` key:

    >>> env[run_task.name]['stdout']
    '/.../run_task/stdout'

We can now execute `how_many_task`:

    >>> env_up, status = how_many_task.do(env=env, config=config)
    >>> print(status)
    TaskStatus.DONE

The ``'result'`` key now holds the return value of `how_many_chars`:

    >>> env_up[how_many_task.name]['result']
    5


:class:`Use` objects are wrappers
---------------------------------

:class:`Use` also behaves as a wrapper of `how_many_chars`.  You can still call
the underlying wrapped function with explicit parameters if you wish:

    >>> with open('test.txt', 'w') as f:
    ...     _ = f.write('lobster Thermidor\n')
    >>> use_arg_echo('test.txt')
    18
    >>> len('lobster Thermidor\n')
    18

This simplifies testing.


Argument injection via the :func:`using` decorator
--------------------------------------------------

A practical way to create :class:`Use` objects is to call the :func:`using`
decorator:

    >>> @using(task=run_task, key='stdout')
    ... def how_many_chars(filename):
    ...     return len(open(filename).read())

Now `how_many_chars` is itself a :class:`Use` object:

    >>> isinstance(how_many_chars, Use)
    True

This is exactly equivalent to what we did earlier, except for the fact that the
:class:`Use` object now does not have a different name:

.. digraph:: depgraph
    :align: center

    compound=true;
    subgraph cluster_use {
        label="how_many_chars: Use";
        fontcolor=red;
        func [label="how_many_chars: func" shape=diamond];
    }
    run_task [label="run_task: Task"];
    how_many_task [label="how_many_task: Task"]
    { rank=same run_task how_many_task }
    func -> how_many_task [label=" generates" style=dotted ltail=cluster_use];
    how_many_task -> run_task [label="depends on"];

You can still call the underlying `how_many_chars` by calling the :class:`Use`
object as if it were a normal function, as discussed above. Just like before,
we can generate a task from the :class:`Use` object:

    >>> how_many_task = how_many_chars.get_task()
    >>> isinstance(how_many_task, PythonTask)
    True


Injecting multiple arguments
----------------------------

If your function expects multiple arguments to be fed from previous tasks,
you can stack multiple :class:`Use` decorators:

    >>> name_task = RunTask.from_cli('name_task', ['echo', 'Arthur'])
    >>> job_task = RunTask.from_cli('job_task',
    ...                             ['echo', 'King of the Britons'])
    >>> @using(task=name_task, key='stdout')
    ... @using(task=job_task, key='stdout')
    ... def introduce(name_filename, job_filename):
    ...     with open(name_filename) as name_file:
    ...         name = name_file.read().rstrip()
    ...     with open(job_filename) as job_file:
    ...         job = job_file.read().rstrip()
    ...     return 'I am ' + name + ', ' + job + '!'

The resulting task has the correct dependencies, i.e. it depends on both
`name_task` and `job_task`:

    >>> intro_task = introduce.get_task()
    >>> name_task in intro_task.depends_on
    True
    >>> job_task in intro_task.depends_on
    True

We can represent the dependency structure of the generated tasks with the
following graph:

.. digraph:: depgraph
    :align: center

    compound=true;
    subgraph cluster_intro {
      label="introduce: Use";
      introduce [label="introduce: func" shape=diamond];
    }
    name [label="name_task: Task"];
    job [label="job_task: Task"];
    "intro_task: Task" -> name [label="depends on"];
    "intro_task: Task" -> job [label="depends on"];
    introduce -> "intro_task: Task"
      [label=" generates" style=dotted ltail=cluster_intro];


If we manually execute `name_task` and `job_task`, we can then execute
`intro_task`:

    >>> env = Env()
    >>> for task in [name_task, job_task, intro_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[intro_task.name]['result'])
    I am Arthur, King of the Britons!

Keyword arguments
-----------------

In the previous example, note that the order of the decorators is important!
The outer decorator (`name_task`) injects the first argument (`name_filename`),
and the inner one (`job_task`) injects the second argument (`job_filename`). If
we nest the decorators the other way around, we inverse the order of the
arguments:

    >>> @using(task=job_task, key='stdout')
    ... @using(task=name_task, key='stdout')
    ... def introduce_inv(name_filename, job_filename):
    ...     with open(name_filename) as name_file:
    ...         name = name_file.read().rstrip()
    ...     with open(job_filename) as job_file:
    ...         job = job_file.read().rstrip()
    ...     return 'I am ' + name + ', ' + job + '!'
    >>> intro_inv_task = introduce_inv.get_task()
    >>> for task in [name_task, job_task, intro_inv_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[intro_inv_task.name]['result'])
    I am King of the Britons, Arthur!

If you are injecting many arguments, it may be a good idea to use the `kwarg`
argument to :func:`using`, which allows you to inject values into arguments by
name instead of by position:

    >>> @using(kwarg='name_filename', task=name_task, key='stdout')
    ... @using(kwarg='job_filename', task=job_task, key='stdout')
    ... def introduce_kwargs(name_filename, job_filename):
    ...     return introduce(name_filename, job_filename)
    >>> @using(kwarg='job_filename', task=job_task, key='stdout')
    ... @using(kwarg='name_filename', task=name_task, key='stdout')
    ... def introduce_kwargs_swap(name_filename, job_filename):
    ...     return introduce(name_filename, job_filename)

Note that the `introduce_kwargs` and `introduce_kwargs_swap` functions are
identical, but the `@using` decorators appear in reverse order. In the previous
example, this mattered and we ended up with ``I am King of the Britons,
Arthur!``. But since now we are using the `kwarg` argument, the order of the
decorators does not matter any more.  Both `introduce_kwargs` and
`introduce_kwargs_swap` will inject the arguments as expected:

    >>> intro_kwargs_task = introduce_kwargs.get_task()
    >>> intro_kwargs_swap_task = introduce_kwargs_swap.get_task()
    >>> env_up, _ = intro_kwargs_task.do(env=env, config=config)
    >>> print(env_up[intro_kwargs_task.name]['result'])
    I am Arthur, King of the Britons!
    >>> env_up, _ = intro_kwargs_swap_task.do(env=env, config=config)
    >>> print(env_up[intro_kwargs_swap_task.name]['result'])
    I am Arthur, King of the Britons!


Modifying an existing :class:`Use` decorator
--------------------------------------------

You can pipe the result of the task generated by a :class:`Use` decorator by
using the :meth:`Use.map` method:

    >>> intro_stars = introduce.map(lambda x: '★★★' + x + '★★★')

Here `intro_stars` is a new :class:`Use` object that will apply the specified
function (here, a lambda that surrounds its argument with ★★★cute little
stars★★★) to the result of `intro_task` (see above). The task associated to
`intro_stars` depends on `intro_task`:

    >>> intro_stars_task = intro_stars.get_task()
    >>> intro_task in intro_stars_task.depends_on
    True

In our schematic representation, `intro_stars` and `intro_stars_task` would
appear like this:

.. digraph:: depgraph
    :align: center

    compound=true;
    subgraph cluster_intro {
        label="introduce: Use";
        introduce [label="introduce: func" shape=diamond];
    }
    name [label="name_task: Task"];
    job [label="job_task: Task"];
    intro_task [label="intro_task: Task"];
    intro_task -> name [label="depends on"];
    intro_task -> job [label="depends on"];
    introduce -> intro_task
      [label=" generates" style=dotted ltail=cluster_intro];

    subgraph cluster_stars {
        label="intro_stars: Use";
        color=red;
        fontcolor=red;
        stars [label=": <lambda>" shape=diamond color=red fontcolor=red];
    }
    intro_stars_task
      [label="intro_stars_task: Task" color=red fontcolor=red];
    stars -> intro_stars_task
      [label=" generates" style=dotted ltail=cluster_stars];
    intro_stars_task -> intro_task [label="depends on"];

    { rank=same intro_task intro_stars_task }


If we execute `intro_stars_task`, we find that our string now has stars!

    >>> env_up, _ = intro_stars_task.do(env=env, config=config)
    >>> env.apply(env_up)
    >>> print(env[intro_stars_task.name]['result'])
    ★★★I am Arthur, King of the Britons!★★★


.. rubric:: Footnotes

.. [#] The proof is left to the reader as an exercise.


Injecting arguments into tasks created by a :class:`~.RunTaskFactory`
=====================================================================

There is a typical use case for :class:`Use` which consists in injecting the
result of a :class:`~.RunTask` generated by a :class:`~.RunTaskFactory` as an
argument to a subsequent task `B`. Since this use case is common, there is a
special :class:`UseRun` class that helps reducing the boilerplate.

First, we create a :class:`~.RunTaskFactory` object:

    >>> from valjean.cosette.run import RunTaskFactory
    >>> factory = RunTaskFactory.from_executable('echo')

Instead of creating :class:`~.RunTask` objects and wrapping them in
:class:`Use` by hand, we instantiate a :class:`UseRun` object:

    >>> using_run = UseRun.from_factory(factory)

The :class:`UseRun` object will create the :class:`~.RunTask` objects on the
fly, when invoked as a decorator:

    >>> @using_run(extra_args=['spam'])
    ... def read_and_check_text(filename):
    ...     with open(filename) as f:
    ...         return f.read() == 'spam\n'

The decorated function is simply an instance of the :class:`Use` class that we
all know and love:

    >>> isinstance(read_and_check_text, Use)
    True

so we can call :meth:`Use.get_task` to generate a task:

    >>> read_and_check_task = read_and_check_text.get_task()
    >>> run_task = read_and_check_task.depends_on.pop()

Since a picture is worth a thousand words, the objects have the following
structure:

.. digraph:: depgraph
    :align: center

    compound=true;
    using_run [label="using_run: UseRun" shape=box];
    subgraph cluster_read {
        label="read_and_check_text: Use";
        read [label="read_and_check_text: func" shape=diamond];
        factory [label="factory: RunTaskFactory"];
    }
    using_run -> read [label=" generates" lhead=cluster_read style=dotted];
    factory -> run_task [label="generates" style=dotted];
    read_task [label="read_and_check_task: Task"];
    run_task [label="run_task: Task"];
    read_task -> run_task [label="depends on"];
    read -> read_task [label=" generates" style=dotted ltail=cluster_read];
    { rank=same read_task run_task }

Let's check that our tasks work as expected:

    >>> env, _ = run_task.do(env=Env(), config=config)
    >>> env, _ = read_and_check_task.do(env=env, config=config)
    >>> print(env[read_and_check_task.name]['result'])
    True


Pipelines
---------

This is already nice! However, if you often want to perform the same additional
actions after creating your :class:`~.RunTask`, you can cut the boilerplate
further with the :meth:`UseRun.map` method. In our example, we might want to
factorize out the ``with open(filename) as f`` bit and focus in the text
comparison:

    >>> def slurp(filename):
    ...     with open(filename) as f:
    ...         return f.read()
    >>> using_run_as_text = using_run.map(slurp)

The  :meth:`UseRun.map` method creates a new :class:`UseRun` object which will
enqueue the specified function (as a task) to be executed on the result of the
:class:`~.RunTask`. We can simplify `read_and_check_text` from above as
follows:

    >>> @using_run_as_text(extra_args=['spam'])
    ... def check_text(text):
    ...     return text == 'spam\n'

The diagram now looks like this:

.. digraph:: depgraph
    :align: center

    compound=true;
    using_run [label="using_run: UseRun" shape=box];
    using_run_as_text [label="using_run_as_text: UseRun" shape=box];
    using_run -> using_run_as_text [label=" map(slurp)" style=dotted];
    subgraph cluster_check {
        label="check_text: Use";
        slurp [label="slurp: func" shape=diamond];
        check [label="check_text: func" shape=diamond];
        factory [label="factory: RunTaskFactory"];
        { rank=same slurp check }
    }
    using_run_as_text -> slurp
      [label=" generates" lhead=cluster_check style=dotted];
    factory -> run_task [label=" generates" style=dotted];
    check_task [label="check_task: Task"];
    slurp_task [label="slurp_task: Task"];
    run_task [label="run_task: Task"];
    check_task -> slurp_task [label="depends on"];
    slurp_task -> run_task [label="depends on"];
    slurp -> slurp_task [label=" generates" style=dotted ltail=cluster_check];
    check -> check_task [label=" generates" style=dotted ltail=cluster_check];
    { rank=same slurp_task check_task run_task }

Checking that this works is a bit more laborious, because we now have one extra
task to run; in the real world, of course, :mod:`valjean` would take care of
running the tasks via a dependency graph and we wouldn't need to worry about
any of this:

    >>> check_task = check_text.get_task()
    >>> slurp_task = check_task.depends_on.pop()
    >>> run_task = slurp_task.depends_on.pop()
    >>> env = Env()
    >>> for task in [run_task, slurp_task, check_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[check_task.name]['result'])
    True

You can also chain :meth:`UseRun.map` calls:

    >>> using_run_as_stripped_text = using_run.map(slurp) \
    ...                                       .map(lambda x: x.strip())
    >>> @using_run_as_stripped_text(extra_args=['spam'])
    ... def check_stripped_text(text):
    ...     return text == 'spam'  # note that the \n is gone

Proof that it works:

    >>> check_stripped_task = check_stripped_text.get_task()
    >>> strip_task = check_stripped_task.depends_on.pop()
    >>> slurp_task = strip_task.depends_on.pop()
    >>> run_task = slurp_task.depends_on.pop()
    >>> env = Env()
    >>> for task in [run_task, slurp_task, strip_task, check_stripped_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[check_stripped_task.name]['result'])
    True

and a final diagram to show the dependencies among the objects:

.. digraph:: depgraph
    :align: center

    compound=true;
    using_run [label="using_run: UseRun" shape=box];
    using_run_anonymous
      [label="<anonymous>: UseRun" shape=box];
    using_run_as_stripped_text
      [label="using_run_as_stripped_text: UseRun" shape=box];
    using_run -> using_run_anonymous [label=" map(slurp)" style=dotted];
    using_run_anonymous -> using_run_as_stripped_text
      [label=" map(strip)" style=dotted];
    subgraph cluster_check_stripped {
        label="check_stripped_text: Use";
        slurp [label="slurp: func" shape=diamond];
        strip [label="strip: func" shape=diamond];
        check_stripped [label="check_stripped_text: func" shape=diamond];
        factory [label="factory: RunTaskFactory"];
        { rank=same slurp check_stripped strip }
    }
    using_run_as_stripped_text -> slurp
      [label=" generates" lhead=cluster_check_stripped style=dotted];
    factory -> run_task [label=" generates" style=dotted];
    check_stripped_task [label="check_stripped_task: Task"];
    strip_task [label="strip_task: Task"];
    slurp_task [label="slurp_task: Task"];
    run_task [label="run_task: Task"];
    check_stripped_task -> strip_task [label="depends on"];
    strip_task -> slurp_task [label="depends on"];
    slurp_task -> run_task [label="depends on"];
    strip -> strip_task
      [label=" generates" style=dotted ltail=cluster_check_stripped];
    slurp -> slurp_task
      [label=" generates" style=dotted ltail=cluster_check_stripped];
    check_stripped -> check_stripped_task
      [label=" generates" style=dotted ltail=cluster_check_stripped];
    { rank=same slurp_task check_stripped_task run_task strip_task }


Module API
==========
'''

from uuid import uuid4
from functools import update_wrapper

from .task import TaskStatus
from .pythontask import PythonTask
from .. import LOGGER


def from_env(*, env, task_name, key):
    '''Helper function to extract a value from the environment for argument
    injection.

    :param env: the environment.
    :type env: :class:`~.Env`
    :param str task_name: the name of the task to look up.
    :param str key: the key to look up.
    :raises KeyError: if the required task_name or key are not available.
    '''
    try:
        task_env = env[task_name]
    except KeyError:
        LOGGER.error('Task %r is required for argument injection, but the '
                     'task is not in the environment', task_name)
        raise
    try:
        task_result = task_env[key]
    except KeyError:
        LOGGER.error('Task %r is required for argument injection, but I '
                     'could not find the %r key in the result environment',
                     task_name, key)
        raise
    return task_result


class Use:
    '''A function wrapper around a free Python function. Lifts the function
    into a :mod:`~.valjean` :class:`~.Task`.'''

    def __init__(self, *, func, task, key='result', kwarg=None):
        '''Create a :class:`Use` from a function.

        :param func: a function or a callable object.
        :param task: the task whose result should be injected as an argument to
                     `func`.
        :type task: :class:`~.Task`
        :param str key: the name of the key that contains the task result in
                        the environment.
        :param kwarg: the name of the keyword argument to `func` that must be
                      fed with the `task` result. If None, the result of `task`
                      will be passed as a positional argument.
        :type kwarg: None or str
        '''
        if isinstance(func, self.__class__):
            # when we decorate another Use object, we just extend the decorated
            # object's inj_args list and inj_kwargs dictionary
            LOGGER.debug('decorating a "%s" object', self.__class__.__name__)
            self.inj_args = func.inj_args.copy()
            self.inj_kwargs = func.inj_kwargs.copy()
            self.func_name = func.func_name
        else:
            LOGGER.debug('decorating a free function')
            self.inj_args = []
            self.inj_kwargs = {}
            self.func_name = (func.__qualname__ if func.__name__ is None
                              else func.__name__)
            update_wrapper(self, func)
        if kwarg is None:
            self.inj_args.append((task, key))
        else:
            self.inj_kwargs[kwarg] = (task, key)
        self.wrapped = func
        self.pytask = None
        LOGGER.debug('inj_args = %s', self.inj_args)
        LOGGER.debug('inj_kwargs = %s', self.inj_kwargs)

    def _make_task(self):
        from itertools import chain

        pytask_name = self.func_name + '-' + str(uuid4())

        LOGGER.debug('creating %s task', pytask_name)
        LOGGER.debug('  args: %s', self.inj_args)
        LOGGER.debug('  kwargs: %s', self.inj_kwargs)

        deps = set(value[0] for value in chain(self.inj_kwargs.values(),
                                               self.inj_args))
        LOGGER.debug('%s task will depend on %s', pytask_name, deps)

        def inject_from_env(env):
            # Prepare the args for the function; we loop over self.inj_args in
            # reverse because stacked decorators are invoked from the inside
            # out. If we do not reverse the list, the outermost decorator will
            # provide the last positional argument.
            args = []
            for task, key in reversed(self.inj_args):
                task_result = from_env(env=env, task_name=task.name, key=key)
                args.append(task_result)

            # prepare the kwargs for the function
            kwargs = {}
            for kwarg, (task, key) in self.inj_kwargs.items():
                task_result = from_env(env=env, task_name=task.name, key=key)
                kwargs[kwarg] = task_result

            LOGGER.debug('injecting args: %s', args)
            LOGGER.debug('injecting kwargs: %s', kwargs)

            result = self.wrapped(*args, **kwargs)
            env_up = {pytask_name: {'result': result}}
            return env_up, TaskStatus.DONE

        return PythonTask(pytask_name, inject_from_env, deps=deps,
                          env_kwarg='env')

    def __call__(self, *args, **kwargs):
        '''Redirect the call to the wrapped function.'''
        return self.wrapped(*args, **kwargs)

    def get_task(self):
        '''Return the task representing this decorated function.'''
        if self.pytask is None:
            self.pytask = self._make_task()
        return self.pytask

    def map(self, func):
        '''Create a new :class:`Use` object that applies `func` to the result
        of the task defined by `self`.'''
        return Use(func=func, task=self.get_task())


def using(*, key='result', task, kwarg=None):
    '''Make it possible to instantiate :class:`Use` as a decorator.

    See :meth:`Use.__init__` for a description of the parameters.
    '''
    def decorator(wrapped):
        return Use(task=task, key=key, kwarg=kwarg, func=wrapped)
    return decorator


class UseRun:
    '''Produce :class:`Use` decorators from a :class:`~.RunTaskFactory`.'''

    @classmethod
    def from_factory(cls, factory):
        '''Create a :class:`UseRun` from a :class:`~.RunTaskFactory`.

        Given a :class:`~.RunTaskFactory`, the :class:`UseRun` class can be
        used to construct :class:`~.RunTask` objects on demand and inject their
        results into the decorated function.

        :param RunTaskFactory factory: a :class:`~.RunTaskFactory` object.
        '''
        return cls(factory, [])

    def __init__(self, factory, posts):
        '''Instantiate a :class:`UseRun` object.

        Given a :class:`~.RunTaskFactory`, the :class:`UseRun` class can be
        used to construct :class:`~.RunTask` objects on demand and inject their
        results into the decorated function.

        The `posts` parameters is a list of functions that will be sequentially
        applied to the result of the generated :class:`~.RunTask`. Each
        function becomes a new :class:`~.PythonTask` object depending on the
        result of the previous one.

        :param RunTaskFactory factory: a :class:`~.RunTaskFactory` object.
        :param posts: a collection of post-processing functions. Each function
                      will be converted to a :class:`~.PythonTask` object.
        '''
        self.factory = factory
        self.posts = posts

    def __call__(self, kwarg=None, **kwargs):
        uname = str(uuid4())
        task = self.factory.make(name='run_' + uname, **kwargs)
        key = 'stdout'
        for post in self.posts:
            use = Use(task=task, key=key, func=post)
            task = use.get_task()
            key = 'result'
        return using(kwarg=kwarg, task=task, key=key)

    def copy(self):
        '''Return a copy of this object.'''
        return UseRun(self.factory.copy(), self.posts.copy())

    def map(self, func):
        '''Create a new instance of :class:`UseRun` by extending the list of
        post-processing functions with a new one.

        :param func: a function with one argument to be applied to the result
                     of `self`.
        '''
        copy = self.copy()
        copy.posts.append(func)
        return copy
