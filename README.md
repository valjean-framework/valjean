# Valjean #

Quick installation guide:

*valjean* needs at least python3.6 (deprecated on December 23, 2021).

## Installation using *pip* ##

### Setup a virtual environment ###

```
python3 -m venv MY_VIRTUAL_ENV
source MY_VIRTUAL_ENV/bin/activate
pip install -U pip setuptools
```

### Installation from git ###

```
git clone https://github.com/valjean-framework/valjean.git
pip install ./valjean  # or pip install path/to/valjean
```

### Installation from archive ###

The pip archive can be downloaded from the *Fichiers*/*Files* area of Tuleap.

```
pip install valjean-VERSION.tar.gz
```


## Installation using *conda* ##

1. Download and install *conda*.
2. Download the *valjean-conda* archive from the *Fichiers*/*Files* area of
   Tuleap.
3. Install *valjean*:

```
source MY_CONDA/bin/activate
conda create -n MY_ENV python=PY_VERSION
conda activate MY_ENV
conda install -c file://PATH/TO/valjean-VERSION.tar.bz2 --use-local valjean
```

The python version of *conda* should be the same as the one used to build the
*valjean* archive.


## Documentation ##

The documentation can be downloaded from the *Fichiers*/*Files* area of Tuleap.

```
tar xzf valjean-doc-*.tar.gz
```

You can also consult the source files for the documentation in the ``doc/src``
directory.
