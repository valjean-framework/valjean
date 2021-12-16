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

'''This module extends the functionalities provided by :mod:`~.cosette.use` to
the commonplace task of parsing Tripoli-4 output files. The decorators defined
by this module, :func:`using_parse_result` and :func:`using_browser`,
can be used to remove boilerplate code that parses and accesses the Tripoli-4
results. At the same time, they simplify the integration of user-defined
post-processing (tests) into the :mod:`valjean` workflow.

.. doctest:: eponine_use
    :hide:

    >>> # pylint: disable=trailing-whitespace,line-too-long
    >>> # noqa: E501,W291
    >>> from valjean.config import Config
    >>> config = Config()

We will need to set up a few things to show an example of how to use the
decorators. We don't want to build and run Tripoli-4 for the purpose of this
documentation, but we can mock a Tripoli-4 run by writing an existing Tripoli-4
output to a file. Here is the sample output::

    >>> example = """BATCH 10
    ... initialization time (s): 7
    ...  batch number : 10
    ... *********************************************************
    ...  RESULTS ARE GIVEN FOR SOURCE INTENSITY : 8.111452e+04
    ... *********************************************************
    ...
    ...
    ...  Mean weight leakage = 7.929746e+00	 sigma = 7.929746e+00	 sigma% = 1.000000e+02
    ...
    ...
    ...  Edition after batch number : 10
    ...
    ...
    ...
    ... ******************************************************************************
    ... RESPONSE FUNCTION : FLUX
    ... RESPONSE NAME :
    ... ENERGY DECOUPAGE NAME : DEC_SPECTRE
    ...
    ...
    ...  PARTICULE : NEUTRON
    ... ******************************************************************************
    ...
    ... 	 scoring mode : SCORE_SURF
    ... 	 scoring zone : 	 Frontier 	 volumes : 14,27
    ...
    ...
    ... 	 SPECTRUM RESULTS
    ... 	 number of first discarded batches : 0
    ...
    ... 	 group			 score		 sigma_% 	 score/lethargy
    ... Units:	 MeV			 neut.s^-1	 %		 neut.s^-1
    ...
    ... 2.000000e+01 - 1.000000e-11	1.307419e+00	8.719708e+01	1.046074e+01
    ...
    ... 	 ENERGY INTEGRATED RESULTS
    ...
    ... 	 number of first discarded batches : 0
    ...
    ... number of batches used: 10	1.307419e+00	8.719708e+01
    ...
    ...
    ...
    ...  simulation time (s) : 20
    ...
    ...
    ...  Type and parameters of random generator at the end of simulation:
    ... 	 DRAND48_RANDOM 13531 45249 20024  COUNTER	2062560
    ...
    ...
    ...  simulation time (s): 20
    ...
    ...
    ... =====================================================================
    ... 	NORMAL COMPLETION
    ... =====================================================================
    ... """

We construct a :class:`~.RunTaskFactory` that simply echoes any text passed as
an argument::

    >>> from valjean.cosette.run import RunTaskFactory
    >>> echo_factory = RunTaskFactory.from_executable('/bin/echo', name='echo',
    ...                                               default_args=['{text}'])

In the real world, the :class:`~.RunTaskFactory` would actually generate tasks
to run a Tripoli-4 executable.


Injecting the raw parse results
===============================

Now we can construct the decorator that parses the Tripoli-4 results and apply
it to a Python function::

    >>> from valjean.eponine.tripoli4 import use
    >>> using_last_parse_result = use.using_last_parse_result(echo_factory)
    >>> @using_last_parse_result(text=example)
    ... def source(results):
    ...     return results.res['batch_data']['source_intensity']

If we inspect `source`, we can see that it is a :class:`~.Use` object::

    >>> type(source)
    <class 'valjean.cosette.use.Use'>

If you are not sure what :class:`~.Use` does, this is a good moment to go and
read its documentation. Don't worry, I'll wait.

*(time passes)*

:mod:`valjean` can inspect this object and convert it into a :class:`~.Task`::

    >>> source_task = source.get_task()
    >>> type(source_task)
    <class 'valjean.cosette.pythontask.PythonTask'>
    >>> source_task.name
    '....source'

The task has explicit dependencies, which means that it will be correctly
integrated in the :mod:`valjean` dependency graph. In particular, this task
depends on a task that actually does the parsing::

    >>> source_task.depends_on
    {Task('....parse_batch_index')}
    >>> parse_task = next(iter(source_task.depends_on))

It depends on the `make_parser_task`, that scans the file and build the parser

    >>> parse_task.depends_on
    {Task('....make_parser')}
    >>> make_parser_task = next(iter(parse_task.depends_on))

and `make_parser_task` in turn depends on the :class:`~.RunTask` that was
generated by `echo_factory`::

    >>> make_parser_task.depends_on
    {Task('....echo')}
    >>> run_task = next(iter(make_parser_task.depends_on))

We manually execute the tasks in the correct order and we check that we recover
the right result at the end::

    >>> from valjean.cosette.env import Env
    >>> env = Env()
    >>> for task in [run_task, make_parser_task, parse_task, source_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[source_task.name]['result'])
    81114.52


Using a :class:`~.browser.Browser`
=============================================

The raw parse results are useful in some situations, but most of the time you
probably want to work with a higher-level representation of the calculation
result, such as a :class:`~.browser.Browser`. This module provides a function
to construct a decorator that automatically creates the :class:`~.RunTask` from
the :class:`~.RunTaskFactory`, runs the task, parses the resulting output and
wraps the parse results in an :class:`~.browser.Browser`::


    >>> using_browser = use.using_browser(echo_factory, 10)
    >>> @using_browser(text=example)
    ... def extract_simulation_time(browser):
    ...     return browser.globals['simulation_time']

We can again check that everything went as expected by manually unwrapping the
sequence of tasks and running them::

    >>> extract_task = extract_simulation_time.get_task()
    >>> browse_task = next(iter(extract_task.depends_on))
    >>> parse_task = next(iter(browse_task.depends_on))
    >>> make_parser_task = next(iter(parse_task.depends_on))
    >>> run_task = next(iter(make_parser_task.depends_on))
    >>> env = Env()
    >>> for task in [run_task, make_parser_task, parse_task,
    ...              browse_task, extract_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[extract_task.name]['result'])
    20


Module API
==========
'''

import functools
from .parse import Parser
from ...cosette.use import UseRun
from ...cosette.pythontask import TaskException
from ..tripoli4.parse import ParserException


def partial(func, *args, **kwargs):
    '''An improved version of :func:`functools.partial` that calls
    :func:`functools.update_wrapper` on the partially applied function in order
    to update its metadata (name, etc.).'''
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    return partial_func


def make_parser(filename):
    '''Create a Parser object and scan a Tripoli-4 output file.

    :param str filename: the name of the file to parse.
    :param int batch: the number of the batch to parse; see
                      :meth:`~.Parser.__init__`.
    :raises ValueError: if parsing fails.
    :returns: the parser
    :rtype: Parser
    '''
    try:
        parser = Parser(filename)
    except ParserException as tpe:
        raise TaskException(f'cannot build parser {filename}: {tpe}') from None
    return parser


def parse_batch_number(parser, *, batch_number):
    '''Parse a batch result from Tripoli-4.

    :param int batch_number: batch number
    :rtype: ParseResult
    '''
    try:
        pres = parser.parse_from_number(batch_number=batch_number)
    except ParserException as t4pe:
        raise TaskException(f'cannot parse {parser.jdd}: {t4pe}') from None
    return pres


def parse_batch_index(parser, *, batch_index=-1):
    '''Parse a batch result from Tripoli-4.

    :param int batch_index: index of the batch in the list of batches
    :rtype: ParseResult
    '''
    try:
        pres = parser.parse_from_index(batch_index=batch_index)
    except ParserException as t4pe:
        raise TaskException(f'cannot parse {parser.jdd}: {t4pe}') from None
    return pres


def using_parser(factory):
    '''Construct a decorator that injects Tripoli-4 parser into a Python
    function.

    :param factory: a factory producing Tripoli-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :returns: a decorator (see the module docstring for more information).
    '''
    use_run = UseRun.from_factory(factory)
    return use_run.map(make_parser)


def using_parse_result(factory, batch_number):
    '''Construct a decorator that injects the raw Tripoli-4 parse results into
    a Python function.

    :param factory: a factory producing Tripoli-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :param int batch_number: the number of the batch to parse; see
        :meth:`~.Parser.__init__`.
    :returns: a decorator (see the module docstring for more information).
    '''
    use_parser = using_parser(factory)
    return use_parser.map(partial(parse_batch_number,
                                  batch_number=batch_number))


def using_last_parse_result(factory):
    '''Construct a decorator that injects the last raw Tripoli-4 parse results
    into a Python function.

    :param factory: a factory producing Tripoli-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :returns: a decorator (see the module docstring for more information).
    '''
    use_parser = using_parser(factory)
    return use_parser.map(partial(parse_batch_index, batch_index=-1))


def to_browser(result):
    '''Create a :class:`~.Browser` from the parsing result.

    :param ParseResult result: result from T4 parser
    :returns: the browser
    :rtype: Browser
    '''
    return result.to_browser()


def using_browser(factory, batch_number):
    '''Construct a decorator that injects an
    :class:`~.browser.Browser` to the Tripoli-4 parse results into a
    Python function.

    :param factory: a factory producing Tripoli-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :param int batch_number: the number of the required batch (will be parsed
        then transformed in  :class:`~.browser.Browser`)
    :returns: a decorator (see the module docstring for more information).
    '''
    use_parse_result = using_parse_result(factory, batch_number=batch_number)
    return use_parse_result.map(to_browser)


def using_last_browser(factory):
    '''Construct a decorator that injects a
    :class:`~.browser.Browser` to the Tripoli-4 last parse results
    into a Python function.

    :param factory: a factory producing Tripoli-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :returns: a decorator (see the module docstring for more information).
    '''
    use_parse_result = using_last_parse_result(factory)
    return use_parse_result.map(to_browser)
