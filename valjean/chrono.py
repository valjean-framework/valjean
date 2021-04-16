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

'''This module provides the :class:`~.Chrono` context manager.'''

import time


class Chrono:
    '''Time some code and store the elapsed time.

    This class is a simple context manager that measures the execution time of
    a code fragment. The elapsed time is stored as a float in `self.elapsed`
    and can be accessed as such.

    Examples:

    >>> with Chrono() as chrono:
    ...     print(42)
    42
    >>> print('printing 42 took {} seconds'.format(chrono))
    printing 42 took ... seconds
    '''

    def __init__(self):
        self._start = None
        self.elapsed = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.elapsed = time.perf_counter() - self._start
        self._start = None

    def __str__(self):
        '''Return the elapsed time, as a string.'''
        return str(self.elapsed)

    def __float__(self):
        '''Return the elapsed time, as a float.'''
        return float(self.elapsed)

    def __int__(self):
        '''Return the elapsed time, as an int.'''
        return int(self.elapsed)

    def __format__(self, format_spec):
        '''Return the elapsed time, formatted according to `format_spec`.

        >>> chrono = Chrono()
        >>> chrono.elapsed = 1e-6
        >>> '{}'.format(chrono)
        '1e-06'
        >>> '{:f}'.format(chrono)
        '0.000001'
        '''
        return format(self.elapsed, format_spec)
