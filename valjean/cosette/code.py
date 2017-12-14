# -*- coding: utf-8 -*-
u'''This submodule contains a few useful tasks for checking out, configuring,
and building arbitrary code.

The :class:`CheckoutTask` task class checks out a version-controlled
repository. For the moment, only ``git`` repositories are supported. The path
to the ``git`` executable may be specified through the :data:`CheckoutTask.GIT`
class variable.

.. todo::

   Implement ``svn`` and ``cvs`` checkout; ``copy`` checkout (i.e. copy a
   directory from somewhere) may also be useful.

The :class:`BuildTask` task class builds code from a given source directory. A
build directory must also be specified and will be created if necessary. For
the moment, :class:`BuildTask` only supports ` ``cmake`` builds, but there are
plans to add support for ``autoconf``/``configure``/``make`` builds. The path
to the ``cmake`` executable may be specified through the
:data:`BuildTask.CMAKE` class variable.

.. todo::

   Implement ``autoconf``/``configure``/``make`` builds.

An example of the usage of :class:`CheckoutTask` and :class:`BuildTask`:

.. testsetup:: code

   from valjean.cosette.code import CheckoutTask, BuildTask

.. doctest:: code

   >>> import os
   >>> test_dir = '/path/to/test_project'
   >>> source_dir = os.path.join(test_dir, 'src')
   >>> build_dir = os.path.join(test_dir, 'build')
   >>> ct = CheckoutTask(name='project_checkout',
   ...                   repository='/path/to/project.git',
   ...                   checkout_dir=source_dir,
   ...                   log_dir=test_dir)
   >>> bt = BuildTask(name='project_build',
   ...                source_dir=source_dir,
   ...                build_dir=build_dir,
   ...                build_flags='-- -j4',
   ...                log_dir=test_dir)
   >>> ct_up, ct_status = ct.do(dict())  # doctest: +SKIP
   >>> print(ct_status)             # doctest: +SKIP
   TaskStatus.DONE
   >>> pprint(ct_up)                 # doctest: +SKIP
   {'checkout': {'project_checkout': {'checkout_dir': \
'/path/to/test_project/src',
                                      'checkout_log': \
'/path/to/test_project/checkout_project_checkout.log',
                                      'repository': '/path/to/project.git'}},
    'tasks': {'project_checkout': {'return_code': 0,
                                   'wallclock_time': 0.34877443313598633}}}
   >>> bt_up, bt_status = bt.do(dict())  # doctest: +SKIP
   >>> print(bt_status)             # doctest: +SKIP
   TaskStatus.DONE
   >>> pprint(bt_up)                 # doctest: +SKIP
   {'build': {'project_build': {'build_log': \
'/path/to/test_project/build_project_build.log',
                                'configure_log': \
'/path/to/test_project/configure_project_build.log'}},
    'tasks': {'project_build': {'return_code': 0,
                                'wallclock_time': 173.11953258514404}}}

:class:`CheckoutTask` and :class:`BuildTask` can also be created from a
name and a :class:`~.Config` object, using the
:meth:`CheckoutTask.from_config()` and :meth:`BuildTask.from_config()` class
methods, respectively. The class methods will look for configuration sections
called ``[checkout <name>]`` (``[build <name>]``, respectively) and take their
parameters from there. The expected parameters are documented in the method
docstrings.
'''

import logging
import os
from ..config import Config
from .task import ShellTask


LOGGER = logging.getLogger('valjean')


class CheckoutTask(ShellTask):
    '''Task to check out code from a version-control system.  The actual code
    checkout is performed when the task is executed.
    '''

    @classmethod
    def from_config(cls, name: str, config: Config):
        '''Construct a :class:`CheckoutTask` from a :class:`~.Config` object.

        This method searches `config` for a section called ``[checkout
        <name>]``, where ``<name>`` is the name of the task. If the section is
        not found, :exc:`KeyError` is raised. Within this section, the optional
        ``vcs`` option selects the version-control system (defaults to
        ``git``). Depending on the value of ``vcs``, certain other options are
        also required:

        ``git``
          For ``vcs = git``, the only mandatory option is:

          ``repository``
            The path to or the address of the repository to clone.

          The following additional options are also available:

          ``checkout-dir``
            If present, it will be used as the path to the checkout directory.
            Otherwise, the path will be constructed as
            ``<core.checkout-dir>/<name>``.

          ``flags``
            Any flags that should be passed to ``git clone`` on checkout (for
            instance, ``--depth 1`` for shallow clones).

          ``ref``
            The hash/tag/branch name that should be checked out. If omitted,
            the ``master`` branch will be checked out.

        ``svn``
          Not implemented!

        ``cvs``
          Not implemented!

        ``copy``
          Not implemented!

        :param str name: The name of this task.
        :param Config config: The configuration object.
        :raises KeyError: if a configuration section called ``[checkout
                          <name>]`` is not found, or if any of the required
                          options is not found.
        '''

        from shlex import split

        sec_name = 'checkout {}'.format(name)
        if not config.has_section(sec_name):
            raise KeyError('Expecting section {} in configuration'
                           .format(sec_name))
        sec_conf = config[sec_name]

        # take the log directory from the config
        log_dir = config.get('core', 'log-dir')

        # if the checkout dir is specified in the [checkout <name>] config
        # section, use it; otherwise, default to <core.checkout-dir>/<name>
        checkout_dir = sec_conf.get('checkout-dir', None)
        if checkout_dir is None:
            checkout_dir = os.path.join(config.get('core', 'checkout-dir'),
                                        name)

        vcs = sec_conf.get('vcs', 'git')
        repository = sec_conf.get('repository')
        flags = split(sec_conf.get('flags', ''))
        ref = sec_conf.get('ref', 'master')

        return cls(name=name,
                   checkout_dir=checkout_dir,
                   log_dir=log_dir,
                   repository=repository,
                   flags=flags,
                   ref=ref,
                   vcs=vcs)

    # pylint: disable=too-many-arguments
    def __init__(self, name: str, checkout_dir: str, repository: str,
                 log_dir: str, flags=None, ref=None, vcs='git'):
        '''Construct a :class:`CheckoutTask`.

        :param str name: The name of this task.
        :param str checkout_dir: The directory where the code will be checked
                                 out.
        :param str repository: The repository for checkout.
        :param str log_dir: The path to the log directory.
        :param flags: The flags to be used at checkout time, as a list of
                      strings.
        :type flags: list or None
        :param ref: The reference to check out.
        :type ref: str or None
        :param vcs: The version-control system to use. Must be one of:
                    ``'git'`` (default), ``'svn'``, ``'cvs'``, ``'copy'``.
        :type vcs: str or None
        '''

        self.log_dir = log_dir
        self.checkout_dir = checkout_dir
        self.checkout_log = os.path.join(
            log_dir, 'checkout_{}.log'.format(self.sanitize_filename(name)))

        keywords = ['log_dir', 'checkout_dir', 'checkout_log', 'repository',
                    'flags', 'ref', 'GIT']

        if vcs == 'git':
            self.repository = os.path.expanduser(repository)
            self.flags = flags if flags is not None else []
            self.ref = ref if ref is not None else 'master'
            unformatted_script = self._GIT_TEMPLATE
        elif vcs == 'svn':
            raise NotImplementedError('SVN checkout not implemented yet')
        elif vcs == 'cvs':
            raise NotImplementedError('CVS checkout not implemented yet')
        elif vcs == 'copy':
            raise NotImplementedError('copy checkout not implemented yet')
        else:
            raise ValueError('unrecognized VCS: {}'.format(vcs))

        kwargs = self._make_kwargs(keywords)
        super().__init__(name, unformatted_script, **kwargs)

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        for keyword in keywords:
            LOGGER.debug('  - %s = %s', keyword, getattr(self, keyword))

    def do(self, env):
        '''Check out the code as specified. In addition to proposing updates to
        the ``env['tasks']`` dictionary with the execution result/time of the
        underlying checkout shell script (see :meth:`.ShellTask.do()`), this
        method proposes::

            env['checkout'][task.name]['checkout_dir'] = checkout_dir
            env['checkout'][task.name]['repository'] = repository
            env['checkout'][task.name]['checkout_log'] = checkout_log

        :param mapping env: The environment for the execution of this task.
        :returns: The proposed environment updates.
        '''

        env_up, status = super().do(env)
        env_up.setdefault('checkout', {}).setdefault(self.name, {})
        env_up['checkout'][self.name]['checkout_dir'] = self.checkout_dir
        env_up['checkout'][self.name]['repository'] = self.repository
        env_up['checkout'][self.name]['checkout_log'] = self.checkout_log
        return env_up, status

    #: Path to the :file:`git` executable. May be overridden before class
    #: instantiation.
    GIT = 'git'

    _GIT_TEMPLATE = r'''test -d {log_dir} || mkdir -p {log_dir}
test -d {checkout_dir} || mkdir -p {checkout_dir}
{GIT} clone {flags} -- {repository} {checkout_dir} >>{checkout_log} 2>&1
{GIT} -C {checkout_dir} checkout {ref} >>{checkout_log} 2>&1
'''


class BuildTask(ShellTask):
    '''Task to build an existing source tree. The build is actually performed
    when the task is executed.
    '''

    @classmethod
    def from_config(cls, name: str, config: Config):
        '''Construct a :class:`BuildTask` from a :class:`~.Config` object.

        This method searches `config` for a section called ``[build <name>]``,
        where ``<name>`` is the name of the task. If the section is not found,
        :exc:`KeyError` is raised.  Within this section, the optional
        ``build-system`` option selects the version-control system (defaults to
        ``cmake``). Depending on the value of ``build-system``, certain other
        options are also required:

        ``cmake``
          For ``build-system = cmake``, the only mandatory option is:

          ``source-dir``
            The path to the directory containing the sources.

          The following additional options are also available:

          ``build-dir``
            If present, it will be used as the path to the build directory.
            Otherwise, the path will be constructed as
            ``<core.build-dir>/<name>``.

          ``configure-flags``
            Flags to be passed to CMake at configure time (e.g.
            '-DCMAKE_BUILD_TYPE=Debug' for a debug build).

          ``build-flags``
            Flags to be passed to CMake at build time (e.g. '-- -j8' for
            parallel builds).

          ``build-targets``
            The CMake targets to be built, separated by spaces.

        ``svn``
          Not implemented!

        ``cvs``
          Not implemented!

        ``copy``
          Not implemented!

        :param str name: The name of this task.
        :param Config config: The configuration object.
        :raises KeyError: if a configuration section called ``[build <name>]``
                          is not found, or if any of the required
                          options is not found.
        '''

        from shlex import split

        sec_name = 'build {}'.format(name)
        if not config.has_section(sec_name):
            raise KeyError('Expecting section {} in configuration'
                           .format(sec_name))
        sec_conf = config[sec_name]

        # take the log directory from the config
        log_dir = config.get('core', 'log-dir')

        # if the build dir is specified in the [build <name>] config section,
        # use it; otherwise, default to <core.build-dir>/<name>
        build_dir = sec_conf.get('build-dir', None)
        if build_dir is None:
            build_dir = os.path.join(
                config.get('core', 'build-dir'),
                name
                )

        build_system = sec_conf.get('build-system', 'cmake')

        configure_flags = split(sec_conf.get('configure-flags', ''))
        build_flags = split(sec_conf.get('build-flags', ''))
        source_dir = sec_conf.get('source-dir', None)
        targets = sec_conf.get('build-targets', None)
        if targets is not None:
            targets = split(targets)

        return cls(name=name, source_dir=source_dir, build_dir=build_dir,
                   log_dir=log_dir, targets=targets, build_system=build_system,
                   configure_flags=configure_flags, build_flags=build_flags)

    # pylint: disable=too-many-arguments,too-many-locals
    def __init__(self, name: str, source_dir: str, build_dir: str,
                 log_dir: str, targets=None, build_system='cmake',
                 configure_flags=None, build_flags=None):
        '''Construct a :class:`BuildTask`.

        :param str name: The name of this task.
        :param str source_dir: The path to the directory containing the
                               sources.
        :param str build_dir: The path to the directory where the code will be
                              build.
        :param str log_dir: The path to the log directory.
        :param targets: A list of targets to build, or `None` for the default
                        target.
        :type targets: list or None
        :param str build_system: The name of the build system to use. Must be
                                 one of: ``'cmake'`` (default),
                                 ``'configure'``.
        :param configure_flags: The flags that will be passed to the build tool
                                at configuration time, as a list of strings.
        :type configure_flags: list
        :param build_flags: The flags that will be passed to the build tool at
                            build time, as a list of strings.
        :type build_flags: list
        '''

        self.log_dir = log_dir

        if source_dir is not None:
            self.source_dir = source_dir
        else:
            self.source_dir = ('{{env[checkout][{name}][checkout_dir]}}'
                               .format(name=name))
        LOGGER.debug('will look for source files in %s', self.source_dir)
        self.build_dir = build_dir
        LOGGER.debug('will use build dir %s', self.build_dir)

        keywords = ['log_dir', 'configure_log', 'build_log', 'configure_flags',
                    'build_flags', 'source_dir', 'build_dir', 'CMAKE']

        if build_system == 'cmake':
            if targets is None:
                build_commands = self._CMAKE_BUILD_DEF_TEMPLATE
            else:
                build_commands = '\n'.join(
                    self._CMAKE_BUILD_TEMPLATE.format(i=i)
                    for i in range(len(targets))
                    )
                for i, target in enumerate(targets):
                    attr_name = 'target{}'.format(i)
                    setattr(self, attr_name, target)
                    keywords.append(attr_name)
            unformatted_script = '\n'.join([self._CMAKE_TEMPLATE,
                                            build_commands])
        elif build_system == 'autoconf' or build_system == 'configure':
            raise NotImplementedError('configure build not implemented yet')
        else:
            raise ValueError('unrecognized build system: {}'
                             .format(build_system))

        self.configure_flags = (configure_flags if configure_flags is not None
                                else [])
        self.build_flags = build_flags if build_flags is not None else []
        self.configure_log = os.path.join(
            log_dir,
            'configure_{}.log'.format(self.sanitize_filename(name))
            )
        self.build_log = os.path.join(
            log_dir,
            'build_{}.log'.format(self.sanitize_filename(name))
            )

        kwargs = self._make_kwargs(keywords)
        super().__init__(name, unformatted_script, **kwargs)

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        for keyword in keywords:
            LOGGER.debug('  - %s = %s', keyword, getattr(self, keyword))

    def do(self, env):
        '''Invoke the build tool as specified. In addition to proposing updates
        to the ``env['tasks']`` argument with the execution result/time of the
        underlying checkout shell script (see :meth:`.ShellTask.do()`), this
        method proposes::

            env['build'][task.name]['configure_log'] = configure_log
            env['build'][task.name]['build_log'] = build_log

        :param mapping env: The environment for the execution of this task.
        :returns: The proposed environment updates.
        '''

        env_up, status = super().do(env)
        env_up.setdefault('build', {}).setdefault(self.name, {})
        env_up['build'][self.name]['configure_log'] = self.configure_log
        env_up['build'][self.name]['build_log'] = self.build_log
        return env_up, status

    #: Path to the :file:`cmake` executable. May be overridden before class
    #: instantiation.
    CMAKE = 'cmake'

    _CMAKE_TEMPLATE = r'''test -d {log_dir} || mkdir -p {log_dir}
test -d {build_dir} || mkdir -p {build_dir}
cd {build_dir}
{CMAKE} {configure_flags} {source_dir} >>{configure_log} 2>&1'''

    _CMAKE_BUILD_TEMPLATE = (r'''{{CMAKE}} --build {{build_dir}} '''
                             '''--target {{target{i}}} '''
                             ''' {{build_flags}} >>{{build_log}} 2>&1''')

    _CMAKE_BUILD_DEF_TEMPLATE = (r'''{CMAKE} --build {build_dir} '''
                                 '''{build_flags} >>{build_log} 2>&1''')
