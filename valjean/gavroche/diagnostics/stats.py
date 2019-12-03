'''This module defines a few tests that report about the success/failure status
of other tests/tasks.
'''

from collections import defaultdict
from functools import partial, update_wrapper
from enum import IntEnum

from ...cosette.task import TaskStatus, close_dependency_graph
from ...cosette.use import Use
from ..test import Test, TestResult
from ..eval_test_task import EvalTestTask


def task_stats(*, name, description='', tasks):
    '''Create a :class:`TestStatsTasks` from a list of tasks.

    The :class:`TestStatsTasks` class must be instantiated with the list of
    task results, which are not available to the user when the tests are
    specified in the job file. Therefore, the creation of the
    :class:`TestStatsTasks` must be delayed until the other tasks have finished
    and their results are available in the environment. For this purpose it is
    necessary to wrap the instantiation of :class:`TestStatsTasks` in a
    :class:`~.Use` wrapper, and evaluate the resulting test using a
    :class:`~.EvalTestTask`.

    This function hides this bit of complexity from the user. Assume you have a
    list of tasks that you would like to produce statistics about (we will use
    :class:`~.DelayTask` objects for our example):

    >>> from valjean.cosette.task import DelayTask
    >>> my_tasks = [DelayTask(1), DelayTask(3), DelayTask(0.2)]

    Here is how you make a :class:`TestStatsTasks`:

    >>> stats = task_stats(name='stats', tasks=my_tasks)
    >>> from valjean.gavroche.eval_test_task import EvalTestTask
    >>> isinstance(stats, EvalTestTask)
    True
    >>> print(stats.depends_on)
    {Task('create_stats-...')}
    >>> create_stats = next(task for task in stats.depends_on)

    Here `create_stats` is the task that actually creates the
    :class:`TestStatsTasks`. It soft-depends on the tasks in `my_tasks`:

    >>> [task in create_stats.soft_depends_on for task in my_tasks]
    [True, True, True]

    The reason why the dependency is soft is that we want to collect statistics
    about the task outcome in any case, even (especially!) if some of the tasks
    failed.

    :param str name: the name of the task to create.
    :param str description: its description.
    :param tasks: the list of tasks to be tested.
    :type tasks: list(Task)
    :returns: an :class:`~.EvalTestTask` that evaluates the diagnostic test.
    :rtype: EvalTestTask
    '''
    def create_test(*task_results, name, description):
        return [TestStatsTasks(name=name, description=description,
                               task_results=task_results)]

    create_test.__name__ = 'create_' + name
    create_test.__qualname__ = create_test.__qualname__[-10] + 'create_' + name
    inj_args = [(task, None) for task in close_dependency_graph(tasks)]
    wrapped = partial(create_test, name=name, description=description)
    update_wrapper(wrapped, create_test)
    use_create_test = Use(inj_args=inj_args, wrapped=wrapped,
                          priority=EvalTestTask.PRIORITY - 1, deps_type='soft')
    return EvalTestTask.from_test_task(use_create_test.get_task())


class TestStatsTasks(Test):
    '''A test that evaluates statistics about the success/failure status of the
    given tasks.
    '''

    def __init__(self, *, name, description='', task_results):
        '''Instantiate a :class:`TestStatsTasks`.

        :param str name: the test name.
        :param str description: the test description.
        :param task_results: a list of task results, intended as the contents
            of the environment sections associated with the executed tasks.
            This test notably inspects the ``'status'`` key to see if the task
            succeeded.
        :type task_results: list(dict(str, *stuff*))
        '''
        super().__init__(name=name, description=description)
        self.task_results = task_results

    def evaluate(self):
        '''Evaluate this test and turn it into a :class:`TestResultStatsTasks`.
        '''
        status_dict = defaultdict(list)
        for task_name, task_result in self.task_results:
            status_dict[task_result['status']].append(task_name)
        return TestResultStatsTasks(test=self, classify=status_dict)


class TestResultStatsTasks(TestResult):
    '''The result of the evaluation of a :class:`TestStatsTasks`. The test is
    considered successful if all the observed tasks have successfully completed
    (``TaskStatus.DONE``).
    '''

    def __init__(self, *, test, classify):
        '''Instantiate a :class:`TestResultStatsTasks`.

        :param TestStatsTasks test: the test producing this result.
        :param classify: a dictionary mapping the task status to the list of
            task names with the given status.
        :type classify: dict(TaskStatus, list(str))
        '''
        super().__init__(test=test)
        self.classify = classify

    def __bool__(self):
        '''Returns `True` if all the observed tests have succeeded.'''
        return TaskStatus.DONE in self.classify and len(self.classify) == 1


class TestOutcome(IntEnum):
    '''An enumeration that represents the possible outcomes of a test:

    `SUCCESS`
        represents tests that have been evaluated and have succeeded;

    `FAILURE`
        represents tests that have been evaluated and have failed;

    `MISSING`
        represents tasks that did not generate any ``'result'`` key;

    `NOT_A_TEST`
        represents tasks that did not generate a :class:`~.TestResult` object
        as a result;
    '''
    SUCCESS = 0
    FAILURE = 1
    MISSING = 2
    NOT_A_TEST = 3
    __test__ = False


def test_stats(*, name, description='', tasks):
    '''Create a :class:`TestStatsTests` from a list of tests.

    The :class:`TestStatsTests` class must be instantiated with the list of
    test results, which are not available to the user when the tests are
    specified in the job file. Therefore, the creation of the
    :class:`TestStatsTests` must be delayed until the test tasks have finished
    and their results are available in the environment. For this purpose it is
    necessary to wrap the instantiation of :class:`TestStatsTests` in a
    :class:`~.Use` wrapper, and evaluate the resulting test using a
    :class:`~.EvalTestTask`.

    This function hides this bit of complexity from the user. Assume you have a
    list of tasks that generate some tests and that you would like to produce
    statistics about the tests results. Let us construct a toy dataset first:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.eponine.base_dataset import BaseDataset
    >>> x = np.linspace(-5., 5., num=100)
    >>> y = x**2
    >>> error = np.zeros_like(y)
    >>> bins = OrderedDict([('x', x)])
    >>> parabola = BaseDataset(y, error, bins=bins, name='parabola')

    Now we write a function that generates dummy tests for the `parabola`
    dataset:

    >>> from valjean.gavroche.test import TestEqual, TestApproxEqual
    >>> def test_generator():
    ...     return [TestEqual(parabola, parabola, name='equal?'),
    ...             TestApproxEqual(parabola, parabola, name='approx_equal?')]

    We need to wrap this function in a PythonTask so that it can be executed as
    a part of the dependency graph:

    >>> from valjean.cosette.pythontask import PythonTask
    >>> create_tests_task = PythonTask('test_generator', test_generator)

    Here is how you make a :class:`TestStatsTests` to collect statistics about
    the results of the generated tests:

    >>> stats = test_stats(name='stats', tasks=[create_tests_task])
    >>> from valjean.gavroche.eval_test_task import EvalTestTask
    >>> isinstance(stats, EvalTestTask)
    True

    Here `stats` evaluates the test that gathers the statistics, and it depends
    on a special task that generates the :class:`TestStatsTests` instance:

    >>> print(stats.depends_on)
    {Task('create_stats-...')}
    >>> create_stats = next(task for task in stats.depends_on)

    In turn, `create_stats` has a soft dependency on the task that generates
    our test, `create_tests_task`:

    >>> create_tests_task in create_stats.soft_depends_on
    True

    The reason why the dependency is soft is that we want to collect statistics
    about the test outcome in any case, even (especially!) if some of the tests
    failed or threw exceptions.

    :param str name: the name of the task to create.
    :param str description: its description.
    :param tasks: the list of tasks that generate the tests to observe.
    :type tasks: list(Task)
    :returns: an :class:`~.EvalTestTask` that evaluates the diagnostic test.
    :rtype: EvalTestTask
    '''

    def create_test(*task_results, name, description):
        return [TestStatsTests(name=name, description=description,
                               task_results=task_results)]

    create_test.__name__ = 'create_' + name
    create_test.__qualname__ = create_test.__qualname__[-10] + 'create_' + name
    inj_args = [(task, None) for task in tasks]
    wrapped = partial(create_test, name=name, description=description)
    update_wrapper(wrapped, create_test)
    use_create_test = Use(inj_args=inj_args, wrapped=wrapped,
                          priority=EvalTestTask.PRIORITY - 1, deps_type='soft')
    return EvalTestTask.from_test_task(use_create_test.get_task())


# hey, pytest!
test_stats.__test__ = False


class TestStatsTests(Test):
    '''A test that evaluates statistics about the success/failure of the given
    tests.
    '''

    def __init__(self, *, name, description='', task_results):
        '''Instantiate a :class:`TestStatsTests` from a collection of task
        results. The tasks are expected to generate :class:`~.TestResult`
        objects, which must appear in the ``'result'`` key of the task result.
        '''
        super().__init__(name=name, description=description)
        self.task_results = task_results

    def evaluate(self):
        '''Evaluate this test and turn it into a :class:`TestResultStatsTests`.
        '''
        status_dict = defaultdict(list)
        for task_name, task_result in self.task_results:
            if 'result' not in task_result:
                status_dict[TestOutcome.MISSING].append(task_name)
                continue
            test_results = task_result['result']
            for test_result in test_results:
                if not isinstance(test_result, TestResult):
                    status_dict[TestOutcome.NOT_A_TEST].append(task_name)
                if bool(test_result):
                    test_lst = status_dict[TestOutcome.SUCCESS]
                else:
                    test_lst = status_dict[TestOutcome.FAILURE]
                test_lst.append(test_result.test.name)
        return TestResultStatsTests(test=self, classify=status_dict)


class TestResultStatsTests(TestResultStatsTasks):
    '''The result of the evaluation of a :class:`TestStatsTests`. The test is
    considered successful if all the observed tests have been successfully
    evaluated and have succeeded.
    '''
    def __bool__(self):
        return TestOutcome.SUCCESS in self.classify and len(self.classify) == 1
