'''Tests for the :mod:`scan_t4` module.'''

from hypothesis import given, note, assume, event, settings
from hypothesis.strategies import (integers, sets, text, lists, composite,
                                   sampled_from, booleans)
import pytest

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from glob import glob
import os
import sys

# pylint: disable=wrong-import-order
import valjean.eponine.scan_t4 as scan
from valjean.eponine.parse_t4 import T4Parser
from valjean.eponine.pyparsing_t4 import transform

def test_gauss_spectrum(datadir):
    '''Test Tripoli-4 listing with spectrum in output depending on time, µ and
    φ angles. Also control number of batchs.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"gauss_time_mu_phi_E.d.res.ceav5"), 0)
    assert t4_res
    # t4_res.print_t4_stats()
    assert t4_res.check_t4_times()
    # t4_res.print_t4_times()
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 2
    assert t4_res.scan_res.times['initialization time'] == 0
    assert len(t4_res.scan_res) == 2
    assert len(t4_res.result) == 2
    assert len(t4_res.result[-1]['list_responses']) == 6
    for ibatch, batch in enumerate(t4_res.scan_res):
        assert batch == 200*(ibatch+1)
    for rbatch, batch in enumerate(reversed(t4_res.scan_res)):
        assert batch == 200*(len(t4_res.scan_res)-rbatch)
    assert t4_res.scan_res.get_last_edited_batch_number() == 400
    resp0 = t4_res.result[-1]['list_responses'][0]
    assert resp0['response_description']['resp_function'] == "COURANT"
    assert resp0['results'][0]['scoring_mode'] == "SCORE_SURF"


def test_tungstene_file(datadir):
    '''Use Tripoli-4 output from tungstene.d to test meshes (also depending on
    energy).
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"tungstene.d.res.ceav5"), -1)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 423
    assert t4_res.scan_res.times['initialization time'] == 0
    assert len(t4_res.scan_res) == 1
    assert len(t4_res.result) == 1
    assert len(t4_res.result[-1]['list_responses']) == 1
    resp0 = t4_res.result[-1]['list_responses'][0]
    assert resp0['response_description']['particle'] == "PHOTON"
    assert resp0['results'][0]['scoring_mode'] == "SCORE_TRACK"
    print(list(resp0['results'][0].keys()))
    # assert resp0['results'][0]

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
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        str(datadir/"ttsSimplePacket20.d.PARA.res.ceav5"), -1, -1)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 0
    assert t4_res.scan_res.times['initialization time'] == 4
    assert t4_res.scan_res.times['elapsed time'] == 250
    assert len(t4_res.scan_res) == 1
    assert len(t4_res.result) == 1
    assert len(t4_res.result[-1]['list_responses']) == 4
    resp2desc = t4_res.result[-1]['list_responses'][2]['response_description']
    assert resp2desc['compo_details'][0]['reaction_on_nucleus'] == "U235"
    assert resp2desc['compo_details'][0]['temperature'] == 300
    assert resp2desc['compo_details'][0]['composition'] == "COMBUSTIBLE"

def test_entropy_in_debug(datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum and
    debug mode.
    '''
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        str(datadir/"entropy.d.res.ceav5"), -1, 10, "number of batches used")
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 24
    assert t4_res.scan_res.times['initialization time'] == 6
    assert len(t4_res.scan_res) == 10
    assert len(t4_res.result) == 1
    assert len(t4_res.result[-1]['list_responses']) == 1
    res0 = t4_res.result[-1]['list_responses'][0]['results'][0]
    rescontent = ['scoring_mode', 'scoring_zone',
                  'mesh_res', 'boltzmann_entropy', 'shannon_entropy',
                  'spectrum_res', 'integrated_res']
    print('batch:', t4_res.result[-1]['edition_batch_number'])
    assert "{0:6e}".format(res0['boltzmann_entropy']) == "8.342621e-01"
    assert sorted(list(res0.keys())) == sorted(rescontent)

def test_entropy(datadir):
    '''Use Tripoli-4 result from entropy.d to test entropy, mesh, spectrum with
    progressively converging results.
    '''
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        str(datadir/"entropy.d.res.ceav5"), 0, 10)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 24
    assert t4_res.scan_res.times['initialization time'] == 6
    assert len(t4_res.scan_res) == 10
    assert len(t4_res.result) == 10
    assert len(t4_res.result[-1]['list_responses']) == 2
    lastres = t4_res.result[-1]['list_responses']
    resp_func = ['REACTION', 'KEFFS']
    for ind, ires in enumerate(lastres):
        assert ires['response_description']['resp_function'] == resp_func[ind]
    firstres = t4_res.result[0]['list_responses']
    assert 'not_converged' in firstres[1]['results']['keff_res']

# @pytest.fixture(scope="function", params="valjean_verbose", autouse=True)
# def use_verbosity(request):
#     # print(request.config.getoption("valjean-verbose"))
#     yield request.param

# def test_entropy_verbose(datadir, monkeypatch, use_verbosity):
# def test_entropy_verbose(datadir, monkeypatch, pytestconfig):
# def test_entropy_verbose(datadir, monkeypatch, metafunc):
# def test_entropy_verbose(datadir, monkeypatch, valjean_verbose):
# @pytest.config('valjean_verbose')
# def test_entropy_verbose(datadir, monkeypatch):  #, pytestconfig):
def test_entropy_verbose(datadir, monkeypatch):
    '''Use Tripoli-4 result from entropy.d to test verbosity (mesh and spectrum
    in same jdd), but long.
    '''
    # verb = pytestconfig.getoption('valjean_verbose')
    # print("verb =", verb)
    # print(valjean_verbose)
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        str(datadir/"entropy.d.res.ceav5"), -1, 10)
    assert t4_res
    assert t4_res.scan_res.normalend
    # pytestconfig.addinivalue_line('valjean_verbose', "--valjean-verbose")
    # print(pytestconfig.getoption('valjean_verbose', default=True))
    # if verbose:
    import logging
    logger = logging.getLogger('valjean')
    logger.setLevel(logging.DEBUG)
    # monkeypatch.setattr(logging, "getLogger", logging.DEBUG)
    # monkeypatch.setattr("logging.getLogger('valjean')", logging.DEBUG)
    # monkeypatch.setattr("logger", logging.DEBUG)
    # print(metafunc.fixturenames)
    # monkeypatch.setitem(pytestconfig, "valjean-verbose", True)
    monkeypatch.setattr("valjean.eponine.pyparsing_t4.transform.MAX_DEPTH", 5)
    transform.print_result(t4_res.result)

# def test_entropy_verbose(datadir, monkeypatch, verbose):
#     '''Use Tripoli-4 result from entropy.d to test verbosity (mesh and spectrum
#     in same jdd), but long.
#     '''
#     # verb = pytestconfig.getoption('valjean_verbose')
#     # print("verb =", verb)
#     # print(valjean_verbose)
#     t4_res = T4Parser.parse_jdd_with_mesh_lim(
#         str(datadir/"entropy.d.res.ceav5"), -1, 10)
#     assert t4_res
#     assert t4_res.scan_res.normalend
#     # if verbose:
#     # import logging
#     # logger = logging.getLogger('valjean')
#     # logger.setLevel(logging.DEBUG)
#     # monkeypatch.setattr(logging, "getLogger", logging.DEBUG)
#     # monkeypatch.setattr("logging.getLogger('valjean')", logging.DEBUG)
#     # monkeypatch.setattr("logger", logging.DEBUG)
#     # print(metafunc.fixturenames)
#     if verbose:
#         monkeypatch.setattr("valjean.eponine.pyparsing_t4.transform.MAX_DEPTH", 5)
#     transform.print_result(t4_res.result)

def test_ifp(datadir):
    '''Use Tripoli-4 result from GODIVA_ifp_statistics.d to test IFP parsing.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"GODIVA_ifp_statistics.d.res.ceav5"), -1)
    assert t4_res
    print(t4_res.scan_res.end_flags)
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 15
    assert t4_res.scan_res.times['initialization time'] == 18
    assert len(t4_res.result) == 1
    assert len(t4_res.result[-1]['list_responses']) == 20
    last_resp = t4_res.result[-1]['list_responses'][-1]
    assert (last_resp['response_description']['resp_function']
            == "IFP ADJOINT WEIGHTED ROSSI ALPHA")
    assert last_resp['results']['ifp_res']['used_batch'] == 81

def test_kij(datadir):
    '''Use tripoli-4 result from cylindreDecR_with_kij_on_mesh.d to test
    k\ :sub:`ij` matrix parsing.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"cylindreDecR_with_kij_on_mesh.d.res.ceav5"), -1)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 69
    assert t4_res.scan_res.times['initialization time'] == 1
    assert len(t4_res.result) == 1
    assert len(t4_res.result[-1]['list_responses']) == 16
    resp_list = t4_res.result[-1]['list_responses']
    assert (resp_list[13]['response_description']['resp_function']
            == "KIJ_MATRIX")
    assert (resp_list[14]['response_description']['resp_function']
            == "KIJ_SOURCES")
    assert resp_list[15]['response_description']['resp_function'] == "KEFFS"

def test_green_bands(datadir):
    '''Use Tripoli-4 result from greenband_exploit_T410_contrib.d to test Green
    bands parsing and exploitation jobs.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"greenband_exploit_T410_contrib.d.res.ceav5"), -1)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['exploitation time'] == 2
    assert t4_res.scan_res.times['initialization time'] == 2
    assert len(t4_res.result) == 1

def test_tt_simple_packet20_mono(datadir):
    '''Use Tripoli-4 result from ttsSimplePacket20.d run in mono-processor
    mode to test PACKET_LENGTH feature in MONO case.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"ttsSimplePacket20.d.res.ceav5"), 0)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 217
    assert t4_res.scan_res.times['initialization time'] == 3
    assert len(t4_res.scan_res) == 2
    assert len(t4_res.result[-1]['list_responses']) == 4

def test_pertu(datadir):
    '''Use Tripoli-4 result from pertu_covariances.d to test perturbations and
    uncertainty spectrum.
    '''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"pertu_covariances.d.res.ceav5"), -1)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 27
    assert t4_res.scan_res.times['initialization time'] == 0
    assert len(t4_res.scan_res) == 1
    assert len(t4_res.result[-1]['list_responses']) == 2

def test_vov(datadir):
    '''Use Tripoli-4 result from vov.d to test vov spectra.'''
    t4_res = T4Parser.parse_jdd(
        str(datadir/"vov.d.res.ceav5"), 0)
    assert t4_res
    assert t4_res.scan_res.normalend
    assert t4_res.scan_res.times['simulation time'] == 33
    assert t4_res.scan_res.times['initialization time'] == 6
    assert len(t4_res.scan_res) == 2
    assert len(t4_res.result[-1]['list_responses']) == 2
