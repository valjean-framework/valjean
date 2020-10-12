# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`~.valjean.config` module.'''

from hypothesis import given, note

from .context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.config import Config

# pylint: disable=unused-import
from .conftest import IDS, configs


###########
#  tests  #
###########

@given(conf=configs())
def test_copy_roundtrip(conf):
    '''Test roundtrip (i.e. copy).'''
    reconf = Config(conf)
    note('conf={!r}'.format(conf))
    note('reconf={!r}'.format(reconf))
    note('reconf.conf={!r}'.format(reconf.conf))
    assert conf == reconf


@given(conf=configs())
def test_file_roundtrip(conf, tmp_path):
    '''Test roundtrip to file.'''
    conf_file = tmp_path / 'conf.toml'
    conf_file.write_text(str(conf))
    reconf = Config.from_file(str(conf_file))
    note('conf={!r}'.format(conf))
    note('reconf={!r}'.format(reconf))
    assert conf == reconf


@given(conf=configs())
def test_equality_reflective(conf):
    '''Test that the == operator is reflective.'''
    note(conf)
    # pylint: disable=comparison-with-itself
    assert conf == conf


def test_read_config_file(tmp_path):
    '''Test reading from a config file.'''
    conf_str = ('["African swallow"]\nspeed = 40\n\n'
                '["European swallow"]\nspeed = 55\n')
    conf_file = tmp_path / 'test.toml'
    conf_file.write_text(conf_str)
    conf = Config.from_file(str(conf_file))
    expected = Config({'African swallow': {'speed': 40},
                       'European swallow': {'speed': 55}})
    assert conf == expected


########################################
#  tests that should raise exceptions  #
########################################

def test_compare_wrong_type_raises(empty_config):
    '''Test that comparing a config with another object type raises.'''
    assert not empty_config == 'Romani ite domum'
