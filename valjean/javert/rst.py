'''This module provides the classes to convert test results to reStructuredText
format. reStructuredText_ is a text markup language meant for easy human
consumption. The `reStructuredText primer`_ provides a good introduction to its
syntax.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _reStructuredText primer: http://
    docutils.sourceforge.net/docs/user/rst/quickstart.html
'''


import numpy as np

from .. import LOGGER
from .formatter import Formatter


class Rst:
    '''Class to convert :class:`~.TestResult` objects into reStructuredText
    format.'''

    def __init__(self, representation):
        '''Initialize a class instance with the given representation.

        :param representation: A representation.
        :type representation: :class:`~.Representation`
        '''
        self.representation = representation
        self.formatter = RstFormatter()

    def format(self, results):
        '''Format a bunch of test results.

        :param results: An iterable yielding :class:`~.TestResult` objects.
        :type results: iterable(:class:`~.TestResult`)
        :returns: the formatted test results.
        :rtype: str
        '''
        fmt_results = '\n'.join(self.format_result(res) for res in results)
        LOGGER.debug('formatted results: %s', fmt_results)
        return fmt_results

    def format_result(self, result):
        '''Format one test result.

        :param result: A :class:`~.TestResult`.
        :type result: :class:`~.gavroche.test.TestResult`
        :returns: the formatted test result.
        :rtype: str
        '''
        lines = [self.formatter.header(result)]
        lines.extend(fmt_item for items in self.representation(result)
                     for item in items
                     for fmt_item in self.formatter(item))
        return '\n'.join(lines)


class RstFormatter(Formatter):
    '''Class that dispatches the task of formatting items as reStructuredText.
    The concrete formatting is handled by separate classes
    (:class:`RstTable`...).
    '''

    def header(self, result):
        '''Produce the header for formatting a :class:`~.TestResult`.

        :param result: A test result.
        :type result: :class:`~.TestResult`
        :returns: the test header, for inclusion in a reST document.
        :rtype: str
        '''
        name = result.name
        lines = [name]
        lines.append('='*len(name))
        lines.append('')
        lines.append(result.desc)
        return '\n'.join(lines)

    @staticmethod
    def format_tableitem(table):
        '''Format a :class:`~.TableItem`.

        :param table: A table.
        :type result: :class:`~.TableItem`
        :returns: the reST table.
        :rtype: str
        '''
        print("ON EST DANS format_tableitem")
        return str(RstTable(table))


class RstTable:
    '''Convert a :class:`~.TableItem` into a reStructuredText table.'''

    HIGHLIGHT_ROLE = 'hl'
    COL_SEP = '  '

    def __init__(self, table, num_fmt='{:13.8g}'):
        '''Construct an :class:`RstTable` from the given
        :class:`~.items.TableItem`.

        :param table: The table to convert.
        :type table: :class:`~.items.TableItem`
        :param str num_fmt: A :func:`format` string to specify how numerical
                            table entries should be represented. The default
                            value for this option is ``'{:13.8g}'``.
        '''
        self.table = table
        self.num_fmt = num_fmt

    def __str__(self):
        '''Yield the table, as a reST string. This is probably the method that
        you want to call.'''
        columns = self.table.columns
        highlights = self.gen_mask(self.table.highlight, columns)
        rows = list(self.format_rows(self.transpose(columns), highlights,
                                     self.num_fmt))
        # rows = list(self.format_rows(columns, highlights, self.num_fmt))
        print("rows =", rows)
        return self.tabularize(self.table.headers, rows)

    @classmethod
    def tabularize(cls, headers, rows):
        '''Transform a list of headers and a list of rows into a nice reST
        table.

        The `headers` argument must be a list of strings. The `rows` argument
        represents the table rows, as a list of lists of strings. Each sublist
        represents a table row, and it must have the same length as `headers`,
        or terrible things will happen.

        The column widths are automatically computed to accommodate the largest
        item in each column. Smaller items are automatically right-justified.

            >>> headers = ['name', 'quest', 'favourite colour']
            >>> rows = [['Lancelot', 'to seek the Holy Grail', 'blue'],
            ...         ['Galahad', 'to seek the Holy Grail', 'yellow']]
            >>> table = RstTable.tabularize(headers, rows)
            >>> print(table)
            ========  ======================  ================
              name            quest           favourite colour
            ========  ======================  ================
            Lancelot  to seek the Holy Grail              blue
             Galahad  to seek the Holy Grail            yellow
            ========  ======================  ================

        :param list(str) headers: The table headers.
        :param list(list(str)) rows: The table rows.
        :returns: The reST table, as a string.
        '''
        widths = cls.compute_column_widths(headers, rows)
        LOGGER.debug('widths: %s', widths)

        sep_row = cls.COL_SEP.join('='*w for w in widths)
        header_row = cls.COL_SEP.join('{:^{width}}'
                                      .format(header, width=w)
                                      for w, header in zip(widths, headers))
        lines = [sep_row, header_row, sep_row]
        lines.extend(cls.concat_rows(widths, rows))
        lines.append(sep_row)
        lines.append('')  # in order to get 2 tables
        return '\n'.join(lines)

    @classmethod
    def gen_mask(cls, predicate, columns):
        '''Generate a stream of booleans by applying the given predicate to the
        matrix **rows**. However, the function accepts a collection of columns
        as an argument. For instance:

            >>> def sum_is_odd(*row):
            ...     return sum(row) % 2 == 1
            >>> columns = [[1, 2, 3], [8, 10, 12]]
            >>> list(RstTable.gen_mask(sum_is_odd, columns))
            [True, False, True]

        Here the first row is ``(1, 9)`` and ``1 + 8==9``, which is odd:
        therefore, the first element of the list is ``True``. Likewise, ``2 +
        10`` is even (``False``) and ``3 + 12`` is odd (``True``).

        This function also works with lists of numpy arrays:

            >>> columns = [np.array([1, 2, 3]), np.array([8, 10, 12])]
            >>> list(RstTable.gen_mask(sum_is_odd, columns))
            [True, False, True]

        :param predicate: A function of the form `f(*row) -> bool`.
        :param columns: An iterable of columns. It must contain tuples, lists
                        or :class:`numpy.ndarray` objects.
        '''
        for row in cls.transpose(columns):
            yield predicate(*row)

    @staticmethod
    def transpose(columns):
        r'''Given a matrix as a list of columns, yield the matrix rows.
        (Equivalently, if the matrix is given as a list of rows, yield the
        columns). For instance, consider the following list:

            >>> matrix = [(11, 21, 31), (12, 22, 32), (13, 23, 33)]
            >>> for column in matrix:
            ...     print(' '.join(str(elem) for elem in column))
            11 21 31
            12 22 32
            13 23 33

        If the tuples are interpreted as columns, `matrix` represents the
        following matrix:

        .. math::

            \begin{pmatrix}11&12&13\\21&22&23\\31&32&33\end{pmatrix}

        Transposing it yields:

            >>> transposed = RstTable.transpose(matrix)
            >>> for row in transposed:
            ...     print(' '.join(str(elem) for elem in row))
            11 12 13
            21 22 23
            31 32 33

        .. note::

            The matrix elements returned by :meth:`transpose` are actually
            0-dimensional :class:`numpy.ndarray` objects. For the purpose of
            their further manipulation this is of little consequence, as they
            transparently support most numerical operations.

        :param columns: An iterable yielding columns
        :type columns: list(list) or list(tuple) or
                       list(:class:`numpy.ndarray`)
        :raises ValueError: if the columns do not have the same length.
        :returns: a generator for the rows of the transposed matrix.
        '''
        try:
            yield from np.nditer(columns)
        except ValueError:
            raise ValueError('all columns must have the same length')

    @classmethod
    def format_rows(cls, rows, highlights, num_fmt):
        '''Transform a bunch of rows (containing arbitrary data: floats,
        bools, ints, strings...) into an iterable of lists of (optionally
        highlighted) strings.

        Example:

            >>> rows = [('European swallow', 27.7, 'km/h'),
            ...         ('African swallow', 35.1, 'km/h')]
            >>> highlights = [False, False]
            >>> for row in RstTable.format_rows(rows, highlights, '{:13.8f}'):
            ...     print(row)
            ['European swallow', '27.7', 'km/h']
            ['African swallow', '35.1', 'km/h']

        :param rows: An iterable yielding rows. The table rows may contain any
                     kind of data; if the data type is numeric, it will be
                     formatted according to the `num_fmt` argument; other types
                     will just get stringified (:class:`str`).
        :param highlights: An iterable yielding a bool for each row. The `i`-th
                           element decides whether the `i`-th table row should
                           be highlighted.
        :param num_fmt: The format string to be used for numerical types.
        :returns: a generator yielding lists of strings.
        '''
        def _format_val(val):
            try:
                type_ = val.dtype.type
            except AttributeError:
                return str(val)
            if type_ in (np.bool, np.bool_, np.int, np.integer, np.int32,
                         np.int64, np.str_):
                return str(val)
            return num_fmt.format(val)
        for row, high in zip(rows, highlights):
            yield [cls.highlight(_format_val(val), high) for val in row]

    @staticmethod
    def compute_column_widths(headers, rows):
        '''Compute the width of the columns that are necessary to accommodate
        all the headers and table rows.

            >>> headers = ['swallow sub-species', 'airspeed', 'laden']
            >>> rows = [['European', '27.7 km/h', 'no'],
            ...         ['European', '22.0 km/h', 'yes'],
            ...         ['African', '35.1 km/h', 'no'],
            ...         ['African', '26.2 km/h', 'yes']]
            >>> RstTable.compute_column_widths(headers, rows)
            [19, 9, 5]
            >>> [len('swallow sub-species'), len('27.7 km/h'), len('laden')]
            [19, 9, 5]


        :param list(str) headers: A list of column headers.
        :param list(list(str)) rows: A list of table rows.
        :returns: a list of integers indicating how wide each columns must be
                  to accommodate all the table elements and the headers.
        :rtype: list(int)
        '''
        col_widths = [len(header) for header in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(val))
        return col_widths

    @classmethod
    def highlight(cls, val, flag):
        '''Wrap `val` in highlight reST markers if flag is `True`.

        >>> RstTable.highlight('dis', False)
        'dis'
        >>> RstTable.highlight('DAT', True)
        ':hl:`DAT`'
        '''
        if flag:
            return ':{}:`{}`'.format(cls.HIGHLIGHT_ROLE, val)
        return val

    @classmethod
    def concat_rows(cls, widths, rows, just='>'):
        '''Concatenate the given rows and justify them according to the `just`
        parameter (see the :ref:`python:formatspec`). The columns widths (for
        justification) must be provided using the `width` argument.

        :param list(int) widths: The list of columns widths.
        :param list(list(str)) rows: The list of rows; each row must be a list
                                     of strings.
        :param str just: A format character for the justification (usually one
                         of '<', '^', '>').
        :returns: the concatenated, justified rows.
        :rtype: str
        '''
        for row in rows:
            centered = list('{val:{just}{width}}'
                            .format(val=val, width=width, just=just)
                            for width, val in zip(widths, row))
            yield cls.COL_SEP.join(centered)
