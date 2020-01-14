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
import threading
from pyparsing import ParseException

from . import scan
from .grammar import t4gram
from .common import SpectrumDictBuilderException
from ..response_book import ResponseBook


LOGGER = logging.getLogger('valjean')

PYPARSING_LOCK = threading.RLock()

# in Eponine, profile is a key of globals
if 'profile' not in globals()['__builtins__']:
    def profile(fprof):
        '''To profile memory usage.'''
        return fprof


class T4ParserException(Exception):
    '''An error that may be raised by the :class:`T4Parser` class.'''


class T4Parser:
    '''Scan Tripoli-4 listings, then parse the required batches.'''

    @profile
    def __init__(self, jddname, *, mesh_lim=-1):
        '''Initialize the :class:`T4Parser` object.

        :param str jddname: path to the Tripoli-4 output
        :param int mesh_lim: limit of meshes to read (-1 per default)

        It also initalizes the result of :class:`.scan.T4Scan` to ``None``,
        then executes the scan. If this step fails an exception is raised.

        The T4Parser main object instance variable is:

        `scan_res` (:class:`~.scan.T4Scan`)
            result from the scan of the Tripoli-4 output. See in the related
            documentation the various instance variables available (like
            ``times``). Inheriting from :class:`collections.abc.Mapping`
            various default methods are available like ``len``, ``[]``, etc.
            The keys of :class:`~.scan.T4Scan` are the batch numbers available
            from the Tripoli-4 output. To get their list, use
            :meth:`batch_numbers`.

        Parsing (e.g. :meth:`parse_from_number`) returns a
        :class:`T4ParseResult`.
        '''
        LOGGER.info("Parsing %s", jddname)
        start_time = time.time()
        self.jdd = jddname
        self.mesh_limit = mesh_lim
        self.scan_res = None
        try:
            self._scan(start_time)
        except scan.T4ScanException as t4se:
            LOGGER.error(t4se)
            raise T4ParserException("Scan failed.") from None
        except T4ParserException as t4pe:
            LOGGER.error(t4pe)
            raise T4ParserException("Scan failed.") from None

    def _scan(self, start_time):
        '''Scan the parse the given jdd.'''
        self._scan_listing()
        self._check_scan()
        LOGGER.info("Successful scan in %f s", time.time()-start_time)

    @profile
    def _scan_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.'''
        self.scan_res = scan.T4Scan(self.jdd, self.mesh_limit)

    def _check_scan(self):
        '''Check existence of scan result and presence of normal end (per
        default NORMAL COMPLETION).
        '''
        if not self.scan_res:
            raise T4ParserException(
                "No result found in Tripoli-4 listing.\n{}"
                .format(self.scan_res.fatal_error()))
        if not self.scan_res.normalend:
            LOGGER.warning("Tripoli-4 listing did not finish with "
                           "NORMAL COMPLETION.")

    def batch_numbers(self):
        '''Help method to get the available batch numbers.

        :rtype: list(int)
        '''
        return list(self.scan_res.keys())

    @staticmethod
    def _parse_listing_worker(gram, str_to_parse):
        '''Parse the given string and raise exception if parsing failed.'''
        try:
            with PYPARSING_LOCK:
                result = gram.parseString(str_to_parse).asList()
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
        return result

    def _time_consistency(self, pres, batch_number):
        '''Check time consistency between parsed result and scan.'''
        if 'batch_data' not in pres:
            raise T4ParserException('No batch_data in parsed result, '
                                    'something looks wrong in the T4 output.')
        bdata = pres['batch_data']
        try:
            time_key = next(k for k in bdata if 'time' in k)
        except StopIteration:
            raise T4ParserException(
                'No "time" variable found in the TRIPOLI-4 output, '
                'please check it.')
        if bdata[time_key] != self.scan_res.times[time_key][batch_number]:
            msg = ('{} looks inconsistent between parsing ({}) and scanning '
                   '({})'.format(time_key, bdata[time_key],
                                 self.scan_res.times[time_key][batch_number]))
            if self.scan_res.partial:
                LOGGER.warning(msg)
            else:
                raise T4ParserException(msg)

    def parse_from_number(self, batch_number):
        '''Parse from batch index or batch number.

        :param int batch_number: number of the batch to parse
        :rtype: T4ParseResult
        '''
        LOGGER.debug('Using parse from T4Parser')
        start_parse = time.time()
        pres, = self._parse_listing_worker(
            t4gram, self.scan_res[batch_number])
        LOGGER.info("Successful parsing in %f s", time.time()-start_parse)
        self._time_consistency(pres, batch_number)
        scan_vars = self.scan_res.global_variables(batch_number)
        return T4ParseResult(pres, scan_vars)

    def parse_from_index(self, batch_index=-1):
        '''Parse from batch index or batch number.

        Per default the last batch is parsed (index = -1).

        :param int batch_index: index of the batch in the list of batches
        :rtype: T4ParseResult
        '''
        batch_number = self.scan_res.batch_number(batch_index)
        return self.parse_from_number(batch_number)

    def print_stats(self):
        '''Print Tripoli-4 statistics (warnings and errors).'''
        self.scan_res.print_statistics()

    def check_times(self):
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
        return self.scan_res.check_times()

    def print_times(self):
        '''Print time characteristics of the Tripoli-4 result considered.
        This print includes initialization time, simulation time, exploitation
        time and elapsed time.
        '''
        for stime, vtime in self.scan_res.times.items():
            print(stime.capitalize(), "=", vtime)


class T4ParseResult:
    '''Class containing a parsing result from TRIPOLI-4 output for one batch.


        The :class:`T4ParseResult` object is accessible from the instance
        attribute

        `res`
            that is a unique dictionary containing all the results from
            scanning and parsing steps. Variables characteristic to a batch are
            stored under the key ``'batch_data'`` no matter if they come from
            :class:`.T4Scan` or from :class:`T4Parser`. Variables
            characteristic to a run (= one execution of TRIPOLI-4) are stored
            under ``'run_data'``, coming from the scanning step.

        It is possible to transform the ``res`` dictionary in a
        :class:`~valjean.eponine.response_book.ResponseBook` thanks to the
        method :meth:`to_response_book`.
    '''

    def __init__(self, parse_res, scan_vars):
        '''Initialize the :class:`T4ParseResult` from:

        :param dict parse_res: result from T4 parsing (for 1 batch)
        :param dict scan_vars: variables coming from :class:`.T4Scan` global to
            job or specific to the batch.

        Fill the `res` object.
        '''
        self._check_batch_number(parse_res, scan_vars)
        self.res = self._build_unique_dict(parse_res, scan_vars)

    @staticmethod
    def _check_batch_number(pres, svars):
        '''Check that batch number from scan variables and edition batch number
        if exists are the same, else emit a warning.
        '''
        ebn = pres.get('edition_batch_number')
        sbn = svars.get('batch_number')
        if sbn is None:
            LOGGER.warning('No batch number was set in T4Scan, please check.')
        if ebn is not None and ebn != sbn:
            LOGGER.warning('Edition batch number different from batch number')

    @staticmethod
    def _build_unique_dict(pres, svars):
        '''Build a unique dictionary from parsed result and globl variables
        from T4Scan.

        Variables specific to batch are added to the already existing
        dictionary under the key ``'batch_data'`` from parsed result, while a
        new item is created for the run data (key: ``'run_data'``).

        :param dict pres: parsed result
        :param dict svars: global variables from T4Scan
        :returns: updated parsed result
        '''
        gvars = svars.copy()
        bdata_keys = {'batch_number', 'simulation_time', 'elapsed_time',
                      'exploitation_time'}
        for key in bdata_keys & set(gvars.keys()):
            pres['batch_data'].update({key: gvars.pop(key)})
        pres['run_data'] = gvars
        return pres

    def to_response_book(self):
        '''Get a :class:`~valjean.eponine.response_book.ResponseBook` from the
        :class:`T4ParseResult`.

        The global variables in ResponseBook are the batch data. You can access
        the `run data` only from the parsed result.

        :rtype: ResponseBook
        '''
        list_resps = [resp for key, lresp in self.res.items()
                      for resp in lresp
                      if key not in ('batch_data', 'run_data')]
        resp_book = ResponseBook(list_resps,
                                 global_vars=self.res['batch_data'])
        if resp_book.is_empty():
            LOGGER.error('ResponseBook creation failed, please check what')
        return resp_book
