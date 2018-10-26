# pylint: disable=redefined-outer-name,no-value-for-parameter

'''Tests for the :mod:`~.valjean.config` module.'''

from configparser import DuplicateSectionError, NoOptionError

import pytest
from hypothesis import given, note, settings, assume, HealthCheck
from hypothesis.strategies import data, lists

from .context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean import LOGGER
from valjean.config import Config

# pylint: disable=unused-import
from .conftest import (IDS, STANDARD_SECS, configs, spaces, section_names,
                       intercalate_strings)


###########
#  tests  #
###########

@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=configs())
def test_as_dict_roundtrip(conf):
    '''Test roundtrip with the as_dict method.'''
    dct = conf.as_dict(raw=True)
    reconf = Config.from_mapping(dct)
    note('conf={!r}'.format(conf))
    note('reconf={!r}'.format(reconf))
    assert conf == reconf


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=configs())
def test_equality_reflective(conf):
    '''Test that the == operator is reflective.'''
    note(conf.as_dict())
    # pylint: disable=comparison-with-itself
    assert conf == conf


@settings(suppress_health_check=(HealthCheck.too_slow,),
          deadline=None)
@given(conf=configs())
def test_merge_with_self(conf):
    '''Test that merging with `self` results in the identity.'''
    assert conf + conf == conf


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=configs())
def test_merge_with_empty(conf):
    '''Test that merging with the empty configuration is the identity.'''
    assert conf + Config() == conf


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf1=configs(), conf2=configs(), conf3=configs())
def test_merge_associative(conf1, conf2, conf3):
    '''Test that merging configurations is associative.'''
    assert (conf1 + conf2) + conf3 == conf1 + (conf2 + conf3)


@settings(deadline=None, suppress_health_check=(HealthCheck.too_slow,))
@given(conf1=configs(), conf2=configs())
def test_merge_all_sections(conf1, conf2):
    '''Test that merging all configuration sections is the same as merging
    the whole configuration.'''
    conf_merge = conf1 + conf2
    for sec in conf2.sections():
        LOGGER.debug('merging section %s', sec)
        conf1.merge_section(conf2, sec)
    note('conf1: {}'.format(conf1))
    note('conf_merge: {}'.format(conf_merge))
    assert conf1 == conf_merge


@given(sec=IDS, opt=IDS, val=IDS)
def test_set_in_section(sec, opt, val):
    '''Test that the set method correctly sets values.'''
    conf = Config(paths=[])
    conf.add_section(sec)
    conf.set(sec, opt, val)
    assert val == conf.get(sec, opt, raw=True)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=configs(), opt=IDS)
def test_get_with_fallback(conf, opt):
    '''Test that fallback values work for normal options.'''
    for sec in conf.sections():
        assume(not conf.has_option(sec, opt))
        val = conf.get(sec, opt, fallback=None)
        assert val is None


def test_read_config_file(tmpdir):
    '''Test reading from a config file.'''
    conf_str = ('[swallow african]\nspeed = 40\n\n'
                '[swallow   european]\nspeed = 55\n')
    conf_file = tmpdir.join('test.cfg')
    conf_file.write(conf_str)
    conf = Config([str(conf_file)])
    assert conf.get('swallow african', 'speed') == '40'
    assert conf.get('swallow european', 'speed') == '55'


########################################
#  tests that should raise exceptions  #
########################################

def test_compare_wrong_type_raises(empty_config):
    '''Test that comparing a config with another object type raises.'''
    assert not empty_config == 'Romani ite domum'


@settings(suppress_health_check=(HealthCheck.too_slow,),
          deadline=None)
@given(conf=configs(), sampler=data())
def test_duplicate_sections(conf, sampler):
    '''Test that section names which differ only in the amount of
    whitespace raise an exception.'''
    for section in conf.sections():
        split = section.split()
        n_spaces = len(split) + 1
        blanks = sampler.draw(lists(spaces(min_size=1),
                                    min_size=n_spaces, max_size=n_spaces))
        mod_section = intercalate_strings(blanks, split)
        with pytest.raises(DuplicateSectionError):
            conf.add_section(mod_section)
        assert conf.has_section(mod_section)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(conf=configs(), opt=IDS)
def test_get_missing_no_fallback(conf, opt):
    '''Test that get raises on missing options without fallback.'''
    for sec in conf.sections():
        assume(not conf.has_option(sec, opt))
        with pytest.raises(NoOptionError):
            conf.get(sec, opt)
