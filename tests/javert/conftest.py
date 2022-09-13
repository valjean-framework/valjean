# Copyright French Alternative Energies and Atomic Energy Commission
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

'''Fixtures for the :mod:`~.valjean.javert` tests.'''

from hypothesis import assume
from hypothesis.strategies import (composite, tuples, integers, text, none,
                                   just, sampled_from, lists, booleans)
from hypothesis.extra.numpy import arrays, array_shapes

# pylint: disable=wrong-import-order,unused-import,no-value-for-parameter
import string
import pytest
import numpy as np

from ..context import valjean  # noqa: F401
from ..eponine.conftest import finite
from ..gavroche.conftest import some_dataset, other_dataset, run_tasks
from valjean import LOGGER
from valjean.javert.verbosity import Verbosity
from valjean.javert.representation import (FullRepresenter, EmptyRepresenter,
                                           FullTableRepresenter,
                                           PlotRepresenter, Representation)
from valjean.javert.templates import (TableTemplate, PlotTemplate,
                                      SubPlotElements, CurveElements,
                                      TextTemplate)
from valjean.javert.test_report import TestReport
from valjean.javert.rst import Rst, RstFormatter


ALPHABET_RST = string.ascii_letters + string.digits


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
def rfull_repr():
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


@pytest.fixture
def full_repr():
    '''Create a :class:`~.FullRepresenter` object.'''
    return FullRepresenter()


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


@pytest.fixture
def text_template():
    '''Create a text template with ReST marks.'''
    return TextTemplate(
        'Essai de rst\n'
        '============\n'
        '\n'
        '.. role:: hl\n'
        '\n'
        'Un essai de **text** avec :hl:`balises` et *tout* et `tout`\n'
        '\n'
        '* et\n'
        '* une\n'
        '* liste\n')


@pytest.fixture
def plot_template():
    '''Create a plot template.'''
    celt0 = CurveElements(values=np.arange(5), bins=[np.arange(6)],
                          legend='c0', index=0)
    celt1 = CurveElements(values=np.arange(5)*1.2, bins=[np.arange(6)],
                          legend='c1', index=1)
    return PlotTemplate(subplots=[SubPlotElements(
        curves=[celt0, celt1], axnames=('X', 'Y'))])


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
def curve_elements(draw, legend=text(), index=integers(0, 10), shape=None):
    # pylint: disable=too-many-arguments
    '''Strategy for generating :class:`~.CurveElements` objects.'''
    if shape is None:
        a_shape = draw(array_shapes())
    else:
        a_shape = draw(shape)
    a_size = a_shape if isinstance(a_shape, int) else a_shape[0]
    a_values = draw(arrays(np.float64, a_shape, elements=finite()))
    a_errors = draw(none()
                    | arrays(np.float64, a_shape, elements=finite()))
    a_bins_size = draw(sampled_from((a_size, a_size+1)))
    a_bins = draw(arrays(np.float64, shape=just(a_bins_size),
                         elements=finite(), unique=True))
    a_bins.sort()
    return CurveElements(a_values, legend=draw(legend),
                         errors=a_errors, index=draw(index), bins=[a_bins])


@composite
def sub_plot_elements(draw, n_curves=integers(1, 3), xname=text()):
    '''Strategy for generating :class:`~.SubPlotElements` objects.'''
    a_n_curves = draw(n_curves)
    a_curves = [draw(curve_elements(shape=integers(1, 10)))
                for _ in range(a_n_curves)]
    a_xname = draw(xname)
    return SubPlotElements(curves=a_curves,
                           axnames=[a_xname, draw(text())],
                           ptype='1D')


@composite
def plot_templates(draw, n_subplots=integers(1, 5), same_xaxis=booleans()):
    '''Strategy for generating :class:`~.PlotTemplate` objects.'''
    a_n_subplots = draw(n_subplots)
    a_same_xaxis = draw(same_xaxis)
    if a_same_xaxis:
        a_xname = draw(text())
        a_subplots = [draw(sub_plot_elements(xname=just(a_xname)))
                      for _ in range(a_n_subplots)]
    else:
        a_subplots = [draw(sub_plot_elements(xname=text()))
                      for _ in range(a_n_subplots)]
    return PlotTemplate(subplots=a_subplots)


@composite
def text_templates(draw, ltext=text(alphabet=ALPHABET_RST, min_size=2)):
    '''Strategy for generating :class:`~.TextTemplate` objects.'''
    a_text = draw(ltext)
    return TextTemplate(a_text)


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
    '''Import and return the `rstcheck` module, if it is installed. If it
    isn't, tests depending on this fixture will be automatically skipped.'''

    class RstCheckWrapper:
        '''A wrapper class to ignore specific :mod:`rstcheck` warnings.'''

        IGNORE = r'(Hyperlink target .* is not referenced)'
        RSTCHECK = pytest.importorskip('rstcheck')

        @classmethod
        def check(cls, rst):
            '''Call :func:`rstcheck.check` with the predefined ignore
            pattern.'''
            return cls.RSTCHECK.check(rst, ignore={'messages': cls.IGNORE})

    return RstCheckWrapper


@pytest.fixture(
    params=[['table_template'], ['plot_template'], ['text_template'],
            ['text_template', 'plot_template', 'table_template']],
    ids=['table', 'plot', 'text', 'all of them'])
def templates(request):
    '''Return lists of valid :class:`~.Test` objects.'''
    fixtures = [request.getfixturevalue(fix_name)
                for fix_name in request.param]
    return fixtures


@composite
def ranges(draw, min_value=None, max_value=None):
    '''Strategy to generate valid float ranges.

    A range `(l, h)` is valid if `l < h`.
    '''
    bounds = draw(tuples(finite(min_value=min_value, max_value=max_value),
                         finite(min_value=min_value, max_value=max_value)))
    assume(bounds[0] != bounds[1])
    return min(bounds), max(bounds)


@pytest.fixture(params=list(Verbosity), ids=list(v.name for v in Verbosity))
def verb_level(request):
    '''Return lists of valid :class:`~.Test` objects.'''
    return request.param


def check_rst(rstcheck, rst_formatter, templates):
    '''Factorized checks for rst generation'''
    rst = '\n'.join(str(rst_formatter.template(template))
                    for template in templates
                    if isinstance(template, TableTemplate))
    LOGGER.debug('generated rst:\n%s', rst)
    errs = rstcheck.check(rst)
    assert not list(errs)
