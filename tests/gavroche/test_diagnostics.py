# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
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

'''Tests for the submodules in :mod:`valjean.gavroche.diagnostics`.'''

# pylint: disable=unused-import,wrong-import-order,no-value-for-parameter
from ..context import valjean

import pytest
from hypothesis import given, event
from hypothesis.strategies import shared, one_of

from valjean.gavroche.diagnostics.metadata import TestMetadata
from .conftest import metadata_dicts
from valjean.cosette.pythontask import PythonTask
from valjean.cosette.task import TaskStatus
from valjean.gavroche.diagnostics.stats import test_stats_by_labels
from valjean.gavroche.test import TestResultFailed
from valjean.config import Config
from valjean.cosette.env import Env

from .conftest import generate_test_tasks, run_tasks


@given(metadata1=shared(metadata_dicts(), key='metadata'),
       metadata2=one_of(shared(metadata_dicts(), key='metadata'),
                        metadata_dicts()))
def test_metadata_success(metadata1, metadata2):
    '''Test that :class:`~.TestMetadata` yields outcomes that are consistent
    with direct dictionary comparison.

    This test sometimes draws equal metadata, and sometimes draws different
    metadata, thank to the magic of :func:`hypothesis.strategies.shared`.
    '''
    test = TestMetadata({'metadata1': metadata1, 'metadata2': metadata2},
                        name='metadata_test', description='a metadata test')
    if metadata1 == metadata2:
        event('equal metadata')
        assert test.evaluate()
    else:
        event('different metadata')
        assert not test.evaluate()


@given(metadata=metadata_dicts())
def test_metadata_exclude(metadata):
    '''Test that the `exclude` keyword excludes the comparison of a metadata
    keyword.'''
    metadata_mod = metadata.copy()
    # modify the first element of metadata_mod
    first_key, first_value = next(x for x in metadata_mod.items())
    metadata_mod[first_key] = first_value + '_modified'
    # exclude first_key from the test
    test = TestMetadata({'metadata1': metadata, 'metadata2': metadata_mod},
                        name='metadata_test', description='a metadata test',
                        exclude=(first_key,))
    # the test should succeed
    assert test.evaluate()


def generate_stats_tasks(name, test_task, labels):
    '''Generate to tasks to make the diagnostic based on tests' labels.'''
    stats = test_stats_by_labels(name=name, tasks=[test_task],
                                 by_labels=labels)
    create_stats = next(task for task in stats.depends_on)
    return [create_stats, stats]


def one_label_case(ttask, env):
    '''Statistics based on one label.'''
    tasks = generate_stats_tasks('stats_day', ttask, labels=('day',))
    tasks.extend(generate_stats_tasks('stats_meal', ttask, labels=('meal',)))
    env, status = run_tasks(tasks, env)
    assert status == TaskStatus.DONE
    assert len(env[tasks[1].name]['result']) == 1
    stats_day_res = env[tasks[1].name]['result'][0]
    assert not stats_day_res
    assert stats_day_res.n_labels == 4
    assert (stats_day_res.classify == [
        {'KO': 0, 'OK': 1, 'labels': ('Christmas Eve',), 'total': 1},
        {'KO': 1, 'OK': 2, 'labels': ('Wednesday',), 'total': 3}])
    assert stats_day_res.nb_missing_labels() == 0
    stats_meal_res = env[tasks[3].name]['result'][0]
    assert (stats_meal_res.classify == [
        {'KO': 1, 'OK': 0, 'labels': ('dinner',), 'total': 1},
        {'KO': 0, 'OK': 1, 'labels': ('lunch',), 'total': 1}])
    assert stats_meal_res.nb_missing_labels() == 2


def two_labels_case(ttask, env):
    '''Statistics based on two labels.'''
    tasks_md = generate_stats_tasks('stats_md', ttask, labels=('meal', 'day'))
    env, status = run_tasks(tasks_md, env)
    assert status == TaskStatus.DONE
    stats_md_res = env[tasks_md[1].name]['result'][0]
    assert stats_md_res.test.by_labels == ('meal', 'day')
    assert (stats_md_res.classify == [
        {'KO': 1, 'OK': 0, 'labels': ('dinner', 'Wednesday'), 'total': 1},
        {'KO': 0, 'OK': 1, 'labels': ('lunch', 'Wednesday'), 'total': 1}])
    assert stats_md_res.nb_missing_labels() == 2
    tasks_dm = generate_stats_tasks('stats_dm', ttask, labels=('day', 'meal'))
    env, status = run_tasks(tasks_dm, env)
    assert status == TaskStatus.DONE
    stats_dm_res = env[tasks_dm[1].name]['result'][0]
    assert (stats_dm_res.classify == [
        {'KO': 1, 'OK': 0, 'labels': ('Wednesday', 'dinner'), 'total': 1},
        {'KO': 0, 'OK': 1, 'labels': ('Wednesday', 'lunch'), 'total': 1}])


def exception_case(ttask, env):
    '''Test raising an exception that is caught during the evaluation and
    stored in a :class:`~.TestResultFailed`.'''
    task_badlab = generate_stats_tasks('stats_bl', ttask, labels=('consumer',))
    env, status = run_tasks(task_badlab, env)
    assert status == TaskStatus.DONE
    badlab_res = env[task_badlab[1].name]['result'][0]
    assert isinstance(badlab_res, TestResultFailed)
    assert ("TestStatsTestsByLabels: ('consumer',) not found in tests labels"
            in str(badlab_res.msg))


def test_stats_diagnostic():
    '''Test the statistics test by labels using a common set of tests.'''
    tasks = [generate_test_tasks()]
    env = Env()
    env, status = run_tasks(tasks, env)
    assert status == TaskStatus.DONE
    one_label_case(tasks[0], env)
    two_labels_case(tasks[0], env)
    exception_case(tasks[0], env)
