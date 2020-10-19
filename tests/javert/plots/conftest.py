'''Fixtures for the :mod:`~.valjean.javert.plot_repr` tests.'''
from collections import OrderedDict
import pytest
import numpy as np

from valjean.eponine.dataset import Dataset
from valjean.gavroche.stat_tests.student import TestStudent
from valjean.javert.representation import PlotRepresenter
from ...context import valjean  # noqa: F401, pylint: disable=unused-import


@pytest.fixture
def plot_repr():
    '''Create a :class:`~.PlotRepresenter` object.'''
    return PlotRepresenter()


@pytest.fixture
def plot_no_post_repr():
    '''Create a :class:`~.PlotRepresenter` object with no post-treatment.'''
    return PlotRepresenter(post='None')


@pytest.fixture
def studentt_res_range_lrbin():
    '''Return a Student test result from datasets with 2 large extreme bins
    triggering range adaptation.'''
    bins = OrderedDict([('e', np.array([-1000., 2.0, 3.0, 4.0, 5.0, 2000.]))])
    ds1 = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                  np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                  bins=bins, name="ds1", what='the quantity')
    ds2 = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                  np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_range_lbin():
    '''Return a Student test result from datasets with 2 large extreme bins,
    only the left one triggers range adaptation.'''
    bins = OrderedDict([('e', np.array([-1000., 2.0, 3.0, 4.0, 5.0, 1000.]))])
    ds1 = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                  np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                  bins=bins, name="ds1", what='the quantity')
    ds2 = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                  np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_range_rbin():
    '''Return a Student test result from datasets with a very large last bin
    triggering range adaptation.'''
    bins = OrderedDict([('e', np.array([0., 2.0, 3.0, 4.0, 5.0, 10000.]))])
    ds1 = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                  np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                  bins=bins, name="ds1", what='the quantity')
    ds2 = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                  np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d():
    '''Return a Student test result from 2-dimensions datasets.'''
    bins = OrderedDict([('e', np.array([0, 2, 4, 6, 8])),
                        ('t', np.array([0, 1, 2, 3]))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d_range_elr():
    '''Return a Student test result from 2-dimensions datasets with large first
    and last bins in e.'''
    bins = OrderedDict([('e', np.array([-2000, 2, 4, 6, 8000])),
                        ('t', np.arange(4))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d_range_etlr():
    '''Return a Student test result from 2-dimensions datasets with large first
    and last bins in e and t.'''
    bins = OrderedDict([('e', np.array([-2000, 2, 4, 6, 8000])),
                        ('t', np.array([-5000, 1, 2, 3000]))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d_range_etr():
    '''Return a Student test result from 2-dimensions datasets with large last
    bins in e and t.'''
    bins = OrderedDict([('e', np.array([0, 2, 4, 6, 8000])),
                        ('t', np.array([0, 1, 2, 3000]))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.2,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()
