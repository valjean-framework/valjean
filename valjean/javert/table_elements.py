'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from itertools import chain
from .. import LOGGER
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
    table_template = TableTemplate(
        result.test.dsref.value,
        *chain.from_iterable(dscols),
        highlight=lambda *cols: any([not col for col in cols
                                     if col.dtype == 'bool']),
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
    table_template = TableTemplate(
        result.test.dsref.value,
        *chain.from_iterable(dscols),
        highlight=lambda *cols: any([not col for col in cols
                                     if col.dtype == 'bool']),
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
    dscols = tuple((ds.value, ds.error, delta, studbool)
                   for ds, delta, studbool in zip(result.test.datasets,
                                                  result.delta,
                                                  result.oracles()))
    heads = [('v_ref', 'σ_ref')]
    for ids in range(len(dscols)):
        str_ids = str(ids)
        heads.append(('v'+str_ids, 'σ'+str_ids, 'Δ'+str_ids,
                      result_header.replace('?', str_ids+'?'))
                     if len(dscols) > 1
                     else ('v_test', 'σ_test', 'Δ_test', result_header))
    table_template = TableTemplate(
        result.test.dsref.value, result.test.dsref.error,
        *chain.from_iterable(dscols),
        highlight=lambda *cols: any([not col for col in cols
                                     if col.dtype == 'bool']),
        headers=list(chain.from_iterable(heads)))
    return [table_template]


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
    table_template = TableTemplate(
        [result.first_test_res.test.name] * ndatasets,
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [result.test.bonf_signi_level] * ndatasets,
        [min(pval) for pval in result.first_test_res.pvalue],
        [res for res in result.oracles()],
        highlight=lambda _t, _ndf, _sl, _bsl, _min, rnh: not rnh,
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
    ndatasets = len(result.first_test_res.test.datasets)
    table_template = TableTemplate(
        [result.first_test_res.test.name] * ndatasets,
        [result.test.ntests] * ndatasets,
        [result.test.alpha] * ndatasets,
        [min(pval) for pval in result.first_test_res.pvalue],
        [alpha_i[0] for alpha_i in result.alphas_i],
        [nr for nr in result.nb_rejected],
        [res for res in result.oracles()],
        highlight=lambda _t, _ndf, _sl, _min, _malp, _rej, rnh: not rnh,
        headers=['test', 'ndf', 'α', 'min(p-value)', 'min(α)',
                 'N rejected', result_header])
    return [table_template]
