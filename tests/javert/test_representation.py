'''Tests for the :mod:`~valjean.javert.representation` module.'''
# pylint: disable=redefined-outer-name
# pylint: disable=wrong-import-order

import pytest

from ..context import valjean  # pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.items import TableItem, PlotItem, concatenate
from valjean.javert.representation import (TableRepresentation,
                                           EmptyRepresentation)
from valjean.javert.mpl import MplPlot

from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 approx_equal_test, some_1d_dataset,
                                 other_1d_dataset, different_1d_dataset,
                                 some_1d_dataset_edges, other_1d_dataset_edges,
                                 student_test, student_test_result,
                                 student_test_edges, student_test_edges_result,
                                 student_test_fail, student_test_result_fail)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_full_repr(test_name, request):
    '''Test that :class:`~.FullRepresentation` yields all the expected items
    for equality tests.'''
    test = request.getfixturevalue(test_name)
    representation = TableRepresentation()
    items = representation(test.evaluate())
    assert isinstance(items, list)
    assert any(isinstance(item, TableItem) for item in items)


@pytest.mark.mpl_image_compare(filename='student_comp_points.png',
                               baseline_dir='ref_plots')
def test_student_full(student_test_result, full_repr, rst_formatter, rstcheck):
    '''Test plot of student resultwhen  bins are given by centers of bins.'''
    items = full_repr(student_test_result)
    rst = '\n'.join(rst_formatter(item) for item in items
                    if isinstance(item, TableItem))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)][0])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='ref_plots')
def test_student_edges_full(student_test_edges_result, full_repr,
                            rst_formatter, rstcheck):
    '''Test plot of student result when bins are given by edges.'''
    items = full_repr(student_test_edges_result)
    rst = '\n'.join(rst_formatter(item) for item in items
                    if isinstance(item, TableItem))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)][0])
    return mplt.fig


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_empty_repr(test_name, request):
    '''Test that :class:`~.EmptyRepresentation` yields no items for equality
    tests.'''
    test = request.getfixturevalue(test_name)
    representation = EmptyRepresentation()
    items = representation(test.evaluate())
    assert isinstance(items, list)
    assert not items


def test_full_concatenation(student_test_result, student_test_result_fail,
                            full_repr):
    '''Test concatenation of all items.'''
    item1 = full_repr(student_test_result)
    item2 = full_repr(student_test_result_fail)
    items3 = concatenate(item1 + item2)
    assert len(items3) == 2
    assert [isinstance(it, TableItem) for it in items3] == [True, False]
    assert [isinstance(it, PlotItem) for it in items3] == [False, True]
