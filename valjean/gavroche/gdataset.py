# pylint: disable=trailing-whitespace
'''Extension of class eponine.dataset.Dataset in other to perform simple
calculations and usual operations on datasets ``(+, -, *, /, [])``.

All operations conserve the name of the initial dataset.

.. todo::

    Real documentation, implementation of tests in this documentation and tests
    for pytest using hypothesis.

.. _numpy indexing:
   https://docs.scipy.org/doc/numpy/user/basics.indexing.html


Creation of a :class:`GDataset`
-------------------------------

GDatasets can be created from :class:`Dataset` or directly from their
arguments.

    >>> from collections import OrderedDict
    >>> from valjean.gavroche.gdataset import GDataset

From the default arguments:

    >>> bins = OrderedDict([('e', np.array([1, 2, 3])), ('t', np.arange(5))])
    >>> gd1 = GDataset(np.arange(10).reshape(2, 5),
    ...                np.array([0.1]*10).reshape(2, 5), bins=bins, name='gd1')
    >>> print(gd1)
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[0 1 2 3 4]
     [5 6 7 8 9]],
            error: [[0.1 0.1 0.1 0.1 0.1]
     [0.1 0.1 0.1 0.1 0.1]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

From a :class:`Dataset` (usually obtained from parsing):

    >>> from valjean.eponine.dataset import Dataset
    >>> ds = Dataset(np.arange(3), np.array([0.5]*3), name='ds')
    >>> print(ds)
    class: <class 'valjean.eponine.dataset.Dataset'>, data type: \
<class 'numpy.ndarray'>
            name: ds, with shape (3,),
            value: [0 1 2],
            error: [0.5 0.5 0.5],
            bins: OrderedDict()
    >>> gds = GDataset(ds)
    >>> print(gds)
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: ds, with shape (3,),
            value: [0 1 2],
            error: [0.5 0.5 0.5],
            bins: OrderedDict()


Operations available on Datasets
--------------------------------

Standard operations are available for :class:`GDataset`, inherited from
:class:`Dataset`. Examples of their use are given, including failing cases.
Some are used in various methods but shown only once.

Addition and subtraction
^^^^^^^^^^^^^^^^^^^^^^^^^
Addition and subtraction are possible between a :class:`GDataset` and a scalar
(:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another :class:`GDataset`.
The operator to use for addition is ``+`` and for subtraction ``-``.

Retrictions in addition or subtraction with a :obj:`numpy.ndarray` are handled
by `Numpy`.

The addition or subtraction f 2 :class:`GDataset` can be done if
* both values have the same shape
* bins conditions:

    * OR the second :class:`GDataset` no has bins
    * OR bins are approximately the same, i.e. have the same keys and bins
      values are without 1e-5 tolerance (default from `Numpy` for allclose
      method)


Example addition of a scalar value (only on value)
``````````````````````````````````````````````````

    >>> gd1 + 10
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[10 11 12 13 14]
     [15 16 17 18 19]],
            error: [[0.1 0.1 0.1 0.1 0.1]
     [0.1 0.1 0.1 0.1 0.1]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

As expected it 'only' acts on the value, error and bins are unchanged.

Example of subtraction of a :obj:`numpy.ndarray`
`````````````````````````````````````````````````

    >>> a = np.array([100]*10).reshape(2, 5)
    >>> gd1 - a
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[-100  -99  -98  -97  -96]
     [ -95  -94  -93  -92  -91]],
            error: [[0.1 0.1 0.1 0.1 0.1]
     [0.1 0.1 0.1 0.1 0.1]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

``a`` and ``gd1`` have the same shape to everything is fine.

    >>> b = np.array([100]*10)
    >>> gd1 + b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `Numpy` raises an exception.

.. _addition_gdataset:

Example of addition or subtraction of another :class:`GDataset`
````````````````````````````````````````````````````````````````

    >>> gd2 = GDataset(np.arange(20, 30).reshape(2, 5),
    ...                np.arange(2., 7., 0.5).reshape(2, 5),
    ...                bins=bins, name='gd2')
    >>> gd1 + gd2
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[20 22 24 26 28]
     [30 32 34 36 38]],
            error: [[2.00249844 2.5019992  3.0016662  3.50142828 4.0012498 ]
     [4.50111097 5.0009999  5.50090902 6.00083328 6.50076919]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

The error is calulated considering both datasets are independent, so
quadratically (e = sqrt(gd1.e**2 + gd2.e**2)).

Datasets without binning can also be added:

    >>> gd3 = GDataset(np.arange(200, 300, 10).reshape(2, 5),
    ...                np.array([0.1]*10).reshape(2, 5), name='gd3')
    >>> print(gd3)
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd3, with shape (2, 5),
            value: [[200 210 220 230 240]
     [250 260 270 280 290]],
            error: [[0.1 0.1 0.1 0.1 0.1]
     [0.1 0.1 0.1 0.1 0.1]],
            bins: OrderedDict()
    >>> gd1 + gd3  # doctest: +NORMALIZE_WHITESPACE
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[200 211 222 233 244]
     [255 266 277 288 299]],
            error: [[0.14142136 0.14142136 0.14142136 0.14142136 0.14142136]
     [0.14142136 0.14142136 0.14142136 0.14142136 0.14142136]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

Bins of the dataset on the left are kept.

Like in `Numpy` array addition, values need to have the same shape:

    >>> gd4 = GDataset(np.arange(5), np.array([0.01]*5), name='gd4')
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

    >>> bins6 = OrderedDict([('e', np.array([1, 2, 30])), ('t', np.arange(5))])
    >>> gd6 = GDataset(np.arange(0, -10, -1).reshape(2, 5),
    ...                np.array([0.01]*10).reshape(2, 5),
    ...                bins=bins6, name='gd5')
    >>> gd1 - gd6
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to subtract do not seem to have the same bins


Multiplication and division
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Multiplication and division are possible between a :class:`GDataset` and a
scalar (:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another
:class:`GDataset`.
The operator to use for multiplication is ``*`` and for division ``/``.

Retrictions in multiplication and division with a :obj:`numpy.ndarray` are
handled by `Numpy`.

The multiplication or division of 2 :class:`GDataset` can be done if
* both values have the same shape
* bins conditions:

    * OR the second :class:`GDataset` no has bins
    * OR bins are approximately the same, i.e. have the same keys and bins
      values are without 1e-5 tolerance (default from `Numpy` for allclose
      method)

Division by zero, nan or inf are handled by `Numpy` and return a
RunningWarning from `Numpy` (only in the zero case).


Example multiplication of a scalar value
````````````````````````````````````````

    >>> gd1 * 10
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[ 0 10 20 30 40]
     [50 60 70 80 90]],
            error: [[1. 1. 1. 1. 1.]
     [1. 1. 1. 1. 1.]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

As expected it acts on the value and on the error. Bins are unchanged.


.. _division_by_nparray:

Example of division of a :obj:`numpy.ndarray`
`````````````````````````````````````````````

    >>> gd1 / a
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 5),
            value: [[0.   0.01 0.02 0.03 0.04]
     [0.05 0.06 0.07 0.08 0.09]],
            error: [[0.001 0.001 0.001 0.001 0.001]
     [0.001 0.001 0.001 0.001 0.001]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])

``a`` and ``gd1`` have the same shape to everything is fine.

    >>> gd1 / b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `Numpy` raises an exception.

If the :obj:`numpy.ndarray`: contains ``0``, ``nan`` or ``inf``, `Numpy` deals
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


Example 1: removing first and last bin in time on ``gd1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Time is the second dimension, to remove first and last bins the usual slice is
``[1:-1]``, the first dimension, energy, is conserved, so its slice is ``[:]``.
The slice to apply is then ``[:, 1:-1]``.

    >>> print(gd1[:, 1:-1])
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (2, 3),
            value: [[1 2 3]
     [6 7 8]],
            error: [[0.1 0.1 0.1]
     [0.1 0.1 0.1]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([1, 2, 3]))])

Slicing is also applied on bins.


Example 2: removing first and last bin in energy on ``gd1``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following the same logic the slice is ``[1:-1, :]``, but the issue is that
``gd1`` has only 2 bins in energy, so removing first and second should give an
empty GDataset.

    >>> print(gd1[1:-1, :])
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd1, with shape (0, 5),
            value: [],
            error: [],
            bins: OrderedDict([('e', array([2])), ('t', \
array([0, 1, 2, 3, 4]))])

This is what we obtain. Note that in this case, as bins are in reality the
edges of the bins we have N+1 values in the bins compared to the value/error
where we have N values. Slicing then give one value in energy bins, so unusable
here (it would be if we have values and centers of bins instead of edges of
bins).


Example 3: index, ellipsis are not possible on GDataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Index and ellipsis are other slicing possibilities on :obj:`numpy.ndarray` (see
`numpy indexing_` for current version of `Numpy`), but they are disabled here
to avoid confusions. Assertion errors are raised if called.

    >>> gd1[1]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    >>> bins2 = OrderedDict([('e', np.arange(4)), ('t', np.arange(3)),
    ...                      ('mu', np.arange(3)), ('phi', np.arange(5))])
    >>> gd6 = GDataset(np.arange(48).reshape(3, 2, 2, 4),
    ...                np.array([0.5]*48).reshape(3, 2, 2, 4),
    ...                bins=bins2, name='gd6')
    >>> print(gd6[1:, ..., :-1])
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

To avoid this ellipsis use ``:`` for the untouched dimensions. Number of ','
has to be dimension -1.

    >>> print(gd6[1:, :, :, :-1])  # doctest: +ELLIPSIS
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd6, with shape (2, 2, 2, 3),
            value: [[[[16 17 18]
    ...
       [44 45 46]]]],
            error: [[[[0.5 0.5 0.5]
    ...
       [0.5 0.5 0.5]]]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2])), ('mu', array([0, 1, 2])), ('phi', array([0, 1, 2, 3]))])

To get the GDataset on one index (or one bins), index won't be possible. For
example, with ``gd6``, we want the second bin in time keeping all bins in
energy and direction angles.

    >>> print(gd6[:, 1, :, :])
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

This is failing as an index had been required. Instead build the corresponding
slice:

    >>> print(gd6[:, 1:2, :, :]) # doctest: +ELLIPSIS
    class: <class 'valjean.gavroche.gdataset.GDataset'>, data type: \
<class 'numpy.ndarray'>
            name: gd6, with shape (3, 1, 2, 4),
            value: [[[ 8  9 10 11]
    ...
      [44 45 46 47]]],
            error: [[[0.5 0.5 0.5 0.5]
    ...
      [0.5 0.5 0.5 0.5]]],
            bins: OrderedDict([('e', array([0, 1, 2, 3])), ('t', \
array([1, 2])), ('mu', array([0, 1, 2])), ('phi', array([0, 1, 2, 3, 4]))])

Slicing can also only be applied on :obj:`numpy.ndarray`, not on
:obj:`numpy.generic`:

    >>> gd7 = GDataset(np.int32(100), np.int32(1))
    >>> gd7[0:1]
    Traceback (most recent call last):
        [...]
    TypeError: [] (__getitem__) can only be applied on numpy.ndarrays

Bins are changed accordingly.
'''
# pylint: enable=trailing-whitespace
import logging
from collections import OrderedDict
import numpy as np
from valjean.eponine.dataset import Dataset
# from ..eponine.dataset import Dataset

LOGGER = logging.getLogger('valjean')


class GDataset(Dataset):
    '''Sub-class to extend Dataset (in eponine).'''

    # works but looks useless
    # def __new__(cls, obj):
    #     instance = super(GDataset, cls).__new__(cls)
    #     return instance

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(**args[0].__dict__())
        else:
            # if kwargs:
            super().__init__(*args, **kwargs)
            # else:
            #     super().__init__(*args)

    # def __init__(self, obds):
    #     print("\x1b[36m", type(obds), "\x1b[0m")
    #     super().__init__(**obds.__dict__())

    # def __repr__(self):
    #     return super().__repr__()

    # def __setattr__(self, name, value):
    #     print("in __setattr__, name:", name, "value:", value)
    #     return super().__setattr__(name, value)

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
        # assert (other.value.shape == self.value.shape
        #         and (other.bins == OrderedDict()
        #              or all((s == o
        #                      and np.allclose(self.bins[s], other.bins[o]))
        #                     for s, o in zip(self.bins, other.bins)))), \
        #     ("Datasets to {} do not have same dimensions or the same bins"
        #      .format(operation))

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
        error = value * np.sqrt((self.error / self.value)**2
                                + (other.error / other.value)**2)
        return GDataset(value, error, bins=self.bins, name=self.name)

    def __truediv__(self, other):
        LOGGER.debug("in %s.__truediv__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return GDataset(
                self.value / other, self.error / other,
                bins=self.bins, name=self.name)
        self._check_datasets_consistency(other, "divide")
        value = self.value / other.value
        # RunningWarning can be ignored thanks to the commented line.
        # 'log' can be used instead of 'ignore' but did not work.
        # with np.errstate(divide='divide', invalid='ignore'):
        error = value * np.sqrt((self.error / self.value)**2
                                + (other.error / other.value)**2)
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
            or (isinstance(index, slice) and self.value.ndim == 1)):
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
