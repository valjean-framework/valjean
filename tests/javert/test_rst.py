'''Tests for the :mod:`~valjean.javert.rst` module.'''
# pylint: disable=unused-argument

import numpy as np
from hypothesis import given, note

# pylint: disable=wrong-import-order
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean import LOGGER
from valjean.javert.rst import RstTable
from valjean.javert.templates import join
from valjean.javert.table_elements import repr_bins
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
                                 student_test_with_pvals,
                                 bonferroni_test_fail,
                                 bonferroni_test_result_fail,
                                 student_test_fail_with_pvals,
                                 holm_bonferroni_test,
                                 holm_bonferroni_test_result,
                                 holm_bonferroni_test_fail,
                                 holm_bonf_test_result_fail, datasets)


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


def test_rst_table(rstcheck, table_template, rst_formatter):
    '''Test that :class:`~.RstFormatter` generates correct reST tables.'''
    table = str(rst_formatter.template(table_template))
    LOGGER.debug('generated rst:\n%s', table)
    errs = rstcheck.check(table)
    assert not list(errs)


def test_rst_equal(rstcheck, equal_test_result, rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test.'''
    templates = table_repr(equal_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_equal_full(rstcheck, equal_test_result, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test.'''
    templates = table_repr(equal_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_equal_hl(rstcheck, equal_test_result_fail, rst_formatter,
                      table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an equality test with highlighted elements.'''
    templates = table_repr(equal_test_result_fail)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    # patch the generated rst with a declaration for the highlight role
    rst = '.. role:: hl\n\n' + rst
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_approx_equal(rstcheck, approx_equal_test_result, rst_formatter,
                          table_repr):
    '''Test that :class:`~.RstFormatter` yields syntactically correct reST
    tables when formatting an approximate equality test.'''
    templates = table_repr(approx_equal_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_student(rstcheck, student_test_result, rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table.'''
    templates = table_repr(student_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_student_hl(rstcheck, student_test_result_fail, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Student results.'''
    templates = table_repr(student_test_result_fail)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    # patch the generated rst with a declaration for the highlight role
    rst = '.. role:: hl\n\n' + rst
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_bonferroni(rstcheck, bonferroni_test_result, rst_formatter,
                        table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Bonferroni result.'''
    templates = table_repr(bonferroni_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
    LOGGER.debug('generated rst:\n%s', rst)
    # print()
    # print(rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_holm_bonferroni(rstcheck, holm_bonferroni_test_result,
                             rst_formatter, table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Holm-Bonferroni results.'''
    templates = table_repr(holm_bonferroni_test_result)
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates)
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
    templates = table_repr(bonferroni_test_result)
    templates2 = table_repr(bonferroni_test_result_fail)
    ntabtemplate = templates + templates2
    rst = str(rst_formatter.template(ntabtemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_rst_holm_bonferronis(rstcheck, holm_bonferroni_test_result,
                              holm_bonf_test_result_fail, rst_formatter,
                              table_repr):
    '''Test that :class:`~.RstFormatter` generates correct reST table for
    Holm-Bonferroni results.'''
    templates = table_repr(holm_bonferroni_test_result)
    templates2 = table_repr(holm_bonf_test_result_fail)
    ntabtemplate = templates + templates2
    rst = str(rst_formatter.template(ntabtemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)


def test_tabletemplate_tjoin(table_repr,
                             bonferroni_test_result,
                             bonferroni_test_result_fail):
    '''Test :meth:`~valjean.javert.templates.TableTemplate.join`.'''
    templates = table_repr(bonferroni_test_result)
    templates_id = id(templates[1])
    LOGGER.debug("templates = %s", templates)
    templates2 = table_repr(bonferroni_test_result_fail)
    LOGGER.debug("templates2 = %s", templates2)
    templates[1].join(templates2[1])
    LOGGER.debug("templates+templates2 = %s", templates)
    assert id(templates[1]) != id(templates2[1])
    assert id(templates[1]) == templates_id
    assert all(tuple((row[0] in templates[1].columns[i]
                      for i, row in enumerate(templates2[1].columns))))


def test_tabletemplate_join(table_repr,
                            bonferroni_test_result,
                            bonferroni_test_result_fail):
    '''Test  :meth:`~valjean.javert.templates.join`.'''
    templates1 = table_repr(bonferroni_test_result)
    LOGGER.debug("templates1 = %s", templates1)
    first_test = bonferroni_test_result_fail.first_test_res
    first_test.test.datasets[0].name = "other 1D dataset"
    templates2 = table_repr(bonferroni_test_result_fail)
    LOGGER.debug("templates2 = %s", templates2)
    templates3 = join(templates1[1], templates2[1])
    LOGGER.debug("templates1+templates2 = %s", templates3)
    assert id(templates1[1]) != id(templates2[1])
    assert id(templates1[1]) != id(templates3)
    assert id(templates2[1]) != id(templates3)
    # check the 2 results are not identical = contains some different elements
    assert any(tuple((row[0] not in templates2[1].columns[i]
                      for i, row in enumerate(templates1[1].columns))))
    # templates1 column elements are all in templates3
    assert all(tuple((row[0] in templates3.columns[i]
                      for i, row in enumerate(templates1[1].columns))))
    # templates2 column elements are all in templates3
    assert all(tuple((row[0] in templates3.columns[i]
                      for i, row in enumerate(templates2[1].columns))))
    templates4 = templates1 + templates2
    LOGGER.debug("templates1+templates2 = %s", templates4)
    assert len(templates4) == 4
    templates5 = [join(it1, it2) for it1, it2 in zip(templates1, templates2)]
    LOGGER.debug("templates1+templates2 = %s", templates5)
    assert len(templates5) == 2
    assert templates5[0].headers[-1] == 'Student(other 1D dataset)?'
    assert templates5[0].columns[0].size == 10
    assert templates5[1].headers[-1] == 'Bonferroni?'


def test_tabletemplate_join_array(table_repr,
                                  student_test_result,
                                  student_test_result_fail):
    '''Test join table templates containing arrays.'''
    template1 = table_repr(student_test_result)
    template1_cc = template1[0].copy()
    LOGGER.debug('template1 = %s', template1)
    student_test_result_fail.test.datasets[0].name = "other 1D dataset"
    template2 = table_repr(student_test_result_fail)
    LOGGER.debug('template2 = %s', template2)
    template1[0].join(template2[0])
    LOGGER.debug('after join: template1 = %s', template1)
    assert template1[0].headers == template1_cc.headers
    assert template1[0].headers == template2[0].headers
    assert all(col.size == col1.size + col2.size
               for col, col1, col2 in zip(template1[0].columns,
                                          template1_cc.columns,
                                          template2[0].columns))
    assert all(np.isin(template1[0].columns[4][template1_cc.columns[4].size:],
                       template2[0].columns[4]))
    assert all(np.isin(template1[0].columns[4][:template1_cc.columns[4].size],
                       template1_cc.columns[4]))


def test_rst_report(rstcheck, report, rst_full, tmpdir):
    '''Test that :class:`~.RstFormatter` correctly generates a report.'''
    fmt_report = rst_full.format_report(report=report, author='pytest',
                                        version='0.1')
    LOGGER.debug('generated rst:\n%s', fmt_report)
    fmt_report.write(str(tmpdir))
    for path in tmpdir.visit(fil='*.rst'):
        content = path.read()
        errs = rstcheck.check(content)
        assert not list(errs), content


@given(dset=datasets())  # pylint: disable=no-value-for-parameter
def test_repr_bins(dset):
    '''Check bins representation'''
    note('dataset: {}'.format(dset))
    names, bins = repr_bins(dset)
    dset_squeezed = dset.squeeze()
    note('squeezed dataset: {}'.format(dset_squeezed))
    squeezed_ndim = len(dset.shape) - dset.shape.count(1)
    assert len(names) == squeezed_ndim
    assert len(bins) == squeezed_ndim
    assert all(dset.shape == abin.shape for abin in bins)
