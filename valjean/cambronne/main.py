'''Main :program:`valjean` executable.'''

import sys
import argparse
import pkgutil
import importlib
import logging

from . import commands
from .. import LOGGER, LOG_FILE_FORMAT, __version__
from ..config import Config


def main(argv=None):
    '''Main entry point for the :program:`valjean` executable.'''
    if argv is None:
        argv = sys.argv[1:]

    parser = make_parser()
    args = parser.parse_args(argv)

    config = process_options(args)

    LOGGER.info('vajean %s', __version__)
    LOGGER.info('run starts...')
    if hasattr(args, 'func'):
        # collect stuff from valjean.py
        job_file = config.get('path', 'job-file')
        priority = getattr(args.func.__self__, 'PRIORITY', None)
        collected_tasks = _collect_tasks(priority, job_file, args.job_args)
        args.func(args, collected_tasks, config)
    else:
        parser.print_help()
    LOGGER.info('...finished!')


def _collect_tasks(priority, job_file, job_args):
    from ..dyn_import import dyn_import
    try:
        module = dyn_import(job_file)
    except FileNotFoundError:
        LOGGER.fatal('Cannot find job file %s', job_file)
        sys.exit(1)

    try:
        collected_tasks = [obj for obj in module.job(*job_args)
                           if priority is None or obj.PRIORITY <= priority]
    except TypeError as err:
        if str(err).startswith('job()'):
            import inspect
            signature = inspect.getfullargspec(module.job)
            n_args = len(signature.args)
            new_msg = ('This valjean job expects exactly {} -a/--args '
                       'option(s)'.format(n_args))
            err = TypeError(new_msg)
        raise err
    LOGGER.debug('collected tasks: %s', collected_tasks)
    return collected_tasks


def make_parser():
    '''Construct the argument parser.'''
    parser = argparse.ArgumentParser(prog='valjean')

    # -V/--version
    version_string = '%(prog)s ' + __version__
    parser.add_argument('-V', '--version', action='version',
                        version=version_string,
                        help='show the code version number and exit')
    parser.add_argument('-v', '--verbose', action='count',
                        help='increase verbosity')
    parser.add_argument('-c', '--config', action='append',
                        help='use the specified configuration file; '
                        'may be specified multiple times')
    parser.add_argument('-l', '--log', help='path to the log file')
    parser.add_argument('-a', '--args', action='append',
                        default=[], dest='job_args',
                        help='arguments that will be passed to the job() '
                        'function; may be specified multiple times')
    parser.add_argument('--env-path', action='store', default='valjean.env',
                        help='path to the file containing the persistent '
                        'environment (default: valjean.env)')
    parser.add_argument('--env-skip-read', action='store_true',
                        help='do not read the environment from the path '
                        'specified by --env_path at the beginning of the run')
    parser.add_argument('--env-skip-write', action='store_true',
                        help='do not write the environment to the path '
                        'specified by --env_path at the end of the run')
    parser.add_argument('--env-format', action='store',
                        choices=('json', 'pickle'), default='json',
                        help='environment persistency format')

    # here come the subcommands
    cmd_parsers = parser.add_subparsers(title='Valid commands',
                                        dest='command_name')

    # import each submodule in commands.* and create a new subparser for it
    prefix = commands.__name__ + '.'
    submods_iter = pkgutil.iter_modules(commands.__path__)
    for _, modname, _ in submods_iter:
        cmd_name = modname.capitalize() + 'Command'
        module = importlib.import_module(prefix + modname)
        cmd_cls = getattr(module, cmd_name)
        cmd = cmd_cls()
        cmd_parser = cmd_parsers.add_parser(cmd_cls.NAME,
                                            help=cmd_cls.HELP,
                                            aliases=cmd_cls.ALIASES)
        cmd.register(cmd_parser)

    return parser


def process_options(args):
    '''Process the parsed options.

    :returns: The configuration.'''

    # configuration file
    config = Config(paths=args.config)

    # verbosity
    if args.verbose is not None:
        if args.verbose >= 1:
            log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    LOGGER.setLevel(log_level)
    for handler in LOGGER.handlers:
        handler.setLevel(log_level)

    # log to file
    if args.log is not None:
        formatter = logging.Formatter(LOG_FILE_FORMAT,
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(args.log)
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        LOGGER.addHandler(handler)

    return config
