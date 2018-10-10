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

The default files are in the :data:`BaseConfig.DEFAULT_CONFIG_FILES` class
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
    work-dir = ...
    log-root = ${work-dir}/log
    checkout-root = ${work-dir}/checkout
    build-root = ${work-dir}/build
    run-root = ${work-dir}/run
    test-root = ${work-dir}/test
    report-root = ${work-dir}/report

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
    ...     print('{}/{}: {}'.format(sec_name, option, value))
    path/work-dir: /...
    path/log-root: ${work-dir}/log_dir
    path/checkout-root: ${work-dir}/checkout
    path/build-root: ${work-dir}/build
    path/run-root: ${work-dir}/run
    path/test-root: ${work-dir}/test
    path/report-root: ${work-dir}/report

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

.. todo::

    Document section families/section IDs.


Option handlers
---------------

The methods described so far are actually implemented in the
:class:`BaseConfig` class, from which :class:`Config` inherits.  In addition,
:class:`Config` features an extensible mechanism to attach complex logic to
configuration queries. For instance, it is possible to implement a fallback
mechanism stipulating that if you look up option `eggs` and it is missing, the
value of option `spam` will be returned instead.

The mechanisms are implemented by `option handlers`. An option handler is a
callable class with an :meth:`accepts` method; :meth:`accepts` takes a section
family, a section ID and an option name as arguments and must return `True` if
it is willing to handle the query. If so, the handler will be called with all
the relevant context information and must return whatever value is appropriate,
along with any dependencies incurred.

.. todo::

    Refactor dependencies outside handlers?

The :mod:`.config_handlers` module documents the signatures and the contracts
of the handler methods, and also provides a few useful handler definitions.


Automatic dependency discovery
------------------------------

.. todo:: Document it. Perhaps refactor it somewhere else?

Module API
----------
'''

from configparser import (ConfigParser, ExtendedInterpolation, _UNSET,
                          NoOptionError, NoSectionError)
from collections import OrderedDict
import os
import re

from . import LOGGER
from .priority_set import PrioritySet
from .config_handlers import (LookupOtherHandler, LookupSectionFromOptHandler,
                              PathHandler, AddMissingSectionHandler,
                              DefineHandler, trigger)


class BaseConfig:
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
        string mappings. Note that `mapping` may also be a :class:`BaseConfig`
        or :class:`Config` object (in which case this method acts as a copy).

        :param mapping: The mapping for initialization.
        :type mapping: :term:`mapping`
        :returns: The constructed BaseConfig object.
        '''
        new = cls(paths=[])
        new.merge(mapping)
        return new

    @classmethod
    def split_section(cls, section):
        '''Split section name into a ``(family, id)`` tuple.'''
        return section.split('/', maxsplit=1)

    @classmethod
    def normalize_section(cls, section):
        '''Normalize a section name by removing repeated spaces.'''
        sec_split = cls.split_section(section)
        return '/'.join(' '.join(w.split()) for w in sec_split)

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

    # pylint: disable=redefined-builtin
    def get(self, *args, raw=False, vars=None, fallback=_UNSET):
        '''get(section, option, raw=False, fallback)

        Get the value of an option.

        This function can be called with two signatures:

          * ``get(section, option)`` returns the value of `option` in
            `section`;
          * ``get(section_family, section_id, option)`` returns the value
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
        :type vars: :term:`mapping` or None
        :param fallback: A value to return if the option cannot be found.
        '''

        if len(args) == 3:
            return self.get('/'.join(args[0:2]), args[2], raw=raw, vars=vars,
                            fallback=fallback)
        if len(args) > 3 or len(args) < 2:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3, got ' + str(len(args)))
        section = args[0]
        option = args[1]
        xsection = self.normalize_section(section)

        try:
            val = self._conf.get(xsection, option, raw=raw, vars=vars)
            LOGGER.debug('get(%r, %r) = %r', xsection, option, val)
            return val
        except (NoOptionError, NoSectionError):
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
        if len(args) > 4 or len(args) < 3:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3, got ' + str(len(args)))
        section = args[0]
        option = args[1]
        value = args[2]
        xsection = self.normalize_section(section)
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

        :param BaseConfig other: The configuration to merge into `self`.
        :returns: The modified configuration.
        '''
        self._conf.read_dict(other)
        return self

    def merge_section(self, other, section):
        '''In-place merge a section of another configuration. Options from the
        `other` configuration override those from `self`.

        :param BaseConfig other: The configuration to merge into `self`.
        :param str section: The name of the section to merge.
        :returns: The modified configuration.
        '''
        if not self.has_section(section):
            self.add_section(section)
        for opt, val in other.items(section, raw=True):
            LOGGER.debug('merging option %r:%r = %r', section, opt, val)
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
        :raises configparser.NoSectionError: if no section from this family can
                                             be found.
        '''
        try:
            return next(self.sections_by_family(sec_family))
        except StopIteration:
            raise NoSectionError('No section from family {}'
                                 .format(sec_family))

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
        if not isinstance(other, BaseConfig):
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
        return 'BaseConfig({})'.format(self.as_dict())


class Config(BaseConfig):
    '''The configuration class for :mod:`valjean`. It derives from
    :class:`BaseConfig` and extends it by providing the possibility to define
    handlers for special options that are invoked on lookup failure.
    '''

    def __init__(self, paths=None, handlers=None, defines=True):
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
        :param handlers: An iterable of handlers for specific options. If this
                         is `None`, the default handlers from
                         ``Config.DEFAULT_HANDLERS`` will be installed. The
                         elements of the iterables must be triples of the form
                         ``(fams, opt, handler)``, where ``fams`` is a list of
                         section families, ``opt`` is the name of the option to
                         handle and ``handler`` is the handler callable proper.
        :type handlers: :term:`iterable` or None
        :param bool defines: If `True`, add special handlers for
                             :samp:`[define/{sec_id}]` sections.
        '''
        super().__init__(paths)

        #: list of handlers
        if handlers is None:
            self._handlers = PrioritySet(self.DEFAULT_HANDLERS)
        else:
            self._handlers = PrioritySet(handlers)

        # initialize the list of cumulated dependencies with an empty set
        self._deps = set()

        if defines:
            # add DefineHandlers for each 'define/*' section
            for sec, _ in self.items():
                if sec.startswith('define/'):
                    self._add_define_handler(50, sec)

    def _add_define_handler(self, priority, sec):
        _, sec_id = self.split_section(sec)
        try:
            base = self.get(sec, 'base')
        except NoOptionError:
            err = "[define/*] sections must have a 'base' option"
            raise ValueError(err)
        extra = {key: value
                 for key, value in self.items(section=sec, raw=True)
                 if key != 'base'}
        handler = DefineHandler(sec_id, base=base, extra=extra)
        self.add_option_handler(priority, handler)

    # pylint: disable=redefined-builtin
    def get(self, *args, raw=False, vars=None, fallback=_UNSET):
        '''get(section, option, raw=False, fallback)

        Get the value of an option.

        This function can be called with two signatures:

          * ``get(section, option)`` returns the value of `option` in
            `section`;
          * ``get(section_family, section_id, option)`` returns the value
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
        :type vars: :term:`mapping` or None
        :param fallback: A value to return if the option cannot be found.
        '''

        if len(args) == 3:
            return self.get('/'.join(args[0:2]), args[2], raw=raw, vars=vars,
                            fallback=fallback)
        if len(args) > 3 or len(args) < 2:
            raise ValueError('Wrong number of arguments to get(); expected 2 '
                             'or 3, got ' + str(len(args)))
        section = args[0]
        option = args[1]
        xsection = self.normalize_section(section)

        try:
            val = self._conf.get(xsection, option, raw=raw, vars=vars)
            LOGGER.debug('get(%r, %r) = %r', xsection, option, val)
            return val
        except (NoOptionError, NoSectionError):
            split = self.split_section(xsection)
            if len(split) == 1:
                family, sec_id = '', split[0]
            else:
                family, sec_id = split
            for handler in self._handlers:
                if handler.accepts(self, family, sec_id, option):
                    LOGGER.debug('handler %s triggers on %s/%s:%s',
                                 handler, family, sec_id, option)
                    val, deps = handler(self, xsection, split, option, raw,
                                        vars, fallback)
                    self._deps.update(deps)
                    LOGGER.debug('get(%r, %r) = %r', xsection, option, val)
                    LOGGER.debug('deps = %r', deps)
                    return val
            if fallback is not _UNSET:
                LOGGER.debug('get(%r, %r) falls back to %r', xsection, option,
                             fallback)
                return fallback
            raise

    def get_deps(self):
        '''Return the dependencies induced by all the queries since the last
        call to :meth:`~.clear_deps()`.'''
        return self._deps.copy()

    def clear_deps(self):
        '''Clear the cached dependencies.'''
        self._deps.clear()

    def add_option_handler(self, priority, handler):
        '''Add an option handler.

        :param int priority: the priority of the new handler.
        :param handler: an option handler.
        '''
        self._handlers.add(priority, handler)

    def has_option_handler(self, family=None, section_id=None, option=None):
        '''Check if an option handler is installed for given section family,
        section ID and option name.'''
        return any(h.accepts(self, family, section_id, option)
                   for h in self._handlers)

    def get_option_handler(self, family=None, section_id=None, option=None):
        '''Return the option handler for given section family and option
        name.'''
        return next(h for h in self._handlers
                    if h.accepts(self, family, section_id, option))

    def __repr__(self):
        return 'Config({})'.format(self.as_dict())

    #: Default option handlers
    DEFAULT_HANDLERS = (
        (0, AddMissingSectionHandler()),
        (10, PathHandler('executable')),
        (50, LookupSectionFromOptHandler(
            trigger(family='build', option='source-dir'),
            'checkout'
        )),
        (50, LookupSectionFromOptHandler(
            trigger(family='run', option='args'),
            'executable'
        )),
        (50, LookupSectionFromOptHandler(
            trigger(family='run', option='path'), 'executable'
        )),
        (50, LookupOtherHandler(
            trigger(family='checkout', option='checkout-dir'),
            other_sec='path',
            other_opt='checkout-root',
            finalizer=lambda val, split, _: os.path.join(val, split[1])
        )),
        (50, LookupOtherHandler(
            trigger(family='checkout', option='source-dir'),
            other_opt='checkout-dir'
        )),
        (50, LookupOtherHandler(
            trigger(family='build', option='build-dir'),
            other_sec='path',
            other_opt='build-root',
            finalizer=lambda val, split, _: os.path.join(val, split[1])
        )),
    )
