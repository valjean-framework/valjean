Documentation
=============

.. highlight:: bash

If you are reading this, chances are high that you already know where to look
for the documentation, but anyway: the documentation is distributed along with
the sources of :mod:`valjean`, in the ``doc`` folder. You will find the
documentation in reStructuredText in ``doc/src``, and the HTML version in
``doc/build/html/index.html``.

If, for some reason, the HTML documentation is missing, you can generate it by
running

.. code-block:: bash

    $ cd /path/to/valjean-x.y.z
    $ ./setup.py build_sphinx

or

.. code-block:: bash

    $ cd /path/to/valjean-x.y.z/doc/src
    $ make html
