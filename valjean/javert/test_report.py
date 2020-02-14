'''This module contains a simple class that models a test report. A report
consists of a number of sections, and each section contains:
* a title;
* some optional introductory text;
* optionally, other test reports and some test results.

This module also contains a task that creates a report from a list of
test-evaluation tasks.
'''

from ..cosette.task import TaskStatus
from ..cosette.pythontask import PythonTask
from ..gavroche.test import TestResult


class TestReport:
    '''This class models a test report. It is essentially a rose tree (i.e. a
    tree with an arbitrary number of children at each node) with nodes
    annotated with a title and some introductory text. :class:`~.TestResult`
    objects play the role of tree leaves.
    '''

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False

    def __init__(self, *, title, text='', content=None):
        '''Create a report.

        :param str title: the report title.
        :param str text: some introductory text.
        :param content: a list of :class:`TestReport` or :class:`~.TestResult`
                        objects.
        :type content: list(TestReport or TestResult)
        '''
        self.title = title
        self.text = text
        self.content = [] if content is None else content
        for sec in self.content:
            if not isinstance(sec, (TestReport, TestResult)):
                raise TypeError('expected a list of TestReport or TestResult '
                                'objects, but one of the items is a {} instead'
                                .format(type(sec)))


class TestReportTask(PythonTask):
    '''Task class that creates a :class:`TestReport` from a function that
    classifies test results into report sections.
    '''

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False

    def __init__(self, name, *, make_report, eval_tasks):
        '''Instantiate a :class:`TestReportTask` from a list of
        :class:`~.EvalTestTask` objects. The `make_report` argument is expected
        to be a function taking one argument, which is a dictionary associating
        the names of the tasks in `eval_tasks` to the results of their
        execution (in the sense of the ``'result'`` key of the associated
        environment section). For tasks that evaluate tests
        (:class:`~.EvalTestTask`), the result typically consists of a list of
        :class:`~.TestResult` objects. The `make_report` function must return a
        :class:`TestReport` object.

        :param str name: the name of this task.
        :param make_report: a function taking a single argument and returning a
            :class:`TestReport`.
        :param eval_tasks: a list of tasks, typically :class:`~.EvalTestTask`.
        :type eval_tasks: list(Task)
        '''

        def report(*, env):
            result_dict = {}
            for test_task in eval_tasks:
                tname = test_task.name
                if (tname not in env
                        or env[tname]['status'] != TaskStatus.DONE
                        or 'result' not in env[tname]):
                    continue  # skip failed or missing tasks
                result_dict[tname] = env[tname]['result']
            report = make_report(result_dict)
            env_up = {self.name: {'result': report}}
            return env_up, TaskStatus.DONE

        super().__init__(name, report, soft_deps=eval_tasks,
                         env_kwarg='env')
