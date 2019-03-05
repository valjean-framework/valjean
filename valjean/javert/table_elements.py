'''Module containing all available methods to convert a test result in a table
to be converted in rst.
'''
from .. import LOGGER
from .items import TableItem


def repr_testresultequal(result):
    '''Represent the result of a :class:`~.TestEqual` test.

    :param result: a test result.
    :type result: :class:`~.TestResultEqual`
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    return repr_equal(result, 'equal?')


def repr_equal(result, result_header):
    '''Representation of equal test.

    :param result: a test result.
    :type result: :class:`~.TestResultEqual`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultEqual` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    LOGGER.debug('shape of the result: %s', result.equal.shape)
    table_item = TableItem(result.test.dataset1.value,
                           result.test.dataset2.value,
                           result.equal,
                           highlight=lambda _v1, _v2, eq: not eq,
                           headers=['reference', 'dataset', result_header])
    return [table_item]


def repr_testresultapproxequal(result):
    '''Represent the result of a :class:`~.TestApproxEqual` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    return repr_approx_equal(result, 'approx equal?')


def repr_approx_equal(result, result_header):
    '''Representation of approx equal test.

    :param result: a test result.
    :type result: :class:`~.TestResultApproxEqual`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultApproxEqual` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    LOGGER.debug('shape of the result: %s', result.approx_equal.shape)
    table_item = TableItem(result.test.dataset1.value,
                           result.test.dataset2.value,
                           result.approx_equal,
                           highlight=lambda _v1, _v2, eq: not eq,
                           headers=['reference', 'dataset', result_header])
    return [table_item]


def repr_testresultstudent(result):
    '''Represent the result of a :class:`~.TestStudent` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultStudent`
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    return repr_student(result, 'Student?')


def repr_student(result, result_header):
    '''Reprensetation of Student test result.

    :param result: a test result.
    :type result: :class:`~.TestResultStudent`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultStudent` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    table_item = TableItem(
        result.test.ds1.value, result.test.ds1.error,
        result.test.ds2.value, result.test.ds2.error,
        result.delta, result.bool_array(),
        highlight=lambda _v1, _e1, _v2, _e2, _delta, eq: not eq,
        headers=['v1', 'σ1', 'v2', 'σ2', 'Δ', result_header])
    return [table_item]


def repr_testresultbonferroni(result):
    '''Represent the result of a :class:`~.TestBonferroni` test.

    Only reprensents the Bonferroni result, not the input test result.

    :param  result: a test result.
    :type result: :class:`~.TestResultBonferroni`
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    return repr_bonferroni(result, 'Bonferroni?')


def repr_bonferroni(result, result_header):
    '''Reprensetation of Bonferroni test result.

    Only reprensents the Bonferroni result, not the input test result.

    :param result: a test result.
    :type result: :class:`~.TestResultBonferroni`
    :param str result_header: result header appearing in the table
    :returns: Representation of a :class:`~.TestResultBonferroni` as a table.
    :rtype: list(:class:`~.TableItem`)
    '''
    table_item = TableItem(
        [result.first_test_res.test.name],
        [result.test.ntests],
        [result.test.alpha],
        [min(result.first_test_res.pvalue)],
        [bool(result)],
        highlight=lambda _t, _ndf, _sl, _min, rnh: not rnh,
        headers=['test', 'ndf', 'α', 'min(p-value)', result_header])
    return [table_item]


def repr_testresultholmbonferroni(result):
    '''Represent the result of a :class:`~.TestHolmBonferroni` test.

    :param  result: a test result.
    :type result: :class:`~.TestResultHolmBonferroni`
    :returns: Representation of a :class:`~.TestResultHolmBonferroni` as a
        table.
    :rtype: list(:class:`~.TableItem`)
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
    :rtype: list(:class:`~.TableItem`)
    '''
    table_item = TableItem(
        [result.first_test_res.test.name],
        [result.test.ntests],
        [result.test.alpha],
        [min(result.first_test_res.pvalue)],
        [result.alphas_i[0]],
        [result.nb_rejected],
        [bool(result)],
        highlight=lambda _t, _ndf, _sl, _min, _malp, _rej, rnh: not rnh,
        headers=['test', 'ndf', 'α', 'min(p-value)', 'min(α)',
                 'N rejected', result_header])
    return [table_item]
