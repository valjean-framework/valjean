# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''Tests of the logger: check that the different levels appear corretly, that
it can be set by module or sub-package.
'''
from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import logging

# pylint: disable=unused-import
from ..gavroche.conftest import (some_1d_dataset, other_1d_dataset,
                                 different_1d_dataset, some_dataset,
                                 other_dataset, different_dataset,
                                 student_test_with_pvals,
                                 student_test_fail_with_pvals,
                                 holm_bonferroni_test_fail,
                                 holm_bonf_test_result_fail,
                                 equal_test_result, equal_test,
                                 equal_test_result_fail, equal_test_fail,
                                 approx_equal_test_result, approx_equal_test,
                                 bonferroni_test_result, bonferroni_test,
                                 student_test_result, student_test,
                                 student_test_result_fail, student_test_fail)
from ..javert.conftest import (full_repr, rst_formatter, report, rst_full,
                               report_section1, report_section2,
                               report_section3)
from valjean.javert.test_report import TestReport
from valjean import set_logger_level, local_logger_level
from valjean.eponine.tripoli4.parse import Parser
from valjean.gavroche.stat_tests.student import TestStudent
from valjean.gavroche.stat_tests.bonferroni import TestHolmBonferroni


LOG_LEVELS = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO,
              logging.NOTE, logging.DEBUG]


def test_valjean_logger(caplog, log_level, report, rst_full, tmpdir):
    '''Test levels of valjean logger (common to all modules).'''
    with local_logger_level('valjean', log_level):
        fmt_report = rst_full.format_report(report=report, author='pytest',
                                            version='0.1')
        fmt_report.write(str(tmpdir))
    if log_level > logging.INFO:
        assert len(caplog.records) == 0
    elif log_level == logging.INFO:
        assert len(caplog.records) == 1
        assert any(rec.levelno == log_level for rec in caplog.records)
    else:
        assert len(caplog.records) > 1
        assert any(rec.levelno == logging.INFO for rec in caplog.records)
        assert any(rec.levelno == log_level for rec in caplog.records)
        assert ("Will adapt range for 3 bins, binning might be not "
                "suitable" in caplog.text)
        assert "writing tree_path" in caplog.text
    assert all(rec.module in ("plot_repr", "rst")
               for rec in caplog.records if rec.levelno == logging.NOTE)


def test_module_logger(caplog, log_level, report, rst_full, tmpdir):
    '''Test logger at module level.'''
    with local_logger_level('valjean.javert.plot_repr', log_level):
        fmt_report = rst_full.format_report(report=report, author='pytest',
                                            version='0.1')
        fmt_report.write(str(tmpdir))
    plot_repr_recs = [rec for rec in caplog.records
                      if rec.module == "plot_repr"]
    other_recs = [rec for rec in caplog.records if rec.module != "plot_repr"]
    assert len(other_recs) == 1
    assert "writing 4 plots in sequential mode" in caplog.text
    assert all(rec.levelno == logging.INFO for rec in other_recs)
    assert all(rec.module in ("rst",) for rec in other_recs)
    if log_level > logging.NOTE:
        assert len(plot_repr_recs) == 0
    elif log_level == logging.NOTE:
        assert len(plot_repr_recs) == 6
        assert all("Will adapt range for 3 bins" in rec.message
                   for rec in plot_repr_recs)
        assert "Will adapt range for 3 bins" in caplog.text
    else:
        assert all(rec.levelno in (logging.NOTE, logging.DEBUG)
                   for rec in plot_repr_recs)


def test_set_logger_level(caplog, report, rst_full, tmpdir):
    '''Test ``set_logger_level`` function.'''
    saved_level = logging.getLogger('valjean').getEffectiveLevel()
    set_logger_level("valjean", logging.NOTE)
    fmt_report = rst_full.format_report(report=report, author='pytest',
                                        version='0.1')
    fmt_report.write(str(tmpdir))
    assert set(rec.levelno for rec in caplog.records) == {logging.INFO,
                                                          logging.NOTE}
    caplog.clear()
    set_logger_level("valjean", saved_level)
    fmt_report = rst_full.format_report(report=report, author='pytest',
                                        version='0.1')
    fmt_report.write(str(tmpdir))
    assert all(rec.levelno >= saved_level for rec in caplog.records)


def gauss_report(datadir):
    '''Build a ``TestReport`` from the T4 result on gauss distributions.'''
    t4p = Parser(str(datadir/"gauss_E_time_mu_phi.res.ceav5"))
    assert t4p
    t4b = t4p.parse_from_index(-1).to_browser()
    r_et = t4b.select_by(score_name='courant_Et')
    et_dist = r_et["results"]['score'].squeeze()
    et12_stud = TestStudent(et_dist[:, 1:2].squeeze(),
                            et_dist[:, 2:3].squeeze(),
                            name="comp time bins 1 and 2",
                            ndf=r_et['results']['used_batches'].value)
    et12_hb = TestHolmBonferroni(test=et12_stud,
                                 name="HB all t").evaluate()
    greport = TestReport(title="et12 comp", content=[et12_hb])
    return greport


def test_eponine_logs(caplog, log_level, datadir, tmpdir, rst_full):
    '''Test logger on ``eponine`` sub-package using ``gauss_report``.'''
    with local_logger_level('valjean.eponine', log_level):
        greport = gauss_report(datadir)
        fmt_report = rst_full.format_report(
            report=greport, author="pytest", version="0.1")
        fmt_report.write(str(tmpdir))
    eponine_recs = [rec for rec in caplog.records if "eponine" in rec.name]
    other_recs = [rec for rec in caplog.records if "eponine" not in rec.name]
    assert len(other_recs) == 1
    if log_level > logging.INFO:
        assert len(eponine_recs) == 0
    elif log_level in (logging.INFO, logging.NOTE):
        assert len(eponine_recs) == 3
        assert all(rec.levelno in (logging.WARNING, logging.INFO)
                   for rec in eponine_recs)
        assert "Successful scan" in caplog.text
        assert "Successful parsing" in caplog.text
    else:
        assert any(rec.levelno == logging.DEBUG for rec in eponine_recs)
        assert len(eponine_recs) > 200


def test_javert_logs(caplog, log_level, datadir, tmpdir, rst_full):
    '''Test logger on ``javert`` sub-package using ``gauss_report``.'''
    with local_logger_level('valjean.javert', log_level):
        greport = gauss_report(datadir)
        fmt_report = rst_full.format_report(
            report=greport, author="pytest", version="0.1")
        fmt_report.write(str(tmpdir))
    javert_recs = [rec for rec in caplog.records if "javert" in rec.name]
    other_recs = [rec for rec in caplog.records if "javert" not in rec.name]
    assert len(other_recs) == 3
    if log_level > logging.INFO:
        assert len(javert_recs) == 0
    elif log_level == logging.INFO:
        assert len(javert_recs) == 1
        assert all(rec.module in ('rst',) for rec in javert_recs)
    elif log_level == logging.NOTE:
        assert len(javert_recs) == 2
        assert all(rec.module in ('rst',) for rec in javert_recs)
    else:
        assert len(javert_recs) > 40
        assert all(rec.levelno in (logging.INFO, logging.NOTE, logging.DEBUG)
                   for rec in javert_recs)


def test_custom_epjav1(caplog, datadir, rst_full, tmpdir):
    '''Test logger with a high level first (``WARNING``) and low one next
    (``DEBUG``).
    '''
    with local_logger_level('valjean.eponine', logging.WARNING),\
         local_logger_level('valjean.javert.plot_repr', logging.DEBUG):
        greport = gauss_report(datadir)
        fmt_report = rst_full.format_report(
            report=greport, author="pytest", version="0.1")
        fmt_report.write(str(tmpdir))
    assert len([rec for rec in caplog.records if "eponine" in rec.name]) == 0
    assert all(rec.levelno == logging.DEBUG for rec in caplog.records
               if rec.module == "plot_repr")
    assert "rst" in [rec.module for rec in caplog.records]
    assert set(rec.levelno for rec in caplog.records) == {logging.INFO,
                                                          logging.DEBUG}


def test_custom_epjav2(caplog, datadir, rst_full, tmpdir):
    '''Test logger with a low level first (``DEBUG``) and high one next
    (``WARNING``).
    '''
    with local_logger_level('valjean.eponine.tripoli4.common', logging.DEBUG),\
         local_logger_level('valjean.javert', logging.WARNING):
        greport = gauss_report(datadir)
        fmt_report = rst_full.format_report(
            report=greport, author="pytest", version="0.1")
        fmt_report.write(str(tmpdir))
    assert len([rec for rec in caplog.records if "javert" in rec.name]) == 0
    assert all(rec.levelno == logging.DEBUG for rec in caplog.records
               if rec.module == "common")
    assert "rst" not in [rec.module for rec in caplog.records]
    assert set(rec.levelno for rec in caplog.records) == {logging.INFO,
                                                          logging.DEBUG}
