r'''This module is designed to pick the required results from an Apollo3
standard HDF5 output file. This means that the users should already know which
result they want to extract. Some navigation methods exist, but they are not
optimised for speed of access.

One possibility is to first explore the output file interactively with a
:class:`~.hdf5_reader.Reader`, and then to write the efficient code using
:class:`Picker`.


Picking results with :class:`Picker`
------------------------------------

.. code-block:: python

    from valjean.eponine.apollo3.hdf5_picker import Picker
    ap3p = Picker('MON_FICHIER.hdf')
    rate_ds = ap3p.pick_standard_value(output='OUTPUT_FOLDER',
                                       zone='ZONE_FOLDER',
                                       result_name='REQUIRED_RESULT')

For example to get the k\ :sub:`eff`, in ``output_1`` under ``totaloutput``:

.. code-block:: python

    keff = ap3p.pick_standard_value(output='output_1', zone='totaloutput',
                                    result_name='KEFF')

The result will be a :class:`~valjean.eponine.dataset.Dataset`. The error is
not available and it is set to ``numpy.nan`` by default. It can be changed
using the ``error_value`` to the :class:`Picker` constructor.

Results per isotopes can be obtained with an additional keyword argument, for
example for :sup:`10`\ B absorption in ``output_0`` from zone ``5``:

.. code-block:: python

    b10abs = ap3p.pick_standard_value(output='output_0', zone='5',
                                      result_name='Absorption', isotope='B10')

Macroscopic rates are obtained with ``isotope='macro'``.

Local values can also be retrived using the
:meth:`Picker.pick_user_value` method:

* if ``'LOCALNAME'`` and ``'LOCALVALUE'`` belong to zone names:

    .. code-block:: python

        locv = ap3p.pick_user_value(output='output', zone=None,
                                    result_name='LOCAL_VALUE_NAME')

* if ``'LOCALNAME'`` and ``'LOCALVALUE'`` belong to result names in a zone:

    .. code-block:: python

        locv = ap3p.pick_user_value(output='output', zone='totaloutput',
                                    result_name='LOCAL_VALUE_NAME')

* if ``'localvalue'`` belongs to zone names:

    .. code-block:: python

        locv = ap3p.pick_user_value(output='output', zone='localvalue',
                                    result_name='LOCAL_VALUE_NAME')

In both cases, it might be useful to check the zones and the local names first.


Quick exploration with :class:`Picker`
--------------------------------------

Some helpers exist if needed:

* :meth:`Picker.outputs`: list of output folders
* :meth:`Picker.geometry`: list of geometries stored in a given output folder
* :meth:`Picker.nb_groups`: number of energy groups available in a given output
  folder
* :meth:`Picker.zones`: list of zones in a given output folder
* :meth:`Picker.isotopes`: list of isotopes in a given zone of a given output
  folder
* :meth:`Picker.results`: list of available results in a given zone of a given
  output folder, isotope can be precised if needed
* :meth:`Picker.local_names`: list of names of the local values stored in a
  given zone from a given output folder
'''

from functools import lru_cache
import h5py
import numpy as np

from ... import LOGGER
from ...chrono import Chrono
from ..dataset import Dataset
from ...cosette.rlist import RList


class Picker:
    '''Pick selected values from an Apollo3 HDF5 file.'''

    CACHE_SIZE = 512

    def __init__(self, fname, error_value=np.nan):
        '''Initialize the :class:`Picker` object and read the HDF5 file.

        :param str fname: path to the Apollo3 HDF5 ouput file
        :param error_value: value to give to the error (default: ``numpy.nan``)
        :type error: int, float
        '''
        LOGGER.info('Reading %s', fname)
        self.error_value = error_value
        chrono = Chrono()
        with chrono:
            self.hfile = h5py.File(fname, 'r')
        LOGGER.info('HDF5 loading done in %f s', chrono)

    def close(self):
        '''Close HDF5 file.'''
        self.hfile.close()

    def geometry_from_geomid(self, *, geometry):
        '''Return geometry as a dictionary of zone names and volumes.

        :param str geometry: geometry name
        '''
        LOGGER.debug("In geometry_from_geomid")
        ageoms = {
            name.decode('UTF-8').strip(): vol
            for name, vol in zip(self.hfile['geometry'][geometry]['ZONENAME'],
                                 self.hfile['geometry'][geometry]['VOLUME'])}
        return ageoms

    def geometry(self, *, output):
        '''Return geometry characteristics (zones and their volumes) from the
        output name.

        :param str output: output in which zones will be found
        :rtype: dict
        '''
        return self.geometry_from_geomid(
            geometry=self.hfile['info'][output]['GEOMID'][...][0])

    def nb_groups(self, *, output):
        '''Return the number of groups for the `output`.

        :param str output: output in which zones will be found
        :rtype: int
        '''
        return self.hfile['info'][output]['NG'][...][0]

    def outputs(self):
        '''Return list of available outputs.

        :rtype: list(str)
        '''
        return [f for f in self.hfile if 'output' in f]

    def zones(self, *, output):
        '''Return list of available zones in `output`.

        :param str output: output in which zones will be found
        :rtype: list(str)
        '''
        return list(self.hfile[output])

    @lru_cache(maxsize=CACHE_SIZE)
    def isotopes(self, *, output, zone):
        '''Return list of available isotopes in `zone` from `output`.

        :param str output: output folder considered
        :param str zone: zone from output folder
        :rtype: list(str)
        '''
        if zone == 'totaloutput':
            return RList([], key=lambda x: x)
        if self.hfile[output][zone]['NISOT'][...][0] == 0:
            LOGGER.debug('No isotopes available in %s from %s', zone, output)
            if 'macro' in self.hfile[output][zone]:
                return RList(['macro'], key=lambda x: x)
            return RList([], key=lambda x: x)
        return RList([n.decode('UTF-8').strip()
                      for n in self.hfile[output][zone]['ISOTOPE']]
                     + ['macro'], key=lambda x: x)

    def results(self, *, output, zone, isotope=None):
        '''Return available results for the given configuration.

        :param str output: output folder considered
        :param str zone: zone from the output folder
        :param isotope: isotope considered for results (`'macro'` is
            counted as an isotope, if no isotope is given global results are
            given like flux or keff)
        :type isotope: str or None
        :rtype: list(str)
        '''
        if not isotope:
            lisot = set(self.isotopes(output=output, zone=zone))
            exkeys = lisot | {'NISOT', 'ISOTOPE', 'CONCEN', 'macro'}
            return [k for k in self.hfile[output][zone] if k not in exkeys]
        lres = list(self.hfile[output][zone][isotope])
        if isotope != 'macro':
            lres.append('concentration')
        return lres

    def _make_dataset(self, data):
        '''Build dataset from data.

        Data can be a scalar or an array.

        :param data: data to transform in :class:`Dataset`
        :type data: np.generic, np.ndarray
        :rtype: Dataset
        '''
        if len(data.shape) > 1:
            raise PickerException('Multiple dimensions array not already '
                                  'supported')
        return Dataset(value=data,
                       error=np.full_like(data, self.error_value,
                                          dtype=(float
                                                 if np.isnan(self.error_value)
                                                 else data.dtype)))

    def pick_standard_value(self, *, output, zone, result_name, isotope=None):
        '''Pick a result according to required parameters from a standard file
        (like keff, flux or rate).'''
        if result_name == 'KEFF':
            return self._make_dataset(
                self.hfile[output][zone][result_name][...][0])
        if not isotope:
            return self._make_dataset(
                self.hfile[output][zone][result_name][...])
        if result_name == 'concentration':
            iisot = self.isotopes(output=output, zone=zone).index(isotope)
            return self._make_dataset(
                self.hfile[output][zone]['CONCEN'][iisot])
        return self._make_dataset(
            self.hfile[output][zone][isotope][result_name][...])

    @lru_cache(maxsize=CACHE_SIZE)
    def local_names(self, *, output, zone):
        '''Return the list of available local value names.

        .. note::

            The most common zones seem to be in this case: `'totaloutput'`
            (especially in rates files), `None` or `'localvalue'` in core
            files.

        :param str output: output folder considered
        :param zone: zone from the output folder
        :type zone: str or None
        :rtype: list(str)
        '''
        if not zone:
            return RList([n.decode('UTF-8').strip()
                          for n in self.hfile[output]['LOCALNAME']],
                         key=lambda x: x)
        return RList([n.decode('UTF-8').strip()
                      for n in self.hfile[output][zone]['LOCALNAME']],
                     key=lambda x: x)

    def pick_value_from_index(self, *, output, result_index, zone):
        '''Pick a user value result from required parameters.

        :param str output: output folder considered
        :param int result_index: index of the required result
        :param str zone: zone from the output folder
        :rtype: Dataset
        '''
        if zone is None:
            return self._make_dataset(
                self.hfile[output]['LOCALVALUE'][result_index][...])
        return self._make_dataset(
            self.hfile[output][zone]['LOCALVALUE'][result_index][...])

    def pick_user_value(self, *, output, result_name, zone):
        '''Pick a user value result from required parameters (under local value
        in the file).

        :param str output: output folder considered
        :param str result_name: name of the required result
        :param str zone: zone from the output folder
        :rtype: Dataset
        '''
        if zone == 'localvalue':
            return self._make_dataset(
                self.hfile[output][zone][result_name][...])
        ilocal = self.local_names(output=output, zone=zone).index(result_name)
        return self.pick_value_from_index(output=output, result_index=ilocal,
                                          zone=zone)


class PickerException(Exception):
    '''An error that may be raised by the :class:`Picker` class.'''
