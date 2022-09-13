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

'''Tests for the :mod:`~.depletion` module: read Tripoli-4 ROOT outputs and
store as :class:`~.valjean.eponine.dataset.Dataset`.
'''

from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import pytest
import numpy as np
root = pytest.importorskip('ROOT')
# pylint: disable=wrong-import-position
from valjean.eponine.tripoli4.depletion import DepletionReader  # noqa: E402


@pytest.mark.timeout(3600)
def test_t4_depletion(datadir, tmp_path_factory, tmp_path, capfd):
    '''Test of depletion module, of most of methods available.'''
    # pylint: disable=too-many-statements
    root_dir = tmp_path_factory.mktemp('t4depletion')
    depr = DepletionReader.from_evolution_steps(
        str(datadir/"evolution.root"), root_build=str(root_dir))
    assert depr
    assert depr.nb_simu() == 1
    assert depr.nb_compositions() == 6
    assert depr.nb_steps() == 71
    assert depr.burnup(42).value == 31000
    assert depr.burnup_array().ndim == 1
    assert np.isnan(depr.time(42).error)
    assert depr.time_array().size == 71
    cnames = depr.composition_names()
    assert len(cnames) == 6
    assert 'FUEL_R3' in cnames
    liso = depr.isotope_names(42, 'FUEL_R3')
    assert len(liso) == 161
    assert 'U238' in liso
    rnames = depr.reaction_names(42, 'FUEL_R3', 'U235')
    assert rnames == ['DISPAR', 'REAMT102', 'REAMT16', 'REAMT18']
    dirn = depr.isotope_reaction_names(42, 'FUEL_R3')
    assert dirn['U235'] == ['DISPAR', 'REAMT102', 'REAMT16', 'REAMT18']
    # quantities without arguments
    # pylint: disable=no-member
    assert np.greater(depr.kcoll(42).value, depr.kcoll(71).value)
    assert list(depr.kcoll_time().bins.keys()) == ['time']
    assert np.greater(depr.kstep(42).value, depr.kstep(71).value)
    assert depr.kstep_burnup().size == 71
    assert np.greater(depr.ktrack(42).value, depr.ktrack(71).value)
    assert depr.ktrack_time().size == 71
    assert np.array_equal(depr.beff_prompt(42).value, -1)
    assert np.array_equal(np.unique(depr.beff_prompt_burnup().value), [-1])
    assert np.array_equal(depr.beff_nauchi(42).value, -1)
    assert np.array_equal(np.unique(depr.beff_nauchi_time().value), [-1])
    assert np.isnan(depr.renorm(42).error)
    assert depr.renorm_time().what == 'renorm'
    assert np.array_equal(depr.total_power(42).value,
                          depr.total_power(71).value)
    assert depr.total_power_burnup().value.shape == (71,)
    # quantities with one argument: composition name
    assert np.less(depr.power(step=42, componame='FUEL_R3').value,
                   depr.power(step=42, componame='FUEL_R1').value)
    assert (np.unique(depr.power_burnup(componame='FUEL_R3').value).size
            == 71)
    assert np.less(depr.local_burnup(step=42, componame='FUEL_R3').value,
                   depr.local_burnup(step=71, componame='FUEL_R3').value)
    assert np.all(
        np.diff(depr.local_burnup_time(componame='FUEL_R1').value) > 0)
    assert np.less(depr.fast_flux(step=42, componame='FUEL_R3').value,
                   depr.fast_flux(step=42, componame='FUEL_R1').value)
    assert depr.fast_flux_burnup(componame='FUEL_R1').name == ''
    assert np.less(depr.therm_flux(step=42, componame='FUEL_R3').value,
                   depr.therm_flux(step=71, componame='FUEL_R3').value)
    assert (list(depr.therm_flux_burnup(componame='FUEL_R1').bins.keys())
            == ['burnup'])
    # quantities with 2 arguments: composition and isotope names
    assert np.isclose(depr.mass(step=42, componame='FUEL_R3',
                                isotope='U238').value, 8.941861)
    assert depr.mass_time(componame='FUEL_R3', isotope='U238').size == 71
    assert len(depr.concentration(step=42, componame='FUEL_R3',
                                  isotope='U238').bins) == 0
    assert depr.concentration_burnup(
        componame='FUEL_R3', isotope='U238').size == 71
    assert depr.activity(step=42, componame='FUEL_R3',
                         isotope='U238').name == ''
    assert depr.activity_time(componame='FUEL_R3', isotope='U238').ndim == 1
    # quantities with 3 arguments: composition, isotope and reaction names
    assert np.less(depr.reaction_rate(
        step=42, componame='FUEL_R3', isotope='U238',
        reaction='REAMT102').value, 1e-8)
    assert depr.reaction_rate_burnup(
        componame='FUEL_R3', isotope='U238', reaction='REAMT102').ndim == 1
    assert np.less(depr.thermal_reaction_rate(
        step=42, componame='FUEL_R3', isotope='U238',
        reaction='REAMT102').value, 1e-8)
    assert depr.thermal_reaction_rate_time(
        componame='FUEL_R3', isotope='U238', reaction='REAMT102').ndim == 1
    assert np.less(depr.fast_reaction_rate(
        step=42, componame='FUEL_R3', isotope='U238',
        reaction='REAMT102').value, 1e-8)
    assert depr.fast_reaction_rate_burnup(
        componame='FUEL_R3', isotope='U238', reaction='REAMT18').ndim == 1
    depr.dump_global_results(42)
    captured = capfd.readouterr()
    assert 'Dumping mean results for composition :  FUEL_R3' in captured.out
    depr.save_mbr(str(tmp_path / 'test_mbr.root'))
    ndepr = DepletionReader.from_mbr(str(tmp_path / 'test_mbr.root'),
                                     mbr_name='MeanBurnupResults',
                                     root_build=str(root_dir))
    assert ndepr
    assert ndepr.nb_simu() == depr.nb_simu()
