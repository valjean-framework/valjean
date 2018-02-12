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

@pytest.fixture
def datadir(tmpdir, request):
    '''Fixture responsible for searching a folder called 'data' in the same
    directory as the test module and, if available, moving all contents to a
    temporary directory so tests can use them freely.
    '''
    filename = request.fspath
    test_dir = filename.dirpath('data')

    if test_dir.check():
        test_dir.copy(tmpdir)

    return tmpdir

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
        print("len(t4_res.result) =", len(t4_res.result))
        assert len(t4_res.result) == 1
        print("keys in results:", list(t4_res.result[-1].keys()))
        print("nbre respinbses :", len(t4_res.result[-1]['list_responses']))
        assert len(t4_res.result[-1]['list_responses']) == 1

def test_entropy_in_debug():
    t4_res = T4Parser.parse_jdd_with_mesh_lim(
        "/home/el220326/valjean/tests/eponine/data/entropy.d.res.ceav5",
        -1, 10, "simulation time")
    if t4_res:
        t4_res.print_t4_stats()
        print("result of the function =", t4_res.check_t4_times())
        t4_res.print_t4_times()
        assert t4_res.scan_res.normalend == True
        assert t4_res.scan_res.times['simulation time'] == 2471
        assert t4_res.scan_res.times['initialization time'] == 6
        assert len(t4_res.scan_res) == 1000
        print("len(t4_res.result) =", len(t4_res.result))
        assert len(t4_res.result) == 1
        print("keys in results:", list(t4_res.result[-1].keys()))
        print("nbre respinbses :", len(t4_res.result[-1]['list_responses']))
        assert len(t4_res.result[-1]['list_responses']) == 2
