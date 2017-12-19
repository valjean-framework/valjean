#!/usr/bin/env python3

from hypothesis import given, note, settings, HealthCheck, event, assume
from hypothesis.strategies import (text, dictionaries, composite, sampled_from,
                                   lists)
from string import ascii_letters
from configparser import ParsingError
import tempfile
import pytest

from .context import valjean  # noqa: F401
from valjean.config import Config, DuplicateSectionError


ID_CHARS = ascii_letters
ids = text(ID_CHARS, min_size=1)


@composite
def sec_names(draw, sec_ids):
    '''Hypothesis strategy to generate section names, with or without slash
    separator.'''
    sec = draw(lists(sec_ids, min_size=1, max_size=2))
    return '/'.join(sec)


@composite
def config(draw, keys=ids, vals=ids, sec_names=sec_names(ids)):
    '''Composite Hypothesis strategy to generate Config objects.'''
    secs = dictionaries(keys, vals, min_size=2)
    as_dict = draw(dictionaries(sec_names, secs, min_size=2))
    conf = Config(paths=[])
    for sec, opts in as_dict.items():
        ssec = sec.strip()
        conf.add_section(ssec)
        for opt, val in opts.items():
            conf.set(ssec, opt.strip(), val.strip())
    return conf


@composite
def config_with_sections(draw, section_templates):
    '''Composite Hypothesis strategy to generate Config objects with sections
    following the given templates.'''
    sec_ids = draw(lists(ids, min_size=1))
    sec_names = []
    for sec_id in sec_ids:
        sec_family = draw(sampled_from(section_templates))
        sec_names.append(sec_family.format(sec_id))
    return draw(config(sec_names=sampled_from(sec_names)))


class TestConfig:
    @settings(max_examples=20)
    @given(conf=config())
    def test_write_read_roundtrip(self, conf):
        with tempfile.NamedTemporaryFile() as conf_file:
            conf.write(conf_file)
            conf_file.seek(0)
            try:
                conf_reread = Config(paths=[conf_file.name])
            except ParsingError:
                conf_file.seek(0)
                note(conf_file.read())
                note(conf.as_dict())
                raise
            try:
                assert conf_reread == conf
            except AssertionError:
                conf_file.seek(0)
                note(conf_file.read())
                note(conf.as_dict())
                note(conf_reread.as_dict())
                raise

    @given(conf=config())
    def test_as_dict_roundtrip(self, conf):
        '''Test roundtrip with the as_dict method.'''
        dct = conf.as_dict()
        reconf = Config.from_mapping(dct)
        note('conf={!r}'.format(conf))
        note('reconf={!r}'.format(reconf))
        assert conf == reconf

    @settings(suppress_health_check=(HealthCheck.too_slow,))
    @given(conf=config())
    def test_merge_with_self_is_identity(self, conf):
        '''Test that merging with `self` results in the identity.'''
        assert conf + conf == conf

    @given(conf=config())
    def test_merge_with_empty_is_identity(self, conf):
        '''Test that merging with the empty configuration is the identity.'''
        assert conf + Config(paths=[]) == conf

    @settings(suppress_health_check=(HealthCheck.too_slow,))
    @given(conf1=config(), conf2=config(), conf3=config())
    def test_merge_associative(self, conf1, conf2, conf3):
        '''Test that merging configurations is associative.'''
        assert (conf1 + conf2) + conf3 == conf1 + (conf2 + conf3)

    @settings(suppress_health_check=(HealthCheck.too_slow,))
    @given(conf1=config(), conf2=config())
    def test_merge_all_sections_same_as_merge(self, conf1, conf2):
        '''Test that merging all configuration sections is the same as merging
        the whole configuration.'''
        conf_merge = conf1 + conf2
        conf_copy = Config(paths=[]).merge(conf1)
        for sec in conf2.sections():
            conf_copy.merge_section(conf2, sec)
        assert conf_merge == conf_copy

    @given(conf=config_with_sections(['build/{}', 'checkout/{}', 'other/{}']))
    def test_get_special_does_not_raise(self, conf):
        '''Test that "special" options do not raise exceptions when queried.'''
        for sec in conf.sections():
            sec_family, sec_id = conf.split_section(sec)
            for opt, val in conf.SPECIAL_OPTS.items():
                if sec_family in val[0]:
                    conf.get(sec, opt)

    @given(conf=config())
    def test_split_section_by_family_and_id(self, conf):
        n_sections = 0
        for section in conf.sections():
            note('section = {}'.format(section))
            split = conf.split_section(section)
            if len(split)==1:
                continue
            note('split = {}'.format(split))
            n_sections += 1
            rec_section = conf.section_by_family(*split)
            assert rec_section[0].name == section
        if n_sections < 3:
            event('tested {} sections'.format(n_sections))
        else:
            event('tested > 3 sections')



class TestConfigFailure:

    @given(conf=config())
    def test_duplicate_sections_raises(self, conf):
        '''Test that duplicate section names raise an exception.'''
        for section in conf.sections():
            with pytest.raises(DuplicateSectionError):
                conf.add_section(section)

    @given(conf=config(),
           spaces_before=text([' '], average_size=2),
           spaces_in1=text([' '], average_size=2),
           spaces_in2=text([' '], average_size=2),
           spaces_after=text([' '], average_size=2)
           )
    def test_almost_duplicate_sections_raises(self, conf,
                                              spaces_before, spaces_in1,
                                              spaces_in2, spaces_after):
        '''Test that section names which differ only in the amount of
        whitespace raise an exception.'''
        for section in conf.sections():
            split = conf.split_section(section)
            if len(split)>1:
                event("'/' in section name")
                mod_section = ''.join([spaces_before, split[0], spaces_in1,
                                       '/', spaces_in2, split[1],
                                       spaces_after])
            else:
                event("no '/' in section name")
                mod_section = ''.join([spaces_before, section, spaces_after])
            with pytest.raises(DuplicateSectionError):
                conf.add_section(mod_section)
