'''Tests for the :mod:`~valjean.javert.mpl` module.

To prepare the test, i.e. to generate the reference plots:
``pytest --mpl-generate-path=PATH_TO_VALJEAN/tests/javert/ref_plots
tests/javert/test_mpl.py``.

To be sure the comparison with the reference plots is done, don't forget the
``--mpl`` option:
``pytest --mpl tests/javert/test_mpl.py``.
'''
# pylint: disable=unused-import

from collections import namedtuple
import pytest
import numpy as np
from hypothesis import given, settings, HealthCheck, note
from hypothesis.strategies import just, integers, data, lists, text
from hypothesis.extra.numpy import array_shapes

from ...context import valjean  # pylint: disable=wrong-import-order

from valjean import LOGGER
from valjean.javert.templates import (PlotTemplate, join, TableTemplate,
                                      CurveElements, SubPlotElements)
from valjean.javert.mpl import MplPlot, MplPlotException
from valjean.javert import plot_elements as plt_elts
from valjean.javert.representation import PlotRepresenter
from ...gavroche.conftest import (some_1d_dataset, one_dim_dataset,
                                  other_1d_dataset, some_1d_dataset_edges,
                                  other_1d_dataset_edges, different_1d_dataset)
from ...gavroche.conftest import (student_test, student_test_result,
                                  student_test_fail, student_test_result_fail,
                                  student_test_edges,
                                  student_test_edges_result,
                                  student_test_3ds, student_test_result_3ds,
                                  student_test_with_pvals,
                                  student_test_result_with_pvals)
from ...gavroche.conftest import datasets


def test_plot_1d_dataset(some_1d_dataset):
    '''Test plot of 1-D dataset.'''
    plt = PlotTemplate(subplots=[SubPlotElements(
        curves=[CurveElements(some_1d_dataset.value,
                              bins=[some_1d_dataset.bins['e']],
                              legend='', index=0)],
        axnames=('e', ''))])
    assert (plt.subplots[0].curves[0].values.size
            == plt.subplots[0].curves[0].bins[0].size)
    assert plt.nb_plots == 1


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_bins_edges(oneds):
    '''Test plot where bins are given by edges.'''
    pelt = CurveElements(oneds.value, bins=list(oneds.bins.values()),
                         legend='', index=0)
    plt = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt], axnames=tuple(list(oneds.bins.keys()) + ['score']))])
    assert plt.nb_plots == 1
    crv0 = plt.subplots[0].curves[0]
    assert (crv0.values.size == crv0.bins[0].size
            or crv0.values.size+1 == crv0.bins[0].size)
    assert len(plt.subplots[0].axnames) == len(crv0.bins)+1


@settings(suppress_health_check=(HealthCheck.too_slow,), deadline=None,
          max_examples=10)
@given(oneds=one_dim_dataset())  # pylint: disable=no-value-for-parameter
def test_plot_with_errors(oneds):
    '''Test plot where bins are given by edges.'''
    pelt = CurveElements(oneds.value, bins=list(oneds.bins.values()),
                         legend='', index=0, errors=oneds.error)
    plt = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt], axnames=(tuple(list(oneds.bins.keys()) + ['score'])))])
    assert oneds.error.size == oneds.value.size
    assert list(plt.subplots[0].axnames[:-1]) == list(oneds.bins.keys())


def test_pltatt_limits(caplog):
    '''Test limits from :class:`PlotAttributes`.'''
    pcelt = CurveElements(values=np.arange(5), bins=[np.arange(5)], legend='',
                          index=0)
    ptemp = PlotTemplate(subplots=[
        SubPlotElements(curves=[pcelt], axnames=('X', 'Y'))])
    ptemp.subplots[0].attributes.limits = [(0, 2), (1, 3)]
    assert 'Wrong number of limits given: expected 1, got 2' in caplog.text


@pytest.mark.mpl_image_compare(filename='plot_reg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), bins=[np.arange(6)], legend='',
                         index=0)
    plti = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt], axnames=('X', 'Y'), ptype='1D')])
    mplt = MplPlot(plti)
    fig, splts = mplt.draw()
    splts[0].set_title('Simple plot')
    return fig


@pytest.mark.mpl_image_compare(filename='plot_irreg_bins.png',
                               baseline_dir='ref_plots')
def test_plot_show_irreg_bins():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), legend='', index=0,
                         bins=[np.array([0, 2, 3, 6, 7, 10])])
    plti = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt], axnames=('X', 'Y'), ptype='1D')])
    mplt = MplPlot(plti)
    fig, splts = mplt.draw()
    splts[0].set_title('Plot irregular bins')
    return fig


def test_plot_exception():
    '''Test with matplotlib test.'''
    pelt = CurveElements(values=np.arange(5), legend='', index=0,
                         bins=[np.array([0, 2, 3, 6, 7, 10])])
    plti = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt], axnames=('X', 'Y'), ptype='1d')])
    mplt = MplPlot(plti)
    with pytest.raises(MplPlotException):
        mplt.draw()


@pytest.mark.mpl_image_compare(filename='student_plot.png',
                               baseline_dir='ref_plots')
def test_student_plot(student_test_result, plot_repr):
    '''Test plot of Student result.'''
    templates = plot_repr(student_test_result)
    mplt = MplPlot(templates[-1])
    fig, _ = mplt.draw()
    return fig


@pytest.mark.mpl_image_compare(filename='student_failed.png',
                               baseline_dir='ref_plots')
def test_student_fail(student_test_result_fail, plot_repr):
    '''Test plot of a failed Student result.'''
    template = plot_repr(student_test_result_fail)
    mplt = MplPlot(template[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi(student_test_edges_result, plot_repr):
    '''Test plot of Student result when bins are given by edges.'''
    template = plot_repr(student_test_edges_result)
    mplt = MplPlot(template[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_wfpi_delta.png',
                               baseline_dir='ref_plots')
def test_student_with_fpi_d(student_test_result):
    '''Test plot of Student result.'''
    template = plt_elts.repr_student_delta(student_test_result)
    mplt = MplPlot(template[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_edges_wfpi_values.png',
                               baseline_dir='ref_plots')
def test_student_edges_with_fpi_v(student_test_edges_result):
    '''Test plot of Student result when bins are given by edges.'''
    template = plt_elts.repr_datasets_values(student_test_edges_result)
    mplt = MplPlot(template[0])
    return mplt.draw()[0]


def test_fplit_cc(student_test_result, plot_repr):
    '''Test copy of FullPlotTemplate from Student result.'''
    template1 = plot_repr(student_test_result)[0]
    template2 = template1.copy()
    assert id(template1.subplots) != id(template2.subplots)
    for sp1, sp2 in zip(template1.subplots, template2.subplots):
        assert id(sp1.curves) != id(sp2.curves)
        for cv1, cv2 in zip(sp1.curves, sp2.curves):
            assert id(cv1.bins) != id(cv2.bins)
            assert id(cv1.values) != id(cv2.values)
            if cv1.errors is not None and cv2.errors is not None:
                assert id(cv1.errors) != id(cv2.errors)
        assert id(sp1.axnames) != id(sp2.axnames)
        assert id(sp1.axnames[0]) == id(sp2.axnames[0])
    old_id = id(template2.subplots[0].axnames)
    template2.subplots[0].axnames[0] += 'f'
    assert old_id == id(template2.subplots[0].axnames)
    assert (id(template1.subplots[0].axnames[0])
            != id(template2.subplots[0].axnames[0])
            and template1.subplots[0].axnames != template2.subplots[0].axnames)


@pytest.mark.mpl_image_compare(filename='student_fplit_3ds.png',
                               baseline_dir='ref_plots')
def test_fplit_3ds(student_test_result_3ds, plot_repr):
    '''Test concatenation of FullPlotTemplate from Student result.'''
    templ = plot_repr(student_test_result_3ds)[0]
    assert set(s.axnames[1] for s in templ.subplots) == {'', r'$t_{Student}$'}
    assert templ.subplots[0].axnames[1] == ''
    assert len(templ.subplots[0].curves) == 3
    assert templ.subplots[1].axnames[1] == r'$t_{Student}$'
    assert len(templ.subplots[1].curves) == 2
    mplt = MplPlot(templ)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_fplit_add.png',
                               baseline_dir='ref_plots')
def test_fplit_pjoin(student_test_result_with_pvals, plot_repr):
    '''Test concatenation of PlotTemplate from Student result.'''
    templ = plot_repr(student_test_result_with_pvals)[0]
    assert 'p-value' not in tuple(s.axnames[1] for s in templ.subplots)
    pvaltempl = plt_elts.repr_student_pvalues(student_test_result_with_pvals)
    templ.join(pvaltempl[0])
    assert templ.nb_plots == 3
    mplt = MplPlot(templ)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='adapt_range_lrbin.png',
                               baseline_dir='ref_plots')
def test_adapt_range_lrbin(studentt_res_range_lrbin, plot_repr):
    '''Test with matplotlib test.'''
    templ = plot_repr(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='adapt_range_lbin.png',
                               baseline_dir='ref_plots')
def test_adapt_range_lbin(studentt_res_range_lbin, plot_repr):
    '''Test with matplotlib test.'''
    templ = plot_repr(studentt_res_range_lbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='adapt_range_rbin.png',
                               baseline_dir='ref_plots')
def test_adapt_range_rbin(studentt_res_range_rbin, plot_repr):
    '''Test with matplotlib test.'''
    templ = plot_repr(studentt_res_range_rbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='noadapt_range_lrbin.png',
                               baseline_dir='ref_plots')
def test_noadapt_range_lrbin(studentt_res_range_lrbin, plot_no_post_repr):
    '''Test with matplotlib test.'''
    templ = plot_no_post_repr(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d.png',
                               baseline_dir='ref_plots')
def test_student_2d(studentt_res_2d, plot_repr):
    '''2D plot for Student test'''
    templ = plot_repr(studentt_res_2d)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_range_elr.png',
                               baseline_dir='ref_plots')
def test_student_2d_range_elr(studentt_res_2d_range_elr, plot_repr):
    '''2D plot for Student test with large extreme bins in e (x-axis).'''
    templ = plot_repr(studentt_res_2d_range_elr)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_range_etlr.png',
                               baseline_dir='ref_plots')
def test_student_2d_range_etlr(studentt_res_2d_range_etlr, plot_repr):
    '''2D plot for Studnet test with large extreme bins in e and t (both axis).
    '''
    templ = plot_repr(studentt_res_2d_range_etlr)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_range_etr.png',
                               baseline_dir='ref_plots')
def test_student_2d_range_etr(studentt_res_2d_range_etr, plot_repr):
    '''2D plot for Student test with large last bins in e and t (both axis).'''
    templ = plot_repr(studentt_res_2d_range_etr)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_nopost.png',
                               baseline_dir='ref_plots')
def test_student_2d_no_post(studentt_res_2d, plot_no_post_repr):
    '''2D plot for Student test'''
    templ = plot_no_post_repr(studentt_res_2d)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_logx.png',
                               baseline_dir='ref_plots')
def test_studentt_res_logx(studentt_res_range_lrbin):
    '''Test logarithmic x-axis with 1D plot.'''
    def log_post(templates, tres):  # pylint: disable=unused-argument
        for templ in templates:
            for splt in templ.subplots:
                splt.attributes.logx = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_logy.png',
                               baseline_dir='ref_plots')
def test_studentt_res_logy(studentt_res_range_lrbin):
    '''Test logarithmic y-axis with 1D plot.'''
    def log_post(templates, tres):
        plt_elts.post_treatment(templates, tres)
        for templ in templates:
            templ.subplots[0].attributes.logy = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_logy2.png',
                               baseline_dir='ref_plots')
def test_studentt_res_logy2(studentt_res_range_lrbin):
    '''Test logarithmic y-axis with 1D plot.'''
    def log_post(templates, tres):
        plt_elts.post_treatment(templates, tres)
        for templ in templates:
            for splt in templ.subplots:
                splt.attributes.logy = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_logxy.png',
                               baseline_dir='ref_plots')
def test_studentt_res_logxy(studentt_res_range_lrbin):
    '''Test logarithmic x- and y-axis with 1D plot.'''
    def log_post(templates, tres):  # pylint: disable=unused-argument
        for templ in templates:
            for splt in templ.subplots:
                splt.attributes.logx = True
            templ.subplots[0].attributes.logy = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_range_lrbin)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_logz.png',
                               baseline_dir='ref_plots')
def test_studentt_2d_logz(studentt_res_2d):
    '''Test logarithmic colorbar with 2D plot.'''
    def log_post(templates, tres):  # pylint: disable=unused-argument
        for templ in templates:
            templ.subplots[0].attributes.logz = True
            templ.subplots[1].attributes.logz = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_2d)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_logxy.png',
                               baseline_dir='ref_plots')
def test_studentt_2d_logxy(studentt_res_2d_range_etlr):
    '''Test logarithmic x- and y-axis with 2D plot.'''
    def log_post(templates, tres):
        plt_elts.post_treatment(templates, tres)
        for templ in templates:
            for splt in templ.subplots:
                splt.attributes.logx = True
                splt.attributes.logy = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_2d_range_etlr)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='student_2d_logxz.png',
                               baseline_dir='ref_plots')
def test_studentt_2d_logxz(studentt_res_2d_range_etlr):
    '''Test logarithmic x-axis and colorbar with 2D plot.'''
    def log_post(templates, tres):
        plt_elts.post_treatment(templates, tres)
        for templ in templates:
            for splt in templ.subplots:
                splt.attributes.logx = True
            templ.subplots[0].attributes.logz = True
            templ.subplots[1].attributes.logz = True
        return templates
    templ = PlotRepresenter(post=log_post)(studentt_res_2d_range_etlr)
    mplt = MplPlot(templ[0])
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='mult_curves.png',
                               baseline_dir='ref_plots')
def test_mult_curves():
    '''Test for multiple curves on the same subplot.'''
    pelt = CurveElements(values=np.arange(5), bins=[np.arange(6)], legend='c0',
                         index=0)
    pelt2 = CurveElements(values=np.arange(5)*1.2, bins=[np.arange(6)],
                          legend='c1', index=1)
    pelt3 = CurveElements(values=np.arange(5)*0.7, bins=[np.arange(6)],
                          legend='c2', index=2)
    plti = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt, pelt2, pelt3], axnames=('X', 'Y'))])
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='mult_curves_a_splts.png',
                               baseline_dir='ref_plots')
def test_mult_curves_a_splts():
    '''Test for multiple curves on the different subplots.'''
    pelt = CurveElements(values=np.arange(5), bins=[np.arange(6)], legend='c0',
                         index=0)
    pelt2 = CurveElements(values=np.arange(5)*1.2, bins=[np.arange(6)],
                          legend='c1', index=1)
    pelt3 = CurveElements(values=np.arange(5)*0.7, bins=[np.arange(6)],
                          legend='c2', index=2)
    pelt4 = CurveElements(values=np.arange(5)*0.3, bins=[np.arange(6)],
                          legend='c1', index=1)
    pelt5 = CurveElements(values=np.arange(5)*0.5, bins=[np.arange(6)],
                          legend='c2', index=2)
    plti = PlotTemplate(
        subplots=[
            SubPlotElements(curves=[pelt, pelt2, pelt3], axnames=('X', 'Y')),
            SubPlotElements(curves=[pelt4, pelt5], axnames=('X', 'other Y'))],
        suppress_xaxes=True, suppress_legends=True)
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='diff_binnings.png',
                               baseline_dir='ref_plots')
def test_diff_bins():
    '''Test for different binnings on same subplot (same axis names).'''
    pelt = CurveElements(values=np.arange(5), bins=[np.arange(6)], legend='c0',
                         index=0)
    pelt2 = CurveElements(values=np.arange(5), bins=[np.arange(6)+1.3],
                          legend='c1', index=1)
    plti = PlotTemplate(subplots=[SubPlotElements(
        curves=[pelt, pelt2], axnames=('X', 'Y'))])
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='diff_xaxes.png',
                               baseline_dir='ref_plots')
def test_diff_axes():
    '''Test of subplots with different axes.'''
    pelt = CurveElements(values=np.arange(5), bins=[np.arange(6)], legend='c1',
                         index=0)
    pelt2 = CurveElements(values=np.arange(5), bins=[np.arange(6)+1.3],
                          legend='c2', index=0)
    plti = PlotTemplate(
        subplots=[SubPlotElements(curves=[pelt], axnames=('X', 'Y')),
                  SubPlotElements(curves=[pelt2], axnames=('x', 'Y'))],
        small_subplots=False)
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='mult_curves_a_splts_join.png',
                               baseline_dir='ref_plots')
def test_join_subplots():
    '''Test of join plots with different cases.'''
    celt1 = CurveElements(values=np.arange(5), bins=[np.arange(6)],
                          legend='c0', index=0)
    celt2 = CurveElements(values=np.arange(5)*1.2, bins=[np.arange(6)],
                          legend='c1', index=10)
    plt1 = PlotTemplate(subplots=[
        SubPlotElements(curves=[celt1, celt2], axnames=('X', 'Y'))])
    celt3 = CurveElements(values=np.arange(5)*0.7, bins=[np.arange(6)],
                          legend='c2', index=2)
    plt3 = PlotTemplate(subplots=[
        SubPlotElements(curves=[celt3], axnames=('X', 'Y'))])
    plt1.join(plt3)
    celt4 = CurveElements(values=np.arange(5)*0.3, bins=[np.arange(6)],
                          legend='c1', index=10)
    celt5 = CurveElements(values=np.arange(5)*0.5, bins=[np.arange(6)],
                          legend='c2', index=2)
    plt4 = PlotTemplate(subplots=[
        SubPlotElements(curves=[celt4, celt5], axnames=('X', 'other Y'))])
    plt1.join(plt4)
    mplt = MplPlot(plt1)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='diff_axes_limits.png',
                               baseline_dir='ref_plots')
def test_plt_limits():
    '''Test limits modifications.'''
    celt1 = CurveElements(values=np.array([1, 3, 2, 5, 4]),
                          bins=[np.array([0, 2, 4, 6, 8, 10000])],
                          legend='c0', index=0)
    celt2 = CurveElements(values=np.array([2, 0, 3, 5, 1]),
                          bins=[np.array([0, 1, 2, 3, 4, 5])],
                          legend='c1', index=1)
    celt3 = CurveElements(values=np.array([5, 4, 2, 1, 0]),
                          bins=[np.array([-2, 2, 3, 4, 6, 100000])],
                          legend='c2', index=2)
    plt1 = PlotTemplate(subplots=[
        SubPlotElements(curves=[celt1, celt2, celt3], axnames=('X', 'Y'))])
    for splt in plt1.subplots:
        blimits = [plt_elts.trim_range(sc.bins) for sc in splt.curves]
    assert any(b[1] for a in blimits for b in a)
    nlimits = []
    for idim in range(len(blimits[0])):
        nlimits.append((min(crv[idim][0][0] for crv in blimits),
                        max(crv[idim][0][1] for crv in blimits)))
    plt1.subplots[0].attributes.limits = nlimits
    mplt = MplPlot(plt1)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='diff_axes_limits_2d.png',
                               baseline_dir='ref_plots')
def test_plt_limits_2d():
    '''Test limits modifications using 2D plots.'''
    spelt1 = SubPlotElements(
        curves=[CurveElements(
            values=np.arange(12).reshape(3, 4),
            bins=[np.array([0, 2, 4, 10000]), np.array([1, 3, 5, 7, 9])],
            legend='c0', index=0)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    spelt2 = SubPlotElements(
        curves=[CurveElements(
            values=np.arange(12).reshape(3, 4)*1.2,
            bins=[np.array([0, 1, 2, 3]), np.array([0, 1, 2, 3, 10000])],
            legend='c1', index=1)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    spelt3 = SubPlotElements(
        curves=[CurveElements(
            values=np.arange(12).reshape(3, 4)*1.2,
            bins=[np.array([-1, 0, 1, 2]), np.array([1, 2, 4, 6, 7])],
            legend='c2', index=2)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    plt1 = PlotTemplate(subplots=[spelt1, spelt2, spelt3],
                        small_subplots=False)
    blimits = [plt_elts.trim_range(c.bins) for s in plt1.subplots
               for c in s.curves]
    assert any(b[1] for a in blimits for b in a)
    nlimits = []
    for idim in range(len(blimits[0])):
        nlimits.append((min(crv[idim][0][0] for crv in blimits),
                        max(crv[idim][0][1] for crv in blimits)))
    for splt in plt1.subplots:
        splt.attributes.limits = nlimits
    mplt = MplPlot(plt1)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='diff_axes_limits_2d_2.png',
                               baseline_dir='ref_plots')
def test_plt_limits_2d_2():
    '''Test limits modifications using 2D plots.'''
    spelt1 = SubPlotElements(
        curves=[CurveElements(
            values=np.arange(12).reshape(3, 4),
            bins=[np.array([0, 2, 4, 10000]), np.array([1, 3, 5, 7, 9])],
            legend='c0', index=0)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    spelt2 = SubPlotElements(
        curves=[CurveElements(
            values=np.arange(12).reshape(3, 4)*1.2,
            bins=[np.array([0, 1, 2, 3]), np.array([0, 1, 2, 3, 10000])],
            legend='c1', index=1)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    plt1 = PlotTemplate(subplots=[spelt1, spelt2], small_subplots=False)
    blimits = [plt_elts.trim_range(c.bins) for s in plt1.subplots
               for c in s.curves]
    assert any(b[1] for a in blimits for b in a)
    nlimits = []
    for idim in range(len(blimits[0])):
        nlimits.append((min(crv[idim][0][0] for crv in blimits),
                        max(crv[idim][0][1] for crv in blimits)))
    for splt in plt1.subplots:
        splt.attributes.limits = nlimits
    mplt = MplPlot(plt1)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='mix_1d_and_2d.png',
                               baseline_dir='ref_plots')
def test_mix_1d_and_2d():
    '''Test limits modifications using 2D plots.'''
    values = np.arange(12).reshape(3, 4)
    spelt2d = SubPlotElements(
        curves=[CurveElements(
            values=values,
            bins=[np.array([0, 2, 4, 10000]), np.array([1, 3, 5, 7, 9])],
            legend='c0', index=0)],
        axnames=('X', 'Y', 'Z'), ptype='2D')
    spelt1dsx = SubPlotElements(
        curves=[CurveElements(
            values=np.sum(values, axis=0),
            bins=[np.array([1, 3, 5, 7, 9])],
            legend='c1', index=1)],
        axnames=('Y', 'sum(Z) over X'), ptype='1D')
    spelt1dsy = SubPlotElements(
        curves=[CurveElements(
            values=np.sum(values, axis=1),
            bins=[np.array([0, 2, 4, 10000])],
            legend='c1', index=1)],
        axnames=('X', 'sum(Z) over Y'), ptype='1D')
    plt1 = PlotTemplate(subplots=[spelt2d, spelt1dsx, spelt1dsy],
                        small_subplots=False, suppress_legends=True)
    blimits = [plt_elts.trim_range(c.bins) for s in plt1.subplots
               for c in s.curves]
    assert any(b[1] for a in blimits for b in a)
    for splt, lim in zip(plt1.subplots, blimits):
        splt.attributes.limits = [li[0] for li in lim]
    mplt = MplPlot(plt1)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='string_bins_1d_same_axes.png',
                               baseline_dir='ref_plots')
def test_string_bins_1d_same_axes():
    '''Test for multiple curves on the same subplot.'''
    bins = [np.array(['spam', 'bacon', 'egg+spam', 'egg+bacon',
                      'egg+spam+bacon'])]
    pelt1 = CurveElements(values=np.arange(5), bins=bins, legend='c0',
                          index=0)
    pelt2 = CurveElements(values=np.arange(5)*1.2, bins=bins,
                          legend='c1', index=1)
    pelt3 = CurveElements(values=np.arange(5)*0.7, bins=bins,
                          legend='c2', index=2)
    plti = PlotTemplate(
        subplots=[SubPlotElements(curves=[pelt1, pelt2], axnames=('X', 'Y')),
                  SubPlotElements(curves=[pelt3], axnames=('X', 'Y'))],
        suppress_xaxes=True)
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='string_bins_1d_diff_axes.png',
                               baseline_dir='ref_plots')
def test_string_bins_1d_diff_axes():
    '''Test for multiple curves on the same subplot.'''
    bins1 = [np.array(['spam', 'bacon', 'egg+spam', 'egg+bacon',
                       'egg+spam+bacon'])]
    bins2 = [np.array(['wine', 'beer', 'champagne', 'water', 'orange juice'])]
    pelt1 = CurveElements(values=np.arange(5), bins=bins1, legend='c0',
                          index=0)
    pelt2 = CurveElements(values=np.arange(5)*1.2, bins=bins1,
                          legend='c1', index=1)
    pelt3 = CurveElements(values=np.arange(5)*0.7, bins=bins2,
                          legend='c2', index=2)
    plti = PlotTemplate(
        subplots=[SubPlotElements(curves=[pelt1, pelt2], axnames=('X', 'Y')),
                  SubPlotElements(curves=[pelt3], axnames=('X', 'Y'))])
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='string_bins_2d.png',
                               baseline_dir='ref_plots')
def test_string_bins_2d():
    '''Test for multiple curves on the same subplot.'''
    bins = [np.array(['spam', 'bacon', 'egg+spam', 'egg+bacon',
                      'egg+spam+bacon']),
            # np.arange(4)]
            np.array(['wine', 'beer', 'champagne', 'orange juice'])]
    pelt1 = CurveElements(values=np.arange(20).reshape(5, 4), bins=bins,
                          legend='c0')
    pelt2 = CurveElements(values=np.arange(20).reshape(5, 4)*1.2, bins=bins,
                          legend='c1')
    plti = PlotTemplate(
        subplots=[SubPlotElements(curves=[pelt1],
                                  axnames=('meal', 'drink', 'Z'), ptype='2D'),
                  SubPlotElements(curves=[pelt2],
                                  axnames=('meal', 'drink', 'Z'), ptype='2D')],
        small_subplots=False)
    mplt = MplPlot(plti)
    return mplt.draw()[0]


@pytest.mark.mpl_image_compare(filename='pie_chart.png',
                               baseline_dir='ref_plots')
def test_pie_chart():
    '''Test pie chart.'''
    bins = [np.array(['spam', 'bacon', 'egg', 'lobster'])]
    celts = CurveElements(values=np.array([2, 4, 5, 1]), bins=bins, legend='')
    splte = SubPlotElements(curves=[celts],
                            axnames=['Frequency of ingredients', ''],
                            ptype='pie')
    ptemp = PlotTemplate(subplots=[splte])
    mplt = MplPlot(ptemp)
    return mplt.draw()[0]
