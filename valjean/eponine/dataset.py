# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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

# pylint: disable=trailing-whitespace
# pylint: disable=too-many-lines
'''Common module to structure data in same way for all codes.

.. _numpy indexing: https://numpy.org/doc/stable/user/basics.indexing.html
.. _numpy masked: https://numpy.org/doc/stable/reference/maskedarray.html

.. doctest:: dataset
    :hide:

    >>> # noqa: W291

Dataset definition and initialisation
-------------------------------------

A dataset is composed by 5 members:

  * value: a :obj:`numpy.ndarray` or a :obj:`numpy.generic` (scalar from numpy
    represented like the arrays, with dim, etc)
  * error: an object of same type as value
  * bins: an :obj:`collections.OrderedDict` (optional and named argument)
  * name: name of the dataset (optional and named argument)
  * what: can be used to store the name of the quantity represented by the
    dataset (optional and named argument)

The bins object should have the same dimension as the value, the order matches
the dimensions. If no bins are available it is still possible to use an empty
:obj:`collections.OrderedDict`.

>>> from valjean.eponine.dataset import Dataset
>>> import numpy as np
>>> from collections import OrderedDict
>>> bins = OrderedDict([('e', np.array([1, 2, 3])), ('t', np.arange(5))])
>>> ds1 = Dataset(np.arange(10).reshape(2, 5),
...               np.array([0.3]*10).reshape(2, 5),
...               bins=bins, name='ds1', what='spam')
>>> ds1.name
'ds1'
>>> ds1.what
'spam'
>>> len(bins) == ds1.ndim
True
>>> ds1.error.shape == ds1.value.shape
True
>>> ds1.value.shape == (2, 5)
True
>>> np.array_equal(ds1.value, [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
True
>>> np.array_equal(ds1.error,
...                [[0.3, 0.3, 0.3, 0.3, 0.3], [0.3, 0.3, 0.3, 0.3, 0.3]])
True
>>> list(bins.keys())
['e', 't']
>>> np.array_equal(bins['e'], [1, 2, 3])
True
>>> np.array_equal(bins['t'], [0, 1, 2, 3, 4])
True

A new dataset can also be created from an already existing one, using ``copy``.
No matter how the dataset is generated, attributes can be changed afterwards:

>>> nds = ds1.copy()
>>> nds.name = 'egg'
>>> nds.what = ''
>>> print('name: ds1={!r}, nds={!r}'.format(ds1.name, nds.name))
name: ds1='ds1', nds='egg'
>>> print('what: ds1={!r}, nds={!r}'.format(ds1.what, nds.what))
what: ds1='spam', nds=''
>>> np.array_equal(ds1.value, nds.value)
True


Errors are emitted if the arguments do not have the expected type or if the
shapes or dimensions are not consistent:

>>> tds = Dataset([1, 2, 3], [0.5, 0.5, 0.5])
Traceback (most recent call last):
        [...]
TypeError: value does not have the expected type (numpy.ndarray or \
numpy.generic = scalar)

>>> tds = Dataset(np.arange(6).reshape(2, 3), np.arange(6).reshape(3, 2))
Traceback (most recent call last):
        [...]
ValueError: Value and error do not have the same shape

>>> tds = Dataset(np.arange(6).reshape(2, 3),
...               np.array([0.5]*6).reshape(2, 3),
...               bins={'spam': [1, 2], 'egg': [1, 2, 3]})
Traceback (most recent call last):
        [...]
TypeError: bins should be an OrderedDict

>>> tds = Dataset(np.arange(6).reshape(2, 3),
...               np.array([0.5]*6).reshape(2, 3),
...               bins=OrderedDict([('spam', [1, 2])]))
Traceback (most recent call last):
        [...]
ValueError: Number of dimensions of bins does not correspond to number of \
dimensions of value


Squeezing a dataset
-------------------

If there are useless dimensions, the dataset can be squeezed:

>>> vals = np.arange(6).reshape(1, 2, 1, 3)
>>> errs = np.array([0.1]*6).reshape(1, 2, 1, 3)
>>> bins2 = OrderedDict([('bacon', np.array([0, 1])),
...                      ('egg', np.array([0, 2, 4])),
...                      ('sausage', np.array([10, 20])),
...                      ('spam', np.array([-5, 0, 5, 10]))])
>>> ds = Dataset(vals, errs, bins=bins2)
>>> ds.value.shape == (1, 2, 1, 3)
True
>>> len(ds.bins) == 4
True
>>> np.array_equal(ds.value, np.array([[[[0, 1, 2]], [[3, 4, 5]]]]))
True
>>> sds = ds.squeeze()
>>> sds.ndim
2
>>> len(sds.bins) == 2
True
>>> sds.shape
(2, 3)
>>> list(len(x)-1 for x in sds.bins.values())  # edges of bins, so N+1
[2, 3]
>>> list(sds.bins.keys()) == ['egg', 'spam']
True
>>> np.array_equal(sds.value, np.array([[0, 1, 2], [3, 4, 5]]))
True

The dimensions with only one bin are squeezed, the same is done on the bins.

>>> nsds = ds.squeeze()
>>> np.array_equal(nsds.value, sds.value)
True
>>> nsds.bins == sds.bins
True


Operations available on Datasets
--------------------------------

Standard operations, ``(+, -, *, /, [])``, are available for :class:`Dataset`.
Examples of their use are given, including failing cases. Some are used in
various methods but shown only once.

All operations conserve the name of the initial dataset.

The **what** attribute can be used to store the name of the quantity
represented by the dataset. It is updated if it involves another dataset:

* in addition or substraction, if **what** is different it contains both
  separated by the symbol
* in multiplication or division it always contains both separeted by the symbol

Addition and subtraction
^^^^^^^^^^^^^^^^^^^^^^^^
Addition and subtraction are possible between a :class:`Dataset` and a scalar
(:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another :class:`Dataset`.
The operator to use for addition is ``+`` and for subtraction ``-``.

Restrictions in addition or subtraction with a :obj:`numpy.ndarray` are handled
by `NumPy`.

The addition or subtraction of two :class:`Dataset` can be done if

* both values have the same shape (:func:`consistent_datasets`)
* bins conditions (:func:`same_coords`):

    * EITHER the second :class:`Dataset` does not have any bins
    * OR bins are the same, i.e. have the same keys and bins values


Example addition of a scalar value (only on value)
``````````````````````````````````````````````````

    >>> ds1p10 = ds1 + 10
    >>> np.array_equal(ds1p10.value,
    ...                [[10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
    True
    >>> np.array_equal(ds1p10.error, ds1.error)
    True
    >>> ds1p10.bins == ds1.bins
    True
    >>> ds1p10.what == ds1.what
    True

As expected it 'only' acts on the value, error and bins are unchanged.


Example of subtraction of a :obj:`numpy.ndarray`
````````````````````````````````````````````````

    >>> a = np.array([100]*10).reshape(2, 5)
    >>> ds1.value.shape == a.shape
    True
    >>> ds1ma = ds1 - a
    >>> ds1ma.__class__
    <class 'valjean.eponine.dataset.Dataset'>
    >>> np.array_equal(ds1ma.value, [[-100, -99, -98, -97, -96],
    ...                              [-95, -94, -93, -92, -91]])
    True
    >>> np.array_equal(ds1ma.error, ds1.error)
    True
    >>> ds1ma.bins == ds1.bins
    True
    >>> ds1ma.what == ds1.what
    True

``a`` and ``ds1`` have the same shape to everything is fine.

    >>> b = np.array([100]*10)
    >>> ds1.value.shape == b.shape
    False
    >>> ds1pb = ds1 + b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `NumPy` raises an exception (and ds1pb is not
defined).


.. _addition_dsataset:

Example of addition or subtraction of another :class:`Dataset`
``````````````````````````````````````````````````````````````

    >>> ds2 = Dataset(value=np.arange(20, 30).reshape(2, 5),
    ...               error=np.array([0.4]*10).reshape(2, 5),
    ...               bins=bins, name='ds2', what='spam')
    >>> ds1.bins == ds2.bins
    True
    >>> ds1p2 = ds1 + ds2
    >>> ds1p2.name == ds1.name
    True
    >>> ds1p2.what == ds1.what
    True
    >>> np.array_equal(ds1p2.value, [[20, 22, 24, 26, 28],
    ...                              [30, 32, 34, 36, 38]])
    True
    >>> np.array_equal(ds1p2.error, np.array([0.5]*10).reshape(2, 5))
    True

The error is calulated considering both datasets are independent, so
quadratically (:math:`e = \\sqrt{ds1.e^2 + ds2.e^2}`).

Datasets without binning can also be added:

    >>> ds3 = Dataset(value=np.arange(200, 300, 10).reshape(2, 5),
    ...               error=np.array([0.4]*10).reshape(2, 5), name='ds3')
    >>> ds3.bins
    OrderedDict()
    >>> ds1p3 = ds1 + ds3
    >>> ds1p3.name == ds1.name
    True
    >>> ds1p3.what == ds1.what
    False
    >>> ds1p3.what
    'spam+'
    >>> np.array_equal(ds1p3.value, [[200, 211, 222, 233, 244],
    ...                              [255, 266, 277, 288, 299]])
    True
    >>> np.array_equal(ds1p3.error, np.array([0.5]*10).reshape(2, 5))
    True
    >>> same_coords(ds1p3, ds1)
    True

Bins of the dataset on the left are kept.

Like in `NumPy` array addition, values need to have the same shape:

    >>> ds4 = Dataset(np.arange(5), np.array([0.01]*5), name='ds4')
    >>> "shape ds1 {0}, ds4 {1} -> comp = {2}".format(
    ...   ds1.value.shape, ds4.value.shape, ds1.value.shape == ds4.value.shape)
    'shape ds1 (2, 5), ds4 (5,) -> comp = False'
    >>> ds1 + ds4
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to add do not have same shape

If bins are given, they need to have the same keys and the same values.

    >>> bins5 = OrderedDict([('E', np.array([1, 2, 3])), ('t', np.arange(5))])
    >>> ds5 = Dataset(np.arange(0, -10, -1).reshape(2, 5),
    ...               np.array([0.01]*10).reshape(2, 5),
    ...               bins=bins5, name='ds5')
    >>> ds1 + ds5
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to add do not have same bins names
    >>> "bins ds1: {0}, bins ds5: {1}".format(list(ds1.bins.keys()),
    ...                                     list(ds5.bins.keys()))
    "bins ds1: ['e', 't'], bins ds5: ['E', 't']"

    >>> bins6 = OrderedDict([('e', np.array([1, 2, 30])), ('t', np.arange(5))])
    >>> ds6 = Dataset(np.arange(0, -10, -1).reshape(2, 5),
    ...               np.array([0.01]*10).reshape(2, 5),
    ...               bins=bins6, name='ds6')
    >>> ds1 - ds6
    Traceback (most recent call last):
        [...]
    ValueError: Datasets to subtract do not seem to have the same bins
    >>> same_coords(ds1, ds6)
    False
    >>> list(ds1.bins.keys()) == list(ds6.bins.keys())
    True
    >>> np.array_equal(ds1.bins['e'], ds6.bins['e'])
    False
    >>> np.array_equal(ds1.bins['t'], ds6.bins['t'])
    True


Multiplication and division
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Multiplication and division are possible between a :class:`Dataset` and a
scalar (:obj:`numpy.generic`), a :obj:`numpy.ndarray` and another
:class:`Dataset`.
The operator to use for multiplication is ``*`` and for division ``/``.

Restrictions in multiplication and division with a :obj:`numpy.ndarray` are
handled by `NumPy`.

The multiplication or division of 2 :class:`Dataset` can be done if

* both values have the same shape (:func:`consistent_datasets`)
* bins conditions (:func:`same_coords`):

    * EITHER the second :class:`Dataset` does not have any bins
    * OR bins are the same, i.e. have the same keys and bins values

Division by zero, nan or inf are handled by `NumPy` and return a
RuntimeWarning from `NumPy` (only in the zero case).


Example multiplication of a scalar value
````````````````````````````````````````

    >>> ds1m10 = ds1 * 10
    >>> ds1m10.__class__
    <class 'valjean.eponine.dataset.Dataset'>
    >>> np.array_equal(ds1m10.value, [[0, 10, 20, 30, 40],
    ...                               [50, 60, 70, 80, 90]])
    True
    >>> np.array_equal(ds1m10.error, np.array([3.]*10).reshape(2, 5))
    True
    >>> same_coords(ds1m10, ds1)
    True

As expected it acts on the value and on the error. Bins are unchanged.


.. _division_by_nparray:

Example of division of a :obj:`numpy.ndarray`
`````````````````````````````````````````````

    >>> ds1da = ds1 / a
    >>> ds1da.name == ds1.name
    True
    >>> ds1da.what == ds1.what
    True
    >>> np.array_equal(ds1da.value, [[0., 0.01, 0.02, 0.03, 0.04],
    ...                              [0.05, 0.06, 0.07, 0.08, 0.09]])
    True
    >>> np.array_equal(ds1da.error, np.array([0.003]*10).reshape(2, 5))
    True
    >>> same_coords(ds1da, ds1)
    True

``a`` and ``ds1`` have the same shape to everything is fine.

    >>> ds1 / b
    Traceback (most recent call last):
        ...
    ValueError: operands could not be broadcast together with shapes (2,5) \
(10,) 


If the shapes are not the same `NumPy` raises an exception.

If the :obj:`numpy.ndarray`: contains ``0``, ``nan`` or ``inf``, `NumPy` deals
with them. It sends a RunningWarning about the division by zero.

    >>> c = np.array([[2., 3., np.nan, 4., 0.], [1., np.inf, 5., 10., 0.]])
    >>> ds1 / c  # doctest: +SKIP
    class: <class 'valjean.gavroche.dataset.Dataset'>, data type: \
<class 'numpy.ndarray'>
            name: ds1, with shape (2, 5),
            value: [[0.         0.33333333        nan 0.75              inf]
     [5.         0.         1.4        0.8               inf]],
            error: [[0.15       0.03333333        nan 0.075             inf]
     [0.3        0.         0.06       0.03              inf]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> # prints *** RuntimeWarning: divide by zero encountered in true_divide


Example of multiplication or division of another :class:`Dataset`
`````````````````````````````````````````````````````````````````

    >>> ds1m2 = ds1 * ds2
    >>> ds1m2  # doctest: +SKIP
    class: <class 'valjean.gavroche.dataset.Dataset'>, data type: \
<class 'numpy.ndarray'>
            shape (2, 5),
            value: [[  0  21  44  69  96]
     [125 156 189 224 261]],
            error: [[6.         6.31268564 6.64830806 7.00357052 7.37563557]
     [7.76208735 8.16088231 8.57029754 8.98888202 9.4154129 ]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> ds1m2.what
    'spam*spam'
    >>> same_coords(ds1m2, ds2)
    True

    >>> ds1o2 = ds1 / ds2
    >>> ds1o2  # doctest: +SKIP
    class: <class 'valjean.gavroche.dataset.Dataset'>, data type: \
<class 'numpy.ndarray'>
            shape (2, 5),
            value: [[0.         0.04761905 0.09090909 0.13043478 0.16666667]
     [0.2        0.23076923 0.25925926 0.28571429 0.31034483]],
            error: [[0.015      0.01431448 0.01373617 0.01323926 0.01280492]
     [0.01241934 0.01207231 0.01175624 0.01146541 0.0111955 ]],
            bins: OrderedDict([('e', array([1, 2, 3])), ('t', \
array([0, 1, 2, 3, 4]))])
    >>> ds1o2.what
    'spam/spam'

In both cases the error is calulated considering both datasets are independent,
so quadratically :math:`e = v*\\sqrt{{(\\frac{ds_1.e}{ds_1.v})}^2 +
{(\\frac{ds_2.e}{ds_2.v})}^2}`.

The same restictions on bins as for addition and subtraction are set for
multiplication and division, same ``AssertError`` are raised, see
:ref:`addition_dsataset`.

About the division by ``0``, ``nan`` or ``inf``, it acts like in the
multiplication or division by a :obj:`numpy.ndarray`, see
:ref:`division_by_nparray` (warnings and ``nan``, ``inf``, etc.)

>>> np.isnan((ds1/ds1).value[0][0])
True
>>> np.isinf(((ds1+1)/ds1).value[0][0])
True


Indexing and slicing
--------------------

It is only possible to get a **slice** of a dataset, getting an Dataset at a
given index is not possible (for dimensions consistency reasons). Requiring a
given index can then be done using a slice.


Getting a subset of the :class:`Dataset`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Time is the second dimension, to remove first and last bins the usual slice is
``[1:-1]``, the first dimension, energy, is conserved, so its slice is ``[:]``.
The slice to apply is then ``[:, 1:-1]``.

    >>> ds1sltfl = ds1[:, 1:-1]
    >>> ds1sltfl.__class__
    <class 'valjean.eponine.dataset.Dataset'>
    >>> np.array_equal(ds1sltfl.value, [[1, 2, 3], [6, 7, 8]])
    True
    >>> np.array_equal(ds1sltfl.error, np.array([0.3]*6).reshape(2, 3))
    True
    >>> list(ds1sltfl.bins.keys()) == list(ds1.bins.keys())
    True
    >>> np.array_equal(ds1sltfl.bins['e'], ds1.bins['e'])
    True
    >>> np.array_equal(ds1sltfl.bins['t'], ds1.bins['t'])
    False
    >>> np.array_equal(ds1sltfl.bins['t'], [1, 2, 3])
    True
    >>> ds1sltfl.name == ds1.name
    True

Slicing is also applied on bins.


.. warning::
    Requiring a slice when there are not enough elements on the dimension give
    empty arrays.

    For example: removing first and last bin in energy on ``ds1``. The slice is
    ``[1:-1, :]`` in that case, but ``ds1`` has only 2 bins in energy.

    >>> ds1slefl = ds1[1:-1, :]
    >>> ds1slefl.value.shape == (0, 5)
    True
    >>> np.array_equal(ds1slefl.value, np.array([]).reshape(0, 5))
    True
    >>> np.array_equal(ds1slefl.error, np.array([]).reshape(0, 5))
    True
    >>> np.array_equal(ds1slefl.bins['t'], ds1.bins['t'])
    True
    >>> np.array_equal(ds1slefl.bins['e'], ds1.bins['e'])
    False
    >>> np.array_equal(ds1slefl.bins['e'], [2])
    True

    Note that in this case, as bins are in reality the edges of the bins, so we
    have N+1 values in the bins compared to the value/error where we have N
    values. Slicing then give one value in energy bins, so unusable here (it
    would be empty if we have values and centers of bins instead of edges of
    bins).


All dimensions have to be present in the slice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use ``:`` for the untouched dimensions. Number of ``,`` has to be dimension -1.

Let's consider a new Dataset, with 4 dimensions:

    >>> bins2 = OrderedDict([('e', np.arange(4)), ('t', np.arange(3)),
    ...                      ('mu', np.arange(3)), ('phi', np.arange(5))])
    >>> ds6 = Dataset(np.arange(48).reshape(3, 2, 2, 4),
    ...               np.array([0.5]*48).reshape(3, 2, 2, 4),
    ...               bins=bins2, name='ds6')
    >>> ds6.value.ndim == 4
    True

To remove first bin on energy dimension and last bin on phi dimension, the
slice to be used is: ``[1:, :, :, :-1]``.

    >>> ds6_1 = ds6[1:, :, :, :-1]
    >>> ds6.value.shape == (3, 2, 2, 4)
    True
    >>> ds6_1.value.shape == (2, 2, 2, 3)
    True
    >>> np.array_equal(ds6_1.value, [[[[16, 17, 18], [20, 21, 22]],
    ...                               [[24, 25, 26], [28, 29, 30]]],
    ...                              [[[32, 33, 34], [36, 37, 38]],
    ...                               [[40, 41, 42], [44, 45, 46]]]])
    True
    >>> np.array_equal(ds6_1.error, np.array([0.5]*24).reshape(2, 2, 2, 3))
    True
    >>> list(ds6_1.bins.keys()) == list(ds6.bins.keys())
    True
    >>> np.array_equal(ds6_1.bins['e'], ds6.bins['e'][1:])
    True
    >>> np.array_equal(ds6_1.bins['t'], ds6.bins['t'])
    True
    >>> np.array_equal(ds6_1.bins['mu'], ds6.bins['mu'])
    True
    >>> np.array_equal(ds6_1.bins['phi'], ds6.bins['phi'][:-1])
    True

If we only want the second bin in time keeping all bins in energy and direction
angles, the slice is ``[:, 1:2, :, :]``.

    >>> ds6_2 = ds6[:, 1:2, :, :]
    >>> ds6_2.value.shape == (3, 1, 2, 4)
    True
    >>> np.array_equal(ds6_2.value, [[[[8,  9, 10, 11], [12, 13, 14, 15]]],
    ...                              [[[24, 25, 26, 27], [28, 29, 30, 31]]],
    ...                              [[[40, 41, 42, 43], [44, 45, 46, 47]]]])
    True
    >>> list(ds6_2.bins.keys()) == list(ds6.bins.keys())
    True
    >>> all(x.size == y+1
    ...     for x, y in zip(ds6_2.bins.values(), ds6_2.value.shape)) == True
    True
    >>> np.array_equal(ds6_2.bins['t'], [1, 2])
    True

Bins are changed accordingly.


.. warning::
    Comparison to `NumPy`: index and ellipsis are other slicing possibilities
    on :obj:`numpy.ndarray` (see `numpy indexing`_ for current version of
    `NumPy`), but they are disabled here to avoid confusions. Errors are raised
    if required.

    >>> ds1[1]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    >>> ds6_2e = ds6[:, 1, :, :]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    >>> ds6e = ds6[1:, ..., :-1]
    Traceback (most recent call last):
        [...]
    TypeError: Index can only be a slice or a tuple of slices

    It also need to have the same dimension as the value:

    >>> ds6_2e = ds6[:, 1:2]
    Traceback (most recent call last):
        [...]
    ValueError: len(index) should have the same dimension as the value \
numpy.ndarray, i.e. (# ',' = dim-1).
    ':' can be used for a slice (dimension) not affected by the selection.
    Slicing is only possible if ndim == 1

    A single slice is only possible for arrays for dimension 1:

    >>> ds6_2f = ds6[1:2]
    Traceback (most recent call last):
        [...]
    ValueError: len(index) should have the same dimension as the value \
numpy.ndarray, i.e. (# ',' = dim-1).
    ':' can be used for a slice (dimension) not affected by the selection.
    Slicing is only possible if ndim == 1

    >>> ds7 = Dataset(value=np.arange(48), error=np.array([1]*48))
    >>> ds7.ndim
    1
    >>> ds7.shape
    (48,)
    >>> ds7_extract = ds7[20:24]
    >>> np.array_equal(ds7_extract.value, [20, 21, 22, 23])
    True

.. warning::
    Slicing can also only be applied on :obj:`numpy.ndarray`, not on
    :obj:`numpy.generic`:

    >>> ds8 = Dataset(value=np.int32(100), error=np.int32(1))
    >>> ds8[0:1]
    Traceback (most recent call last):
        [...]
    TypeError: [] (__getitem__) can only be applied on numpy.ndarrays


Masked datasets
---------------

In some case it can be useful to mask some elements of a dataset. This
functionality is provided by the `numpy masked`_ arrays module. In the case of
datasets, once the mask is given it is applied to both the value and the error.

>>> mask = np.ma.masked_greater(ds1.value, 6).mask
>>> np.array_equal(mask, [[False, False, False, False, False],
...                       [False, False, True, True, True]])
True
>>> mds = ds1.mask(mask)
>>> np.ma.is_masked(ds1.value)
False
>>> np.ma.is_masked(mds.value)
True
>>> np.ma.is_masked(mds.error)
True

Bins and shape are kept.

>>> mds.shape == ds1.shape
True
>>> np.array_equal(mds.bins['e'], ds1.bins['e'])
True
>>> np.array_equal(mds.bins['t'], ds1.bins['t'])
True

The mask is propagated when performing operations on dataset.

>>> np.sum(ds1.value) == 45
True
>>> np.sum(mds.value) == 21
True
>>> sds = ds1 + mds
>>> np.ma.is_masked(sds.value)
True
>>> np.ma.is_masked(sds.error)
True
>>> np.sum(sds.value) == 42
True
'''
# pylint: enable=trailing-whitespace
from hashlib import sha256
from collections import OrderedDict
import numpy as np
from .. import LOGGER


class Dataset:
    '''Common class for data from all codes.

    For the moment, units are not treated (removed).

    .. todo::

        Think about units. Possibility: using a units package from scipy.

    .. todo::

        How to deal with bins of N values (= center of bins)
    '''

    def __init__(self, value, error, *, bins=None, name='', what=''):
        '''Dataset class initialization.

        :param value: array of N dimensions representing the values
        :type value: numpy.ndarray or numpy.generic
        :param error: array of N dimensions representing the **absolute**
          errors
        :type error: numpy.ndarray or numpy.generic
        :param bins: bins corresponding to value (named optional parameter)
        :type bins: collections.OrderedDict (str, numpy.ndarray)
        :param str name: name of the dataset (used in test representation)
        :param str what: name of the quantity represented by the dataset
        '''
        if not isinstance(value, (np.ndarray, np.generic)):
            raise TypeError("value does not have the expected type "
                            "(numpy.ndarray or numpy.generic = scalar)")
        if not isinstance(error, (np.ndarray, np.generic)):
            raise TypeError("error does not have the expected type "
                            "(numpy.ndarray or numpy.generic = scalar)")
        LOGGER.debug("Type of value: %s", type(value))
        LOGGER.debug("Value charac: ndim = %s, shape = %s, size = %s",
                     value.ndim, value.shape, value.size)
        if value.shape != error.shape:
            raise ValueError("Value and error do not have the same shape")
        if bins is not None:
            if not isinstance(bins, OrderedDict):
                raise TypeError("bins should be an OrderedDict")
            LOGGER.debug("Number of dimensions from bins: %s", len(bins))
            if bins and len(bins) != value.ndim:
                raise ValueError("Number of dimensions of bins does not "
                                 "correspond to number of dimensions of value")
            if bins and any(b.size != s and b.size != s+1
                            for b, s in zip(bins.values(), value.shape)
                            if b.size):
                raise ValueError('Number of bins does not correspond to value '
                                 'shape, bins={}, shape={}'.format(
                                     [len(b) for b in bins.values()],
                                     value.shape))
        self.value = value
        self.error = error
        self.bins = bins.copy() if bins is not None else OrderedDict()
        self.name = name
        self.what = what

    def copy(self):
        '''Return a deep copy of `self`.'''
        return Dataset(value=self.value.copy(),
                       error=self.error.copy(),
                       bins=self.bins.copy(),
                       name=self.name, what=self.what)

    def __repr__(self):
        if isinstance(self.value, np.ndarray):
            return ("class: {}, data type: {}\n"
                    "        shape: {}\n"
                    "        value: {},\n"
                    "        error: {},\n"
                    "        bins: {},\n"
                    "        name: {!r}, what: {!r}"
                    .format(self.__class__, type(self.value), self.value.shape,
                            self.value.squeeze(), self.error.squeeze(),
                            self.bins, self.name, self.what))
        return (
            "class: {}, data type: {}\n"
            "value: {:6e}, error: {:6e}, bins: {}\n"
            "name: {!r}, what: {!r}\n"
            .format(self.__class__, type(self.value),
                    self.value, self.error, self.bins,
                    self.name, self.what))

    def __str__(self):
        if isinstance(self.value, np.ndarray):
            return ("shape: {}, dim: {}, type: {}, bins: {},"
                    "name: {}, what: {}"
                    .format(self.value.shape, self.value.ndim,
                            type(self.value),
                            ["{}: {}".format(k, str(v).replace('\n', ''))
                             for k, v in self.bins.items()],
                            self.name, self.what))
        return (
            "value: {:6e}, error: {:6e}, bins: {}, type: {},"
            "name: {}, what: {}"
            .format(self.value, self.error, self.bins, type(self.value),
                    self.name, self.what))

    def squeeze(self):
        '''Squeeze dataset: remove useless dimensions.

        Squeeze is based on the shape and on the bins dim ??? To confirm...
        First squeeze bins, then arrays.
        Edges, if only one bin are not kept. Example: spectrum with one bin in
        energy (quite common)
        '''
        key_axis = dict(enumerate(self.bins))
        lbins = self.bins.copy()
        for axis, dim in enumerate(self.shape):
            if dim < 2:
                lbins.pop(key_axis[axis])
        return self.__class__(self.value.squeeze(),
                              self.error.squeeze(),
                              bins=lbins,
                              name=self.name,
                              what=self.what)

    @property
    def shape(self):
        '''Return the data shape, as a read-only property.'''
        return self.value.shape

    @property
    def ndim(self):
        '''Return the data dimension, as a read-only property.'''
        return self.value.ndim

    @property
    def size(self):
        '''Return the data size (total number of elements in the array), as a
        read-only property.'''
        return self.value.size

    def fingerprint(self):
        '''Return a hash of the content of the dataset.

        >>> vals = np.arange(10).reshape(2, 5)
        >>> errs = np.array([1]*10).reshape(2, 5)
        >>> ds = Dataset(vals, errs)
        >>> ds.fingerprint()
        'a8411470d7766c543e90f0f38241dc918b9448d1b9d19b0a9b8b6c91f61944d0'
        >>> bins = OrderedDict([('bacon', np.arange(3)),
        ...                     ('egg', np.arange(5))])
        >>> ds = Dataset(vals, errs, bins=bins)
        >>> ds.fingerprint()
        'dfec4e6ac118d30b7a83cfc500fefaec94f93a76a024d7550732cd08fbfb0fee'
        '''
        hasher = sha256()
        for data in self.data():
            hasher.update(data)
        return hasher.hexdigest()

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.

        >>> vals = np.arange(10).reshape(2, 5)
        >>> errs = np.array([1]*10).reshape(2, 5)
        >>> ds = Dataset(vals, errs)
        >>> ds.fingerprint()
        'a8411470d7766c543e90f0f38241dc918b9448d1b9d19b0a9b8b6c91f61944d0'
        >>> bins = OrderedDict([('bacon', np.arange(3)),
        ...                     ('egg', np.arange(5))])
        >>> ds = Dataset(vals, errs, bins=bins)
        >>> ds.fingerprint()
        'dfec4e6ac118d30b7a83cfc500fefaec94f93a76a024d7550732cd08fbfb0fee'
        >>> ds = Dataset(vals, errs, bins=bins, name='name')
        >>> ds.fingerprint()
        '441623c096bf917414013ebbfe345c66124f9a8dfbbd7051cf733ea20d7b651a'
        >>> ds = Dataset(vals, errs, bins=bins, name='name', what='what!')
        >>> ds.fingerprint()
        '9a42c91381d696c1af651665f84efc43efa14d9c471c4ac851239ed0779a48a0'
        '''
        yield self.__class__.__name__.encode('utf-8')
        yield np.require(self.value, requirements='C').data.cast('b')
        yield np.require(self.error, requirements='C').data.cast('b')
        if self.bins is not None:
            for key, val in self.bins.items():
                yield key.encode('utf-8')
                yield np.require(val, requirements='C').data.cast('b')
        yield self.__class__.__name__.encode('utf-8')
        yield self.name.encode('utf-8')
        yield self.what.encode('utf-8')

    def _check_datasets_consistency(self, other, operation=""):
        if other.shape != self.shape:
            raise ValueError("Datasets to {} do not have same shape"
                             .format(operation))
        if other.bins != OrderedDict():
            if any((s != o) for s, o in zip(self.bins, other.bins)):
                raise ValueError("Datasets to {} do not have same bins names"
                                 .format(operation))
            if not all(np.array_equal(self.bins[s], other.bins[o])
                       for s, o in zip(self.bins, other.bins)):
                raise ValueError("Datasets to {} do not seem to have the same "
                                 "bins".format(operation))

    def __add__(self, other):
        LOGGER.debug("in %s.__add__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Int, float, np.array and Dataset"
                            "accepted for the moment")
        if not isinstance(other, Dataset):
            return Dataset(self.value + other, self.error,
                           bins=self.bins, name=self.name, what=self.what)
        self._check_datasets_consistency(other, "add")
        value = self.value + other.value
        error = np.sqrt(self.error**2 + other.error**2)
        what = (self.what if other.what == self.what
                else self.what+'+'+other.what)
        return Dataset(value, error, bins=self.bins, name=self.name, what=what)

    def __sub__(self, other):
        LOGGER.debug("in %s.__sub__", self.__class__.__name__)
        if not isinstance(other, (int, float, np.ndarray, Dataset)):
            raise TypeError("Int, float, np.array and Dataset "
                            "accepted for the moment")
        if not isinstance(other, Dataset):
            return Dataset(self.value - other, self.error,
                           bins=self.bins, name=self.name, what=self.what)
        self._check_datasets_consistency(other, "subtract")
        value = self.value - other.value
        error = np.sqrt(self.error**2 + other.error**2)
        what = (self.what if other.what == self.what
                else self.what+'-'+other.what)
        return Dataset(value, error, bins=self.bins, name=self.name, what=what)

    def __mul__(self, other):
        LOGGER.debug("in %s.__mul__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return Dataset(
                self.value * other, self.error * other,
                bins=self.bins, name=self.name, what=self.what)
        self._check_datasets_consistency(other, "multiply")
        value = self.value * other.value
        error = np.sqrt((self.error * other.value)**2
                        + (other.error * self.value)**2)
        return Dataset(value, error, bins=self.bins, name=self.name,
                       what=self.what+'*'+other.what)

    def __truediv__(self, other):
        LOGGER.debug("in %s.__truediv__", self.__class__.__name__)
        if not isinstance(other, Dataset):
            return Dataset(
                self.value / other, self.error / other,
                bins=self.bins, name=self.name, what=self.what)
        self._check_datasets_consistency(other, "divide")
        value = self.value / other.value
        # RuntimeWarning can be ignored thanks to the commented line.
        # 'log' can be used instead of 'ignore' but did not work.
        # with np.errstate(divide='divide', invalid='ignore'):
        error = np.sqrt((self.error / other.value)**2
                        + (self.value * other.error / other.value**2)**2)
        return Dataset(value, error, bins=self.bins, name=self.name,
                       what=self.what+'/'+other.what)

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
        for ind, kbin, dim in zip(slices, self.bins, self.shape):
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
                             "Slicing is only possible if ndim == 1")
        value = self.value[index]
        error = self.error[index]
        bins = self._get_bins_items(index)
        LOGGER.debug("Shape: %s -> %s", self.shape, value.shape)
        LOGGER.debug("Bins:%s -> %s", self.bins, bins)
        return Dataset(value, error, bins=bins, name=self.name, what=self.what)

    def mask(self, mask):
        '''Apply a mask to the Dataset value and error.

        Value and error become in that case masked_arrays instead of usual
        arrays, calcuations are preserved, not using the masked elements.

        :rtype: Dataset
        '''
        return Dataset(value=np.ma.masked_array(self.value, mask),
                       error=np.ma.masked_array(self.error, mask),
                       bins=self.bins.copy(),
                       name=self.name, what=self.what)


def consistent_datasets(dss1, dss2):
    '''Return `True` if datasets are consistent = same shape.'''
    return dss1.shape == dss2.shape


def same_coords(ds1, ds2):
    '''Return `True` if coordinates (bins) are compatible.

    :param ds1: the first array of coordinate arrays.
    :param ds2: the second array of coordinate arrays.

    Comparison on keys and values.
    '''
    if not consistent_datasets(ds1, ds2):
        return False
    if len(ds1.bins) != len(ds2.bins):
        return False
    return all((s == o and np.array_equal(ds1.bins[s], ds2.bins[o]))
               for s, o in zip(ds1.bins, ds2.bins))
