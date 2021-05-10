# Valjean-demo #

This repository contains demonstrations of the use of the *valjean* package.
Main purposes of *valjean* are VV and data analysis. It can be used directly in
python, importing the needed modules, especially in analysis case, or using the
executable and the full architecture, what is more foreseen in a VV case.

Examples of both cases are shown here.

## Installation from git ##

```
git clone https://codev-tuleap.intra.cea.fr/plugins/git/valjean/valjean-demo.git
```

## Prerequisites ##

To be able to use *valjean-demo* you need:

1. Installation of *valjean* (see [*valjean* repository](
   https://codev-tuleap.intra.cea.fr/plugins/git/valjean/valjean))
2. Examples executed in python are using *jupyter*, you need to install it in
   you python environment (virtual or not):

   ```
   pip install -U ipython jupyter
   ```

## Description of the package ##

### Examples using *valjean* directly in python ###

These examples are using *jupyter*.

#### livermore_exps ####

Generic example of data analysis using a Livermore sphere from international
benchmark. Tripoli-4 data is compared to experimental data. This example shows:

* Use of Tripoili-4 parser, selection using `Browser`, `Dataset` construction
* `Dataset` manipulations
* Quick examples of statistical tests
* Use of `Dataset` members in an external analysis code

#### replica ####

Generic example using the Replica benchmark. This example gives more
explanations on:

*  Tripoli-4 parsing and available data
* `Browser` object: exploration and data selection
* `Dataset` creation, kinematic coordinates used for spectra and meshes (for
  example)
* Statistical test use and representation (Student test)

#### sensitivities ####

Generic example using a Godiva simulation. The Tripoli-4 includes senstivities
calculations. This example details:

* Selections with `Browser` object
* Creation of `Dataset` from various kind of results (spectrum, number of
  batches, integrated results, k<sub>eff</sub>)
* Statistical tests use and representation (Equal, ApproxEqual and Student)
* Creation of `Dataset` from other `Datasets` to make a custom test
  (k<sub>eff</sub> comparison using estimator in x-axis)


### Examples using *valjean* executable ###

#### spherical_cows

Example with explanations given in a *jupyter* notebook (not to be executed).
Comparisons between Tripoli-4 and MCNP on spheres made of one element. The
`job.py` file:

* Runs Tripoli-4 and MCNP
* Compares the obtained results
* Builds an *html* report.

#### alavtrin ####

**probably not up to date**

Examples from Tripoli-4 VV with no explanations (up to now). Different `job()`
functions can be found:

* Checkout, build and run Tripoli-4 using 2 different versions
* Run Tripoli-4 from already built executable
* Comparisons for various responses types (k<sub>eff</sub>, adjoint results,
  generic responses, etc)
