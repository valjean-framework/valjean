# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: valjean developers
# valjean-support@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

'''Tests for the :mod:`valjean.cambronne.main` module.'''

import pytest
from hypothesis import given

from ..cosette.conftest import dep_tasks, DoNothingTask
from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.task import close_dependency_graph
from valjean.cambronne.common import check_unique_task_names


# pylint: disable=no-value-for-parameter
@given(tasks=dep_tasks())
def test_tasks_dependencies(tasks):
    '''Check that :func:`~valjean.cosette.task.close_dependency_graph`
    correctly recovers all the dependencies.'''
    # if a task appears as a dependency, remove it from the list
    to_remove = set(dep for task in tasks for dep in task.depends_on)
    indep_tasks = list(set(tasks).difference(to_remove))
    collected_tasks = close_dependency_graph(indep_tasks)
    # check that close_dependency_graph has correctly recovered all the tasks
    assert len(collected_tasks) == len(tasks)


@given(tasks=dep_tasks())
def test_unique_names(tasks):
    '''Check that :func:`~valjean.cambronne.common.check_unique_task_names`
    does not raise if the names are all different (ensured by construction in
    :func:`~tests.cosette.conftest.dep_tasks`).'''
    check_unique_task_names(tasks)


@given(tasks=dep_tasks(min_size=1))
def test_check_unique_names(tasks):
    '''Check that :func:`~valjean.cambronne.common.check_unique_task_names`
    raises if two tasks have the same name.'''
    a_name = next(task.name for task in tasks)
    tasks.append(DoNothingTask(a_name))
    with pytest.raises(ValueError):
        check_unique_task_names(tasks)
