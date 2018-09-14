'''Tests for the :mod:`~.using` module.'''

from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.eponine.using import using
from valjean import LOGGER


@using('param1', len, 'asd')
@using('param2', lambda x: x+1, 1)
def some_function(param1, param2):
    '''Test that the :func:`using` decorator works.'''
    assert param1 == 3
    assert param2 == 2


def test_using_multiple():
    '''Test that multiple :func:`~.using` decorators work.'''
    some_function()  # pylint: disable=no-value-for-parameter


def check_kwargs_return_42(expected_task_name, **kwargs):
    '''Helper function to test kwargs to :func:`using`.'''
    assert kwargs == {'task': expected_task_name}
    return 42


@using('param', check_kwargs_return_42, 'task_name', task='task_name')
def with_kwargs(param):
    '''Helper function to test kwargs to :func:`~.using`.'''
    assert param == 42


def test_using_with_kwargs():
    '''Test that `using` correctly pass kwargs to the delayed function.'''
    with_kwargs()  # pylint: disable=no-value-for-parameter


def test_using_data_deps():
    '''Test that :func:`~.using` correctly tracks data dependencies.'''
    assert hasattr(with_kwargs, 'using_dict')
    assert 'param' in with_kwargs.using_dict
    func, args, kwargs = with_kwargs.using_dict['param']
    assert func == check_kwargs_return_42
    assert args == ('task_name',)
    assert kwargs == {'task': 'task_name'}


TASK_TESTS = {}
for task in ['task1', 'task2']:
    # the `a_task` argument is necessary to capture the *value* of the `task`
    # variable at the moment the function is defined
    @using('param', check_kwargs_return_42, task, task=task)
    def with_kwargs_in_loop(param,
                            a_task=task):  # pylint: disable=unused-argument
        '''Helper function to test :func:`~.using` in a loop.'''
        assert param == 42
    TASK_TESTS[task] = with_kwargs_in_loop


def test_using_data_deps_loop():
    '''Test :func:`~.using` data dependencies for multiple uses.

    This test checks that data dependencies are correctly handled in case
    :func:`~.using` is used multiple times to decorate the "same" function in a
    loop with different arguments.
    '''
    for a_task, test in TASK_TESTS.items():
        LOGGER.debug('running test %s', test.__name__)
        test()
        assert hasattr(test, 'using_dict')
        assert 'param' in test.using_dict
        func, args, kwargs = test.using_dict['param']
        assert func == check_kwargs_return_42
        assert args == (a_task,)
        assert kwargs == {'task': a_task}


def test_using_class():
    '''Test that :func:`~.using` also works on object constructors.'''
    @using('param', lambda x: x + 'sindaco', 'vice')
    class _SomeClass:
        def __init__(self, param):
            self.param = param

    some_object = _SomeClass()  # pylint: disable=no-value-for-parameter
    assert some_object.param == 'vicesindaco'
