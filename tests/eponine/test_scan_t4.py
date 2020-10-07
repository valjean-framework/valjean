'''Tests for the :mod:`~.scan` module: scan and parse Tripoli-4 outputs
stored in the data folder associated to tests on :mod:`~.eponine` package.
These tests should cover most of functionalities of :mod:`~.scan` and main
ones for :mod:`~.parse`.
'''

import os

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import numpy as np
import logging
import pytest
from valjean.eponine.tripoli4.parse import T4Parser, T4ParserException
from valjean.eponine.tripoli4.parse_debug import T4ParserDebug
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
    bds = dcv.convert_data(resp['results'], data_type='spectrum')
    assert bds.shape == (1, 1, 1, 4, 1, 1, 1)
    bdsi = dcv.convert_data(resp['results'], data_type='integrated')
    assert bdsi.shape == (1, 1, 1, 1, 1, 1, 1)
    assert bdsi.bins['e'].size == 2
    assert bds.bins['e'].size == 5
    assert np.array_equal(bdsi.bins['e'], bds.bins['e'][::4])
    assert 'discarded_batches' in resp['results']
    assert 'used_batches' in resp['results']


def check_gauss_et_spectrum(resp):
    '''Check gauss spectrum: spectrum in time and energy. Integrated results
    are given by time bins.
    '''
    bds = dcv.convert_data(resp['results'], data_type='spectrum')
    assert bds.shape == (1, 1, 1, 4, 4, 1, 1)
    bdsi = dcv.convert_data(resp['results'], data_type='spectrum',
                            array_type='eintegrated_array')
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
    bds = dcv.convert_data(resp['results'], data_type='spectrum')
    assert bds.shape == (1, 1, 1, 4, 4, 4, 2)
    assert list(bds.bins.keys()) == ['s0', 's1', 's2', 'e', 't', 'mu', 'phi']
    assert ([x for x, y in bds.bins.items() if y.size > 0]
            == list(bds.squeeze().bins.keys()))
    assert list(bds.squeeze().bins.keys()) == ['e', 't', 'mu', 'phi']
    bdsi = dcv.convert_data(resp['results'], data_type='integrated')
    assert bdsi is None
    bdsei = dcv.convert_data(resp['results'], data_type='spectrum',
                             array_type='eintegrated_array')
    assert bdsei is None
    assert 'discarded_batches' in resp['results']
    assert 'used_batches' not in resp['results']


def test_gauss_spectrum(datadir):
    '''Test Tripoli-4 listing with spectrum in output depending on time, µ and
    φ angles. Also control number of batchs.
    '''
    t4p = T4Parser(str(datadir/"gauss_time_mu_phi_E.d.res.ceav5"))
    assert t4p
    assert t4p.check_times()
    assert t4p.scan_res.normalend
    assert t4p.scan_res.times['initialization_time'] == 0
    assert t4p.scan_res.times['simulation_time'] == {200: 1, 400: 2}
    assert len(t4p.scan_res) == 2
    t4_res = t4p.parse_from_index(-1)
    assert len(t4_res.res['list_responses']) == 6
    assert t4_res.res['list_responses'][-1]['response_index'] == 5
    for ibatch, batch in enumerate(t4p.scan_res):
        assert batch == 200*(ibatch+1)
    for rbatch, batch in enumerate(reversed(t4p.scan_res)):
        assert batch == 200*(len(t4p.scan_res)-rbatch)
    assert t4p.scan_res.batch_number(-1) == 400
    resp0 = t4_res.res['list_responses'][0]
    assert resp0['response_function'] == "COURANT"
    assert resp0['response_type'] == 'score'
    assert resp0['scoring_mode'] == "SCORE_SURF"
    assert all(x in resp0['results']
               for x in ('spectrum', 'integrated'))
    t4rb = t4_res.to_browser()
    assert len(t4rb.keys()) == 14
    assert (list(t4rb.available_values('response_function'))
            == ['COURANT'])
    assert len(list(t4rb.available_values('response_index'))) == 6
    # use response 0: usual spectrum
    selresp0 = t4rb.select_by(response_index=0, squeeze=True)
    check_gauss_e_spectrum(selresp0)
    # use response 1: spectrum in energy and time
    # speciticity: integrated result in energy per time bin
    selresp1 = t4rb.select_by(response_index=1, squeeze=True)
    check_gauss_et_spectrum(selresp1)
    # use response 4: spectrum in e, t, mu and phi
    # no integral available
    selresp = t4rb.select_by(response_index=4, squeeze=True)
    check_gauss_etmuphi_spectrum(selresp)


def test_tungstene_file(datadir):
    '''Use Tripoli-4 output from tungstene.d to test meshes (also depending on
    energy).
    '''
    t4p = T4Parser(str(datadir/"tungstene.d.res.ceav5"))
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
    assert 'mesh' in resp0['results']
    t4rb = t4_res.to_browser()
    assert t4rb.globals['simulation_time'] == 423
    resp = t4rb.select_by(response_function='FLUX', squeeze=True)
    bd_mesh = dcv.convert_data(resp['results'], data_type='mesh')
    bd_mesh_squeeze = bd_mesh.squeeze()
    assert bd_mesh.shape == (1, 1, 17, 3, 1, 1, 1)
    assert list(bd_mesh_squeeze.bins.keys()) == ['s2', 'e']
    bd_int = dcv.convert_data(resp['results'], data_type='integrated')
    assert bd_int.shape == (1, 1, 1, 1, 1, 1, 1)
    assert bd_int.bins['e'].size == 2
    bd_int_squeeze = bd_int.squeeze()
    assert bd_int_squeeze.shape == ()
    assert not bd_int_squeeze.bins
    bd_eintm = dcv.convert_data(resp['results'], data_type='mesh',
                                array_type='eintegrated_array')
    assert bd_eintm.shape == (1, 1, 17, 1, 1, 1, 1)
    assert bd_eintm.bins['e'].size == 2


# def test_petit_coeur_para():
#     t4_res = T4Parser.parse_jdd_with_mesh_lim(
#         "/home/el220326/valjean/tests/eponine/data/"
#         "create_petitcoeur.d.PARA.res.ceav5",
#         -1, -1, "simulation time")
#     if t4_res:
#         t4_res.print_t4_stats()
#         print("result of the function =", t4_res.check_t4_times())
#         t4_res.print_t4_times()
#         assert t4_res.scan_res.normalend is True
#         assert t4_res.scan_res.times['simulation time'] == 0
#         assert t4_res.scan_res.times['initialization time'] == 11
#         assert t4_res.scan_res.times['elapsed time'] == 47
#         assert len(t4_res.scan_res) == 1
#         print("len(t4_res.result) =", len(t4_res.result))
#         assert len(t4_res.result) == 1
#         print("keys in results:", list(t4_res.result[-1].keys()))
#         print("nbre respinbses :", len(t4_res.result[-1]['list_responses']))
#         assert len(t4_res.result[-1]['list_responses']) == 2


def test_tt_simple_packet20_para(datadir):
    '''Use Tripoli-4 result from ttsSimplePacket100.d run in parallel mode to
    test parallel mode specific features (number of batchs used for edition,
    number of batchs required in case PACKET_LENGTH case, etc.
    '''
    t4p = T4Parser(str(datadir/"ttsSimplePacket20.d.PARA.res.ceav5"),
                   mesh_lim=-1)
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


def test_debug_entropy(caplog, datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum and
    debug mode.
    '''
    caplog.set_level(logging.DEBUG, logger='valjean')
    t4p = T4ParserDebug(str(datadir/"entropy.d.res.ceav5"),
                        mesh_lim=10,
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
    resp0 = t4_res.res['list_responses'][0]
    assert resp0['response_type'] == 'score'
    res0 = resp0['results']
    scorecontent = ['mesh', 'boltzmann_entropy', 'shannon_entropy',
                    'spectrum', 'integrated', 'discarded_batches',
                    'used_batches']
    assert "{0:6e}".format(res0['boltzmann_entropy']) == "8.342621e-01"
    assert sorted(list(res0.keys())) == sorted(scorecontent)
    assert "You are running with an end flag" in caplog.text
    assert "debug_ent.log" in os.listdir()
    with open("debug_ent.log") as ofile:
        lines = ofile.readlines()
        assert len(lines) == 62
        assert "RESULTS ARE GIVEN FOR SOURCE INTENSITY" in lines[0]
        assert "number of batches used" in lines[-1]


def check_last_entropy_result(entropy_rb):
    '''Check last entropy result (all converged).'''
    # response_function = reaction
    resp = entropy_rb.select_by(response_function='REACTION',
                                squeeze=True)
    assert (sorted(list(resp['results'].keys()))
            == ['boltzmann_entropy', 'discarded_batches',
                'integrated', 'mesh', 'shannon_entropy',
                'spectrum', 'used_batches'])
    bd_mesh = dcv.convert_data(resp['results'], data_type='mesh')
    assert bd_mesh.shape == (24, 3, 1, 1, 1, 1, 1)
    bd_entropy = dcv.convert_data(resp['results'],
                                  data_type='shannon_entropy')
    assert np.isnan(bd_entropy.error)
    bd_entropy = dcv.convert_data(resp['results'],
                                  data_type='boltzmann_entropy')
    assert np.isnan(bd_entropy.error)
    bd_spectrum = dcv.convert_data(resp['results'], data_type='spectrum')
    assert bd_spectrum.shape == (1, 1, 1, 1, 1, 1, 1)
    assert bd_spectrum.bins['e'].size == 2
    assert np.array_equal(bd_spectrum.bins['e'], bd_mesh.bins['e'])
    bd_int = dcv.convert_data(resp['results'], data_type='integrated')
    assert np.array_equal(bd_spectrum.bins['e'], bd_int.bins['e'])
    # response_function = keff
    resps = entropy_rb.select_by(response_type='keff')
    assert len(resps) == 7
    for resp in resps:
        bd_keff = dcv.convert_data(resp['results'], data_type='keff')
        assert bd_keff.shape == ()
        assert not bd_keff.bins
        bd_corr = dcv.convert_data(resp['results'], data_type='keff',
                                   correlation=True)
        assert bd_corr
        assert np.isnan(bd_corr.error)
        if resp['keff_estimator'] in ('KSTEP', 'KCOLL', 'KTRACK'):
            assert bd_corr.value == 1
        if resp['keff_estimator'] == 'full_combination':
            assert np.isnan(bd_corr.value)
    assert 'KSTEP-KCOLL' in entropy_rb.available_values('keff_estimator')
    assert 'full combination' in entropy_rb.available_values('keff_estimator')
    resps = entropy_rb.select_by(response_type='keff_auto')
    assert len(resps) == 4
    for resp in resps:
        bd_keff = dcv.convert_data(resp['results'], data_type='keff_auto')
        assert bd_keff.shape == ()


def check_first_entropy_result(entropy_rb):
    '''Check first entropy result (not converged).'''
    resp0 = entropy_rb.select_by(response_function='REACTION',
                                 squeeze=True)
    bd_int0 = dcv.convert_data(resp0['results'], data_type='integrated')
    assert bd_int0 is not None
    assert np.isnan(bd_int0.value)
    resp0 = entropy_rb.select_by(response_type='keff',
                                 squeeze=True)
    bd_keff = dcv.convert_data(resp0['results'],
                               data_type='keff_per_estimator',
                               estimator='KSTEP')
    assert bd_keff is not None
    assert np.isnan(bd_keff.value)
    bd_keff = dcv.convert_data(resp0['results'],
                               data_type='keff_combination')
    assert bd_keff is not None
    assert np.isnan(bd_keff.value)


def test_entropy(datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum with
    progressively converging results.
    '''
    t4p = T4Parser(str(datadir/"entropy.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.check_times()
    assert list(t4p.scan_res.keys())[-1] == 10
    assert t4p.scan_res.times['simulation_time'][10] == 24
    assert t4p.scan_res.times['initialization_time'] == 6
    assert len(t4p.scan_res) == 10
    lastres = t4p.parse_from_number(10)
    assert len(lastres.res['list_responses']) == 8
    lastresps = lastres.res['list_responses']
    for ires in lastresps:
        assert ires['response_function'] in ['REACTION', 'KEFFS']
    assert lastresps[1]['response_type'] == 'keff'
    # keffs_checks(lastresps[1]['results'])
    t4rb = lastres.to_browser()
    assert t4rb.globals['simulation_time'] == 24
    check_last_entropy_result(t4rb)
    firstres = t4p.parse_from_index(0)
    firstresps = firstres.res['list_responses']
    assert firstresps[1]['response_type'] == 'keff'
    assert 'not_converged' in firstresps[1]['results']
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
    t4p = T4Parser(str(datadir/"entropy.d.res.ceav5"), mesh_lim=10)
    t4_res = t4p.parse_from_index(batch_index=-1)
    assert t4_res
    assert t4p.scan_res.normalend
    with open(str(datadir/"entropy_debug.log"), 'r') as ifile:
        for line in ifile:
            assert line in caplog.text, "Line %r not found in caplog." % line


def test_ifp(datadir):
    '''Use Tripoli-4 result from  pu_met_fast_001_decompose_list_small.d to
    test IFP parsing.
    '''
    t4p = T4Parser(
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
    last_resp = t4_res.res['list_responses'][-1]
    assert (last_resp['response_function']
            == "IFP ADJOINT WEIGHTED MIGRATION AREA")
    assert last_resp['response_type'] == 'adjoint'
    assert last_resp['results']['used_batches'] == 81
    t4rb = t4_res.to_browser()
    assert (len(list(t4rb.available_values('response_function')))
            == 22)
    resps = t4rb.select_by(
        response_function="IFP ADJOINT WEIGHTED ROSSI ALPHA")
    assert len(resps) == 20  # number of IFP cycles
    assert sorted(list(resps[0].keys())) == ['index', 'length',
                                             'response_function',
                                             'response_index', 'response_type',
                                             'results']
    bd_cycle = dcv.convert_data(resps[0]['results'],
                                data_type='generic')
    assert bd_cycle.shape == ()
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
            == ['generic', 'used_batches'])
    assert resp['results']['used_batches'] == 81
    bd_pu239_f5 = dcv.convert_data(resp['results'], data_type='generic')
    assert bd_pu239_f5.shape == ()
    assert not bd_pu239_f5.bins


def test_ifp_adjoint_edition(datadir):
    '''Use Tripoli-4 result from test_adjoint_small.d to test IFP adjoint
    criticality edition parsing.

    Caution: T4 output has been modified due to a bug in Equivalent keff.
    '''
    t4p = T4Parser(str(datadir/"test_adjoint_small.d.res"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 20
    assert t4p.scan_res.times['simulation_time'][20] == 77
    assert t4p.scan_res.times['initialization_time'] == 3
    t4_res = t4p.parse_from_index(-1)
    t4rb = t4_res.to_browser()
    assert (set(t4rb.available_values('response_type'))
            == set(('keff', 'ifp_adj_crit_edition', 'keff_auto')))
    assert (sorted(t4rb.keys())
            == ['ifp_cycle_length', 'ifp_response', 'index', 'keff_estimator',
                'response_function', 'response_index', 'response_type',
                'score_name'])
    resp = t4rb.select_by(score_name='FluxAdj_1', squeeze=True)
    bd_adj = dcv.convert_data(resp['results'], data_type='adj_crit_ed')
    assert bd_adj.shape == (2, 2, 2, 1, 1, 3, 1)
    assert (list(bd_adj.bins.keys())
            == ['X', 'Y', 'Z', 'Phi', 'Theta', 'E', 'T'])
    assert bd_adj.bins['X'].size == bd_adj.shape[0]+1
    resp = t4rb.select_by(score_name='FluxAdj_ang_1', squeeze=True)
    bd_adj = dcv.convert_data(resp['results'], data_type='adj_crit_ed')
    assert bd_adj.shape == (2, 2, 2, 2, 2, 3, 1)
    assert (list(bd_adj.bins.keys())
            == ['X', 'Y', 'Z', 'Phi', 'Theta', 'E', 'T'])
    resp = t4rb.select_by(score_name='flux_vol', squeeze=True)
    bd_adj = dcv.convert_data(resp['results'], data_type='adj_crit_ed')
    assert bd_adj.shape == (2, 3)
    assert list(bd_adj.bins.keys()) == ['Vol', 'E']
    assert bd_adj.bins['Vol'].size == bd_adj.shape[0]
    assert np.array_equal(bd_adj.bins['Vol'], [10, 11])


def test_sensitivity(datadir):
    '''Use Tripoli-4 result from sensitivity_godiva.d to test sensitivity
    parsing and dataset construction.
    '''
    t4p = T4Parser(str(datadir/"sensitivity_godiva.d.res"))
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
    bds = dcv.convert_data(resp['results'],
                           data_type='sensitivity_spectrum')
    assert bds.shape == (1, 33, 1)
    assert list(bds.bins.keys()) == ['einc', 'e', 'mu']
    bds_int = dcv.convert_data(resp['results'],
                               data_type='integrated')
    assert bds_int.shape == (1, 1, 1)
    assert list(bds_int.bins.keys()) == list(bds.bins.keys())
    resp = rb_sensitiv.select_by(
        sensitivity_nucleus='U238',
        sensitivity_reaction='SCATTERING LAW 21 (CONSTRAINED)',
        squeeze=True)
    bds = dcv.convert_data(resp['results'],
                           data_type='sensitivity_spectrum')
    assert bds.shape == (2, 3, 4)
    assert list(bds.bins.keys()) == ['einc', 'e', 'mu']
    bds_int = dcv.convert_data(resp['results'],
                               data_type='integrated')
    assert bds_int.shape == (1, 1, 1)
    assert list(bds_int.bins.keys()) == list(bds.bins.keys())


def test_kij(datadir):
    r'''Use tripoli-4 result from cylindreDecR_with_kij_on_mesh.d to test
    k\ :sub:`ij` matrix parsing.
    '''
    t4p = T4Parser(
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
    for res in kijmat['results']:
        assert dcv.convert_data(kijmat['results'], data_type=res)
    kijakeff = t4rb.select_by(response_type='kijkeff', squeeze=True)
    for res in kijakeff['results']:
        assert dcv.convert_data(kijakeff['results'], data_type=res)


def test_green_bands(datadir):
    '''Use Tripoli-4 result from greenband_exploit_T410_contrib.d to test Green
    bands parsing and exploitation jobs.
    '''
    t4p = T4Parser(
        str(datadir/"greenband_exploit_T410_contrib.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert list(t4p.scan_res.keys())[-1] == 500
    assert t4p.scan_res.times['exploitation_time'][500] == 2
    assert t4p.scan_res.times['initialization_time'] == 2
    t4_res = t4p.parse_from_number(500)
    assert t4_res.res['batch_data']['batch_number'] == 500
    t4rb = t4_res.to_browser()
    resp = t4rb.select_by(response_function='FLUX', squeeze=True)
    bd_gb = dcv.convert_data(resp['results'], data_type='green_bands')
    assert bd_gb.shape == (2, 2, 1, 2, 4, 3)
    assert list(bd_gb.bins.keys()) == ['se', 'ns', 'u', 'v', 'w', 'e']


def test_tt_simple_packet20_mono(datadir):
    '''Use Tripoli-4 result from ttsSimplePacket20.d run in mono-processor
    mode to test PACKET_LENGTH feature in MONO case.
    '''
    t4p = T4Parser(str(datadir/"ttsSimplePacket20.d.res.ceav5"))
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
    t4p = T4Parser(str(datadir/"pertu_covariances.d.res.ceav5"))
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


def test_vov(datadir):
    '''Use Tripoli-4 result from vov.d to test vov spectra.'''
    t4p = T4Parser(str(datadir/"vov.d.res.ceav5"))
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
    t4p = T4Parser(str(datadir/"ELECTRON_PHOTON_BALANCE.d.res.ceav5"))
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
    t4p = T4Parser(str(datadir/"angle.d.res.ceav5"))
    assert t4p
    assert t4p.scan_res.normalend
    assert t4p.scan_res.homog_mat
    assert len(t4p.scan_res.homog_mat) == 2
    t4res = t4p.parse_from_index(batch_index=-1).to_browser()
    assert len(t4res) == 17


def test_empty_file(caplog):
    '''Test Tripoli-4 parsing on an empty file: this should fail.'''
    with open('empty_file.txt', 'w') as ofile:
        ofile.write("")
    with pytest.raises(T4ParserException):
        T4Parser('empty_file.txt')
    assert ("No result found in Tripoli-4 listing empty_file.txt"
            in caplog.text)


def test_no_usual_output(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_segFault.d.res as example of
    "failed" jobs: response required in a neutron flux from a neutron source
    while the particles tracked are photons, so Tripoli-4 fails at execution.
    '''
    tfile = str(datadir/"failure_test_segFault.d.res")
    with pytest.raises(T4ParserException):
        T4Parser(tfile)
    assert ("No result found in Tripoli-4 listing {}".format(tfile)
            in caplog.text)
    assert "FATAL ERROR" in caplog.text
    assert "error message" in caplog.text


def test_no_a_t4_opt_no_spectrum(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_spec_res.d.res as example of
    parsing failure due to lack of option '-a'. In that case all the intervals
    in the spectrum are at 0, so without option '-a', none of them appears in
    the output. Parsing succeeds to parse the spectrum columns (and units here)
    but fails after as it cannot find any row from the spectrum.
    '''
    t4p = T4Parser(str(datadir/"failure_test_no_spec_res.d.res"))
    with pytest.raises(T4ParserException):
        t4p.parse_from_index(batch_index=-1)
    assert ("Parsing error in spectrum (_spectrumvals), "
            "please check you run Tripoli-4 with '-a' option"
            in caplog.text)


def test_no_a_t4_opt_bad_bins(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_a_opt.d.res as example of
    parsing failure due to lack of option '-a'. In this case the spectrum is
    partially filled but filled bins are not adjacent, they are inconsistent
    (no possibility for example to guess bin width, if spectrum was also in
    time for example an new energy bin could appear in the next time step). A
    specific error is sent.
    '''
    t4p = T4Parser(str(datadir/"failure_test_no_a_opt.d.res"))
    with pytest.raises(T4ParserException):
        t4p.parse_from_index(-1)
    assert ("Problem with energy bins: some bins are probably missing. "
            "Please make sure you run Tripoli-4 with '-a' option."
            in caplog.text)


def test_no_a_t4_opt_bad_bins_2(datadir, caplog):
    '''Use Tripoli-4 result from failure_noaopt_uniform_sources.d.res as
    example of parsing failure due to lack of option '-a'. In this case the
    spectrum is partially filled: bins are adjacent, but as the spectrum is in
    (*E*, *t*), the number of filled energy bins in the second time step being
    higher than in the first one, we get missing bins in the second step due to
    the use of '-a' optoin. A specific error is sent.
    '''
    t4p = T4Parser(str(datadir/"failure_noaopt_uniform_sources.d.res"))
    with pytest.raises(T4ParserException):
        t4p.parse_from_index(-1)
    assert ("IndexError: all (sub-)spectra should have the same bins."
            in caplog.text)
    assert ("Please make sure you run Tripoli-4 with option '-a'."
            in caplog.text)


def test_bad_response_name(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_bad_resp_name.d.res as example of
    failing parsing. In this case a not foreseen character, @, has been used in
    a response name. Pyparsing does not know to do with it and fails.
    '''
    t4p = T4Parser(str(datadir/"failure_test_bad_resp_name.d.res"))
    with pytest.raises(T4ParserException):
        t4p.parse_from_index(-1)
    assert "Parsing error located at line: 12, col: 1" in caplog.text


def test_no_normal_completion(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_normal_completion.d.res as
    example of lack of "NORMAL COMPLETION" in the output.

    In this case parsing is successful: its result exists, but the
    ``normalend`` boolean in scan is ``False``.
    '''
    t4p = T4Parser(str(datadir/"failure_test_no_normal_completion.d.res"))
    assert t4p
    assert ("Tripoli-4 listing did not finish with NORMAL COMPLETION."
            in caplog.text)
    assert t4p.scan_res.normalend is False
    assert t4p.scan_res.partial is True
    t4_res = t4p.parse_from_index(-1)
    assert t4_res.res['batch_data']['batch_number'] == 37
    t4rb = t4_res.to_browser()
    assert not t4rb.is_empty()
    assert len(t4rb.globals) == 4
    assert len(t4rb) == 1


def test_no_simulation_time(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_simu_time.d.res as example of
    lack of the end flag. In this case "NORMAL COMPLETION" is also missing but
    as pyparsing cannot find the end flag no parsing result can be built.
    '''
    with pytest.raises(T4ParserException):
        T4Parser(str(datadir/"failure_test_no_simu_time.d.res"))
    assert "No scan result built: no end flag found in the file" in caplog.text


def test_no_simulation_time_debug(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_simu_time.d.res as example of
    lack of the end flag. In this case "NORMAL COMPLETION" is also missing but
    as pyparsing cannot find the end flag no parsing result can be built.
    '''
    caplog.set_level(logging.DEBUG, logger='valjean')
    t4p = T4ParserDebug(str(datadir/"failure_test_no_simu_time.d.res"),
                        end_flag='ENERGY INTEGRATED RESULTS')
    _t4_res = t4p.parse_from_index(-1)
    assert ('No "time" variable found in the TRIPOLI-4 output, '
            'please check it.' in caplog.text)
    assert ('Remark: you are in parsing debug mode with an end flag not '
            'containing "time", this is expected.'
            in caplog.text)
    _t4_res.to_browser()
