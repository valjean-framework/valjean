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
def studentt_res_2d_cbins():
    '''Return a Student test result from 2-dimensions datasets with axes given
    by center of bins.
    '''
    bins = OrderedDict([('e', np.array([-1, 0, 1, 2])),
                        ('t', np.array([0.5, 1, 1.5]))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d_irrcbins():
    '''Return a Student test result from 2-dimensions datasets with axes given
    by center of bins with irregular bins.
    '''
    bins = OrderedDict([('e', np.array([0, 0.5, 1, 2])),
                        ('t', np.array([0.5, 1, 2]))])
    tarr = np.arange(12).reshape(4, 3)
    ds1 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds1", what='the quantity')
    tarr = np.arange(12)[::-1].reshape(4, 3)
    ds2 = Dataset(tarr, tarr*0.5,
                  bins=bins, name="ds2", what='the quantity')
    return TestStudent(ds1, ds2, name='A Student test').evaluate()


@pytest.fixture
def studentt_res_2d_vbins():
    '''Return a Student test result from 2-dimensions datasets with x-axis
    given by bin edges and y-axis given by bin centers. Both are irregular.
    '''
    bins = OrderedDict([('e', np.array([0, 0.5, 1, 2, 3])),
                        ('t', np.array([0.5, 1, 2]))])
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
