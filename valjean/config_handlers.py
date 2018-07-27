'''Option handlers for the :class:`.Config` class.

An option handler is a class :class:`SomeHandler` providing the following
methods:

.. method:: SomeHander.accepts(family, section_id, option)

    This method takes a section family, a section ID and an option name as
    arguments and must return a bool indicating whether it is willing to handle
    the query.

    :param str family: a section family.
    :param str section_id: a section ID.
    :param str option: an option name.
    :returns: True if the handler is willing to handle this query.

.. method:: SomeHander. __call__(config, section, split, option, raw, vars,\
                                 fallback):

    If the handler accepts the query, it is called with the following
    arguments:

    :param config: the configuration object.
    :type config: .Config
    :param str section: the full name (:samp:`{family}/{ID}`) of the queried
                        section.
    :param tuple split: a pair of strings representing the section family and
                        the section ID.
    :param str option: the name of the option requested.
    :param bool raw: whether option values should be interpolated.
    :param dict vars: any additional key-value mapping that should be
                      consulted.
    :param fallback: a fallback value that must be returned if the handler
                     fails.

    For the meaning of `raw`, `vars` and `fallback`, you can consult the
    documentation for :meth:`.Config.get` and
    :meth:`configparser.ConfigParser.get`.

    The handler must return a pair `(val, deps)`. The first element of the pair
    is the value resulting from the handled lookup. The second element is a
    list of any dependencies that this lookup may have incurred. Dependencies
    are accumulated by :class:`.Config` and can later be consulted
    (:meth:`.Config.get_deps`).

.. doctest:: config_handlers
   :hide:

As an example, here is a handler that turns all unsuccessful lookups of the
`'eggs'` option into lookups of `'spam'`:

    >>> from valjean.config_handlers import trigger
    >>> from configparser import NoOptionError
    >>> from valjean.config import BaseConfig, Config
    >>> class EggsHandler:
    ...     @staticmethod
    ...     def accepts(config, family, sec_id, option):
    ...         return option == 'eggs'
    ...     @staticmethod
    ...     def __call__(config, section, split, option, raw, vars, fallback):
    ...         try:
    ...             val = BaseConfig.get(config, section, option, raw=raw,
    ...                                  vars=vars, fallback=fallback)
    ...             deps = []
    ...         except NoOptionError:
    ...             val = config.get(section, 'spam', raw=raw, vars=vars,
    ...                              fallback=fallback)
    ...             deps = ['section/spam']
    ...         return val, deps

Now we construct a :class:`.Config` object and we attach the handler to it:

    >>> conf = Config(paths=[], handlers=[])
    >>> conf.add_section('has_eggs')
    >>> conf.set('has_eggs', 'eggs', 'EGGS')
    >>> conf.set('has_eggs', 'spam', 'SPAM')
    >>> conf.add_section('no_eggs')
    >>> conf.set('no_eggs', 'spam', 'BACON')
    >>> conf.add_section('empty')
    >>> conf.add_option_handler(50, EggsHandler())

and here we see the handler in action:

    >>> conf.get('has_eggs', 'eggs')
    'EGGS'
    >>> conf.get('no_eggs', 'eggs')
    'BACON'
    >>> conf.get('empty', 'eggs')
    Traceback (most recent call last):
        [...]
    configparser.NoOptionError: No option 'spam' in section: 'empty'


Some useful handlers
--------------------

This module provides a few useful handlers:
'''

import os
from configparser import NoOptionError
from collections import ChainMap

from . import LOGGER


class Handler:
    '''Base class for option handlers.'''

    def __init__(self, accepts):
        '''Initialize a handler.

        :param callable accepts: a callable that will be called by
                                 :meth:`Handler.accepts`.
        '''
        self._accepts = accepts

    def accepts(self, *args):
        '''Return `True` if this handler accepts to deal with the requested
        option.'''
        return self._accepts(*args)

    # pylint: disable=too-many-arguments
    def __call__(self, config, sec, split, opt, raw, vars_, fallback):
        error = 'handlers must implement the __call__() method'
        raise NotImplementedError(error)


class LookupOtherHandler(Handler):
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

    def __init__(self, accepts, other_sec=None, other_opt=None,
                 finalizer=None):
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
        super().__init__(accepts)
        self.other_sec = other_sec
        self.other_opt = other_opt
        self.finalizer = finalizer

    # pylint: disable=too-many-arguments
    def __call__(self, config, sec, split, opt, raw, vars_, fallback):
        '''Look up `other_opt` (defaults to `opt`) in `other_sec` (defaults
        to `sec`), and apply `finalizer` to the result.
        '''
        lookup_opt = opt if self.other_opt is None else self.other_opt
        if self.other_sec:
            lookup_sec = self.other_sec
            deps = [self.other_sec]
        else:
            lookup_sec = sec
            deps = []
        val = config.get(lookup_sec, lookup_opt, raw=raw, vars=vars_,
                         fallback=fallback)
        if self.finalizer is not None:
            return self.finalizer(val, split, opt), deps
        return val, deps


class LookupSectionFromOptHandler(Handler):
    '''Handle missing options by looking up options in sections defined by
    other options.

    This handler can be used to provide default values to missing options
    based on the values of other options in sections specified in the
    configuration file.

    .. doctest:: config_handlers_lookupsection
        :hide:

        >>> from valjean.config import Config
        >>> from valjean.config_handlers import (LookupSectionFromOptHandler,
        ...                                      trigger)
        >>> config_string= """[executable/dog_kennel]
        ... args = ${arg1} ${arg2}
        ... arg1 = mattress
        ...
        ... [run/paper_bag]
        ... executable = dog_kennel
        ... arg2 = paper_bag
        ...
        ... [run/chest]
        ... executable = dog_kennel
        ... arg1 = sing
        ... arg2 = chest"""
        >>> with open('file.cfg', 'w') as fout:
        ...     print(config_string, file=fout)
        >>> config = Config(paths=['file.cfg'], handlers=[])

    Let's make an example, so it will hopefully be clearer. Consider the
    following configuration:

        >>> print(config_string)
        [executable/dog_kennel]
        args = ${arg1} ${arg2}
        arg1 = mattress
        <BLANKLINE>
        [run/paper_bag]
        executable = dog_kennel
        arg2 = paper_bag
        <BLANKLINE>
        [run/chest]
        executable = dog_kennel
        arg1 = sing
        arg2 = chest

    Assume we install the following option handler for `args` in the `run`
    sections::

        >>> config.add_option_handler(50,   # a priority
        ...   LookupSectionFromOptHandler(trigger(family='run', option='args'),
        ...                               'executable')
        ...   )

    This means that the handler will fire only in sections of the `run`
    family.  Now let us look up `args` in the different sections:

        >>> config.get('executable', 'dog_kennel', 'args', raw=True)
        '${arg1} ${arg2}'

    The handler does not fire here because we are asking for the `args`
    option of the ``executable/dog_kennel`` section, which does not belong
    to the `run` family. Additionally, since ``raw=True`` was specified,
    the lookup result is not interpolated and we obtain ``${arg1}
    ${arg2}``. Suppressing ``raw=True`` results in an exception:

        >>> config.get('executable',
        ...            'dog_kennel',
        ...            'args')  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        configparser.InterpolationMissingOptionError: Bad value substitution:
            ...

    Without ``raw=True``, the configuration tries to interpolate `arg2` and
    fails, because this option is not defined in ``executable/dog_kennel``.
    Now consider the following:

        >>> config.get('run', 'paper_bag', 'args', raw=True)
        '${arg1} ${arg2}'

    Here the handler fires because the `args` option is not explicitly
    present in the ``run/paper_bag`` section. The handler looks up the
    `executable` option (which yields ``dog_kennel``) and queries
    ``executable/dog_kennel`` for the `args` parameter. Thus, we get the
    same (uninterpolated) result as before.

    If we activate interpolation (``raw=False``)

        >>> config.get('run', 'paper_bag', 'args')
        'mattress paper_bag'

    we see that the query now succeeds (compare to the lookup of `args`
    from ``executable/dog_kennel`` above).  The ``${arg1}`` option is
    interpolated from the ``executable/dog_kennel`` section, but
    ``${arg2}`` is interpolated from ``run/paper_bag``.

        >>> config.get('run', 'chest', 'args')
        'sing chest'

    From the ``run/chest`` section, interpolation also works. However, note
    that here ``${arg1}`` has been overridden by the value specified in
    ``run/chest``. This makes it possible to specify default option values
    in the base section (``executable/dog_kennel`` in our example) and
    override them in later sections (``run/chest``).
    '''

    def __init__(self, accepts, opt, finalizer=None):
        '''Instantiate an option handler.

        :param accepts: a :func:`trigger`
        :param str opt: Name of an option that indicates in which section
                        the lookup should be performed. The option name is
                        taken to be the section family, and the option
                        value is taken to be the section ID.
        :param finalizer: A callable; see
                          :meth:`.LookupOtherHandler.__init__()`.
        '''
        super().__init__(accepts)
        self.opt = opt
        self.finalizer = finalizer

    # pylint: disable=too-many-arguments
    def __call__(self, config, sec, split, opt, raw, vars_, fallback):
        sec_id = config.get(sec, self.opt, raw=False)

        # pylint: disable=protected-access
        chain = ChainMap(config._conf[sec])
        if vars_ is not None:
            chain.maps.append(vars_)
        val = config.get(self.opt, sec_id, opt, vars=chain, raw=raw)
        deps = ['{}/{}'.format(self.opt, sec_id)]
        if self.finalizer is not None:
            return self.finalizer(val, split, opt), deps
        return val, deps


class PathHandler(Handler):
    '''Handle the 'path' option for executable/run sections.

    This handler specifies the logic to extract the path of an executable
    for a section of the `executable` family.  If the `path` option is not
    explicitly specified, we first look for `from-build` (which must be the
    name of a section of the `build` family) and `relative-path` (which
    must be a relative path). The path to the executable is constructed by
    concatenating the build directory of `from-build` with `relative-path`.
    '''

    def __init__(self, family):
        '''Initialize the handler for the given section.'''
        super().__init__(trigger(family=family, option='path'))

    # pylint: disable=too-many-arguments
    @staticmethod
    def __call__(config, sec, _1, _2, raw, vars_, fallback):
        try:
            path = config.get(sec, 'relative-path', raw=raw, vars=vars_)
            if os.path.isabs(path):
                raise ValueError("'relative-path' in section {} "
                                 "cannot be an absolute path"
                                 .format(sec))
            from_build = config.get(sec, 'from-build', raw=raw, vars=vars_)
            build_dir = config.get('build', from_build, 'build-dir',
                                   raw=raw, vars=vars_)
            deps = ['build/{}'.format(from_build)]
            return os.path.join(build_dir, path), deps
        except NoOptionError:
            deps = []
            return fallback, deps


class DefineHandler(Handler):
    '''Handle user-defined sections.

    This handler is instantiated by the :class:`~.Config` constructor on all
    sections of the form :samp:`[define/{name}]`. It allows to "subclass" the
    behaviour of any existing section by specifying some of its option values.

.. doctest:: DefineHandler
   :hide:

    >>> from valjean.config import Config
    >>> config_string= """[build/frob]
    ... source-dir = /path/to/frob/sec
    ...
    ... [define/frob it]
    ... base = executable
    ... from-build = frob
    ... args = ${it} ${SECTION_ID}
    ... it = this
    ...
    ... [frob it/foo]
    ... it = that
    ...
    ... [frob it/bar]"""
    >>> with open('file.cfg', 'w') as fout:
    ...     print(config_string, file=fout)
    >>> config = Config(paths=['file.cfg'])

    Let us look at an example:

    >>> print(config_string)
    [build/frob]
    source-dir = /path/to/frob/sec
    <BLANKLINE>
    [define/frob it]
    base = executable
    from-build = frob
    args = ${it} ${SECTION_ID}
    it = this
    <BLANKLINE>
    [frob it/foo]
    it = that
    <BLANKLINE>
    [frob it/bar]

    This config file defines a new section family called ``frob it``. The
    ``base = executable`` option specifies that ``frob it`` sections are
    nothing but ``executable`` sections, but the ``path`` and ``args`` are
    fixed beforehand.

    We add the handler to the config object:

    >>> from valjean.config_handlers import DefineHandler, trigger
    >>> config.add_option_handler(60,   # a priority
    ...   DefineHandler('frob it',
    ...                 base='executable',
    ...                 extra={'from-build': 'frob',
    ...                        'args': '${it} ${SECTION_ID}',
    ...                        'it': 'this'}))

    Now the ``frob it`` sections are treated as ``executable`` sections. Proof:

    >>> config.get('frob it', 'foo', 'from-build')
    'frob'
    >>> config.get('frob it', 'foo', 'args')
    'that foo'
    >>> config.get('frob it', 'bar', 'args')
    'this bar'

    :class:`DefineHandler` plays especially well with
    :class:`MissingSectionHandler`, which adds a section when it is missing
    from the input file.

    >>> config.get('frob it', 'fleep', 'args')
    'this fleep'
    '''

    def __init__(self, name, base, extra):
        super().__init__(trigger(family=name))
        self.base = base
        self.extra = extra

    # pylint: disable=too-many-arguments
    def __call__(self, config, sec, split, opt, raw, vars_, fallback):
        other_opts = {key: value
                      for key, value in config.items(sec, raw=True)
                      if key != opt}
        other_opts['SECTION_ID'] = split[1]
        chain = ChainMap()
        chain.maps.extend(dic
                          for dic in (vars_, other_opts, self.extra)
                          if dic is not None)

        LOGGER.debug('DefineHandler: chain.maps=%s', chain.maps)

        new_sec = self.base + '/' + split[1]
        LOGGER.debug('DefineHandler: looking up %r in %r',
                     opt, new_sec)
        val = config.get(new_sec, opt, raw=raw, vars=chain,
                         fallback=fallback)
        LOGGER.debug('DefineHandler: got %r', val)
        deps = [new_sec]
        return val, deps


class AddMissingSectionHandler:
    '''Add empty sections if they are missing.

    This handler simply adds an empty section to the configuration if the
    section is not present, and calls
    :meth:`Config.get <valjean.config.Config.get>` again.
    '''
    @staticmethod
    def accepts(config, family, sec_id, _):
        '''Returns `True` if the configuration does not contain a section
        called :samp:`{family}/{sec_id}`.
        '''
        if family is not None and sec_id is not None:
            return not config.has_section('/'.join([family, sec_id]))
        return False

    # pylint: disable=too-many-arguments
    @staticmethod
    def __call__(config, sec, split, opt, raw, vars_, fallback):
        '''Add the missing section and recurse on
        :meth:`Config.get <valjean.config.Config.get>`'''
        assert not config.has_section(sec)  # otherwise what are we doing here?
        config.add_section(sec)
        val = config.get(sec, opt, raw=raw, vars=vars_, fallback=fallback)
        return val, []


def trigger(family=None, section_id=None, option=None):
    '''Return a predicate to recognize a particular family/section_id/option.

    The predicate will return `True` if the values of all the non-None
    arguments to :func:`trigger` are equal to its arguments.

    Functions generated by :func:`trigger` can be fed to the `accepts` argument
    to the constructors of most handlers in this module.

    Examples:

        >>> from valjean.config import Config
        >>> family_foo = trigger(family='foo')
        >>> from valjean.config import Config
        >>> conf = Config([])
        >>> family_foo(conf, 'foo', 'some_id', 'some_opt')
        True
        >>> family_foo(conf, 'bar', 'some_id', 'some_opt')
        False

        >>> family_foo_option_frob = trigger(family='foo', option='frob')
        >>> family_foo_option_frob(conf, 'foo', 'some_id', 'some_opt')
        False
        >>> family_foo_option_frob(conf, 'foo', 'some_id', 'frob')
        True

    :param family: a section family.
    :type family: str or None
    :param section_id: a section ID.
    :type section_id: str or None
    :param option: an option name.
    :type option: str or None
    '''
    if family is None and section_id is None and option is None:
        def _accepts(_0, _1, _2, _3):
            return True
    elif family is None and section_id is None:
        def _accepts(_0, _1, _2, opt, *, capture=option):
            return opt == capture
    elif family is None and option is None:
        def _accepts(_0, _1, sec_id, _2, *, capture=section_id):
            return sec_id == capture
    elif section_id is None and option is None:
        def _accepts(_0, fam, _1, _2, *, capture=family):
            return fam == capture
    elif family is None:
        def _accepts(_0, _1, sec_id, opt, *, capture=(section_id, option)):
            return (sec_id, opt) == capture
    elif section_id is None:
        def _accepts(_0, fam, _1, opt, *, capture=(family, option)):
            return (fam, opt) == capture
    elif option is None:
        def _accepts(_0, fam, sec_id, _1, *, capture=(family, section_id)):
            return (fam, sec_id) == capture
    else:
        def _accepts(_, fam, sec_id, opt, capt=(family, section_id, option)):
            return (fam, sec_id, opt) == capt
    return _accepts
