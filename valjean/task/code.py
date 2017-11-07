# -*- coding: utf-8 -*-
u'''Tasks for checking out and building code.

This module contains a few useful tasks for checking out, configuring,
compiling and running arbitrary code.

.. todo::

   Implement ``svn`` and ``cvs`` checkout.
'''

from .task import ShellTask

'''Path to the git executable.'''
GIT = 'git'


class CheckoutTask(ShellTask):
    '''Task to check out code from a version-control system.  The actual code
    checkout is performed when the task is executed.

    :param str name: The name of this task.
    :param str repository: The path to the code repository.
    :param ref: The name of the reference to check out. For instance, it may be
                a branch name or a hash for ``git`` repositories. If ``None``
                is given, the default will be used (``master`` for ``git``, the
                trunk for ``svn`` or ``cvs``, etc.).
    :type ref: None or str
    :param str checkout_dir: The path to the checkout directory.
    :param str flags: Any additional flag (as a string) to be passed to the
                      checkout/clone command.
    :param str vcs: The version-control system to use. Must be one of: ``git``.
    '''

    _git_template = r'''{git} clone {flags} -- {repository} {checkout_dir}
                        {git} -C {checkout_dir} checkout {ref}'''

    def __init__(self, name: str, repository: str, ref=None, checkout_dir=None,
                 flags=None, vcs='git'):
        if vcs == 'git':
            _flags = flags if flags is not None else ''
            _ref = ref if ref is not None else 'master'
            script = self._git_template.format(git=GIT, flags=_flags,
                                               repository=repository,
                                               checkout_dir=checkout_dir,
                                               ref=_ref)
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
        '''Check out the code as specified. This method populates the
        ``env['tasks']`` argument with the execution result/time of the
        underlying checkout shell script (see :class:`.ExecuteTask`). In
        addition, it sets the following fields::

            env['checkout'][task.name]['checkout_dir'] = checkout_dir
            env['checkout'][task.name]['repository'] = repository

        This allows later tasks to retrieve the location of the source files
        and e.g. build the code.
        '''

        super().do(env)
        env.setdefault('checkout', {}).setdefault(self.name, {})
        if env['tasks'][self.name]['return_code'] == 0:
            env['checkout'][self.name]['checkout_dir'] = self.checkout_dir
            env['checkout'][self.name]['repository'] = self.repository


class CodeBuildTask(ShellTask):

    pass
