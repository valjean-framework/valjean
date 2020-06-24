.. _building-documentation:

Documentation
=============

.. highlight:: bash

If you are reading this, chances are high that you already know where to look
for the documentation, but anyway: the documentation is distributed along with
the sources of :mod:`valjean`, in the ``doc`` folder. You will find the
documentation in reStructuredText in ``doc/src``, and the HTML version in
``doc/build/html/index.html``.

You can also find it in the valjean package release on Tuleap under the
*Fichiers* area in the valjean project.

If, for some reason, the HTML documentation isl missing, you can generate it by
running

.. code-block:: bash

    $ cd /path/to/valjean-x.y.z
    $ ./setup.py build_sphinx

or

.. code-block:: bash

    $ cd /path/to/valjean-x.y.z/doc/src
    $ make html
