Building the documentation
==========================

.. highlight:: bash

:mod:`valjean` uses the :mod:`sphinx` package for its own documentation.
Before building the documentation, you will need to install :mod:`valjean`, as
explained in :ref:`the installation section <installation>`.

The HTML documentation can be built with::

    $ ./setup.py build_sphinx
    $ cd doc/src && make html   # equivalently

The documentation will appear in :file:`doc/build/html` and can be browsed
starting with the :file:`index.html` file.

:mod:`sphinx` is also able to build a LaTeX version of the documentation with::

    $ ./setup.py build_sphinx -b latex
    $ cd doc/src && make latex   # equivalently

This will dump the LaTeX sources in :file:`doc/build/latex`, where you can compile
them to PDF with :command:`make`.

The :mod:`sphinx` system is deeply customizable; most of the options are set in
:file:`doc/src/conf.py`, which is fairly well documented.

Version numbering weirdness
---------------------------

By default, the version number in the :mod:`sphinx` documentation is extracted
from the **installed** version of :mod:`valjean`, and **not** the version in
the current directory. Yeah, I know. If you are building the package
documentation locally, then it doesn't really matter, but if you are building
the documentation because you want to distribute the code to your users,
**remember to install the package first!** It is simple::

    $ pip install -U -e .
    $ ./setup.py build_sphinx

You will find the full recipe in :ref:`release-recipe`.

Extensions
----------

We use a few :mod:`sphinx` extensions:

:mod:`~sphinx.ext.autodoc`
  Extracts the docstrings from the Python code and turns them into
  documentation.

:mod:`~sphinx.ext.doctest`
  Runs the example code included in the docstrings, in the form of code
  execution at a Python prompt.

:mod:`~sphinx.ext.intersphinx`
  Add hyperlinks to :mod:`sphinx` documentation outside the current project
  (for instance, in the Python standard library).

:mod:`~sphinx.ext.graphviz`
  Include ``dot`` graphs inline, render them when the documentation is built.

:mod:`~sphinx.ext.todo`
  Add TODO items, collect all of them in one place.

:mod:`~sphinx.ext.coverage`
  Measure documentation coverage. To use it::

      $ ./setup.py build_sphinx -b coverage

:mod:`~sphinx.ext.viewcode`
  Add links to the source code.

:mod:`~sphinx.ext.imgmath`
  Allows to write in math mode.
