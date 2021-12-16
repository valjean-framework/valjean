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

''':class:`Config` objects encapsulate a set of configuration options for a
:mod:`valjean` run. Here is how you create one:

    >>> from valjean.config import Config
    >>> config = Config()

By default, :class:`Config` objects come with a ``'path'`` configuration
section, which may be used to set default values for any configuration option.
A few options are set from the beginning:

    >>> for opt, val in sorted(config['path'].items()):
    ...     print(f'{opt} = {val}')
    log-root = /.../log
    output-root = /.../output
    report-root = /.../report

The :class:`Config` class behaves like a simple dictionary:

    >>> print(config.query('path', 'report-root'))
    /.../report

Module API
----------
'''

from collections.abc import MutableMapping
from pathlib import Path
import toml


class Config(MutableMapping):
    '''The base configuration class for :mod:`valjean`.'''

    @classmethod
    def from_file(cls, path):
        '''Construct a configuration object from a TOML file.

        :param path: A path for the configuration file.
        :type path: pathlib.Path or str
        '''
        file_content = toml.load(str(path))
        return cls(file_content)

    def __init__(self, dictionary=None):
        '''Construct a configuration object from a dictionary.

        The configuration will be initialized to contain a few default options.

        :param dict dictionary: The configuration object.
        :returns: The constructed Config object.
        '''
        self.conf = dict(dictionary) if dictionary is not None else {}

        # sanity check
        if 'path' in self.conf and not isinstance(self.conf['path'], dict):
            raise ValueError('the "path" option is forbidden at the top level')

        # Set some default options
        if 'path' not in self:
            self['path'] = {}
        conf_path = self['path']
        work_dir = Path.cwd()
        if 'log-root' not in conf_path:
            conf_path['log-root'] = f'{work_dir}/log'
        if 'output-root' not in conf_path:
            conf_path['output-root'] = f'{work_dir}/output'
        if 'report-root' not in conf_path:
            conf_path['report-root'] = f'{work_dir}/report'

    def __getitem__(self, key):
        return self.conf[key]

    def __setitem__(self, key, value):
        self.conf[key] = value

    def __delitem__(self, key):
        del self.conf[key]

    def __iter__(self):
        yield from self.conf

    def __len__(self):
        return len(self.conf)

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        return self.conf == other.conf

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return toml.dumps(self.conf)

    def __repr__(self):
        return f'Config({self.conf})'

    def query(self, section, option):
        '''Return the value of `option` from `section`.'''
        return self.conf[section][option]

    def set(self, section, option, value):
        '''Set the value of `option` in `section` to be `value`.'''
        self.conf[section][option] = value
