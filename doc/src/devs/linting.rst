.. _linting:

Linting
=======

.. highlight:: bash

The :pep:`8` document makes a number of style recommendations for writing
Python code. :mod:`valjean` tries to be PEP 8-compliant; you can check many
of the PEP 8 recommendations with linters such as :command:`flake8` or
:command:`pylint`, which are automatically pulled and installed when
:mod:`valjean` is installed with the ``[dev]`` extra feature. Just run one of
the following from the source folder::

    $ flake8
    $ pylint valjean tests

As a rule, try hard to keep :mod:`valjean` lint-free by running these commands
often. If the linter emits a warning, you can do one of the following:

1. Fix the warning;
2. No, really, fix the warning;
3. If there's a warning you really can't fix, you can shut up the linter about
   that particular code line by adding special annotations (see below). But
   really, you should fix the warning instead.

Suppressing linter warnings
---------------------------

Sometimes, linters emit warning, but you **know** that the warning is actually
benign. You can tell :command:`flake8` or :command:`pylint` to shut up about a
specific warning by adding a comment with a special annotation in the source
code. For :command:`flake8`, suppression annotations look like this:

.. code-block:: python

   <code raising a warning>  # noqa: E402

Note the ``E402`` error code, which must matches :command:`flake8`'s output
message. For :command:`pylint`, annotations look like this:

.. code-block:: python

   <code raising a warning>  # pylint: disable=trailing-whitespace

Again, the string after ``disable=`` must match the name of the warning in the
:command:`pylint` output.

See the :command:`flake8` and :command:`pylint` documentation for more details.


``tox`` integration
-------------------

There is a specific ``tox`` test environment to run the linters. Check the
page about :ref:`using tox for continuous integration <tox-integration>`.
