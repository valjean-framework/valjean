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
