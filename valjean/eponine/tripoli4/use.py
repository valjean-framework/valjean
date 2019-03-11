'''This module extends the functionalities provided by :mod:`~.cosette.use` to
the commonplace task of parsing TRIPOLI-4 output files. The decorators defined
by this module, :func:`using_parse_results` and :func:`using_accessor`, can be
used to remove boilerplate code that parses and accesses the TRIPOLI-4 results.
At the same time, they simplify the integration of user-defined post-processing
(tests) into the :mod:`valjean` workflow.

.. doctest:: eponine_use
    :hide:

    >>> # pylint: disable=trailing-whitespace,line-too-long
    >>> # noqa: E501,W291
    >>> from valjean.config import Config
    >>> config = Config(paths=[])

We will need to set up a few things to show an example of how to use the
decorators. We don't want to build and run TRIPOLI-4 for the purpose of this
documentation, but we can mock a TRIPOLI-4 run by writing an existing TRIPOLI-4
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
    >>> echo_factory = RunTaskFactory.from_executable('/bin/echo',
    ...                                               default_args=['{text}'])

In the real world, the :class:`~.RunTaskFactory` would actually generate tasks
to run a TRIPOLI-4 executable.


Injecting the raw parse results
===============================

Now we can construct the decorator that parses the TRIPOLI-4 results and apply
it to a Python function::

    >>> from valjean.eponine.tripoli4 import use
    >>> using_parse_results = use.using_parse_results(echo_factory)
    >>> @using_parse_results(text=example)
    ... def source(results):
    ...     return results[0]['source_intensity']

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
    'source-...'

The task has explicit dependencies, which means that it will be correctly
integrated in the :mod:`valjean` dependency graph. In particular, this task
depends on a task that actually does the parsing::

    >>> source_task.depends_on
    {Task('parse_output_file-...')}
    >>> parse_task = source_task.depends_on.pop()

and `parse_task` in turn depends on the :class:`~.RunTask` that was generated
by `echo_factory`::

    >>> parse_task.depends_on
    {Task('run_...-...')}
    >>> run_task = parse_task.depends_on.pop()

We manually execute the tasks in the correct order and we check that we recover
the right result at the end::

    >>> from valjean.cosette.env import Env
    >>> env = Env()
    >>> for task in [run_task, parse_task, source_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[source_task.name]['result'])
    81114.52


Injecting an :class:`~.Accessor`
================================

The raw parse results are useful in some situations, but most of the time you
probably want to work with a higher-level representation of the calculation
result, such as an :class:`~.Accessor`. This module provides a function to
construct a decorator that automatically creates the :class:`~.RunTask` from
the :class:`~.RunTaskFactory`, runs the task, parses the resulting output and
wraps the parse results in an :class:`~.Accessor`::


    >>> using_accessor = use.using_accessor(echo_factory)
    >>> @using_accessor(text=example)
    ... def extract_simulation_time(accessor):
    ...     return accessor.simulation_time()

We can again check that everything went as expected by manually unwrapping the
sequence of tasks and running them::

    >>> extract_task = extract_simulation_time.get_task()
    >>> access_task = extract_task.depends_on.pop()
    >>> parse_task = access_task.depends_on.pop()
    >>> run_task = parse_task.depends_on.pop()
    >>> env = Env()
    >>> for task in [run_task, parse_task, access_task, extract_task]:
    ...     env_up, _ = task.do(env=env, config=config)
    ...     env.apply(env_up)
    >>> print(env[extract_task.name]['result'])
    20


Module API
==========
'''

from .accessor import Accessor
from .parse import T4Parser
from ...cosette.use import UseRun
from ...cosette.pythontask import TaskException
from ..tripoli4.parse import T4ParserException


def partial(func, *args, **kwargs):
    '''An improved version of :func:`functools.partial` that calls
    :func:`functools.update_wrapper` on the partially applied function in order
    to update its metadata (name, etc.).'''
    import functools
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
    return partial_func


def parse_output_file(filename, *, batch=-1):
    '''Parse a TRIPOLI-4 output file and return the list of parse results.

    :param str filename: the name of the file to parse.
    :param int batch: the number of the batch to parse; see
                      :meth:`~.T4Parser.__init__`.
    :raises ValueError: if parsing fails.
    :returns: the list of parse results.
    '''
    try:
        parser = T4Parser(filename, batch=batch)
    except T4ParserException as t4pe:
        raise TaskException('cannot parse {}: {}'.format(filename, t4pe))
    return parser.result


def access(parse_results, *, index):
    '''Construct an :class:`~.Accessor` to a given TRIPOLI-4 parse result.

    :param parse_results: the list of raw parse results.
    :param int index: the index of the required parse result.
    :returns: an :class:`~.Accessor`.
    '''
    return Accessor(parse_results[index])


def using_parse_results(factory, batch=-1):
    '''Construct a decorator that injects the raw TRIPOLI-4 parse results into
    a Python function.

    :param factory: a factory producing TRIPOLI-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :param int batch: the number of the batch to parse; see
                      :meth:`~.T4Parser.__init__`.
    :returns: a decorator (see the module docstring for more information).
    '''
    use_run = UseRun.from_factory(factory)
    return use_run.map(partial(parse_output_file, batch=batch))


def using_accessor(factory, index=-1):
    '''Construct a decorator that injects an :class:`~.Accessor` to the
    TRIPOLI-4 parse results into a Python function.

    :param factory: a factory producing TRIPOLI-4 runs.
    :type factory: :class:`~.RunTaskFactory`
    :param int index: the index of the required parse result.
    :returns: a decorator (see the module docstring for more information).
    '''
    use_parse_results = using_parse_results(factory)
    return use_parse_results.map(partial(access, index=index))
