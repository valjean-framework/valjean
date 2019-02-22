'''Tests for the :mod:`~javert.mpl` module.'''
# pylint: disable=redefined-outer-name

import pytest
import numpy as np
from hypothesis import given, settings, HealthCheck
from ..gavroche.conftest import (some_1d_dataset, one_dim_dataset,
                                 other_1d_dataset, some_1d_dataset_edges,
                                 other_1d_dataset_edges)
from valjean.javert.items import PlotItem
from valjean.javert.mpl import MplPlot, MplPlot2
from ..gavroche.conftest import (student_test, student_test_result,
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
    # mplt = MplPlot(plti)
    # mplt.show()


# @image_comparison(baseline_images=["/home/el220326/valjean/tests/javert/data/my_baseline_image.png"])
@pytest.mark.mpl_image_compare(filename='monplot.png',
                               baseline_dir='mes_plots')
def test_plot_with_matplotlib():
    '''Test with matplotlib test.'''
    plti = PlotItem(np.arange(5), np.arange(5), xname='X', yname='Y')
    mplt = MplPlot(plti)
    mplt.splt.set_title('my test')
    return mplt.fig
    # mplt.save("/home/el220326/valjean/tests/javert/data/monplot.png")
    # mpl = mplt.plt()


@pytest.mark.mpl_image_compare(filename='plot_reg_bins.png',
                               baseline_dir='mes_plots')
def test_plot_show():
    '''Test with matplotlib test.'''
    plti = PlotItem(np.arange(5), np.arange(6), xname='X', yname='Y')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Simple plot')
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='plot_irreg_bins.png',
                               baseline_dir='mes_plots')
def test_plot_show_irreg_bins():
    '''Test with matplotlib test.'''
    plti = PlotItem(np.arange(5), np.array([0, 2, 3, 6, 7, 10]),
                    xname='X', yname='Y')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Plot irregular bins')
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_plot.png',
                               baseline_dir='mes_plots')
def test_student_plot(student_test_result, plot_repr):
    '''Test plot of student result.'''
    items = plot_repr(student_test_result, dim='e', plot_res=True)
    mplt = MplPlot(items[-1])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_points.png',
                               baseline_dir='mes_plots')
def test_student_full(student_test_result, full_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    items = full_repr(student_test_result, dim='e', plot_res=True)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='mes_plots')
def test_student_edges_full(student_test_edges_result, full_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    items = full_repr(student_test_edges_result, dim='e', plot_res=True)
    mplt = MplPlot([item for item in items if isinstance(item, PlotItem)])
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi.png',
                               baseline_dir='mes_plots')
def test_student_with_fpi(student_test_result, fplt_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_result, dim='e')
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi.png',
                               baseline_dir='mes_plots')
def test_student_edges_with_fpi(student_test_edges_result, fplt_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_edges_result, dim='e')
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi_delta.png',
                               baseline_dir='mes_plots')
def test_student_with_fpi_d(student_test_result, fplt_repr):
    '''Test plot of student result.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_result, dim='e', only_res=True)
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi_values.png',
                               baseline_dir='mes_plots')
def test_student_edges_with_fpi_v(student_test_edges_result, fplt_repr):
    '''Test plot of student result when bins are given by edges.'''
    # items = full_repr(student_test_result, dim='e')
    item = fplt_repr(student_test_edges_result, dim='e', only_values=True)
    mplt = MplPlot2(item)
    # mplt.show()
    return mplt.fig
