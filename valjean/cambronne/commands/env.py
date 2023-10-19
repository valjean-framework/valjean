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

'''Module for the ``env`` subcommand.'''

import logging
from pprint import pprint

from ..common import Command
from ...cosette.env import Env


LOGGER = logging.getLogger(__name__)


class EnvCommand(Command):
    '''Command class for the ``env`` subcommand.'''

    NAME = 'env'

    HELP = 'Inspect the content of one or more serialized environment files.'

    DESC = HELP

    def register(self, parser):
        '''Register options for this command in the parser.'''
        parser.add_argument('--env-format', action='store',
                            choices=('pickle',), default='pickle',
                            help='environment persistency format')
        parser.add_argument('env_files', metavar='ENV_FILE', nargs='+',
                            help='The environment file to show.')
        parser.set_defaults(func=self.env)

    @staticmethod
    def env(args, _config):
        '''Execute the ``show-env`` command.'''
        # deserialize the environment
        for env_file in args.env_files:
            env = Env.from_file(env_file, fmt=args.env_format)
            if env is None:
                LOGGER.error('cannot show the environment for task %s',
                             env_file)
            else:
                pprint(dict(env.items()))
