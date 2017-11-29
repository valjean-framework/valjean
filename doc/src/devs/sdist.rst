Creating a source distribution
==============================

.. highlight:: bash

You can produce a tarball with the sources and the documentation as follows::

    $ ./setup.py build_sphinx
    $ ./setup.py sdist

This will produce a :file:`valjean-{x.y.z}.tar.gz` archive in the :file:`dist`
folder. The archive is suitable for distribution of :mod:`valjean` to users,
for example by unpacking it to a shared folder::

    $ cd /home/valjean
    $ tar xzf /path/to/valjean/dist/valjean-x.y.z.tar.gz

Users can then simply install :mod:`valjean` by running::

    $ pip3 install /home/valjean/valjean-x.y.z
