# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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
def test_file_roundtrip(conf, tmp_path_factory):
    '''Test roundtrip to file.'''
    tmp_path = tmp_path_factory.mktemp('test_file_roundtrip')
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
