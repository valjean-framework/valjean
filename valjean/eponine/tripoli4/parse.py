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
from .common import SpectrumDictBuilderException, MeshDictBuilderException
from ...chrono import Chrono
from ..browser import Browser
from .data_convertor import convert_data
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
    def __init__(self, jddname):
        '''Initialize the :class:`Parser` object.

        :param str jddname: path to the Tripoli-4 output

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
        return scan.Scanner(self.jdd)

    def _check_scan(self, scan_res):
        '''Check existence of scan result and presence of normal end (per
        default NORMAL COMPLETION).

        :param Scanner scan_res: scan result
        '''
        if not scan_res:
            raise ParserException(
                f"No result found in Tripoli-4 listing {self.jdd}\n"
                f"{scan_res.fatal_error()}")
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
                # Disable packrat caching: it degrades the performance of our
                # grammar. We have to disable it globally here, because other
                # packages (matplotlib for example) may have enabled it
                # globally
                ParserElement.disable_memoization()
                result = gram.parseString(str_to_parse).asList()
        except ParseException as err:
            LOGGER.error("Parsing failed in %s, you are probably trying to "
                         "read a new response. Please update the parser "
                         "before re-running.", self.jdd)
            LOGGER.debug("Exception explanation:\n%s", err.explain(depth=None))
            # from None allows to raise a new exception without traceback and
            # message of the previous one here.
            raise ParserException("Error in parsing") from None
        except (SpectrumDictBuilderException, MeshDictBuilderException) as dbe:
            LOGGER.error(dbe)
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
                'No "time" variable found in the Tripoli-4 output, '
                'please check it.') from sit
        if bdata[time_key] != self.scan_res.times[time_key][batch_number]:
            msg = (f'{time_key} looks inconsistent between parsing '
                   f'({bdata[time_key]}) and scanning '
                   f'({self.scan_res.times[time_key][batch_number]})')
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
    '''Class containing a parsing result from Tripoli-4 output for one batch.


        The :class:`ParseResult` object is accessible from the instance
        attribute

        `res`
            that is a unique dictionary containing all the results from
            scanning and parsing steps. Variables characteristic to a batch are
            stored under the key ``'batch_data'`` no matter if they come from
            :class:`.Scanner` or from :class:`Parser`. Variables
            characteristic to a run (= one execution of Tripoli-4) are stored
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
        self.name = name
        self._check_batch_number(parse_res, scan_vars)
        self.pres = parse_res
        self.res = self._build_unique_dict(self._build_datasets(),
                                           scan_vars, name)

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

    def _build_datasets(self):
        ares = {}
        for key, val in self.pres.items():
            if key == 'batch_data':
                ares[key] = val.copy()
            else:
                ares[key] = [self._make_datasets(r) for r in val]
        return ares

    @staticmethod
    def _set_array_what(score, resp):
        if resp['response_type'] == 'sensitivity':
            return 'sensitivity'
        if resp['response_type'] == 'spherical_harmonics':
            return resp['results']['spherical_harmonics']['what']
        # score_name for adjoint criticality edition
        what = resp.get('response_function', resp.get('score_name'))
        return score.replace('score', what).lower()

    @staticmethod
    def _set_scalar_what(resn, resp):
        if resp['response_type'] == 'sensitivity':
            return 'sensitivity'
        if 'batches' in resn or 'kij' in resn:
            return resn
        return resp.get('response_function', resp.get('response_type')).lower()

    @staticmethod
    def _set_args(score, resn, resp):
        rname = '_'.join((score, resn)).replace('not_converged',
                                                resp['response_type'])
        sigma = 'sigma' if 'sigma' in resp['results'][resn] else None
        if score == 'keff':
            sigma = 'sigma%'
            rname = score
            what = 'keff'
        elif 'correlation' in score:
            what = 'correlation'
            sigma = None
        elif score == 'equivalent_keff':
            what = 'keff'
            rname = score
            sigma = None
        elif 'vovstar' in score:
            sigma = 'vovstar_sigma'
            what = 'vovstar'
        elif 'uncert' in resn:
            rname = rname.replace('uncert_', '')
            what = score
        else:
            what = resp['response_function'].lower()
        return rname, sigma, what

    def _dset_from_dict(self, resn, res, resp):
        tdict = {}
        for arr in res:
            if arr in ('units', 'coordinates'):
                tdict[arr] = res[arr]
                continue
            if ((isinstance(res[arr], str)
                 and arr not in ('not_converged', 'what'))):
                tdict[arr] = res[arr]
                continue
            if arr in ('bins', 'sigma', 'sigma%', 'what'):
                continue
            if 'array' in arr:
                scores = [k for k in res[arr].dtype.names if k != 'sigma']
                for score in scores:
                    rname = ('_'.join([score, arr]) if score not in arr
                             else arr).replace('_array', '')
                    what = self._set_array_what(score, resp)
                    tdict[rname] = convert_data(
                        resp['results'], resn, array_key=arr, score=score,
                        name=self.name, what=what)
            else:
                rname, sigma, what = self._set_args(arr, resn, resp)
                tdict[rname] = convert_data(
                    resp['results'], resn, name=self.name,
                    what=what, score=arr, sigma=sigma)
        return tdict

    def _make_datasets(self, resp):
        ress = {k: v for k, v in resp.items() if k != 'results'}
        res = {}
        resp_res = resp['results']
        for resn, ires in resp_res.items():
            if resn == 'spectrum' and {'mesh', 'spectrum'}.issubset(resp_res):
                if not any('entropy' in n for n in resp_res['mesh']):
                    LOGGER.warning(
                        'Mesh and spectrum in same result, skipping spectrum. '
                        'Not foreseen case, please contact a developer')
                continue
            if isinstance(ires, dict):
                res.update(self._dset_from_dict(resn, ires, resp))
            elif isinstance(res, str) and resn != 'not_converged':
                res[resn] = ires
            else:
                rname = (resp['response_type'] if resn == 'not_converged'
                         else resn)
                what = self._set_scalar_what(resn, resp)
                res[rname] = convert_data(resp_res, resn, name=self.name,
                                          what=what)
        ress['results'] = res
        return ress

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
