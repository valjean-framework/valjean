:mod:`~valjean.eponine.tripoli4` – Parsing for TRIPOLI-4
========================================================

.. automodule:: valjean.eponine.tripoli4
   :undoc-members:

.. _pyparsing: https://pythonhosted.org/pyparsing/


Introduction
------------

The goal of this sub-package is to parse TRIPOLI-4 results giving them an easy
access and transforming them in the standard data format of :mod:`~valjean`.

It contains various modules from scanning the TRIPOLI-4 output to conversion of
its data in datasets, listed here starting from the more external modules to
the inner ones:

   * General task for parsing in :mod:`~.parse_task`
   * Conversion of data to :class:`~.base_dataset.BaseDataset` in
     :mod:`~.data_convertor`
   * Easy access to TRIPOLI-4 results thanks to metadata in :mod:`~.accessor`
   * Parsing module :mod:`~.parse` calling the scanning one :mod:`~.scan`
   * The parsing itself it done thanks to 3 modules:

      * :mod:`~.grammar`: the grammar of TRIPOLI-4 outputs (ASCII ones) using
        `pyparsing`
      * :mod:`~.transform`: methods to transform the parsing result in standard
        `python` and `NumPy` objects called in :mod:`~.grammar` via
        ``setParseAction`` applied on the ``pyparsing.ParseResults``
      * :mod:`~valjean.eponine.tripoli4.common`: methods to transform TRIPOLI-4
        data in `NumPy` objects


Main modules
------------

:mod:`~.parse_task` – Module to build a task for parsing TRIPOLI-4 results
--------------------------------------------------------------------------

.. automodule:: valjean.eponine.tripoli4.parse_task
   :synopsis: Task to parse TRIPOLI-4 results using :class:`~.cosette.Task`
   :private-members:


:mod:`~.data_convertor` – Module to convert TRIPOLI-4 results in :class:`~.eponine.base_dataset.BaseDataset`
------------------------------------------------------------------------------------------------------------

.. automodule:: valjean.eponine.tripoli4.data_convertor
   :synopsis: Module to convert TRIPOLI-4 results in
      :class:`~.eponine.base_dataset.BaseDataset`
   :private-members:


:mod:`~.accessor` – Access class to TRIPOLI-4 results
-----------------------------------------------------

.. automodule:: valjean.eponine.tripoli4.accessor
   :synopsis: Access class to obtain TRIPOLI-4 results in easy way
   :private-members:


:mod:`~.parse` – Parse TRIPOLI-4 outputs
----------------------------------------

.. automodule:: valjean.eponine.tripoli4.parse
   :synopsis: Parse TRIPOLI-4 outputs


:mod:`~.scan` – Scan TRIPOLI-4 outputs and select relevant results
------------------------------------------------------------------

.. automodule:: valjean.eponine.tripoli4.scan
   :synopsis: Scan TRIPOLI-4 outputs and select relevant results



More details on parsing
-----------------------

Module using the `pyparsing`_ package to parse Tripoli-4 output listings.

Most of the TRIPOLI-4 functionalities are now parsed thanks to `pyparsing`.
If a new score or a new response in implemented in Tripoli-4, it would be easier
for its output to match the exisiting response, else parsing will have to be
updated.

When parsing fails it can

   * or crash, last line indicating where it had to stop in the listing,
   * or it says nothing.

Tests should be performed in the code to take that last case into account
(example: test presence of ``'simulation time'`` keyword).


:mod:`~.grammar` – Pyparsing grammar
------------------------------------

.. automodule:: valjean.eponine.tripoli4.grammar
   :synopsis: Grammar for pyparsing parser

:mod:`~.transform` – Transform pyparsing result
-----------------------------------------------

.. automodule:: valjean.eponine.tripoli4.transform
   :synopsis: Methods to transform pyparsing results in python standard objects
   		(dictionaries and lists) and numpy arrays

:mod:`~valjean.eponine.tripoli4.common` – Common methods to build numpy arrays from dictionaries and lists
------------------------------------------------------------------------------------------------------------

.. automodule:: valjean.eponine.tripoli4.common
   :synopsis: Common methods to build numpy arrays from dictionaries and lists
   :private-members:
