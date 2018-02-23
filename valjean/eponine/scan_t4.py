'''
Module performing a scan of Tripoli-4 output listing in order to only keep
relevant parts of it = results to be used for V&V or analysis or the run.

Summary
-------

* Quickly reads the results file
* Recognize beginning and end of results sections
* Get the required number of batchs
* Get the edition batch numbers (if exists)


Use of ``scan_t4``
------------------

To use ``scan_t4`` you need to create a :class:`Scan` object giving at least
the path to the file you want to read. This file should be a Tripoli-4 output
containing at least the flags precised in :ref:`eponine-scan_t4-caveats`.

.. testsetup:: scan_t4

   from valjean.eponine.scan_t4 import Scan
   import os
   work_dir = os.path.join(doctest_tmpdir, 'scan_t4')
   os.mkdir(work_dir)
   tmpfile = open(os.path.join(work_dir, 'spam.res'), 'w')
   tmpfile.write("BATCH 10\\n")
   tmpfile.write("initialization time (s): 7\\n")
   tmpfile.write(" batch number : 10\\n")
   tmpfile.write("RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00\\n")
   tmpfile.write("Edition after batch number : 10\\n")
   tmpfile.write("simulation time (s) : 1\\n")
   tmpfile.write("NORMAL COMPLETION")
   tmpfile.close()


.. doctest:: scan_t4

   >>> import os
   >>> results = Scan(os.path.join(work_dir, 'spam.res'))
   >>> results.normalend
   True
   >>> len(results)
   1
   >>> results.times['initialization time']
   7
   >>> 'simulation time' in results[-1]
   True

.. note::

   It will probably be better to directly load a test file...


.. _eponine-scan_t4-caveats:

Caveats
-------

Beginning and end of results sections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Important for the scan: results will be kept

* **from** "RESULTS ARE GIVEN"
* **to** an end flag available in the list :py:attr:`Scan.END_FLAGS`.
  Possibilities are:

  * Default end flag is ``"simulation time"``;
  * For exploitation jobs use ``"exploitation time"`` (example: Green bands);
  * for jobs running in parallel, ``"elapsed time"`` will also appear, after
    ``"simulation time"`` normal.


Mesh results
^^^^^^^^^^^^
Mesh results can be really long, so they can be long to read and mainly,
afterwards to parse. If meshes are not used in the rest of the job
(for example: you are only interested in integrated results), a limit can be
set on the number of lines read using the argument ``mesh_limit``:

* ``mesh_limit`` can take all values except 0.
* Default is -1: all the lines of mesh result will be read
* Else **Minimum is 1**: to avoid crash in parsing as it needs to parse at
  least one line of mesh result


Others
------

Memory profiling is available using memory_profiler::

  mprof run --python python3 scan.py FILE
  mprof plot

'''

import sys
from collections.abc import Mapping
from collections import OrderedDict
import logging


LOGGER = logging.getLogger('valjean')


LOGGER.info("sys.argv: %s", str(sys.argv))


# get profile from globals (cleaner)
if 'profile' not in globals()['__builtins__']:
    def profile(fmem):
        '''Deactivate profiling if not required in command line.'''
        return fmem


class BatchResultScanner:
    '''Class to build batchs collection.

    :param count_excess: current count of meshes
    :type count_excess: int
    :param current_batch: current batch number
    :type current_batch: int
    :param mesh_limit: limit of number of lines of mesh
    :type mesh_limit: int
    :param line: current line in file
    :type line: str

    .. note::

      * **current_batch** normally refers to lines before flag
        "RESULTS ARE GIVEN". They can be used if "Edition after batch number"
        does not appear in the file.
      * **line** should contain "RESULTS ARE GIVEN" here. It is used to
        initialize the list of strings corresponding to the result block.

    '''
    def __init__(self, count_excess, current_batch, mesh_limit, line):
        self.count_mesh_exceeding = count_excess
        self.batch_counts = {'number': -1,
                             'current': current_batch,
                             'greater': 0}
        self.result = [line]
        self.in_mesh = False
        self.mesh_limit = mesh_limit
        self.nb_mesh_lines = 0
        self.prev_line_mesh = False

    def add_meshline(self, line):
        '''Add mesh line to result if stop mesh is not reached.

        :param count_excess: counter for mesh lines excess
        :type count_excess: int
        :param result: batch result
        :type result: list of strings
        :param line: mesh line
        :type line: string
        '''
        if self.nb_mesh_lines > self.mesh_limit and self.mesh_limit != -1:
            if self.nb_mesh_lines == self.mesh_limit+1:
                self.count_mesh_exceeding += 1
                if self.count_mesh_exceeding < 5:
                    LOGGER.warning("[31mToo much mesh lines, keeping %d "
                                   "lines, if needed change mesh_limit [0m",
                                   self.mesh_limit)
        else:
            self.result.append(line)

    def build_result(self, line):
        '''Scan line to build batch result: mainly deals with mesh
        specificities and store line.

        :param line: last line to be taken into account
        :type line: string
        '''
        if self.in_mesh:
            if "(" in line and ")" in line and "," in line:
                self.nb_mesh_lines += 1
                self.prev_line_mesh = True
                if ((self.mesh_limit != -1
                     and self.nb_mesh_lines > self.mesh_limit+2)):
                    return
            elif "****" in line:
                self.in_mesh = False
            elif line.isspace() and self.prev_line_mesh:
                self.prev_line_mesh = False
                self.nb_mesh_lines = 0
        elif "Edition after batch number" in line:
            self.batch_counts['number'] = int(line.split()[-1])
        elif "Results on a mesh" in line:
            self.in_mesh = True
            assert self.mesh_limit != 0
        if "PARA" in sys.argv and "number of batches used" in line:
            self._set_greater_batch_number(line)
        self._store_line(line)

    def _store_line(self, line):
        if self.in_mesh:
            self.add_meshline(line)
        else:
            self.result.append(line)

    def _set_greater_batch_number(self, line):
        newbatch = int(line.split()[4])
        if self.batch_counts['greater'] < newbatch:
            self.batch_counts['greater'] = newbatch

    def check_batch_number(self):
        '''Check batch number value and replace it by current value or by the
        greater value if needed.
        '''
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

    def get_result(self):
        '''Send result.
        Called if end flag has been found, add last line and concatenates
        result.

        :return: string build from lsit of strings junction
        '''
        LOGGER.debug("[1;31mEND FLAG found, batch number = %d, "
                     "current batch = %d, greater batch = %d[0m",
                     self.batch_counts['number'],
                     self.batch_counts['current'],
                     self.batch_counts['greater'])
        return ''.join(self.result)


class Scan(Mapping):
    '''Class to keep marks on the file

    Members needed at initialization:

    :param fname: name of the input file
    :type fname: string
    :param endflag: end flag of the results block in Tripoli-4 listing
    :type endflag: string
    :param mesh_limit: limit on number of lines to read in meshes outputs
                      (can be really long).

                      * default = -1, all cells will be read
                      * Minimum value is 1, use it to skip the mesh.
                      * If 0 is used, AssertException will be raised (else
                        parsing would fail)

    :type mesh_limit: int
    '''
    END_FLAGS = ["simulation time", "exploitation time", "elapsed time"]

    @profile
    def __init__(self, fname, mesh_lim=-1):
        '''Initialize the instance from the file `fname`, meaning reads the
        file and store the relevant parts of it, i.e. result block for each
        batch edition.

        Results are stored in an internal `OrderedDict`:
        ``{batch_number_1: 'result_1', batch_number_2: 'result_2', ...}``

        * `batch_number` is `int`
        * `result` is `str`
        * Order follows the listing order, so increasing `batch_number`

        :ivar reqbatchs: number of batchs required (read from file fname)
        :type reqbatchs: int
        :ivar normalend: presence of "NORMAL COMPLETION"
        :type normalend: bool
        :ivar countwarnings: count number of warnings (for statistics)
        :type countwarnings: int
        :var counterrors: count number of errors (for statistics)
        :type counterrors: int
        :ivar dict times: save times (initialization, simulation, exploitation
                          and elapsed if exists). Mandatory ones are
                          ``'initialization time'`` and ``'simulation time'``
                          or ``'exploitation time'``. ``'elapsed time'`` only
                          appears in listings from parallel jobs.
        :var last_generator_state: keep the random generator state (not
                                     included in the result as given after
                                     `endflag`)
        :type last_generator_state: string
        '''
        self.fname = fname
        self.reqbatchs = -1
        self.normalend = False
        # keep mesh_lim as instance variable and not class variable to prevent
        # risk of changing its value for all instances of the class
        self.mesh_limit = mesh_lim
        self.countwarnings = 0
        self.counterrors = 0
        self.times = OrderedDict()
        self.last_generator_state = ""
        self._collres = OrderedDict()
        self._get_collres()

    @classmethod
    def debug_scan(cls, fname, mesh_lim=-1, end_flag=""):
        '''Debug constructor, adding possibilty to use a custom end flag.

        :param str fname: path to the file to scan
        :param int mesh_lim: limit on number of lines of mesh to read
        :param str end_flag: end flag on which ending scanning
        :returns: instance of :class:`Scan`.
        '''
        if end_flag:
            cls.END_FLAGS.insert(0, end_flag)
        print(cls.END_FLAGS)
        return cls(fname, mesh_lim)

    def _check_input_data(self, line):
        '''Get some parameters from introdcution of the results file, i.e.
        from the data file. Typilcally the number of batchs required.
        '''
        if "BATCH" in line and '_' not in line and "THIS" not in line:
            indbatch = line.split().index('BATCH')
            self.reqbatchs = int(line.split()[indbatch+1])
        elif "PACKET_LENGTH" in line:
            LOGGER.info("[1mBatchs grouped by packets -> "
                        "number of batchs expected divided "
                        "by PACKET_LENGTH in PARA[0m")
            indpacket = line.split().index('PACKET_LENGTH')
            if "PARA" in sys.argv:
                self.reqbatchs //= int(line.split()[indpacket+1])
            LOGGER.debug("new number of batchs = %d", self.reqbatchs)
        elif "initialization time" in line:  # correspond to end of data file
            self.times['initialization time'] = int(line.split()[3])

    def _is_end_flag(self, line):
        # len(END_FLAGS) = 3: default list, no user's end flag added
        if "time" not in line and len(self.END_FLAGS) == 3:
            return
        for end_flag in self.END_FLAGS:
            if end_flag in line:
                return end_flag

    def _add_time(self, end_flag, line):
        self.times[end_flag] = (int(line.split()[-1])
                                if line.split()[-1].isdigit()
                                else "Not a time")

    @profile
    def _get_collres(self):
        '''Read the file and store all relevant information.
        '''
        count_mesh_exceeding = 0
        generator_state = []
        current_batch = 0
        _batch_scan = None
        with open(self.fname, errors='ignore') as fil:
            for line in fil:
                if line.lstrip().startswith("//"):  # comment in the jdd
                    continue
                elif _batch_scan:
                    _batch_scan.build_result(line)
                    end_flag = self._is_end_flag(line)
                    if end_flag:
                        LOGGER.debug('end flag "%s" found', end_flag)
                        # check batch number has to be before get result to
                        # modify batch number before storage if necessary...
                        _batch_scan.check_batch_number()
                        batch_number = _batch_scan.batch_counts['number']
                        self._collres[batch_number] = _batch_scan.get_result()
                        count_mesh_exceeding = _batch_scan.count_mesh_exceeding
                        _batch_scan = None
                        # ordered dictionary -> unique keys, so only last kept
                        self._add_time(end_flag, line)
                    continue
                elif not self.times:
                    self._check_input_data(line)
                    continue
                elif "RESULTS ARE GIVEN" in line:
                    _batch_scan = BatchResultScanner(
                        count_mesh_exceeding, current_batch,
                        self.mesh_limit, line)
                elif line.startswith(' batch number :'):
                    current_batch = int(line.split()[-1])
                elif "WARNING" in line:
                    self.countwarnings += 1
                elif "ERROR" in line:
                    self.counterrors += 1
                elif self._is_end_flag(line):
                    # still needed to be sure "elapsed time" appears in
                    # parallel jobs
                    self._add_time(self._is_end_flag(line), line)
                elif ("Type and parameters of random generator "
                      "at the end of simulation:" in line):
                    generator_state.append('')
                    continue
                elif generator_state:
                    generator_state.append(line)
                    if "COUNTER" in line:
                        self.last_generator_state = ''.join(generator_state)
                        generator_state = []
                elif "NORMAL COMPLETION" in line:
                    self.normalend = True
        if count_mesh_exceeding > 4:
            LOGGER.warning("Number of mesh exceeding mesh_limit arg: %d",
                           count_mesh_exceeding)

    def __getitem__(self, batch_number):
        '''Get result corresponding to batch_number.

        If `batch_number` == -1 return the last result.
        A warning is printed if the last batch_number doesn't correspond to
        the number of batchs required.

        Use: ``Scan[X]``
        '''
        LOGGER.debug("__getitem__, batch number = %d", batch_number)
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
        '''Iteration over the collection of results, on the keys to match
        `dict` and `OrderedDict` behaviour.
        '''
        yield from self._collres.__iter__()

    def __len__(self):
        '''Return length of the collection of results, equivalent to get the
        number of edited batchs.
        '''
        return len(self._collres)

    def __reversed__(self):
        '''Reversed the `OrderedDict` order (easier to get last element).'''
        yield from self._collres.__reversed__()

    @profile
    def get_last_edited_batch_number(self):
        '''Return last edited batch number'''
        return list(self._collres.keys())[-1]

    @profile
    def get_all_batch_results(self):
        '''Return all batchs results in one string, to be parsed in once.'''
        return ''.join(self._collres.values())

    def print_statistics(self):
        '''Print statistics of the listing scanned: normal end, number of
        warnings and errors.
        '''
        print("Normal end of the jdd:", self.normalend)
        print("Number of warnings found:", self.countwarnings)
        print("Number of errors found:", self.counterrors)
