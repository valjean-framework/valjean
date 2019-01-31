'''Extension of :mod:`~.parse` module for debugging.

Main difference is the possibility of using the ``end_flag`` parameter in the
:mod:`~.scan`.
'''

import time
import logging

from .parse import T4Parser, T4ParserException
from . import scan
from .grammar import t4debug_gram


LOGGER = logging.getLogger('valjean')


class T4ParserDebug(T4Parser):
    '''Scan up to the end flag then parse. For parsing debugging.'''

    def __init__(self, jddname, batch=-1, mesh_lim=-1, end_flag="", ofile=""):
        # pylint: disable=too-many-arguments
        '''Initialize the :class:`T4ParserDebug` object.

        :param str jddname: path to the Tripoli-4 output
        :param int batch: batch to read (-1 = last, 0 = all, then X)
        :param int mesh_lim: limit of meshes to read (-1 per default)
        :param str end_flag: optional end flag to stop scanning and parsing
                             (empty string per default)

        It also initalize the result of :class:`.scan.Scan` to ``None`` and
        the parsing result, from *pyparsing*, to ``None``.

        If the path contains the ``"PARA"`` string, the checks will be done for
        parallel mode.
        '''
        super().__init__(jddname, batch, mesh_lim)
        self.end_flag = end_flag
        self.ofile = ofile

    @classmethod
    def parse_debug(cls, jdd, batch, mesh_lim=-1, end_flag="", ofile=""):
        # pylint: disable=too-many-arguments
        '''Constructor for T4ParserDebug for cases where a limit on meshes can
        be set. It is also possible, for debug cases, to put a user's end flag.
        Scanning and parsing are automatically done.

        :param str jdd: path to the output from Tripoli-4
        :param int batch: number of the batch to parse (-1 = last one
                          (*default*), 0 = all of them, X > 0 = batch X to be
                          parsed)
        :param int mesh_lim: limit on lines of meshes (-1 = all of them,
                             X > 0 = lines kept for each mesh, X = 0 will fail)
        :param str end_flag: optional end flag to stop scanning (and parsing)
        :returns: T4ParserDebug object
        '''
        start_time = time.time()
        parser = cls(jdd, batch, mesh_lim, end_flag, ofile)
        if parser.scan_then_parse(start_time):
            parser.check_t4_parsing()
            return parser
        return None

    def scan_t4_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.'''
        self.scan_res = scan.Scan.debug_scan(self.jdd, self.mesh_limit,
                                             self.para, self.end_flag)
        if not self.scan_res:
            raise T4ParserException("No result found in Tripoli-4 listing.")
        if not self.scan_res.normalend:
            LOGGER.warning("Tripoli-4 listing did not finish with "
                           "NORMAL COMPLETION.")

    def parse_t4_listing(self):
        '''Parse Tripoli-4 results, calling pyparsing and
        :mod:`~valjean.eponine.tripoli4`. Use the debug grammar.

        If debugging is activated in the logger and if an output file is given,
        the string sent to the parser is printed in a file.
        '''
        str_to_parse = self._str_to_parse()
        if LOGGER.isEnabledFor(logging.DEBUG) and self.ofile:
            with open(self.ofile, 'w') as fout:
                fout.write(str_to_parse)
        self._parse_t4_listing_worker(t4debug_gram, str_to_parse)

    def check_t4_parsing(self):
        '''Check if parsing went to the end:

        * if the end flag was not precised, a time should appear in the last
          result;
        * if not, no check can be performed as the end flag can be anywhere,
          even "transformed" during parsing.

        Print a logger message if not found but don't block access to the
        parsing result (this can help to find the issue).
        '''
        if not self.end_flag:
            if not any("_time" in s for s in self.result[-1].keys()):
                LOGGER.error("Time not found in the parsing result, "
                             "parsing probably stopped before end, "
                             "please check.")
        if self.end_flag:
            LOGGER.info("You are running with an end flag ('%s'), "
                        "no automatic check of correct end of parsing is "
                        "currently available in that case, "
                        "please check carefully.", self.end_flag)
