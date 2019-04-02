'''The purpose of this module is to define the :class:`EvalTestTask` class, a
task that evaluates a collection of :class:`~.gavroche.test.Test` objects and
transforms them into :class:`~.gavroche.test.TestResult` objects, which can be
subsequently processed for inclusion in a test report.
'''

from ..cosette.task import TaskStatus
from ..cosette.use import from_env
from ..cosette.pythontask import PythonTask
from ..gavroche.test import Test


class EvalTestTask(PythonTask):
    '''Class that evaluates a list of tests and stores the resulting
    :class:`~.TestResult` objects in the environment.'''

    PRIORITY = 40

    @classmethod
    def from_test_task(cls, test_task):
        '''This method instantiates an :class:`EvalTestTask` that will evaluate
        all the tests generated by a given task.

        :param Task test_task: a task that is expected to generate a list of
                               tests as a result.
        '''
        test_task_name = test_task.name
        eval_task_name = 'eval-' + test_task_name
        return cls(eval_task_name, test_task_name, deps=[test_task])

    def __init__(self, name, test_task_name, *, deps=None, soft_deps=None):
        '''Direct instantiation of an :class:`EvalTestTask`.

        :param str name: the name of this task.
        :param str test_task_name: the name of the task that generated the
                                   tests.
        :param deps: the list of dependencies for this task.
        :type deps: list(Task) or None
        :param soft_deps: the list of soft dependencies for this task.
        :type soft_deps: list(Task) or None
        '''
        def evaluate(*, env):
            tests = from_env(env=env, task_name=test_task_name, key='result')
            if not isinstance(tests, list):
                raise TypeError('Expected a list of tests in EvalTestTask '
                                '{!r}; got a {} instead'
                                .format(self.name, type(tests)))
            for test in tests:
                if not isinstance(test, Test):
                    raise TypeError('Expected a list of tests in EvalTestTask '
                                    '{!r}, but one of the list elements is a '
                                    '{}'.format(self.name, type(test)))

            results = [test.evaluate() for test in tests]

            env_up = {self.name: {'result': results}}
            status = TaskStatus.DONE
            return env_up, status

        super().__init__(name, evaluate, deps=deps, soft_deps=soft_deps,
                         env_kwarg='env')
