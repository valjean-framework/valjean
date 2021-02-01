'''Module performing a scan of Tripoli-4 output listing in order to only keep
relevant parts of it = results to be used for V&V or analysis or the run.

Summary
-------

* Quickly reads the results file
* Recognize beginning and end of results sections
* Get the required number of batchs
* Get the edition batch numbers (if exists)


Use of :mod:`~valjean.eponine.tripoli4.scan`
-----------------------------------------------

.. doctest:: scan
    :hide:

    >>> import os
    >>> work_dir = 'scan'
    >>> os.mkdir(work_dir)
    >>> with open(os.path.join(work_dir, 'spam.res'), 'w') as tmpfile:
    ...     print("BATCH 10\\n"
    ...           "initialization time (s): 7\\n"
    ...           " batch number : 10\\n"
    ...           "RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00\\n"
    ...           "Edition after batch number : 10\\n"
    ...           "simulation time (s) : 1\\n"
    ...           "NORMAL COMPLETION",
    ...           file=tmpfile)

To use this module you need to create a :class:`Scanner` object giving at least
the path to the file you want to read. This file should be a Tripoli-4 output
containing at least the flags precised in :ref:`eponine-t4-scan-caveats`.

    >>> import os
    >>> from valjean.eponine.tripoli4.scan import Scanner
    >>> results = Scanner(os.path.join(work_dir, 'spam.res'))
    >>> results.normalend
    True
    >>> len(results)
    1
    >>> results.times['initialization_time']
    7

    The expected key of the :class:`Scanner` object is the batch number, not an
    index. If you have the index you need to obtain the corresponding batch
    number first.

    >>> 'simulation time' in results[10]  # batch number = 10
    True
    >>> 'simulation time' in results[-1]  # -1 can only be an index, like 0
    Traceback (most recent call last):
        ...
    KeyError: -1
    >>> 'simulation time' in results[results.batch_number(-1)]
    True

.. note::

   It will probably be better to directly load a test file...


.. _eponine-t4-scan-caveats:

Caveats
-------

Beginning and end of results sections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Important for the scan: results will be kept

* **from** "RESULTS ARE GIVEN"
* **to** an end flag available in the list ``Scanner.end_flags``.
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

Module API
----------
'''

from collections.abc import Mapping
from collections import OrderedDict


from ... import LOGGER


# get profile from globals (cleaner)
if 'profile' not in globals()['__builtins__']:
    def profile(fmem):
        '''Deactivate profiling if not required in command line.'''
        return fmem


class PhEmEpBalanceOutput:
    '''Class to store photon-electron-positron balance.'''

    def __init__(self):
        self.content = []
        self.in_phemep = False
        self.count = 0

    def _count(self, line):
        if "Total" in line:
            self.count += 1
            if self.count == 3:
                self.in_phemep = False

    def add_line(self, line):
        '''Add line to the photon electron positron output and counts.'''
        self.content.append(line)
        self._count(line)


class HomogMatOutput:
    '''Class to store the homogenized material output.'''

    def __init__(self):
        self.content = []
        self.in_dump = False
        self.nb_groups = 0
        self.counting = False
        self.nb_corr_lines = 0

    def _count(self, line):
        '''Count the number of bins for the homogenized material dump.'''
        if self.counting:
            if self.nb_corr_lines > 0:
                self.nb_corr_lines += 1
            elif line[0].isdigit():
                self.nb_groups += 1
        if 'dump total section :' in line:
            self.counting = True
        elif 'dump absorption section :' in line:
            self.counting = False
        elif "correlation between absorption and total cross section" in line:
            self.nb_corr_lines += 1
            self.counting = True
        elif self.nb_corr_lines > self.nb_groups:
            self.counting = False
            self.in_dump = False

    def add_line(self, line):
        '''Add line to the homogenized material output and count.'''
        self.content.append(line)
        self._count(line)


class BatchResultScanner:
    # pylint: disable=too-many-instance-attributes
    '''Class to build batchs collection.

    :param int count_excess: current count of meshes
    :param int current_batch: current batch number
    :param int mesh_limit: limit of number of lines of mesh
    :param str line: current line in file

    .. note::

      * **current_batch** normally refers to lines before flag
        "RESULTS ARE GIVEN". They can be used if "Edition after batch number"
        does not appear in the file.
      * **line** should contain "RESULTS ARE GIVEN" here. It is used to
        initialize the list of strings corresponding to the result block.

    '''

    def __init__(self, count_excess, current_batch, mesh_limit, para, line):
        # pylint: disable=too-many-arguments
        self.count_mesh_exceeding = count_excess
        self.batch_counts = {'number': -1,
                             'current': current_batch,
                             'greater': 0}
        self.result = [line]
        self.para = para
        self.mesh_limit = mesh_limit
        self.in_mesh = False
        self.nb_mesh_lines = 0
        self.prev_line_mesh = False
        self.phemep_balance = PhEmEpBalanceOutput()
        self.homog_mat = HomogMatOutput()

    def add_meshline(self, line):
        '''Add mesh line to result if stop mesh is not reached.

        :param int count_excess: counter for mesh lines excess
        :param list(str) result: batch result
        :param str line: mesh line
        '''
        if self.nb_mesh_lines > self.mesh_limit and self.mesh_limit != -1:
            if self.nb_mesh_lines == self.mesh_limit+1:
                self.count_mesh_exceeding += 1
                if self.count_mesh_exceeding < 5:
                    LOGGER.warning("Too much mesh lines, keeping %d "
                                   "lines, if needed change mesh_limit ",
                                   self.mesh_limit)
        else:
            self.result.append(line)

    def build_result(self, line):
        '''Scan line to build batch result: mainly deals with mesh
        specificities and store line.

        :param str line: last line to be taken into account
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
        elif '#'*64 in line and not self.phemep_balance.in_phemep:
            LOGGER.debug('phe+e- balance')
            self.phemep_balance.in_phemep = True
        elif "DUMP HOMOGENIZED MATERIAL" in line:
            LOGGER.debug("In DUMP HOMOGENIZED MATERIAL")
            self.homog_mat.in_dump = True
        if self.para and "number of batches used" in line:
            self._set_greater_batch_number(line)
        self._store_line(line)

    def _store_line(self, line):
        if self.in_mesh:
            self.add_meshline(line)
        elif self.phemep_balance.in_phemep:
            self.phemep_balance.add_line(line)
        elif self.homog_mat.in_dump:
            self.homog_mat.add_line(line)
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
        if not self.para:
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

        :return: string build from list of strings junction
        '''
        LOGGER.debug("END FLAG found, batch number = %d, "
                     "current batch = %d, greater batch = %d",
                     self.batch_counts['number'],
                     self.batch_counts['current'],
                     self.batch_counts['greater'])
        return ''.join(self.result)


class ScannerException(Exception):
    '''An error that may be raised by the :class:`Scanner` class.'''


class Scanner(Mapping):
    # pylint: disable=too-many-instance-attributes
    '''Class to scan the Tripoli-4 listing and keep the relevant parts of it
    like results per batch used for edition or times.

    There are no class variables, but instance variables (initialized when
    the object is built or when the file is read). They are directly accessible
    from the object. Main results are accessible directly from the
    :obj:`Scanner` object.

    **Instance variables:**

    `fname` (:class:`str`)
        name of the file that will be scanned

    `batches` (:class:`dict`)
        keep the number of batches and the packet_length
        (read from file `fname`)

    `normalend` (:class:`bool`)
        presence of "NORMAL COMPLETION"

    `end_flags` (:class:`list` (:class:`str`))
        possible end flags to stop the saving of results

    `mesh_limit` (:class:`int`)
        maximum lines of mesh to be stored

    `para` (:class:`bool`)
        `True` in parallel mode

    `countwarnings` (:class:`int`)
        count number of warnings (for statistics)

    `counterrors` (:class:`int`)
        count number of errors (for statistics)

    `times` (:class:`collections.OrderedDict`)
        save times (initialization, simulation, exploitation and elapsed if
        exists). Mandatory ones are ``'initialization time'`` and ``'simulation
        time'`` or ``'exploitation time'``. ``'elapsed time'`` only appears in
        listings from parallel jobs.

    `last_generator_state` (:class:`str`)
        keep the random generator state (not included in the result as given
        after `endflag`)

    `phemep_balance` (:class:`dict`)
        keep the photon electron positron balance as :class:`str` indexed by
        batch number

    `homog_mat` (:class:`dict`)
        keep the homogenized material dump as :class:`str` indexed by batch
        number


    **Available methods:**

    :class:`Scanner` inherits from :class:`collections.abc.Mapping` so many
    methods are implemented or available by default: ``keys``, ``items``,
    ``values``, ``get``, ``__contains__`` (used via ``in``). ``__getitem``
    (used with ``[]``), ``__iter__`` (when iterators are required), ``__len__``
    and ``__reversed__`` are redefined.

    This class points on the :obj:`collections.OrderedDict` that it contains.
    The keys are the available batch numbers in the Tripoli-4 output, obtained
    using ``scan_obj.keys()``.
    '''

    @profile
    def __init__(self, fname, mesh_lim=-1, end_flag=""):
        '''Initialize the instance from the file `fname`, meaning reads the
        file and store the relevant parts of it, i.e. result block for each
        batch edition.

        Results are stored in an internal :obj:`collections.OrderedDict`:
        ``{batch_number_1: 'result_1', batch_number_2: 'result_2', ...}``

        * ``batch_number_*`` is `int`
        * ``result_*`` is `str`
        * Order follows the listing order, so increasing ``batch_number``

        Members needed at initialization:

        :param str fname: name of the input file
        :param int mesh_lim: limit on number of lines to read in meshes outputs
                      (can be really long).

                      * default = -1, all cells will be read
                      * Minimum value is 1, use it to skip the mesh.
                      * If 0 is used, AssertException will be raised (else
                        parsing would fail)

        :param bool para: run in mono-processor or parallel mode
        :param str end_flag: end flag of the results block in Tripoli-4 listing
        '''
        self.fname = fname
        self.batches = {"batches": None,
                        "packet_length": 1}
        self.tasks = 1
        self.normalend = False
        self.end_flags = ["simulation time", "exploitation time",
                          "elapsed time"]
        if end_flag:
            self.end_flags.insert(0, end_flag)
        # keep mesh_lim as instance variable and not class variable to prevent
        # risk of changing its value for all instances of the class
        self.mesh_limit = mesh_lim
        self.para = False
        self.partial = False
        self.countwarnings = 0
        self.counterrors = 0
        self.times = OrderedDict()
        self.last_generator_state = ""
        self.phemep_balance = {}
        self.homog_mat = {}
        self._fatal_error = []
        self._collres = OrderedDict()
        self._get_collres()

    def _check_input_data(self, line):
        '''Get some parameters from introdcution of the results file, i.e.
        from the data file. Typically the number of batches required.
        '''
        if "BATCH" in line and '_' not in line and "THIS" not in line:
            indbatch = line.split().index('BATCH')
            self.batches["batches"] = (int(line.split()[indbatch+1])
                                       if len(line.split()) > 1
                                       else None)
        elif "number of tasks is" in line:
            self.para = True
            self.tasks = int(line.split()[5])
        elif "BATCH_PER_SIMULATOR" in line:
            self.batches["batches"] = (int(line.split()[1])
                                       * (self.tasks-2
                                          if self.tasks > 1 else 1))
        elif "PACKET_LENGTH" in line:
            LOGGER.info("Batchs grouped by packets -> "
                        "number of batchs expected divided "
                        "by PACKET_LENGTH in PARA")
            indpacket = line.split().index('PACKET_LENGTH')
            if self.para:
                self.batches["packet_length"] = int(line.split()[indpacket+1])
            LOGGER.debug("Packet length = %d", self.batches["packet_length"])
        elif "initialization time" in line:  # correspond to end of data file
            self.times['initialization_time'] = int(line.split()[3])

    def _is_end_flag(self, line):
        # len(end_flags) == 3: default list, no user's end flag added
        if "time" not in line and len(self.end_flags) == 3:
            return None
        for end_flag in self.end_flags:
            if end_flag in line:
                return end_flag
        return None

    def _add_time(self, end_flag, line):
        batch_number = next(reversed(self._collres)) if self._collres else 0
        eflag = end_flag.replace(' ', '_')
        time = (int(line.split()[-1]) if line.split()[-1].isdigit()
                else "Not a time")
        self.times.setdefault(eflag, {}).setdefault(batch_number, time)
        if self.times[eflag][batch_number] != time and 'time' in end_flag:
            if self.partial:
                LOGGER.warning("Partial edition: %s set to last found", eflag)
                self.times[eflag][batch_number] = time
            else:
                LOGGER.warning("More than one %s found for the same batch, %s",
                               eflag, batch_number)

    def _set_counters_and_flags(self, line):
        if "WARNING" in line:
            self.countwarnings += 1
        elif "ERROR" in line:
            self.counterrors += 1
            if "FATAL ERROR" in line:
                self._fatal_error = ["fatal error in TRIPOLI-4:\n\n"]
        elif "PARTIAL EDITION" in line:
            self.partial = True
        elif "NORMAL COMPLETION" in line:
            self.normalend = True

    def _additional_outputs(self, batch_scan):
        bnum = batch_scan.batch_counts['number']
        if batch_scan.phemep_balance.count == 3:
            self.phemep_balance[bnum] = ''.join(
                batch_scan.phemep_balance.content)
        if (batch_scan.homog_mat.nb_corr_lines != 0
                and not batch_scan.homog_mat.in_dump):
            self.homog_mat[bnum] = ''.join(batch_scan.homog_mat.content)

    @profile
    def _get_collres(self):
        # pylint: disable=too-many-branches
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
                if line.lstrip().startswith("!!!"):
                    continue
                self._set_counters_and_flags(line)
                if _batch_scan:
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
                        self._additional_outputs(_batch_scan)
                        _batch_scan = None
                        # ordered dictionary -> unique keys, so only last kept
                        self._add_time(end_flag, line)
                        continue
                elif self._fatal_error:
                    self._fatal_error.append(line)
                elif not self.times:
                    self._check_input_data(line)
                    continue
                elif "RESULTS ARE GIVEN" in line:
                    _batch_scan = BatchResultScanner(
                        count_mesh_exceeding, current_batch,
                        self.mesh_limit, self.para, line)
                elif (self.partial and line.startswith(' number of batch')
                      or line.startswith(' batch number :')):
                    current_batch = int(line.split()[-1])
                elif self._is_end_flag(line):
                    check_current_batch = (
                        current_batch == list(self._collres.keys())[-1]
                        if self._collres else False)
                    if not self.para and not check_current_batch:
                        continue
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
        if count_mesh_exceeding > 4:
            LOGGER.warning("Number of mesh exceeding mesh_limit arg: %d",
                           count_mesh_exceeding)
        if not self._collres and _batch_scan:
            raise ScannerException("No scan result built: "
                                   "no end flag found in the file")

    def __getitem__(self, batch_number):
        '''Get result corresponding to batch_number.

        A warning is printed if the last batch_number doesn't correspond to
        the number of batchs required.

        :param int batch_number: batch number (>0), corresponding the keys of
            Scanner.
        :raises KeyError: if ``batch_number`` does not exist (for example if
            confusion between ``batch_number`` and ``batch_index`` using -1 or
            0)

        Use: ``Scanner[X]``
        '''
        LOGGER.debug("__getitem__, batch number = %d", batch_number)
        try:
            return self._collres[batch_number]
        except KeyError:
            message = ("Wrong batch number required, batch number {} doesn't "
                       "exist, please change it to an existing one."
                       .format(batch_number))
            LOGGER.error(message)
            raise

    def __iter__(self):
        '''Iteration over the collection of results, on the keys to match
        :obj:`dict` and :obj:`collections.OrderedDict` behaviour.
        '''
        yield from self._collres.__iter__()

    def __len__(self):
        '''Return length of the collection of results, equivalent to get the
        number of edited batchs.
        '''
        return len(self._collres)

    def __reversed__(self):
        '''Reversed the :obj:`collections.OrderedDict` order (easier to get
        last element).
        '''
        yield from self._collres.__reversed__()

    def batch_index(self, batch_number):
        '''Get the index of the batch_number in the results list.'''
        return list(self._collres.keys()).index(batch_number)

    def batch_number(self, batch_index):
        '''Get the batch number from the batch index.'''
        return list(self.keys())[batch_index]

    def fatal_error(self):
        '''Return the fatal error message if found.'''
        return ''.join(self._fatal_error)

    def global_variables(self, batch_number):
        '''Return a dictionary of the global quantities in the TRIPOILI-4
        output:

        * warnings
        * errors
        * number of tasks (to distinguish MONO and PARA for example)
        * normal end
        * required batches
        * partial (if the job as been stopped)
        * batch number, especially when 'edition after batch number' is not in
          the TRIPOLI-4 output
        * t4_file: path to the scanned file
        * times of the required batch (can be simulation time, initialisation
          time, elapsed time)

        :param int batch_number: batch number (used for times)
        :rtype: dict
        '''
        gvars = {'warnings': self.countwarnings,
                 'errors': self.counterrors,
                 'number_of_tasks': self.tasks,
                 'normal_end': self.normalend,
                 'required_batches': (self.batches["batches"]
                                      // self.batches["packet_length"]
                                      if self.batches["batches"] is not None
                                      else None),
                 'partial': self.partial,
                 'batch_number': batch_number,
                 't4_file': self.fname}
        for ktime, val in self.times.items():
            gvars[ktime] = val if isinstance(val, int) else val[batch_number]
        return gvars

    def print_statistics(self):
        '''Print statistics of the listing scanned: normal end, number of
        warnings and errors.
        '''
        print("Normal end of the jdd:", self.normalend)
        print("Number of warnings found:", self.countwarnings)
        print("Number of errors found:", self.counterrors)

    def check_times(self):
        '''Check times.

        If the results come from a parallel job, the *times* dictionary should
        contain the ``'elapsed_time'`` key.
        In all kind of outputs or ``'simulation_time'`` or
        ``'exploitation_time'`` should be found (in parallel case the only
        possibility is in reality ``'simulation_time'``).
        Finally, while ``'initialization_time'`` value is an *int* as occuring
        only once, the others are lists with length equal to the number of
        batches in the edition for ``'simulation_time'`` and
        ``'exploitation_time'`` and equal to the number of batches + 1 for
        ``'elapsed_time'``.
        If all these checks are successful True is returned, else False.

        :rtype: bool
        '''
        if self.para:
            if 'elapsed_time' not in self.times:
                return False
            if self.partial:
                return True
        setimes = {'simulation_time', 'exploitation_time'}
        if not setimes.intersection(self.times):
            return False
        for time, times in self.times.items():
            if time in setimes and len(times) != len(self):
                LOGGER.error("Number of %s not matching: %d for %d editions",
                             time, len(times), len(self))
                return False
            if time == 'elapsed_time' and len(times) != len(self)+1:
                LOGGER.error("Number of elasped_time not matching: %d"
                             "(N+1 editions expected, %d editions)",
                             len(times), len(self))
                return False
        return True
