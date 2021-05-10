.. _installation:

Installation and setup
======================

.. _poetry: https://python-poetry.org/

.. highlight:: bash

:mod:`valjean` uses `poetry`_ for packaging and dependency management; follow
the instructions on the `poetry`_ home page to install this tool.

If you plan to develop :mod:`valjean` and you have checked out the source
repository, you may want to use ``poetry`` to install the package in
"development mode" instead::

    $ python3 -m venv ~/venv-valjean-dev
    $ source ~/venv-valjean-dev/bin/activate
    (venv-valjean-dev) $ cd /path/to/valjean-X.Y.Z
    (venv-valjean-dev) $ poetry install

This will install :mod:`valjean` and all of its dependencies in your current
virtual environment. The development dependencies (e.g. `sphinx`, `pytest`,
etc.) will also be installed; if you want to skip them, pass the ``--no-dev``
flag to ``poetry install``.

This procedure should install just a link to your source folder
``/path/to/valjean-X.Y.Z``, instead of copying the source files to the
installation directory.  This way, you will not need to reinstall the package
every time you modify the sources.

Dependency management
---------------------

Dependencies are managed by `poetry`_. We ship a `poetry`_ lock file to
guarantee that :mod:`valjean` will not be broken by future package updates.
This also means that developers should think about updating the package
constraints in :file:`pyproject.toml` and regenerating the lock file from time
to time.

See the `poetry`_ documentation for more information about adding or upgrading
dependencies. 
