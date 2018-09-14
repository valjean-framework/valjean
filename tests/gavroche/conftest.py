'''Fixtures for the :mod:`gavroche` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
from hypothesis.strategies import composite, just

from valjean.gavroche.gdataset import GDataset
from ..eponine.conftest import datasets, perturbed_datasets


def gdatasets(*, elements=None, shape=None, dtype=None, coords=None):
    '''Strategy for generating :class:`~.gdataset.GDataset` objects.

    This strategy uses the :func:`~.datasets` strategy to generate
    :class:`~.Dataset` object and converts it to :class:`GDataset`.
    '''
    # pylint: disable=no-member
    return (datasets(elements=elements, shape=shape, dtype=dtype,
                     coords=coords)
            .map(GDataset.from_dataset))


@composite
def multiple_gdatasets(draw, size, *, elements=None):
    '''Strategy for generating multiple gdatasets with the same shape and bins.
    '''
    gd0 = draw(gdatasets())
    mult_gds = [gd0]
    for _ in range(1, size):  # elt 0 is gds
        gds = draw(gdatasets(elements=elements, shape=just(gd0.value.shape),
                             coords=just(gd0.bins)))
        mult_gds.append(gds)
    return mult_gds


def perturbed_gdatasets(min_size=0, max_size=6):
    '''Strategy to generate a list of perturbed :class:`~.GDataset` objects.

    This strategy uses the :func:`~.perturbed_datasets` strategy to generate a
    list of perturbed :class:`~.Dataset` objects, and converts them to
    :class:`GDataset`.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    # pylint: disable=no-member
    return (perturbed_datasets(min_size=min_size, max_size=max_size)
            .map(lambda ds: [GDataset.from_dataset(d) for d in ds]))
