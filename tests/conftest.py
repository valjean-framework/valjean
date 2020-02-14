# pylint: disable=no-value-for-parameter
'''Fixtures for the :mod:`~.valjean` tests.'''

from string import ascii_lowercase

import py
import pytest
from hypothesis.strategies import text, dictionaries, composite, lists

from .context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.config import Config

ID_CHARS = ascii_lowercase

# normalized IDs are stripped lowercase strings
IDS = text(ID_CHARS, min_size=1).map(lambda s: s.strip())

STANDARD_SECS = ['build/{}', 'checkout/{}', 'executable/{}', 'run/{}',
                 'other/{}']


###########################
#  Hypothesis strategies  #
###########################

def intercalate_strings(list1, list2):
    '''Build a string by intercalating strings from `list1` and `list2`.

    Returns a string by concatenating alternatively strings from `list1` and
    `list2`.  For instance:

        >>> list1 = ['a', 'b', 'c']
        >>> list2 = ['A', 'B']
        >>> intercalate_strings(list1, list2)
        'aAbBc'

    `list1` and `list2` must respect the following invariant::

        len(list1) == len(list2) + 1

    :param list1: a list of strings.
    :type list1: list(str)
    :paral list2: a list of strings.
    :type list2: list(str)
    '''
    intercalated = ''.join(''.join((s1, s2)) for s1, s2 in zip(list1, list2))
    return ''.join((intercalated, list1[-1]))


@composite
def section_names(draw, sec_ids):
    '''Hypothesis strategy to generate section names, with or without slash
    separator.'''
    words = draw(lists(sec_ids, min_size=1))
    n_blanks = len(words) + 1
    blanks = draw(lists(spaces(), min_size=n_blanks, max_size=n_blanks))
    return intercalate_strings(blanks, words)


@composite
def configs(draw, keys=IDS, vals=IDS, sec_names=section_names(IDS),
            min_size=0, max_size=None):
    # pylint: disable=too-many-arguments
    '''Composite Hypothesis strategy to generate Config objects.'''
    secs = dictionaries(keys, vals, min_size=min_size, max_size=max_size)
    as_dict = draw(dictionaries(sec_names, secs,
                                min_size=min_size, max_size=max_size))
    conf = Config.from_mapping(as_dict)
    return conf


@composite
def spaces(draw, min_size=0, max_size=None):
    '''Generate strings of spaces.'''
    return draw(text(' ', min_size=min_size, max_size=max_size))


#####################
#  pytest fixtures  #
#####################

@pytest.fixture(scope='function')
def empty_config():
    '''Return an empty :class:`~.Config` object.'''
    return Config([])


@pytest.fixture(scope='function')
def config_tmp(tmpdir_factory):
    '''Create a configuration object with the path options set to temporary
    directories.'''
    log_dir = str(tmpdir_factory.mktemp('log'))
    output_dir = str(tmpdir_factory.mktemp('output'))
    config = Config(paths=[])
    config.set('path', 'log-root', log_dir)
    config.set('path', 'output-root', output_dir)
    return config


def foreach_data(*args, **kwargs):
    '''Decorator that parametrizes a test function over files in the data
    directory for the current tests.

    Assume that the following snippet resides in
    :file:`tests/submod/test_submod.py`::

        @foreach_data('datafile')
        def test_something(datafile):
            pass

    When `pytest` imports :file:`test_submod.py`, it will parametrize
    the `datafile` argument to :func:`!test_something` over all the files
    present in :file:`tests/submod/data/`.

    If you wish to filter away some of the files, you can use the alternative
    syntax::

        @foreach_data(datafile=lambda path: str(path).endswith('.txt'))
        def test_something(datafile):
            pass

    Here the argument to the `datafile` keyword argument is a predicate that
    must return `True` if `path` is to be parametrized over, and `False`
    otherwise. Note that the `path` argument to the lambda is a
    :class:`py._path.local.LocalPath` object.  In this example, `pytest` will
    parametrize :func:`!test_something` only over files whose name ends in
    ``'.txt'``.
    '''

    if args:
        assert len(args) == 1, ('Only one positional argument allowed '
                                'to @foreach_data')
        assert not kwargs, ('No kwargs allowed with a positional '
                            'argument to @foreach_data')
        fix_name = args[0]
        fil = None
    else:
        assert len(kwargs) == 1, 'Only one kwarg allowed in @foreach_data'
        fix_name, fil = next(iter(kwargs.items()))

    def _decorator(wrapped):
        from inspect import getfile
        module_dir = py.path.local(getfile(wrapped))
        test_dir = module_dir.dirpath('data')
        datafiles = [path for path in test_dir.listdir(fil=fil)
                     if path.isfile()]
        ids = [str(path.basename) for path in datafiles]
        return pytest.mark.parametrize(fix_name, datafiles, ids=ids)(wrapped)
    return _decorator
