'''Tests for the :mod:`~valjean.javert.rst` module.'''
# pylint: disable=unused-argument,redefined-outer-name

import numpy as np
from hypothesis import given, note

# pylint: disable=wrong-import-order
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.rst import RstTable
from valjean.javert.items import join
from .conftest import int_matrices
from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 equal_test_result, equal_test_fail,
                                 equal_test_result_fail, approx_equal_test,
                                 approx_equal_test_result, different_dataset,
                                 student_test, student_test_result,
                                 some_1d_dataset, other_1d_dataset,
                                 student_test_fail, student_test_result_fail,
                                 different_1d_dataset, bonferroni_test,
                                 bonferroni_test_result,
                                 student_test_with_pvalues,
                                 bonferroni_test_fail,
                                 bonferroni_test_result_fail,
                                 student_test_fail_with_pvalues,
                                 holm_bonferroni_test,
                                 holm_bonferroni_test_result,
                                 holm_bonferroni_test_fail,
                                 holm_bonf_test_result_fail)


@given(matrix=int_matrices())  # pylint: disable=no-value-for-parameter
def test_rsttable_col_widths(matrix):
    '''Check that :meth:`RstTable.compute_column_widths
    <valjean.javert.rst.RstTable.compute_column_widths>` correctly computes the
    column widths for rows with known shapes.'''
    expected = np.amax(matrix, axis=0)
    headers = ['☺'*n for n in matrix[0, :]]
    note('headers: {}'.format(headers))
    rows = [['☹'*n for n in row] for row in matrix[1:, :]]
    note('rows: {}'.format(rows))
    result = RstTable.compute_column_widths(headers, rows)
    note('expecting: {}'.format(expected))
    note('result: {}'.format(result))
    assert np.equal(expected, result).all()


def test_rst_table(rstcheck, table_item, rst_formatter):
    '''Test that :class:`~.RstFormatter` generates correct reST tables.'''
    table = rst_formatter(table_item)
    LOGGER.debug('generated rst:\n%s', table)
    errs = rstcheck.check(table)
    assert not list(errs)


def test_rst_equal(rstcheck, equal_test_result, rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test.'''
    items = table_repr(equal_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_equal_full(rstcheck, equal_test_result, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test.'''
    items = table_repr(equal_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_equal_hl(rstcheck, equal_test_result_fail, rst_formatter,
                      table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test with highlighted elements.'''
    items = table_repr(equal_test_result_fail)
    rst = '\n'.join(rst_formatter(item) for item in items)
    # patch the generated rst with a declaration for the highlight role
    rst = '.. role:: hl\n\n' + rst
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_approx_equal(rstcheck, approx_equal_test_result, rst_formatter,
                          table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an approximate equality test.'''
    items = table_repr(approx_equal_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_student(rstcheck, student_test_result, rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table.'''
    items = table_repr(student_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_student_hl(rstcheck, student_test_result_fail, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Student results.'''
    items = table_repr(student_test_result_fail)
    rst = '\n'.join(rst_formatter(item) for item in items)
    # patch the generated rst with a declaration for the highlight role
    rst = '.. role:: hl\n\n' + rst
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_bonferroni(rstcheck, bonferroni_test_result, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Bonferroni result.'''
    items = table_repr(bonferroni_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_holm_bonferroni(rstcheck, holm_bonferroni_test_result,
                             rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Holm-Bonferroni results.'''
    items = table_repr(holm_bonferroni_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_more_bonferronis(rstcheck, bonferroni_test_result,
                              bonferroni_test_result_fail, rst_formatter,
                              table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Bonferroni result.'''
    items = table_repr(bonferroni_test_result)
    items2 = table_repr(bonferroni_test_result_fail)
    ntabitem = items + items2
    rst = rst_formatter(ntabitem)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_holm_bonferronis(rstcheck, holm_bonferroni_test_result,
                              holm_bonf_test_result_fail, rst_formatter,
                              table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Holm-Bonferroni results.'''
    items = table_repr(holm_bonferroni_test_result)
    items2 = table_repr(holm_bonf_test_result_fail)
    ntabitem = items + items2
    rst = rst_formatter(ntabitem)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_tableitem_tjoin(rstcheck, rst_formatter, table_repr,
                         bonferroni_test_result, bonferroni_test_result_fail):
    '''Test :meth:`~valjean.javert.items.TableItem.join`.'''
    items = table_repr(bonferroni_test_result)
    items_id = id(items[1])
    LOGGER.debug("items = %s", items)
    items2 = table_repr(bonferroni_test_result_fail)
    LOGGER.debug("items2 = %s", items2)
    items[1].join(items2[1])
    LOGGER.debug("items+items2 = %s", items)
    assert id(items[1]) != id(items2[1])
    assert id(items[1]) == items_id
    assert all(tuple((row[0] in items[1].columns[i]
                      for i, row in enumerate(items2[1].columns))))


def test_tableitem_join(rstcheck, rst_formatter, table_repr,
                        bonferroni_test_result, bonferroni_test_result_fail):
    '''Test  :meth:`~valjean.javert.items.join`.'''
    items1 = table_repr(bonferroni_test_result)
    LOGGER.debug("items1 = %s", items1)
    items2 = table_repr(bonferroni_test_result_fail)
    LOGGER.debug("items2 = %s", items2)
    items3 = join(items1[1], items2[1])
    LOGGER.debug("items1+items2 = %s", items3)
    assert id(items1[1]) != id(items2[1])
    assert id(items1[1]) != id(items3)
    assert id(items2[1]) != id(items3)
    # check the 2 results are not identical = contains some different elements
    assert any(tuple((row[0] not in items2[1].columns[i]
                      for i, row in enumerate(items1[1].columns))))
    # items1 column elements are all in items3
    assert all(tuple((row[0] in items3.columns[i]
                      for i, row in enumerate(items1[1].columns))))
    # items2 column elements are all in items3
    assert all(tuple((row[0] in items3.columns[i]
                      for i, row in enumerate(items2[1].columns))))
    items4 = items1 + items2
    LOGGER.debug("items1+items2 = %s", items4)
    assert len(items4) == 4
    items5 = [join(it1, it2) for it1, it2 in zip(items1, items2)]
    LOGGER.debug("items1+items2 = %s", items5)
    assert len(items5) == 2
    assert items5[0].headers[-1] == 'Student?'
    assert items5[0].columns[0].size == 10
    assert items5[1].headers[-1] == 'Bonferroni?'


def test_tableitem_join_array(table_repr,
                              student_test_result,
                              student_test_result_fail):
    '''Test join table items containing arrays.'''
    item1 = table_repr(student_test_result)
    item1_cc = item1[0].copy()
    LOGGER.debug('item1 = %s', item1)
    item2 = table_repr(student_test_result_fail)
    LOGGER.debug('item2 = %s', item2)
    item1[0].join(item2[0])
    LOGGER.debug('after join: item1 = %s', item1)
    assert item1[0].headers == item1_cc.headers
    assert item1[0].headers == item2[0].headers
    assert all(col.size == col1.size + col2.size
               for col, col1, col2 in zip(item1[0].columns, item1_cc.columns,
                                          item2[0].columns))
    assert all(np.isin(item1[0].columns[4][item1_cc.columns[4].size:],
                       item2[0].columns[4]))
    assert all(np.isin(item1[0].columns[4][:item1_cc.columns[4].size],
                       item1_cc.columns[4]))
