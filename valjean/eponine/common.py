'''This module provides generic functions to convert parsing outputs to `numpy`
objects.

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

Goal
----

Parsing results are normally stored as lists and dictionaries but it could be
easier to use other objects, as `numpy` arrays. In our context these objects
are used to represent

* spectrum results, i.e. tables splitted at least in energy, sometimes with
  additional splittings in time, µ and φ direction angles
* mesh results, i.e. tables splitted in space (cartesian, cylindrical,
  spherical depending on case), sometimes with additional splittings in energy
  and/or time
* keff results, especially the matrical ones
* Green bands results
* IFP results
* k\ :sub:`ij` results (matrices, eigenvectors and eigenvalues)

`Numpy` objects are useful for future calculations or plotting for example.


Spectrum and meshes
-------------------


.. _eponine-spectrummesh-intro:

Generalities
````````````

.. _doc: https://docs.scipy.org/doc/numpy/user/basics.rec.html

Spectrum and meshes results use a common representation build using
:class:`DictBuilder`. This common representation is a **7-dimension structured
array** from `numpy`, see `doc`_.

Dimensions are given in :py:data:`DictBuilder.VARS`:

* **s0**, **s1**, **s2**: space coordinates (typically (x, y, z), (r, θ, z) or
  (r, θ, ϕ), depending on frame reference)
* **e**: energy
* **t**: time
* **mu, phi**: direction angles µ and φ whose definitions can vary depending on
  the reference frame of direction [#dir_angles]_.

Order should always be that one.


The result for each bin ``(s0, s1, s2, e, t, mu, phi)`` is filled in a
**structured array** whose `numpy.dtype` can be:

* meshes: normally ``'tally'`` and ``'sigma'`` where *sigma* is in % and
  *tally* in its unit (not necessarly precised in the listing)
* default spectrum: ``'score'``, ``'sigma'``, ``'score/lethargy'`` where
  *sigma* is in %, *score* and *score/lethargy* in the unit of the score (not
  necessarly precised in the listing)
* spectrum with variance of variance (vov): as default spectrum case + a
  fourth element named ``'vov'`` (no unit)
* uncertainties spectrum: in case of *covariance perturbations*, elements are
  ``'sigma2(means)'``, ``'mean(sigma_n2)'``, ``'sigma(sigma_n2)'`` and
  ``'fisher test'`` [#uncertainties]_


Spectrum and mesh results don't only consist in arrays: binning (except in
space) and number of dicarded batchs are also available for example. Other
optional can also be added, like integrated result on one or more dimensions.
The final result of spectrum and mesh is returned as a dictionary detailed in
:ref:`result_spectrum <eponine-spectrum-res>` and
:ref:`result_mesh <eponine-mesh-res>`.


Initialization
``````````````

:class:`DictBuilder` cannot be instantiated as it has abstract methods (pure
virtual): :meth:`~DictBuilder.fill_arrays_and_bins` and
:meth:`~DictBuilder.add_last_energy_bins`. It is mother class of
:class:`MeshDictBuilder` for mesh and :class:`SpectrumDictBuilder` for
spectrum.

Initialization is done giving names of the columns (``'tally'`` and ``'sigma'``
for mesh for example) and the list of number of bins. The length of this list
should be 7 as we have 7 dimensison.

.. testsetup:: common

   import valjean.eponine.common as epcm

.. doctest:: common

   >>> db = epcm.DictBuilder(['tally', 'sigma'], [1,2,3,4,5,6,7])
   Traceback (most recent call last):
         ...
   TypeError: Can't instantiate abstract class DictBuilder with abstract \
methods _add_last_energy_bin, fill_arrays_and_bins
   >>> mdb = epcm.MeshDictBuilder(['tally', 'sigma'], [1,2,3,4,5,6,7])
   >>> sdb = epcm.SpectrumDictBuilder(['score', 'sigma', 'score/lethargy'],
   ...                                [1,2,3,4,5,6,7])

Errors are raised if the dimension is not correct.

.. doctest:: common

   >>> mdb = epcm.MeshDictBuilder(['tally', 'sigma'], [1,2,3,4,5,6])
   Traceback (most recent call last):
       ...
   AssertionError

Number of bins should be 7 (3 space dimensions, 1 energy, 1 time, 2 direction
angles).

These methods initializes both the 7-dimensions structured arrays and the
arrays of bins, first stored as list for simplicity. Arrays of bins are in
reality array of the edges of bins, starting by the lower one to the higher one
after flipping if needed.

.. _eponine-spectrummesh-fill:

Filling arrays and bins
```````````````````````

Mesh and spectrum are read from the output listing and first stored as list and
dictionary following listing structure. Building `numpy` arrays and bins
simplifies post-processing. It calls :meth:`~DictBuilder.fill_arrays_and_bins`.

To fill arrays and bins needed objects are outputs from the chosen parser. Some
dictionary keys may be needed:

* mesh: data is a list of all meshes available. Each mesh is a dictionary that
  can have the following keys:

  * ``'meshes'``: list of dictionary containing the mesh results (mandatory),
    dictionaries with keys:

    * ``{'mesh_energyrange': [], 'mesh_vals': [[], ]}`` to get mesh per energy
      range (mandatory)
    * ``{'mesh_energyintegrated':, 'mesh_vals': [[], ]}`` if result is also
      available on the full range of energy but still splitted in space
      (facultative)

    A mesh line in the list under ``'mesh_vals'`` key is constructed as a list
    of ``[[s0, s1, s2], tally, sigma]``. In ``'mesh_energyrange'``, energy
    range is given as ``['unit', e1, e2]``.

  * ``'time_step'``: if a time splitting is available
    Remark: for the moment, no splitting in µ or φ are available.
  * ``'integrated result'``: if ``'time_step'`` exists, integrated result can
    be available, meaning integrated over space and energy (not time)

* spectrum: data is a list of dictionaries containing spectrum results.
  Possible keys are:

  * ``'spectrum_vals'``: spectrum values, given in a list
    ``[e1, e2, score, sigma, score/lethargy]`` (mandatory)
  * ``'time_step'``: if result splitted in time
  * ``'mu_angle_zone'``: if result splitted in µ angle
  * ``'phi_angle_zone'``: if result splitted in φ angle
  * ``'integrated_res'``: if ``'time_step'`` exits, integrated result can also
    be given in time steps, so integrated over energy.

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



Result and use in global code
`````````````````````````````

In the framework, :class:`MeshDictBuilder` and :class:`SpectrumDictBuilder` are
called in :meth:`convert_mesh` and :meth:`convert_spectrum`, themselves from
transformation modules (transforming parsing result in `numpy`/`python`
containers. Theses methods then returns dictionaries containing the `numpy`
arrays and other results.

.. _eponine-mesh-res:

mesh
....

   Default keys are:

   * ``'mesh'``: `numpy` 7-dimension structured array with dtype
     ``('tally', 'sigma')``
   * ``'ebins'``: `numpy` array of edges of energy bins
   * ``'eunit'``: energy unit

   Other keys can be available:

   * ``'tbins'``: `numpy` array of edges of time bins (if ``'time_step'``
     available)
   * ``'mesh_energyintegrated'``: `numpy` 7-dimension structured array with
     dtype ``('tally', 'sigma')`` and list of number of bins (``lnbins``) is
     ``[n_s0, n_s1, n_s2, 1, n_t, 1, 1]``
   * ``'integrated_res'``: `numpy` 7-dimension structured array with
     dtype ``('tally', 'sigma')`` and list of number of bins (``lnbins``) is
     ``[1, 1, 1, 1, n_t, 1, 1]``
   * ``'used_batch'``: if ``'integrated_res'`` exists, number of used batch is
     also given

.. _eponine-spectrum-res:

spectrum
........

   Default keys are:

   * ``'spectrum'``: `numpy` 7-dimension structured array with dtype
     ``('score', 'sigma', 'score/lethargy')`` if this is a default spectrum,
     dtype will change in some cases (vov, uncertainties), see
     :ref:`eponine-spectrummesh-intro`
   * ``'ebins'``: `numpy` array of edges of energy bins
   * ``'disc_batch'``: number of discarded batchs

   Optional keys are:

   * ``'tbins'``: `numpy` array of edges of time bins (if ``'time_step'``
     available)
   * ``'mubins'``: `numpy` array of edges of µ angle bins (if
     ``'mu_angle_zone'`` available)
   * ``'phibins'``: `numpy` array of edges of φ angle bins (if
     ``'phi_angle_zone'`` available)
   * ``'integrated_res'``: `numpy` 7-dimension structured array with same dtype
     as ``'spectrum'`` and list of number of bins (``lnbins``) is
     ``[1, 1, 1, 1, n_t, 1, 1]`` (integrated over energy)
   * ``'used_batch'``: if ``'integrated_res'`` exists, number of used batch is
     also given


.. note::

   If time, µ or φ are not required, their binnings are not available in the
   final dictionary.


|keff| results
--------------

Only |keff| as generic response are converted in *numpy* objects; historical
|keff| block is stored in a dictionary (see
:mod:`eponine.pyparsing_t4.grammar`).

In the generic response case, results (value, σ) are available for 3
estimators: KSTEP, KCOLL and KTRACK. Their correlation coefficients, combined
values, combined σ (in %) and the full combination result are also given. This
means that results given are in reality a matrix. One choice in order to store
|keff| results is to use *numpy* arrays seen as matrix
(:meth:`convert_keff_with_matrix`), the other one uses more standard arrays
(:meth:`convert_keff`).

.. _eponine-keff-matrix:

Conversion to matrices
``````````````````````
The 3 estimators are always considered in the listing order KSTEP, KCOLL,
KTRACK, so KSTEP = 0, KCOLL = 1 and KTRACK = 2.

Three arrays are filled:

* ``'keff_matrix'``: symmetric matrix 3×3, with k\ :sub:`eff` result for each
  estimator on diagonal and combined values off-diagonal (for 2 estimators)
* ``'correlation_matrix'``: symmetric matrix 3×3, with 1 on diagonal and
  correlation cofficient off-diagonal (for 2 estimators)
* ``'sigma_matrix'``: symmetric matrix 3×3 with σ in % for each estimator on
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

Values are set to `numpy.NaN` if not converged (string ``"Not converged"``
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
`````````````````````````````
The conversion closer to the output listing is done in :meth:`convert_keff`. A
dictionary is built with the following elements:

* ``'used_batch'``: number of batchs used
* ``'full_comb_estimation'``: full combination result (|keff| and σ in %), like
  in :ref:`eponine-keff-matrix`
* ``'res_per_estimator'``: dictionary with estimator as keyand *numpy*
  structured array with ``dtype = ('keff', 'sigma')`` as value
* ``'correlation_matrix'``: dictionary with tuple as key and *numpy* structured
  array as value, ``('estimator1', 'estimator2'):
  numpy.array('correlations', 'combined values', 'combined sigma%')``

In correlation matrix diagoanl is set to 1 and not converged values (str) are
set to `numpy` NaN. If the full combination did not converged hte string is
kept.


Green bands
-----------

Green bands are stored in *numpy* arrays that look like the spectrum or mesh
ones but with different bins and dtypes, these are 6-dimensions arrays.

The 6 dimensions are given, in order, by:

* **step**: bin of the energy of source (source are treated in energy steps)
* **source**: number of the source
* **u**, **v**, **w**: coordinates of the source, ``(0, 0, 0)`` if not given

The result for each bin (step, source, u, v, w) is filled in a **structured
array** whose `numpy.dtype` is the default spectrum one,
``('score', 'sigma', 'score/lethargy')``.

Bins are also stored for the source and for the followed particles. Like in
spectrum, last bins of energy (source and followed particle) are added after
the main loop.

.. todo::

   No flip in (source) energy bins is performed for the moment, due to some
   uncertainty in order of the energy steps for source (so how they are
   defined).


The returned dictionary contains:

* ``'disc_batch'``: number of discarded batchs
* ``'vals'``: 6-dimension *numpy* structured array
* ``'ebins'``: edges of energy bins (particles)
* ``'sebins'``: edges of source energy bins


IFP statistics results
----------------------

When using Itereted Fission Probability (IFP) method, it is possible to get
results for each cycle. These results are converted in a *numpy* structured
array with ``dtype = ('length', 'score', 'sigma')``. Dimension of the array
corresponds to number of cycles used.


.. |kij| replace:: k\ :sub:`ij`


|kij| results
-------------

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
`````````````
In that case the input dictionary is returned with a conversion of the
``'kij_sources_vals'`` as a numpy array. Its length corresponds to the number
of volumes.


.. _eponine-kij-result:

|kij| matrix (result)
`````````````````````
The |kij| matrix results block contains various results including |kij|
eigenvalues, |kij| eigenvectors and |kij| matrix that will be converted in
numpy.array or numpy.matrix. The size of the arrays depends on the number of
volumes containing fissle material, N.

The returned object is a dictionary containing the following keys and objects:

* ``'used_batch'``: number of batchs used (`int`)
* ``'kijmkeff_res'``: result of |kij|-|keff| (`float`), where |kij| is the
  hightest eigenvalue of |kij|
* ``'kijdomratio'``: dominant ratio (`float`), ratio between the hightest |kij|
  eigenvalue and the next one
* ``'kij_eigenval'``: numpy.array of N **complex** numbers (real and imaginary
  parts given in the listings) corresponding to the eigenvalues.
* ``'kij_eigenvec'``: `numpy.array` of N vectors of N elements corresponding to
  eigenvectors.
* ``'kij_matrix'``: numpy.matrix of N×N being the |kij| matrix.


.. _eponine-kij-in-keff:

|kij| in |keff| block
`````````````````````
|kij| results are also present in the "historical" |keff| block, as an
additional estimator. Results are presented in a different way and are
different... Typical results are |kij| - |keff|, the eigenvector corresponding
to the best estimation, |kij| matrxix, standard deviation matrix and
sensibility matrix.

The returned object is a dictionary with the following keys (faculative can be
specified):

* ``'estimator'``: name of the estimator (`str`), ``'KIJ'`` here
* ``'batchs_kept'``: number of batchs used to calculate the |keff| from |kij|
  (`int`)
* ``'kij-keff'``: result of |kij|-|keff| (`float`), using the best estimation
  of |kij|
* ``'nbins'``: **facultative**, number of volumes/mesh elements considered, or
  N, (`int`)
* ``'spacebins'``: **facultative**, list of N volumes/mesh elements considered
  (`numpy.array` of

    * `int` for volumes,
    * `tuple` (s0, s1, s2) for mesh elements with (`int`, `int`, `int`)),

* ``'eigenvector'``: eigenvector corresponding ti best estimation
  (`numpy.array` of N elements)
* ``'keff_KIJ_matrix'``: |kij| matrix for best estimation of |keff|
  (N×N `numpy.matrix`)
* ``'keff_StdDev_matrix'``: standard deviation matrix for best estimation of
  |keff| (N×N `numpy.matrix`)
* ``'keff_sensibility_matrix'``: sensibility matrix for best estimation of
  |keff| (N×N `numpy.matrix`)

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
        - ``'sigma(sigma_n2)'``: σ(variances) = :math:`\\sqrt{v(v_n)}`
        - ``'fisher test'``: this is an estimator more than a test
        - Variance, or sigma_n2 is given by:
          :math:`v_n = \\frac{\\sum^n_i{(x_i -m)^2}}{n(n-1)}`



'''

import logging
from abc import ABC, abstractmethod
import numpy as np


# get profile from globals (cleaner)
if 'profile' not in globals()['__builtins__']:
    def profile(func):
        '''No memory profiling if "mem" not in arguments of the command line.
        '''
        return func


LOGGER = logging.getLogger('valjean')
ITYPE = np.int32
FTYPE = np.float32  # pylint: disable=E1101


class DictBuilder(ABC):
    '''Class to build the dictionary for spectrum and mesh results as
    7-dimensions structured arrays.
    7-dimensions are: space (3), energy, time, mu and phi (direction angles)

    This class has 2 abstract methods, :meth:`_add_last_energy_bin` and
    :meth:`fill_arrays_and_bins`, so it cannot be initialized directly.

    2 constant objects are available:

    * ``VAR_FLAG = {'t': 'time_step', 'mu': 'mu_angle_zone',
      'phi': 'phi_angle_zone'}`` : correspondance dictionary between internal
      name of dimensions and names in listings
    * ``VARS = ['s0', 's1', 's2', 'e', 't', 'mu', 'phi']``: names of the 7
      dimensions as used internally
    '''
    VAR_FLAG = {'t': 'time_step',
                'mu': 'mu_angle_zone',
                'phi': 'phi_angle_zone'}
    VARS = ['s0', 's1', 's2', 'e', 't', 'mu', 'phi']

    def __init__(self, colnames, lnbins):
        '''Initialization of DictBuilder.

        :param colnames: name of the columns/results (e.g. ``'tally'`` and
                         ``'sigma'`` for mesh, or ``'score'``, ``'sigma'``,
                         ``'score/lethargy'`` for spectrum)
        :type colnames: list of str
        :param lnbins: number of bins for each dimension
        :type lnbins: list of int
        '''
        try:
            assert len(lnbins) == 7
        except TypeError:
            LOGGER.error("lnbins should the list of number of bins")
            raise TypeError
        except AssertionError:
            LOGGER.error("Number of bins should be 7 (3 space dimensions, "
                         "1 energy, 1 time, 2 direction angles)")
            raise AssertionError
        self.bins = {'e': [], 't': [], 'mu': [], 'phi': []}
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays = {'default': np.empty((lnbins), dtype=dtype)}
        LOGGER.debug("bins: %s", str(self.bins))

    def add_array(self, name, colnames, lnbins):
        '''Add a new array to dictionary arrays with key name.

        :param name: name of the new array (integrated_res, etc.)
        :type name: str
        :param colnames: list of the columns names (score, sigma, tally, etc.)
        :type colnames: list/tuple of string
        :param lnbins: number of bins in each dimension
        :type lnbins: list of int
        '''
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays[name] = np.empty((lnbins), dtype=dtype)

    @abstractmethod
    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum or mesh.

        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        '''
        pass

    def _add_last_bin_for_dim(self, data, dim, lastbin):
        '''Add last bin for the dimension dim. Depending on order of the bins
        the last one will be inserted as first bin or added as last bin.

        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        :param dim: dimension where the bin will be added (t, mu, phi)
        :type dim: string
        :param lastbin: index of the bin in mesh or spectrum containing the
                         missing edge of the bins
        :type lastbin: int
        '''
        LOGGER.debug("Adding last bin for dim %s, flag = %s",
                     dim, DictBuilder.VAR_FLAG[dim])
        if len(self.bins[dim]) > 1 and self.bins[dim][0] > self.bins[dim][1]:
            self.bins[dim].insert(0, data[0][DictBuilder.VAR_FLAG[dim]][2])
        else:
            self.bins[dim].append(data[lastbin][DictBuilder.VAR_FLAG[dim]][2])

    def add_last_bins(self, data):
        '''Add last bins in energy, time, mu and phi direction angles.
        Based on keywords presence in data.

        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
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

    def _flip_bins_for_dim(self, dim, axis):
        '''Flip bins for dimension dim.

        :param dim: dimension ('e', 't', 'mu', 'phi')
        :type dim: string
        :param axis: axis of the dimension
                     ('e' -> 3, 't' -> 4, 'mu' -> 5, 'phi' -> 6)
        :type axis: int
        '''
        LOGGER.debug("Bins %s avant flip: %s", dim, str(self.bins[dim]))
        self.bins[dim] = self.bins[dim][::-1]
        for key, array in self.arrays.items():
            self.arrays[key] = np.flip(array, axis=axis)
        LOGGER.debug("et apres: %s", str(self.bins[dim]))

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
        if self.bins['e'] and self.bins['e'][0] > self.bins['e'][1]:
            self._flip_bins_for_dim('e', 3)
        if self.bins['t'] and self.bins['t'][0] > self.bins['t'][1]:
            self._flip_bins_for_dim('t', 4)
        if self.bins['mu'] and self.bins['mu'][0] > self.bins['mu'][1]:
            self._flip_bins_for_dim('mu', 5)
        if self.bins['phi'] and self.bins['phi'][0] > self.bins['phi'][1]:
            self._flip_bins_for_dim('phi', 6)

    @abstractmethod
    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum or mesh data.
        :param data: mesh or spectrum

        :type data: list of meshes or spectrum results
        '''
        pass


class MeshDictBuilder(DictBuilder):
    '''Class specific to mesh dictionary -> mainly filling of bins and arrays.

    This class inherites from DictBuilder, see :class:`DictBuilder` for
    initialization and common methods.
    '''
    itime, imu, iphi = 0, 0, 0

    def _fill_mesh_array(self, meshvals, name, ebin):
        '''Fill mesh array.

        :param meshvals: mesh data for a given energy bin
        :type meshvals: list of mesh results [[[s0, s1, s2], tally, sigma],...]
        :param name: name of the array to be filled ('default',
                     'eintegrated_mesh') for the moment
        :type name: string
        :param ebin: energy bin to fill in the array
        :type ebin: int
        '''
        for smesh in meshvals:
            index = (smesh[0][0], smesh[0][1], smesh[0][2],
                     ebin, self.itime, self.imu, self.iphi)
            self.arrays[name][index] = np.array(tuple(smesh[1:]),
                                                dtype=self.arrays[name].dtype)

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for mesh data.

        :param data: mesh
        :type data: list of meshes results

        Different arrays can be filled. Current possibilities are:

        * ``'default'`` (mandatory)
        * ``'eintegrated_mesh'``
          (facultative, integrated over energy, still splitted in space)
        * ``'integrated_res'`` (over energy and space, splitted in time)
        '''
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

        :param data: mesh data
        :type data: list of meshes results
        '''
        lastmesh = data[-1]['meshes']
        lastebin = self.arrays['default'].shape[3]-1
        self.bins['e'].append(lastmesh[lastebin]['mesh_energyrange'][2])


class SpectrumDictBuilder(DictBuilder):
    '''Class specific to spectrum dictionary
    -> mainly filling of bins and arrays.

    This class inherites from DictBuilder, see :class:`DictBuilder` for
    initialization and common methods.
    '''
    itime, imu, iphi = 0, 0, 0

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum data.

        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results

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
                    self.bins['e'].append(ivals[0])
                index = (0, 0, 0, ienergy, self.itime, self.imu, self.iphi)
                self.arrays['default'][index] = np.array(
                    tuple(ivals[2:]),
                    dtype=self.arrays['default'].dtype)

            # Fill integrated result if exist
            if 'integrated_res' in ispec:
                iintres = ispec['integrated_res']
                index = (0, 0, 0, 0, self.itime, self.imu, self.iphi)
                self.arrays['integrated_res'][index] = (np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype))

    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum.

        :param data: spectrum data
        :type data: list of spectrum results
        '''
        self.bins['e'].append(data[-1]['spectrum_vals'][-1][1])


def _get_number_of_bins(spectrum):
    '''Get number of bins (time, mu and phi angles and energy).

    :param spectrum: input spectrum (full as various levels of list or
      dictionary may be needed.
    :returns: 4 integers in following order

          - *nphibins* = number of bins in phi angle, default = 1
          - *nmubins* = number of bins in mu angle, default = 1
          - *ntbins* = number of bins in time, default = 1
          - *nebins* = number of bins in energy, no default

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
    '''Convert spectrum results in 7D numpy structured array.

    :param spectrum: list of spectra.
     Accepts time and (direction) angular grids.
    :type spectrum: list
    :param colnames: list of the names of the columns.
      Default = ``['score', 'sigma', 'score/lethargy']``
    :type colnames: list of strings
    :returns: dictionary with keys and elements

      * ``'spectrum'``: 7 dimensions numpy structured array with related
        binnings as numpy arrays
        ``v[s0, s1, s2, E, t, mu, phi] = ('score', 'sigma', 'score/lethargy')``
      * ``'disc_batchs'``: number of discarded batchs for the score
      * ``'ebins'``: energy binning
      * ``'tbins'``: time binning if time grid required
      * ``'mubins'``: mu binning if mu grid required
      * ``'phibins'``: phi binning if phi grid required
      * ``'integrated_res'``: 7 dimensions numpy structured array
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
                'ebins': np.array(vals.bins['e']),
                'spectrum': vals.arrays['default']}
    if 'time_step' in spectrum[0]:
        convspec['tbins'] = np.array(vals.bins['t'])
    if 'mu_angle_zone' in spectrum[0]:
        convspec['mubins'] = np.array(vals.bins['mu'])
    if 'phi_angle_zone' in spectrum[0]:
        convspec['phibins'] = np.array(vals.bins['phi'])
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = vals.arrays['integrated_res']
        convspec['used_batch'] = spectrum[0]['integrated_res']['used_batch']
    return convspec


def _get_number_of_space_bins(meshvals):
    '''Get number of space bins used in meshes.

    This function is mainly used when meshes are not entirely saved (tests, or
    useless in the considered case). The limit on the number of lines of mesh
    in the listing does not necessarly match a completed mesh dimension.

    :param meshvals: list of meshes, with mesh [[s0, s1, s2] tally sigma]
      s0, s1 and s2 being the space coordinates
    :returns: 3 integers in following order

        - *ns0bins*: number of bins in the s0 dimension
        - *ns1bins*: number of bins in the s1 dimension
        - *ns2bins*: number of bins in the s2 dimension
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
                             str(meshvals[-int(maxbins1)]), str(lastspacebin))
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

    :param meshes: mesh, list of dictionaries, at least one should have the key
       ``'mesh_energyrange'``
    :type meshes: list of dictionaries
    '''
    nbebins = 0
    for mesh in meshes:
        if 'mesh_energyrange' in mesh:
            nbebins += 1
    return nbebins


@profile
def convert_mesh(meshres):
    '''Convert mesh in 7-dimensions numpy array.

    :param meshres: Mesh result constructed as:
      ``[{'time_step': [], 'meshes': [], 'integrated_res': {}}, {}]``, see
      :ref:`eponine-spectrummesh-fill` for more details.
    :type meshres: list of dictionaries

    :returns: python dictonary with keys

        * ``'mesh'``: numpy structured array of dimension 7
          ``v[s0, s1 ,s2, E, t, mu, phi] = ('tally', 'sigma')``
        * ``'eunit'``: energy unit
        * ``'ebins'``: energy bin edges (size = number of bins + 1)
        * ``'tbins'``: time binning if time grid required
        * ``'eintegrated_mesh'``: 7-dimensions numpy structured array
          ``v[s0,s1,s2,E,t,mu,phi] = ('tally', 'sigma')``
          corresponding to mesh integreted on energy (facultative)
        * ``'integrated_res'``: 7 dimensions numpy structured array
          ``v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)``
          corresponding to mesh integrated over energy and space;
          *facultative*, available when time grid is required (so
          corresponds to integreated results splitted in time)
        * ``'used_batch'``: number of used batchs (only if integrated result)
    '''
    LOGGER.debug("In convert_mesh_class")
    LOGGER.debug("Number of mesh results: %d", len(meshres))
    LOGGER.debug("keys of meshes: %s", str(list(meshres[0]['meshes'].keys())))
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
    vals = MeshDictBuilder(['tally', 'sigma'],
                           [ns0bins, ns1bins, ns2bins, nebins, ntbins, 1, 1])
    # mesh integrated on energy (normally the last mesh)
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        vals.add_array('eintegrated_mesh', ['tally', 'sigma'],
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
    convmesh = {'eunit': meshres[0]['meshes'][0]['mesh_energyrange'][0],
                'ebins': np.array(vals.bins['e']),
                'mesh': vals.arrays['default']}
    if 'time_step' in meshres[0]:
        convmesh['tbins'] = np.array(vals.bins['t'])
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        convmesh['eintegrated_mesh'] = vals.arrays['eintegrated_mesh']
    if 'integrated_res' in meshres[0]:
        convmesh['integrated_res'] = vals.arrays['integrated_res']
        convmesh['used_batch'] = meshres[0]['integrated_res']['used_batch']
    return convmesh


def convert_integrated_result(result):
    '''Convert the energy integrated result in numpy structured array

    :param result: resultat
    :type result: list
    :returns: numpy structured array with (score, sigma)
    '''
    LOGGER.debug("[38;5;37m%s[0m", str(result))
    dtir = np.dtype([('score', FTYPE), ('sigma', FTYPE)])
    return np.array(tuple(result), dtype=dtir)


@profile
def convert_keff_with_matrix(res):
    '''Convert |keff| results in numpy matrices.

    :param res: |keff| results
    :type res: dict
    :returns: dict filled as:

    ::

        {'used_batch': int, 'estimators': [str],
         'full_comb_estimation': numpy.array, 'keff_matrix': numpy.array,
         'correlation_matrix': numpy.array, 'sigma_matrix': numpy.array}

    '''
    # not converged cases a tester...
    LOGGER.debug("In common.convert_keff_with_matrix")
    if 'not_converged' in res:
        return {'used_batch': res['used_batch'],
                'not_converged': res['not_converged']}

    dtkeff = np.dtype([('keff', FTYPE), ('sigma', FTYPE)])
    fullcombres = (np.array(tuple(res['full_comb_estimation']), dtype=dtkeff)
                   if len(res['full_comb_estimation']) > 1
                   else res['full_comb_estimation'][0])
    keffnames = list(zip(*res['res_per_estimator']))[0]
    nbkeff = len(res['res_per_estimator'])
    keffmat = np.empty([nbkeff, nbkeff])
    corrmat = np.identity(nbkeff)
    sigmat = np.empty([nbkeff, nbkeff])
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
            'estimators': keffnames,
            'full_comb_estimation': fullcombres,
            'keff_matrix': keffmat,
            'correlation_matrix': corrmat,
            'sigma_matrix': sigmat}


def convert_keff(res):
    '''Convert |keff| results in dictionary containing numpy objects.

    :param res: keff results
    :type res: dict
    :returns: dict containing

    ::

     {'used_batch': int, 'estimators': [str, ],
      'full_comb_estimation': numpy.array,
      'res_per_estimator': {'estimator': numpy.array, },
      'correlation_matrix': {('estimator1', 'estimator2'): numpy.array, }}

    See :ref:`eponine-keff-stdarrays` for more details.
    '''
    LOGGER.debug("[38;5;56mClefs:%s[0m", str(list(res.keys())))
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


# 17 locals in convert_green_bands instead 15, but helps reading of the method
def convert_green_bands(gbs):  # pylint: disable=R0914
    '''Convert Green bands results in numpy structured array.

    :param gbs: Green bands
    :type gbs: list of dict
    :returns: dict similar to spectum one
      :code:`{'used_batch': int, 'vals': numpy.array, 'ebins': numpy.array,
      'sebins': numpy.array}`
    '''
    lastsource = gbs[-1]['gb_step_res'][-1]['gb_source']
    hassourcetab = True if len(lastsource) > 1 else False
    spectrum = gbs[0]['gb_step_res'][0]['spectrum_res'][0]
    bins = {'e': [], 'se': []}
    index = (len(gbs),  # number of steps (= number of bins of source energy)
             lastsource[0]+1,  # number of sources
             lastsource[1][0]+1 if hassourcetab else 1,  # number of u bins
             lastsource[1][1]+1 if hassourcetab else 1,  # number of v bins
             lastsource[1][2]+1 if hassourcetab else 1,  # number of w bins
             len(spectrum['spectrum_vals']))  # number of energy bins
    vals = np.empty(index,
                    dtype=np.dtype([('score', FTYPE),
                                    ('sigma', FTYPE),
                                    ('score/lethargy', FTYPE)]))
    # Loop over results to fill them in numpy array
    for ist, gbstep in enumerate(gbs):
        istep = gbstep['gb_step_desc'][0]
        bins['se'].append(gbstep['gb_step_desc'][2])
        for ires, gbres in enumerate(gbstep['gb_step_res']):
            isource = gbres['gb_source']
            if len(gbres['spectrum_res']) > 1:
                LOGGER.warning("[31mMore than one spectrum_res "
                               "while only one foreseen for the moment[0m")
            ispectrum = gbres['spectrum_res'][0]['spectrum_vals']
            for iebin, ivals in enumerate(ispectrum):
                if ist == 0 and ires == 0:
                    bins['e'].append(ivals[0])
                locind = ((istep, isource[0],
                           isource[1][0], isource[1][1], isource[1][2],
                           iebin) if hassourcetab
                          else (istep, isource[0], 0, 0, 0, iebin))
                vals[locind] = np.array(tuple(ivals[2:]), dtype=vals.dtype)
    # Add last bins
    bins['se'].append(gbs[-1]['gb_step_desc'][1])
    bins['e'].append(spectrum['spectrum_vals'][-1][1])
    # No flip bins for the moment, question about order of steps (so energy
    # bins of sources)
    return {'ebins': np.array(bins['e']),
            'vals': vals,
            'sebins': np.array(bins['se']),
            'disc_batch': spectrum['disc_batch']}


def convert_ifp(ifp):
    '''Convert IFP (statistics) result in numpy array.

    :param ifp: cycle and associated results
    :type ifp: list
    :returns: numpy structured array of dimension 1
    '''
    dtifp = np.dtype([('length', ITYPE), ('score', FTYPE), ('sigma', FTYPE)])
    vals = np.empty((len(ifp)), dtype=dtifp)
    for ind, ifpcycle in enumerate(ifp):
        vals[ind] = np.array(tuple(ifpcycle), dtype=dtifp)
    return vals


def convert_kij_sources(res):
    '''Convert |kij| sources result in python dictionary in which |kij| sources
    values are converted in a numpy array.

    :param res: |kij| sources
    :type res: dict
    :returns: same dictionary with numpy.array for |kij| sources values
    '''
    kijs = {}
    for key in res:
        if key == 'kij_sources_vals':
            kijs[key] = np.array(res[key])
        else:
            kijs[key] = res[key]
    return kijs


def convert_kij_result(res):
    '''Convert |kij| result in numpy objects and return a dictionary.

    :param dict res: |kij| result with keys ``'used_batch'``,
      ``'kij_eigenval'``, ``'kij_eigenvec'``, ``'kij_matrix'``
    :returns: dictionary containing the same keys but with different types:

    ::

      {'used_batch': int, 'kijmkeff_res': float, 'kijdomratio': float,
      'kij_eigenval': numpy.array, 'kij_eigenvec': numpy.array,
      'kij_matrix': numpy.matrix}

    For more details see :ref:`eponine-kij-result`.
    '''
    # eigen values (re, im) -> store as array of complex
    reegval = np.array(list(zip(*res['kij_eigenval']))[0])
    imegval = np.array(list(zip(*res['kij_eigenval']))[1])
    egvals = reegval + 1j*imegval
    # eigen vectors
    egvecs = np.array(res['kij_eigenvec'])
    # kij matrix
    kijmat = np.matrix(res['kij_matrix'])
    return {'used_batch': res['used_batch'],
            'kijmkeff_res': res['kijmkeff_res'][0],
            'kijdomratio': res['kijmkeff_res'][1],
            'kij_eigenval': egvals,
            'kij_eigenvec': egvecs,
            'kij_matrix': kijmat}


def convert_kij_keff(res):
    '''Convert matrices in numpy array or matrix when estimating |keff| from
    |kij|

    :param dict res: |kij| result from |keff| result block
    :returns: dictionary containing `numpy` arrays:

    ::

       {'estimator': str, 'batchs_kept': int, 'kij-keff': float,
        'nbins': int, 'spacebins': numpy.array of int or tuple(s0, s1, s2),
        'eigenvector': numpy.array,
        'keff_KIJ_matrix': numpy.matrix,
        'keff_StdDev_matrix': numpy matrix,
        'keff_sensibility_matrix': numpy.matrix}

    Keys ``'nbins'`` and ``'spacebins'`` are facultative.

    For more details see :ref:`eponine-kij-in-keff`.
    '''
    LOGGER.debug("Clefs: %s", str(list(res.keys())))
    egvec = np.array(list(zip(*res['eigenvector']))[1])
    nbins = res['nb_fissile_vols'] if 'nb_fissile_vols' in res else len(egvec)
    if nbins != len(egvec):
        LOGGER.warning("[31mIssue in number of fissile volumes "
                       "and size of eigenvector[0m")
    # For the moment 2 possibilities seen for space splitting: mesh or volumes
    # in mesh case: meshes are listed in 1st row of matrix (3 elements)
    # in volume case: list of fissile volumes given, equivalent to 1st row of
    # matrix -> only way kept as closer to mesh case
    if isinstance(res['keff_KIJ_matrix'][0][0], list):
        dtspace = np.dtype([('s0', ITYPE), ('s1', ITYPE), ('s2', ITYPE)])
        spacebins = np.empty(len(res['keff_KIJ_matrix'][0]), dtype=dtspace)
        for ielt, spelt in enumerate(res['keff_KIJ_matrix'][0]):
            spacebins[ielt] = np.array(spelt)
    else:
        spacebins = np.array(res['keff_KIJ_matrix'][0])
    if spacebins.size != len(res['keff_KIJ_matrix'][1:]):
        LOGGER.warning("[31mStrange: not the dimension in space mesh and "
                       "matrix, matrix expected to be squared[0m")
    # Fill the 3 matrices
    kijmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_KIJ_matrix'][1:]):
        kijmat[irow] = np.array(tuple(row[1:]))
    stddevmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_StdDev_matrix'][1:]):
        stddevmat[irow] = np.array(tuple(row[1:]))
    sensibmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_sensibility_matrix'][1:]):
        sensibmat[irow] = np.array(tuple(row[1:]))
    return {'estimator': res['estimator'],
            'batchs_kept': res['batchs_kept'],
            'kij-keff': res['kij-keff'],
            'nbins': nbins,
            'spacebins': spacebins,
            'eigenvector': egvec,
            'keff_KIJ_matrix': np.matrix(kijmat),
            'keff_StdDev_matrix': np.matrix(stddevmat),
            'keff_sensibility_matrix': np.matrix(sensibmat)}
