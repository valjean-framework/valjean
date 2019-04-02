'''Tests for the :mod:`~.templates` module.'''

from hypothesis import given
from hypothesis.strategies import text, data, integers
# pylint: disable=wrong-import-order
from .conftest import plot_templates, table_templates, valid_index


@given(plot_t=plot_templates())  # pylint: disable=no-value-for-parameter
def test_copy_plot_fingerprint(plot_t):
    '''Test that a :class:`~.PlotTemplate` and its copy have the same
    fingerprint.'''
    copy = plot_t.copy()
    assert plot_t == copy
    assert plot_t.fingerprint() == copy.fingerprint()


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1))
def test_xname_plot_fingerprint(plot_t, more_text):
    '''Test that changing the `xname` attribute of :class:`~.PlotTemplate`
    affects its fingerprint.'''
    copy = plot_t.copy()
    copy.xname += more_text
    assert plot_t != copy
    assert plot_t.fingerprint() != copy.fingerprint()


@given(plot_t=plot_templates())  # pylint: disable=no-value-for-parameter
def test_bins_plot_fingerprint(plot_t):
    '''Test that changing the `xname` attribute of :class:`~.PlotTemplate`
    affects its fingerprint.'''
    copy = plot_t.copy()
    copy.bins[-1] *= 1.1
    copy.bins[-1] += 1.0
    assert plot_t != copy
    assert plot_t.fingerprint() != copy.fingerprint()


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1), sampler=data())
def test_clabel_plot_fingerprint(plot_t, more_text, sampler):
    '''Test that changing the `label` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    index = sampler.draw(integers(0, len(copy.curves) - 1))
    copy.curves[index].label += more_text
    assert plot_t != copy
    assert plot_t.fingerprint() != copy.fingerprint()


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       more_text=text(min_size=1), sampler=data())
def test_cyname_plot_fingerprint(plot_t, more_text, sampler):
    '''Test that changing the `yname` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    index = sampler.draw(integers(0, len(copy.curves) - 1))
    copy.curves[index].yname += more_text
    assert plot_t != copy
    assert plot_t.fingerprint() != copy.fingerprint()


@given(plot_t=plot_templates(),  # pylint: disable=no-value-for-parameter
       sampler=data())
def test_cvals_plot_fingerprint(plot_t, sampler):
    '''Test that changing the `yname` of any :class:`~.PlotTemplate` curve
    affects the fingerprint of the plot template.'''
    copy = plot_t.copy()
    index = sampler.draw(integers(0, len(copy.curves) - 1))
    values = copy.curves[index].values
    # pylint: disable=no-value-for-parameter
    values_index = sampler.draw(valid_index(shape=values.shape))
    values[values_index] *= 1.1
    values[values_index] += 1.0
    assert plot_t != copy
    assert plot_t.fingerprint() != copy.fingerprint()


@given(table_t=table_templates())  # pylint: disable=no-value-for-parameter
def test_copy_table_fingerprint(table_t):
    '''Test that a :class:`~.TableTemplate` and its copy have the same
    fingerprint.'''
    copy = table_t.copy()
    assert table_t == copy
    assert table_t.fingerprint() == copy.fingerprint()


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
    assert table_t.fingerprint() != copy.fingerprint()