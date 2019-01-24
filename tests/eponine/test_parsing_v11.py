'''Test parsing of all listing contained in Qualtrip in MONO  and PARA.

.. todo::

   * To be moved in the future "qualtrip" package, in the corresponding
     chronological folder (here checks for version 10.2).
   * ``qualtrip*`` fixtures will also probably be moved to new "qualtrip"
     conftest module instead of here.
'''

import os
from glob import glob
import pytest
import valjean.eponine.tripoli4.parse as ep
from valjean.eponine.tripoli4.accessor import Accessor
from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=redefined-outer-name


MONO = "MONO"
PARA = "PARA"
AUX = "qualtrip_aux"
MAIN = "qualtrip_main"
OUTPUTS = "output/ceav5"
MAIN_CATEGORIES = ["cristal", "elem", "protection"]

EXCLUDED_STRINGS_MONO = ["perle", "epicure", "part1", "phn_intrumen",
                         "test_pondng_auto_coupling", "gado_assembly",
                         "jezebel", "faddegon", "fcore", "ntoffg4"]
EXCLUDED_STRINGS_PARA = ["part1", "exp", "etape2", "homog_p3_prot",
                         "test_pondng_auto_coupling", "gado_assembly"]
EXCLUDED_STRINGS = ["sauv", "_v0", "save", "gammaFRP.", "_connectivity"]
MESH_LIM_FILES = ['godivaBeff_MED.d.res.ceav5']

# EXPECTED_RESULTS are counts expected from the input files run for a given
# version of the code.
# Numbers correspond to: files to read, jobs that fail, files excluded.
# Files can be excluded for various reasons: too long (gado-assembly), in MONO
# folder but run in PARA like epicure, run in MONO but in PARA like
# exploitation input files.
EXPECTED_RESULTS = {("cristal", MONO): (148, 0, 0),
                    ("cristal", PARA): (148, 0, 0),
                    ("elem", MONO): (109, 0, 0),
                    ("elem", PARA): (109, 0, 0),
                    ("protection", MONO): (25, 0, 0),
                    ("protection", PARA): (25, 0, 0),
                    ("tripoli44", MONO): (22, 0, 0),
                    ("tripoli44", PARA): (18, 1, 4),
                    ("tripoli45", MONO): (22, 0, 0),
                    ("tripoli45", PARA): (21, 0, 2),
                    ("tripoli46", MONO): (8, 0, 0),
                    ("tripoli46", PARA): (5, 0, 3),
                    ("tripoli47", MONO): (27, 0, 1),
                    ("tripoli47", PARA): (28, 0, 0),
                    ("tripoli48", MONO): (33, 0, 2),
                    ("tripoli48", PARA): (37, 0, 2),
                    ("tripoli49", MONO): (39, 0, 9),  # many jezebel excluded
                    ("tripoli49", PARA): (36, 0, 1),
                    ("tripoli410", MONO): (59, 4, 5),
                    ("tripoli410", PARA): (59, 4, 6),
                    ("tripoli411", MONO): (62, 0, 7),
                    ("tripoli411", PARA): (59, 4, 6)}

AUX_CATEGORIES = sorted(list(
    filter(lambda y: y not in MAIN_CATEGORIES,
           set(map(lambda x: x[0], EXPECTED_RESULTS.keys())))))

QUALT_CATEGORIES = ([(MAIN, x) for x in MAIN_CATEGORIES]
                    + [(AUX, x) for x in AUX_CATEGORIES])
ALL_FOLDERS = [os.path.join(mode, *qualt_fold)
               for mode in [MONO, PARA]
               for qualt_fold in QUALT_CATEGORIES]
# need to remove tripoli4102 as was not run in PARA for VV of 10.2
# ALL_FOLDERS.remove(os.path.join(PARA, AUX, "tripoli4102"))


@pytest.fixture
def qualtrip(request):
    '''Fixture to give qualtrip folder to pytest.'''
    return request.config.getoption('--qualtrip')


@pytest.fixture
def qualtrip_exclude(request):
    '''Fixture to exclude test on some patterns from qualtrip with pytest.

    Synthax: ``--qualtrip-exclude=spam,egg``
    '''
    return request.config.getoption('--qualtrip-exclude')


@pytest.fixture
def qualtrip_match(request):
    '''Fixture to select patterns to test from qualtrip with pytest.

    Synthax: ``--qualtrip-match=bacon``
    '''
    return request.config.getoption('--qualtrip-match')


@pytest.fixture(params=ALL_FOLDERS)
def folder(qualtrip, qualtrip_exclude, qualtrip_match, request):
    '''Return folder from ``qualtrip`` to test following path given thought
    fixture :py:func:`~.qualtrip`, called by ``--quatrip=`` command line
    option.

    Restriction are done using
    :py:func:`~.qualtrip_exclude` and :py:func:`~.qualtrip_match` fixtures
    respectively called by ``--qualtrip-exclude=`` and ``--qualtrip-match=``
    command line options. These options work like a 'OR': if more than one
    argument are given, it needs to exclude or match with at least one.
    '''
    if not qualtrip:
        pytest.skip('A "qualtrip" folder is need to run this test, '
                    'please specify it thanks to --qualtrip= option')
    folder = request.param
    if qualtrip_exclude:
        if any(pat in folder for pat in qualtrip_exclude.split(',')):
            pytest.skip(str(qualtrip_exclude)+" excluded")
    if qualtrip_match:
        if not any(pat in folder for pat in qualtrip_match.split(',')):
            pytest.skip("No matching with '"+str(qualtrip_match)+"' found")
    return os.path.join(qualtrip, folder, OUTPUTS)


def result_test(res):
    '''Test content of the parsing result: presence of times, ``'results'`` key
    if ``'list_responses'`` is found in the parsing result.

    :retrns: bool if time was found (but should always happen as there is an
             assert before)
    '''
    # get last result (default returns list if more than one batch required)
    # elapsed_time needed for cases with PARTIAL EDITION (not correct end)
    assert ('simulation_time' in res.result[-1].keys()
            or 'exploitation_time' in res.result[-1].keys()
            or 'elapsed_time' in res.result[-1].keys())
    print("keys =", list(res.result[-1].keys()))
    if 'list_responses' in res.result[-1].keys():
        lresp = res.result[-1]['list_responses']
        assert isinstance(lresp, list)
        for resp in lresp:
            assert 'results' in resp
            assert isinstance(resp['results'], dict)
            assert isinstance(resp['response_type'], str)
    if not any("_time" in s for s in res.result[-1].keys()):
        return False
    return True


def accessor_test(res):
    '''Quick test of accessor.

    Main goal of this test is not apparent: it is to check if the accessor can
    be built for all types of responses available in the T4 outputs given set,
    else accessor has to be updated to probably take into account a new type of
    response.
    '''
    t4acc = Accessor(res.result[-1])
    if t4acc.resp_book is None:
        assert all('list_responses' not in x for x in t4acc.parsed_res)
        return
    ids = set()
    for _v0 in t4acc.resp_book.index.values():
        for _v1 in _v0.values():
            ids |= _v1
    assert ids == set(range(len(t4acc.resp_book.responses)))


def loop_on_files(filelist):
    '''Perform the loop over the file list, parse all of them and returns
    result of this parsing.

    :param list filelist: list of paths to the files to be read and parsed
    :returns: a tuple containing

             * **nb_jdds_ok**, `int`: number of jdds correctly parsed
               (``'NORMAL COMPLETION'`` and duration at the end)
             * **failed_jdds**, `list of string`: list of the failed jdds
    '''
    nb_jdds_ok = 0
    failed_jdds = []
    for ifile in filelist:
        print("Reading:", ifile)
        res = (ep.T4Parser.parse_jdd(ifile, -1)
               if os.path.basename(ifile) not in MESH_LIM_FILES
               else ep.T4Parser.parse_jdd_with_mesh_lim(ifile, -1, mesh_lim=2))
        if res:
            if result_test(res):
                nb_jdds_ok += 1
            else:
                print("\x1b[1;31mOn passe par la ?\x1b[0m")
                failed_jdds.append(ifile)
            # quick temporary test of accessor
            accessor_test(res)
        else:
            failed_jdds.append(ifile)
    return nb_jdds_ok, failed_jdds


def print_summary(nb_ok, nb_used, failed, excluded):
    '''Print the summary of the parsing, especially lists of failed and
    excluded files.
    '''
    print("Jdds well passed:", nb_ok, "/", nb_used)
    print("Failed jdds:")
    for ifile in failed:
        print(ifile)
    print("Excluded files:")
    for ifile in excluded:
        print(ifile)


@pytest.mark.slow
def test_t4_listings(folder, request, monkeypatch):
    '''Test parsing of files contained in ``qualtrip``.
    By default all files are included, independent of the mode (MONO or PARA),
    and of the report section (main or aux). Restrictions are possible from
    command line, via options ``'--qualtrip-exclude='["spam", "egg"]'`` and
    ``'--qualtrip-match='["bacon"]'``.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of input files used, excluded and failed.
    '''
    if request.config.getoption('--valjean-verbose'):
        monkeypatch.setattr("valjean.eponine.tripoli4.dump.MAX_DEPTH", 6)
    all_files = sorted(glob(os.path.join(folder, "*.res.ceav5")))
    excluded_patterns = (EXCLUDED_STRINGS_MONO + EXCLUDED_STRINGS
                         if MONO in folder
                         else EXCLUDED_STRINGS_PARA + EXCLUDED_STRINGS)
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in excluded_patterns)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    excluded_files = [fil for fil in excluded_files
                      if not any(pat in fil for pat in EXCLUDED_STRINGS)]
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    mode = MONO if MONO in folder else PARA
    assert len(used_files) == EXPECTED_RESULTS[(category, mode)][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[(category, mode)][1]
    assert len(excluded_files) == EXPECTED_RESULTS[(category, mode)][2]
