'''Tests for the :mod:`~valjean.javert.mpl` module.'''
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

import pytest
import numpy as np
from hypothesis import given, settings, HealthCheck
from valjean.javert.items import PlotItem, concatenate, TableItem, FullPlotItem
from valjean.javert.mpl import MplPlot, MplPlot2
from ..gavroche.conftest import (some_1d_dataset, one_dim_dataset,
                                 other_1d_dataset, some_1d_dataset_edges,
                                 other_1d_dataset_edges, different_1d_dataset)
from ..gavroche.conftest import (student_test, student_test_result,
                                 student_test_fail, student_test_result_fail,
                                 student_test_edges, student_test_edges_result)


def test_plot_1d_dataset(some_1d_dataset):
    '''Test plot of 1-D dataset.'''
    # print(some_1d_dataset)
    plti = PlotItem(some_1d_dataset.value, some_1d_dataset.bins['e'])
    assert plti.vals.size == plti.bins.size
    # mplt = MplPlot(plti)
    # mplt.show()


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_bins_edges(oneds):
    '''Test plot where bins are given by edges.'''
    # print(oneds)
    # print(settings().max_examples)
    dim = list(oneds.bins.keys())[0]
    plti = PlotItem(oneds.value, oneds.bins[dim], xname=dim, yname='score')
    assert (plti.vals.size == plti.bins.size
            or plti.vals.size+1 == plti.bins.size)
    # # if oneds.bins[dim].size == oneds.value.size+1:
    # #     assert plti.bins.size == oneds.bins[dim].size-1
    # #     assert plti.xerrors.size == plti.vals.size
    # # else:
    # #     assert plti.xerrors is None
    # mplt = MplPlot(plti)
    # # print(mplt.splt.nrows)
    # # print(mplt.splt.__class__)
    # # print(type(mplt.the_plot), mplt.the_plot.__class__)
    # # print(mplt.the_plot)
    # # print(mplt.the_plot)
    # mplt.show()


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_with_errors(oneds):
    '''Test plot where bins are given by edges.'''
    # print(oneds)
    # print(settings().max_examples)
    dim = list(oneds.bins.keys())[0]
    # print(oneds.error)
    plti = PlotItem(oneds.value, oneds.bins[dim], yerrors=oneds.error,
                    xname=dim, yname='score')
    assert oneds.error.size == oneds.value.size
    assert plti.xname == dim
    # mplt = MplPlot(plti)
    # mplt.show()


@pytest.mark.mpl_image_compare(filename='plot_reg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show():
    '''Test with matplotlib test.'''
    plti = PlotItem(np.arange(5), np.arange(6), xname='X', yname='Y')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Simple plot')
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='plot_irreg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show_irreg_bins():
    '''Test with matplotlib test.'''
    plti = PlotItem(np.arange(5), np.array([0, 2, 3, 6, 7, 10]),
                    xname='X', yname='Y')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Plot irregular bins')
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_plot.png',
                               baseline_dir='ref_plots')
def test_student_plot(student_test_result, plot_repr):
    '''Test plot of student result.'''
    items = plot_repr(student_test_result, dim='e', plot_res=True)
    mplt = MplPlot(items[-1])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_points.png',
                               baseline_dir='ref_plots')
def test_student_full(student_test_result, full_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    items = full_repr(student_test_result, dim='e', plot_res=True)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='ref_plots')
def test_student_edges_full(student_test_edges_result, full_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    items = full_repr(student_test_edges_result, dim='e', plot_res=True)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi(student_test_result, fplt_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_result, dim='e')
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi(student_test_edges_result, fplt_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_edges_result, dim='e')
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi_delta.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi_d(student_test_result, fplt_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_result, dim='e', only_res=True)
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi_values.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi_v(student_test_edges_result, fplt_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_edges_result, dim='e', only_values=True)
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


def test_fplit_cc(student_test_result, fplt_repr):
    '''Test copy of FullPlotItem from student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_result, dim='e')
    item2 = item.copy()
    assert id(item.bins) != id(item2.bins)
    assert id(item.values) != id(item2.values)
    assert id(item.labels) != id(item2.labels)
    assert id(item.ynames) != id(item2.ynames)
    assert id(item.errors) != id(item2.errors)
    assert ([id(val) for val in item.values]
            != [id(val) for val in item2.values])
    assert all([id(err1) != id(err2)
                for err1, err2 in zip(item.errors, item2.errors)
                if err1 is not None and err2 is not None])
    # xname is a string -> point to same address
    # but can be updated independently
    assert id(item.xname) == id(item2.xname)
    item.xname = 'f'
    assert id(item.xname) != id(item2.xname) and item.xname != item2.xname


def test_fplit_iadd(student_test_result, student_test_result_fail, fplt_repr):
    '''Test addition of FullPlotItem from student result.'''
    item = fplt_repr(student_test_result, dim='e')
    item_cc = item.copy()
    item2 = fplt_repr(student_test_result_fail, dim='e')
    item += item2
    assert item.xname == item2.xname
    assert len(item.values) == len(item_cc.values) + len(item2.values)
    assert len(item.labels) == len(item_cc.labels) + len(item2.labels)
    assert item.ynames[:len(item_cc.ynames)] == item2.ynames


def test_fplit_add(student_test_result, student_test_result_fail, fplt_repr):
    '''Test addition of FullPlotItem from student result.'''
    item1 = fplt_repr(student_test_result, dim='e')
    item2 = fplt_repr(student_test_result_fail, dim='e')
    item3 = item1 + item2
    assert item3.xname == item1.xname
    assert item3.xname == item2.xname
    assert len(item3.values) == len(item1.values) + len(item2.values)
    assert len(item3.labels) == len(item1.labels) + len(item2.labels)
    assert item3.ynames[:len(item1.ynames)] == item2.ynames
    assert item3.ynames[len(item1.ynames):] == item1.ynames


def test_full_concatenation(student_test_result, student_test_result_fail,
                            full_repr2):
    '''Test concatenation of all items.'''
    item1 = full_repr2(student_test_result, dim='e')
    item2 = full_repr2(student_test_result_fail, dim='e')
    items3 = concatenate(item1 + item2)
    assert len(items3) == 3
    assert [isinstance(it, TableItem) for it in items3] == [True, False, True]
    assert ([isinstance(it, FullPlotItem) for it in items3]
            == [False, True, False])
