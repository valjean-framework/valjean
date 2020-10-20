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

.. doctest:: code
   :hide:

   >>> from valjean.cosette.code import CheckoutTask, BuildTask
   >>> import subprocess
   >>> work_dir = getfixture('tmp_path')
   >>> repo_dir = work_dir / 'repo'
   >>> repo_dir.mkdir()
   >>> subprocess.check_call([CheckoutTask.GIT, 'init', str(repo_dir)])
   0
   >>> cmakelists_path = repo_dir / 'CMakeLists.txt'
   >>> with cmakelists_path.open('w') as cmake_file:
   ...     print('project(TestCodeTasks C)\\n'
   ...           'cmake_minimum_required(VERSION 2.6)\\n'
   ...           'set(SOURCE_FILENAME "${PROJECT_BINARY_DIR}/test.c")\\n'
   ...           'file(WRITE "${SOURCE_FILENAME}" "int main(){return 0;}")\\n'
   ...           'add_executable(test_exe "${SOURCE_FILENAME}")\\n',
   ...           file=cmake_file)
   >>> git_dir = repo_dir / '.git'
   >>> subprocess.check_call([CheckoutTask.GIT, '--git-dir', str(git_dir),
   ...                        'config', 'user.email', 'sblinda@antani.com'])
   0
   >>> subprocess.check_call([CheckoutTask.GIT, '--git-dir', str(git_dir),
   ...                        'config', 'user.name', 'Conte Mascetti'])
   0
   >>> subprocess.check_call([CheckoutTask.GIT, '--git-dir', str(git_dir),
   ...                        '--work-tree' , str(repo_dir),
   ...                        'add', 'CMakeLists.txt'])
   0
   >>> subprocess.check_call([CheckoutTask.GIT, '--git-dir', str(git_dir),
   ...                        '--work-tree', str(repo_dir),
   ...                        'commit', '-a', '-m', 'Test commit'])
   0

To describe the usage of :class:`CheckoutTask` and :class:`BuildTask`, let us
assume that ``repo_dir`` contains a ``git`` repository with a CMake project.
We use a temporary directory ``work_dir`` for our test:

   >>> checkout_dir = work_dir / 'checkout'
   >>> build_dir = work_dir / 'build'
   >>> log_dir = work_dir / 'log'

Now we can build checkout and build tasks for this repository:

   >>> from valjean.cosette.code import CheckoutTask, BuildTask
   >>> from pprint import pprint
   >>> ct = CheckoutTask(name='project_checkout',
   ...                   repository=repo_dir,
   ...                   checkout_root=checkout_dir,
   ...                   log_root=log_dir)
   >>> bt = BuildTask(name='project_build',
   ...                source=ct,
   ...                build_root=build_dir,
   ...                build_flags=['--' ,'-j4'],
   ...                log_root=log_dir)

Note how we passed the `ct` object directly to the `source` argument of the
:class:`BuildTask` constructor: we are telling the :class:`BuildTask` to look
for the sources to build in the checkout directory. You can also pass a normal
path to the `source` argument instead.

   >>> from valjean.cosette.env import Env
   >>> env = Env()
   >>> ct_up, ct_status = ct.do(env, config=None)
   >>> print(ct_status)
   TaskStatus.DONE
   >>> pprint(ct_up)
   {'project_checkout': {'checkout_log': '.../log/project_checkout.log',
                         'elapsed_time': ...,
                         'output_dir': '.../checkout/project_checkout',
                         'repository': '.../repo'}}
   >>> env.apply(ct_up)  # apply CheckoutTask's environment update
   ...                   # for this example, this is actually optional
   >>> bt_up, bt_status = bt.do(env=env, config=None)
   >>> print(bt_status)
   TaskStatus.DONE
   >>> pprint(bt_up)
   {'project_build': {'build_log': '.../log/project_build.log',
                      'elapsed_time': ...,
                      'output_dir': '.../build/project_build'}}
"""

import os
import logging

from ..path import ensure
from ..chrono import Chrono
from .run import run
from .task import TaskStatus
from .pythontask import PythonTask
from .. import LOGGER


class CheckoutTask(PythonTask):
    '''Task to check out code from a version-control system.  The actual code
    checkout is performed when the task is executed.
    '''

    # pylint: disable=too-many-arguments
    def __init__(self, name, *, repository, checkout_root=None, log_root=None,
                 flags=None, ref=None, vcs='git', deps=None, soft_deps=None):
        '''Construct a :class:`CheckoutTask`.

        :param str name: The name of this task.
        :param str checkout_root: The directory where the code will be checked
                                  out, or `None` for the configuration default.
        :param str repository: The repository for checkout.
        :param str log_root: The path to the log directory, or `None` for the
                             configuration default.
        :param flags: The flags to be used at checkout time, as a list of
                      strings.
        :type flags: list(str) or None
        :param ref: The reference to check out.
        :type ref: str or None
        :param vcs: The version-control system to use. Must be one of:
                    ``'git'`` (default), ``'svn'``, ``'cvs'``, ``'copy'``.
        :type vcs: str or None
        :param deps: The dependencies for this task (see
               :meth:`Task.__init__() <valjean.cosette.task.Task.__init__>`
               for the format), or `None`.
        :type deps: list(Task) or None
        :param soft_deps: The soft dependencies for this task (see
               :meth:`Task.__init__() <valjean.cosette.task.Task.__init__>`
               for the format), or `None`.
        :type soft_deps: list(Task) or None
        '''
        self.checkout_root = checkout_root
        self.log_root = log_root

        if vcs == 'git':
            if ref is None:
                ref = 'master'

            def checkout_vcs(checkout_dir, log):
                clone_cli = [self.GIT, 'clone']
                if flags is not None:
                    clone_cli.extend(flags)
                clone_cli.extend(['--', str(repository), str(checkout_dir)])
                ret, status, _ = run([clone_cli], stdout=log, stderr=log)
                if ret[-1] != 0:
                    LOGGER.debug('`git clone` returned %s', ret)
                    return status
                checkout_cli = [self.GIT, 'checkout', ref]
                ret, status, _ = run([checkout_cli], stdout=log, stderr=log,
                                     cwd=str(checkout_dir))
                if ret[-1] != 0:
                    LOGGER.debug('`git checkout` returned %s', ret)
                return status
        elif vcs == 'svn':
            raise NotImplementedError('SVN checkout not implemented yet')
        elif vcs == 'cvs':
            raise NotImplementedError('CVS checkout not implemented yet')
        elif vcs == 'copy':
            raise NotImplementedError('copy checkout not implemented yet')
        else:
            raise ValueError('unrecognized VCS: {}'.format(vcs))

        def checkout(*, config):
            # setup log dir and file
            if self.log_root is None:
                self.log_root = config.query('path', 'log-root')
            log_file = ensure(self.log_root, self.name + '.log')
            ensure(log_file)

            # setup checkout dir
            if self.checkout_root is None:
                self.checkout_root = config.query('path', 'output-root')
            checkout_dir = ensure(self.checkout_root, self.name, is_dir=True)

            chrono = Chrono()
            with log_file.open('w') as log:
                with chrono:
                    status = checkout_vcs(checkout_dir, log)

            if status != TaskStatus.DONE:
                LOGGER.warning('CheckoutTask %s did not succeed (status: %s)',
                               self.name, status)
                if LOGGER.isEnabledFor(logging.DEBUG):
                    with log_file.open() as log:
                        LOGGER.debug('checkout log:\n%s', log.read())

            env_up = {self.name: {'checkout_log': str(log_file),
                                  'output_dir': str(checkout_dir),
                                  'repository': str(repository),
                                  'elapsed_time': float(chrono)}}
            return env_up, status

        super().__init__(name, checkout, deps=deps, soft_deps=soft_deps,
                         config_kwarg='config')

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)

    #: Path to the :file:`git` executable. May be overridden before class
    #: instantiation.
    GIT = 'git'


class BuildTask(PythonTask):
    '''Task to build an existing source tree. The build is actually performed
    when the task is executed.
    '''

    # pylint: disable=too-many-arguments
    def __init__(self, name, source, *, build_root=None, log_root=None,
                 targets=None, build_system='cmake', configure_flags=None,
                 build_flags=None, deps=None, soft_deps=None):
        '''Construct a :class:`BuildTask`.

        :param str name: The name of this task.
        :param str source: The path to the directory containing the sources, or
                           a :class:`CheckoutTask` object (in which case the
                           checkout directory will be assumed to contain the
                           sources).
        :param str build_root: The path to the build directory (a subdirectory
                               will be created).
        :param str log_root: The path to the log directory.
        :param targets: A list of targets to build, or `None` for the default
                        target.
        :type targets: list(str) or None
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
                     :meth:`Task.__init__()
                     <valjean.cosette.task.Task.__init__>` for the type), or
                     `None`.
        :type deps: list(Task) or None
        :param soft_deps: The soft dependencies for this task (see
                          :meth:`Task.__init__()
                          <valjean.cosette.task.Task.__init__>` for the type),
                          or `None`.
        :type soft_deps: list(Task) or None
        '''
        assert isinstance(source, (str, CheckoutTask))
        LOGGER.debug('BuildTask %s will look for source files in %s',
                     name, source)

        if deps is None:
            deps = []
        if isinstance(source, CheckoutTask):
            deps.append(source)

        self.log_root = log_root
        self.build_root = build_root

        if build_system == 'cmake':
            build_sys = self.cmake_build_sys(targets, configure_flags,
                                             build_flags)
        elif build_system in ('autoconf', 'configure'):
            raise NotImplementedError('configure build not implemented yet')
        else:
            raise ValueError('unrecognized build system: {}'
                             .format(build_system))

        def build(*, config, env):
            # setup log dir and files
            if self.log_root is None:
                self.log_root = config.query('path', 'log-root')
            log_file = ensure(self.log_root, self.name + '.log')
            ensure(log_file)

            # setup build dir
            if self.build_root is None:
                self.build_root = config.query('path', 'output-root')
            build_dir = (ensure(self.build_root, self.name, is_dir=True)
                         .resolve())

            if isinstance(source, str):
                source_dir = os.path.abspath(source)
            else:
                source_dir = os.path.abspath(env[source.name]['output_dir'])

            chrono = Chrono()
            with chrono:
                with log_file.open('w') as log:
                    status = build_sys(source_dir, build_dir, log)

            if status != TaskStatus.DONE:
                LOGGER.warning('BuildTask %s did not succeed (status: %s)',
                               self.name, status)
                if LOGGER.isEnabledFor(logging.DEBUG):
                    with log_file.open() as log:
                        LOGGER.debug('build log:\n%s', log.read())

            env_up = {self.name: {'build_log': str(log_file),
                                  'output_dir': str(build_dir),
                                  'elapsed_time': float(chrono)}}
            return env_up, status

        super().__init__(name, build, deps=deps, soft_deps=soft_deps,
                         env_kwarg='env', config_kwarg='config')

        LOGGER.debug('Created %s task %r', self.__class__.__name__, self.name)

    def cmake_build_sys(self, targets, configure_flags, build_flags):
        '''Return a function that builds a project using cmake.'''

        def build_sys(source_dir, build_dir, log):
            '''Build a project using cmake.'''
            configure_cli = [self.CMAKE]
            if configure_flags is not None:
                configure_cli.extend(configure_flags)
            configure_cli.append(source_dir)
            ret, status, _ = run([configure_cli], stdout=log, stderr=log,
                                 cwd=str(build_dir))
            if ret[-1] != 0:
                LOGGER.debug('`cmake` (configure step) returned %s', ret)
                return status
            build_cli = [self.CMAKE, '--build', str(build_dir)]
            target_list = [] if targets is None else targets
            for target in target_list:
                build_cli.append('--target')
                build_cli.append(target)
            if build_flags is not None:
                build_cli.extend(build_flags)
            ret, status, _ = run([build_cli], stdout=log, stderr=log,
                                 cwd=str(build_dir))
            if ret[-1] != 0:
                LOGGER.debug('`cmake` (build step) returned %s', ret)
            return status
        return build_sys

    #: Path to the :file:`cmake` executable. May be overridden before class
    #: instantiation.
    CMAKE = 'cmake'
