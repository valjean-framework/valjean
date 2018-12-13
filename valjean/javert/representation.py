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

    def repr_testresultapproxequal(self, result):
        '''Represent the result of a :class:`~.TestApproxEqual` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultApproxEqual`
        :returns: The full representation of a
                  :class:`~.TestResultApproxEqual`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_approx_equal(result, 'approx equal?')

    @staticmethod
    def _repr_approx_equal(result, result_header):
        '''Shared worker function for equality tests.'''
        LOGGER.debug('shape of the result: %s', result.approx_equal.shape)
        table_item = TableItem(result.test.dataset1.value,
                               result.test.dataset2.value,
                               result.approx_equal,
                               highlight=lambda _v1, _v2, eq: not eq,
                               headers=['reference', 'dataset', result_header])
        return [table_item]

    def repr_testresultstudent(self, result):
        '''Represent the result of a :class:`~.TestStudent` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultStudent`
        :returns: The full representation of a
                  :class:`~.TestResultStudent`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_student(result, 'student?')

    @staticmethod
    def _repr_student(result, result_header):
        '''Shared worker function for Student tests.'''
        table_item = TableItem(
            result.test.ds1.value, result.test.ds1.error,
            result.test.ds2.value, result.test.ds2.error,
            result.delta, result.bool_array(),
            highlight=lambda _v1, _e1, _v2, _e2, _delta, eq: not eq,
            headers=['v1', 'σ1', 'v2', 'σ2', 'Δ', result_header])
        return table_item

    def repr_testresultbonferroni(self, result):
        '''Represent the result of a :class:`~.TestBonferroni` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultBonferroni`
        :returns: The full representation of a
                  :class:`~.TestResultBonferroni`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_bonferroni(result, 'bonferroni?')

    @staticmethod
    def _repr_bonferroni(result, result_header):
        '''Shared worker function for Bonferroni tests.'''
        table_item = TableItem(
            [result.first_test_res.test.name],
            [result.test.ntests],
            [result.test.alpha],
            [min(result.first_test_res.pvalue)],
            [bool(result)],
            highlight=lambda _t, _ndf, _sl, _min, rnh: not rnh,
            headers=['test', 'ndf', 'α', 'min(p-value)', result_header])
        return table_item

    def repr_testresultholmbonferroni(self, result):
        '''Represent the result of a :class:`~.TestHolmBonferroni` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultHolmBonferroni`
        :returns: The full representation of a
                  :class:`~.TestResultHolmBonferroni`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return self._repr_holm_bonferroni(result, 'holm-bonferroni?')

    @staticmethod
    def _repr_holm_bonferroni(result, result_header):
        '''Shared worker function for Holm-Bonferroni tests.'''
        table_item = TableItem(
            [result.first_test_res.test.name],
            [result.test.ntests],
            [result.test.alpha],
            [min(result.first_test_res.pvalue)],
            [result.alphas_i[0]],
            [result.nb_rejected],
            [bool(result)],
            highlight=lambda _t, _ndf, _sl, _min, _malp, _rej, rnh: not rnh,
            headers=['test', 'ndf', 'α', 'min(p-value)', 'min(α)',
                     'N rejected', result_header])
        return table_item

class EmptyRepresentation(Representation):
    '''Class that does not generate any items for any test result.'''
