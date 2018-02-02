'''Class calling Lamarque, the parser and transformer,
JDD normally direclty usable in tests.
'''

import sys
import time
# from Larmarque import Lamarque
import scan_t4
from valjean.eponine.lark_t4.larkOnTripoli import OtherTransformer
from lark import Lark
# import pyparsing_org
import valjean.eponine.pyparsing_t4.grammar as pygram
from pprint import pprint
import Enjolras
from pyparsing import ParseResults
from pyparsing import ParseException
import logging


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
    '''Parse Tripoli-4 listings.
    '''

    @profile
    def __init__(self, jddname, batch=-1, mesh_lim=-1, para=False): #config, *,
        self.jdd = jddname
        self.batch_number = batch
        self.mesh_limit = mesh_lim
        self.end_flag = ""
        self.scan_res = None
        self.result = None
        self.para = para

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
    def parse_jdd_with_mesh_lim(cls, jdd, batch, mesh_lim, end_flag=""):
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
        '''Scan Tripoli-4 listing, calling :mod:`.scan_t4`'''
        if self.end_flag:
            print("will use debug_scan")
            self.scan_res = scan_t4.Scan.debug_scan(self.jdd, self.mesh_limit,
                                                    self.end_flag)
        else:
            self.scan_res = scan_t4.Scan(self.jdd, self.mesh_limit)
        print("is scan_res ?", self.scan_res)
        print("len(scan_res) =", len(self.scan_res))
        print("normal end:", self.scan_res.normalend)
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
        if self.result:
            if isinstance(self.result[-1], dict):
                return ((self.para and "elapsed time" in self.result[-1])
                        or (not self.para
                            and ('simulation time' in self.result[-1]
                                 or 'exploitation time' in self.result[-1])))
            return ((self.para and "elapsed time" in self.result)
                    or (not self.para and 'simulation time' in self.result))

    def print_t4_times(self):
        '''Print time characteristics of the Tripoli-4 result considered.
        This print includes initialization time, simulation time, exploitation
        time and elapsed time.
        '''
        for stime, vtime in self.scan_res.times.items():
            print(stime.capitalize(), "=", vtime)

def main(myjdd="", mode="MONO"):
    if myjdd == "":
        try:
            myjdd = sys.argv[1]
        except IndexError:
            print("Eponine: argument needed (jdd name)")
            exit(-1)
    print(myjdd)
    print("mode =", mode)
    # mode = "PARA"

    myendflag = "simulation time"
    # if "exploit" in myjdd:
    if "exp" in myjdd and "verif" not in myjdd:
        myendflag = "exploitation time"
    if mode == "PARA":
        myendflag = "elapsed time"
    print("endflag =", myendflag)

    # need to think about endflag (?), meshlim and para arguments
    # t4_res = T4Parser.parse_jdd(myjdd, -1)  #, meshlim=2)
    t4_res = T4Parser.parse_jdd_with_mesh_lim(myjdd, -1, 2, end_flag="number of batch")
    if t4_res:
        t4_res.print_t4_stats()
        print("result of the function =", t4_res.check_t4_times())
        t4_res.print_t4_times()

if __name__ == "__main__":
    main()
