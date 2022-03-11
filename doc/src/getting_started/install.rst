.. _package-installation:

Installing :mod:`valjean`
=========================

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _sphinx: https://www.sphinx-doc.org/en/master/
.. _pyparsing: https://pythonhosted.org/pyparsing
.. _pip: https://pip.pypa.io/en/stable
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _anaconda: https://www.anaconda.com/products/individual
.. _jupyter: https://docs.jupyter.org/en/latest/
.. _h5py: https://docs.h5py.org/en/stable/

Requirements
------------

:mod:`valjean` requires Python >= 3.5. The package dependencies are handled by
the build system.

Quick start
-----------

.. highlight:: bash

For those in a rush::

    $ python3 -m venv ~/venv-valjean
    $ source ~/venv-valjean/bin/activate
    (venv-valjean) $ pip install --upgrade pip
    (venv-valjean) $ pip install /path/to/valjean

.. note::

    ``/path/to/valjean`` is the location of the package sources.

Using virtual environments
--------------------------

The :mod:`valjean` package can be installed like a normal Python package, using
the `pip`_ package manager.

The recommended way to install :mod:`valjean` is to use a *virtual
environment*.  At the time of writing, the preferred solution to create virtual
environments is the :mod:`venv` module from the standard Python distribution::

     $ python3 -m venv ~/venv-valjean
     $ source ~/venv-valjean/bin/activate
     (valjean) $ pip install /path/to/valjean-x.y.z

.. note::

        Ancient versions of ``pip`` (``<19.0``) will not be able to install
        :mod:`valjean`, because :mod:`valjean` uses a ``pyproject.toml`` file
        to describe the build, as specified in the :pep:`517` and :pep:`518`
        formats. If you are using an old version of ``pip``, you should upgrade
        it (after activating the virtual environment) with::

            (venv-valjean) $ pip install --upgrade pip

Prerequisites
-------------

:mod:`valjean` depends on a number of Python packages. You don't have to do
anything special to install most of these packages, since ``pip`` should take
care of everything. The one exception for the moment is `h5py`_, which will not
work unless the HDF5 library is installed on your machine.

Using conda
-----------

It is also possible to use :mod:`valjean` from a ``conda`` environment. The
first step is to install `miniconda`_ or `anaconda`_. The former is a light
installation of python and only required packages will be installed. The latter
is a full installation and can be used offline. Once the installation is done,
you should run::

    $ source PATH/TO/CONDA/bin/activate

unless you have set up your shell to do that automatically for you.

The recommended way to install :mod:`valjean` with ``conda`` is to create a
``conda`` environment for the package and all of its dependencies::

    (base) $ conda create -n MY_ENV python=PY_VERSION
    (base) $ conda activate MY_ENV
    (MY_ENV) $ conda install -c file://PATH/TO/valjean-DETAILS.tar.bz2 --use-local valjean

``DETAILS`` stands for :samp:`v{VERSION}-{NUMBER_HASH}_{pyPY_VERSION}` with:

* ``VERSION``: last tag from valjean in the branch used to build the archive
* ``NUMBER``: number of commits since this tag
* ``HASH``: short hash of the commit used
* ``PY_VERSION``: python version used to build the archive, the version used
  for the installation should be the same.

This procedure should allow to use :mod:`valjean` from the python interpreter,
from a `jupyter`_ notebook or directly with the ``valjean`` command.

Note: only the :mod:`valjean` package is installed at that step, the others
(`numpy`, `pyparsing`, ...) will be installed when running :mod:`valjean`. If
you want to use :mod:`valjean` directly in python you'll probably need to
install the required packages using ``conda install PACKAGE``.

An offline installation is possible adding the ``--offline`` option in the
installation command line. As a consequence updates of packages won't be
possible, i.e. they will come from the available ones in the local installation
of ``conda``. The Python version of the package should probably be the default
one of ``conda``.

The conda package is not editable. If you prefer to use an editable version of
:mod:`valjean` associated with conda it would probably be easier to use conda
to get the python version, then install the package via ``pip`` or ``poetry``.
Virtual environnment have to be treated carefully in that case. To get an
editable version offline fully working it might be necessary to install all
(direct and indirect) dependencies.

Checking package integrity
--------------------------

The ``md5sum`` of the archives (``pip`` or ``conda`` installation) are given in
Tuleap. To check them, just type ``md5sum MY_ARCHIVE`` and compare the obtained
hash with the one stored on Tuleap.
