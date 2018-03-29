'''Module performing scanning and parsing of Tripoli-4 outputs.

This module also allows quick checks on outputs:

* presence of ``"NORMAL COMPLETION"``
* presence and values of times (simulation, exploitation)

Some options for debugging are available (end flag).

.. todo::

   Change absolute imports in relative ones when main will be moved to
   :ref:`cambronne <cambronne-main>`.
'''

import sys
import time
import logging
import valjean.eponine.pyparsing_t4.grammar as pygram
from valjean.eponine import scan_t4
from pyparsing import ParseException


LOGGER = logging.getLogger('valjean')

# in Eponine, profile is a key of globals
if 'profile' not in globals().keys():
    def profile(fprof):
        '''To profile memory usage.'''
        return fprof


class T4ParserException(Exception):
    '''An error that may be raised by the :class:`T4Parser` class.'''
    pass


class T4Parser():
    '''Scan Tripoli-4 listings, then parse the required batches.
    '''

    @profile
    def __init__(self, jddname, batch=-1, mesh_lim=-1):  # config, *,
        '''
        Initialize the :class:`T4Parser` object.

        :param str jddname: path to the Tripoli-4 output
        :param int batch: batch to read (-1 = last, 0 = all, then X)
        :param int mesh_lim: limit of meshes to read (-1 per default)

        It also initalize the result of :class:`.scan_t4.Scan` to ``None`` and
        the parsing result, from *pyparsing*, to ``None``.

        If the path contains the ``"PARA"`` string, the checks will be done for
        parallel mode.
        '''
        self.jdd = jddname
        self.batch_number = batch
        self.mesh_limit = mesh_lim
        self.end_flag = ""
        self.scan_res = None
        self.result = None
        self.para = True if "PARA" in jddname else False

    @classmethod
    def parse_jdd(cls, jdd, batch):
        '''
        Constructor for T4Parser for "default" cases: no mesh limit. Scanning
        and parsing are automatically done.

        :param str jdd: path to the output from Tripoli-4
        :param int batch: number of the batch to parse (-1 = last one
                          (*default*), 0 = all of them, X > 0 = batch X to be
                          parsed)
        '''
        start_time = time.time()
        parser = cls(jdd, batch)
        try:
            parser.scan_t4_listing()
        except T4ParserException as t4pe:
            print(t4pe)
            return
        LOGGER.info("Successful scan in %f s", time.time()-start_time)
        start_parse = time.time()
        try:
            parser.parse_t4_listing()
        except T4ParserException as t4pe:
            print(t4pe)
            return
        LOGGER.info("Successful parsing in %f s", time.time()-start_parse)
        LOGGER.info("Time (scan + parse) = %f s", time.time()-start_time)
        return parser

    @classmethod
    def parse_jdd_with_mesh_lim(cls, jdd, batch, mesh_lim=-1, end_flag=""):
        '''
        Constructor for T4Parser for cases where a limit on meshes can be set.
        It is also possible, for debug cases, to put a user's end flag.
        Scanning and parsing are automatically done.

        :param str jdd: path to the output from Tripoli-4
        :param int batch: number of the batch to parse (-1 = last one
                          (*default*), 0 = all of them, X > 0 = batch X to be
                          parsed)
        :param int mesh_lim: limit on lines of meshes (-1 = all of them,
                             X > 0 = lines kept for each mesh, X = 0 will fail)
        :param str end_flag: optional end flag to stop scanning (and parsing)
        :returns: T4Parser object
        '''
        start_time = time.time()
        parser = cls(jdd, batch, mesh_lim)
        parser.end_flag = end_flag
        try:
            parser.scan_t4_listing()
        except T4ParserException as t4pe:
            print(t4pe)
            return
        LOGGER.info("Successful scan in %f s", time.time()-start_time)
        start_parse = time.time()
        try:
            parser.parse_t4_listing()
        except T4ParserException as t4pe:
            print(t4pe)
            return
        LOGGER.info("Successful parsing in %f s", time.time()-start_parse)
        LOGGER.info("Time (scan + parse) = %f s", time.time()-start_time)
        return parser

    @profile
    def scan_t4_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan_t4`.

        If end_flag was set, calls :meth:`.scan_t4.Scan.debug_scan` instead of
        the usual constructor.
        '''
        if self.end_flag:
            self.scan_res = scan_t4.Scan.debug_scan(self.jdd, self.mesh_limit,
                                                    self.para, self.end_flag)
        else:
            self.scan_res = scan_t4.Scan(self.jdd, self.mesh_limit, self.para)
        # print("is scan_res ?", self.scan_res)
        # print("len(scan_res) =", len(self.scan_res))
        # print("normal end:", self.scan_res.normalend)
        # need to look if we keep or not the excpetion, catch it,
        # let it crash... -> how to count unsuccessful jobs...
        if not self.scan_res:
            raise T4ParserException("No result found in Tripoli-4 listing.")
        if not self.scan_res.normalend:
            LOGGER.warning("Tripoli-4 listing did not finished with "
                           "NORMAL COMPLETION.")

    def parse_t4_listing(self):
        '''Parse Tripoli-4 results, calling pyparsing and :mod:`.pyparsing_t4`
        '''
        if self.batch_number == 0:
            str_to_parse = self.scan_res.get_all_batch_results()
        else:
            str_to_parse = self.scan_res[self.batch_number]
        if LOGGER.isEnabledFor(logging.DEBUG):
            with open("jddres.txt", 'w') as fout:
                fout.write(str_to_parse)
        # now parse the results string
        try:
            self.result = pygram.mygram.parseString(str_to_parse)
        except ParseException:
            LOGGER.warning("Parsing failed, you are probably trying to read a "
                           "new response. Please implement it before "
                           "re-running.")
            LOGGER.warning("If you want to get the pyparsing failure message, "
                           "please run with LOGGER at level debug.")
            if LOGGER.isEnabledFor(logging.DEBUG):
                raise
            # exception should be caught somewhere ?
            # from None allows to raise a new exception without traceback and
            # message of the previous one here.
            raise T4ParserException("Error in parsing, see above.") from None

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
        return ((self.para and 'elapsed time' in self.scan_res.times
                 and 'simulation time' in self.scan_res.times)
                or (not self.para
                    and ('simulation time' in self.scan_res.times
                         or 'exploitation time' in self.scan_res.times)))

    def print_t4_times(self):
        '''Print time characteristics of the Tripoli-4 result considered.
        This print includes initialization time, simulation time, exploitation
        time and elapsed time.
        '''
        for stime, vtime in self.scan_res.times.items():
            print(stime.capitalize(), "=", vtime)


def main(myjdd="", batch_num=-1, mesh_lim=None):
    '''Main function in order to test parsing directly from this module.

    :param string myjdd: path to the T4 input
    :param int batch_number: batch number to parse
    :param int mesh_lim: number of lines of mesh to read
                         (if required, else None)
    :returns: boolean, True if parsing was successful, else False
    '''
    if myjdd == "":
        try:
            myjdd = sys.argv[1]
        except IndexError:
            print("Eponine: argument needed (jdd name)")
            exit(-1)

    # need to think about endflag (?), meshlim and para arguments
    if mesh_lim:
        t4_res = T4Parser.parse_jdd_with_mesh_lim(myjdd, batch_num, mesh_lim)
    else:
        t4_res = T4Parser.parse_jdd(myjdd, batch_num)
    if t4_res:
        if LOGGER.isEnabledFor(logging.INFO):
            t4_res.print_t4_stats()
            t4_res.print_t4_times()
        return t4_res.check_t4_times()


if __name__ == "__main__":
    main()
