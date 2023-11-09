# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
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

'''This module defines a few useful functions and classes to embed generic
command execution in a :mod:`~.depgraph`.

Spawning external processes
===========================

.. doctest:: code
   :hide:

   >>> from valjean.config import Config
   >>> config = Config()

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
    >>> config = Config()
    >>> def print_stdout(env_up, name):
    ...   """A small function to print the stdout of a task."""
    ...   stdout = env_up[name]['stdout']
    ...   with open(stdout) as stdout_f:
    ...     print(stdout_f.read(), end='')

The simplest way to create a :class:`RunTaskFactory` is to use one of the
:meth:`RunTaskFactory.from_executable` or :meth:`RunTaskFactory.from_task`
class methods. For example, this will create a factory instance that generates
:class:`RunTask` objects for the :command:`echo` executable:

    >>> factory = RunTaskFactory.from_executable('echo', name='echo')

You can use it to generate tasks by invoking the :meth:`RunTaskFactory.make`
method:

    >>> task = factory.make(name='task', extra_args=['spam'])

This creates an `task.echo` object (of type :class:`RunTask`) that executes
:file:`echo spam` when run:

    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task.echo')
    spam

You can also leave the `name` parameter out. If you do so,
:class:`RunTaskFactory` will generate a name for you:

    >>> task_sausage = factory.make(extra_args=['sausage'])
    >>> task_sausage.name
    '....echo'

Of course you can generate multiple tasks using the same factory (this is the
whole point of :class:`RunTaskFactory`, really):

    >>> task_spam = factory.make(name='task_spam', extra_args=['spam'])
    >>> task_eggs = factory.make(name='task_eggs', extra_args=['eggs'])
    >>> task_bacon = factory.make(name='task_bacon', extra_args=['bacon'])

You can also specify a few arguments beforehand and provide the rest later:

    >>> factory = RunTaskFactory.from_executable('echo', name='echo',
    ...                                          default_args=['spam'])
    >>> task = factory.make(name='task', extra_args=['eggs'])
    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task.echo')
    spam eggs

Finally, you can parametrize your arguments on arbitrary keywords that will be
provided when the task is created:

    >>> args = ['{food}', 'with', '{side}']
    >>> factory = RunTaskFactory.from_executable('echo', name='echo',
    ...                                          default_args=args)
    >>> task = factory.make(name='task', food='lobster', side='spam')
    >>> env_up, status = task.do(env={}, config=config)
    >>> print_stdout(env_up, 'task.echo')
    lobster with spam

Default values for the parameters may be specified when creating the factory
and can be overridden when the task is created:

    >>> args = ['{food}', 'with', '{side}']
    >>> factory = RunTaskFactory.from_executable('echo', default_args=args,
    ...                                          side='spam', name='echo')
    >>> beans = factory.make(name='baked beans', food='baked beans')
    >>> eggs = factory.make(name='eggs', food='eggs',
    ...                     side='bacon and spam')
    >>> env_up, status = beans.do(env={}, config=config)
    >>> print_stdout(env_up, 'baked beans.echo')
    baked beans with spam
    >>> env_up, status = eggs.do(env={}, config=config)
    >>> print_stdout(env_up, 'eggs.echo')
    eggs with bacon and spam

Note also that you can refer to the environment or the configuration in your
command-line arguments:

    >>> args = ['{env[side]}']
    >>> factory = RunTaskFactory.from_executable('echo', name='echo',
    ...                                          default_args=args)
    >>> task = factory.make(name='task')
    >>> env_up, status = task.do(env={'side': 'spam'}, config=config)
    >>> print_stdout(env_up, 'task.echo')
    spam


Caching
-------

The :class:`RunTaskFactory` class caches generated tasks under the hood.
Repeated calls to :meth:`RunTaskFactory.make` from the same factory with the
same arguments will result in the same task:

    >>> factory = RunTaskFactory.from_executable('echo', name='echo')
    >>> task_sausage = factory.make(extra_args=['sausage'])
    >>> task_sausage_again = factory.make(extra_args=['sausage'])
    >>> task_sausage is task_sausage_again
    True

If you instantiate another factory, the caching mechanism is defeated:

    >>> other_factory = RunTaskFactory.from_executable('echo', name='echo')
    >>> task_sausage_other = other_factory.make(extra_args=['sausage'])
    >>> task_sausage is task_sausage_other
    False


Module API
==========
'''

import os
import shlex
from functools import partial
from subprocess import call

from .. import LOGGER
from ..chrono import Chrono
from ..path import ensure, sanitize_filename
from .task import TaskStatus, det_hash
from .pythontask import PythonTask


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
    results = []    # collect the return codes of each cli
    status = TaskStatus.DONE    # will change to FAILED in case of trouble
    with Chrono() as chrono:
        for cli in clis:
            LOGGER.debug('Running cli: %s', cli)
            print('$ ' + ' '.join(shlex.quote(token) for token in cli),
                  file=stderr, flush=True)
            LOGGER.debug('subprocess_args: %s', subprocess_args)
            result = call(cli, universal_newlines=True,
                          stdout=stdout, stderr=stderr,
                          **subprocess_args)
            LOGGER.debug('Run result: %s', result)
            results.append(result)
            if result != 0:
                LOGGER.warning('A subprocess ended with return code %s; will '
                               'skip the remaining commands', result)
                status = TaskStatus.FAILED
                break
    return results, status, float(chrono)


def make_cap_paths(base_path):
    '''Construct filenames to capture stdout and stderr.'''
    stdout_path = base_path / 'stdout'
    stderr_path = base_path / 'stderr'
    ensure(stdout_path)
    ensure(stderr_path)
    return stdout_path.resolve(), stderr_path.resolve()


class RunTask(PythonTask):
    '''Task that executes the specified shell commands and waits for their
    completion.'''

    @classmethod
    def from_cli(cls, name, cli, **kwargs):
        '''Create a :class:`RunTask` from a single command line.

        Use the :meth:`RunTask.from_clis` method if you want to run several
        commands in a row.

        :param str name: The name of this task.
        :param list cli: The command line to be executed, as a list of strings.
            The first element of the list is the command and the following ones
            are its arguments.
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
            of strings.  The first element of each sub-list is the command and
            the following ones are its arguments.
        :param kwargs: Any other keyword arguments will be passed on to the
            constructor (see :meth:`RunTask.__init__`).
        '''
        if (not isinstance(clis, (list, tuple))
                or not all(isinstance(cli, (list, tuple)) for cli in clis)):
            raise TypeError('Argument `cli` must be a list (or a tuple) '
                            'of lists (or tuples)')
        return cls(name, lambda _env, _config: clis, **kwargs)

    def __init__(self, name, clis_closure, *, deps=None, soft_deps=None,
                 **subprocess_args):
        '''Initialize this task from a list of command lines.

        The `clis_closure` argument must be a closure. It will be invoked at
        execution time as::

            clis_closure(env, config)

        and it must return the command lines to be executed, as a list of lists
        of strings.

        :param str name: The name of this task.
        :param list clis_closure: A closure to generate the command lines.
        :param dict subprocess_args: Any remaining options will be passed to
            the :class:`.subprocess.Popen` constructor.
        :param deps: The dependencies for this task (see
            :meth:`Task.__init__ <valjean.cosette.task.Task.__init__>` for the
            format), or `None`.
        :type deps: list(Task) or None
        :param soft_deps: The dependencies for this task (see
            :meth:`Task.__init__ <valjean.cosette.task.Task.__init__>` for the
            format), or `None`.
        :type soft_deps: list(Task) or None
        '''
        super().__init__(name, self.run_task(clis_closure, name,
                                             **subprocess_args),
                         deps=deps, soft_deps=soft_deps,
                         env_kwarg='env', config_kwarg='config')
        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        LOGGER.debug('  - deps = %s', deps)
        LOGGER.debug('  - soft_deps = %s', soft_deps)
        LOGGER.debug('  - subprocess_args = %s', subprocess_args)

    def run_task(self, clis_closure, name, **subprocess_args):
        # pylint: disable=unused-argument
        '''Execute the specified command and wait for its completion.

        On completion, this method proposes the following updates to the
        environment::

            env[task.name]['clis'] = clis
            env[task.name]['return_codes'] = return_codes
            env[task.name]['elapsed_time'] = wallclock_time
            env[task.name]['stdout'] = stdout
            env[task.name]['stderr'] = stderr

        Here ``clis`` is the list of command lines that were executed,
        ``return_codes`` is the list of return codes of the executed commands,
        and ``elapsed_time`` is the time the whole list took. The keys
        ``stdout`` and ``stderr`` hold the paths to the files containing
        respectively the captured standard output and standard error streams.

        :param Env env: The task environment.
        :param config: The configuration object.
        :type config: Config or None
        :returns: The proposed environment update.
        '''
        def runner(*, env, config, name, clis_closure, subprocess_args):
            # pylint: disable=too-many-locals
            '''Actually run the command lines.'''
            from pathlib import Path

            clis = clis_closure(env, config)
            output_dir = Path(config.query('path', 'output-root'),
                              sanitize_filename(name))
            stdout_path, stderr_path = make_cap_paths(output_dir)

            with stdout_path.open('w') as stdout:
                with stderr_path.open('w') as stderr:
                    results, status, elapsed = run(clis, stdout, stderr,
                                                   cwd=str(output_dir),
                                                   **subprocess_args)

            env_up = {self.name: {'clis': clis,
                                  'output_dir': str(output_dir),
                                  'return_codes': results,
                                  'elapsed_time': elapsed,
                                  'result': str(stdout_path),
                                  'stdout': str(stdout_path),
                                  'stderr': str(stderr_path)}}

            LOGGER.debug('RunTask %s ends, elapsed time: %f s', name, elapsed)
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
        # pylint: disable=too-many-arguments
        cli = [executable]
        cli.extend(arg.format(env=env, config=config, **kwargs)
                   for arg in default_args)
        cli.extend(extra_args)
        return [cli]

    @classmethod
    def from_task(cls, task, *, relative_path, name=None, default_args=None,
                  **kwargs):
        '''This class method creates a :class:`RunTaskFactory` from a
        :class:`~valjean.cosette.task.Task`. The command to be executed
        must appear in the `output_dir` directory of the given task; its
        relative location must be specified with the `relative_path` argument.

        This method can be used, among other things, to create a
        :class:`RunTaskFactory` from a
        :class:`~valjean.cosette.code.CheckoutTask` or a
        :class:`~valjean.cosette.code.BuildTask`.

        :param task: The :class:`~valjean.cosette.task.Task` object.
        :type task: :class:`~valjean.cosette.task.Task`
        :param str relative_path: The path to the executable, relative to the
            the output directory (`output_dir`) of the task.
        :param name: a unique identifier for this factory. The factory name is
            used to produce unique names for the generated tasks.  If `None` is
            given, the factory name will be constructed by hashing the other
            arguments.
        :type name: str or None
        :param default_args: see :meth:`RunTaskFactory.from_executable`.
        :param kwargs: Any remaining arguments will be passed to the
            :meth:`__init__`.
        '''
        d_args = [] if default_args is None else default_args
        LOGGER.debug('relative_path=%r', relative_path)
        LOGGER.debug('d_args=%s', d_args)
        closure = partial(cls._clis_closure_from_task, task.name,
                          relative_path, d_args)
        name = (name if name is not None
                else det_hash(task.name, relative_path, d_args))
        return cls(closure, deps=[task], name=name, **kwargs)

    @classmethod
    def _clis_closure_from_task(cls, job_name, relative_path, default_args,
                                extra_args, **kwargs):
        '''This static method generates the closure consumed by
        :meth:`RunTaskFactory.from_task`.'''
        def clis_closure(env, config):
            output_dir = env[job_name]['output_dir']
            executable = os.path.join(output_dir, relative_path)
            return cls._generic_clis_closure(executable, env=env,
                                             config=config,
                                             default_args=default_args,
                                             extra_args=extra_args,
                                             **kwargs)
        return clis_closure

    @classmethod
    def from_executable(cls, path, name=None, default_args=None, **kwargs):
        '''This class method creates a :class:`RunTaskFactory` from the path to
        an existing executable.

        :param str path: the path to the executable.
        :param name: a unique identifier for this factory. If `None` is given,
            the factory will use a hash of the other arguments.
        :type name: str or None
        :param default_args: The list of arguments that will be passed to the
            executed command by :class:`RunTask`. It may contain expressions
            understood by Python's format mini-language, such as ``{foo}``.
            These expressions can be filled when the task is generated by
            passing appropriate keyword arguments to the :meth:`make` method.
        :type default_args: list(str) or None
        :param kwargs: Any remaining arguments will be passed to the
            :meth:`__init__`.
        '''
        d_args = [] if default_args is None else default_args
        LOGGER.debug('path=%r', path)
        LOGGER.debug('d_args=%s', d_args)
        name = name if name is not None else det_hash(path, d_args)
        return cls(partial(cls._clis_closure_from_executable, path, d_args),
                   name=name, **kwargs)

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

    def __init__(self, make_closure, *, deps=None, soft_deps=None, name,
                 **kwargs):
        self.make_closure = make_closure
        self.deps = [] if deps is None else deps
        self.soft_deps = [] if soft_deps is None else soft_deps
        self.kwargs = kwargs
        self.cache = {}
        self.name = name
        LOGGER.debug('creating factory with name: %s', self.name)

    def make(self, *, name=None, extra_args=None,
             subprocess_args=None, deps=None, soft_deps=None, **kwargs):
        '''Create a :class:`RunTask` object.

        :param name: the name of the task to be generated, as a string. If
            `None` is passed, :class:`RunTaskFactory` will generate a name by
            hashing the contents of all the other arguments.
        :type name: str or None
        :param extra_args: A list of additional arguments that will be appended
            at the end of the command line.
        :type extra_args: list or None
        :param subprocess_args: A dictionary of arguments for the call to the
            :class:`.subprocess.Popen` constructor.
        :type subprocess_args: dict or None
        :param deps: A list of dependencies for the generated task. Note that
            factories built with :meth:`from_task` automatically inject
            dependencies on the given task.
        :type deps: list(Task) or None
        :param soft_deps: A list of soft dependencies for the generated task.
        :type soft_deps: list(Task) or None
        :param kwargs: Any remaining keyword arguments will be used to format
            the command line before execution. The environment and the
            configuration are available at formatting time as ``env`` and
            ``config``, respectively.
        '''
        LOGGER.debug('RunFactory.make(name=%r, extra_args=%r, '
                     'subprocess_args=%r, deps=%r, soft_deps=%r, **kwargs=%r)',
                     name, extra_args, subprocess_args, deps, soft_deps,
                     kwargs)
        extra_args = [] if extra_args is None else extra_args
        subprocess_args = {} if subprocess_args is None else subprocess_args
        deps = [] if deps is None else deps
        soft_deps = [] if soft_deps is None else soft_deps
        kwargs_ = self.kwargs.copy()
        kwargs_.update(kwargs)
        cli_closure = self.make_closure(extra_args, **kwargs_)

        # handle caching
        if name is None:
            task_name = str(det_hash(self.name, extra_args, kwargs_))
        else:
            task_name = name
        task_name += '.' + self.name
        if task_name in self.cache:
            LOGGER.debug('cache hit for task name %r', task_name)
            cached_task = self.cache[task_name]
            return cached_task

        LOGGER.debug('cache miss for task name %r', task_name)

        task = RunTask(task_name, cli_closure,
                       deps=self.deps + deps,
                       soft_deps=self.soft_deps + soft_deps,
                       **subprocess_args)
        self.cache[task_name] = task
        return task

    def copy(self):
        '''Return a copy of this object.'''
        return self.__class__(self.make_closure,
                              deps=self.deps.copy(),
                              soft_deps=self.soft_deps.copy(),
                              name=self.name, **self.kwargs)
