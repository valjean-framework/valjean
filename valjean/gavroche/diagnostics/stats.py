'''This module defines a few tests that report about the success/failure status
of other tests/tasks.

Three different tests are available:

* statistics over all the tasks done, generated with :func:`task_stats`
* statistics over all the tests performed with :func:`test_stats`
* statistics over the tests performed based on labels given at test
  initialization with :func:`test_stats_by_labels`

The two tests over the test results are performed using the
:class:`~.TestResult`, so the statistics only includes the tests that were
actually run.
'''

from collections import defaultdict
from functools import partial, update_wrapper
from enum import IntEnum

from ...cosette.task import TaskStatus, close_dependency_graph
from ...cosette.use import Use
from ..test import Test, TestResult
from ..eval_test_task import EvalTestTask
from ...eponine.response_book import Index
from ... import LOGGER


def stats_worker(test_fn, name, description, tasks, **kwargs):
    '''Function creating the test for all the required tasks (summary tests of
    test tasks or summary tests on all tasks for example).

    :param test_fn: function generating the test to apply to tasks
    :param str name: the name of the stat task
    :param str description: its description
    :param tasks: the list of tasks to be tested.
    :type tasks: list(Task)
    :returns: an :class:`~.EvalTestTask` that evaluates the diagnostic test.
    :rtype: EvalTestTask
    '''
    test_fn.__name__ = name + '.stats'
    test_fn.__qualname__ = test_fn.__qualname__[-10] + name + '.stats'
    inj_args = [(task, None) for task in tasks]
    wrapped = partial(test_fn, name=name, description=description, **kwargs)
    update_wrapper(wrapped, test_fn)
    use_create_test = Use(inj_args=inj_args, wrapped=wrapped, deps_type='soft')
    return EvalTestTask.from_test_task(use_create_test.get_task())


def task_stats(*, name, description='', labels=None, tasks):
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

    >>> stats = task_stats(name='delays', tasks=my_tasks)
    >>> from valjean.gavroche.eval_test_task import EvalTestTask
    >>> isinstance(stats, EvalTestTask)
    True
    >>> print(stats.depends_on)
    {Task('delays.stats')}
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
    def create_test(*task_results, name, description, labels):
        return [TestStatsTasks(name=name, description=description,
                               labels=labels, task_results=task_results)]

    return stats_worker(create_test, name=name, description=description,
                        labels=labels, tasks=close_dependency_graph(tasks))


class TestStatsTasks(Test):
    '''A test that evaluates statistics about the success/failure status of the
    given tasks.
    '''

    def __init__(self, *, name, description='', labels=None, task_results):
        '''Instantiate a :class:`TestStatsTasks`.

        :param str name: the test name.
        :param str description: the test description.
        :param task_results: a list of task results, intended as the contents
            of the environment sections associated with the executed tasks.
            This test notably inspects the ``'status'`` key to see if the task
            succeeded.
        :type task_results: list(dict(str, *stuff*))
        '''
        super().__init__(name=name, description=description, labels=labels)
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


def test_stats(*, name, description='', labels=None, tasks):
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
    list of tasks that evaluate some tests and that you would like to produce
    statistics about the tests results. Let us construct a toy dataset first:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.gavroche.dataset import Dataset
    >>> x = np.linspace(-5., 5., num=100)
    >>> y = x**2
    >>> error = np.zeros_like(y)
    >>> bins = OrderedDict([('x', x)])
    >>> parabola = Dataset(y, error, bins=bins, name='parabola')
    >>> parabola2 = Dataset(y*(1+1e-6), error, bins=bins, name='parabola2')

    Now we write a function that generates dummy tests for the `parabola`
    dataset:

    >>> from valjean.gavroche.test import TestEqual, TestApproxEqual
    >>> def test_generator():
    ...     result = [TestEqual(parabola, parabola2, name='equal?').evaluate(),
    ...               TestApproxEqual(parabola, parabola2,
    ...                               name='approx_equal?').evaluate()]
    ...     return {'test_generator': {'result': result}}, TaskStatus.DONE


    We need to wrap this function in a PythonTask so that it can be executed as
    a part of the dependency graph:

    >>> from valjean.cosette.pythontask import PythonTask
    >>> create_tests_task = PythonTask('test_generator', test_generator)

    Here is how you make a :class:`TestStatsTests` to collect statistics about
    the results of the generated tests:

    >>> stats = test_stats(name='equal', tasks=[create_tests_task])

    >>> from valjean.gavroche.eval_test_task import EvalTestTask
    >>> isinstance(stats, EvalTestTask)
    True

    Here `stats` evaluates the test that gathers the statistics, and it depends
    on a special task that generates the :class:`TestStatsTests` instance:

    >>> print(stats.depends_on)
    {Task('equal.stats')}
    >>> create_stats = next(task for task in stats.depends_on)

    In turn, `create_stats` has a soft dependency on the task that generates
    our test, `create_tests_task`:

    >>> create_tests_task in create_stats.soft_depends_on
    True

    The reason why the dependency is soft is that we want to collect statistics
    about the test outcome in any case, even (especially!) if some of the tests
    failed or threw exceptions.

    Let's run the tests:

    >>> from valjean.config import Config
    >>> config = Config(paths=[])
    >>> from valjean.cosette.env import Env
    >>> env = Env()
    >>> for task in [create_tests_task, create_stats, stats]:
    ...     env_up, status = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(status)
    TaskStatus.DONE

    The results are stored in a :class:`list` under the key ``'result'``:

    >>> print(len(env[stats.name]['result']))
    1
    >>> stats_res = env[stats.name]['result'][0]
    >>> print("SUCCESS:", stats_res.classify[TestOutcome.SUCCESS])
    SUCCESS: ['approx_equal?']
    >>> print("FAILURE:", stats_res.classify[TestOutcome.FAILURE])
    FAILURE: ['equal?']

    :param str name: the name of the task to create.
    :param str description: its description.
    :param tasks: the list of tasks that generate the tests to observe.
    :type tasks: list(Task)
    :returns: an :class:`~.EvalTestTask` that evaluates the diagnostic test.
    :rtype: EvalTestTask
    '''

    def create_test(*task_results, name, description, labels):
        return [TestStatsTests(name=name, description=description,
                               labels=labels, task_results=task_results)]

    return stats_worker(create_test, name=name, description=description,
                        labels=labels, tasks=tasks)


# hey, pytest!
test_stats.__test__ = False


class TestStatsTests(Test):
    '''A test that evaluates statistics about the success/failure of the given
    tests.
    '''

    def __init__(self, *, name, description='', labels=None, task_results):
        '''Instantiate a :class:`TestStatsTests` from a collection of task
        results. The tasks are expected to generate :class:`~.TestResult`
        objects, which must appear in the ``'result'`` key of the task result.
        '''
        super().__init__(name=name, description=description, labels=labels)
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
                if test_result:
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


def test_stats_by_labels(*, name, description='', labels=None,
                         tasks, by_labels):
    '''Create a :class:`TestStatsTestsByLabels` from a list of tests.

    See :func:`test_stats` for the generalities about this function.

    Compared to :func:`test_stats` it takes one argument more: ``'by_labels'``
    to classify then build statistics based on these labels. **The order of the
    labels matters**, as they are successively selected.

    Let's define three menus:

    >>> menu1 = {'food': 'egg + spam', 'drink': 'beer'}
    >>> menu2 = {'food': 'egg + bacon', 'drink': 'beer'}
    >>> menu3 = {'food': 'lobster thermidor', 'drink': 'brandy'}

    These three menus are ordered by pairs. Statistics on meals are
    kept in the restaurant, using :class:`~.TestMetadata`. The goal of the
    tests is to know if both persons of a pair order the same menu and when
    they do it.

    .. code::

        orders = [TestMetadata(
            {'Graham': menu1, 'Terry': menu1}, name='gt_wday_lunch',
            labels={'day': 'Wednesday', 'meal': 'lunch'}),
                  TestMetadata(
            {'Michael': menu1, 'Eric': menu2}, name='me_wday_dinner',
            labels={'day': 'Wednesday', 'meal': 'dinner'}),
                  TestMetadata(
            {'John': menu2, 'Terry': menu2}, name='jt_wday',
            labels={'day': 'Wednesday'}),
                  TestMetadata(
            {'Terry': menu3, 'John': menu3}, name='Xmasday',
            labels={'day': "Christmas Eve"})]

    The restaurant owner uses :func:`test_stats_by_labels` to build statistics
    on his menus and the habits of his consumers.

    For example, the menus filtered on ``day`` will give:

    .. code::

        =============  ============  =============
              day       % success      % failure
        =============  ============  =============
        Christmas Eve      1/1            0/1
            Wednesday      2/3            1/3
        =============  ============  =============

    These results means, considering the tests requested, both consumers have
    the same meal on Christmas Eve. On Wednesday, one pair of customers out of
    three did not order the same menu.

    The same kind of statistics can be done based on the meal:

    .. code::

        ==========  ============  =============
           meal       % success     % failure
        ==========  ============  =============
          dinner         0/1            1/1
           lunch         1/1            0/1
        ==========  ============  =============

    In that case two tests were not taken into account as they did not have any
    ``'meal'`` label.

    It is also possible to make selections on multiple labels. In that case the
    order matters: the classification is performed following the order of the
    labels requested. For example, ``'meal'`` then ``'day'`` :

    .. code::

        ==========  =========  ============  =============
           meal        day       % success     % failure
        ==========  =========  ============  =============
          dinner    Wednesday       0/1            1/1
           lunch    Wednesday       1/1            0/1
        ==========  =========  ============  =============

    * Only two tests are filtered due to the meal selection
    * Requesting ``'day'`` then ``'meal'`` would only inverse the two first
      columns in that case and emit a **warning**: a preselection on ``'day'``
      is done and in Christmas Eve case the ``'meal'`` label is not provided,
      the selection cannot be done. In the Wednesday one, no problem ``'meal'``
      appears at least in one case (two in our cases).

    Finally if the request involves a label that does not exist in any test an
    exception will be raised, mentioning the failing label.

    :param str name: the name of the task to create.
    :param str description: its description.
    :param tasks: the list of tasks that generate the tests to observe.
    :type tasks: list(Task)
    :param tuple(str) by_labels: labels from the tests on which the
        classification will be based
    :returns: an :class:`~.EvalTestTask` that evaluates the diagnostic test.
    :rtype: EvalTestTask
    '''
    def create_test(*task_results, name, description, labels, by_labels=None):
        return [TestStatsTestsByLabels(
            name=name, description=description, labels=labels,
            task_results=task_results, by_labels=by_labels)]

    return stats_worker(create_test, name=name, description=description,
                        labels=labels, tasks=tasks, by_labels=by_labels)


# hey, pytest!
test_stats_by_labels.__test__ = False


class TestStatsTestsByLabelsException(Exception):
    '''Exception raised during the diagnostic test on :class:`~.TestResult`
    when a classification by labels is required.'''
    # And for pytest...
    __test__ = False


class TestStatsTestsByLabels(Test):
    '''A test that evaluates statistics about the success/failure of the given
    tests using their labels to classify them.

    Usually more than one test is performed for each tested case. This test
    summarize tests done on a given category defined by the user in the usual
    tests (:class:`~.TestStudent`, :class:`~.TestMetadata`, etc.).

    During the evaluation a list of dictionaries of labels is built for each
    test. These labels are given by the user at the initialization of the test.
    Each dictionary also contains the name of the test (name of the task) and
    its result (sucess or failure). From this list of dictionaries an
    :class:`~.Index` is built.

    The result of the evaluation is given a a list of dictionaries containing
    the strings corresponding to the chosen labels under the ``'labels'`` key
    and the number of results OK, KO and total.
    '''
    def __init__(self, *, name, description='', labels=None, task_results,
                 by_labels):
        '''Instantiate a :class:`TestStatsTestsByLabels` from a collection of
        task results. The tasks are expected to generate :class:`~.TestResult`
        objects, which must appear in the ``'result'`` key of the task result.

        :param str name: the test name
        :param str description: the test description
        :param task_result: a list of task results, each task normally contains
            a :class:`~.TestResult`, used in this test.
        :param tuple by_labels: ordered labels to sort the test results. These
            labels are the test labels.
        '''
        super().__init__(name=name, description=description, labels=labels)
        self.task_results = task_results
        self.by_labels = by_labels
        self.labels_lod = None
        self.index = None

    def _build_labels_lod(self):
        '''Build the labels list of dictionaries that allows the creation of
        the index.

        Two additional labels are added to the labels list: ``'_test_name'``
        and ``'_result'`` that should not be used as test's labels. The first
        one could be needed some time and is expected to be unique, the second
        one is filled with :class:`TestOutcome`.
        '''
        self.labels_lod = []
        for _task_name, task_result in self.task_results:
            if 'result' not in task_result:
                continue
            test_results = task_result['result']
            for test_result in test_results:
                ldic = test_result.test.labels.copy()
                if '_test_name' in ldic:
                    LOGGER.warning(
                        "'_test_name' is a label in some test, will be "
                        "replaced in TestStatsTestsByLabels")
                ldic['_test_name'] = test_result.test.name
                if '_result' in ldic:
                    LOGGER.warning(
                        "'_result' is a label in some test, will be replaced"
                        "in TestStatsTestsByLabels")
                if test_result:
                    ldic['_result'] = TestOutcome.SUCCESS
                else:
                    ldic['_result'] = TestOutcome.FAILURE
                self.labels_lod.append(ldic)

    def _build_index(self):
        self.index = Index()
        for itres, tres in enumerate(self.labels_lod):
            for lab in tres:
                self.index[lab][tres[lab]].add(itres)

    def _rloop_over_labels(self, index, labels, rok, rko, plab=()):
        '''Recursive method to select labels and calculate the relative
        statistics.

        If ``labels`` contains only one element, the method build a dictionary
        that summarizes the OK, KO and total number of tests for the considered
        label. The method returns a list containing the dictionary as its only
        element.

        The previous labels are obtained from the ``plab`` argument.

        If ``labels`` contains multiple labels, the first label is considered
        first. For each possible value of the label, the method constructs a
        sub-index by filtering the index on the given label and recursively
        calls itself on the sub-index. The ``plab`` arguement contains the list
        of all the labels that have been considered so far. The lists of
        dictionaries that result from the recursive calls are concatenated into
        a single list and returned.

        :param Index index: index used to calculate the statistics
        :param tuple(str) labels: ordered labels to sort the test results
        :param set rok: successful test results
        :param set rko: failed test results
        :param tuple plab: previous labels
        :rtype: list(dict)
        '''
        # pylint: disable=too-many-arguments
        label = labels[0]
        if label not in index:
            LOGGER.warning('%s not found in some tests labels', label)
            return []
        if len(labels) > 1:
            lres = []
            for lab, labset in index.get(label, {}).items():
                subind = index.keep_only(labset)
                lres.extend(self._rloop_over_labels(subind, labels[1:],
                                                    rok, rko,
                                                    plab=plab+(lab,)))
            return lres
        lres = []
        for lab, labset in index.get(label, {}).items():
            lres.append({'labels': plab + (lab,),
                         'OK': len(labset & rok),
                         'KO': len(labset & rko),
                         'total': len(labset)})
        return lres

    def _stats_for_labels(self):
        '''Check the presence of all required labels in the index, build the
        success and failures sets and return the dictionary of results.

        :raises: TestStatsTestsByLabelsExeption
        :returns: list of dictionaries of labels and states
        :rtype: list(dict)
        '''
        if not set(self.by_labels) <= set(self.index):
            raise TestStatsTestsByLabelsException(
                'TestStatsTestsByLabels: {} not found in tests labels'
                .format(self.by_labels))
        rok = self.index['_result'][TestOutcome.SUCCESS]
        rko = self.index['_result'][TestOutcome.FAILURE]
        res = self._rloop_over_labels(self.index, self.by_labels, rok, rko)
        return sorted(res, key=lambda x: x['labels'])

    def evaluate(self):
        '''Evaluate this test and turn it into a
        :class:`TestResultStatsTestsByLabels`.
        '''
        self._build_labels_lod()
        self._build_index()
        sfl = self._stats_for_labels()
        return TestResultStatsTestsByLabels(test=self, classify=sfl)


class TestResultStatsTestsByLabels(TestResultStatsTasks):
    '''The result of the evaluation of a :class:`TestStatsTestsByLabels`. The
    test is considered successful if all the observed tests have been
    successfully evaluated and have succeeded.

    An oracle is available for each individual test (usually what is required
    here).

    ``self.classify`` is here a list of dictionaries with the following keys:
    ``['labels', 'OK', 'KO', 'total']``.
    '''
    def __bool__(self):
        '''Test is successful if all tests are.'''
        return all(self.oracles())

    def oracles(self):
        '''Test if each test is successful.

        :rtype: list(bool)
        '''
        return [t['OK'] == t['total'] for t in self.classify]

    def nb_missing_labels(self):
        '''Return the number of tests where at least one of the labels required
        were missing.

        :rtype: int
        '''
        return (len(self.test.labels_lod)
                - sum([s['total'] for s in self.classify]))
