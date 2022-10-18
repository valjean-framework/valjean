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
from ...context import valjean  # noqa: F401, pylint: disable=unused-import
# pylint: disable=wrong-import-order
import itertools
import pathlib
import pytest
root = pytest.importorskip('ROOT')
# pylint: disable=wrong-import-position
from valjean.eponine.tripoli4.depletion import DepletionReader  # noqa: E402
from ..conftest import skip_parsing_files  # noqa: E402


@pytest.mark.slow
def test_depletion_files(vv_params, parsing_exclude, parsing_match,
                         tmp_path_factory):
    '''Quick test of depletion ROOT files (chained).'''
    root_dir = tmp_path_factory.mktemp('t4depletion')
    vv_folder, vv_file = vv_params
    if parsing_exclude:
        parsing_exclude = (f"{parsing_exclude},"
                           f"{','.join(vv_file.EXCLUDED_STRINGS_EVOL)}")
    else:
        parsing_exclude = ','.join(vv_file.EXCLUDED_STRINGS_EVOL)
    skip_parsing_files(vv_folder, parsing_exclude, parsing_match)
    folder = (vv_folder.parent if vv_file.PER_FILE
              else pathlib.Path(vv_file.PATH) / vv_folder / vv_file.OUTPUTS)
    excluded_patterns = (vv_file.EXCLUDED_STRINGS
                         + vv_file.EXCLUDED_STRINGS_EVOL)
    path = pathlib.Path(folder)
    cases = [x for x in path.iterdir()
             if x.is_dir() and x.name not in excluded_patterns]
    for case in cases:
        print(f"Case: {case}")
        max_res = max(int(x.name.split('_')[-1])
                      for x in (path/case.name).iterdir()
                      if x.is_dir() and '_' in x.name)
        root_files = list(itertools.chain.from_iterable(
            (path.glob(f"{case.name}/result_{i}/evolution.root"))
            for i in range(1, max_res+1)))
        depr = DepletionReader.from_evolution_steps(
            *[str(rfile) for rfile in root_files], root_build=str(root_dir))
        assert depr
        assert depr.nb_simu() == max_res
        assert depr.burnup_array().ndim == 1
        assert depr.time_array().size == depr.burnup_array().size
        # pylint: disable=no-member
        assert depr.kstep_burnup().size == depr.burnup_array().size
