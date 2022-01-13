:mod:`~valjean.gavroche.stat_tests` – Statistical tests for datasets comparisons
================================================================================

.. automodule:: valjean.gavroche.stat_tests
   :undoc-members:


Introduction
------------

The available statistical tests are:

  * Student's t-test, to compare two datasets, in the :mod:`~.student` module;
  * The χ² test, for comparing distributions (spectra or meshes), in
    the :mod:`~.chi2` module;
  * The Bonferroni and Holm-Bonferroni tests, to solve the problem of multiple
    hypothesis tests, in the :mod:`~.bonferroni` module.


Modules
-------

:mod:`~.student` — Student's t-test
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
   :synopsis: Tests to handle multiple comparisons
