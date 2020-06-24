.. _package-installation:

Installing :mod:`valjean`
=========================

.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/en/latest/
.. _sphinx: https://www.sphinx-doc.org/en/stable/
.. _pyparsing: https://pythonhosted.org/pyparsing
.. _pip: https://pip.pypa.io/en/stable
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _anaconda: https://www.anaconda.com/products/individual

Quick start
-----------

.. highlight:: bash

For those in a rush::

    $ python3 -m venv ~/.venv/valjean
    $ source ~/.venv/valjean/bin/activate
    (valjean) $ pip3 install --upgrade setuptools pip
    (valjean) $ pip3 install /path/to/valjean

.. note::

    ``/path/to/valjean`` is the location of the package sources.

Using virtual environments
--------------------------

The :mod:`valjean` package can be installed like a normal Python package.
However, you will need to have ``root`` priviliges to touch the system-wide
installation; plus, the installation may interfere with your machine's
package-management system. The way to do this is::

    $ sudo pip3 install /path/to/valjean-x.y.z    # bad

It is probably simpler (and cleaner) to install the package into your local
package repository::

    $ pip3 install --user /path/to/valjean-x.y.z  # better

This will typically install the package somewhere in ``$HOME/.local``, and you
are responsible for updating all the relevant environment variables
(``PYTHONPATH``, ``PATH``, possibly ``LD_LIBRARY_PATH``...). Packages installed
in the local repository (and their dependencies) will then be accessible from
any Python session. This may not be what you want, especially if you need to
use/develop packages with conflicting dependencies.

The best way to avoid cluttering your Python installation and escape dependency
hell is to install :mod:`valjean` (or any package, for that matter) in a
*virtual environment*.  At the time of writing, the preferred solution to
create virtual environments is the :mod:`venv` module from the standard Python
distribution::

     $ python3 -m venv ~/.venv/valjean
     $ source ~/.venv/valjean/bin/activate
     (valjean) $ pip3 install /path/to/valjean-x.y.z

For the record, the `virtualenvwrapper`_ package also provides a practical
alternative to manage virtual Python environments.

Prerequisites
-------------

In order to use :mod:`valjean`, you will need at least Python v3.4. Some of the
prerequisites for testing and documentation generation (*looking at you,*
`sphinx`_) have known installation problems with old versions of the
:ref:`setuptools` standard library package. This is the case, for instance, of
boxes running Ubuntu 14.04, that ships by default with :ref:`setuptools` v2.2.
You can work around these problems by upgrading your :ref:`setuptools` package
(and `pip`_, since you're at it) in your virtual environment, before
installing :mod:`valjean` or its dependencies. The command is::

    (valjean) $ pip3 install --upgrade setuptools pip

.. todo::

   Document the real dependencies (`pyparsing`_, etc.) as soon as the code
   that requires them lands in the repository.

Using conda
-----------

It is also possible to use :mod:`valjean` from a **conda** environment. The
first step is to install `miniconda`_ or `anaconda`_. The former is a light
installation of python, only required packages will be installed. The latter is
a full installation and can be used offline. Once the installation is done, if
not automatic in the shell::

    $ source PATH/TO/CONDA/bin/activate

The recommended way to install valjean is to create a conda environment for the
package and all of its dependencies::

    (base) $ conda create -n MY_ENV python=PY_VERSION
    (base) $ conda activate MY_ENV
    (MY_ENV) $ conda install -c file://PATH/TO/valjean-DETAILS.tar.bz2 --use-local valjean

``DETAILS`` stands for ``vVERSION-NUMBER_HASH_pyPY_VERSION`` with:

* VERSION: last tag from valjean in the branch used to build the archive
* NUMBER: number of commits since this tag
* HASH: short hash of the commit used
* PY_VERSION: python version used to build the archive, the version used for the
  installation should be the same.

This procedure should allow to use :mod:`valjean` from the python interpreter,
from jupyter or directly with the ``valjean`` command.

Note: only the valjean package is installed at that step, the others (`numpy`,
`pyparsing`, ...) will be installed when running :mod:`valjean`. If you want to
use :mod:`valjean` directly in python you'll probably need to install the
needed packages thanks to ``conda install PACKAGE``.

An offline installation is possible adding the ``--offline`` option in the
installation command line. As a consequence updates of packages won't be
possible, i.e. they will come from the available ones in the local installation
of conda. The python version of the package should probably be the default one
of conda.

Checking package
----------------

The ``md5sum`` of the archives (``pip`` or ``conda`` installation) are given in
Tuleap. To check them, just type ``md5sum MY_ARCHIVE`` and compare the obtained
hash with the one stored on Tuleap.

