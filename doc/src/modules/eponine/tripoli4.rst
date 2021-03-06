:mod:`~valjean.eponine.tripoli4` – Parsing for Tripoli-4
========================================================

.. automodule:: valjean.eponine.tripoli4
   :undoc-members:

.. _pyparsing: https://pythonhosted.org/pyparsing/


Introduction
------------

The goal of this sub-package is to parse Tripoli-4 results giving them an easy
access and transforming them in the standard data format of :mod:`~valjean`.

It contains various modules from scanning the Tripoli-4 output to conversion of
its data in datasets, listed here starting from the most external modules to
the innest ones:

   * Integration of parsing in the :mod:`valjean` workflow is handled by
     :mod:`~.use`;
   * Conversion of data to :class:`~.dataset.Dataset` in
     :mod:`~.data_convertor`;
   * Parsing module :mod:`~.parse` calling the scanning one :mod:`~.scan`;
   * The parsing itself is done thanks to 3 modules:

      * :mod:`~.grammar`: the grammar of the Tripoli-4 ASCII output using
        `pyparsing`;
      * :mod:`~.transform`: methods to transform the parsing result in standard
        `python` and `NumPy` objects called in :mod:`~.grammar` via
        ``setParseAction`` applied on the ``pyparsing.ParseResults``;
      * :mod:`~valjean.eponine.tripoli4.common`: methods to transform Tripoli-4
        data in `NumPy` objects.
      * One additional module parsing module is available for debugging and
        development: :mod:`~.parse_debug`

    * Access to Tripoli-4 results from depletion, so reading ROOT files is
      handled by :mod:`~.depletion`.


Main modules
------------

.. toctree::

   tripoli4/data_convertor
   tripoli4/parse
   tripoli4/scan
   tripoli4/use
   tripoli4/depletion


More details on parsing
-----------------------

Most of the Tripoli-4 functionalities are now parsed by `pyparsing`_.
If a new score or a new response is implemented in Tripoli-4, it would be
easier for its output to match the existing responses, or else parsing will
have to be updated.

When parsing fails it indicates the last line and column where parsing
succeeded (relative to the beginning of the parsed string, not the full output)
and the problematic line. This should help debugging.

Tests should be performed in the code to take the latter case into account
(example: test presence of ``'simulation time'`` keyword, see
:func:`~valjean.eponine.tripoli4.parse.Parser.check_times`).


.. toctree::

   tripoli4/grammar
   tripoli4/transform
   tripoli4/common
   tripoli4/parse_debug
