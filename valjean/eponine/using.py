# -*- coding: utf-8 -*-
'''This submodule implements several utilities (mostly decorators) that
simplify the task of writing verification and validation tests. The
:mod:`~.using` module intends to make the user's life a bit simpler by lifting
from their shoulders the burden to explicitly define all the data dependencies
and, more generally, reducing the boilerplate in user test code.  Ideally, test
code should be extremely concise and should not be cluttered by administrative
tasks such as opening result files, invoking parsers, etc.

.. testsetup:: using

   from valjean.eponine.using import using

The problem
-----------

Let us assume that Alice, a :program:`valjean` user, wants to check if the
strings contained in files :file:`spam.txt` and :file:`eggs.txt` have the same
length. Alice writes the following simplified test function:

.. doctest:: using

    >>> def compare_strlen_generic(x, y):
    ...     print('OK' if len(x) == len(y) else 'KO')

Alice is happy, because this function is generic (it works for many types of
`x` and `y`) and concise. It does the job of comparing two string lengths, but
does not specify that `x` and `y` should respectively be read from
:file:`spam.txt` and :file:`eggs.txt`. Alice briefly considers amending the
function as follows:

.. doctest:: using

    >>> def compare_strlen_by_hand():
    ...     with open('spam.txt') as fx:
    ...         x = fx.read()
    ...     with open('eggs.txt') as fy:
    ...         y = fy.read()
    ...     print('OK' if len(x) == len(y) else 'KO')

But now the test function is cluttered with unnecessary boilerplate code! Alice
would really like to keep the boilerplate away from the actual test code, so
that the test looks as simple as possible.

Also, and perhaps more importantly, Alice realises that :file:`spam.txt` and
:file:`eggs.txt` may need to be created beforehand, by some other task. There
is no way to make sure that :program:`valjean` will not call
:func:`compare_strlen_by_hand` before the files are created.  In other words,
:program:`valjean` cannot inspect the definition of
:func:`compare_strlen_by_hand` and infer that other tasks need to be run first.
The only way to enforce the correct execution order seems to be to declare the
data dependency by hand. Alice does not like this.  *Isn't this the kind of
thing computers should be good at?*, she ponders.

The :func:`using` decorator
---------------------------

Alice reads about the :func:`using` decorator and writes the following:

.. doctest:: using

    >>> def slurp(filename):
    ...     with open(filename) as f:
    ...         content = f.read()
    ...     return content
    >>> @using('x', slurp, 'spam.txt')
    ... @using('y', slurp, 'eggs.txt')
    ... def compare_strlen_using(x, y):
    ...     print('OK' if len(x) == len(y) else 'KO')

The semantics of :func:`compare_strlen_using` is exactly the same as
:func:`compare_strlen_by_hand`: when :func:`compare_strlen_using` is called,
the content of :file:`spam.txt` will be read into `x`, and :file:`eggs.txt`
will be read into `y`; the resulting strings will be passed as named arguments
to the decorated function.  Alice still thinks this looks a bit noisy, but at
least the boilerplate has been pushed outside the test function.  She tests her
shiny new function by creating some files:

.. doctest:: using

    >>> with open('spam.txt', 'w') as spam:
    ...     print('spam', file=spam)
    >>> with open('eggs.txt', 'w') as eggs:
    ...     print('eggs', file=eggs)

And it works!

.. doctest:: using

    >>> compare_strlen_by_hand()
    OK
    >>> compare_strlen_using()
    OK

Note how Alice did not need to pass any arguments to
:func:`compare_strlen_using`, because the :func:`using` decorators took care of
it.


Explicit data dependencies
--------------------------

How does :func:`using` solve Alice's data-dependency problem? Well, the data
dependencies of :func:`compare_strlen_using` can be inspected through its
`using_dict` attribute:

.. doctest:: using

    >>> from pprint import pprint
    >>> pprint(compare_strlen_using.using_dict)
    {'x': (<function slurp at ...>, ('spam.txt',), {}),
     'y': (<function slurp at ...>, ('eggs.txt',), {})}

This clearly shows that the `x` argument will be given a value that has
something to do with :file:`spam.txt` (specifically, the :func:`slurp` function
that produces `x` will take ``'spam.txt'`` as a positional argument and no
keyword arguments). :program:`valjean` is now free to inspect these
dependencies and discover (most of!) the data dependencies.

Alice reads in the docstring that :func:`~.using` **reifies** the data
dependencies.  Now that she has grasped the concept that data dependencies
become objects, and objects can be inspected, she finds the wording a bit
pretentious.


Keyword arguments
-----------------

:func:`~.using` can also pass named arguments to the function it delays. For
instance:

.. doctest:: using

    >>> @using('hexa42', int, '2A', base=16)
    ... def print_it(hexa42):
    ...     print(hexa42)
    >>> print_it()
    42

Keyword arguments show up in the third element of the `using_dict` value:

.. doctest:: using

    >>> pprint(print_it.using_dict['hexa42'])
    (<class 'int'>, ('2A',), {'base': 16})
'''


from functools import wraps

from valjean import LOGGER


def using(name, func, *args, **kwargs):
    '''Function decorator for lazily evaluated data with reified dependencies.

    This decorator essentially replaces this function

    .. code-block:: python

        @using('param', later, *args, **kwargs)
        def f(param):
            # function body goes here

    with this one

    .. code-block:: python

        def f():
            param = later(*args, **kwargs)
            # function body goes here

    Additionally, the delayed function `later` and its arguments `args` and
    `kwargs` can be inspected by looking at the `using_dict` attribute of the
    decorated function `f`.

    The decorator itself takes some arguments:

    :param name: The name of the argument that will be passed to the decorated
                 function.
    :type name str:
    :param func: Invocation of `func` will be delayed until the decorated
                 function is invoked.
    :type func callable:
    :param args: Any positional arguments that will be passed to `func`.
    :param kwargs: Any keyword arguments that will be passed to `func`.
    '''

    def _decorator(wrapped):
        LOGGER.debug("'using' decorates %s", wrapped.__name__)
        nonlocal args, kwargs

        @wraps(wrapped)
        def _wrapper(*wr_args, **wr_kwargs):
            LOGGER.debug("'using' decorator called with\n\targs: %s\n"
                         '\tkwargs: %s\n', args, kwargs)
            # The logic of the wrapper is to lazily evaluate 'func' with the
            # provided arguments only when the wrapped function is run; the
            # value resulting from the call to 'func' is passed to the wrapped
            # function as a keyword argument, with the name specified by the
            # 'name' option.
            val = func(*args, **kwargs)
            LOGGER.debug("'using' setting %s=%s", name, val)
            wr_kwargs[name] = val
            return wrapped(*wr_args, **wr_kwargs)

        # We store 'func' and its arguments (args, kwargs) as a triple in a
        # dictionary withing the wrapper function. This way, we can reconstruct
        # the data dependencies induced by the 'name' argument.  The dictionary
        # is called using_dict. Its keys are argument names, its values are
        # triples (func, args, kwargs).
        if hasattr(wrapped, 'using_dict'):
            LOGGER.debug('wrapped function has a using dict: %s',
                         wrapped.using_dict)
            _wrapper.using_dict = wrapped.using_dict.copy()
        else:
            _wrapper.using_dict = {}
        _wrapper.using_dict[name] = (func, args, kwargs)
        LOGGER.debug('wrapper function using_dict: %s',
                     _wrapper.using_dict)

        # return the wrapper, as usual for decorators
        return _wrapper

    return _decorator
