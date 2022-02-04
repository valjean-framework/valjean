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

'''Tests for the :mod:`~.scan` module: scan and parse Tripoli-4 outputs
stored in the data folder associated to tests on :mod:`~.eponine` package.
These tests should cover most of functionalities of :mod:`~.scan` and main
ones for :mod:`~.parse`.
'''

import os

from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import numpy as np
import logging
from valjean.eponine.dataset import Dataset
from valjean.eponine.tripoli4.parse import Parser
from valjean.eponine.tripoli4.parse_debug import ParserDebug
import valjean.eponine.tripoli4.data_convertor as dcv


def keffs_checks(keff_res):
    # pylint: disable=too-many-locals
    r'''Quick calculations on k\ :sub:`eff` to check covariance matrix
    calculation and combination. One huge limitation: formulas used are exactly
    the same as in Tripoli-4, so this is not a real check. Their writing in
    matrix formualtion is not straightforward (need permutation matrices,
    Hadamard product instead of the usual matrix product a priori).

    :param dict keff_res: dictionary repesenting the k\ :sub:`eff` results,
                          containing at least 3 `numpy.ndarray`

    Tests performed:

    * Check calculation of combined k\ :sub:`eff`
    * Check calculation of combined σ
    * Test full combination (only working if first combining KSTEP and KCOLL,
      then KTRACK
    '''
    keffestim = keff_res['keff_per_estimator']
    keff = keffestim['keff_matrix'].diagonal()
    sigma = keffestim['sigma_matrix'].diagonal()
    sigma = sigma/100. * keff
    covmat = keffestim['correlation_matrix'] * np.outer(sigma, sigma)
    nums = np.empty([keff.shape[0], keff.shape[0]])
    # print("covariance rank =", np.linalg.matrix_rank(np.matrix(covmat)))
    # print("covariance determinant =", np.linalg.det(covmat))
    # evals, evecs = np.linalg.eig(covmat)
    # print("eigenvalues:", evals)
    # print("eigenvectors:", evecs)
    # print("normes evecs =", list(map(lambda m: np.linalg.norm(m), evecs)))
    # print("1-eval0 =", 1-evals[0])
    # print("keff =", keff)
    # print("keff*evec0 =", np.dot(keff, evecs[0]**2) )
    # print("sig*evec0 *keff0=", np.dot(sigma, evecs[0]**2)*evals[0])
    # print("sig*evec0 =", np.dot(sigma, evecs[0]**2))
    # print("mean keffs =", np.mean(keff))
    for ikeff in range(keff.shape[0]-1):
        for jkeff in range(ikeff+1, keff.shape[0]):
            denom = sigma[ikeff]**2 + sigma[jkeff]**2 - 2*covmat[ikeff, jkeff]
            nums[ikeff, jkeff] = (sigma[jkeff]**2 - covmat[ikeff, jkeff])
            nums[jkeff, ikeff] = (sigma[ikeff]**2 - covmat[ikeff, jkeff])
            cbkeff = (nums[ikeff, jkeff]*keff[ikeff]
                      + nums[jkeff, ikeff]*keff[jkeff]) / denom
            assert np.isclose(cbkeff, keffestim['keff_matrix'][ikeff, jkeff])
            cbsig = (sigma[ikeff]*sigma[jkeff])**2 - covmat[ikeff, jkeff]**2
            cbsig = np.sqrt(cbsig/denom)
            assert np.isclose(cbsig*100/cbkeff,
                              keffestim['sigma_matrix'][ikeff, jkeff])
            # test full combination
            itcomb = keff.shape[0] - ikeff - jkeff
            cov012 = (nums[ikeff, jkeff] * covmat[ikeff, itcomb]
                      + nums[jkeff, ikeff] * covmat[jkeff, itcomb]) / denom
            d012 = sigma[itcomb]**2 + cbsig**2 - 2*cov012
            k012 = ((sigma[itcomb]**2 - cov012) * cbkeff
                    + (cbsig**2 - cov012) * keff[itcomb]) / d012
            v012 = ((cbsig*sigma[itcomb])**2 - cov012**2) / d012
            # print("combination: ", k012, "±", np.sqrt(v012))
            if itcomb == 2:
                assert np.isclose(
                    k012, keff_res['keff_combination']['keff'])
                assert np.isclose(np.sqrt(v012)*100/k012,
                                  keff_res['keff_combination']['sigma'])


def check_gauss_e_spectrum(resp):
    '''Check gauss spectrum: usual spectrum in energy with default integrated
    results.
    '''
    assert resp['score_name'] == 'courant_E'
    assert resp["results"]['score'].shape == (1, 1, 1, 4, 1, 1, 1)
    assert resp["results"]['score_integrated'].shape == (1, 1, 1, 1, 1, 1, 1)
    assert resp["results"]['score_integrated'].bins['e'].size == 2
    assert resp["results"]['score'].bins['e'].size == 5
    assert np.array_equal(resp["results"]['score_integrated'].bins['e'],
                          resp["results"]['score'].bins['e'][::4])
    assert 'discarded_batches' in resp['results']
    assert 'used_batches' in resp['results']
    batch_res = resp['results']['used_batches']
    assert isinstance(batch_res, Dataset)
    assert batch_res.value.dtype == np.int64
    assert batch_res.error.dtype == np.int64
    assert batch_res.error == 0


def check_gauss_et_spectrum(resp):
    '''Check gauss spectrum: spectrum in time and energy. Integrated results
    are given by time bins.
    '''
    assert resp['score_name'] == 'courant_Et'
    bds = resp["results"]['score']
    assert bds.shape == (1, 1, 1, 4, 4, 1, 1)
    bdsi = resp["results"]['score_eintegrated']
    assert bdsi.shape == (1, 1, 1, 1, 4, 1, 1)
    assert bdsi.bins['e'].size == 2
    assert bds.bins['e'].size == 5
    assert bdsi.bins['t'].size == bdsi.shape[4]+1 == 5
    assert np.array_equal(bdsi.bins['e'], bds.bins['e'][::4])
    assert 'discarded_batches' in resp['results']
    assert 'used_batches' in resp['results']


def check_gauss_etmuphi_spectrum(resp):
    '''Check gauss spectrum: spectrum in time, energy, mu and phi. No
    integrated results are available.
    '''
    assert resp['score_name'] == 'courant_Etmuphi'
    bds = resp["results"]['score']
    assert bds.shape == (1, 1, 1, 4, 4, 4, 2)
    assert list(bds.bins.keys()) == ['u', 'v', 'w', 'e', 't', 'mu', 'phi']
    assert ([x for x, y in bds.bins.items() if y.size > 0]
            == list(bds.squeeze().bins.keys()))
    assert list(bds.squeeze().bins.keys()) == ['e', 't', 'mu', 'phi']
    assert 'score_integrated' not in resp["results"]
    assert 'score_eintegrated' not in resp["results"]


def check_gauss_no_res(resp):
    '''Check gauss results: raw response (without datasets).
    Spectrum in time, energy, mu and phi. No integrated results are available.
    '''
    assert resp['score_name'] == 'courant_Etmuphi'
    bds = dcv.convert_data(resp['results'], data_type='spectrum')
    assert bds.shape == (1, 1, 1, 4, 4, 4, 2)
    bdsi = dcv.convert_data(resp['results'], data_type='integrated')
    assert bdsi is None
    bdsei = dcv.convert_data(resp['results'], data_type='spectrum',
                             array_key='eintegrated_array')
    assert bdsei is None
    assert 'discarded_batches' in resp['results']
    ddb = dcv.convert_data(resp['results'], data_type='discarded_batches')
    assert np.isscalar(ddb.value)
    assert ddb.value == 0
    assert 'used_batches' not in resp['results']


def test_gauss_spectrum(datadir):
    '''Test Tripoli-4 listing with spectrum in output depending on time, µ and
    φ angles. Also control number of batchs.
    '''
    t4p = Parser(str(datadir/"gauss_E_time_mu_phi.res.ceav5"))
    assert t4p
    assert t4p.check_times()
    assert t4p.scan_res.normalend
    assert t4p.scan_res.times['initialization_time'] == 0
    assert t4p.scan_res.times['simulation_time'] == {200: 1, 400: 2}
    assert len(t4p.scan_res) == 2
    t4_res = t4p.parse_from_index(-1)
    assert len(t4_res.res['list_responses']) == 7
    assert t4_res.res['list_responses'][-1]['response_index'] == 6
    for ibatch, batch in enumerate(t4p.scan_res):
        assert batch == 200*(ibatch+1)
    for rbatch, batch in enumerate(reversed(t4p.scan_res)):
        assert batch == 200*(len(t4p.scan_res)-rbatch)
    assert t4p.scan_res.batch_number(-1) == 400
    resp0 = t4_res.pres['list_responses'][0]
    assert resp0['response_function'] == "COURANT"
    assert resp0['response_type'] == 'score'
    assert resp0['scoring_mode'] == "SCORE_SURF"
    assert resp0['score_name'] == "courant_E"
    assert all(x in resp0['results']
               for x in ('spectrum', 'integrated'))
    resp1 = t4_res.pres['list_responses'][1]
    assert all(x in resp1['results']['spectrum']
               for x in ('array', 'bins', 'units', 'eintegrated_array'))
    dresp0 = t4_res.res['list_responses'][0]
    assert all(x in dresp0['results']
               for x in ('discarded_batches', 'used_batches', 'score',
                         'score/lethargy', 'units', 'score_integrated'))
    t4rb = t4_res.to_browser()
    assert len(t4rb.keys()) == 16
    assert list(t4rb.available_values('response_function')) == ['COURANT']
    assert list(t4rb.available_values('response_name')) == ['courant']
    assert len(t4rb.available_values('response_index')) == 7
    # use response 0: usual spectrum
    selresp0 = t4rb.select_by(response_index=0, squeeze=True)
    check_gauss_e_spectrum(selresp0)
    # use response 1: spectrum in energy and time
    # speciticity: integrated result in energy per time bin
    selresp1 = t4rb.select_by(response_index=1, squeeze=True)
    check_gauss_et_spectrum(selresp1)
    # use response 5 from score_name: spectrum in e, t, mu and phi
    # no integral available
    selresp = t4rb.select_by(score_name='courant_Etmuphi', squeeze=True)
    check_gauss_etmuphi_spectrum(selresp)
    # checks on datasets not available in response result (integrals)
    resp5 = t4_res.pres['list_responses'][5]
    check_gauss_no_res(resp5)


def test_tungstene(datadir):
    '''Use Tripoli-4 output from tungstene.d to test meshes (also depending on
    energy).
    '''
    t4p = Parser(str(datadir/"tungstene.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 1000
    assert t4p.scan_res.times['simulation_time'][1000] == 423
    assert t4p.scan_res.times['initialization_time'] == 0
    assert len(t4p.scan_res) == 1
    t4_res = t4p.parse_from_index(-1)
    assert t4_res.res['batch_data']['batch_number'] == 1000
    assert t4_res.res['run_data']['initialization_time'] == 0
    assert len(t4_res.res['list_responses']) == 1
    resp0 = t4_res.res['list_responses'][0]
    assert resp0['particle'] == "PHOTON"
    assert resp0['response_type'] == 'score'
    assert resp0['scoring_mode'] == "SCORE_TRACK"
    assert resp0['scoring_zone_type'] == "Mesh"
    t4rb = t4_res.to_browser()
    assert t4rb.globals['simulation_time'] == 423
    resp = t4rb.select_by(response_function='FLUX', squeeze=True)
    bd_mesh = dcv.convert_data(resp['results'], data_type='mesh')
    assert bd_mesh is None
    bd_mesh = resp['results']['score']
    bd_mesh_squeeze = bd_mesh.squeeze()
    assert bd_mesh.shape == (1, 1, 17, 3, 1, 1, 1)
    assert bd_mesh_squeeze.shape == (17, 3)
    assert list(bd_mesh_squeeze.bins.keys()) == ['w', 'e']
    bd_int = resp['results']['score_integrated']
    assert bd_int.shape == (1, 1, 1, 1, 1, 1, 1)
    assert bd_int.bins['e'].size == 2
    assert bd_int.bins['t'].size == 0
    bd_int_squeeze = bd_int.squeeze()
    assert bd_int_squeeze.shape == ()
    assert bd_int_squeeze.ndim == 0
    assert not bd_int_squeeze.bins
    bd_eintm = resp['results']['score_eintegrated']
    assert bd_eintm.shape == (1, 1, 17, 1, 1, 1, 1)
    assert bd_eintm.bins['e'].size == 2


def test_tt_simple_packet20_para(datadir):
    '''Use Tripoli-4 result from ttsSimplePacket100.d run in parallel mode to
    test parallel mode specific features (number of batchs used for edition,
    number of batchs required in case PACKET_LENGTH case, etc.
    '''
    t4p = Parser(str(datadir/"ttsSimplePacket20.d.PARA.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 10
    assert t4p.scan_res.times['simulation_time'][10] == 0
    assert t4p.scan_res.times['initialization_time'] == 4
    assert t4p.scan_res.times['elapsed_time'][10] == 250
    assert len(t4p.scan_res) == 1
    t4_res = t4p.parse_from_index(-1)
    assert t4_res.res['batch_data']['batch_number'] == 10
    assert len(t4_res.res['list_responses']) == 13
    assert t4_res.res['list_responses'][-1]['response_index'] == 3
    assert t4_res.res['list_responses'][-1]['response_function'] == 'KEFFS'
    assert ['score_index' in x
            for x in t4_res.res['list_responses']].count(True) == 6
    resp5 = t4_res.res['list_responses'][4]
    assert resp5['response_function'] == 'REACTION'
    assert resp5['reaction_on_nucleus'] == ("U235",)
    assert resp5['temperature'] == (300,)
    assert resp5['composition'] == ("COMBUSTIBLE",)
    t4rb = t4_res.to_browser()
    assert t4rb
    assert len(t4rb) == 17


def test_debug_entropy(caplog, datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum and
    debug mode.
    '''
    caplog.set_level(logging.DEBUG, logger='valjean')
    t4p = ParserDebug(str(datadir/"entropy.d.res.ceav5"),
                      end_flag="number of batches used",
                      ofile="debug_ent.log")
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 10
    assert t4p.scan_res.times['simulation_time'][10] == 24
    assert t4p.scan_res.times['initialization_time'] == 6
    assert len(t4p.scan_res) == 10
    t4_res = t4p.parse_from_index(-1)
    assert t4_res.res['batch_data']['batch_number'] == 10
    assert len(t4_res.res['list_responses']) == 1
    presp0 = t4_res.pres['list_responses'][0]
    assert presp0['response_type'] == 'score'
    pres0 = presp0['results']
    scorecontent = ['mesh', 'spectrum', 'integrated',
                    'discarded_batches', 'used_batches']
    assert {'array', 'bins', 'units', 'boltzmann_entropy_array',
            'shannon_entropy_array'}.difference(pres0['mesh']) == set()
    bentrop = pres0['mesh']['boltzmann_entropy_array'].squeeze()
    assert np.isclose(bentrop['entropy'], 8.342621e-01)
    assert sorted(list(pres0.keys())) == sorted(scorecontent)
    resp0 = t4_res.res['list_responses'][0]
    assert resp0['response_type'] == 'score'
    res0 = resp0['results']
    rescontent = ['discarded_batches', 'used_batches', 'score', 'units',
                  'boltzmann_entropy', 'shannon_entropy', 'score_integrated']
    bentrop2 = res0['boltzmann_entropy'].squeeze()
    assert np.isclose(bentrop2.value, 8.342621e-01)
    assert sorted(res0.keys()) == sorted(rescontent)
    assert "You are running with an end flag" in caplog.text
    assert "debug_ent.log" in os.listdir()
    with open("debug_ent.log", encoding='utf-8') as ofile:
        lines = ofile.readlines()
        assert len(lines) == 124
        assert "RESULTS ARE GIVEN FOR SOURCE INTENSITY" in lines[0]
        assert "number of batches used" in lines[-1]


def check_last_entropy_result(lastres):
    '''Check last entropy result (all converged).'''
    assert len(lastres.res['list_responses']) == 8
    assert len(lastres.pres['list_responses']) == 8
    lastresps = lastres.res['list_responses']
    for ires in lastresps:
        assert ires['response_function'] in ['REACTION', 'KEFFS']
    assert lastresps[1]['response_type'] == 'keff'
    assert lastres.pres['list_responses'][0]['response_function'] == 'REACTION'
    assert set(lastres.pres['list_responses'][0]['results']) == {
        'discarded_batches', 'integrated', 'mesh', 'spectrum', 'used_batches'}
    # keffs_checks(lastresps[1]['results'])
    t4rb = lastres.to_browser()
    assert t4rb.globals['simulation_time'] == 24
    # response_function = reaction
    resp = t4rb.select_by(response_function='REACTION', squeeze=True)
    assert set(resp['results']) == {
        'discarded_batches', 'used_batches', 'score', 'boltzmann_entropy',
        'shannon_entropy', 'score_integrated', 'units'}
    assert resp['results']['score'].shape == (24, 3, 1, 1, 1, 1, 1)
    assert resp['results']['score'].what == 'reaction'
    assert np.isnan(resp['results']['shannon_entropy'].error)
    assert resp['results']['shannon_entropy'].what == 'entropy'
    assert resp['results']['boltzmann_entropy'].shape == (1, 1, 1, 1, 1, 1, 1)
    assert np.isclose(resp['results']['shannon_entropy'].value.squeeze(),
                      0.9047529)
    assert np.array_equal(resp['results']['score'].bins['e'],
                          resp['results']['score_integrated'].bins['e'])
    assert np.array_equal(resp['results']['score'].bins['e'],
                          resp['results']['boltzmann_entropy'].bins['e'])
    # response_function = keff
    resps = t4rb.select_by(response_type='keff')
    assert len(resps) == 7
    for resp in resps:
        assert set(resp['results']) == {'keff', 'correlation_keff',
                                        'used_batches'}
        assert resp['results']['keff'].shape == ()
        assert resp['results']['keff'].what == 'keff'
        assert not resp['results']['keff'].bins
        assert resp['results']['correlation_keff'].what == 'correlation'
        assert np.isnan(resp['results']['correlation_keff'].error)
        if resp['keff_estimator'] in ('KSTEP', 'KCOLL', 'KTRACK'):
            assert resp['results']['correlation_keff'].value == 1
        if resp['keff_estimator'] == 'full_combination':
            assert np.isnan(resp['results']['correlation_keff'].value)
        if resp['keff_estimator'] == 'KSTEP':
            assert np.isclose(resp['results']['keff'].value, 0.916915)
            assert np.isclose(resp['results']['keff'].error, 7.127724e-3)
    assert 'KSTEP-KCOLL' in t4rb.available_values('keff_estimator')
    assert 'full combination' in t4rb.available_values('keff_estimator')
    resps = t4rb.select_by(response_type='keff_auto')
    assert len(resps) == 4
    for resp in resps:
        assert set(resp['results']) == {'keff', 'used_batches',
                                        'discarded_batches'}
        assert resp['response_type'] == 'keff_auto'
        assert resp['results']['keff'].ndim == 0


def check_first_entropy_result(entropy_rb):
    '''Check first entropy result (not converged).'''
    resp0 = entropy_rb.select_by(response_function='REACTION',
                                 squeeze=True)
    assert np.isnan(resp0['results']['score_integrated'].value)
    resp0 = entropy_rb.select_by(response_type='keff',
                                 squeeze=True)
    assert set(resp0['results']) == {'used_batches', 'keff'}
    assert np.isnan(resp0['results']['keff'].value)


def test_entropy(datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum with
    progressively converging results.
    '''
    t4p = Parser(str(datadir/"entropy.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.check_times()
    assert list(t4p.scan_res.keys())[-1] == 10
    assert t4p.scan_res.times['simulation_time'][10] == 24
    assert t4p.scan_res.times['initialization_time'] == 6
    assert len(t4p.scan_res) == 10
    lastres = t4p.parse_from_number(10)
    check_last_entropy_result(lastres)
    firstres = t4p.parse_from_index(0)
    firstresps = firstres.res['list_responses']
    firstpresps = firstres.pres['list_responses']
    assert firstresps[1]['response_type'] == 'keff'
    assert 'not_converged' in firstpresps[1]['results']
    assert np.isnan(firstresps[1]['results']['keff'].value)
    t4rb_b0 = firstres.to_browser()
    assert t4rb_b0.globals['simulation_time'] == 2
    check_first_entropy_result(t4rb_b0)
    t4rb_b5 = t4p.parse_from_index(5).to_browser()
    assert t4rb_b5
    assert t4rb_b5.globals['simulation_time'] == 14
    assert t4rb_b5.globals['edition_batch_number'] == 6
    t4rb_bn6 = t4p.parse_from_number(6).to_browser()
    assert t4rb_bn6
    assert t4rb_bn6.globals['simulation_time'] == 14
    assert t4rb_b5.globals == t4rb_bn6.globals
    t4_res = t4p.parse_from_number(batch_number=2)
    assert t4_res
    assert len(t4p.scan_res) == 10
    assert t4_res.res['batch_data']['batch_number'] == 2
    t4_rb = t4_res.to_browser()
    assert t4_rb
    assert t4_rb.globals['simulation_time'] == 5


def test_verbose_entropy(datadir, caplog, monkeypatch):
    '''Use Tripoli-4 result from entropy.d to test verbosity (mesh and spectrum
    in same jdd), but long.
    '''
    caplog.set_level(logging.DEBUG, logger='valjean')
    monkeypatch.setattr("valjean.eponine.tripoli4.dump.MAX_DEPTH", 8)
    t4p = Parser(str(datadir/"entropy.d.res.ceav5"))
    t4_res = t4p.parse_from_index(batch_index=-1)
    assert t4_res
    assert t4p.scan_res.normalend
    with open(str(datadir/"entropy_debug.log"), 'r', encoding='utf-8') as ifil:
        for line in ifil:
            assert line in caplog.text, f"Line {line!r} not found in caplog."


def test_ifp(datadir):
    '''Use Tripoli-4 result from  pu_met_fast_001_decompose_list_small.d to
    test IFP parsing.
    '''
    t4p = Parser(
        str(datadir/"pu_met_fast_001_decompose_list_small.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 200
    assert t4p.scan_res.times['simulation_time'][200] == 13
    assert t4p.scan_res.times['initialization_time'] == 1
    t4_res = t4p.parse_from_index(-1)
    assert t4_res.res['batch_data']['batch_number'] == 200
    assert max([v['response_index']
                for v in t4_res.res['list_responses']]) + 1 == 22
    assert len(t4_res.res['list_responses']) == 198
    last_presp = t4_res.pres['list_responses'][-1]
    assert (last_presp['response_function']
            == "IFP ADJOINT WEIGHTED MIGRATION AREA")
    assert last_presp['response_type'] == 'adjoint'
    assert last_presp['results']['used_batches'] == 81
    last_resp = t4_res.res['list_responses'][-1]
    assert (last_resp['response_function']
            == "IFP ADJOINT WEIGHTED MIGRATION AREA")
    assert last_resp['response_type'] == 'adjoint'
    assert last_resp['results']['used_batches'].value == 81
    t4rb = t4_res.to_browser()
    assert len(t4rb.available_values('response_function')) == 22
    resps = t4rb.select_by(
        response_function="IFP ADJOINT WEIGHTED ROSSI ALPHA")
    assert len(resps) == 20  # number of IFP cycles
    assert sorted(list(resps[0].keys())) == ['index', 'length',
                                             'response_function',
                                             'response_index', 'response_type',
                                             'results']
    bd_cycle = resps[0]['results']['score_generic']
    assert bd_cycle.shape == ()
    assert bd_cycle.name == ''
    assert bd_cycle.what == 'ifp adjoint weighted rossi alpha'
    assert np.isclose(bd_cycle.value, -694660.3)
    assert np.isclose(bd_cycle.error, -39568.08)
    assert not bd_cycle.bins
    rb_betai = t4rb.filter_by(
        response_function="BETA_i (DELAYED NEUTRON FRACTION FOR i-th FAMILY): "
                          "NUCLEI CONTRIBUTIONS")
    assert len(rb_betai.content) == 24
    assert (sorted(list(rb_betai.available_values('nucleus')))
            == ['PU239', 'PU240', 'PU241'])
    resp = rb_betai.select_by(family=5, nucleus='PU239', squeeze=True)
    assert resp['response_type'] == 'adjoint'
    assert (sorted(list(resp['results'].keys()))
            == ['score_generic', 'used_batches'])
    assert resp['results']['used_batches'].value == 81
    bd_pu239_f5 = resp['results']['score_generic']
    assert bd_pu239_f5.shape == ()
    assert bd_pu239_f5.what == ("beta_i (delayed neutron fraction "
                                "for i-th family): nuclei contributions")
    assert np.isclose(bd_pu239_f5.value, 7.262777e-4)
    assert np.isclose(bd_pu239_f5.error, 4.567255e-5)
    assert not bd_pu239_f5.bins


def test_ifp_adjoint_edition(datadir):
    '''Use Tripoli-4 result from test_adjoint_small.d to test IFP adjoint
    criticality edition parsing.

    Caution: T4 output has been modified due to a bug in Equivalent keff.
    '''
    t4p = Parser(str(datadir/"test_adjoint_small.d.res"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 20
    assert t4p.scan_res.times['simulation_time'][20] == 77
    assert t4p.scan_res.times['initialization_time'] == 3
    t4_res = t4p.parse_from_index(-1)
    t4rb = t4_res.to_browser()
    assert (set(t4rb.available_values('response_type'))
            == {'keff', 'ifp_adj_crit_edition', 'keff_auto'})
    assert (set(t4rb.keys()) == {
        'ifp_cycle_length', 'ifp_response', 'index', 'keff_estimator',
        'response_function', 'response_index', 'response_type', 'score_name'})
    resp = t4rb.select_by(score_name='FluxAdj_1', squeeze=True)
    bd_adj = resp['results']['score']
    assert bd_adj.shape == (2, 2, 2, 1, 1, 3, 1)
    assert (list(bd_adj.bins.keys())
            == ['X', 'Y', 'Z', 'Phi', 'Theta', 'E', 'T'])
    assert bd_adj.bins['X'].size == bd_adj.shape[0]+1
    resp = t4rb.select_by(score_name='FluxAdj_ang_1', squeeze=True)
    bd_adj = resp['results']['score']
    assert bd_adj.shape == (2, 2, 2, 2, 2, 3, 1)
    assert (list(bd_adj.bins.keys())
            == ['X', 'Y', 'Z', 'Phi', 'Theta', 'E', 'T'])
    resp = t4rb.select_by(score_name='flux_vol', squeeze=True)
    bd_adj = resp['results']['score']
    assert bd_adj.shape == (2, 3)
    assert list(bd_adj.bins.keys()) == ['Vol', 'E']
    assert bd_adj.bins['Vol'].size == bd_adj.shape[0]
    assert np.array_equal(bd_adj.bins['Vol'], [10, 11])
    resp = t4rb.select_by(response_type='keff_auto')
    assert resp[-1]['results']['equivalent_keff'].value == 8.135012e-01
    assert np.isnan(resp[-1]['results']['equivalent_keff'].error)
    resp = t4rb.select_by(response_type='keff')
    assert set(resp[0]['results']) == {'used_batches', 'warning'}


def test_sensitivity(datadir):
    '''Use Tripoli-4 result from sensitivity_godiva.d to test sensitivity
    parsing and dataset construction.
    '''
    t4p = Parser(str(datadir/"sensitivity_godiva.d.res"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 120
    assert t4p.scan_res.times['simulation_time'][120] == 159
    assert t4p.scan_res.times['initialization_time'] == 1
    t4_res = t4p.parse_from_index(-1)
    t4rb = t4_res.to_browser()
    rb_sensitiv = t4rb.filter_by(response_type='sensitivity')
    assert len(rb_sensitiv.content) == 8
    assert (sorted(rb_sensitiv.keys())
            == ['index', 'response_function', 'response_index',
                'response_type', 'sensitivity_index', 'sensitivity_nucleus',
                'sensitivity_reaction', 'sensitivity_type'])
    resp = rb_sensitiv.select_by(sensitivity_nucleus='U235',
                                 sensitivity_reaction='TOTAL FISSION_NU',
                                 squeeze=True)
    assert set(resp['results']) == {'score', 'integrated', 'units',
                                    'used_batches'}
    assert resp['response_type'] == 'sensitivity'
    bds = resp['results']['score']
    assert bds.shape == (1, 33, 1)
    assert list(bds.bins.keys()) == ['einc', 'e', 'mu']
    assert bds.what == 'sensitivity'
    bds_int = resp['results']['integrated']
    assert bds_int.shape == (1, 1, 1)
    assert np.isclose(bds_int.value, 0.9824915)
    assert np.isclose(bds_int.error, 3.4555267e-4)
    assert list(bds_int.bins.keys()) == list(bds.bins.keys())
    resp = rb_sensitiv.select_by(
        sensitivity_nucleus='U238',
        sensitivity_reaction='SCATTERING LAW 21 (CONSTRAINED)',
        squeeze=True)
    bds = resp['results']['score']
    assert bds.shape == (2, 3, 4)
    assert list(bds.bins.keys()) == ['einc', 'e', 'mu']
    bds_int = resp['results']['integrated']
    assert bds_int.shape == (1, 1, 1)
    assert list(bds_int.bins.keys()) == list(bds.bins)
    assert bds_int.what == 'sensitivity'


def test_kij(datadir):
    r'''Use tripoli-4 result from cylindreDecR_with_kij_on_mesh.d to test
    k\ :sub:`ij` matrix parsing.
    '''
    t4p = Parser(
        str(datadir/"cylindreDecR_with_kij_on_mesh.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 100
    assert t4p.scan_res.times['simulation_time'][100] == 69
    assert t4p.scan_res.times['initialization_time'] == 1
    t4_res = t4p.parse_from_number(100)
    assert t4_res.res['batch_data']['batch_number'] == 100
    assert len(t4_res.res['list_responses']) == 22
    resp_list = t4_res.res['list_responses']
    assert resp_list[13]['response_function'] == "KIJ_MATRIX"
    assert resp_list[14]['response_function'] == "KIJ_SOURCES"
    assert resp_list[15]['response_function'] == "KEFFS"
    t4rb = t4_res.to_browser()
    kijmat = t4rb.select_by(response_function='KIJ_MATRIX', squeeze=True)
    assert set(kijmat['results']) == {
        'used_batches', 'kij_mkeff', 'kij_domratio', 'kij_reigenval',
        'kij_reigenvec', 'kij_matrix'}
    assert kijmat['results']['kij_matrix'].shape == (10, 10)
    assert kijmat['results']['kij_reigenvec'].what == 'kij_reigenvec'
    assert kijmat['results']['kij_reigenvec'].shape == (10, 10)
    assert kijmat['results']['kij_reigenval'].shape == (10,)
    assert kijmat['results']['kij_reigenval'].value.dtype.name == 'complex128'
    assert kijmat['results']['kij_reigenval'].error.dtype.name == 'float64'
    assert kijmat['results']['kij_domratio'].ndim == 0
    assert kijmat['results']['kij_mkeff'].shape == ()
    kijakeff = t4rb.select_by(response_type='kijkeff', squeeze=True)
    assert set(kijakeff['results']) == {
        'used_batches', 'kij_leigenvec', 'kij_matrix', 'space_bins',
        'kij_mkeff', 'kij_stddev_matrix', 'kij_sensibility_matrix'}
    for key, res in kijakeff['results'].items():
        if 'matrix' in key:
            assert res.shape == (10, 10)
    assert kijakeff['results']['space_bins'].shape == (10, 3)
    assert kijakeff['results']['kij_leigenvec'].shape == (10,)
    assert kijakeff['results']['kij_leigenvec'].what == 'kij_leigenvec'
    # check error in case of changes (no percentage for auto)
    keffa = t4rb.select_by(response_type='keff_auto', keff_estimator='KSTEP',
                           squeeze=True)
    assert np.isclose(keffa['results']['keff'].error, 1.345008e-03)
    keff = t4rb.select_by(response_type='keff', keff_estimator='KSTEP',
                          squeeze=True)
    assert np.isclose(keff['results']['keff'].error, 1.451522e-03)


def test_green_bands(datadir):
    '''Use Tripoli-4 result from greenband_exploit_T410_contrib.d to test Green
    bands parsing and exploitation jobs.
    '''
    t4p = Parser(
        str(datadir/"greenband_exploit_T410_contrib.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 500
    assert t4p.scan_res.times['exploitation_time'][500] == 2
    assert t4p.scan_res.times['initialization_time'] == 2
    t4_res = t4p.parse_from_number(500)
    assert t4_res.res['batch_data']['batch_number'] == 500
    assert set(t4_res.pres['list_responses'][0]['results']) == {
        'green_bands', 'discarded_batches'}
    t4rb = t4_res.to_browser()
    resp = t4rb.select_by(response_function='FLUX', squeeze=True)
    assert set(resp['results']) == {'score', 'score/lethargy', 'units',
                                    'discarded_batches'}
    bd_gb = resp['results']['score']
    assert bd_gb.shape == (2, 2, 1, 2, 4, 3)
    assert list(bd_gb.bins.keys()) == ['se', 'ns', 'u', 'v', 'w', 'e']
    assert bd_gb.what == 'flux'
    assert resp['results']['score/lethargy'].shape == (2, 2, 1, 2, 4, 3)
    assert np.all(np.isnan(resp['results']['score/lethargy'].error))
    assert resp['results']['score/lethargy'].bins == bd_gb.bins


def test_tt_simple_packet20_mono(datadir):
    '''Use Tripoli-4 result from ttsSimplePacket20.d run in mono-processor
    mode to test PACKET_LENGTH feature in MONO case.
    '''
    t4p = Parser(str(datadir/"ttsSimplePacket20.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.check_times()
    assert list(t4p.scan_res.keys())[-1] == 200
    assert t4p.scan_res.times['simulation_time'][200] == 217
    assert t4p.scan_res.times['initialization_time'] == 3
    assert len(t4p.scan_res) == 2
    t4_res = t4p.parse_from_index()
    assert len(t4_res.res['list_responses']) == 13
    assert t4_res.res['list_responses'][-1]['response_index'] == 3
    assert t4_res.res['list_responses'][-1]['response_function'] == 'KEFFS'
    assert ['score_index' in x
            for x in t4_res.res['list_responses']].count(True) == 6


def test_pertu(datadir):
    '''Use Tripoli-4 result from pertu_covariances.d to test perturbations and
    uncertainty spectrum.
    '''
    t4p = Parser(str(datadir/"pertu_covariances.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 100
    assert t4p.scan_res.times['simulation_time'][100] == 27
    assert t4p.scan_res.times['initialization_time'] == 0
    assert len(t4p.scan_res) == 1
    t4_res = t4p.parse_from_index(batch_index=-1)
    assert (sorted(list(t4_res.res.keys()))
            == ['batch_data', 'list_responses', 'perturbation', 'run_data'])
    assert len(t4_res.res['list_responses']) == 3
    assert t4_res.res['list_responses'][-1]['response_index'] == 0
    assert len(t4_res.res['perturbation']) == 3
    t4rb = t4_res.to_browser()
    slkeys = sorted(list(t4rb.index.keys()))
    assert slkeys == [
        'energy_split_name', 'index', 'particle', 'perturbation_composition',
        'perturbation_index', 'perturbation_method', 'perturbation_rank',
        'perturbation_type', 'response_function', 'response_index',
        'response_type', 'score_index', 'scoring_mode', 'scoring_zone_id',
        'scoring_zone_type', 'scoring_zone_volsurf']
    pertu_vol2 = t4rb.select_by(scoring_zone_id=2,
                                include=('perturbation_rank',), squeeze=True)
    assert pertu_vol2['response_index'] == 0
    assert pertu_vol2['score_index'] == 0
    assert pertu_vol2['response_type'] == 'score'
    assert pertu_vol2['perturbation_rank'] == 0
    assert set(pertu_vol2['results']) == {
        'discarded_batches', 'used_batches', 'score', 'score/lethargy',
        'units', 'score_integrated', 'score_vov', 'sigma2(means)',
        'mean(sigma_n2)', 'sigma(sigma_n2)', 'fisher test',
        'sigma2(means)_integrated', 'mean(sigma_n2)_integrated',
        'sigma(sigma_n2)_integrated', 'fisher test_integrated'}
    pres = pertu_vol2['results']
    assert pres['fisher test'].bins['e'].size <= pres['score'].bins['e'].size
    assert pres['sigma(sigma_n2)'].shape == (1, 1, 1, 10, 1, 1, 1)
    assert np.isnan(pres['mean(sigma_n2)_integrated'].error)
    assert pres['mean(sigma_n2)_integrated'].shape == (1, 1, 1, 1, 1, 1, 1)
    assert pres['mean(sigma_n2)_integrated'].bins['e'].size == 2


def test_vov(datadir):
    '''Use Tripoli-4 result from vov.d to test vov spectra.'''
    t4p = Parser(str(datadir/"vov.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.check_times()
    assert list(t4p.scan_res.keys())[-1] == 400
    assert t4p.scan_res.times['simulation_time'][400] == 33
    assert t4p.scan_res.times['initialization_time'] == 6
    assert len(t4p.scan_res) == 2
    t4_res = t4p.parse_from_index(batch_index=-1)
    list_resp = t4_res.res['list_responses']
    assert len(list_resp) == 8
    assert list_resp[-1]['response_index'] == 1
    assert list_resp[-1]['score_index'] == 2
    assert list_resp[0]['scoring_zone_type'] == 'Point'


def test_phemep_balance(datadir):
    '''Use Tripoli-4 result from ELECTRON_PHOTON_BALANCE.d to test
    photon-electron-positron balance.
    '''
    t4p = Parser(str(datadir/"ELECTRON_PHOTON_BALANCE.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.scan_res.phemep_balance
    assert len(t4p.scan_res.phemep_balance) == 10
    t4res = t4p.parse_from_index(batch_index=-1).to_browser()
    assert len(t4res) == 4
    assert set(t4res.available_values('particle')) == {
        'PHOTON', 'ELECTRON', 'POSITRON', 'CUMUL on all particles'}


def test_homogenize_material(datadir):
    '''Use Tripoli-4 result from angle.d to test the dump of homogenize
    materials.
    '''
    t4p = Parser(str(datadir/"angle.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.scan_res.homog_mat
    assert len(t4p.scan_res.homog_mat) == 2
    t4res = t4p.parse_from_index(batch_index=-1).to_browser()
    assert len(t4res) == 17


def test_box_dyn(datadir):
    '''Use Tripoli-4 result from box_dyn.t4 to test meshes with energy and time
    splitting and precursors results.'''
    t4p = Parser(str(datadir/"box_dyn.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    t4b = t4p.parse_from_index().to_browser()
    assert t4b
    # mesh with energy and time bins
    etmesh = t4b.select_by(score_name='neutron_flux_mesh_score', squeeze=True)
    assert etmesh['energy_split_name'] == 'grid_rough'
    dsmesh = etmesh['results']['score'].squeeze()
    assert dsmesh.shape == (3, 3, 3, 2, 10)
    assert list(dsmesh.bins.keys()) == ['u', 'v', 'w', 'e', 't']
    # precursor weight
    precweight = t4b.select_by(response_function='PRECURSOR WEIGHT')
    assert len(precweight) == 11
    pweight_t3 = t4b.select_by(response_function='PRECURSOR WEIGHT',
                               time_step=3, squeeze=True)
    assert pweight_t3['response_type'] == 'kinetic_generic'
    # neutron weight
    # time_step = 0 corresponds to criticality source (for both weights)
    nweight_t0 = t4b.select_by(response_function='NEUTRON WEIGHT',
                               time_step=0, squeeze=True)
    assert set(nweight_t0['results']) == {'used_batches', 'score_generic',
                                          'units'}
    dsnwt0 = nweight_t0['results']['score_generic']
    assert dsnwt0.shape == ()
    dynom = t4b.select_by(response_function='DYNAMIC NORMALIZATION',
                          squeeze=True)
    assert dynom['response_type'] == 'generic'


