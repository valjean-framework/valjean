# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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

'''Top-level module for the valjean package.'''

import logging
import sys
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'


class ValjeanFormatter:
    '''Custom formatter for log messages.

    This formatter class uses a different format for the ``INFO`` message
    level.
    '''

    def __init__(self, info_fmt, fmt):
        '''Initialize the formatter.

        :param str info_fmt: The format string for the ``INFO`` level.
        :param str fmt: The format string for the other message levels.
        '''
        self.info_formatter = logging.Formatter(info_fmt)
        self.formatter = logging.Formatter(fmt)

    def format(self, record):
        '''Format the given record.'''
        if record.levelno == logging.INFO:
            return self.info_formatter.format(record)
        return self.formatter.format(record)


def _configure_logger(logger):
    default_level = logging.INFO
    _formatter = ValjeanFormatter(LOG_INFO_CONSOLE_FORMAT, LOG_CONSOLE_FORMAT)
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(_formatter)
    _handler.setLevel(default_level)
    logger.addHandler(_handler)
    logger.setLevel(default_level)


LOGGER = logging.getLogger('valjean')
LOG_INFO_CONSOLE_FORMAT = '* %(message)s'
LOG_CONSOLE_FORMAT = '%(levelname)9.9s %(module)12.12s: %(message)s'
LOG_FILE_FORMAT = ('%(levelname)9.9s (%(module)10.10s/%(funcName)12.12s) '
                   '%(asctime)19s: %(message)s')
_configure_logger(LOGGER)


def set_log_level(level):
    '''Set the verbosity level for the default logger.'''
    LOGGER.setLevel(level)
    for handler in LOGGER.handlers:
        handler.setLevel(level)
