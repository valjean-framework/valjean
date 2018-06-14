Building the documentation
==========================

.. highlight:: bash
.. _sphinx: http://www.sphinx-doc.org/en/stable

:mod:`valjean` uses the `sphinx`_ package for its own documentation.
Before building the documentation, you will need to install :mod:`valjean`, as
explained in :ref:`the installation section <installation>`.

The HTML documentation can be built with::

    $ ./setup.py build_sphinx
    $ cd doc/src && make html   # equivalently

The documentation will appear in :file:`doc/build/html` and can be browsed
starting with the :file:`index.html` file.

`sphinx` is also able to build a LaTeX version of the documentation with::

    $ ./setup.py build_sphinx -b latex
    $ cd doc/src && make latex   # equivalently

This will dump the LaTeX sources in :file:`doc/build/latex`, where you can compile
them to PDF with :command:`make`.

The `sphinx` system is deeply customizable; most of the options are set in
:file:`doc/src/conf.py`, which is fairly well documented.

Version numbering weirdness
---------------------------

By default, the version number in the `sphinx` documentation is extracted
from the **installed** version of :mod:`valjean`, and **not** the version in
the current directory. Yeah, I know. If you are building the package
documentation locally, then it doesn't really matter, but if you are building
the documentation because you want to distribute the code to your users,
**remember to install the package first!** It is simple::

    $ cd /path/to/valjean  # the path containing setup.py
    $ pip install -U .[dev]
    $ ./setup.py build_sphinx

You will find the full recipe in :ref:`distributing-code`.

Extensions
----------

We use a few `sphinx` extensions:

:mod:`~sphinx.ext.autodoc`
  Extracts the docstrings from the Python code and turns them into
  documentation.

:mod:`~sphinx.ext.doctest`
  Runs the example code included in the docstrings, in the form of code
  execution at a Python prompt.

:mod:`~sphinx.ext.intersphinx`
  Add hyperlinks to `sphinx` documentation outside the current project
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


.. _nitpicky-mode:

Checking references
-------------------

To check internal references the ``nitpicky`` option can be used::

      $ sphinx-build -a -n src/ build/html

from the ``doc`` folder, ``-n`` to activate the ``nitpicky`` option and ``-a``
(optional) to reconstruct documentation for all files.

This option has to be used carefully, some links are not obvious (especially
those from :mod:`~sphinx.ext.intersphinx` ones).
We intentionally refuse to correct some warnings, like those concerning the
(mis)use of the ``:ivar:`` role. They look like this::

    $ .../valjean/eponine/scan_t4.py:docstring of valjean.eponine.scan_t4.Scan:: WARNING: py:obj reference target not found: fname

We use ``:ivar:`` to document instance variables (that is what they are for,
right?), but apparently `sphinx`_ expects some target object which is not there.

.. _linkcheck:

Checking external links
-----------------------

The special ``linkcheck`` builder can be used to check any external links found
in the documentation. Of course you must run the check from a machine with good
network connectivity. The command is::

      $ sphinx-build -a -b linkcheck src/ build/html
