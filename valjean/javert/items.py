'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.
'''

import numpy as np
# from .. import LOGGER


class TableItem:
    '''A container class that encapsulates all the necessary information to
    represent a table.

    Examples of use of mainly show in context of concatentation of
    :class:`TableItem`, obtained with the operators ``+=`` and ``+``.

    >>> import numpy as np
    >>> tit1 = TableItem(np.float_(1.5), np.float_(1.4),
    ...                  headers=['egg', 'spam'])
    >>> tit2 = TableItem(np.float_(1.2), np.float_(0.9),
    ...                  headers=['egg', 'spam'])
    >>> stab12 = join(tit1, tit2)
    >>> print(len(tit1.columns), len(tit2.columns))
    2 2
    >>> print(tit1.columns[0].size, tit2.columns[0].size)
    1 1
    >>> print(len(stab12.columns))
    2
    >>> print(stab12.columns[0].size)
    2
    >>> print("{!r}".format(stab12))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['egg', 'spam']
    egg: [1.5 1.2]
    spam: [1.4 0.9]
    <BLANKLINE>

    ``stab12`` contained both ``tit1`` and ``tit2`` as expected. Headers of the
    columns are the same, length of the columns is the sum of the two.

    >>> tit3 = TableItem(np.float_(0.8), np.float_(1.1),
    ...                  headers=['knight', 'parrot'])
    >>> stab13 = join(tit1, tit3)
    Traceback (most recent call last):
        ...
    ValueError: TableItems to add should have same headers

    An error is raised as the two :class:`TableItem` don't contain the same
    headers, so not the same kind of columns, thus they cannot be concatenated.

    >>> tit4 = TableItem(np.arange(4), np.arange(4)*0.5,
    ...                  headers=['egg', 'spam'])
    >>> print(len(tit4.columns), tit4.columns[0].size)
    2 4
    >>> stab14 = join(tit1, tit4)
    >>> print(len(stab14.columns), stab14.columns[0].size)
    2 5
    >>> stab14.columns[0].size == tit1.columns[0].size + tit4.columns[0].size
    True
    >>> print("{!r}".format(stab14))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3. ]
    spam: [1.4 0.  0.5 1.  1.5]
    <BLANKLINE>

    If the columns are the same format, concatenation of TableItems containing
    arrays and numbers is possible.

    It is also between arrays, a bigger array is obtained, without separation
    between the initial :class:`TableItem`:

    >>> tit5 = TableItem(np.arange(3)*0.1, np.arange(3)*0.05,
    ...                  headers=['egg', 'spam'])
    >>> stab45 = join(tit4, tit5)
    >>> print(len(stab45.columns), len(stab45.columns[0]))
    2 7
    >>> print("{!r}".format(stab45))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['egg', 'spam']
    egg: [0.  1.  2.  3.  0.  0.1 0.2]
    spam: [0.   0.5  1.   1.5  0.   0.05 0.1 ]
    <BLANKLINE>

    Any number of :class:`TableItem` can be joined (if fulfilling the
    requirements).

    >>> stab124 = join(tit1, tit2, tit4)
    >>> print("{!r}".format(stab124))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['egg', 'spam']
    egg: [1.5 1.2 0.  1.  2.  3. ]
    spam: [1.4 0.9 0.  0.5 1.  1.5]
    <BLANKLINE>

    The :meth:`join` method from in the :class:`TableItem` updates the left
    :class:`TableItem` as expected:

    >>> tit1.join(tit2, tit4)
    >>> print("{!r}".format(tit1))
    class: <class 'valjean.javert.items.TableItem'>
    headers: ['egg', 'spam']
    egg: [1.5 1.2 0.  1.  2.  3. ]
    spam: [1.4 0.9 0.  0.5 1.  1.5]
    <BLANKLINE>
    '''

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
        self.columns = columns
        n_columns = len(columns)
        self.headers = ['']*n_columns if headers is None else headers
        self.units = ['']*n_columns if units is None else units
        self.highlight = highlight

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

    def _binary_join(self, other):
        '''Join another :class:`TableItem` to the current one.

        This method **concatenates** :class:`TableItem` of the same number of
        columns and same headers. It returns an update of the left one.

        If the two :class:`TableItem` are not compatible an exception is
        raised.

        :param other: :class:`TableItem` to add to the current one
        :returns: updated :class:`TableItem`
        :raises TypeError: if the other parameter is not a :class:`TableItem`
        :raises ValueError: if the TableItems don't have the same headers.
        '''
        if not isinstance(other, TableItem):
            raise TypeError("Only a TableItem can be joined to another "
                            "TableItem")
        if self.headers != other.headers:
            raise ValueError("TableItems to add should have same headers")
        self.columns = tuple(
            self.columns[i] + other.columns[i]
            if isinstance(self.columns[i], list)
            else np.hstack((self.columns[i], other.columns[i]))
            for i in range(len(self.columns)))
        self.units = other.units if self.units is None else self.units

    def join(self, *others):
        '''Join a given number a :class:`TableItem` to the current one.

        Only :class:`TableItem` with the same number of columns and same
        headers can be joined. The method returns the updated current one.

        :param others: list of TableItems
        :type others: :class:`list` (:class:`TableItem`)
        :returns: updated :class:`TableItem`
        '''
        for oti in others:
            self._binary_join(oti)

    def __repr__(self):
        '''Print TableItem details.'''
        intro = ["class: {0}\n"
                 "headers: {1}\n".format(self.__class__, self.headers)]
        elts = []
        for icol, col in enumerate(self.columns):
            elts.append("{0}: {1}\n".format(self.headers[icol], col))
        return ''.join(intro + elts)


class CurveElements:
    '''Define the characteristics of a curve to plot.'''

    def __init__(self, values, label, *, yname='', errors=None):
        '''Construction of :class:`CurveElements`: curve details (values,
        label, etc).

        A major parameter is ``yname``, set by default to ``''``: this is the
        y-axis name. When representing the curve on the pyplot, the subplot is
        chosen according this ``yname``.

        The label is used in the legend.

        Values and errors (if given) should be :obj:`numpy.ndarray` of same
        shape.

        :param values: array to be represented on the plot, **mandatory**
        :type values: :obj:`numpy.ndarray`
        :param str label: label to be used in the legend to characterize the
            curve, **mandatory**
        :param str yname: label of y-axis (used to determine the number of
            subplots on the plot)
        :param errors: errors associated to values (per default only on y-axis)
        :type errors: :obj:`numpy.ndarray`
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

    Examples of use of mainly show in context of concatentation of
    :class:`PlotItem`, obtained with the operators ``+=`` and ``+``.

    >>> bins1, data11, data12 = np.arange(4), np.arange(4), np.arange(4)*10
    >>> data13 = data11 + data12
    >>> bins2, data2 = np.arange(5), np.arange(5)*0.5
    >>> pit1 = PlotItem(bins=bins1, xname='egg',
    ...                 curves=[CurveElements(data11, 'd11', yname='brandy')])
    >>> pit2 = PlotItem(bins=bins1, xname='egg',
    ...                 curves=[CurveElements(data12, 'd12', yname='beer')])
    >>> pit3 = PlotItem(bins=bins1, xname='egg',
    ...                 curves=[CurveElements(data13, 'd13', yname='beer')])

    >>> splt12 = join(pit1, pit2)
    >>> print("{!r}".format(splt12))
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3]
    xname: egg
    label:  d11
    yname:  brandy
    values: [0 1 2 3]
    errors: None
    label:  d12
    yname:  beer
    values: [ 0 10 20 30]
    errors: None
    <BLANKLINE>

    We obtain a new :class:`PlotItem` containing two curves with different
    ynames.

    >>> splt123 = join(pit1, pit2, pit3)
    >>> print("{!r}".format(splt123))
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3]
    xname: egg
    label:  d11
    yname:  brandy
    values: [0 1 2 3]
    errors: None
    label:  d12
    yname:  beer
    values: [ 0 10 20 30]
    errors: None
    label:  d13
    yname:  beer
    values: [ 0 11 22 33]
    errors: None
    <BLANKLINE>

    As expected a new :class:`TableItem` is obtained, containing three curves.
    The first and third ones have the same ynmes (can appear on the same
    subplot).

    Like in the TableItem case, the :meth:`join` method from in the
    :class:`PlotItem` updates the left :class:`PlotItem` as expected:

    >>> pit1.join(pit2, pit3)
    >>> print("{!r}".format(pit1))
    class: <class 'valjean.javert.items.PlotItem'>
    bins: [0 1 2 3]
    xname: egg
    label:  d11
    yname:  brandy
    values: [0 1 2 3]
    errors: None
    label:  d12
    yname:  beer
    values: [ 0 10 20 30]
    errors: None
    label:  d13
    yname:  beer
    values: [ 0 11 22 33]
    errors: None
    <BLANKLINE>

    >>> pit4 = PlotItem(bins=bins1, xname='spam',
    ...                 curves=[CurveElements(data12, 'd12', yname='bacon')])
    >>> splt14 = join(pit1, pit4)
    Traceback (most recent call last):
        ...
    ValueError: PlotItems should have the same xname to be joined

    An error is raised a the x-axis don't have the same name. In that case the
    :class:`PlotItem` cannot be concatenated. They will have to be represented
    on two different plots, even if the bins used (``bins1``) are the same
    (they probably don't have the same meaning).

    >>> pit5 = PlotItem(bins=bins2, xname='spam',
    ...                 curves=[CurveElements(data2, 'd2', yname='bacon')])
    >>> splt45 = join(pit4, pit5)
    Traceback (most recent call last):
        ...
    ValueError: Bins should be the same in both PlotItems

    An error is also raised: x-axis bins have the same names but not the same
    number of bins. The two :class:`PlotItem` cannot represent the same
    quantity so be represented on the same plot.
    '''

    def __init__(self, *, bins, curves, xname=''):
        '''Construction of the PlotItem from x-bins and curves.

        The curves should be a list of :class:`CurveElements`.

        The bins mean the x-axis bins. They should be common to all the curves.
        It is up to the user to ensure that (when coming from a unique test
        this should be automatic).

        :param bins: bins, common for all plots (important), only one set is
            needed
        :type bins: :obj:`numpy.ndarray`
        :param str xname: name of x-axis (default: ``''``)
        :param curves: list of curves characteristics
        :type curves: :class:`list` (:class:`CurveElements`)
        '''
        self.bins = bins
        self.xname = xname
        self.curves = curves

        if not isinstance(self.curves, list):
            raise TypeError("The 'curves' argument must a list of "
                            "CurveElements.")

        if not all(isinstance(curve, CurveElements) for curve in self.curves):
            raise TypeError("The 'curves' argument must a list of "
                            "CurveElements.")

    def copy(self):
        '''Copy a :class:`PlotItem` object.

        :returns: :class:`PlotItem`
        '''
        return PlotItem(bins=self.bins.copy(),
                        xname=self.xname,
                        curves=[pelt.copy() for pelt in self.curves])

    def _binary_join(self, other):
        '''Join another :class:`PlotItem` to the current one.

        This method **concatenates** the current :class:`PlotItem` to the
        ``other`` one, i.e., if they share the x-axis (bins and name), the
        curves list is extended.

        The curves are not added in the mathematical sense. If this is what you
        really want to do, please add the datasets themselves before and
        probably redo the test.

        :param other: :class:`PlotItem` to add to the current one
        :returns: updated :class:`PlotItem`
        :raises TypeError: if the other parameter is not a :class:`PlotItem`
        :raises ValueError: if x-axes are not the same (``xname`` and ``bins``)
        '''
        if not isinstance(other, PlotItem):
            raise TypeError("Only a PlotItem can be joined to another "
                            "PlotItem")
        if self.xname != other.xname:
            raise ValueError("PlotItems should have the same xname to be "
                             "joined")
        if not np.array_equal(self.bins, other.bins):
            raise ValueError("Bins should be the same in both PlotItems")
        self.curves.extend(other.curves)

    def join(self, *others):
        '''Join a given number a :class:`PlotItem` to the current one.

        Only :class:`PlotItem` with the same number of columns and same headers
        can be joined. The method returns the updated current one.

        :param others: list of PlotItems
        :type others: :class:`list` (:class:`PlotItem`)
        :returns: updated :class:`PlotItem`
        '''
        for oti in others:
            self._binary_join(oti)

    def __repr__(self):
        '''Printing of :class:`PlotItem`.'''
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


def join(*items):
    '''Join a "list" of items of same kind, :class:`TableItem` or
    :class:`PlotItem` using the related ``join`` methods.

    It returns a new items (:class:`TableItem` or :class:`PlotItem`).

    :param items: list of items
    :type items: :class:`list` (:class:`TableItem`)
        or :class:`list` (:class:`PlotItem`)
    :returns: :class:`TableItem` or :class:`PlotItem`


    See :class:`TableItem` and :class:`PlotItem` for examples of use. ONly few
    error cases will be shown here:

    >>> bins1, data11, data12 = np.arange(4), np.arange(4), np.arange(4)*10
    >>> bins2, data2 = np.arange(5), np.arange(5)*0.5
    >>> tablit = TableItem(bins1, data11, headers=['egg', 'spam'])
    >>> plotit = PlotItem(bins=bins1, xname='egg',
    ...                   curves=[CurveElements(data11, 'd11', yname='spam')])
    >>> tit = join(tablit, plotit)
    Traceback (most recent call last):
        ...
    TypeError: Only a TableItem can be joined to another TableItem
    >>> tit = join(plotit, tablit)
    Traceback (most recent call last):
        ...
    TypeError: Only a PlotItem can be joined to another PlotItem
    '''
    copy = items[0].copy()
    copy.join(*items[1:])
    return copy
