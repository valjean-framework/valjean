'''Module containing the configuration class for the :mod:`valjean` package.

:class:`Config` objects encapsulate a set of configuration options for a
:mod:`valjean` run. Here is how you create one:

.. testsetup:: config

    from valjean.config import Config

.. doctest:: config

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

By default, :class:`Config` objects come with a ``'core'`` configuration
section, which may be used to set default values for any configuration option.
A few options are set from the beginning:

.. doctest:: config

    >>> for opt, val in config.items('core', raw=True):
    ...     print('{} = {}'.format(opt, val))
    work-dir = ...
    log-root = ${work-dir}/log
    checkout-root = ${work-dir}/checkout
    build-root = ${work-dir}/build
    run-root = ${work-dir}/run
    test-root = ${work-dir}/test
    report-root = ${work-dir}/report

The :class:`Config` class provides getters and setters:

.. doctest:: config

    >>> print(config.get('core', 'build-root'))
    /.../build

    # value interpolation is possible
    >>> config.set('core', 'log-root', '${work-dir}/log_dir')
    >>> print(config.get('core', 'log-root'))
    /.../log_dir

It also provides some additional convenience methods:

.. doctest:: config

    >>> from pprint import pprint

    # convert the configuration to an ordered dictionary
    >>> pprint(config.as_dict())
    {'core': {'work-dir': '...',
              'log-root': '${work-dir}/log_dir',
              'checkout-root': '${work-dir}/checkout',
              'build-root': '${work-dir}/build',
              'run-root': '${work-dir}/run',
              'test-root': '${work-dir}/test',
              'report-root': '${work-dir}/report'}}

    # merge two configuration objects; options from the second
    # configuration override those from the first one
    >>> other_config = Config(paths=[])
    >>> other_config.set('core', 'report-root', '${work-dir}/html')
    >>> other_config.set('core', 'extra-option', 'definitely!')
    >>> config += other_config
    >>> print(config.get('core', 'report-root'))
    /.../html
    >>> print(config.get('core', 'extra-option'))
    definitely!
'''

from configparser import (ConfigParser, ExtendedInterpolation, _UNSET,
                          NoOptionError, NoSectionError)
from collections import OrderedDict, namedtuple
from functools import partial
import os
import re

from . import LOGGER


class Config:
    '''The configuration class for :mod:`valjean`. It derives from
    :class:`configparser.ConfigParser`, so all of the methods of the base class
    can also be used with this one.
    '''

    #: Default configuration file paths.
    DEFAULT_CONFIG_FILES = ['~/.valjean.cfg', 'valjean.cfg']

    def __init__(self, paths=None):
        '''Construct a configuration object.

        :param paths: A list of paths for configuration files. If this is
                      `None`, :class:`Config` will search the following paths,
                      and read in the files in order if they exist:

                        * :file:`$HOME/.valjean.cfg`
                        * :file:`valjean.cfg` in the current directory

                      If you want to disable this behaviour, use an empty list.
                      If you want to read the default files **and** some
                      additional ones, the default files are available as
                      ``Config.DEFAULT_CONFIG_FILES``.
        :type paths: list or None
        '''

        self._conf = ConfigParser(interpolation=ExtendedInterpolation(),
                                  delimiters=('=',),
                                  comment_prefixes=('#',),
                                  empty_lines_in_values=False,
                                  default_section='core')
        # skip leading and trailing spaces in section names
        self._conf.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")

        # Set some default options
        self.set('core', 'work-dir', os.path.realpath(os.getcwd()))
        self.set('core', 'log-root', '${work-dir}/log')
        self.set('core', 'checkout-root', '${work-dir}/checkout')
        self.set('core', 'build-root', '${work-dir}/build')
        self.set('core', 'run-root', '${work-dir}/run')
        self.set('core', 'test-root', '${work-dir}/test')
        self.set('core', 'report-root', '${work-dir}/report')

        if paths is None:
            paths = self.DEFAULT_CONFIG_FILES

        other_conf = ConfigParser(default_section='core')
        other_conf.read([os.path.expanduser(p) for p in paths])
        for sec_name, _ in other_conf.items():
            for opt, val in other_conf.items(sec_name, raw=True):
                self.set(sec_name, opt, val)

    @classmethod
    def from_mapping(cls, mapping):
        '''Construct a configuration object from an option mapping.

        The keys of `mapping` must be strings; its values must be string →
        string mappings. Note that `mapping` may also be a :class:`Config`
        object (in which case this method acts as a copy).

        :param mapping mapping: The mapping for initialization.
        :returns: The constructed Config object.
        '''
        new = cls()
        new.merge(mapping)
        return new

    @staticmethod
    def _sectionxform(section):
        '''Normalize a section name by removing repeated spaces.'''
        sec_split = section.split('/', maxsplit=1)
        return '/'.join(' '.join(w.split()) for w in sec_split)

    def add_section(self, section):
        '''Add a configuration section.'''
        xsection = self._sectionxform(section)
        self._conf.add_section(xsection)
        split = self.split_section(xsection)
        if len(split) > 1:
            self._conf.set(xsection, 'family', split[0])
            self._conf.set(xsection, 'id', split[1])

    def remove_section(self, section):
        '''Remove a configuration section.'''
        xsection = self._sectionxform(section)
        self._conf.remove_section(xsection)

    def has_section(self, section):
        '''Check if a configuration section exists.'''
        xsection = self._sectionxform(section)
        return self._conf.has_section(xsection)

    def sections(self):
        '''Yield the configuration sections, excluding ``'core'``.'''
        yield from self._conf.sections()

    def remove_option(self, section, option):
        '''Remove an option from a section.'''
        xsection = self._sectionxform(section)
        self._conf.remove_option(xsection, option)

    def _get(self, section, option, **kwargs):
        xsection = self._sectionxform(section)
        return self._conf.get(xsection, option, **kwargs)

    def get(self, *args, raw=False, fallback=_UNSET):
        '''get(section, option, raw=False, fallback)

        Get the value of an option.

        This function can be called with two signatures:

          * :meth:`get(section, option)` returns the value of `option` in
            `section`;
          * :meth:`get(section_family, section_id, option)` returns the value
            of `option` in section ``section_family/section_id``.

        :param str section: The name of the section.
        :param str option: The name of the option.
        :param bool raw: If `True`, interpolate any ``${section:option}``
                         strings in the value with the value of the
                         corresponding option (see
                         :class:`configparser.ExtendedInterpolation` for more
                         information).
        :param fallback: A value to return if the option cannot be found.
        '''

        if len(args) == 3:
            return self.get('/'.join(args[0:2]), args[2], raw=raw,
                            fallback=fallback)
        elif len(args) > 3 or len(args) < 2:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3')
        section = args[0]
        option = args[1]
        xsection = self._sectionxform(section)

        try:
            val = self._get(xsection, option, raw=raw, fallback=fallback)
            LOGGER.debug('get(%r, %r) succeeded with value %s',
                         xsection, option, val)
            return val
        except NoOptionError as err:
            special = self.SPECIAL_OPTS.get(option, None)
            if special:
                secs, lookup, assemble = special
                split = self.split_section(xsection)
                if len(split) == 1 or split[0] not in secs:
                    raise err
                LOGGER.debug('treating option %s in section %s as special',
                             xsection, option)
                vals = lookup(self, xsection, split, option)
                if assemble is not None:
                    val = assemble(*vals)
                else:
                    val = vals
                return val
            raise err

    def set(self, *args):
        '''Set the value of an option.'''
        if len(args) == 4:
            self.set('/'.join(args[0:2]), args[2], args[3])
        elif len(args) > 4 or len(args) < 3:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3')
        section = args[0]
        option = args[1]
        value = args[2]
        xsection = self._sectionxform(section)
        self._conf.set(xsection, option, value)

    def as_dict(self, *, raw=True):
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
            self.set(section, opt, val)
        return self

    def sections_by_family(self, sec_family):
        '''Yield all sections from a given family.

        This generator filters sections according to a given family; for each
        section of a given family, the generator yields a tuple made of the
        full section name and the corresponding ID (i.e. the section name with
        the family and any subsequent slashes/spaces removed).

        If you know that there is only one section of the given family,
        consider using :meth:`section_by_family()`.

        :param str sec_family: A family to match.
        '''
        prefix = sec_family + '/'
        for section in self.sections():
            if section.startswith(prefix):
                yield (section, section[len(prefix):])

    def section_by_family(self, sec_family):
        '''Return a section by family.

        This method returns the full name of the first configuration section of
        the given family.

        :param str sec_family: A prefix to match.
        :returns: A tuple containing the full name of the found configuration
                  section and its ID.
        :raises NoSectionError: if no section from this family can be found.
        '''
        try:
            return next(self.sections_by_family(sec_family))
        except StopIteration:
            raise NoSectionError('No section from family {}'
                                 .format(sec_family))

    @staticmethod
    def split_section(section):
        '''Split section name into a ``(family, id)`` tuple.'''
        return section.split('/', maxsplit=1)

    def __add__(self, other):
        '''Merge two configurations, return the result as a new object.'''
        return Config.from_mapping(self).merge(other)

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

    def __iter__(self):
        yield from self._conf.__iter__()

    __iadd__ = merge

    __radd__ = __add__

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        return self._conf == other._conf  # pylint: disable=protected-access

    def executable(self, exe):
        '''Return the configuration for an executable.'''
        path_conf = self.get('executable', exe, 'path', fallback=None)
        if path_conf is None:
            raise KeyError('Expecting `path` option in `[executable/{}]` '
                           'configuration section'.format(exe))

        if os.path.isabs(path_conf):
            path = path_conf
        else:
            from_build = self.get('executable', exe, 'from-build',
                                  fallback=None)
            if from_build is None:
                raise KeyError('Expecting `from-build` option in `[executable/'
                               '{}]` configuration section'.format(exe))

            b_path = self.get('build', from_build, 'build-dir')
            path = os.path.abspath(os.path.join(b_path, path_conf))
            self.set('executable', exe, 'path', path)

        args = self.get('executable', exe, 'args', fallback=None)

        exe_conf = ExecutableConfig(path=path, args=args)
        return exe_conf

    def _lookup_other(self, sec, split, opt, *, other_sec=None,
                      other_opt=None):
        lookup_opt = opt if other_opt is None else other_opt
        lookup_sec = sec if other_sec is None else other_sec
        val = self.get(lookup_sec, lookup_opt)
        return (val, split[1])

    def _lookup_from_exe(self, sec, _, opt, **kwargs):
        exe = self.get(sec, 'exe')
        val = self.get('executable', exe, opt, raw=True)
        self.set(sec, opt, val)
        return self.get(sec, opt, **kwargs)

    SPECIAL_OPTS = {'build-dir': (('build',),
                                  partial(_lookup_other,
                                          other_opt='build-root'),
                                  os.path.join),
                    'checkout-dir': (('checkout',),
                                     partial(_lookup_other,
                                             other_opt='checkout-root'),
                                     os.path.join),
                    'args': (('run',), _lookup_from_exe, None)}


ExecutableConfig = namedtuple('ExecutableConfig', ['path', 'args'])
