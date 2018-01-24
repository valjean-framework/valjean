pyparsing_t4 – Pyparsing parser for TRIPOLI-4
=============================================

.. automodule:: valjean.eponine.pyparsing_t4
   :undoc-members:

.. _pyparsing: http://pythonhosted.org/pyparsing/
      
Module using the `pyparsing`_ package to parse Tripoli-4 output listings.

Only the results part of the output listings are parsed, as strings. This module
should called from called from a more general module performing scanning of the
listing to isolate relevant parts of the listing.

Most of the functionalities are now parsed thanks to `pyparsing`. If a new score
or a new response in implemented in Tripoli-4, it would be better for its output
to match the exisiting response, else parsing will have to be updated.

When parsing fails it can or crash, last line indicating where it had to stop in
the listing, or it says nothing. Tests should be performed in the code to take
that last case into account (example: test presence of ``'simulation time'``
keyword.

:mod:`~.grammar` – Pyparsing grammar
------------------------------------

.. automodule:: valjean.eponine.pyparsing_t4.grammar
   :synopsis: Grammar for pyparsing parser


:mod:`~.transform` – Transform pyparsing result
-----------------------------------------------

.. automodule:: valjean.eponine.pyparsing_t4.transform
   :synopsis: Methods to transform pyparsing results in python standard objects (dictionaries and lists) and numpy arrays
