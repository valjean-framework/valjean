Installing :mod:`valjean`
=========================

Quick start
-----------

.. highlight:: bash

For those in a rush::

    $ python3 -m venv ~/.venv/valjean
    $ source ~/.venv/valjean/bin/activate
    (valjean) $ pip3 install --upgrade setuptools pip
    (valjean) $ pip3 install /path/to/valjean

Using virtual environments
--------------------------

The :mod:`valjean` package can be installed like a normal Python package.
However, you will need to have ``root`` priviliges to touch the system-wide
installation; plus, the installation may interfere with your machine's
package-management system. The way to do this is::

    $ sudo pip3 install /path/to/valjean-x.y.z    # bad

It is probably simpler (and cleaner) to install the package into your local package
repository::

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

For the record, the :mod:`virtualenvwrapper` package also provides a practical
alternative to manage virtual Python environments.

Prerequisites
-------------

.. _pyparsing: http://pythonhosted.org/pyparsing/

In order to use :mod:`valjean`, you will need at least Python v3.4. Some of the
prerequisites for testing and documentation generation (*looking at you,*
:doc:`sphinx <sphinx-doc/sphinx>`) have known installation problems with old versions of the
:ref:`setuptools` standard library package. This is the case, for instance, of
boxes running Ubuntu 14.04, that ships by default with :ref:`setuptools` v2.2.
You can work around these problems by upgrading your :ref:`setuptools` package
(and :mod:`pip`, since you're at it) in your virtual environment, before
installing :mod:`valjean` or its dependencies. The command is::

    (valjean) $ pip3 install --upgrade setuptools pip

.. todo::

   Document the real dependencies (`pyparsing`_, etc.) as soon as the code
   that requires them lands in the repository.
