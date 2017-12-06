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
    $ pylint valjean
    $ pylint tests

As a rune, try hard to keep :mod:`valjean` lint-free by running these commands
often. If the linter emits a warning, you can do one of the following:

1. Fix the warning;
2. No, really, fix the warning;
3. If there's a warning you really can't fix, you can shut up the linter about
   that particular code line by adding special annotations (see :ref:`below
   <flake8_shutup>`). But really, you should fix the warning instead.

:command:`flake8`
-----------------

The :command:`flake8` linter is integrated with :mod:`setuptools` and can also
be invoked as an option to the ``setup.py`` script::

    $ ./setup.py flake8

.. _flake8_shutup:

Sometimes, :command:`flake8` emits a warning, but you **know** that the warning
is actually benign. For instance, the :mod:`sphinx` configuration file
:file:`doc/src/conf.py` contains the following lines:

.. code-block:: python

   import os
   import sys
   sys.path.insert(0, os.path.abspath(
       os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
   import valjean

:command:`flake8` complains about the fact that all imports should appear at
the beginning of the file, before any other instructions::

   $ flake8 doc/src/conf.py
   doc/src/conf.py:24:1: E402 module level import not at top of file

However, there is no way we can add :mod:`valjean` to the import path without
making :command:`flake8` sad. So instead we shut :command:`flake8` up by
telling it that we know what we are doing. We add a special annotation at the
end of the line:

.. code-block:: python

   import valjean  # noqa: E402

Note the ``E402`` error code, which matches :command:`flake8`'s output message.
Now :command:`flake8` will see the annotation and will not complain any more.

At the time of writing, both :mod:`valjean` and the unit tests are
:command:`flake8`-clean.

:command:`pylint`
-----------------

The :command:`pylint` linter is much more aggressive than :command:`flake8`; it
seems to have very clear (albeit configurable) ideas about what your variable
names should and should not be, how many public methods your classes should
have... At the time of writing, :mod:`valjean` is :command:`pylint`-clean, but
the tests are not.

.. todo::

   Fix the :command:`pylint` warnings in the unit tests.
