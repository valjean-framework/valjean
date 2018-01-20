'''Main :program:`valjean` executable.'''

import sys
import argparse
import pkgutil
import importlib
import logging

import valjean
import valjean.cambronne
import valjean.cambronne.commands
from valjean import LOGGER
from ..config import Config


def main(argv=None):
    '''Main entry point for the :program:`valjean` executable.'''
    if argv is None:
        argv = sys.argv[1:]

    parser = make_parser()
    args = parser.parse_args(argv)

    config = process_options(args)

    LOGGER.info('vajean %s', valjean.__version__)
    LOGGER.info('run starts...')
    if hasattr(args, 'func'):
        args.func(args, config)
    else:
        parser.print_help()
    LOGGER.info('...finished!')


def make_parser():
    '''Construct the argument parser.'''
    parser = argparse.ArgumentParser(prog='valjean')

    # -V/--version
    version_string = '%(prog)s ' + valjean.__version__
    parser.add_argument(
        '-V', '--version', action='version',
        version=version_string, help='show the code version number and exit'
        )
    parser.add_argument(
        '-v', '--verbose', action='count',
        help='increase verbosity'
        )
    parser.add_argument(
        '-c', '--config', action='append',
        help='use the specified configuration file; '
        'may be specified multiple times'
        )
    parser.add_argument(
        '-l', '--log',
        help='path to the log file'
        )
    parser.add_argument(
        '--env-path', action='store', default='valjean.env',
        help='path to the file containing the persistent environment '
             '(default: valjean.env)'
        )
    parser.add_argument(
        '--env-skip-read', action='store_true',
        help='do not read the environment from the path specified by '
             '--env_path at the beginning of the run'
        )
    parser.add_argument(
        '--env-skip-write', action='store_true',
        help='do not write the environment to the path specified by '
             '--env_path at the end of the run'
        )
    parser.add_argument(
        '--env-format', action='store',
        choices=('json', 'pickle'),
        default='json',
        help='environment persistency format'
        )

    # here come the subcommands
    cmd_parsers = parser.add_subparsers(
        title='Valid commands',
        dest='command_name'
        )

    # import each submodule in commands.* and create a new subparser for it
    prefix = valjean.cambronne.commands.__name__ + '.'
    submods_iter = pkgutil.iter_modules(valjean.cambronne.commands.__path__)
    for _, modname, _ in submods_iter:
        cmd_name = modname.capitalize() + 'Command'
        module = importlib.import_module(prefix + modname)
        cmd_cls = getattr(module, cmd_name)
        cmd = cmd_cls()
        cmd_parser = cmd_parsers.add_parser(
            cmd_cls.NAME,
            help=cmd_cls.HELP,
            aliases=cmd_cls.ALIASES
            )
        cmd.register(cmd_parser)

    return parser


def process_options(args):
    '''Process the parsed options.

    :returns: The configuration.'''

    # configuration file
    config = Config(paths=args.config)

    # verbosity
    if args.verbose is not None:
        if args.verbose == 1:
            log_level = logging.INFO
        elif args.verbose > 1:
            log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    LOGGER.setLevel(log_level)
    for handler in LOGGER.handlers:
        handler.setLevel(log_level)

    # log to file
    if args.log is not None:
        formatter = logging.Formatter(valjean.LOG_FILE_FORMAT,
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(args.log)
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        LOGGER.addHandler(handler)

    return config
