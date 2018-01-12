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


if "mem" not in sys.argv:
    def profile(fmem):
        '''Desactivate profiling if not required in command line.'''
        return fmem


class Scan(Mapping):
    '''Class to keep marks on the file

    Members needed at initialization:
    :param fname: name of the input file
    :type fname: string
    :param endflag: end flag of the results block in Tripoli-4 listing
    :type endflag: string
    :param meshlim: limit on number of lines to read in meshes outputs
                    (can be really long), default = 100
    :type meshlim: int
    '''

    @profile
    def __init__(self, fname, endflag="simulation time", meshlim=100):
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
        started_res = False
        started_gen = False
        batch_number = 0
        current_batch = 0
        inmeshres = False
        nbmeshlines = 0
        prevmeshline = False
        got_batch_number = False
        greater_batch_number = 0
        count_mesh_exceeding = 0
        result = []
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
                    started_res = True
                    got_batch_number = False
                elif line.startswith(' batch number :'):
                    current_batch = int(line.split()[-1])
                elif "Edition after batch number" in line and started_res:
                    batch_number = int(line.split()[-1])
                    got_batch_number = True
                elif "Results on a mesh" in line:
                    inmeshres = True
                    nbmeshlines = 0
                elif "(" in line and ")" in line and "," in line and inmeshres:
                    nbmeshlines += 1
                    prevmeshline = True
                elif ("(" not in line and ")" not in line
                      and prevmeshline and inmeshres):
                    prevmeshline = False
                elif (("Energy range" in line
                       or "ENERGY INTEGRATED RESULTS" in line
                       or "number of batches used" in line
                       or line.isspace())
                      and inmeshres): #and prevmeshline
                    nbmeshlines = 0
                elif "****" in line and inmeshres:
                    inmeshres = False
                elif self.endflag in line and started_res:
                    if "PARA" not in sys.argv:
                        if batch_number != current_batch:
                            LOGGER.info("Edition batch (%d) different from "
                                        "current batch (%d)",
                                        batch_number, current_batch)
                            LOGGER.info("If no Edition batch keep current "
                                        "batch, else keep edition batch")
                            if batch_number < current_batch:
                                batch_number = current_batch
                        if current_batch == 0:
                            LOGGER.warning("Current batch = 0, "
                                           "something to check ?")
                    else:
                        if greater_batch_number > batch_number:
                            batch_number = greater_batch_number
                    result.append(line)  # will change at end of the function
                    self._collres[batch_number] = ''.join(result)
                    result = []
                    started_res = False
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
                if started_res:
                    if inmeshres and nbmeshlines > self.meshlim:
                        if nbmeshlines == self.meshlim+1:
                            count_mesh_exceeding += 1
                            result.append("\n")
                            if count_mesh_exceeding < 5:
                                LOGGER.warning("[31mToo much mesh lines, "
                                               "keeping %d lines, if needed "
                                               "change meshlim arg[0m",
                                               self.meshlim)
                        continue
                    result.append(line)
                if started_gen:
                    if "Type and parameters" not in line:
                        result.append(line)
                if (("PARA" in sys.argv and started_res
                     and not got_batch_number
                     and "number of batches used" in line)):
                    newbatchnum = int(line.split()[4])
                    if greater_batch_number < newbatchnum:
                        greater_batch_number = newbatchnum
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
