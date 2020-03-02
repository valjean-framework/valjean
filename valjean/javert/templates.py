'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.

.. _numpy indexing:
   https://docs.scipy.org/doc/numpy/user/basics.indexing.html
'''
from collections.abc import Iterable
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

    def __init__(self, values, legend, *, index, label='', errors=None):
        '''Construction of :class:`CurveElements`: curve details (values,
        label, etc).

        A major parameter is ``label``, set by default to ``''``: this is the
        y-axis name. When representing the curve on the pyplot, the subplot is
        chosen according this ``label``.

        The label is used in the legend.

        Values and errors (if given) should be essentially one-dimension
        :obj:`numpy.ndarray` of same shape (they must have only one non-trivial
        dimension).

        The curve index is used to share the plotting style between curves that
        should. For example, if on a plot there are the reference and two
        curves representing different data, let's say 'egg' and 'spam', if we
        also want to draw the ratio of these data with the reference, the same
        style will be applied to 'egg vs reference' and 'egg' and to 'spam vs
        reference' and 'spam'. In that case to ensure the same style 'egg vs
        reference' and 'egg' should have the same index (same for the 'spam'
        case). ``index=0`` will always be considered as reference.

        :param values: array to be represented on the plot, **mandatory**
        :type values: numpy.ndarray
        :param str legend: string to be used in the legend to characterize the
            curve, **mandatory**
        :param int index: index of the curve
        :param str label: label of the axis representing the plotted quantity
            (used to determine the number of subplots on the plot if 1D)
        :param errors: errors associated to values (per default only on 1D
            plots and y-axis)
        :type errors: numpy.ndarray
        '''
        self.values = values
        self.legend = legend
        self.index = index
        self.label = label
        self.errors = errors

        if not isinstance(self.values, np.ndarray):
            raise TypeError('Values should be np.ndarray.')

        if self.errors is not None:
            if not isinstance(self.errors, np.ndarray):
                raise TypeError('Errors should be np.ndarray or None')

    def copy(self):
        '''Copy a :class:`CurveElements` object.

        :rtype: CurveElements
        '''
        return CurveElements(values=self.values.copy(),
                             legend=self.legend,
                             index=self.index,
                             label=self.label,
                             errors=(None if self.errors is None
                                     else self.errors.copy()))

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield np.require(self.values, requirements='C').data.cast('b')
        yield self.legend.encode('utf-8')
        yield bytes((self.index,))
        yield self.label.encode('utf-8')
        if self.errors is not None:
            yield np.require(self.errors, requirements='C').data.cast('b')

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`CurveElements`.'''
        return (np.array_equal(self.values, other.values)
                and self.legend == other.legend
                and self.index == other.index
                and self.label == other.label
                and np.array_equal(self.errors, other.errors))

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`CurveElements`.'''
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
    >>> pit1 = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(d11, 'd11', index=0, label='brandy')])
    >>> pit2 = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(d12, 'd12', index=1, label='beer')])
    >>> pit3 = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(d13, 'd13', index=2, label='wine')])

    >>> splt12 = join(pit1, pit2)
    >>> print("{!r}".format(splt12))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    bins:    [array([0, 1, 2, 3])]
    axnames: ['egg']
    legend: d11
    index:  0
    label:  brandy
    values: [0 1 2 3]
    errors: None
    legend: d12
    index:  1
    label:  beer
    values: [ 0 10 20 30]
    errors: None
    <BLANKLINE>

    We obtain a new :class:`PlotTemplate` containing two curves with different
    labels.

    >>> splt123 = join(pit1, pit2, pit3)
    >>> print("{!r}".format(splt123))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    bins:    [array([0, 1, 2, 3])]
    axnames: ['egg']
    legend: d11
    index:  0
    label:  brandy
    values: [0 1 2 3]
    errors: None
    legend: d12
    index:  1
    label:  beer
    values: [ 0 10 20 30]
    errors: None
    legend: d13
    index:  2
    label:  wine
    values: [ 0 11 22 33]
    errors: None
    <BLANKLINE>

    As expected a new :class:`PlotTemplate` is obtained, containing three
    curves.

    Like in the TableTemplate case, the :meth:`PlotTemplate.join` method
    updates the left :class:`PlotTemplate` as expected:

    >>> pit1.join(pit2, pit3)
    >>> print("{!r}".format(pit1))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    bins:    [array([0, 1, 2, 3])]
    axnames: ['egg']
    legend: d11
    index:  0
    label:  brandy
    values: [0 1 2 3]
    errors: None
    legend: d12
    index:  1
    label:  beer
    values: [ 0 10 20 30]
    errors: None
    legend: d13
    index:  2
    label:  wine
    values: [ 0 11 22 33]
    errors: None
    <BLANKLINE>


    It is not possible to join a new curve with the same ``label``. In that
    case they must be added directly in the :class:`CurveElements` list,
    preferably at creation. As a consequence, only new subplots can be added,
    no new curve on an existing plot.

    >>> d14 = d11*2
    >>> pit4 = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(d14, 'd14', index=2, label='beer')])
    >>> split24 = join(pit2, pit4)
    Traceback (most recent call last):
        ...
    ValueError: Only new subplots (labels) can be joined to a previous \
PlotTemplate.

    At creation we get:

    >>> pit24 = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(d12, 'd12', index=1, label='beer'),
    ...             CurveElements(d14, 'd14', index=3, label='beer')])
    >>> print("{!r}".format(pit24))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    bins:    [array([0, 1, 2, 3])]
    axnames: ['egg']
    legend: d12
    index:  1
    label:  beer
    values: [ 0 10 20 30]
    errors: None
    legend: d14
    index:  3
    label:  beer
    values: [0 2 4 6]
    errors: None
    <BLANKLINE>

    >>> pit5 = PlotTemplate(
    ...     bins=[bins1], axnames=['spam'],
    ...     curves=[CurveElements(d12, 'd12', index=0, label='bacon')])
    >>> splt15 = join(pit1, pit5)
    Traceback (most recent call last):
        ...
    ValueError: PlotTemplates should have the same axes names to be joined

    An error is raised if the axes don't have the same name. In that case the
    :class:`PlotTemplate` cannot be concatenated. They will have to be
    represented on two different plots, even if the bins used (``bins1``) are
    the same (they probably don't have the same meaning).

    >>> pit6 = PlotTemplate(
    ...     bins=[bins2], axnames=['spam'],
    ...     curves=[CurveElements(d2, 'd2', index=0, label='bacon')])
    >>> splt56 = join(pit5, pit6)
    Traceback (most recent call last):
        ...
    ValueError: Bins should be the same in both PlotTemplates

    An error is also raised: x-axis bins have the same names but not the same
    number of bins. The two :class:`PlotTemplate` cannot represent the same
    quantity so be represented on the same plot.

    N-dimensional plot templates can be built, but the plotting engine may not
    be able to convert multi-dimensional templates into plots:

    >>> bins3 = np.arange(3)
    >>> d31 = np.arange(bins1.size*bins2.size*bins3.size).reshape(
    ...     bins1.size, bins2.size, bins3.size)
    >>> d32 = np.arange(bins1.size*bins2.size*bins3.size).reshape(
    ...     bins1.size, bins2.size, bins3.size)*0.01
    >>> pit7 = PlotTemplate(
    ...     bins=[bins1, bins2, bins3], axnames=['egg', 'spam', 'bacon'],
    ...     curves=[CurveElements(d31, 'd31', index=0, label='tomato')])
    >>> pit8 = PlotTemplate(
    ...     bins=[bins1, bins2, bins3], axnames=['egg', 'spam', 'bacon'],
    ...     curves=[CurveElements(d32, 'd32', index=0, label='lobster')])
    >>> splt78 = join(pit7, pit8)
    >>> print("{!s}".format(splt78))
    class:   <class 'valjean.javert.templates.PlotTemplate'>
    bins:    [array([0, 1, 2, 3]), array([0, 1, 2, 3, 4]), array([0, 1, 2])]
    axnames: ['egg', 'spam', 'bacon']
    legend: d31
    index:  0
    label:  tomato
    legend: d32
    index:  0
    label:  lobster
    <BLANKLINE>

    The same conditions are expected for multi-dimensions plots (same axes,
    different labels, etc).

    >>> splt77 = join(pit7, pit7)
    Traceback (most recent call last):
        ...
    ValueError: Only new subplots (labels) can be joined to a previous \
PlotTemplate.


    >>> bins4 = np.arange(3)*10
    >>> pit9 = PlotTemplate(
    ...     bins=[bins1, bins2, bins4], axnames=['egg', 'spam', 'bacon'],
    ...     curves=[CurveElements(d32, 'd32', index=0, label='coffee')])
    >>> splt79 = join(pit7, pit9)
    Traceback (most recent call last):
        ...
    ValueError: Bins should be the same in both PlotTemplates

    '''

    def __init__(self, *, bins, curves, axnames=()):
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
        self.bins = bins
        assert isinstance(axnames, Iterable)
        self.axnames = axnames if axnames else ['']*len(self.bins)
        self.curves = curves
        self.customization = {}

        if not isinstance(self.curves, list):
            raise TypeError("The 'curves' argument must a list of "
                            "CurveElements.")

        if not all(isinstance(curve, CurveElements) for curve in self.curves):
            raise TypeError("The 'curves' argument must a list of "
                            "CurveElements.")

    def copy(self):
        '''Copy a :class:`PlotTemplate` object.

        :rtype: PlotTemplate
        '''
        return PlotTemplate(bins=[b.copy() for b in self.bins],
                            axnames=self.axnames.copy(),
                            curves=[pelt.copy() for pelt in self.curves])

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
        if self.axnames != other.axnames:
            raise ValueError("PlotTemplates should have the same axes names "
                             "to be joined")
        if not all(np.array_equal(sb, ob)
                   for sb, ob in zip(self.bins, other.bins)):
            raise ValueError("Bins should be the same in both PlotTemplates")
        if not set(c.label for c in other.curves).isdisjoint(
                set(c.label for c in self.curves)):
            raise ValueError("Only new subplots (labels) can be joined to a "
                             "previous PlotTemplate.")
        self.curves.extend(other.curves)

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
        intro = ["class:   {0}\n"
                 "bins:    {1}\n"
                 "axnames: {2}\n"
                 .format(self.__class__, self.bins, self.axnames)]
        elts = []
        for curve in self.curves:
            elts.append("legend: {0}\n"
                        "index:  {1}\n"
                        "label:  {2}\n"
                        "values: {3}\n"
                        "errors: {4}\n".format(curve.legend, curve.index,
                                               curve.label,
                                               curve.values, curve.errors))
        return ''.join(intro + elts)

    def __str__(self):
        '''Printing of :class:`PlotTemplate`.'''
        intro = ["class:   {0}\n"
                 "bins:    {1}\n"
                 "axnames: {2}\n"
                 .format(self.__class__, self.bins, self.axnames)]
        elts = []
        for curve in self.curves:
            elts.append("legend: {0}\n"
                        "index:  {1}\n"
                        "label:  {2}\n".format(curve.legend, curve.index,
                                               curve.label))
        return ''.join(intro + elts)

    def fingerprint(self):
        '''Compute a fingerprint (a SHA256 hash) for `self`. The fingerprint
        depends only on the content of `self`. Two :class:`PlotTemplate`
        objects containing equal data have the same fingerprint. The converse
        is not true, but very likely.'''
        hasher = sha256()
        for bins in self.bins:
            hasher.update(np.require(bins, requirements='C').data.cast('b'))
        for axname in self.axnames:
            hasher.update(axname.encode('utf-8'))
        for curve in self.curves:
            for data in curve.data():
                hasher.update(data)
        return hasher.hexdigest()

    def __eq__(self, other):
        '''Test for equality of `self` and another :class:`PlotTemplate`.'''
        return (np.array_equal(self.bins, other.bins)
                and self.axnames == other.axnames
                and self.curves == other.curves)

    def __ne__(self, other):
        '''Test for inequality of `self` and another :class:`PlotTemplate`.'''
        return not self == other

    def add_customization(self, **kwargs):
        '''Update customization dictionary.

        The keyword has to be understood in :class:`.mpl.MplPlot`, check it for
        possibilities.
        '''
        self.customization.update(kwargs)


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
        return TextTemplate(text=self.text,
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
        hasher.update(self.highlight.data.cast('b'))
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
    >>> plotit = PlotTemplate(
    ...     bins=[bins1], axnames=['egg'],
    ...     curves=[CurveElements(data11, 'd11', index=0, label='spam')])
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
