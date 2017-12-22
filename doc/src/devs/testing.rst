Testing
=======

.. highlight:: bash

Unit tests
----------

:mod:`valjean` uses :mod:`pytest` as a unit-test framework; some of the unit
tests rely on the :mod:`hypothesis` package for property-based testing. The
tests are defined in the :file:`tests` folder and are automatically discovered
by :mod:`pytest`.

You can run the unit-test suite with::

    $ ./setup.py test
    $ ./setup.py pytest  # equivalently
    $ py.test

This will run the tests and produce a summary report. Additionally,
:mod:`pytest` will calculate code coverage; a text report will be printed to
stdout, and a nice HTML report will be written to :file:`tests/htmlcov`.

The default :mod:`pytest` options are defined in the :file:`pytest.ini` file,
and :mod:`coverage` options are defined in :file:`.coveragerc`. Extra options
to :mod:`pytest` can be passed on the command line::

    $ py.test -k depgraph        # select tests whose name matches "depgraph"
    $ py.test --valjean-verbose  # verbose test output

The ``--valjean-verbose`` option sets all the :mod:`valjean` loggers to
maximum verbosity. It is useful when debugging a failing test, in conjunction
with the ``-k`` option.

Property-based testing and the :mod:`hypothesis` package
--------------------------------------------------------

In traditional unit testing, one verifies that the code gives the expected
answer for a given, fixed set of input values. For instance, one may test a
sort algorithm by verifying that it produces ``[1,2,3,4]`` when fed
``[4,2,3,1]``. However, this does not check that the algorithm behaves sensibly
on any of the following arguments:

* empty lists;
* long lists;
* lists that are already sorted;
* lists of objects other than integers...

You see the point. One could write additional, specific unit tests to address
each of these limitations. However, it is impossible to make sure that we have not
forgotten some important edge case; also, we will need to write essentially the
same tests over and over, and nobody likes doing the same thing over and over.
But wait a minute, isn't "doing the same thing over and over" the kind of thing
that computers are actually good at?

Enter *property-based testing*. The idea of this approach is that the developer
should only check the expected properties of the code to be tested. For
instance, in the case of the sort algorithm, the developer could check the
following invariants about the list returned by the algorithm:

* it is sorted;
* it contains the same elements as the input list.

The testing library will generate a number of random inputs, call the sorting
algorithm on each of them and check that the properties specified by the
developer hold. If a counterexample is found, it will be shown to the user.

In Python, the standard property-based test library is :mod:`hypothesis`, which
offers a flexible and `well-documented API
<https://hypothesis.readthedocs.io/en/latest/>`_. Additionally,
:mod:`hypothesis` is well integrated with :mod:`pytest`.  :mod:`valjean` unit
tests leverage :mod:`hypothesis` whenever possible.

If you want some examples within :mod:`valjean`, a good place to start is the
:mod:`~tests.cosette.test_depgraph` test module, which tests the invariants of
the :class:`~valjean.cosette.depgraph.DepGraph` class.

Testing example docstrings with :mod:`~sphinx.ext.doctest`
----------------------------------------------------------

Sometimes the docstrings contain example code such as the following:

.. code-block:: python

   >>> print(1+2)
   3

These examples can be automatically tested with :mod:`~sphinx.ext.doctest`, a
:mod:`sphinx` extension. You can run the examples with::

    $ ./setup.py build_sphinx -b doctest
    $ cd doc/src && make doctest  # equivalently

This will produce a long report, with a summary (hopefully) like the following:

.. code-block:: none

    Doctest summary
    ===============
       61 tests
        0 failures in tests
        0 failures in setup code
        0 failures in cleanup code