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

'''Tests for the :mod:`~.hdf5_picker` module: read Apollo3 HDF outputs and
build Datasets from them.
'''

from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import numpy as np
from valjean.eponine.apollo3.hdf5_picker import Picker
from valjean.cosette.rlist import RList


def test_rnr_a3c_api(datadir):
    '''Test Apollo3 rates output, with localvalues.'''
    ap3p = Picker(str(datadir/"RnR_A3C_API.hdf"))
    assert ap3p.hfile
    assert ap3p.outputs() == ['output_0']
    zones = ap3p.zones(output='output_0')
    assert 'zone_1' in zones
    assert 'totaloutput' in zones
    assert len(zones) == 21
    nb_grps = ap3p.nb_groups(output='output_0')
    assert nb_grps == 33
    zvols = ap3p.geometry(output='output_0')
    assert len(zvols) == len(zones) - 1
    assert 'macro' in ap3p.isotopes(output='output_0', zone='zone_1')
    assert all(ap3p.results(output='output_0', zone=z) == ['FLUX']
               for z in zones if z != 'totaloutput')
    assert (ap3p.results(output='output_0', zone='totaloutput')
            == ['KEFF', 'LOCALNAME', 'LOCALVALUE', 'PRODUCTION'])
    keff = ap3p.pick_standard_value(output='output_0', zone='totaloutput',
                                    result_name='KEFF')
    assert keff
    assert keff.shape == ()
    flux_5 = ap3p.pick_standard_value(output='output_0', zone='zone_6',
                                      result_name='FLUX')
    assert isinstance(flux_5.value, np.ndarray)
    assert flux_5.shape == (nb_grps,)
    assert (ap3p.local_names(output='output_0', zone='totaloutput')
            == RList(['Eigen value Minos', 'Eigen value Minaret']))
    ev_minos = ap3p.pick_user_value(output='output_0', zone='totaloutput',
                                    result_name='Eigen value Minos')
    assert ev_minos
    assert ev_minos.shape == ()


def test_mosteller(datadir):
    '''Test Apollo3 rates output in Mosteller case: various isotopes.'''
    ap3p = Picker(str(datadir/"Mosteller.hdf"))
    assert ap3p.hfile
    outputs = ap3p.outputs()
    assert len(outputs) == 6
    nb_grps = ap3p.nb_groups(output='output_0')
    assert all(ap3p.nb_groups(output=o) == nb_grps for o in outputs)
    assert ap3p.zones(output='output_0') == ['1', '2', '3', 'totaloutput']
    assert (ap3p.results(output='output_0', zone='totaloutput')
            == ['ABSORPTION', 'FLUX', 'KEFF', 'PRODUCTION'])
    assert (ap3p.isotopes(output='output_0', zone='3')
            == RList(['H2O', 'B10', 'B11', 'macro']))
    assert ap3p.results(output='output_2', zone='2', isotope='Zr96') == [
        'Absorption', 'concentration']
    assert (ap3p.results(output='output_1', zone='2', isotope='macro')
            == ['Absorption', 'NuFission', 'info'])
    assert ap3p.results(output='output_1', zone='1') == ['FLUX']
    flux = ap3p.pick_standard_value(output='output_0', zone='3',
                                    result_name='FLUX')
    assert flux
    assert isinstance(flux.value, np.ndarray)
    assert flux.shape == (nb_grps,)
    absorp = ap3p.pick_standard_value(output='output_0', zone='1',
                                      result_name='Absorption', isotope='U238')
    assert absorp
    assert absorp.shape == (nb_grps)
    conc = ap3p.pick_standard_value(output='output_0', zone='3',
                                    result_name='concentration', isotope='B10')
    assert conc
    assert isinstance(conc.value, np.generic)


def test_simplest_api(datadir):
    '''Test Apollo3 HDF when file contains only local values.'''
    ap3p = Picker(str(datadir/"Simplest_API.hdf"))
    assert ap3p.hfile
    assert ap3p.outputs() == ['output']
    assert ap3p.zones(output='output') == ['LOCALNAME', 'LOCALVALUE']
    assert (ap3p.local_names(output='output', zone=None)
            == RList(['sample_value2_unit2', 'User_time_s',
                      'sample_value1_unit1']))
    svu2 = ap3p.pick_user_value(output='output', zone=None,
                                result_name='sample_value2_unit2')
    assert svu2
    assert isinstance(svu2.value, np.ndarray)


def test_minicoeur_kinetics(datadir):
    '''Test Apollo3 HDF when file contains only local values with LOCALNAME
    under the localvalue key.
    '''
    ap3p = Picker(str(datadir/"AP3F_MiniCoeur_Kinetics_MINOS.hdf"))
    assert ap3p.hfile
    assert ap3p.outputs() == ['output']
    assert ap3p.zones(output='output') == ['localvalue']
    lnames = ap3p.local_names(output='output', zone='localvalue')
    assert len(lnames) == 21
    mino_rho = ap3p.pick_user_value(output='output', zone='localvalue',
                                    result_name='Mino_RHO')
    assert isinstance(mino_rho.value, np.ndarray)
    assert mino_rho.shape == (420,)
    sskeff = ap3p.pick_user_value(output='output', zone='localvalue',
                                  result_name='SteadyState_keff')
    assert isinstance(sskeff.value, np.ndarray)
    assert sskeff.shape == (1,)
