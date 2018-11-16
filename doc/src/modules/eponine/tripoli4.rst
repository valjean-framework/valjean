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
its data in datasets, listed here starting from the most external modules to
the innest ones:

   * General task for parsing in :mod:`~.parse_task`
   * Conversion of data to :class:`~.base_dataset.BaseDataset` in
     :mod:`~.data_convertor`
   * Easy access to TRIPOLI-4 results via metadata in :mod:`~.accessor`
   * Parsing module :mod:`~.parse` calling the scanning one :mod:`~.scan`
   * The parsing itself is done thanks to 3 modules:

      * :mod:`~.grammar`: the grammar of the TRIPOLI-4 ASCII output using
        `pyparsing`
      * :mod:`~.transform`: methods to transform the parsing result in standard
        `python` and `NumPy` objects called in :mod:`~.grammar` via
        ``setParseAction`` applied on the ``pyparsing.ParseResults``
      * :mod:`~valjean.eponine.tripoli4.common`: methods to transform TRIPOLI-4
        data in `NumPy` objects


Main modules
------------

:mod:`~.parse_task` – Task for parsing TRIPOLI-4 results
````````````````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.parse_task
   :synopsis: Task to parse TRIPOLI-4 results using :class:`~.cosette.Task`
   :private-members:


:mod:`~.data_convertor` – Convert TRIPOLI-4 results to :class:`~.eponine.base_dataset.BaseDataset`
``````````````````````````````````````````````````````````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.data_convertor
   :synopsis: Module to convert TRIPOLI-4 results in
      :class:`~.eponine.base_dataset.BaseDataset`
   :private-members:


:mod:`~.accessor` – Access TRIPOLI-4 results
````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.accessor
   :synopsis: Access class to obtain TRIPOLI-4 results in easy way
   :private-members:


:mod:`~.parse` – Parse TRIPOLI-4 outputs
````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.parse
   :synopsis: Parse TRIPOLI-4 outputs


:mod:`~.scan` – Scan TRIPOLI-4 outputs and select relevant results
``````````````````````````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.scan
   :synopsis: Scan TRIPOLI-4 outputs and select relevant results



More details on parsing
-----------------------

Most of the TRIPOLI-4 functionalities are now parsed by `pyparsing`_.
If a new score or a new response in implemented in Tripoli-4, it would be easier
for its output to match the exisiting response, or else parsing will have to be
updated.

When parsing fails it can

   * either crash, last line indicating where it had to stop in the listing,
   * or say nothing.

.. todo::

  A mettre a jour dans la prochaine PR : exception pour ces cas.

Tests should be performed in the code to take the latter case into account
(example: test presence of ``'simulation time'`` keyword, see
:func:`~valjean.eponine.tripoli4.parse.T4Parser.check_t4_times`).


:mod:`~.grammar` – Pyparsing grammar
````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.grammar
   :synopsis: Grammar for pyparsing parser

:mod:`~.transform` – Transform pyparsing result
```````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.transform
   :synopsis: Methods to transform pyparsing results into python standard
      objects (dictionaries and lists) and numpy arrays

:mod:`~valjean.eponine.tripoli4.common` – Common methods to build numpy arrays from dictionaries and lists
````````````````````````````````````````````````````````````````````````````````````````````````````````````

.. automodule:: valjean.eponine.tripoli4.common
   :synopsis: Common methods to build numpy arrays from dictionaries and lists
   :private-members:
