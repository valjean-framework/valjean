'''Tests for the :mod:`~valjean.javert.representation` module.'''
import pytest

# pylint: disable=wrong-import-order
from ..context import valjean  # pylint: disable=unused-import
from valjean.javert.items import TableItem
# from valjean.javert.representation import (FullRepresentation,
#                                            EmptyRepresentation)
from valjean.javert.representation import (TableRepresentation,
                                           EmptyRepresentation)

from ..gavroche.conftest import (equal_test,  # pylint: disable=unused-import
                                 approx_equal_test)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_full_repr(test_name, request):
    '''Test that :class:`~.FullRepresentation` yields all the expected items
    for equality tests.'''
    test = request.getfixturevalue(test_name)
    representation = TableRepresentation()
    items = representation(test.evaluate())
    assert isinstance(items, list)
    assert any(isinstance(item, TableItem) for item in items)


@pytest.mark.parametrize('test_name', ['equal_test', 'approx_equal_test'])
def test_empty_repr(test_name, request):
    '''Test that :class:`~.EmptyRepresentation` yields no items for equality
    tests.'''
    test = request.getfixturevalue(test_name)
    representation = EmptyRepresentation()
    items = representation(test.evaluate())
    assert isinstance(items, list)
    assert not items
