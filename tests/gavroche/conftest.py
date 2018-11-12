'''Fixtures for the :mod:`gavroche` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
from hypothesis.strategies import composite, just

from valjean.gavroche.dataset import Dataset
from ..eponine.conftest import base_datasets, perturbed_base_datasets


def datasets(*, elements=None, shape=None, dtype=None, coords=None):
    '''Strategy for generating :class:`~.dataset.Dataset` objects.

    This strategy uses the :func:`~.base_datasets` strategy to generate
    :class:`~.BaseDataset` object and converts it to :class:`Dataset`.
    '''
    # pylint: disable=no-member
    return (base_datasets(elements=elements, shape=shape, dtype=dtype,
                          coords=coords)
            .map(Dataset.from_dataset))


@composite
def multiple_datasets(draw, size, *, elements=None):
    '''Strategy for generating multiple gdatasets with the same shape and bins.
    '''
    gd0 = draw(datasets())
    mult_gds = [gd0]
    for _ in range(1, size):  # elt 0 is gds
        gds = draw(datasets(elements=elements, shape=just(gd0.value.shape),
                            coords=just(gd0.bins)))
        mult_gds.append(gds)
    return mult_gds


def perturbed_datasets(min_size=0, max_size=6):
    '''Strategy to generate a list of perturbed :class:`~.Dataset` objects.

    This strategy uses the :func:`~.perturbed_base_datasets` strategy to
    generate a list of perturbed :class:`~.BaseDataset` objects, and converts
    them to :class:`Dataset`.

    :param int min_size: the minimum list size.
    :param int max_size: the maximum list size.
    '''
    # pylint: disable=no-member
    return (perturbed_base_datasets(min_size=min_size, max_size=max_size)
            .map(lambda ds: [Dataset.from_dataset(d) for d in ds]))
