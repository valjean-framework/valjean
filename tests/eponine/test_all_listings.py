import sys
import os
from glob import glob
import pytest

import valjean.eponine.parse_t4 as ep

QUALTRIP = "/data/tmplepp/el220326/QualTassadit/RC1/"
MONO = "MONO"
PARA = "PARA"
AUX = "qualtrip_aux"
MAIN = "qualtrip_main"
OUTPUTS = "output/ceav5"
MAIN_CATEGORIES = ["cristal", "elem", "protection"]

EXCLUDED_STRINGS_MONO = ["perle", "epicure", "part1", "phn_intrumen",
                         "test_pondng_auto_coupling", "gado_assembly",
                         "_v0", "sauv"]
EXCLUDED_STRINGS_PARA = ["part1", "exp", "etape2", "homog_p3_prot",
                         "test_pondng_auto_coupling",
                         "gado_assembly", "sauv"]
MESH_LIM_FILES = ['godivaBeff_MED.d.res.ceav5']

EXPECTED_RESULTS = {"cristal": [[148, 0, 0], [148, 0, 0]],
                    "elem": [[99, 0, 1], [99, 0, 0]],
                    "protection": [[25, 0, 0], [25, 0, 0]],
                    "tripoli44": [[23, 0, 0], [18, 1, 4]],
                    "tripoli45": [[24, 0, 0], [21, 0, 2]],
                    "tripoli46": [[8, 0, 0], [5, 0, 3]],
                    "tripoli47": [[27, 0, 1], [28, 0, 0]],
                    "tripoli48": [[36, 0, 2], [37, 0, 3]],
                    "tripoli49": [[44, 0, 1], [36, 0, 1]],
                    "tripoli410":[[62, 5, 5], [59, 4, 6]],
                    "tripoli4102": [[2, 0, 2], []]}


@pytest.fixture(
    params=(glob(os.path.join(QUALTRIP, MONO, AUX, "tripoli*", OUTPUTS))))
def aux_folder(request):
    print(request.param)
    fold = request.param
    return fold

@pytest.fixture(
    params=(glob(os.path.join(QUALTRIP, PARA, AUX, "tripoli*", OUTPUTS))))
def para_aux_folder(request):
    print(request.param)
    fold = request.param
    return fold

@pytest.fixture(
    params=(list(map(lambda x: os.path.join(QUALTRIP, MONO, MAIN, x, OUTPUTS),
                     MAIN_CATEGORIES))))
def main_folder(request):
    return request.param

@pytest.fixture(
    params=(list(map(lambda x: os.path.join(QUALTRIP, PARA, MAIN, x, OUTPUTS),
                     MAIN_CATEGORIES))))
def para_main_folder(request):
    return request.param

def loop_on_files(filelist):
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
    print("Jdds well passed:", nb_ok, "/", nb_used)
    print("Failed jdds:")
    for ifile in failed:
        print(ifile)
    print("Excluded files:")
    for ifile in excluded:
        print(ifile)

def test_aux_folder(aux_folder):
    print("FOLDER:", aux_folder)
    all_files = sorted(glob(aux_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_MONO)]
    # print("[31m", excluded_files, "[0m")
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    # print(usedfiles)
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    assert len(used_files) == EXPECTED_RESULTS[category][0][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][0][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][0][2]

def test_main_folder(main_folder):
    print("FOLDER:", main_folder)
    all_files = sorted(glob(main_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    # print("[31m", excluded_files, "[0m")
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    # print(usedfiles)
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    assert len(used_files) == EXPECTED_RESULTS[category][0][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][0][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][0][2]

def test_para_aux_folder(para_aux_folder):
    print("FOLDER:", para_aux_folder)
    all_files = sorted(glob(para_aux_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    # print("[31m", excluded_files, "[0m")
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    # print(usedfiles)
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    assert len(used_files) == EXPECTED_RESULTS[category][1][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][1][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][1][2]


def test_para_main_folder(para_main_folder):
    print("FOLDER:", para_main_folder)
    all_files = sorted(glob(para_main_folder+"/*.res.ceav5"))
    excluded_files = [fil for fil in all_files
                      if any(pat in fil for pat in EXCLUDED_STRINGS_PARA)]
    # print("[31m", excluded_files, "[0m")
    used_files = list(filter(lambda x: x not in excluded_files, all_files))
    # print(usedfiles)
    jdds_ok, failed_jdds = loop_on_files(used_files)
    print_summary(jdds_ok, len(used_files), failed_jdds, excluded_files)
    category = used_files[0].split('/')[-4]
    assert len(used_files) == EXPECTED_RESULTS[category][1][0]
    assert len(failed_jdds) == EXPECTED_RESULTS[category][1][1]
    assert len(excluded_files) == EXPECTED_RESULTS[category][1][2]
