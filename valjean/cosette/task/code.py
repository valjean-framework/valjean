# -*- coding: utf-8 -*-
u'''Tasks for checking out and building code.

This submodule contains a few useful tasks for checking out, configuring, and
building arbitrary code.

The :class:`CheckoutTask` task class checks out a version-controlled
repository. For the moment, only ``git`` repositories are supported. The path
to the ``git`` executable may be specified through the :data:`GIT` module
variable.

.. todo::

   Implement ``svn`` and ``cvs`` checkout.

The :class:`BuildTask` task class builds code from a given source directory. A
build directory must also be specified and will be created if necessary. For
the moment, :class:`BuildTask` only supports ` ``cmake`` builds, but there are
plans to add support for ``autoconf``/``configure``/``make`` builds. The path
to the ``cmake`` executable may be specified through the :data:`CMAKE` module
variable.

.. todo::

   Implement ``autoconf``/``configure``/``make`` builds.

An example of the usage of :class:`CheckoutTask` and :class:`BuildTask`:

.. testsetup:: task.code

   from valjean.cosette.task.code import CheckoutTask, BuildTask

.. doctest:: task.code

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
   >>> env = {}
   >>> ct_up = ct.do({})  # doctest: +SKIP
   >>> pprint(ct_up) # doctest: +SKIP
   {'checkout': {'project_checkout': {'checkout_dir': \
'/path/to/test_project/src',
                                      'checkout_log': \
'/path/to/test_project/checkout_project_checkout.log',
                                      'repository': '/path/to/project.git'}},
    'tasks': {'project_checkout': {'return_code': 0,
                                   'wallclock_time': 0.34877443313598633}}}
   >>> bt_up = bt.do({})  # doctest: +SKIP
   >>> pprint(bt_up) # doctest: +SKIP
   {'build': {'project_build': {'build_log': \
'/path/to/test_project/build_project_build.log',
                                'configure_log': \
'/path/to/test_project/configure_project_build.log'}},
    'tasks': {'project_build': {'return_code': 0,
                                'wallclock_time': 173.11953258514404}}}
'''

import logging
import os
from .task import ShellTask


logger = logging.getLogger(__name__)


def _q(string):
    '''Quote a string so that it is correctly interpreted by shell scripts.'''
    import shlex
    if len(string) == 0:
        return string
    return shlex.quote(string)


def _sq(string):
    '''Split a string, quote the pieces and put everything back together.'''
    import shlex
    if len(string) == 0:
        return string
    return ' '.join(map(shlex.quote, shlex.split(string)))


#: Path to the git executable.
GIT = 'git'


class CheckoutTask(ShellTask):
    '''Task to check out code from a version-control system.  The actual code
    checkout is performed when the task is executed.

    :param str name: The name of this task.
    :param str repository: The path to the code repository.
    :param str checkout_dir: The path to the checkout directory.
    :param str log_dir: The path to the directory containing log files.
    :param ref: The name of the reference to check out. For instance, it may be
                a branch name or a hash for ``git`` repositories. If ``None``
                is given, the default will be used (``master`` for ``git``, the
                trunk for ``svn`` or ``cvs``, etc.).
    :type ref: None or str
    :param str flags: Any additional flag (as a string) to be passed to the
                      checkout/clone command.
    :param str vcs: The version-control system to use. Must be one of:
                    ``'git'``.
    '''

    _git_template = r'''test -d {checkout_dir} || mkdir -p {checkout_dir}
{{
    {git} clone {flags} -- {repository} {checkout_dir}
    {git} -C {checkout_dir} checkout {ref}
}} >{checkout_log} 2>&1'''

    def __init__(self,
                 name: str,
                 repository: str,
                 checkout_dir: str,
                 log_dir: str,
                 ref=None,
                 flags=None,
                 vcs='git'):
        self.checkout_log = os.path.join(
            os.path.expanduser(log_dir),
            self.sanitize_filename('checkout_' + name + '.log')
            )
        if vcs == 'git':
            _flags = flags if flags is not None else ''
            _ref = ref if ref is not None else 'master'
            script = self._git_template.format(
                git=_q(GIT),
                flags=_sq(_flags),
                repository=_q(repository),
                checkout_dir=_q(checkout_dir),
                ref=_q(_ref),
                checkout_log=_q(self.checkout_log)
                )
        elif vcs == 'svn':
            raise NotImplementedError('SVN checkout not implemented yet')
        elif vcs == 'cvs':
            raise NotImplementedError('CVS checkout not implemented yet')
        else:
            raise ValueError('unrecognized VCS: {}'.format(vcs))
        super().__init__(name, script)
        self.checkout_dir = checkout_dir
        self.repository = repository
        logger.info('Created %s task %s', self.__class__.__name__, self.name)
        logger.info('  - repository = %s', self.repository)
        logger.info('  - checkout_log = %s', self.checkout_log)
        logger.info('  - checkout_dir = %s', self.checkout_dir)

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

        env_up = super().do(env)
        env_up.setdefault('checkout', {}).setdefault(self.name, {})
        env_up['checkout'][self.name]['checkout_dir'] = self.checkout_dir
        env_up['checkout'][self.name]['repository'] = self.repository
        env_up['checkout'][self.name]['checkout_log'] = self.checkout_log
        return env_up


#: Path to the cmake executable.
CMAKE = 'cmake'


class BuildTask(ShellTask):
    '''Task to build an existing source tree. The build is actually performed
    when the task is executed.

    :param str name: The name of this task.
    :param str source_dir: The path to the source tree.
    :param str build_dir: The path to the build directory. If it does not
                          exist, it will be created.
    :param str log_dir: The path to the directory containing log files.
    :param configure_flags: Flags to be passed to the build tool at
                            configuration time.
    :type configure_flags: None or str
    :param str build_flags: Flags to be passed to the build tool at build time.
    :type build_flags: None or str
    :param str build_target: Name of the target to build.
    :type build_target: None or str
    :param str build_system: Name of the build tool to use. Must be one of:
                             ``'cmake'``.
    '''

    _cmake_template = r'''test -d {build_dir} || mkdir -p {build_dir}
cd {build_dir}
{cmake} {cflags} {source_dir} >{configure_log} 2>&1
{cmake_build_commands}'''

    _cmake_build_template = (r'''{cmake} --build {build_dir} {target_flag} '''
                             '''{bflags} >{build_log} 2>&1''')

    def __init__(self,
                 name: str,
                 source_dir: str,
                 build_dir: str,
                 log_dir: str,
                 configure_flags=None,
                 build_flags=None,
                 build_targets=None,
                 build_system='cmake'):
        _cflags = configure_flags if configure_flags is not None else ''
        _bflags = build_flags if build_flags is not None else ''
        self.configure_log = os.path.join(
            os.path.expanduser(log_dir),
            self.sanitize_filename('configure_' + name + '.log'))
        self.build_log = os.path.join(
            os.path.expanduser(log_dir),
            self.sanitize_filename('build_' + name + '.log')
            )
        _build_targets = [None] if build_targets is None else build_targets
        if build_system == 'cmake':

            format_env = {
                'cmake': _q(CMAKE),
                'source_dir': _q(source_dir),
                'build_dir': _q(build_dir),
                'bflags': _sq(_bflags),
                'cflags': _sq(_cflags),
                'configure_log': _q(self.configure_log),
                'build_log': _q(self.build_log)
                }

            cmake_build_list = []
            for target in _build_targets:
                _target_flag = '' if target is None else '--target ' + target
                cmake_build_command = self._cmake_build_template.format(
                    target_flag=_target_flag,
                    **format_env)
                cmake_build_list.append(cmake_build_command)
            cmake_build_commands = '\n'.join(cmake_build_list)
            format_env['cmake_build_commands'] = cmake_build_commands

            script = self._cmake_template.format(**format_env)

        elif build_system == 'autoconf' or build_system == 'configure':
            raise NotImplementedError('configure build not implemented yet')
        super().__init__(name, script)
        logger.info('Created %s task %s', self.__class__.__name__, self.name)
        logger.info('  - source_dir = %s', source_dir)
        logger.info('  - build_dir = %s', build_dir)
        logger.info('  - configure_log = %s', self.configure_log)
        logger.info('  - build_log = %s', self.build_log)

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

        env_up = super().do(env)
        env_up.setdefault('build', {}).setdefault(self.name, {})
        env_up['build'][self.name]['configure_log'] = self.configure_log
        env_up['build'][self.name]['build_log'] = self.build_log
        return env_up
