.. _distributing-code:

Distributing the code
=====================

.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _anaconda: https://www.anaconda.com/products/individual

.. highlight:: bash

Two package management systems are currently supported: ``pip`` and ``conda``.

All the packages, including the documentation package, are available in
the `Fichiers` area of valjean's **Tuleap**
(``https://codev-tuleap.intra.cea.fr/projects/valjean``).


Source distribution
-------------------

Creation
^^^^^^^^

A source distribution can be created with the command::

	$ python setup.py sdist

This will produce a :samp:`valjean-{x.y.z}.tar.gz` archive in the :file:`dist`
folder. The archive is suitable for distribution of :mod:`valjean` to users,
for example by unpacking it to a shared folder.

Installation
^^^^^^^^^^^^

The source distribution may be installed with::

	$ pip install /path/to/valjean-{x.y.z}.tar.gz

.. note::
	If the archive is built from a commit not corresponding to a tag, the
	archive name will contain the hash of the commit, like
	:samp:`valjean-{x.y}.dev{z}+g{hash}.tar.gz`.


Conda package
-------------

Creation
^^^^^^^^

It is possible to create a conda package of :mod:`valjean` following these
steps:

1. Install `conda` with `miniconda`_ or `anaconda`_
2. Setup your conda workspace (``source MY/CONDA/PATH/bin/activate``)
3. Create the **conda** package::

	$ cd /path/to/valjean
	$ conda build conda.recipe --python=PY_VERSION

The conda package should appear in the conda installation at the path:
``MY/CONDA/PATH/conda-bld/linux-64/valjean-vVERSION-NUMBER_HASH_pyPY_VERSION.tar.bz2``
with:

* VERSION: last tag from valjean in the branch used to build the archive
* NUMBER: number of commits since this tag
* HASH: short hash of the commit used
* PY_VERSION: python version.

The option ``--python`` is needed in the command to get the correct python
version in the archive name (else it uses the default version of conda).

If the build corresponds to the tag and the hash seems useless, it is possible
to modify or comment the string. Without the string the default name would be
``valjean-vVERSION-pyPY_VERSION_NUMBER.tar.bz2``

Installation
^^^^^^^^^^^^

To install the conda package:

1. Setup your favorite conda workspace
2. Install the package::

	$ conda install -c file://PATH/TO/valjean-DETAILS.tar.bz2 --use-local valjean

with ``DETAILS = vVERSION-NUMBER_HASH_pyPY_VERSION``.

Offline installation can be done adding the ``--offline`` option.


Documentation package
---------------------

Creation
^^^^^^^^
Follow the documentation build steps in :ref:`building-documentation-dvpers`,
then archive the `html` folder::

	$ cd doc/build
	$ tar czf valjean-doc-XXX.tar.gz --transform 's,^,valjean-doc-XXX/,' html

Installation
^^^^^^^^^^^^

To install the documentation::

	$ tar xzf valjean-doc-XXX.tar.gz
