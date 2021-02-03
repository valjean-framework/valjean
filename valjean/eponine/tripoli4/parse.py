'''Module performing scanning and parsing of Tripoli-4 outputs.

This module also allows quick checks on outputs:

* presence of ``"NORMAL COMPLETION"``
* presence and values of times (simulation, exploitation)

Some options for debugging are available (end flag).

.. todo::

   Change absolute imports in relative ones when main will be moved to
   :ref:`cambronne <cambronne-main>`.
'''

import threading
from pyparsing import ParseException, ParserElement

from . import scan
from .grammar import t4gram
from .common import SpectrumDictBuilderException
from ...chrono import Chrono
from ..browser import Browser
from ... import LOGGER


PYPARSING_LOCK = threading.RLock()

# in Eponine, profile is a key of globals
if 'profile' not in globals()['__builtins__']:
    def profile(fprof):
        '''To profile memory usage.'''
        return fprof


class ParserException(Exception):
    '''An error that may be raised by the :class:`Parser` class.'''


class Parser:
    '''Scan Tripoli-4 listings, then parse the required batches.'''

    @profile
    def __init__(self, jddname, *, mesh_lim=-1):
        '''Initialize the :class:`Parser` object.

        :param str jddname: path to the Tripoli-4 output
        :param int mesh_lim: limit of meshes to read (-1 per default)

        It also initalizes the result of :class:`.scan.Scanner` to ``None``,
        then executes the scan. If this step fails an exception is raised.

        The Parser main object instance variable is:

        `scan_res` (:class:`~.scan.Scanner`)
            result from the scan of the Tripoli-4 output. See in the related
            documentation the various instance variables available (like
            ``times``). Inheriting from :class:`collections.abc.Mapping`
            various default methods are available like ``len``, ``[]``, etc.
            The keys of :class:`~.scan.Scanner` are the batch numbers available
            from the Tripoli-4 output. To get their list, use
            :meth:`batch_numbers`.

        Parsing (e.g. :meth:`parse_from_number`) returns a
        :class:`ParseResult`.
        '''
        LOGGER.info("Parsing %s", jddname)
        self.jdd = jddname
        self.mesh_limit = mesh_lim
        try:
            with Chrono() as chrono:
                self.scan_res = self._scan()
        except scan.ScannerException as t4se:
            LOGGER.error(t4se)
            raise ParserException("Scan failed.") from None
        except ParserException as t4pe:
            LOGGER.error(t4pe)
            raise ParserException("Scan failed.") from None
        else:
            LOGGER.info("Successful scan in %f s", chrono)

    def _scan(self):
        '''Scan the parse the given jdd.'''
        scan_res = self._scan_listing()
        self._check_scan(scan_res)
        return scan_res

    @profile
    def _scan_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan`.

        :rtype: Scanner
        '''
        return scan.Scanner(self.jdd, self.mesh_limit)

    def _check_scan(self, scan_res):
        '''Check existence of scan result and presence of normal end (per
        default NORMAL COMPLETION).

        :param Scanner scan_res: scan result
        '''
        if not scan_res:
            raise ParserException(
                "No result found in Tripoli-4 listing {}\n{}"
                .format(self.jdd, scan_res.fatal_error()))
        if not scan_res.normalend:
            LOGGER.warning("Tripoli-4 listing did not finish with "
                           "NORMAL COMPLETION.")

    def batch_numbers(self):
        '''Help method to get the available batch numbers.

        :rtype: list(int)
        '''
        return list(self.scan_res.keys())

    def _parse_listing_worker(self, gram, str_to_parse):
        '''Parse the given string and raise exception if parsing failed.'''
        try:
            with PYPARSING_LOCK:
                # pylint: disable=protected-access
                ParserElement._parse = ParserElement._parseNoCache
                result = gram.parseString(str_to_parse).asList()
        except ParseException:
            LOGGER.error("Parsing failed in %s, you are probably trying to "
                         "read a new response. Please update the parser "
                         "before re-running.", self.jdd)
            # from None allows to raise a new exception without traceback and
            # message of the previous one here.
            raise ParserException("Error in parsing") from None
        except SpectrumDictBuilderException as sdbe:
            LOGGER.error(sdbe)
            raise ParserException("Error in parsing") from None
        return result

    def _time_consistency(self, pres, batch_number):
        '''Check time consistency between parsed result and scan.'''
        if 'batch_data' not in pres:
            raise ParserException('No batch_data in parsed result, '
                                  'something looks wrong in the T4 output.')
        bdata = pres['batch_data']
        try:
            time_key = next(k for k in bdata if 'time' in k)
        except StopIteration as sit:
            raise ParserException(
                'No "time" variable found in the TRIPOLI-4 output, '
                'please check it.') from sit
        if bdata[time_key] != self.scan_res.times[time_key][batch_number]:
            msg = ('{} looks inconsistent between parsing ({}) and scanning '
                   '({})'.format(time_key, bdata[time_key],
                                 self.scan_res.times[time_key][batch_number]))
            if self.scan_res.partial:
                LOGGER.warning(msg)
            else:
                raise ParserException(msg)

    def parse_from_number(self, batch_number, name=''):
        '''Parse from batch index or batch number.

        :param int batch_number: number of the batch to parse
        :rtype: ParseResult
        '''
        LOGGER.debug('Using parse from Parser')
        with Chrono() as chrono:
            pres, = self._parse_listing_worker(
                t4gram, self.scan_res[batch_number])
        LOGGER.info("Successful parsing in %f s", chrono)
        self._time_consistency(pres, batch_number)
        scan_vars = self.scan_res.global_variables(batch_number)
        return ParseResult(pres, scan_vars, name)

    def parse_from_index(self, batch_index=-1, name=''):
        '''Parse from batch index or batch number.

        Per default the last batch is parsed (index = -1).

        :param int batch_index: index of the batch in the list of batches
        :rtype: ParseResult
        '''
        batch_number = self.scan_res.batch_number(batch_index)
        return self.parse_from_number(batch_number, name)

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


class ParseResult:
    '''Class containing a parsing result from TRIPOLI-4 output for one batch.


        The :class:`ParseResult` object is accessible from the instance
        attribute

        `res`
            that is a unique dictionary containing all the results from
            scanning and parsing steps. Variables characteristic to a batch are
            stored under the key ``'batch_data'`` no matter if they come from
            :class:`.Scanner` or from :class:`Parser`. Variables
            characteristic to a run (= one execution of TRIPOLI-4) are stored
            under ``'run_data'``, coming from the scanning step.

        It is possible to transform the ``res`` dictionary in a
        :class:`~valjean.eponine.browser.Browser` thanks to the
        method :meth:`to_browser`.
    '''

    def __init__(self, parse_res, scan_vars, name=''):
        '''Initialize the :class:`ParseResult` from:

        :param dict parse_res: result from T4 parsing (for 1 batch)
        :param dict scan_vars: variables coming from :class:`.Scanner` global
            to job or specific to the batch.
        :param str name: name to give to the parse result (will be propagated
            to data)

        Fill the `res` object.
        '''
        self._check_batch_number(parse_res, scan_vars)
        self.res = self._build_unique_dict(parse_res, scan_vars, name)

    @staticmethod
    def _check_batch_number(pres, svars):
        '''Check that batch number from scan variables and edition batch number
        if exists are the same, else emit a warning.
        '''
        ebn = pres.get('edition_batch_number')
        sbn = svars.get('batch_number')
        if sbn is None:
            LOGGER.warning('No batch number was set in Scanner, please check.')
        if ebn is not None and ebn != sbn:
            LOGGER.warning('Edition batch number different from batch number')

    @staticmethod
    def _build_unique_dict(pres, svars, name):
        '''Build a unique dictionary from parsed result and global variables
        from Scanner.

        Variables specific to batch are added to the already existing
        dictionary under the key ``'batch_data'`` from parsed result, while a
        new item is created for the run data (key: ``'run_data'``).

        :param dict pres: parsed result
        :param dict svars: global variables from Scanner
        :param str name: name of the parsed result (be considered as
            ``'batch_data'``)
        :returns: updated parsed result
        '''
        gvars = svars.copy()
        bdata_keys = {'batch_number', 'simulation_time', 'elapsed_time',
                      'exploitation_time'}
        for key in bdata_keys & set(gvars.keys()):
            pres['batch_data'].update({key: gvars.pop(key)})
        pres['batch_data'].update({'name': name})
        pres['run_data'] = gvars
        return pres

    def to_browser(self):
        '''Get a :class:`~valjean.eponine.browser.Browser` from the
        :class:`ParseResult`.

        The global variables in Browser are the batch data. You can access the
        `run data` only from the parsed result.

        :rtype: Browser
        '''
        list_resps = [resp for key, lresp in self.res.items()
                      for resp in lresp
                      if key not in ('batch_data', 'run_data')]
        browser = Browser(list_resps, global_vars=self.res['batch_data'])
        if browser.is_empty():
            LOGGER.error('Browser creation failed, please check what happened')
        return browser
