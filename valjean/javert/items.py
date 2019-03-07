'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.

Examples are mainly given in the :func:`concatenate`.
'''

import numpy as np
# from .. import LOGGER


class TableItem:
    '''A container class that encapsulates all the necessary information to
    represent a table.'''

    def __init__(self, *columns, headers=None, units=None,
                 highlight=lambda *args: False):
        '''Construct a table from a set of columns. The columns must be
        :class:`numpy.ndarray` objects, and they must all contain the same
        number of elements (same array *size*).

        Column headers may be specified using the `headers` argument; in this
        case, the number of headers must be equal to the number of columns.

        Column units can also be specified using the `units` argument. Again,
        you must pass as many units as there are columns.

        Finally, it is possible to specify which table rows should be
        highlighted. This is done by passing a predicate (a closure returning a
        bool) as the `highlight` argument. Formatters will call the closure
        passing the contents of each row in turn, and will highlight those rows
        for which the predicate returns `True`. What it means for a row to be
        highlighted specifically depends on the chosen output format.

        :param columns: a list of columns.
        :type columns: :class:`list` (:class:`numpy.ndarray`)
        :param list(str) headers: a list of headers.
        :param list(str) units: a list of measurement units.
        :param highlight: a callable of the form `f(*row) -> bool`.
        '''
        # print(columns, type(columns))
        self.columns = columns
        n_columns = len(columns)
        self.headers = ['']*n_columns if headers is None else headers
        self.units = ['']*n_columns if units is None else units
        self.highlight = highlight

        # print(self.columns, id(self.columns))
        # print(self.columns[0], id(self.columns[0]))
        # print(len(columns))
        # print(len(headers), id(self.headers))

        # some sanity checks follow
        if not columns:
            raise ValueError('at least one column expected')

        if len(self.headers) != len(self.columns):
            err = ('number of column headers ({}) must match number of '
                   'columns ({})'.format(len(self.headers), len(self.columns)))
            raise ValueError(err)

        if len(self.units) != len(self.columns):
            err = ('number of column units ({}) must match number of '
                   'columns ({})'.format(len(self.units), len(self.columns)))
            raise ValueError(err)

        for i, col in enumerate(self.columns):
            if not isinstance(col, (np.ndarray, np.generic, list)):
                raise TypeError('table columns must be lists or Numpy arrays, '
                                'not {}'.format(type(col)))

            col_size = (col.size if isinstance(col, (np.ndarray, np.generic))
                        else len(col))
            if i == 0:
                n_elems = col_size
            elif col_size != n_elems:
                err = ('columns must have the same number of elements; '
                       'column 0 has size {}, but column {} has size {}'
                       .format(n_elems, i, col_size))
                raise ValueError(err)

    def copy(self):
        '''Copy a :class:`TableItem` object.

        :returns: :class:`TableItem`

        .. note:: the highlignt function is not really copied, it has the same
            address as the self one. I don't know how to change that.
        '''
        return TableItem(*tuple(col.copy() for col in self.columns),
                         headers=self.headers.copy(),
                         units=self.units.copy(), highlight=self.highlight)

    def __iadd__(self, other):
        '''Implement ``+=`` operator.

        :param other: :class:`TableItem` to add to the current one
        :returns: updated :class:`TableItem`
        '''
        if self.headers != other.headers:
            raise ValueError("TableItems to add should have same headers")
        # if any([isinstance(col, np.ndarray) for col in self.columns]):
        #     raise TypeError("No addition permitted on array (else it would "
        #                     "really add the arrays)")
        self.columns = tuple(
            self.columns[i] + other.columns[i]
            if isinstance(self.columns[i], list)
            else np.hstack((self.columns[i], other.columns[i]))
            for i in range(len(self.columns)))
        self.units = other.units if self.units is None else self.units
        return self

    def __add__(self, other):
        '''Implement ``+`` operator.

        :param other: :class:`TableItem` to add to the current one
        :returns: new :class:`TableItem`
        '''
        copy = self.copy()
        copy += other
        return copy

    def __repr__(self):
        '''Print TableItem details.'''
        intro = ["class: {0}\n"
                 "headers: {1}\n".format(self.__class__, self.headers)]
        elts = []
        for icol, col in enumerate(self.columns):
            elts.append("{0}: {1}\n".format(self.headers[icol], col))
        return ''.join(intro + elts)


class CurveElements:
    '''Class to define the characteristics of each curve to be plotted.'''

    def __init__(self, values, label, *, yname='', errors=None):
        '''Construction of :class:`CurveElements`: curve details (values,
        label, etc).

        Major parameters are ``yname``, set per default to ``''``: this is the
        y-axis name. When representing the curve on the pyplot, the subplot is
        chosen according this ``yname``.

        The label is used in the legend.

        Values and errors (if given) should be :obj:`numpy.ndarray` of same
        shape.

        :param values: list of arrays to be represented on the plot,
            **mandatory**
        :type values: :class:`list` (:obj:`numpy.ndarray`)
        :param str label: label to be used in the legend to characterize the
            curve, **mandatory**
        :param str yname: label of y-axis (used to determine the number of
            subplots on the plot)
        :param errors: errors associated to values (per default only on y-axis)
        :type errors: :class:`list` (:obj:`numpy.ndarray`)
        '''
        self.values = values
        self.label = label
        self.yname = yname
        self.errors = errors

        if not isinstance(self.values, np.ndarray):
            raise TypeError('Values should be np.ndarray.')

        if self.errors is not None:
            if not isinstance(self.errors, np.ndarray):
                raise TypeError('Errors should be np.ndarray or None')

    def copy(self):
        '''Copy a :class:`CurveElements` object.

        :returns: :class:`CurveElements`
        '''
        return CurveElements(values=self.values.copy(),
                             label=self.label,
                             yname=self.yname,
                             errors=(None if self.errors is None
                                     else self.errors.copy()))


class PlotItem:
    '''A container for full test result to be represented as a plot. This
    includes all the datasets and the test result. This can also include
    p-values or other test parameters, depending on what is given to the
    PlotItem.
    '''

    def __init__(self, *, bins, curves, xname=''):
        '''Construction of the PlotItem from x-bins and curves.

        The curves should be :class:`CurveElements`.

        The bins means the x-axis bins. They should be common to all the
        curves. It is up to the user to insure that (when coming from a unique
        test this should be automatic).

        :param bins: bins, common for all plots (important), only one set is
            needed
        :type bins: :obj:`numpy.ndarray`
        :param str xname: name of x-axis (default: ``''``)
        :param curves: list of curves characteristics
        :type curves: :class:`list` ( :class:`CurveElements` )
        '''
        self.bins = bins
        self.xname = xname
        self.curves = curves

        if not isinstance(self.curves, list):
            raise TypeError("Curves should be a list of CurveElements.")

        for curve in self.curves:
            if not isinstance(curve, CurveElements):
                raise TypeError("Curve should be a PlotElement.")

    def copy(self):
        '''Copy a :class:`PlotItem` object.

        :returns: :class:`PlotItem`
        '''
        return PlotItem(bins=self.bins.copy(),
                        xname=self.xname,
                        curves=[pelt.copy() for pelt in self.curves])

    def __iadd__(self, other):
        '''Implement ``+=`` operator.

        :param other: :class:`PlotItem` to add to the current one
        :returns: updated :class:`PlotItem`
        '''
        if self.xname != other.xname:
            raise ValueError("PlotItems should have the same xname")
        if not np.array_equal(self.bins, other.bins):
            raise ValueError("Bins should be the same in both PlotItems")
        self.curves.extend(other.curves)
        return self

    def __add__(self, other):
        '''Implement ``+`` operator.

        :param other: :class:`PlotItem` to add to the current one
        :returns: new :class:`PlotItem`
        '''
        copy = self.copy()
        copy += other
        return copy

    def __repr__(self):
        '''Printing of PlotItem.'''
        intro = ["class: {0}\n"
                 "bins: {1}\n"
                 "xname: {2}\n".format(self.__class__, self.bins, self.xname)]
        elts = []
        for curve in self.curves:
            elts.append("label:  {0}\n"
                        "yname:  {1}\n"
                        "values: {2}\n"
                        "errors: {3}\n".format(curve.label, curve.yname,
                                               curve.values, curve.errors))
        return ''.join(intro + elts)


def concatenate(litems):
    '''Concatenate a list of items containing TableItems, PlotItems.

    It concatenates the various items of same shape, following the
    :meth:`TableItem.__iadd__` and :meth:`PlotItem.__iadd__` methods:

    * same number of columns and same headers for TableItems
    * same bins and x-axis names for PlotItems

    This means that the same list could be obtained in return if none of the
    items are compatible.

    :param litems: list of items
    :type litems: :class:`list` ( :class:`TableItem`, :class:`PlotItem`)
    :returns: :class:`list` ( :class:`TableItem`, :class:`PlotItem`)


    >>> import numpy as np
    >>> litems = [TableItem(np.arange(4), np.arange(4)*0.5,
    ...                     headers=['col1', 'col2']),
    ...           TableItem(np.float_(1.5), np.float_(1.4),
    ...                     headers=['col1', 'col2']),
    ...           TableItem(np.float_(1.2), np.float_(0.9),
    ...                     headers=['col1', 'col2']),
    ...           TableItem(np.float_(0.8), np.float_(1.1),
    ...                     headers=['valA', 'valB'])]
    >>> conc_list = concatenate(litems)
    >>> print(len(conc_list))
    2
    >>> for item in conc_list:
    ...     print("{!r}".format(item))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['col1', 'col2']
    col1: [0.  1.  2.  3.  1.5 1.2]
    col2: [0.  0.5 1.  1.5 1.4 0.9]
    <BLANKLINE>
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['valA', 'valB']
    valA: 0.8
    valB: 1.1
    <BLANKLINE>

    In this case all :class:`TableItem` objects with same headers are
    concatenated in one.

    Concatenation is possible for arrays to provide a bigger array without
    separation between each of them

    >>> litems = [TableItem(np.arange(4), np.arange(4)*0.5,
    ...                     headers=['col1', 'col2']),
    ...           TableItem(np.arange(3)*0.1, np.arange(3)*0.05,
    ...                     headers=['col1', 'col2']),]
    >>> conc_items = concatenate(litems)
    >>> for item in conc_items:
    ...     print("{!r}".format(item))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['col1', 'col2']
    col1: [0.  1.  2.  3.  0.  0.1 0.2]
    col2: [0.   0.5  1.   1.5  0.   0.05 0.1 ]
    <BLANKLINE>

    With :class:`PlotItem` and :class:`TableItem` each own concatenation is
    used:

    >>> bins1, data11, data12 = np.arange(4), np.arange(4), np.arange(4)*10
    >>> bins2, data2 = np.arange(5), np.arange(5)*0.5
    >>> litems = [TableItem(bins1, data11,
    ...                     headers=['col1', 'col2']),
    ...           TableItem(bins1, data12,
    ...                     headers=['valA', 'valB']),
    ...           TableItem(bins2, data2,
    ...                     headers=['col1', 'col2']),
    ...           PlotItem(bins=bins1, xname='x1',
    ...                    curves=[CurveElements(data11, 'd11', yname='y11')]),
    ...           PlotItem(bins=bins1, xname='x1',
    ...                    curves=[CurveElements(data12, 'd12', yname='y12')]),
    ...           PlotItem(bins=bins2, xname='x2',
    ...                    curves=[CurveElements(data2, 'd2', yname='y1')]),
    ...           PlotItem(bins=bins1, xname='x2',
    ...                    curves=[CurveElements(data12, 'd12', yname='y1')])]
    >>> conc_items = concatenate(litems)
    >>> print(len(conc_items))
    5
    >>> for item in conc_items:
    ...     print("{!r}".format(item))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['col1', 'col2']
    col1: [0 1 2 3 0 1 2 3 4]
    col2: [0.  1.  2.  3.  0.  0.5 1.  1.5 2. ]
    <BLANKLINE>
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['valA', 'valB']
    valA: [0 1 2 3]
    valB: [ 0 10 20 30]
    <BLANKLINE>
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3]
    xname: x1
    label:  d11
    yname:  y11
    values: [0 1 2 3]
    errors: None
    label:  d12
    yname:  y12
    values: [ 0 10 20 30]
    errors: None
    <BLANKLINE>
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3 4]
    xname: x2
    label:  d2
    yname:  y1
    values: [0.  0.5 1.  1.5 2. ]
    errors: None
    <BLANKLINE>
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3]
    xname: x2
    label:  d12
    yname:  y1
    values: [ 0 10 20 30]
    errors: None
    <BLANKLINE>

    As soon as tables have the same headers they can be concatenated. For the
    plots same bins and same name of x-axis are needed.
    '''
    nitems = [litems[0].copy()]
    for it1 in litems[1:]:
        added = False
        for it2 in nitems:
            if isinstance(it1, type(it2)):
                try:
                    it2 += it1
                except ValueError:
                    continue
                except TypeError:
                    continue
                added = True
                break
        if not added:
            nitems.append(it1.copy())
    return nitems
