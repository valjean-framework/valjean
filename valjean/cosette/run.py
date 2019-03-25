'''This module defines a few useful functions and classes to embed generic
command execution in a :mod:`~.depgraph`.

Spawning external processes
===========================

.. doctest:: code
   :hide:

   >>> from valjean.config import Config
   >>> config = Config(paths=[])

The :class:`RunTask` class is the basic building block to run tasks that
consist in spawning external processes and waiting for their completion.  It
makes it possible to execute arbitrary commands. Consider:

   >>> from valjean.cosette.run import RunTask
   >>> task = RunTask.from_cli(name='say', cli=['echo', 'ni!'])
   >>> env_update, status = task.do(env=dict(), config=config) # prints 'ni!'
   >>> print(status)
   TaskStatus.DONE

The task succeeded, but where is the output of our command?! Note that
:class:`RunTask` captures standard output and standard error and redirects them
to files. If you want to see what was printed, you have to look there:

   >>> def print_stdout(env_up, name):
   ...   """A small function to print the stdout of a task."""
   ...   stdout = env_up[name]['stdout']
   ...   with open(stdout) as stdout_f:
   ...     print(stdout_f.read(), end='')
   >>> print_stdout(env_update, 'say')
   ni!

Note that `command` is not parsed by a shell. So the following may not do what
you expect:

   >>> task = RunTask.from_cli(name='want',
   ...                         cli=['echo', 'We want... ', '&&',
   ...                              'echo', 'a shrubbery!'])
   >>> env_update, status = task.do(env=dict(), config=config)
   >>> print_stdout(env_update, 'want')
   We want...  && echo a shrubbery!

Indeed, :class:`RunTask` ran :command:`echo` only once.  If you need to execute
several commands, you can wrap them in a shell script and execute it.
Alternatively, you can directly invoke the :meth:`RunTask.from_clis` class
method:

   >>> task = RunTask.from_clis(name='want',
   ...                          clis=[['echo', '-n', 'We want... '],
   ...                                ['echo', 'a shrubbery!']])
   >>> env_update, status = task.do(env=dict(), config=config)
   >>> print_stdout(env_update, 'want')
   We want... a shrubbery!


Creating tasks using a factory
==============================

When you want to create multiple :class:`RunTask` objects using the same
executable, it can be convenient to use :class:`RunTaskFactory`. This class can
be parametrized to create tasks by specifying the path to the executable once
and for all, for instance, and providing the missing arguments later.

.. doctest:: RunTaskFactory
    :hide:

    >>> import os
    >>> from valjean.config import Config
    >>> config = Config(paths=[])
    >>> def print_stdout(env_up, name):
    ...   """A small function to print the stdout of a task."""
    ...   stdout = env_up[name]['stdout']
    ...   with open(stdout) as stdout_f:
    ...     print(stdout_f.read(), end='')

The simplest way to create a :class:`RunTaskFactory` is to use one of the
:meth:`RunTaskFactory.from_executable`, :meth:`RunTaskFactory.from_checkout` or
:meth:`RunTaskFactory.from_build`, class methods. For example, this will create
a factory instance that generates :class:`RunTask` objects for the
:command:`echo` executable:

    >>> factory = RunTaskFactory.from_executable('echo')

You can use it to generate tasks by invoking the :meth:`RunTaskFactory.make`
method:

    >>> task = factory.make(name='task', extra_args=['spam'])

This creates a `task` object (of type :class:`RunTask`) that executes
:file:`echo spam` when run:

    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task')
    spam

You can also leave the `name` parameter out. If you do so,
:class:`RunTaskFactory` will generate a name for you:

    >>> task_sausage = factory.make(extra_args=['sausage'])
    >>> print(task_sausage.name)
    run#...

Of course you can generate multiple tasks using the same factory (this is the
whole point of :class:`RunTaskFactory`, really):

    >>> task_spam = factory.make(name='task_spam', extra_args=['spam'])
    >>> task_eggs = factory.make(name='task_eggs', extra_args=['eggs'])
    >>> task_bacon = factory.make(name='task_bacon', extra_args=['bacon'])

You can also specify a few arguments beforehand and provide the rest later:

    >>> factory = RunTaskFactory.from_executable('echo',
    ...                                          default_args=['spam'])
    >>> task = factory.make(name='task', extra_args=['eggs'])
    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task')
    spam eggs

Finally, you can parametrize your arguments on arbitrary keywords that will be
provided when the task is created:

    >>> args = ['{food}', 'with', '{side}']
    >>> factory = RunTaskFactory.from_executable('echo', default_args=args)
    >>> task = factory.make(name='task', food='lobster', side='spam')
    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task')
    lobster with spam

Default values for the parameters may be specified when creating the factory
and can be overridden when the task is created:

    >>> args = ['{food}', 'with', '{side}']
    >>> factory = RunTaskFactory.from_executable('echo', default_args=args,
    ...                                          side='spam')
    >>> beans = factory.make(name='baked beans', food='baked beans')
    >>> eggs = factory.make(name='eggs', food='eggs',
    ...                     side='bacon and spam')
    >>> env_up, status = beans.do(env={}, config=config)
    >>> print_stdout(env_up, 'baked beans')
    baked beans with spam
    >>> env_up, status = eggs.do(env={}, config=config)
    >>> print_stdout(env_up, 'eggs')
    eggs with bacon and spam

Note also that you can refer to the environment or the configuration in your
command-line arguments:

    >>> args = ['{env[side]}']
    >>> factory = RunTaskFactory.from_executable('echo', default_args=args)
    >>> task = factory.make(name='task')
    >>> env_up, status = task.do(env={'side': 'spam'}, config=config)
    >>> print_stdout(env_up, 'task')
    spam


Caching
-------

The :class:`RunTaskFactory` class caches generated tasks under the hood.
Repeated calls to :meth:`RunTaskFactory.make` from the same factory with the
same arguments will result in the same task:

    >>> factory = RunTaskFactory.from_executable('echo')
    >>> task_sausage = factory.make(extra_args=['sausage'])
    >>> task_sausage_again = factory.make(extra_args=['sausage'])
    >>> task_sausage is task_sausage_again
    True

If you instantiate another factory, the caching mechanism is defeated:

    >>> other_factory = RunTaskFactory.from_executable('echo')
    >>> task_sausage_other = other_factory.make(extra_args=['sausage'])
    >>> task_sausage is task_sausage_other
    False


Module API
==========
'''

import os
from functools import partial

from .. import LOGGER
from .task import TaskStatus, det_hash
from .pythontask import PythonTask


def sanitize_filename(name):
    '''Sanitize a string so that it may be used as a filename.'''
    return ''.join(c if _allowed_char(c) else '_' for c in name)


def _allowed_char(char):
    return char.isalnum() or char == '.'


# The following functions are helpers for RunTask, but they may be used
# elsewhere, too
def run(clis, stdout, stderr, **subprocess_args):
    '''Run the given command lines and capture their stdout/stderr.

    Execution stops at the first failure (result value != 0).

    :param list clis: The list of commands to execute.
    :param stdout: File handle to capture the stdout stream.
    :type stdout: :term:`file object`
    :param stderr: File handle to capture the stderr stream.
    :type stderr: :term:`file object`
    :param dict subprocess_args: Parameters to be passed to
                                 :func:`subprocess.call`.
    '''
    from subprocess import call
    from time import time

    results = []    # collect the return codes of each cli
    status = TaskStatus.DONE    # will change to FAILED in case of trouble
    start_time = time()
    for i_cli, cli in enumerate(clis):
        LOGGER.debug('Running cli: %s', cli)
        print('$ ' + ' '.join(cli), file=stderr, flush=True)
        LOGGER.debug('subprocess_args: %s', subprocess_args)
        result = call(cli, universal_newlines=True,
                      stdout=stdout, stderr=stderr,
                      **subprocess_args)
        LOGGER.debug('Run result: %s', result)
        results.append(result)
        if result != 0:
            LOGGER.warning('A subprocess ended with return code %s; will '
                           'skip the remaining %s commands',
                           result, len(clis) - i_cli - 1)
            status = TaskStatus.FAILED
            break
    end_time = time()
    elapsed = end_time - start_time
    return results, status, elapsed


def make_cap_paths(base_path):
    '''Construct filenames to capture stdout and stderr.'''
    stdout_path = base_path / 'stdout'
    stderr_path = base_path / 'stderr'
    ensure(stdout_path)
    ensure(stderr_path)
    return stdout_path.resolve(), stderr_path.resolve()


def ensure(path, *, is_dir=False):
    '''Make sure that the given path exists.

    :param pathlib.Path path: A path.
    :param bool is_dir: If `True`, the path will be constructed as a directory.
    '''
    if path.exists():
        return
    if is_dir:
        path.mkdir(parents=True)
    else:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.touch()


class RunTask(PythonTask):
    '''Task that executes the specified shell commands and waits for their
    completion.'''

    PRIORITY = 30

    @classmethod
    def from_cli(cls, name, cli, **kwargs):
        '''Create a :class:`RunTask` from a single command line.

        Use the :meth:`RunTask.from_clis` method if you want to run several
        commands in a row.

        :param str name: The name of this task.
        :param list cli: The command line to be executed, as a list of strings.
                         The first element of the list is the command and the
                         following ones are its arguments.
        :param kwargs: Any other keyword arguments will be passed on to the
                       constructor (see :meth:`RunTask.__init__`).
        '''
        if not isinstance(cli, (list, tuple)):
            raise TypeError('Argument `cli` must be a list or a tuple')
        return cls.from_clis(name, [cli], **kwargs)

    @classmethod
    def from_clis(cls, name, clis, **kwargs):
        '''Create a :class:`RunTask` from a list of command lines.

        :param str name: The name of this task.
        :param list clis: The command lines to be executed, as a list of lists
                          of strings.  The first element of each sub-list is
                          the command and the following ones are its arguments.
        :param kwargs: Any other keyword arguments will be passed on to the
                       constructor (see :meth:`RunTask.__init__`).
        '''
        if (not isinstance(clis, (list, tuple))
                or not all(isinstance(cli, (list, tuple)) for cli in clis)):
            raise TypeError('Argument `cli` must be a list (or a tuple) '
                            'of lists (or tuples)')
        return cls(name, lambda _env, _config: clis, **kwargs)

    def __init__(self, name, clis_closure, *, deps=None, **subprocess_args):
        '''Initialize this task from a list of command lines.

        The `clis_closure` argument must be a closure. It will be invoked at
        execution time as::

            clis_closure(env, config)

        and it must return the command lines to be executed, as a list of lists
        of strings.

        :param str name: The name of this task.
        :param list clis_closure: A closure to generate the command lines.
        :param dict subprocess_args: Any remaining options will be passed to
                                     the :class:`.subprocess.Popen`
                                     constructor.
        :param deps: The dependencies for this task (see
                     :meth:`Task.__init__ <valjean.cosette.task.Task.__init__>`
                     for the format), or `None`.
        :type deps: list(Task) or None
        '''
        super().__init__(name, self.run_task(clis_closure, name,
                                             **subprocess_args),
                         deps=deps, env_kwarg='env', config_kwarg='config')
        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        LOGGER.debug('  - deps = %s', deps)
        LOGGER.debug('  - subprocess_args = %s', subprocess_args)

    # pylint: disable=unused-argument
    def run_task(self, clis_closure, name, **subprocess_args):
        '''Execute the specified command and wait for its completion.

        On completion, this method proposes the following updates to the
        environment::

            env[task.name]['clis'] = clis
            env[task.name]['return_codes'] = return_codes
            env[task.name]['wallclock_time'] = wallclock_time
            env[task.name]['stdout'] = stdout
            env[task.name]['stderr'] = stderr

        Here ``clis`` is the list of command lines that were executed,
        ``return_codes`` is the list of return codes of the executed commands,
        and ``wallclock_time`` is the time the whole list took. The keys
        ``stdout`` and ``stderr`` hold the paths to the files containing
        respectively the captured standard output and standard error streams.

        :param Env env: The task environment.
        :param config: The configuration object.
        :type config: Config or None
        :returns: The proposed environment update.
        '''
        # pylint: disable=too-many-locals
        def runner(*, env, config, name, clis_closure, subprocess_args):
            '''Actually run the command lines.'''
            from pathlib import Path

            clis = clis_closure(env, config)
            run_dir = Path(config.get('path', 'run-root'),
                           sanitize_filename(name))
            stdout_path, stderr_path = make_cap_paths(run_dir)

            with stdout_path.open('w') as stdout:
                with stderr_path.open('w') as stderr:
                    results, status, elapsed = run(clis, stdout, stderr,
                                                   cwd=str(run_dir),
                                                   **subprocess_args)

            env_up = {self.name: {'clis': clis,
                                  'return_codes': results,
                                  'wallclock_time': elapsed,
                                  'stdout': str(stdout_path),
                                  'stderr': str(stderr_path)}}

            LOGGER.debug('RunTask %s ends, elapsed time: %s s', name, elapsed)
            return env_up, status

        # saturate name, clis and subprocess_args with the values from the
        # enclosing scope
        return partial(runner, name=name, clis_closure=clis_closure,
                       subprocess_args=subprocess_args)


class RunTaskFactory:
    '''Create multiple tasks from the same executable without even breaking a
    sweat.'''

    @classmethod
    def _generic_clis_closure(cls, executable, *, env, config, default_args,
                              extra_args, **kwargs):
        cli = [executable]
        cli.extend(arg.format(env=env, config=config, **kwargs)
                   for arg in default_args)
        cli.extend(extra_args)
        return [cli]

    @classmethod
    def from_checkout(cls, checkout_task, *, relative_path,
                      default_args=None, **kwargs):
        '''This class method creates a :class:`RunTaskFactory` from a
        :class:`~valjean.cosette.code.CheckoutTask`. The command to be executed
        must appear in the checkout directory; its relative location must be
        specified with the `relative_path` argument.

        :param checkout_task: The :class:`~valjean.cosette.code.CheckoutTask`
                              object.
        :type checkout_task: :class:`~valjean.cosette.code.CheckoutTask`
        :param str relative_path: The path to the executable, relative to the
                                  the checkout directory.
        :param default_args: see :meth:`RunTaskFactory.from_executable`.
        :param kwargs: Any remaining arguments will be passed to the
                       :meth:`__init__`.
        '''
        d_args = [] if default_args is None else default_args
        LOGGER.debug('relative_path=%r', relative_path)
        LOGGER.debug('d_args=%s', d_args)
        closure = partial(cls._clis_closure_from_checkout,
                          checkout_task.name, relative_path, d_args)
        uid = det_hash(checkout_task.name, relative_path, d_args)
        return cls(closure, deps=[checkout_task], uid=uid, **kwargs)

    @classmethod
    def _clis_closure_from_checkout(cls, checkout_name, relative_path,
                                    default_args, extra_args,
                                    **kwargs):
        '''This static method generates the closure consumed by
        :meth:`RunTaskFactory.from_checkout`.'''
        def clis_closure(env, config):
            checkout_dir = env[checkout_name]['checkout_dir']
            executable = os.path.join(checkout_dir, relative_path)
            return cls._generic_clis_closure(executable, env=env,
                                             config=config,
                                             default_args=default_args,
                                             extra_args=extra_args,
                                             **kwargs)
        return clis_closure

    @classmethod
    def from_build(cls, build_task, *, relative_path,
                   default_args=None, **kwargs):
        '''This class method creates a :class:`RunTaskFactory` from a
        :class:`~valjean.cosette.code.BuildTask`. The command to be executed
        must appear in the build directory; its relative location must be
        specified with the `relative_path` argument.

        :param build_task: The :class:`~valjean.cosette.code.BuildTask` object.
        :type build_task: :class:`~valjean.cosette.code.BuildTask`
        :param str relative_path: The path to the executable, relative to the
                                  the build directory.
        :param default_args: see :meth:`RunTaskFactory.from_executable`.
        :param kwargs: Any remaining arguments will be passed to the
                       :meth:`__init__`.
        '''
        d_args = [] if default_args is None else default_args
        LOGGER.debug('relative_path=%r', relative_path)
        LOGGER.debug('d_args=%s', d_args)
        closure = partial(cls._clis_closure_from_build,
                          build_task.name, relative_path, d_args)
        uid = det_hash(build_task.name, relative_path, d_args)
        return cls(closure, deps=[build_task], uid=uid, **kwargs)

    @classmethod
    def _clis_closure_from_build(cls, build_name, relative_path,
                                 default_args, extra_args,
                                 **kwargs):
        '''This static method generates the closure consumed by
        :meth:`RunTaskFactory.from_build`.'''
        def clis_closure(env, config):
            build_dir = env[build_name]['build_dir']
            executable = os.path.join(build_dir, relative_path)
            return cls._generic_clis_closure(executable, env=env,
                                             config=config,
                                             default_args=default_args,
                                             extra_args=extra_args,
                                             **kwargs)
        return clis_closure

    @classmethod
    def from_executable(cls, path, default_args=None, **kwargs):
        '''This class method creates a :class:`RunTaskFactory` from the path to
        an existing executable.

        :param default_args: The list of arguments that will be passed to the
                             executed command by :class:`RunTask`. It may
                             contain expressions understood by Python's format
                             mini-language, such as ``{foo}``. These
                             expressions can be filled when the task is
                             generated by passing appropriate keyword arguments
                             to the :meth:`make` method.
        :type default_args: list(str) or None
        :param kwargs: Any remaining arguments will be passed to the
                       :meth:`__init__`.
        '''
        d_args = [] if default_args is None else default_args
        LOGGER.debug('path=%r', path)
        LOGGER.debug('d_args=%s', d_args)
        uid = det_hash(path, d_args)
        return cls(partial(cls._clis_closure_from_executable, path, d_args),
                   uid=uid, **kwargs)

    @classmethod
    def _clis_closure_from_executable(cls, executable, default_args,
                                      extra_args, **kwargs):
        def clis_closure(env, config):
            return cls._generic_clis_closure(executable, env=env,
                                             config=config,
                                             default_args=default_args,
                                             extra_args=extra_args,
                                             **kwargs)
        return clis_closure

    def __init__(self, make_closure, *, deps=None, uid, **kwargs):
        self.make_closure = make_closure
        self.deps = [] if deps is None else deps
        self.kwargs = kwargs
        self.cache = {}
        self.uid = uid
        LOGGER.debug('creating factory with UID: %s', self.uid)

    def make(self, *, name=None, extra_args=None,
             subprocess_args=None, deps=None, **kwargs):
        '''Create a :class:`RunTask` object.

        :param name: the name of the task to be generated, as a string. If
                     `None` is passed, :class:`RunTaskFactory` will generate a
                     name by hashing the contents of all the other arguments.
        :type name: str or None
        :param extra_args: A list of additional arguments that will be
                           appended at the end of the command line.
        :type extra_args: list or None
        :param subprocess_args: A dictionary of arguments for the call to
                                the :class:`.subprocess.Popen` constructor.
        :type subprocess_args: dict or None
        :param deps: A list of dependencies for the generated task. Note that
                     factories built with :meth:`from_checkout` and
                     :meth:`from_build` automatically inject dependencies on
                     the checkout and build tasks, respectively.
        :type deps: list(Task) or None
        :param kwargs: Any remaining keyword arguments will be used to format
                       the command line before execution. The environment and
                       the configuration are available at formatting time as
                       ``env`` and ``config``, respectively.
        '''
        e_args = [] if extra_args is None else extra_args
        sp_args = {} if subprocess_args is None else subprocess_args
        deps_ = [] if deps is None else deps
        kwargs_ = self.kwargs.copy()
        kwargs_.update(kwargs)
        cli_closure = self.make_closure(e_args, **kwargs_)

        # handle caching
        uid = det_hash(self.uid, e_args, kwargs_)
        if uid in self.cache:
            LOGGER.debug('cache hit for uid %s', uid)
            cached_task = self.cache[uid]
            if name is not None and cached_task.name != name:
                LOGGER.warning('task %r has already been cached under a '
                               'different name (%r)', name, cached_task.name)
            return cached_task

        LOGGER.debug('cache miss for uid %s', uid)
        name = name if name is not None else 'run#' + str(uid)

        task = RunTask(name, cli_closure, deps=self.deps + deps_, **sp_args)
        self.cache[uid] = task
        return task

    def copy(self):
        '''Return a copy of this object.'''
        return self.__class__(self.make_closure, deps=self.deps.copy(),
                              uid=self.uid, **self.kwargs)
