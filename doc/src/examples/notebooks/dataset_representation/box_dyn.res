
=====================================================================
$Id$
 hostname: 
 pid: 4203

=====================================================================
$Id$

 HOSTNAME : 

 PROCESS ID is : 4203

 DATE : Tue May 10 14:30:02 2022

 Version is $Name$.

 git version is ffc75da7e58d9571e4426cde942f44ffadd996f4 (CLEAN).

=====================================================================

 data filename = box_dyn.t4
 catalogname = t4path.ceav512
 execution call = tripoli4 -c t4path.ceav512 -s NJOY -a -d box_dyn.t4 -o box_dyn.res 


 dictionary file : ceav512.dictionary
 mass file : mass_rmd.mas95
 Q fission directory : Qfission
 electron cross section directory : Electron_Photon
 electron bremsstrahlung cross section directory : Bremsstrahlung
 abondance file : abundance
 own evaluations directory : 

  reading geometry : 
  checking association of compositions and volumes :  ok 


/* This input file tests kinetic transport. It describes a homogeneous box. The
 * system is very nearly critical with ceav512 (keff = 0.99996 ± 0.00001);
 * therefore, the total flux in the system should be constant over time.
 * D. Mancusi, 1/7/2020
 */

LANG ENGLISH
GEOMETRY
  TITLE box
  TYPE 1 BOX 10 20 24
  VOLU 1 COMBI 1 0 0 0 ENDV
ENDGEOM

COMPOSITION 1
PONCTUAL 824 FUEL 1 U235 0.044925
END_COMPOSITION

GEOMCOMP
  FUEL 1 1
END_GEOMCOMP

SOURCES_LIST  1
    SOURCE
    NORM 1.
    NEUTRON
    FACTORIZED
      FRAME CARTESIAN
      0 0 0
      1 0 0
      0 1 0
      0 0 1
    ALL_VOLUMES_INSIDE_MESH
    GEOMETRIC_DISTRIBUTION TABULATED
      TYPE F_UVW
      VAR_U X 2 -5 5
      VAR_V Y 2 -10 10
      VAR_W Z 2 -12 12
      F_UVW 1
    ANGULAR_DISTRIBUTION ISOTROPIC.
    ENERGETIC_DISTRIBUTION SPECTRUM WATT_SPECTRUM
    TIME_DISTRIBUTION DIRAC 0.			 	   
    END_SOURCE		 	 
END_SOURCES_LIST

GRID_LIST 2
  grid_rough 3 1e-11 1e-3 20
  grid_time 11 0 IN_LIN 9 3.13e-6
END_GRID_LIST


RESPONSES 1
 NAME neutron_flux_response FLUX NEUTRON
END_RESPONSES

SCORE 1
    NAME neutron_flux_mesh_score
    neutron_flux_response
    TRACK
    GRID grid_rough
    EXTENDED_MESH MESH_INFO
      WINDOW
        -5.0 -5.0 -12.0
        5.0 5.0 12.0
        3 3 3
      FRAME CARTESIAN
        0 0 0
        1 0 0
        0 1 0
        0 0 1
END_SCORE

SIMULATION
    DYNAMIC
        GRID grid_time
        POPULATION_CONTROL COMBING
        CRITICALITY_SOURCE 200 1
        POPULATION_IMPORTANCE_RATIO 7e-8
    BATCH 10
    SIZE 1000
    EDITION 10
    PARTICLES 2 NEUTRON PRECURSOR
    TIME_INF NEUTRON 0
    TIME_SUP NEUTRON 3.13e-6
END_SIMULATION



 data reading time (s): 0

 Total concentration of material FUEL (1.E24at/cm3) is: 4.492500e-02


 Loading response functions ...
 Constructing score  ...0
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 9.999997e-01

		 Energetic density simulation intensity = 9.999997e-01

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 4.800000e+03

		 Calculated source simulation intensity = 6.031856e+04

		 Calculated source definition intensity = 6.031856e+04

	         NORM = 1.000000e+00   SIMULATION INTENSITY = 1.000000e+00   BIASED SIMULATION INTENSITY = 1.000000e+00

   SUM OF SIMULATION INTENSITIES = 1.000000e+00

   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 0


 batch number : 1

  Preparing critical source : iteration 1 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.380000e+00	 sigma_n : 8.866488e-02
	 number of secondary particules: 970
	 number of fission neutrons: 970
  Preparing critical source : iteration 2 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569072e+00	 sigma_n : 8.530534e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004
  Preparing critical source : iteration 3 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724104e+00	 sigma_n : 9.063649e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063
  Preparing critical source : iteration 4 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.404516e+00	 sigma_n : 7.802154e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030
  Preparing critical source : iteration 5 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666019e+00	 sigma_n : 9.085643e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061
  Preparing critical source : iteration 6 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622055e+00	 sigma_n : 8.484177e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120
  Preparing critical source : iteration 7 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578571e+00	 sigma_n : 8.592494e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152
  Preparing critical source : iteration 8 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.424479e+00	 sigma_n : 7.878091e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174
  Preparing critical source : iteration 9 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.404600e+00	 sigma_n : 7.481880e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133
  Preparing critical source : iteration 10 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.331862e+00	 sigma_n : 7.952523e-02
	 number of secondary particules: 989
	 number of fission neutrons: 989
  Preparing critical source : iteration 11 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.879676e+00	 sigma_n : 9.832479e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160
  Preparing critical source : iteration 12 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.391379e+00	 sigma_n : 7.289698e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137
  Preparing critical source : iteration 13 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.394899e+00	 sigma_n : 7.744916e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049
  Preparing critical source : iteration 14 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530029e+00	 sigma_n : 8.356723e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067
  Preparing critical source : iteration 15 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547329e+00	 sigma_n : 7.895385e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048
  Preparing critical source : iteration 16 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720420e+00	 sigma_n : 8.963120e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131
  Preparing critical source : iteration 17 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643678e+00	 sigma_n : 7.836963e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161
  Preparing critical source : iteration 18 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.374677e+00	 sigma_n : 7.717856e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096
  Preparing critical source : iteration 19 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543796e+00	 sigma_n : 8.157358e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090
  Preparing critical source : iteration 20 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.433945e+00	 sigma_n : 7.701073e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065
  Preparing critical source : iteration 21 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582160e+00	 sigma_n : 8.538317e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099
  Preparing critical source : iteration 22 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.508644e+00	 sigma_n : 7.680674e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097
  Preparing critical source : iteration 23 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515041e+00	 sigma_n : 8.081307e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079
  Preparing critical source : iteration 24 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.488415e+00	 sigma_n : 8.058552e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090
  Preparing critical source : iteration 25 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655963e+00	 sigma_n : 8.620967e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125
  Preparing critical source : iteration 26 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525333e+00	 sigma_n : 8.270118e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169
  Preparing critical source : iteration 27 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.485030e+00	 sigma_n : 8.203167e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127
  Preparing critical source : iteration 28 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491571e+00	 sigma_n : 8.743636e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105
  Preparing critical source : iteration 29 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.411765e+00	 sigma_n : 7.836515e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103
  Preparing critical source : iteration 30 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757933e+00	 sigma_n : 9.034109e-02
	 number of secondary particules: 1202
	 number of fission neutrons: 1202
  Preparing critical source : iteration 31 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.342762e+00	 sigma_n : 7.516847e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105
  Preparing critical source : iteration 32 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.484163e+00	 sigma_n : 8.211603e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096
  Preparing critical source : iteration 33 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578467e+00	 sigma_n : 8.156007e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110
  Preparing critical source : iteration 34 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542342e+00	 sigma_n : 8.181321e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 35 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547135e+00	 sigma_n : 8.064073e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087
  Preparing critical source : iteration 36 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571297e+00	 sigma_n : 8.641948e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119
  Preparing critical source : iteration 37 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468275e+00	 sigma_n : 8.107170e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085
  Preparing critical source : iteration 38 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556682e+00	 sigma_n : 8.255492e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067
  Preparing critical source : iteration 39 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503280e+00	 sigma_n : 7.922275e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047
  Preparing critical source : iteration 40 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592168e+00	 sigma_n : 8.197208e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049
  Preparing critical source : iteration 41 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.472831e+00	 sigma_n : 7.795928e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037
  Preparing critical source : iteration 42 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543877e+00	 sigma_n : 8.147300e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064
  Preparing critical source : iteration 43 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574248e+00	 sigma_n : 8.603609e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066
  Preparing critical source : iteration 44 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523452e+00	 sigma_n : 8.332253e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067
  Preparing critical source : iteration 45 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653233e+00	 sigma_n : 8.752667e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104
  Preparing critical source : iteration 46 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515399e+00	 sigma_n : 8.133554e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138
  Preparing critical source : iteration 47 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.509666e+00	 sigma_n : 8.481761e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123
  Preparing critical source : iteration 48 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512021e+00	 sigma_n : 8.076297e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118
  Preparing critical source : iteration 49 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532200e+00	 sigma_n : 7.977940e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104
  Preparing critical source : iteration 50 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491848e+00	 sigma_n : 7.747904e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095
  Preparing critical source : iteration 51 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579909e+00	 sigma_n : 8.483147e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146
  Preparing critical source : iteration 52 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.460733e+00	 sigma_n : 8.194283e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163
  Preparing critical source : iteration 53 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.294927e+00	 sigma_n : 7.174339e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049
  Preparing critical source : iteration 54 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689228e+00	 sigma_n : 9.128421e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116
  Preparing critical source : iteration 55 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.450717e+00	 sigma_n : 7.758536e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105
  Preparing critical source : iteration 56 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630769e+00	 sigma_n : 8.699896e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105
  Preparing critical source : iteration 57 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519457e+00	 sigma_n : 8.602527e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041
  Preparing critical source : iteration 58 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699328e+00	 sigma_n : 9.082498e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084
  Preparing critical source : iteration 59 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691882e+00	 sigma_n : 8.780546e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151
  Preparing critical source : iteration 60 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.377932e+00	 sigma_n : 7.859588e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069
  Preparing critical source : iteration 61 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.485500e+00	 sigma_n : 7.890973e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036
  Preparing critical source : iteration 62 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583977e+00	 sigma_n : 8.363185e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060
  Preparing critical source : iteration 63 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567925e+00	 sigma_n : 8.733523e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046
  Preparing critical source : iteration 64 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614723e+00	 sigma_n : 8.842003e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063
  Preparing critical source : iteration 65 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.795861e+00	 sigma_n : 9.083549e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138
  Preparing critical source : iteration 66 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.443761e+00	 sigma_n : 7.854689e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103
  Preparing critical source : iteration 67 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702629e+00	 sigma_n : 9.058707e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172
  Preparing critical source : iteration 68 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.303754e+00	 sigma_n : 8.046510e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055
  Preparing critical source : iteration 69 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585782e+00	 sigma_n : 7.997402e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073
  Preparing critical source : iteration 70 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637465e+00	 sigma_n : 8.737734e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130
  Preparing critical source : iteration 71 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.441593e+00	 sigma_n : 8.237371e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 72 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637708e+00	 sigma_n : 8.547803e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137
  Preparing critical source : iteration 73 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.461741e+00	 sigma_n : 7.837774e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 74 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621996e+00	 sigma_n : 8.183156e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125
  Preparing critical source : iteration 75 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553778e+00	 sigma_n : 8.272732e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107
  Preparing critical source : iteration 76 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645890e+00	 sigma_n : 8.921621e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153
  Preparing critical source : iteration 77 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489159e+00	 sigma_n : 7.871582e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142
  Preparing critical source : iteration 78 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514011e+00	 sigma_n : 8.275348e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148
  Preparing critical source : iteration 79 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.394599e+00	 sigma_n : 8.085459e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128
  Preparing critical source : iteration 80 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.393617e+00	 sigma_n : 7.705084e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072
  Preparing critical source : iteration 81 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709888e+00	 sigma_n : 8.848265e-02
	 number of secondary particules: 1179
	 number of fission neutrons: 1179
  Preparing critical source : iteration 82 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.335878e+00	 sigma_n : 7.417291e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065
  Preparing critical source : iteration 83 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589671e+00	 sigma_n : 8.452423e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058
  Preparing critical source : iteration 84 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556711e+00	 sigma_n : 8.408688e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062
  Preparing critical source : iteration 85 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594162e+00	 sigma_n : 8.435588e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077
  Preparing critical source : iteration 86 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610028e+00	 sigma_n : 8.632720e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096
  Preparing critical source : iteration 87 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.439781e+00	 sigma_n : 7.785295e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094
  Preparing critical source : iteration 88 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.425960e+00	 sigma_n : 7.362395e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065
  Preparing critical source : iteration 89 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644131e+00	 sigma_n : 8.761273e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116
  Preparing critical source : iteration 90 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.448925e+00	 sigma_n : 8.312496e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073
  Preparing critical source : iteration 91 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513514e+00	 sigma_n : 8.128513e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076
  Preparing critical source : iteration 92 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632900e+00	 sigma_n : 8.871675e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144
  Preparing critical source : iteration 93 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.484266e+00	 sigma_n : 8.730078e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 94 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640481e+00	 sigma_n : 9.087468e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130
  Preparing critical source : iteration 95 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.398230e+00	 sigma_n : 7.730862e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036
  Preparing critical source : iteration 96 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582046e+00	 sigma_n : 8.660295e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039
  Preparing critical source : iteration 97 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577478e+00	 sigma_n : 7.847423e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055
  Preparing critical source : iteration 98 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566825e+00	 sigma_n : 7.933643e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102
  Preparing critical source : iteration 99 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569873e+00	 sigma_n : 9.116634e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087
  Preparing critical source : iteration 100 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615455e+00	 sigma_n : 8.293322e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121
  Preparing critical source : iteration 101 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493310e+00	 sigma_n : 8.236868e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087
  Preparing critical source : iteration 102 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516099e+00	 sigma_n : 8.195819e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060
  Preparing critical source : iteration 103 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645283e+00	 sigma_n : 9.224875e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121
  Preparing critical source : iteration 104 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622658e+00	 sigma_n : 8.072380e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144
  Preparing critical source : iteration 105 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.361014e+00	 sigma_n : 7.906396e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096
  Preparing critical source : iteration 106 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548358e+00	 sigma_n : 8.452110e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154
  Preparing critical source : iteration 107 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.212305e+00	 sigma_n : 7.638302e-02
	 number of secondary particules: 970
	 number of fission neutrons: 970
  Preparing critical source : iteration 108 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661856e+00	 sigma_n : 9.174246e-02
	 number of secondary particules: 985
	 number of fission neutrons: 985
  Preparing critical source : iteration 109 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743147e+00	 sigma_n : 9.254994e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086
  Preparing critical source : iteration 110 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493554e+00	 sigma_n : 7.666451e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083
  Preparing critical source : iteration 111 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558633e+00	 sigma_n : 8.819645e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086
  Preparing critical source : iteration 112 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617864e+00	 sigma_n : 8.417288e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136
  Preparing critical source : iteration 113 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.401408e+00	 sigma_n : 7.750370e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135
  Preparing critical source : iteration 114 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628194e+00	 sigma_n : 8.883423e-02
	 number of secondary particules: 1192
	 number of fission neutrons: 1192
  Preparing critical source : iteration 115 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.310403e+00	 sigma_n : 7.631966e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144
  Preparing critical source : iteration 116 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525350e+00	 sigma_n : 8.074540e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109
  Preparing critical source : iteration 117 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.455365e+00	 sigma_n : 7.767165e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106
  Preparing critical source : iteration 118 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.449367e+00	 sigma_n : 7.934287e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088
  Preparing critical source : iteration 119 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613051e+00	 sigma_n : 8.278976e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113
  Preparing critical source : iteration 120 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.483378e+00	 sigma_n : 8.267681e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133
  Preparing critical source : iteration 121 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.456311e+00	 sigma_n : 7.629205e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169
  Preparing critical source : iteration 122 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473909e+00	 sigma_n : 8.500214e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135
  Preparing critical source : iteration 123 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.474009e+00	 sigma_n : 8.174658e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067
  Preparing critical source : iteration 124 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570759e+00	 sigma_n : 9.159904e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127
  Preparing critical source : iteration 125 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489796e+00	 sigma_n : 8.584452e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157
  Preparing critical source : iteration 126 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511668e+00	 sigma_n : 8.274337e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168
  Preparing critical source : iteration 127 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514555e+00	 sigma_n : 8.275949e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145
  Preparing critical source : iteration 128 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.331878e+00	 sigma_n : 7.681938e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060
  Preparing critical source : iteration 129 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.417925e+00	 sigma_n : 8.020909e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030
  Preparing critical source : iteration 130 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571845e+00	 sigma_n : 8.270813e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058
  Preparing critical source : iteration 131 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.484877e+00	 sigma_n : 7.973745e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032
  Preparing critical source : iteration 132 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796512e+00	 sigma_n : 9.691357e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126
  Preparing critical source : iteration 133 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516874e+00	 sigma_n : 8.107809e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119
  Preparing critical source : iteration 134 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.554066e+00	 sigma_n : 9.056239e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117
  Preparing critical source : iteration 135 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512981e+00	 sigma_n : 7.568725e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136
  Preparing critical source : iteration 136 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618838e+00	 sigma_n : 8.563783e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155
  Preparing critical source : iteration 137 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.333333e+00	 sigma_n : 7.588149e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078
  Preparing critical source : iteration 138 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612245e+00	 sigma_n : 8.301945e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099
  Preparing critical source : iteration 139 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566879e+00	 sigma_n : 7.984935e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132
  Preparing critical source : iteration 140 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568021e+00	 sigma_n : 8.804961e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098
  Preparing critical source : iteration 141 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.418033e+00	 sigma_n : 8.001185e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049
  Preparing critical source : iteration 142 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680648e+00	 sigma_n : 9.113127e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129
  Preparing critical source : iteration 143 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.458813e+00	 sigma_n : 8.052759e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128
  Preparing critical source : iteration 144 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.456560e+00	 sigma_n : 8.262093e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136
  Preparing critical source : iteration 145 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.455106e+00	 sigma_n : 7.972714e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109
  Preparing critical source : iteration 146 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541028e+00	 sigma_n : 8.403472e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129
  Preparing critical source : iteration 147 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464128e+00	 sigma_n : 7.772140e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074
  Preparing critical source : iteration 148 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553073e+00	 sigma_n : 8.059492e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050
  Preparing critical source : iteration 149 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653333e+00	 sigma_n : 9.186737e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103
  Preparing critical source : iteration 150 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.460562e+00	 sigma_n : 8.489348e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 151 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.272643e+00	 sigma_n : 7.556406e-02
	 number of secondary particules: 946
	 number of fission neutrons: 946
  Preparing critical source : iteration 152 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743129e+00	 sigma_n : 9.252146e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027
  Preparing critical source : iteration 153 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699124e+00	 sigma_n : 8.794693e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118
  Preparing critical source : iteration 154 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.363148e+00	 sigma_n : 7.483983e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049
  Preparing critical source : iteration 155 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704480e+00	 sigma_n : 8.786038e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102
  Preparing critical source : iteration 156 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490926e+00	 sigma_n : 8.275621e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089
  Preparing critical source : iteration 157 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556474e+00	 sigma_n : 8.767060e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080
  Preparing critical source : iteration 158 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581481e+00	 sigma_n : 8.678531e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126
  Preparing critical source : iteration 159 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.309059e+00	 sigma_n : 7.739823e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050
  Preparing critical source : iteration 160 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583810e+00	 sigma_n : 8.363873e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040
  Preparing critical source : iteration 161 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566346e+00	 sigma_n : 8.574998e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042
  Preparing critical source : iteration 162 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602687e+00	 sigma_n : 8.520796e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077
  Preparing critical source : iteration 163 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521820e+00	 sigma_n : 8.319422e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087
  Preparing critical source : iteration 164 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507820e+00	 sigma_n : 7.784580e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105
  Preparing critical source : iteration 165 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.509502e+00	 sigma_n : 7.734651e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084
  Preparing critical source : iteration 166 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515683e+00	 sigma_n : 8.877816e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066
  Preparing critical source : iteration 167 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564728e+00	 sigma_n : 8.924413e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094
  Preparing critical source : iteration 168 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.478976e+00	 sigma_n : 7.582600e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032
  Preparing critical source : iteration 169 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679264e+00	 sigma_n : 9.200617e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119
  Preparing critical source : iteration 170 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.447721e+00	 sigma_n : 8.012990e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075
  Preparing critical source : iteration 171 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622326e+00	 sigma_n : 8.434040e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093
  Preparing critical source : iteration 172 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462946e+00	 sigma_n : 7.917356e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035
  Preparing critical source : iteration 173 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733333e+00	 sigma_n : 8.872358e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111
  Preparing critical source : iteration 174 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468947e+00	 sigma_n : 8.583888e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092
  Preparing critical source : iteration 175 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619963e+00	 sigma_n : 8.482020e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082
  Preparing critical source : iteration 176 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596118e+00	 sigma_n : 8.987834e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098
  Preparing critical source : iteration 177 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.433515e+00	 sigma_n : 7.930588e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059
  Preparing critical source : iteration 178 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.446648e+00	 sigma_n : 7.689998e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045
  Preparing critical source : iteration 179 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579904e+00	 sigma_n : 8.629627e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059
  Preparing critical source : iteration 180 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779037e+00	 sigma_n : 9.370637e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113
  Preparing critical source : iteration 181 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575022e+00	 sigma_n : 8.244215e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101
  Preparing critical source : iteration 182 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.488647e+00	 sigma_n : 7.816272e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052
  Preparing critical source : iteration 183 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584601e+00	 sigma_n : 8.569483e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092
  Preparing critical source : iteration 184 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586996e+00	 sigma_n : 8.679349e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093
  Preparing critical source : iteration 185 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507777e+00	 sigma_n : 8.031579e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062
  Preparing critical source : iteration 186 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518832e+00	 sigma_n : 8.268248e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059
  Preparing critical source : iteration 187 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514636e+00	 sigma_n : 7.547539e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054
  Preparing critical source : iteration 188 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765655e+00	 sigma_n : 9.129828e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117
  Preparing critical source : iteration 189 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538944e+00	 sigma_n : 8.264124e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141
  Preparing critical source : iteration 190 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.424189e+00	 sigma_n : 7.944046e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104
  Preparing critical source : iteration 191 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.441123e+00	 sigma_n : 8.131754e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091
  Preparing critical source : iteration 192 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463795e+00	 sigma_n : 7.853874e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056
  Preparing critical source : iteration 193 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536932e+00	 sigma_n : 7.830148e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093
  Preparing critical source : iteration 194 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681610e+00	 sigma_n : 8.471247e-02
	 number of secondary particules: 1216
	 number of fission neutrons: 1216
  Preparing critical source : iteration 195 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.245066e+00	 sigma_n : 6.952223e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060
  Preparing critical source : iteration 196 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736792e+00	 sigma_n : 9.504051e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098
  Preparing critical source : iteration 197 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463570e+00	 sigma_n : 7.785526e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035
  Preparing critical source : iteration 198 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473430e+00	 sigma_n : 8.174927e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026
  Preparing critical source : iteration 199 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597466e+00	 sigma_n : 8.306835e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088
  Preparing critical source : iteration 200 out of 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493566e+00	 sigma_n : 8.614260e-02
	 number of secondary particules: 6505
	 number of fission neutrons: 1079
	 number of sampled neutrons for dynamic: 2713
	 number of sampled precursors for dynamic: 2713

           Dynamic normalization factor = 1.000000e+00


         Stats about population importance biasing:
           neutron weight  = 6.190848e-06   precursor weight = 8.028355e+01   ratio = 7.711228e-08
           biased neutron weight = 8.844069e+01
           neutron importance = 1.471123e-07


 Stat infos before Combing: Nn = 2713 ; Nc = 2713 ; w_n =  8.844069e+01 ; w_c = 8.028355e+01


 Stat infos after Combing: Nn = 524 ; Nc = 476 ; w_n =  5.240000e+02 ; w_c = 4.760000e+02


 simulation time (s) : 4


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.508855e+00	 sigma_n : 1.398942e-02
	 number of secondary particules: 35835
	 number of fission neutrons: 35438

 Stat infos before Combing: Nn = 810 ; Nc = 699 ; w_n =  7.420062e+02 ; w_c = 4.760000e+02


 Stat infos after Combing: Nn = 609 ; Nc = 391 ; w_n =  6.090000e+02 ; w_c = 3.910000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533561e+00	 sigma_n : 1.410296e-02
	 number of secondary particules: 37685
	 number of fission neutrons: 37291

 Stat infos before Combing: Nn = 726 ; Nc = 650 ; w_n =  6.639546e+02 ; w_c = 3.910000e+02


 Stat infos after Combing: Nn = 629 ; Nc = 371 ; w_n =  6.290000e+02 ; w_c = 3.710000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537630e+00	 sigma_n : 1.641929e-02
	 number of secondary particules: 28115
	 number of fission neutrons: 27792

 Stat infos before Combing: Nn = 367 ; Nc = 547 ; w_n =  3.347134e+02 ; w_c = 3.710000e+02


 Stat infos after Combing: Nn = 474 ; Nc = 526 ; w_n =  4.740000e+02 ; w_c = 5.260000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534131e+00	 sigma_n : 1.735812e-02
	 number of secondary particules: 24751
	 number of fission neutrons: 24447

 Stat infos before Combing: Nn = 404 ; Nc = 671 ; w_n =  3.670158e+02 ; w_c = 5.260000e+02


 Stat infos after Combing: Nn = 411 ; Nc = 589 ; w_n =  4.110000e+02 ; w_c = 5.890000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526902e+00	 sigma_n : 2.047371e-02
	 number of secondary particules: 17920
	 number of fission neutrons: 17625

 Stat infos before Combing: Nn = 311 ; Nc = 687 ; w_n =  2.862501e+02 ; w_c = 5.890000e+02


 Stat infos after Combing: Nn = 327 ; Nc = 673 ; w_n =  3.270000e+02 ; w_c = 6.730000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516759e+00	 sigma_n : 1.888588e-02
	 number of secondary particules: 20572
	 number of fission neutrons: 20233

 Stat infos before Combing: Nn = 531 ; Nc = 777 ; w_n =  4.809547e+02 ; w_c = 6.730000e+02


 Stat infos after Combing: Nn = 417 ; Nc = 583 ; w_n =  4.170000e+02 ; w_c = 5.830000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524807e+00	 sigma_n : 1.600188e-02
	 number of secondary particules: 28647
	 number of fission neutrons: 28278

 Stat infos before Combing: Nn = 609 ; Nc = 764 ; w_n =  5.579535e+02 ; w_c = 5.830000e+02


 Stat infos after Combing: Nn = 489 ; Nc = 511 ; w_n =  4.890000e+02 ; w_c = 5.110000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528247e+00	 sigma_n : 1.675962e-02
	 number of secondary particules: 25985
	 number of fission neutrons: 25646

 Stat infos before Combing: Nn = 474 ; Nc = 681 ; w_n =  4.319097e+02 ; w_c = 5.110000e+02


 Stat infos after Combing: Nn = 458 ; Nc = 542 ; w_n =  4.580000e+02 ; w_c = 5.420000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535191e+00	 sigma_n : 1.744822e-02
	 number of secondary particules: 24119
	 number of fission neutrons: 23805

 Stat infos before Combing: Nn = 433 ; Nc = 681 ; w_n =  3.961586e+02 ; w_c = 5.420000e+02


 Stat infos after Combing: Nn = 423 ; Nc = 578 ; w_n =  4.230000e+02 ; w_c = 5.780000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539774e+00	 sigma_n : 1.699477e-02
	 number of secondary particules: 25701
	 number of fission neutrons: 25347

 Stat infos before Combing: Nn = 429 ; Nc = 730 ; w_n =  3.877693e+02 ; w_c = 5.780000e+02


 Stat infos after Combing: Nn = 402 ; Nc = 598 ; w_n =  4.020000e+02 ; w_c = 5.980000e+02


 batch number : 2

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562558e+00	 sigma_n : 8.701756e-02
	 number of secondary particules: 6617
	 number of fission neutrons: 1087
	 number of sampled neutrons for dynamic: 2765
	 number of sampled precursors for dynamic: 2765

           Dynamic normalization factor = 8.028356e-02


         Stats about population importance biasing:
           neutron weight  = 6.142494e-06   precursor weight = 8.299918e+01   ratio = 7.400668e-08
           biased neutron weight = 8.774991e+01
           neutron importance = 1.440067e-07


 Stat infos before Combing: Nn = 2765 ; Nc = 2765 ; w_n =  8.774991e+01 ; w_c = 8.299918e+01


 Stat infos after Combing: Nn = 514 ; Nc = 487 ; w_n =  5.140000e+02 ; w_c = 4.870000e+02


 simulation time (s) : 9


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490758e+00	 sigma_n : 1.441268e-02
	 number of secondary particules: 35140
	 number of fission neutrons: 34760

 Stat infos before Combing: Nn = 519 ; Nc = 704 ; w_n =  4.766509e+02 ; w_c = 4.870000e+02


 Stat infos after Combing: Nn = 494 ; Nc = 506 ; w_n =  4.940000e+02 ; w_c = 5.060000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546668e+00	 sigma_n : 1.574554e-02
	 number of secondary particules: 30892
	 number of fission neutrons: 30498

 Stat infos before Combing: Nn = 791 ; Nc = 736 ; w_n =  7.225426e+02 ; w_c = 5.060000e+02


 Stat infos after Combing: Nn = 588 ; Nc = 412 ; w_n =  5.880000e+02 ; w_c = 4.120000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542699e+00	 sigma_n : 1.549497e-02
	 number of secondary particules: 31477
	 number of fission neutrons: 31159

 Stat infos before Combing: Nn = 535 ; Nc = 603 ; w_n =  4.876408e+02 ; w_c = 4.120000e+02


 Stat infos after Combing: Nn = 542 ; Nc = 458 ; w_n =  5.420000e+02 ; w_c = 4.580000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525879e+00	 sigma_n : 1.545865e-02
	 number of secondary particules: 31537
	 number of fission neutrons: 31198

 Stat infos before Combing: Nn = 575 ; Nc = 638 ; w_n =  5.271687e+02 ; w_c = 4.580000e+02


 Stat infos after Combing: Nn = 535 ; Nc = 465 ; w_n =  5.350000e+02 ; w_c = 4.650000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552183e+00	 sigma_n : 1.947081e-02
	 number of secondary particules: 20049
	 number of fission neutrons: 19767

 Stat infos before Combing: Nn = 478 ; Nc = 592 ; w_n =  4.376872e+02 ; w_c = 4.650000e+02


 Stat infos after Combing: Nn = 485 ; Nc = 515 ; w_n =  4.850000e+02 ; w_c = 5.150000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.501976e+00	 sigma_n : 1.682041e-02
	 number of secondary particules: 25468
	 number of fission neutrons: 25140

 Stat infos before Combing: Nn = 377 ; Nc = 662 ; w_n =  3.441998e+02 ; w_c = 5.150000e+02


 Stat infos after Combing: Nn = 400 ; Nc = 600 ; w_n =  4.000000e+02 ; w_c = 6.000000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531153e+00	 sigma_n : 1.745921e-02
	 number of secondary particules: 24872
	 number of fission neutrons: 24503

 Stat infos before Combing: Nn = 474 ; Nc = 770 ; w_n =  4.310375e+02 ; w_c = 6.000000e+02


 Stat infos after Combing: Nn = 418 ; Nc = 582 ; w_n =  4.180000e+02 ; w_c = 5.820000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523028e+00	 sigma_n : 1.856512e-02
	 number of secondary particules: 21576
	 number of fission neutrons: 21272

 Stat infos before Combing: Nn = 391 ; Nc = 711 ; w_n =  3.585146e+02 ; w_c = 5.820000e+02


 Stat infos after Combing: Nn = 381 ; Nc = 619 ; w_n =  3.810000e+02 ; w_c = 6.190000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539176e+00	 sigma_n : 2.167130e-02
	 number of secondary particules: 16080
	 number of fission neutrons: 15772

 Stat infos before Combing: Nn = 298 ; Nc = 718 ; w_n =  2.736449e+02 ; w_c = 6.190000e+02


 Stat infos after Combing: Nn = 307 ; Nc = 693 ; w_n =  3.070000e+02 ; w_c = 6.930000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525815e+00	 sigma_n : 2.206176e-02
	 number of secondary particules: 15154
	 number of fission neutrons: 14812

 Stat infos before Combing: Nn = 318 ; Nc = 795 ; w_n =  2.885678e+02 ; w_c = 6.930000e+02


 Stat infos after Combing: Nn = 294 ; Nc = 706 ; w_n =  2.940000e+02 ; w_c = 7.060000e+02


 batch number : 3

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524379e+00	 sigma_n : 8.358360e-02
	 number of secondary particules: 6560
	 number of fission neutrons: 1072
	 number of sampled neutrons for dynamic: 2744
	 number of sampled precursors for dynamic: 2744

           Dynamic normalization factor = 8.299919e-02


         Stats about population importance biasing:
           neutron weight  = 6.198433e-06   precursor weight = 8.173813e+01   ratio = 7.583283e-08
           biased neutron weight = 8.854905e+01
           neutron importance = 1.458328e-07


 Stat infos before Combing: Nn = 2744 ; Nc = 2744 ; w_n =  8.854905e+01 ; w_c = 8.173813e+01


 Stat infos after Combing: Nn = 520 ; Nc = 480 ; w_n =  5.200000e+02 ; w_c = 4.800000e+02


 simulation time (s) : 13


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473573e+00	 sigma_n : 1.377536e-02
	 number of secondary particules: 36730
	 number of fission neutrons: 36376

 Stat infos before Combing: Nn = 996 ; Nc = 684 ; w_n =  9.084167e+02 ; w_c = 4.800000e+02


 Stat infos after Combing: Nn = 654 ; Nc = 346 ; w_n =  6.540000e+02 ; w_c = 3.460000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537781e+00	 sigma_n : 1.472852e-02
	 number of secondary particules: 34578
	 number of fission neutrons: 34252

 Stat infos before Combing: Nn = 568 ; Nc = 547 ; w_n =  5.164541e+02 ; w_c = 3.460000e+02


 Stat infos after Combing: Nn = 599 ; Nc = 402 ; w_n =  5.990000e+02 ; w_c = 4.020000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559472e+00	 sigma_n : 1.779517e-02
	 number of secondary particules: 24156
	 number of fission neutrons: 23866

 Stat infos before Combing: Nn = 267 ; Nc = 557 ; w_n =  2.451036e+02 ; w_c = 4.020000e+02


 Stat infos after Combing: Nn = 379 ; Nc = 621 ; w_n =  3.790000e+02 ; w_c = 6.210000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543787e+00	 sigma_n : 2.452984e-02
	 number of secondary particules: 12279
	 number of fission neutrons: 12012

 Stat infos before Combing: Nn = 266 ; Nc = 684 ; w_n =  2.406804e+02 ; w_c = 6.210000e+02


 Stat infos after Combing: Nn = 279 ; Nc = 720 ; w_n =  2.790000e+02 ; w_c = 7.200000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536663e+00	 sigma_n : 2.055234e-02
	 number of secondary particules: 17536
	 number of fission neutrons: 17179

 Stat infos before Combing: Nn = 346 ; Nc = 833 ; w_n =  3.132693e+02 ; w_c = 7.200000e+02


 Stat infos after Combing: Nn = 303 ; Nc = 697 ; w_n =  3.030000e+02 ; w_c = 6.970000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528792e+00	 sigma_n : 1.937830e-02
	 number of secondary particules: 19871
	 number of fission neutrons: 19505

 Stat infos before Combing: Nn = 495 ; Nc = 831 ; w_n =  4.533648e+02 ; w_c = 6.970000e+02


 Stat infos after Combing: Nn = 394 ; Nc = 606 ; w_n =  3.940000e+02 ; w_c = 6.060000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545237e+00	 sigma_n : 2.014689e-02
	 number of secondary particules: 18562
	 number of fission neutrons: 18234

 Stat infos before Combing: Nn = 473 ; Nc = 728 ; w_n =  4.319751e+02 ; w_c = 6.060000e+02


 Stat infos after Combing: Nn = 416 ; Nc = 584 ; w_n =  4.160000e+02 ; w_c = 5.840000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516145e+00	 sigma_n : 1.590846e-02
	 number of secondary particules: 28924
	 number of fission neutrons: 28545

 Stat infos before Combing: Nn = 470 ; Nc = 750 ; w_n =  4.291401e+02 ; w_c = 5.840000e+02


 Stat infos after Combing: Nn = 424 ; Nc = 576 ; w_n =  4.240000e+02 ; w_c = 5.760000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516955e+00	 sigma_n : 1.424548e-02
	 number of secondary particules: 35441
	 number of fission neutrons: 35037

 Stat infos before Combing: Nn = 718 ; Nc = 788 ; w_n =  6.574612e+02 ; w_c = 5.760000e+02


 Stat infos after Combing: Nn = 533 ; Nc = 467 ; w_n =  5.330000e+02 ; w_c = 4.670000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535046e+00	 sigma_n : 1.650584e-02
	 number of secondary particules: 27104
	 number of fission neutrons: 26728

 Stat infos before Combing: Nn = 451 ; Nc = 654 ; w_n =  4.117817e+02 ; w_c = 4.670000e+02


 Stat infos after Combing: Nn = 468 ; Nc = 531 ; w_n =  4.680000e+02 ; w_c = 5.310000e+02


 batch number : 4

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527052e+00	 sigma_n : 7.666024e-02
	 number of secondary particules: 6545
	 number of fission neutrons: 1127
	 number of sampled neutrons for dynamic: 2709
	 number of sampled precursors for dynamic: 2709

           Dynamic normalization factor = 8.173813e-02


         Stats about population importance biasing:
           neutron weight  = 6.100371e-06   precursor weight = 8.102430e+01   ratio = 7.529063e-08
           biased neutron weight = 8.714815e+01
           neutron importance = 1.452906e-07


 Stat infos before Combing: Nn = 2709 ; Nc = 2709 ; w_n =  8.714815e+01 ; w_c = 8.102430e+01


 Stat infos after Combing: Nn = 518 ; Nc = 482 ; w_n =  5.180000e+02 ; w_c = 4.820000e+02


 simulation time (s) : 17


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.476417e+00	 sigma_n : 1.811847e-02
	 number of secondary particules: 22297
	 number of fission neutrons: 22009

 Stat infos before Combing: Nn = 190 ; Nc = 611 ; w_n =  1.727257e+02 ; w_c = 4.820000e+02


 Stat infos after Combing: Nn = 264 ; Nc = 736 ; w_n =  2.640000e+02 ; w_c = 7.360000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490183e+00	 sigma_n : 1.744947e-02
	 number of secondary particules: 23202
	 number of fission neutrons: 22800

 Stat infos before Combing: Nn = 1030 ; Nc = 876 ; w_n =  9.414286e+02 ; w_c = 7.360000e+02


 Stat infos after Combing: Nn = 561 ; Nc = 438 ; w_n =  5.610000e+02 ; w_c = 4.380000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525655e+00	 sigma_n : 1.482709e-02
	 number of secondary particules: 34095
	 number of fission neutrons: 33703

 Stat infos before Combing: Nn = 495 ; Nc = 676 ; w_n =  4.542843e+02 ; w_c = 4.380000e+02


 Stat infos after Combing: Nn = 510 ; Nc = 491 ; w_n =  5.100000e+02 ; w_c = 4.910000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537117e+00	 sigma_n : 1.410166e-02
	 number of secondary particules: 37872
	 number of fission neutrons: 37466

 Stat infos before Combing: Nn = 926 ; Nc = 710 ; w_n =  8.430509e+02 ; w_c = 4.910000e+02


 Stat infos after Combing: Nn = 632 ; Nc = 368 ; w_n =  6.320000e+02 ; w_c = 3.680000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546476e+00	 sigma_n : 1.466210e-02
	 number of secondary particules: 34285
	 number of fission neutrons: 33968

 Stat infos before Combing: Nn = 682 ; Nc = 568 ; w_n =  6.195820e+02 ; w_c = 3.680000e+02


 Stat infos after Combing: Nn = 627 ; Nc = 372 ; w_n =  6.270000e+02 ; w_c = 3.720000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527706e+00	 sigma_n : 1.181822e-02
	 number of secondary particules: 53636
	 number of fission neutrons: 53180

 Stat infos before Combing: Nn = 974 ; Nc = 694 ; w_n =  8.868613e+02 ; w_c = 3.720000e+02


 Stat infos after Combing: Nn = 704 ; Nc = 295 ; w_n =  7.040000e+02 ; w_c = 2.950000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547133e+00	 sigma_n : 1.291649e-02
	 number of secondary particules: 44768
	 number of fission neutrons: 44417

 Stat infos before Combing: Nn = 832 ; Nc = 544 ; w_n =  7.574631e+02 ; w_c = 2.950000e+02


 Stat infos after Combing: Nn = 720 ; Nc = 281 ; w_n =  7.200000e+02 ; w_c = 2.810000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542889e+00	 sigma_n : 1.468404e-02
	 number of secondary particules: 34861
	 number of fission neutrons: 34519

 Stat infos before Combing: Nn = 654 ; Nc = 527 ; w_n =  5.985260e+02 ; w_c = 2.810000e+02


 Stat infos after Combing: Nn = 680 ; Nc = 319 ; w_n =  6.800000e+02 ; w_c = 3.190000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551758e+00	 sigma_n : 1.550429e-02
	 number of secondary particules: 32151
	 number of fission neutrons: 31823

 Stat infos before Combing: Nn = 390 ; Nc = 527 ; w_n =  3.565091e+02 ; w_c = 3.190000e+02


 Stat infos after Combing: Nn = 528 ; Nc = 472 ; w_n =  5.280000e+02 ; w_c = 4.720000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546213e+00	 sigma_n : 1.714926e-02
	 number of secondary particules: 25134
	 number of fission neutrons: 24838

 Stat infos before Combing: Nn = 493 ; Nc = 611 ; w_n =  4.510378e+02 ; w_c = 4.720000e+02


 Stat infos after Combing: Nn = 489 ; Nc = 512 ; w_n =  4.890000e+02 ; w_c = 5.120000e+02


 batch number : 5

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511091e+00	 sigma_n : 8.503277e-02
	 number of secondary particules: 6776
	 number of fission neutrons: 1116
	 number of sampled neutrons for dynamic: 2830
	 number of sampled precursors for dynamic: 2830

           Dynamic normalization factor = 8.102431e-02


         Stats about population importance biasing:
           neutron weight  = 6.344910e-06   precursor weight = 8.327232e+01   ratio = 7.619470e-08
           biased neutron weight = 9.064157e+01
           neutron importance = 1.461947e-07


 Stat infos before Combing: Nn = 2830 ; Nc = 2830 ; w_n =  9.064157e+01 ; w_c = 8.327232e+01


 Stat infos after Combing: Nn = 521 ; Nc = 479 ; w_n =  5.210000e+02 ; w_c = 4.790000e+02


 simulation time (s) : 23


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507125e+00	 sigma_n : 1.582857e-02
	 number of secondary particules: 28426
	 number of fission neutrons: 28075

 Stat infos before Combing: Nn = 598 ; Nc = 656 ; w_n =  5.443274e+02 ; w_c = 4.790000e+02


 Stat infos after Combing: Nn = 532 ; Nc = 469 ; w_n =  5.320000e+02 ; w_c = 4.690000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512769e+00	 sigma_n : 1.675101e-02
	 number of secondary particules: 25611
	 number of fission neutrons: 25321

 Stat infos before Combing: Nn = 617 ; Nc = 612 ; w_n =  5.649734e+02 ; w_c = 4.690000e+02


 Stat infos after Combing: Nn = 546 ; Nc = 454 ; w_n =  5.460000e+02 ; w_c = 4.540000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540307e+00	 sigma_n : 1.959702e-02
	 number of secondary particules: 19154
	 number of fission neutrons: 18890

 Stat infos before Combing: Nn = 274 ; Nc = 567 ; w_n =  2.517764e+02 ; w_c = 4.540000e+02


 Stat infos after Combing: Nn = 357 ; Nc = 643 ; w_n =  3.570000e+02 ; w_c = 6.430000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502462e+00	 sigma_n : 1.533604e-02
	 number of secondary particules: 30301
	 number of fission neutrons: 29864

 Stat infos before Combing: Nn = 857 ; Nc = 839 ; w_n =  7.816873e+02 ; w_c = 6.430000e+02


 Stat infos after Combing: Nn = 548 ; Nc = 451 ; w_n =  5.480000e+02 ; w_c = 4.510000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555362e+00	 sigma_n : 1.803224e-02
	 number of secondary particules: 23186
	 number of fission neutrons: 22881

 Stat infos before Combing: Nn = 322 ; Nc = 604 ; w_n =  2.922465e+02 ; w_c = 4.510000e+02


 Stat infos after Combing: Nn = 394 ; Nc = 607 ; w_n =  3.940000e+02 ; w_c = 6.070000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.506784e+00	 sigma_n : 1.527467e-02
	 number of secondary particules: 30599
	 number of fission neutrons: 30193

 Stat infos before Combing: Nn = 658 ; Nc = 790 ; w_n =  6.031254e+02 ; w_c = 6.070000e+02


 Stat infos after Combing: Nn = 498 ; Nc = 501 ; w_n =  4.980000e+02 ; w_c = 5.010000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538716e+00	 sigma_n : 1.564910e-02
	 number of secondary particules: 30478
	 number of fission neutrons: 30145

 Stat infos before Combing: Nn = 695 ; Nc = 676 ; w_n =  6.331934e+02 ; w_c = 5.010000e+02


 Stat infos after Combing: Nn = 558 ; Nc = 442 ; w_n =  5.580000e+02 ; w_c = 4.420000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522272e+00	 sigma_n : 1.820957e-02
	 number of secondary particules: 22563
	 number of fission neutrons: 22266

 Stat infos before Combing: Nn = 281 ; Nc = 575 ; w_n =  2.560903e+02 ; w_c = 4.420000e+02


 Stat infos after Combing: Nn = 367 ; Nc = 633 ; w_n =  3.670000e+02 ; w_c = 6.330000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498255e+00	 sigma_n : 1.799882e-02
	 number of secondary particules: 21833
	 number of fission neutrons: 21467

 Stat infos before Combing: Nn = 520 ; Nc = 768 ; w_n =  4.720331e+02 ; w_c = 6.330000e+02


 Stat infos after Combing: Nn = 427 ; Nc = 573 ; w_n =  4.270000e+02 ; w_c = 5.730000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536440e+00	 sigma_n : 1.770862e-02
	 number of secondary particules: 23988
	 number of fission neutrons: 23631

 Stat infos before Combing: Nn = 561 ; Nc = 715 ; w_n =  5.105841e+02 ; w_c = 5.730000e+02


 Stat infos after Combing: Nn = 471 ; Nc = 529 ; w_n =  4.710000e+02 ; w_c = 5.290000e+02


 batch number : 6

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.390681e+00	 sigma_n : 7.481897e-02
	 number of secondary particules: 6374
	 number of fission neutrons: 1038
	 number of sampled neutrons for dynamic: 2668
	 number of sampled precursors for dynamic: 2668

           Dynamic normalization factor = 8.327233e-02


         Stats about population importance biasing:
           neutron weight  = 5.952104e-06   precursor weight = 7.886317e+01   ratio = 7.547381e-08
           biased neutron weight = 8.503005e+01
           neutron importance = 1.454738e-07


 Stat infos before Combing: Nn = 2668 ; Nc = 2668 ; w_n =  8.503005e+01 ; w_c = 7.886317e+01


 Stat infos after Combing: Nn = 518 ; Nc = 481 ; w_n =  5.180000e+02 ; w_c = 4.810000e+02


 simulation time (s) : 28


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.479349e+00	 sigma_n : 1.517202e-02
	 number of secondary particules: 30078
	 number of fission neutrons: 29736

 Stat infos before Combing: Nn = 750 ; Nc = 667 ; w_n =  6.834363e+02 ; w_c = 4.810000e+02


 Stat infos after Combing: Nn = 587 ; Nc = 413 ; w_n =  5.870000e+02 ; w_c = 4.130000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570400e+00	 sigma_n : 1.886544e-02
	 number of secondary particules: 21618
	 number of fission neutrons: 21358

 Stat infos before Combing: Nn = 271 ; Nc = 537 ; w_n =  2.475800e+02 ; w_c = 4.130000e+02


 Stat infos after Combing: Nn = 375 ; Nc = 625 ; w_n =  3.750000e+02 ; w_c = 6.250000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504417e+00	 sigma_n : 2.257250e-02
	 number of secondary particules: 13751
	 number of fission neutrons: 13458

 Stat infos before Combing: Nn = 121 ; Nc = 713 ; w_n =  1.105879e+02 ; w_c = 6.250000e+02


 Stat infos after Combing: Nn = 151 ; Nc = 850 ; w_n =  1.510000e+02 ; w_c = 8.500000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.481841e+00	 sigma_n : 2.614551e-02
	 number of secondary particules: 10022
	 number of fission neutrons: 9660

 Stat infos before Combing: Nn = 365 ; Nc = 918 ; w_n =  3.341739e+02 ; w_c = 8.500000e+02


 Stat infos after Combing: Nn = 282 ; Nc = 718 ; w_n =  2.820000e+02 ; w_c = 7.180000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510276e+00	 sigma_n : 1.668475e-02
	 number of secondary particules: 25355
	 number of fission neutrons: 24968

 Stat infos before Combing: Nn = 380 ; Nc = 859 ; w_n =  3.461909e+02 ; w_c = 7.180000e+02


 Stat infos after Combing: Nn = 326 ; Nc = 675 ; w_n =  3.260000e+02 ; w_c = 6.750000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559980e+00	 sigma_n : 1.839426e-02
	 number of secondary particules: 22207
	 number of fission neutrons: 21837

 Stat infos before Combing: Nn = 351 ; Nc = 809 ; w_n =  3.226208e+02 ; w_c = 6.750000e+02


 Stat infos after Combing: Nn = 323 ; Nc = 677 ; w_n =  3.230000e+02 ; w_c = 6.770000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524549e+00	 sigma_n : 1.678751e-02
	 number of secondary particules: 26029
	 number of fission neutrons: 25653

 Stat infos before Combing: Nn = 689 ; Nc = 816 ; w_n =  6.270766e+02 ; w_c = 6.770000e+02


 Stat infos after Combing: Nn = 481 ; Nc = 519 ; w_n =  4.810000e+02 ; w_c = 5.190000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538577e+00	 sigma_n : 1.766229e-02
	 number of secondary particules: 23594
	 number of fission neutrons: 23275

 Stat infos before Combing: Nn = 471 ; Nc = 655 ; w_n =  4.275403e+02 ; w_c = 5.190000e+02


 Stat infos after Combing: Nn = 452 ; Nc = 548 ; w_n =  4.520000e+02 ; w_c = 5.480000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513188e+00	 sigma_n : 1.548153e-02
	 number of secondary particules: 30952
	 number of fission neutrons: 30560

 Stat infos before Combing: Nn = 698 ; Nc = 749 ; w_n =  6.388364e+02 ; w_c = 5.480000e+02


 Stat infos after Combing: Nn = 539 ; Nc = 462 ; w_n =  5.390000e+02 ; w_c = 4.620000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531218e+00	 sigma_n : 1.455733e-02
	 number of secondary particules: 34148
	 number of fission neutrons: 33793

 Stat infos before Combing: Nn = 912 ; Nc = 666 ; w_n =  8.302865e+02 ; w_c = 4.620000e+02


 Stat infos after Combing: Nn = 643 ; Nc = 358 ; w_n =  6.430000e+02 ; w_c = 3.580000e+02


 batch number : 7

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544316e+00	 sigma_n : 8.249534e-02
	 number of secondary particules: 6363
	 number of fission neutrons: 1081
	 number of sampled neutrons for dynamic: 2641
	 number of sampled precursors for dynamic: 2641

           Dynamic normalization factor = 7.886317e-02


         Stats about population importance biasing:
           neutron weight  = 6.122397e-06   precursor weight = 8.010611e+01   ratio = 7.642859e-08
           biased neutron weight = 8.746281e+01
           neutron importance = 1.464286e-07


 Stat infos before Combing: Nn = 2641 ; Nc = 2641 ; w_n =  8.746281e+01 ; w_c = 8.010611e+01


 Stat infos after Combing: Nn = 522 ; Nc = 478 ; w_n =  5.220000e+02 ; w_c = 4.780000e+02


 simulation time (s) : 33


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463594e+00	 sigma_n : 1.741382e-02
	 number of secondary particules: 23110
	 number of fission neutrons: 22809

 Stat infos before Combing: Nn = 357 ; Nc = 611 ; w_n =  3.237342e+02 ; w_c = 4.780000e+02


 Stat infos after Combing: Nn = 404 ; Nc = 597 ; w_n =  4.040000e+02 ; w_c = 5.970000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520721e+00	 sigma_n : 1.712935e-02
	 number of secondary particules: 25051
	 number of fission neutrons: 24706

 Stat infos before Combing: Nn = 695 ; Nc = 739 ; w_n =  6.309886e+02 ; w_c = 5.970000e+02


 Stat infos after Combing: Nn = 514 ; Nc = 486 ; w_n =  5.140000e+02 ; w_c = 4.860000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514838e+00	 sigma_n : 1.452843e-02
	 number of secondary particules: 34571
	 number of fission neutrons: 34201

 Stat infos before Combing: Nn = 697 ; Nc = 694 ; w_n =  6.348509e+02 ; w_c = 4.860000e+02


 Stat infos after Combing: Nn = 566 ; Nc = 434 ; w_n =  5.660000e+02 ; w_c = 4.340000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520813e+00	 sigma_n : 1.450782e-02
	 number of secondary particules: 35003
	 number of fission neutrons: 34603

 Stat infos before Combing: Nn = 840 ; Nc = 664 ; w_n =  7.639180e+02 ; w_c = 4.340000e+02


 Stat infos after Combing: Nn = 638 ; Nc = 362 ; w_n =  6.380000e+02 ; w_c = 3.620000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536666e+00	 sigma_n : 1.589563e-02
	 number of secondary particules: 29667
	 number of fission neutrons: 29360

 Stat infos before Combing: Nn = 562 ; Nc = 557 ; w_n =  5.097013e+02 ; w_c = 3.620000e+02


 Stat infos after Combing: Nn = 584 ; Nc = 415 ; w_n =  5.840000e+02 ; w_c = 4.150000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552374e+00	 sigma_n : 1.644334e-02
	 number of secondary particules: 28158
	 number of fission neutrons: 27831

 Stat infos before Combing: Nn = 432 ; Nc = 593 ; w_n =  3.947595e+02 ; w_c = 4.150000e+02


 Stat infos after Combing: Nn = 487 ; Nc = 512 ; w_n =  4.870000e+02 ; w_c = 5.120000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513191e+00	 sigma_n : 1.623076e-02
	 number of secondary particules: 26996
	 number of fission neutrons: 26678

 Stat infos before Combing: Nn = 653 ; Nc = 666 ; w_n =  5.964600e+02 ; w_c = 5.120000e+02


 Stat infos after Combing: Nn = 539 ; Nc = 462 ; w_n =  5.390000e+02 ; w_c = 4.620000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542182e+00	 sigma_n : 1.733204e-02
	 number of secondary particules: 24553
	 number of fission neutrons: 24205

 Stat infos before Combing: Nn = 257 ; Nc = 638 ; w_n =  2.366670e+02 ; w_c = 4.620000e+02


 Stat infos after Combing: Nn = 339 ; Nc = 661 ; w_n =  3.390000e+02 ; w_c = 6.610000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516928e+00	 sigma_n : 1.548762e-02
	 number of secondary particules: 31440
	 number of fission neutrons: 31044

 Stat infos before Combing: Nn = 1008 ; Nc = 836 ; w_n =  9.172529e+02 ; w_c = 6.610000e+02


 Stat infos after Combing: Nn = 581 ; Nc = 419 ; w_n =  5.810000e+02 ; w_c = 4.190000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531035e+00	 sigma_n : 1.513133e-02
	 number of secondary particules: 32615
	 number of fission neutrons: 32275

 Stat infos before Combing: Nn = 540 ; Nc = 604 ; w_n =  4.950521e+02 ; w_c = 4.190000e+02


 Stat infos after Combing: Nn = 542 ; Nc = 459 ; w_n =  5.420000e+02 ; w_c = 4.590000e+02


 batch number : 8

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532840e+00	 sigma_n : 8.418001e-02
	 number of secondary particules: 6546
	 number of fission neutrons: 1070
	 number of sampled neutrons for dynamic: 2738
	 number of sampled precursors for dynamic: 2738

           Dynamic normalization factor = 8.010611e-02


         Stats about population importance biasing:
           neutron weight  = 6.271400e-06   precursor weight = 8.150919e+01   ratio = 7.694102e-08
           biased neutron weight = 8.959143e+01
           neutron importance = 1.469410e-07


 Stat infos before Combing: Nn = 2738 ; Nc = 2738 ; w_n =  8.959143e+01 ; w_c = 8.150919e+01


 Stat infos after Combing: Nn = 524 ; Nc = 477 ; w_n =  5.240000e+02 ; w_c = 4.770000e+02


 simulation time (s) : 38


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491987e+00	 sigma_n : 1.632848e-02
	 number of secondary particules: 26614
	 number of fission neutrons: 26267

 Stat infos before Combing: Nn = 584 ; Nc = 659 ; w_n =  5.340745e+02 ; w_c = 4.770000e+02


 Stat infos after Combing: Nn = 528 ; Nc = 471 ; w_n =  5.280000e+02 ; w_c = 4.710000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530184e+00	 sigma_n : 1.403265e-02
	 number of secondary particules: 38138
	 number of fission neutrons: 37731

 Stat infos before Combing: Nn = 659 ; Nc = 722 ; w_n =  5.996120e+02 ; w_c = 4.710000e+02


 Stat infos after Combing: Nn = 560 ; Nc = 440 ; w_n =  5.600000e+02 ; w_c = 4.400000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522553e+00	 sigma_n : 1.405139e-02
	 number of secondary particules: 37646
	 number of fission neutrons: 37280

 Stat infos before Combing: Nn = 869 ; Nc = 669 ; w_n =  7.871478e+02 ; w_c = 4.400000e+02


 Stat infos after Combing: Nn = 641 ; Nc = 358 ; w_n =  6.410000e+02 ; w_c = 3.580000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526825e+00	 sigma_n : 1.214956e-02
	 number of secondary particules: 50240
	 number of fission neutrons: 49817

 Stat infos before Combing: Nn = 1317 ; Nc = 651 ; w_n =  1.204571e+03 ; w_c = 3.580000e+02


 Stat infos after Combing: Nn = 771 ; Nc = 229 ; w_n =  7.710000e+02 ; w_c = 2.290000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546222e+00	 sigma_n : 1.458763e-02
	 number of secondary particules: 35933
	 number of fission neutrons: 35626

 Stat infos before Combing: Nn = 436 ; Nc = 457 ; w_n =  3.985480e+02 ; w_c = 2.290000e+02


 Stat infos after Combing: Nn = 635 ; Nc = 365 ; w_n =  6.350000e+02 ; w_c = 3.650000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552346e+00	 sigma_n : 1.762646e-02
	 number of secondary particules: 24421
	 number of fission neutrons: 24142

 Stat infos before Combing: Nn = 444 ; Nc = 529 ; w_n =  4.027016e+02 ; w_c = 3.650000e+02


 Stat infos after Combing: Nn = 525 ; Nc = 476 ; w_n =  5.250000e+02 ; w_c = 4.760000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528875e+00	 sigma_n : 1.447374e-02
	 number of secondary particules: 35223
	 number of fission neutrons: 34847

 Stat infos before Combing: Nn = 722 ; Nc = 692 ; w_n =  6.591864e+02 ; w_c = 4.760000e+02


 Stat infos after Combing: Nn = 580 ; Nc = 419 ; w_n =  5.800000e+02 ; w_c = 4.190000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538268e+00	 sigma_n : 1.651161e-02
	 number of secondary particules: 26957
	 number of fission neutrons: 26663

 Stat infos before Combing: Nn = 514 ; Nc = 557 ; w_n =  4.688130e+02 ; w_c = 4.190000e+02


 Stat infos after Combing: Nn = 528 ; Nc = 472 ; w_n =  5.280000e+02 ; w_c = 4.720000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528220e+00	 sigma_n : 1.513033e-02
	 number of secondary particules: 32269
	 number of fission neutrons: 31883

 Stat infos before Combing: Nn = 783 ; Nc = 703 ; w_n =  7.125630e+02 ; w_c = 4.720000e+02


 Stat infos after Combing: Nn = 601 ; Nc = 399 ; w_n =  6.010000e+02 ; w_c = 3.990000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520887e+00	 sigma_n : 1.477237e-02
	 number of secondary particules: 33493
	 number of fission neutrons: 33148

 Stat infos before Combing: Nn = 938 ; Nc = 597 ; w_n =  8.540664e+02 ; w_c = 3.990000e+02


 Stat infos after Combing: Nn = 682 ; Nc = 319 ; w_n =  6.820000e+02 ; w_c = 3.190000e+02


 batch number : 9

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.377570e+00	 sigma_n : 8.028880e-02
	 number of secondary particules: 6059
	 number of fission neutrons: 971
	 number of sampled neutrons for dynamic: 2544
	 number of sampled precursors for dynamic: 2544

           Dynamic normalization factor = 8.150920e-02


         Stats about population importance biasing:
           neutron weight  = 5.726339e-06   precursor weight = 7.646301e+01   ratio = 7.489032e-08
           biased neutron weight = 8.180485e+01
           neutron importance = 1.448903e-07


 Stat infos before Combing: Nn = 2544 ; Nc = 2544 ; w_n =  8.180485e+01 ; w_c = 7.646301e+01


 Stat infos after Combing: Nn = 517 ; Nc = 483 ; w_n =  5.170000e+02 ; w_c = 4.830000e+02


 simulation time (s) : 45


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.433405e+00	 sigma_n : 1.834252e-02
	 number of secondary particules: 20023
	 number of fission neutrons: 19702

 Stat infos before Combing: Nn = 509 ; Nc = 631 ; w_n =  4.634937e+02 ; w_c = 4.830000e+02


 Stat infos after Combing: Nn = 490 ; Nc = 510 ; w_n =  4.900000e+02 ; w_c = 5.100000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546238e+00	 sigma_n : 1.744905e-02
	 number of secondary particules: 24595
	 number of fission neutrons: 24272

 Stat infos before Combing: Nn = 523 ; Nc = 659 ; w_n =  4.771146e+02 ; w_c = 5.100000e+02


 Stat infos after Combing: Nn = 484 ; Nc = 517 ; w_n =  4.840000e+02 ; w_c = 5.170000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531589e+00	 sigma_n : 1.550089e-02
	 number of secondary particules: 31106
	 number of fission neutrons: 30757

 Stat infos before Combing: Nn = 601 ; Nc = 688 ; w_n =  5.496805e+02 ; w_c = 5.170000e+02


 Stat infos after Combing: Nn = 515 ; Nc = 485 ; w_n =  5.150000e+02 ; w_c = 4.850000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550226e+00	 sigma_n : 1.650050e-02
	 number of secondary particules: 28583
	 number of fission neutrons: 28228

 Stat infos before Combing: Nn = 538 ; Nc = 664 ; w_n =  4.906586e+02 ; w_c = 4.850000e+02


 Stat infos after Combing: Nn = 503 ; Nc = 497 ; w_n =  5.030000e+02 ; w_c = 4.970000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570213e+00	 sigma_n : 1.788852e-02
	 number of secondary particules: 24901
	 number of fission neutrons: 24599

 Stat infos before Combing: Nn = 454 ; Nc = 635 ; w_n =  4.125855e+02 ; w_c = 4.970000e+02


 Stat infos after Combing: Nn = 454 ; Nc = 546 ; w_n =  4.540000e+02 ; w_c = 5.460000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555923e+00	 sigma_n : 1.690738e-02
	 number of secondary particules: 27240
	 number of fission neutrons: 26872

 Stat infos before Combing: Nn = 475 ; Nc = 720 ; w_n =  4.367860e+02 ; w_c = 5.460000e+02


 Stat infos after Combing: Nn = 444 ; Nc = 556 ; w_n =  4.440000e+02 ; w_c = 5.560000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551555e+00	 sigma_n : 1.552440e-02
	 number of secondary particules: 31482
	 number of fission neutrons: 31088

 Stat infos before Combing: Nn = 643 ; Nc = 739 ; w_n =  5.880378e+02 ; w_c = 5.560000e+02


 Stat infos after Combing: Nn = 514 ; Nc = 486 ; w_n =  5.140000e+02 ; w_c = 4.860000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527340e+00	 sigma_n : 1.537982e-02
	 number of secondary particules: 31028
	 number of fission neutrons: 30691

 Stat infos before Combing: Nn = 661 ; Nc = 682 ; w_n =  5.990193e+02 ; w_c = 4.860000e+02


 Stat infos after Combing: Nn = 552 ; Nc = 447 ; w_n =  5.520000e+02 ; w_c = 4.470000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534193e+00	 sigma_n : 1.821815e-02
	 number of secondary particules: 22234
	 number of fission neutrons: 21952

 Stat infos before Combing: Nn = 467 ; Nc = 582 ; w_n =  4.261551e+02 ; w_c = 4.470000e+02


 Stat infos after Combing: Nn = 488 ; Nc = 512 ; w_n =  4.880000e+02 ; w_c = 5.120000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526025e+00	 sigma_n : 1.423898e-02
	 number of secondary particules: 36101
	 number of fission neutrons: 35696

 Stat infos before Combing: Nn = 915 ; Nc = 751 ; w_n =  8.364082e+02 ; w_c = 5.120000e+02


 Stat infos after Combing: Nn = 620 ; Nc = 379 ; w_n =  6.200000e+02 ; w_c = 3.790000e+02


 Type and parameters of random generator before batch 10 : 
	 DRAND48_RANDOM 27752 12090 55898  COUNTER	96532343


 batch number : 10

  Preparing critical source : iteration 1 out of 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.821833e+00	 sigma_n : 9.124789e-02
	 number of secondary particules: 6553
	 number of fission neutrons: 1073
	 number of sampled neutrons for dynamic: 2740
	 number of sampled precursors for dynamic: 2740

           Dynamic normalization factor = 7.646301e-02


         Stats about population importance biasing:
           neutron weight  = 6.519725e-06   precursor weight = 8.380523e+01   ratio = 7.779616e-08
           biased neutron weight = 9.313892e+01
           neutron importance = 1.477961e-07


 Stat infos before Combing: Nn = 2740 ; Nc = 2740 ; w_n =  9.313892e+01 ; w_c = 8.380523e+01


 Stat infos after Combing: Nn = 527 ; Nc = 473 ; w_n =  5.270000e+02 ; w_c = 4.730000e+02


 simulation time (s) : 50


	 Dynamic calculation : beginning time step number : 1 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.484626e+00	 sigma_n : 1.316967e-02
	 number of secondary particules: 41148
	 number of fission neutrons: 40745

 Stat infos before Combing: Nn = 994 ; Nc = 714 ; w_n =  9.036679e+02 ; w_c = 4.730000e+02


 Stat infos after Combing: Nn = 657 ; Nc = 344 ; w_n =  6.570000e+02 ; w_c = 3.440000e+02


	 Dynamic calculation : beginning time step number : 2 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534284e+00	 sigma_n : 1.593185e-02
	 number of secondary particules: 29825
	 number of fission neutrons: 29504

 Stat infos before Combing: Nn = 436 ; Nc = 535 ; w_n =  3.989887e+02 ; w_c = 3.440000e+02


 Stat infos after Combing: Nn = 537 ; Nc = 463 ; w_n =  5.370000e+02 ; w_c = 4.630000e+02


	 Dynamic calculation : beginning time step number : 3 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525472e+00	 sigma_n : 1.731216e-02
	 number of secondary particules: 24634
	 number of fission neutrons: 24310

 Stat infos before Combing: Nn = 466 ; Nc = 626 ; w_n =  4.227251e+02 ; w_c = 4.630000e+02


 Stat infos after Combing: Nn = 478 ; Nc = 523 ; w_n =  4.780000e+02 ; w_c = 5.230000e+02


	 Dynamic calculation : beginning time step number : 4 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500781e+00	 sigma_n : 1.434589e-02
	 number of secondary particules: 35616
	 number of fission neutrons: 35244

 Stat infos before Combing: Nn = 1083 ; Nc = 745 ; w_n =  9.892795e+02 ; w_c = 5.230000e+02


 Stat infos after Combing: Nn = 654 ; Nc = 346 ; w_n =  6.540000e+02 ; w_c = 3.460000e+02


	 Dynamic calculation : beginning time step number : 5 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545741e+00	 sigma_n : 1.631641e-02
	 number of secondary particules: 28719
	 number of fission neutrons: 28448

 Stat infos before Combing: Nn = 509 ; Nc = 511 ; w_n =  4.635162e+02 ; w_c = 3.460000e+02


 Stat infos after Combing: Nn = 572 ; Nc = 428 ; w_n =  5.720000e+02 ; w_c = 4.280000e+02


	 Dynamic calculation : beginning time step number : 6 out of 10



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.020696e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522064e+00	 sigma_n : 1.703392e-02
	 number of secondary particules: 25031
	 number of fission neutrons: 24726

 Stat infos before Combing: Nn = 479 ; Nc = 605 ; w_n =  4.359581e+02 ; w_c = 4.280000e+02


 Stat infos after Combing: Nn = 504 ; Nc = 495 ; w_n =  5.040000e+02 ; w_c = 4.950000e+02


	 Dynamic calculation : beginning time step number : 7 out of 10



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.214613e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539450e+00	 sigma_n : 1.505838e-02
	 number of secondary particules: 31760
	 number of fission neutrons: 31377

 Stat infos before Combing: Nn = 774 ; Nc = 706 ; w_n =  7.087014e+02 ; w_c = 4.950000e+02


 Stat infos after Combing: Nn = 588 ; Nc = 412 ; w_n =  5.880000e+02 ; w_c = 4.120000e+02


	 Dynamic calculation : beginning time step number : 8 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547249e+00	 sigma_n : 1.667168e-02
	 number of secondary particules: 27342
	 number of fission neutrons: 27046

 Stat infos before Combing: Nn = 449 ; Nc = 585 ; w_n =  4.097799e+02 ; w_c = 4.120000e+02


 Stat infos after Combing: Nn = 498 ; Nc = 501 ; w_n =  4.980000e+02 ; w_c = 5.010000e+02


	 Dynamic calculation : beginning time step number : 9 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549268e+00	 sigma_n : 1.731005e-02
	 number of secondary particules: 24865
	 number of fission neutrons: 24545

 Stat infos before Combing: Nn = 327 ; Nc = 645 ; w_n =  2.961124e+02 ; w_c = 5.010000e+02


 Stat infos after Combing: Nn = 372 ; Nc = 629 ; w_n =  3.720000e+02 ; w_c = 6.290000e+02


	 Dynamic calculation : beginning time step number : 10 out of 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527996e+00	 sigma_n : 1.711854e-02
	 number of secondary particules: 25446
	 number of fission neutrons: 25086

 Stat infos before Combing: Nn = 327 ; Nc = 765 ; w_n =  2.987526e+02 ; w_c = 6.290000e+02


 Stat infos after Combing: Nn = 322 ; Nc = 678 ; w_n =  3.220000e+02 ; w_c = 6.780000e+02


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 5.142170e+03	 sigma = 3.950727e+02	 sigma% = 7.682995e+00


 Edition after batch number : 10



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : neutron_flux_response
SCORE NAME : neutron_flux_mesh_score
ENERGY DECOUPAGE NAME : grid_rough


 PARTICULE : NEUTRON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)


Energy range (in MeV): 1.000000e-11 - 1.000000e-03
	 (0,0,0)	 (-3.3333, -3.3333, -8.0000)   	8.888889e+01	1.881159e-12	5.613183e+01
	 (0,0,1)	 (-3.3333, -3.3333, 0.0000)   	8.888889e+01	2.328291e-12	8.865155e+01
	 (0,0,2)	 (-3.3333, -3.3333, 8.0000)   	8.888889e+01	4.185260e-12	4.173750e+01
	 (0,1,0)	 (-3.3333, -0.0000, -8.0000)   	8.888889e+01	3.446027e-12	6.151311e+01
	 (0,1,1)	 (-3.3333, -0.0000, 0.0000)   	8.888889e+01	3.720632e-12	7.563773e+01
	 (0,1,2)	 (-3.3333, -0.0000, 8.0000)   	8.888889e+01	1.279066e-12	6.251798e+01
	 (0,2,0)	 (-3.3333, 3.3333, -8.0000)   	8.888889e+01	8.972453e-12	4.985785e+01
	 (0,2,1)	 (-3.3333, 3.3333, 0.0000)   	8.888889e+01	6.567828e-12	5.796363e+01
	 (0,2,2)	 (-3.3333, 3.3333, 8.0000)   	8.888889e+01	4.930132e-12	4.420874e+01
	 (1,0,0)	 (-0.0000, -3.3333, -8.0000)   	8.888889e+01	1.384531e-11	7.817644e+01
	 (1,0,1)	 (-0.0000, -3.3333, 0.0000)   	8.888889e+01	8.712167e-12	4.116847e+01
	 (1,0,2)	 (-0.0000, -3.3333, 8.0000)   	8.888889e+01	1.414736e-11	2.644131e+01
	 (1,1,0)	 (-0.0000, -0.0000, -8.0000)   	8.888889e+01	8.298290e-12	2.524264e+01
	 (1,1,1)	 (-0.0000, -0.0000, 0.0000)   	8.888889e+01	8.610659e-12	2.809260e+01
	 (1,1,2)	 (-0.0000, -0.0000, 8.0000)   	8.888889e+01	1.232625e-11	3.123814e+01
	 (1,2,0)	 (-0.0000, 3.3333, -8.0000)   	8.888889e+01	1.362514e-11	5.593718e+01
	 (1,2,1)	 (-0.0000, 3.3333, 0.0000)   	8.888889e+01	3.822722e-12	6.372923e+01
	 (1,2,2)	 (-0.0000, 3.3333, 8.0000)   	8.888889e+01	8.669567e-12	5.417393e+01
	 (2,0,0)	 (3.3333, -3.3333, -8.0000)   	8.888889e+01	1.585482e-12	6.682385e+01
	 (2,0,1)	 (3.3333, -3.3333, 0.0000)   	8.888889e+01	8.441054e-12	4.376305e+01
	 (2,0,2)	 (3.3333, -3.3333, 8.0000)   	8.888889e+01	6.944476e-12	5.653471e+01
	 (2,1,0)	 (3.3333, -0.0000, -8.0000)   	8.888889e+01	4.805484e-12	7.217379e+01
	 (2,1,1)	 (3.3333, -0.0000, 0.0000)   	8.888889e+01	1.480615e-12	4.383946e+01
	 (2,1,2)	 (3.3333, -0.0000, 8.0000)   	8.888889e+01	9.388352e-12	5.033698e+01
	 (2,2,0)	 (3.3333, 3.3333, -8.0000)   	8.888889e+01	4.910860e-12	6.234199e+01
	 (2,2,1)	 (3.3333, 3.3333, 0.0000)   	8.888889e+01	7.465950e-12	5.139918e+01
	 (2,2,2)	 (3.3333, 3.3333, 8.0000)   	8.888889e+01	5.793184e-12	6.742898e+01

Energy range (in MeV): 1.000000e-03 - 2.000000e+01
	 (0,0,0)	 (-3.3333, -3.3333, -8.0000)   	8.888889e+01	3.509046e-07	4.573222e+00
	 (0,0,1)	 (-3.3333, -3.3333, 0.0000)   	8.888889e+01	5.545677e-07	4.304534e+00
	 (0,0,2)	 (-3.3333, -3.3333, 8.0000)   	8.888889e+01	3.524989e-07	4.365844e+00
	 (0,1,0)	 (-3.3333, -0.0000, -8.0000)   	8.888889e+01	3.799885e-07	4.289582e+00
	 (0,1,1)	 (-3.3333, -0.0000, 0.0000)   	8.888889e+01	6.080182e-07	4.393297e+00
	 (0,1,2)	 (-3.3333, -0.0000, 8.0000)   	8.888889e+01	3.855219e-07	4.384487e+00
	 (0,2,0)	 (-3.3333, 3.3333, -8.0000)   	8.888889e+01	3.466607e-07	4.165400e+00
	 (0,2,1)	 (-3.3333, 3.3333, 0.0000)   	8.888889e+01	5.525350e-07	4.270214e+00
	 (0,2,2)	 (-3.3333, 3.3333, 8.0000)   	8.888889e+01	3.467975e-07	4.450902e+00
	 (1,0,0)	 (-0.0000, -3.3333, -8.0000)   	8.888889e+01	4.830758e-07	4.492233e+00
	 (1,0,1)	 (-0.0000, -3.3333, 0.0000)   	8.888889e+01	7.733358e-07	4.470193e+00
	 (1,0,2)	 (-0.0000, -3.3333, 8.0000)   	8.888889e+01	4.823414e-07	4.194053e+00
	 (1,1,0)	 (-0.0000, -0.0000, -8.0000)   	8.888889e+01	5.281598e-07	4.402387e+00
	 (1,1,1)	 (-0.0000, -0.0000, 0.0000)   	8.888889e+01	8.466185e-07	4.546959e+00
	 (1,1,2)	 (-0.0000, -0.0000, 8.0000)   	8.888889e+01	5.363593e-07	4.373216e+00
	 (1,2,0)	 (-0.0000, 3.3333, -8.0000)   	8.888889e+01	4.773077e-07	4.217313e+00
	 (1,2,1)	 (-0.0000, 3.3333, 0.0000)   	8.888889e+01	7.689001e-07	4.048204e+00
	 (1,2,2)	 (-0.0000, 3.3333, 8.0000)   	8.888889e+01	4.899336e-07	4.403347e+00
	 (2,0,0)	 (3.3333, -3.3333, -8.0000)   	8.888889e+01	3.494020e-07	4.622985e+00
	 (2,0,1)	 (3.3333, -3.3333, 0.0000)   	8.888889e+01	5.586536e-07	4.372939e+00
	 (2,0,2)	 (3.3333, -3.3333, 8.0000)   	8.888889e+01	3.497184e-07	4.042350e+00
	 (2,1,0)	 (3.3333, -0.0000, -8.0000)   	8.888889e+01	3.833813e-07	4.640119e+00
	 (2,1,1)	 (3.3333, -0.0000, 0.0000)   	8.888889e+01	6.123770e-07	4.092040e+00
	 (2,1,2)	 (3.3333, -0.0000, 8.0000)   	8.888889e+01	3.904692e-07	4.296427e+00
	 (2,2,0)	 (3.3333, 3.3333, -8.0000)   	8.888889e+01	3.439675e-07	4.542347e+00
	 (2,2,1)	 (3.3333, 3.3333, 0.0000)   	8.888889e+01	5.560981e-07	4.061926e+00
	 (2,2,2)	 (3.3333, 3.3333, 8.0000)   	8.888889e+01	3.539183e-07	4.337801e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-3.3333, -3.3333, -8.0000)	8.888889e+01	3.509065e-07	4.573411e+00
	 (0,0,1)	 (-3.3333, -3.3333, 0.0000)	8.888889e+01	5.545700e-07	4.304654e+00
	 (0,0,2)	 (-3.3333, -3.3333, 8.0000)	8.888889e+01	3.525031e-07	4.366116e+00
	 (0,1,0)	 (-3.3333, -0.0000, -8.0000)	8.888889e+01	3.799919e-07	4.289698e+00
	 (0,1,1)	 (-3.3333, -0.0000, 0.0000)	8.888889e+01	6.080220e-07	4.393297e+00
	 (0,1,2)	 (-3.3333, -0.0000, 8.0000)	8.888889e+01	3.855232e-07	4.384402e+00
	 (0,2,0)	 (-3.3333, 3.3333, -8.0000)	8.888889e+01	3.466697e-07	4.165301e+00
	 (0,2,1)	 (-3.3333, 3.3333, 0.0000)	8.888889e+01	5.525415e-07	4.270050e+00
	 (0,2,2)	 (-3.3333, 3.3333, 8.0000)	8.888889e+01	3.468025e-07	4.450692e+00
	 (1,0,0)	 (-0.0000, -3.3333, -8.0000)	8.888889e+01	4.830896e-07	4.491966e+00
	 (1,0,1)	 (-0.0000, -3.3333, 0.0000)	8.888889e+01	7.733445e-07	4.470397e+00
	 (1,0,2)	 (-0.0000, -3.3333, 8.0000)	8.888889e+01	4.823555e-07	4.194221e+00
	 (1,1,0)	 (-0.0000, -0.0000, -8.0000)	8.888889e+01	5.281681e-07	4.402180e+00
	 (1,1,1)	 (-0.0000, -0.0000, 0.0000)	8.888889e+01	8.466271e-07	4.546910e+00
	 (1,1,2)	 (-0.0000, -0.0000, 8.0000)	8.888889e+01	5.363716e-07	4.373223e+00
	 (1,2,0)	 (-0.0000, 3.3333, -8.0000)	8.888889e+01	4.773213e-07	4.218040e+00
	 (1,2,1)	 (-0.0000, 3.3333, 0.0000)	8.888889e+01	7.689039e-07	4.048329e+00
	 (1,2,2)	 (-0.0000, 3.3333, 8.0000)	8.888889e+01	4.899423e-07	4.403088e+00
	 (2,0,0)	 (3.3333, -3.3333, -8.0000)	8.888889e+01	3.494036e-07	4.623054e+00
	 (2,0,1)	 (3.3333, -3.3333, 0.0000)	8.888889e+01	5.586620e-07	4.373001e+00
	 (2,0,2)	 (3.3333, -3.3333, 8.0000)	8.888889e+01	3.497253e-07	4.042921e+00
	 (2,1,0)	 (3.3333, -0.0000, -8.0000)	8.888889e+01	3.833861e-07	4.640324e+00
	 (2,1,1)	 (3.3333, -0.0000, 0.0000)	8.888889e+01	6.123785e-07	4.092033e+00
	 (2,1,2)	 (3.3333, -0.0000, 8.0000)	8.888889e+01	3.904786e-07	4.295660e+00
	 (2,2,0)	 (3.3333, 3.3333, -8.0000)	8.888889e+01	3.439724e-07	4.542533e+00
	 (2,2,1)	 (3.3333, 3.3333, 0.0000)	8.888889e+01	5.561056e-07	4.062117e+00
	 (2,2,2)	 (3.3333, 3.3333, 8.0000)	8.888889e+01	3.539241e-07	4.338166e+00

number of batches used: 10	1.316169e-05	4.302001e+00

******************************************************************************
RESPONSE FUNCTION : PRECURSOR WEIGHT
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	10

 CRITICALITY SOURCE	4.796000e+02	2.604253e-01
 END OF TIME STEP 1	4.783000e+02	7.941016e+00
 END OF TIME STEP 2	4.608000e+02	4.888120e+00
 END OF TIME STEP 3	5.389000e+02	8.070823e+00
 END OF TIME STEP 4	4.745000e+02	1.075992e+01
 END OF TIME STEP 5	5.293000e+02	7.753656e+00
 END OF TIME STEP 6	5.301000e+02	6.170724e+00
 END OF TIME STEP 7	4.698000e+02	6.037676e+00
 END OF TIME STEP 8	5.318000e+02	6.072467e+00
 END OF TIME STEP 9	5.204000e+02	5.777749e+00
 END OF TIME STEP 10	5.069000e+02	8.172174e+00


******************************************************************************
RESPONSE FUNCTION : NEUTRON WEIGHT
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	10

 CRITICALITY SOURCE	5.205000e+02	2.366052e-01
 END OF TIME STEP 1	5.219000e+02	7.278704e+00
 END OF TIME STEP 2	5.393000e+02	4.174894e+00
 END OF TIME STEP 3	4.613000e+02	9.404855e+00
 END OF TIME STEP 4	5.253000e+02	9.728586e+00
 END OF TIME STEP 5	4.707000e+02	8.690548e+00
 END OF TIME STEP 6	4.696000e+02	6.946794e+00
 END OF TIME STEP 7	5.303000e+02	5.359725e+00
 END OF TIME STEP 8	4.679000e+02	6.877655e+00
 END OF TIME STEP 9	4.799000e+02	6.257123e+00
 END OF TIME STEP 10	4.933000e+02	8.412611e+00


******************************************************************************
RESPONSE FUNCTION : DYNAMIC NORMALIZATION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	10	8.100642e-02	8.660519e-01



 simulation time (s) : 55


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 924 58514 55883  COUNTER	106890667


=====================================================================
	NORMAL COMPLETION
=====================================================================
