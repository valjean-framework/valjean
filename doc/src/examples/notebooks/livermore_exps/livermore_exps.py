import numpy as np
from collections import OrderedDict
from valjean.eponine.dataset import Dataset


class LivermoreExps():
    '''Class to read experimental results from Livermore sphere (same file as
    in fortran tests.
    '''

    def __init__(self, path=("/data/tmplepp/el220326/QualTassadit/RC1/"
                             "MONO/qualtrip_main/elem/post_processing_main/"
                             "s10a11.res.mesure")):
        self.fname = path
        self.res = {}
        self.read_results()
        print("ALL KEYS:\n", list(self.res.keys()))

    def read_results(self):
        '''Read experimental results and stored them in dict as
        :obj:`numpy.ndarray`.
        '''
        charac = None
        results = None
        print(self.fname)
        with open(self.fname) as fil:
            for line in fil:
                if "MFP" in line or not line.split():
                    if charac:
                        print(charac)
                        self.save_res(charac, results)
                    charac = None
                    results = None
                    lelts = line.split()
                    charac = lelts[:-1]
                elif "DEGRES" in line:
                    charac.append(line.split()[1])
                elif "FP=" in line:
                    charac.append(float(line.split()[1]))
                elif "TEMPS" in line and "TO" in line:
                    results = []
                elif "CNT" in line or "prob" in line: # or "FP=" in line:
                    continue
                else:
                    results.append(tuple(np.fromstring(line, sep=' ')))

    def save_res(self, charac, results):
        '''Fill the internal dictionary for experimental results.

        ``{charac: results}``,
        with charac a tuple (element, thickness in mfp, detector angle)
        and results a :obj:`numpy.ndarray` with dtype:  ``[('time', int),
        ('cntPtimePsource', float), ('error', float), ('cntCum', float)]``
        '''
        # pylint: disable=no-member
        dtype = np.dtype({
            'names': ['time', 'cntPtimePsource', 'error', 'cntCum'],
            'formats': [np.float64, np.float64, np.float64, np.float64]})
        tmpres = np.array(results, dtype=dtype)
        self.res[tuple(charac[:-1])] = Dataset(
            tmpres['cntPtimePsource'], tmpres['error'],
            bins=OrderedDict([('t', tmpres['time'])]), name='data')
