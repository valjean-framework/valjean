'''Module for the ``tasks`` subcommand.'''


import re
from ... import LOGGER
from ..common import Command, init_env, write_env


class TasksCommand(Command):
    '''Command class for the ``tasks`` subcommand.'''

    NAME = 'tasks'

    HELP = 'inspect and modify the task status and environment'

    def register(self, parser):
        '''Register options for this command in the parser.'''
        env_subparsers = parser.add_subparsers(title='tasks subcommands',
                                               dest='tasks_command')
        names_help = ('Print the names of the tasks in the environment to the '
                      'screen.')
        names_cmd = env_subparsers.add_parser('names', help=names_help)
        names_cmd.set_defaults(func=self.names)

        show_help = ('Print the environment to the screen. If a task name is '
                     'specified, print only the corresponding environment '
                     'section.')
        show_cmd = env_subparsers.add_parser('show', help=show_help)
        show_cmd.add_argument('name', metavar='NAME', nargs='*',
                              help='The names of the environment sections to '
                              'show, or all of them if no argument is '
                              'provided.')
        show_cmd.set_defaults(func=self.show)

        rm_help = 'Remove the given section from the environment.'
        rm_cmd = env_subparsers.add_parser('rm', help=rm_help)
        rm_cmd.add_argument('name', metavar='NAME', nargs='+',
                            help='the names of the environment sections to '
                            'delete.')
        rm_cmd.add_argument('-e', '--regexp', action='store_true',
                            help='interpret the arguments as regular '
                            'expressions')
        rm_cmd.set_defaults(func=self.remove)

    # pylint: disable=no-self-use
    def names(self, args, _collected_tasks, _config):
        '''Execute the ``tasks names`` command.'''
        # deserialize the environment
        env = init_env(path=args.env_path, skip_read=False,
                       fmt=args.env_format)

        print('\n'.join(env.keys()))

    # pylint: disable=no-self-use
    def show(self, args, _collected_tasks, _config):
        '''Execute the ``tasks show`` command.'''
        # deserialize the environment
        env = init_env(path=args.env_path, skip_read=False,
                       fmt=args.env_format)

        from pprint import pprint
        if not args.name:
            pprint(env)
            return

        for name in args.name:
            if name in env:
                pprint(env[name])
            else:
                LOGGER.error('cannot show task %s (missing from the '
                             'environment)', name)

    # pylint: disable=no-self-use
    def remove(self, args, _collected_tasks, _config):
        '''Execute the ``tasks rm`` command.'''
        # deserialize the environment
        env = init_env(path=args.env_path, skip_read=False,
                       fmt=args.env_format)
        for name in args.name:
            if args.regexp:
                regexp = re.compile(name)
                to_delete = set(task_name for task_name in env
                                if re.search(regexp, task_name))
                for task_name in to_delete:
                    LOGGER.info('deleting task %s', task_name)
                    del env[task_name]
            else:
                if name in env:
                    del env[name]
                else:
                    LOGGER.error('cannot delete task %s (missing from the '
                                 'environment)', name)
        write_env(env=env, path=args.env_path, fmt=args.env_format)
