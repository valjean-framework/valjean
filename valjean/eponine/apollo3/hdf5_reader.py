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

'''This module is designed to read all results contained an standard HDF5
output file from Apollo3 (with keff, fluxes and rates) and to store them in
memory as a :class:`~valjean.eponine.browser.Browser`. This makes it possible
to explore the content of the file using the facilities provided by
:class:`~valjean.eponine.browser.Browser`.

.. note::

    The main limitation is on speed, especially if the HDF5 file is big or
    contains a lot of nested groups. In that case, if you do not need to
    explore the file and you know exactly which results will be used, use
    :class:`~valjean.eponine.apollo3.hdf5_picker.Picker` instead.


Data models of Apollo3 HDF5 files
---------------------------------

The Apollo3 HDF5 output files mainly follow the standard data model, initially
designed for reaction rates, which is structured as follows:

.. code-block::

    ┌─ info ─┬─ (COMMENT)
    │        ├─ NOUT
    │        ├─ output_id1 ┬─ GEOMID
    │        │             ├─ NG
    │        │             └─ COMMENT
    │        ├─ output_id2 ┄
    │        ┆
    │        ┆
    │        └─ output_idNOUT ┄
    │
    ├─ geometry ─┬─ NGEO
    │            ├─ geometry_id1 ┬─ NZONE
    │            │               ├─ VOLUME[NZONE]
    │            │               └─ ZONENAME[NZONE]
    │            ├─ geometry_id2 ┄
    │            ┆
    │            ┆
    │            └─ geometry_idNGEO ┄
    │
    ├─ output_id1 ─┬─ totaloutput ─┬─ KEFF (float)
    │              │               ├─ (KINF (float))
    │              │               ├─ (ABSORPTION[NG])
    │              │               ├─ (CURRENT[NG])
    │              │               ├─ (FLUX[NG])
    │              │               ├─ (MIGRATIONAREA (float))
    │              │               ├─ (PRODUCTION[NG])
    │              │               ├─ (NVAL)
    │              │               ├─ (LOCALVALUE[NVAL])
    │              │               ├─ (LOCALNAME[NVAL])
    │              │               └─ (localvalue) ─┬─ LOCALNAME[NVAL]
    │              │                                ├─ value_id1
    │              │                                ├─ value_id2
    │              │                                ┆
    │              │                                ┆
    │              │                                └─ value_idNVAL
    │              ├─ zone_id_1 ─┬─ NISOT
    │              │             ├─ ISOTOPE[NISOT]
    │              │             ├─ CONCEN[NISOT]
    │              │             ├─ FLUX[NG]
    │              │             ├─ macro ─┬─ reaction_id[NG]
    │              │             │         ├─┄
    │              │             │         ┆
    │              │             │
    │              │             ├─ isotope_id1 ─┬─ reaction_id[NG]
    │              │             │               ├─┄
    │              │             │               ┆
    │              │             │               ┆
    │              │             │
    │              │             ├─ isotope_id2 ┄
    │              │             ┆
    │              │             ┆
    │              │             └─ isotope_idNISOT ┄
    │              ├─ zone_id2 ┄
    │              ┆
    │              ┆
    │              └─ zone_idNZONE ┄
    ├─ output_id2 ┄
    ┆
    ┆
    └─ output_idNOUT ┄

Elements in brackets are optional. If ``NISOT == 0``, the ``ISOTOPE``,
``CONCEN`` and ``isotope_id`` groups will be absent. The ``macro`` group
stores the macroscopic reaction rates (= reaction rates for a medium). The
``zone_id`` folder names appear as values in the ZONENAME dataset in the
geometry group, and they are arbitrary strings (chosen by the user in the
Apollo3 case). ``VOLUME`` stores the volumes (in cm³) of the zones, if needed
later for normalisation for example. Most physics quantities are given on
``NG`` energy groups but the group bounds are not stored in the file. Some
quantities are given as a function of energy groups and anisotropy. The order
of the anisotropy development is available in the ``'info'`` group, possibly in
the ``'isotope_id`` one. Current and surfacic flux (under ``'totaloutput'``)
have a ``surface id`` component in addition to energy groups.

Some files can also contain custom values or user values, especially in some
cases the standard structure does not appear at all (no ``zone_id`` or
``totaloutput`` folder) but directly local values:

.. code-block::

    ┌─ info ─┬─ (COMMENT)
    │        ├─ (FORMAT)
    │        ├─ (VERSION)
    │
    └─ output ─┬─ (LOCALVALUE[NVAL])
               ├─ (LOCALNAME[NVAL])
               └─ (localvalue) ─┬─ LOCALNAME[NVAL]
                                ├─ value_id1
                                ┆
                                ┆
                                └─ value_idNVAL


Use of :class:`Reader`
----------------------

.. code-block:: python

    from valjean.eponine.apollo3.hdf5_reader import Reader
    ap3r = Reader('MON_FICHIER.hdf')
    ap3b = ap3r.to_browser()

See :mod:`~valjean.eponine.browser` to get more details on how to use the
:class:`~valjean.eponine.browser.Browser` objects.

In the resulting :class:`~valjean.eponine.browser.Browser`, the metadata are
taken from the :obj:`h5py.Group` values, while the actual data are taken from
the :obj:`h5py.Dataset` ones.

Data are directly stored as :class:`~valjean.eponine.dataset.Dataset`. Errors
are set to ``numpy.nan`` by default but this can be changed and be set to 0
(for example) using the ``error_value`` argument to the constructor. Bins are
set to the group indices, or to group indices and number of anisotropies when
available. Two specific cases are added:
* surfacic flux: bins are given in group indices and surface numbers
* current: bins are given in group indices, surface numbers and direction

Some metadata keys in the browser are slightly different from the corresponding
names of the HDF5 file:

* in the global variables (``Browser.globals``):
    * under the ``'info'`` key:
        * ``'geom_id' `` for the ``'GEOMID'`` metadata
        * ``'ngroups'`` for ``'NG'``
    * under the ``'geometry'`` key: a dictonary associating the ``'geom_id'``
      names to dictionaries of {``'ZONENAME'``: ``'VOLUME'``}.
* in the results (``Browser.content``):
    * zone names: kept as they are given in the HDF5 file (also true for
      ``'totaloutput'``)
    * reaction names, flux, keff are set in lower case instead of upper
    * ``'CONCEN'`` is renamed in ``'concentration'`` and appears as a standard
      result (like reaction rates)
    * isotopes names are kept as they are but spaces surrounding the name are
      stripped. The ``'macro'`` key is kept unchanged for macroscopic results
      (integrated over isotopes)
    * local value names are left inchanged (under the ``'result_name'`` key).

The most common keys in the :class:`~valjean.eponine.browser.Browser` are
``['result_name', 'output', 'zone', 'isotope']``.


An inspect function is also available (no class:`Reader` object needed) to have
a quick look at the content of the file.

.. code-block:: python

    from valjean.eponine.apollo3.hdf5_reader import inspect
    inspect('MON_FICHIER.hdf')
'''

from collections import OrderedDict
import logging
import h5py
import numpy as np

from ...chrono import Chrono
from ..browser import Browser
from ..dataset import Dataset


LOGGER = logging.getLogger(__name__)


def hdf_to_browser(*args, **kwargs):
    '''Build a :class:`~valjean.eponine.browser.Browser` from an Apollo3 HDF5
    output.

    :param args: other arguments to be passed to :class:`Reader` constructor
    :param kargs: keyword arguments to be passed to :class:`Reader` constructor
    :returns: Browser
    '''
    return Reader(*args, **kwargs).to_browser()


class Reader:
    '''Read an HDF5 file from Apollo3.'''

    def __init__(self, fname, error_value=np.nan):
        '''Initialize the :class:`Reader` object and read the HDF5 file.

        :param str fname: path to the Apollo3 HDF5 ouput
        :param error_value: value to give to the error (default: ``numpy.nan``)
        :type error: int, float
        '''
        LOGGER.info('Reading %s', fname)
        self.error_value = error_value
        self.geom = {}
        self.info = {}
        self.res = {}
        with Chrono() as chrono:
            hfile = h5py.File(fname, 'r')
        LOGGER.info('hdf5 loading done in %f s', chrono)
        with chrono:
            self.read_file(hfile)
        hfile.close()
        LOGGER.info('Successful reading in %f s', chrono)

    def read_file(self, hfile):
        '''Read the HDF5 file.

        The information read depends on the type of file. In the case of a
        *standard* output file, we read ``'info'``, ``'geometry'`` and all
        results. In a *user* output, only results are read.

        :param str hfile: path to the HDF5 file

        :raises ReaderException: if unexpected keys are found.
        '''
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug('Keys in HDF5 file: %s', list(hfile.keys()))
        if 'info' not in hfile:
            raise ReaderException("'info' missing in the HDF5 file")
        self.info = extract_info(hfile['info'])
        if self.info:
            self.process_standard_values(hfile)
        else:
            self.process_user_values(hfile)

    def process_standard_values(self, hfile):
        '''Process standard values (keff, flux, rates).'''
        self.geom = extract_geometry(hfile['geometry'])
        for key, value in hfile.items():
            if not key.startswith('output_'):
                continue
            self.res[key] = extract_standard_values(
                value, self.info[key]['ngroups'], self.error_value)

    def process_user_values(self, hfile):
        '''Process user values stored in files (named local values in file).
        '''
        for key, value in hfile.items():
            if key == 'info':
                continue
            self.res[key] = extract_user_values(value, self.error_value)

    def to_browser(self):
        '''Build a :class:`~valjean.eponine.browser.Browser` from
        the results in the HDF5 file.

        :rtype: Browser
        '''
        browser = Browser(
            dict_to_list('output', self.res),
            global_vars={'info': self.info, 'geometry': self.geom})
        return browser


def extract_geometry(geometry):
    '''Extract geometry in dict to go to
    :class:`~valjean.eponine.browser.Browser` globals.

    :param h5py.Group geometry: geometry stored in HDF5
    '''
    LOGGER.debug("In extract_geometry")
    dgeom = {}
    for geom in geometry:
        if geom == 'NGEO':
            continue
        igeom = geometry[geom]
        dgeom[geom] = {
            name.decode('UTF-8').strip(): vol
            for name, vol in zip(igeom['ZONENAME'], igeom['VOLUME'])}
    LOGGER.debug("geometry dict done")
    return dgeom


def extract_info(info):
    '''Extract info in dict to go to
    :class:`~valjean.eponine.browser.Browser` globals.

    :param h5py.Group info: info stored in HDF5
    '''
    LOGGER.debug("In extract_info")
    dinfo = {}
    if 'NOUT' not in info:
        LOGGER.debug('No description of output* folders, info not stored')
        LOGGER.debug('keys are %s', list(info.keys()))
        return dinfo
    infos = [(k, v) for k, v in info.items() if k.startswith('output_')]
    for nout, a_info in infos:
        dinfo[nout] = {
            'geom_id': a_info['GEOMID'][...][0].decode('UTF-8'),
            'ngroups': a_info['NG'][...][0]}
    LOGGER.debug("Leaving extract_info")
    return dinfo


def extract_standard_values(val, ngroups, error):
    '''Extract results from Apollo3 HDF5 file.

    :param str out_id: name of the output folder in HDF5
    :param h5py.Group val: results stored in the folder
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :returns: list of all results stored with metadata and data shaped as
        `Dataset`
    :rtype: list(dict)
    '''
    tdict = {}
    for zone in val:
        if zone == 'totaloutput':
            tdict[zone] = loop_over_std_values(
                val['totaloutput'], ngroups, error)
        else:
            tdict[zone] = extract_zone_values(val[zone], ngroups, error)
    return dict_to_list('zone', tdict)


def extract_user_values(val, error):
    '''Extract user results (or 'local' values).

    :param h5py.Group val: results stored under ``'LOCALVALUES'``
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :returns: list of results including metadata
    :rtype: list(dict)
    '''
    if 'LOCALNAME' in val:
        return extract_localvalues(val['LOCALNAME'], val['LOCALVALUE'], error)
    rlist = []
    locval = 'localvalue'
    lkeys = [e.decode('UTF-8').strip()
             for e in val[locval]['LOCALNAME'][...]]
    rlist = [{'result_name': k,
              'results': hdfdataset_to_dataset(val[locval][k], k, error)}
             for k in lkeys]
    return rlist


def extract_localvalues(lnames, lvals, error):
    '''Extract local values from a list of local names.

    :param list(str) lnames: list of the names of the local values
    :param h5py.Dataset lvals: local (scalar) values
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :returns: list of results including metadata
    :rtype: list(dict)
    '''
    LOGGER.debug('In extract_localvalues')
    return [{'result_name': key.decode('UTF-8').strip(),
             'results': build_dataset(val, error, key.decode('UTF-8').strip())}
            for key, val in zip(lnames, lvals)]


def loop_over_std_values(lres, ngroups, error):
    '''Loop over results stored in the ``'output_*'`` groups of the HDF5
    file.

    Also retrieve number of anisotropies from the `info` :obj:`h5py.Group`.

    :param h5py.Group lres: list of results
    :param int ngroups: number of energy groups
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :returns: list of results including metadata
    :rtype: list(dict)
    '''
    rlist = []
    res = [(k, v) for k, v in lres.items()
           if not k.startswith(('LOCAL', 'local', 'info', 'NSURF'))]
    anisotropies = extract_output_info(lres.get('info'))
    nsurfaces = extract_surfaces_number(lres.get('NSURF'))
    for nres, vres in res:
        bins = make_bins(nres, vres, ngroups, anisotropies, nsurfaces)
        rlist.append({
            'result_name': nres.lower(),
            'results': hdfdataset_to_dataset(
                vres, what=nres.lower(), error=error, bins=bins)})
    if 'LOCALNAME' in lres or 'localvalue' in lres:
        rlist.extend(extract_user_values(lres, error))
    return rlist


def hdfdataset_to_dataset(hdf_data, what, error, bins=None):
    '''Build :class:`~valjean.eponine.dataset.Dataset` from HDF5 dataset (in
    *rates* cases).

    Returns a scalar or an array depending on data shape.

    :param h5py.Dataset hdf_data: dataset containing the data
    :param str what: quantity name
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :param collections.OrderedDict bins: bins corresponding to data, default
      `None`
    :rtype: Dataset
    '''
    if not isinstance(hdf_data, h5py.Dataset):
        raise TypeError(f'Expected a h5py.Dataset, got a {type(hdf_data)}')
    if hdf_data.shape == (1,) and not bins:  # ngroups == 0:
        val = hdf_data[...][0]
    else:
        val = hdf_data[...]
    return build_dataset(val, error, what, bins)  # ngroups, naniso)


def build_dataset(data, error, what, bins=None):
    '''Build :class:`~valjean.eponine.dataset.Dataset` from HDF5 result.

    :param data: data
    :type data: numpy.generic, numpy.ndarray
    :param str what: quantity name
    :param error: value of error
    :type error: numpy.generic, float, int, default = ``numpy.nan``
    :param str what: quantity name
    :param collections.OrderedDict bins: bins corresponding to data, default
      `None`
    :rtype: Dataset
    '''
    error = np.full_like(data, error,
                         dtype=(float if np.isnan(error) else data.dtype))
    if not bins:
        return Dataset(value=data, error=error, what=what)
    if 'anisotropies' in bins:
        ngroups = len(bins['groups'])
        naniso = len(bins['anisotropies'])
        return Dataset(value=data.reshape(naniso, ngroups),
                       error=error.reshape(naniso, ngroups),
                       what=what, bins=bins)
    if 'incident neutron groups' in bins:
        ngroups = len(bins['groups'])
        nincg = len(bins['incident neutron groups'])
        return Dataset(value=data.reshape(nincg, ngroups),
                       error=error.reshape(nincg, ngroups),
                       what=what, bins=bins)
    return Dataset(value=data, error=error, what=what, bins=bins)


def make_bins(nres, vres, ngroups, anisotropies=None, nsurfaces=None):
    '''Build bins :obj:`collections.OrderedDict`.

    The bins currently available are
    * number of energy groups
    * number of anisotropies (for isotopes reaction rates)
    * number of surfaces (for current and surface flux)

    :param h5py.Group data: `info` block from `output_*`
    :rtype: dict
    :returns: dictionary of all possible number of bins
    '''
    if nres in ('KEFF', 'KINF', 'MIGRATIONAREA', 'Buckling'):
        return None
    data = vres[...]
    if ngroups == data.size:
        return OrderedDict([('groups', np.arange(ngroups))])
    if nres == 'SURFFLUX':
        return OrderedDict([('groups', np.arange(ngroups)),
                            ('surfaces', np.arange(nsurfaces))])
    if nres == 'CURRENT':
        return OrderedDict([('groups', np.arange(ngroups)),
                            ('surfaces', np.arange(nsurfaces)),
                            ('direction', np.array(['incoming', 'leaving']))])
    if nres == 'MultigroupSpectrum':
        incgrps = data.size // ngroups
        return OrderedDict([('incident neutron groups', np.arange(incgrps)),
                            ('groups', np.arange(ngroups))])
    naniso = anisotropies.get(nres, anisotropies['anisotropy'])
    if ngroups * naniso != data.size:
        raise ReaderException(
            f"Dataset size ({data.size})not corresponding to "
            f"NG*Nanisotropies {ngroups}*{naniso} for {nres}")
    return OrderedDict([('anisotropies', np.arange(naniso)),
                        ('groups', np.arange(ngroups))])


def extract_output_info(data, name='anisotropy'):
    '''Extract info from output group containing number of anisotripies.

    :param h5py.Group data: `info` block from `output_*`
    :param str name: anisotropy name (`'anisotropy'` per default, result name
      if one
    :rtype: dict
    :returns: dictionary indexed by anisotropy name
    '''
    aniso = {'anisotropy': 1}
    if not data:
        return aniso
    for dname, dat in data.items():
        if 'macro' in dat.name and isinstance(dat, h5py.Group):
            aniso.update(extract_output_info(dat, name=dname))
            continue
        if dname != 'nbAnisotropy':
            raise ReaderException('info group should contain nbAnisotropy')
        aniso[name] = dat[...][0]
    return aniso


def extract_surfaces_number(data):
    '''Extract number of surfaces if available.'''
    if not data:
        return None
    return data[...][0]


def extract_concentrations(zone, error):
    '''Store isotopes list and concentration from the zone group.

    :param h5py.Group zone: HDF5 group corresponding to the zone
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :returns: list of dictionaries with isotope name in metadata,
        ``'concentration'`` as ``result_name`` and concentration values
        stored in a :class:`~valjean.eponine.dataset.Dataset` under the
        ``'results'`` key
    :rtype: list(dict)
    '''
    tdict = OrderedDict()
    for isotop, conc in zip(zone.get('ISOTOPE'), zone.get('CONCEN')):
        tdict[isotop.decode('UTF-8').strip()] = {
            'result_name': 'concentration',
            'results': Dataset(value=conc,
                               error=np.full_like(conc, error, dtype=float),
                               what='concentration')}
    return dict_to_list('isotope', tdict)


def extract_zone_values(val, ngroups, error):
    '''Store results by zone.

    Results are stored depending on their nature (flux, concentrations,
    etc.).

    :param h5py.Group val: HDF5 group containing results from a given zone
    :returns: list of results including metadata
    :param error: value to give to the error (default: ``numpy.nan``)
    :type error: int, float
    :rtype: list(dict)
    '''
    tlist = []
    isotd = {}
    if val['NISOT'][...][0] != 0:
        liso = set(iso.decode('UTF-8').strip() for iso in val['ISOTOPE'])
    else:
        liso = {}
    for key in val:
        if key == 'CONCEN':
            tlist.extend(extract_concentrations(val, error))
        elif key == 'macro':
            isotd[key] = loop_over_std_values(val['macro'], ngroups, error)
        elif key in ('NISOT', 'ISOTOPE'):
            continue
        elif key in liso:
            isotd[key] = loop_over_std_values(val[key], ngroups, error)
        else:
            bins = make_bins(key, val[key], ngroups)
            tlist.append({'result_name': key.lower(),
                          'results': hdfdataset_to_dataset(
                              val[key], key.lower(), error, bins)})
    tlist.extend(dict_to_list('isotope', isotd))
    return tlist


def dict_to_list(key_name, tdict):
    '''Transform a dictionary in a list of dictionaries including the key
    as a new key, value member of each dictionary.

    :param str key_name: key of the new dictionary
    :param dict tdict: dictionary whose keys will become values of key_name
    :returns: list of results including metadata
    :rtype: list(dict)

    >>> tdict = OrderedDict()
    >>> tdict['Graham'] = [{'day': 'Monday', 'meal': 'spam'},
    ...                    {'day': 'Tuesday', 'meal': 'egg'}]
    >>> tdict['Terry'] =  {'day': 'Monday', 'meal': 'bacon'}
    >>> tlist = dict_to_list('consumer', tdict)
    >>> len(tlist)
    3
    >>> from pprint import pprint
    >>> pprint(tlist)
    [{'consumer': 'Graham', 'day': 'Monday', 'meal': 'spam'},
     {'consumer': 'Graham', 'day': 'Tuesday', 'meal': 'egg'},
     {'consumer': 'Terry', 'day': 'Monday', 'meal': 'bacon'}]

    .. todo::

        Simplify this example by changing back OrderedDict in dict when python
        3.5 won't be anymore supported.
    '''
    tlist = []
    for k, val in tdict.items():
        if isinstance(val, dict):
            val_copy = val.copy()
            val_copy[key_name] = k
            tlist.append(val_copy)
        elif isinstance(val, list):
            for dic in val:
                dic_copy = dic.copy()
                dic_copy[key_name] = k
                tlist.append(dic_copy)
    return tlist


def inspect(hfile, name_spaces=50):
    '''Loop recursively over content of the file and print it.

    :param str hfile: path to the Apollo3 HDF5 ouput
    :param int name_spaces: number of spaces reserved for the folder's names,
        default = 50
    '''
    def find_subobj(name, obj):
        LOGGER.info(f'{name:<{name_spaces}}  {obj}')  # pylint: disable=W1203
    hfile.visititems(find_subobj)


class ReaderException(Exception):
    '''An error that may be raised by the :class:`Reader` class.'''
