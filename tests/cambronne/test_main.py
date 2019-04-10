'''Tests for the :mod:`valjean.cambronne.main` module.'''

import pytest
from hypothesis import given

from ..cosette.conftest import dep_tasks, DoNothingTask
from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.task import close_dependency_graph
from valjean.cambronne.main import check_unique_task_names


# pylint: disable=no-value-for-parameter
@given(tasks=dep_tasks())
def test_tasks_dependencies(tasks):
    '''Check that :func:`~valjean.cambronne.main.close_dependency_graph`
    correctly recovers all the dependencies.'''
    # if a task appears as a dependency, remove it from the list
    to_remove = set(dep for task in tasks for dep in task.depends_on)
    indep_tasks = list(set(tasks).difference(to_remove))
    collected_tasks = close_dependency_graph(indep_tasks)
    # check that close_dependency_graph has correctly recovered all the tasks
    assert len(collected_tasks) == len(tasks)


@given(tasks=dep_tasks())
def test_unique_names(tasks):
    '''Check that :func:`~valjean.cambronne.main.check_unique_task_names` does
    not raise if the names are all different (ensured by construction in
    :func:`~tests.cosette.conftest.dep_tasks`).'''
    check_unique_task_names(tasks)


@given(tasks=dep_tasks(min_size=1))
def test_check_unique_names(tasks):
    '''Check that :func:`~valjean.cambronne.main.check_unique_task_names`
    raises if two tasks have the same name.'''
    a_name = next(task.name for task in tasks)
    tasks.append(DoNothingTask(a_name))
    with pytest.raises(ValueError):
        check_unique_task_names(tasks)
