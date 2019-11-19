'''Tests for the :mod:`~valjean.javert.representation` module.'''
# pylint: disable=redefined-outer-name
# pylint: disable=wrong-import-order

import pytest
import logging

from ..context import valjean  # pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.templates import TableTemplate, PlotTemplate, join
from valjean.javert.representation import (TableRepresenter, EmptyRepresenter,
                                           PlotRepresenter)
from valjean.javert.mpl import MplPlot
from valjean.gavroche.test import Test, TestResult

from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 approx_equal_test, some_1d_dataset,
                                 other_1d_dataset, different_1d_dataset,
                                 some_1d_dataset_edges, other_1d_dataset_edges,
                                 student_test, student_test_result,
                                 student_test_edges, student_test_edges_result,
                                 student_test_fail, student_test_result_fail,
                                 student_test_3ds, student_test_result_3ds)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_full_repr(test_name, request):
    '''Test that :class:`~.FullRepresenter` yields all the expected templates
    for equality tests.'''
    test = request.getfixturevalue(test_name)
    representer = TableRepresenter()
    templates = representer(test.evaluate())
    assert isinstance(templates, list)
    assert any(isinstance(template, TableTemplate) for template in templates)


@pytest.mark.mpl_image_compare(filename='student_comp_points.png',
                               baseline_dir='ref_plots')
def test_student_full(student_test_result, full_repr, rst_formatter, rstcheck):
    '''Test plot of student result when bins are given by centers of bins.'''
    templates = full_repr(student_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([template for template in templates
                    if isinstance(template, PlotTemplate)][0])
    return mplt.fig


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='ref_plots')
def test_student_edges_full(student_test_edges_result, full_repr,
                            rst_formatter, rstcheck):
    '''Test plot of student result when bins are given by edges.'''
    templates = full_repr(student_test_edges_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([template for template in templates
                    if isinstance(template, PlotTemplate)][0])
    return mplt.fig


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_empty_repr(test_name, request):
    '''Test that :class:`~.EmptyRepresenter` yields no templates for equality
    tests.'''
    test = request.getfixturevalue(test_name)
    representer = EmptyRepresenter()
    templates = representer(test.evaluate())
    assert templates is None


def test_full_concatenation(student_test_result, student_test_result_fail,
                            full_repr):
    '''Test concatenation of all templates.'''
    student_test_result_fail.test.datasets[0].name = "other 1D dataset"
    templ1 = full_repr(student_test_result)
    templ2 = full_repr(student_test_result_fail)
    for it1, it2 in zip(templ1, templ2):
        if isinstance(it1, TableTemplate) and isinstance(it2, TableTemplate):
            conc = join(it1, it2)
            assert (conc.columns[0].size
                    == it1.columns[0].size + it2.columns[0].size)
        else:
            with pytest.raises(ValueError):
                join(it1, it2)


@pytest.mark.mpl_image_compare(filename='student_fplit_3ds.png',
                               baseline_dir='ref_plots')
def test_full_repr_3d(student_test_result_3ds, full_repr, rst_formatter,
                      rstcheck):
    '''Test full representation with 3 datasets (1 reference, 2 test datasets).
    '''
    templ = full_repr(student_test_result_3ds)
    rst = '\n'.join(str(rst_formatter.template(template)) for template in templ
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    rst = '.. role:: hl\n\n' + rst
    errs = rstcheck.check(rst)
    assert not list(errs)
    assert len([_tp for _tp in templ if isinstance(_tp, PlotTemplate)]) == 1
    mplt = MplPlot([template for template in templ
                    if isinstance(template, PlotTemplate)][0])
    return mplt.fig


@pytest.fixture(scope='function', params=['spam', 'egg'])
def str_choice(request):
    '''Return a string among 'spam' and 'egg'.'''
    return request.param


class TestResultSpam(TestResult):
    '''Fake test result class to test representation exceptions.'''

    def __init__(self, test, is_spam):
        super().__init__(test)
        self.is_spam = is_spam

    def __bool__(self):
        return self.is_spam


class TestSpam(Test):
    '''Fake test class to test representation exceptions.'''

    def __init__(self, the_str, name, description=''):
        super().__init__(name=name, description=description)
        self.the_str = the_str

    def evaluate(self):
        '''Evaluation of the test.'''
        is_spam = self.the_str == 'spam'
        return TestResultSpam(self, is_spam)


def test_spam_repr(caplog, str_choice, full_repr):
    '''Test representation outputs when the test result has not been
    implemented in :mod:`~valjean.javert.table_elements` module or in
    :mod:`~valjean.javert.plot_elements` module from the fake test
    :class:`TestSpam` defined in the current module.

    Outputs from :class:`~valjean.javert.representation.Representation` and
    from some of the Representers are tested (empty list in first case,
    ``None`` in the second one).

    The presence of the logger messages is also checked (appearing twice in
    last test as foreseen).
    '''
    caplog.set_level(logging.INFO, logger='valjean')
    spam_test = TestSpam(str_choice, name='spam_test', description='desc')
    spamres = spam_test.evaluate()
    assert bool(spamres) == (str_choice == 'spam')
    templates = full_repr(spamres)
    assert templates == []
    loginfo_tabrepr = "no table representer repr_testresultspam"
    loginfo_pltrepr = "no plot representer repr_testresultspam"
    assert loginfo_tabrepr in caplog.text
    assert loginfo_pltrepr in caplog.text
    tabrepresenter = TableRepresenter()
    templates = tabrepresenter(spamres)
    assert templates is None
    pltrepresenter = PlotRepresenter()
    templates = pltrepresenter(spamres)
    assert templates is None
    assert caplog.text.count(loginfo_tabrepr) == 2
    assert caplog.text.count(loginfo_pltrepr) == 2
