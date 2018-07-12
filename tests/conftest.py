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
