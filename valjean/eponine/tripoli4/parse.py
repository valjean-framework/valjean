'''Module performing scanning and parsing of Tripoli-4 outputs.

This module also allows quick checks on outputs:

* presence of ``"NORMAL COMPLETION"``
* presence and values of times (simulation, exploitation)

Some options for debugging are available (end flag).

.. todo::

   Change absolute imports in relative ones when main will be moved to
   :ref:`cambronne <cambronne-main>`.
'''

import time
import logging
from pyparsing import ParseException

from . import scan
from .grammar import t4gram
from .common import SpectrumDictBuilderException


LOGGER = logging.getLogger('valjean')

# in Eponine, profile is a key of globals
if 'profile' not in globals()['__builtins__']:
    def profile(fprof):
        '''To profile memory usage.'''
        return fprof


class T4ParserException(Exception):
    '''An error that may be raised by the :class:`T4Parser` class.'''


class T4Parser():
    '''Scan Tripoli-4 listings, then parse the required batches.'''

    @profile
    def __init__(self, jddname, batch=-1, *, mesh_lim=-1):
        '''Initialize the :class:`T4Parser` object.

        :param str jddname: path to the Tripoli-4 output
        :param int batch: batch to read (-1 = last, 0 = all, then X)
        :param int mesh_lim: limit of meshes to read (-1 per default)

        It also initalize the result of :class:`.scan.Scan` to ``None`` and
        the parsing result, from *pyparsing*, to ``None``.

        If the path contains the ``"PARA"`` string, the checks will be done for
        parallel mode.

        The T4Parser object instance variables are:

        `scan_res` (:class:`~.scan.Scan`)
            result from the scan of the Tripoli-4 output. See in the related
            documentation the various instance variables available (like
            ``times``). Inheriting from :class:`collections.abc.Mapping`
            various default methods are available like ``len``, ``[]``, etc.
            The keys of :class:`~.scan.Scan` are the batch numbers available
            from the Tripoli-4 output. To get their list, use the ``keys``
            method.

        `result` (:class:`list` (:class:`dict`))
            stores the result from *pyparsing*. Each item of the list (most
            external one) corresponds to a batch, i.e. to all results available
            for that batch.

        This class takes care of the scanning of the Tripoli-4 output, then of
        its parsing if the first step was successful. If one of these steps
        fails, exceptions will be raised.
        '''
        LOGGER.info("Parsing %s (batch %d)", jddname, batch)
        start_time = time.time()
        self.jdd = jddname
        self.batch_number = batch
        self.mesh_limit = mesh_lim
        self.scan_res = None
        self.result = None
        self.para = "PARA" in jddname or "th_task" in jddname
        try:
            self.scan_then_parse(start_time)
        except T4ParserException as t4pe:
            LOGGER.error(t4pe)
            raise T4ParserException("Scanning or parsing failed.") from None

    def scan_then_parse(self, start_time):
        '''Scan the parse the given jdd.'''
        self.scan_t4_listing()
        self.check_t4_scan()
        LOGGER.info("Successful scan in %f s", time.time()-start_time)
        start_parse = time.time()
        self.parse_t4_listing()
        LOGGER.info("Successful parsing in %f s", time.time()-start_parse)
        LOGGER.info("Time (scan + parse) = %f s", time.time()-start_time)

    @profile
    def scan_t4_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.'''
        self.scan_res = scan.Scan(self.jdd, self.mesh_limit, self.para)

    def check_t4_scan(self):
        '''Check existence of scan result and presence of normal end (per
        default NORMAL COMPLETION).
        '''
        if not self.scan_res:
            raise T4ParserException("No result found in Tripoli-4 listing.")
        if not self.scan_res.normalend:
            LOGGER.warning("Tripoli-4 listing did not finish with "
                           "NORMAL COMPLETION.")

    def _str_to_parse(self):
        '''Return string to parse (depends on the required batches).

        :returns: str
        '''
        if self.batch_number == 0:
            return self.scan_res.get_all_batch_results()
        return self.scan_res[self.batch_number]

    def parse_t4_listing(self):
        '''Parse Tripoli-4 results, calling pyparsing and
        :mod:`~valjean.eponine.tripoli4`. Use the default grammar.
        '''
        self._parse_t4_listing_worker(t4gram, self._str_to_parse())

    def _parse_t4_listing_worker(self, gram, str_to_parse):
        '''Parse the given string and raise exception if parsing failed.'''
        try:
            self.result = gram.parseString(str_to_parse).asList()
        except ParseException:
            LOGGER.error("Parsing failed, you are probably trying to read a "
                         "new response. Please update the parser before "
                         "re-running.")
            # from None allows to raise a new exception without traceback and
            # message of the previous one here.
            raise T4ParserException("Error in parsing") from None
        except SpectrumDictBuilderException as sdbe:
            LOGGER.error(sdbe)
            raise T4ParserException("Error in parsing") from None

    def print_t4_stats(self):
        '''Print Tripoli-4 statistics (warnings and errors).'''
        self.scan_res.print_statistics()

    def check_t4_times(self):
        '''Check if running times are well written in Tripoli-4 listings.
        These times are at the end of the result block and mark the end flag.

        :returns: boolean, True if well present, else False

        Returned bool depends on the listing:

        * if the job was run in parallel mode (and declared so),
          ``"simulation time"`` and ``"elapsed time"`` should be present in
          that order, only the second one is checked
        * if the listing name contains ``"exploit"`` or ``"verif"``, it is most
          probably an exploitation job (Green bands for example),
          ``"exploitation time"`` is checked
        * else ``"simulation time"`` is checked
        '''
        result = ((self.para and 'elapsed time' in self.scan_res.times
                   and 'simulation time' in self.scan_res.times)
                  or (not self.para
                      and ('simulation time' in self.scan_res.times
                           or 'exploitation time' in self.scan_res.times)))
        LOGGER.debug('scan_res.times: %s', self.scan_res.times)
        LOGGER.debug('check_t4_times() returns: %s', result)
        return result

    def print_t4_times(self):
        '''Print time characteristics of the Tripoli-4 result considered.
        This print includes initialization time, simulation time, exploitation
        time and elapsed time.
        '''
        for stime, vtime in self.scan_res.times.items():
            print(stime.capitalize(), "=", vtime)
