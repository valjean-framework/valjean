'''External test used to represent user formatted results in the report.

This test has been designed in order to offer the possibility to define and run
user-defined tests outside valjean and include their results in a report, along
with the native valjean tests.

The user is responsible for defining and representing the test results. The
representation must be done with templates (see :mod:`.templates` module).

For example, the simplest case is a custom plot to represent a test. In that
case, if the path to the image is known a :class:`~.templates.TextTemplate` can
be created and given to the test:

>>> txtemp = TextTemplate("And this represents Javert\\n\\n"
...                       ".. image:: ../../doc/src/images/javert.jpg\\n\\n")
>>> textr = TestExternal(txtemp, name='', success=True).evaluate()
>>> print(bool(textr))
True
'''

from ..gavroche.test import Test, TestResult
from .templates import TextTemplate, PlotTemplate, TableTemplate


class TestResultExternal(TestResult):
    '''Result from a external test.'''

    def __bool__(self):
        '''This test returns the return value specified in the test
        initialisation.
        '''
        return self.test.success


class TestExternal(Test):
    '''Class building a test that will return the boolean value specified at
    initialisation.
    '''

    def __init__(self, *templates, name, description='', labels=None,
                 success=True):
        '''Initialize the :class:`~.TestExternal` object with the templates to
        represent in the report, a name, a description of the test (may be
        long).

        External test are performed by the user who only gives its
        representation as templates and its return value. The return value can
        be an arbitrary value (a test that always returns `True` or `False`)
        for example.

        :param templates: templates representing the external test
        :type templates: TextTemplate, PlotTemplate, TableTemplate
        :param str name: name of the test
        :param str description: description of the test expected with context
        :param dict labels: labels for test classification
        :param bool success: returned value by :class:`TestResultExternal`
        '''
        super().__init__(name=name, description=description, labels=labels)
        if any(not isinstance(t, (TextTemplate, PlotTemplate, TableTemplate))
               for t in templates):
            raise TypeError('Expected templates')
        self.templates = templates
        self.success = success

    def evaluate(self):
        '''Evaluate the test (do nothing in this case except building the
        TestResult).

        :rtype: TestResultExternal
        '''
        return TestResultExternal(self)
