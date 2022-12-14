# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''This module provides the classes to convert test results to reStructuredText
format. reStructuredText_ is a text markup language meant for easy human
consumption. The `reStructuredText primer`_ provides a good introduction to its
syntax.

.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _reStructuredText primer: https://
    docutils.sourceforge.io/docs/user/rst/quickstart.html
.. _pkg_resources: https://setuptools.pypa.io/en/latest/pkg_resources.html
'''


from datetime import datetime
from collections import defaultdict
from pathlib import Path
import multiprocessing as mp
import pkg_resources as pkg
import numpy as np

from .. import LOGGER
from ..fingerprint import fingerprint
from ..path import ensure, sanitize_filename
from ..cosette.task import TaskStatus
from ..cosette.pythontask import PythonTask
from ..gavroche.test import TestResult
from .formatter import Formatter
from .mpl import MplPlot
from .test_report import TestReport, TestReportTask
from .verbosity import Verbosity


class Rst:
    '''Class to convert :class:`~.TestResult` objects into `reStructuredText`_
    format.'''

    def __init__(self, representation, *, n_workers=None):
        '''Initialize a class instance with the given representation.

        :param Representation representation: A representation.
        '''
        self.representation = representation
        self.formatter = RstFormatter()
        self.plots = {}
        self.tree_dict = defaultdict(list)
        self.text_dict = defaultdict(list)
        self.n_workers = n_workers

    def clear(self):
        '''Clear the content of `self`.'''
        self.plots.clear()
        self.tree_dict.clear()
        self.text_dict.clear()

    def format_report(self, *, report, author, version):
        '''Format a report.

        Most of the work is actually done in the :meth:`format_report_rec`
        method.

        :param TestReport report: the report to format.
        :returns: the formatted report.
        :rtype: FormattedRst
        '''
        self.clear()

        self.format_report_rec(report=report, tree=())

        fmt_report = FormattedRst(author=author, title=report.title,
                                  version=version,
                                  tree_dict=self.tree_dict,
                                  text_dict=self.text_dict,
                                  plots=self.plots,
                                  n_workers=self.n_workers)
        LOGGER.debug('formatted report: %s', fmt_report)
        return fmt_report

    def format_report_rec(self, *, report, tree):
        '''Recursively format report sections and populate the
        ``tree_dict`` and ``text_dict`` attributes.

        Report sections, as represented by the :class:`~.TestReport` class, are
        essentially trees, with :class:`~.TestResult` objects playing the role
        of the tree leaves and :class:`~.TestReport` objects playing the role
        of the tree nodes. This method performs a recursive, pre-order,
        depth-first traversal of the tree and fills the ``tree_dict`` and
        ``text_dict`` dictionaries with the information that is necessary
        to instantiate the final :class:`FormattedRst` object.

        Given a report object, this method constructs a dictionary key by
        concatenating in a tuple the titles of the parent reports and the
        present report. The tuple containing the parent reports' titles is
        recursively passed as the `tree` argument (and it is initialized to the
        empty tuple in the call from :meth:`format_report`). For instance,
        consider the following simplified report structure:

            >>> from valjean.javert.test_report import TestReport
            >>> subsub1 = TestReport(title='SubSub1')
            >>> subsub2 = TestReport(title='SubSub2')
            >>> sub1 = TestReport(title='Sub1', content=[subsub1, subsub2])
            >>> sub2 = TestReport(title='Sub2')
            >>> main = TestReport(title='Main', content=[sub1, sub2],
            ...                   text='Si six scies scient six cyprès, '
            ...                        'six-cent-six scies scient '
            ...                        'six-cent-six cyprès.')

        We instantiate an :class:`Rst` object and we format the report:

            >>> import valjean.javert.representation as rpr
            >>> from valjean.javert.rst import Rst
            >>> rst = Rst(rpr.Representation(rpr.FullRepresenter()))
            >>> formatted_report = rst.format_report(report=main, author='Me',
            ...                                      version='0.1')

        Let us look at the dictionary keys:

            >>> print(sorted(rst.text_dict.keys()))
            [(), ('Sub1',), ('Sub1', 'SubSub1'), ('Sub1', 'SubSub2'), \
('Sub2',)]

        The empty tuple, ``()``, is associated to the main report. The other
        keys represent subreports. The length of the tuple corresponds to the
        depth of the nested report; for instance, the ``'SubSub2'`` section
        appears in the ``('Sub1', 'SubSub2')`` tuple with length 2, because
        ``'SubSub2'`` is nested twice (``Main``/``Sub1``/``SubSub2``).

        The values of the ``text_dict`` dictionary are lists of strings
        representing the text of the given section. For instance, here is what
        the main section looks like:

        .. doctest::

            >>> print('\\n'.join(rst.text_dict[()]))
            Main
            ====
            <BLANKLINE>
            Si six scies scient six cyprès, six-cent-six scies scient \
six-cent-six cyprès.
            <BLANKLINE>

        The ``tree_dict`` dictionary associates a tuple representing a
        report section to the list of tuples that represent the subsections:

            >>> print(rst.tree_dict[()])
            [('Sub1',), ('Sub2',)]
            >>> print(rst.tree_dict[('Sub1',)])
            [('Sub1', 'SubSub1'), ('Sub1', 'SubSub2')]

        If a section does not have any subsection, the corresponding tuple does
        not appear in the dictionary:

            >>> ('Sub2',) in rst.tree_dict
            False

        The ``tree_dict`` and ``text_dict`` dictionaries contain most
        of the information required by :class:`FormattedRst` to write out the
        report in the form of a `reStructuredText`_ file tree (see
        :meth:`~.FormattedRst.write`).
        '''
        LOGGER.debug('formatting tree: %s', tree)
        LOGGER.debug('formatting report: %s', report.title)
        report_text = self.format_section(report, depth=len(tree))
        self.text_dict[tree].extend(report_text)
        for stuff in report.content:
            if isinstance(stuff, TestReport):
                subtree = tree + (stuff.title,)
                self.tree_dict[tree].append(subtree)
                self.format_report_rec(report=stuff, tree=subtree)
            elif isinstance(stuff, TestResult):
                LOGGER.debug('tree: %s', tree)
                LOGGER.debug('tree_dict: %s', dict(self.tree_dict))
                assert tree in self.text_dict
                res_text = self.format_result(stuff)
                self.text_dict[tree].extend(res_text)
            else:
                raise TypeError('expected TestReport or TestResult in '
                                f'TestReport content, found {type(stuff)} '
                                'instead')

    def format_section(self, section, *, depth):
        '''Format a report section.

        :param TestReport report: the report section to format.
        :returns: the formatted report section.
        :rtype: str
        '''
        lines = [self.formatter.header(section.title, depth),
                 self.formatter.text(section.text),
                 '']
        LOGGER.debug('formatted section: %s', lines)
        return lines

    def format_result(self, result):
        '''Format one test result.

        :param TestResult result: A :class:`~.TestResult`.
        :returns: the formatted test result.
        :rtype: str
        '''
        lines = [self.formatter.anchor(fingerprint(result.test)),
                 self.formatter.text(result.test.description), '']
        res_repr = self.representation(result)
        if (not res_repr
                and self.representation.verbosity in (Verbosity.SILENT,
                                                      Verbosity.SUMMARY)):
            return []
        for template in res_repr:
            fmt = self.formatter.template(template)
            lines.append(str(fmt))
            if isinstance(fmt, RstPlot):
                self.plots[fmt.fingerprint] = fmt.mpl_plot
        LOGGER.debug('formatted result: %s', lines)
        return lines


class RstFormatter(Formatter):
    '''Class that dispatches the task of formatting templates as
    `reStructuredText`_. The concrete formatting is handled by separate classes
    (:class:`RstTable`...).
    '''

    HEADER_CHARS = ('=', '-', '`', "'", '"')

    def header(self, name, depth):
        '''Produce the header for formatting a :class:`~.TestResult`.

        :param str name: A header name
        :param int depth: the depth of this header, 0 being the top.
        :returns: the test header, for inclusion in a reST document.
        :rtype: str
        '''
        if depth >= len(self.HEADER_CHARS):
            raise ValueError(f'maximum depth exceeded: {depth} > '
                             f'{self.HEADER_CHARS}')
        lines = [name]
        lines.append(self.HEADER_CHARS[depth]*len(name))
        lines.append('')
        return '\n'.join(lines)

    def text(self, text):
        '''Format some text.

        :param str text: some text to include.
        :returns: the text, in rst format.
        :rtype: str
        '''
        return text

    @staticmethod
    def anchor(fingerprint):
        '''Format an anchor with the given fingerprint.'''
        return f'\n.. _anchor_{fingerprint}:\n\n'

    @staticmethod
    def format_tabletemplate(table):
        '''Format a :class:`~.TableTemplate`.

        :param TableTemplate table: A table.
        :returns: the reST table.
        :rtype: RstTable
        '''
        return RstTable(table)

    @staticmethod
    def format_plottemplate(plot):
        '''Format a :class:`~.PlotTemplate`.

        :param PlotTemplate plot: A plot.
        :returns: the formatted plot
        :rtype: RstPlot
        '''
        return RstPlot(plot)

    @staticmethod
    def format_texttemplate(text):
        '''Format a :class:`~.TextTemplate`.

        :param TextTemplate text: A text with its highlight positions
        :returns: the formatted text (text itself)
        :rtype: str
        '''
        return RstText(text)


class RstTable:
    '''Convert a :class:`~.TableTemplate` into a `reStructuredText`_ table.'''

    HIGHLIGHT_ROLE = 'hl'
    COL_SEP = '  '

    def __init__(self, table, num_fmt='{:11.6g}'):
        '''Construct an :class:`RstTable` from the given
        :class:`~.templates.TableTemplate`.

        :param TableTemplate table: The table to convert.
        :param str num_fmt: A :func:`format` string to specify how numerical
                            table entries should be represented. The default
                            value for this option is ``'{:11.6g}'``.
        '''
        self.table = table
        self.num_fmt = num_fmt

    def __str__(self):
        '''Yield the table, as a reST string. This is probably the method that
        you want to call.'''
        columns = self.table.columns
        highlights = self.table.highlights
        rows = list(self.format_columns(columns, highlights, self.num_fmt))
        table = self.tabularize(self.table.headers, rows, indent=4)
        header = ('.. role:: ' + RstTable.HIGHLIGHT_ROLE + '\n\n'
                  '.. table::\n    :widths: auto\n\n')
        return header + table + '\n'

    @classmethod
    def tabularize(cls, headers, rows, *, indent=0):
        '''Transform a list of headers and a list of rows into a nice reST
        table.

        The `headers` argument must be a list of strings. The `rows` argument
        represents the table rows, as a list of lists of strings. Each sublist
        represents a table row, and it must have the same length as `headers`,
        or terrible things will happen.

        The column widths are automatically computed to accommodate the largest
        template in each column. Smaller templates are automatically
        right-justified.

        .. doctest::

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
            <BLANKLINE>

        You can also indent the table by a given amount of spaces with the
        `indent` keyword argument:

        .. doctest::

            >>> table = RstTable.tabularize(headers, rows, indent=4)
            >>> print(table)
                ========  ======================  ================
                  name            quest           favourite colour
                ========  ======================  ================
                Lancelot  to seek the Holy Grail              blue
                 Galahad  to seek the Holy Grail            yellow
                ========  ======================  ================
            <BLANKLINE>

        :param list(str) headers: The table headers.
        :param list(list(str)) rows: The table rows.
        :returns: The reST table, as a string.
        '''
        widths = cls.compute_column_widths(headers, rows)
        LOGGER.debug('widths: %s', widths)

        sep_row = cls.COL_SEP.join('='*w for w in widths)
        header_row = cls.COL_SEP.join(f'{header:^{w}}'
                                      for w, header in zip(widths, headers))
        lines = [' '*indent + sep_row, header_row, sep_row]
        lines.extend(cls.concat_rows(widths, rows))
        lines.append(sep_row)
        lines.append('')  # in order to get 2 tables
        lines_sep = '\n' + ' '*indent
        return lines_sep.join(lines)

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
        :type columns: list(list) or list(tuple) or list(numpy.ndarray)
        :raises ValueError: if the columns do not have the same length.
        :returns: a generator for the rows of the transposed matrix.
        '''
        LOGGER.debug('columns: %s, %s', type(columns), len(columns))
        try:
            yield from np.nditer(columns)
        except ValueError as exc:
            raise ValueError('all columns must have the same length') from exc

    @classmethod
    def format_columns(cls, columns, highlights, num_fmt):
        '''Transform a bunch of columns (containing arbitrary data: floats,
        bools, ints, strings...) into an iterable of lists of (optionally
        highlighted) strings representing the table **rows**.

        Example:

            >>> cols = [('European swallow', 'African swallow'),
            ...         (27.7, 35.1),
            ...         ('km/h', 'km/h')]
            >>> highs = [[False, False], [False, True], [False, True]]
            >>> for row in RstTable.format_columns(cols, highs, '{:13.8f}'):
            ...     print(row)
            ['European swallow', '  27.70000000', 'km/h']
            ['African swallow', ':hl:`35.10000000`', ':hl:`km/h`']

        :param columns: An iterable yielding columns. The table columns may
                        contain any kind of data; if the data type is numeric,
                        it will be formatted according to the `num_fmt`
                        argument; other types will just get stringified
                        (:class:`str`).
        :param highlights: An iterable yielding a collection of bools for each
                           column.  The `j`-th element of the `i`-th iteration
                           decides whether the element in the `j`-th column of
                           the `i`-th row should be highlighted.
        :param num_fmt: The format string to be used for numerical types.
        :returns: a generator yielding lists of strings, representing the table
                  rows.
        '''
        def _format_val(val):
            try:
                type_ = val.dtype.type
            except AttributeError:
                return str(val)
            if issubclass(type_, (float, np.inexact)):
                return num_fmt.format(val)
            return str(val)
        for row, hlrow in zip(cls.transpose(columns),
                              cls.transpose(highlights)):
            yield [cls.highlight(_format_val(val), high)
                   for val, high in zip(row, hlrow)]

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
            return f':{cls.HIGHLIGHT_ROLE}:`{val.strip()}`'
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
            centered = list(f'{val:{just}{width}}'
                            for width, val in zip(widths, row))
            yield cls.COL_SEP.join(centered)


class RstPlot:
    '''This class models a plot in an `reStructuredText`_ document. It converts
    a :class:`~.PlotTemplate` object into an :class:`~.MplPlot`, and it
    provides the ``.. image::`` directive to include in the .rst file.
    '''
    def __init__(self, plot):
        self.fingerprint = fingerprint(plot)
        self.mpl_plot = MplPlot(plot)

    def __str__(self):
        return f'.. image:: /figures/{self.filename()}\n'

    def filename(self):
        '''Make up a(n almost) unique filename for this plot.

        :returns: the filename from fingerprint (png format)
        :rtype: str
        '''
        return f'plot_{self.fingerprint}.png'


class RstText:
    '''Construct an :class:`RstText` from the given
    :class:`~.templates.TextTemplate`.
    '''
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text.text


class FormattedRst:
    '''This class represents a formatted rst document tree, which typically
    consists of an index file and of several sections.
    '''
    def __init__(self, *, author, title, version,
                 tree_dict, text_dict, plots, n_workers=None):
        '''Create a :class:`FormattedRst` object. The `author`, `title` and
        `version` arguments are expected to be strings and are
        self-explanatory.

        The `tree_dict` and `text_dict` arguments must be dictionaries.  The
        `tree_dict` dictionary represents the tree structure of the
        `reStructuredText`_ document, and the `text_dict` represent the
        contents of each section. The report sections, which appear as keys in
        both dictionaries, are expected to be tuples of strings, with each
        string representing an additional layer in the document hierarchy. The
        section contents (the values of `text_dict`) are expected to be lists
        of strings to be written to disk.

        Finally, the `plots` argument is a list of the plots referenced by the
        text sections. The plots will be written to disk with filenames of the
        form :samp:`plot_{fingerprint}.png`, where `fingerprint` is the plot
        fingerprint.

        :param str author: the author of this report.
        :param str title: the title of this report.
        :param str version: the version number for this report.
        :param dict tree_dict: dictionary mapping tuples of sections to lists
            of tuples of sections.
        :param dict text_dict: dictionary mapping tuples of sections to lists
            of strings.
        :param plots: list of plots to be written to disk.
        :type plots: list(MplPlot)
        :param n_workers: number of subprocesses to use to write out the plots
            in parallel.  If `None` is given, write the plots in sequential
            mode.
        :type n_workers: int or None
        '''
        if not isinstance(tree_dict, dict):
            raise TypeError("expecting a dictionary as 'tree_dict'"
                            f", got {type(tree_dict)}")
        if not isinstance(text_dict, dict):
            raise TypeError("expecting a dictionary as 'text_dict'"
                            f", got {type(tree_dict)}")

        self.author = author
        self.title = title
        self.version = version
        self.tree_dict = tree_dict.copy()
        self.text_dict = text_dict.copy()
        self.plots = plots.copy()
        self.n_workers = n_workers

    def write(self, path):
        '''Write the text files and the plots into the directory specified by
        `path`.

        :param path: path to the directory that will be written to. It is OK if
                     the directory does not exist.
        :type path: str or pathlib.Path
        '''
        path = Path(path)

        self.setup(path)
        self._write_rec(tree=(), path=path)

        items = [(plot, str(path / 'figures'
                            / f'plot_{fingerprint}.png'))
                 for fingerprint, plot in self.plots.items()]
        if self.n_workers is not None:
            LOGGER.info('writing %d plots using %d subprocesses',
                        len(items), self.n_workers)
            with mp.Pool(self.n_workers) as pool:
                pool.map(self._static_writer, items)
        else:
            LOGGER.info('writing %d plots in sequential mode', len(items))
            for item in items:
                self._static_writer(item)

    @staticmethod
    def _static_writer(plot_path_pair):
        plot_path_pair[0].save(plot_path_pair[1])

    def _write_rec(self, *, tree, path):

        if tree:
            tree_path = self.tree_to_path(base=path, tree=tree)
        else:
            tree_path = path / 'index'

        LOGGER.info('writing tree_path: %s', tree_path)
        ensure(tree_path.parent, is_dir=True)

        subtrees = self.tree_dict[tree]
        write_path = tree_path.with_name(tree_path.name + '.rst')
        with write_path.open('w') as tree_file:
            text = '\n'.join(self.text_dict[tree])
            tree_file.write(text)
            if subtrees:
                toc = self.toc('Contents', subtrees)
                tree_file.write(toc)

        for subtree in subtrees:
            self._write_rec(tree=subtree, path=path)

    @staticmethod
    def tree_to_path(*, base, tree):
        '''Convert a tree to a file path.

        :param base: the base path for all subtrees.
        :type base: pathlib.Path
        :param tuple(str) tree: a sequence of tree nodes, starting from the
                          tree root.
        '''
        paths = [sanitize_filename(node) for node in tree]
        return base.joinpath(*paths)

    def toc(self, toc_title, subtrees):
        '''Build an rst table of contents.

        :param str toc_title: the title for the table of contents (e.g.
                              ``'Contents'``).
        '''
        lines = ['\n\n.. toctree::\n    :titlesonly:\n    '
                 f':caption: {toc_title}:\n']
        for subtree in subtrees:
            # need to remove upper level to subtree in toc else they appear N
            # times in the toc, depending on level, breaking the links
            fname = str(self.tree_to_path(base=Path(''), tree=subtree[-2:]))
            line = ' '*4 + fname
            lines.append(line)
        lines.append('')
        lines.append('')
        return '\n'.join(lines)

    def setup(self, path):
        '''Set up the output directory for :meth:`write`.

        :param pathlib.Path path: the path to the directory.
        '''
        ensure(path, is_dir=True)
        ensure(path / '.static', is_dir=True)
        ensure(path / '.templates', is_dir=True)
        ensure(path / 'figures', is_dir=True)
        year = datetime.now().year
        self.configure(resource='conf.py.template', dest=path / 'conf.py',
                       author=self.author, project=self.title,
                       version=self.version, theme='alabaster',
                       theme_options={}, year=year)
        self.configure(resource='valjean.css',
                       dest=path / '.static' / 'valjean.css',
                       formatting=False)

    @staticmethod
    def configure(resource, dest, formatting=True, **kwargs):
        '''Copy a package resource to the specified destination, optionally
        formatting the resource content using :meth:`str.format`.

        For more information about resources, see `pkg_resources`_.

        :param str resource: the name of the resource.
        :param pathlib.Path dest: the destination path.
        :param bool formatting: whether formatting should be applied.
        :param dict kwargs: any additional keyword arguments will be passed to
                            the formatting.
        '''
        assert pkg.resource_exists('valjean.javert.resources.rst', resource)
        res_template = pkg.resource_string('valjean.javert.resources.rst',
                                           resource).decode('utf-8')
        res_str = res_template.format(**kwargs) if formatting else res_template
        with dest.open('w') as res_file:
            res_file.write(res_str)


class RstTestReportTask(PythonTask):
    '''Task class that transforms a list of tests into a test report.
    :class:`~.TestResult` objects in the environment.'''

    @classmethod
    def from_tasks(cls, name, *, make_report, eval_tasks, representation,
                   author, version, kwargs=None, deps=None, soft_deps=None):
        '''Construct an :class:`RstTestReportTask` from a list of test
        evaluation tasks and a function to classify test results and put them
        in test reports.
        '''
        report_name = 'report-' + name
        report_task = TestReportTask(report_name, make_report=make_report,
                                     eval_tasks=eval_tasks, kwargs=kwargs)
        return cls(name, report_task=report_task,
                   representation=representation, author=author,
                   version=version, deps=deps, soft_deps=soft_deps)

    def __init__(self, name, *, report_task, representation, author, version,
                 deps=None, soft_deps=None):

        def write_rst(*, env, config):
            report = env[report_task.name]['result']
            if 'args' in config and 'workers' in config['args']:
                n_workers = config['args']['workers']
                LOGGER.debug('will use %d subprocesses to write the report',
                             n_workers)
            else:
                n_workers = None
                LOGGER.debug('will write the report in sequential mode')
            rst = Rst(representation, n_workers=n_workers)
            fmt_report = rst.format_report(report=report, author=author,
                                           version=version)
            report_root = Path(config.query('path', 'report-root'))
            report_path = report_root / sanitize_filename(self.name)
            ensure(report_path, is_dir=True)
            fmt_report.write(report_path)
            env_up = {self.name: {'result': fmt_report,
                                  'output_dir': str(report_path)}}
            return env_up, TaskStatus.DONE

        deps = [] if deps is None else deps
        deps.append(report_task)

        super().__init__(name, write_rst, deps=deps, soft_deps=soft_deps,
                         env_kwarg='env', config_kwarg='config')
