'''This module contains a simple class that models a test report. A report
consists of a number of sections, and each section contains:
* a title;
* some optional introductory text;
* optionally, other test reports and some test results.
'''

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
