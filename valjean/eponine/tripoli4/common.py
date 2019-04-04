# pylint: disable=anomalous-backslash-in-string
# pylint: disable=too-many-lines
r'''This module provides generic functions to convert parsing outputs to
`NumPy` objects.

Inputs (outputs from parsers) should be python lists or dictionary,
dictionary keys should be the same in all parsers...

.. todo::

   | Not a standalone code, needs inputs.
   | To be tested in a more general context.


.. |keff| replace:: k\ :sub:`eff`
.. |ck| replace:: cb k\ :sub:`eff`
.. |KS| replace:: KSTEP
.. |KC| replace:: KCOLL
.. |KT| replace:: KTRACK
.. |kij| replace:: k\ :sub:`ij`
.. _numpy structured array:
   https://docs.scipy.org/doc/numpy/user/basics.rec.html

Goal
====

Parsing results are normally stored as lists and dictionaries but it could be
easier to use other objects, as `NumPy` arrays. In our context these objects
are used to represent

* spectrum results, i.e. tables splitted at least in energy, sometimes with
  additional splittings in time, µ and φ direction angles
* mesh results, i.e. tables splitted in space (cartesian, cylindrical,
  spherical depending on case), sometimes with additional splittings in energy
  and/or time
* Green bands results
* IFP results
* |keff| results
* k\ :sub:`ij` results (matrices, eigenvectors and eigenvalues)

`NumPy` objects are useful for future calculations or plotting for example.


Spectrum and meshes
===================

.. _eponine-spectrummesh-intro:

Generalities
------------

.. _doc: https://docs.scipy.org/doc/numpy/user/basics.rec.html

Spectrum and meshes results use a common representation build using
:class:`DictBuilder`. This common representation is a **7-dimension structured
array** from `NumPy`, see `doc`_ or `numpy structured array`_.

Kinematic dimensions are:

:s0, s1, s2:
    space coordinates (typically (x, y, z), (r, θ, z) or (r, θ, φ), depending
    on frame reference)
:e: energy
:t: time
:mu, phi: direction angles µ and φ whose definitions can vary depending on
    the reference frame of direction [#dir_angles]_.

Order should always be that one.


The result for each bin ``(s0, s1, s2, e, t, mu, phi)`` is filled in a
`numpy structured array`_ whose :obj:`numpy.dtype` can be:

:meshes: normally ``'score'`` and ``'sigma'`` where *sigma* is in % and
    *score* in its unit (not necessarly precised in the listing)
:default spectrum: ``'score'``, ``'sigma'``, ``'score/lethargy'`` where
    *sigma* is in %, *score* and *score/lethargy* in the unit of the score (not
    necessarly precised in the listing)
:spectrum with variance of variance (vov): as default spectrum case + a
    fourth element named ``'vov'`` (no unit)
:uncertainties spectrum: in case of *covariance perturbations*, elements are
    ``'sigma2(means)'``, ``'mean(sigma_n2)'``, ``'sigma(sigma_n2)'`` and
    ``'fisher test'`` [#uncertainties]_


Spectrum and mesh results don't only consist in arrays: binning (except in
space) and number of dicarded batchs are also available for example. Other
optional can also be added, like integrated result on one or more dimensions.
The final result of spectrum and mesh is returned as a dictionary detailed in
:ref:`result_spectrum <eponine-spectrum-res>` and
:ref:`result_mesh <eponine-mesh-res>`.


Initialization
--------------

:class:`DictBuilder` cannot be instantiated as it has abstract methods (pure
virtual): :meth:`~DictBuilder.fill_arrays_and_bins` and
:meth:`~DictBuilder.add_last_bins`. It is mother class of
:class:`MeshDictBuilder` for mesh and :class:`SpectrumDictBuilder` for
spectrum.

Initialization is done giving names of the columns (``'score'`` and ``'sigma'``
for mesh for example) and the list of number of bins. The length of this list
should be 7 as we have 7 dimensison.

   >>> from valjean.eponine.tripoli4.common import (DictBuilder,
   ...     MeshDictBuilder, SpectrumDictBuilder)
   >>> db = DictBuilder(['score', 'sigma'], [1,2,3,4,5,6,7])
   Traceback (most recent call last):
       [...]
   TypeError: Can't instantiate abstract class DictBuilder with ...
   >>> mdb = MeshDictBuilder(['score', 'sigma'], [1,2,3,4,5,6,7])
   >>> mdb = MeshDictBuilder(['result', 'sigma'], [1,2,3,4,5,6,7])
   >>> sdb = SpectrumDictBuilder(['score', 'sigma', 'score/lethargy'],
   ...                           [1,2,3,4,5,6,7])

Errors are raised if the dimension is not correct.

   >>> mdb = MeshDictBuilder(['score', 'sigma'], [1,2,3,4,5,6])
   Traceback (most recent call last):
       ...
   AssertionError

Number of bins should be 7 (3 space dimensions, 1 energy, 1 time, 2 direction
angles).

These methods initializes both the 7-dimensions `numpy structured array`_ and
the arrays of bins, first stored as list for simplicity. Arrays of bins are in
reality array of the edges of bins, starting by the lower one to the higher one
after flipping if needed.

.. _eponine-spectrummesh-fill:

Filling arrays and bins
-----------------------

Mesh and spectrum are read from the output listing and first stored as list and
dictionary following listing structure. Building :obj:`numpy.ndarray` for
arrays and bins simplifies post-processing. It calls
:meth:`~DictBuilder.fill_arrays_and_bins`.

To fill arrays and bins needed objects are outputs from the chosen parser. Some
dictionary keys may be needed:

mesh:
    data is a list of all meshes available. Each mesh is a dictionary that can
    have the following keys:

    :``'meshes'``: list of dictionary containing the mesh results (mandatory),
      dictionaries with keys:

      * ``{'mesh_energyrange': [], 'mesh_vals': [[], ]}`` to get mesh per
        energy range (mandatory)
      * ``{'mesh_energyintegrated':, 'mesh_vals': [[], ]}`` if result is also
        available on the full range of energy but still splitted in space
        (facultative)

      A mesh line in the list under ``'mesh_vals'`` key is constructed as a
      list of ``[[s0, s1, s2], score, sigma]``. In ``'mesh_energyrange'``,
      energy range is given as ``['unit', e1, e2]``.

    :``'time_step'``: if a time splitting is available
      Remark: for the moment, no splitting in µ or φ are available.
    :``'integrated result'``: if ``'time_step'`` exists, integrated result can
      be available, meaning integrated over space and energy (not time)

spectrum:
    data is a list of dictionaries containing spectrum results.

    Possible keys are:

    :``'spectrum_vals'``: spectrum values, given in a list
      ``[e1, e2, score, sigma, score/lethargy]`` (mandatory)
    :``'time_step'``: if result splitted in time
    :``'mu_angle_zone'``: if result splitted in µ angle
    :``'phi_angle_zone'``: if result splitted in φ angle
    :``'integrated_res'``: if ``'time_step'`` exits, integrated result can
      also be given in time steps, so integrated over energy.

When arrays are filled, bins are also filled on their first appearance. At the
end of the filling special care needs to be taken to bins. Indeed, as usual
there are Nbins+1 edges. The last edge may be the lowest one or the highest
one, depending on the order required in the job. So it will inserted in first
position or appended to the end.

If bins are in decreasing order in one dimension (energy, time, µ or φ), arrays
will be flipped in that direction. This step as to be done on all arrays stored
and on the bins array to stay consistant.

If time, µ or φ grids are given, they will always appear in the same order:
t -> µ -> φ. µ and φ can exist without time; time can exist alone, like µ; φ
cannot exist without µ [#dir_angles]_. If more than one is present, the first
one is not repeated at each step, so needs to be propagated to the next steps
(instance variables ``itime``, ``imu`` and ``iphi``).



Result and use in the framework
-------------------------------

In the framework, :class:`MeshDictBuilder` and :class:`SpectrumDictBuilder` are
called in :meth:`convert_mesh` and :meth:`convert_spectrum`, themselves from
transformation modules (transforming parsing result in `NumPy`/`python`
containers. Theses methods then returns dictionaries containing the
:obj:`numpy.ndarray` and other results.

.. _eponine-mesh-res:

mesh:
   Default keys are:

   :``'array'``: 7-dimensions `numpy structured array`_ with
     :obj:`numpy.dtype` ``('score', 'sigma')``
   :``'bins'``: :class:`collections.OrderedDict` (str, :obj:`numpy.ndarray`),
     order corresponds to the order of the shape in the array. Space are
     normally at center of the bin, while E, t, μ and φ are given as edges. If
     no binning is available an empty array is present.
   :``'units'``: available limits (default set, including score and sigma)

   Other keys can be available:

   :``'eintegrated_array'``: 7-dimensions `numpy structured array`_ with
     dtype ``('score', 'sigma')`` and list of number of bins (``lnbins``) is
     ``[n_s0, n_s1, n_s2, 1, n_t, 1, 1]``
   :``'integrated_res'``: 7-dimensions `numpy structured array`_ with
     dtype ``('score', 'sigma')`` and list of number of bins (``lnbins``) is
     ``[1, 1, 1, 1, n_t, 1, 1]``
   :``'used_batch'``: if ``'integrated_res'`` exists, number of used batch is
     also given


.. _eponine-spectrum-res:

spectrum:
   Default keys are:

   :``'spectrum'``: 7-dimensions `numpy structured array`_ with
     :obj:`numpy.dtype` ``('score', 'sigma', 'score/lethargy')`` if this is a
     default spectrum, :obj:`numpy.dtype` will change in some cases (vov,
     uncertainties), see :ref:`eponine-spectrummesh-intro`
   :``'bins'``: :class:`collections.OrderedDict` (str, :obj:`numpy.ndarray`),
     order corresponds to the order of the shape in the array. In spectrum no
     space bins are given (corresponding to empty arrays), other dimensions are
     normally given as edges when available, else as an empty array.
   :``'disc_batch'``: number of discarded batchs

   Optional keys are:

   :``'integrated_res'``: 7-dimensions `numpy structured array`_ with same
     :obj:`numpy.dtype` as ``'array'`` and list of number of bins
     (``lnbins``) is ``[1, 1, 1, 1, n_t, 1, 1]`` (integrated over energy)
   :``'used_batch'``: if ``'integrated_res'`` exists, number of used batch is
     also given


Other available arrays
======================

Green bands
-----------

Green bands are stored in :obj:`numpy.ndarray` that look like the spectrum or
mesh ones but with different bins and dtypes, these are 6-dimensions arrays.

The 6 dimensions are given, in order, by:

:se: ``'step'`` in input,  bin of the energy of source (source are treated in
    energy steps)
:ns: ``'source'`` in input, number of the source
:u, v, w: coordinates of the source, ``(0, 0, 0)`` if not given
:e: energy of the output neutron

The result for each bin (se, ns, u, v, w, e) is filled in a
`numpy structured array`_ whose :obj:`numpy.dtype` is the default spectrum one,
``('score', 'sigma', 'score/lethargy')``.

Bins are also stored for all the dimensions in same order as in the array.
Empty array corresponds to unused dimensions. Like in spectrum, last bins of
energy (source and followed particle) are added after the main loop.

The returned dictionary contains:

:``'disc_batch'``: number of discarded batchs
:``'array'``: 6-dimension `numpy structured array`_
:``'bins'``: :class:`collections.OrderedDict` (str, :obj:`numpy.ndarray`) of
    bins in same order as array shape
:``'units'``: dict of units


Adjoint results
---------------

Results obtained from the calculation of the adjoint can beassociated to array
like spectra or meshes or to more generic scores. Dimensions are usually a bit
different. The output from Tripoli-4 is also different and has to be treated
separately.

Different knid of arrays are available, depending on the type of calculation:

Generic adjoint result:
    corresponds generic scores calculated by IFP or Wielandt methods. They are
    returned as standard dictionary containing usual integrated results (pair
    score, sigma), so no array. 'Dimensions' correspond to the dictionary keys
    (like nucleus, family, length, etc.).

Adjoint criticality results from specific edition:
    only calculated with the IFP method. Two kind of results are for the moment
    available: multi-dimensions arrays, close to meshes and arrays in (volume,
    energy) where volume corresponds to the geometrical id of the volume. The
    available dimension for the multi-dimensions arrays are: X, Y, Z (only
    cartesian in space), φ and θ in direction, energy. No time is considered.
    These spectra inherit from :class:`KinematicDictBuilder` but have a
    different order of bins compared to spectra and meshes and time is
    automatically set to 1 bin (integrated).

More details and code are available in :func:`convert_generic_adjoint`,
:class:`AdjointCritEdDictBuilder` and :class:`VolAdjCritEdDictBuilder`.


Nu and (Z,A) spectrum
---------------------

Spectra indexed by the number of neutrons produced in fission (Nu) and indexed
by the (Z,A) of the produced fission products (isotopes) as also available as
spectra.

The results are given as standard array results: a dictionary with the usual
keys (``'array'``, ``'bins'``, ``'units'``, ``'integrated_res'``,
``'disc_batch'``).

More details in :func:`convert_nu_spectrum` and :func:`convert_za_spectrum`.


|keff| results
==============

Only |keff| as generic response are converted in *NumPy* objects; historical
|keff| block is stored in a dictionary (see
:mod:`valjean.eponine.tripoli4.grammar`).

In the generic response case, results (value, σ) are available for 3
estimators: KSTEP, KCOLL and KTRACK. Their correlation coefficients, combined
values, combined σ (in %) and the full combination result are also given. This
means that results given are in reality a matrix. One choice in order to store
|keff| results is to use :obj:`numpy.ndarray` seen as matrix
(:meth:`convert_keff_with_matrix`), the other one uses more standard arrays
(:meth:`convert_keff`).

.. _eponine-keff-matrix:

Conversion to matrices
----------------------
The 3 estimators are always considered in the listing order KSTEP, KCOLL,
KTRACK, so KSTEP = 0, KCOLL = 1 and KTRACK = 2.

Three arrays are filled:

:``'keff_matrix'``: symmetric matrix 3×3, with k\ :sub:`eff` result for each
  estimator on diagonal and combined values off-diagonal (for 2 estimators)
:``'correlation_matrix'``: symmetric matrix 3×3, with 1 on diagonal and
  correlation cofficient off-diagonal (for 2 estimators)
:``'sigma_matrix'``: symmetric matrix 3×3 with σ in % for each estimator on
  diagonal and combined σ in % off-diagonal (for 2 estimators)


In summary:

* for k\ :sub:`eff` and σ matrices (replace |keff| by σ in 2\ :sup:`d`
  case, cb stands for combined):

  +--------+-------------------+-------------------+-------------------+
  |        | KSTEP             | KCOLL             | KTRACK            |
  +--------+-------------------+-------------------+-------------------+
  | KSTEP  | |keff| (KSTEP)    | |ck| (|KS|, |KC|) | |ck| (|KS|, |KT|) |
  +--------+-------------------+-------------------+-------------------+
  | KCOLL  | |ck| (|KS|, |KC|) | |keff| (KCOLL)    | |ck| (|KC|, |KT|) |
  +--------+-------------------+-------------------+-------------------+
  | KTRACK | |ck| (|KS|, |KT|) | |ck| (|KC|, |KT|) | |keff| (KTRACK)   |
  +--------+-------------------+-------------------+-------------------+


* the correlation matrix:

  +--------+------------------+------------------+------------------+
  |        | KSTEP            | KCOLL            | KTRACK           |
  +--------+------------------+------------------+------------------+
  | KSTEP  | 1                | corr(|KS|, |KC|) | corr(|KS|, |KT|) |
  +--------+------------------+------------------+------------------+
  | KCOLL  | corr(|KS|, |KC|) | 1                | corr(|KC|, |KT|) |
  +--------+------------------+------------------+------------------+
  | KTRACK | corr(|KS|, |KT|) | corr(|KC|, |KT|) | 1                |
  +--------+------------------+------------------+------------------+

Values are set to `numpy.nan` if not converged (string ``"Not converged"``
appearing in the listing).

These arrays can be easily converted to matrices if matrix methods are needed
but array is easier to initialized and more general.

The method :meth:`convert_keff_with_matrix` takes as input the generic |keff|
response as a dictionary and returns a dictinary containing different keys:

* the 3 matrices mentioned above (``'keff_matrix'``, ``'correlation_matrix'``
  and ``'sigma_matrix'``)
* the list of estimators names ``['KSTEP', 'KCOLL',' 'KTRACK']`` under
  ``'estimators'`` key
* the full combination result (|keff| and σ in %) under
  ``'full_comb_estimation'`` key
* the number of batchs used under ``'used_batch'``

Not converged cases are taken into account and return a key
``'not_converged'``.


.. _eponine-keff-stdarrays:

Conversion to standard arrays
-----------------------------
The conversion closer to the output listing is done in :meth:`convert_keff`. A
dictionary is built with the following elements:

:``'used_batch'``: number of batchs used
:``'full_comb_estimation'``: full combination result (|keff| and σ in %), like
  in :ref:`eponine-keff-matrix`
:``'res_per_estimator'``: dictionary with estimator as key and `numpy
  structured array`_ with ``dtype = ('keff', 'sigma')`` as value
:``'correlation_matrix'``: dictionary with tuple as key and `numpy structured
  array`_ as value, ``('estimator1', 'estimator2'):
  numpy.array('correlations', 'combined values', 'combined sigma%')``

In correlation matrix diagoanl is set to 1 and not converged values (str) are
set to `numpy.nan`. If the full combination did not converged hte string is
kept.


|kij| results
=============

|kij| matrix gives the number of neutrons produced by fission in the volume i
from a neutron emited in the volume j. Its highest eigenvalue is equal to the
|keff| of the system. The corresponding eigenvector represents the neutrons
sources in the volumes (necessarly containing fissile metrial). For more
details, see user guide.

Different |kij| results can be available:

* list of |kij| sources in :meth:`convert_kij_sources`
* |kij| matrix and associated results in :meth:`convert_kij_result`
* |kij| estimation in historical |keff| block (|kij| is an additional estimator
  in that case) in :meth:`convert_kij_keff`


|kij| sources
-------------
In that case the input dictionary is returned with a conversion of the
``'kij_sources_vals'`` as a :obj:`numpy.ndarray`. Its length corresponds to the
number of volumes.


.. _eponine-kij-result:

|kij| matrix (result)
---------------------
The |kij| matrix results block contains various results including |kij|
eigenvalues, |kij| eigenvectors and |kij| matrix that will be converted in
:obj:`numpy.ndarray` or :obj:`numpy.matrix`. The size of the arrays depends on
the number of volumes containing fissle material, N.

The returned object is a dictionary containing the following keys and objects:

:``'used_batch'``: number of batchs used (`int`)
:``'kijmkeff_res'``: result of |kij|-|keff| (`float`), where |kij| is the
  hightest eigenvalue of |kij|
:``'kijdomratio'``: dominant ratio (`float`), ratio between the hightest |kij|
  eigenvalue and the next one
:``'kij_eigenval'``: :obj:`numpy.ndarray` of N **complex** numbers (real and
  imaginary parts given in the listings) corresponding to the eigenvalues.
:``'kij_eigenvec'``: :obj:`numpy.ndarray` of N vectors of N elements
  corresponding to eigenvectors.
:``'kij_matrix'``: :obj:`numpy.matrix` of N×N being the |kij| matrix.


.. _eponine-kij-in-keff:

|kij| in |keff| block
---------------------
|kij| results are also present in the "historical" |keff| block, as an
additional estimator. Results are presented in a different way and are
different... Typical results are |kij| - |keff|, the eigenvector corresponding
to the best estimation, |kij| matrix, standard deviation matrix and
sensibility matrix.

The returned object is a dictionary with the following keys (faculative can be
specified):

:``'estimator'``: name of the estimator (:class:`str`), ``'KIJ'`` here
:``'batchs_kept'``: number of batchs used to calculate the |keff| from |kij|
  (:class:`int`)
:``'kij-keff'``: result of |kij|-|keff| (`float`), using the best estimation
  of |kij|
:``'nbins'``: **facultative**, number of volumes/mesh elements considered, or
  N, (:class:`int`)
:``'spacebins'``: **facultative**, list of N volumes/mesh elements considered
  (:obj:`numpy.ndarray` of

    * :class:`int` for volumes,
    * :class:`tuple` of :class:`int` (s0, s1, s2) for mesh elements,

:``'eigenvector'``: eigenvector corresponding to best estimation
  (:obj:`numpy.ndarray` of N elements)
:``'keff_KIJ_matrix'``: |kij| matrix for best estimation of |keff|
  (N×N :obj:`numpy.matrix`)
:``'keff_StdDev_matrix'``: standard deviation matrix for best estimation of
  |keff| (N×N :obj:`numpy.matrix`)
:``'keff_sensibility_matrix'``: sensibility matrix for best estimation of
  |keff| (N×N :obj:`numpy.matrix`)

.. rubric:: Footnotes

.. [#dir_angles] Definition of µ and φ, direction angles (see also user guide)

                - µ = cos(θ)
                - if ANGULAR keyword used: result only splitted in µ, with θ is
                  defined with respect to the normal of the surface used in
                  SURF
                - if 2D_ANGULAR keyword used: result splitted in µ and φ,
                  defined in the global frame

.. [#uncertainties] The structured array elements in uncertainty spectrum case
   are:

        - ``'sigma2(means)'``: variance of means or σ\ :sup:`2` of means
        - ``'mean(sigma_n2)'``: mean of variances, with variance = v\ :sub:`n`
        - ``'sigma(sigma_n2)'``: σ(variances) = :math:`\sqrt{v(v_n)}`
        - ``'fisher test'``: this is an estimator more than a test
        - Variance, or sigma_n2 is given by:
          :math:`v_n = \frac{\sum^n_i{(x_i -m)^2}}{n(n-1)}`



Module API
==========
'''

import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
import numpy as np


# get profile from globals (cleaner)
if 'profile' not in globals()['__builtins__']:
    def profile(func):
        '''No memory profiling if "mem" not in arguments of the command line.
        '''
        return func


LOGGER = logging.getLogger('valjean')
ITYPE = np.int64
FTYPE = np.float64


class DictBuilder(ABC):
    '''General class to build dictionaries.

    This class implements a pattern for array results storage as dictionaries.
    It transforms the Tripoli-4 array strings in numpy arrays of a given number
    of dimensions, depending on the kind of array (spectrum, mesh, IFP result,
    etc.). General methods are implemented, mandatory methods are implemented
    as abstract and need to be derived in daughter classes.
    '''

    def __init__(self, colnames, lnbins):
        '''Initialization of DictBuilder.

        :param list(str) colnames: name of the columns/results
           (e.g. ``'score'`` and ``'sigma'`` for mesh, or
           ``'score'``, ``'sigma'``, ``'score/lethargy'`` for spectrum)
        :param list(int) lnbins: number of bins for each dimension
        '''
        LOGGER.debug("Initialisation of DictBuilder")
        self.bins = OrderedDict()
        self.units = {}
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays = {'default': np.full((lnbins), np.nan, dtype=dtype)}

    def add_array(self, name, colnames, lnbins):
        '''Add a new array to dictionary arrays with key name.

        :param str name: name of the new array (integrated_res, etc.)
        :type name: str
        :param colnames: list of the columns names (score, sigma, etc.)
        :type colnames: tuple(str)
        :param lnbins: number of bins in each dimension
        :type lnbins: list(int)
        '''
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays[name] = np.full((lnbins), np.nan, dtype=dtype)

    @abstractmethod
    def add_last_bins(self, data):
        '''Add last bins based on keywords presence in data.

        :param list data: mesh or spectrum results
        '''

    def _flip_bins_for_dim(self, dim, axis):
        '''Flip bins for dimension dim.

        :param str dim: dimension (examples: 'e', 't', 'mu', 'phi')
        :param int axis: axis of the dimension
                     (example: 'e' -> 3, 't' -> 4, 'mu' -> 5, 'phi' -> 6)
        '''
        LOGGER.debug("Bins %s avant flip: %s", dim, self.bins[dim])
        self.bins[dim] = np.flip(self.bins[dim], 0)
        for key, array in self.arrays.items():
            self.arrays[key] = np.flip(array, axis=axis)
        LOGGER.debug("et apres: %s", self.bins[dim])

    def flip_bins(self):
        '''Flip bins if given in decreasing order in the output listing.

        Depending on the required grid (GRID or DECOUPAGE) energies, times, mu
        and phi can be given from upper edge to lower edge. This is not
        convenient for post-traitements, especially plots. They have to be
        flipped at a moment, here or later, easiest is here, and all results
        will look the same :-).

        This function calls an internal function and needs to match the
        dimension with the number of the axis:
        ('e' → 3, 't' → 4, 'mu' → 5, 'phi' → 6)
        '''
        LOGGER.debug("In DictBuilder.flip_bins")
        key_axis = [(d, a) for a, d in enumerate(self.bins)]
        for key, axis in key_axis:
            bins = self.bins[key]
            if len(bins) > 1 and bins[0] > bins[1]:
                self._flip_bins_for_dim(key, axis)
            else:
                self.bins[key] = np.array(self.bins[key])

    @abstractmethod
    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum or mesh data.

        :param list data: mesh or spectrum results
        '''


class KinematicDictBuilder(DictBuilder):
    '''Class to build the dictionary for spectrum and mesh results as
    7-dimensions structured arrays.
    7-dimensions are: space (3, written ``'s0', 's1', 's2'``), energy
    (``'e'``), time (``'t'``), mu (``mu'``) and phi (``'phi'``) (direction
    angles).

    This class has 2 abstract methods, :meth:`_add_last_energy_bin` and
    :meth:`fill_arrays_and_bins`, so it cannot be initialized directly.

    .. data:: KinematicDictBuilder.VAR_FLAG

       ``{'t': 'time_step', 'mu': 'mu_angle_zone', 'phi': 'phi_angle_zone'}``:
       correspondance dictionary between internal name of dimensions and names
       in listings
    '''
    VAR_FLAG = {'t': 'time_step',
                'mu': 'mu_angle_zone',
                'phi': 'phi_angle_zone'}

    def __init__(self, colnames, lnbins):
        '''Initialization of KinematicDictBuilder.

        :param list(str) colnames: name of the columns/results
           (e.g. ``'score'`` and ``'sigma'`` for mesh, or
           ``'score'``, ``'sigma'``, ``'score/lethargy'`` for spectrum)
        :param list(int) lnbins: number of bins for each dimension
        '''
        LOGGER.debug("Initialisation of KinematicDictBuilder")
        try:
            assert len(lnbins) == 7
        except TypeError:
            LOGGER.error("lnbins should the list of number of bins")
            raise TypeError
        except AssertionError:
            LOGGER.error("Number of bins should be 7 (3 space dimensions, "
                         "1 energy, 1 time, 2 direction angles)")
            raise AssertionError
        super().__init__(colnames, lnbins)
        self.bins = OrderedDict([('s0', []), ('s1', []), ('s2', []),
                                 ('e', []), ('t', []),
                                 ('mu', []), ('phi', [])])
        self.units = {'s0': 'cm', 's1': 'unknown', 's2': 'unknown',
                      'e': 'MeV', 't': 's', 'mu': '', 'phi': 'rad',
                      'score': 'unknown', 'sigma': '%'}

    @abstractmethod
    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum or mesh.

        :param list data: mesh or spectrum results
        '''

    def _add_last_bin_for_dim(self, data, dim, lastbin):
        '''Add last bin for the dimension dim. Depending on order of the bins
        the last one will be inserted as first bin or added as last bin.

        :param list data: mesh or spectrum results
        :param str dim: dimension where the bin will be added (t, mu, phi)
        :param int lastbin: index of the bin in mesh or spectrum containing the
                         missing edge of the bins
        '''
        LOGGER.debug("Adding last bin for dim %s, flag = %s",
                     dim, KinematicDictBuilder.VAR_FLAG[dim])
        if len(self.bins[dim]) > 1 and self.bins[dim][0] > self.bins[dim][1]:
            self.bins[dim].insert(
                0, data[0][KinematicDictBuilder.VAR_FLAG[dim]][2])
        else:
            self.bins[dim].append(
                data[lastbin][KinematicDictBuilder.VAR_FLAG[dim]][2])

    def add_last_bins(self, data):
        '''Add last bins in energy, time, mu and phi direction angles.
        Based on keywords presence in data.

        :param list data: mesh or spectrum results
        '''
        self._add_last_energy_bin(data)
        nphibins = len(self.bins['phi']) if self.bins['phi'] else 1
        nmubins = len(self.bins['mu']) if self.bins['mu'] else 1
        # other possibility: if DictBuilder.VAR_FLAG['t'] in data[0]
        if 'time_step' in data[0]:
            self._add_last_bin_for_dim(data, 't', -int(nphibins)*int(nmubins))
        if 'mu_angle_zone' in data[0]:
            self._add_last_bin_for_dim(data, 'mu', -int(nphibins))
        if 'phi_angle_zone' in data[0]:
            self._add_last_bin_for_dim(data, 'phi', -1)

    @abstractmethod
    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum or mesh data.

        :param list data: mesh or spectrum results
        '''


class MeshDictBuilder(KinematicDictBuilder):
    '''Class specific to mesh dictionary -> mainly filling of bins and arrays.

    This class inherites from KinematicDictBuilder, see
    :class:`KinematicDictBuilder` for initialization and common methods.
    '''
    itime, imu, iphi = 0, 0, 0

    def __init__(self, colnames, lnbins):
        '''Initialization of MeshDictBuilder.

        :param list(str) colnames: name of the columns/results
           (e.g. ``'score'`` and ``'sigma'`` for mesh, or
           ``'score'``, ``'sigma'``, ``'score/lethargy'`` for spectrum)
        :param list(int) lnbins: number of bins for each dimension

        As no bins (centers or edges) are given for space mesh, they are
        initialised to index in mesh (in the considered direction), starting at
        0 by convention.
        '''
        LOGGER.debug("Initialisation of MeshDictBuilder")
        super().__init__(colnames, lnbins)

    def _fill_space_bins(self, meshvals):
        '''Fill the space bins.

        Two different cases are possible:

        * the default one, where only the cell indices are given: the space
          bins are set to all possible cell index in the 3 dimensions. For
          example: if there are 3 cells in `s0`, the bins will be 0, 1, 2.
          Only center of bins are given here (no possibility of calculation of
          a width).
        * a standard MESH was required with the option ``MESH_INFO`` in
          Tripoli-4: center of cells are given in all dimensions, the space
          bins will be set to these values. Width can be calculated (regular
          binning but possible in any case), but not done here. If needed for
          plot representation this will be proposed at the plotting step.

        :param list meshvals: mesh data for a given energy bin
                         ``[[[s0, s1, s2], score, sigma],...]``
        '''
        LOGGER.debug("Filling space bins")
        if isinstance(meshvals[0][1], float):
            self.bins['s0'] = np.arange(self.arrays['default'].shape[0])
            self.bins['s1'] = np.arange(self.arrays['default'].shape[1])
            self.bins['s2'] = np.arange(self.arrays['default'].shape[2])
        else:
            self.bins['s0'] = np.unique([smesh[1][0] for smesh in meshvals])
            self.bins['s1'] = np.unique([smesh[1][1] for smesh in meshvals])
            self.bins['s2'] = np.unique([smesh[1][2] for smesh in meshvals])

    def _fill_mesh_array(self, meshvals, name, ebin):
        '''Fill mesh array.

        :param list meshvals: mesh data for a given energy bin
                         ``[[[s0, s1, s2], score, sigma],...]``
        :param str name: name of the array to be filled ('default',
                     'eintegrated_mesh') for the moment
        :param int ebin: energy bin to fill in the array
        '''
        for smesh in meshvals:
            index = (smesh[0][0], smesh[0][1], smesh[0][2],
                     ebin, self.itime, self.imu, self.iphi)
            self.arrays[name][index] = np.array(tuple(smesh[-2:]),
                                                dtype=self.arrays[name].dtype)

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for mesh data.

        :param list data: mesh results

        Different arrays can be filled. Current possibilities are:

        * ``'default'`` (mandatory)
        * ``'eintegrated_mesh'``
          (facultative, integrated over energy, still splitted in space)
        * ``'integrated_res'`` (over energy and space, splitted in time)
        '''
        self._fill_space_bins(data[0]['meshes'][0]['mesh_vals'])
        for ires in data:
            LOGGER.debug("MeshDictBuilder.fill_arrays_bins, "
                         "keys: %s, number of elements: %d",
                         list(ires.keys()), len(ires))
            if 'time_step' in ires:
                self.itime = ires['time_step'][0]
                self.bins['t'].append(ires['time_step'][1])
            for inde, emesh in enumerate(ires['meshes']):
                if 'mesh_energyrange' in emesh:
                    if self.itime == 0:
                        self.bins['e'].append(emesh['mesh_energyrange'][1])
                    self._fill_mesh_array(emesh['mesh_vals'], 'default', inde)
                if 'mesh_energyintegrated' in emesh:
                    LOGGER.debug("Will fill mesh integrated in energy")
                    self._fill_mesh_array(emesh['mesh_vals'],
                                          'eintegrated_mesh', 0)
            if 'integrated_res' in ires:
                iintres = ires['integrated_res']
                index = (0, 0, 0, 0, self.itime, 0, 0)
                self.arrays['integrated_res'][index] = np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype)

    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from mesh data.

        :param list data: mesh results
        '''
        lastmesh = data[-1]['meshes']
        lastebin = self.arrays['default'].shape[3]-1
        self.bins['e'].append(lastmesh[lastebin]['mesh_energyrange'][2])


class SpectrumDictBuilderException(Exception):
    '''Exception to spectrum builder (bad bins)'''


class SpectrumDictBuilder(KinematicDictBuilder):
    '''Class specific to spectrum dictionary
    -> mainly filling of bins and arrays.

    This class inherites from KinematicDictBuilder, see
    :class:`KinematicDictBuilder` for initialization and common methods.
    '''
    itime, imu, iphi = 0, 0, 0

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum data.

        :param list data: spectrum results

        Current arrays possibly filled are:

        * ``'default'`` (mandatory)
        * ``'integrated_res'`` (over energy, splitted in time for the moment)
        '''
        LOGGER.debug("In SpectrumDictBuilder.fill_arrays_and_bins")
        for ispec in data:
            # Fill bins -> caution to not replicate them
            if 'time_step' in ispec:
                self.itime = ispec['time_step'][0]
                self.bins['t'].append(ispec['time_step'][1])
            if 'mu_angle_zone' in ispec:
                self.imu = ispec['mu_angle_zone'][0]
                if self.itime == 0:
                    self.bins['mu'].append(ispec['mu_angle_zone'][1])
            if 'phi_angle_zone' in ispec:
                self.iphi = ispec['phi_angle_zone'][0]
                if self.itime == 0 and self.imu == 0:
                    self.bins['phi'].append(ispec['phi_angle_zone'][1])

            # Fill spectrum values
            for ienergy, ivals in enumerate(ispec['spectrum_vals']):
                if self.itime == 0 and self.imu == 0 and self.iphi == 0:
                    self._check_bins(ispec['spectrum_vals'], ienergy)
                    self.bins['e'].append(ivals[0])
                index = (0, 0, 0, ienergy, self.itime, self.imu, self.iphi)
                array = np.array(tuple(ivals[2:]),
                                 dtype=self.arrays['default'].dtype)
                try:
                    self.arrays['default'][index] = array
                except IndexError:
                    LOGGER.error(
                        "IndexError: all (sub-)spectra should have the same "
                        "bins.\n"
                        "Please make sure you run Tripoli-4 with option '-a'.")
                    raise

            # Fill integrated result if exist
            if 'integrated_res' in ispec and 'integrated_res' in self.arrays:
                iintres = ispec['integrated_res']
                index = (0, 0, 0, 0, self.itime, self.imu, self.iphi)
                self.arrays['integrated_res'][index] = (np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype))

    def _check_bins(self, vals, ienergy):
        '''Check bins validity.'''
        if self.bins['e'] and vals[ienergy][0] != vals[ienergy-1][1]:
            raise SpectrumDictBuilderException(
                "Problem with energy bins: some bins are probably missing. "
                "Please make sure you run Tripoli-4 with '-a' option.")

    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum.

        :param list data: spectrum results
        '''
        self.bins['e'].append(data[-1]['spectrum_vals'][-1][1])


def _get_number_of_bins(spectrum):
    '''Get number of bins (time, mu and phi angles and energy).

    :param spectrum: input spectrum (full as various levels of list or
                     dictionary may be needed.
    :returns: 4 integers in following order

          :nphibins: number of bins in phi angle, default = 1
          :nmubins: number of bins in mu angle, default = 1
          :ntbins: number of bins in time, default = 1
          :nebins: number of bins in energy, no default

    Mu and phi angle are angles relative to the direction of the particle.
    '''
    # complication: time, mu and phi angles are always in that order
    # and only appears when changing value -> complication for number of "bins"
    # all the available coordinates are listed in element 0
    # if more than one loop necessary to get size of each
    nphibins = (spectrum[-1]["phi_angle_zone"][0]+1
                if "phi_angle_zone" in spectrum[0]
                else 1)
    nmubins = (spectrum[-int(nphibins)]["mu_angle_zone"][0]+1
               if "mu_angle_zone" in spectrum[0]
               else 1)
    ntbins = (spectrum[-int(nphibins)*int(nmubins)]["time_step"][0]+1
              if "time_step" in spectrum[0]
              else 1)
    nebins = len(spectrum[0]["spectrum_vals"])
    return nphibins, nmubins, ntbins, nebins


@profile
def convert_spectrum(spectrum, colnames=('score', 'sigma', 'score/lethargy')):
    '''Convert spectrum results in 7D NumPy structured array.

    :param list spectrum: list of spectra.
     Accepts time and (direction) angular grids.
    :param list(str) colnames: list of the names of the columns.
      Default = ``['score', 'sigma', 'score/lethargy']``
    :returns: dictionary with keys and elements

      * ``'spectrum'``: 7 dimensions NumPy structured array with related
        binnings as NumPy arrays
        ``v[s0, s1, s2, E, t, mu, phi] = ('score', 'sigma', 'score/lethargy')``
      * ``'disc_batchs'``: number of discarded batchs for the score
      * ``'bins'``: :class:`collections.OrderedDict` of the available bins
      * ``'units'``: dict containing units of dimensions (bins), score and
        sigma
      * ``'integrated_res'``: 7 dimensions NumPy structured array
        ``v[s0, s1, s2, E, t, mu, phi] = ('score', 'sigma')``;
        facultative, seen when time required alone and sometimes
        when neither time nor mu nor phi are required
      * ``'used_batch'``: number of used batchs (only if integrated result)
    '''
    nphibins, nmubins, ntbins, nebins = _get_number_of_bins(spectrum)
    LOGGER.debug("nebins = %d, ntbins = %d, nmubins = %d, nphibins = %d",
                 nebins, ntbins, nmubins, nphibins)
    vals = SpectrumDictBuilder(colnames,
                               [1, 1, 1, nebins, ntbins, nmubins, nphibins])
    if 'integrated_res' in spectrum[0]:
        vals.add_array('integrated_res', ['score', 'sigma'],
                       [1, 1, 1, 1, ntbins, nmubins, nphibins])
    # Fill spectrum, bins and integrated result if exists
    vals.fill_arrays_and_bins(spectrum)
    vals.add_last_bins(spectrum)
    # Flip bins
    vals.flip_bins()
    # Build dictionary to be returned
    convspec = {'disc_batch': spectrum[0]['disc_batch'],
                'array': vals.arrays['default'],
                'bins': vals.bins,
                'units': vals.units}
    if 'units' in spectrum[0]:
        convspec['units']['e'] = spectrum[0]['units'][0]
        convspec['units']['score'] = spectrum[0]['units'][1]
        convspec['units']['sigma'] = spectrum[0]['units'][2]
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = vals.arrays['integrated_res']
        convspec['used_batch'] = spectrum[0]['integrated_res']['used_batch']
    return convspec


def _get_number_of_space_bins(meshvals):
    '''Get number of space bins used in meshes.

    This function is mainly used when meshes are not entirely saved (tests, or
    useless in the considered case). The limit on the number of lines of mesh
    in the listing does not necessarly match a completed mesh dimension.

    :param list meshvals: list of meshes, with mesh
                          ``[[s0, s1, s2] score sigma]``
                          s0, s1 and s2 being the space coordinates
    :returns: 3 integers in following order

        :ns0bins: number of bins in the s0 dimension
        :ns1bins: number of bins in the s1 dimension
        :ns2bins: number of bins in the s2 dimension
    '''
    lastspacebin = meshvals[-1][0]
    ns0bins = lastspacebin[0]+1
    ns2bins = (meshvals[-int(lastspacebin[2]+2)][0][2]+1
               if lastspacebin[2]+1 < len(meshvals)
               else lastspacebin[2]+1)
    maxbins1 = (lastspacebin[1]*ns2bins+lastspacebin[2]+2
                if lastspacebin[0] != 0
                else lastspacebin[2]+2)
    if LOGGER.isEnabledFor(logging.DEBUG):
        if len(meshvals) > maxbins1:
            if meshvals[-int(maxbins1)][0][1] > lastspacebin[1]:
                LOGGER.debug("will use meshvals[-int(maxbins1)] = %s instead "
                             "of lastspacebin = %s",
                             meshvals[-int(maxbins1)], lastspacebin)
            else:
                LOGGER.debug("will use lastspacebin = %s instead of "
                             "meshvals[-int(maxbins1)] = %s",
                             lastspacebin, meshvals[-int(maxbins1)])
        else:
            LOGGER.debug("will use lastspacebin = %s as "
                         "len(meshvals) > maxbins1", lastspacebin)
    ns1bins = (meshvals[-int(maxbins1)][0][1]+1
               if (len(meshvals) > maxbins1
                   and meshvals[-int(maxbins1)][0][1] > lastspacebin[1])
               else lastspacebin[1]+1)
    return ns0bins, ns1bins, ns2bins


def get_energy_bins(meshes):
    '''Get the number of energy bins for mesh.

    :param list meshes: mesh, list of dictionaries, at least one should have
                        the key ``'mesh_energyrange'``
    '''
    nbebins = 0
    for mesh in meshes:
        if 'mesh_energyrange' in mesh:
            nbebins += 1
    return nbebins


@profile
def convert_mesh(meshres):
    '''Convert mesh in 7-dimensions NumPy array.

    :param list meshres: Mesh result constructed as:
      ``[{'time_step': [], 'meshes': [], 'integrated_res': {}}, {}]``,
      see :ref:`eponine-spectrummesh-fill` for more details.

    :returns: python dictonary with keys

        * ``'array'``: NumPy structured array of dimension 7
          ``v[s0, s1 ,s2, E, t, mu, phi] = ('score', 'sigma')``
        * ``'bins'``: :class:`collections.OrderedDict` of the available bins
        * ``'units'``: dict containing units of dimensions (bins), score and
          sigma
        * ``'eintegrated_array'``: 7-dimensions NumPy structured array
          ``v[s0,s1,s2,E,t,mu,phi] = ('score', 'sigma')``
          corresponding to mesh integrated on energy (facultative)
        * ``'integrated_res'``: 7 dimensions NumPy structured array
          ``v[s0,s1,s2,E,t,mu,phi] = (score, sigma)``
          corresponding to mesh integrated over energy and space;
          *facultative*, available when time grid is required (so
          corresponds to integrated results splitted in time)
        * ``'used_batch'``: number of used batchs (only if integrated result)
    '''
    LOGGER.debug("In convert_mesh_class")
    LOGGER.debug("Number of mesh results: %d", len(meshres))
    LOGGER.debug("keys of meshes: %s", list(meshres[0]['meshes'].keys()))
    LOGGER.debug("elts in meshes: %d", len(meshres[0]['meshes']))
    # dimensions/number of bins of space coordinates are given by last bin
    ns0bins, ns1bins, ns2bins = _get_number_of_space_bins(
        meshres[0]['meshes'][0]['mesh_vals'])
    # ntbins supposes for the moment no mu or phi bins
    ntbins = (meshres[-1]['time_step'][0]+1
              if "time_step" in meshres[0]
              else 1)
    nebins = get_energy_bins(meshres[0]['meshes'])
    LOGGER.debug("ns0bins = %d, ns1bins = %d, ns2bins = %d, ntbins = %d, "
                 "nebins = %d", ns0bins, ns1bins, ns2bins, ntbins, nebins)
    # up to now no mesh splitted in mu or phi angle seen, update easy now
    vals = MeshDictBuilder(['score', 'sigma'],
                           [ns0bins, ns1bins, ns2bins, nebins, ntbins, 1, 1])
    # mesh integrated on energy (normally the last mesh)
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        vals.add_array('eintegrated_mesh', ['score', 'sigma'],
                       [ns0bins, ns1bins, ns2bins, 1, ntbins, 1, 1])
    # integrated result (space and energy)
    if 'integrated_res' in meshres[0]:
        vals.add_array('integrated_res', ['score', 'sigma'],
                       [1, 1, 1, 1, ntbins, 1, 1])
    # fill arrays, bins, put them in inceasing order
    vals.fill_arrays_and_bins(meshres)
    vals.add_last_bins(meshres)
    vals.flip_bins()
    # build dictionary to be returned
    convmesh = {'array': vals.arrays['default'],
                'bins': vals.bins,
                'units': vals.units}
    if 'unit' in meshres[0]:
        convmesh['units']['score'] = meshres[0]['unit']
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        convmesh['eintegrated_array'] = vals.arrays['eintegrated_mesh']
    if 'integrated_res' in meshres[0]:
        convmesh['integrated_res'] = vals.arrays['integrated_res']
        convmesh['used_batch'] = meshres[0]['integrated_res']['used_batch']
    return convmesh


class NuSpectrumDictBuilder(DictBuilder):
    '''Class specific to spectrum dictionary
    -> mainly filling of bins and arrays.

    This class inherites from DictBuilder, see :class:`DictBuilder` for
    initialization and common methods.
    '''

    def __init__(self, colnames, lnbins):
        super().__init__(colnames, lnbins)
        self.bins = OrderedDict([('nu', [])])
        self.units = {'nu': ''}

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum data.

        :param list data: spectrum results

        Current arrays possibly filled are:

        * ``'default'`` (mandatory)
        * ``'integrated_res'`` (over nu)
        '''
        LOGGER.debug("In NuSpectrumDictBuilder.fill_arrays_and_bins")
        for ispec in data:
            # Fill spectrum values
            for inu, ivals in enumerate(ispec['spectrum_vals']):
                self._check_bins(ispec['spectrum_vals'], inu)
                self.bins['nu'].append(ivals[0])
                index = (inu, )
                array = np.array(tuple(ivals[2:]),
                                 dtype=self.arrays['default'].dtype)
                try:
                    self.arrays['default'][index] = array
                except IndexError:
                    LOGGER.error(
                        "IndexError: all (sub-)spectra should have the same "
                        "bins.\n"
                        "Please make sure you run Tripoli-4 with option '-a'.")
                    raise

            # Fill integrated result if exist
            if 'integrated_res' in ispec and 'integrated_res' in self.arrays:
                iintres = ispec['integrated_res']
                index = (0, )
                self.arrays['integrated_res'][index] = (np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype))

    def _check_bins(self, vals, inu):
        '''Check bins validity.'''
        if self.bins['nu'] and vals[inu][0] != vals[inu-1][1]:
            raise SpectrumDictBuilderException(
                "Problem with energy bins: some bins are probably missing. "
                "Please make sure you run Tripoli-4 with '-a' option.")

    def add_last_bins(self, data):
        '''Add last bin in nu from spectrum.

        :param list data: spectrum results
        '''
        self.bins['nu'].append(data[-1]['spectrum_vals'][-1][1])


def convert_nu_spectrum(spectrum, colnames=('score', 'sigma')):
    '''Convert nu spectrum results in 1D NumPy structured array.

    :param list spectrum: list of spectra.
     Accepts time and (direction) angular grids.
    :param list(str) colnames: list of the names of the columns.
      Default = ``['score', 'sigma']``
    :returns: dictionary with keys and elements

      * ``'array'``: 1 dimension NumPy structured array with related
        binnings as NumPy arrays
        ``v[nu] = ('score', 'sigma')``
      * ``'disc_batchs'``: number of discarded batchs for the score
      * ``'bins'``: :class:`collections.OrderedDict`, nu binning
      * ``'units'``: dict containing units of dimensions (bins), score and
        sigma
      * ``'integrated_res'``: 1 dimension NumPy structured array
        ``v[nu] = ('score', 'sigma')``
      * ``'used_batch'``: number of used batchs (only if integrated result)
    '''
    nnubins = len(spectrum[0]["spectrum_vals"])
    LOGGER.debug("nnubins = %d", nnubins)
    vals = NuSpectrumDictBuilder(colnames, [nnubins])
    if 'integrated_res' in spectrum[0]:
        vals.add_array('integrated_res', ['score', 'sigma'], [1])
    # Fill spectrum, bins and integrated result if exists
    vals.fill_arrays_and_bins(spectrum)
    vals.add_last_bins(spectrum)
    # Flip bins
    vals.flip_bins()
    # Build dictionary to be returned
    convspec = {'disc_batch': spectrum[0]['disc_batch'],
                'array': vals.arrays['default'],
                'bins': vals.bins,
                'units': vals.units}
    if 'units' in spectrum[0]:
        convspec['units']['nu'] = spectrum[0]['units'][0]
        convspec['units']['score'] = spectrum[0]['units'][1]
        convspec['units']['sigma'] = spectrum[0]['units'][2]
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = vals.arrays['integrated_res']
        convspec['used_batch'] = spectrum[0]['integrated_res']['used_batch']
    return convspec


class ZASpectrumDictBuilder(DictBuilder):
    '''Class specific to spectrum dictionary to parse arrays indexed by Z and A
    numbers (isotopes).

    This class inherites from DictBuilder, see :class:`DictBuilder` for
    initialization and common methods.
    '''

    def __init__(self, colnames, bins):
        '''Initialization of ZASpectrumDictBuilder.

        :param list(str) colnames: name of the columns/results
           (``'score'`` and ``'sigma'`` in the current case)
        :param bins: Z, A bins
        :type bins: :class:`collections.OrderedDict` of
            (str, :obj:`numpy.ndarray` (int))
        '''
        super().__init__(colnames, [bins['Z'].size, bins['A'].size])
        self.bins = bins  # OrderedDict([('Z', []), ('A', [])])
        self.units = {'Z': '', 'A': '', 'score': 'unknown', 'sigma': '%'}

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum data.

        :param list data: spectrum results

        Current arrays possibly filled are:

        * ``'default'`` (mandatory)
        * ``'integrated_res'`` (over Z and A, i.e. all isotopes)
        '''
        LOGGER.debug("In ZASpectrumDictBuilder.fill_arrays_and_bins")
        for ispec in data:
            # Fill spectrum values
            for ivals in ispec['spectrum_vals']:
                # no energy bins for the moment
                # self._check_bins(ispec['spectrum_vals'], inu)
                index = (ivals[0]-np.min(self.bins['Z']),
                         ivals[1]-np.min(self.bins['A']))
                array = np.array(tuple(ivals[2:]),
                                 dtype=self.arrays['default'].dtype)
                try:
                    self.arrays['default'][index] = array
                except IndexError:
                    LOGGER.error(
                        "IndexError: all (sub-)spectra should have the same "
                        "bins.\n"
                        "Please make sure you run Tripoli-4 with option '-a'.")
                    raise
            # Fill integrated result if exist
            if 'integrated_res' in ispec and 'integrated_res' in self.arrays:
                iintres = ispec['integrated_res']
                index = (0, )
                self.arrays['integrated_res'][index] = (np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype))

    def add_last_bins(self, data):
        '''Add last bin in Z,A from spectrum, not applicable in this case.

        :param list data: spectrum results
        '''


def _get_za_bins(values):
    '''Determine the bins in Z, A before filling the array from the values.

    :param list values: spectrum results
    :returns: bins: Z, A bins as a  :class:`collections.OrderedDict` of
            (str, :obj:`numpy.ndarray` (int))
    '''
    z_vals = [vals[0] for vals in values]
    a_vals = [vals[1] for vals in values]
    bins = OrderedDict()
    bins['Z'] = np.unique(z_vals)
    bins['A'] = np.unique(a_vals)
    if bins['Z'].size * bins['A'].size != len(values):
        LOGGER.warning("Length of the Z,A spectrum does not correspnds to "
                       "len(Z) * len(A). This may be expected if values are "
                       "required around expected isotopes.")
    return bins


def convert_za_spectrum(spectrum, colnames=('score', 'sigma')):
    '''Convert nu spectrum results in 1D NumPy structured array.

    :param list spectrum: list of spectra.
     Accepts time and (direction) angular grids.
    :param list(str) colnames: list of the names of the columns.
      Default = ``['score', 'sigma']``
    :returns: dictionary with keys and elements

      * ``'array'``: 1 dimension NumPy structured array with related
        binnings as NumPy arrays
        ``v[Z, A] = ('score', 'sigma')``
      * ``'disc_batchs'``: number of discarded batchs for the score
      * ``'bins'``: :class:`collections.OrderedDict`, Z and A binnings
      * ``'units'``: dict containing units of dimensions (bins), score and
        sigma
      * ``'integrated_res'``: 1 dimension NumPy structured array
        ``v[Z, A] = ('score', 'sigma')``
      * ``'used_batch'``: number of used batchs (only if integrated result)

    Remark: no call to add_last_bins or flip_bins is done here as no energy,
    time or space bins are given for the moment.
    '''
    LOGGER.debug("nzabins = %d", len(spectrum[0]["spectrum_vals"]))
    bins = _get_za_bins(spectrum[0]["spectrum_vals"])
    vals = ZASpectrumDictBuilder(colnames, bins)
    if 'integrated_res' in spectrum[0]:
        vals.add_array('integrated_res', ['score', 'sigma'], [1]*len(bins))
    # Fill spectrum, bins and integrated result if exists
    vals.fill_arrays_and_bins(spectrum)
    # Build dictionary to be returned
    convspec = {'disc_batch': spectrum[0]['disc_batch'],
                'array': vals.arrays['default'],
                'bins': vals.bins,
                'units': vals.units}
    if 'units' in spectrum[0]:
        convspec['units']['score'] = spectrum[0]['units'][1]
        convspec['units']['sigma'] = spectrum[0]['units'][2]
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = vals.arrays['integrated_res']
        convspec['used_batch'] = spectrum[0]['integrated_res']['used_batch']
    return convspec


@profile
def convert_keff_with_matrix(res):
    '''Convert |keff| results in NumPy matrices.

    :param dict res: |keff| results
    :returns: dict filled as:

    ::

        {'used_batch': int, 'estimators': [str],
         'full_comb_estimation': numpy.array,
         'keff_matrix': numpy.array,
         'correlation_matrix': numpy.array,
         'sigma_matrix': numpy.array}

    '''
    # not converged cases a tester...
    LOGGER.debug("In common.convert_keff_with_matrix")
    if 'not_converged' in res or 'warning' in res:
        return res
    dtkeff = np.dtype([('keff', FTYPE), ('sigma', FTYPE)])
    fullcombres = (np.array(tuple(res['full_comb_estimation']), dtype=dtkeff)
                   if len(res['full_comb_estimation']) > 1
                   else res['full_comb_estimation'][0])
    keffnames = list(zip(*res['res_per_estimator']))[0]
    nbkeff = len(res['res_per_estimator'])
    keffmat = np.full([nbkeff, nbkeff], np.nan)
    corrmat = np.identity(nbkeff)
    sigmat = np.full([nbkeff, nbkeff], np.nan)
    for ikeff, keffname in enumerate(keffnames):
        keffmat[ikeff, ikeff] = res['res_per_estimator'][ikeff][1]
        sigmat[ikeff, ikeff] = res['res_per_estimator'][ikeff][2]
        for jcorr in range(len(res['correlation_mat'])):
            lkeff = res['correlation_mat'][jcorr]
            # list needed as type = pyparsing result
            if keffname in lkeff[0]:
                iokeff = keffnames.index(
                    [okeff for okeff in lkeff[0] if okeff != keffname][0])
                keffmat[ikeff, iokeff] = (lkeff[2]
                                          if not isinstance(lkeff[2], str)
                                          else np.nan)
                corrmat[ikeff, iokeff] = (lkeff[1]
                                          if not isinstance(lkeff[1], str)
                                          else np.nan)
                sigmat[ikeff, iokeff] = (lkeff[3]
                                         if not isinstance(lkeff[3], str)
                                         else np.nan)
            else:
                continue
    return {'used_batch': res['used_batch'],
            'keff_per_estimator_res': {'estimators': keffnames,
                                       'keff_matrix': keffmat,
                                       'correlation_matrix': corrmat,
                                       'sigma_matrix': sigmat},
            'keff_combination_res': fullcombres}


def convert_keff(res):
    '''Convert |keff| results in dictionary containing NumPy objects.

    :param dict res: keff results
    :returns: dict containing

    ::

     {'used_batch': int, 'estimators': [str, ],
      'full_comb_estimation': numpy.array,
      'res_per_estimator': {'estimator': numpy.array, },
      'correlation_matrix': {('estimator1', 'estimator2'): numpy.array, }}

    See :ref:`eponine-keff-stdarrays` for more details.
    '''
    LOGGER.debug("[38;5;56mClefs:%s[0m", list(res.keys()))
    usedbatchs = res['used_batch']
    if 'not_converged' in res:
        return {'used_batch': res['used_batch'],
                'not_converged': res['not_converged']}
    keffnames = list(zip(*res['res_per_estimator']))[0]
    keffres = {}
    dtkeff = np.dtype([('keff', FTYPE), ('sigma', FTYPE)])
    for keff in res['res_per_estimator']:
        keffres[keff[0]] = np.array(tuple(keff[1:]), dtype=dtkeff)
    fullcombres = (np.array(tuple(res['full_comb_estimation']), dtype=dtkeff)
                   if len(res['full_comb_estimation']) == 2
                   else res['full_comb_estimation'])
    corrres = {}
    dtcorr = np.dtype([('correlations', FTYPE),
                       ('combined values', FTYPE),
                       ('combined sigma%', FTYPE)])
    for elt in res['correlation_mat']:
        corrval = (elt[1:]
                   if all(isinstance(ielt, FTYPE) for ielt in elt[1:])
                   else [np.nan if isinstance(x, str) else x for x in elt[1:]])
        corrres[tuple(elt[0])] = np.array(tuple(corrval), dtype=dtcorr)
    return {'used_batch': usedbatchs,
            'estimators': keffnames,
            'res_per_estimator': keffres,
            'full_comb_estimation': fullcombres,
            'correlation_matrix': corrres}


class GreenBandsDictBuilder(DictBuilder):
    '''Class to build Green bands spectrum results.'''

    def __init__(self, colnames, lnbins):
        '''Initialisation of GreenBandsDictBuilder.'''
        super().__init__(colnames, lnbins)
        self.bins = OrderedDict([('se', []), ('ns', []),
                                 ('u', []), ('v', []), ('w', []),
                                 ('e', [])])
        self.units = {'se': 'MeV', 'ns': '', 'u': '', 'v': '', 'w': '',
                      'e': 'MeV', 'score': 'unknown', 'sigma': '%'}

    def add_last_bins(self, data):
        '''Add last bins from source energy bins and energy bins.
        Also remove duplicates in source number and source tabulations.

        :param data: Green bands results
        '''
        if ((len(self.bins['se']) > 1
             and self.bins['se'][0] > self.bins['se'][1])):
            self.bins['se'].append(data[-1]['gb_step_desc'][1])
        else:
            self.bins['se'].insert(0, data[0]['gb_step_desc'][1])
        spectrum = data[0]['gb_step_res'][0]['spectrum_res'][0]
        self.bins['e'].append(spectrum['spectrum_vals'][-1][1])
        for key in ('ns', 'u', 'v', 'w'):
            self.bins[key] = np.unique(self.bins[key])

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins from Green bands result.

        :param data: Green bands results
        '''
        for ist, gbstep in enumerate(data):
            istep = gbstep['gb_step_desc'][0]
            self.bins['se'].append(gbstep['gb_step_desc'][2])
            for ires, gbres in enumerate(gbstep['gb_step_res']):
                isource = gbres['gb_source']
                if ist == 0:
                    self.bins['ns'].append(isource[0])
                    if len(isource) > 1:
                        self.bins['u'].append(isource[1][0])
                        self.bins['v'].append(isource[1][1])
                        self.bins['w'].append(isource[1][2])
                if len(gbres['spectrum_res']) > 1:
                    LOGGER.warning("\x1b[31mMore than one spectrum_res while "
                                   "only one foreseen for the moment\x1b[0m")
                ispectrum = gbres['spectrum_res'][0]['spectrum_vals']
                for iebin, ivals in enumerate(ispectrum):
                    if ist == 0 and ires == 0:
                        self.bins['e'].append(ivals[0])
                    locind = ((istep, isource[0],
                               isource[1][0], isource[1][1], isource[1][2],
                               iebin) if len(isource) > 1
                              else (istep, isource[0], 0, 0, 0, iebin))
                    self.arrays['default'][locind] = np.array(
                        tuple(ivals[2:]), dtype=self.arrays['default'].dtype)


def _get_gb_nbins(gbres):
    '''Get the number of bins for Green bands results.

    :param gbres: Green bands results
    :returns: tuple(int)
    '''
    lastsource = gbres[-1]['gb_step_res'][-1]['gb_source']
    hassourcetab = len(lastsource) > 1
    spectrum = gbres[0]['gb_step_res'][0]['spectrum_res'][0]
    index = (len(gbres),  # number of steps (= number of bins of source energy)
             lastsource[0]+1,  # number of sources
             lastsource[1][0]+1 if hassourcetab else 1,  # number of u bins
             lastsource[1][1]+1 if hassourcetab else 1,  # number of v bins
             lastsource[1][2]+1 if hassourcetab else 1,  # number of w bins
             len(spectrum['spectrum_vals']))  # number of energy bins
    return index


def convert_green_bands(gbs):
    '''Convert Green bands contribution results in arrays, using same schema as
    spectrum or mesh.

    :param gbs: Green bands results
    :returns: dict
    '''
    LOGGER.debug("In convert_green_bands")
    lnbins = _get_gb_nbins(gbs)
    gbdb = GreenBandsDictBuilder(('score', 'sigma', 'score/lethargy'), lnbins)
    gbdb.fill_arrays_and_bins(gbs)
    gbdb.add_last_bins(gbs)
    gbdb.flip_bins()
    spectrum = gbs[0]['gb_step_res'][0]['spectrum_res'][0]
    return {'array': gbdb.arrays['default'],
            'bins': gbdb.bins,
            'units': gbdb.units,
            'disc_batch': spectrum['disc_batch']}


def convert_generic_adjoint(res):
    '''Convert adjoint results in association of dictionaries and NumPy array.

    :param list res: Adjoint result got thanks to IFP or Wielandt method to be
      converted
    :returns: list(dict) each dictionary containing

      * metadata like nucleus name, family number or cycle length
      * data saved as ``'integrated_res'``

    Units, if available, and used batch are also saved under the integrated
    result.

    This structure is compatible with the response book and the index.
    Selections are done like in the default score cases.
    '''
    keys = ('score', 'sigma')
    tlist = []
    loctype = list(res['adj_res'].keys())[0]
    index = loctype.split('_')[2:]
    adjres = res.pop('adj_res')
    if len(adjres.asDict()) != 1:
        LOGGER.warning("Issue: more than one key for adjoint result")
    for ires in adjres[loctype]:
        mydict = {}
        find = ires[0]
        nindex = index[0]
        mydict[nindex] = find
        if len(ires) == 1:
            mydict['integrated_res'] = {
                'not_converged': "No result available"}
            mydict['integrated_res'].update(res.asDict())
            tlist.append(mydict)
            continue
        if isinstance(ires[1], FTYPE):
            mydict['integrated_res'] = dict(zip(keys, tuple(ires[1:])))
            mydict['integrated_res'].update(res.asDict())
            tlist.append(mydict)
        else:
            for iires in ires[1:]:
                myrdict = mydict.copy()
                lind = iires[0]
                nindex2 = index[1]
                myrdict[nindex2] = lind
                myrdict['integrated_res'] = dict(zip(keys, tuple(iires[1:])))
                myrdict['integrated_res'].update(res.asDict())
                tlist.append(myrdict)
    return tlist


class AdjointCritEdDictBuilderException(Exception):
    '''Exception to adjoint criticality edition array builder (bad bins)'''


class AdjointCritEdDictBuilder(KinematicDictBuilder):
    '''Specific class to build IFP adjoint criticality edition results as a
    KinematicDictBuilder.
    '''
    VARS = ['X', 'Y', 'Z', 'Phi', 'Theta', 'E', 'T']

    def __init__(self, colnames, bins):
        '''Initialisation of AdjointCritEdDictBuilder.

        Caution: in that case bins are direclty sent, not 'only' their number
        as done per default in :class:`DictBuilder`.

        Order of the kinematic variables is also different from the usual
        spectra or mesh. Time is a 'fake' dimension (only one bin available, no
        splitting allowed there).

        Dimensions are then, in bins order and array order (seen in shape):
        ``('X', 'Y', 'Z', 'Phi', 'Theta', 'E', 't')```.

        Dimensions not present in the screened result are set to empty array in
        the bins :class:`collections.OrderedDict` and to 1 in the array shape.
        '''
        lnbins, odbins = [], OrderedDict()
        for var in AdjointCritEdDictBuilder.VARS:
            if var in bins:
                lnbins.append(bins[var].size-1)
                odbins[var] = bins[var]
            else:
                lnbins.append(1)
                odbins[var] = np.array([])
        super().__init__(colnames, lnbins)
        self.bins = odbins
        self.units = {'X': 'cm', 'Y': 'cm', 'Z': 'cm',
                      'Phi': 'rad', 'Theta': 'rad', 'E': 'MeV', 'T': 's',
                      'score': 'unknown', 'sigma': '%'}

    def _fill_array(self, data):
        '''Fill array of results from IFP adjoint criticality edition.

        Results are looping in the following order: X, Y, Z, Phi, Theta, E.
        This is then the order to fill the array (indices).
        '''
        for _iv, val in enumerate(data):
            lindex = [0]*7
            pdims = 1
            for dim, bsize in enumerate([b.size for b in self.bins.values()]):
                lindex[dim] = (_iv//pdims) % (bsize-1 if bsize else 1)
                pdims *= bsize-1 if bsize else 1
            index = tuple(lindex)
            array = np.array(tuple(val), dtype=self.arrays['default'].dtype)
            self.arrays['default'][index] = array
        LOGGER.debug("array.shape: %s", self.arrays['default'].shape)

    def fill_arrays_and_bins(self, data):
        '''Only fill array in IFP adjoint criticality edition case.'''
        self._fill_array(data)

    def _add_last_energy_bin(self, data):
        pass


class VolAdjCritEdDictBuilder(DictBuilder):
    '''Class to build spectrum per volume instead of per kinematic variables.
    E is still present.
    '''

    def __init__(self, colnames, bins):
        '''Initialisation of VolAdjCritEdDictBuilder.

        Caution: in that case bins are direclty sent, not 'only' their number
        as done per default in :class:`DictBuilder`.

        Two kinds of bins are expected: Vol (volume id in geometry) and E
        (energy).
        '''
        LOGGER.debug("VolAdjCritEdDictBuilder: bins = %s", bins)
        lnbins = [bins['Vol'].size, bins['E'].size-1]
        LOGGER.debug("Number of bins per dimension: %s", lnbins)
        super().__init__(colnames, lnbins)
        self.bins = bins
        self.units = {'Vol': '', 'E': 'MeV', 'score': 'unknown', 'sigma': '%'}

    def _fill_array(self, data):
        '''Fill array of results from IFP adjoint criticality edition when
        spectrum is given by volume.

        Results are looping in the following order: Vol, E.
        This is then the order to fill the array (indices).
        '''
        for _iv, val in enumerate(data):
            index = (_iv % self.bins['Vol'].size,
                     (_iv//self.bins['Vol'].size % (self.bins['E'].size-1)))
            self.arrays['default'][index] = np.array(
                tuple(val), dtype=self.arrays['default'].dtype)
        LOGGER.debug("array.shape: %s", self.arrays['default'].shape)

    def fill_arrays_and_bins(self, data):
        '''Only fill array in IFP adjoint criticality edition case.'''
        self._fill_array(data)

    def add_last_bins(self, data):
        pass


def _get_ace_kin_bins(columns, values):
    '''Initialize bins for IFP adjoint criticality edition.'''
    bins = OrderedDict()
    for idim, dim in enumerate(columns):
        bins[dim] = np.unique(values[:, idim*2:(idim+1)*2])
    total_dim = np.prod([val.size-1 for val in bins.values()])
    if total_dim != values.shape[0]:
        raise AdjointCritEdDictBuilderException(
            "Issue with the bins: the total dimension ({0}) does not match "
            "the length of the table in the output ({1}), please check the "
            "-a option has been used.".format(total_dim, values.shape[0]))
    return bins


def _get_ace_vol_bins(values):
    '''Initialize bins for IFP adjoint criticality edition.'''
    bins = OrderedDict()
    bins['Vol'] = np.array(np.unique(values[:, 0]), dtype=ITYPE)
    bins['E'] = np.array(np.unique(values[:, 1:3]), dtype=FTYPE)
    total_dim = bins['Vol'].size * (bins['E'].size-1)
    if total_dim != values.shape[0]:
        raise AdjointCritEdDictBuilderException(
            "Issue with the bins: the total dimension ({0}) does not match "
            "the length of the table in the output ({1}), please check the "
            "-a option has been used.".format(total_dim, values.shape[0]))
    return bins


def _crit_edition_dict_builder(columns, values):
    '''Return the needed DictBuilder for IFP adjoint criticality edition
    according to columns names.

    :param list(str) columns: columns names
    :param list(int,float) values: bins edges or centers
    :returns: :class:`~AdjointCritEdDictBuilder` or
              :class:`~VolAdjCritEdDictBuilder`.
    '''
    if 'Vol' in columns:
        bins = _get_ace_vol_bins(values)
        return VolAdjCritEdDictBuilder(['score', 'sigma'], bins)
    bins = _get_ace_kin_bins(columns, values)
    return AdjointCritEdDictBuilder(['score', 'sigma'], bins)


def convert_crit_edition(res):
    '''Convert IFP adjpint criticality edition results in standard kinematic
    result.
    '''
    LOGGER.debug('In convert_crit_edition')
    if 'score' not in res['columns'][-2]:
        raise ValueError("Issue with the columns names, not foreseen case "
                         "(score should be second to last, last being sigma)")
    acedb = _crit_edition_dict_builder(
        res['columns'][:-2],
        np.array([dval[:-2] for dval in res['values']]))
    acedb.fill_arrays_and_bins([vals[-2:] for vals in res['values']])
    acedb.flip_bins()
    convres = {'array': acedb.arrays['default'],
               'bins': acedb.bins,
               'units': acedb.units}
    return {'adj_crit_ed_res': convres}


def convert_kij_sources(res):
    '''Convert |kij| sources result in python dictionary in which |kij| sources
    values are converted in a NumPy array.

    :param dict res: |kij| sources
    :returns: same dictionary with :obj:`numpy.ndarray` for |kij| sources
      values
    '''
    kijs = {}
    for key in res:
        if key == 'kij_sources_vals':
            kijs[key] = np.array(res[key])
        else:
            kijs[key] = res[key]
    return kijs


def convert_kij_result(res):
    '''Convert |kij| result in NumPy objects and return a dictionary.

    :param dict res: |kij| result with keys ``'used_batch'``,
      ``'kij_eigenval'``, ``'kij_eigenvec'``, ``'kij_matrix'``
    :returns: dictionary containing the same keys but with different types:

    ::

      {'used_batch': int, 'kijmkeff_res': float, 'kijdomratio': float,
      'kij_eigenval': numpy.array, 'kij_eigenvec': numpy.array,
      'kij_matrix': numpy.array}

    For more details see :ref:`eponine-kij-result`.
    '''
    # eigen values (re, im) -> store as array of complex
    reegval = np.array(list(zip(*res['kij_eigenval']))[0])
    imegval = np.array(list(zip(*res['kij_eigenval']))[1])
    egvals = reegval + 1j*imegval
    # eigen vectors
    egvecs = (np.array(res['kij_eigenvec'])
              if isinstance(res['kij_eigenvec'], list)
              else res['kij_eigenvec'])
    # kij matrix
    kijmat = (np.array(res['kij_matrix'])
              if isinstance(res['kij_matrix'], list)
              else res['kij_matrix'])
    return {'used_batch': res['used_batch'],
            'kijmkeff_res': res['kijmkeff_res'][0],
            'kijdomratio': res['kijmkeff_res'][1],
            'kij_eigenval': egvals,
            'kij_eigenvec': egvecs,
            'kij_matrix': kijmat
            }


def convert_kij_keff(res):
    '''Convert matrices in NumPy array or matrix when estimating |keff| from
    |kij|

    :param dict res: |kij| result from |keff| result block
    :returns: dictionary containing `NumPy` arrays:

    ::

       {'estimator': str,
        'batchs_kept': int,
        'kij-keff': float,
        'nbins': int,
        'spacebins': numpy.array of int with shape (nbins,) or (nbins, 3), the
            latter case corresponding to space mesh,
        'eigenvector': numpy.array,
        'keff_KIJ_matrix': numpy.array,
        'keff_StdDev_matrix': numpy.array,
        'keff_sensibility_matrix': numpy.array}

    Keys ``'nbins'`` and ``'spacebins'`` are facultative.

    For more details see :ref:`eponine-kij-in-keff`.
    '''
    LOGGER.debug("Clefs: %s", str(list(res.keys())))
    egvec = np.array(list(zip(*res['eigenvector']))[1])
    nbins = res['nb_fissile_vols'] if 'nb_fissile_vols' in res else len(egvec)
    if nbins != len(egvec):
        LOGGER.warning("[31mIssue in number of fissile volumes "
                       "and size of eigenvector[0m")
    spacebins = np.array(res['keff_KIJ_matrix'][0])
    if spacebins.shape[0] != len(res['keff_KIJ_matrix'][1:]):
        LOGGER.warning("[31mStrange: not the dimension in space mesh and "
                       "matrix, matrix expected to be squared[0m")
    if spacebins.shape[0] != nbins:
        LOGGER.warning("[31mStrange: not the same number of space bins and "
                       "eigenvectors[0m")
    # Fill the 3 matrices
    kijmat = np.full([nbins, nbins], np.nan)
    for irow, row in enumerate(res['keff_KIJ_matrix'][1:]):
        kijmat[irow] = np.array(tuple(row[1:]))
    stddevmat = np.full([nbins, nbins], np.nan)
    for irow, row in enumerate(res['keff_StdDev_matrix'][1:]):
        stddevmat[irow] = np.array(tuple(row[1:]))
    sensibmat = np.full([nbins, nbins], np.nan)
    for irow, row in enumerate(res['keff_sensibility_matrix'][1:]):
        sensibmat[irow] = np.array(tuple(row[1:]))
    return {'estimator': res['estimator'],
            'batchs_kept': res['batchs_kept'],
            'kij-keff': res['kij-keff'],
            'nbins': nbins,
            'spacebins': spacebins,
            'eigenvector': egvec,
            'keff_KIJ_matrix': np.array(kijmat),
            'keff_StdDev_matrix': np.array(stddevmat),
            'keff_sensibility_matrix': np.array(sensibmat)}


class SensitivityDictBuilder(DictBuilder):
    '''Class to build sensitivity results dictionary.'''

    def __init__(self, colnames, lnbins):
        super().__init__(colnames, lnbins)
        self.bins = OrderedDict([('einc', []), ('e', []), ('mu', [])])
        self.units = {'einc': 'MeV', 'e': 'MeV', 'mu': '',
                      'score': 'unknown', 'sigma': '%'}

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for sensitivities.

        Fill integrated result (written as energy integrated but integrated
        over all dimensions) in the ``'integrated_res'`` array, that will be in
        parallel of the default sensitivity result (a priori always here).
        '''
        ibin = [0, 0, 0]
        for ind, vals in enumerate(data['vals']):
            if 'direction_cosine' in vals:
                if ind != 0:
                    ibin[2] += 1
                    ibin[:2] = [0, 0]
                self.bins['mu'].append(vals['direction_cosine'][0])
            if 'energy_incident' in vals:
                if ibin[2] == 0:
                    self.bins['einc'].append(vals['energy_incident'][0])
                if ind % self.arrays['default'].shape[0] != 0:
                    ibin[0] += 1
            for ienergy, ivals in enumerate(vals['values']):
                if ibin[0] == ibin[2] == 0:
                    self.bins['e'].append(ivals[0])
                ibin[1] = ienergy
                self.arrays['default'][tuple(ibin)] = np.array(
                    tuple(ivals[2:]), dtype=self.arrays['default'].dtype)
        if 'energy_integrated' in data:
            self.arrays['integrated_res'][(0, 0, 0)] = np.array(
                (data['energy_integrated']['score'],
                 data['energy_integrated']['sigma']),
                dtype=self.arrays['default'].dtype)

    def add_last_bins(self, data):
        '''Add last bins in incident energy (E), energy (E') and direction
        cosine (µ). All orders are possible.

        :param list data: results as a list of dictionaries
        '''
        if len(self.bins['e']) > 1 and self.bins['e'][0] > self.bins['e'][1]:
            self.bins['e'].insert(0, data[-1]['values'][0][1])
        else:
            self.bins['e'].append(data[-1]['values'][-1][1])
        if self.bins['mu']:
            if ((len(self.bins['mu']) > 1
                 and self.bins['mu'][0] > self.bins['mu'][1])):
                self.bins['mu'].insert(0, data[0]['direction_cosine'][1])
            else:
                self.bins['mu'].append(data[-len(self.bins['einc'])]
                                       ['direction_cosine'][1])
        if self.bins['einc']:
            if ((len(self.bins['einc']) > 1
                 and self.bins['einc'][0] > self.bins['einc'][1])):
                self.bins['einc'].insert(0, data[0]['energy_incident'][1])
            else:
                self.bins['einc'].append(data[-1]['energy_incident'][1])


def _get_sensitivity_bins(data):
    nbcos = len([x for x in data if "direction_cosine" in x.keys()])
    if nbcos == 0:
        nbcos = 1
    nbeinc = int(len([x for x in data if "energy_incident" in x.keys()])/nbcos)
    if nbeinc == 0:
        nbeinc = 1
    nbebins = len(data[-1]['values'])
    return (nbeinc, nbebins, nbcos)


def convert_sensitivities(res):
    '''Convert sensitivities to dictionary containing :obj:`numpy.ndarray`.

    :param res: result
    :return: list(dict) containing the results and the associated metadata.

    The dictionary contains a structured array of 3 dimensions: incident
    energy ``'einc'``, exiting energy ``'e'`` and direction cosine ``'mu'``.
    The dtype is ``('score', 'sigma')``.

    Bins are filled in an :class:`collections.OrderedDict` always containing
    the 3 keys ``'einc', 'e', 'mu'`` in the order of the bins in the
    :obj:`numpy.ndarray`.
    '''
    lres = res['sensit_res']
    thelist = []
    for ires in lres:
        itype = ''.join(ires['sensitivity_type'])
        for iindex in ires['res']:
            sensidb = SensitivityDictBuilder(
                ['score', 'sigma'],
                _get_sensitivity_bins(iindex['vals']))
            if 'energy_integrated' in iindex:
                sensidb.add_array('integrated_res', ['score', 'sigma'],
                                  [1]*sensidb.arrays['default'].ndim)
            sensidb.fill_arrays_and_bins(iindex)
            sensidb.add_last_bins(iindex['vals'])
            sensidb.flip_bins()
            if 'units' in res:
                sensidb.units['score'] = res['units'][0]['uscore']
            datadict = {
                'array': sensidb.arrays['default'],
                'bins': sensidb.bins,
                'used_batch': res['used_batch'],
                'units': sensidb.units}
            resdict = iindex['charac'].asDict()
            resdict['sensitivity_type'] = itype
            resdict['sensitivity_spectrum_res'] = datadict
            resdict['integrated_res'] = sensidb.arrays['integrated_res']
            thelist.append(resdict)
    return thelist


def convert_list_to_tuple(liste):
    '''Convert nested list to nested tuple (to get imutable object).

    If list is not nested just convert it to tuple.

    :param liste: result as a liste
    :return: (nested) tuple
    '''
    assert not any(isinstance(n, dict) for n in liste), \
        "No dict expected in that list, please do something"
    if any(isinstance(n, list) for n in liste):
        return tuple(convert_list_to_tuple(n) if isinstance(n, list)
                     else n for n in liste)
    return tuple(liste)
