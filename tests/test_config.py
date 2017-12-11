#!/usr/bin/env python3

from hypothesis import given, note, settings
from hypothesis.strategies import text, dictionaries, composite, sampled_from
from string import ascii_letters
from configparser import ParsingError
import tempfile

from .context import valjean  # noqa: F401
from valjean.config import Config


ID_CHARS = ascii_letters


@composite
def config(draw):
    '''Composite Hypothesis strategy to generate Config objects.'''
    key_strat = text(sampled_from(ID_CHARS), min_size=1)
    val_strat = text(sampled_from(ID_CHARS), min_size=1)
    sec_strat = dictionaries(key_strat, val_strat, min_size=2)
    as_dict = draw(dictionaries(key_strat, sec_strat, min_size=2))
    conf = Config(paths=[])
    for sec, opts in as_dict.items():
        ssec = sec.strip()
        conf.add_section(ssec)
        for opt, val in opts.items():
            conf.set(ssec, opt.strip(), val.strip())
    return conf


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

    @given(conf=config())
    def test_merge_with_self_is_identity(self, conf):
        '''Test that merging with `self` results in the identity.'''
        assert conf + conf == conf

    @given(conf=config())
    def test_merge_with_empty_is_identity(self, conf):
        '''Test that merging with the empty configuration is the identity.'''
        assert conf + Config(paths=[]) == conf

    @given(conf1=config(), conf2=config(), conf3=config())
    def test_merge_associative(self, conf1, conf2, conf3):
        '''Test that merging configurations is associative.'''
        assert (conf1 + conf2) + conf3 == conf1 + (conf2 + conf3)
