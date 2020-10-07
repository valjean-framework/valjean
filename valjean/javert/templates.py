# pylint: disable=too-many-lines
'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.

.. _numpy indexing: https://numpy.org/doc/stable/user/basics.indexing.html
'''
from hashlib import sha256
import numpy as np
from .. import LOGGER


class TableTemplate:
    '''A container class that encapsulates all the necessary information to
    represent a table.

    Examples of use of mainly show in context of concatentation of
    :class:`TableTemplate`, obtained with the :meth:`join` method.

    >>> import numpy as np
    >>> tit1 = TableTemplate(np.float_(1.5), np.float_(1.4),
    ...                      headers=['egg', 'spam'])
    >>> tit2 = TableTemplate(np.float_(1.2), np.float_(0.9),
    ...                      headers=['egg', 'spam'])
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
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 1.2]
    spam: [1.4 0.9]
    highlights: [array([0., 0.]), array([0., 0.])]

    ``stab12`` contained both ``tit1`` and ``tit2`` as expected. Headers of the
    columns are the same, length of the columns is the sum of the two.

    >>> tit3 = TableTemplate(np.float_(0.8), np.float_(1.1),
    ...                      headers=['knight', 'parrot'])
    >>> stab13 = join(tit1, tit3)
    Traceback (most recent call last):
        ...
    ValueError: TableTemplates to add should have same headers

    An error is raised as the two :class:`TableTemplate` don't contain the same
    headers, so not the same kind of columns, thus they cannot be concatenated.

    It is also possible to join tables with same headers but different 'types'
    (scalars and arrays):

    >>> tit4 = TableTemplate(np.arange(4), np.arange(4)*0.5,
    ...                      headers=['egg', 'spam'])
    >>> print(len(tit4.columns), tit4.columns[0].size)
    2 4
    >>> stab14 = join(tit1, tit4)
    >>> print(len(stab14.columns), stab14.columns[0].size)
    2 5
    >>> stab14.columns[0].size == tit1.columns[0].size + tit4.columns[0].size
    True
    >>> print("{!r}".format(stab14))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3. ]
    spam: [1.4 0.  0.5 1.  1.5]
    highlights: [array([0., 0., 0., 0., 0.]), array([0., 0., 0., 0., 0.])]


    It is also possible to join arrays, a bigger array is obtained, without
    separation between the initial :class:`TableTemplate`:

    >>> tit5 = TableTemplate(np.arange(3)*0.1, np.arange(3)*0.05,
    ...                      headers=['egg', 'spam'])
    >>> stab45 = join(tit4, tit5)
    >>> print(len(stab45.columns), len(stab45.columns[0]))
    2 7
    >>> print("{!r}".format(stab45))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [0.  1.  2.  3.  0.  0.1 0.2]
    spam: [0.   0.5  1.   1.5  0.   0.05 0.1 ]
    highlights: [array([0., 0., 0., 0., 0., 0., 0.]), \
array([0., 0., 0., 0., 0., 0., 0.])]

    Any number of :class:`TableTemplate` can be joined (if fulfilling the
    requirements).

    >>> stab145 = join(tit1, tit4, tit5)
    >>> print("{!r}".format(stab145))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3.  0.  0.1 0.2]
    spam: [1.4  0.   0.5  1.   1.5  0.   0.05 0.1 ]
    highlights: [array([0., 0., 0., 0., 0., 0., 0., 0.]), \
array([0., 0., 0., 0., 0., 0., 0., 0.])]

    The :meth:`TableTemplate.join` method updates the left
    :class:`TableTemplate` as expected:

    >>> tit1.join(tit4, tit5)
    >>> print("{!r}".format(tit1))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3.  0.  0.1 0.2]
    spam: [1.4  0.   0.5  1.   1.5  0.   0.05 0.1 ]
    highlights: [array([0., 0., 0., 0., 0., 0., 0., 0.]), \
array([0., 0., 0., 0., 0., 0., 0., 0.])]
    '''

    def __init__(self, *columns, headers=None, units=None,
                 highlights=None):
        '''Construct a table from a set of columns. The columns must be
        :class:`numpy.ndarray` objects, and they must all contain the same
        number of elements (same array *size*).

        Column headers may be specified using the `headers` argument; in this
        case, the number of headers must be equal to the number of columns.

        Column units can also be specified using the `units` argument. Again,
        you must pass as many units as there are columns.

        Finally, it is possible to specify which table elements should be
        highlighted. This is done by passing a list of lists (or
        :class:`numpy.ndarray`) to the `highlights` argument. Each element of
        the `highlights` (outer) list represents a table column and therefore
        must have the same shape as all the other columns; also, the length of
        `highlights` must be equal to the number of columns. Elements of the
        inner lists (or :class:`numpy.ndarray`) must be booleans and indicate
        whether the corresponding table element must be highlighted.

        :param columns: a list of columns.
        :type columns: list(numpy.ndarray)
        :param list(str) headers: a list of headers.
        :param list(str) units: a list of measurement units.
        :param highlights: a list describing which table elements should be
            highlighted.
        :type highlights: list(list(bool)) or list(numpy.ndarray(bool))
        '''
        self.columns = columns
        n_columns = len(columns)
        self.headers = ['']*n_columns if headers is None else headers
        self.units = ['']*n_columns if units is None else units

        if not columns:
            raise ValueError('at least one column expected')

        if highlights is None:
            self.highlights = [np.full_like(self.columns[0], False)
                               for _ in self.columns]
        else:
            self.highlights = highlights

        if len(self.headers) != len(self.columns):
            err = ('number of column headers ({}) must match number of '
                   'columns ({})'.format(len(self.headers), len(self.columns)))
            raise ValueError(err)

        if len(self.units) != len(self.columns):
            err = ('number of column units ({}) must match number of '
                   'columns ({})'.format(len(self.units), len(self.columns)))
            raise ValueError(err)

        if not isinstance(self.highlights, list):
            raise TypeError('expected a list as the `highlights` argument, '
                            'got a {} instead'.format(type(self.highlights)))
        if len(self.highlights) != len(self.columns):
            raise ValueError('expected a list of {} elements as the '
                             '`highlights` argument, got {} elements instead'
                             .format(len(self.columns), len(self.highlights)))

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
        '''Copy a :class:`TableTemplate` object.

        :rtype: TableTemplate

        .. note:: the highlignt function is not really copied, it has the same
            address as the self one. I don't know how to change that.
        '''
        return TableTemplate(*tuple(col.copy() for col in self.columns),
                             headers=self.headers.copy(),
                             units=self.units.copy(),
                             highlights=self.highlights.copy())

    def _binary_join(self, other):
        '''Join another :class:`TableTemplate` to the current one.

        This method **concatenates** :class:`TableTemplate` of the same number
        of columns and same headers. It returns an update of the left one.

        If the two :class:`TableTemplate` are not compatible an exception is
        raised.

        :param other: :class:`TableTemplate` to be added to the current one
        :raises TypeError: if the other parameter is not a
            :class:`TableTemplate`
        :raises ValueError: if the TableTemplates don't have the same headers.
        '''
        if not isinstance(other, TableTemplate):
            raise TypeError("Only a TableTemplate can be joined to another "
                            "TableTemplate")
        if self.headers != other.headers:
            raise ValueError("TableTemplates to add should have same headers")
        self.columns = tuple(np.hstack((self.columns[i], other.columns[i]))
                             for i in range(len(self.columns)))
        self.units = other.units if self.units is None else self.units
        self.highlights = list(np.hstack((
            [np.atleast_1d(h) for h in self.highlights],
            [np.atleast_1d(h) for h in other.highlights])))

    def join(self, *others):
        '''Join a given number a :class:`TableTemplate` to the current one.

        Only :class:`TableTemplate` with the same number of columns and same
        headers can be joined. The method returns the updated current one.

        :param others: list of TableTemplates to be joined to the current
            TableTemplate
        :type others: list(TableTemplate)
        '''
        for oti in others:
            self._binary_join(oti)

    def __repr__(self):
        '''Print TableTemplate details.'''
        intro = ["class: {0}\n"
                 "headers: {1}\n".format(self.__class__, self.headers)]
        elts = []
        for header, col in zip(self.headers, self.columns):
            elts.append("{0}: {1}\n".format(header, col))
        hlight = ['highlights: {}'.format(self.highlights)]
        return ''.join(intro + elts + hlight)

    def __getitem__(self, index):
        '''Build a sliced :class:`TableTemplate` from the current
        :class:`TableTemplate`.

        Slicing is done like in the usual `NumPy` arrays, see:
        `numpy indexing`_ for more informations. No treatment like in
        :mod:`~valjean.eponine.dataset` is done.

        :param index: index, slice or tuple of slices
        :type index: int, slice, tuple(slice)
        :rtype: TableTemplate
        '''
        LOGGER.debug("In TableTemplate.__getitem__")
        if not isinstance(self.columns[0], np.ndarray):
            raise TypeError("Slicing is only possible when the values if the "
                            "TableTemplate is np.ndarray.")
        return TableTemplate(*tuple(col[index] for col in self.columns),
                             headers=self.headers.copy(),
                             units=self.units.copy(),
                             highlights=self.highlights.copy())

    def fingerprint(self):
        '''Compute a fingerprint (a SHA256 hash) for `self`. The fingerprint
        depends only on the content of `self`. Two :class:`TableTemplate`
        objects containing equal data have the same fingerprint. The converse
        is not true, but very likely.'''
        hasher = sha256()
        for col, head, unit, high in zip(self.columns, self.headers,
                                         self.units, self.highlights):
            hasher.update(np.require(col, requirements='C').data.cast('b'))
            hasher.update(head.encode('utf-8'))
            hasher.update(unit.encode('utf-8'))
            hasher.update(high.data.cast('b'))
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`TableTemplate`.'''
        return (len(self.columns) == len(other.columns)
                and all(np.array_equal(this, that)
                        for this, that in zip(self.columns, other.columns))
                and self.headers == other.headers
                and self.units == other.units
                and self.highlights == other.highlights)

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`TableTemplate`.'''
        return not self == other


class CurveElements:
    '''Define the characteristics of a curve to plot.'''

    def __init__(self, values, bins, legend, *, index=0, errors=None):
        '''Construction of :class:`CurveElements`: curve details (values, bins,
        etc).

        Values and errors (if given) should be :obj:`numpy.ndarray` of same
        shape (they must have only non-trivial dimension).

        Bins are stored as a list of :obj:`numpy.ndarray`. This list should
        have the same length as the dimension of the values.

        The index is used to share the plotting style between curves that
        should. For example, if on a plot there are the reference and two
        curves representing different data, let's say 'egg' and 'spam', if we
        also want to draw the ratio of these data with the reference, the same
        style will be applied to 'egg vs reference' and 'egg' and to 'spam vs
        reference' and 'spam'. In that case to ensure the same style 'egg vs
        reference' and 'egg' should have the same index (same for the 'spam'
        case).

        :param numpy.ndarray values: array to be represented on the plot,
            **mandatory**
        :param list(numpy.ndarray) bins: bins to be used to represent the
            values
        :param str legend: string to be used in the legend to characterize the
            curve, **mandatory**
        :param int index: index of the curve (used for style for example)
        :param numpy.ndarray errors: errors associated to values (per default
            only on 1D plots and y-axis)
        '''
        self.values = values
        self.bins = bins
        self.legend = legend
        self.index = index
        self.errors = errors

        if not isinstance(self.values, np.ndarray):
            raise TypeError('Values should be np.ndarray.')

        if not len(bins) == self.values.ndim:
            raise ValueError('len(bins) should be equal to values dimension')

        if self.errors is not None:
            if not isinstance(self.errors, np.ndarray):
                raise TypeError('Errors should be np.ndarray or None')

    def copy(self):
        '''Copy a :class:`CurveElements` object.

        :rtype: CurveElements
        '''
        return CurveElements(values=self.values.copy(),
                             legend=self.legend,
                             bins=[b.copy() for b in self.bins],
                             index=self.index,
                             errors=(None if self.errors is None
                                     else self.errors.copy()))

    def __repr__(self):
        '''Printing of :class:`CurveElements`.'''
        elts = ("  legend:  {}\n"
                "  index:   {}\n"
                "  bins:    {}\n"
                "  values:  {}\n"
                "  errors:  {}\n".format(
                    self.legend, self.index, self.bins, self.values,
                    self.errors))
        return elts

    def __str__(self):
        '''Printing of :class:`CurveElements`.'''
        elts = ("  legend:  {}\n"
                "  index:   {}\n"
                "  bins:    {}\n".format(self.legend, self.index, self.bins))
        return elts

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield np.require(self.values, requirements='C').data.cast('b')
        yield self.legend.encode('utf-8')
        for bins in self.bins:
            yield np.require(bins, requirements='C').data.cast('b')
        yield bytes((self.index,))
        if self.errors is not None:
            yield np.require(self.errors, requirements='C').data.cast('b')

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`CurveElements`.'''
        return (np.array_equal(self.values, other.values)
                and self.legend == other.legend
                and np.array_equal(self.bins, other.bins)
                and self.index == other.index
                and np.array_equal(self.errors, other.errors))

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`CurveElements`.'''
        return not self == other


class SubPlotAttributes:
    # pylint: disable=too-many-instance-attributes
    '''Container to store sub-plots attributes:

    * axis limits
    * axis scale: linear (default) or logatithmic
    * additional horizontal or vertical lines

    Theses attributes are independent of the used backend (examples:
    **matplotlib**, **Root**, **gnuplot**, **D3**). The backend then gets the
    attributes and apply them with its own features.

    .. note:

        If needed new attributes can be added.
    '''
    def __init__(self, dim):
        '''Initialisation of PlotAttributes.

        The attributes of the instance are private.

        :param int dim: dimension of the data on the sub-plot (used to check
            consistency of limits)
        '''
        self.dim = dim
        self.logx = False
        self.logy = False
        self.logz = False
        self._limits = None
        self._lines = None

    def copy(self):
        '''Copy a :class:`SubPlotAttributes` object.

        :rtype: SubPlotAttributes
        '''
        spa = SubPlotAttributes(self.dim)
        spa.logx = self.logx
        spa.logy = self.logy
        spa.logz = self.logz
        spa.limits = self.limits.copy() if self.limits is not None else None
        spa.lines = self.lines.copy() if self.lines is not None else None
        return spa

    @property
    def limits(self):
        '''Return limits.'''
        return self._limits

    @limits.setter
    def limits(self, limits):
        '''Store limits for curves in the :class:`PlotTemplate`.

        :param list(tuple) limits: limits for each axis of the sub-plot

        Each tuple corresponds to an axis, 2 values are expected: min and max.
        '''
        if limits is not None:
            if len(limits) != self.dim:
                LOGGER.warning('Wrong number of limits given: expected %s, '
                               'got %s', self.dim, len(limits))
                return
        self._limits = limits

    @property
    def lines(self):
        '''Return lines to be plotted.'''
        return self._lines

    @lines.setter
    def lines(self, lines):
        '''Set lines to be added to the plots.

        :param list(list(dict)) lines: lines to be added to the plots
        '''
        if lines is None:
            self._lines = None
            return
        for line in lines:
            if len({'x', 'y'}.intersection(line)) != 1:
                LOGGER.warning('Only vertical or horizontal lines accepted')
                return
        self._lines = lines


class SubPlotElementsException(Exception):
    '''Error raised if the sub plot looks inconsistent.'''


class SubPlotElements:
    '''Container to store a given sub-plot.'''

    def __init__(self, *, curves, axnames=('', ''), ptype='1D'):
        '''Initialisation of :class:`SubPlotElements`.

        A subplot is defined as data (``curves``) sharing the same plotting
        properties:

        * axis names
        * type of the plot (e.g. ``'1D'``, ``'2D'``, ...), see the chosen
          backend to get the list of possibilities (example:
          :class:`~.mpl.MplPlot`)
        * axis scales
        * axis limits

        The last axis name corresponds to the quantity to be drawn, the first
        ones to the bins.

        Axis scales can be linear (default) or logarithmic (if set to
        ``True``).

        Vertical or horizontal lines can also be added.

        :param list(CurveElements) curves: list of curves to go on the sub-plot
        :param tuple axnames: name of the axes of the sub-plot
        :param str type: type of the sub-plot, default: ``'1D'``
        '''
        self.curves = curves
        self.axnames = list(axnames)
        self.ptype = ptype
        self._check_axes_consistency()
        self.attributes = SubPlotAttributes(len(self.axnames)-1)

    def _check_axes_consistency(self):
        '''Check axes consistency.

        Expected:

        * number of axis names = dimension of the curve + 1
        * if 1D: 2 axis names, if 2D: 3 axis names
        '''
        for crv in self.curves[1:]:
            if len(crv.bins) != len(self.curves[0].bins):
                raise SubPlotElementsException(
                    'Not the same number of axes in the curves')
        if len(self.axnames) != len(self.curves[0].bins)+1:
            raise SubPlotElementsException(
                'Inconsistent number of axis names and bins')
        if self.ptype == '1D' and len(self.axnames) != 2:
            raise SubPlotElementsException(
                'Expecting a 1D plot but got {} axes'
                .format(len(self.axnames)))
        if self.ptype == '2D' and len(self.axnames) != 3:
            raise SubPlotElementsException(
                'Expecting a 2D plot but got {} axes'
                .format(len(self.axnames)))
        if self.ptype == '2D' and len(self.curves) > 1:
            LOGGER.warning('Only one subplot expected by SubPlotElements in '
                           '2D case')

    def copy(self):
        '''Copy a :class:`SubPlotElements` object.

        :rtype: SubPlotElements
        '''
        celt = SubPlotElements(curves=[c.copy() for c in self.curves],
                               axnames=list(self.axnames),
                               ptype=self.ptype,)
        celt.attributes = self.attributes.copy()
        return celt

    def __repr__(self):
        '''Printing of :class:`SubPlotElements`'''
        elts = [" axnames: {}, plot type: {}, N curves: {}\n"
                .format(self.axnames, self.ptype, len(self.curves))]
        for j, curve in enumerate(self.curves):
            elts.append(" Curve {}\n{!r}".format(j, curve))
        return ''.join(elts)

    def __str__(self):
        '''Printing of :class:`SubPlotElements`'''
        elts = [" axnames: {}, plot type: {}\n"
                .format(self.axnames, self.ptype)]
        for j, curve in enumerate(self.curves):
            elts.append(" Curve {}\n{!s}".format(j, curve))
        return ''.join(elts)

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        for aname in self.axnames:
            yield aname.encode('utf-8')
        yield self.ptype.encode('utf-8')
        for curve in self.curves:
            for data in curve.data():
                yield data

    def __eq__(self, other):
        '''Test of equality of `self` and another :class:`SubPlotElements`.'''
        return (all(s == o for s, o in zip(self.curves, other.curves))
                and self.axnames == other.axnames
                and self.ptype == other.ptype)

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`SubPlotElements`.
        '''
        return not self == other


class PlotTemplate:
    '''A container for full test result to be represented as a plot. This
    includes all the datasets and the test result. This can also include
    p-values or other test parameters, depending on what is given to the
    :class:`PlotTemplate`.

    Examples mainly present the :meth:`join` method, used to concatentate
    :class:`PlotTemplate`.

    >>> bins1, d11, d12 = np.arange(4), np.arange(4), np.arange(4)*10
    >>> d13 = d11 + d12
    >>> bins2, d2 = np.arange(5), np.arange(5)*0.5
    >>> pit1 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d11, [bins1], 'd11', index=0)],
    ...     axnames=['egg', 'brandy'])])
    >>> pit2 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d12, bins=[bins1], legend='d12', index=1)],
    ...     axnames=['egg', 'beer'])])
    >>> pit3 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d13, legend='d13', bins=[bins1], index=2)],
    ...     axnames=['egg', 'wine'])])
    >>> splt123 = join(pit1, pit2, pit3)
    >>> print("{!r}".format(splt123))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    N subplots: 3
    Subplot 0
     axnames: ['egg', 'brandy'], plot type: 1D, N curves: 1
     Curve 0
      legend:  d11
      index:   0
      bins:    [array([0, 1, 2, 3])]
      values:  [0 1 2 3]
      errors:  None
    Subplot 1
     axnames: ['egg', 'beer'], plot type: 1D, N curves: 1
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
      values:  [ 0 10 20 30]
      errors:  None
    Subplot 2
     axnames: ['egg', 'wine'], plot type: 1D, N curves: 1
     Curve 0
      legend:  d13
      index:   2
      bins:    [array([0, 1, 2, 3])]
      values:  [ 0 11 22 33]
      errors:  None
    <BLANKLINE>

    As expected a new :class:`PlotTemplate` is obtained, containing three
    subplots, each one containing one curve.

    Like in the TableTemplate case, the :meth:`PlotTemplate.join` method
    updates the left :class:`PlotTemplate` as expected:

    >>> pit1.join(pit2, pit3)
    >>> pit1 == splt123
    True

    A new curve with the same axes will also create a new suplot:

    >>> d14 = d11*2
    >>> pit4 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d14, legend='d14', index=3, bins=[bins1])],
    ...     axnames=['egg', 'beer'])])
    >>> split24 = join(pit2, pit4)
    >>> print(split24)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
    Subplot 1
     axnames: ['egg', 'beer'], plot type: 1D
     Curve 0
      legend:  d14
      index:   3
      bins:    [array([0, 1, 2, 3])]
    <BLANKLINE>


    To get it in the same subplot it has to be done at creation.

    >>> pit24 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d12, legend='d12', index=1, bins=[bins1]),
    ...             CurveElements(d14, legend='d14', index=3, bins=[bins1])],
    ...     axnames=['egg', 'beer'])])
    >>> print(pit24)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
     Curve 1
      legend:  d14
      index:   3
      bins:    [array([0, 1, 2, 3])]
    <BLANKLINE>
    >>> split24 == pit24
    False


    N-dimensional plot templates can be built, but the plotting engine may not
    be able to convert multi-dimensional templates into plots.

    The same behavior is expected for multi-dimensions plots: ``join`` will had
    a new subplot. To be noted: only one curve can be plotted on a subplot in
    multi-dimensional case, so any additional curve will throw a warning. Plot
    representation may not be as expected.

    >>> d31 = np.arange(bins1.size*bins2.size).reshape(bins1.size, bins2.size)
    >>> d32 = np.arange(bins1.size*bins2.size).reshape(
    ...     bins1.size, bins2.size)*0.01
    >>> pit7 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d31, bins=[bins1, bins2],
    ...                           legend='d31', index=0)],
    ...     axnames=['egg', 'spam', 'bacon'], ptype='2D')])
    >>> pit8 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d32, bins=[bins1, bins2],
    ...                           legend='d32', index=1)],
    ...     axnames=['egg', 'spam', 'lobster'], ptype='2D')])
    >>> splt78 = join(pit7, pit8)
    >>> print("{!s}".format(splt78))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'spam', 'bacon'], plot type: 2D
     Curve 0
      legend:  d31
      index:   0
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    Subplot 1
     axnames: ['egg', 'spam', 'lobster'], plot type: 2D
     Curve 0
      legend:  d32
      index:   1
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    <BLANKLINE>

    It is also possible to mix 1D and 2D plots:

    >>> splt27 = join(pit2, pit7)
    >>> print("{!s}".format(splt27))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
    Subplot 1
     axnames: ['egg', 'spam', 'bacon'], plot type: 2D
     Curve 0
      legend:  d31
      index:   0
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    <BLANKLINE>

    '''
    def __init__(self, *, subplots, small_subplots=True, suppress_xaxes=False,
                 suppress_legends=False):
        '''Construction of the PlotTemplate from a list of
        :class:`SubPlotElements`.

        :param list(SubPlotElements) subplots: list of sub-plots
        :param bool small_subplots: draw additional subplots in smaller size
            than the first one, default = ``True``
        :param bool suppress_xaxes: suppress label and ticks labels of the
            x-axis of subplots except the last one, default = ``False``
        :param bool suppress_legends: suppress legend on all subplots except
            the first one, default = ``False``
        '''
        self.subplots = subplots
        self.nb_plots = len(self.subplots)
        self.small_subplots = small_subplots
        self.suppress_xaxes = suppress_xaxes
        self.suppress_legends = suppress_legends

        if not isinstance(self.subplots, list):
            raise TypeError("The 'subplots' argument must a list of "
                            "SubPlotElements.")

        if not all(isinstance(spl, SubPlotElements) for spl in self.subplots):
            raise TypeError("The 'subplots' argument must a list of "
                            "SubPlotElements.")

    def copy(self):
        '''Copy a :class:`PlotTemplate` object.

        :rtype: PlotTemplate
        '''
        ccplt = PlotTemplate(subplots=[pelt.copy() for pelt in self.subplots],
                             small_subplots=self.small_subplots,
                             suppress_xaxes=self.suppress_xaxes,
                             suppress_legends=self.suppress_legends)
        return ccplt

    def _binary_join(self, other):
        '''Join another :class:`PlotTemplate` to the current one.

        This method **concatenates** the current :class:`PlotTemplate` to the
        ``other`` one, i.e., if they share the axes (bins and name), the curves
        list is extended.

        The curves are not added in the mathematical sense. If this is what you
        really want to do, please add the datasets themselves before and
        probably redo the test.

        :param other: PlotTemplate to be added to the current one
        :type other: PlotTemplate
        :raises TypeError: if the other parameter is not a
            :class:`PlotTemplate`
        :raises ValueError: if axes are not the same (``axname`s` and ``bins``)
        '''
        if not isinstance(other, PlotTemplate):
            raise TypeError("Only a PlotTemplate can be joined to another "
                            "PlotTemplate")
        self.subplots.extend(other.subplots)
        self.nb_plots = len(self.subplots)
        if other.small_subplots != self.small_subplots:
            LOGGER.warning('Not same value for small_subplots in self and '
                           'other, keeping self one (%s)', self.small_subplots)
        if other.suppress_xaxes != self.suppress_xaxes:
            LOGGER.warning('Not same value for suppress_xaxes in self and '
                           'other, keeping self one (%s)', self.suppress_xaxes)
        if other.suppress_legends != self.suppress_legends:
            LOGGER.warning('Not same value for suppress_legends in self and '
                           'other, keeping self one (%s)',
                           self.suppress_legends)

    def join(self, *others):
        '''Join a given number a :class:`PlotTemplate` to the current one.

        Only :class:`PlotTemplate` with the same number of columns and same
        headers can be joined. The method returns the updated current one.

        :param others: list of PlotTemplates to be join with the current
            PlotTemplate
        :type others: list(PlotTemplate)
        '''
        for oti in others:
            self._binary_join(oti)

    def __repr__(self):
        '''Printing of :class:`PlotTemplate`.'''
        intro = ["class:   {}\n"
                 "N subplots: {}\n".format(self.__class__, self.nb_plots)]
        elts = []
        for i, splt in enumerate(self.subplots):
            elts.append("Subplot {}\n{!r}".format(i, splt))
        return ''.join(intro + elts)

    def __str__(self):
        '''Printing of :class:`PlotTemplate`.'''
        intro = ["class:   {0}\n".format(self.__class__)]
        elts = []
        for i, splt in enumerate(self.subplots):
            elts.append("Subplot {}\n{!s}".format(i, splt))
        return ''.join(intro + elts)

    def fingerprint(self):
        '''Compute a fingerprint (a SHA256 hash) for `self`. The fingerprint
        depends only on the content of `self`. Two :class:`PlotTemplate`
        objects containing equal data have the same fingerprint. The converse
        is not true, but very likely.'''
        hasher = sha256()
        for splt in self.subplots:
            for data in splt.data():
                hasher.update(data)
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`PlotTemplate`.'''
        return self.subplots == other.subplots

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`PlotTemplate`.'''
        return not self == other

    def curves_index(self):
        '''Return a sorted list of unique index of the curves.'''
        lind = []
        for splt in self.subplots:
            for crv in splt.curves:
                if crv.index not in lind:
                    lind.append(crv.index)
        return lind


class TextTemplate:
    '''A container class that encapsulates text for the report.

    The user has to write the text as a string. ReST markdown can be used as
    compilation is expected to be done by sphinx.

    .. note::

        Titles might not be well represented in a ReSt formatted TextTemplate:
        no knowledge of the current level of title, nor the associated symbol.
        Lists or enumerations might be more suitable.

    As in the other templates, examples will focus on the concatenation (join)
    of different TextTemplate.

    >>> ttplt1 = TextTemplate('Spam egg bacon')
    >>> print("{!r}".format(ttplt1))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg bacon')
    >>> ttplt2 = TextTemplate('**Spam** egg bacon')
    >>> print("{!r}".format(ttplt2))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='**Spam** egg bacon')
    >>> ttplt3 = TextTemplate(r".. role:: hl\\n\\nsausage :hl:`tomato`")
    >>> ttplt1.join(ttplt3)
    >>> print("{!r}".format(ttplt1))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg bacon.. role:: hl\\\\n\\\\nsausage :hl:`tomato`')

    The sphinx compilation will fail there, as the are no empty line between
    the first and the second string. If you know some text will follow, think
    about the ``\\n``.

    >>> ttplt1 = TextTemplate('Spam egg bacon\\n\\n')
    >>> ttplt3 = TextTemplate('.. role:: hl\\n\\nsausage :hl:`tomato`\\n\\n')
    >>> ttplt1.join(ttplt3)
    >>> print("{!r}".format(ttplt1))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg bacon\\n\\n.. role:: hl\\n\\nsausage :hl:`tomato`\\n\\n')

    Test of the external function :meth:`join`:

    >>> ttplt4 = join(ttplt3, ttplt3)
    >>> print("{!r}".format(ttplt4))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='.. role:: hl\\n\\nsausage :hl:`tomato`\\n\\n\
.. role:: hl\\n\\nsausage :hl:`tomato`\\n\\n')

    The copy doesn't affect the original:

    >>> ttplt5 = ttplt2.copy()
    >>> ttplt5.text += ' sausage'
    >>> print("{!r}".format(ttplt2))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='**Spam** egg bacon')
    >>> print("{!r}".format(ttplt5))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='**Spam** egg bacon sausage')
    '''

    def __init__(self, text):
        '''Construct the text to be sent to the report.

        :param str text: text to be written in the report
        '''
        self.text = text

    def __repr__(self):
        '''Print :class:`TextTemplate` details.'''
        return '{}(text={!r})'.format(self.__class__, self.text)

    def _binary_join(self, other):
        self.text += other.text

    def copy(self):
        '''Copy a :class:`TextTemplate` object.

        :rtype: TextTemplate
        '''
        return TextTemplate(text=self.text)

    def join(self, *others):
        '''Join a given number of :class:`TextTemplate` to the current one.'''
        for oti in others:
            self._binary_join(oti)

    def fingerprint(self):
        '''Compute a fingerprint (a SHA256 hash) for `self`. The fingerprint
        depends only on the content of `self`. Two :class:`TextTemplate`
        objects containing equal data have the same fingerprint. The converse
        is not true, but very likely.'''
        hasher = sha256()
        hasher.update(self.text.encode('utf-8'))
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`TextTemplate`.'''
        return self.text == other.text

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`TextTemplate`.
        '''
        return not self == other


def join(*templates):
    '''Join a "list" of templates of same kind, :class:`TableTemplate` or
    :class:`PlotTemplate` using the related ``join`` methods.

    It returns a new templates (:class:`TableTemplate` or
    :class:`PlotTemplate`).

    :param templates: list of templates
    :type templates: list(TableTemplate) or list(PlotTemplate)
    :rtype: TableTemplate, PlotTemplate, TextTemplate


    See :class:`TableTemplate` and :class:`PlotTemplate` for examples of use.
    Only few error cases will be shown here:

    >>> bins1, data11, data12 = np.arange(4), np.arange(4), np.arange(4)*10
    >>> bins2, data2 = np.arange(5), np.arange(5)*0.5
    >>> tablit = TableTemplate(bins1, data11, headers=['egg', 'spam'])
    >>> plotit = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(data11, bins=[bins1], legend='d11')],
    ...     axnames=['egg', 'spam'])])
    >>> tit = join(tablit, plotit)
    Traceback (most recent call last):
        ...
    TypeError: Only a TableTemplate can be joined to another TableTemplate
    >>> tit = join(plotit, tablit)
    Traceback (most recent call last):
        ...
    TypeError: Only a PlotTemplate can be joined to another PlotTemplate
    '''
    copy = templates[0].copy()
    copy.join(*templates[1:])
    return copy
