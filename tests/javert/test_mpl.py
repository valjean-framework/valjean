'''Tests for the :mod:`~valjean.javert.mpl` module.'''
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

import pytest
import numpy as np
from hypothesis import given, settings, HealthCheck
from valjean.javert.items import (PlotItem, concatenate, TableItem,
                                  CurveElements)
from valjean.javert.mpl import MplPlot
from ..gavroche.conftest import (some_1d_dataset, one_dim_dataset,
                                 other_1d_dataset, some_1d_dataset_edges,
                                 other_1d_dataset_edges, different_1d_dataset)
from ..gavroche.conftest import (student_test, student_test_result,
                                 student_test_fail, student_test_result_fail,
                                 student_test_edges, student_test_edges_result)


def test_plot_1d_dataset(some_1d_dataset):
    '''Test plot of 1-D dataset.'''
    # print(some_1d_dataset)
    plti = PlotItem(bins=some_1d_dataset.bins['e'],
                    curves=[CurveElements(some_1d_dataset.value, '')])
    assert plti.curves[0].values.size == plti.bins.size
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
    pelt = CurveElements(oneds.value, label='', yname='score')
    plti = PlotItem(bins=oneds.bins[dim], curves=[pelt], xname=dim)
    assert (plti.curves[0].values.size == plti.bins.size
            or plti.curves[0].values.size+1 == plti.bins.size)
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
    pelt = CurveElements(oneds.value, label='', yname='score',
                         errors=oneds.error)
    plti = PlotItem(bins=oneds.bins[dim], curves=[pelt], xname=dim)
    assert oneds.error.size == oneds.value.size
    assert plti.xname == dim
    # mplt = MplPlot(plti)
    # mplt.show()


@pytest.mark.mpl_image_compare(filename='plot_reg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), label='', yname='Y')
    plti = PlotItem(bins=np.arange(6), curves=[pelt], xname='X')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Simple plot')
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='plot_irreg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show_irreg_bins():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), label='', yname='Y')
    plti = PlotItem(bins=np.array([0, 2, 3, 6, 7, 10]), xname='X',
                    curves=[pelt])
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
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)][0])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='ref_plots')
def test_student_edges_full(student_test_edges_result, full_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    items = full_repr(student_test_edges_result, dim='e', plot_res=True)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)][0])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi(student_test_result, plot_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = plot_repr(student_test_result, dim='e')
    mplt = MplPlot(item[0])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi(student_test_edges_result, plot_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = plot_repr(student_test_edges_result, dim='e')
    mplt = MplPlot(item[0])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi_delta.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi_d(student_test_result, plot_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = plot_repr(student_test_result, dim='e', only_res=True)
    mplt = MplPlot(item[0])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi_values.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi_v(student_test_edges_result, plot_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = plot_repr(student_test_edges_result, dim='e', only_values=True)
    mplt = MplPlot(item[0])
    # mplt.show()
    return mplt.fig


def test_fplit_cc(student_test_result, plot_repr):
    '''Test copy of FullPlotItem from student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = plot_repr(student_test_result, dim='e')[0]
    item2 = item.copy()
    assert id(item.bins) != id(item2.bins)
    assert id(item.curves) != id(item2.curves)
    assert ([id(c.values) for c in item.curves]
            != [id(c.values) for c in item2.curves])
    assert all([id(c1.errors) != id(c2.errors)
                for c1, c2 in zip(item.curves, item2.curves)
                if c1.errors is not None and c2.errors is not None])
    # xname is a string -> point to same address
    # but can be updated independently
    assert id(item.xname) == id(item2.xname)
    item.xname = 'f'
    assert id(item.xname) != id(item2.xname) and item.xname != item2.xname


def test_fplit_iadd(student_test_result, student_test_result_fail, plot_repr):
    '''Test addition of FullPlotItem from student result.'''
    item = plot_repr(student_test_result, dim='e')[0]
    item_cc = item.copy()
    item2 = plot_repr(student_test_result_fail, dim='e')[0]
    item += item2
    assert item.xname == item2.xname
    assert len(item.curves) == len(item_cc.curves) + len(item2.curves)
    assert ([c.yname for c in item.curves][:len(item_cc.curves)]
            == [c.yname for c in item2.curves])


@pytest.mark.mpl_image_compare(filename='student_fplit_add.png',
                               baseline_dir='ref_plots')
def test_fplit_add(student_test_result, student_test_result_fail, plot_repr):
    '''Test addition of FullPlotItem from student result.'''
    item1 = plot_repr(student_test_result, dim='e')[0]
    item2 = plot_repr(student_test_result_fail, dim='e')[0]
    item3 = item1 + item2
    assert item3.xname == item1.xname
    assert item3.xname == item2.xname
    assert len(item3.curves) == len(item1.curves) + len(item2.curves)
    assert ([c.yname for c in item3.curves][:len(item1.curves)]
            == [c.yname for c in item2.curves])
    assert ([c.yname for c in item3.curves][len(item1.curves):]
            == [c.yname for c in item1.curves])
    mplt = MplPlot(item3)
    # mplt.show()
    return mplt.fig


def test_full_concatenation(student_test_result, student_test_result_fail,
                            full_repr):
    '''Test concatenation of all items.'''
    item1 = full_repr(student_test_result, dim='e')
    item2 = full_repr(student_test_result_fail, dim='e')
    items3 = concatenate(item1 + item2)
    assert len(items3) == 3
    assert [isinstance(it, TableItem) for it in items3] == [True, False, True]
    assert ([isinstance(it, PlotItem) for it in items3]
            == [False, True, False])
