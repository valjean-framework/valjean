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
Default end flag is "simulation time", for exploitation jobs "exploitation time"
will be used (example: Green bands), for jobs running in parallel end flag
should be "elapsed time". In any case, it is always possible to set a different
end flag.

Memory profinling is available using memory_profiler:
mprof run --python python3 scan.py FILE
mprof plot
'''

import sys
import time
from collections import OrderedDict
from itertools import islice

print("sys.argv:", sys.argv)

if "mem" not in sys.argv:
    def profile(f):
        return f


class Scan():
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
        '''Initialize the instance from the file "fname", meaning reads the file
        and store the relevant parts of it, i.e. result block for each batch
        edition.

        :param reqbatchs: number of batchs required (read from file fname)
        :type reqbatchs: int
        :param normalend: bool for presence of "NORMAL COMPLETION"
        :type normalend: bool
        :param countwarnings: count number of warnings (for statistics)
        :type countwarnings: int
        :param counterrors: count number of errors (for statistics)
        :type counterrors: int
        :param initializationTime: save initialization time (no saved in the
                                   result)
        :type initializationTime: int
        :param lastGeneratorState: keep the random generator state (not inculded
                                   in the the result)
        :type lastGeneratorState: string
        :param collres: ordered dictionary containing
                        {batch_number : 'result block',}
                        batch_number is an int
        :type collres: OrderedDict
        '''
        start_time = time.time()
        self.fname = fname
        self.endflag = endflag
        self.meshlim = meshlim
        self.reqbatchs = -1
        self.normalend = False
        self.countwarnings = 0
        self.counterrors = 0
        self.initializationTime = -1
        self.lastGeneratorState = ""
        self.collres = OrderedDict()
        self._get_collres()
        print("End of initialization:", time.time()-start_time)

    @profile
    def _get_collres(self):
        '''Read the file and store all relevant information.
        '''

        countBATCH = 0
        started_res = False
        started_gen = False
        batch_number = 0
        current_batch = 0
        inmeshres = False
        nbmeshlines = 0
        prevmeshline = False
        prev2meshline = False
        gotBatchNumber = False
        greaterbatchnum = 0
        countMeshExceeding = 0
        start_time = time.time()
        result = []
        with open(self.fname, errors='ignore') as fil:
            for line in fil:
                if line.lstrip().startswith("//"):  # comment in the jdd
                    continue
                elif ("BATCH" in line and '_' not in line
                      and "THIS" not in line):
                    indbatch = line.split().index('BATCH')
                    self.reqbatchs = int(line.split()[indbatch+1])
                    countBATCH += 1
                elif "PACKET_LENGTH" in line:
                    print("[1mBatchs grouped by packets -> "
                          "number of batchs expected divided "
                          "by PACKET_LENGTH in PARA[0m")
                    indpacket = line.split().index('PACKET_LENGTH')
                    if "PARA" in sys.argv:
                        self.reqbatchs //= int(line.split()[indpacket+1])
                    print("new number of batchs =", self.reqbatchs)
                elif "RESULTS ARE GIVEN" in line:
                    started_res = True
                    gotBatchNumber = False
                elif line.startswith(' batch number :'):
                    current_batch = int(line.split()[-1])
                elif "Edition after batch number" in line and started_res:
                    batch_number = int(line.split()[-1])
                    gotBatchNumber = True
                elif "Results on a mesh" in line:
                    inmeshres = True
                    nbmeshlines = 0
                elif "(" in line and ")" in line and "," in line and inmeshres:
                    nbmeshlines += 1
                    prevmeshline = True
                elif ("(" not in line and ")" not in line
                      and prevmeshline and inmeshres):
                    prevmeshline = False
                    prev2meshline = True
                elif (("Energy range" in line
                       or "ENERGY INTEGRATED RESULTS" in line
                       or line.isspace())
                      and inmeshres):
                    nbmeshlines = 0
                    prev2meshline = True
                elif ("Energy range" not in line
                      and "ENERGY INTEGRATED RESULTS" not in line
                      and inmeshres and prev2meshline):
                    inmeshres = False
                    prev2meshline = False
                elif self.endflag in line and started_res:
                    if "PARA" not in sys.argv:
                        if batch_number != current_batch:
                            print("Edition batch,", batch_number,
                                  "different from current batch,",
                                  current_batch)
                            print("If no Edition batch keep current batch, "
                                  "else keep edition batch")
                            if batch_number < current_batch:
                                batch_number = current_batch
                        if current_batch == 0:
                            print("Current batch = 0, something to check ?")
                    else:
                        if greaterbatchnum > batch_number:
                            batch_number = greaterbatchnum
                    result.append(line)  # will change at end of the function
                    self.collres[batch_number] = ''.join(result)
                    result = []
                    started_res = False
                elif "NORMAL COMPLETION" in line:
                    self.normalend = True
                elif "WARNING" in line:
                    self.countwarnings += 1
                elif "ERROR" in line:
                    self.counterrors += 1
                elif "initialization time" in line:
                    self.initializationTime = int(line.split()[3])
                elif ("Type and parameters of random generator "
                      "at the end of simulation:" in line):
                    started_gen = True
                elif started_gen and "COUNTER" in line:
                    result.append(line)
                    self.lastGeneratorState = ''.join(result)
                    result = []
                    started_gen = False
                if started_res:
                    # if nbmeshlines%1000 == 0:
                    #     print("[34mIn start_res for nbmeshlines =",
                    #           nbmeshlines,"[0m")
                    # print("inmesh:", inmeshres, "nbmeshline:", nbmeshlines,
                    #       "meshlim:", self.meshlim,
                    #       "prevmeshline:", prevmeshline,
                    #       line.replace('\n', ''))
                    if inmeshres and nbmeshlines > self.meshlim:
                        if nbmeshlines == self.meshlim+1:
                            countMeshExceeding += 1
                            result.append("\n")
                            if countMeshExceeding < 5:
                                print("[31mToo much mesh lines, keeping",
                                      self.meshlim,
                                      "lines, if needed change meshlim arg[0m")
                        continue
                    result.append(line)
                if started_gen:
                    if "Type and parameters" not in line:
                        result.append(line)
                if (("PARA" in sys.argv and started_res and not gotBatchNumber
                     and "number of batches used" in line)):
                    newbatchnum = int(line.split()[4])
                    if greaterbatchnum < newbatchnum:
                        greaterbatchnum = newbatchnum
        print("Duration of loop over the file "
              "(no readlines, fill text in dict):",
              time.time()-start_time)
        print("Number of string 'BATCH' seen:", countBATCH)
        if countMeshExceeding > 4 :
            print("Number of mesh exceeding meshlim arg:",countMeshExceeding)

    def getResultsCollection(self):
        return self.collres

    @profile
    def getRequiredBatchNumber(self):
        return self.reqbatchs

    def getNormalEnd(self):
        return self.normalend

    def getNumberOfEditedBatchs(self):
        return len(self.collres)

    @profile
    def getLastEditedBatchNumber(self):
        # print(list(self.collres.keys()))
        return list(self.collres.keys())[-1]

    def getLastBatchResults(self):
        lastbn = self.getLastEditedBatchNumber()
        if lastbn != self.reqbatchs:
            print("[1;31mWARNING: last batch number", lastbn,
                  "!= required number of batchs", self.reqbatchs, "[0m")
        result = self.collres[lastbn]
        return result

    @profile
    def getAllBatchResults(self):
        # print(list(self.collres.keys()))
        return ''.join(self.collres.values())

    def getResultForBatch(self, batchnum):
        result = ""
        if batchnum not in self.collres.keys():
            print("Batch number", batchnum, "not found in edited btachs")
            return result
        result = self.collres[batchnum]
        return result

    def getLastGeneratorState(self):
        return self.lastGeneratorState

    def getInitializationTime(self):
        return self.initializationTime

    def printStatistics(self):
        print("Normal end of the jdd:", self.normalend)
        print("Number of warnings found:", self.countwarnings)
        print("Number of errors found:", self.counterrors)


if __name__ == "__main__":
    try:
        myfname = sys.argv[1]
    except IndexError:
        print("Argument needed: file name")
        exit(-1)

    lamres = Lamarque(myfname)
    myres = lamres.getResultsCollection()
    print(len(myres))
    if len(myres) > 10:
        for res in islice(myres, len(myres)-10, None):
            print(res, ":", myres[res], ",", end=" ")
        for res in islice(myres, 0, 3):
            print(res, ":", myres[res], ",", end=" ")
        print()
    else:
        print(myres)

    print("Will try to re-read the last batch of the file")
    start = myres[list(myres.keys())[-1]][0]
    print(start)
    end = myres[list(myres.keys())[-1]][1]

    if lamres.getNumberOfEditedBatch() > 1:
        print("Will try to re-read the last-1 batch of the file")
        start = myres[list(myres.keys())[-2]][0]
        print(start)
        end = myres[list(myres.keys())[-2]][1]
        start_time = time.time()
        with open(myfname) as fil:
            result = ''.join(fil.readlines()[start:end])
            # print(result)
        print("Duration of construction of string result from lines",
              time.time()-start_time)
        result2 = ""
        start_time = time.time()
        with open(myfname) as fil:
            for line in fil.readlines()[start:end]:
                result2 += line
        print("Duration of construction of string result from readlines",
              time.time()-start_time)

        # if result != test:
        #     print("[1;31mAAAAAAAARRRGGGG we are different ![0m")
        # else: print("[32mCool ! This is successful, we are identical ![0m")

    print("[35mTest other functions[0m")
    print("Did the jdd correctly finished (NORMAL COMPLETION):",
          lamres.getNormalEnd())
    print("Number of batchs required:", lamres.getRequiredBatchNumber())
    print("Number of batchs edited:", lamres.getEditedBatchNumber())
    print("Et les stats:")
    lamres.printStatistics()
    print("Get last batch")
    start_time = time.time()
    lastbatch = lamres.getLastBatchResults()
    print("Duration:", time.time()-start_time)
    print(len(lastbatch))
    print("Result for batch 1:")
    start_time = time.time()
    print("Readlines:", len(lamres.getResultForBatch(1)))
    print("Duration:", time.time()-start_time)
    print("Try to get all batchs")

    print(" - from dict")
    start_time = time.time()
    fullresdict = lamres.getAllBatchResults()
    print("Duration:", time.time()-start_time)
    print(len(fullresdict))
