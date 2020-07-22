Purpose
=======

This folder contains scripts and bits to create a
[spack](https://spack.readthedocs.io/) environment where you can install all
the Python versions that you want and test valjean against them.


Creating a new spack repository for valjean
-------------------------------------------

1. Clone spack somewhere;
2. Drop the files contained in `etc/spack` into `${SPACK_ROOT}/etc/spack`;

This needs to be done only once if all the test machines can share access to a
common network folder somewhere.


Creating a new spack environment
--------------------------------

1. Activate the spack repository:

   ```
   $ source ${SPACK_ROOT}/share/spack/setup-env.sh
   ```

2. Run `new_spack_env` with the python versions that you want to add as
   arguments.

   ```
   $ ./new_spack_env 3.7.7 3.8.3
   ```
