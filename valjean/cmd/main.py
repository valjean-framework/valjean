'''Main :program:`valjean` executable.'''

import sys
import argparse
import importlib
import logging

import valjean
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
        '--start-from', action='store', metavar='PHASE',
        help='start execution from the given phase'
        )

    # here come the subcommands
    # WARNING: some code downstream assumes that no aliases are used
    cmd_parsers = parser.add_subparsers(
        title='Valid commands',
        dest='command_name'
        )
    cmd_parsers.add_parser(
        'config', help='inspect the configuration'
        )
    cmd_parsers.add_parser(
        'checkout', help='checkout code'
        )
    cmd_parsers.add_parser(
        'build', help='build code'
        )

    # inspect the added commands; for each command, import the corresponding
    # submodule and fill its parser
    for cmd, cmd_parser in cmd_parsers.choices.items():
        module = importlib.import_module('..{}'.format(cmd), __name__)
        cmd_name = '{}Command'.format(cmd.capitalize())
        cmd_cls = getattr(module, cmd_name)
        cmd = cmd_cls()
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
