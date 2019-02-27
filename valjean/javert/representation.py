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
from .items import TableItem, PlotItem, FullPlotItem


class Representation:
    '''Base class for representing test results as items (in the sense of the
    :mod:`~.items` module).'''

    def __call__(self, result, **kwargs):
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
        return meth(result, **kwargs)


class TableRepresentation(Representation):
    '''This class represents the different representations available for
    tables.
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
        return [table_item]

    def repr_testresultbonferroni(self, result):
        '''Represent the result of a :class:`~.TestBonferroni` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultBonferroni`
        :returns: The full representation of a
                  :class:`~.TestResultBonferroni`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return (self.repr_testresultstudent(result.first_test_res)
                + self._repr_bonferroni(result, 'bonferroni?'))

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
        return [table_item]

    def repr_testresultholmbonferroni(self, result):
        '''Represent the result of a :class:`~.TestHolmBonferroni` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultHolmBonferroni`
        :returns: The full representation of a
                  :class:`~.TestResultHolmBonferroni`.
        :rtype: list(:class:`~.TableItem`)
        '''
        return (self.repr_testresultstudent(result.first_test_res)
                + self._repr_holm_bonferroni(result, 'holm-bonferroni?'))

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
        return [table_item]


class PlotRepresentation(Representation):
    '''This class represents the different representations available for plots.
    '''

    def repr_testresultstudent(self, result, **kwargs):
        '''Represent the result of a :class:`~.TestStudent` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultStudent`
        :returns: The full representation of a
                  :class:`~.TestResultStudent`.
        :rtype: list(:class:`~.PlotItem`)
        '''
        dims = [k for k, v in result.test.ds1.bins.items() if v.size != 0]
        dim = kwargs.pop('dim', dims[0] if dims else '')
        return self._repr_student(result, test_name=r'$\Delta_{Student}$',
                                  dim=dim, **kwargs)

    @staticmethod
    def _repr_student(result, *, dim, test_name='', plot_res=False,
                      only_res=False, **kwargs):
        '''Shared worker function for Student tests.

        :returns: list( :class:`~.PlotItem` )
        '''
        lres = []
        plot_res = True if only_res else plot_res
        if not only_res:
            lres.append(PlotItem(
                result.test.ds1.value, result.test.ds1.bins[dim],
                yerrors=result.test.ds1.error, xname=dim,
                label=result.test.ds1.name, **kwargs))
            lres.append(PlotItem(
                result.test.ds2.value, result.test.ds2.bins[dim],
                yerrors=result.test.ds2.error, xname=dim,
                label=result.test.ds2.name, **kwargs))
        if plot_res:
            lres.append(PlotItem(result.delta,
                                 result.test.ds1.bins[dim],
                                 xname=dim, yname=test_name, **kwargs))
        # return [plot_item]
        return lres


class PlotRepresentation2(Representation):
    '''PlotRepresentation usinf FullPlotItem.'''

    def repr_testresultstudent(self, result, **kwargs):
        '''Represent the result of a :class:`~.TestStudent` test.

        :param  result: a test result.
        :type result: :class:`~.TestResultStudent`
        :returns: The full representation of a
                  :class:`~.TestResultStudent`.
        :rtype: list(:class:`~.PlotItem`)
        '''
        if kwargs.pop('only_res', False):
            return self._repr_student_delta(result, dim=kwargs['dim'])
        if kwargs.pop('only_values', False):
            return self._repr_student_values(result, **kwargs)
        return self._repr_student(result, **kwargs)

    @staticmethod
    def _repr_student(result, dim, **kwargs):
        '''Shared worker function for Student tests returning FullPlotItems.

        :returns: :class:`~.FullPlotItem`

        Remark: if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.
        '''
        bins = result.test.ds1.bins[dim]
        xname = dim
        values = [result.test.ds1.value, result.test.ds2.value, result.delta]
        labels = (['dataset 1', 'dataset 2', r'$\Delta_{Student}$']
                  if 'labels' not in kwargs else kwargs['labels'])
        ynames = (['score', 'score', r'$\Delta_{Student}$']
                  if 'ynames' not in kwargs else kwargs['ynames'])
        errors = [result.test.ds1.error, result.test.ds2.error, None]
        return [FullPlotItem(bins=bins, values=values, labels=labels,
                             ynames=ynames, xname=xname, errors=errors)]

    @staticmethod
    def _repr_student_delta(result, dim):
        '''Shared worker function for Student tests returning FullPlotItems.
        Only returns the delta distribution here.

        :returns: :class:`~.FullPlotItem`

        Remark: if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.
        '''
        bins = result.test.ds1.bins[dim]
        xname = dim
        values = [result.delta]
        labels = [r'$\Delta_{Student}$']
        ynames = [r'$\Delta_{Student}$']
        errors = [None]
        return [FullPlotItem(bins=bins, values=values, labels=labels,
                             ynames=ynames, xname=xname, errors=errors)]

    @staticmethod
    def _repr_student_values(result, dim, **kwargs):
        '''Shared worker function for Student tests returning FullPlotItems.
        Only returns the delta distribution here.

        :returns: :class:`~.FullPlotItem`

        Remark: if we have a member ``units`` in base_dataset the axis names
        would be constructed like ``name + units['name']``.
        '''
        bins = result.test.ds1.bins[dim]
        xname = dim
        values = [result.test.ds1.value, result.test.ds2.value]
        labels = (['dataset 1', 'dataset 2'] if 'labels' not in kwargs
                  else kwargs['labels'])
        ynames = (['score', 'score'] if 'ynames' not in kwargs
                  else kwargs['ynames'])
        errors = [result.test.ds1.error, result.test.ds2.error]
        return [FullPlotItem(bins=bins, values=values, labels=labels,
                             ynames=ynames, xname=xname, errors=errors)]


class EmptyRepresentation(Representation):
    '''Class that does not generate any items for any test result.'''


class FullRepresentation(Representation):
    '''This class generates the fullest possible representation for test
    results. If anything can be represented as an item,
    :class:`FullRepresentation` will do it.
    '''

    def __init__(self):
        self.table_repr = TableRepresentation()
        self.plot_repr = PlotRepresentation()

    def __call__(self, result, **kwargs):
        '''Dispatch handling of `result` to all the Representation subclass
        instance attributes of :class:`FullRepresentation`, based on the name
        of the class of `result`.'''
        class_name = result.__class__.__name__
        meth_name = 'repr_' + class_name.lower()
        try:
            table_meth = getattr(self.table_repr, meth_name)
            table_res = table_meth(result)
        except AttributeError:
            LOGGER.debug('no table representation for class %s', class_name)
            table_res = []
        try:
            plot_meth = getattr(self.plot_repr, meth_name)
            plot_res = plot_meth(result, **kwargs)
        except AttributeError:
            LOGGER.debug('no plot representation for class %s', class_name)
            plot_res = []
        return table_res + plot_res


class FullRepresentation2(Representation):
    '''This class generates the fullest possible representation for test
    results. If anything can be represented as an item,
    :class:`FullRepresentation` will do it.
    '''

    def __init__(self):
        self.table_repr = TableRepresentation()
        self.plot_repr = PlotRepresentation2()

    def __call__(self, result, **kwargs):
        '''Dispatch handling of `result` to all the Representation subclass
        instance attributes of :class:`FullRepresentation`, based on the name
        of the class of `result`.'''
        class_name = result.__class__.__name__
        meth_name = 'repr_' + class_name.lower()
        try:
            table_meth = getattr(self.table_repr, meth_name)
            table_res = table_meth(result)
        except AttributeError:
            LOGGER.debug('no table representation for class %s', class_name)
            table_res = []
        try:
            plot_meth = getattr(self.plot_repr, meth_name)
            plot_res = plot_meth(result, **kwargs)
        except AttributeError:
            LOGGER.debug('no plot representation for class %s', class_name)
            plot_res = []
        return table_res + plot_res
