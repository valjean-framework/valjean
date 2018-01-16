'''
Module performing a scan of Tripoli-4 output listing in order to only keep
relevant parts of it = results to be used for VV or analysis or the run.

Code :
- quickly reads the results file
- recognize beginning and end of results sections
- get the required number of batchs
- get the edition batch numbers (if exists)

Important for the scan: results will be kept
- from 'RESULTS ARE GIVEN'
- to an end flag given by user
Default end flag is "simulation time",
for exploitation jobs "exploitation time"will be used (example: Green bands),
for jobs running in parallel end flagshould be "elapsed time".
In any case, it is always possible to set a different end flag.

Memory profinling is available using memory_profiler:
mprof run --python python3 scan.py FILE
mprof plot
'''

import sys
import time
from collections.abc import Mapping
from collections import OrderedDict
import logging


LOGGER = logging.getLogger('valjean')


LOGGER.info("sys.argv: %s", str(sys.argv))

# count_mesh_exceeding = 0


if "mem" not in sys.argv:
    def profile(fmem):
        '''Desactivate profiling if not required in command line.'''
        return fmem


# class MeshScanner:
#     '''Class to scan mesh, find end of mesh block (for one energy range for
#     example) and implement limit in number of lines of mesh kept in the batch
#     result (minimum is 1).
#     '''
#     def __init__(self, meshlim):
#         self.meshlim = meshlim
#         self.nbmeshlines = 0
#         self.prevmeshline = False
#         # self.inmeshres = False
#         self.stopmesh = False

#     def scan_mesh(self, line):
#         '''Scan mesh: look for end of mesh taking into account multiple energy
#         bins and energy integrated mesh.
#         :param line: line to be scanned
#         :type line: string
#         '''
#         # print("stopmesh =", self.stopmesh)
#         if "(" in line and ")" in line and "," in line:
#             self.nbmeshlines += 1
#             self.prevmeshline = True
#         elif "(" not in line and ")" not in line and self.prevmeshline:
#             self.prevmeshline = False
#         elif ("Energy range" in line
#               or "ENERGY INTEGRATED RESULTS" in line
#               or "number of batches used" in line
#               or line.isspace()):
#             self.nbmeshlines = 0
#             self.stopmesh = False

#     def add_meshline(self, count_excess, result, line):
#         '''Add mesh line to result if stop mesh is not reached.
#         :param count_excess: counter for mesh lines excess
#         :type count_excess: int
#         :param result: batch result
#         :type result: list of strings
#         :param line: mesh line
#         :type line: string
#         '''
#         if not self.stopmesh:
#             if self.nbmeshlines == self.meshlim+1:
#                 count_excess += 1
#                 result.append("\n")
#                 self.stopmesh = True
#                 if count_excess < 5:
#                     LOGGER.warning("[31mToo much mesh lines, keeping %d "
#                                    "lines, if needed change meshlim arg[0m",
#                                    self.meshlim)
#             else:
#                 result.append(line)
#         return count_excess


class BatchResultScanner():
    '''Class to build batchs collection.
    '''
    def __init__(self, count_excess, current_batch, meshlim):
        self.count_batch = 0
        self.inmeshres = False
        self.count_mesh_exceeding = count_excess
        self.batch_counts = {'number': -1,
                             'current': current_batch,
                             'greater': 0}
        self.result = []
        # self.meshscanner = None
        self.inmesh = False
        self.meshlim = meshlim
        self.nbmeshlines = 0
        self.prevmeshline = False
        self.stopmesh = False

    def scan_mesh(self, line):
        '''Scan mesh: look for end of mesh taking into account multiple energy
        bins and energy integrated mesh.
        :param line: line to be scanned
        :type line: string
        '''
        # print("stopmesh =", self.stopmesh)
        if "(" in line and ")" in line and "," in line:
            self.nbmeshlines += 1
            self.prevmeshline = True
        elif "(" not in line and ")" not in line and self.prevmeshline:
            self.prevmeshline = False
        elif ("Energy range" in line
              or "ENERGY INTEGRATED RESULTS" in line
              or "number of batches used" in line
              or line.isspace()):
            self.nbmeshlines = 0
            self.stopmesh = False

    def add_meshline(self, line):
        '''Add mesh line to result if stop mesh is not reached.
        :param count_excess: counter for mesh lines excess
        :type count_excess: int
        :param result: batch result
        :type result: list of strings
        :param line: mesh line
        :type line: string
        '''
        if not self.stopmesh:
            if self.nbmeshlines == self.meshlim+1:
                self.count_mesh_exceeding += 1
                self.result.append("\n")
                self.stopmesh = True
                if self.count_mesh_exceeding < 5:
                    LOGGER.warning("[31mToo much mesh lines, keeping %d "
                                   "lines, if needed change meshlim arg[0m",
                                   self.meshlim)
            else:
                self.result.append(line)

    def build_result(self, line):
        '''Scan line to build batch result: mainly deals with mesh
        specificities and store line.
        :param line: last line to be taken into account
        :type line: string
        '''
        if "Edition after batch number" in line:
            self.batch_counts['number'] = int(line.split()[-1])
        elif "Results on a mesh" in line:
            self.inmesh = True
        if self.inmesh and ("****" in line):
            self.inmesh = False
        if "PARA" in sys.argv and "number of batches used" in line:
            self._set_greater_batch_number(line)
        self._store_line(line)

    def _store_line(self, line):
        if self.inmesh:
            self.scan_mesh(line)
            self.add_meshline(line)
        else:
            self.result.append(line)

    def _set_greater_batch_number(self, line):
        newbatch = int(line.split()[4])
        if self.batch_counts['greater'] < newbatch:
            self.batch_counts['greater'] = newbatch

    def _check_batch_number(self):
        if "PARA" not in sys.argv:
            if self.batch_counts['number'] != self.batch_counts['current']:
                LOGGER.info("Edition batch (%d) different from "
                            "current batch (%d)",
                            self.batch_counts['number'],
                            self.batch_counts['current'])
                LOGGER.info("If no Edition batch keep current batch, "
                            "else keep edition batch")
                if self.batch_counts['number'] < self.batch_counts['current']:
                    self.batch_counts['number'] = self.batch_counts['current']
            if self.batch_counts['current'] == 0:
                LOGGER.warning("Current batch = 0, something to check ?")
        else:
            if self.batch_counts['greater'] > self.batch_counts['number']:
                self.batch_counts['number'] = self.batch_counts['greater']

    def get_result(self, line):
        '''Send result.
        Called if end flag has been found, add last line and concatenates
        result.
        :param line: last line to be taken into account
        :type line: string
        :return: string build from lsit of strings junction
        '''
        self._check_batch_number()
        LOGGER.debug("[1;31mEND FLAG found, batch number = %d, "
                     "current batch = %d, greater batch = %d[0m",
                     self.batch_counts['number'],
                     self.batch_counts['current'],
                     self.batch_counts['greater'])
        self.result.append(line)
        return ''.join(self.result)

class Scan(Mapping):
    '''Class to keep marks on the file

    Members needed at initialization:
    :param fname: name of the input file
    :type fname: string
    :param endflag: end flag of the results block in Tripoli-4 listing
    :type endflag: string
    :param meshlim: limit on number of lines to read in meshes outputs
                    (can be really long), default = -1, all cells will be read
                    Minimum value is 1, use it to skip the mesh.
                    If 0 is used, parsing will fail as no mesh will be found.
    :type meshlim: int
    '''

    @profile
    def __init__(self, fname, endflag="simulation time", meshlim=-1):
        '''Initialize the instance from the file "fname", meaning reads the
        file and store the relevant parts of it, i.e. result block for each
        batch edition.

        :param reqbatchs: number of batchs required (read from file fname)
        :type reqbatchs: int
        :param normalend: bool for presence of "NORMAL COMPLETION"
        :type normalend: bool
        :param countwarnings: count number of warnings (for statistics)
        :type countwarnings: int
        :param counterrors: count number of errors (for statistics)
        :type counterrors: int
        :param initialization_time: save initialization time (no saved in the
                                   result)
        :type initialization_time: int
        :param last_generator_state: keep the random generator state (not
                                   included in the the result)
        :type last_generator_state: string
        :param _collres: ordered dictionary containing
                        {batch_number : 'result block',}
                        batch_number is an int
        :type _collres: OrderedDict
        '''
        self.start_time = time.time()
        self.fname = fname
        self.endflag = endflag
        self.meshlim = meshlim
        self.reqbatchs = -1
        self.normalend = False
        self.countwarnings = 0
        self.counterrors = 0
        self.initialization_time = -1
        self.last_generator_state = ""
        self._collres = OrderedDict()
        self._get_collres()
        LOGGER.info("End of initialization: %f s",
                    time.time()-self.start_time)

    @profile
    def _get_collres(self):
        '''Read the file and store all relevant information.
        '''
        count_batch = 0
        started_gen = False
        count_mesh_exceeding = 0
        result = []
        current_batch = 0
        _batch_scan = None
        with open(self.fname, errors='ignore') as fil:
            for line in fil:
                if line.lstrip().startswith("//"):  # comment in the jdd
                    continue
                elif ("BATCH" in line and '_' not in line
                      and "THIS" not in line):
                    indbatch = line.split().index('BATCH')
                    self.reqbatchs = int(line.split()[indbatch+1])
                    count_batch += 1
                elif "PACKET_LENGTH" in line:
                    LOGGER.info("[1mBatchs grouped by packets -> "
                                "number of batchs expected divided "
                                "by PACKET_LENGTH in PARA[0m")
                    indpacket = line.split().index('PACKET_LENGTH')
                    if "PARA" in sys.argv:
                        self.reqbatchs //= int(line.split()[indpacket+1])
                    LOGGER.debug("new number of batchs = %d", self.reqbatchs)
                elif "RESULTS ARE GIVEN" in line:
                    _batch_scan = BatchResultScanner(count_mesh_exceeding,
                                                     current_batch,
                                                     self.meshlim)
                elif line.startswith(' batch number :'):
                    current_batch = int(line.split()[-1])
                elif "NORMAL COMPLETION" in line:
                    self.normalend = True
                elif "WARNING" in line:
                    self.countwarnings += 1
                elif "ERROR" in line:
                    self.counterrors += 1
                elif "initialization time" in line:
                    self.initialization_time = int(line.split()[3])
                elif ("Type and parameters of random generator "
                      "at the end of simulation:" in line):
                    started_gen = True
                elif started_gen and "COUNTER" in line:
                    result.append(line)
                    self.last_generator_state = ''.join(result)
                    result = []
                    started_gen = False
                if _batch_scan:
                    _batch_scan.build_result(line)
                if self.endflag in line and _batch_scan:
                    batch_number = _batch_scan.batch_counts['number']
                    self._collres[batch_number] = _batch_scan.get_result(line)
                    count_mesh_exceeding = _batch_scan.count_mesh_exceeding
                    _batch_scan = None
                if started_gen:
                    if "Type and parameters" not in line:
                        result.append(line)
        LOGGER.debug("Number of string 'BATCH' seen: %d", count_batch)
        if count_mesh_exceeding > 4:
            LOGGER.warning("Number of mesh exceeding meshlim arg: %d",
                           count_mesh_exceeding)

    def __getitem__(self, batch_number):
        '''Get result corresponding to batch_number.
        If batch_number == -1 return the last result. A warning is printed if
        the last batch_number doesn't correspond to the number of batchs
        required.

        Use: Scan[X]
        '''
        LOGGER.debug("[1;38;5;79m__getitem__, batch number = %d[0m",
                     batch_number)
        if batch_number == -1:
            last_batch = next(reversed(self._collres))
            LOGGER.info("last batch number = %d", last_batch)
            if last_batch != self.reqbatchs:
                LOGGER.warning("[1;33mWARNING: last batch number %d"
                               "!= required number of batchs %d[0m",
                               last_batch, self.reqbatchs)
            return self._collres[last_batch]
        else:
            try:
                return self._collres[batch_number]
            except KeyError:  # as err:
                message = ("Wrong batch number required, {} doesn't exist, "
                           "please change it to an existing one"
                           .format(batch_number))
                LOGGER.error("[1;31m%s[0m", message)
                raise
                # raise type(err)(message).with_traceback(sys.exc_info()[2])

    def __iter__(self):
        '''Iteration over the collection of results, on the keys to match dict
        and OrderedDict behaviour.
        '''
        yield from self._collres.__iter__()

    def __len__(self):
        '''Return length of the collection of results, equivalent to get the
        number of edited batchs.
        '''
        return len(self._collres)

    def __reversed__(self):
        '''Reversed the OrderedDict order (easier to get last element)
        '''
        yield from self._collres.__reversed__()

    @profile
    def get_last_edited_batch_number(self):
        '''Return last edited batch number'''
        return list(self._collres.keys())[-1]

    @profile
    def get_all_batch_results(self):
        '''Return all batchs results in one string, to be parsed in once.
        '''
        return ''.join(self._collres.values())

    def print_statistics(self):
        '''Print statistics of the listing scanned: normal end, number of
        warnings and errors.
        '''
        print("Normal end of the jdd:", self.normalend)
        print("Number of warnings found:", self.countwarnings)
        print("Number of errors found:", self.counterrors)
