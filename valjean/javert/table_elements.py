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
    >>> from valjean.eponine.base_dataset import BaseDataset
    >>> import numpy as np
    >>> from collections import OrderedDict

    >>> vals = np.arange(6).reshape(1, 2, 1, 3)
    >>> errs = np.array([0.1]*6).reshape(1, 2, 1, 3)
    >>> bins = OrderedDict([('bacon', np.array([0, 1])),
    ...                     ('egg', np.array([0, 2, 4])),
    ...                     ('sausage', np.array([10, 20])),
    ...                     ('spam', np.array([-5, 0, 5]))])
    >>> ds = BaseDataset(vals, errs, bins=bins, name="ds_to_squeeze")
    >>> names, rbins = repr_bins(ds)
    >>> print(list(ds.bins.keys()))
    ['bacon', 'egg', 'sausage', 'spam']
    >>> print(names)
    ['egg', 'spam']
    >>> print(ds.shape)
    (1, 2, 1, 3)
    >>> print([rb.shape for rb in rbins])
    [(1, 2, 1, 3), (1, 2, 1, 3)]

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
    :type dsref: :class:`~valjean.gavroche.dataset.Dataset`
    :returns: list of the non-trivial dimensions and a tuple of the bins

    The tuple should have the same length as the list of dimensions and the
    bins insdide should have the same shape as ``dsref.value``.
    '''
    bins, dim_names = [], []
    for idim, dim in enumerate(dsref.bins.keys()):
        # reject trivial dimensions (1 bin or no bin)
        if dsref.value.shape[idim] < 2:
            continue
        dim_names.append(dim)
        dims_af = int(np.prod(dsref.value.shape[idim+1:]))
        dims_bf = int(np.prod(dsref.value.shape[:idim]))
        if dsref.bins[dim].size == dsref.value.shape[idim]+1:
            dbins = [["{0:.4g} - {1:.4g}".format(a, b)] * dims_af
                     for a, b in zip(dsref.bins[dim][:-1],
                                     dsref.bins[dim][1:])]
        else:
            dbins = [["{0:.4g}".format(a)] * dims_af
                     for a in dsref.bins[dim]]
        dbins = [dbins] * dims_bf
        bins.append(np.array(dbins).squeeze().reshape(dsref.shape))
    assert all(abin.shape == dsref.shape for abin in bins)
    return dim_names, tuple(bins)


def repr_testresultequal(result, verbosity=None):
    '''Represent the result of a :class:`~.TestEqual` test.

    :param result: a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("IN repr_testresultequal, %s, res = %s",
                 verbosity, bool(result))
    if bool(result):
        if verbosity != Verbosity.FULL_DETAILS:
            return []
        return repr_equal(result, 'equal?')
    if verbosity not in (Verbosity.INTERMEDIATE, Verbosity.FULL_DETAILS):
        return repr_equal_summary(result)
    return repr_equal(result, 'equal?')


def repr_equal_summary(result):
    '''Function to generate a summary table for the equal test (only tells if
    the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("repr_equal_summary found")
    if result:
        return [TextTemplate('Equal test: OK')]
    return [TextTemplate('Equal test: KO', highlight=[(-2, 2)])]


def repr_equal(result, result_header):
    '''Representation of equal test.

    :param result: a test result.
    :type result: :class:`~.TestResultEqual`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("In repr_equal")
    dscols = tuple((ds.value, eq)
                   for ds, eq in zip(result.test.datasets, result.equal))
    heads = [('reference',)]
    for ids in range(len(dscols)):
        str_ids = str(ids)
        heads.append(
            ('dataset'+str_ids, result_header.replace('?', str_ids+'?'))
            if len(dscols) > 1 else ('dataset', result_header))
    falses = np.full_like(result.test.dsref.value, False)
    highlights = [(falses,)]
    for equal in result.equal:
        highlights.append((falses, np.logical_not(equal)))
    table_template = TableTemplate(
        result.test.dsref.value,
        *chain.from_iterable(dscols),
        highlights=list(chain.from_iterable(highlights)),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


def repr_testresultapproxequal(result, verbosity=None):
    '''Represent the result of a :class:`~.TestApproxEqual` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_approx_equal_summary(result)
    return repr_approx_equal(result, 'approx equal?')


def repr_approx_equal_summary(result):
    '''Function to generate a summary table for the approx equal test (only
    tells if the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("repr_approx_equal_summary found")
    if result:
        return [TextTemplate('Approx equal test: OK')]
    return [TextTemplate('Approx equal test: KO', highlight=[(-2, 2)])]


def repr_approx_equal(result, result_header):
    '''Representation of approx equal test.

    :param result: a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("In repr_approx_equal")
    dscols = tuple((ds.value, eq)
                   for ds, eq in zip(result.test.datasets,
                                     result.approx_equal))
    heads = [('reference',)]
    for ids in range(len(dscols)):
        str_ids = str(ids)
        heads.append(
            ('dataset'+str_ids, result_header.replace('?', str_ids+'?'))
            if len(dscols) > 1 else ('dataset', result_header))
    falses = np.full_like(result.test.dsref.value, False)
    highlights = [(falses,)]
    for approx_equal in result.approx_equal:
        highlights.append((falses, np.logical_not(approx_equal)))
    table_template = TableTemplate(
        result.test.dsref.value,
        *chain.from_iterable(dscols),
        highlights=list(chain.from_iterable(highlights)),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


def repr_testresultstudent(result, verbosity=None):
    '''Represent the result of a :class:`~.TestStudent` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
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

    :param test_res: the test (not the result)
    :type test_res: :class:`~.TestStudent`
    :returns: list of headers
    '''
    heads = [('v_'+test_res.dsref.name, 'σ_'+test_res.dsref.name)]
    for _ds in test_res.datasets:
        heads.append(('v_'+_ds.name, 'σ_'+_ds.name, 't_'+_ds.name,
                      'Student('+_ds.name+')?'))
    if bin_names:
        heads.insert(0, bin_names)
    return heads


def repr_student(result):
    '''Representation of Student test result.

    :param result: a test result.
    :type result: :class:`~.TestResultStudent`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("In repr_student")
    oracles = result.oracles()
    nbins, bins = repr_bins(result.test.dsref)
    dscols = tuple((ds.value, ds.error, delta, studbool)
                   for ds, delta, studbool in zip(result.test.datasets,
                                                  result.delta,
                                                  oracles))

    falses = np.full_like(result.test.dsref.value, False)
    highlights = [(falses, falses)]
    heads = _student_heads(result.test, nbins)
    if nbins:
        highlights.insert(0, [(falses,)]*len(nbins))
    for oracle in oracles:
        highlights.append((falses, falses, falses, np.logical_not(oracle)))
    table_template = TableTemplate(
        *bins, result.test.dsref.value, result.test.dsref.error,
        *chain.from_iterable(dscols),
        highlights=list(chain.from_iterable(highlights)),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


def repr_student_silent(_result):
    '''Function to generate a silent table for the Student test (only tells if
    the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("student silent")
    return []


def repr_student_summary(result):
    '''Function to generate a summary table for the Student test (only tells if
    the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("repr_student_summary found")
    if result:
        return [TextTemplate('Student test: OK')]
    return [TextTemplate('Student test: KO', highlight=[(-2, 2)])]


def repr_student_intermediate(result):
    '''Function to generate an intermediate table for the Student test: print
    all the failing results.
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
                          False)
    highlights = [(falses, falses)]
    if nbins:
        highlights.insert(0, [(falses,)]*len(nbins))
    for oracle in oracles:
        highlights.append((falses, falses, falses,
                           np.logical_not(oracle[np.where(falses_ind == 0)])))
    cols = (list((b[np.where(falses_ind == 0)],) for b in bins)
            + [(result.test.dsref.value[np.where(falses_ind == 0)],
                result.test.dsref.error[np.where(falses_ind == 0)])])
    table_template = TableTemplate(
        *chain.from_iterable(cols),
        *chain.from_iterable(dscols),
        highlights=list(chain.from_iterable(highlights)),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


def repr_testresultbonferroni(result, verbosity=None):
    '''Represent the result of a :class:`~.TestBonferroni` test.

    Only reprensents the Bonferroni result, not the input test result.

    :param  result: a test result.
    :type result: :class:`~.TestResultBonferroni`
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("bonf repr, %s, res = %s", verbosity, bool(result))
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    return repr_bonferroni(result)


def repr_bonferroni(result):
    '''Reprensetation of Bonferroni test result.

    Only reprensents the Bonferroni result, not the input test result.

    :param result: a test result.
    :type result: :class:`~.TestResultBonferroni`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
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


def repr_testresultholmbonferroni(result, verbosity=None):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
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

    Only reprensents the Holm-Bonferroni result, not the input test result.

    :param result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
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

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    if result:
        return [TextTemplate('Holm-Bonferroni test: OK')]
    return [TextTemplate('Holm-Bonferroni test: KO', highlight=[(-2, 2)])]


def percent_fmt(num, den):
    '''Format a fraction as a percentage. Example:

    >>> percent_fmt(2, 4)
    '2/4 (50.0%)'
    >>> percent_fmt(0, 3)
    '0/3 (0.0%)'
    >>> percent_fmt(7, 7)
    '7/7 (100.0%)'
    >>> percent_fmt(0, 0)
    '0/0 (???%)'

    :param int num: the numerator.
    :param int den: the denominator.
    '''
    if den != 0:
        percent = 100.0 * num / den
        return '{:d}/{:d} ({:.1f}%)'.format(num, den, percent)
    return '{:d}/{:d} (???%)'.format(num, den)


def repr_testresultstatstasks(result, verbosity=None):
    '''Represent a :class:`~.TestResultStatsTasks` as a table. The table
    breaks down the tasks by status.

    :param TestResultStatsTasks result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    return repr_testresultstats(result, TaskStatus.DONE)


def repr_testresultstatstests(result, verbosity=None):
    '''Represent a :class:`~.TestResultStatsTests` as a table. The table
    breaks down the tests by success status.

    :param TestResultStatsTests result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    if verbosity == Verbosity.SILENT and bool(result):
        return []
    return repr_testresultstats(result, TestOutcome.SUCCESS)


def repr_testresultstats(result, status_ok):
    '''Helper function for :func:`repr_testresultstatstests` and
    :func:`repr_testresultstatstasks`. It generates a table with the
    `status_ok` value in the first row. Non-null results in other rows are
    considered as failures, and are highlighted if the count is non-zero.

    :param TestResultStatsTasks result: the test result to represent.
    :param status_ok: the status value that must be considered as a success.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    classify = result.classify

    statuses = [status_ok]
    statuses.extend(status for status in status_ok.__class__
                    if status != status_ok)
    statuses_txt = [status.name for status in statuses]

    counts = [len(classify[status]) for status in statuses]
    n_tasks = sum(counts)
    percents = [percent_fmt(count, n_tasks) for count in counts]

    statuses_txt.append('total')
    counts.append(n_tasks)
    percents.append(percent_fmt(n_tasks, n_tasks))

    hl_column = [False]
    hl_column.extend(count > 0 for count in counts[1:-1])
    highlights = [hl_column, hl_column]
    table = TableTemplate(statuses_txt, percents, headers=['status', 'counts'],
                          highlights=highlights)
    return [table]


def repr_testresultmetadata(result, verbosity=None):
    '''Represent the result of a :class:`~.TestMetadata` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("metadata res, %s, res = %s", verbosity, bool(result))
    if verbosity == Verbosity.SILENT:
        return []
    if verbosity == Verbosity.SUMMARY:
        return repr_metadata_summary(result)
    if verbosity == Verbosity.INTERMEDIATE:
        return repr_metadata_intermediate(result)
    if verbosity == Verbosity.FULL_DETAILS:
        return repr_metadata_full_details(result)
    return repr_metadata(result)


def repr_metadata(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    if result:
        return [TableTemplate(["Metadata:"], ["OK"],
                              highlights=[[False], [False]])]
    ko_list = list(result.only_failed_comparisons().keys())
    return [TableTemplate(["Failed metadata:"], [', '.join(ko_list)],
                          highlights=[[False], [True]])]


def repr_metadata_full_details(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
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

    Different levels of verbosity should be allowed.
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

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("repr_metadata_summary")
    if result:
        return [TextTemplate('Metadata: OK')]
    return [TextTemplate('Metadata: KO', highlight=[(-2, 2)])]


def repr_metadata_silent(_result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    LOGGER.debug("repr_metadata_silent")
    return []


def repr_testresultfailed(result, _verbosity=None):
    '''Represent a failed result as rst text.'''
    LOGGER.debug("In repr_testresultfailed")
    defmsg = ' failed with message:'
    cname = result.test.__class__.__name__
    return [TextTemplate('{}{} \n{}'.format(cname, defmsg, result.msg),
                         highlight=[(0, len(defmsg) + len(cname))])]
