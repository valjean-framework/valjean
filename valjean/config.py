''':class:`Config` objects encapsulate a set of configuration options for a
:mod:`valjean` run. Here is how you create one:

    >>> from valjean.config import Config
    >>> config = Config()

By default, :class:`Config` objects come with a ``'path'`` configuration
section, which may be used to set default values for any configuration option.
A few options are set from the beginning:

    >>> for opt, val in sorted(config['path'].items()):
    ...     print('{} = {}'.format(opt, val))
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
            conf_path['log-root'] = '{}/log'.format(work_dir)
        if 'output-root' not in conf_path:
            conf_path['output-root'] = '{}/output'.format(work_dir)
        if 'report-root' not in conf_path:
            conf_path['report-root'] = '{}/report'.format(work_dir)

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
        return 'Config({})'.format(self.conf)

    def query(self, section, option):
        '''Return the value of `option` from `section`.'''
        return self.conf[section][option]

    def set(self, section, option, value):
        '''Set the value of `option` in `section` to be `value`.'''
        self.conf[section][option] = value
