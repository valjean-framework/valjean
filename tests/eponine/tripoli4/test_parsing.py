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

'''Test parsing of all listings contained in the selected folders from
``--parsing-config-file-t4`` option.

Exclusion and matching are possible via ``--parsing-exclude`` and
``--parsing-match`` options.

Tests are done on successful parsing of all the listed files and on possibility
to access the results via the
:class:`~valjean.eponine.browser.Browser`.

Expected variables in the configuration file are:
  * PATH: path to the folder containing the screened folder structure
  * ALL_FOLDERS: folders structures (like ``MONO/qualtrip_main/tripoli44/``)
  * OUTPUTS: final folders (like ``output/ceav5/``)
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
import itertools
import pathlib
import logging
from collections import namedtuple
import pytest
from valjean.eponine.dataset import Dataset
from valjean.eponine.tripoli4.parse import Parser, ParserException
from ...context import valjean  # noqa: F401, pylint: disable=unused-import
from ..conftest import skip_parsing_files, skip_excluded_files


def result_test(t4pres, norm_end):
    '''Test content of the parsing result: presence of times, ``'results'`` key
    if ``'list_responses'`` is found in the parsing result.

    :param res: ParseResult
    :param bool norm_end: if normal end is expected and checked should be True,
        else False

    :returns: bool if time was found (but should always happen as there is an
        assert before)
    '''
    # get last result (default returns list if more than one batch required)
    # elapsed_time needed for cases with PARTIAL EDITION (not correct end)
    assert any("_time" in s for s in t4pres.res['batch_data'].keys())
    if 'list_responses' in t4pres.res.keys():
        lresp = t4pres.res['list_responses']
        assert isinstance(lresp, list)
        for resp in lresp:
            assert 'results' in resp
            assert isinstance(resp['results'], dict)
            assert isinstance(resp['response_type'], str)
    if norm_end:
        return t4pres.res['run_data']['normal_end']
    return True


def check_data(responses):
    '''Check content of data and conversion fo dataset.

    Check content of data: ``'results'`` key should be present in all the
    responses of the *Browser*, ``'_res'`` should have be removed from all
    ``response_type``, no key under ``'results'`` should contain ``'_res'``.
    Check the conversion in dataset: test conversion of all elements under
    ``'results'`` in a dataset.

    If the results is a string, it is highly probable not converged, so not
    possible to be converted in a dataset.
    '''
    for iresp in responses:
        assert 'results' in iresp
        assert not all('_res' in dtype for dtype in iresp['results'])
        for dname, data in iresp['results'].items():
            if ((not isinstance(data, str)
                 and dname not in ('units', 'coordinates'))):
                assert isinstance(data, Dataset), 'Not a Dataset'


def browser_test(res):
    '''Quick test of Browser.

    Main goal of this test is not apparent: it is to check if the
    *Browser* can be built for all types of responses available in the T4
    outputs given set, else parsing, transform or common have to be updated to
    probably take into account a new type of response.
    '''
    t4rb = res.to_browser()
    if t4rb is None:
        return
    ids = set()
    for _v0 in t4rb.index.values():
        for _v1 in _v0.values():
            ids |= _v1
    assert ids == set(range(len(t4rb.content)))
    assert t4rb.globals
    if t4rb.content:
        assert not all('_res' in rtype
                       for rtype in t4rb.available_values('response_type'))
        check_data(t4rb.content)


def loop_on_files(filelist, norm_end=True):
    '''Perform the loop over the file list, parse all of them and returns
    result of this parsing.

    :param list filelist: list of paths to the files to be read and parsed
    :param bool norm_end: if normal end is expected and checked should be True,
        else False, default: True
    :returns: a tuple containing

             * **nb_jdds_ok**, `int`: number of jdds correctly parsed
               (``'NORMAL COMPLETION'`` and duration at the end)
             * **failed_jdds**, `list of string`: list of the failed jdds
    '''
    nb_jdds_ok = 0
    failed_jdds, failed_time_jdds, failed_browser_jdds = [], [], []
    for ifile in filelist:
        print("Reading:", ifile)
        try:
            res = Parser(ifile)
        except ParserException as pex:
            print(f"ParserException: {pex} (probably in scan)")
            failed_jdds.append(ifile)
            continue
        if not res.check_times():
            print("Issue with times, please check")
            failed_time_jdds.append(ifile)
        try:
            pres = res.parse_from_index(-1)
        except ParserException as pex:
            print(f"ParserException: {pex}")
            failed_jdds.append(ifile)
            continue
        if result_test(pres, norm_end):
            nb_jdds_ok += 1
        else:
            failed_jdds.append(ifile)
        try:
            browser_test(pres)
        except AssertionError as aerb:
            print(f"Error in browser: {aerb}")
            failed_browser_jdds.append(ifile)
    return {'jdds_ok': nb_jdds_ok,
            'failed_jdds': failed_jdds,
            'failed_time': failed_time_jdds,
            'failed_browser': failed_browser_jdds}


def print_summary(nb_used, excluded, summary):
    '''Print the summary of the parsing, especially lists of failed and
    excluded files.
    '''
    print("Jdds well passed:", summary['jdds_ok'], "/", nb_used)
    print("Failed jdds:")
    for ifile in summary['failed_jdds']:
        print(str(ifile))
    print("Excluded files:")
    for ifile in excluded:
        print(str(ifile))
    if summary['failed_time']:
        print(f"Jdds where times check failed: {len(summary['failed_time'])}")
        for ifile in summary['failed_time']:
            print(str(ifile))
    if summary['failed_browser']:
        print(f"Jdds where browser failed: {len(summary['failed_browser'])}")
        for ifile in summary['failed_browser']:
            print(str(ifile))


Params = namedtuple('Params', ['used_files', 'excluded_files',
                               'category', 'mode', 'norm_end'])


def params_by_file(path):
    '''Returns parameters (files to use, excluded ones, category, mode, ...)
    for listings read by files (1 test by file).

    :param pathlib.Path path: path to file
    :rType: Params
    '''
    params = Params(used_files=[path], excluded_files=[],
                    category=path.parts[-4], mode=path.parts[-6],
                    norm_end=True)
    return params


def params_evol(path, excluded_patterns):
    '''Returns parameters (files to use, excluded ones, category, mode, ...)
    for depletion listings.

    :param pathlib.Path path: path to folder
    :param list excluded_patterns: list of excluded patterns
    :rType: Params
    '''
    cases = [x for x in path.iterdir() if x.is_dir()]
    excl_cases = [case for case in cases
                  if any(pat in case.name for pat in excluded_patterns)]
    used_cases = list(filter(lambda x: x not in excl_cases, cases))
    all_files = []
    for case in used_cases:
        max_res = max(int(x.name.split('_')[-1])
                      for x in (path/case.name).iterdir()
                      if x.is_dir() and '_' in x.name)
        all_files.extend((path/case.name/f"result_{max_res}").glob("*t4*"))
    used_files = all_files
    params = Params(used_files=used_files, excluded_files=excl_cases,
                    category=all_files[0].parts[-5],
                    mode=all_files[0].parts[-7],
                    norm_end=False)
    return params


def params_by_folder(path, excluded_patterns, excluded_strings):
    '''Returns parameters (files to use, excluded ones, category, mode, ...)
    for listings read by folder.

    :param pathlib.Path path: path to folder
    :param list excluded_patterns: list of excluded patterns
    :param list excluded_strings: list of excluded strings
    :rType: Params
    '''
    all_files = sorted(itertools.chain.from_iterable(
        list(path.glob(f"{x.name}/*.res.{x.name}"))
        for x in path.iterdir() if x.is_dir()))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil.name for pat in excluded_patterns)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    excluded_files = [fil for fil in excluded_files
                      if not any(pat in fil.name for pat in excluded_strings)]
    params = Params(used_files=used_files, excluded_files=excluded_files,
                    category=all_files[0].parts[-4],
                    mode=all_files[0].parts[-6],
                    norm_end=True)
    return params


@pytest.mark.slow
def test_listing_parsing(caplog, vv_params, parsing_exclude, parsing_match):
    '''Test parsing of files configured from the ``--parsing-config-file-t4``
    option.

    By default all files are included, independent of the mode (MONO or PARA),
    and of the report section (main or aux). Restrictions are possible from
    command line, via options ``'--parsing-exclude=spam,egg`` and
    ``'--parsing-match=bacon`` (comma separated strings in both case meaning
    logical OR).
    Currently adapted to version 11 of Tripoli-4.

    Tests performed on number of input files used, excluded and failed.
    '''
    caplog.set_level(logging.WARNING, logger='valjean')
    vv_folder, vv_file = vv_params
    skip_parsing_files(vv_folder, parsing_exclude, parsing_match)
    folder = (vv_folder.parent if vv_file.PER_FILE
              else pathlib.Path(vv_file.PATH) / vv_folder / vv_file.OUTPUTS)
    excluded_patterns = (
        vv_file.EXCLUDED_STRINGS_MONO + vv_file.EXCLUDED_STRINGS
        if vv_file.MONO in folder.parts
        else vv_file.EXCLUDED_STRINGS_PARA + vv_file.EXCLUDED_STRINGS)
    if vv_file.PER_FILE:
        skip_excluded_files(vv_folder, excluded_patterns)
        params = params_by_file(vv_folder)
    else:
        if "EVOL" in folder.parts:
            params = params_evol(folder, excluded_patterns)
        else:
            params = params_by_folder(folder, excluded_patterns,
                                      vv_file.EXCLUDED_STRINGS)
    summary = loop_on_files(params.used_files, params.norm_end)
    if not vv_file.PER_FILE:
        print_summary(len(params.used_files), params.excluded_files, summary)

    counts = vv_file.EXPECTED_RESULTS.get((params.category, params.mode), None)
    if counts is not None:
        assert len(params.used_files) == counts[0]
        assert len(summary['failed_jdds']) == counts[1]
        assert len(params.excluded_files) == counts[2]
        if len(counts) > 3:
            assert len(summary['failed_time']) == counts[3]
            assert len(summary['failed_browser']) == counts[4]
    if vv_file.PER_FILE:
        assert len(summary['failed_jdds']) == 0
        assert len(summary['failed_browser']) == 0
        print('failed time:', summary['failed_time'])
