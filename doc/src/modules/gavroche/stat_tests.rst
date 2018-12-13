:mod:`~valjean.gavroche.stat_tests` – Statistical tests for datasets comparisons
================================================================================

.. automodule:: valjean.gavroche.stat_tests
   :undoc-members:


Introduction
------------

Available statistical tests are:

  * Student's t-test, to compare two datasets, especially generic score, in :mod:`~.student` module
  * χ² test, for distribution (spectrum or mesh) comparisons, in :mod:`~.chi2` module
  * Bonferroni correction and Holm-Bonferroni, to conclude from multiple hypothesis tests, in :mod:`~.bonferroni` module


Main modules
------------

:mod:`~.student` – Student's t-test
```````````````````````````````````

.. automodule:: valjean.gavroche.stat_tests.student
   :synopsis: Student's t-test to compare datasets

:mod:`~.chi2` – :math:`\chi^2` test
```````````````````````````````````

.. automodule:: valjean.gavroche.stat_tests.chi2
   :synopsis: χ² test to compare datasets (especially spectra or meshes)

:mod:`~.bonferroni` – Multiple hypothesis tests
```````````````````````````````````````````````

.. automodule:: valjean.gavroche.stat_tests.bonferroni
   :synopsis: Test for cases where multiple hypothesis tests are done using
   			  Bonferroni correction and Holm-Bonferroni method
