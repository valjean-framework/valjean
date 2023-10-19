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

'''Tests errors for the modules :mod:`~.scan` and :mod:`~.parse` from
Tripoli-4 :mod:`~.eponine` package.
'''

from ...context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
import logging
import pytest
from valjean.eponine.tripoli4.parse import Parser, ParserException
from valjean.eponine.tripoli4.parse_debug import ParserDebug


def test_empty_file(caplog):
    '''Test Tripoli-4 parsing on an empty file: this should fail.'''
    with open('empty_file.txt', 'w', encoding='utf-8') as ofile:
        ofile.write("")
    with pytest.raises(ParserException):
        Parser('empty_file.txt')
    assert ("No result found in Tripoli-4 listing empty_file.txt"
            in caplog.text)


def test_no_usual_output(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_segFault.d.res as example of
    "failed" jobs: response required in a neutron flux from a neutron source
    while the particles tracked are photons, so Tripoli-4 fails at execution.
    '''
    tfile = str(datadir/"failure_test_segFault.d.res")
    with pytest.raises(ParserException):
        Parser(tfile)
    assert f"No result found in Tripoli-4 listing {tfile}" in caplog.text
    assert "FATAL ERROR" in caplog.text
    assert "error message" in caplog.text


def test_no_a_t4_opt_no_spectrum(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_spec_res.d.res as example of
    parsing failure due to lack of option '-a'. In that case all the intervals
    in the spectrum are at 0, so without option '-a', none of them appears in
    the output. Parsing succeeds to parse the spectrum columns (and units here)
    but fails after as it cannot find any row from the spectrum.
    '''
    t4p = Parser(str(datadir/"failure_test_no_spec_res.d.res"))
    with pytest.raises(ParserException):
        t4p.parse_from_index(batch_index=-1)
    assert ("Parsing error in spectrum (_spectrumvals), "
            "please check you run Tripoli-4 with '-a' option"
            in caplog.text)


def test_no_a_t4_opt_bad_bins(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_a_opt.d.res as example of
    parsing failure due to lack of option '-a'. In this case the spectrum is
    partially filled but filled bins are not adjacent, they are inconsistent
    (no possibility for example to guess bin width, if spectrum was also in
    time for example an new energy bin could appear in the next time step). A
    specific error is sent.
    '''
    t4p = Parser(str(datadir/"failure_test_no_a_opt.d.res"))
    with pytest.raises(ParserException):
        t4p.parse_from_index(-1)
    assert ("Problem with energy bins: some bins are probably missing. "
            "Please make sure you run Tripoli-4 with '-a' option."
            in caplog.text)


def test_no_a_t4_opt_bad_bins_2(datadir, caplog):
    '''Use Tripoli-4 result from failure_noaopt_uniform_sources.d.res as
    example of parsing failure due to lack of option '-a'. In this case the
    spectrum is partially filled: bins are adjacent, but as the spectrum is in
    (*E*, *t*), the number of filled energy bins in the second time step being
    higher than in the first one, we get missing bins in the second step due to
    the use of '-a' optoin. A specific error is sent.
    '''
    t4p = Parser(str(datadir/"failure_noaopt_uniform_sources.d.res"))
    with pytest.raises(ParserException):
        t4p.parse_from_index(-1)
    assert ("IndexError: all (sub-)spectra should have the same bins."
            in caplog.text)
    assert ("Please make sure you run Tripoli-4 with option '-a'."
            in caplog.text)


def test_tungstene_missing_vals(datadir, caplog):
    '''Use Tripoli-4 output from tungstene.d to test meshes (also depending on
    energy).
    '''
    t4p = Parser(str(datadir/"tungstene_missing_vals.d.res"))
    assert t4p
    assert t4p.scan_res.normalend
    with pytest.raises(ParserException):
        t4p.parse_from_index(-1)
    assert "Mesh looks incomplete" in caplog.text


def test_bad_response_name(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_bad_resp_name.d.res as example of
    failing parsing. In this case a not foreseen character, @, has been used in
    a response name. Pyparsing does not know to do with it and fails.
    '''
    t4p = Parser(str(datadir/"failure_test_bad_resp_name.d.res"))
    with pytest.raises(ParserException):
        t4p.parse_from_index(-1)
    assert "Parsing error located at line: 12, col: 1" in caplog.text


def test_no_normal_completion(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_normal_completion.d.res as
    example of lack of "NORMAL COMPLETION" in the output.

    In this case parsing is successful: its result exists, but the
    ``normalend`` boolean in scan is ``False``.
    '''
    t4p = Parser(str(datadir/"failure_test_no_normal_completion.d.res"))
    assert t4p
    assert ("Tripoli-4 listing did not finish with NORMAL COMPLETION."
            in caplog.text)
    assert t4p.scan_res.normalend is False
    assert t4p.scan_res.partial is True
    t4_res = t4p.parse_from_index(-1, name='bad end')
    assert t4_res.res['batch_data']['batch_number'] == 37
    assert t4_res.res['batch_data']['name'] == 'bad end'
    t4rb = t4_res.to_browser()
    assert not t4rb.is_empty()
    assert len(t4rb.globals) == 5
    assert len(t4rb) == 1


def test_no_simulation_time(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_simu_time.d.res as example of
    lack of the end flag. In this case "NORMAL COMPLETION" is also missing but
    as pyparsing cannot find the end flag no parsing result can be built.
    '''
    with pytest.raises(ParserException):
        Parser(str(datadir/"failure_test_no_simu_time.d.res"))
    assert "No scan result built: no end flag found in the file" in caplog.text


def test_no_simulation_time_debug(datadir, caplog):
    '''Use Tripoli-4 result from failure_test_no_simu_time.d.res as example of
    lack of the end flag. In this case "NORMAL COMPLETION" is also missing but
    as pyparsing cannot find the end flag no parsing result can be built.
    '''
    with caplog.at_level(logging.DEBUG, 'valjean'):
        t4p = ParserDebug(str(datadir/"failure_test_no_simu_time.d.res"),
                          end_flag='ENERGY INTEGRATED RESULTS')
        _t4_res = t4p.parse_from_index(-1)
        assert ('No "time" variable found in the Tripoli-4 output, '
                'please check it.' in caplog.text)
        assert ('Remark: you are in parsing debug mode with an end flag not '
                'containing "time", this is expected.' in caplog.text)
        _t4_res.to_browser()
