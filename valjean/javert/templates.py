'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.

.. _numpy indexing:
   https://docs.scipy.org/doc/numpy/user/basics.indexing.html
'''
from collections import defaultdict
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
    <BLANKLINE>

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

    >>> tit4 = TableTemplate(np.arange(4), np.arange(4)*0.5,
    ...                      headers=['egg', 'spam'])
    >>> print(len(tit4.columns), tit4.columns[0].size)
    2 4
    >>> stab14 = join(tit1, tit4)
    Traceback (most recent call last):
        ...
    ValueError: all the input arrays must have same number of dimensions, \
but the array at index 0 has 1 dimension(s) \
and the array at index 1 has 2 dimension(s)

    It is still possible to join these tables if *tit1* columns are declared as
    arrays:

    >>> tit1b = TableTemplate(np.array([1.5]), np.array([1.4]),
    ...                       headers=['egg', 'spam'])
    >>> stab14 = join(tit1b, tit4)
    >>> print(len(stab14.columns), stab14.columns[0].size)
    2 5
    >>> stab14.columns[0].size == tit1b.columns[0].size + tit4.columns[0].size
    True
    >>> print("{!r}".format(stab14))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3. ]
    spam: [1.4 0.  0.5 1.  1.5]
    <BLANKLINE>

    If the columns are the same format, concatenation of TableTemplates
    containing arrays and numbers is possible.

    It is also between arrays, a bigger array is obtained, without separation
    between the initial :class:`TableTemplate`:

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
    <BLANKLINE>

    Any number of :class:`TableTemplate` can be joined (if fulfilling the
    requirements).

    >>> stab145 = join(tit1b, tit4, tit5)
    >>> print("{!r}".format(stab145))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3.  0.  0.1 0.2]
    spam: [1.4  0.   0.5  1.   1.5  0.   0.05 0.1 ]
    <BLANKLINE>

    The :meth:`TableTemplate.join` method updates the left
    :class:`TableTemplate` as expected:

    >>> tit1b.join(tit4, tit5)
    >>> print("{!r}".format(tit1b))
    class: <class 'valjean.javert.templates.TableTemplate'>
    headers: ['egg', 'spam']
    egg: [1.5 0.  1.  2.  3.  0.  0.1 0.2]
    spam: [1.4  0.   0.5  1.   1.5  0.   0.05 0.1 ]
    <BLANKLINE>
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
        self.highlights = list(np.hstack((self.highlights, other.highlights)))

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
        return ''.join(intro + elts)

    def __getitem__(self, index):
        '''Build a sliced :class:`TableTemplate` from the current
        :class:`TableTemplate`.

        Slicing is done like in the usual `NumPy` arrays, see:
        `numpy indexing`_ for more informations. No treatment like in
        :mod:`~valjean.gavroche.dataset` is done.

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
        case). ``index=0`` will always be considered as reference.

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


class SubPlotElementsException(Exception):
    '''Error raised if the sub plot looks inconsistent.'''


class SubPlotElements:
    # pylint: disable=too-many-instance-attributes
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
        self.axnames = axnames
        self.ptype = ptype
        self._check_axes_consistency()
        self.logx = False
        self.logy = False
        self.logz = False
        self._limits = None
        self._lines = None

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
            LOGGER.warning('Expecting a 1D plot but got %d axes',
                           len(self.axnames))
        if self.ptype == '2D' and len(self.axnames) != 3:
            LOGGER.warning('Expecting a 1D plot but got %d axes',
                           len(self.axnames))

    def consistent(self, other):
        '''Check if 2 :class:`SubPlotElements` are consistent.

        Check bins of the curves, axnames and plot type (``ptype``).

        :rtype: bool
        '''
        if other.axnames != self.axnames:
            return False
        if other.ptype != self.ptype:
            return False
        # should normally never happened due to _check_axes_consistency, keep?
        if len(other.curves[0].bins) != len(self.curves[0].bins):
            return False
        ind = [c.index for c in self.curves] + [c.index for c in other.curves]
        if len(set(ind)) != len(ind):
            LOGGER.warning('Some indices are them same in self and other, '
                           'might generate a representation issue.')
        return True

    def copy(self):
        '''Copy a :class:`SubPlotElements` object.

        :rtype: SubPlotElements
        '''
        celt = SubPlotElements(curves=[c.copy() for c in self.curves],
                               axnames=list(self.axnames).copy(),
                               ptype=self.ptype)
        celt.limits = self.limits
        celt.logx = self.logx
        celt.logy = self.logy
        celt.logz = self.logz
        celt.lines = self.lines
        return celt

    def __eq__(self, other):
        '''Test of equality of `self` and another :class:`SubPlotElements`.'''
        return (all(s == o for s, o in zip(self.curves, other.curves))
                and self.axnames == other.axnames
                and self.ptype == other.ptype)

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`SubPlotElements`.
        '''
        return not self == other

    @property
    def limits(self):
        '''Return limits.'''
        return self._limits

    @limits.setter
    def limits(self, limits):
        '''Store limits for curves in the :class:`PlotTemplate`.

        :param list(tuple) limits: limits for each axis of the plots

        List must contain a list whose items corresponds to a plot, this list
        must contain a tuple whose items correspond to the axes.
        '''
        if limits is not None:
            if len(limits) != len(self.axnames)-1:
                LOGGER.warning('Inconsistent limits given')
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
            if (line is not None
                    and not all(len({'x', 'y'}.intersection(li)) == 1
                                for li in line)):
                LOGGER.warning('Only vertical or horizontal lines accepted')
                return
        self._lines = lines


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
    >>> splt12 = join(pit1, pit2)
    >>> print("{!r}".format(splt12))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    N subplots: 2, N curves: 2
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
    <BLANKLINE>

    We obtain a new :class:`PlotTemplate` containing two different subplots.

    >>> splt123 = join(pit1, pit2, pit3)
    >>> print("{!r}".format(splt123))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    N subplots: 3, N curves: 3
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

    It is possible to join a new curve with the same axes. In that
    case they are added directly in the :class:`CurveElements` list.

    >>> d14 = d11*2
    >>> pit4 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d14, legend='d14', index=3, bins=[bins1])],
    ...     axnames=['egg', 'beer'])])
    >>> split24 = join(pit2, pit4)
    >>> print(split24)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D, N curves: 2
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
     Curve 1
      legend:  d14
      index:   3
      bins:    [array([0, 1, 2, 3])]
    <BLANKLINE>


    We get the same result as if it was done at creation:

    >>> pit24 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d12, legend='d12', index=1, bins=[bins1]),
    ...             CurveElements(d14, legend='d14', index=3, bins=[bins1])],
    ...     axnames=['egg', 'beer'])])
    >>> print(pit24)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D, N curves: 2
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
    True

    Warning: if axnames are given in a tuple in one subplot and in a list in
    the other one (axis names being the same), curves will stay in different
    subplots after a ``join`` and not be in the same one.

    If axes names are different a new subplot is created, curves cannot be
    drawn on the same one. Bins can be the same or not, only the name counts
    here, as it supposes quantities are different.

    >>> pit5 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d12, legend='d15', index=4, bins=[bins1])],
    ...     axnames=['Egg', 'beer'])])
    >>> splt25 = join(pit2, pit5)
    >>> print(splt25)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'beer'], plot type: 1D, N curves: 1
     Curve 0
      legend:  d12
      index:   1
      bins:    [array([0, 1, 2, 3])]
    Subplot 1
     axnames: ['Egg', 'beer'], plot type: 1D, N curves: 1
     Curve 0
      legend:  d15
      index:   4
      bins:    [array([0, 1, 2, 3])]
    <BLANKLINE>

    If the axis names are identical, even if bins are different, curves can be
    represented in the same subplot:

    >>> pit6 = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=[CurveElements(d2, legend='d2', index=5, bins=[bins2])],
    ...     axnames=['Egg', 'beer'])])
    >>> splt56 = join(pit5, pit6)
    >>> print(splt56)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['Egg', 'beer'], plot type: 1D, N curves: 2
     Curve 0
      legend:  d15
      index:   4
      bins:    [array([0, 1, 2, 3])]
     Curve 1
      legend:  d2
      index:   5
      bins:    [array([0, 1, 2, 3, 4])]
    <BLANKLINE>


    N-dimensional plot templates can be built, but the plotting engine may not
    be able to convert multi-dimensional templates into plots:

    The same behaviors are expected for multi-dimensions plots: same subplot
    for same axes, different subplots for different axes.

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
     axnames: ['egg', 'spam', 'bacon'], plot type: 2D, N curves: 1
     Curve 0
      legend:  d31
      index:   0
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    Subplot 1
     axnames: ['egg', 'spam', 'lobster'], plot type: 2D, N curves: 1
     Curve 0
      legend:  d32
      index:   1
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    <BLANKLINE>

    >>> splt77 = join(pit7, pit7)
    >>> print(splt77)
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    Subplot 0
     axnames: ['egg', 'spam', 'bacon'], plot type: 2D, N curves: 2
     Curve 0
      legend:  d31
      index:   0
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
     Curve 1
      legend:  d31
      index:   0
      bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    <BLANKLINE>

    To be noted: multiple curves on a given subplots will probably mean
    multiple subplots, one curve by subplot but all subplots with the same
    properties. For example, if logx is required all curves in the subplot will
    be in logarithmic scale.
    '''
    def __init__(self, *, subplots):  # curves):
        '''Construction of the PlotTemplate from x-bins and curves.

        The curves should be a list of :class:`CurveElements`.

        Bins should be common to all the curves. It is up to the user to ensure
        that (when coming from a unique test this should be automatic).

        :param bins: bins, common for all plots (important), only one set is
            needed
        :type bins: list(numpy.ndarray)
        :param axnames: names of axes (default: ``''``)
        :type axnames: list(str)
        :param curves: list of curves characteristics
        :type curves: list(CurveElements)
        '''
        self.subplots = subplots
        self.nb_plots = len(self.subplots)
        self.nb_curves = sum(len(s.curves) for s in self.subplots)

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
        ccplt = PlotTemplate(subplots=[pelt.copy() for pelt in self.subplots])
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
        # axnames = [splt.axnames for splt in self.subplots]
        # for splt in other.subplots:
        #     if splt.axnames in axnames:  # and splt.ptype == ptype
        #         ind = axnames.index(splt.axnames)
        #         self.subplots[ind].curves.extend(splt.curves)
        #     else:
        #         self.subplots.append(splt)
        for osplt in other.subplots:
            added = False
            for ssplt in self.subplots:
                if ssplt.consistent(osplt):
                    ssplt.curves.extend(osplt.curves)
                    added = True
                    break
            if not added:
                self.subplots.append(osplt)
        self.nb_plots = len(self.subplots)
        self.nb_curves = sum(len(s.curves) for s in self.subplots)

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
                 "N subplots: {}, N curves: {}\n".format(
                     self.__class__, self.nb_plots, self.nb_curves)]
        elts = []
        for i, splt in enumerate(self.subplots):
            elts.append("Subplot {}\n"
                        " axnames: {}, plot type: {}, N curves: {}\n"
                        .format(i, splt.axnames, splt.ptype, len(splt.curves)))
            for j, curve in enumerate(splt.curves):
                elts.append(
                    " Curve {}\n"
                    "  legend:  {}\n"
                    "  index:   {}\n"
                    "  bins:    {}\n"
                    "  values:  {}\n"
                    "  errors:  {}\n".format(
                        j, curve.legend, curve.index, curve.bins, curve.values,
                        curve.errors))
        return ''.join(intro + elts)

    def __str__(self):
        '''Printing of :class:`PlotTemplate`.'''
        intro = ["class:   {0}\n".format(self.__class__)]
        elts = []
        for i, splt in enumerate(self.subplots):
            elts.append("Subplot {}\n"
                        " axnames: {}, plot type: {}, N curves: {}\n"
                        .format(i, splt.axnames, splt.ptype, len(splt.curves)))
            for j, curve in enumerate(splt.curves):
                elts.append(
                    " Curve {}\n"
                    "  legend:  {}\n"
                    "  index:   {}\n"
                    "  bins:    {}\n".format(
                        j, curve.legend, curve.index, curve.bins))
        return ''.join(intro + elts)

    def fingerprint(self):
        '''Compute a fingerprint (a SHA256 hash) for `self`. The fingerprint
        depends only on the content of `self`. Two :class:`PlotTemplate`
        objects containing equal data have the same fingerprint. The converse
        is not true, but very likely.'''
        hasher = sha256()
        for splt in self.subplots:
            for axn in splt.axnames:
                hasher.update(axn.encode('utf-8'))
            for curve in splt.curves:
                for data in curve.data():
                    hasher.update(data)
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`PlotTemplate`.'''
        return self.subplots == other.subplots

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`PlotTemplate`.'''
        return not self == other

    def same_xaxis(self):
        '''Returns True if all axes have the same names (no check on the bins).
        '''
        min0 = min(c.bins[0][0] for c in self.subplots[0].curves)
        max0 = max(c.bins[0][-1] for c in self.subplots[0].curves)
        for splt in self.subplots[1:]:
            if splt.axnames[0] != self.subplots[0].axnames[0]:
                return False
            if (not np.isclose(min(c.bins[0][0] for c in splt.curves), min0)
                    or not np.isclose(max(c.bins[0][-1] for c in splt.curves),
                                      max0)):
                return False
        return True

    def pack_by_index(self):
        '''Pack the curves by index (typically used to attribute style to
        curves).

        :rtype: collections.defaultdict(list)
        '''
        ind_dict = defaultdict(list)
        for isplt, splt in enumerate(self.subplots):
            for crv in splt.curves:
                ind_dict[crv.index].append((crv, isplt))
        return ind_dict


class TextTemplate:
    '''A container class that encapsulates text for the report.

    The user has to write the text that can be highlighted using the start
    position and the length of the text to highlight.

    As in the other templates, examples will focus on the concatenation (join)
    of different TextTemplate.

    >>> ltext = 'Spam egg bacon'
    >>> ttplt1 = TextTemplate(ltext)
    >>> print("{!r}".format(ttplt1))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg bacon', highlight=None)
    >>> ttplt2 = TextTemplate(ltext, highlight=[(0, 4)])
    >>> print("{!r}".format(ttplt2))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg bacon', highlight=[(0, 4)])
    >>> ttplt3 = TextTemplate('sausage tomato', highlight=[(2, 3), (-3, 2)])
    >>> ttplt1.join(ttplt3)
    >>> print("{!r}".format(ttplt1))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg baconsausage tomato', highlight=[(16, 3), (-3, 2)])

    Test of the external function :meth:`join`:

    >>> ttplt4 = join(ttplt2, ttplt3)
    >>> print("{!r}".format(ttplt4))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='Spam egg baconsausage tomato', highlight=[(0, 4), (16, 3), (-3, 2)])
    >>> ttplt5 = join(ttplt3, ttplt1)
    >>> print("{!r}".format(ttplt5))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='sausage tomatoSpam egg baconsausage tomato', \
highlight=[(2, 3), (-31, 2), (30, 3), (-3, 2)])

    The copy doesn't affect the original:

    >>> ttplt6 = ttplt3.copy()
    >>> ttplt6.highlight = [(6, 3)]
    >>> print("{!r}".format(ttplt3))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='sausage tomato', highlight=[(2, 3), (-3, 2)])
    >>> print("{!r}".format(ttplt6))
    <class 'valjean.javert.templates.TextTemplate'>\
(text='sausage tomato', highlight=[(6, 3)])
    '''

    def __init__(self, text, highlight=None):
        '''Construct the text to be sent to the report.

        :param str text: text to be written in the report
        :param list(tuple(int)) highlight: parts of the string to highlight
            given as a list of tuples of 2 ints, first being the start position
            and the second the legth of the text to highlight
        '''
        self.text = text.replace('\n', '\n\n')
        if highlight is not None:
            msg = ("highlight should be a list of tuple of int, each tuple "
                   "being (start, length) of highlighted text")
            if not isinstance(highlight, list):
                raise TypeError(msg)
            if any(not isinstance(h, tuple) for h in highlight):
                raise TypeError(msg)
        self.highlight = highlight

    def __repr__(self):
        '''Print :class:`TextTemplate` details.'''
        return ('{}(text={!r}, highlight={!r})'
                .format(self.__class__, self.text, self.highlight))

    def _binary_join(self, other):
        lst = len(self.text)
        self.text += other.text
        nhl = []
        if self.highlight is not None:
            for pos in self.highlight:
                if pos[0] >= 0:
                    nhl.append(pos)
                else:
                    nhl.append((pos[0] - len(other.text), pos[1]))
        if other.highlight is not None:
            for pos in other.highlight:
                if pos[0] > 0:
                    nhl.append((pos[0] + lst, pos[1]))
                else:
                    nhl.append(pos)
        self.highlight = nhl

    def copy(self):
        '''Copy a :class:`TextTemplate` object.

        :rtype: TextTemplate
        '''
        return TextTemplate(text=self.text.replace('\n\n', '\n'),
                            highlight=(self.highlight.copy()
                                       if self.highlight is not None
                                       else None))

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
        hasher.update(
            np.require(np.array(self.highlight),
                       requirements='C').data.cast('b')
            if isinstance(self.highlight, list)
            else 'None'.encode('utf-8'))
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`TextTemplate`.'''
        return self.text == other.text and self.highlight == other.highlight

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
