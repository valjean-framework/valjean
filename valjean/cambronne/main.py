# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''Main :program:`valjean` executable.'''

import sys
import argparse
import pkgutil
import importlib
import logging

from . import commands
from .. import LOG_FILE_FORMAT, __version__
from ..config import Config
from ..path import ensure


LOGGER = logging.getLogger(__name__)


def main(argv=None):
    '''Main entry point for the :program:`valjean` executable.'''
    if argv is None:
        argv = sys.argv[1:]
    LOGGER.debug('arguments: %s', argv)

    parser = make_parser()
    args = parser.parse_args(argv)
    LOGGER.debug('parsed args: %s', args)

    config = process_options(args)

    if hasattr(args, 'func'):
        # collect the tasks and call the processing function
        args.func(args, config)
    else:
        parser.print_help()


def make_parser():
    '''Construct the argument parser.'''
    parser = argparse.ArgumentParser(
        prog='valjean',
        description='VALidation, Journal d’Évolution et ANalyse',
        epilog='You can pass the -h/--help option to the subcommands to get '
        'specific help.')

    # -V/--version
    version_string = '%(prog)s ' + __version__
    parser.add_argument('-V', '--version', action='version',
                        version=version_string,
                        help='show the code version number and exit')
    parser.add_argument('-v', '--verbose', action='count',
                        help='increase verbosity')
    parser.add_argument('-c', '--config', action='store',
                        help='use the specified configuration file')
    parser.add_argument('-l', '--log', help='path to the log file')

    # here come the subcommands
    cmd_parsers = parser.add_subparsers(title='Valid commands',
                                        dest='command_name')

    # import each submodule in commands.* and create a new subparser for it
    prefix = commands.__name__ + '.'
    submods_iter = pkgutil.iter_modules(commands.__path__)
    cmd_objs = []
    for _, modname, _ in submods_iter:
        cmd_name = modname.capitalize() + 'Command'
        LOGGER.debug('registering new command %s from class %s',
                     modname, cmd_name)
        module = importlib.import_module(prefix + modname)
        cmd_cls = getattr(module, cmd_name)
        cmd_obj = cmd_cls()
        cmd_objs.append(cmd_obj)

    for cmd_obj in cmd_objs:
        cmd_parser = cmd_parsers.add_parser(cmd_obj.NAME,
                                            help=cmd_obj.HELP,
                                            description=cmd_obj.DESC,
                                            aliases=cmd_obj.ALIASES)
        cmd_obj.register(cmd_parser)

    return parser


def process_options(args):
    '''Process the parsed options.

    :returns: The configuration.'''
    # pylint: disable=possibly-used-before-assignment
    # configuration file
    if args.config is not None:
        config = Config.from_file(args.config)
    else:
        config = Config()

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
        ensure(args.log)
        handler = logging.FileHandler(args.log)
        handler.setFormatter(formatter)
        handler.setLevel(log_level)
        LOGGER.addHandler(handler)

    return config
