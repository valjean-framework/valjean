# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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
