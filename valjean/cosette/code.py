# -*- coding: utf-8 -*-
"""This submodule contains a few useful tasks for checking out, configuring,
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

.. testsetup:: code

   from valjean.cosette.code import CheckoutTask, BuildTask
   import os
   work_dir = os.path.join(doctest_tmpdir, 'code')
   os.mkdir(work_dir)
   repo_dir = os.path.join(work_dir, 'repo')
   os.mkdir(repo_dir)
   os.system(CheckoutTask.GIT + ' init ' + repo_dir)
   cmakelists_path = os.path.join(repo_dir, 'CMakeLists.txt')
   with open(cmakelists_path, 'w') as cmake_file:
       cmake_file.write('project(TestCodeTasks C)\\n'
           'set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")\\n'
           'file(WRITE "${SOURCE_FILENAME}" "int main() { return 0; }")\\n'
           'add_executable(test_exe "${SOURCE_FILENAME}")\\n'
           )
   git_dir = os.path.join(repo_dir, '.git')
   os.system(CheckoutTask.GIT + ' --git-dir ' + git_dir + ' --work-tree ' +
             repo_dir + ' add CMakeLists.txt')
   os.system(CheckoutTask.GIT + ' --git-dir ' + git_dir + ' --work-tree ' +
             repo_dir + ' commit -a -m "Test commit"')

To describe the usage of :class:`CheckoutTask` and :class:`BuildTask`, let us
assume that ``repo_dir`` contains a ``git`` repository with a CMake project.
We use a temporary directory ``work_dir`` for our test:

.. doctest:: code

   >>> import os
   >>> checkout_dir = os.path.join(work_dir, 'checkout')
   >>> build_dir = os.path.join(work_dir, 'build')
   >>> log_dir = os.path.join(work_dir, 'log')

Now we can build checkout and build tasks for this repository:

.. doctest:: code

   >>> from valjean.cosette.env import Env
   >>> from pprint import pprint
   >>> ct = CheckoutTask(name='project_checkout',
   ...                   repository=repo_dir,
   ...                   checkout_dir=checkout_dir,
   ...                   log_root=log_dir)
   >>> bt = BuildTask(name='project_build',
   ...                source_dir=checkout_dir,
   ...                build_dir=build_dir,
   ...                build_flags=['--' ,'-j4'],
   ...                log_root=log_dir)
   >>> env = Env()
   >>> ct_up, ct_status = ct.do(env)
   >>> print(ct_status)
   TaskStatus.DONE
   >>> pprint(ct_up)
   {'checkout/project_checkout': {'checkout_dir': '/.../checkout',
                                  'checkout_log': \
'/.../log/checkout_project_checkout.log',
                                  'repository': '/.../repo',
                                  'return_code': 0,
                                  'script_filename': \
'/.../checkout_project_checkout...',
                                  'wallclock_time': ...}}
   >>> env.apply(ct_up)  # apply CheckoutTask's environment update
   ...                   # for this example, this is actually optional
   >>> bt_up, bt_status = bt.do(env)
   >>> print(bt_status)
   TaskStatus.DONE
   >>> pprint(bt_up)
   {'build/project_build': {'build_log': '/.../log/build_project_build.log',
                            'configure_log': \
'/.../log/configure_project_build.log',
                            'return_code': 0,
                            'script_filename': \
'/.../build_project_build...',
                            'wallclock_time': ...}}


:class:`CheckoutTask` and :class:`BuildTask` can also be created from a
name and a :class:`~.Config` object, using the
:meth:`CheckoutTask.from_config()` and :meth:`BuildTask.from_config()` class
methods, respectively. The class methods will look for configuration sections
called ``[checkout/<name>]`` (``[build/<name>]``, respectively) and take their
parameters from there. The expected parameters are documented in the method
docstrings.
"""

import os

from ..config import Config
from .task import ShellTask
from .. import LOGGER


class CheckoutTask(ShellTask):
    '''Task to check out code from a version-control system.  The actual code
    checkout is performed when the task is executed.
    '''

    @classmethod
    def from_config(cls, name: str, config: Config):
        '''Construct a :class:`CheckoutTask` from a :class:`~.Config` object.

        This method searches `config` for a section called
        ``[checkout/<name>]``, where ``<name>`` is the name of the task. If the
        section is not found, :exc:`KeyError` is raised. Within this section,
        the optional ``vcs`` option selects the version-control system
        (defaults to ``git``). Depending on the value of ``vcs``, certain other
        options are also required:

        ``git``
          For ``vcs = git``, the only mandatory option is:

          ``repository``
            The path to or the address of the repository to clone.

          The following additional options are also available:

          ``checkout-dir``
            If present, it will be used as the path to the checkout directory.
            Otherwise, the path will be constructed as
            ``<core.checkout-root>/<name>``.

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
        :raises KeyError: if a configuration section called
                          ``[checkout/<name>]`` is not found, or if any of the
                          required options is not found.
        '''

        from shlex import split

        sec_fam = 'checkout'

        # take the log directory from the config
        log_root = config.get('core', 'log-root')

        # if the checkout dir is specified in the [checkout/<name>] config
        # section, use it; otherwise, default to <core.checkout-root>/<name>
        checkout_dir = config.get(sec_fam, name, 'checkout-dir')
        LOGGER.debug('checkout_dir = %s', checkout_dir)

        vcs = config.get(sec_fam, name, 'vcs', fallback='git')
        repository = config.get(sec_fam, name, 'repository')
        flags = split(config.get(sec_fam, name, 'flags', fallback=''))
        ref = config.get(sec_fam, name, 'ref', fallback='master')
        deps = config.get(sec_fam, name, 'depends-on', fallback=None)

        return cls(name=name, checkout_dir=checkout_dir, log_root=log_root,
                   repository=repository, flags=flags, ref=ref, vcs=vcs,
                   deps=deps)

    # pylint: disable=too-many-arguments
    def __init__(self, name: str, checkout_dir: str, repository: str,
                 log_root: str, *, flags=None, ref=None, vcs='git', deps=None):
        '''Construct a :class:`CheckoutTask`.

        :param str name: The name of this task.
        :param str checkout_dir: The directory where the code will be checked
                                 out.
        :param str repository: The repository for checkout.
        :param str log_root: The path to the log directory.
        :param flags: The flags to be used at checkout time, as a list of
                      strings.
        :type flags: list or None
        :param ref: The reference to check out.
        :type ref: str or None
        :param vcs: The version-control system to use. Must be one of:
                    ``'git'`` (default), ``'svn'``, ``'cvs'``, ``'copy'``.
        :type vcs: str or None
        :param deps: The dependencies for this task (see
                     :meth:`Task.__init__()` for the format), or `None`.
        :type deps: str or None
        '''

        self.log_root = log_root
        self.checkout_dir = checkout_dir
        self.checkout_log = os.path.join(
            log_root, 'checkout_{}.log'.format(self.sanitize_filename(name)))

        keywords = ['log_root', 'checkout_dir', 'checkout_log', 'repository',
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
        task_name = 'checkout/' + name
        super().__init__(task_name, unformatted_script, deps=deps, **kwargs)

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        for keyword in keywords:
            LOGGER.debug('  - %s = %s', keyword, getattr(self, keyword))

    def do(self, env):
        '''Check out the code as specified. In addition to proposing updates to
        the ``env`` dictionary with the execution result/time of the underlying
        checkout shell script (see :meth:`.ShellTask.do()`), this method
        proposes::

            env[task.name]['checkout_dir'] = checkout_dir
            env[task.name]['repository'] = repository
            env[task.name]['checkout_log'] = checkout_log

        :param mapping env: The environment for the execution of this task.
        :returns: The proposed environment updates.
        '''

        env_up, status = super().do(env)
        env_up.setdefault(self.name, {})
        env_up[self.name]['checkout_dir'] = self.checkout_dir
        env_up[self.name]['repository'] = self.repository
        env_up[self.name]['checkout_log'] = self.checkout_log
        return env_up, status

    #: Path to the :file:`git` executable. May be overridden before class
    #: instantiation.
    GIT = 'git'

    _GIT_TEMPLATE = r'''test -d {log_root} || mkdir -p {log_root}
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

        This method searches `config` for a section called ``[build/<name>]``,
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
            ``<core.build-root>/<name>``.

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
        :raises KeyError: if a configuration section called ``[build/<name>]``
                          is not found, or if any of the required
                          options is not found.
        '''

        from shlex import split

        sec_fam = 'build'

        # take the log directory from the config
        log_root = config.get('core', 'log-root')

        # if the build dir is specified in the [build/<name>] config section,
        # use it; otherwise, default to <core.build-root>/<name>
        build_dir = config.get(sec_fam, name, 'build-dir')

        build_system = config.get(sec_fam, name, 'build-system',
                                  fallback='cmake')

        configure_flags = split(config.get(sec_fam, name, 'configure-flags',
                                           fallback=''))
        build_flags = split(config.get(sec_fam, name, 'build-flags',
                                       fallback=''))
        source_dir = config.get(sec_fam, name, 'source-dir', fallback=None)
        targets = config.get(sec_fam, name, 'build-targets', fallback=None)
        if targets is not None:
            targets = split(targets)
        deps = config.get(sec_fam, name, 'depends-on', fallback=None)

        return cls(name=name, source_dir=source_dir, build_dir=build_dir,
                   log_root=log_root, targets=targets,
                   build_system=build_system, configure_flags=configure_flags,
                   build_flags=build_flags, deps=deps)

    # pylint: disable=too-many-arguments,too-many-locals
    def __init__(self, name: str, source_dir: str, build_dir: str,
                 log_root: str, *, targets=None, build_system='cmake',
                 configure_flags=None, build_flags=None, deps=None):
        '''Construct a :class:`BuildTask`.

        :param str name: The name of this task.
        :param str source_dir: The path to the directory containing the
                               sources.
        :param str build_dir: The path to the directory where the code will be
                              build.
        :param str log_root: The path to the log directory.
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
        :param deps: The dependencies for this task (see
                     :meth:`Task.__init__()` for the format), or `None`.
        :type deps: str or None
        '''

        self.log_root = log_root

        if source_dir is not None:
            self.source_dir = source_dir
        else:
            self.source_dir = (
                '{{env[checkout/{name}][checkout_dir]}}'
                .format(name=name)
                )

        LOGGER.debug('will look for source files in %s', self.source_dir)
        self.build_dir = build_dir
        LOGGER.debug('will use build dir %s', self.build_dir)

        keywords = ['log_root', 'configure_log', 'build_log',
                    'configure_flags', 'build_flags', 'source_dir',
                    'build_dir', 'CMAKE']

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
            log_root,
            'configure_{}.log'.format(self.sanitize_filename(name))
            )
        self.build_log = os.path.join(
            log_root,
            'build_{}.log'.format(self.sanitize_filename(name))
            )

        kwargs = self._make_kwargs(keywords)
        task_name = 'build/' + name
        super().__init__(task_name, unformatted_script, deps=deps, **kwargs)

        if source_dir is None:
            self.add_dependency('checkout/' + name)

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)
        for keyword in keywords:
            LOGGER.debug('  - %s = %s', keyword, getattr(self, keyword))

    def do(self, env):
        '''Invoke the build tool as specified. In addition to proposing updates
        to the ``env`` argument with the execution result/time of the
        underlying checkout shell script (see :meth:`.ShellTask.do()`), this
        method proposes::

            env[task.name]['configure_log'] = configure_log
            env[task.name]['build_log'] = build_log

        :param mapping env: The environment for the execution of this task.
        :returns: The proposed environment updates.
        '''

        env_up, status = super().do(env)
        env_up.setdefault(self.name, {})
        env_up[self.name]['configure_log'] = self.configure_log
        env_up[self.name]['build_log'] = self.build_log
        return env_up, status

    #: Path to the :file:`cmake` executable. May be overridden before class
    #: instantiation.
    CMAKE = 'cmake'

    _CMAKE_TEMPLATE = r'''test -d {log_root} || mkdir -p {log_root}
test -d {build_dir} || mkdir -p {build_dir}
cd {build_dir}
{CMAKE} {configure_flags} {source_dir} >>{configure_log} 2>&1'''

    _CMAKE_BUILD_TEMPLATE = (r'''{{CMAKE}} --build {{build_dir}} '''
                             '''--target {{target{i}}} '''
                             ''' {{build_flags}} >>{{build_log}} 2>&1''')

    _CMAKE_BUILD_DEF_TEMPLATE = (r'''{CMAKE} --build {build_dir} '''
                                 '''{build_flags} >>{build_log} 2>&1''')
