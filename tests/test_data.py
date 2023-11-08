# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
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

'''Tests if all paths have been removed from data files like Tripoli4 outputs
in eponine data folder and in notebooks.'''

import re
from pprint import pformat
import pytest
from valjean import LOGGER


FORBIDDEN_PATH = (r'((?<!\w|\.|\/|\)|`|\'|\}|!|<|\+)'
                  r'(\/(?!path)((\\\b)|[^ \b%\|*:\n\"\\\/])+)'
                  r'+\/?(?<!\*))')
FORBIDDEN_STR = r'\s[a-zA-Z]{2}[0-9]{6}\s'
CPATH = re.compile(FORBIDDEN_PATH)
CSTR = re.compile(FORBIDDEN_STR)
FORBIDDEN_PATTERNS = re.compile(f'({FORBIDDEN_PATH})|({FORBIDDEN_STR})')


@pytest.fixture(params=['tests/eponine/tripoli4/data', 'doc/src/examples'])
def list_t4_datafiles(request, pytestconfig):
    '''List Tripoli4 output files in the given folder'''
    folder = pytestconfig.rootpath / request.param
    flist = list(folder.glob('**/*.res*'))
    flist.extend(f for f in folder.glob('**/*.ipynb')
                 if "ipynb_checkpoints" not in str(f))
    flist.extend(folder.glob('**/*.rst'))
    flist.extend(folder.glob('**/*.md'))
    flist.extend(folder.glob('**/*.py'))
    return flist


def contains_forbidden_patterns(lfile):
    '''Find a path in the file (or not)

    :param str lfile: name of the file to scan
    :returns: ``True`` if the file contains one of the forbidden pattern,
        ``False`` otherwise
    '''
    dfpat = {}
    with open(lfile, 'r', encoding='utf-8', errors='ignore') as rfile:
        for iline, line in enumerate(rfile.readlines()):
            if re.search(FORBIDDEN_PATTERNS, line):
                dfpat[iline] = line[:-1]
    if dfpat:
        LOGGER.warning('Forbidden pattern found in %s (line: string):\n%s',
                       lfile, pformat(dfpat))
        return True
    return False


def executed_notebook(lfile):
    '''Find if a notebook is executed.

    :param str lfile: name of the file to scan (only .ipynb considered)
    :returns: ``True`` if the file is executed, ``False`` otherwise
    '''
    with open(lfile, 'r', encoding='utf-8', errors='ignore') as rfile:
        for line in rfile.readlines():
            matches = re.findall(r'   "execution_count": (\w+?),', line)
            if matches and matches[0].isdigit():
                LOGGER.warning('Executed notebook: %s', lfile)
                return True
    return False


def test_t4_eponine_data(list_t4_datafiles):
    '''Test if there are paths in Tripoli4 outputs in eponine.tripoli4.data.'''
    failed_files = []
    for tfile in list_t4_datafiles:
        if contains_forbidden_patterns(tfile):
            failed_files.append(tfile)
        if tfile.suffix == ".ipynb" and executed_notebook(tfile):
            failed_files.append(tfile)
    if failed_files:
        LOGGER.warning("Failed files:\n%s", pformat(failed_files))
    assert not failed_files
