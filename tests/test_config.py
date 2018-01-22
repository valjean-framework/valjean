#!/usr/bin/env python3
# pylint: disable=redefined-outer-name,no-value-for-parameter

'''Tests for the :mod:`~.valjean.config` module.'''

from string import ascii_letters
from configparser import (DuplicateSectionError, NoOptionError, NoSectionError,
                          InterpolationMissingOptionError)
from collections import Counter, defaultdict
from itertools import chain
import os

import pytest
from hypothesis import given, note, settings, HealthCheck, event, assume
from hypothesis.strategies import (text, dictionaries, composite, sampled_from,
                                   lists)

from .context import valjean  # noqa: F401, pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.config import BaseConfig, Config


ID_CHARS = ascii_letters
IDS = text(ID_CHARS, min_size=1)

STANDARD_SECS = ['build/{}', 'checkout/{}', 'executable/{}', 'run/{}',
                 'other/{}']


###########################
#  Hypothesis strategies  #
###########################

@settings(suppress_health_check=(HealthCheck.too_slow,))
@composite
def sec_names(draw, sec_ids):
    '''Hypothesis strategy to generate section names, with or without slash
    separator.'''
    sec = draw(lists(sec_ids, min_size=1, max_size=2))
    return '/'.join(sec)


@composite
def baseconfig(draw, keys=IDS, vals=IDS, sec_names=sec_names(IDS)):
    '''Composite Hypothesis strategy to generate BaseConfig objects.'''
    secs = dictionaries(keys, vals, min_size=2)
    as_dict = draw(dictionaries(sec_names, secs, min_size=2))
    conf = BaseConfig()
    for sec, opts in as_dict.items():
        ssec = sec.strip()
        conf.add_section(ssec)
        for opt, val in opts.items():
            conf.set(ssec, opt.strip(), val.strip())
    return conf


@composite
def config(draw, keys=IDS, vals=IDS, sec_names=sec_names(IDS)):
    '''Composite Hypothesis strategy to generate Config objects.'''
    baseconf = draw(baseconfig(keys, vals, sec_names))
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


#####################
#  pytest fixtures  #
#####################

@pytest.fixture(scope='function')
def empty_config():
    '''Return an empty :class:`~.Config` object.'''
    return Config([])


###########
#  tests  #
###########

@given(conf=baseconfig())
def test_as_dict_roundtrip(conf):
    '''Test roundtrip with the as_dict method.'''
    dct = conf.as_dict(raw=True)
    reconf = BaseConfig.from_mapping(dct)
    note('conf={!r}'.format(conf))
    note('reconf={!r}'.format(reconf))
    assert conf == reconf


@given(conf=baseconfig())
def test_equality_reflective(conf):
    '''Test that the == operator is reflective.'''
    note(conf.as_dict())
    assert conf == conf


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=baseconfig())
def test_merge_with_self(conf):
    '''Test that merging with `self` results in the identity.'''
    assert conf + conf == conf


@given(conf=baseconfig())
def test_merge_with_empty(conf):
    '''Test that merging with the empty configuration is the identity.'''
    assert conf + BaseConfig() == conf


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf1=baseconfig(), conf2=baseconfig(), conf3=baseconfig())
def test_merge_associative(conf1, conf2, conf3):
    '''Test that merging configurations is associative.'''
    assert (conf1 + conf2) + conf3 == conf1 + (conf2 + conf3)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf1=baseconfig(), conf2=baseconfig())
def test_merge_all_sections(conf1, conf2):
    '''Test that merging all configuration sections is the same as merging
    the whole configuration.'''
    conf_merge = conf1 + conf2
    conf_copy = BaseConfig().merge(conf1)
    for sec in conf2.sections():
        conf_copy.merge_section(conf2, sec)
    assert conf_merge == conf_copy


@given(conf=baseconfig())
def test_split_section_by_family(conf):
    '''Test that :meth:`~.BaseConfig.sections_by_family` does not skip any
    section.'''
    family_counter = Counter()
    no_family = 0
    n_sections = 0
    for section in conf.sections():
        n_sections += 1
        split = conf.split_section(section)
        if len(split) == 1:
            no_family += 1
            continue
        note('section = {}'.format(section))
        note('split = {}'.format(split))
        family_counter[split[0]] += 1

    event('sections with a family: {}'.format(n_sections - no_family))

    for family, count in family_counter.items():
        assert (len(list(conf.sections_by_family(family)))
                == count)
    assert (len(list(conf.sections()))
            == sum(family_counter.values()) + no_family)


@given(sec=IDS, opt=IDS, val=IDS)
def test_set_in_section_no_slash(sec, opt, val):
    '''Test that the set method correctly sets values.'''
    conf = BaseConfig(paths=[])
    conf.add_section(sec)
    conf.set(sec, opt, val)
    assert val == conf.get(sec, opt, raw=True)


@given(sec_fam=IDS, sec_id=IDS, opt=IDS, val=IDS)
def test_set_in_section_with_slash(sec_fam, sec_id, opt, val):
    '''Test that the set method correctly sets values.'''
    conf = BaseConfig(paths=[])
    sec = '/'.join((sec_fam, sec_id))
    conf.add_section(sec)
    conf.set(sec_fam, sec_id, opt, val)
    assert val == conf.get(sec_fam, sec_id, opt, raw=True)


@given(conf=baseconfig(), opt=IDS)
def test_get_with_fallback(conf, opt):
    '''Test that fallback values work for normal options.'''
    for sec in conf.sections():
        assume(not conf.has_option(sec, opt))
        val = conf.get(sec, opt, fallback=None)
        assert val is None


def test_read_config_file(tmpdir):
    '''Test reading from a config file.'''
    conf_str = ('[swallow/african]\nspeed = 40\n\n'
                '[swallow/european]\nspeed = 55\n')
    conf_file = tmpdir.join('test.cfg')
    conf_file.write(conf_str)
    conf = BaseConfig([str(conf_file)])
    assert conf.get('swallow', 'african', 'speed') == '40'
    assert conf.get('swallow', 'european', 'speed') == '55'


####################################################
#  Specific tests for the :class:`~.Config` class  #
####################################################

TOTAL_HANDLERS = defaultdict(tuple, {
    'build': ('build-dir',),
    'checkout': ('checkout-dir',)
    })

PARTIAL_HANDLERS = defaultdict(tuple, {
    'run': ('args',)
    })


def test_handlers_exist():
    '''Test that handlers are correctly installed for the options in
    TOTAL_HANDLERS and PARTIAL_HANDLERS.'''
    conf = Config(paths=[])
    handlers = chain(TOTAL_HANDLERS.items(),
                     PARTIAL_HANDLERS.items())
    for family, opts in handlers:
        for opt in opts:
            assert conf.has_option_handler(family, opt)


@given(conf=config_with_sections(STANDARD_SECS))
def test_get_handler_with_fallback(conf):
    '''Test that options with handlers override fallback values.'''
    for sec in conf.sections():
        sec_family, _ = conf.split_section(sec)
        for opt in TOTAL_HANDLERS[sec_family]:
            val = conf.get(sec, opt, fallback=None)
            assert val is not None


def test_lookup_other():
    '''Test that values are correctly handled by
    :class:`~.LookupOtherHandler`.
    '''
    conf = Config(paths=[])
    conf.add_section('checkout/spam')
    conf.add_section('build/spam')
    assert conf.has_option_handler('checkout', 'checkout-dir')
    assert (conf.get('checkout', 'spam', 'checkout-dir', raw=True) ==
            os.path.join('${work-dir}/checkout', 'spam'))
    assert conf.has_option_handler('build', 'build-dir')
    assert (conf.get('build', 'spam', 'build-dir', raw=True) ==
            os.path.join('${work-dir}/build', 'spam'))


def test_lookup_section_from_opt():
    '''Test that values can be correctly handled and interpolated by the
    :class:`~.LookupSectionFromOptHandler` handler.'''
    conf = Config(paths=[])
    conf.add_section('executable/spam')
    conf.set('executable', 'spam', 'path', '/path/to/spam')
    conf.set('executable', 'spam', 'args', '${input}')
    conf.add_section('run/spam the eggs')
    conf.set('run', 'spam the eggs', 'executable', 'spam')
    conf.set('run', 'spam the eggs', 'input', 'foo')
    assert conf.get('executable', 'spam', 'args', raw=True) == '${input}'
    with pytest.raises(InterpolationMissingOptionError):
        conf.get('executable', 'spam', 'args')
    assert conf.get('run', 'spam the eggs', 'args', raw=True) == '${input}'
    assert conf.get('run', 'spam the eggs', 'args') == 'foo'


########################################
#  tests that should raise exceptions  #
########################################

def test_compare_wrong_type_raises(empty_config):
    '''Test that comparing a config with another object type raises.'''
    assert not empty_config == 'Romani ite domum'


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=baseconfig(),
       spaces_before=text([' '], average_size=2),
       spaces_in1=text([' '], average_size=2),
       spaces_in2=text([' '], average_size=2),
       spaces_after=text([' '], average_size=2))
def test_duplicate_sections(conf, spaces_before, spaces_in1, spaces_in2,
                            spaces_after):
    '''Test that section names which differ only in the amount of
    whitespace raise an exception.'''
    for section in conf.sections():
        split = conf.split_section(section)
        if len(split) > 1:
            event("'/' in section name")
            mod_section = ''.join([spaces_before, split[0], spaces_in1,
                                   '/', spaces_in2, split[1],
                                   spaces_after])
        else:
            event("no '/' in section name")
            mod_section = ''.join([spaces_before, section, spaces_after])
        with pytest.raises(DuplicateSectionError):
            conf.add_section(mod_section)


def test_get_wrong_arg_number(empty_config):
    '''Test that :meth:`~.Config.get` cannot be called with less than 2 or
    more than 3 arguments.'''
    with pytest.raises(ValueError):
        empty_config.get('first')
    with pytest.raises(ValueError):
        empty_config.get('first', 'second', 'third', 'fourth')


def test_set_wrong_arg_number(empty_config):
    '''Test that :meth:`~.Config.set` cannot be called with less than 3 or
    more than 4 arguments.'''
    with pytest.raises(ValueError):
        empty_config.set('first')
    with pytest.raises(ValueError):
        empty_config.set('first', 'second')
    with pytest.raises(ValueError):
        empty_config.set('first', 'second', 'third', 'fourth', 'fifth')


@given(conf=baseconfig(), opt=IDS)
def test_get_missing_no_fallback(conf, opt):
    '''Test that get raises on missing options without fallback.'''
    for sec in conf.sections():
        assume(not conf.has_option(sec, opt))
        with pytest.raises(NoOptionError):
            conf.get(sec, opt)


@given(conf=baseconfig(), missing=IDS)
def test_missing_section_by_family(conf, missing):
    '''Test that get raises on missing options without fallback.'''
    assume(all(conf.split_section(sec)[0] != missing
               for sec in conf.sections()))
    LOGGER.debug('sections = %s', list(conf.sections()))
    LOGGER.debug('missing = %s', missing)
    with pytest.raises(NoSectionError):
        conf.section_by_family(missing)
