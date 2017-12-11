'''Module containing the configuration class for the :mod:`valjean` package.

:class:`Config` objects encapsulate a set of configuration options for a
:mod:`valjean` run. Here is how you create one:

.. testsetup:: config

    from valjean.config import Config

.. doctest:: config

    >>> config = Config()

The :class:`Config` constructor will look for the following configuration
files, and read them in order if they exist:

    * :file:`$HOME/.valjeanrc`
    * :file:`valjeanrc` (in the current directory)

The :file:`$HOME/.valjeanrc` file is useful for setting user defaults. The
:file:`valjeanrc` file is where you should write the configuration for your
current test run.

If you want to read other files on object creation instead, you can pass them
using the ``paths`` argument:

.. doctest:: config

    >>> config = Config(paths=['valjean.conf'])

The default files are in the :data:`Config.DEFAULT_CONFIG_FILES` class
attribute, so you can do

.. doctest:: config

    >>> config = Config(paths=Config.DEFAULT_CONFIG_FILES + ['valjean.conf'])

to read the default files *and* :file:`valjean.conf`.

If you don't want to read any files (useful for testing), just pass an empty
list:

.. doctest:: config

    >>> config = Config(paths=[])

By default, :class:`Config` objects come with a few default options set:

.. doctest:: config

    >>> for opt, val in config['core'].items():
    ...     print('{} = {}'.format(opt, val))
    work-dir = .
    log-dir = ./log
    checkout-dir = ./checkout
    build-dir = ./build
    run-dir = ./run
    test-dir = ./test
    report-dir = ./report

The :class:`Config` class inherits from :class:`configparser.ConfigParser`, and
as such can be accessed and modified using all the methods of its parent class:

.. doctest:: config

    >>> print(config['core']['build-dir'])
    ./build
    >>> list(config.sections())
    ['core']
    >>> # value interpolation is possible
    >>> config['core']['log-dir'] = '${work-dir}/log_dir'
    >>> print(config['core']['log-dir'])
    ./log_dir

It also provides some additional convenience methods:

.. doctest:: config

    >>> from pprint import pprint
    >>> # convert the configuration to an ordered dictionary
    >>> pprint(config.as_dict())
    {'core': {'work-dir': '.',
              'log-dir': './log_dir',
              'checkout-dir': './checkout',
              'build-dir': './build',
              'run-dir': './run',
              'test-dir': './test',
              'report-dir': './report'}}
    >>> # merge two configuration objects
    >>> # options from the second configuration take precedence
    >>> other_config = Config(paths=[])
    >>> other_config['core']['report-dir'] = '${work-dir}/html'
    >>> other_config['core']['extra-option'] = 'definitely!'
    >>> config += other_config
    >>> print(config['core']['report-dir'])
    ./html
    >>> print(config['core']['extra-option'])
    definitely!
'''

from configparser import ConfigParser, ExtendedInterpolation, DEFAULTSECT
from collections import OrderedDict
import os


class Config(ConfigParser):
    '''The configuration class for :mod:`valjean`. It derives from
    :class:`configparser.ConfigParser`, so all of the methods of the base class
    can also be used with this one.
    '''

    def __init__(self, paths=None):
        '''Construct a configuration object.

        :param paths: A list of paths for configuration files. If this is
                      `None`, :class:`Config` will search the following paths,
                      and read in the files in order if they exist:

                        * :file:`$HOME/.valjeanrc`
                        * :file:`valjeanrc` in the current directory

                      If you want to disable this behaviour, use an empty list.
                      If you want to read the default files **and** some
                      additional ones, the default files are available as
                      ``Config.DEFAULT_CONFIG_FILES``.
        :type paths: list or None
        '''

        if paths is None:
            paths = self.DEFAULT_CONFIG_FILES

        super().__init__(interpolation=ExtendedInterpolation(),
                         delimiters=('=',),
                         comment_prefixes=('#',))

        def_dict = OrderedDict(
            (sec, OrderedDict(
                (opt, default) for (opt, (_, default)) in opts.items()
                ))
            for sec, opts in self._KNOWN_OPTIONS.items()
            )
        self.read_dict(def_dict)
        self.read([os.path.expanduser(p) for p in paths])

    @classmethod
    def from_mapping(cls, mapping):
        '''Construct a configuration object from an option mapping.

        The keys of `mapping` must be strings; its values must be string ->
        string mappings. Note that `mapping` may also be a :class:`Config`
        object (in which case this method acts as a copy).

        :param mapping mapping: The mapping for initialization.
        :returns: The constructed Config object.
        '''
        new = cls()
        new.merge(mapping)
        return new

    # pylint: disable=arguments-differ
    def write(self, f_obj, space_around_delimiters=True):
        '''Write the configuration to the given file object.'''

        dlm = ' ' if space_around_delimiters else ''
        for sec, opts in self.items():
            if not opts:
                continue
            f_obj.write('[{}]\n'.format(sec).encode('utf-8'))
            known_sec = self._KNOWN_OPTIONS.get(sec, dict())
            for opt, value in opts.items():
                desc, _ = known_sec.get(opt, (None, ''))
                if desc is not None:
                    f_obj.write('# {desc}\n'.format(desc=desc).encode('utf-8'))
                f_obj.write('{opt}{dlm}={dlm}{value}\n\n'
                            .format(opt=opt, value=value, dlm=dlm)
                            .encode('utf-8'))

    def as_dict(self):
        '''Convert the object to a dictionary.'''
        dct = OrderedDict()
        for sec, opts in self.items():
            if sec == DEFAULTSECT:
                continue
            sec_dct = OrderedDict()
            for opt, val in opts.items():
                sec_dct[opt] = val
            dct[sec] = sec_dct
        return dct

    def merge(self, other):
        '''In-place merge two configurations. Options from the `other`
        configuration supersede those from `self`.

        :param Config other: The configuration to merge into `self`.
        :returns: The modified configuration.
        '''
        for sec, opts in other.items():
            if sec == DEFAULTSECT:
                continue
            if not self.has_section(sec):
                self.add_section(sec)
            for opt, val in opts.items():
                self.set(sec, opt, val)
        return self

    __iadd__ = merge

    def __add__(self, other):
        '''Merge two configurations, return the result as a new object.'''
        return Config.from_mapping(self).merge(other)

    __radd__ = __add__

    # Dictionary containing the known options, their descriptions and default
    # values.
    _KNOWN_OPTIONS = OrderedDict()
    _KNOWN_OPTIONS['core'] = OrderedDict()
    _KNOWN_OPTIONS['core']['work-dir'] = ('path to the working directory', '.')
    _KNOWN_OPTIONS['core']['log-dir'] = ('path to the directory for log files',
                                         '${work-dir}/log')
    _KNOWN_OPTIONS['core']['checkout-dir'] = (
        'path to the directory for code sources',
        '${work-dir}/checkout'
        )
    _KNOWN_OPTIONS['core']['build-dir'] = (
        'path to the directory for code compilation', '${work-dir}/build'
        )
    _KNOWN_OPTIONS['core']['run-dir'] = (
        'path to the directory for code execution',
        '${work-dir}/run'
        )
    _KNOWN_OPTIONS['core']['test-dir'] = (
        'path to the directory for test execution',
        '${work-dir}/test'
        )
    _KNOWN_OPTIONS['core']['report-dir'] = (
        'path to the directory for report generation',
        '${work-dir}/report'
        )

    #: Default configuration file paths.
    DEFAULT_CONFIG_FILES = ['~/.valjeanrc', 'valjeanrc']
