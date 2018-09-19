'''This module contains classes that are supposed to act as containers of all
the information that is necessary to represent a test in a given format. For
instance, in the case of tables this includes the column contents, the headers,
etc.  It does **not** include any formatting information, such as column
widths, floating-point precision, colours, etc.  Decisions about the formatting
are handled by suitable formatting classes, such as :class:`~.Rst`.
'''

import numpy as np


class TableItem:
    '''A container class that encapsulates all the necessary information to
    represent a table.'''

    def __init__(self, *columns, headers=None, units=None, highlight=None):
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
            if not isinstance(col, np.ndarray):
                raise TypeError('table columns must be Numpy arrays, not {}'
                                .format(type(col)))

            if i == 0:
                n_elems = self.columns[0].size
            elif col.size != n_elems:
                err = ('columns must have the same number of elements; '
                       'column 0 has size {}, but column {} has size {}'
                       .format(n_elems, i, col.size))
                raise ValueError(err)
