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

'''Tests for the :mod:`~.templates` module.'''

import numpy as np
from hypothesis import given
from hypothesis.strategies import text, data, integers
# pylint: disable=wrong-import-order
from .conftest import (plot_templates, table_templates, valid_index,
                       text_templates)
from valjean.fingerprint import fingerprint
from valjean.javert.templates import TableTemplate


@given(plot_t=plot_templates())  # pylint: disable=no-value-for-parameter
def test_copy_plot_fingerprint(plot_t):
    '''Test that a :class:`~.PlotTemplate` and its copy have the same
    fingerprint.'''
    copy = plot_t.copy()
    assert plot_t == copy
    assert fingerprint(plot_t) == fingerprint(copy)


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1))
def test_xname_plot_fingerprint(plot_t, more_text):
    '''Test that changing the first element of the `axnames` attribute of
    :class:`~.PlotTemplate` affects its fingerprint.'''
    copy = plot_t.copy()
    copy.subplots[0].axnames[0] += more_text
    assert plot_t != copy
    assert fingerprint(plot_t) != fingerprint(copy)


@given(plot_t=plot_templates())  # pylint: disable=no-value-for-parameter
def test_bins_plot_fingerprint(plot_t):
    '''Test that changing the `bins` attribute of :class:`~.PlotTemplate`
    affects its fingerprint. THe last bin of the first dimension is used.
    '''
    copy = plot_t.copy()
    copy.subplots[0].curves[0].bins[0][-1] *= 1.1
    copy.subplots[0].curves[0].bins[0][-1] += 1.0
    assert plot_t != copy
    assert fingerprint(plot_t) != fingerprint(copy)


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1), sampler=data())
def test_clegend_plot_fingerprint(plot_t, more_text, sampler):
    '''Test that changing the `legend` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    index = sampler.draw(integers(0, len(copy.subplots[0].curves) - 1))
    copy.subplots[0].curves[index].legend += more_text
    assert plot_t != copy
    assert fingerprint(plot_t) != fingerprint(copy)


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1), sampler=data())
def test_yname_plot_fingerprint(plot_t, more_text, sampler):
    '''Test that changing the `label` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    index = sampler.draw(integers(0, len(copy.subplots) - 1))
    copy.subplots[index].axnames[1] += more_text
    assert plot_t != copy
    assert fingerprint(plot_t) != fingerprint(copy)


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       sampler=data())
def test_cvals_plot_fingerprint(plot_t, sampler):
    '''Test that changing the `label` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    isplt = sampler.draw(integers(0, len(copy.subplots) - 1))
    icrv = sampler.draw(integers(0, len(copy.subplots[isplt].curves) - 1))
    values = copy.subplots[isplt].curves[icrv].values
    # pylint: disable=no-value-for-parameter
    values_index = sampler.draw(valid_index(shape=values.shape))
    values[values_index] *= 1.1
    values[values_index] += 1.0
    assert plot_t != copy
    assert fingerprint(plot_t) != fingerprint(copy)


@given(table_t=table_templates())  # pylint: disable=no-value-for-parameter
def test_copy_table_fingerprint(table_t):
    '''Test that a :class:`~.TableTemplate` and its copy have the same
    fingerprint.'''
    copy = table_t.copy()
    assert table_t == copy
    assert fingerprint(table_t) == fingerprint(copy)


@given(table_t=table_templates(),  # pylint: disable=no-value-for-parameter
       sampler=data())
def test_tcolumns_table_fingerprint(table_t, sampler):
    '''Test that a :class:`~.TableTemplate` and its copy have the same
    fingerprint.'''
    copy = table_t.copy()
    index = sampler.draw(integers(0, len(copy.columns) - 1))
    column = copy.columns[index]
    # pylint: disable=no-value-for-parameter
    column_index = sampler.draw(valid_index(shape=column.shape))
    column[column_index] *= 1.1
    column[column_index] += 1.0
    assert table_t != copy
    assert fingerprint(table_t) != fingerprint(copy)


@given(text_t=text_templates())  # pylint: disable=no-value-for-parameter
def test_copy_text_fingerprint(text_t):
    '''Test that a :class:`~.TextTemplate` and its copy have the same
    fingerprint.'''
    copy = text_t.copy()
    assert text_t == copy
    assert fingerprint(text_t) == fingerprint(copy)


@given(text_t=text_templates(),  # pylint: disable=no-value-for-parameter
       sampler=data())
def test_modif_text_fingerprint(text_t, sampler):
    '''Test that a :class:`~.TextTemplate` and its copy have the same
    fingerprint.'''
    copy = text_t.copy()
    copy.text += sampler.draw(text(alphabet='azertyuiop', min_size=1))
    assert text_t != copy
    assert fingerprint(text_t) != fingerprint(copy)


def test_table_list():
    '''Check that fingerprint are equal when containing the same data.
    Pretext to test list inside :class:`~.TableTemplate` and their
    fingerprints.
    '''
    tab1 = TableTemplate(['s', 'p', 'a', 'm'], np.arange(4)*0.5,
                         headers=['egg', 'bacon'])
    tab2 = TableTemplate(np.array(['s', 'p', 'a', 'm']), np.arange(4)*0.5,
                         headers=['egg', 'bacon'])
    assert fingerprint(tab1) == fingerprint(tab2)
