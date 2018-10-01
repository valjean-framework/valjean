'''Tasks for parsing the TRIPOLI-4 output files. '''

from .. import LOGGER
from ..cosette.pythontask import PythonTask
from .parse_t4 import T4Parser


class ParseT4Task(PythonTask):
    '''Integrate parsing of TRIPOLI-4 run results in a Task.

    This class represents the task of parsing the output file of a TRIPOLI-4
    run into an object that can later be processed by valjean. Since
    :class:`ParseT4Task` inherits from :class:`~cosette.Task`, it is easy to
    integrate objects of this class in valjean's standard framework for
    handling tasks and their dependency graphs (see :class:`~cosette.DepGraph`
    and :class:`~cosette.Scheduler`).
    '''

    def __init__(self, from_run, *, deps=None):
        '''Create a :class:`ParseT4Task` from the name of a TRIPOLI-4 run.

        The `from_run` argument is the name of a TRIPOLI-4 run. When
        :class:`ParseT4Task` is scheduled for execution, it will search the
        environment for the output file of a task called ``'run/' + from_run``.

        The name of this task will be automatically set to
        ``'parse/' + from_run``.

        :param from_run str: The name of a TRIPOLI-4 run.
        :param deps: If this task depends on other tasks (and valjean cannot
                     automatically discover this), pass them (as a list)
                     of strings) to the `deps` parameter.
        :type deps: None or list
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
                output_file = run_result['output_file']
            except KeyError:
                LOGGER.error('Results of run %s are required for '
                             'ParseT4Task %s, but I could not find them',
                             run_name, parse_name)
                raise
            return T4Parser.parse_jdd(output_file)

        parse_name = 'parse/' + from_run
        run_name = 'run/' + from_run
        super().__init__(parse_name, parse_run_from_env, deps=deps,
                         args=(parse_name, run_name), env_kwarg='env')
