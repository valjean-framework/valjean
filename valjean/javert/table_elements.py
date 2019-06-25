'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from itertools import chain
import numpy as np
from .. import LOGGER
from ..cosette.task import TaskStatus
from ..gavroche.diagnostics.stats import TestOutcome
from .templates import TableTemplate


def repr_testresultequal(result):
    '''Represent the result of a :class:`~.TestEqual` test.

    :param result: a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_equal(result, 'equal?')


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


def repr_testresultapproxequal(result):
    '''Represent the result of a :class:`~.TestApproxEqual` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_approx_equal(result, 'approx equal?')


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


def repr_testresultstudent(result):
    '''Represent the result of a :class:`~.TestStudent` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_student(result, 'Student?')


def repr_student(result, result_header):
    '''Reprensetation of Student test result.

    :param result: a test result.
    :type result: :class:`~.TestResultStudent`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    LOGGER.debug("In repr_student")
    oracles = result.oracles()
    dscols = tuple((ds.value, ds.error, delta, studbool)
                   for ds, delta, studbool in zip(result.test.datasets,
                                                  result.delta,
                                                  oracles))
    heads = [('v_ref', 'σ_ref')]
    for ids in range(len(dscols)):
        str_ids = str(ids)
        heads.append(('v'+str_ids, 'σ'+str_ids, 'Δ'+str_ids,
                      result_header.replace('?', str_ids+'?'))
                     if len(dscols) > 1
                     else ('v_test', 'σ_test', 'Δ_test', result_header))
    falses = np.full_like(result.test.dsref.value, False)
    highlights = [(falses, falses)]
    for oracle in oracles:
        highlights.append((falses, falses, falses, np.logical_not(oracle)))
    table_template = TableTemplate(
        result.test.dsref.value, result.test.dsref.error,
        *chain.from_iterable(dscols),
        highlights=list(chain.from_iterable(highlights)),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


def repr_testresultstudent_silent(result):
    '''Represent the result of a :class:`~.TestStudent` test for the SILENT
    level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_student_silent(result)


def repr_student_silent(result):
    '''Function to generate a silent table for the Student test (only tells if
    the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    return []


def repr_testresultstudent_summary(result):
    '''Represent the result of a :class:`~.TestStudent` test for the SUMMARY
    level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_student_summary(result)


def repr_student_summary(result):
    '''Function to generate a summary table for the Student test (only tells if
    the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    if bool(result):
        return [TableTemplate(["Holm-Bonferroni test:"], ["OK"],
                              highlights=[[False], [False]])]
    return [TableTemplate(["Holm-Bonferroni test:"], ["KO"],
                          highlights=[[False], [True]])]


def repr_testresultstudent_full_details(result):
    '''Represent the result of a :class:`~.TestStudent` test for the
    FULL_DETAILS level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_student(result, 'Student?')


def repr_testresultbonferroni(result):
    '''Represent the result of a :class:`~.TestBonferroni` test.

    Only reprensents the Bonferroni result, not the input test result.

    :param  result: a test result.
    :type result: :class:`~.TestResultBonferroni`
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_bonferroni(result, 'Bonferroni?')


def repr_bonferroni(result, result_header):
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
        [result.first_test_res.test.name] * ndatasets,
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [result.test.bonf_signi_level] * ndatasets,
        [min(pval) for pval in result.first_test_res.pvalue],
        oracles,
        highlights=highlights,
        headers=['test', 'ndf', 'α', 'α(Bonferroni)', 'min(p-value)',
                 result_header])
    return [table_template]


def repr_testresultholmbonferroni(result):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    return repr_holm_bonferroni(result, 'Holm-Bonferroni?')


def repr_holm_bonferroni(result, result_header):
    '''Reprensetation of Holm-Bonferroni test result.

    Only reprensents the Holm-Bonferroni result, not the input test result.

    :param result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    print("\x1b[31mOn est ici !\x1b[0m")
    ndatasets = len(result.first_test_res.test.datasets)
    oracles = list(result.oracles())
    highlights = [[False] * ndatasets] * 6  # 6 non-highlighted columns
    highlights.append([not oracle for oracle in oracles])
    table_template = TableTemplate(
        [result.first_test_res.test.name] * ndatasets,
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [min(pval) for pval in result.first_test_res.pvalue],
        [alpha_i[0] for alpha_i in result.alphas_i],
        list(result.nb_rejected),
        oracles,
        highlights=highlights,
        headers=['test', 'ndf', 'α', 'min(p-value)', 'min(α)',
                 'N rejected', result_header])
    print(table_template)
    return [table_template]


def repr_testresultholmbonferroni_silent(result):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test for the
    SILENT level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    print("C'est silent qui est choisi...")
    return repr_holm_bonferroni_silent(result)


def repr_holm_bonferroni_silent(result):
    '''Function to generate a silent table for the Holm-Bonferroni test (only
    tells if the test was successful or not).

    Different levels of verbosity should be allowed.
    '''
    if bool(result):
        return [TableTemplate(["Holm-Bonferroni test:"], ["OK"],
                              highlights=[[False], [False]])]
    return [TableTemplate(["Holm-Bonferroni test:"], ["KO"],
                          highlights=[[False], [True]])]


def repr_testresultholmbonferroni_summary(result):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test for the
    SUMMARY level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)
    '''
    print("C'est summary qui est choisi")
    return repr_holm_bonferroni(result, 'Holm-Bonferroni?')


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


def repr_testresultstatstasks(result):
    '''Represent a :class:`~.TestResultStatsTasks` as a table. The table
    breaks down the tasks by status.

    :param TestResultStatsTasks result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
    return repr_testresultstats(result, TaskStatus.DONE)


def repr_testresultstatstests(result):
    '''Represent a :class:`~.TestResultStatsTests` as a table. The table
    breaks down the tests by success status.

    :param TestResultStatsTests result: the test result to represent.
    :returns: the tables representing the test result.
    :rtype: list(TableTemplate)
    '''
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


def repr_testresultmetadata(result):
    '''Represent the result of a :class:`~.TestMetadata` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    Different levels of verbosity should be allowed.
    '''
    return repr_metadata(result)


def repr_metadata(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    if bool(result):
        return [TableTemplate(["Metadata:"], ["OK"],
                              highlights=[[False], [False]])]
    ko_list = list(result.only_failed_comparisons().keys())
    return [TableTemplate(["Failed metadata:"], [', '.join(ko_list)],
                          highlights=[[False], [True]])]


def repr_testresultmetadata_full_details(result):
    # pylint: disable=invalid-name
    '''Represent the result of a :class:`~.TestMetadata` test with all details.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    "All details" means the full list of metadata will be represented, the
    missing ones and the different ones should be highlighted.
    '''
    return repr_metadata_full_details(result)


def repr_metadata_full_details(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    samp_names = [name for name in result.test.dmd.keys()]
    keys = []
    tdict = {name: [] for name in samp_names}
    hdict = {name: [] for name in samp_names}
    for dkey in result.test.all_md.keys():
        keys.append(dkey)
        for nam in samp_names:
            tdict[nam].append(str(result.test.all_md[dkey][nam]))
            hdict[nam].append(not result.dict_res[dkey][nam])
    ocols = [col for col in tdict.values()]
    highl = [[False]*len(keys)]
    highl.extend([hl for hl in hdict.values()])
    heads = ['key']
    heads.extend([name for name in result.test.dmd.keys()])
    table = TableTemplate(keys, *ocols,
                          highlights=highl,
                          headers=heads)
    return [table]


def repr_testresultmetadata_intermediate(result):
    # pylint: disable=invalid-name
    '''Represent the result of a :class:`~.TestMetadata` test with an
    intermediate level of verbosity.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    "Intermediate level of verbosity" means the list of metadata failing
    comparison will be represented. The comparison can fail for example if one
    is missing or if an name changed.
    '''
    return repr_metadata_intermediate(result)


def repr_metadata_intermediate(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    if not result.only_failed_comparisons():
        return repr_metadata_silent(result)
    samp_names = [name for name in result.test.dmd.keys()]
    keys = []
    tdict = {name: [] for name in samp_names}
    hdict = {name: [] for name in samp_names}
    for dkey in result.only_failed_comparisons():
        keys.append(dkey)
        for nam in samp_names:
            tdict[nam].append(str(result.only_failed_comparisons()[dkey][nam]))
            hdict[nam].append(not result.dict_res[dkey][nam])
    ocols = [col for col in tdict.values()]
    highl = [[False]*len(keys)]
    highl.extend([hl for hl in hdict.values()])
    heads = ['key']
    heads.extend([name for name in result.test.dmd.keys()])
    table = TableTemplate(keys, *ocols,
                          highlights=highl,
                          headers=heads)
    return [table]


def repr_testresultmetadata_summary(result):
    '''Represent the result of a :class:`~.TestMetadata` with a summary over
    all metadata.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    "Summary over all metadata" means the list of metadata with OK if
    comparison was successful else KO.
    '''
    return repr_metadata_summary(result)


def repr_metadata_summary(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    keys = list(result.per_key().keys())
    vals = ["OK" if res else "KO" for res in result.per_key().values()]
    highl = [[False]*len(keys)]
    highl.extend([[not res for res in result.per_key().values()]])
    table = TableTemplate(
        keys, vals,
        highlights=highl,
        headers=['metadata', '?'])
    return [table]


def repr_testresultmetadata_silent(result):
    '''Represent the result of a :class:`~.TestMetadata` with silent verbosity
    level.

    :param  result: a test result.
    :type result: :class:`~.TestResultMetadata`
    :returns: Representation of a :class:`~.TestResultMetadata` as a
        table.
    :rtype: :class:`list` (:class:`~.TableTemplate`)

    "Silent verbosity level" means that the comparison of all metadata gives a
    OK if everything was fine, else a KO. To get more details, please use a
    different level of verbosity.
    '''
    return repr_metadata_silent(result)


def repr_metadata_silent(result):
    '''Function to generate a table from the metadata test results.

    Different levels of verbosity should be allowed.
    '''
    if bool(result):
        return [TableTemplate(["Metadata:"], ["OK"],
                              highlights=[[False], [False]])]
    return [TableTemplate(["Metadata:"], ["KO"],
                          highlights=[[False], [True]])]
