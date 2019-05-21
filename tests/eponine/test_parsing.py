'''Test parsing of all listings contained in the selected folders from
``--parsing-config-file`` option.

Exclusion and matching are possible via ``--parsing-exclude`` and
``--parsing-match`` options.

Tests are done on successful parsing of all the listed files and on possibility
to access the results via the module :mod:`~valjean.eponine.tripoli4.accessor`.

Expected variables in the configuration file are:
  * PATH: path to the folder containing the screened folder structure
  * ALL_FOLDERS: folders structures (like ``MONO/qualtrip_main/tripoli44/``)
  * OUTPUTS: final folsers (like ``output/ceav5/``)
  * END_FILES: common file extension (like ``res.ceav5``)
  * MONO: path part to idenity listings run in mono-processor
  * PARA: path part to idenity listings run in parallel
  * EXCLUDED_STRINGS_MONO: strings to exclude from parsing of files run in MONO
    (known failures, parallel listings linked, etc)
  * EXCLUDED_STRINGS_PARA: strings to exclude from parsing of files run in PARA
    (know listings run in mono-processor mode like exploitation ones)
  * EXCLUDED_STRINGS: strings excluded both in MONO and PARA (like too long
    ones)
  * EXPECTED_RESULTS: dictionary of results containing
      (name of category, mode) : (number of files to read,
                                  number of jobs that failed,
                                  number of files excluded from strings)
'''

import os
from glob import glob
import logging
import pytest
from valjean.eponine.tripoli4.parse import T4Parser, T4ParserException
from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=redefined-outer-name


def result_test(res):
    '''Test content of the parsing result: presence of times, ``'results'`` key
    if ``'list_responses'`` is found in the parsing result.

    :retrns: bool if time was found (but should always happen as there is an
             assert before)
    '''
    # get last result (default returns list if more than one batch required)
    # elapsed_time needed for cases with PARTIAL EDITION (not correct end)
    assert any("_time" in s for s in res.result[-1].keys())
    print("keys =", list(res.result[-1].keys()))
    if 'list_responses' in res.result[-1].keys():
        lresp = res.result[-1]['list_responses']
        assert isinstance(lresp, list)
        for resp in lresp:
            assert 'results' in resp
            assert isinstance(resp['results'], dict)
            assert isinstance(resp['response_type'], str)
    return res.scan_res.normalend


def response_book_test(res):
    '''Quick test of ResponseBook.

    Main goal of this test is not apparent: it is to check if the accessor can
    be built for all types of responses available in the T4 outputs given set,
    else accessor has to be updated to probably take into account a new type of
    response.

    A first check on the presence of the ``book_type`` is done in order to
    avoid a useless error here.
    '''
    t4rb = res.build_response_book()
    if t4rb is None:
        return
    ids = set()
    for _v0 in t4rb.index.values():
        for _v1 in _v0.values():
            ids |= _v1
    assert ids == set(range(len(t4rb.responses)))
    assert t4rb.globals


def loop_on_files(filelist, cfile):
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
        try:
            res = (T4Parser(ifile, -1)
                   if os.path.basename(ifile) not in cfile.MESH_LIM_FILES
                   else T4Parser(ifile, -1, mesh_lim=2))
        except T4ParserException:
            failed_jdds.append(ifile)
            continue
        if result_test(res):
            nb_jdds_ok += 1
        else:
            failed_jdds.append(ifile)
        # quick temporary test of accessor
        assert res.check_t4_times()
        response_book_test(res)
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
def test_listing_parsing(caplog, vv_params, parsing_exclude, parsing_match):
    '''Test parsing of files configured from the ``--parsing-config-file``
    option.

    By default all files are included, independent of the mode (MONO or PARA),
    and of the report section (main or aux). Restrictions are possible from
    command line, via options ``'--parsing-exclude='["spam", "egg"]'`` and
    ``'--parsing-exclude-match='["bacon"]'``.
    Currently adapted to version 11 of Tripoli-4.

    Tests performed on number of input files used, excluded and failed.
    '''
    caplog.set_level(logging.WARNING, logger='valjean')
    vv_folder, vv_file = vv_params
    if parsing_exclude:
        if any(pat in vv_folder for pat in parsing_exclude.split(',')):
            pytest.skip(str(parsing_exclude)+" excluded")
    if parsing_match:
        if not any(pat in vv_folder for pat in parsing_match.split(',')):
            pytest.skip("No matching with '"+str(parsing_match)+"' found")
    folder = os.path.join(vv_file.PATH, vv_folder, vv_file.OUTPUTS)
    all_files = sorted(glob(os.path.join(folder, "*."+vv_file.END_FILES)))
    excluded_patterns = (
        vv_file.EXCLUDED_STRINGS_MONO + vv_file.EXCLUDED_STRINGS
        if vv_file.MONO in folder
        else vv_file.EXCLUDED_STRINGS_PARA + vv_file.EXCLUDED_STRINGS)
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in excluded_patterns)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    excluded_files = [
        fil for fil in excluded_files
        if not any(pat in fil for pat in vv_file.EXCLUDED_STRINGS)]
    jdds_ok, failed_jdds = loop_on_files(used_files, vv_file)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    mode = vv_file.MONO if vv_file.MONO in folder else vv_file.PARA
    assert len(used_files) == vv_file.EXPECTED_RESULTS[(category, mode)][0]
    assert len(failed_jdds) == vv_file.EXPECTED_RESULTS[(category, mode)][1]
    assert len(excluded_files) == vv_file.EXPECTED_RESULTS[(category, mode)][2]
