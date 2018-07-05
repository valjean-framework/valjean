Release checklist
=================

.. highlight:: bash

This page contains a list of things that you should check before issuing a new
:mod:`valjean` release. In the future, some or all of the things below may
(should!) be automated.

#. Create a new branch off the development branch. If you are aiming at
   releasing version :file:`{x.y}`, call the branch :file:`releng-v{x.y}`.
   Commit all the following steps on this branch.

#. Revise this TODO list, if necessary!

#. Run the code :ref:`linters <linting>` and fix all the warnings.

#. Run all the :ref:`unit tests <unit-tests>`, including the slow ones. Make
   sure they all pass. Use parallelism::

    $ pytest -m slow -n 4   # for 4 tests in parallel

   Push the ``-n`` option and overload the test machine a bit (e.g. use ``-n
   6`` if you have 4 cores). If the tests start failing because they run too
   slowly, they are probably quite close to failing the health checks/deadlines
   in sequential mode anyway,  and they may do so on another machine. Fix them
   so that they run faster.

   Also, run the command above a few times, in case some tests fail
   erratically.

   Running `pytest` also runs doctests.  Make sure they all pass.

#. Test :ref:`package installation <package-installation>`, with and without
   optional dependencies. Check the install/setup/tests/extras requirements:
   are they up to date?

#. Build the HTML documentation :ref:`in nitpicky mode <nitpicky-mode>`. Fix
   all the warnings, except the intentional ones.

#. :ref:`Check external documentation links <linkcheck>` with the ``linkcheck``
   builder. Fix the broken ones.

#. Check the :ref:`TODO list <todolist>` and update it. Can anything be
   removed?

#. Update the :ref:`changelog <changelog>`.

#. Commit and make a pull request.

#. Once the pull request is accepted, tag the new version::

    $ git tag vx.y  # for appropriate values of x and y

   Remember to push the tag to the shared repository.

#. :ref:`Create a source tarball and deploy it on the local network
   <distributing-code>`. This requires reinstalling the package and rebuilding
   the documentation.

#. Remember to merge any release changes back into the development branch.

#. Congratulations, you have made a new :mod:`valjean` release!
