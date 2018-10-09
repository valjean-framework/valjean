'''Fixtures for the :mod:`~.valjean` tests.'''

from string import ascii_lowercase

import pytest
from hypothesis.strategies import (text, dictionaries, composite, sampled_from,
                                   lists, tuples, integers)

from .context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.config import BaseConfig, Config
from valjean.priority_set import PrioritySet

ID_CHARS = ascii_lowercase

# normalized IDs are stripped lowercase strings
IDS = text(ID_CHARS, min_size=1).map(lambda s: s.strip())

STANDARD_SECS = ['build/{}', 'checkout/{}', 'executable/{}', 'run/{}',
                 'other/{}']


###########################
#  Hypothesis strategies  #
###########################

@composite
def section_names(draw, sec_ids, with_slash=None):
    '''Hypothesis strategy to generate section names, with or without slash
    separator.'''
    if with_slash is None:
        min_size = 1
        max_size = 2
    elif with_slash:
        min_size = max_size = 2
    else:
        min_size = max_size = 1
    sec = draw(lists(sec_ids, min_size=min_size, max_size=max_size))
    return '/'.join(sec)


# pylint: disable=no-value-for-parameter
@composite
def baseconfig(draw, keys=IDS, vals=IDS, sec_names=section_names(IDS),
               min_size=None):
    '''Composite Hypothesis strategy to generate BaseConfig objects.'''
    secs = dictionaries(keys, vals)
    as_dict = draw(dictionaries(sec_names, secs, min_size=min_size))
    conf = BaseConfig.from_mapping(as_dict)
    return conf


@composite
def config(draw, keys=IDS, vals=IDS, sec_names=section_names(IDS),
           min_size=None):
    '''Composite Hypothesis strategy to generate Config objects.'''
    baseconf = draw(baseconfig(keys, vals, sec_names, min_size=min_size))
    conf = Config.from_mapping(baseconf)
    return conf


@composite
def config_with_sections(draw, section_templates):
    '''Composite Hypothesis strategy to generate Config objects with sections
    following the given templates.'''
    sec_ids = draw(lists(IDS, min_size=1))
    sec_names = []
    for sec_id in sec_ids:
        sec_family = draw(sampled_from(section_templates))
        sec_names.append(sec_family.format(sec_id))
    return draw(config(sec_names=sampled_from(sec_names)))


@composite
def spaces(draw):
    '''Generate strings of spaces.'''
    return draw(text(' '))


@composite
def priority_sets(draw, elements=text(), min_size=None, max_size=None):
    '''Strategy to generate :class:`PrioritySet` objects.'''
    items = draw(lists(tuples(integers(), elements),
                       min_size=min_size, max_size=max_size))
    prs = PrioritySet(items)
    return prs


#####################
#  pytest fixtures  #
#####################

@pytest.fixture(scope='function')
def empty_config():
    '''Return an empty :class:`~.Config` object.'''
    return Config([])


def foreach_data(*args, **kwargs):
    '''Decorator that parametrizes a test function over files in the data
    directory for the current tests.

    Assume that the following snippet resides in
    :file:`tests/submod/test_submod.py`::

        @foreach_data('datafile')
        def test_something(datafile):
            pass

    When `pytest` imports :file:`test_submod.py`, it will parametrize
    the `datafile` argument to :func:`test_something` over all the files
    present in :file:`tests/submod/data/`.

    If you wish to filter away some of the files, you can use the alternative
    syntax::

        @foreach_data(datafile=lambda path: str(path).endswith('.txt'))
        def test_something(datafile):
            pass

    Here the argument to the `datafile` keyword argument is a predicate that
    must return `True` if `path` is to be parametrized over, and `False`
    otherwise. Note that the `path` argument to the lambda is a
    :class:`py.path.local` object.  In this example, `pytest` will parametrize
    :func:`test_something` only over files whose name ends in '.txt'.
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
        import py
        from inspect import getfile
        module_dir = py.path.local(getfile(wrapped))
        test_dir = module_dir.dirpath('data')
        datafiles = [path for path in test_dir.listdir(fil=fil)
                     if path.isfile()]
        ids = [str(path.basename) for path in datafiles]
        return pytest.mark.parametrize(fix_name, datafiles, ids=ids)(wrapped)
    return _decorator
