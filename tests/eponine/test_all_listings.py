'''Test parsing of all listing contained in Qualtrip in MONO  and PARA.

.. todo::

   * To be moved in the future "qualtrip" package, in the corresponding
     chronological folder (here checks for version 10.2).
   * ``qualtrip*`` fixtures will also probably be moved to new "qualtrip"
     conftest module instead of here.
'''

import os
from glob import glob
import ast
import pytest
import valjean.eponine.parse_t4 as ep
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
# pylint: disable=redefined-outer-name

MONO = "MONO"
PARA = "PARA"
AUX = "qualtrip_aux"
MAIN = "qualtrip_main"
OUTPUTS = "output/ceav5"
MAIN_CATEGORIES = ["cristal", "elem", "protection"]

EXCLUDED_STRINGS_MONO = ["perle", "epicure", "part1", "phn_intrumen",
                         "test_pondng_auto_coupling", "gado_assembly"]
EXCLUDED_STRINGS_PARA = ["part1", "exp", "etape2", "homog_p3_prot",
                         "test_pondng_auto_coupling", "gado_assembly"]
EXCLUDED_STRINGS = ["sauv", "_v0", "save"]
MESH_LIM_FILES = ['godivaBeff_MED.d.res.ceav5']

# EXPECTED_RESULTS are counts expected from the input files run for a given
# version of the code.
# Numbers correspond to: files to read, jobs that fail, files excluded.
# Files can be excluded for various reasons: too long (gado-assembly), in MONO
# folder but run in PARA like epicure, run in MONO but in PARA like
# exploitation input files.
EXPECTED_RESULTS = {("cristal", MONO): (148, 0, 0),
                    ("cristal", PARA): (148, 0, 0),
                    ("elem", MONO): (99, 0, 0),
                    ("elem", PARA): (99, 0, 0),
                    ("protection", MONO): (25, 0, 0),
                    ("protection", PARA): (25, 0, 0),
                    ("tripoli44", MONO): (23, 0, 0),
                    ("tripoli44", PARA): (18, 1, 4),
                    ("tripoli45", MONO): (24, 0, 0),
                    ("tripoli45", PARA): (21, 0, 2),
                    ("tripoli46", MONO): (8, 0, 0),
                    ("tripoli46", PARA): (5, 0, 3),
                    ("tripoli47", MONO): (27, 0, 1),
                    ("tripoli47", PARA): (28, 0, 0),
                    ("tripoli48", MONO): (36, 0, 2),
                    ("tripoli48", PARA): (37, 0, 2),
                    ("tripoli49", MONO): (43, 0, 1),
                    ("tripoli49", PARA): (36, 0, 1),
                    ("tripoli410", MONO): (62, 5, 5),
                    ("tripoli410", PARA): (59, 4, 6),
                    ("tripoli4102", MONO): (2, 0, 0)}

AUX_CATEGORIES = sorted(list(
    filter(lambda y: y not in MAIN_CATEGORIES,
           set(map(lambda x: x[0], EXPECTED_RESULTS.keys())))))

QUALT_CATEGORIES = ([(MAIN, x) for x in MAIN_CATEGORIES]
                    + [(AUX, x) for x in AUX_CATEGORIES])
ALL_FOLDERS = [os.path.join(mode, *qualt_fold)
               for mode in [MONO, PARA]
               for qualt_fold in QUALT_CATEGORIES]
# need to remove tripoli4102 as was not run in PARA for VV of 10.2
ALL_FOLDERS.remove(os.path.join(PARA, AUX, "tripoli4102"))


@pytest.fixture
def qualtrip(request):
    '''Fixture to give qualtrip folder to pytest.'''
    return request.config.getoption('--qualtrip')


@pytest.fixture
def qualtrip_exclude(request):
    '''Fixture to exclude test on some patterns from qualtrip with pytest.

    Synthax: ``--qualtrip-exclude='["spam", "egg"]'``
    '''
    return request.config.getoption('--qualtrip-exclude')


@pytest.fixture
def qualtrip_match(request):
    '''Fixture to select patterns to test from qualtrip with pytest.

    Synthax: ``--qualtrip-match='["bacon"]'``
    '''
    return request.config.getoption('--qualtrip-match')


@pytest.fixture(params=ALL_FOLDERS)
def folder(qualtrip, qualtrip_exclude, qualtrip_match, request):
    '''Return folder from ``qualtrip`` to test following path given thought
    fixture :py:func:`tests.conftest.qualtrip`.

    Restriction are done using
    :py:func:`tests.conftest.qualtrip_exclude` and
    :py:func:`tests.conftest.qualtrip_match` fixtures'''
    folder = request.param
    if qualtrip_exclude:
        if any(pat in folder for pat in ast.literal_eval(qualtrip_exclude)):
            pytest.skip(str(qualtrip_exclude)+" excluded")
    if qualtrip_match:
        if not any(pat in folder for pat in ast.literal_eval(qualtrip_match)):
            pytest.skip("No matching with "+str(qualtrip_match)+" found")
    return os.path.join(qualtrip, folder, OUTPUTS)


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
        found_time = (ep.main(ifile, -1)
                      if os.path.basename(ifile) not in MESH_LIM_FILES
                      else ep.main(ifile, -1, mesh_lim=2))
        if found_time:
            nb_jdds_ok += 1
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
def test_t4_listings(folder):
    '''Test parsing of files contained in ``qualtrip``.
    By default all files are included, independent of the mode (MONO or PARA),
    and of the report section (main or aux). Restrictions are possible from
    command line, via options ``'--qualtrip-exclude='["spam", "egg"]'`` and
    ``'--qualtrip-match='["bacon"]'``.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of input files used, excluded and failed.
    '''
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
