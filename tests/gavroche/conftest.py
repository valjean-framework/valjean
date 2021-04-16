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

'''Fixtures for the :mod:`~.valjean.gavroche` module.'''

# pylint: disable=wrong-import-order,no-value-for-parameter
import string
from collections import OrderedDict

import pytest
from hypothesis.strategies import composite, just, integers, dictionaries, text
import numpy as np

from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from valjean.eponine.dataset import Dataset
from valjean.gavroche.test import TestEqual, TestApproxEqual
from valjean.gavroche.stat_tests.student import TestStudent
from valjean.gavroche.stat_tests.bonferroni import (TestBonferroni,
                                                    TestHolmBonferroni)
from valjean.gavroche.diagnostics.metadata import TestMetadata
from ..eponine.conftest import datasets
from valjean.cosette.pythontask import PythonTask
from valjean.cosette.task import TaskStatus
from valjean.config import Config


##################################
#  fixtures for the test module  #
##################################

@pytest.fixture
def some_dataset():
    '''Return a simple :class:`~.Dataset` object.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0])),
                        ('t', np.linspace(0.0, 3.0, 4))])
    dataset = Dataset(np.linspace(0.0, 5.0, 6).reshape(2, 3),
                      np.array([0.3]*6).reshape(2, 3),
                      bins=bins,
                      name='some dataset')
    return dataset


@pytest.fixture
def other_dataset(some_dataset):
    '''Return a simple :class:`~.Dataset` object, with the same content as
    :func:`some_dataset` but with a different name.'''
    dataset = some_dataset.copy()
    dataset.name = 'other dataset'
    return dataset


@pytest.fixture
def different_dataset(some_dataset):
    '''Return a :class:`~.Dataset` object, with the same structure as
    :func:`some_dataset` but with different content (so that equality tests
    will fail).'''
    dataset = some_dataset.copy()
    dataset.name = 'other dataset'
    dataset.value[:2] += 5.0
    return dataset


@pytest.fixture
def some_1d_dataset():
    '''Return a simple 1D :class:`~.Dataset` object.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                      np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                      bins=bins,
                      name="some 1D dataset")
    return dataset


@pytest.fixture
def other_1d_dataset():
    '''Return a other 1D :class:`~.Dataset` object, successfully compared to
    :func:`some_1d_dataset` when taking into account errors.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                      np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                      bins=bins,
                      name="other 1D dataset")
    return dataset


@pytest.fixture
def different_1d_dataset():
    '''Return a different 1D :class:`~.Dataset` object, unsuccessfully compared
    to :func:`some_1d_dataset` also when taking into account errors.'''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0]))])
    dataset = Dataset(np.array([1.5, 2.6, 2.3, 4.5, 3.5]),
                      np.array([0.1, 0.2, 0.1, 0.1, 0.2]),
                      bins=bins,
                      name="different 1D dataset")
    return dataset


@pytest.fixture
def some_1d_dataset_edges():
    '''Return a simple 1D :class:`~.Dataset` object, bins are given by edges.
    '''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))])
    dataset = Dataset(np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
                      np.array([0.3, 0.1, 0.2, 0.3, 0.5]),
                      bins=bins,
                      name="some 1D dataset")
    return dataset


@pytest.fixture
def other_1d_dataset_edges():
    '''Return a other 1D :class:`~.Dataset` object, successfully compared to
    :func:`some_1d_dataset` when taking into account errors. Bines are given by
    edges.
    '''
    bins = OrderedDict([('e', np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))])
    dataset = Dataset(np.array([1.5, 2.0, 2.7, 4.5, 5.7]),
                      np.array([0.3, 0.2, 0.3, 0.3, 0.4]),
                      bins=bins,
                      name="other 1D dataset")
    return dataset


@pytest.fixture
def some_scalar_dataset():
    '''Return a scalar :class:`~.Dataset` object.'''
    return Dataset(np.float_(1.2), np.float_(0.2), name='some scalar dataset')


@pytest.fixture
def other_scalar_dataset():
    '''Return an other scalar :class:`~.Dataset` object.'''
    return Dataset(np.float_(1.0), np.float_(0.1), name='other scalar dataset')


@pytest.fixture
def different_scalar_dataset():
    '''Return a different scalar :class:`~.Dataset` object.'''
    return Dataset(np.float_(4.3), np.float_(0.1),
                   name='different scalar dataset')


@pytest.fixture
def equal_test(some_dataset, other_dataset):
    '''Return an equality test between datasets.'''
    return TestEqual(some_dataset, other_dataset,
                     name='An equality test',
                     description='Are these datasets equal?')


@pytest.fixture
def equal_test_fail(some_dataset, different_dataset):
    '''Return an equality test between different datasets.'''
    return TestEqual(
        some_dataset, different_dataset,
        name='Another equality test',
        description='Are these datasets equal? (Spoiler alert: no.)')


@pytest.fixture
def approx_equal_test(some_dataset, other_dataset):
    '''Return an approx-equality test between datasets.'''
    return TestApproxEqual(
        some_dataset, other_dataset,
        name='An approximate equality test',
        description='Are these datasets approximately equal?')


@pytest.fixture
def equal_test_result(equal_test):
    '''Return an equality test result between datasets.'''
    return equal_test.evaluate()


@pytest.fixture
def equal_test_result_fail(equal_test_fail):
    '''Return a failing equality test result between datasets.'''
    return equal_test_fail.evaluate()


@pytest.fixture
def approx_equal_test_result(approx_equal_test):
    '''Return an approx-equality test result between datasets.'''
    return approx_equal_test.evaluate()


@pytest.fixture
def student_test(some_1d_dataset, other_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, other_1d_dataset,
                       name='A Student test',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def student_test_result(student_test):
    '''Return a Student test result between datasets.'''
    return student_test.evaluate()


@pytest.fixture
def student_test_2d(some_dataset, other_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_dataset, other_dataset,
                       name='A Student test',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def student_test_2d_result(student_test_2d):
    '''Return a Student test result between datasets.'''
    return student_test_2d.evaluate()


@pytest.fixture
def student_test_edges(some_1d_dataset_edges, other_1d_dataset_edges):
    '''Return a Student test between datasets with bins given by edges.'''
    return TestStudent(some_1d_dataset_edges, other_1d_dataset_edges,
                       name='A Student test',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def student_test_edges_result(student_test_edges):
    '''Return a Student test result between datasets with bins given by edges.
    '''
    return student_test_edges.evaluate()


@pytest.fixture
def student_test_fail(some_1d_dataset, different_1d_dataset):
    '''Return a Student test between different datasets (failing test).'''
    return TestStudent(some_1d_dataset, different_1d_dataset,
                       name='Failing Student test',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors? no...')


@pytest.fixture
def student_test_result_fail(student_test_fail):
    '''Return a Student test result between different datasets (failing test).
    '''
    return student_test_fail.evaluate()


@pytest.fixture
def student_test_3ds(some_1d_dataset, other_1d_dataset, different_1d_dataset):
    '''Return a Student test between one reference dataset, ``some_1d_dataset``
    and two other ones (``other_1d_dataset``, ``different_1d_dataset``). First
    one succeeds, second one fails.'''
    return TestStudent(some_1d_dataset, other_1d_dataset, different_1d_dataset,
                       name='Student test (3 datasets)',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors? no...')


@pytest.fixture
def student_test_result_3ds(student_test_3ds):
    '''Return a Student test result between one reference dataset and two
    others.'''
    return student_test_3ds.evaluate()


@pytest.fixture
def student_test_with_pvals(some_1d_dataset, other_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, other_1d_dataset,
                       name='A Student test',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?',
                       ndf=20)


@pytest.fixture
def student_test_result_with_pvals(student_test_with_pvals):
    '''Return a Student test between datasets.'''
    return student_test_with_pvals.evaluate()


@pytest.fixture
def student_test_fail_with_pvals(some_1d_dataset, different_1d_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_1d_dataset, different_1d_dataset,
                       name='A Student test failing',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?',
                       ndf=20)


@pytest.fixture
def student_test_scalar(some_scalar_dataset, other_scalar_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_scalar_dataset, other_scalar_dataset,
                       name='A Student test from scalars',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def student_test_fail_scalar(some_scalar_dataset, different_scalar_dataset):
    '''Return a Student test between datasets.'''
    return TestStudent(some_scalar_dataset, different_scalar_dataset,
                       name='A Student test from scalars',
                       description='Do the datasets have the same mean taking '
                                   'into account the errors?')


@pytest.fixture
def equal_test_scalar(some_scalar_dataset):
    '''Return an equality test between datasets.'''
    return TestEqual(
        some_scalar_dataset, some_scalar_dataset,
        name='An equality test',
        description='Are these datasets equal?')


@pytest.fixture
def equal_test_fail_scalar(some_scalar_dataset, other_scalar_dataset):
    '''Return an equality test between datasets.'''
    return TestEqual(
        some_scalar_dataset, other_scalar_dataset,
        name='An equality test',
        description='Are these datasets equal?')


@pytest.fixture
def bonferroni_test(student_test_with_pvals):
    '''Return a Bonferroni test based on a Student test.'''
    return TestBonferroni(name='A Bonferroni test',
                          description='Can we consider this distribution OK?',
                          test=student_test_with_pvals, alpha=0.05)


@pytest.fixture
def bonferroni_test_result(bonferroni_test):
    '''Return a Bonferroni test result based on a Student test.'''
    return bonferroni_test.evaluate()


@pytest.fixture
def bonferroni_test_fail(student_test_fail_with_pvals):
    '''Return a Bonferroni test based on a Student test.'''
    return TestBonferroni(name='A Bonferroni test',
                          description='Can we consider this distribution OK?',
                          test=student_test_fail_with_pvals, alpha=0.05)


@pytest.fixture
def bonferroni_test_result_fail(bonferroni_test_fail):
    '''Return a Bonferroni test result based on a Student test.'''
    return bonferroni_test_fail.evaluate()


@pytest.fixture
def holm_bonferroni_test(student_test_with_pvals):
    '''Return a HolmBonferroni test based on a Student test.'''
    return TestHolmBonferroni(
        name='A Holm-Bonferroni test',
        description='Can we consider this distribution OK?',
        test=student_test_with_pvals, alpha=0.05)


@pytest.fixture
def holm_bonferroni_test_result(holm_bonferroni_test):
    '''Return a Holm-Bonferroni test result based on a Student test.'''
    return holm_bonferroni_test.evaluate()


@pytest.fixture
def holm_bonferroni_test_fail(student_test_fail_with_pvals):
    '''Return a Holm-Bonferroni test based on a Student test.'''
    return TestHolmBonferroni(
        name='A Holm-Bonferroni test',
        description='Can we consider this distribution OK?',
        test=student_test_fail_with_pvals, alpha=0.05)


@pytest.fixture
def holm_bonf_test_result_fail(holm_bonferroni_test_fail):
    '''Return a Holm-Bonferroni test result based on a Student test.'''
    return holm_bonferroni_test_fail.evaluate()


@composite
def one_dim_dataset(draw):
    '''Strategy for generating 1-dimension datasets.'''
    return draw(datasets(elements=integers(min_value=-5, max_value=5),
                         shape=just(5)))


@pytest.fixture(params=[['equal_test'],
                        ['equal_test_fail'],
                        ['equal_test', 'approx_equal_test'],
                        ['student_test', 'student_test_2d',
                         'student_test_edges', 'student_test_fail',
                         'student_test_3ds', 'student_test_with_pvals',
                         'student_test_fail_with_pvals',
                         'student_test_scalar', 'equal_test_scalar',
                         'bonferroni_test', 'bonferroni_test_fail',
                         'holm_bonferroni_test',
                         'holm_bonferroni_test_fail']],
                ids=['one successful test', 'one failing test', 'two tests',
                     'all the other tests'])
def valid_tests(request):
    '''Return lists of valid :class:`~.Test` objects.'''
    fixtures = [request.getfixturevalue(fix_name)
                for fix_name in request.param]
    return fixtures


@pytest.fixture(params=[[1, 2], 'pinicho oinichba'],
                ids=['list of not tests', 'not even a list'])
def invalid_tests(request):
    '''Return invalid lists of :class:`~.Test` objects (or not even lists!).'''
    return request.param


############################################
#  fixtures for the diagnostics submodule  #
############################################

@composite
def metadata_dicts(draw, min_size=1):
    '''Generate a dictionary of metadata (string to string).'''
    return draw(dictionaries(keys=text(alphabet=string.printable),
                             values=text(alphabet=string.printable),
                             min_size=min_size))


def generate_test_tasks():
    '''Generate :class:`~.TestMetadata` to test the statistics diagnostics
    based on labels.'''
    menu1 = {'food': 'egg + spam', 'drink': 'beer'}
    menu2 = {'food': 'egg + bacon', 'drink': 'beer'}
    menu3 = {'food': 'lobster thermidor', 'drink': 'brandy'}

    def test_generator():
        result = [TestMetadata({'Graham': menu1, 'Terry': menu1},
                               name='gt_wday_lunch',
                               labels={'day': 'Wednesday', 'meal': 'lunch'}
                               ).evaluate(),
                  TestMetadata({'Michael': menu1, 'Eric': menu2},
                               name='me_wday_dinner',
                               labels={'day': 'Wednesday', 'meal': 'dinner'}
                               ).evaluate(),
                  TestMetadata({'John': menu2, 'Terry': menu2},
                               name='jt_wday',
                               labels={'day': 'Wednesday'}).evaluate(),
                  TestMetadata({'Terry': menu3, 'John': menu3},
                               name='Xmasday',
                               labels={'day': "Christmas Eve"}).evaluate()]
        return {'test_generator': {'result': result}}, TaskStatus.DONE

    return PythonTask('test_generator', test_generator)


def run_tasks(tasks, env):
    '''Run the tasks and update the environnment.'''
    config = Config()
    for task in tasks:
        env_up, status = task.do(env=env, config=config)
        env.set_status(task, status)
        env.apply(env_up)
    return env, status
