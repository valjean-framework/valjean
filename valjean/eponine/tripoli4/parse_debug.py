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

'''Extension of :mod:`~.parse` module for debugging.

Main difference is the possibility of using the ``end_flag`` parameter in the
:mod:`~.scan`.
'''

import logging

from .parse import Parser, ParseResult, ParserException
from . import scan
from .grammar import t4debug_gram
from ...chrono import Chrono


LOGGER = logging.getLogger(__name__)


class ParserDebug(Parser):
    '''Scan up to the end flag then parse. For parsing debugging.'''

    def __init__(self, jddname, *, end_flag="", ofile=""):
        '''Initialize the :class:`ParserDebug` object.

        :param str jddname: path to the Tripoli-4 output
        :param int batch: batch to read (-1 = last, 0 = all, then X)
        :param str end_flag: optional end flag to stop scanning and parsing
                             (empty string per default)

        It also initalize the result of :class:`.scan.Scanner` to ``None`` and
        the parsing result, from *pyparsing*, to ``None``.

        If the path contains the ``"PARA"`` string, the checks will be done for
        parallel mode.
        '''
        self.end_flag = end_flag
        self.ofile = ofile
        super().__init__(jddname)

    def _scan_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.'''
        return scan.Scanner(self.jdd, self.end_flag)

    def parse_from_number(self, batch_number, name=''):
        '''Parse from batch index or batch number.

        Per default the last batch is parsed (index = -1).

        :param int batch_number: the number of the batch to parse
        :returns: list(dict)
        '''
        LOGGER.debug('Using parse from ParserDebug')
        with Chrono() as chrono:
            batch_edition = self.scan_res[batch_number]
            if LOGGER.isEnabledFor(logging.DEBUG) and self.ofile:
                with open(self.ofile, 'w', encoding='utf-8') as fout:
                    fout.write(batch_edition)
            pres, = self._parse_listing_worker(
                t4debug_gram, self.scan_res[batch_number])
        LOGGER.info("Successful parsing in %f s", chrono)
        self.check_parsing(pres)
        try:
            self._time_consistency(pres, batch_number)
        except ParserException as tcve:
            if not self.end_flag:
                raise ParserException(tcve) from None
            LOGGER.info(tcve)
            LOGGER.info('Remark: you are in parsing debug mode with an end '
                        'flag not containing "time", this is expected.')
        scan_vars = self.scan_res.global_variables(batch_number)
        return ParseResult(pres, scan_vars, name=name)

    def check_parsing(self, parsed_res):
        '''Check if parsing went to the end:

        * if the end flag was not precised, a time should appear in the last
          result;
        * if not, no check can be performed as the end flag can be anywhere,
          even "transformed" during parsing.

        Print a logger message if not found but don't block access to the
        parsing result (this can help to find the issue).
        '''
        if not self.end_flag:
            if not any("_time" in s for s in parsed_res['batch_data']):
                LOGGER.error("Time not found in the parsing result, "
                             "parsing probably stopped before end, "
                             "please check.")
        if self.end_flag:
            LOGGER.info("You are running with an end flag ('%s'), "
                        "no automatic check of correct end of parsing is "
                        "currently available in that case, "
                        "please check carefully.", self.end_flag)
