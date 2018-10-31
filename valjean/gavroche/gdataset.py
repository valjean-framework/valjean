# pylint: disable=trailing-whitespace
'''Extension of class :class:`Dataset <valjean.eponine.dataset.Dataset>` in
other to perform simple calculations and usual operations on datasets
``(+, -, *, /, [])``.

All operations conserve the name of the initial dataset.

.. todo::

    Adding comparisons to gdataset.

.. _numpy indexing:
   https://docs.scipy.org/doc/numpy/user/basics.indexing.html


Creation of a :class:`GDataset`
-------------------------------

.. doctest:: gdataset
    :hide:

    >>> # noqa: W291


GDatasets can be created from :class:`Dataset
<valjean.eponine.dataset.Dataset>` or directly from their arguments.

    >>> from collections import OrderedDict
    >>> from valjean.gavroche.gdataset import GDataset

From the default arguments:

    >>> bins = OrderedDict([('e', np.array([1, 2, 3])), ('t', np.arange(5))])
    >>> gd1 = GDataset(np.arange(10).reshape(2, 5),
    ...                np.array([0.3]*10).reshape(2, 5), bins=bins, name='gd1')
    >>> gd1.name
    'gd1'
    >>> gd1.value.shape == (2, 5)
    True
    >>> np.array_equal(gd1.value, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
    True
    >>> np.array_equal(gd1.error,
    ...                [[0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3]])
    True
    >>> list(bins.keys())
    ['e', 't']
    >>> np.array_equal(bins['e'], [1, 2, 3])
    True
    >>> np.array_equal(bins['t'], [0, 1, 2, 3, 4])
    True

From a :class:`Dataset <valjean.eponine.dataset.Dataset>` (usually obtained
from parsing):

    >>> from valjean.eponine.dataset import Dataset
    >>> ds = Dataset(np.arange(3), np.array([1]*3), name='ds')
    >>> gds = GDataset.from_dataset(ds)
    >>> ds.__class__
    <class 'valjean.eponine.dataset.Dataset'>
    >>> gds.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> ds.name == gds.name
    True
    >>> np.array_equal(ds.value, gds.value)
    True
    >>> np.array_equal(ds.error, gds.error)
    True
    >>> ds.bins == gds.bins
    True


Operations available on GDatasets
---------------------------------

Standard operations are available for :class:`GDataset`, inherited from
:class:`Dataset <valjean.eponine.dataset.Dataset>`. Examples of their use are
given, including failing cases. Some are used in various methods but shown only
once.

Addition and subtraction
^^^^^^^^^^^^^^^^^^^^^^^^
Addition and subtraction are possible between a :class:`GDataset` and a scalar
(:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another :class:`GDataset`.
The operator to use for addition is ``+`` and for subtraction ``-``.

Restrictions in addition or subtraction with a :obj:`numpy.ndarray` are handled
by `NumPy`.

The addition or subtraction f 2 :class:`GDataset` can be done if

* both values have the same shape (:func:`consistent_datasets`)
* bins conditions (:func:`same_coords`):

    * EITHER the second :class:`GDataset` does not have any bins
    * OR bins are approximately the same, i.e. have the same keys and bins
      values are within 1e-5 tolerance (default from :func:`numpy.allclose`)


Example addition of a scalar value (only on value)
``````````````````````````````````````````````````

    >>> gd1p10 = gd1 + 10
    >>> np.array_equal(gd1p10.value,
    ...                [[10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
    True
    >>> np.array_equal(gd1p10.error, gd1.error)
    True
    >>> gd1p10.bins == gd1.bins
    True

As expected it 'only' acts on the value, error and bins are unchanged.


Example of subtraction of a :obj:`numpy.ndarray`
````````````````````````````````````````````````

    >>> a = np.array([100]*10).reshape(2, 5)
    >>> gd1.value.shape == a.shape
    True
    >>> gd1ma = gd1 - a
    >>> gd1ma.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> np.array_equal(gd1ma.value, [[-100, -99, -98, -97, -96],
    ...                              [-95, -94, -93, -92, -91]])
    True
    >>> np.array_equal(gd1ma.error, gd1.error)
    True
    >>> gd1ma.bins == gd1.bins
    True

``a`` and ``gd1`` have the same shape to everything is fine.

    >>> b = np.array([100]*10)
    >>> gd1.value.shape == b.shape
    False
    >>> gd1pb = gd1 + b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `NumPy` raises an exception (and gd1pb is not
defined).


.. _addition_gdataset:

Example of addition or subtraction of another :class:`GDataset`
```````````````````````````````````````````````````````````````

    >>> gd2 = GDataset(value=np.arange(20, 30).reshape(2, 5),
    ...                error=np.array([0.4]*10).reshape(2, 5),
    ...                bins=bins, name='gd2')
    >>> gd1.bins == gd2.bins
    True
    >>> gd1p2 = gd1 + gd2
    >>> gd1p2.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> gd1p2.name == gd1.name
    True
    >>> np.array_equal(gd1p2.value, [[20, 22, 24, 26, 28],
    ...                              [30, 32, 34, 36, 38]])
    True
    >>> np.array_equal(gd1p2.error, np.array([0.5]*10).reshape(2, 5))
    True

The error is calulated considering both datasets are independent, so
quadratically (:math:`e = \\sqrt{gd1.e^2 + gd2.e^2}`).

Datasets without binning can also be added:

    >>> gd3 = GDataset(value=np.arange(200, 300, 10).reshape(2, 5),
    ...                error=np.array([0.4]*10).reshape(2, 5), name='gd3')
    >>> gd3.bins
    OrderedDict()
    >>> gd1p3 = gd1 + gd3
    >>> gd1p3.name == gd1.name
    True
    >>> np.array_equal(gd1p3.value, [[200, 211, 222, 233, 244],
    ...                              [255, 266, 277, 288, 299]])
    True
    >>> np.array_equal(gd1p3.error, np.array([0.5]*10).reshape(2, 5))
    True
    >>> same_coords(gd1p3, gd1)
    True

Bins of the dataset on the left are kept.

Like in `NumPy` array addition, values need to have the same shape:

    >>> gd4 = GDataset(np.arange(5), np.array([0.01]*5), name='gd4')
    >>> "shape gd1 {0}, gd4 {1} -> comp = {2}".format(
    ...   gd1.value.shape, gd4.value.shape, gd1.value.shape == gd4.value.shape)
    'shape gd1 (2, 5), gd4 (5,) -> comp = False'
    >>> gd1 + gd4
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to add do not have same shape

If bins are given, they need to have the same keys and the same values
(approximately if float values).

    >>> bins5 = OrderedDict([('E', np.array([1, 2, 3])), ('t', np.arange(5))])
    >>> gd5 = GDataset(np.arange(0, -10, -1).reshape(2, 5),
    ...                np.array([0.01]*10).reshape(2, 5),
    ...                bins=bins5, name='gd5')
    >>> gd1 + gd5
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to add do not have same bins names
    >>> "bins gd1: {0}, bins gd5: {1}".format(list(gd1.bins.keys()),
    ...                                     list(gd5.bins.keys()))
    "bins gd1: ['e', 't'], bins gd5: ['E', 't']"

    >>> bins6 = OrderedDict([('e', np.array([1, 2, 30])), ('t', np.arange(5))])
    >>> gd6 = GDataset(np.arange(0, -10, -1).reshape(2, 5),
    ...                np.array([0.01]*10).reshape(2, 5),
    ...                bins=bins6, name='gd5')
    >>> gd1 - gd6
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to subtract do not seem to have the same bins
    >>> same_coords(gd1, gd6)
    False
    >>> list(gd1.bins.keys()) == list(gd6.bins.keys())
    True
    >>> np.array_equal(gd1.bins['e'], gd6.bins['e'])
    False
    >>> np.array_equal(gd1.bins['t'], gd6.bins['t'])
    True


Multiplication and division
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Multiplication and division are possible between a :class:`GDataset` and a
scalar (:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another
:class:`GDataset`.
The operator to use for multiplication is ``*`` and for division ``/``.

Restrictions in multiplication and division with a :obj:`numpy.ndarray` are
handled by `NumPy`.

The multiplication or division of 2 :class:`GDataset` can be done if

* both values have the same shape (:func:`consistent_datasets`)
* bins conditions (:func:`same_coords`):

    * EITHER the second :class:`GDataset` does not have any bins
    * OR bins are approximately the same, i.e. have the same keys and bins
      values are within 1e-5 tolerance (default from :func:`numpy.allclose`)

Division by zero, nan or inf are handled by `NumPy` and return a
RuntimeWarning from `NumPy` (only in the zero case).


Example multiplication of a scalar value
````````````````````````````````````````

    >>> gd1m10 = gd1 * 10
    >>> gd1m10.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> np.array_equal(gd1m10.value, [[0, 10, 20, 30, 40],
    ...                               [50, 60, 70, 80, 90]])
    True
    >>> np.array_equal(gd1m10.error, np.array([3.]*10).reshape(2, 5))
    True
    >>> same_coords(gd1m10, gd1)
    True

As expected it acts on the value and on the error. Bins are unchanged.


.. _division_by_nparray:

Example of division of a :obj:`numpy.ndarray`
`````````````````````````````````````````````

    >>> gd1da = gd1 / a
    >>> gd1da.name == gd1.name
    True
    >>> np.array_equal(gd1da.value, [[0., 0.01, 0.02, 0.03, 0.04],
    ...                              [0.05, 0.06, 0.07, 0.08, 0.09]])
    True
    >>> np.array_equal(gd1da.error, np.array([0.003]*10).reshape(2, 5))
    True
    >>> same_coords(gd1da, gd1)
    True

``a`` and ``gd1`` have the same shape to everything is fine.

    >>> gd1 / b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `NumPy` raises an exception.

If the :obj:`numpy.ndarray`: contains ``0``, ``nan`` or ``inf``, `NumPy` deals
with them. It sends a RunningWarning about the division by zero.

    >>> c = np.array([[2., 3., np.nan, 4., 0.], [1., np.inf, 5., 10., 0.]])
    >>> gd1 / c  # doctest: +SKIP
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[0.         0.33333333        nan 0.75              inf]
     [5.         0.         1.4        0.8               inf]],
            error: [[0.05       0.03333333        nan 0.025             inf]
     [0.1        0.         0.02       0.01              inf]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> # prints *** RuntimeWarning: divide by zero encountered in true_divide


Example of multiplication or division of another :class:`GDataset`
``````````````````````````````````````````````````````````````````

    >>> gd1 * gd2  # doctest: +SKIP
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[  0  21  44  69  96]
     [125 156 189 224 261]],
            error: [[        nan  3.26496554  6.39061812 10.74895344 \
16.17899873]
     [22.63846285 30.11245589 38.5945592  48.08159731 58.57183624]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> # prints *** RuntimeWarning: divide by zero encountered in true_divide
    >>> # prints *** invalid value encountered in multiply

    >>> gd1 / gd2  # doctest: +SKIP
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[0.         0.04761905 0.09090909 0.13043478 0.16666667]
     [0.2        0.23076923 0.25925926 0.28571429 0.31034483]],
            error: [[       nan 0.00740355 0.01320376 0.02031938 0.02808854]
     [0.03622154 0.04454505 0.05294178 0.06132857 0.06964547]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> # prints *** RuntimeWarning: divide by zero encountered in true_divide
    >>> # prints *** RuntimeWarning: invalid value encountered in multiply

In both cases the error is calulated considering both datasets are independent,
so quadratically :math:`e = v*\\sqrt{{(\\frac{gd_1.e}{gd_1.v})}^2 +
{(\\frac{gd_2.e}{gd_2.v})}^2}`.

The same restictions on bins as for addition and subtraction are set for
multiplication and division, same ``AssertError`` are raised, see
:ref:`addition_gdataset`.

About the division by ``0``, ``nan`` or ``inf``, it acts like in the
multiplication or division by a :obj:`numpy.ndarray`, see
:ref:`division_by_nparray`.


Indexing and slicing
--------------------

It is only possible to get a **slice** of a dataset, getting an GDataset at a
given index is not possible (for dimensions consistency reasons). Requiring a
given index can then be done using a slice.


Getting a subset of the :class:`GDataset`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Time is the second dimension, to remove first and last bins the usual slice is
``[1:-1]``, the first dimension, energy, is conserved, so its slice is ``[:]``.
The slice to apply is then ``[:, 1:-1]``.

    >>> gd1sltfl = gd1[:, 1:-1]
    >>> gd1sltfl.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> np.array_equal(gd1sltfl.value, [[1, 2, 3], [6, 7, 8]])
    True
    >>> np.array_equal(gd1sltfl.error, np.array([0.3]*6).reshape(2, 3))
    True
    >>> list(gd1sltfl.bins.keys()) == list(gd1.bins.keys())
    True
    >>> np.array_equal(gd1sltfl.bins['e'], gd1.bins['e'])
    True
    >>> np.array_equal(gd1sltfl.bins['t'], gd1.bins['t'])
    False
    >>> np.array_equal(gd1sltfl.bins['t'], [1, 2, 3])
    True
    >>> gd1sltfl.name == gd1.name
    True

Slicing is also applied on bins.


.. warning::
    Requiring a slice when there are not enough elements on the dimension give
    empty arrays.

    For example: removing first and last bin in energy on ``gd1``. The slice is
    ``[1:-1, :]`` in that case, but ``gd1`` has only 2 bins in energy.

    >>> gd1slefl = gd1[1:-1, :]
    >>> gd1slefl.value.shape == (0, 5)
    True
    >>> np.array_equal(gd1slefl.value, np.array([]).reshape(0, 5))
    True
    >>> np.array_equal(gd1slefl.error, np.array([]).reshape(0, 5))
    True
    >>> np.array_equal(gd1slefl.bins['t'], gd1.bins['t'])
    True
    >>> np.array_equal(gd1slefl.bins['e'], gd1.bins['e'])
    False
    >>> np.array_equal(gd1slefl.bins['e'], [2])
    True

    Note that in this case, as bins are in reality the edges of the bins, so we
    have N+1 values in the bins compared to the value/error where we have N
    values. Slicing then give one value in energy bins, so unusable here (it
    would be empty if we have values and centers of bins instead of edges of
    bins).


All dimensions have to be present in the slice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``:`` for the untouched dimensions. Number of ``,`` has to be dimension -1.

Let's consider a new GDataset, with 4 dimensions:

    >>> bins2 = OrderedDict([('e', np.arange(4)), ('t', np.arange(3)),
    ...                      ('mu', np.arange(3)), ('phi', np.arange(5))])
    >>> gd6 = GDataset(np.arange(48).reshape(3, 2, 2, 4),
    ...                np.array([0.5]*48).reshape(3, 2, 2, 4),
    ...                bins=bins2, name='gd6')
    >>> gd6.value.ndim == 4
    True

To remove first bin on energy dimension and last bin on phi dimension, the
slice to be used is: ``[1:, :, :, :-1]``.

    >>> gd6_1 = gd6[1:, :, :, :-1]
    >>> gd6_1.__class__
    <class 'valjean.gavroche.gdataset.GDataset'>
    >>> gd6.value.shape == (3, 2, 2, 4)
    True
    >>> gd6_1.value.shape == (2, 2, 2, 3)
    True
    >>> np.array_equal(gd6_1.value, [[[[16, 17, 18], [20, 21, 22]],
    ...                               [[24, 25, 26], [28, 29, 30]]],
    ...                              [[[32, 33, 34], [36, 37, 38]],
    ...                               [[40, 41, 42], [44, 45, 46]]]])
    True
    >>> np.array_equal(gd6_1.error, np.array([0.5]*24).reshape(2, 2, 2, 3))
    True
    >>> list(gd6_1.bins.keys()) == list(gd6.bins.keys())
    True
    >>> np.array_equal(gd6_1.bins['e'], gd6.bins['e'][1:])
    True
    >>> np.array_equal(gd6_1.bins['t'], gd6.bins['t'])
    True
    >>> np.array_equal(gd6_1.bins['mu'], gd6.bins['mu'])
    True
    >>> np.array_equal(gd6_1.bins['phi'], gd6.bins['phi'][:-1])
    True

If we only want the second bin in time keeping all bins in energy and direction
angles, the slice is ``[:, 1:2, :, :]``.

    >>> gd6_2 = gd6[:, 1:2, :, :]
    >>> gd6_2.value.shape == (3, 1, 2, 4)
    True
    >>> np.array_equal(gd6_2.value, [[[[8,  9, 10, 11], [12, 13, 14, 15]]],
    ...                              [[[24, 25, 26, 27], [28, 29, 30, 31]]],
    ...                              [[[40, 41, 42, 43], [44, 45, 46, 47]]]])
    True
    >>> list(gd6_2.bins.keys()) == list(gd6.bins.keys())
    True
    >>> all(x.size == y+1
    ...     for x, y in zip(gd6_2.bins.values(), gd6_2.value.shape)) == True
    True
    >>> np.array_equal(gd6_2.bins['t'], [1, 2])
    True

Bins are changed accordingly.


.. warning::
    Comparison to `NumPy`: index and ellipsis are other slicing possibilities
    on :obj:`numpy.ndarray` (see `numpy indexing`_ for current version of
    `NumPy`), but they are disabled here to avoid confusions. Errors are raised
    if required.

    >>> gd1[1]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    >>> gd6_2e = gd6[:, 1, :, :]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    >>> gd6e = gd6[1:, ..., :-1]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    It also need to have the same dimension as the value:

    >>> gd6_2e = gd6[:, 1:2]
    Traceback (most recent call last):
        [...]
    ValueError: len(index) should have the same dimension as the value \
numpy.ndarray, i.e. (# ',' = dim-1).
    ':' can be used for a slice (dimension) not affected by the selection.
    If dim(value) == 1 a slice can be required.

    A single slice is only possible for arrays for dimension 1:

    >>> gd6_2f = gd6[1:2]
    Traceback (most recent call last):
        [...]
    ValueError: len(index) should have the same dimension as the value \
numpy.ndarray, i.e. (# ',' = dim-1).
    ':' can be used for a slice (dimension) not affected by the selection.
    If dim(value) == 1 a slice can be required.

    >>> gd7 = GDataset(value=np.arange(48), error=np.array([1]*48))
    >>> gd7.ndim
    1
    >>> gd7.shape
    (48,)
    >>> gd7_extract = gd7[20:24]
    >>> np.array_equal(gd7_extract.value, [20, 21, 22, 23])
    True

.. warning::
    Slicing can also only be applied on :obj:`numpy.ndarray`, not on
    :obj:`numpy.generic`:

    >>> gd8 = GDataset(value=np.int32(100), error=np.int32(1))
    >>> gd8[0:1]
    Traceback (most recent call last):
        [...]
    TypeError: [] (__getitem__) can only be applied on numpy.ndarrays
'''
# pylint: enable=trailing-whitespace
import logging
from collections import OrderedDict
import numpy as np
from ..eponine.dataset import Dataset

LOGGER = logging.getLogger('valjean')


class GDataset(Dataset):
    '''A :class:`~eponine.Dataset` with mathematical operations.'''

    @classmethod
    def from_dataset(cls, dataset):
        '''Construct a :class:`GDataset` from an instance of a
        :class:`~eponine.Dataset`.'''
        return cls(value=dataset.value, error=dataset.error,
                   bins=dataset.bins, name=dataset.name)

    def _check_datasets_consistency(self, other, operation=""):
        if other.value.shape != self.value.shape:
            raise ValueError("Datasets to {} do not have same shape"
                             .format(operation))
        if other.bins != OrderedDict():
            if any((s != o) for s, o in zip(self.bins, other.bins)):
                raise ValueError("Datasets to {} do not have same bins names"
                                 .format(operation))
            if not all(np.allclose(self.bins[s], other.bins[o])
                       for s, o in zip(self.bins, other.bins)):
                raise ValueError("Datasets to {} do not seem to have the same "
                                 "bins".format(operation))

    def __add__(self, other):
        LOGGER.debug("in %s.__add__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Int, float, np.array and Dataset"
                            "accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(self.value + other, self.error,
                            bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "add")
        value = self.value + other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __sub__(self, other):
        LOGGER.debug("in %s.__sub__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Int, float, np.array and Dataset "
                            "accepted for the moment")
        if not isinstance(other, Dataset):
            return GDataset(self.value - other, self.error,
                            bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "subtract")
        value = self.value - other.value
        error = np.sqrt(self.error**2 + other.error**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __mul__(self, other):
        LOGGER.debug("in %s.__mul__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                self.value * other, self.error * other,
                bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "multiply")
        value = self.value * other.value
        error = np.sqrt((self.error * other.value)**2
                        + (other.error * self.value)**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __truediv__(self, other):
        LOGGER.debug("in %s.__truediv__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                self.value / other, self.error / other,
                bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "divide")
        value = self.value / other.value
        # RuntimeWarning can be ignored thanks to the commented line.
        # 'log' can be used instead of 'ignore' but did not work.
        # with np.errstate(divide='divide', invalid='ignore'):
        error = np.sqrt((self.error / other.value)**2
                        + (self.value * other.error / other.value**2)**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    @staticmethod
    def _get_bins_slice(index):
        if index.stop is not None:
            stop = index.stop+1 if index.stop > 0 else index.stop
            tmpind = slice(index.start, stop, index.step)
            return tmpind
        return index

    def _get_bins_items(self, index):
        nbins = self.bins.copy()
        slices = index if isinstance(index, tuple) else (index,)
        for ind, kbin, dim in zip(slices, self.bins, self.value.shape):
            bindex = (ind if len(self.bins[kbin]) == dim
                      else self._get_bins_slice(ind))
            nbins[kbin] = self.bins[kbin][bindex]
        return nbins

    def __getitem__(self, index):
        LOGGER.debug("in %s.__getitem__ with index=%s of type %s",
                     self.__class__.__name__, index, type(index))
        if not isinstance(self.value, np.ndarray):
            raise TypeError("[] (__getitem__) can only be applied "
                            "on numpy.ndarrays")
        if not (isinstance(index, slice)
                or (isinstance(index, tuple)
                    and all(isinstance(i, slice) for i in index))):
            raise TypeError("Index can only be a slice or a tuple of slices")
        if ((isinstance(index, tuple) and self.value.ndim != len(index))
                or (isinstance(index, slice) and self.value.ndim != 1)):
            raise ValueError("len(index) should have the same dimension as "
                             "the value numpy.ndarray, i.e. (# ',' = dim-1).\n"
                             "':' can be used for a slice (dimension) not "
                             "affected by the selection.\n"
                             "If dim(value) == 1 a slice can be required.")
        value = self.value[index]
        error = self.error[index]
        bins = self._get_bins_items(index)
        LOGGER.debug("Shape: %s -> %s", self.value.shape, value.shape)
        LOGGER.debug("Bins:%s -> %s", self.bins, bins)
        return GDataset(value, error, bins=bins, name=self.name)


def consistent_datasets(gds1, gds2):
    '''Return `True` if datasets are consistent = same shape.'''
    return gds1.value.shape == gds2.value.shape


def same_coords(ds1, ds2, *, rtol=1e-5, atol=1e-8):
    '''Return `True` if coordinates (bins) are compatible.

    :param ds1: the first array of coordinate arrays.
    :param ds2: the second array of coordinate arrays.
    :param float rtol: the relative tolerance — see :func:`numpy.allclose`.
    :param float atol: the absolute tolerance — see :func:`numpy.allclose`.

    Comparison on keys and values.
    '''
    if not consistent_datasets(ds1, ds2):
        return False
    if len(ds1.bins) != len(ds2.bins):
        return False
    return all(
        (s == o
         and np.allclose(ds1.bins[s], ds2.bins[o], rtol=rtol, atol=atol))
        for s, o in zip(ds1.bins, ds2.bins))
