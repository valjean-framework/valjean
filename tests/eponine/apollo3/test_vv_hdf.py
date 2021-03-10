'''Test parsing of all listings contained in the selected folders from
``--parsing-config-file-ap3`` option.

Exclusion and matching are possible via ``--parsing-exclude`` and
``--parsing-match`` options.


Expected variables in the configuration file are:
  * PATH: path to the folder containing the scanned folder structure
  * ALL_FOLDERS: folders structures. In Apollo3 VV case, in most of the cases
    the folder name is the ``basename`` of the hdf file, i.e. ``'case_name'``
    if ``'case_name.hdf'``.
  * END_FILES: common file extension (like ``hdf``)
  * EXCLUDED_STRINGS: strings excluded from case names (to avoid too long ones
    for example)
'''
import os
from glob import glob
import logging
import pytest
from valjean.eponine.apollo3.hdf5_reader import Reader
from ...context import valjean  # noqa: F401, pylint: disable=unused-import
from ..conftest import skip_parsing_files


def loop_on_files(filelist):
    '''Perform the loop over the file list, parse all of them and returns
    result of this parsing.

    :param list filelist: list of paths to the files to be read and parsed
    '''
    for ifile in filelist:
        print("Reading:", ifile)
        ap3r = Reader(ifile)
        assert ap3r.res
        ap3b = ap3r.to_browser()
        assert ap3b
        assert len(ap3b.content) == sum(len(res) for res in ap3r.res.values())
        assert {'info', 'geometry'} == ap3b.globals.keys()
        if 'zone' in ap3b.keys():
            assert ap3b.globals['info']
            assert ap3b.globals['geometry']
            assert len(ap3b.globals['info']) == len(ap3r.res)
            assert (len(ap3b.globals['info'])
                    == len(ap3b.available_values('output')))
        else:
            assert not ap3b.globals['info']
            assert not ap3b.globals['geometry']


@pytest.mark.slow
def test_apollo3_hdf(caplog, vv_params, parsing_exclude, parsing_match):
    '''Test reading of files configured from the ``--parsing-config-file``
    option.

    By default all files are included. Restrictions are possible from command
    line, via options ``'--parsing-exclude='["spam", "egg"]'`` and
    ``'--parsing-match='["bacon"]'``.

    Tests performed on number of input files used, excluded and failed.
    '''
    caplog.set_level(logging.WARNING, logger='valjean')
    vv_folder, vv_file = vv_params
    skip_parsing_files(vv_folder, parsing_exclude, parsing_match)
    folder = os.path.join(vv_file.PATH, vv_folder)
    all_files = sorted(glob(os.path.join(folder, "*."+vv_file.END_FILES)))
    excluded_patterns = vv_file.EXCLUDED_STRINGS
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in excluded_patterns)]
    used_files = [x for x in all_files if x not in excluded_files]
    loop_on_files(used_files)
