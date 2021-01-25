# pylint: disable=no-value-for-parameter

'''Tests for the :mod:`~.cosette.env` module.'''

import tempfile

from hypothesis import given, event, note, settings, HealthCheck, assume
from hypothesis.strategies import data, sampled_from, lists

from .conftest import envs
from ..context import valjean  # pylint: disable=unused-import

# pylint: disable=wrong-import-order
from valjean.cosette.env import Env
from valjean.cosette.task import TaskStatus


#############
#  helpers  #
#############

def event_frac(name, frac):
    '''Emit an event annotation about the number of updated keys.'''
    n_tiers = 4
    frac_rounded = int(n_tiers * frac)
    lower_perc = int(100. * min(n_tiers - 1, frac_rounded) / n_tiers)
    higher_perc = int(100. * min(n_tiers, frac_rounded + 1) / n_tiers)
    event('{}% < {} < {}%'.format(lower_perc, name, higher_perc))


###########
#  tests  #
###########

@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(env=envs())
def test_persistence_roundtrip(env, persistence_format):
    '''Test the roundtrip to all the persistence formats.'''
    with tempfile.NamedTemporaryFile() as persist:
        env.to_file(persist.name, fmt=persistence_format)
        re_env = Env.from_file(persist.name, fmt=persistence_format)
    assert env == re_env


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(env=envs(), data=data())
def test_updates(env, data):
    '''Test environment updates.'''
    # generate a new environment with keys taken from those of the first
    env_keys = list(env.keys())
    assume(env_keys)
    env_update = data.draw(envs(sampled_from(list(env.keys()))))
    old_env = env.copy()
    env.apply(env_update)

    # now perform some checks
    count_no_update = 0
    count_update = 0
    count_sub_update = 0
    count_sub_no_update = 0
    for key, value in env.items():
        if key not in env_update:
            # keys that were not updated are the same as before
            assert key in old_env
            assert value == old_env[key]
            count_no_update += 1
            continue
        count_update += 1

        # here `value` was at least partially updated
        for upd_key, upd_val in env_update[key].items():
            # subvalues from the update override the previous ones
            assert upd_key in value
            assert value[upd_key] == upd_val
            count_sub_update += 1
        for sub_key, sub_val in value.items():
            # subvalues that were not updated stayed put
            if sub_key not in env_update[key]:
                assert key in old_env
                assert sub_key in old_env[key]
                assert sub_val == old_env[key][sub_key]
                count_sub_no_update += 1

    # do some bookkeeping to make sure we are testing deeply enough
    event_frac('updated keys', count_update / (count_update + count_no_update))
    event_frac('updated subkeys',
               count_sub_update / (count_sub_update + count_sub_no_update))


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(env=envs(), data=data())
def test_merge_done_tasks(env, data):
    '''Test merging two environments.'''
    # generate a new environment with keys taken from those of the first
    env_keys = list(env.keys())
    note('env_keys: {}'.format(env_keys))
    assume(env_keys)
    env_to_merge = data.draw(envs(lists(sampled_from(env_keys))))
    note('env_to_merge: {}'.format(env_to_merge))
    old_env = env.copy()
    env.merge_done_tasks(env_to_merge)

    # now perform some checks
    count_merge_done = 0
    count_real_merge = 0

    # merge_done_tasks() does not add any key
    assert len(env) == len(old_env)

    for key, value in env.items():
        # merge_done_tasks() does not add any key
        assert key in old_env
        old_value = old_env[key]

        if key not in env_to_merge:
            # merge_done_tasks() should have done nothing on this key
            assert value == old_value
            continue

        new_value = env_to_merge[key]
        if new_value['status'] == TaskStatus.DONE:
            # merge_done_tasks() should have updated the value
            assert key in env_to_merge
            assert value == new_value
            count_real_merge += 1
        else:
            # merge_done_tasks() only updates DONE tasks
            assert value == old_value
            count_merge_done += 1

    # do some bookkeeping to make sure we are testing deeply enough
    event('no merge (status == DONE): {}'.format(count_merge_done))
    event('real merge: {}'.format(count_real_merge))
