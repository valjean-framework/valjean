'''Fixtures for the :mod:`~.valjean.javert` tests.'''

from hypothesis.strategies import (composite, tuples, integers, text, none,
                                   just, sampled_from, lists)
from hypothesis.extra.numpy import arrays, array_shapes

import pytest
import numpy as np

# pylint: disable=wrong-import-order,unused-import,no-value-for-parameter
from ..context import valjean  # noqa: F401
from ..eponine.conftest import finite
from ..gavroche.conftest import some_dataset, other_dataset
from valjean.javert.representation import (FullRepresenter, EmptyRepresenter,
                                           FullTableRepresenter,
                                           PlotRepresenter, Representation)
from valjean.javert.templates import TableTemplate, PlotTemplate, CurveElements
from valjean.javert.test_report import TestReport
from valjean.javert.rst import Rst, RstFormatter


@composite
def int_matrices(draw, min_rows=2, max_rows=10, min_cols=2, max_cols=10):
    '''Strategy to generate matrices of distinct integers.

    :param int min_rows: the minimum number of matrix rows.
    :param int max_rows: the maximum number of matrix rows.
    :param int min_columns: the minimum number of matrix columns.
    :param int max_columns: the maximum number of matrix columns.
    :returns: a matrix of random small integers.
    :rtype: :class:`numpy.ndarray`
    '''
    return draw(arrays(dtype=int,
                       shape=tuples(integers(min_rows, max_rows),
                                    integers(min_cols, max_cols)),
                       elements=integers(0, max_cols*max_rows),
                       unique=True))


@pytest.fixture
def rst_full(full_repr):
    '''Create an :class:`~.Rst` object with full representation.'''
    return Rst(representation=full_repr)


@pytest.fixture
def rst_formatter():
    '''Create an :class:`~.RstFormatter` object.'''
    return RstFormatter()


@pytest.fixture
def full_repr():
    '''Create a :class:`~.FullRepresenter` object.'''
    return Representation(FullRepresenter())


@pytest.fixture
def empty_repr():
    '''Create an :class:`~.EmptyRepresenter` object.'''
    return EmptyRepresenter()


@pytest.fixture
def table_repr():
    '''Create a :class:`~.TableRepresenter` object.'''
    return FullTableRepresenter()


@pytest.fixture
def plot_repr():
    '''Create a :class:`~.PlotRepresenter` object.'''
    return PlotRepresenter()


@composite
def valid_index(draw, *, shape):
    '''Strategy that generates a valid index into an array with the given
    shape.

    :param tuple(int) shape: the shape of the array.
    '''
    return tuple(draw(integers(-n, n-1)) for n in shape)


@pytest.fixture
def table_template(some_dataset, other_dataset):
    '''Create a simple :class:`~.TableTemplate` object.'''
    return TableTemplate(some_dataset.value, other_dataset.value,
                         headers=['some', 'other'],
                         units=['furlong', 'fortnight'])


@composite
def table_templates(draw, n_columns=integers(1, 5),
                    shape=array_shapes(min_side=1, max_side=5)):
    '''Strategy for generating :class:`~.TableTemplate` objects.'''
    a_n_columns = draw(n_columns)
    a_shape = draw(shape)
    a_columns = draw(lists(arrays(np.float64, a_shape, elements=finite()),
                           min_size=a_n_columns, max_size=a_n_columns))
    a_headers = draw(none()
                     | lists(text(),
                             min_size=a_n_columns,
                             max_size=a_n_columns))
    a_units = draw(none()
                   | lists(text(),
                           min_size=a_n_columns,
                           max_size=a_n_columns))
    a_highlights = draw(none()
                        | lists(arrays(bool, a_shape),
                                min_size=a_n_columns, max_size=a_n_columns))
    return TableTemplate(*a_columns, headers=a_headers, units=a_units,
                         highlights=a_highlights)


@composite
def curve_elements(draw, shape=None, legend=text(), label=text(),
                   index=integers(0, 10)):
    '''Strategy for generating :class:`~.CurveElements` objects.'''
    if shape is None:
        a_shape = draw(array_shapes())
    else:
        a_shape = draw(shape)
    a_values = draw(arrays(np.float64, a_shape, elements=finite()))
    a_errors = draw(none()
                    | arrays(np.float64, a_shape, elements=finite()))
    a_legend = draw(legend)
    a_label = draw(label)
    a_index = draw(index)
    return CurveElements(a_values, a_legend, label=a_label, errors=a_errors,
                         index=a_index)


@composite
def plot_templates(draw, n_curves=integers(1, 5), size=integers(1, 10),
                   xname=text()):
    '''Strategy for generating :class:`~.PlotTemplate` objects.'''
    a_n_curves = draw(n_curves)
    a_size = draw(size)
    a_bins_size = draw(sampled_from((a_size, a_size+1)))
    a_bins = draw(arrays(np.float64, shape=just(a_bins_size),
                         elements=finite(), unique=True))
    a_bins.sort()
    a_curves = [draw(curve_elements(shape=just(a_size)))
                for _ in range(a_n_curves)]
    a_xname = draw(xname)
    return PlotTemplate(bins=[a_bins], curves=a_curves, axnames=[a_xname])


@pytest.fixture
def report_section1(equal_test_result, equal_test_result_fail,
                    report_section3):
    '''Create a simple :class:`~.TestReport` object.'''
    return TestReport(title='A section title',
                      content=[equal_test_result,
                               equal_test_result_fail,
                               report_section3])


@pytest.fixture
def report_section2(bonferroni_test_result, student_test_result,
                    student_test_result_fail):
    '''Create another simple :class:`~.TestReport` object.'''
    return TestReport(title='Another amazing section title!',
                      content=[bonferroni_test_result,
                               student_test_result,
                               student_test_result_fail])


@pytest.fixture
def report_section3(approx_equal_test_result):
    '''Create yet another simple :class:`~.TestReport` object.'''
    return TestReport(title='A subsubsection title',
                      content=[approx_equal_test_result])


@pytest.fixture
def report(report_section1, report_section2,
           holm_bonf_test_result_fail):
    '''Create a :class:`~.TestReport` object aggregating two other test
    reports and a test result.'''
    return TestReport(title='The report title! Too many exclamation marks!!!',
                      content=[report_section1, report_section2,
                               holm_bonf_test_result_fail])


@pytest.fixture
def rstcheck():
    '''Import and return the :mod:`rstcheck` module, if it is installed. If it
    isn't, tests depending on this fixture will be automatically skipped.'''
    return pytest.importorskip('rstcheck')
