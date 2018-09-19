'''This module contains code that converts a test result into some kind of
human-readable representation (table, plots, etc.).

.. todo::

    Possible improvement: turn :class:`Representation` into an `ABC`; loop over
    the classes in :mod:`~.eponine` that inherit from `:class:`~.TestResult`
    and add `@abstractmethod` methods in :class:`Representation`. This way, if
    a new :class:`~.TestResult` is added to :mod:`~.eponine`, it will no longer
    be possible to instantiate any of the classes that derive from
    :class:`Representation`, pointing to the fact that the code in this module
    needs to be extended to handle the new class. This is better than silently
    falling back to some default do-nothing implementation, which may lead to
    bugs.
'''
from .. import LOGGER
from .items import TableItem


class Representation:
    '''Base class for representing test results as items (in the sense of the
    :mod:`~.items` module).'''

    def __call__(self, result):
        '''Dispatch handling of `result` to the appropriate subclass method,
        based on the name of the class of `result`. This methods essentially
        implements a simplified, run-time version of the Visitor pattern.'''
        class_name = result.__class__.__name__
        meth_name = 'repr_' + class_name.lower()
        try:
            meth = getattr(self, meth_name)
        except AttributeError:
            LOGGER.debug('no representation for class %s', class_name)
            return []
        return meth(result)


class FullRepresentation(Representation):
    '''This class generates the fullest possible representation for test
    results. If anything can be represented as an item,
    :class:`FullRepresentation` will do it.
    '''

    def repr_testresultequal(self, result):
        '''Represent the result of a :class:`~.TestEqual` test.

        :param result: a test result.
        :type result: :class:`~.TestResultEqual`
        :returns: The full representation of a :class:`~.TestResultEqual`; for
                  the moment, this consists of... a table. Wow.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_equal(result, 'equal?')

    def repr_testresultapproxequal(self, result):
        '''Represent the result of a :class:`~.TestApproxEqual` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultApproxEqual`
        :returns: The full representation of a
                  :class:`~.TestResultApproxEqual`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_equal(result, 'approx equal?')

    @staticmethod
    def _repr_equal(result, result_header):
        '''Shared worker function for equality tests.'''
        LOGGER.debug('shape of the result: %s', result.equal.shape)
        table_item = TableItem(result.test.dataset1.value,
                               result.test.dataset2.value,
                               result.equal,
                               highlight=lambda _v1, _v2, eq: not eq,
                               headers=['reference', 'dataset', result_header])
        return [table_item]

    def repr_testresultstudent(self, result):
        '''Represent a :class:`~.TestResultStudent`.'''
        raise NotImplementedError()


class EmptyRepresentation(Representation):
    '''Class that does not generate any items for any test result.'''
