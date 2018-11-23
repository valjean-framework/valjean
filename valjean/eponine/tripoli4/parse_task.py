'''Tasks for parsing the TRIPOLI-4 output files. '''

from ... import LOGGER
from ...cosette.task import TaskStatus
from ...cosette.pythontask import PythonTask
from .parse import T4Parser


class ParseT4Task(PythonTask):
    '''Integrate parsing of TRIPOLI-4 run results in a Task.

    This class represents the task of parsing the output file of a TRIPOLI-4
    run into an object that can later be processed by valjean. Since
    :class:`ParseT4Task` inherits from :class:`~valjean.cosette.task.Task`, it
    is easy to integrate objects of this class in valjean's standard framework
    for handling tasks and their dependency graphs (see
    :class:`~valjean.cosette.depgraph.DepGraph` and
    :class:`~valjean.cosette.scheduler.Scheduler`).
    '''

    PRIORITY = 40

    def __init__(self, name, run, *, deps=None):
        '''Create a :class:`ParseT4Task` from the name of a TRIPOLI-4 run.

        The `run` argument is a TRIPOLI-4
        :class:`~valjean.cosette.run.RunTask`. When :class:`ParseT4Task` is
        scheduled for execution, it will search the environment for the output
        file of a task called ``'run'``.

        :param str name: The name of this task.
        :param run: A TRIPOLI-4 run task.
        :type run: :class:`~valjean.cosette.run.RunTask`
        :param deps: If this task depends on other tasks (and valjean cannot
                     automatically discover this), pass them (as a list) to the
                     `deps` parameter.
        :type deps: None or list(:class:`~valjean.cosette.task.Task`)
        '''

        def parse_run_from_env(parse_name, run_name, *, env):
            # extract the names of the output file from the environment
            try:
                run_result = env[run_name]
            except KeyError:
                LOGGER.error('Results of %s are required for ParseT4Task '
                             '%s, but %s is not in the environment',
                             run_name, parse_name, run_name)
                raise
            try:
                output_file = run_result['stdout']
            except KeyError:
                LOGGER.error('Results of run %s are required for '
                             'ParseT4Task %s, but I could not find them',
                             run_name, parse_name)
                raise
            parse_result = T4Parser.parse_jdd(output_file)
            env_up = {parse_name: {'result': parse_result}}
            if parse_result is None:
                return env_up, TaskStatus.FAILED
            return env_up, TaskStatus.DONE

        deps_ = [] if deps is None else deps.copy()
        deps_.append(run)
        super().__init__(name, parse_run_from_env, deps=deps_,
                         args=(name, run.name), env_kwarg='env')
