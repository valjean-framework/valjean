'''Test parsing of all listing contained in Qualtrip in MONO  and PARA.'''

import os
from glob import glob
import pytest
import valjean.eponine.parse_t4 as ep
from ..context import valjean  # noqa: F401, pylint: disable=unused-import
from pytest_lazyfixture import lazy_fixture
# pylint: disable=redefined-outer-name

QUALTRIP = "/data/tmplepp/el220326/QualTassadit/RC1"
MONO = "MONO"
PARA = "PARA"
AUX = "qualtrip_aux"
MAIN = "qualtrip_main"
OUTPUTS = "output/ceav5"
MAIN_CATEGORIES = ["cristal", "elem", "protection"]

EXCLUDED_STRINGS_MONO = ["perle", "epicure", "part1", "phn_intrumen",
                         "test_pondng_auto_coupling", "gado_assembly"]
EXCLUDED_STRINGS_PARA = ["part1", "exp", "etape2", "homog_p3_prot",
                         "test_pondng_auto_coupling", "gado_assembly"]
EXCLUDED_STRINGS = ["sauv", "_v0", "save"]
MESH_LIM_FILES = ['godivaBeff_MED.d.res.ceav5']

EXPECTED_RESULTS = {"cristal": [[148, 0, 0], [148, 0, 0]],
                    "elem": [[99, 0, 1], [99, 0, 0]],
                    "protection": [[25, 0, 0], [25, 0, 0]],
                    "tripoli44": [[23, 0, 0], [18, 1, 4]],
                    "tripoli45": [[24, 0, 0], [21, 0, 2]],
                    "tripoli46": [[8, 0, 0], [5, 0, 3]],
                    "tripoli47": [[27, 0, 1], [28, 0, 0]],
                    "tripoli48": [[36, 0, 2], [37, 0, 3]],
                    "tripoli49": [[43, 0, 1], [36, 0, 1]],
                    "tripoli410":[[62, 5, 5], [59, 4, 6]],
                    "tripoli4102": [[2, 0, 0], []]}

AUX_CATEGORIES = sorted([key for key in list(EXPECTED_RESULTS.keys())
                         if key not in MAIN_CATEGORIES])

# @pytest.mark.usefixtures('qualtrip')
# @pytest.mark.parametrize('qualtrip', config.getoption('--qualtrip'))
@pytest.fixture(scope='function',
    # params=(glob(os.path.join(qualtrip, MONO, AUX, "tripoli*", OUTPUTS))), autouse=True)
    # params=([os.path.join(QUALTRIP, MONO, AUX, "tripoli*", OUTPUTS)]))
    # params=(glob(os.path.join(pytest.fixture_request('qualtrip'), MONO, AUX, "tripoli*", OUTPUTS))))
    # params=(glob(os.path.join(pytest.mark.qualtrip, MONO, AUX, "tripoli*", OUTPUTS))))
    params=(glob(os.path.join(QUALTRIP, MONO, AUX, "tripoli*", OUTPUTS))))
def aux_folder(request):
    '''Return folder from ``'aux'`` in MONO case to be tested for parsing.'''
    # print(qualtrip)
    print(request.param)
    print(glob(request.param))
    return request.param

# @pytest.fixture(scope='module')
# def qualtrip(request, monkeypatch):
#     print("[33min fixture qualtrip[0m")
#     print("[36m", request.config.getoption('--qualtrip'),
#           "type:", type(request.config.getoption('--qualtrip')), "[0m")
#     print("WILL RETURN")
#     monkeypatch.setattr("tests.eponine.test_all_listings.QUALTRIP", request.config.getoption('--qualtrip'))
    # return request.config.getoption('--qualtrip')
    # return request.getfixturevalue('qualtrip')

@pytest.fixture(
    # params=(glob(os.path.join(lazy_fixture('qualtrip'), MONO, AUX, "tripoli*", OUTPUTS)))
    # params=(glob(os.path.join(QUALTRIP, MONO, AUX, "tripoli*", OUTPUTS)))
    # params=[os.path.join(lazy_fixture('qualtrip'), MONO, AUX, "tripoli*", OUTPUTS)]
    params=[lazy_fixture('qualtrip')]
    )
def aux_folder_test(request, qualtrip):
    print("requested param:", request.param)
    print("and qualtrip", qualtrip)
    # return glob(os.path.join(qualtrip, MONO, AUX, "tripoli*", OUTPUTS))
    print(lazy_fixture('--qualtrip'), "type:", type(lazy_fixture('qualtrip')),
          str(lazy_fixture('--qualtrip')), request.getfixturevalue('qualtrip'),
          lazy_fixture(qualtrip))
    return request.param

@pytest.fixture
def my_list(qualtrip):
    return glob(os.path.join(qualtrip, MONO, AUX, "tripoli*", OUTPUTS))

@pytest.fixture(params=[(MONO, AUX, AUX_CATEGORIES)])
def gal_list(qualtrip, request):
    par = request.param
    return list(map(lambda x: os.path.join(qualtrip, par[0], par[1], x, OUTPUTS),
                    par[2]))

@pytest.fixture(params=AUX_CATEGORIES)
def my_folder(request, my_list):
    my_dict = dict(zip(AUX_CATEGORIES, sorted(my_list)))
    return my_dict[request.param]


@pytest.fixture(params=AUX_CATEGORIES)
def gal_folder(request, gal_list):
    my_dict = dict(zip(AUX_CATEGORIES, sorted(gal_list)))
    return my_dict[request.param]

@pytest.fixture(params=[(MONO, AUX, AUX_CATEGORIES)])
def list_folder_to_test(request, qualtrip):
    par = request.param
    print("[32m", par, "[0m")
    folder_list = list(map(
        lambda x: os.path.join(qualtrip, par[0], par[1], x, OUTPUTS), par[2]))
    return folder_list

@pytest.fixture(params=AUX_CATEGORIES)
def aux_folder_to_test(request, list_folder_to_test):
    print(request.param)
    categories = [fold.split('/')[-3] for fold in sorted(list_folder_to_test)]
    print(categories)
    my_dict = dict(zip(categories, sorted(list_folder_to_test)))
    return my_dict[request.param]

@pytest.fixture(params=MAIN_CATEGORIES)
def folder_to_test(request, list_folder_to_test):
    print("in main_folder_to_test")
    print(request.param)
    categories = [fold.split('/')[-3] for fold in sorted(list_folder_to_test)]
    print(categories)
    my_dict = dict(zip(categories, sorted(list_folder_to_test)))
    return my_dict[request.param]

# @pytest.fixture(params=[MAIN, AUX])
# def folder_to_test(request, list_folder_to_test):
#     print("in folder to test")
#     print(request.param)
#     if request.param == MAIN:
#         print("in the main...")
#         request.addfinalizer(main_folder_to_test)
#         # return request.getfixturevalue('main_folder_to_test')
#     else:
#         return request.getfixturevalue('aux_folder_to_test')

@pytest.fixture(params=[
    pytest.mark.fixture('my_list')])
def other_folder(request):
    return request.param

# @pytest.fixture(params=[lazy_fixture('my_list')])
# def my_folder(request):
#     print(request.param)
#     return request.param
# @pytest.fixture
# def my_folder(request):
#     return request.getfixturevalue('my_list')

@pytest.fixture(
    params=(glob(os.path.join(QUALTRIP, PARA, AUX, "tripoli*", OUTPUTS))))
def para_aux_folder(request):
    '''Return folder from ``'aux'`` in PARA case to be tested for parsing.'''
    return request.param


@pytest.fixture(
    params=(list(map(lambda x: os.path.join(QUALTRIP, MONO, MAIN, x, OUTPUTS),
                     MAIN_CATEGORIES))))
def main_folder(request):
    '''Return folder from ``'main'`` in MONO case to be tested for parsing.'''
    return request.param


@pytest.fixture(
    params=(list(map(lambda x: os.path.join(QUALTRIP, PARA, MAIN, x, OUTPUTS),
                     MAIN_CATEGORIES))))
def para_main_folder(request):
    '''Return folder from ``'main'`` in PARA case to be tested for parsing.'''
    return request.param


def loop_on_files(filelist):
    '''Perform the loop over the file list, parse all of them and returns
    result of this parsing.

    :param list filelist: list of paths to the files to be read and parsed
    :returns:

             * **nb_jdds_ok**, `int`: number of jdds correctly parsed
               (``'NORMAL COMPLETION'`` and duration at the end)
             * **failed_jdds**, `list of string`: list of the failed jdds
    '''
    nb_jdds_ok = 0
    failed_jdds = []
    for ifile in filelist:
        print("Reading:", ifile)
        found_time = (ep.main(ifile, -1)
                      if os.path.basename(ifile) not in MESH_LIM_FILES
                      else ep.main(ifile, -1, mesh_lim=2))
        if found_time:
            nb_jdds_ok += 1
        else:
            failed_jdds.append(ifile)
    return nb_jdds_ok, failed_jdds


def print_summary(nb_ok, nb_used, failed, excluded):
    '''Print the summary of the parsing, especially lists of failed and
    excluded files.
    '''
    print("Jdds well passed:", nb_ok, "/", nb_used)
    print("Failed jdds:")
    for ifile in failed:
        print(ifile)
    print("Excluded files:")
    for ifile in excluded:
        print(ifile)


@pytest.mark.slow
def test_aux_folder(aux_folder):
    '''Test parsing of ``'aux'`` folders in mono-processor case.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of jdds used, excluded and failed.
    '''
    all_files = sorted(glob(aux_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_MONO)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    category = used_files[0].split('/')[-4]
    print("Tests for category", category, "in MONO")
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    assert len(used_files) == EXPECTED_RESULTS[category][0][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][0][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][0][2]


# @pytest.fixture(params=aux_folder_test)
# def my_fixture(request):
#     return request.param
# @pytest.mark.parametrize("qualtrip", aux_folder_test)
# def test_aux_folder_test(aux_folder_test):
# def test_aux_folder_test(my_fixture):
# @pytest.mark.parametrize('folder', lazy_fixture('my_folder'))
# def test_aux_folder_test(monkeypatch, qualtrip, aux_folder):
# def test_aux_folder_test(aux_folder):
# @pytest.mark.parametrize('folder', [lazy_fixture('my_list')[0]])
# @pytest.mark.parametrize('folder', my_list(qualtrip))
# @pytest.mark.parametrize('my_folder', [my_list()])
# def test_aux_folder_test(other_folder):
# def test_aux_folder_test(gal_folder):
# @pytest.mark.parametrize('folder_to_test', [MAIN_CATEGORIES])
# @pytest.mark.parametrize(('list_folder_to_test','folder_to_test'),
#                          [((MONO, MAIN, MAIN_CATEGORIES), (MAIN_CATEGORIES))],
#                          indirect=['list_folder_to_test'])
# @pytest.mark.parametrize('folder_to_test', [MAIN_CATEGORIES])
# @pytest.mark.parametrize('list_folder_to_test',
#                          [(MONO, MAIN, MAIN_CATEGORIES),
#                           (PARA, MAIN, MAIN_CATEGORIES)],
#                          indirect=['list_folder_to_test'])
# @pytest.mark.parametrize(('main_folder_to_test', 'list_folder_to_test'),
#                          [(MAIN_CATEGORIES[0], (MONO, MAIN, MAIN_CATEGORIES)),
#                           (MAIN_CATEGORIES[1], (MONO, MAIN, MAIN_CATEGORIES))],
#                          indirect=['main_folder_to_test', 'list_folder_to_test'])
@pytest.mark.parametrize(('folder_to_test', 'list_folder_to_test'),
                         [(category, (MONO, MAIN, MAIN_CATEGORIES))
                          for category in MAIN_CATEGORIES]
                         + [(category, (MONO, AUX, AUX_CATEGORIES))
                            for category in AUX_CATEGORIES],
                         indirect=['folder_to_test', 'list_folder_to_test'])
# @pytest.mark.parametrize('folder_to_test', [MAIN_CATEGORIES])
def test_aux_folder_test(folder_to_test):
    # monkeypatch.setattr("tests.eponine.test_all_listings.QUALTRIP", qualtrip)
    # def mon_folder(aux_folder):
    #     return aux_folder
    # print(mon_folder)
    print("mon essai de test:")
    print(QUALTRIP)
    gal_folder = folder_to_test
    print("[34m", gal_folder, "[0m")
    all_files = sorted(glob(gal_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat
                             in EXCLUDED_STRINGS_MONO+EXCLUDED_STRINGS)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    print(used_files)
    # excluded_files = [fil for fil in excluded_files
    #                   if not any(pat in fil for pat in EXCLUDED_STRINGS)]
    # category = used_files[0].split('/')[-4]
    # print("Tests for category", category, "in MONO")
    # jdds_ok, failed_jdds = loop_on_files(used_files)
    # print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    # assert len(used_files) == EXPECTED_RESULTS[category][0][0]
    # assert len(failed_jdds) == EXPECTED_RESULTS[category][0][1]
    # assert len(excluded_files) == EXPECTED_RESULTS[category][0][2]
    # for folder in my_list:
    #     test_aux_folder(folder)
    # print(aux_folder_test)
    # print("[34m", aux_folder, "[0m")
    # print(lazy_fixture(aux_folder))


@pytest.mark.slow
def test_main_folder(main_folder):
    '''Test parsing of ``'main'`` folders in mono-processor case.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of jdds used, excluded and failed.
    '''
    all_files = sorted(glob(main_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    category = used_files[0].split('/')[-4]
    print("Tests for category", category, "in MONO")
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    assert len(used_files) == EXPECTED_RESULTS[category][0][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][0][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][0][2]


@pytest.mark.slow
def test_para_aux_folder(para_aux_folder):
    '''Test parsing of ``'aux'`` folders in parallel case.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of jdds used, excluded and failed.
    '''
    all_files = sorted(glob(para_aux_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    category = used_files[0].split('/')[-4]
    print("Tests for category", category, "in PARA")
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    assert len(used_files) == EXPECTED_RESULTS[category][1][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][1][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][1][2]


@pytest.mark.slow
def test_para_main_folder(para_main_folder):
    '''Test parsing of ``'main'`` folders in parallel case.
    Currently adapted to version 10.2 of Tripoli-4.

    Tests performed on number of jdds used, excluded and failed.
    '''
    all_files = sorted(glob(para_main_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    category = used_files[0].split('/')[-4]
    print("Tests for category", category, "in PARA")
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    assert len(used_files) == EXPECTED_RESULTS[category][1][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][1][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][1][2]
