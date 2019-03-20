'''Fixtures for the :mod:`~.valjean.javert` tests.'''

from hypothesis.strategies import composite, tuples, integers
from hypothesis.extra.numpy import arrays

import pytest

# pylint: disable=wrong-import-order,unused-import,no-value-for-parameter
from ..context import valjean  # noqa: F401
from ..gavroche.conftest import some_dataset, other_dataset
from valjean.javert.representation import (FullRepresenter, EmptyRepresenter,
                                           FullTableRepresenter,
                                           PlotRepresenter, Representation)
from valjean.javert.templates import TableTemplate
from valjean.javert.rst import RstFormatter
from valjean.javert.mpl import MplPlot


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


@pytest.fixture
def table_template(some_dataset, other_dataset):
    # pylint: disable=redefined-outer-name
    '''Create a simple :class:`~.TableTemplate` object.'''
    return TableTemplate(some_dataset.value, other_dataset.value,
                         headers=['some', 'other'],
                         units=['furlong', 'fortnight'])


@pytest.fixture
def rstcheck():
    '''Import and return the :mod:`rstcheck` module, if it is installed. If it
    isn't, tests depending on this fixture will be automatically skipped.'''
    return pytest.importorskip('rstcheck')
