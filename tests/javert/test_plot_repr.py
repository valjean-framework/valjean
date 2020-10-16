'''Tests for the :mod:`~valjean.javert.plot_repr` module.'''
# pylint: disable=wrong-import-order

import numpy as np
from hypothesis import given

from ..eponine.conftest import finite
from .conftest import ranges

from ..context import valjean  # pylint: disable=unused-import
from valjean.javert.plot_repr import pad_range


@given(limits=ranges())  # pylint: disable=no-value-for-parameter
def test_pad_range_zero_lin(limits):
    '''Test that :func:`~.pad_range` with zero padding does not modify the
    input range, in linear scale.'''
    new_limits = pad_range(limits, log=False, padding=0.0)
    assert new_limits == limits


@given(limits=ranges(1e-300))  # pylint: disable=no-value-for-parameter
def test_pad_range_zero_log(limits):
    '''Test that :func:`~.pad_range` with zero padding does not modify the
    input range, in log scale.'''
    new_limits = pad_range(limits, log=True, padding=0.0)
    assert new_limits == limits


@given(limits=ranges(),  # pylint: disable=no-value-for-parameter
       padding=finite(1e-2, 10.0))
def test_pad_range_wider_lin(limits, padding):
    '''Test that :func:`~.pad_range` increases the range by the expected amount
    (padding), in linear scale.'''
    new_limits = pad_range(limits, log=False, padding=padding)
    width = limits[1] - limits[0]
    new_width = new_limits[1] - new_limits[0]
    expected = width*(1.0 + padding)
    assert np.isclose(expected, new_width)
    assert new_limits[0] <= limits[0]
    assert new_limits[1] >= limits[1]
    assert np.isclose(limits[0] - new_limits[0], new_limits[1] - limits[1])


@given(limits=ranges(1e-30),  # pylint: disable=no-value-for-parameter
       padding=finite(1e-2, 10.0))
def test_pad_range_wider_log(limits, padding):
    '''Test that :func:`~.pad_range` increases the range by the expected amount
    (padding), in log scale.'''
    new_limits = pad_range(limits, log=True, padding=padding)
    width = np.log(limits[1]) - np.log(limits[0])
    new_width = np.log(new_limits[1]) - np.log(new_limits[0])
    expected = width*(1.0 + padding)
    assert np.isclose(expected, new_width)
    assert new_limits[0] <= limits[0]
    assert new_limits[1] >= limits[1]
    assert np.isclose(np.log(limits[0]) - np.log(new_limits[0]),
                      np.log(new_limits[1]) - np.log(limits[1]))
