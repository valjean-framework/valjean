'''Tests for the :mod:`~javert.rst` module.'''
# pylint: disable=unused-argument,redefined-outer-name

import numpy as np
from hypothesis import given, note

# pylint: disable=wrong-import-order
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.rst import RstTable
from .conftest import int_matrices
from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 equal_test_result, equal_test_fail,
                                 equal_test_result_fail, approx_equal_test,
                                 approx_equal_test_result, different_dataset)


@given(matrix=int_matrices())  # pylint: disable=no-value-for-parameter
def test_rsttable_col_widths(matrix):
    '''Check that :meth:`RstTable.compute_column_widths` correctly computes the
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


def test_rst_equal(rstcheck, equal_test_result, rst_formatter, full_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test.'''
    items = full_repr(equal_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_equal_hl(rstcheck, equal_test_result_fail, rst_formatter,
                      full_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test with highlighted elements.'''
    items = full_repr(equal_test_result_fail)
    rst = '\n'.join(rst_formatter(item) for item in items)
    # patch the generated rst with a declaration for the highlight role
    rst = '.. role:: hl\n\n' + rst
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_approx_equal(rstcheck, approx_equal_test_result, rst_formatter,
                          full_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an approximate equality test.'''
    items = full_repr(approx_equal_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
