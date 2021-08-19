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
import os
from glob import glob
import logging
import pytest
from valjean.eponine.tripoli4.parse import Parser, ParserException
import valjean.eponine.tripoli4.data_convertor as dcv
from ...context import valjean  # noqa: F401, pylint: disable=unused-import
from ..conftest import skip_parsing_files


def result_test(t4pres):
    '''Test content of the parsing result: presence of times, ``'results'`` key
    if ``'list_responses'`` is found in the parsing result.

    :param res: ParseResult

    :retrns: bool if time was found (but should always happen as there is an
             assert before)
    '''
    # get last result (default returns list if more than one batch required)
    # elapsed_time needed for cases with PARTIAL EDITION (not correct end)
    assert any("_time" in s for s in t4pres.res['batch_data'].keys())
    print("keys =", list(t4pres.res.keys()))
    if 'list_responses' in t4pres.res.keys():
        lresp = t4pres.res['list_responses']
        assert isinstance(lresp, list)
        for resp in lresp:
            assert 'results' in resp
            assert isinstance(resp['results'], dict)
            assert isinstance(resp['response_type'], str)
    return t4pres.res['run_data']['normal_end']


def check_array_datasets(response, dname, data):
    '''Check datasets for arrays.

    This function is mainly meant to deal with the spectrum special cases as
    spectra containing variance of variance or uncertainty spectra (subcase of
    perturbations, old way). Related integrated results are also checked in
    these special cases.
    '''
    if dname == 'uncert_spectrum':
        for elt in data['array'].dtype.names:
            assert dcv.convert_data(response['results'], dname, score=elt)
    elif dname == 'uncert_integrated':
        for elt in data:
            assert dcv.convert_data(data, elt)
    else:
        if isinstance(data, dict) and 'array' in data:
            for akey in data:
                if 'array' not in akey:
                    continue
                assert dcv.convert_data(response['results'], dname,
                                        array_type=akey)
        else:
            assert dcv.convert_data(response['results'], dname)
    if dname == 'spectrum' and 'vov' in data['array'].dtype.names:
        assert dcv.convert_data(response['results'], dname, score='vov')
    if 'integrated' in dname and 'vov' in data:
        assert dcv.convert_data(data, 'vov')
    if 'best_result' in dname and 'discarded_batches' in data:
        assert dcv.convert_data(data, 'discarded_batches')


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
            if isinstance(data, str):
                continue
            if iresp['response_type'] == 'score':
                check_array_datasets(iresp, dname, data)
            else:
                assert dcv.convert_data(iresp['results'], dname)


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
    failed_jdds, failed_time_jdds, failed_browser_jdds = [], [], []
    for ifile in filelist:
        print("Reading:", ifile)
        try:
            res = (Parser(ifile)
                   if os.path.basename(ifile) not in cfile.MESH_LIM_FILES
                   else Parser(ifile, mesh_lim=2))
        except ParserException:
            failed_jdds.append(ifile)
            continue
        if not res.check_times():
            print("Issue with times, please check")
            failed_time_jdds.append(ifile)
        try:
            pres = res.parse_from_index(-1)
        except ParserException:
            failed_jdds.append(ifile)
            continue
        if result_test(pres):
            nb_jdds_ok += 1
        else:
            failed_jdds.append(ifile)
        try:
            browser_test(pres)
        except AssertionError as aerb:
            print("Error in browser: {}".format(aerb))
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
        print(ifile)
    print("Excluded files:")
    for ifile in excluded:
        print(ifile)
    if summary['failed_time']:
        print("Jdds where times check failed: {}"
              .format(len(summary['failed_time'])))
        for ifile in summary['failed_time']:
            print(ifile)
    if summary['failed_browser']:
        print("Jdds where browser failed: {}"
              .format(len(summary['failed_browser'])))
        for ifile in summary['failed_browser']:
            print(ifile)


@pytest.mark.slow
def test_listing_parsing(caplog, vv_params, parsing_exclude, parsing_match):
    '''Test parsing of files configured from the ``--parsing-config-file``
    option.

    By default all files are included, independent of the mode (MONO or PARA),
    and of the report section (main or aux). Restrictions are possible from
    command line, via options ``'--parsing-exclude='["spam", "egg"]'`` and
    ``'--parsing-match='["bacon"]'``.
    Currently adapted to version 11 of Tripoli-4.

    Tests performed on number of input files used, excluded and failed.
    '''
    caplog.set_level(logging.WARNING, logger='valjean')
    vv_folder, vv_file = vv_params
    skip_parsing_files(vv_folder, parsing_exclude, parsing_match)
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
    summary = loop_on_files(used_files, vv_file)
    print_summary(len(used_files), excluded_files, summary)
    category = used_files[0].split('/')[-4]
    mode = vv_file.MONO if vv_file.MONO in folder else vv_file.PARA

    counts = vv_file.EXPECTED_RESULTS.get((category, mode), None)
    if counts is None:
        return

    assert len(used_files) == counts[0]
    assert len(summary['failed_jdds']) == counts[1]
    assert len(excluded_files) == counts[2]
    if len(counts) > 3:
        assert len(summary['failed_time']) == counts[3]
        assert len(summary['failed_browser']) == counts[4]
