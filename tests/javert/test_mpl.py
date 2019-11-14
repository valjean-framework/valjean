'''Tests for the :mod:`~valjean.javert.mpl` module.

To prepare the test, i.e. to generate the reference plots:
``pytest --mpl-generate-path=PATH_TO_VALJEAN/tests/javert/ref_plots
tests/javert/test_mpl.py``.

To be sure the comparison with the reference plots is done, don't forget the
``--mpl`` option:
``pytest --mpl tests/javert/test_mpl.py``.
'''
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

from collections import namedtuple
import pytest
import numpy as np
from hypothesis import given, settings, HealthCheck, note
from hypothesis.strategies import just, integers, data, lists, text
from hypothesis.extra.numpy import array_shapes

from ..context import valjean  # pylint: disable=wrong-import-order

from valjean import LOGGER
from valjean.javert.templates import (PlotTemplate, join, TableTemplate,
                                      CurveElements)
from valjean.javert.mpl import MplPlot
from valjean.javert import plot_elements as plt_elts
from ..gavroche.conftest import (some_1d_dataset, one_dim_dataset,
                                 other_1d_dataset, some_1d_dataset_edges,
                                 other_1d_dataset_edges, different_1d_dataset)
from ..gavroche.conftest import (student_test, student_test_result,
                                 student_test_fail, student_test_result_fail,
                                 student_test_edges, student_test_edges_result,
                                 student_test_3ds, student_test_result_3ds,
                                 student_test_with_pvals,
                                 student_test_result_with_pvals)
from ..gavroche.conftest import datasets


def test_plot_1d_dataset(some_1d_dataset):
    '''Test plot of 1-D dataset.'''
    plti = PlotTemplate(bins=some_1d_dataset.bins['e'],
                        curves=[CurveElements(some_1d_dataset.value, '',
                                              index=0)])
    assert plti.curves[0].values.size == plti.bins.size


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_bins_edges(oneds):
    '''Test plot where bins are given by edges.'''
    dim = list(oneds.bins.keys())[0]
    pelt = CurveElements(oneds.value, label='', index=0, yname='score')
    plti = PlotTemplate(bins=oneds.bins[dim], curves=[pelt], xname=dim)
    assert (plti.curves[0].values.size == plti.bins.size
            or plti.curves[0].values.size+1 == plti.bins.size)


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_with_errors(oneds):
    '''Test plot where bins are given by edges.'''
    dim = list(oneds.bins.keys())[0]
    pelt = CurveElements(oneds.value, label='', index=0, yname='score',
                         errors=oneds.error)
    plti = PlotTemplate(bins=oneds.bins[dim], curves=[pelt], xname=dim)
    assert oneds.error.size == oneds.value.size
    assert plti.xname == dim


@given(sampler=data())
def test_pack_by_index(sampler):
    '''Test the :meth:`~valjean.javert.mpl.MplPlot.pack_by_index` static
    method.'''
    index = sampler.draw(lists(integers(min_value=0, max_value=5),
                               min_size=2, max_size=5))
    values = sampler.draw(lists(text(alphabet="AZERTYUIOP"), unique=True,
                                min_size=len(index), max_size=len(index)))
    ntcont = namedtuple('ntcont', ['index', 'value'])
    tmpdict = [ntcont(index=ind, value=val) for ind, val in zip(index, values)]
    packed_dict = MplPlot.pack_by_index(tmpdict)
    for ind, pdict in packed_dict.items():
        assert len(pdict) == len([i for i in index if i == ind])


@given(sampler=data())
def test_sbplts_by_yname(sampler):
    '''Test the :meth:`~valjean.javert.mpl.MplPlot.sbplts_by_yname` static
    method.'''
    ynames = sampler.draw(lists(text(alphabet="AZ", min_size=2, max_size=2),
                                min_size=2, max_size=5))
    values = sampler.draw(lists(integers(min_value=0, max_value=5),
                                min_size=len(ynames), max_size=len(ynames)))
    ntcont = namedtuple('ntcont', ['yname', 'value'])
    tmpdict = [ntcont(yname=yax, value=val)
               for yax, val in zip(ynames, values)]
    spltbn = MplPlot.sbplts_by_yname(tmpdict)
    for yax, cyax in spltbn.items():
        assert cyax[0] == ynames.count(yax)
        assert cyax[1] < len(set(ynames))


@pytest.mark.mpl_image_compare(filename='plot_reg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), label='', index=0, yname='Y')
    plti = PlotTemplate(bins=np.arange(6), curves=[pelt], xname='X')
    mplt = MplPlot(plti)
    mplt.splt.set_title('Simple plot')
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='plot_irreg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show_irreg_bins():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), label='', index=0, yname='Y')
    plti = PlotTemplate(bins=np.array([0, 2, 3, 6, 7, 10]), xname='X',
                        curves=[pelt])
    mplt = MplPlot(plti)
    mplt.splt.set_title('Plot irregular bins')
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_plot.png',
                               baseline_dir='ref_plots')
def test_student_plot(student_test_result, plot_repr):
    '''Test plot of Student result.'''
    templates = plot_repr(student_test_result)
    mplt = MplPlot(templates[-1])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi(student_test_result, plot_repr):
    '''Test plot of Student result.'''
    template = plot_repr(student_test_result)
    mplt = MplPlot(template[0])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi(student_test_edges_result, plot_repr):
    '''Test plot of Student result when bins are given by edges.'''
    template = plot_repr(student_test_edges_result)
    mplt = MplPlot(template[0])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_wfpi_delta.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi_d(student_test_result):
    '''Test plot of Student result.'''
    template = plt_elts.repr_student_delta(student_test_result)
    mplt = MplPlot(template[0])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi_values.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi_v(student_test_edges_result):
    '''Test plot of Student result when bins are given by edges.'''
    template = plt_elts.repr_student_values(student_test_edges_result)
    mplt = MplPlot(template[0])
    return mplt.fig


def test_fplit_cc(student_test_result, plot_repr):
    '''Test copy of FullPlotTemplate from Student result.'''
    template = plot_repr(student_test_result)[0]
    template2 = template.copy()
    assert id(template.bins) != id(template2.bins)
    assert id(template.curves) != id(template2.curves)
    assert ([id(c.values) for c in template.curves]
            != [id(c.values) for c in template2.curves])
    assert all([id(c1.errors) != id(c2.errors)
                for c1, c2 in zip(template.curves, template2.curves)
                if c1.errors is not None and c2.errors is not None])
    # xname is a string -> point to same address
    # but can be updated independently
    assert id(template.xname) == id(template2.xname)
    template.xname = 'f'
    assert (id(template.xname) != id(template2.xname)
            and template.xname != template2.xname)


@pytest.mark.mpl_image_compare(filename='student_fplit_3ds.png',
                               baseline_dir='ref_plots')
def test_fplit_3ds(student_test_result_3ds, plot_repr):
    '''Test concatenation of FullPlotTemplate from Student result.'''
    templ = plot_repr(student_test_result_3ds)[0]
    assert set(c.yname for c in templ.curves) == {'', r'$t_{Student}$'}
    assert len([c for c in templ.curves if c.yname == '']) == 3
    assert (len([c for c in templ.curves if c.yname == r'$t_{Student}$'])
            == 2)
    mplt = MplPlot(templ)
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_fplit_add.png',
                               baseline_dir='ref_plots')
def test_fplit_pjoin(student_test_result_with_pvals, plot_repr):
    '''Test concatenation of PlotTemplate from Student result.'''
    templ = plot_repr(student_test_result_with_pvals)[0]
    assert 'p-value' not in tuple(c.yname for c in templ.curves)
    pvaltempl = plt_elts.repr_student_pvalues(student_test_result_with_pvals)
    templ.join(pvaltempl[0])
    assert len(set(c.yname for c in templ.curves)) == 3
    mplt = MplPlot(templ)
    return mplt.fig


def test_fplit_join(student_test_result, student_test_result_fail, plot_repr):
    '''Test concatenation of FullPlotTemplate from Student result: fails as an
    addition of new curves is required on an existing subplot.'''
    templ1 = plot_repr(student_test_result)[0]
    templ2 = plot_repr(student_test_result_fail)[0]
    with pytest.raises(ValueError):
        join(templ1, templ2)
