.. _tox: https://tox.readthedocs.io/en/latest/
.. _ROOT: https://root.cern.ch/

.. _tox-integration:

Using ``tox`` for continuous integration
========================================

Unit tests, linting and documentation checks are part of the continuous
integration (CI) suite. We use `tox`_ to orchestrate the tests and run the
tests with different Python versions.

Configuration
-------------

The ``tox`` configuration is included in the :file:`pyproject.toml` file.

Available test environments
---------------------------

In CI, the unit tests are run for several versions of Python (at the time of
writing, all the supported versions are tested). For the most recent Python
version (3.9 at the time of writing), the CI environment provides the optional
`ROOT`_ dependency, which makes it possible to run the tests for the
:mod:`~valjean.eponine.tripoli4.depletion` module. For this reason, we pass the
``PYTHONPATH`` environment variable into the test environment.

Additional environments
-----------------------

There are three additional test environments, with specific purposes:

* ``docs``: :ref:`builds the documentation <building-documentation-dvpers>`,
  with and without the ``tests`` tag, in :ref:`nitpicky mode <nitpicky-mode>`.
  It also runs :ref:`the linkcheck builder <linkcheck>` to check for broken or
  redirecting external links.

* ``linting``: :ref:`runs the linters <linting>`.

* ``parsing``: runs all the unit tests, plus the specific (slow) parsing tests
  on the outputs of older TRIPOLI-4 versions.


Using ``tox`` from the command line
-----------------------------------

You can use ``tox`` to run your tests, build the documentation or lint the code
from the command line. First, install ``tox`` in your :ref:`virtual environment
<installation>`::

      $ pip install tox

* To run the unit tests::

      $ tox -e py39 valjean tests  # for Python 3.9, for example

  You need to specify the Python version on the command line.

* Building the documentation::

      $ tox -e docs

* Linting::

      $ tox -e linting valjean tests
