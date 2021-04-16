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

# pylint: disable=no-value-for-parameter
'''Fixtures for the :mod:`~.valjean` tests.'''

import string
import logging

import py
import pytest
from hypothesis import assume
from hypothesis.strategies import text, dictionaries, composite

from .context import valjean  # pylint: disable=unused-import
# pylint: disable=wrong-import-order
from valjean.config import Config


IDS = text(string.ascii_letters + string.digits + '-_', min_size=1)


###########################
#  Hypothesis strategies  #
###########################

@composite
def configs(draw, keys=IDS, vals=IDS, sec_names=IDS,
            min_size=0, max_size=5):
    # pylint: disable=too-many-arguments
    '''Composite Hypothesis strategy to generate Config objects.'''
    secs = dictionaries(keys, vals, min_size=min_size, max_size=max_size)
    as_dict = draw(dictionaries(sec_names, secs,
                                min_size=min_size, max_size=max_size))
    assume('path' not in as_dict)
    conf = Config(as_dict)
    return conf


#####################
#  pytest fixtures  #
#####################

@pytest.fixture(scope='function')
def empty_config():
    '''Return an empty :class:`~.Config` object.'''
    return Config()


@pytest.fixture(scope='function')
def config_tmp(tmp_path_factory):
    '''Create a configuration object with the path options set to temporary
    directories.'''
    work_dir = tmp_path_factory.mktemp('work')
    config = Config({'path': {'log-root': str(work_dir / 'log'),
                              'output-root': str(work_dir / 'output'),
                              'report-root': str(work_dir / 'report')}})
    return config


def foreach_data(*args, **kwargs):
    '''Decorator that parametrizes a test function over files in the data
    directory for the current tests.

    Assume that the following snippet resides in
    :file:`tests/submod/test_submod.py`::

        @foreach_data('datafile')
        def test_something(datafile):
            pass

    When `pytest` imports :file:`test_submod.py`, it will parametrize
    the `datafile` argument to :func:`!test_something` over all the files
    present in :file:`tests/submod/data/`.

    If you wish to filter away some of the files, you can use the alternative
    syntax::

        @foreach_data(datafile=lambda path: str(path).endswith('.txt'))
        def test_something(datafile):
            pass

    Here the argument to the `datafile` keyword argument is a predicate that
    must return `True` if `path` is to be parametrized over, and `False`
    otherwise. Note that the `path` argument to the lambda is a
    :class:`py._path.local.LocalPath` object.  In this example, `pytest` will
    parametrize :func:`!test_something` only over files whose name ends in
    ``'.txt'``.
    '''

    if args:
        assert len(args) == 1, ('Only one positional argument allowed '
                                'to @foreach_data')
        assert not kwargs, ('No kwargs allowed with a positional '
                            'argument to @foreach_data')
        fix_name = args[0]
        fil = None
    else:
        assert len(kwargs) == 1, 'Only one kwarg allowed in @foreach_data'
        fix_name, fil = next(iter(kwargs.items()))

    def _decorator(wrapped):
        from inspect import getfile
        module_dir = py.path.local(getfile(wrapped))
        test_dir = module_dir.dirpath('data')
        datafiles = [path for path in test_dir.listdir(fil=fil)
                     if path.isfile()]
        ids = [str(path.basename) for path in datafiles]
        return pytest.mark.parametrize(fix_name, datafiles, ids=ids)(wrapped)
    return _decorator


class CaptureLogHandler(logging.NullHandler):
    '''A logger handler that keeps track of all the logging records it has
    seen. Useful for testing.'''

    def __init__(self):
        super().__init__()
        self.records = []

    def handle(self, record):
        '''Handle the given record.'''
        self.records.append(record)
        super().handle(record)

    def __contains__(self, string):
        '''Returns `True` if the given string appears in the stored records.'''
        return any(string in record.message for record in self.records)


class CaptureLog:
    '''A context manager that captures log messages directed to a logger and
    exposes them so you can analyse them.

    It works by temporarily installing a special additional handler
    (:class:`CaptureLogHandler`) in the logger and returning the handler itself
    in the `as` clause. You can use the `in` operator to look for messages:

    >>> import logging
    >>> logger = logging.getLogger('my_logger')
    >>> with CaptureLog(logger) as log_messages:
    ...     logger.warning('some log message')
    >>> 'some log message' in log_messages
    True

    You can also search the list of :class:`logging.LogRecord` objects:
    >>> log_messages.records
    [<LogRecord: my_logger, ... <doctest tests.conftest.CaptureLog[2]>, 2, \
"some log message">]
    '''
    def __init__(self, logger):
        self.logger = logger
        self.caplog_handler = None

    def __enter__(self):
        self.caplog_handler = CaptureLogHandler()
        self.logger.addHandler(self.caplog_handler)
        return self.caplog_handler

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.logger.removeHandler(self.caplog_handler)
        self.caplog_handler = None
