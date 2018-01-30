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

# in Eponine, profile is a key of globals
if 'profile' not in globals().keys():
    def profile(fprof):
        '''To profile memory usage.'''
        return fprof


class EndListingError(Exception):
    '''Listing did not finished by NORMAL COMPLETION and/or had no result
    block.
    '''
    pass


class T4Parser():
    '''Parse Tripoli-4 listings.
    '''

    @profile
    def __init__(self, jddname, batch=-1, endflag="simulation time",
                 meshlim=1000, para=False):
        self.jdd = jddname
        self.batch_number = batch
        self.end_flag = endflag
        self.mesh_lim = meshlim
        self.scan_res = None
        self.result = None
        self.para = para


    @profile
    def scan_t4_listing(self):
        '''Scan Tripoli-4 listing, calling :mod:`.scan_t4`'''
        self.scan_res = scan_t4.Scan(self.jdd, self.end_flag, self.mesh_lim)
        if not self.scan_res.normalend and len(self.scan_res) == 0:
            raise EndListingError

    def parse_t4_listing(self):
        '''Parse Tripoli-4 results, calling pypasing and :mod:`.pyparsing_t4`
        '''
        str_to_parse = ""
        if self.batch_number == 0:
            str_to_parse = self.scan_res.get_all_batch_results()
        else:
            str_to_parse = self.scan_res[self.batch]
        # now parse the results string
        start_time = time.time()
        try:
            self.result = pygram.mygram.parseString(self.strres)
        except:
            LOGGER.warning("Parsing failed, please look carefully to the "
                           "output to understand why.")
            # sys.exit()
        print("[31mTemps:", time.time()-start_time, "[0m")

    def print_t4_stats(self):
        '''Print Tripoli-4 statistics (warnings and errors).'''
        self.scan_res.print_statistics()

    def print_t4_times(self):
        '''Print time characteristics of the Tripoli-4 result considered.
        This print includes initialization time, simulation time, exploitation
        time and elapsed time.
        '''
        print("initialization time:", self.scan_res.initialization_time)
        print("end times:")
        if self.result:
            if isinstance(self.result[-1], dict):
                if (('simulation_time' in self.result[-1]
                     or (self.para and "elpased time" in self.result[-1]))):
                    return True
                elif 'exploitation_time' in self.result[-1]:
                    return True
                else:
                    return False
            else:
                if (('simulation_time' in self.result
                     or (self.para and "elpased time" in self.result))):
                    return True
                else:
                    return False
