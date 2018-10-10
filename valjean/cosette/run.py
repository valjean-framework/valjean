'''This module defines a few useful functions and classes to embed generic
command execution in a :mod:`~.DepGraph`.

Spawning external processes
---------------------------

.. doctest:: code
   :hide:

   >>> import os
   >>> from valjean.config import Config
   >>> run_dir = 'run_dir'
   >>> os.mkdir(run_dir)
   >>> config = Config(paths=[])
   >>> config.set('path', 'run-root', run_dir)

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

Indeed, :class:`RunTask` ran :prog:`echo` only once.  If you need to execute
several commands, you can wrap them in a shell script and execute it.
Alternatively, you can directly invoke the :class:`RunTask` constructor:

   >>> task = RunTask(name='want', clis=[['echo', '-n', 'We want... '],
   ...                                   ['echo', 'a shrubbery!']])
   >>> env_update, status = task.do(env=dict(), config=config)
   >>> print_stdout(env_update, 'want')
   We want... a shrubbery!
'''

from .. import LOGGER
from .task import Task, TaskStatus


def sanitize_filename(name):
    '''Sanitize a string so that it may be used as a filename.'''
    return ''.join(c if _allowed_char(c) else '_' for c in name)


def _allowed_char(char):
    return char.isalnum() or char == '.'


# The following functions are helpers for RunTask, but they may be used
# elsewhere, too
def format_cli(cli, env, config):
    '''Format a command line using values from the environment and the
    configuration.

    :param Env env: The environment.
    :param Config config: The configuration.
    '''

    try:
        formatted_cli = [c.format(config=config, env=env)
                         for c in cli]
    except KeyError as err:
        key = err.args[0]
        LOGGER.exception('missing key %r when formatting CLI:\n%s'
                         '\nenv:\n%s'
                         '\nconfig:\n%s',
                         key, cli, env, config)
        raise
    LOGGER.debug('  - formatted cli = %s', formatted_cli)
    return formatted_cli


def format_clis(clis, env, config):
    '''Format several command lines using values from the environment and
    the configuration.

    :param Env env: The environment.
    :param Config config: The configuration.
    '''
    formatted_clis = [format_cli(cli, env, config) for cli in clis]
    return formatted_clis


def run(clis, stdout, stderr, **subprocess_args):
    '''Run the given command lines and capture their stdout/stderr.

    Execution stops at the first failure (result value != 0).

    :param list clis: The list of commands to execute.
    :param file stdout: File handle to capture the stdout stream.
    :param file stderr: File handle to capture the stderr stream.
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
    '''Construct filenames to capture stdout and stderr of this task.'''
    stdout_path = base_path / 'stdout'
    stderr_path = base_path / 'stderr'
    ensure(stdout_path)
    ensure(stderr_path)
    return stdout_path.resolve(), stderr_path.resolve()


def ensure(path, *, is_dir=False):
    '''Make sure that the given path exists.

    :param pathlib.path path: A path.
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


class RunTask(Task):
    '''Task that executes the specified shell command and waits for its
    completion.

    The command line is passed in as a list of strings. It may contain Python
    format strings of the form ``'{spam}'``. When the :meth:`do()` method is
    called, the command line is formatted using the keyword-value pairs that
    were passed to the constructor. Additionally, the special `config`
    parameter will also be passed to the :func:`format()` call and will contain
    the global current :class:`~.Config` object.
    '''

    PRIORITY = 30

    @classmethod
    def from_cli(cls, name, cli, **kwargs):
        '''Create a :class:`RunTask` from a single command line.

        Use the :meth:`RunTask.__init__` method if you want to run several
        commands in a row.

        :param str name: The name of this task.
        :param list cli: The command line to be executed, as a list of strings.
                         The first element of the list is the command and the
                         following ones are its arguments.
        :param kwargs: Any other keyword arguments will be passed on to the
                       constructor (see :meth:`RunTask.__init__`).
        '''
        assert isinstance(cli, list)
        return cls(name, [cli], **kwargs)

    def __init__(self, name, clis, *, deps=None, **subprocess_args):
        '''Initialize this task from a list of command lines.

        :param str name: The name of this task.
        :param list clis: The command lines to be executed, as a list of lists
                          of strings.  The first element of each sub-list is
                          the command and the following ones are its arguments.
        :param dict subprocess_args: Any remaining options will be passed to
                                     the :class:`.subprocess.Popen`
                                     constructor.
        :param deps: The dependencies for this task (see
                     :meth:`Task.__init__()` for the format), or `None`.
        :type deps: list of Task or None
        '''
        super().__init__(name, deps=deps)
        self.clis = clis
        self.subprocess_args = subprocess_args
        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        LOGGER.debug('  - clis = %s', self.clis)
        LOGGER.debug('  - subprocess_args = %s', self.subprocess_args)

    def do(self, env, config):
        '''Execute the specified command and wait for its completion.

        On completion, this method proposes the following updates to the
        environment::

            env[task.name]['return_codes'] = return_codes
            env[task.name]['wallclock_time'] = wallclock_time
            env[task.name]['stdout'] = stdout
            env[task.name]['stderr'] = stderr

        Here ``return_codes`` is the list of return codes of the executed
        commands, and ``wallclock_time`` is the time they took. The keys
        ``stdout`` and ``stderr`` hold the paths to the files containing
        respectively the captured standard output and standard error streams.

        :param Env env: The task environment.
        :param config: The configuration object.
        :type config: Config or None
        :returns: The proposed environment update.
        '''
        from pathlib import Path

        formatted_clis = format_clis(self.clis, env, config)
        run_dir = Path(config.get('path', 'run-root'),
                       sanitize_filename(self.name))
        stdout_path, stderr_path = make_cap_paths(run_dir)

        with stdout_path.open('w') as stdout:
            with stderr_path.open('w') as stderr:
                results, status, elapsed = run(formatted_clis, stdout, stderr,
                                               cwd=str(run_dir),
                                               **self.subprocess_args)

        env_up = {self.name: {'return_codes': results,
                              'wallclock_time': elapsed,
                              'stdout': str(stdout_path),
                              'stderr': str(stderr_path)}}

        LOGGER.debug('RunTask %s ends, elapsed time: %s s', self.name, elapsed)
        return env_up, status
