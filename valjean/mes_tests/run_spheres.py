from os.path import join
from spheresLivermore import Comparison
import numpy as np
from collections import OrderedDict

FOLDER = "/data/tmplepp/el220326/RunTripoli/spheresLivermore"
T4CEAV5 = join(FOLDER, "PARA/ceav5")
T4ENDF = join(FOLDER, "PARA/endfb7r1")
MCNP = join(FOLDER, "MCNP/run")

T4resp30deg = 'neutron_response_30deg'
T4resp30degInt = 'neutron_response_integral_30deg'

# odir = 'final_plots_v6'
odir = 'final_plots_corr'

comp = Comparison()

# comp.set_t4_files([
#     ("Fe_new", join(T4CEAV5, "prob107_fe0p9_fine.SPHAIR.d.res")),
#     ('Fe_new_nbAtom', join(T4CEAV5, "prob107_fe0p9_fine_nbAtom_SPHAIR.d.res")),
#     ("Fe_endfb7r1", join(T4ENDF, "prob107_fe0p9_fine_nbAtom_SPHAIR.d.res")),
#     ('Fe_old', join(T4CEAV5, "iron/prob107.SPHAIR.d.res")),
#     ('Fe_roulette', join(T4CEAV5,
#                          'iron/prob107_fe0p9_fine_roulette_SPHAIR.d.res')),
#     ('Fe_boundLeak', join(T4CEAV5,
#                           'iron/prob107_fe0p9_fine_boundLeakage_SPHAIR.d.res')),
#     ('Fe_sourceGauss', join(T4CEAV5,
#                             'iron/prob107_fe0p9_fine_sourceGauss_SPHAIR.d.res'))])

# comp.set_mcnp_files([
#     ("Fe_30deg", join(FOLDER, "MCNP/results/llnl_ironm"), True),
#     ("Fe_30deg_imp1", join(FOLDER, "MCNP/run/llnl_iron_imp1m"), True)])

# comp.compare_plots(
#     ('IRON', '0.9', '30'),
#     {"Fe_new_nbAtom": [T4resp30deg, T4resp30degInt,
#                        {'fmt': 's-', 'c': 'violet', 'ms': 3, 'mfc': 'plum',
#                         'label': 'T4: atom frac'}],
#      "Fe_endfb7r1": [T4resp30deg, T4resp30degInt,
#                      {'fmt': 'o-', 'c': 'b', "ms": 3, 'mfc': 'lightskyblue',
#                       'label': "T4 endfb7r1"}],
#      "Fe_old": [0, 1, {'fmt': '*-', 'c': 'blueviolet', 'ms': 3,
#                        'mfc': 'mediumslateblue', 'label': 'T4: old'}],
#      "Fe_sourceGauss": [T4resp30deg, T4resp30degInt,
#                         {'fmt': 'o-', 'c': 'limegreen', 'ms': 3, 'mfc': 'lime',
#                          'label': 'T4: source Gauss'}],
#      "Fe_roulette": [T4resp30deg, T4resp30degInt,
#                      {'fmt': 'o-', 'c': 'gold', 'ms': 3, 'mfc': 'yellow',
#                       'label': 'T4: roulette = 100'}],
#      "Fe_boundLeak": [T4resp30deg, T4resp30degInt,
#                       {'fmt': 'o-', 'c': 'crimson', 'ms': 3, 'mfc': 'coral',
#                        'label': 'T4: boundary = Leakage'}]},
#     mcnp={'Fe_30deg': {'c': 'c', 'fmt': '+-'},
#           'Fe_30deg_imp1': {'c': 'salmon', 'fmt': '+-',
#                             'label': "MCNP, imp=1", 'slab': 'MCNPimp1'}},
#     ratios={"T4 atom frac/exp": ['Fe_new_nbAtom', 'exp', {'c': 'violet'}],
#             "MCNP/exp": ['MCNP', 'exp', {'c': 'c'}],
#             "T4 old/exp": ['Fe_old', 'exp', {'c': 'blueviolet'}],
#             "T4 source Gauss/exp": ['Fe_sourceGauss', 'exp', {'c': 'limegreen'}],
#             "T4 roulette/exp": ['Fe_roulette', 'exp', {'c': 'gold'}],
#             "T4 boundary Leakage/exp": ['Fe_boundLeak', 'exp', {'c': 'crimson'}]})


comp.set_monaco_files([
    ('C_monaco_photons', "Monaco/R2/c/finalPaper/photon030R1.out"),
    # ('C_monaco_photons120', 'Monaco/R2/c/finalPaper/photon120R1.out'),
    ('Conc_monaco_photons', "Monaco/R2/conc/finalPaper/photonR1.out"),
    ('Fe_monaco_photons', "Monaco/R2/fe/finalPaper/photon030R1.out"),
    # ('Fe_monaco_photons120', 'Monaco/R2/fe/finalPaper/photon120R1.out'),
    ("N_monaco_photons", "Monaco/R2/n/finalPaper/photonR1.out"),
    ('Be_monaco_photons', 'Monaco/R2/be/finalPaper/photonR1.out')])

comp.set_monaco_files([
    ('C_monaco_30', "Monaco/R2/c/finalPaper/neutron030R1.out"),
    ('C_monaco_120', 'Monaco/R2/c/finalPaper/neutron120R1.out'),
    ('Conc_monaco_120', "Monaco/R2/conc/finalPaper/neutronR1.out"),
    ('Fe_monaco_30', "Monaco/R2/fe/finalPaper/neutron030R1.out"),
    ('Fe_monaco_120', 'Monaco/R2/fe/finalPaper/neutron120R1.out'),
    ("N_monaco_30", "Monaco/R2/n/finalPaper/neutronR1.out"),
    ('Be_monaco_30', 'Monaco/R2/be/finalPaper/neutronR1.out')])

comp.set_mcnp_files([
    ('Conc_mcnp', join(MCNP, 'concrete/llnl_conc_wphotons_nbinsm'), True, (205, 2)),
    ('Conc_mcnp_noimp', join(MCNP, 'concrete/llnl_conc_wphotons_nbins_noimpm'), True, (205, 2)),
    ('Fe_mcnp', join(MCNP, 'iron/llnl_iron_wphotonsm'), True, (205, 2)),
    ('Fe_mcnp_noimp', join(MCNP, 'iron/llnl_iron_wphotons_noimpm'), True, (205, 2)),
    ('Be_mcnp', join(MCNP, 'beryllium/llnl_berl_f2_wphotonsm'), True, (205, 2)),
    ('C_mcnp', join(MCNP, 'carbon/llnl_carbon_wphotonsm'), True, (205, 2)),
    ('N_mcnp', join(MCNP, 'nitrogen/llnl_nitro_wphotonsm'), True, (205, 2)),
])

# comp.set_t4_files([
#     ("Conc_ceav5", join(T4CEAV5, "prob111_concrete_fine_RPSD_SPHAIR.d.res")),
#     ('Conc_endf', join(T4ENDF, "prob111_concrete_fine_RPSD_SPHAIR.d.res")),
#     ("Be_ceav5", join(T4CEAV5, "prob100_fine_RPSD_SPHAIR.d.res")),
#     ("Be_endf", join(T4ENDF, "prob100_fine_RPSD_SPHAIR.d.res")),
#     ("C_ceav5", join(T4CEAV5, "prob102_carboneNat2.9_fine_RPSD_SPHAIR.d.res")),
#     ("C_endf", join(T4ENDF, "prob102_carboneNat2.9_fine_RPSD_SPHAIR.d.res")),
#     ("Fe_ceav5", join(T4CEAV5, "prob107_fe0p9_fine_RPSD_SPHAIR.d.res")),
#     ("Fe_endf", join(T4ENDF, "prob107_fe0p9_fine_RPSD_SPHAIR.d.res")),
#     ("N_ceav5", join(T4CEAV5, "prob103_nitrogen3.1_fine_RPSD_SPHAIR.d.res")),
#     ("N_endf", join(T4ENDF, "prob103_nitrogen3.1_fine_RPSD_SPHAIR.d.res")),
#     # ("Fe_ceav5_leak", join(T4CEAV5, "prob107_fe0p9_fine_all_SPHAIR.d.res")),
#     # ("Fe_endf_leak", join(T4ENDF, "prob107_fe0p9_fine_all_SPHAIR.d.res")),
# ])
comp.set_t4_files([
    ("Conc_ceav5", join(T4CEAV5, "prob111_concrete_fine_timeShifted_SPHAIR.d.res")),
    ('Conc_endf', join(T4ENDF, "prob111_concrete_fine_timeShifted_SPHAIR.d.res")),
    ("Be_ceav5", join(T4CEAV5, "prob100_fine_timeShifted_SPHAIR.d.res")),
    ("Be_endf", join(T4ENDF, "prob100_fine_timeShifted_SPHAIR.d.res")),
    ("C_ceav5", join(T4CEAV5, "prob102_carboneNat2.9_fine_timeShifted_SPHAIR.d.res")),
    ("C_endf", join(T4ENDF, "prob102_carboneNat2.9_fine_timeShifted_SPHAIR.d.res")),
    ("Fe_ceav5", join(T4CEAV5, "prob107_fe0p9_fine_timeShifted_SPHAIR.d.res")),
    ("Fe_endf", join(T4ENDF, "prob107_fe0p9_fine_timeShifted_SPHAIR.d.res")),
    ("N_ceav5", join(T4CEAV5, "prob103_nitrogen3.1_fine_timeShifted_SPHAIR.d.res")),
    ("N_endf", join(T4ENDF, "prob103_nitrogen3.1_fine_timeShifted_SPHAIR.d.res")),
    # ("Fe_ceav5_leak", join(T4CEAV5, "prob107_fe0p9_fine_all_SPHAIR.d.res")),
    # ("Fe_endf_leak", join(T4ENDF, "prob107_fe0p9_fine_all_SPHAIR.d.res")),
])

# normalisation a l'air et a la largeur du bin en energie (*0.1)
def normalisation(aire):
    norm = aire*1.329903e-4*0.1
    return 1/norm

A_N = 2*np.pi*(1+np.sqrt(1-13.60**2/(4*61.11**2)))*61.11**2
Norm_N = normalisation(A_N)
A_Be = 2*np.pi*(1+np.sqrt(1-5.72**2/(4*12.58**2)))*12.58**2
Norm_Be = normalisation(A_Be)
A_C = 2*np.pi*(1+np.sqrt(1-4.67**2/(4*20.96**2)))*20.96**2
Norm_C = normalisation(A_C)
cone_ang_4deg = 4*np.pi/180
theta2_Fe = np.arcsin((1.11*np.cos(cone_ang_4deg)
                       + 0.475*np.sin(cone_ang_4deg))/4.46)
theta_Fe = 4 + theta2_Fe*180/np.pi
A_Fe = 2*np.pi*(1+np.cos(theta_Fe*np.pi/180))*4.46**2
Norm_Fe = normalisation(A_Fe)
theta2_Conc = np.arcsin(((3.8/2)*np.cos(cone_ang_4deg)
                         - 5.1*np.sin(cone_ang_4deg))/21.0)
theta_Conc = 4 + theta2_Conc*180/np.pi
A_Conc = 2*np.pi*(1+np.cos(theta_Conc*np.pi/180))*21.0**2
Norm_Conc = normalisation(A_Conc)

extensions = [".png"]  #, ".pdf", ".svg"]
spheresDict = {
    'N_30': {
        'exp': ('NITROGEN', '3.1', '30'),
        'ceav': 'N_ceav5',
        'endf': 'N_endf',
        'norm': Norm_N,
        'resp_angle': '30deg',
        'monaco_neutrons': 'N_monaco_30',
        'monaco_photons': 'N_monaco_photons',
        # 'mcnp': 'N_mcnp',
        'file_neutrons': join(odir, 'N_3.1_30deg'),
        'file_photons': [join(odir, 'N_3.1_photons.png')]},
    'C_30': {
        'exp': ('CARBON', '2.9', '30'),
        'ceav': 'C_ceav5',
        'endf': 'C_endf',
        'norm': Norm_C,
        'resp_angle': '30deg',
        'monaco_neutrons': 'C_monaco_30',
        'monaco_photons': 'C_monaco_photons',
        # 'mcnp': 'C_mcnp',
        'file_neutrons': join(odir, 'C_2.9_30deg'),
        'file_photons': [join(odir, 'C_2.9_photons.png')]},
    'C_120': {
        'exp': ('CARBON', '2.9', '120'),
        'ceav': 'C_ceav5',
        'endf': 'C_endf',
        'norm': Norm_C,
        'resp_angle': '120deg',
        'monaco_neutrons': 'C_monaco_120',
        'monaco_photons': 'C_monaco_photons',
        'file_neutrons': join(odir, 'C_2.9_120deg'),
        'file_photons': [join(odir, 'C_2.9_photons_120.png')]},
    'Fe_30': {
        'exp': ('IRON', '0.9', '30'),
        'ceav': 'Fe_ceav5',
        'endf': 'Fe_endf',
        'norm': Norm_Fe,
        'resp_angle': '30deg',
        'monaco_neutrons': 'Fe_monaco_30',
        'monaco_photons': 'Fe_monaco_photons',
        # 'mcnp': 'Fe_mcnp',
        'file_neutrons': join(odir, 'Fe_0.9_30deg'),
        'file_photons': [join(odir, 'Fe_0.9_photons.png')]},
    'Fe_120': {
        'exp': ('IRON', '0.9', '120'),
        'ceav': 'Fe_ceav5',
        'endf': 'Fe_endf',
        'norm': Norm_Fe,
        'resp_angle': '120deg',
        'monaco_neutrons': 'Fe_monaco_120',
        'monaco_photons': 'Fe_monaco_photons',
        'file_neutrons': join(odir, 'Fe_0.9_120deg'),
        'file_photons': [join(odir, 'Fe_0.9_photons_120.png')]},
    # 'Fe_30_noimp': {
    #     'exp': ('IRON', '0.9', '30'),
    #     'ceav': 'Fe_ceav5',
    #     'endf': 'Fe_endf',
    #     'norm': Norm_Fe,
    #     'resp_angle': '30deg',
    #     'monaco_neutrons': 'Fe_monaco_30',
    #     'monaco_photons': 'Fe_monaco_photons',
    #     'mcnp': 'Fe_mcnp_noimp',
    #     'file_neutrons': join(odir, 'Fe_0.9_30deg_noimp'),
    #     'file_photons': [join(odir, 'Fe_0.9_photons_noimp.png')]},
    'Be_30': {
        'exp': ('BERYLLIUM', '0.8', '30'),
        'ceav': 'Be_ceav5',
        'endf': 'Be_endf',
        'norm': Norm_Be,
        'resp_angle': '30deg',
        'monaco_neutrons': 'Be_monaco_30',
        'monaco_photons': 'Be_monaco_photons',
        # 'mcnp': 'Be_mcnp',
        'file_neutrons': join(odir, 'Be_0.8_30deg'),
        'file_photons': [join(odir, 'Be_0.8_photons.png')]},
    'Conc_120': {
        'exp': ('CONCRETE', '2.0', '120'),
        'ceav': 'Conc_ceav5',
        'endf': 'Conc_endf',
        'norm': Norm_Conc,
        'resp_angle': '120deg',
        'monaco_neutrons': 'Conc_monaco_120',
        'monaco_photons': 'Conc_monaco_photons',
        # 'mcnp': 'Conc_mcnp',
        'file_neutrons': join(odir, 'Conc_2.0_120deg'),
        'file_photons': [join(odir, 'Conc_2.0_photons.png')]},
    # 'Conc_120_noimp': {
    #     'exp': ('CONCRETE', '2.0', '120'),
    #     'ceav': 'Conc_ceav5',
    #     'endf': 'Conc_endf',
    #     'norm': Norm_Conc,
    #     'resp_angle': '120deg',
    #     'monaco_neutrons': 'Conc_monaco_120',
    #     'monaco_photons': 'Conc_monaco_photons',
    #     # 'mcnp': 'Conc_mcnp_noimp',
    #     'file_neutrons': join(odir, 'Conc_2.0_120deg_noimp'),
    #     'file_photons': [join(odir, 'Conc_2.0_photons_noimp.png')]}
}

for key, sphere in spheresDict.items():
    # in the loop due to pop (of ewidth) -> precaution
    mcnp_n_style =  {'c': 'C3', 'label': 'MCNP', 'drawstyle': 'steps-mid'}
    mcnp_p_tal2 = {'c': 'C3', 'label': 'MCNP', 'drawstyle': 'steps-mid',
                   'ls': '-', 'tally': 2, 'ewidth': 10}

    print(sphere)
    print(sphere['exp'])
    t4_ordDict = OrderedDict()
    t4_ordDict[sphere['ceav']] = {
        'photon_flux_sphere':
        {'sphere': {'label': "T4, JEFF-3.1.1",
                    'c': 'C0', 'drawstyle': 'steps-mid',
                    'ls': '-','ewidth': sphere['norm']}}}
    t4_ordDict[sphere['endf']] = {
        'photon_flux_sphere':
        {'sphere': {'label': 'T4, ENDF/BVII.1',
                    'c': 'C2', 'drawstyle': 'steps-mid',
                    'ls': '-', 'ewidth': sphere['norm']}}}
    mcnp_p_plot = {sphere['mcnp']: [mcnp_p_tal2]} if 'mcnp' in sphere else {}
    mcnp_p_ratio = (sphere['mcnp'], sphere['endf'],
                    {'c': 'C3', 'label': 'MCNP, ENDF / T4, ENDF',
                     'drawstyle': 'steps-mid'}) if 'mcnp' in sphere else ()
    comp.compare_photons(
        sphere['exp'],
        t4_ordDict,
        monaco={sphere['monaco_photons']: {
            'c': 'C1',
            'label': 'MONACO, ENDF/BVII.1',
            'ls': '-', 'ewidth': 10, 'drawstyle': 'steps-mid'}},
        mcnp=mcnp_p_plot,
        ratio=[(sphere['monaco_photons'], sphere['endf'],
                {'c': 'C1', 'label': 'MONACO, ENDF / T4, ENDF',
                 'drawstyle': 'steps-mid'}),
               (sphere['ceav'], sphere['endf'],
                {'c': 'C0', 'label': 'T4, JEFF / T4, ENDF',
                 'drawstyle': 'steps-mid'}),
               mcnp_p_ratio],
        save_file=sphere['file_photons'])

    t4_ordDict_n = OrderedDict()
    t4_ordDict_n[sphere['ceav']] = [
        'neutron_response_'+sphere['resp_angle'],
        'neutron_response_integral_'+sphere['resp_angle'],
        {'fmt': '-', 'label': 'T4, JEFF-3.1.1',
         'c': 'C0', 'slab': 'ceav5',
         'drawstyle': 'steps-mid'}]
    t4_ordDict_n[sphere['endf']] = [
        'neutron_response_'+sphere['resp_angle'],
        'neutron_response_integral_'+sphere['resp_angle'],
        {'fmt': '-', 'label': 'T4, ENDF/BVII.1',
         'c': 'C2', 'slab': 'endf',
         'drawstyle': 'steps-mid'}]
    mcnp_plot = {sphere['mcnp']: mcnp_n_style} if 'mcnp' in sphere else {}
    for ext in extensions:
        comp.compare_plots(
            sphere['exp'],
            t4_ordDict_n,
            monaco={sphere['monaco_neutrons']: {'c': 'C1',
                                                'label': 'MONACO ENDF/BVII.1',
                                                'fmt': '-',
                                                'drawstyle': 'steps-mid'}},
            mcnp=mcnp_plot,
            ratios={'T4, ENDF/exp': ['endf', 'exp',
                                     {'c': 'C2',
                                      'drawstyle': 'steps-mid'}],
                    "T4, JEFF/exp": ["ceav5", 'exp',
                                     {'c': 'C0',
                                      'drawstyle': 'steps-mid'}],
                    'MONACO, ENDF/exp': ['MONACO', 'exp',
                                         {'c': 'C1',
                                          'drawstyle': 'steps-mid'}],
                    'MCNP, ENDF/exp': ['MCNP', 'exp',
                                       {'c': 'C3',
                                        'drawstyle': 'steps-mid'}]},
            save_file=sphere['file_neutrons']+ext)


if "Fe_ceav5_leak" in comp.simu_res:
    fe_ordered_120 = OrderedDict()
    fe_ordered_120["Fe_ceav5"] = ['neutron_response_120deg',
                                  'neutron_response_integral_120deg',
                                  {'fmt': '-', 'label': 'T4, JEFF-3.1.1', 'c': 'C0',
                                   'slab': 'ceav5', 'drawstyle': 'steps-mid'}]
    fe_ordered_120["Fe_endf"] = ['neutron_response_120deg',
                                 'neutron_response_integral_120deg',
                                 {'fmt': '-', 'label': 'T4, ENDF/BVII.1', 'c': 'C2',
                                  'slab': 'endf', 'drawstyle': 'steps-mid'}]
    fe_ordered_120["Fe_ceav5_leak"] = ['neutron_response_120deg',
                                       'neutron_response_integral_120deg',
                                       {'fmt': '-', 'label': 'T4, JEFF-3.1.1, leak',
                                        'c': 'C3', 'slab': 'ceav5_leak',
                                        'drawstyle': 'steps-mid'}]
    fe_ordered_120["Fe_endf_leak"] = ['neutron_response_120deg',
                                      'neutron_response_integral_120deg',
                                      {'fmt': '-', 'label': 'T4, ENDF/BVII.1, leak',
                                       'c': 'C4', 'slab': 'endf_leak',
                                       'drawstyle': 'steps-mid'}]


    fe_ordered_30 = OrderedDict()
    fe_ordered_30["Fe_ceav5"] = ['neutron_response_30deg',
                                 'neutron_response_integral_30deg',
                                 {'fmt': '-', 'label': 'T4, JEFF-3.1.1', 'c': 'C0',
                                  'slab': 'ceav5', 'drawstyle': 'steps-mid'}]
    fe_ordered_30["Fe_endf"] = ['neutron_response_30deg',
                                'neutron_response_integral_30deg',
                                {'fmt': '-', 'label': 'T4, ENDF/BVII.1', 'c': 'C2',
                                 'slab': 'endf', 'drawstyle': 'steps-mid'}]
    fe_ordered_30["Fe_ceav5_leak"] = ['neutron_response_30deg',
                                      'neutron_response_integral_30deg',
                                      {'fmt': '-', 'label': 'T4, JEFF-3.1.1, leak',
                                       'c': 'C3', 'slab': 'ceav5_leak',
                                       'drawstyle': 'steps-mid'}]
    fe_ordered_30["Fe_endf_leak"] = ['neutron_response_30deg',
                                     'neutron_response_integral_30deg',
                                     {'fmt': '-', 'label': 'T4, ENDF/BVII.1, leak',
                                      'c': 'C4', 'slab': 'endf_leak',
                                      'drawstyle': 'steps-mid'}]

    fe_ratios={'T4, ENDF/exp': ['endf', 'exp',
                                {'c': 'C2','drawstyle': 'steps-mid'}],
               "T4, JEFF/exp": ["ceav5", 'exp',
                                {'c': 'C0', 'drawstyle': 'steps-mid'}],
               'T4, ENDF, leakage/exp': ['endf_leak', 'exp',
                                         {'c': 'C4', 'drawstyle': 'steps-mid'}],
               'T4, JEFF, leakage/exp': ["ceav5_leak", 'exp',
                                         {'c': 'C3', 'drawstyle': 'steps-mid'}]}

    for ext in extensions:
        comp.compare_plots(('IRON', '0.9', '120'),
                           fe_ordered_120,
                           ratios=fe_ratios,
                           save_file=join(odir, "Fe_0.9_120deg_collimators"+ext))
        comp.compare_plots(('IRON', '0.9', '30'),
                           fe_ordered_30,
                           ratios=fe_ratios,
                           save_file=join(odir, "Fe_0.9_30deg_collimators"+ext))
