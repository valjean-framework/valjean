'''Extension of :mod:`~.parse` module for debugging.

Main difference is the possibility of using the ``end_flag`` parameter in the
:mod:`~.scan`.
'''

import time
import logging

from .parse import T4Parser, T4ParseResult, T4ParserException
from . import scan
from .grammar import t4debug_gram


LOGGER = logging.getLogger('valjean')


class T4ParserDebug(T4Parser):
    '''Scan up to the end flag then parse. For parsing debugging.'''

    def __init__(self, jddname, *, mesh_lim=-1, end_flag="", ofile=""):
        # pylint: disable=too-many-arguments
        '''Initialize the :class:`T4ParserDebug` object.

        :param str jddname: path to the Tripoli-4 output
        :param int batch: batch to read (-1 = last, 0 = all, then X)
        :param int mesh_lim: limit of meshes to read (-1 per default)
        :param str end_flag: optional end flag to stop scanning and parsing
                             (empty string per default)

        It also initalize the result of :class:`.scan.T4Scan` to ``None`` and
        the parsing result, from *pyparsing*, to ``None``.

        If the path contains the ``"PARA"`` string, the checks will be done for
        parallel mode.
        '''
        self.end_flag = end_flag
        self.ofile = ofile
        super().__init__(jddname, mesh_lim=mesh_lim)

    def _scan_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.'''
        self.scan_res = scan.T4Scan(self.jdd, self.mesh_limit, self.end_flag)

    def parse_from_number(self, batch_number):
        '''Parse from batch index or batch number.

        Per default the last batch is parsed (index = -1).

        :param int batch_number: the number of the batch to parse
        :returns: list(dict)
        '''
        LOGGER.debug('Using parse from T4ParserDebug')
        start_time = time.time()
        batch_edition = self.scan_res[batch_number]
        if LOGGER.isEnabledFor(logging.DEBUG) and self.ofile:
            with open(self.ofile, 'w') as fout:
                fout.write(batch_edition)
        pres, = self._parse_listing_worker(
            t4debug_gram, self.scan_res[batch_number])
        LOGGER.info("Successful parsing in %f s", time.time()-start_time)
        self.check_parsing(pres)
        try:
            self._time_consistency(pres, batch_number)
        except T4ParserException as tcve:
            if not self.end_flag:
                raise T4ParserException(tcve) from None
            LOGGER.info(tcve)
            LOGGER.info('Remark: you are in parsing debug mode with an end '
                        'flag not containing "time", this is expected.')
        scan_vars = self.scan_res.global_variables(batch_number)
        return T4ParseResult(pres, scan_vars)

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
