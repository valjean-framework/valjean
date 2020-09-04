:mod:`~valjean.eponine.apollo3` – Data reading for Apollo3
==========================================================

.. automodule:: valjean.eponine.apollo3


Introduction
------------

This sub-package transforms some results from Apollo3 in the standard data
format of :mod:`~valjean`. For the moment only results stored in the HDF5
format are concerned.

Two possibilities are given to the user, available in two different modules:

* Reading and storing all results in the HDF5 file in a
  :class:`~valjean.eponine.browser.Browser` with :mod:`~.hdf5_reader`. All
  results are converted in :class:`~valjean.eponine.dataset.Dataset`, metadata
  allow selection in :class:`~valjean.eponine.browser.Browser`. Further
  selections are possible with the :class:`~valjean.eponine.browser.Browser` as
  usual.
* Picking only results of interest for the user (normally largely quicker) with
  :mod:`~.hdf5_picker`. All results are returned as
  :class:`~valjean.eponine.dataset.Dataset`. No
  :class:`~valjean.eponine.browser.Browser` is built.


Main modules
------------

.. toctree::

   apollo3/hdf5_reader
   apollo3/hdf5_picker
