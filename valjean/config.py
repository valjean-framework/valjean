''':class:`Config` objects encapsulate a set of configuration options for a
:mod:`valjean` run. Here is how you create one:

    >>> from valjean.config import Config
    >>> config = Config()

The :class:`Config` constructor will look for the following configuration
files, and read them in order if they exist:

    * :file:`$HOME/.valjean.cfg`
    * :file:`valjean.cfg` (in the current directory)

The :file:`$HOME/.valjean.cfg` file is useful for setting user defaults. The
:file:`valjean.cfg` file is where you should write the configuration for your
current test run.

If you want to read other files on object creation instead, you can pass them
using the ``paths`` argument:

    >>> config = Config(paths=['valjean.conf'])

The default files are in the :data:`Config.DEFAULT_CONFIG_FILES` class
attribute, so you can do

    >>> config = Config(paths=list(Config.DEFAULT_CONFIG_FILES)
    ...                 + ['valjean.conf'])

to read the default files *and* :file:`valjean.conf`.

If you don't want to read any files (useful for testing), just pass an empty
list:

    >>> config = Config(paths=[])

By default, :class:`Config` objects come with a ``'path'`` configuration
section, which may be used to set default values for any configuration option.
A few options are set from the beginning:

    >>> for opt, val in config.items('path', raw=True):
    ...     print('{} = {}'.format(opt, val))
    work-dir = /...
    log-root = ${work-dir}/log
    checkout-root = ${work-dir}/checkout
    build-root = ${work-dir}/build
    run-root = ${work-dir}/run
    test-root = ${work-dir}/test
    report-root = ${work-dir}/report
    job-file = ${work-dir}/job.py

The :class:`Config` class provides getters and setters:

    >>> print(config.get('path', 'build-root'))
    /.../build

    # value interpolation is possible
    >>> config.set('path', 'log-root', '${work-dir}/log_dir')
    >>> print(config.get('path', 'log-root'))
    /.../log_dir

It also provides some additional convenience methods:

    >>> from pprint import pprint

    # convert the configuration to a dictionary
    # the as_dict method actually returns an OrderedDict
    >>> for sec_name, section in config.as_dict(raw=True).items():
    ...   for option, value in section.items():
    ...     print('{}.{}: {}'.format(sec_name, option, value))
    path.work-dir: /...
    path.log-root: ${work-dir}/log_dir
    path.checkout-root: ${work-dir}/checkout
    path.build-root: ${work-dir}/build
    path.run-root: ${work-dir}/run
    path.test-root: ${work-dir}/test
    path.report-root: ${work-dir}/report
    path.job-file: ${work-dir}/job.py

    # merge two configuration objects; options from the second
    # configuration override those from the first one
    >>> other_config = Config(paths=[])
    >>> other_config.set('path', 'report-root', '${work-dir}/html')
    >>> other_config.set('path', 'extra-option', 'definitely!')
    >>> config += other_config
    >>> print(config.get('path', 'report-root'))
    /.../html
    >>> print(config.get('path', 'extra-option'))
    definitely!


Automatic dependency discovery
------------------------------

.. todo:: Document it. Perhaps refactor it somewhere else?


Module API
----------
'''

from configparser import ConfigParser, ExtendedInterpolation, _UNSET
from collections import OrderedDict
import os
import re

from . import LOGGER


class Config:
    '''The base configuration class for :mod:`valjean`.'''

    #: Default configuration file paths.
    DEFAULT_CONFIG_FILES = ('~/.valjean.cfg', 'valjean.cfg')

    def __init__(self, paths=None):
        '''Construct a configuration object.

        :param paths: An iterable of paths for configuration files. If this is
                      `None`, :class:`Config` will search the following paths,
                      and read in the files in order if they exist:

                        * :file:`$HOME/.valjean.cfg`
                        * :file:`valjean.cfg` in the current directory

                      If you want to disable this behaviour, use an empty list.
                      If you want to read the default files **and** some
                      additional ones, the default files are available as
                      ``Config.DEFAULT_CONFIG_FILES``.
        :type paths: :term:`iterable` or None
        '''

        self._conf = ConfigParser(interpolation=ExtendedInterpolation(),
                                  delimiters=('=',),
                                  comment_prefixes=('#',),
                                  empty_lines_in_values=False,
                                  default_section='path')
        # skip leading and trailing spaces in section names
        self._conf.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")

        # Set some default options
        self.set('path', 'work-dir', os.path.realpath(os.getcwd()))
        self.set('path', 'log-root', '${work-dir}/log')
        self.set('path', 'checkout-root', '${work-dir}/checkout')
        self.set('path', 'build-root', '${work-dir}/build')
        self.set('path', 'run-root', '${work-dir}/run')
        self.set('path', 'test-root', '${work-dir}/test')
        self.set('path', 'report-root', '${work-dir}/report')
        self.set('path', 'job-file', '${work-dir}/job.py')

        if paths is None:
            paths = self.DEFAULT_CONFIG_FILES

        other_conf = ConfigParser(default_section='path')
        other_conf.read([os.path.expanduser(p) for p in paths])
        for sec_name, _ in other_conf.items():
            if (not self.has_section(sec_name) and
                    sec_name != self._conf.default_section):
                self.add_section(sec_name)
            for opt, val in other_conf.items(sec_name, raw=True):
                self.set(sec_name, opt, val)

    @classmethod
    def from_mapping(cls, mapping):
        '''Construct a configuration object from an option mapping.

        The keys of `mapping` must be strings; its values must be string →
        string mappings. Note that `mapping` may also be a :class:`Config`
        or :class:`Config` object (in which case this method acts as a copy).

        :param mapping: The mapping for initialization.
        :type mapping: :term:`mapping`
        :returns: The constructed Config object.
        '''
        new = cls(paths=[])
        normalized_mapping = {cls.normalize_section(sec): opts
                              for sec, opts in mapping.items()}
        new.merge(normalized_mapping)
        return new

    @classmethod
    def normalize_section(cls, section):
        '''Normalize a section name by removing repeated spaces.'''
        sec_split = section.split()
        return ' '.join(w for w in sec_split)

    def add_section(self, section):
        '''Add a configuration section.'''
        xsection = self.normalize_section(section)
        self._conf.add_section(xsection)

    def remove_section(self, section):
        '''Remove a configuration section.'''
        xsection = self.normalize_section(section)
        self._conf.remove_section(xsection)

    def has_section(self, section):
        '''Check if a configuration section exists.'''
        xsection = self.normalize_section(section)
        return self._conf.has_section(xsection)

    def sections(self):
        '''Yield the configuration sections, excluding ``'path'``.'''
        yield from self._conf.sections()

    def remove_option(self, section, option):
        '''Remove an option from a section.'''
        xsection = self.normalize_section(section)
        self._conf.remove_option(xsection, option)

    def has_option(self, section, option):
        '''Check if a configuration option exists.'''
        xsection = self.normalize_section(section)
        return self._conf.has_option(xsection, option)

    # pylint: disable=redefined-builtin,too-many-arguments
    def get(self, section, option, raw=False, vars=None, fallback=_UNSET):
        '''get(section, option, raw=False, fallback)

        Get the value of an option.

        :param str section: The name of the section.
        :param str option: The name of the option.
        :param bool raw: If `True`, interpolate any ``${section:option}``
                         strings in the value with the value of the
                         corresponding option (see
                         :class:`configparser.ExtendedInterpolation` for more
                         information).
        :param vars: An option/value dictionary that will be looked up before
                     the configuration itself, or `None` if not needed.
        :type vars: :term:`mapping` or None
        :param fallback: A value to return if the option cannot be found.
        '''
        xsection = self.normalize_section(section)
        return self._conf.get(xsection, option,
                              raw=raw, vars=vars, fallback=fallback)

    def set(self, section, option, value):
        '''Set the value of an option.'''
        xsection = self.normalize_section(section)
        self._conf.set(xsection, option, value)

    def as_dict(self, *, raw=False):
        '''Convert the object to a dictionary.'''
        dct = OrderedDict()
        for sec_name, _ in self._conf.items():
            sec_dct = OrderedDict()
            for opt, val in self.items(sec_name, raw=raw):
                sec_dct[opt] = val
            dct[sec_name] = sec_dct
        return dct

    def merge(self, other):
        '''In-place merge two configurations. Options from the `other`
        configuration override those from `self`.

        :param Config other: The configuration to merge into `self`.
        :returns: The modified configuration.
        '''
        self._conf.read_dict(other)
        return self

    def merge_section(self, other, section):
        '''In-place merge a section of another configuration. Options from the
        `other` configuration override those from `self`.

        :param Config other: The configuration to merge into `self`.
        :param str section: The name of the section to merge.
        :returns: The modified configuration.
        '''
        if not self.has_section(section):
            self.add_section(section)
        for opt, val in other.items(section, raw=True):
            LOGGER.debug('merging option %r:%r = %r', section, opt, val)
            self.set(section, opt, val)
        return self

    def __add__(self, other):
        '''Merge two configurations, return the result as a new object.'''
        return self.from_mapping(self).merge(other)

    def items(self, section=_UNSET, *, raw=False):
        '''Yield the configuration items.

        If `section` is not speficied, yield ``(section_name, section_proxy)``
        pairs for each section. If `section` is given, yield all the ``(option,
        value)`` pairs from the given section.
        '''
        if section is _UNSET:
            yield from self._conf.items(raw=raw)
        else:
            yield from self._conf.items(section, raw=raw)

    __iadd__ = merge

    __radd__ = __add__

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        return self._conf == other._conf  # pylint: disable=protected-access

    def __str__(self):
        from itertools import chain
        all_secs = chain(self.sections(), [self._conf.default_section])
        return ('\n'.join('[{}]\n'.format(sec) + '\n'
                          .join('{} = {}'.format(key, val)
                                for key, val in self.items(sec, raw=True))
                          for sec in all_secs))

    def __repr__(self):
        return 'Config({})'.format(self.as_dict())
