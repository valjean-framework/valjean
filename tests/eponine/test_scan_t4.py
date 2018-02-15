'''Tests for the :mod:`scan_t4` module.'''

from hypothesis import given, note, assume, event, settings
from hypothesis.strategies import (integers, sets, text, lists, composite,
                                   sampled_from, booleans)
import pytest

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from glob import glob
import os

# pylint: disable=wrong-import-order
import valjean.eponine.scan_t4 as scan
from valjean.eponine.parse_t4 import T4Parser
# from ..conftest import datadir

# @pytest.fixture
# def datadir(tmpdir, request):
#     '''Fixture responsible for searching a folder called 'data' in the same
#     directory as the test module and, if available, moving all contents to a
#     temporary directory so tests can use them freely.
#     '''
#     filename = request.fspath
#     test_dir = filename.dirpath('data')

#     if test_dir.check():
#         test_dir.copy(tmpdir)

#     return tmpdir

# def test_scan_files(datadir):
#     print(os.path.isdir(datadir))
def test_scan_files():
    # t4_res = T4Parser.parse_jdd(datadir, 0)
    t4_res = T4Parser.parse_jdd("/home/el220326/valjean/tests/eponine/data/gauss_time_mu_phi_E.d.res.ceav5", 0)
    if t4_res:
        t4_res.print_t4_stats()
        print("result of the function =", t4_res.check_t4_times())
        t4_res.print_t4_times()
        assert t4_res.scan_res.normalend == True
        assert t4_res.scan_res.times['simulation time'] == 2
        assert t4_res.scan_res.times['initialization time'] == 0
        assert len(t4_res.scan_res) == 2
        print("len(t4_res.result) =", len(t4_res.result))
        assert len(t4_res.result) == 2
        print("keys in results:", list(t4_res.result[-1].keys()))
        print("nbre respinbses :", len(t4_res.result[-1]['list_responses']))
        assert len(t4_res.result[-1]['list_responses']) == 6
        for ibatch, batch in enumerate(t4_res.scan_res):
            assert batch == 200*(ibatch+1)
        for rbatch, batch in enumerate(reversed(t4_res.scan_res)):
            assert batch == 200*(len(t4_res.scan_res)-rbatch)
        assert t4_res.scan_res.get_last_edited_batch_number() == 400
    # print(datadir.getpath())
    # print(datadir.listdir())
    # lfiles = glob(datadir+"*res*")
    # print(lfiles)


def test_tungstene_file():
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        "/home/el220326/valjean/tests/eponine/data/tungstene.d.res.ceav5", -1, 5)
    if t4_res:
        t4_res.print_t4_stats()
        print("result of the function =", t4_res.check_t4_times())
        t4_res.print_t4_times()
        assert t4_res.scan_res.normalend == True
        assert t4_res.scan_res.times['simulation time'] == 6411
        assert t4_res.scan_res.times['initialization time'] == 0
        assert len(t4_res.scan_res) == 100
        assert len(t4_res.result) == 1
        assert len(t4_res.result[-1]['list_responses']) == 1

# def test_petit_coeur_para():
#     t4_res = T4Parser.parse_jdd_with_mesh_lim(
#         "/home/el220326/valjean/tests/eponine/data/create_petitcoeur.d.PARA.res.ceav5",
#         -1, -1, "simulation time")
#     if t4_res:
#         t4_res.print_t4_stats()
#         print("result of the function =", t4_res.check_t4_times())
#         t4_res.print_t4_times()
#         assert t4_res.scan_res.normalend == True
#         assert t4_res.scan_res.times['simulation time'] == 0
#         assert t4_res.scan_res.times['initialization time'] == 11
#         assert t4_res.scan_res.times['elapsed time'] == 47
#         assert len(t4_res.scan_res) == 1
#         print("len(t4_res.result) =", len(t4_res.result))
#         assert len(t4_res.result) == 1
#         print("keys in results:", list(t4_res.result[-1].keys()))
#         print("nbre respinbses :", len(t4_res.result[-1]['list_responses']))
#         assert len(t4_res.result[-1]['list_responses']) == 2

def test_ttSimplePacket100_para():
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        "/home/el220326/valjean/tests/eponine/data/ttsSimplePacket100.d.PARA.res.ceav5",
        -1, -1)
    if t4_res:
        assert t4_res.scan_res.normalend == True
        assert t4_res.scan_res.times['simulation time'] == 0
        assert t4_res.scan_res.times['initialization time'] == 3
        assert t4_res.scan_res.times['elapsed time'] == 1057
        assert len(t4_res.scan_res) == 1
        assert len(t4_res.result) == 1
        assert len(t4_res.result[-1]['list_responses']) == 4

# END_FLAGS has to be "re-initialized" at the end, else would continue to stop
# at number of batchs
def test_entropy_in_debug():
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        "/home/el220326/valjean/tests/eponine/data/entropy.d.res.ceav5",
        -1, 10, "number of batches used")
    if t4_res:
        assert t4_res.scan_res.normalend == True
        assert t4_res.scan_res.times['simulation time'] == 2471
        assert t4_res.scan_res.times['initialization time'] == 6
        assert len(t4_res.scan_res) == 1000
        assert len(t4_res.result) == 1
        assert len(t4_res.result[-1]['list_responses']) == 1
        t4_res.scan_res.END_FLAGS.pop(0)

def test_ifp():
    t4_res = T4Parser.parse_jdd(
        "/home/el220326/valjean/tests/eponine/data/GODIVA_ifp_statistics.d.res.ceav5", -1)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['simulation time'] == 4421
        assert t4_res.scan_res.times['initialization time'] == 47
        assert len(t4_res.result) == 1
        assert len(t4_res.result[-1]['list_responses']) == 20

def test_kij():
    t4_res = T4Parser.parse_jdd(
        "/home/el220326/valjean/tests/eponine/data/kijAssRoot.d.res.ceav5", -1)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['simulation time'] == 247247
        assert t4_res.scan_res.times['initialization time'] == 23
        assert len(t4_res.result) == 1
        assert len(t4_res.result[-1]['list_responses']) == 3

def test_green_bands():
    t4_res = T4Parser.parse_jdd(
        "/home/el220326/valjean/tests/eponine/data/"
        "greenband_exploit_T410_contrib.d.res.ceav5", -1)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['exploitation time'] == 2
        assert t4_res.scan_res.times['initialization time'] == 2
        assert len(t4_res.result) == 1

def test_ttSimplePacket100_mono():
    t4_res = T4Parser.parse_jdd("/home/el220326/valjean/tests/eponine/data/"
                                "ttsSimplePacket100.d.res.ceav5", 0)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['simulation time'] == 4984
        assert t4_res.scan_res.times['initialization time'] == 3
        assert len(t4_res.scan_res) == 40
        assert len(t4_res.result[-1]['list_responses']) == 4

# @pytest.mark.usefixtures("datadir")
def test_pertu():
    # mondir = datadir("datatmp", os.path("/home/el220326/valjean/tests/eponine"))
    # print(mondir)
    # print(os.listdir(os.getcwd()))
    print(os.listdir("tests/eponine/data"))
    t4_res = T4Parser.parse_jdd("/home/el220326/valjean/tests/eponine/data/"
                                "pertu_covariances.d.res.ceav5", -1)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['simulation time'] == 370
        assert t4_res.scan_res.times['initialization time'] == 0
        assert len(t4_res.scan_res) == 10
        assert len(t4_res.result[-1]['list_responses']) == 2

def test_vov():
    t4_res = T4Parser.parse_jdd("/home/el220326/valjean/tests/eponine/data/"
                                "vov.d.res.ceav5", -1)
    if t4_res:
        assert t4_res.scan_res.normalend is True
        assert t4_res.scan_res.times['simulation time'] == 112
        assert t4_res.scan_res.times['initialization time'] == 9
        assert len(t4_res.scan_res) == 5
        assert len(t4_res.result[-1]['list_responses']) == 2
