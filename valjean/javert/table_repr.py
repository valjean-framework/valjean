'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from itertools import chain
import numpy as np
from .. import LOGGER
from ..cosette.task import TaskStatus
from ..gavroche.diagnostics.stats import TestOutcome
from .templates import TableTemplate, TextTemplate
from .verbosity import Verbosity

# turn off pylint warnings about invalid names in this file; there are just too
# many long function names and they cannot be renamed because
# javert.representation looks for them by programmatically constructing their
# name based on the name of the test result class, the verbosity, etc.
# pylint: disable=invalid-name


def repr_bins(dsref):
    '''Representation of bins in tables.

    When bins are given by edges, representation is ``min - max``, when they
    are given at center, representation is ``center``.

    Trivial dimensions are not represented, i.e. dimensions where there is only
    one bin.

    If there are more than one non-trivial dimensions, some repetition is
    expected. For example with two non-trivial dimensions of two bins each one
    point will be defined by its coordinated in the two dimensions and we
    expect all the bins to possibily be shown in a table. We expected 4 bins
    and their associated values in that case.

    Let's consider the following dataset:
    >>> from valjean.eponine.dataset import Dataset
    >>> import numpy as np
    >>> from collections import OrderedDict

    >>> vals = np.arange(6).reshape(1, 2, 1, 3, 1)
    >>> errs = np.array([0.1]*6).reshape(1, 2, 1, 3, 1)
    >>> bins = OrderedDict([('bacon', np.array([0, 1])),
    ...                     ('egg', np.array([0, 2, 4])),
    ...                     ('sausage', np.array([10, 20])),
    ...                     ('spam', np.array([-5, 0, 5])),
    ...                     ('tomato', np.array([-2, 2]))])
    >>> ds = Dataset(vals, errs, bins=bins)
    >>> names, rbins = repr_bins(ds)
    >>> print(list(ds.bins.keys()))
    ['bacon', 'egg', 'sausage', 'spam', 'tomato']
    >>> print(names)
    ['egg', 'spam']
    >>> print(ds.shape)
    (1, 2, 1, 3, 1)
    >>> print([rb.shape for rb in rbins])
    [(1, 2, 1, 3, 1), (1, 2, 1, 3, 1)]

    ``'bacon'`` and ``'sausage'`` are trivial dimensions, so won't be
    represented in the table, but we expect 6 values corresponding to 2 bins in
    ``'egg'`` and 3 in ``'spam'``. Each value corresponds to a line in the
    table so each columns should have the same size and the same shape, the
    shape of the given dataset without trivial dimensions. We then have 3
    ``'spam'`` bins in each ``'egg'`` bins or 2 ``'egg'`` bins in each
    ``'spam'`` bins. Each couple appears only once.

    >>> for name, rbin in zip(names, rbins):
    ...     print(name, ':', rbin.flatten())
    egg : ['0 - 2' '0 - 2' '0 - 2' '2 - 4' '2 - 4' '2 - 4']
    spam : ['-5' '0' '5' '-5' '0' '5']

    As expected from the bins, ``'egg'`` bins are given by edges
    (``min - max``) while ``'spam'`` bins are given by center (``center``).

    :param dsref: dataset
    :type dsref: Dataset
    :returns: list of the non-trivial dimensions and a tuple of the bins
    :rtype: (list(str), tuple(numpy.ndarray))

    The tuple must have the same length as the list of dimensions and the bins
    inside must have the same shape as ``dsref.value``.
    '''
    bins, dim_names = [], []
    for idim, dim in enumerate(dsref.bins.keys()):
        # reject trivial dimensions (1 bin or no bin)
        if dsref.value.shape[idim] < 2:
            continue
        dim_names.append(dim)
        shape = [dsref.value.shape[idim]] + [1] * (dsref.ndim - 1 - idim)
        if dsref.value.shape[:idim] == tuple([1]*idim):
            shape = [1]*idim + shape
        if dsref.bins[dim].size == dsref.value.shape[idim]+1:
            dbins = ["{0:.4g} - {1:.4g}".format(a, b)
                     for a, b in zip(dsref.bins[dim][:-1],
                                     dsref.bins[dim][1:])]
        else:
            dbins = (["{0:.4g}".format(a) for a in dsref.bins[dim]]
                     if dsref.bins[dim].dtype.kind != 'U'
                     else dsref.bins[dim])
        bins.append(np.array(dbins).reshape(shape))
    bbins = np.broadcast_arrays(*bins)
    return dim_names, tuple(bbins)


def repr_testresultequal(result, verbosity=None):
    '''Represent the result of a :class:`~.TestEqual` test.

    :param TestResultEqual result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a :class:`~.TestResultEqual`
    '''
    LOGGER.debug("IN repr_testresultequal, %s, res = %s",
                 verbosity, bool(result))
    if bool(result):
        if verbosity != Verbosity.FULL_DETAILS:
            return []
        return repr_equal(result)
    if verbosity is None:
        return repr_equal(result)
    if verbosity.value < Verbosity.INTERMEDIATE.value:
        return repr_equal_summary(result)
    return repr_equal(result)


def repr_equal_summary(result):
    '''Function to generate a summary table for the equal test (only tells if
    the test was successful or not).

    :param TestResultEqual result: a test result.
    :rtype: list(TextTemplate)
    '''
    LOGGER.debug("repr_equal_summary found")
    if result:
        return [TextTemplate('Equal test: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Equal test: :hl:`KO`\n\n')]


def repr_equal(result):
    '''Representation of equal test.

    :param TestResultEqual result: a test result.
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_equal")
    nbins, bins = repr_bins(result.test.dsref)
    dscols = tuple((ds.value, eq)
                   for ds, eq in zip(result.test.datasets, result.equal))
    heads = nbins + [result.test.dsref.name]
    for ds in result.test.datasets:
        heads.extend([ds.name,
                      'equal({})?'.format(ds.name)
                      if len(result.test.datasets) > 1 else 'equal?'])
    falses = np.full_like(result.test.dsref.value, False, dtype=bool)
    highlights = [falses] * (len(nbins) + 1)
    for equal in result.equal:
        highlights.extend([falses, np.logical_not(equal)])
    table_template = TableTemplate(
        *bins, result.test.dsref.value, *chain.from_iterable(dscols),
        highlights=highlights, headers=heads)
    return [table_template]


def repr_testresultapproxequal(result, verbosity=None):
    '''Represent the result of a :class:`~.TestApproxEqual` test.

    :param TestResultApproxEqual result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a :class:`~.TestResultApproxEqual`
    '''
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_approx_equal_summary(result)
    return repr_approx_equal(result)


def repr_approx_equal_summary(result):
    '''Function to generate a summary table for the approx equal test (only
    tells if the test was successful or not).

    :param TestResultApproxEqual result: a test result.
    :rtype: list(TextTemplate)
    '''
    LOGGER.debug("repr_approx_equal_summary found")
    if result:
        return [TextTemplate('Approx equal test: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Approx equal test: :hl:`KO`\n\n')]


def repr_approx_equal(result):
    '''Representation of approx equal test.

    :param TestResultApproxEqual result: a test result.
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_approx_equal")
    nbins, bins = repr_bins(result.test.dsref)
    dscols = tuple((ds.value, eq)
                   for ds, eq in zip(result.test.datasets,
                                     result.approx_equal))
    heads = nbins + [result.test.dsref.name]
    for ds in result.test.datasets:
        heads.extend([ds.name,
                      'approx equal({})?'.format(ds.name)
                      if len(result.test.datasets) > 1
                      else 'approx equal?'])
    falses = np.full_like(result.test.dsref.value, False, dtype=bool)
    highlights = [falses] * (len(nbins) + 1)
    for approx_equal in result.approx_equal:
        highlights.extend([falses, np.logical_not(approx_equal)])
    table_template = TableTemplate(
        *bins, result.test.dsref.value, *chain.from_iterable(dscols),
        highlights=highlights, headers=heads)
    return [table_template]


def repr_testresultstudent(result, verbosity=None):
    '''Represent the result of a :class:`~.TestStudent` test.

    :param TestResultStudent result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a :class:`~.TestResultStudent`
    '''
    LOGGER.debug("student repr, %s, res = %s", verbosity, bool(result))
    if verbosity == Verbosity.SILENT:
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_student_summary(result)
    if verbosity == Verbosity.INTERMEDIATE:
        return repr_student_intermediate(result)
    return repr_student(result)


def _student_heads(test_res, bin_names):
    '''Build the column names for Student test representation.

    Reference appears first then all the tested datasets. They are identified
    by their name if unique, else their index in the list of datasets is used.

    :param TestStudent test_res: the test (not the result)
    :param list(str) bin_names: names of the bins (dimensions)
    :returns: list of headers
    '''
    heads = ['v('+test_res.dsref.name+')', 'σ('+test_res.dsref.name+')']
    for _ds in test_res.datasets:
        heads.extend(['v('+_ds.name+')', 'σ('+_ds.name+')'])
        if len(test_res.datasets) > 1:
            heads.extend([r't('+_ds.name+')', 'Student('+_ds.name+')?'])
        else:
            heads.extend(['t', 'Student?'])
    heads = bin_names + heads
    return heads


def repr_student(result):
    '''Representation of Student test result.

    :param TestResultStudent result: a test result.
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_student")
    oracles = result.oracles()
    nbins, bins = repr_bins(result.test.dsref)
    dscols = tuple((ds.value, ds.error, delta, studbool)
                   for ds, delta, studbool in zip(result.test.datasets,
                                                  result.delta,
                                                  oracles))
    falses = np.full_like(result.test.dsref.value, False, dtype=bool)
    heads = _student_heads(result.test, nbins)
    highlights = [falses]*(len(nbins) + 2)
    for oracle in oracles:
        highlights += [falses, falses, falses, np.logical_not(oracle)]
    table_template = TableTemplate(
        *bins, result.test.dsref.value, result.test.dsref.error,
        *chain.from_iterable(dscols),
        highlights=highlights, headers=heads)
    return [table_template]


def repr_student_silent(_result):
    '''Function to generate a silent table for the Student test (only tells if
    the test was successful or not).

    :param TestResultStudent result: a Student test result.
    :returns: empty list
    '''
    LOGGER.debug("student silent")
    return []


def repr_student_summary(result):
    '''Function to generate a summary table for the Student test (only tells if
    the test was successful or not).

    :param TestResultStudent result: a Student test result.
    :rtype: list(TextTemplate)
    '''
    LOGGER.debug("repr_student_summary found")
    if result:
        return [TextTemplate('Student test: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Student test: :hl:`KO`\n\n')]


def repr_student_intermediate(result):
    '''Function to generate an intermediate table for the Student test: print
    all the failing results.

    :param TestResultStudent result: a Student test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("repr_student_intermediate found")
    if result:
        return repr_student_summary(result)
    if result.test.dsref.shape == ():
        return repr_student(result)
    oracles = result.oracles()
    falses_ind = np.ones_like(result.test.dsref.value)
    for oracle in oracles:
        falses_ind[np.where(oracle == 0)] = 0
    nbins, bins = repr_bins(result.test.dsref)
    dscols = tuple((ds.value[np.where(falses_ind == 0)],
                    ds.error[np.where(falses_ind == 0)],
                    delta[np.where(falses_ind == 0)],
                    studbool[np.where(falses_ind == 0)])
                   for ds, delta, studbool in zip(result.test.datasets,
                                                  result.delta,
                                                  oracles))
    heads = _student_heads(result.test, nbins)
    falses = np.full_like(result.test.dsref.value[np.where(falses_ind == 0)],
                          False, dtype=bool)
    highlights = [falses]*(len(nbins) + 2)
    for oracle in oracles:
        highlights += [falses, falses, falses,
                       np.logical_not(oracle[np.where(falses_ind == 0)])]
    cols = (list((b[np.where(falses_ind == 0)],) for b in bins)
            + [(result.test.dsref.value[np.where(falses_ind == 0)],
                result.test.dsref.error[np.where(falses_ind == 0)])])
    table_template = TableTemplate(
        *chain.from_iterable(cols), *chain.from_iterable(dscols),
        highlights=highlights, headers=heads)
    return [table_template]


def repr_testresultbonferroni(result, verbosity=None):
    '''Represent the result of a :class:`~.TestBonferroni` test.

    Only represents the Bonferroni result, not the input test result.

    :param TestResultBonferroni result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a :class:`~.TestResultBonferroni`
    '''
    LOGGER.debug("bonf repr, %s, res = %s", verbosity, bool(result))
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_bonferroni_summary(result)
    return repr_bonferroni(result)


def repr_bonferroni(result):
    '''Reprensetation of Bonferroni test result.

    Only represents the Bonferroni result, not the input test result.

    :param TestResultBonferroni result: a test result.
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: list(TableTemplate)
    '''
    ndatasets = len(result.first_test_res.test.datasets)
    oracles = list(result.oracles())
    highlights = [[False] * ndatasets] * 5  # 5 non-highlighted columns
    highlights.append([not oracle for oracle in oracles])
    table_template = TableTemplate(
        ["{0} vs {1}".format(result.first_test_res.test.dsref.name, dtest.name)
         for dtest in result.first_test_res.test.datasets],
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [result.test.bonf_signi_level] * ndatasets,
        [min(pval) for pval in result.first_test_res.pvalue],
        oracles,
        highlights=highlights,
        headers=['test', 'ndf', 'α', 'α(Bonferroni)', 'min(p-value)',
                 'Bonferroni?'])
    return [table_template]


def repr_bonferroni_summary(result):
    '''Represent the result of a :class:`~.TestBonferroni` test for the
    SUMMARY level of verbosity.

    :param TestResultBonferroni result: a test result.
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: list(TextTemplate)
    '''
    if result:
        return [TextTemplate('Bonferroni test: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Bonferroni test: :hl:`KO`\n\n')]


def repr_testresultholmbonferroni(result, verbosity=None):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test.

    :param TestResultHolmBonferroni result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a
        :class:`~.TestResultHolmBonferroni`
    '''
    LOGGER.debug("HB res, %s, res = %s", verbosity, bool(result))
    if verbosity == Verbosity.SILENT:
        if bool(result):
            return []
        return repr_holm_bonferroni_summary(result)
    if verbosity == Verbosity.SUMMARY:
        return repr_holm_bonferroni_summary(result)
    return repr_holm_bonferroni(result)


def repr_holm_bonferroni(result):
    '''Reprensetation of Holm-Bonferroni test result.

    Only represents the Holm-Bonferroni result, not the input test result.

    :param TestResultHolmBonferroni result: a test result.
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: list(TableTemplate)
    '''
    ndatasets = len(result.first_test_res.test.datasets)
    oracles = list(result.oracles())
    highlights = [[False] * ndatasets] * 6  # 6 non-highlighted columns
    highlights.append([not oracle for oracle in oracles])
    table_template = TableTemplate(
        ["{0} vs {1}".format(result.first_test_res.test.dsref.name, dtest.name)
         for dtest in result.first_test_res.test.datasets],
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [np.amin(pval) for pval in result.first_test_res.pvalue],
        [np.amin(alpha_i) for alpha_i in result.alphas_i],
        list(result.nb_rejected),
        oracles,
        highlights=highlights,
        headers=['test', 'ndf', 'α', 'min(p-value)', 'min(α)',
                 'N rejected', 'Holm-Bonferroni?'])
    return [table_template]


def repr_holm_bonferroni_summary(result):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test for the
    SUMMARY level of verbosity.

    :param TestResultHolmBonferroni result: a test result.
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: list(TextTemplate)
    '''
    if result:
        return [TextTemplate('Holm-Bonferroni test: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Holm-Bonferroni test: :hl:`KO`\n\n')]


def percent_fmt(num, den):
    '''Format a fraction as a percentage. Example:

    >>> percent_fmt(2, 4)
    '2/4 (50.0%)'
    >>> percent_fmt(0, 3)
    '0/3 (0.0%)'
    >>> percent_fmt(7, 7)
    '7/7 (100.0%)'
    >>> percent_fmt(0, 0)
    '0/0 (???%)'

    :param int num: the numerator.
    :param int den: the denominator.
    :rtype: str
    '''
    nbsp = ' '
    if den != 0:
        percent = 100.0 * num / den
        return '{:d}/{:d}{}({:.1f}%)'.format(num, den, nbsp, percent)
    return '{:d}/{:d}{}(???%)'.format(num, den, nbsp)


def repr_testresultstatstasks(result, verbosity=None):
    '''Represent a :class:`~.TestResultStatsTasks` as a table. The table
    breaks down the tasks by status.

    :param TestResultStatsTasks result: the test result to represent.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing the test result.
    '''
    LOGGER.debug("In repr_testresultstatstasks")
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    return repr_testresultstats(result, TaskStatus.DONE, 'tasks')


def repr_testresultstatstests(result, verbosity=None):
    '''Represent a :class:`~.TestResultStatsTests` as a table. The table
    breaks down the tests by success status.

    :param TestResultStatsTests result: the test result to represent.
    :param Verbosity verbosity: verbosity level
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_testresultstatstests")
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    return repr_testresultstats(result, TestOutcome.SUCCESS, 'tests')


def repr_testresultstats(result, status_ok, label):
    '''Helper function for :func:`repr_testresultstatstests` and
    :func:`repr_testresultstatstasks`. It generates a table with the
    `status_ok` value in the first row. Non-null results in other rows are
    considered as failures, and are highlighted if the count is non-zero. Null
    results are omitted from the table.

    :param result: the test result to represent.
    :type result: TestResultStatsTasks or TestResultStatsTests
    :param status_ok: the status value that must be considered as a success.
    :param str label: the type of things that we are testing (``'tests'`` or
        ``'tasks'``)
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    classify = result.classify

    statuses = [status_ok]
    statuses.extend(status for status in status_ok.__class__
                    if status != status_ok)

    counts = [len(classify[status]) for status in statuses]
    n_tasks = sum(counts)
    percents = [percent_fmt(count, n_tasks) for count in counts
                if count != 0]
    statuses = [status for status, count in zip(statuses, counts)
                if count != 0]
    counts = [count for count in counts if count != 0]
    statuses_txt = [status.name for status in statuses]

    statuses_txt.append('total')
    counts.append(n_tasks)
    percents.append(percent_fmt(n_tasks, n_tasks))

    hl_column = [False]
    hl_column.extend(count > 0 for count in counts[1:-1])
    table = TableTemplate(statuses_txt, percents, headers=['status', 'counts'],
                          highlights=[hl_column, hl_column])
    text = []
    for status, status_txt in zip(statuses, statuses_txt):
        if status_ok == status:
            continue
        text.append('List of {} with status {}:\n\n'.format(label, status_txt))
        for item in sorted(classify[status]):
            if item.fingerprint:
                text.append('#. :ref:`{} <anchor_{}>`'
                            .format(item.name, item.fingerprint))
            else:
                text.append('#. {}'.format(item.name))
        text.append('\n')
    return [table, TextTemplate('\n'.join(text))]


def repr_testresultstatstestsbylabels(result, verbosity=None):
    '''Represent a :class:`~.TestResultStatsTestsByLabels` as tables. Shape of
    the table may change according to the number of flags required.

    :param TestResultStatsTestsByLabels result: the test result to represent.
    :param Verbosity verbosity: verbosity level
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_testresultstatstestsbylabels")
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_testresultstatsbylabels_summary(result)
    return repr_testresultstatsbylabels(result)


def _sbl_labels_1column(labels, results, oracles):
    '''Build a :class:`TableTemplate` from the results where labels are
    concantenated in one column.

    :param tuple(str) labels: labels used to make statistics
    :param dict results: result from :class:`TestResultStatsTestsByLabels`
    :param list(bool) oracles: result of each individual test
    :rtype: TableTemplate
    '''
    lnames, lok, lko, hlight = [], [], [], []
    for res, ora in zip(results, oracles):
        lnames.append('/'.join(res['labels']))
        lok.append(percent_fmt(res['OK'], res['total']))
        lko.append(percent_fmt(res['KO'], res['total']))
        hlight.append([not ora])
    return TableTemplate(
        lnames, lok, lko,
        headers=['/'.join(labels), r'% success', r'% failure'],
        highlights=[hlight]*3)


def _sbl_1colbylabel(labels, results, oracles):
    '''Build a :class:`TableTemplate` from the results where each label will be
    represented in a separate column.

    :param tuple(str) labels: labels used to make statistics
    :param dict results: result from :class:`TestResultStatsTestsByLabels`
    :param list(bool) oracles: result of each individual test
    :rtype: TableTemplate
    '''
    lnames = [[] for _ in range(len(labels))]
    lok, lko, hlight = [], [], []
    for res, ora in zip(results, oracles):
        for i, lab in enumerate(res['labels']):
            lnames[i].append(lab)
        lok.append(percent_fmt(res['OK'], res['total']))
        lko.append(percent_fmt(res['KO'], res['total']))
        hlight.append([not ora])
    return TableTemplate(
        *lnames, lok, lko,
        headers=[*labels] + [r'% success', r'% failure'],
        highlights=[hlight]*(len(labels)+2))


def repr_testresultstatsbylabels(result):
    '''Function to print detailed statistics on tests, per category and sample
    run.

    :param TestResultStatsTestsByLabels result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("In repr_testresultstatsbylabels")
    res = []
    res.append(_sbl_1colbylabel(
        result.test.by_labels, result.classify, result.oracles()))
    if result.nb_missing_labels() != 0:
        res.append(TextTemplate('At least one of the labels used for sorting '
                                '{} is missing in {} tests\n\n'
                                .format(result.test.by_labels,
                                        result.nb_missing_labels())))
    return res


def repr_testresultstatsbylabels_summary(result):
    '''Function to print detailed statistics on tests, per category and sample
    run in summary case: only print failed cases.

    :param TestResultStatsTestsByLabels result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate), list(TextTemplate)
    '''
    LOGGER.debug("In repr_testresultstatsbylabels")
    res = []
    lnames = [[] for _ in range(len(result.test.by_labels))]
    lok, lko, hlight = [], [], []
    for resu, ora in zip(result.classify, result.oracles()):
        if ora:
            continue
        for i, lab in enumerate(resu['labels']):
            lnames[i].append(lab)
        lok.append(percent_fmt(resu['OK'], resu['total']))
        lko.append(percent_fmt(resu['KO'], resu['total']))
        hlight.append([not ora])
    tabtemp = TableTemplate(
        *lnames, lok, lko,
        headers=[*result.test.by_labels] + [r'% success', r'% failure'],
        highlights=[hlight]*(len(result.test.by_labels)+2))
    if lok:
        res.append(tabtemp)
    else:
        res.append(TextTemplate('No failed test found.\n\n'))
    if result.nb_missing_labels() != 0:
        res.append(TextTemplate('At least one of the labels used for sorting '
                                '{} is missing in {} tests\n\n'
                                .format(result.test.by_labels,
                                        result.nb_missing_labels())))
    return res


def repr_testresultmetadata(result, verbosity=None):
    '''Represent the result of a :class:`~.TestMetadata` test.

    :param TestResultMetadata result: a test result.
    :param Verbosity verbosity: verbosity level
    :returns: list of templates representing a :class:`~.TestResultMetadata`
    '''
    LOGGER.debug("metadata res, %s, res = %s", verbosity, bool(result))
    if verbosity is None:
        return repr_metadata(result)
    if verbosity == Verbosity.SILENT:
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_metadata_summary(result)
    if verbosity == Verbosity.INTERMEDIATE:
        return repr_metadata_intermediate(result)
    if verbosity.value >= Verbosity.FULL_DETAILS.value:
        return repr_metadata_full_details(result)
    return repr_metadata(result)


def repr_metadata(result):
    '''Function to generate a table from the metadata test results.

    :param TestResultMetadata result: a test result.
    :rtype: list(TableTemplate)
    '''
    if result:
        return [TableTemplate(["Metadata:"], ["OK"],
                              highlights=[[False], [False]])]
    ko_list = list(result.only_failed_comparisons().keys())
    return [TableTemplate(["Failed metadata:"], [', '.join(ko_list)],
                          highlights=[[False], [True]])]


def repr_metadata_full_details(result):
    '''Function to generate a table from the metadata test results.

    :param TestResultMetadata result: a test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("repr_metadata_full_details")
    samp_names = list(result.test.dmd)
    keys = []
    tdict = {name: [] for name in samp_names}
    hdict = {name: [] for name in samp_names}
    for dkey in result.test.all_md.keys():
        keys.append(dkey)
        for nam in samp_names:
            tdict[nam].append(str(result.test.all_md[dkey][nam]))
            hdict[nam].append(not result.dict_res[dkey][nam])
    ocols = list(tdict.values())
    highl = [[False]*len(keys)]
    highl.extend(hdict.values())
    heads = ['key']
    heads.extend(result.test.dmd)
    table = TableTemplate(keys, *ocols,
                          highlights=highl,
                          headers=heads)
    return [table]


def repr_metadata_intermediate(result):
    '''Function to generate a table from the metadata test results.

    :param TestResultMetadata result: a test result.
    :rtype: list(TableTemplate)
    '''
    LOGGER.debug("repr_metadata_intermediate")
    if not result.only_failed_comparisons():
        return repr_metadata_summary(result)
    samp_names = list(result.test.dmd)
    keys = []
    tdict = {name: [] for name in samp_names}
    hdict = {name: [] for name in samp_names}
    for dkey in result.only_failed_comparisons():
        keys.append(dkey)
        for nam in samp_names:
            tdict[nam].append(str(result.only_failed_comparisons()[dkey][nam]))
            hdict[nam].append(not result.dict_res[dkey][nam])
    ocols = list(tdict.values())
    highl = [[False]*len(keys)]
    highl.extend(hdict.values())
    heads = ['key']
    heads.extend(result.test.dmd)
    table = TableTemplate(keys, *ocols,
                          highlights=highl,
                          headers=heads)
    return [table]


def repr_metadata_summary(result):
    '''Function to generate a table from the metadata test results.

    :param TestResultMetadata result: a test result.
    :rtype: list(TextTemplate)
    '''
    LOGGER.debug("repr_metadata_summary")
    if result:
        return [TextTemplate('Metadata: OK\n\n')]
    return [TextTemplate('.. role:: hl\n\n'
                         'Metadata test: :hl:`KO`\n\n')]


def repr_metadata_silent(_result):
    '''Function to generate a table from the metadata test results.

    :param TestResultMetadata result: a test result.
    :returns: empty list
    '''
    LOGGER.debug("repr_metadata_silent")
    return []


def repr_testresultexternal(_result, _verbosity=None):
    '''Represent external test as tables -> no table done.

    If tables are required they are already done. Their representation in the
    report is done by :class:`.ExternalRepresenter`.

    :returns: empty list
    '''
    return []


def repr_testresultfailed(result, _verbosity=None):
    '''Represent a failed result as rst text.

    :param TestResultFailed result: a failed test result.
    :rtype: list(TextTemplate)
    '''
    LOGGER.debug("In repr_testresultfailed")
    defmsg = ' failed with message:'
    cname = result.test.__class__.__name__
    text = ':hl:`{}{}`\n{}\n'.format(cname, defmsg, result.msg)
    return [TextTemplate('.. role:: hl\n\n' + text.replace('\n', '\n\n'))]
