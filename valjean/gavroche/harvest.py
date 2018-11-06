'''Collect tests from user files.

This module provides tools to load test functions from user files. It imports
Python source files and filters out functions (actually, any callable object)
matching a specific regular expression. For instance, let us write some Python
code to a test file:

.. doctest:: harvest
   :hide:

   >>> from pprint import pprint
   >>> code = ("def test_function():\\n  return sentence"
   ...         "\\n\\nsentence = 'My hovercraft is full of eels!'")
   >>> more_code = "def compute_stuff(x):\\n  return 5 * 9 - x"
   >>> bad = 'for i in range(4):\\n  def test_in_loop(x=i):\\n    print(x)'
   >>> better = ("import sys\\n"
   ...           "for i in range(4):\\n"
   ...           "  def test_in_loop(x=i):\\n"
   ...           "    print(x)\\n"
   ...           "  name = 'test_in_loop_{}'.format(i)\\n"
   ...           "  setattr(sys.modules[__name__], name, test_in_loop)\\n"
   ...           "del test_in_loop  # required to remove the last function")
   >>> best = ("from valjean.gavroche.harvest import export\\n"
   ...         "for i in range(4):\\n"
   ...         "  @export\\n"
   ...         "  def test_in_loop(x=i):\\n"
   ...         "    print(x)\\n"
   ...         "del test_in_loop  # required to remove the last function")


   >>> print(code)
   def test_function():
     return sentence
   <BLANKLINE>
   sentence = 'My hovercraft is full of eels!'

Our test consists of a single function called, well, :func:`!test_function`. We
write it to a file called, well, :file:`test_file.py`:

   >>> test_file = 'test_file.py'
   >>> with open(test_file, 'w') as fout:
   ...   print(code, file=fout)

Now we can invoke :func:`harvest` to collect it:

   >>> from valjean.gavroche.harvest import harvest
   >>> tests = harvest(test_file)
   >>> print(tests)
   {'test_function': <function test_function at ...>}

As you can see, :func:`harvest` returns a dictionary mapping test names to
their representation as a Python object (a function, in this case).  We can
invoke the test function as follows:

   >>> result = tests['test_function']()
   >>> print(result)
   My hovercraft is full of eels!

Note that :func:`harvest` did not collect ``sentence``, although it appears as
a top-level symbol in :file:`test_file.py`.  The reason is that ``'sentence'``
does not match the default regular expression that :func:`harvest` uses to
filter test functions, which is ``'test_.*'``.  This makes it possible make
liberal use of identifiers in test files — just stick a ``test_`` prefix in
front of the functions that you would like :program:`valjean` to collect. The
principle is very similar to unit-testing frameworks such as :mod:`unittest` or
`pytest`.

If you want to harvest functions matching a different regex, you can customize
it:

   >>> print(more_code)
   def compute_stuff(x):
     return 5 * 9 - x
   >>> test_stuff = 'test_stuff.py'
   >>> with open(test_stuff, 'w') as fout:
   ...   print(more_code, file=fout)
   >>> stuff = harvest(test_stuff, test_regex='compute_.*')
   >>> print(stuff)
   {'compute_stuff': <function compute_stuff at ...>}
   >>> stuff['compute_stuff'](3)
   42


The :func:`export` decorator
----------------------------

A rather common need is to programmatically generate test code based on some
kind of iteration. This doesn't work:

   >>> print(bad)  # DO NOT TRY THIS AT HOME
   for i in range(4):
     def test_in_loop(x=i):
       print(x)
   >>> test_loop_bad = 'test_loop_bad.py'
   >>> with open(test_loop_bad, 'w') as fout:
   ...   print(bad, file=fout)
   >>> loop_bad = harvest(test_loop_bad)
   >>> print(loop_bad)
   {'test_in_loop': <function test_in_loop at ...>}
   >>> len(loop_bad)  # seriously, where are my functions?
   1
   >>> loop_bad['test_in_loop']()  # so which one is it?
   3

You may have expected to find four dictionary keys in ``loop``, but only the
function defined at the last loop iteration was harvested. This is not really a
problem with harvesting, but rather with function definition. If you import the
:mod:`!test_loop` module, you will see that it contains only one function.  A
moment's reflection should convince you that this makes sense; even if the
module contained several functions called :func:`!test_in_loop`, how would you
tell them apart since they have the same name?

So, if you want to define tests in a loop, you may be tempted to attempt
shenanigans such as:

   >>> print(better)  # DO NOT TRY THIS AT HOME EITHER
   import sys
   for i in range(4):
     def test_in_loop(x=i):
       print(x)
     name = 'test_in_loop_{}'.format(i)
     setattr(sys.modules[__name__], name, test_in_loop)
   del test_in_loop  # required to remove the last function
   >>> test_loop_better = 'test_loop_better.py'
   >>> with open(test_loop_better, 'w') as fout:
   ...   print(better, file=fout)
   >>> loop_better = harvest(test_loop_better)
   >>> pprint(list((k, loop_better[k]) for k in sorted(loop_better)))
   [('test_in_loop_0', <function test_in_loop at ...>),
    ('test_in_loop_1', <function test_in_loop at ...>),
    ('test_in_loop_2', <function test_in_loop at ...>),
    ('test_in_loop_3', <function test_in_loop at ...>)]
   >>> len(loop_better)
   4
   >>> for name, func in sorted(loop_better.items()):
   ...   func()
   0
   1
   2
   3

This works but it is way too verbose. You can actually ask
:mod:`~valjean.gavroche` to jump through all the hoops using the :func:`export`
decorator:

   >>> print(best)
   from valjean.gavroche.harvest import export
   for i in range(4):
     @export
     def test_in_loop(x=i):
       print(x)
   del test_in_loop  # required to remove the last function
   >>> test_loop_best = 'test_loop_best.py'
   >>> with open(test_loop_best, 'w') as fout:
   ...   print(best, file=fout)
   >>> loop_best = harvest(test_loop_best)
   >>> pprint(list((k, loop_best[k]) for k in sorted(loop_best)))
   [('test_in_loop_...',
     <function test_in_loop_... at ...>),
    ('test_in_loop_...',
     <function test_in_loop_... at ...>),
    ('test_in_loop_...',
     <function test_in_loop_... at ...>),
    ('test_in_loop_...',
     <function test_in_loop_... at ...>)]

As you can see, the function names were decorated with a hexadecimal hash to
make them unique. If you prefer to specify the suffix yourself, you can do so
by passing an argument to :func:`export`:

   >>> from valjean.gavroche.harvest import export
   >>> @export('expect_spanish_inquisition')
   ... def surprise():
   ...   print('NOBODY EXPECTS THE SPANISH INQUISITION!')

.. doctest::
   :hide:

   >>> from valjean.gavroche.harvest import expect_spanish_inquisition
   ... # This line is required to make doctests work. The doctest prompt
   ... # '>>>' does not really behave like a Python prompt: at a real prompt,
   ... # the definition of `surprise` would be stored in the `__main__` module.
   ... # During doctests, instead, `surprise` is considered to be defined in
   ... # the present module (`valjean.gavroche.harvest`). The `@export`
   ... # decorator therefore puts the wrapper in the same place. This hidden
   ... # doctest line reimports the wrapper and makes the HTML documentation
   ... # look like what would happen if you tried it on the prompt.

The wrapper is tucked up in the module where the wrapped function is defined.
If ``@export`` is used from the Python prompt, the decorated function ends up
in the :mod:`builtins` module.

   >>> expect_spanish_inquisition()
   NOBODY EXPECTS THE SPANISH INQUISITION!

Note that the old function is still around:

   >>> surprise()
   NOBODY EXPECTS THE SPANISH INQUISITION!


Harvesting directories or collections of files
----------------------------------------------

You can harvest many files at once with :func:`harvest_many`:

   >>> from valjean.gavroche.harvest import harvest_many
   >>> tests = harvest_many([test_loop_bad, test_loop_better, test_loop_best])
   >>> pprint(sorted(tests))
   ['test_loop_bad.py', 'test_loop_best.py', 'test_loop_better.py']
   >>> tests['test_loop_bad.py'] == loop_bad
   True

You can also harvest whole directories with :func:`harvest_dir`, which accepts
a `file_regex` argument to filter which files should be harvested; by default,
the file name must match ``'test_.*\\.py$'``. You can harvest recursively using
`recurse=True`.

   >>> from valjean.gavroche.harvest import harvest_dir
   >>> tests_dir = harvest_dir('.')
   >>> pprint(sorted(tests_dir))
   ['test_file.py',
    'test_loop_bad.py',
    'test_loop_best.py',
    'test_loop_better.py',
    'test_stuff.py']


Implementation details
----------------------

Test files are full-fledged Python source files. They can import other modules,
play with `sys.path`, launch missiles, and so on.  Harvesting a test file for
tests will actually

    1. add its path to `sys.path`, if it is not already there, and
    2. import the module.

So you can have test files importing other modules in the same directory if you
feel the need to refactor some of your tests.
'''

import logging
from pathlib import Path

from .. import LOGGER
from ..dyn_import import dyn_import


def harvest(file_name, *, test_regex=None):
    '''Collect tests from the given file.

    :param str file_name: the name of the file to harvest.
    :param str test_regex: a regular expression that must be matched by
                           the name of harvested functions. If `None`,
                           functions must match ``'test_.*'``.
    :returns: the harvested tests, as a dictionary mapping test names to test
              functions.
    '''
    import re
    regex = 'test_.*' if test_regex is None else test_regex
    compiled = re.compile(regex)
    LOGGER.debug('filtering tests with regex: %s', compiled)
    module = dyn_import(file_name)
    tests = {
        name: obj
        for name, obj in vars(module).items()
        if re.match(compiled, name) and callable(obj)
    }
    return tests


def harvest_many(file_names, *, relative_to=None, test_regex=None):
    '''Collect tests from the given files.

    :param str file_names: an iterable over the names of the files to harvest.
    :param str test_regex: a regular expression that must be matched by
                           the name of harvested functions. If `None`,
                           functions must match ``'test_.*'``.
    :returns: the harvested tests, as a dictionary mapping file names to test
              dictionaries (see the return value of :func:`harvest`).
    '''
    test_dict = {}
    for file_name in file_names:
        if relative_to is None:
            key = file_name
        else:
            key = Path(file_name).relative_to(relative_to)
        test_dict[str(key)] = harvest(file_name, test_regex=test_regex)
    return test_dict


def harvest_dir(dir_name, *, file_regex=None, test_regex=None, recurse=True):
    r'''Collect tests from the given directory.

    This function collects user tests from all the files in the given
    directory, and returns them as a dictionary.  If `file_regex` is specified,
    only file names matching `file_regex` are harvested; otherwise, the file
    name must match ``'test_.*\.py$'``.

    The `test_regex` argument is passed to :func:`harvest`.

    :param str dir_name: the name of the directory to harvest.
    :param str file_regex: a regular expression that must be matched by
                           harvested files.
    :param str test_regex: a regular expression that must be matched by
                           harvested functions.
    :param bool recurse: if true, recurse into subdirectories.
    :returns: the harvested tests, as a dictionary mapping file names to test
              dictionaries (see the return value of :func:`harvest`).
    '''
    dir_str = str(dir_name)
    file_names = _walk_dir(dir_str, file_regex, recurse)
    if LOGGER.isEnabledFor(logging.DEBUG):
        file_names = list(file_names)
        LOGGER.debug('walked dir %s, collected %d files: %s',
                     dir_str, len(file_names), file_names)
    test_dict = harvest_many(file_names,
                             test_regex=test_regex, relative_to=dir_str)
    return test_dict


def _walk_dir(dir_name, file_regex, recurse):
    '''Worker function for harvest_dir.

    The parameters have the same meaning as in harvest_dir.
    '''
    import re
    regex = r'test_.*\.py$' if file_regex is None else file_regex
    compiled = re.compile(regex)

    dir_path = Path(dir_name)
    paths = dir_path.rglob('*') if recurse else dir_path.iterdir()
    paths = list(paths)
    LOGGER.debug('Walking %s with regex %s', dir_name, compiled.pattern)

    yield from (path for path in paths
                if path.is_file() and re.match(compiled, path.name))


def export(name=None):
    '''(Returns a) decorator for persisting temporary functions in the module.

    The decorator is used as follows (unnamed version)::

        >>> @export
        ... def func():
        ...   pass

    or as follows (named version)::

        >>> @export('new_name')
        ... def func():
        ...   pass

    In the former case, a copy of `func` is stored in the module under a name
    of the form ``func_#####``, where ``#####`` represents a hexadecimal hash.
    In the second case, a copy of `func` is stored under the name ``new_name``.
    The copies persist in the module even if `func` is explicitly deleted
    (``del func``) or if the name is overwritten.

    :param str name: an optional name.
    '''

    if callable(name) or name is None:
        from hashlib import sha1
        LOGGER.debug('generating SHA1 hash from counter: %s', export.counter)
        suffix = sha1(bytes([export.counter])).hexdigest()
        wr_name = None
        LOGGER.debug('generated SHA1 hash: %s', suffix)
        export.counter += 1
    else:
        wr_name = name
        LOGGER.debug('using external name: %s', wr_name)

    def _decorator(func):
        from sys import modules
        from functools import wraps
        nonlocal wr_name, suffix

        if wr_name is None:
            wr_name = func.__name__ + '_' + suffix
            wr_qualname = func.__qualname__ + '_' + suffix
        else:
            wr_qualname = func.__qualname__.replace(func.__name__, wr_name)

        @wraps(func)
        def _wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        _wrapper.__name__ = wr_name
        _wrapper.__qualname__ = wr_qualname

        if func.__module__ is not None:
            module = func.__module__
        else:
            # if there is no module, putting the wrapper in builtins makes
            # @export work as expected when called from the command line
            module = 'builtins'

        LOGGER.debug('storing decorated function as %s in %s',
                     wr_name, module)
        setattr(modules[module], wr_name, _wrapper)

        return _wrapper

    if callable(name):
        # direct decoration, `name` is actually the decorated function
        return _decorator(name)
    return _decorator


export.counter = 0
