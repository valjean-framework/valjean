'''Tests for the submodules in :mod:`valjean.gavroche.diagnostics`.'''

# pylint: disable=unused-import,wrong-import-order,no-value-for-parameter
from ..context import valjean

from hypothesis import given, event
from hypothesis.strategies import shared, one_of

from valjean.gavroche.diagnostics.metadata import TestMetadata
from .conftest import metadata_dicts


@given(metadata1=shared(metadata_dicts(), key='metadata'),
       metadata2=one_of(shared(metadata_dicts(), key='metadata'),
                        metadata_dicts()))
def test_metadata_success(metadata1, metadata2):
    '''Test that :class:`~.TestMetadata` yields outcomes that are consistent
    with direct dictionary comparison.

    This test sometimes draws equal metadata, and sometimes draws different
    metadata, thank to the magic of :func:`hypothesis.strategies.shared`.
    '''
    test = TestMetadata({'metadata1': metadata1, 'metadata2': metadata2},
                        name='metadata_test', description='a metadata test')
    if metadata1 == metadata2:
        event('equal metadata')
        assert test.evaluate()
    else:
        event('different metadata')
        assert not test.evaluate()


@given(metadata=metadata_dicts())
def test_metadata_exclude(metadata):
    '''Test that the `exclude` keyword excludes the comparison of a metadata
    keyword.'''
    metadata_mod = metadata.copy()
    # modify the first element of metadata_mod
    first_key, first_value = next(x for x in metadata_mod.items())
    metadata_mod[first_key] = first_value + '_modified'
    # exclude first_key from the test
    test = TestMetadata({'metadata1': metadata, 'metadata2': metadata_mod},
                        name='metadata_test', description='a metadata test',
                        exclude=(first_key,))
    # the test should succeed
    assert test.evaluate()
