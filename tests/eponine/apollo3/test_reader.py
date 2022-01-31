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

'''Tests for the :mod:`~.hdf5_reader` module: read Apollo3 HDF outputs and
build a Browser from them.
'''
import numpy as np
from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.eponine.apollo3.hdf5_reader import Reader, hdf_to_browser


def test_rnr_a3c_api(datadir):
    '''Test Apollo3 rates output, with localvalues.'''
    ap3r = Reader(str(datadir/"RnR_A3C_API.hdf"))
    assert ap3r.res
    ap3b = ap3r.to_browser()
    assert ap3b
    assert len(ap3b.keys()) == 5
    assert set(ap3b.keys()) == {'result_name', 'zone', 'output', 'index',
                                'isotope'}
    assert all('results' in res for res in ap3b.content)
    assert ({'keff', 'production', 'Eigen value Minos', 'Eigen value Minaret',
             'flux', 'nufission', 'total'}
            == set(ap3b.available_values('result_name')))
    assert ['output_0'] == list(ap3b.available_values('output'))
    assert ['macro'] == list(ap3b.available_values('isotope'))
    assert len(ap3b.available_values('zone')) == 21
    assert set(ap3b.globals.keys()) == {'info', 'geometry'}
    assert len(ap3b.globals['info']) == len(ap3r.res)
    assert (len(ap3b.globals['info'])
            == len(ap3b.available_values('output')))
    assert (sum([len(g) for g in ap3b.globals['geometry'].values()])
            == len(ap3b.available_values('zone')) - 1)
    assert 'totaloutput' in ap3b.available_values('zone')
    flux = ap3b.select_by(result_name='flux', zone='zone_1')
    assert flux['results'].shape == (33,)


def test_mosteller(datadir):
    '''Test Apollo3 rates output in Mosteller case: various isotopes.'''
    ap3r = Reader(str(datadir/"Mosteller.hdf"))
    assert ap3r.res
    ap3b = ap3r.to_browser()
    assert ap3b
    assert len(ap3b.keys()) == 5
    isotopes = list(ap3b.available_values('isotope'))
    assert len(isotopes) == 17
    assert 'macro' in isotopes
    rbfiss = ap3b.filter_by(result_name='fission')
    assert len(rbfiss.available_values('isotope')) == 7
    rbconc = ap3b.filter_by(result_name='concentration')
    assert len(rbconc.available_values('isotope')) == len(isotopes) - 1
    assert len(ap3b.available_values('output')) == 6
    assert all(o['ngroups'] == 10 for o in ap3b.globals['info'].values())
    flux = ap3b.select_by(result_name='flux', zone='totaloutput',
                          output='output_2')
    assert flux['results'].shape == (10,)


def test_hexarot_kinetic(datadir):
    '''Test Apollo3 rates output with localvalue containing array.'''
    ap3r = Reader(str(datadir/"Hexarot_Kinetic.hdf"))
    assert ap3r.res
    ap3b = ap3r.to_browser()
    assert ap3b
    assert len(ap3b.keys()) == 5
    assert list(ap3b.available_values('isotope')) == ['macro']
    assert len(ap3b.available_values('output')) == 3
    assert set(ap3b.available_values('result_name')) == {
        'keff', 'production', 'RelativePower', 'flux', 'nufission', 'total'}
    relpow = ap3b.filter_by(result_name='RelativePower')
    assert len(relpow) == 3
    assert all(o['ngroups'] == 4 for o in ap3b.globals['info'].values())
    # why 101 ? what is the binning ?
    assert all(r['results'].shape[0] == 101 for r in relpow.content)
    assert all(r['results'].ndim == 1 for r in relpow.content)


def test_simplest_api(datadir):
    '''Test Apollo3 HDF when file contains only local values.'''
    ap3r = Reader(str(datadir/"Simplest_API.hdf"))
    assert ap3r.res
    ap3b = ap3r.to_browser()
    assert ap3b
    assert set(ap3b.keys()) == {'result_name', 'output', 'index'}
    assert sorted(list(ap3b.available_values('result_name'))) == [
        'User_time_s', 'sample_value1_unit1', 'sample_value2_unit2']
    assert set(ap3b.globals.keys()) == {'info', 'geometry'}
    assert not ap3b.globals['info']
    assert not ap3b.globals['geometry']
    assert all(isinstance(d['results'].value, np.generic)
               for d in ap3b.content)


def test_minicoeur_kinetics(datadir):
    '''Test Apollo3 HDF when file contains only local values with LOCALNAME
    under the localvalue key.
    '''
    ap3r = Reader(str(datadir/"AP3F_MiniCoeur_Kinetics_MINOS.hdf"))
    assert ap3r.res
    ap3b = ap3r.to_browser()
    assert ap3b
    assert set(ap3b.keys()) == {'result_name', 'output', 'index'}
    assert len(ap3b.available_values('result_name')) == 21
    assert set(ap3b.globals.keys()) == {'info', 'geometry'}
    assert not ap3b.globals['info']
    assert not ap3b.globals['geometry']
    keff = ap3b.select_by(result_name='SteadyState_keff')
    assert isinstance(keff['results'].value, np.generic)
    assert not keff['results'].bins
    res2 = ap3b.content[2]
    assert isinstance(res2['results'].value, np.ndarray)
    assert res2['results'].shape[0] == 420


def test_mosteller_to_brow(datadir):
    '''Test Apollo3 rates output in Mosteller case: various isotopes.'''
    ap3b = hdf_to_browser(str(datadir/"Mosteller.hdf"))
    assert ap3b
    assert len(ap3b.keys()) == 5
    isotopes = list(ap3b.available_values('isotope'))
    assert len(isotopes) == 17
    assert 'macro' in isotopes
    rbfiss = ap3b.filter_by(result_name='fission')
    assert len(rbfiss.available_values('isotope')) == 7
    rbconc = ap3b.filter_by(result_name='concentration')
    assert len(rbconc.available_values('isotope')) == len(isotopes) - 1
    assert len(ap3b.available_values('output')) == 6
    assert all(o['ngroups'] == 10 for o in ap3b.globals['info'].values())
    flux = ap3b.select_by(result_name='flux', zone='totaloutput',
                          output='output_2')
    assert flux['results'].shape == (10,)
