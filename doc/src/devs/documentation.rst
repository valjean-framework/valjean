Building documentation
======================

.. highlight:: bash

:mod:`valjean` uses the standard Python :mod:`sphinx` package for its own
documentation. The HTML documentation can be built with::

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
