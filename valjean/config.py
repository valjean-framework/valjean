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

    >>> config = Config(paths=list(Config.DEFAULT_CONFIG_FILES)
    ...                 + ['valjean.conf'])

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
    >>> pprint(config.as_dict(raw=True))
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


Option handlers
---------------

.. todo:: Write documentation about option handlers.
'''

from configparser import (ConfigParser, ExtendedInterpolation, _UNSET,
                          NoOptionError, NoSectionError)
from collections import OrderedDict
import os
import re

from . import LOGGER


class Config:
    '''The configuration class for :mod:`valjean`. It derives from
    :class:`configparser.ConfigParser`, so all of the methods of the base class
    can also be used with this one.
    '''

    #: Default configuration file paths.
    DEFAULT_CONFIG_FILES = ('~/.valjean.cfg', 'valjean.cfg')

    def __init__(self, paths=None, handlers=None):
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
        :type paths: iterable or None
        :param handlers: An iterable of handlers for specific options. If this
                         is `None`, the default handlers from
                         ``Config.DEFAULT_HANDLERS`` will be installed. The
                         elements of the iterables must be triples of the form
                         ``(fams, opt, handler)``, where ``fams`` is a list of
                         section families, ``opt`` is the name of the option to
                         handle and ``handler`` is the handler callable proper.
        :type handlers: iterable or None
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
            if sec_name != self._conf.default_section:
                self.add_section(sec_name)
            for opt, val in other_conf.items(sec_name, raw=True):
                self.set(sec_name, opt, val)

        #: dictionary
        self._handlers = dict()
        if handlers is None:
            the_handlers = self.DEFAULT_HANDLERS
        else:
            the_handlers = handlers
        for handler in the_handlers:
            self.add_option_handler(*handler)

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

    def has_option(self, section, option):
        '''Check if a configuration option exists.'''
        xsection = self._sectionxform(section)
        return self._conf.has_option(xsection, option)

    # pylint: disable=redefined-builtin
    def get(self, *args, raw=False, vars=None, fallback=_UNSET):
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
        :param vars: An option/value dictionary that will be looked up before
                     the configuration itself, or `None` if not needed.
        :type vars: mapping or None
        :param fallback: A value to return if the option cannot be found.
        '''

        if len(args) == 3:
            return self.get('/'.join(args[0:2]), args[2], raw=raw, vars=vars,
                            fallback=fallback)
        elif len(args) > 3 or len(args) < 2:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3')
        section = args[0]
        option = args[1]
        xsection = self._sectionxform(section)

        try:
            val = self._conf.get(xsection, option, raw=raw, vars=vars)
            LOGGER.debug('get(%r, %r) = %r', xsection, option, val)
            return val
        except NoOptionError:
            split = self.split_section(xsection)
            if len(split) > 1:
                handler = self._handlers.get((option, split[0]), None)
                if handler is not None:
                    LOGGER.debug('treating option %s in section %s as special',
                                 xsection, option)
                    val = handler(self, xsection, split, option, raw, vars,
                                  fallback)
                    LOGGER.debug('get(%r, %r) = %r', xsection, option, val)
                    return val
            if fallback is not _UNSET:
                LOGGER.debug('get(%r, %r) falls back to %r', xsection, option,
                             fallback)
                return fallback
            raise

    def set(self, *args):
        '''Set the value of an option.'''
        LOGGER.debug('len(args) = %s', len(args))
        LOGGER.debug('args = %s', list(args))
        if len(args) == 4:
            LOGGER.debug('set() called with 4 args, desugaring to 3')
            self.set('/'.join(args[0:2]), args[2], args[3])
            return
        elif len(args) > 4 or len(args) < 3:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3')
        section = args[0]
        option = args[1]
        value = args[2]
        xsection = self._sectionxform(section)
        LOGGER.debug('params: %s %s %s %s', section, xsection, option, value)
        LOGGER.debug('set(%r, %r, %r)', xsection, option, value)
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

    __iadd__ = merge

    __radd__ = __add__

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        return self._conf == other._conf  # pylint: disable=protected-access

    def add_option_handler(self, sec_families, option, handler):
        '''Add an option handler.

        :param list sec_families: The list of section families where the
                                  handler will be active.
        :param str option: The name of the option to be handled.
        :param handler: An option handler.
        '''
        for sec_family in sec_families:
            self._handlers[(option, sec_family)] = handler

    def has_option_handler(self, sec_family, option):
        '''Check if an option handler is installed for given section family and
        option name.'''
        return (option, sec_family) in self._handlers

    def get_option_handler(self, sec_family, option):
        '''Return the option handler for given section family and option
        name.'''
        return self._handlers[(option, sec_family)]

    class LookupOtherHandler:
        '''Handle missing options by looking up alternate options.

        This handler can be used to look up different options in other sections
        on failure. The result of the lookup can then be combined with the
        section name and the option name by specifying a `finalizer`, which
        must be a callable accepting three parameters:

          * the result of the alternate lookup;
          * the ``(section_name, section_id)`` pair for the original section;
          * the name of the original option.

        The `raw`, `vars` and `fallback` parameters to :meth:`Config.get()`
        will be passed through to the lookup of the alternate option.
        '''

        def __init__(self, other_sec=None, other_opt=None, finalizer=None):
            '''Instantiate an option handler.

            :param other_sec: Name of the alternate section where the lookup
                              will be done, or `None` to use the same section.
            :type other_sec: str or None
            :param other_opt: Name of the alternate option to look up, or
                              `None` to use the same option name.
            :type other_opt: str or None
            :param finalizer: A callable that will be passed three arguments:
                              1) the result of the alternate lookup, 2) the
                              ``(section_name, section_id)`` pair for the
                              original section, and 3) the name of the original
                              option. It should return the final value of the
                              handler. If finalizer is `None`, the value for
                              the alternate look-up will be returned as-is.
            '''
            self.other_sec = other_sec
            self.other_opt = other_opt
            self.finalizer = finalizer

        # pylint: disable=too-many-arguments
        def __call__(self, config, sec, split, opt, raw, vars_, fallback):
            '''Look up `other_opt` (defaults to `opt`) in `other_sec` (defaults
            to `sec`), and apply `finalizer` to the result.
            '''
            lookup_opt = opt if self.other_opt is None else self.other_opt
            lookup_sec = sec if self.other_sec is None else self.other_sec
            val = config.get(lookup_sec, lookup_opt, raw=raw, vars=vars_,
                             fallback=fallback)
            if self.finalizer is not None:
                return self.finalizer(val, split, opt)
            return val

    class LookupSectionFromOptHandler:
        '''Handle missing options by looking up options in sections defined by
        other options.

        This handler can be used to provide default values to missing options
        based on the values of other options in sections specified in the
        configuration file.

        Let's make an example, so it will hopefully be clearer. Consider the
        following configuration::

            [executable/dog_kennel]
            args = ${arg1} {arg2}
            arg1 = mattress

            [run/paper_bag]
            executable = dog_kennel
            arg2 = paper_bag

            [run/chest]
            executable = dog_kennel
            arg1 = sing
            arg2 = chest

        Assume we install the following option handler for `args` in the `run`
        sections::

            Config.add_option_handler(
                ['run'],
                'args',
                Config.LookupSectionFromOptHandler('executable')
                )

        Now let us look up `args` in the different sections::

            >>> config.get('executable', 'dog_kennel', 'args', raw=True)
            ${arg1} ${arg2}

        The handler is not activated here. Since ``raw=True`` was specified,
        the lookup result is not interpolated.

            >>> config.get('executable', 'dog_kennel', 'args')
            # throws InterpolationMissingOptionError

        Without ``raw=True``, the interpolation fails because `arg2` is not
        defined in the ``executable/dog_kennel`` section.

            >>> config.get('run', 'paper_bag', 'args', raw=True)
            ${arg1} ${arg2}

        Here the handler is activated because the `args` option is not present
        in the ``run/paper_bag`` section. The handler looks up the `executable`
        option (which yields ``dog_kennel``) and queries
        ``executable/dog_kennel`` for the `args` parameter.

            >>> config.get('run', 'paper_bag', 'args')
            mattress paper_bag

        If we activate interpolation (``raw=False``), we see that it succeeds
        (compare to the lookup of `args` from ``executable/dog_kennel`` above).
        The ``${arg2}`` option is interpolated from the ``run/paper_bag``
        section.

            >>> config.get('run', 'chest', 'args')
            sing chest

        From the ``run/chest`` section, interpolation also works. However, note
        that here ``${arg1}`` has been overridden by the value specified in
        ``run/chest``. This makes it possible to specify default option values
        in the base section (``executable/dog_kennel`` in our example) and
        override them in later sections (``run/chest``).
        '''

        def __init__(self, opt, finalizer=None):
            '''Instantiate an option handler.

            :param str opt: Name of an option that indicates in which section
                            the lookup should be performed. The option name is
                            taken to be the section family, and the option
                            value is taken to be the section ID.
            :param finalizer: A callable; see
                              :meth:`.LookupOtherHandler.__init__()`.
            '''
            self.opt = opt
            self.finalizer = finalizer

        # pylint: disable=too-many-arguments
        def __call__(self, config, sec, split, opt, raw, vars_, fallback):
            from collections import ChainMap
            try:
                sec_id = config.get(sec, self.opt, raw=False)
            except NoOptionError:
                return fallback

            # pylint: disable=protected-access
            chain = ChainMap(config._conf[sec])
            if vars_ is not None:
                chain.maps.append(vars_)
            val = config.get(self.opt, sec_id, opt, vars=chain, raw=raw)
            if self.finalizer is not None:
                return self.finalizer(val, split, opt)
            return val

    class PathHandler:
        '''Handle the 'path' option for executable/run sections.'''

        # pylint: disable=too-many-arguments
        @staticmethod
        def __call__(config, sec, _1, _2, raw, vars_, fallback):
            try:
                path = config.get(sec, 'relative-path', raw=raw, vars=vars_)
                if os.path.isabs(path):
                    return path
                from_build = config.get(sec, 'from-build', raw=raw, vars=vars_)
                build_dir = config.get('build', from_build, 'build-dir',
                                       raw=raw, vars=vars_)
                return os.path.join(build_dir, path)
            except NoOptionError:
                return fallback

    #: Default option handlers
    DEFAULT_HANDLERS = (
        (('run',), 'args', LookupSectionFromOptHandler('executable')),
        (('executable',), 'build-dir',
         LookupSectionFromOptHandler('from-build')),
        (('executable',), 'path', PathHandler()),
        (('run',), 'path', LookupSectionFromOptHandler('executable')),
        (('checkout',), 'checkout-dir',
         LookupOtherHandler(other_opt='checkout-root',
                            finalizer=lambda val, split, opt:
                            os.path.join(val, split[1]))),
        (('build',), 'build-dir',
         LookupOtherHandler(other_opt='build-root',
                            finalizer=lambda val, split, _:
                            os.path.join(val, split[1])))
    )
