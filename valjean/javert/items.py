'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.
'''

import numpy as np
from .. import LOGGER

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
        :type columns: list(:class:`numpy.ndarray`)
        :param list(str) headers: a list of headers.
        :param list(str) units: a list of measurement units.
        :param highlight: a callable of the form `f(*row) -> bool`.
        '''
        print(columns, type(columns))
        self.columns = columns
        n_columns = len(columns)
        self.headers = ['']*n_columns if headers is None else headers
        self.units = ['']*n_columns if units is None else units
        self.highlight = highlight

        print(self.columns, id(self.columns))
        print(self.columns[0], id(self.columns[0]))
        print(len(columns))
        print(len(headers), id(self.headers))

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
            if not isinstance(col, (np.ndarray, list)):
                raise TypeError('table columns must be lists or Numpy arrays, '
                                'not {}'.format(type(col)))

            col_size = col.size if isinstance(col, np.ndarray) else len(col)
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
        self.units = other.units if self.units is None else self.units
        self.columns = tuple(self.columns[i] + other.columns[i]
                             for i in range(len(self.columns)))
        return self

    def __add__(self, other):
        '''Implement ``+`` operator.

        :param other: :class:`TableItem` to add to the current one
        :returns: new :class:`TableItem`
        '''
        copy = self.copy()
        copy += other
        return copy


class PlotItem:
    '''A container for various shapes of plots depending on data nature
    (points, points series, etc). 2D plots per default (y=f(x)).'''

    def __init__(self, vals, bins, *, xerrors=None, yerrors=None,
                 xname='', yname='', title=''):
        self.vals = vals
        self.bins = bins
        self.xerrors = xerrors
        self.yerrors = yerrors
        self.xname = xname
        self.yname = yname
        self.title = title

        if ((not isinstance(self.vals, np.ndarray)
             or not isinstance(self.bins, np.ndarray))):
            raise TypeError('Vals and bins have to be np.ndarrays')

        if self.vals.ndim > 1:
            raise ValueError("Only 1-D values arrays taken into account")

        if self.xerrors is not None:
            if not isinstance(self.xerrors, np.ndarray):
                raise TypeError("x-errors has to be np.ndarray")
            if self.xerrors.size != self.vals.size:
                raise ValueError("Errors and values should have the same size")

        if self.yerrors is not None:
            if not isinstance(self.yerrors, np.ndarray):
                raise TypeError("y-errors has to be np.ndarray")
            if self.yerrors.size != self.vals.size:
                raise ValueError("Errors and values should have the same size")
