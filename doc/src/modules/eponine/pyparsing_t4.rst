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
   :members:

   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.intro
      :annotation: introduction parser
		   
      ..
	 .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
	    :lines: 418
		   
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.runtime
      :annotation: run time parser

	 ..
	    .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
	       :lines: 426
      
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.respdesc
      :annotation: response description
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.respcarac
      :annotation: response characteristics
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.respintro
      :annotation: response introduction
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 523
		   
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.scoremode
      :annotation: score mode
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.scorezone
      :annotation: score zone
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.scoredesc
      :annotation: score description
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 607-608
	      
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.defintegratedres
      :annotation: default integrated result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.spectrumblock
      :annotation: spectrum block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.vovspectrumblock
      :annotation: spectrum block result with variance of variance
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.meshblock
      :annotation: mesh block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.kijres
      :annotation: kij result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.kijsources
      :annotation: kij sources
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.keffblock
      :annotation: keff block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.defkeffblock
      :annotation: default keff block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.medfile
      :annotation: med file path
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.entropy
      :annotation: entropy results
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.orderedres
      :annotation: ordred results
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.gbblock
      :annotation: Green bands block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.ifpblock
      :annotation: IFP block result
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.ifpadjointcriticality
      :annotation: IFP adjoint criticality edition block
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.pertu_desc
      :annotation: perturbation description
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.uncertblock
      :annotation: uncertainties block parser
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.uncertintegblock
      :annotation: = integrated uncertainties block parser
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.contribpartblock
      :annotation: = contributing particles block parser
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.scoreblock
      :annotation:
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 1044-1055
	      
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.responseblock
      :annotation: response block parser
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 1057-1064
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.response
      :annotation: response parser
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 1066-1069
   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.perturbation
      :annotation: perturbation parser
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 1071-1072

   .. autoattribute:: valjean.eponine.pyparsing_t4.grammar.mygram
      :annotation:
	 
      Tripoli-4 parser (full)
   .. literalinclude:: ../../../../valjean/eponine/pyparsing_t4/grammar.py
      :lines: 1079-1088
      
   ..
      .. autodata:: valjean.eponine.pyparsing_t4.grammar.mygram
	 :annotation:

:mod:`~.transform` – Transform pyparsing result
-----------------------------------------------

.. automodule:: valjean.eponine.pyparsing_t4.transform
   :synopsis: Methods to transform pyparsing results in python standard objects (dictionaries and lists) and numpy arrays
