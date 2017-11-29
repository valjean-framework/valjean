Installation and setup
======================

.. highlight:: bash

If you plan to develop :mod:`valjean` and you have checked out the source
repository, you may want to install the package in "development mode" instead::

    $ pip3 install -e /path/to/valjean[dev]

The ``-e`` flag tells :command:`pip3` that it should install just a link to
your source folder, instead of copying the source files to the installation
directory.  This way, you will not need to reinstall the package every time you
modify the sources.

Also, the ``[dev]`` suffix will trigger the installation of all the development
dependencies for :mod:`valjean` (e.g. :py:mod:`sphinx`, :mod:`pytest`, etc.). They
are specified in the ``extras_require`` argument to :func:`setup()`, in
:file:`setup.py`.

The :file:`setup.py` script
---------------------------

The :file:`setup.py` executable script is the place where the package developer
specifies how the package is to be installed. In addition, :file:`setup.py`
accepts a number of useful commands. The easiest way to obtain documentation
about the commands is to run::

    $ ./setup.py --help
    $ ./setup.py --help-commands

A good deal of extra documentation is available on the Internet (search for the
documentation of packages ``distutils`` and ``setuptools``). However, at the
time of writing, it is not very readable (few tutorials, huge reference
manuals). We will detail here the commands that most likely will be useful in
the development workflow of :mod:`valjean`.
