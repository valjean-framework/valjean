# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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

In the case of a *rates* file, bins are set to groups index in most cases. When
the quantity is also calculated on anisotropies (e.g. diffusion) the bins are
``('anisotropies', 'groups')``. The surfacic flux (``'SURFFLUX'``) bins are
``('groups', 'surfaces')`` and the current (``'CURRENT'``) ones are
``('groups', 'surfaces', 'direction')``.

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
* :meth:`Picker.nb_anisotropies`: number of anisotropies available for a given
  result for the considered isotope in its zone and output
* :meth:`Picker.local_names`: list of names of the local values stored in a
  given zone from a given output folder
'''

import logging
from functools import lru_cache
from collections import OrderedDict
import h5py
import numpy as np

from ...chrono import Chrono
from ..dataset import Dataset
from ...cosette.rlist import RList


LOGGER = logging.getLogger(__name__)


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
        with Chrono() as chrono:
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

        The `'info'` group is not considered as a result (group containing the
        number of anisotropies), so it is omitted from of the results list.

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
        lres = [r for r in self.hfile[output][zone][isotope] if r != 'info']
        if isotope != 'macro':
            lres.append('concentration')
        return lres

    def nb_anisotropies(self, *, output, zone, isotope, result):
        '''Return number of anisotropies for the given configuration.

        :param str output: output folder considered
        :param str zone: zone from the output folder
        :param isotope: isotope considered for results (`'macro'` is
            counted as an isotope, if no isotope is given global results are
            given like flux or keff)
        :type isotope: str or None
        :param str result: result considered
        :rtype: list(str)
        '''
        isores = self.hfile[output][zone][isotope]
        if 'info' not in isores:
            return None
        if result in isores['info']:
            return isores['info'][result]['nbAnisotropy'][...][0]
        if 'nbAnisotropy' in isores['info']:
            return isores['info']['nbAnisotropy'][...][0]
        return 1

    def _make_dataset(self, data, name, bins=None):
        '''Build dataset from data.

        Data can be a scalar or an array.

        :param data: data to transform in :class:`Dataset`
        :type data: np.generic, np.ndarray
        :param int ngroups: number of groups
        :param int naniso: number of anisotropies
        :rtype: Dataset
        '''
        error = np.full_like(
            data, self.error_value,
            dtype=(float if np.isnan(self.error_value) else data.dtype))
        if not bins:
            return Dataset(value=data, error=error, what=name.lower())
        if 'anisotropies' in bins:
            nb_groups = len(bins['groups'])
            nb_aniso = len(bins['anisotropies'])
            return Dataset(value=data.reshape(nb_aniso, nb_groups),
                           error=error.reshape(nb_aniso, nb_groups),
                           what=name.lower(), bins=bins)
        if 'incident neutron groups' in bins:
            nb_groups = len(bins['groups'])
            nb_incg = len(bins['incident neutron groups'])
            return Dataset(value=data.reshape(nb_incg, nb_groups),
                           error=error.reshape(nb_incg, nb_groups),
                           what=name.lower(), bins=bins)
        return Dataset(value=data, error=error, what=name.lower(), bins=bins)

    @staticmethod
    def _make_bins(data_size, name, ngroups, naniso=None, nsurf=None):
        '''Make bins for the given data.

        :param int data_size: data size
        :param str name: data name
        :param int ngroups: number of energy groups
        :param int naniso: number of anisotropies
        :param int nsurf: number of surfaces
        :rtype: collections.OrderedDict
        '''
        if ngroups == 0:
            return None
        if ngroups == data_size:  # and (naniso is None or naniso == 1):
            return OrderedDict([('groups', np.arange(ngroups))])
        if name == 'SURFFLUX':
            return OrderedDict([('groups', np.arange(ngroups)),
                                ('surfaces', np.arange(nsurf))])
        if name == 'CURRENT':
            return OrderedDict([
                ('groups', np.arange(ngroups)),
                ('surfaces', np.arange(nsurf)),
                ('direction', np.array(['incoming', 'leaving']))])
        if name == 'MultigroupSpectrum':
            incgrps = data_size // ngroups
            return OrderedDict([
                ('incident neutron groups', np.arange(incgrps)),
                ('groups', np.arange(ngroups))])
        if ngroups * naniso != data_size:
            raise PickerException(
                f"Dataset size ({data_size}) not corresponding to "
                f"NG*Nanisotropies {ngroups}*{naniso} for {name}")
        return OrderedDict([('anisotropies', np.arange(naniso)),
                            ('groups', np.arange(ngroups))])

    def pick_standard_value(self, *, output, zone, result_name, isotope=None):
        '''Pick a result according to required parameters from a standard file
        (like keff, flux or rate).'''
        if result_name in ('KEFF', 'KINF', 'NSURF', 'MIGRATIONAREA', 'Buckling'):
            return self._make_dataset(
                self.hfile[output][zone][result_name][...][0], result_name)
        if not isotope:
            data = self.hfile[output][zone][result_name][...]
            nsurf = (self.hfile[output][zone]['NSURF'][...][0]
                     if 'NSURF' in self.hfile[output][zone] else None)
            bins = self._make_bins(data.size, result_name,
                                   self.nb_groups(output=output), nsurf=nsurf)
            return self._make_dataset(data, result_name, bins=bins)
        if result_name == 'concentration':
            iisot = self.isotopes(output=output, zone=zone).index(isotope)
            return self._make_dataset(
                self.hfile[output][zone]['CONCEN'][iisot], 'concentration')
        data = self.hfile[output][zone][isotope][result_name][...]
        bins = self._make_bins(
            data.size, result_name, self.nb_groups(output=output),
            self.nb_anisotropies(output=output, zone=zone, isotope=isotope,
                                 result=result_name))
        return self._make_dataset(data, result_name, bins)

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

    def pick_value_from_index(self, *, output, result_index, zone, name):
        '''Pick a user value result from required parameters.

        :param str output: output folder considered
        :param int result_index: index of the required result
        :param str zone: zone from the output folder
        :rtype: Dataset
        '''
        if zone is None:
            return self._make_dataset(
                self.hfile[output]['LOCALVALUE'][result_index][...], name)
        return self._make_dataset(
            self.hfile[output][zone]['LOCALVALUE'][result_index][...], name)

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
                self.hfile[output][zone][result_name][...], result_name)
        ilocal = self.local_names(output=output, zone=zone).index(result_name)
        return self.pick_value_from_index(output=output, result_index=ilocal,
                                          zone=zone, name=result_name)


class PickerException(Exception):
    '''An error that may be raised by the :class:`Picker` class.'''
