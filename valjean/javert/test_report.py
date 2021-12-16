# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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
                                'objects, but one of the items is a '
                                f'{type(sec)} instead')


class TestReportTask(PythonTask):
    '''Task class that creates a :class:`TestReport` from a function that
    classifies test results into report sections.
    '''

    # tell pytest that this class and derived classes should NOT be collected
    # as tests
    __test__ = False

    def __init__(self, name, *, make_report, eval_tasks, kwargs=None):
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
        :param kwargs: a dictionary of kwargs that will be passed to the
            `make_report` function.
        :type kwargs: dict or None
        '''
        kwargs = {} if kwargs is None else kwargs.copy()

        def report(*, env):
            result_dict = {}
            for test_task in eval_tasks:
                tname = test_task.name
                if (tname not in env
                        or env[tname]['status'] != TaskStatus.DONE
                        or 'result' not in env[tname]):
                    continue  # skip failed or missing tasks
                result_dict[tname] = env[tname]['result']
            report = make_report(result_dict, **kwargs)
            env_up = {self.name: {'result': report}}
            return env_up, TaskStatus.DONE

        super().__init__(name, report, soft_deps=eval_tasks,
                         env_kwarg='env')
