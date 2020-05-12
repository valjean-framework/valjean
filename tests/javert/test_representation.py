'''Tests for the :mod:`~valjean.javert.representation` module.'''
# pylint: disable=wrong-import-order

import pytest
import logging

from ..context import valjean  # pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.templates import (TableTemplate, PlotTemplate,
                                      TextTemplate, join)
from valjean.javert.representation import (TableRepresenter, EmptyRepresenter,
                                           PlotRepresenter, FullRepresenter,
                                           Representation)
from valjean.javert.mpl import MplPlot
from valjean.javert.verbosity import Verbosity
from valjean.gavroche.test import Test, TestResult
from valjean.gavroche.diagnostics.metadata import TestMetadata
from valjean.gavroche.diagnostics.stats import (test_stats_by_labels,
                                                test_stats, task_stats)
from valjean.cosette.pythontask import PythonTask
from valjean.cosette.env import Env
from valjean.cosette.task import TaskStatus
from valjean.config import Config

from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 equal_test_result, approx_equal_test,
                                 approx_equal_test_result, some_dataset,
                                 other_dataset, student_test_2d,
                                 student_test_2d_result, some_1d_dataset,
                                 other_1d_dataset, different_1d_dataset,
                                 some_1d_dataset_edges, other_1d_dataset_edges,
                                 student_test, student_test_result,
                                 student_test_edges, student_test_edges_result,
                                 student_test_fail, student_test_result_fail,
                                 student_test_with_pvals,
                                 student_test_result_with_pvals,
                                 student_test_3ds, student_test_result_3ds,
                                 holm_bonferroni_test,
                                 holm_bonferroni_test_result,
                                 bonferroni_test, bonferroni_test_result)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_full_repr(test_name, request):
    '''Test that :class:`~.FullRepresenter` yields all the expected templates
    for equality tests.'''
    test = request.getfixturevalue(test_name)
    # representer = TableRepresenter()
    representer = FullRepresenter()
    templates = representer(test.evaluate(), Verbosity.FULL_DETAILS)
    assert isinstance(templates, list)
    assert any(isinstance(template, TableTemplate) for template in templates)
    assert any(isinstance(template, PlotTemplate) for template in templates)


@pytest.mark.mpl_image_compare(filename='student_comp_points.png',
                               baseline_dir='plots/ref_plots')
def test_student_full(student_test_result, rfull_repr, rst_formatter,
                      rstcheck):
    '''Test plot of student result when bins are given by centers of bins.'''
    templates = rfull_repr(student_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([template for template in templates
                    if isinstance(template, PlotTemplate)][0])
    return mplt.draw()


@pytest.mark.mpl_image_compare(filename='student_comp_edges.png',
                               baseline_dir='plots/ref_plots')
def test_student_edges_full(student_test_edges_result, rfull_repr,
                            rst_formatter, rstcheck):
    '''Test plot of student result when bins are given by edges.'''
    templates = rfull_repr(student_test_edges_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
    mplt = MplPlot([template for template in templates
                    if isinstance(template, PlotTemplate)][0])
    return mplt.draw()


@pytest.mark.parametrize('verb_level', [None, Verbosity.SILENT,
                                        Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS,
                                        Verbosity.DEVELOPMENT])
def test_student_verb(verb_level, student_test_2d_result, rst_formatter,
                      rstcheck):
    '''Test Student templates with verbosity.'''
    frepr = Representation(FullRepresenter(), verb_level)
    templates = frepr(student_test_2d_result)
    ttempl = filter(lambda x: isinstance(x, TableTemplate), templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    if verb_level in (Verbosity.SILENT, Verbosity.SUMMARY):
        assert not ptempl
    elif (verb_level is not None
          and verb_level.value >= Verbosity.FULL_DETAILS.value):
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 1
    else:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 2


@pytest.mark.parametrize('verb_level', [Verbosity.SILENT, Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_student_pvals_verb(verb_level, student_test_result_with_pvals,
                            rst_formatter, rstcheck):
    '''Test Student templates with verbosity requiring p-values.'''
    frepr = Representation(FullRepresenter(), verb_level)
    templates = frepr(student_test_result_with_pvals)
    ttempl = filter(lambda x: isinstance(x, (TableTemplate, TextTemplate)),
                    templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    if verb_level in (Verbosity.SILENT, Verbosity.SUMMARY):
        assert not ptempl
    elif verb_level.value >= Verbosity.FULL_DETAILS.value:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 3
    else:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 2


@pytest.mark.parametrize('verb_level', [Verbosity.SILENT, Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_equal_verb(verb_level, equal_test_result, full_repr, rst_formatter,
                    rstcheck):
    '''Test equal templates with verbosity.'''
    templates = full_repr(equal_test_result, verb_level)
    ttempl = filter(lambda x: isinstance(x, (TableTemplate, TextTemplate)),
                    templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    assert len(ptempl) == 1
    assert ptempl[0].nb_plots == 1


@pytest.mark.parametrize('verb_level', [Verbosity.SILENT, Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_holm_bonferroni_verb(verb_level, holm_bonferroni_test_result,
                              full_repr, rst_formatter, rstcheck):
    '''Test Holm-Bonferroni templates with verbosity.'''
    templates = full_repr(holm_bonferroni_test_result, verb_level)
    ttempl = filter(lambda x: isinstance(x, (TableTemplate, TextTemplate)),
                    templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    if verb_level in (Verbosity.SILENT, Verbosity.SUMMARY):
        assert not ptempl
    elif verb_level.value >= Verbosity.FULL_DETAILS.value:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 3
    else:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 2


@pytest.mark.parametrize('verb_level', [Verbosity.SILENT, Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_bonferroni_verb(verb_level, bonferroni_test_result, full_repr,
                         rst_formatter, rstcheck):
    '''Test Bonferroni templates with verbosity.'''
    templates = full_repr(bonferroni_test_result, verb_level)
    ttempl = filter(lambda x: isinstance(x, (TableTemplate, TextTemplate)),
                    templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    if verb_level in (Verbosity.SILENT, Verbosity.SUMMARY):
        assert not ptempl
    elif verb_level.value >= Verbosity.FULL_DETAILS.value:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 3
    else:
        assert len(ptempl) == 1
        assert ptempl[0].nb_plots == 2


@pytest.mark.parametrize('verb_level', [None, Verbosity.SILENT,
                                        Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_metadata_verb(verb_level, full_repr, rst_formatter, rstcheck):
    '''Test metadata templates with verbosity.'''
    mtest = TestMetadata({'md1': {'spam': 1, 'egg': 'wine'},
                          'md2': {'spam': 1, 'egg': 'beer'}}, name='md_test')
    templates = full_repr(mtest.evaluate(), verb_level)
    ttempl = filter(lambda x: isinstance(x, TableTemplate), templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    assert not ptempl


def generate_test_tasks():
    '''Generate :class:`~.TestMetadata` to test the statistics diagnostics
    based on labels.'''
    menu1 = {'food': 'egg + spam', 'drink': 'beer'}
    menu2 = {'food': 'egg + bacon', 'drink': 'beer'}
    menu3 = {'food': 'lobster thermidor', 'drink': 'brandy'}

    def test_generator():
        result = [TestMetadata({'Graham': menu1, 'Terry': menu1},
                               name='gt_wday_lunch',
                               labels={'day': 'Wednesday', 'meal': 'lunch'}
                               ).evaluate(),
                  TestMetadata({'Michael': menu1, 'Eric': menu2},
                               name='me_wday_dinner',
                               labels={'day': 'Wednesday', 'meal': 'dinner'}
                               ).evaluate(),
                  TestMetadata({'John': menu2, 'Terry': menu2},
                               name='jt_wday',
                               labels={'day': 'Wednesday'}).evaluate(),
                  TestMetadata({'Terry': menu3, 'John': menu3},
                               name='Xmasday',
                               labels={'day': "Christmas Eve"}).evaluate()]
        return {'test_generator': {'result': result}}, TaskStatus.DONE

    return PythonTask('test_generator', test_generator)


def generate_labstats_tasks(name, test_task, labels):
    '''Generate to tasks to make the diagnostic based on tests' labels.'''
    stats = test_stats_by_labels(name=name, tasks=[test_task],
                                 by_labels=labels)
    create_stats = next(task for task in stats.depends_on)
    return [create_stats, stats]


def generate_stats_tasks(test_task):
    '''Generate to tasks to make the diagnostic based on tests' labels.'''
    stats = task_stats(name='stats_tasks', tasks=[test_task])
    create_stats = next(task for task in stats.depends_on)
    return [create_stats, stats]


def generate_statstests_tasks(test_task):
    '''Generate to tasks to make the diagnostic based on tests' labels.'''
    stats = test_stats(name='stats_tests', tasks=[test_task])
    create_stats = next(task for task in stats.depends_on)
    return [create_stats, stats]


def run_tasks(tasks, env):
    '''Run the tasls and update the environnment.'''
    config = Config(paths=[])
    for task in tasks:
        env_up, status = task.do(env=env, config=config)
        env.apply(env_up)
    return env, status


def stats_result(tasks_md, env):  # , env, name, labels):
    '''Run the stats task test and return result.'''
    # tasks_md = generate_labstats_tasks(name, ttask, labels=labels)
    env, status = run_tasks(tasks_md, env)
    assert status == TaskStatus.DONE
    return env[tasks_md[1].name]['result'][0]


def stats_representation(sres, verb_level, full_repr, rst_formatter, rstcheck):
    '''Representation of stats tests.'''
    templates = full_repr(sres, verb_level)
    ttempl = filter(lambda x: isinstance(x, (TableTemplate, TextTemplate)),
                    templates)
    ptempl = list(filter(lambda x: isinstance(x, PlotTemplate), templates))
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in ttempl)
    errs = rstcheck.check(rst)
    assert not list(errs)
    assert not ptempl


@pytest.mark.parametrize('verb_level', [None, Verbosity.SILENT,
                                        Verbosity.SUMMARY,
                                        Verbosity.INTERMEDIATE,
                                        Verbosity.FULL_DETAILS])
def test_stats_diagnostic_verb(verb_level, full_repr, rst_formatter, rstcheck):
    '''Test the statistics test by labels using a common set of tests.'''
    tasks = [generate_test_tasks()]
    env = Env()
    env, status = run_tasks(tasks, env)
    assert status == TaskStatus.DONE
    stats_representation(
        stats_result(generate_labstats_tasks(
            'one_lab', tasks[0], ('day',)), env),
        verb_level, full_repr, rst_formatter, rstcheck)
    stats_representation(
        stats_result(generate_labstats_tasks(
            'two_lab', tasks[0], ('day', 'meal')), env),
        verb_level, full_repr, rst_formatter, rstcheck)
    stats_representation(
        stats_result(generate_labstats_tasks(
            'except', tasks[0], ('consumer',)), env),
        verb_level, full_repr, rst_formatter, rstcheck)
    stats_representation(stats_result(generate_stats_tasks(tasks[0]), env),
                         verb_level, full_repr, rst_formatter, rstcheck)
    stats_representation(
        stats_result(generate_statstests_tasks(tasks[0]), env),
        verb_level, full_repr, rst_formatter, rstcheck)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_empty_repr(test_name, request):
    '''Test that :class:`~.EmptyRepresenter` yields no templates for equality
    tests.'''
    test = request.getfixturevalue(test_name)
    representer = EmptyRepresenter()
    templates = representer(test.evaluate())
    assert templates is None


def test_full_concatenation(student_test_result, student_test_result_fail,
                            rfull_repr, caplog):
    '''Test concatenation of all templates.'''
    student_test_result_fail.test.datasets[0].name = "other 1D dataset"
    templ1 = rfull_repr(student_test_result)
    templ2 = rfull_repr(student_test_result_fail)
    for it1, it2 in zip(templ1, templ2):
        if isinstance(it1, TableTemplate) and isinstance(it2, TableTemplate):
            conc = join(it1, it2)
            assert (conc.columns[0].size
                    == it1.columns[0].size + it2.columns[0].size)
        else:
            join(it1, it2)
            assert ('Some indices are them same in self and other, '
                    'might generate a representation issue.' in caplog.text)


@pytest.mark.mpl_image_compare(filename='student_fplit_3ds.png',
                               baseline_dir='plots/ref_plots')
def test_full_repr_3d(student_test_result_3ds, rfull_repr, rst_formatter,
                      rstcheck):
    '''Test full representation with 3 datasets (1 reference, 2 test datasets).
    '''
    templ = rfull_repr(student_test_result_3ds)
    rst = '\n'.join(str(rst_formatter.template(template)) for template in templ
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    rst = '.. role:: hl\n\n' + rst
    errs = rstcheck.check(rst)
    assert not list(errs)
    assert len([_tp for _tp in templ if isinstance(_tp, PlotTemplate)]) == 1
    mplt = MplPlot([template for template in templ
                    if isinstance(template, PlotTemplate)][0])
    mplt.draw()
    return mplt.mpl_plot.fig


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


def test_spam_repr(caplog, str_choice, rfull_repr):
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
    templates = rfull_repr(spamres)
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
