
=====================================================================
$Id$
 hostname: is232540
 pid: 638

=====================================================================
$Id$

 HOSTNAME : is232540

 PROCESS ID is : 638

 DATE : Wed Jan 12 18:26:14 2022

 Version is tripoli4_11_1.

 git version is dba218c0aa0d9c8b8ca51198567c96ee29b5ff73 (CLEAN).

=====================================================================

 data filename = heu-met-fast-001-shell_model.t4
 catalogname = /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512
 execution call = tripoli4 -s NJOY -a -c /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512 -d heu-met-fast-001-shell_model.t4 -o heu-met-fast-001-shell_model.res 


 dictionary file : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/ceav512.dictionary
 mass file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/mass_rmd.mas95
 Q fission directory : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/Qfission
 electron cross section directory : /data/tmpuranus2/GALILEE-V0-3.0/PEID/Electron_Photon
 electron bremsstrahlung cross section directory : /home/tripoli4.11/tripoli4.11.1/AdditionalData/Bremsstrahlung
 abondance file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/abundance
 own evaluations directory : 


 WARNING
 method name : T4_path
 error message : No such directory for own evaluations




 	 reading geometry : 

 	 checking association of compositions and volumes :  ok 


// valjean: old_name: cristal/CL12_s001_c01_geo_detail
COMMENT
NEA/NSC/DOC(95)03/II HEU-MET-FAST-001
Bare, Highly Enriched Uranium Sphere (Godiva), geometry_detail
Resultats existes   7
Experience                              1.0000   0.0010
KENO (16g Hansen-Roach)                 0.9997   0.0010
KENO (27g ENDF/B-IV)                    1.0032   0.0009
MCNP (ENDF/B-V)                         0.9972   0.0011
ONEDANT (27g ENDF/B-IV)                 1.0080   0.
MONK6B (UKNDL)                          1.0058   0.0010
KENO (299g ABBN-93)                     0.9976   0.0001
COMMENT

GEOMETRIE
TITRE

TYPE 1  SPHERE 1.0216
TYPE 2  SPHERE 1.0541
TYPE 3  SPHERE 6.2809
TYPE 4  SPHERE 6.2937
TYPE 5  SPHERE 7.7525
TYPE 6  SPHERE 7.7620
TYPE 7  SPHERE 8.2527
TYPE 8  SPHERE 8.2610
TYPE 9  SPHERE 8.7062
TYPE 10 SPHERE 8.7499
VOLU 10 COMBI 10 0 0 0 FINV
VOLU 9  COMBI 9 0 0 0  ECRASE 1 10 FINV
VOLU 8  COMBI 8 0 0 0  ECRASE 1 9  FINV
VOLU 7  COMBI 7 0 0 0  ECRASE 1 8  FINV
VOLU 6  COMBI 6 0 0 0  ECRASE 1 7  FINV
VOLU 5  COMBI 5 0 0 0  ECRASE 1 6  FINV
VOLU 4  COMBI 4 0 0 0  ECRASE 1 5  FINV
VOLU 3  COMBI 3 0 0 0  ECRASE 1 4  FINV
VOLU 2  COMBI 2 0 0 0  ECRASE 1 3  FINV
VOLU 1  COMBI 1 0 0 0  ECRASE 1 2  FINV

COMMENT
GRAF
-10 0 -10
1 0 0
0 0 1
20 20
1
COMMENT
FING

COMPOSITION
    7
    PONCTUAL 300  URANIUM_1   3
          U234  4.9357E-4
          U235  4.4936E-2
          U238  2.7213E-3
    PONCTUAL 300  URANIUM_2   3
          U234  4.9357E-4
          U235  4.5244E-2
          U238  2.4168E-3
    PONCTUAL 300  URANIUM_3   3
          U234  4.9357E-4
          U235  4.5268E-2
          U238  2.3930E-3
    PONCTUAL 300  URANIUM_4   3
          U234  4.9357E-4
          U235  4.5090E-2
          U238  2.5690E-3
    PONCTUAL 300  URANIUM_5   3
          U234  4.9357E-4
          U235  4.5239E-2
          U238  2.4215E-3
    PONCTUAL 300  URANIUM_6   3
          U234  4.8974E-4
          U235  4.4874E-2
          U238  2.4169E-3
    PONCTUAL 300  AIR   2
          N14   3.5214E-5
          O16   1.5092E-5
FIN_COMPO

GEOMCOMP
    URANIUM_1   1   1
    URANIUM_2   1   3
    URANIUM_3   1   5
    URANIUM_4   1   7
    URANIUM_5   1   9
    URANIUM_6   1   10
    AIR         4   2 4 6 8
FIN_GEOMCOMP

LIST_SOURCE 1
SOURCE 
    NEUTRON  PONCTUAL  0  0 0
    ANGULAR_DISTRIBUTION   ISOTROPIC 
    ENERGETIC_DISTRIBUTION SPECTRE   WATT_SPECTRE
    TIME_DISTRIBUTION  DIRAC 0
FIN_SOURCE
FIN_LIST_SOURCE

SIMULATION
    CRITICITE DISCARD  100
    BATCH    2100
    SIZE      1000
    EDITION 1050
    ENERGY_INF NEUTRON 1.E-11
    PARTICULES   1 NEUTRON
    GLOBAL_SCORES
FIN_SIMULATION



 data reading time (s): 0

 Total concentration of material URANIUM_1 (1.E24at/cm3) is: 4.815087e-02

 Total concentration of material URANIUM_2 (1.E24at/cm3) is: 4.815437e-02

 Total concentration of material URANIUM_3 (1.E24at/cm3) is: 4.815457e-02

 Total concentration of material URANIUM_4 (1.E24at/cm3) is: 4.815257e-02

 Total concentration of material URANIUM_5 (1.E24at/cm3) is: 4.815407e-02

 Total concentration of material URANIUM_6 (1.E24at/cm3) is: 4.778064e-02

 Total concentration of material AIR (1.E24at/cm3) is: 5.030600e-05


 Loading response functions ...
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 9.999997e-01

		 Energetic density simulation intensity = 9.999997e-01

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         SIMULATION INTENSITY = 1.256637e+01   BIASED SIMULATION INTENSITY = 1.256637e+01

   SUM OF SIMULATION INTENSITIES = 1.256637e+01

   GLOBAL SIMULATION INTENSITY = 1.256637e+01

   BIASED TOTAL SOURCE INTENSITY = 1.256637e+01


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.782000e+00	 sigma_n : 9.945032e-02
	 number of secondary particules: 1398
	 number of fission neutrons: 1398

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.432046e+00	 sigma_n : 7.556922e-02
	 number of secondary particules: 1261
	 number of fission neutrons: 1261

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651864e+00	 sigma_n : 8.260670e-02
	 number of secondary particules: 1282
	 number of fission neutrons: 1282

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491420e+00	 sigma_n : 7.927382e-02
	 number of secondary particules: 1187
	 number of fission neutrons: 1187

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505476e+00	 sigma_n : 8.245262e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619217e+00	 sigma_n : 8.818951e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597260e+00	 sigma_n : 8.543272e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664810e+00	 sigma_n : 9.178154e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862368e+00	 sigma_n : 1.007045e-01
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616216e+00	 sigma_n : 8.263814e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 simulation time (s) : 0


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628410e+00	 sigma_n : 8.589092e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 simulation time (s) : 0


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808285e+00	 sigma_n : 9.775818e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 simulation time (s) : 0


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733772e+00	 sigma_n : 8.873882e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 simulation time (s) : 0


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553425e+00	 sigma_n : 8.420859e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 simulation time (s) : 0


 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737132e+00	 sigma_n : 9.009065e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 simulation time (s) : 0


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581659e+00	 sigma_n : 7.927808e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 simulation time (s) : 0


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521968e+00	 sigma_n : 8.400989e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 simulation time (s) : 0


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639640e+00	 sigma_n : 8.702097e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 simulation time (s) : 0


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536128e+00	 sigma_n : 8.421703e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 simulation time (s) : 0


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774163e+00	 sigma_n : 9.435429e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 simulation time (s) : 0


 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799430e+00	 sigma_n : 9.168705e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578611e+00	 sigma_n : 8.885549e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685581e+00	 sigma_n : 9.417547e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786822e+00	 sigma_n : 9.426791e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600948e+00	 sigma_n : 8.508997e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659309e+00	 sigma_n : 8.728455e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616279e+00	 sigma_n : 9.200214e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640777e+00	 sigma_n : 8.705925e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522727e+00	 sigma_n : 8.544356e-02
	 number of secondary particules: 1008
	 number of fission neutrons: 1008

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.842262e+00	 sigma_n : 9.405702e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671684e+00	 sigma_n : 9.005057e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769231e+00	 sigma_n : 9.601807e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576350e+00	 sigma_n : 8.674883e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704457e+00	 sigma_n : 8.603046e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559667e+00	 sigma_n : 7.768890e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602050e+00	 sigma_n : 8.848027e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.850000e+00	 sigma_n : 9.390829e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 38

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647393e+00	 sigma_n : 8.498332e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 39

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717349e+00	 sigma_n : 8.930883e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 40

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510483e+00	 sigma_n : 8.246417e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 41

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800575e+00	 sigma_n : 9.016032e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 42

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690000e+00	 sigma_n : 8.337378e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 43

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.517904e+00	 sigma_n : 8.597341e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 44

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552486e+00	 sigma_n : 8.789229e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 45

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677716e+00	 sigma_n : 8.745035e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 46

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621908e+00	 sigma_n : 8.931094e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 47

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751144e+00	 sigma_n : 9.252693e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 48

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595427e+00	 sigma_n : 8.502666e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 49

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729412e+00	 sigma_n : 8.807930e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 50

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578853e+00	 sigma_n : 8.087065e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 51

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.440966e+00	 sigma_n : 7.598156e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 52

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641584e+00	 sigma_n : 8.784610e-02
	 number of secondary particules: 990
	 number of fission neutrons: 990

 batch number : 53

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781818e+00	 sigma_n : 9.024978e-02
	 number of secondary particules: 1008
	 number of fission neutrons: 1008

 batch number : 54

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723214e+00	 sigma_n : 8.675516e-02
	 number of secondary particules: 986
	 number of fission neutrons: 986

 batch number : 55

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.924949e+00	 sigma_n : 9.535309e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 56

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550778e+00	 sigma_n : 8.726158e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 57

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667625e+00	 sigma_n : 8.578734e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 58

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655139e+00	 sigma_n : 8.875892e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 59

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.817374e+00	 sigma_n : 9.136318e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 60

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754006e+00	 sigma_n : 9.152361e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 61

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760989e+00	 sigma_n : 9.249520e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 62

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.487109e+00	 sigma_n : 8.026549e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 63

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.916256e+00	 sigma_n : 9.333499e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 64

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.876751e+00	 sigma_n : 9.093263e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 65

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588542e+00	 sigma_n : 8.719413e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 66

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658949e+00	 sigma_n : 9.082657e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 67

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567616e+00	 sigma_n : 8.147894e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 68

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585059e+00	 sigma_n : 8.124301e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 69

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632205e+00	 sigma_n : 8.477647e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 70

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.506387e+00	 sigma_n : 8.454337e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 71

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759771e+00	 sigma_n : 9.171553e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 72

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711261e+00	 sigma_n : 9.065530e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 73

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711911e+00	 sigma_n : 9.075769e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 74

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719198e+00	 sigma_n : 8.672755e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 75

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664129e+00	 sigma_n : 8.580264e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 76

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705660e+00	 sigma_n : 8.904266e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 77

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749316e+00	 sigma_n : 9.307717e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 78

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535590e+00	 sigma_n : 8.114405e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 79

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636119e+00	 sigma_n : 8.339534e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 80

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774528e+00	 sigma_n : 9.061426e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 81

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593002e+00	 sigma_n : 8.686078e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 82

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689293e+00	 sigma_n : 8.990925e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 83

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757843e+00	 sigma_n : 9.054467e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 84

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633552e+00	 sigma_n : 8.286228e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 85

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748837e+00	 sigma_n : 9.160409e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 86

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632727e+00	 sigma_n : 8.498696e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 87

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846948e+00	 sigma_n : 9.223465e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 88

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632988e+00	 sigma_n : 8.789630e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 89

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556612e+00	 sigma_n : 8.058475e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 90

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632314e+00	 sigma_n : 8.730537e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 91

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620564e+00	 sigma_n : 8.525483e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 92

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.802988e+00	 sigma_n : 1.000686e-01
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 93

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558770e+00	 sigma_n : 8.385049e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 94

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558935e+00	 sigma_n : 8.142966e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 95

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618306e+00	 sigma_n : 9.376682e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 96

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.844961e+00	 sigma_n : 9.806047e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 97

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516038e+00	 sigma_n : 8.425459e-02
	 number of secondary particules: 993
	 number of fission neutrons: 993

 batch number : 98

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787298e+00	 sigma_n : 9.891279e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 99

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751671e+00	 sigma_n : 8.530502e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510000e+00	 sigma_n : 8.475922e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 101

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.818182e+00	 sigma_n : 9.544085e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 102

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761046e+00	 sigma_n : 8.503733e-02
	 number of secondary particules: 1202
	 number of fission neutrons: 1202

 batch number : 103

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638103e+00	 sigma_n : 9.035489e-02
	 number of secondary particules: 1254
	 number of fission neutrons: 1254

 batch number : 104

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.434609e+00	 sigma_n : 8.206584e-02
	 number of secondary particules: 1187
	 number of fission neutrons: 1187

 batch number : 105

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.384162e+00	 sigma_n : 8.027044e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 106

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566092e+00	 sigma_n : 8.991023e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 107

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793035e+00	 sigma_n : 1.026156e-01
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 108

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680266e+00	 sigma_n : 9.359900e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 109

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687443e+00	 sigma_n : 8.993447e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 110

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625000e+00	 sigma_n : 8.776840e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 111

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699074e+00	 sigma_n : 8.901301e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 112

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602941e+00	 sigma_n : 8.315853e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 113

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.802271e+00	 sigma_n : 9.075595e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 114

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728558e+00	 sigma_n : 8.860647e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 115

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724046e+00	 sigma_n : 9.000115e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 116

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514706e+00	 sigma_n : 8.616426e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 117

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750912e+00	 sigma_n : 9.412729e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 118

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666965e+00	 sigma_n : 8.531853e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 119

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.421324e+00	 sigma_n : 7.958525e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 120

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.470641e+00	 sigma_n : 8.265747e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 121

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735075e+00	 sigma_n : 8.615848e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 122

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597826e+00	 sigma_n : 8.469738e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 123

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570240e+00	 sigma_n : 8.171010e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 124

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664403e+00	 sigma_n : 8.985471e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 125

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644231e+00	 sigma_n : 8.695535e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 126

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749265e+00	 sigma_n : 9.077715e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 127

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786982e+00	 sigma_n : 9.475204e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 128

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788425e+00	 sigma_n : 9.168581e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 129

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570285e+00	 sigma_n : 8.389146e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 130

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650624e+00	 sigma_n : 8.500802e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 131

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544362e+00	 sigma_n : 8.217549e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 132

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.914428e+00	 sigma_n : 9.367756e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 133

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628972e+00	 sigma_n : 8.608096e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 134

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655378e+00	 sigma_n : 9.271722e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 135

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615970e+00	 sigma_n : 8.786980e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 136

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778320e+00	 sigma_n : 9.706032e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 137

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698219e+00	 sigma_n : 8.393287e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 138

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629764e+00	 sigma_n : 8.792098e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 139

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600726e+00	 sigma_n : 8.626190e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 140

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749765e+00	 sigma_n : 8.650348e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 141

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665766e+00	 sigma_n : 8.611609e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 142

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761596e+00	 sigma_n : 8.873541e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 143

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.385022e+00	 sigma_n : 7.889183e-02
	 number of secondary particules: 994
	 number of fission neutrons: 994

 batch number : 144

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776660e+00	 sigma_n : 9.957357e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 145

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745829e+00	 sigma_n : 9.238222e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 146

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862911e+00	 sigma_n : 9.833763e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 147

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723035e+00	 sigma_n : 9.155495e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 148

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604905e+00	 sigma_n : 8.632505e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 149

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568097e+00	 sigma_n : 8.590674e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 150

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.831527e+00	 sigma_n : 9.247906e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 151

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568461e+00	 sigma_n : 8.304945e-02
	 number of secondary particules: 993
	 number of fission neutrons: 993

 batch number : 152

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.940584e+00	 sigma_n : 9.631260e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 153

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744661e+00	 sigma_n : 8.883266e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 154

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551293e+00	 sigma_n : 8.021860e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 155

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586331e+00	 sigma_n : 8.448285e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 156

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704874e+00	 sigma_n : 8.547169e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 157

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622458e+00	 sigma_n : 8.480657e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 158

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607985e+00	 sigma_n : 8.876857e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 159

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510678e+00	 sigma_n : 8.230989e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 160

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583254e+00	 sigma_n : 8.607167e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 161

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651163e+00	 sigma_n : 8.683756e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 162

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676749e+00	 sigma_n : 8.568988e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 163

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643363e+00	 sigma_n : 8.676079e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 164

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568142e+00	 sigma_n : 8.351063e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 165

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759734e+00	 sigma_n : 9.724787e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 166

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.459246e+00	 sigma_n : 8.097722e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 167

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.028155e+00	 sigma_n : 9.608066e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 168

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510256e+00	 sigma_n : 8.387663e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 169

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678108e+00	 sigma_n : 8.693884e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 170

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720469e+00	 sigma_n : 9.038930e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 171

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.430192e+00	 sigma_n : 8.274885e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 172

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652632e+00	 sigma_n : 8.710149e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 173

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691105e+00	 sigma_n : 9.116043e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 174

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801377e+00	 sigma_n : 9.204346e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 175

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631879e+00	 sigma_n : 8.493858e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 176

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646654e+00	 sigma_n : 8.410221e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 177

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693359e+00	 sigma_n : 9.195451e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 178

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.854267e+00	 sigma_n : 9.783162e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 179

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604464e+00	 sigma_n : 8.412640e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 180

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540633e+00	 sigma_n : 8.337916e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 181

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556808e+00	 sigma_n : 8.382215e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 182

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.481343e+00	 sigma_n : 7.984585e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 183

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750700e+00	 sigma_n : 8.895689e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 184

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721281e+00	 sigma_n : 8.762454e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 185

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792098e+00	 sigma_n : 9.152696e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 186

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.457789e+00	 sigma_n : 8.208269e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 187

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.882521e+00	 sigma_n : 9.652899e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 188

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.441696e+00	 sigma_n : 8.078350e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 189

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782651e+00	 sigma_n : 8.930085e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 190

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584300e+00	 sigma_n : 8.661120e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 191

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465909e+00	 sigma_n : 8.747998e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 192

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762631e+00	 sigma_n : 9.009669e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 193

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744250e+00	 sigma_n : 8.853384e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 194

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663645e+00	 sigma_n : 8.788462e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 195

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776093e+00	 sigma_n : 8.824427e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 196

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583029e+00	 sigma_n : 8.902010e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 197

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790720e+00	 sigma_n : 9.551908e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 198

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537991e+00	 sigma_n : 7.980588e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 199

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596050e+00	 sigma_n : 9.058587e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775070e+00	 sigma_n : 9.498511e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 201

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608696e+00	 sigma_n : 8.434528e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 202

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736499e+00	 sigma_n : 9.291274e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 203

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585022e+00	 sigma_n : 8.655933e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 204

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709271e+00	 sigma_n : 9.149270e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 205

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653949e+00	 sigma_n : 8.630870e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 206

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609137e+00	 sigma_n : 8.776870e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 207

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601702e+00	 sigma_n : 8.479109e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 208

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703226e+00	 sigma_n : 8.862776e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 209

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687616e+00	 sigma_n : 8.470655e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 210

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767760e+00	 sigma_n : 9.039248e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 211

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566459e+00	 sigma_n : 8.745777e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 212

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.837994e+00	 sigma_n : 8.971355e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 213

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654859e+00	 sigma_n : 9.787962e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 214

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573622e+00	 sigma_n : 8.723301e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 215

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666353e+00	 sigma_n : 8.837018e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 216

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740201e+00	 sigma_n : 8.856646e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 217

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642419e+00	 sigma_n : 8.460228e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 218

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543636e+00	 sigma_n : 8.612438e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 219

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663734e+00	 sigma_n : 8.467612e-02
	 number of secondary particules: 970
	 number of fission neutrons: 970

 batch number : 220

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.128866e+00	 sigma_n : 1.026750e-01
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 221

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590383e+00	 sigma_n : 8.571609e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 222

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778285e+00	 sigma_n : 9.126027e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 223

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486014e+00	 sigma_n : 7.816839e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 224

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611358e+00	 sigma_n : 9.234600e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 225

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464348e+00	 sigma_n : 7.816934e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 226

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652381e+00	 sigma_n : 8.985045e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 227

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597514e+00	 sigma_n : 8.908911e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 228

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718540e+00	 sigma_n : 9.000589e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 229

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.859551e+00	 sigma_n : 9.674114e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 230

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593310e+00	 sigma_n : 9.285158e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 231

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.479058e+00	 sigma_n : 8.041858e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 232

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681946e+00	 sigma_n : 8.450982e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 233

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803017e+00	 sigma_n : 9.980379e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 234

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673820e+00	 sigma_n : 9.024533e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 235

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523810e+00	 sigma_n : 8.980743e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 236

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783394e+00	 sigma_n : 9.173573e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 237

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621239e+00	 sigma_n : 8.561769e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 238

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493506e+00	 sigma_n : 7.821862e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 239

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665768e+00	 sigma_n : 8.751783e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 240

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588078e+00	 sigma_n : 8.418762e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 241

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635936e+00	 sigma_n : 8.571482e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 242

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669838e+00	 sigma_n : 8.906725e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 243

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637044e+00	 sigma_n : 8.661510e-02
	 number of secondary particules: 998
	 number of fission neutrons: 998

 batch number : 244

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.890782e+00	 sigma_n : 1.021430e-01
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 245

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.424270e+00	 sigma_n : 8.194972e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 246

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.408451e+00	 sigma_n : 7.629085e-02
	 number of secondary particules: 999
	 number of fission neutrons: 999

 batch number : 247

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719720e+00	 sigma_n : 9.373293e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 248

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779744e+00	 sigma_n : 9.350797e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 249

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722430e+00	 sigma_n : 9.029840e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 250

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705882e+00	 sigma_n : 8.654618e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 251

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608811e+00	 sigma_n : 8.785459e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 252

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644651e+00	 sigma_n : 8.413266e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 253

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597415e+00	 sigma_n : 8.570077e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 254

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729282e+00	 sigma_n : 9.806025e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 255

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596892e+00	 sigma_n : 8.891425e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 256

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533693e+00	 sigma_n : 7.891187e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 257

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631031e+00	 sigma_n : 8.924501e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 258

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642789e+00	 sigma_n : 8.815275e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 259

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808061e+00	 sigma_n : 9.268151e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 260

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562832e+00	 sigma_n : 8.551761e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 261

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.469589e+00	 sigma_n : 8.164521e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 262

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.933140e+00	 sigma_n : 1.007606e-01
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 263

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804209e+00	 sigma_n : 9.251692e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 264

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.408778e+00	 sigma_n : 7.549374e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 265

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748571e+00	 sigma_n : 8.745146e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 266

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769513e+00	 sigma_n : 9.231472e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 267

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697264e+00	 sigma_n : 8.805778e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 268

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670130e+00	 sigma_n : 8.379696e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 269

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635171e+00	 sigma_n : 8.879117e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 270

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.449821e+00	 sigma_n : 8.020273e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 271

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636280e+00	 sigma_n : 8.324480e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 272

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550000e+00	 sigma_n : 8.489263e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 273

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733459e+00	 sigma_n : 9.151025e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 274

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668207e+00	 sigma_n : 8.880358e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 275

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760223e+00	 sigma_n : 8.696559e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 276

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630199e+00	 sigma_n : 8.684679e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 277

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698853e+00	 sigma_n : 9.021459e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 278

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694915e+00	 sigma_n : 9.008978e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 279

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672023e+00	 sigma_n : 8.660201e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 280

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.829945e+00	 sigma_n : 9.267065e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 281

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.472997e+00	 sigma_n : 7.912626e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 282

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661525e+00	 sigma_n : 8.850868e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 283

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602993e+00	 sigma_n : 8.621546e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 284

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593002e+00	 sigma_n : 8.496413e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 285

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769231e+00	 sigma_n : 9.378132e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 286

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643732e+00	 sigma_n : 8.633714e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 287

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502317e+00	 sigma_n : 7.944737e-02
	 number of secondary particules: 985
	 number of fission neutrons: 985

 batch number : 288

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.847716e+00	 sigma_n : 9.499873e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 289

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574230e+00	 sigma_n : 8.598100e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 290

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702913e+00	 sigma_n : 8.732980e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 291

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688213e+00	 sigma_n : 8.868372e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 292

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.909971e+00	 sigma_n : 9.477991e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 293

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585172e+00	 sigma_n : 8.759557e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 294

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769088e+00	 sigma_n : 8.928501e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 295

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.496084e+00	 sigma_n : 8.062913e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 296

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687558e+00	 sigma_n : 8.914898e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 297

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663073e+00	 sigma_n : 8.417177e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 298

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490418e+00	 sigma_n : 8.139124e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 299

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793039e+00	 sigma_n : 8.879276e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 300

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808411e+00	 sigma_n : 9.022654e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 301

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556719e+00	 sigma_n : 7.830994e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 302

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636197e+00	 sigma_n : 8.239191e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 303

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640666e+00	 sigma_n : 8.239515e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 304

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595427e+00	 sigma_n : 7.936578e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 305

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619303e+00	 sigma_n : 8.750700e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 306

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473413e+00	 sigma_n : 7.971875e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 307

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585544e+00	 sigma_n : 8.325623e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 308

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685820e+00	 sigma_n : 8.941002e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 309

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641778e+00	 sigma_n : 9.188779e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 310

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597874e+00	 sigma_n : 8.615754e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 311

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625831e+00	 sigma_n : 8.694796e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 312

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585878e+00	 sigma_n : 8.332479e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 313

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809145e+00	 sigma_n : 9.127683e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 314

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643330e+00	 sigma_n : 8.876403e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 315

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.624299e+00	 sigma_n : 8.312169e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 316

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608333e+00	 sigma_n : 8.944639e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 317

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639070e+00	 sigma_n : 9.100538e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 318

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533569e+00	 sigma_n : 8.809378e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 319

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626728e+00	 sigma_n : 8.962649e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 320

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611586e+00	 sigma_n : 9.009682e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 321

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678742e+00	 sigma_n : 8.621090e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 322

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685068e+00	 sigma_n : 8.886827e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 323

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613678e+00	 sigma_n : 9.418882e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 324

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671684e+00	 sigma_n : 8.952770e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 325

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759809e+00	 sigma_n : 9.188364e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 326

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565498e+00	 sigma_n : 8.772423e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 327

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598485e+00	 sigma_n : 8.472780e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 328

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769608e+00	 sigma_n : 9.535609e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 329

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619048e+00	 sigma_n : 8.779337e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 330

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833659e+00	 sigma_n : 9.205134e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 331

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551317e+00	 sigma_n : 7.962400e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 332

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707635e+00	 sigma_n : 9.195409e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 333

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601671e+00	 sigma_n : 8.070591e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 334

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789377e+00	 sigma_n : 9.315051e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 335

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543630e+00	 sigma_n : 8.852185e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 336

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598190e+00	 sigma_n : 8.863364e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 337

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.529194e+00	 sigma_n : 8.559962e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 338

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800584e+00	 sigma_n : 9.042259e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 339

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769804e+00	 sigma_n : 9.299803e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 340

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717536e+00	 sigma_n : 8.959374e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 341

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687674e+00	 sigma_n : 8.471582e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 342

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656163e+00	 sigma_n : 8.885513e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 343

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808947e+00	 sigma_n : 9.340701e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 344

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614593e+00	 sigma_n : 8.871350e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 345

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641419e+00	 sigma_n : 8.761052e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 346

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789675e+00	 sigma_n : 8.917212e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 347

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.446364e+00	 sigma_n : 7.839609e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 348

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.910537e+00	 sigma_n : 1.061399e-01
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 349

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710476e+00	 sigma_n : 9.477706e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 350

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792877e+00	 sigma_n : 9.024441e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 351

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603860e+00	 sigma_n : 8.126502e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 352

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694129e+00	 sigma_n : 8.780991e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 353

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.852830e+00	 sigma_n : 9.676582e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 354

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645191e+00	 sigma_n : 9.001155e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 355

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779124e+00	 sigma_n : 9.400458e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 356

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630282e+00	 sigma_n : 8.369936e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 357

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647611e+00	 sigma_n : 8.264333e-02
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 358

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555081e+00	 sigma_n : 8.398255e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 359

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497754e+00	 sigma_n : 7.974329e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 360

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804924e+00	 sigma_n : 9.280743e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 361

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587927e+00	 sigma_n : 8.315059e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 362

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525154e+00	 sigma_n : 8.224034e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 363

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681186e+00	 sigma_n : 8.994609e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 364

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617273e+00	 sigma_n : 8.729287e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 365

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747547e+00	 sigma_n : 8.958240e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 366

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630017e+00	 sigma_n : 8.991762e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 367

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714541e+00	 sigma_n : 8.838791e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 368

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588646e+00	 sigma_n : 8.182114e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 369

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.483478e+00	 sigma_n : 8.664212e-02
	 number of secondary particules: 1179
	 number of fission neutrons: 1179

 batch number : 370

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519084e+00	 sigma_n : 8.479558e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 371

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710952e+00	 sigma_n : 8.558994e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 372

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782095e+00	 sigma_n : 9.347234e-02
	 number of secondary particules: 1246
	 number of fission neutrons: 1246

 batch number : 373

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.365971e+00	 sigma_n : 7.648608e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 374

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586667e+00	 sigma_n : 7.971281e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 375

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672367e+00	 sigma_n : 9.440500e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 376

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552200e+00	 sigma_n : 8.367374e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 377

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636364e+00	 sigma_n : 8.408143e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 378

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617295e+00	 sigma_n : 8.506880e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 379

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781338e+00	 sigma_n : 9.300041e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 380

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613322e+00	 sigma_n : 8.877331e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 381

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.487805e+00	 sigma_n : 7.998856e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 382

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793103e+00	 sigma_n : 9.162267e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 383

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559491e+00	 sigma_n : 8.838664e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 384

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716015e+00	 sigma_n : 9.092055e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 385

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516309e+00	 sigma_n : 8.256865e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 386

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805221e+00	 sigma_n : 8.778045e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 387

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655534e+00	 sigma_n : 8.782116e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 388

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.889101e+00	 sigma_n : 1.054002e-01
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 389

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503951e+00	 sigma_n : 8.396726e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 390

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723485e+00	 sigma_n : 8.612266e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 391

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800000e+00	 sigma_n : 8.908308e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 392

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703568e+00	 sigma_n : 8.902729e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 393

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543243e+00	 sigma_n : 9.508436e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 394

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655412e+00	 sigma_n : 9.176924e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 395

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.823923e+00	 sigma_n : 9.505550e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 396

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670898e+00	 sigma_n : 8.960578e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 397

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574839e+00	 sigma_n : 8.375839e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 398

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719669e+00	 sigma_n : 8.703875e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 399

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805171e+00	 sigma_n : 9.196161e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 400

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552920e+00	 sigma_n : 8.665078e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 401

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.817729e+00	 sigma_n : 8.970628e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 402

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.875589e+00	 sigma_n : 8.931487e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 403

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.428696e+00	 sigma_n : 7.816748e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 404

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634218e+00	 sigma_n : 9.245288e-02
	 number of secondary particules: 972
	 number of fission neutrons: 972

 batch number : 405

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.007202e+00	 sigma_n : 1.018624e-01
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 406

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760485e+00	 sigma_n : 8.721536e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 407

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520143e+00	 sigma_n : 7.972244e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 408

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748306e+00	 sigma_n : 8.879070e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 409

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636106e+00	 sigma_n : 8.716657e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 410

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757632e+00	 sigma_n : 9.090864e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 411

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692998e+00	 sigma_n : 8.827160e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 412

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503046e+00	 sigma_n : 8.046916e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 413

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741302e+00	 sigma_n : 9.030597e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 414

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688323e+00	 sigma_n : 9.079915e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 415

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550260e+00	 sigma_n : 8.246103e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 416

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710272e+00	 sigma_n : 9.024533e-02
	 number of secondary particules: 1187
	 number of fission neutrons: 1187

 batch number : 417

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.360573e+00	 sigma_n : 7.547631e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 418

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792671e+00	 sigma_n : 9.362110e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 419

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705775e+00	 sigma_n : 8.927820e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 420

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708566e+00	 sigma_n : 9.231943e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 421

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.554437e+00	 sigma_n : 8.663321e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 422

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822375e+00	 sigma_n : 9.068494e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 423

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737689e+00	 sigma_n : 8.794339e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 424

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743144e+00	 sigma_n : 9.155378e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 425

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.417476e+00	 sigma_n : 7.809223e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 426

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.915122e+00	 sigma_n : 9.644804e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 427

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595933e+00	 sigma_n : 8.653528e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 428

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574188e+00	 sigma_n : 9.038239e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 429

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.879507e+00	 sigma_n : 9.342773e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 430

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644702e+00	 sigma_n : 8.908347e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 431

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625427e+00	 sigma_n : 8.664238e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 432

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573516e+00	 sigma_n : 8.656087e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 433

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726236e+00	 sigma_n : 9.195534e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 434

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662362e+00	 sigma_n : 9.022333e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 435

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699454e+00	 sigma_n : 8.363264e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 436

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589065e+00	 sigma_n : 9.106367e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 437

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.447748e+00	 sigma_n : 8.118004e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 438

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756244e+00	 sigma_n : 9.017977e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 439

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807839e+00	 sigma_n : 9.125431e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 440

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632299e+00	 sigma_n : 8.633231e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 441

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674789e+00	 sigma_n : 8.997574e-02
	 number of secondary particules: 989
	 number of fission neutrons: 989

 batch number : 442

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.795753e+00	 sigma_n : 9.385184e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 443

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688172e+00	 sigma_n : 9.369137e-02
	 number of secondary particules: 972
	 number of fission neutrons: 972

 batch number : 444

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.052469e+00	 sigma_n : 1.031820e-01
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 445

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664557e+00	 sigma_n : 9.122493e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 446

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530088e+00	 sigma_n : 8.237767e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 447

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685740e+00	 sigma_n : 8.937099e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 448

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585321e+00	 sigma_n : 8.422547e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 449

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747093e+00	 sigma_n : 9.271926e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 450

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702439e+00	 sigma_n : 9.454563e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 451

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665695e+00	 sigma_n : 9.031834e-02
	 number of secondary particules: 997
	 number of fission neutrons: 997

 batch number : 452

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808425e+00	 sigma_n : 1.009536e-01
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 453

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804035e+00	 sigma_n : 9.467469e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 454

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583862e+00	 sigma_n : 8.359444e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 455

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804388e+00	 sigma_n : 9.794978e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 456

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500849e+00	 sigma_n : 8.454480e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 457

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650090e+00	 sigma_n : 8.332632e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 458

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530482e+00	 sigma_n : 8.632202e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 459

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777457e+00	 sigma_n : 9.169095e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 460

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722222e+00	 sigma_n : 9.318816e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 461

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553555e+00	 sigma_n : 8.940138e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 462

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736202e+00	 sigma_n : 9.469451e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 463

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726673e+00	 sigma_n : 9.035983e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 464

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718864e+00	 sigma_n : 9.039354e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 465

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516825e+00	 sigma_n : 8.428959e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 466

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704007e+00	 sigma_n : 9.419317e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 467

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540541e+00	 sigma_n : 8.581892e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 468

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518750e+00	 sigma_n : 8.323884e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 469

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779886e+00	 sigma_n : 9.221062e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 470

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522099e+00	 sigma_n : 8.336521e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 471

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790927e+00	 sigma_n : 9.279869e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 472

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693642e+00	 sigma_n : 8.793077e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 473

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659755e+00	 sigma_n : 8.222717e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 474

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611830e+00	 sigma_n : 8.418288e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 475

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637218e+00	 sigma_n : 8.895559e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 476

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641987e+00	 sigma_n : 8.574848e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 477

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688275e+00	 sigma_n : 8.372905e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 478

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625000e+00	 sigma_n : 8.527694e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 batch number : 479

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728444e+00	 sigma_n : 9.061682e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 480

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755703e+00	 sigma_n : 9.494146e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 481

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465789e+00	 sigma_n : 8.744863e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 482

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788746e+00	 sigma_n : 9.179764e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 483

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678538e+00	 sigma_n : 8.699794e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 484

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.817753e+00	 sigma_n : 9.601867e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 485

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511384e+00	 sigma_n : 8.271673e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 486

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.823062e+00	 sigma_n : 9.722267e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 487

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758389e+00	 sigma_n : 9.597656e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 488

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763431e+00	 sigma_n : 9.177017e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 489

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659152e+00	 sigma_n : 9.008183e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 490

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608059e+00	 sigma_n : 8.257868e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 491

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700193e+00	 sigma_n : 8.831606e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 492

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516569e+00	 sigma_n : 8.232939e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 493

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.043173e+00	 sigma_n : 1.021017e-01
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 494

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682796e+00	 sigma_n : 8.981477e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 495

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.496007e+00	 sigma_n : 7.894956e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 496

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648402e+00	 sigma_n : 9.050133e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 497

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728137e+00	 sigma_n : 9.103152e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 498

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698569e+00	 sigma_n : 8.810306e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 499

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595614e+00	 sigma_n : 9.222747e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 500

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623188e+00	 sigma_n : 8.751942e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 501

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618492e+00	 sigma_n : 8.654545e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 502

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607143e+00	 sigma_n : 8.771356e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 503

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709108e+00	 sigma_n : 8.827693e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 504

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.381834e+00	 sigma_n : 8.014000e-02
	 number of secondary particules: 998
	 number of fission neutrons: 998

 batch number : 505

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680361e+00	 sigma_n : 9.681863e-02
	 number of secondary particules: 973
	 number of fission neutrons: 973

 batch number : 506

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.908530e+00	 sigma_n : 1.010063e-01
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 507

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561022e+00	 sigma_n : 8.359621e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 508

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.848126e+00	 sigma_n : 9.319092e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 509

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538318e+00	 sigma_n : 8.194036e-02
	 number of secondary particules: 972
	 number of fission neutrons: 972

 batch number : 510

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.941358e+00	 sigma_n : 9.812580e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 511

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591894e+00	 sigma_n : 8.226024e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 512

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.894839e+00	 sigma_n : 9.529416e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 513

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512090e+00	 sigma_n : 8.203856e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 514

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638609e+00	 sigma_n : 8.794930e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 515

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685637e+00	 sigma_n : 8.928673e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 516

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696691e+00	 sigma_n : 9.375663e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 517

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.443299e+00	 sigma_n : 8.233607e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 518

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687262e+00	 sigma_n : 9.285072e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 519

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763134e+00	 sigma_n : 8.769075e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 520

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548187e+00	 sigma_n : 8.114944e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 521

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732291e+00	 sigma_n : 8.986432e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 522

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.517179e+00	 sigma_n : 8.439274e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 523

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780511e+00	 sigma_n : 9.287050e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 524

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639680e+00	 sigma_n : 8.865561e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 525

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522293e+00	 sigma_n : 8.372190e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 526

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750000e+00	 sigma_n : 8.615779e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 527

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598048e+00	 sigma_n : 8.309850e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 528

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673095e+00	 sigma_n : 8.780933e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 529

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660343e+00	 sigma_n : 9.396525e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 530

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.391530e+00	 sigma_n : 7.539891e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 531

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719198e+00	 sigma_n : 8.893157e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 532

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803157e+00	 sigma_n : 9.251325e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 533

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.396797e+00	 sigma_n : 7.775324e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 534

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579724e+00	 sigma_n : 8.445541e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 535

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761397e+00	 sigma_n : 8.867010e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 536

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732767e+00	 sigma_n : 8.890222e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 537



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.103659e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545619e+00	 sigma_n : 7.882056e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 538

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.880117e+00	 sigma_n : 9.186082e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 539

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589790e+00	 sigma_n : 9.010473e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 540

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728880e+00	 sigma_n : 9.047735e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 541

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752336e+00	 sigma_n : 8.970005e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 542

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727783e+00	 sigma_n : 9.447307e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 543

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611007e+00	 sigma_n : 8.934477e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 544

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774043e+00	 sigma_n : 9.300856e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 545

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.396825e+00	 sigma_n : 7.912234e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 546

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693898e+00	 sigma_n : 9.332583e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 547

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.837349e+00	 sigma_n : 9.216250e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 548

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735654e+00	 sigma_n : 8.878403e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 549

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699543e+00	 sigma_n : 8.939936e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 550

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555359e+00	 sigma_n : 8.536718e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 551

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555866e+00	 sigma_n : 8.671336e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 552

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.960159e+00	 sigma_n : 9.307877e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 553

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688277e+00	 sigma_n : 8.849145e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 554

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.414336e+00	 sigma_n : 8.334758e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 555

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694931e+00	 sigma_n : 8.938044e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 556

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607460e+00	 sigma_n : 8.841520e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 557

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791099e+00	 sigma_n : 9.229213e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 558

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561251e+00	 sigma_n : 8.618304e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 559

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614953e+00	 sigma_n : 8.765928e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 560

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750471e+00	 sigma_n : 8.670501e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 561

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772812e+00	 sigma_n : 9.012578e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 562

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564947e+00	 sigma_n : 8.382916e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 563

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.481449e+00	 sigma_n : 7.721151e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 564

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.840353e+00	 sigma_n : 9.469711e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 565

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637017e+00	 sigma_n : 8.193768e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 566

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464851e+00	 sigma_n : 7.866582e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 567

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741728e+00	 sigma_n : 9.358746e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 568

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683522e+00	 sigma_n : 9.367381e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 569

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616438e+00	 sigma_n : 8.509746e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 570

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619626e+00	 sigma_n : 8.265349e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 571

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700382e+00	 sigma_n : 9.272399e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 572

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712898e+00	 sigma_n : 8.732780e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 573

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.461993e+00	 sigma_n : 8.270297e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 574

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784741e+00	 sigma_n : 8.946664e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 575

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632007e+00	 sigma_n : 8.613478e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 576

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.474890e+00	 sigma_n : 8.296382e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 577

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730989e+00	 sigma_n : 8.370548e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 578

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527410e+00	 sigma_n : 8.622178e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 579

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805421e+00	 sigma_n : 9.154408e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 580

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807196e+00	 sigma_n : 9.325163e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 581

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639011e+00	 sigma_n : 9.029689e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 582

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548444e+00	 sigma_n : 8.910881e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 583

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.873120e+00	 sigma_n : 9.839365e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 584

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620750e+00	 sigma_n : 8.183090e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 585

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602954e+00	 sigma_n : 8.353949e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 586

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619982e+00	 sigma_n : 8.386317e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 587

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621080e+00	 sigma_n : 8.771999e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 588

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617208e+00	 sigma_n : 8.825156e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 589

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468354e+00	 sigma_n : 8.056952e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 590

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735654e+00	 sigma_n : 8.703069e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 591

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658943e+00	 sigma_n : 8.604870e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 592

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733833e+00	 sigma_n : 9.911776e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 593

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792523e+00	 sigma_n : 9.132551e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 594

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653226e+00	 sigma_n : 8.501154e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 595

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520797e+00	 sigma_n : 8.297174e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 596

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770258e+00	 sigma_n : 9.333620e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 597

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.451335e+00	 sigma_n : 8.826199e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 598

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778641e+00	 sigma_n : 8.866171e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 599

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625465e+00	 sigma_n : 9.043502e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 600

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591128e+00	 sigma_n : 8.241232e-02
	 number of secondary particules: 979
	 number of fission neutrons: 979

 batch number : 601

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.959142e+00	 sigma_n : 9.357812e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 602

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661724e+00	 sigma_n : 8.626343e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 603

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720862e+00	 sigma_n : 8.968976e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 604

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797348e+00	 sigma_n : 9.491521e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 605

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604499e+00	 sigma_n : 8.761402e-02
	 number of secondary particules: 971
	 number of fission neutrons: 971

 batch number : 606

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.050463e+00	 sigma_n : 1.017880e-01
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 607

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564655e+00	 sigma_n : 8.242133e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 608

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719298e+00	 sigma_n : 8.674099e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 609

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569873e+00	 sigma_n : 7.906206e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 610

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748357e+00	 sigma_n : 9.062520e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 611

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538603e+00	 sigma_n : 8.653641e-02
	 number of secondary particules: 999
	 number of fission neutrons: 999

 batch number : 612

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809810e+00	 sigma_n : 9.233322e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 613

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652964e+00	 sigma_n : 8.803270e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 614

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712535e+00	 sigma_n : 8.762513e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 615

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804267e+00	 sigma_n : 8.495658e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 616

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676698e+00	 sigma_n : 8.864156e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 617

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.453138e+00	 sigma_n : 8.160806e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 618

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696768e+00	 sigma_n : 9.589905e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 619

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654460e+00	 sigma_n : 8.313016e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 620

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703772e+00	 sigma_n : 8.306261e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 621

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740056e+00	 sigma_n : 9.229933e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 622

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560673e+00	 sigma_n : 8.304195e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 623

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.920422e+00	 sigma_n : 9.618381e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 624

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.265411e+00	 sigma_n : 7.592617e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 625

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705191e+00	 sigma_n : 8.997204e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 626

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706215e+00	 sigma_n : 8.746660e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 627

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.856338e+00	 sigma_n : 9.531648e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 628

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510490e+00	 sigma_n : 8.374243e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 629

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673561e+00	 sigma_n : 8.834571e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 630

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728844e+00	 sigma_n : 8.493550e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 631

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.455172e+00	 sigma_n : 8.061708e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 632

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792578e+00	 sigma_n : 9.636021e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 633

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733864e+00	 sigma_n : 8.823012e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 634

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600172e+00	 sigma_n : 8.813356e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 635

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515284e+00	 sigma_n : 7.845221e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 636

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586420e+00	 sigma_n : 8.359749e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 637

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556828e+00	 sigma_n : 8.192270e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 638

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.381786e+00	 sigma_n : 7.837277e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 639

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.838552e+00	 sigma_n : 9.864793e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 640

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814109e+00	 sigma_n : 9.251190e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 641

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579855e+00	 sigma_n : 8.396768e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 642

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702899e+00	 sigma_n : 9.073193e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 643

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708036e+00	 sigma_n : 8.511529e-02
	 number of secondary particules: 1194
	 number of fission neutrons: 1194

 batch number : 644

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535176e+00	 sigma_n : 8.493154e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 645

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723792e+00	 sigma_n : 9.081227e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 646

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671603e+00	 sigma_n : 8.562151e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 647

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553603e+00	 sigma_n : 8.343423e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 648

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672269e+00	 sigma_n : 8.426968e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 649

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660326e+00	 sigma_n : 8.606407e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 650

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641987e+00	 sigma_n : 8.679812e-02
	 number of secondary particules: 1008
	 number of fission neutrons: 1008

 batch number : 651

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731151e+00	 sigma_n : 8.780694e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 652

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566219e+00	 sigma_n : 8.144872e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 653

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709179e+00	 sigma_n : 8.730661e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 654

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611370e+00	 sigma_n : 8.205628e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 655

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773394e+00	 sigma_n : 9.249396e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 656

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546928e+00	 sigma_n : 8.201919e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 657

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649774e+00	 sigma_n : 8.581362e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 658

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566636e+00	 sigma_n : 8.358124e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 659

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693625e+00	 sigma_n : 8.508630e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 660

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752161e+00	 sigma_n : 9.375329e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 661

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819751e+00	 sigma_n : 9.275395e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 662

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733813e+00	 sigma_n : 8.812879e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 663

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.421603e+00	 sigma_n : 8.449091e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 664

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780039e+00	 sigma_n : 9.409811e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 665

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498688e+00	 sigma_n : 8.469713e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 666

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662050e+00	 sigma_n : 9.442678e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 667

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553832e+00	 sigma_n : 8.354633e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 668

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.908471e+00	 sigma_n : 9.417594e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 669

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597796e+00	 sigma_n : 8.867118e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 670

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808511e+00	 sigma_n : 9.477819e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 671

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533566e+00	 sigma_n : 7.852623e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 672

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659963e+00	 sigma_n : 8.539397e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 673

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464968e+00	 sigma_n : 8.411294e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 674

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739645e+00	 sigma_n : 9.002754e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 675

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.818094e+00	 sigma_n : 9.404513e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 676

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601266e+00	 sigma_n : 8.536152e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 677

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651636e+00	 sigma_n : 8.675383e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 678

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.439502e+00	 sigma_n : 7.892561e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 679

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746047e+00	 sigma_n : 9.080392e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 680

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534499e+00	 sigma_n : 7.741353e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 681

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626781e+00	 sigma_n : 8.708152e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 682

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569030e+00	 sigma_n : 7.934942e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 683

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642300e+00	 sigma_n : 9.200289e-02
	 number of secondary particules: 974
	 number of fission neutrons: 974

 batch number : 684

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822382e+00	 sigma_n : 9.275914e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 685

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544685e+00	 sigma_n : 8.908736e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 686

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.884347e+00	 sigma_n : 9.689985e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 687

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468388e+00	 sigma_n : 7.990863e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 688

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811284e+00	 sigma_n : 9.573097e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 689

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.869981e+00	 sigma_n : 8.700458e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 690

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505697e+00	 sigma_n : 7.827309e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 691

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725681e+00	 sigma_n : 8.614455e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 692

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682904e+00	 sigma_n : 8.295682e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 693

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688845e+00	 sigma_n : 8.676333e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 694

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731898e+00	 sigma_n : 8.811955e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 695

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528897e+00	 sigma_n : 8.991498e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 696

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683065e+00	 sigma_n : 8.494907e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 697

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647556e+00	 sigma_n : 8.773900e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 698

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698148e+00	 sigma_n : 9.262436e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 699

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726406e+00	 sigma_n : 8.903327e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 700

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758652e+00	 sigma_n : 9.050843e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 701

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709251e+00	 sigma_n : 9.393934e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 702

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642550e+00	 sigma_n : 8.458982e-02
	 number of secondary particules: 1208
	 number of fission neutrons: 1208

 batch number : 703

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490894e+00	 sigma_n : 8.333544e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 704

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544051e+00	 sigma_n : 8.912975e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 705

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740458e+00	 sigma_n : 8.770047e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 706

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791667e+00	 sigma_n : 8.968974e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 707

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683511e+00	 sigma_n : 8.486658e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 708

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702165e+00	 sigma_n : 8.573630e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 709

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.429553e+00	 sigma_n : 8.095159e-02
	 number of secondary particules: 998
	 number of fission neutrons: 998

 batch number : 710

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.895792e+00	 sigma_n : 9.682968e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 711

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750951e+00	 sigma_n : 8.871948e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 712

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548187e+00	 sigma_n : 8.529570e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 713

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751671e+00	 sigma_n : 9.269207e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 714

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642922e+00	 sigma_n : 9.012445e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 715

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604108e+00	 sigma_n : 8.396975e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 716

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.837573e+00	 sigma_n : 9.200612e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 717

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763981e+00	 sigma_n : 9.314881e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 718

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524680e+00	 sigma_n : 8.160468e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 719

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709091e+00	 sigma_n : 8.926691e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 720

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726750e+00	 sigma_n : 8.656045e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 721

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839810e+00	 sigma_n : 9.557758e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 722

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647654e+00	 sigma_n : 8.354785e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 723

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702403e+00	 sigma_n : 8.807995e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 724

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753559e+00	 sigma_n : 9.368543e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 725

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645447e+00	 sigma_n : 8.339723e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 726

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608924e+00	 sigma_n : 8.695740e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 727

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.482823e+00	 sigma_n : 8.404145e-02
	 number of secondary particules: 998
	 number of fission neutrons: 998

 batch number : 728

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809619e+00	 sigma_n : 1.007099e-01
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 729

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607843e+00	 sigma_n : 9.176164e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 730

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598353e+00	 sigma_n : 9.079187e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 731

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626617e+00	 sigma_n : 9.358158e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 732

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639252e+00	 sigma_n : 8.617764e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 733

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788911e+00	 sigma_n : 9.272440e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 734

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596700e+00	 sigma_n : 8.133294e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 735

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669716e+00	 sigma_n : 9.357794e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 736

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775201e+00	 sigma_n : 8.893006e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 737

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.421995e+00	 sigma_n : 8.008031e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 738

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634259e+00	 sigma_n : 8.431627e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 739

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617225e+00	 sigma_n : 8.816827e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 740

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572541e+00	 sigma_n : 8.432939e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 741

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.967480e+00	 sigma_n : 1.010605e-01
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 742

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634428e+00	 sigma_n : 9.305839e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 743

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607111e+00	 sigma_n : 8.479661e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 744

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542831e+00	 sigma_n : 7.884765e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 745

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803419e+00	 sigma_n : 9.589288e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 746

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671546e+00	 sigma_n : 8.950189e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 747

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680458e+00	 sigma_n : 8.331061e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 748

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610727e+00	 sigma_n : 8.425727e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 749

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749314e+00	 sigma_n : 9.230482e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 750

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796972e+00	 sigma_n : 8.667429e-02
	 number of secondary particules: 1245
	 number of fission neutrons: 1245

 batch number : 751

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.359036e+00	 sigma_n : 7.754227e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 752

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646083e+00	 sigma_n : 8.376308e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 753

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605634e+00	 sigma_n : 8.578174e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 754

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695522e+00	 sigma_n : 8.881263e-02
	 number of secondary particules: 997
	 number of fission neutrons: 997

 batch number : 755

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747242e+00	 sigma_n : 9.305274e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 756

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730203e+00	 sigma_n : 9.135540e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 757

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754751e+00	 sigma_n : 8.797893e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 758

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648789e+00	 sigma_n : 8.989363e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 759

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498699e+00	 sigma_n : 8.988019e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 760

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613924e+00	 sigma_n : 8.612014e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 761

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729345e+00	 sigma_n : 8.841653e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 762

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782690e+00	 sigma_n : 8.709216e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 763

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784091e+00	 sigma_n : 8.774124e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 764

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728417e+00	 sigma_n : 9.072995e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 765

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465816e+00	 sigma_n : 7.963618e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 766

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771564e+00	 sigma_n : 9.157003e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 767

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678839e+00	 sigma_n : 8.628872e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 768

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531634e+00	 sigma_n : 7.812030e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 769

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670330e+00	 sigma_n : 9.309427e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 770

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.892644e+00	 sigma_n : 9.125001e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 771

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.485816e+00	 sigma_n : 7.925779e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 772

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684110e+00	 sigma_n : 8.921308e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 773

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669202e+00	 sigma_n : 9.136194e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 774

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819963e+00	 sigma_n : 9.204086e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 775

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587374e+00	 sigma_n : 8.432441e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 776

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.881308e+00	 sigma_n : 8.982937e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 777

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690647e+00	 sigma_n : 8.608621e-02
	 number of secondary particules: 1209
	 number of fission neutrons: 1209

 batch number : 778

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.338296e+00	 sigma_n : 7.358753e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 779

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645833e+00	 sigma_n : 8.763792e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 780

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634146e+00	 sigma_n : 8.974398e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 781

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692235e+00	 sigma_n : 8.256672e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 782

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763889e+00	 sigma_n : 9.027466e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 783

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646182e+00	 sigma_n : 8.865502e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 784

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627181e+00	 sigma_n : 8.615501e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 785

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688951e+00	 sigma_n : 8.494970e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 786

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658168e+00	 sigma_n : 8.727544e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 787

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790170e+00	 sigma_n : 8.731272e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 788

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619796e+00	 sigma_n : 8.436120e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 789

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777256e+00	 sigma_n : 9.106863e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 790

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640429e+00	 sigma_n : 8.492851e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 791

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651037e+00	 sigma_n : 8.677228e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 792

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565178e+00	 sigma_n : 8.893492e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 793

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697585e+00	 sigma_n : 8.720423e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 794

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622605e+00	 sigma_n : 8.580683e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 795

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778530e+00	 sigma_n : 9.468650e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 796

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658310e+00	 sigma_n : 8.679597e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 797

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819734e+00	 sigma_n : 9.195042e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 798

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595260e+00	 sigma_n : 9.160102e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 799

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745205e+00	 sigma_n : 9.345226e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 800

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590622e+00	 sigma_n : 8.795621e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 801

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642921e+00	 sigma_n : 8.824463e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 802

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673469e+00	 sigma_n : 8.825524e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 803

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573859e+00	 sigma_n : 8.418766e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 804

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589862e+00	 sigma_n : 8.105160e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 805

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687161e+00	 sigma_n : 8.866502e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 806

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670992e+00	 sigma_n : 8.990724e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 807

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822057e+00	 sigma_n : 9.318307e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 808

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653262e+00	 sigma_n : 8.743226e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 809

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536477e+00	 sigma_n : 8.433440e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 810

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793404e+00	 sigma_n : 9.267726e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 811

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698864e+00	 sigma_n : 8.951093e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 812

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633364e+00	 sigma_n : 8.513566e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 813

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790066e+00	 sigma_n : 9.704065e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 814

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616487e+00	 sigma_n : 9.001207e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 815

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566636e+00	 sigma_n : 8.598075e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 816

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.815939e+00	 sigma_n : 9.567002e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 817

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646679e+00	 sigma_n : 8.208249e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 818

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584310e+00	 sigma_n : 8.207492e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 819

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642659e+00	 sigma_n : 8.053770e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 820

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787274e+00	 sigma_n : 9.576119e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 821

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647913e+00	 sigma_n : 8.911487e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 822

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556452e+00	 sigma_n : 8.501459e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 823

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715377e+00	 sigma_n : 9.242447e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 824

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716432e+00	 sigma_n : 9.221699e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 825

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688220e+00	 sigma_n : 8.864091e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 826

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737168e+00	 sigma_n : 8.864509e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 827

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617699e+00	 sigma_n : 8.552130e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 828

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541998e+00	 sigma_n : 8.445972e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 829

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.901501e+00	 sigma_n : 8.958214e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 830

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.355631e+00	 sigma_n : 7.621364e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 831

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661654e+00	 sigma_n : 8.668140e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 832

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708178e+00	 sigma_n : 8.737336e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 833

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733514e+00	 sigma_n : 8.440463e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 834

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522071e+00	 sigma_n : 7.908551e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 835

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542656e+00	 sigma_n : 8.261727e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 836

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604356e+00	 sigma_n : 8.467645e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 837

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557392e+00	 sigma_n : 8.349858e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 838

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651803e+00	 sigma_n : 8.503422e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 839

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738028e+00	 sigma_n : 8.524275e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 840

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600370e+00	 sigma_n : 8.464817e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 841

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581699e+00	 sigma_n : 8.720415e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 842

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611926e+00	 sigma_n : 8.297951e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 843

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.877228e+00	 sigma_n : 9.307734e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 844

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771041e+00	 sigma_n : 8.923955e-02
	 number of secondary particules: 1167
	 number of fission neutrons: 1167

 batch number : 845

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522708e+00	 sigma_n : 7.837838e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 846

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.826606e+00	 sigma_n : 9.434802e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 847

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468031e+00	 sigma_n : 8.240789e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 848

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743542e+00	 sigma_n : 9.256401e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 849

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546889e+00	 sigma_n : 9.023353e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 850

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715179e+00	 sigma_n : 8.493048e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 851

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660517e+00	 sigma_n : 8.843370e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 852

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757986e+00	 sigma_n : 8.810631e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 853

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633333e+00	 sigma_n : 8.283913e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 854

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777277e+00	 sigma_n : 9.237810e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 855

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741039e+00	 sigma_n : 9.235774e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 856

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563368e+00	 sigma_n : 8.879855e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 857

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594348e+00	 sigma_n : 8.648310e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 858

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719927e+00	 sigma_n : 8.481693e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 859

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644954e+00	 sigma_n : 8.643224e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 860

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756604e+00	 sigma_n : 8.783917e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 861

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597109e+00	 sigma_n : 8.702472e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 862

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740845e+00	 sigma_n : 9.004841e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 863

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.899705e+00	 sigma_n : 1.054596e-01
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 864

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811215e+00	 sigma_n : 9.100869e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 865

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545775e+00	 sigma_n : 8.527327e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 866

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774888e+00	 sigma_n : 9.030990e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 867

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502168e+00	 sigma_n : 8.405407e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 868

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709677e+00	 sigma_n : 8.784355e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 869

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722791e+00	 sigma_n : 8.858152e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 870

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578512e+00	 sigma_n : 8.206547e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 871

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731618e+00	 sigma_n : 9.034750e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 872

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720803e+00	 sigma_n : 8.647576e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 873

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728584e+00	 sigma_n : 9.375673e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 874

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527463e+00	 sigma_n : 8.811530e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 875

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703985e+00	 sigma_n : 8.579600e-02
	 number of secondary particules: 1002
	 number of fission neutrons: 1002

 batch number : 876

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698603e+00	 sigma_n : 9.297863e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 877

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664717e+00	 sigma_n : 9.227605e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 878

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620921e+00	 sigma_n : 8.855962e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 879

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503250e+00	 sigma_n : 8.003551e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 880

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694818e+00	 sigma_n : 9.152714e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 881

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643206e+00	 sigma_n : 8.983071e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 882

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585868e+00	 sigma_n : 8.858990e-02
	 number of secondary particules: 988
	 number of fission neutrons: 988

 batch number : 883

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.866397e+00	 sigma_n : 9.639084e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 884

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633459e+00	 sigma_n : 8.976239e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 885

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463661e+00	 sigma_n : 7.548469e-02
	 number of secondary particules: 999
	 number of fission neutrons: 999

 batch number : 886

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656657e+00	 sigma_n : 8.497577e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 887

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719281e+00	 sigma_n : 8.944338e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 888

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775510e+00	 sigma_n : 9.005705e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 889

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803468e+00	 sigma_n : 9.076586e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 890

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580586e+00	 sigma_n : 8.277999e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 891

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.837761e+00	 sigma_n : 1.057824e-01
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 892

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788462e+00	 sigma_n : 9.060428e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174

 batch number : 893

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.399489e+00	 sigma_n : 7.908795e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 894

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824022e+00	 sigma_n : 9.320791e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 895

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687217e+00	 sigma_n : 8.881061e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 896

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628647e+00	 sigma_n : 8.244991e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 897

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.454308e+00	 sigma_n : 7.829946e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 898

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770476e+00	 sigma_n : 8.692070e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 899

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539872e+00	 sigma_n : 7.969564e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 900

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655204e+00	 sigma_n : 8.732740e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 901

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699711e+00	 sigma_n : 8.950725e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 902

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.877456e+00	 sigma_n : 9.536430e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 903

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600862e+00	 sigma_n : 8.488012e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 904

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645890e+00	 sigma_n : 8.600928e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174

 batch number : 905

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574957e+00	 sigma_n : 8.201448e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 906

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525674e+00	 sigma_n : 8.574744e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 907

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.430368e+00	 sigma_n : 8.040225e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 908

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641527e+00	 sigma_n : 8.523898e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 909

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579943e+00	 sigma_n : 8.625038e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 910

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819265e+00	 sigma_n : 9.953837e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 911

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662617e+00	 sigma_n : 9.872820e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 912

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463927e+00	 sigma_n : 8.276727e-02
	 number of secondary particules: 997
	 number of fission neutrons: 997

 batch number : 913

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.806419e+00	 sigma_n : 9.524194e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 914

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.858902e+00	 sigma_n : 9.486481e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 915

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666667e+00	 sigma_n : 8.588544e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 916

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741395e+00	 sigma_n : 9.414324e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 917

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610357e+00	 sigma_n : 8.394403e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 918

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.343776e+00	 sigma_n : 7.854039e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 919

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714147e+00	 sigma_n : 8.851711e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 920

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505736e+00	 sigma_n : 7.847491e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 921

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.867000e+00	 sigma_n : 9.392621e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 922

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590950e+00	 sigma_n : 8.574504e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 923

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621212e+00	 sigma_n : 7.948431e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 924

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696069e+00	 sigma_n : 8.837784e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 925

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710983e+00	 sigma_n : 8.937023e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 926

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679846e+00	 sigma_n : 8.771438e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 927

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622326e+00	 sigma_n : 8.593760e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 928

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833333e+00	 sigma_n : 9.432504e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 929

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604310e+00	 sigma_n : 8.920064e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 930

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677029e+00	 sigma_n : 9.285232e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 931

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.300778e+00	 sigma_n : 7.487996e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 932

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798411e+00	 sigma_n : 9.393087e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 933

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740385e+00	 sigma_n : 8.427208e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 934

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788626e+00	 sigma_n : 9.847833e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 935

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545130e+00	 sigma_n : 7.721791e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 936

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650926e+00	 sigma_n : 8.701525e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 937

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574040e+00	 sigma_n : 8.611562e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 938

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585086e+00	 sigma_n : 8.456025e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 939

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758049e+00	 sigma_n : 9.115826e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 940

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797742e+00	 sigma_n : 9.127722e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 941

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530488e+00	 sigma_n : 8.051427e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 942

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642664e+00	 sigma_n : 8.678990e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 943

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649550e+00	 sigma_n : 8.328523e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 944

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620412e+00	 sigma_n : 8.757784e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 945

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618018e+00	 sigma_n : 8.854872e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 946

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731773e+00	 sigma_n : 9.215930e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 947

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.434858e+00	 sigma_n : 7.888980e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 948

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610902e+00	 sigma_n : 8.839198e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 949

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.829389e+00	 sigma_n : 9.338332e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 950

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592697e+00	 sigma_n : 8.764579e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 951

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812261e+00	 sigma_n : 9.618147e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 952

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628182e+00	 sigma_n : 8.949693e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 953

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.881448e+00	 sigma_n : 9.145517e-02
	 number of secondary particules: 1226
	 number of fission neutrons: 1226

 batch number : 954

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513866e+00	 sigma_n : 8.073086e-02
	 number of secondary particules: 1191
	 number of fission neutrons: 1191

 batch number : 955

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492863e+00	 sigma_n : 7.703929e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 956

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658036e+00	 sigma_n : 8.374735e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 957

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522928e+00	 sigma_n : 7.960032e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 958

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601762e+00	 sigma_n : 9.102392e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 959

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706157e+00	 sigma_n : 8.236318e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 960

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671815e+00	 sigma_n : 8.873263e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 961

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752354e+00	 sigma_n : 8.953006e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 962

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607335e+00	 sigma_n : 8.501882e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 963

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617342e+00	 sigma_n : 8.612736e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 964

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592081e+00	 sigma_n : 8.418235e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 965

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603039e+00	 sigma_n : 8.417040e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 966

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606481e+00	 sigma_n : 8.540447e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 967

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613936e+00	 sigma_n : 8.820104e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 968

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692829e+00	 sigma_n : 8.571726e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 969

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646952e+00	 sigma_n : 8.816144e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 970

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711009e+00	 sigma_n : 8.728755e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 971

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544292e+00	 sigma_n : 8.126742e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 972

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749260e+00	 sigma_n : 9.542149e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 973

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794600e+00	 sigma_n : 9.462401e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 974

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599432e+00	 sigma_n : 8.840769e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 975

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772772e+00	 sigma_n : 9.452612e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 976

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714958e+00	 sigma_n : 8.733506e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 977

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640294e+00	 sigma_n : 9.211390e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 978

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497227e+00	 sigma_n : 8.314834e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 979

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778316e+00	 sigma_n : 9.227049e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 980

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710843e+00	 sigma_n : 9.028693e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 981

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.879201e+00	 sigma_n : 9.873669e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 982

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553712e+00	 sigma_n : 8.274752e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 983

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600913e+00	 sigma_n : 8.201892e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 984

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639815e+00	 sigma_n : 8.752406e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 985

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684161e+00	 sigma_n : 9.086256e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 986

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728814e+00	 sigma_n : 8.967877e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 987

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770659e+00	 sigma_n : 1.057371e-01
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 988

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744374e+00	 sigma_n : 8.641661e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 989

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591659e+00	 sigma_n : 8.580812e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 990

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573828e+00	 sigma_n : 8.169940e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 991

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733971e+00	 sigma_n : 8.742260e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 992

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704397e+00	 sigma_n : 9.807942e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 993

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.508870e+00	 sigma_n : 8.206469e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 994

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728261e+00	 sigma_n : 8.854883e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 995

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538679e+00	 sigma_n : 7.893029e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 996

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767000e+00	 sigma_n : 8.816169e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 997

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615385e+00	 sigma_n : 8.733244e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 998

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733886e+00	 sigma_n : 9.151385e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 999

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.908672e+00	 sigma_n : 9.765664e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1000

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.421970e+00	 sigma_n : 7.908763e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1001

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750916e+00	 sigma_n : 8.850534e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1002

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551724e+00	 sigma_n : 8.339805e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 1003

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.423439e+00	 sigma_n : 8.494156e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1004

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797688e+00	 sigma_n : 9.123347e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1005

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.483784e+00	 sigma_n : 7.952576e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1006

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619732e+00	 sigma_n : 9.052910e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 1007

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688000e+00	 sigma_n : 8.708754e-02
	 number of secondary particules: 986
	 number of fission neutrons: 986

 batch number : 1008

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750507e+00	 sigma_n : 9.345629e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 1009

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715139e+00	 sigma_n : 9.155194e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1010

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707897e+00	 sigma_n : 8.588121e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1011

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752558e+00	 sigma_n : 9.052932e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1012

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648313e+00	 sigma_n : 8.570506e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1013

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.355343e+00	 sigma_n : 7.544258e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 1014

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642857e+00	 sigma_n : 8.957627e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 1015

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769153e+00	 sigma_n : 9.394432e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1016

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745698e+00	 sigma_n : 9.699840e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1017

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710945e+00	 sigma_n : 8.811150e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1018

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502747e+00	 sigma_n : 8.140520e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1019

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799410e+00	 sigma_n : 9.001923e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1020

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808552e+00	 sigma_n : 9.281822e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1021

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608813e+00	 sigma_n : 8.229456e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1022

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510483e+00	 sigma_n : 7.988208e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1023

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755471e+00	 sigma_n : 9.673271e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1024

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634508e+00	 sigma_n : 8.559440e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1025

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699543e+00	 sigma_n : 9.081677e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1026

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568079e+00	 sigma_n : 8.469418e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1027

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.907649e+00	 sigma_n : 9.491812e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 1028

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489673e+00	 sigma_n : 8.043546e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1029

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862264e+00	 sigma_n : 9.732050e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1030

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530950e+00	 sigma_n : 8.451829e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1031

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.495396e+00	 sigma_n : 9.585036e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1032

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763957e+00	 sigma_n : 9.410274e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1033

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745506e+00	 sigma_n : 9.382766e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1034

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618605e+00	 sigma_n : 8.549787e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1035

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813155e+00	 sigma_n : 9.017482e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1036

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640909e+00	 sigma_n : 9.055467e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1037

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541779e+00	 sigma_n : 8.357283e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 1038

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707799e+00	 sigma_n : 8.795953e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1039

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757310e+00	 sigma_n : 9.909288e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1040

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791825e+00	 sigma_n : 9.444093e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1041

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675070e+00	 sigma_n : 8.857589e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1042

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708295e+00	 sigma_n : 8.857170e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1043

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559322e+00	 sigma_n : 8.298589e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1044

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645508e+00	 sigma_n : 8.826038e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1045

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701273e+00	 sigma_n : 8.375747e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1046

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704356e+00	 sigma_n : 9.049098e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1047

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541850e+00	 sigma_n : 8.759531e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1048

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785392e+00	 sigma_n : 9.067507e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1049

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539654e+00	 sigma_n : 8.315917e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 Type and parameters of random generator before batch 1050 : 
	 DRAND48_RANDOM 8712 49160 10431  COUNTER	41664023


 batch number : 1050

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594701e+00	 sigma_n : 8.398925e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 KEFF at step  : 1050
 keff = 9.972318e-01 sigma : 1.310841e-03
 number of batch used: 950


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.256637e+01
*********************************************************


 Mean weight leakage = 5.733807e+02	 sigma = 4.886413e-01	 sigma% = 8.522110e-02


 Edition after batch number : 1050

******************************************************************************
RESPONSE FUNCTION : PRODUCTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	1.253158e+01	1.314480e-01


******************************************************************************
RESPONSE FUNCTION : ABSORPTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	5.386599e+00	1.089488e-01


******************************************************************************
RESPONSE FUNCTION : LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	7.208789e+00	8.478926e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE_INSIDE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : NXN EXCESS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	3.296462e-02	1.675216e+00


******************************************************************************
RESPONSE FUNCTION : FLUX TOTAL
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	8.508953e+01	8.904580e-02


******************************************************************************
RESPONSE FUNCTION : ENERGY LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : KEFFS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950

 KSTEP  9.972318e-01	1.314480e-01
 KCOLL  9.968199e-01	1.025910e-01
 KTRACK 9.951222e-01	9.013526e-02

  	  estimators  			  correlations   	  combined values  	  combined sigma%
  	  KSTEP <-> KCOLL  	    	  8.027361e-01  	  9.967995e-01  	  1.025195e-01
  	  KSTEP <-> KTRACK  	    	  6.469295e-01  	  9.952147e-01  	  9.001908e-02
  	  KCOLL <-> KTRACK  	    	  7.903519e-01  	  9.954596e-01  	  8.921498e-02

  	  full combined estimator  9.954612e-01	8.917943e-02



	  KSTEP ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.971058e-01	 sigma = 1.294098e-03	 sigma% = 1.297854e-01


	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.967445e-01	 sigma = 1.010942e-03	 sigma% = 1.014244e-01


	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.950699e-01	 sigma = 8.897736e-04	 sigma% = 8.941820e-02


	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.966720e-01	 sigma = 1.010291e-03	 sigma% = 1.013665e-01


 simulation time (s) : 0


 batch number : 1051

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618677e+00	 sigma_n : 8.689926e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 1052

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.806452e+00	 sigma_n : 9.315436e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 1053

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.936064e+00	 sigma_n : 9.227889e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1054

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670968e+00	 sigma_n : 8.757146e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1055

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536473e+00	 sigma_n : 8.276699e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 1056

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707722e+00	 sigma_n : 8.973930e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1057

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.499537e+00	 sigma_n : 8.257801e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1058

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654064e+00	 sigma_n : 8.648936e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1059

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600909e+00	 sigma_n : 8.132719e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1060

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700185e+00	 sigma_n : 8.490782e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1061

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592328e+00	 sigma_n : 8.470696e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1062

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670653e+00	 sigma_n : 8.766457e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1063

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674956e+00	 sigma_n : 8.610160e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1064

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620690e+00	 sigma_n : 9.327972e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1065

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761948e+00	 sigma_n : 8.875300e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1066

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.495163e+00	 sigma_n : 8.134254e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1067

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640741e+00	 sigma_n : 9.100279e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1068

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647727e+00	 sigma_n : 8.835384e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1069

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716636e+00	 sigma_n : 9.158727e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1070

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620072e+00	 sigma_n : 8.854053e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1071

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627660e+00	 sigma_n : 8.678037e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1072

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656637e+00	 sigma_n : 8.394839e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1073

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665154e+00	 sigma_n : 8.896701e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1074

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589767e+00	 sigma_n : 8.900436e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 1075

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722167e+00	 sigma_n : 9.249723e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1076

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862959e+00	 sigma_n : 9.269853e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1077

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751812e+00	 sigma_n : 9.234427e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1078

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648815e+00	 sigma_n : 9.212001e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1079

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.480000e+00	 sigma_n : 8.441272e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1080

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812731e+00	 sigma_n : 9.304258e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1081

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810345e+00	 sigma_n : 8.961278e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1082

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627281e+00	 sigma_n : 9.429423e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1083

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.472420e+00	 sigma_n : 8.094379e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1084

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753283e+00	 sigma_n : 9.647265e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1085

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725365e+00	 sigma_n : 9.132969e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1086

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661157e+00	 sigma_n : 9.203462e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1087

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756957e+00	 sigma_n : 9.162272e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1088

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512620e+00	 sigma_n : 8.491485e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1089

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750469e+00	 sigma_n : 8.856840e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1090

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522847e+00	 sigma_n : 8.198908e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1091

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656100e+00	 sigma_n : 9.190668e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1092

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721018e+00	 sigma_n : 8.937381e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1093

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717172e+00	 sigma_n : 8.674203e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1094

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775322e+00	 sigma_n : 9.170416e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1095

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590090e+00	 sigma_n : 8.382877e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1096

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800000e+00	 sigma_n : 9.534168e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1097

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803017e+00	 sigma_n : 8.663327e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 1098

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594502e+00	 sigma_n : 8.939625e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1099

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751337e+00	 sigma_n : 8.652175e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.496090e+00	 sigma_n : 8.263103e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1101

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723783e+00	 sigma_n : 8.711197e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1102

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753165e+00	 sigma_n : 9.128350e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 1103

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500000e+00	 sigma_n : 8.631562e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1104

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653005e+00	 sigma_n : 8.934403e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1105

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.899057e+00	 sigma_n : 9.543633e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1106

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600177e+00	 sigma_n : 8.533184e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1107

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567343e+00	 sigma_n : 8.058700e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1108

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.886792e+00	 sigma_n : 9.058133e-02
	 number of secondary particules: 1214
	 number of fission neutrons: 1214

 batch number : 1109

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.485173e+00	 sigma_n : 8.260888e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1110

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722222e+00	 sigma_n : 8.774264e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 1111

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.474182e+00	 sigma_n : 8.194800e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1112

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801512e+00	 sigma_n : 9.032747e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1113

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645796e+00	 sigma_n : 8.824073e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1114

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504333e+00	 sigma_n : 8.339853e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1115

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674978e+00	 sigma_n : 8.960371e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1116

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785259e+00	 sigma_n : 8.815346e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1117

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692576e+00	 sigma_n : 8.793090e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 1118

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549479e+00	 sigma_n : 8.275748e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1119

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543937e+00	 sigma_n : 7.966749e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1120

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570209e+00	 sigma_n : 8.008548e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 batch number : 1121

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846383e+00	 sigma_n : 9.763427e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 1122

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724976e+00	 sigma_n : 9.400172e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1123

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647273e+00	 sigma_n : 8.838185e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1124

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677180e+00	 sigma_n : 8.898708e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1125

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697321e+00	 sigma_n : 8.823087e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1126

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619048e+00	 sigma_n : 8.022621e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1127

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549123e+00	 sigma_n : 7.961451e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1128

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608531e+00	 sigma_n : 9.178278e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 1129

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810651e+00	 sigma_n : 9.419381e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1130

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736842e+00	 sigma_n : 9.819090e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1131

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680000e+00	 sigma_n : 9.234678e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1132

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652462e+00	 sigma_n : 8.746808e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1133

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684557e+00	 sigma_n : 8.183123e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1134

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701657e+00	 sigma_n : 8.664179e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1135

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599474e+00	 sigma_n : 8.960605e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1136

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525135e+00	 sigma_n : 8.085515e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1137

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675024e+00	 sigma_n : 8.546650e-02
	 number of secondary particules: 999
	 number of fission neutrons: 999

 batch number : 1138

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756757e+00	 sigma_n : 9.297207e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1139

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728697e+00	 sigma_n : 9.536839e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1140

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566020e+00	 sigma_n : 8.210819e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1141

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660305e+00	 sigma_n : 8.810308e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1142

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672053e+00	 sigma_n : 9.267400e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1143

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686408e+00	 sigma_n : 8.668250e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1144

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705598e+00	 sigma_n : 8.368488e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1145

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658649e+00	 sigma_n : 9.079806e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1146

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632184e+00	 sigma_n : 8.190502e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1147

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570736e+00	 sigma_n : 8.041766e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1148

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683333e+00	 sigma_n : 8.586263e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1149

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619224e+00	 sigma_n : 8.514299e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1150

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729205e+00	 sigma_n : 8.981722e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1151

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684022e+00	 sigma_n : 8.814254e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1152

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502203e+00	 sigma_n : 8.099591e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1153

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698529e+00	 sigma_n : 8.768538e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1154

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591195e+00	 sigma_n : 8.469971e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1155

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713472e+00	 sigma_n : 8.902152e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1156

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489150e+00	 sigma_n : 7.991167e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1157

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619048e+00	 sigma_n : 8.256774e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1158

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713737e+00	 sigma_n : 9.072223e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1159

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.855100e+00	 sigma_n : 8.925519e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1160

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665121e+00	 sigma_n : 8.624657e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1161

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696249e+00	 sigma_n : 9.460811e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1162

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648826e+00	 sigma_n : 9.415037e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1163

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750962e+00	 sigma_n : 9.407219e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1164

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727962e+00	 sigma_n : 9.116144e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1165

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493542e+00	 sigma_n : 8.172513e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1166

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551040e+00	 sigma_n : 7.903619e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1167

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668959e+00	 sigma_n : 8.971762e-02
	 number of secondary particules: 979
	 number of fission neutrons: 979

 batch number : 1168

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.853933e+00	 sigma_n : 9.686722e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1169

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693625e+00	 sigma_n : 9.317884e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1170

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691406e+00	 sigma_n : 8.735896e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1171

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.850050e+00	 sigma_n : 9.866807e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1172

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559701e+00	 sigma_n : 8.182069e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 1173

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704724e+00	 sigma_n : 9.174141e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1174

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.820320e+00	 sigma_n : 8.932098e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 1175

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603969e+00	 sigma_n : 8.393438e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1176

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754190e+00	 sigma_n : 8.751997e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1177

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562044e+00	 sigma_n : 7.941990e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1178

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789279e+00	 sigma_n : 9.549341e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 1179

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473459e+00	 sigma_n : 8.233923e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1180

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.909935e+00	 sigma_n : 1.005325e-01
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1181

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.391187e+00	 sigma_n : 7.861228e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 1182

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774096e+00	 sigma_n : 9.604693e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1183

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680344e+00	 sigma_n : 9.425445e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1184

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747655e+00	 sigma_n : 9.360418e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1185

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741121e+00	 sigma_n : 9.206608e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1186

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774429e+00	 sigma_n : 1.010628e-01
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 1187

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520922e+00	 sigma_n : 8.071660e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 1188

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807826e+00	 sigma_n : 8.979625e-02
	 number of secondary particules: 1177
	 number of fission neutrons: 1177

 batch number : 1189

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553101e+00	 sigma_n : 7.899286e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1190

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.624667e+00	 sigma_n : 8.958453e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1191

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638640e+00	 sigma_n : 8.831454e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 1192

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.452031e+00	 sigma_n : 7.880717e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1193

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750469e+00	 sigma_n : 8.947868e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1194

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768802e+00	 sigma_n : 8.561061e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1195

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590710e+00	 sigma_n : 8.149067e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1196

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490958e+00	 sigma_n : 8.076740e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1197

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633962e+00	 sigma_n : 8.909173e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1198

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613592e+00	 sigma_n : 8.528064e-02
	 number of secondary particules: 982
	 number of fission neutrons: 982

 batch number : 1199

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768839e+00	 sigma_n : 8.705362e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 1200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839482e+00	 sigma_n : 9.898539e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1201

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730159e+00	 sigma_n : 8.818140e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1202

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.446942e+00	 sigma_n : 8.283394e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1203

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796053e+00	 sigma_n : 9.330585e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1204

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.482543e+00	 sigma_n : 7.331759e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1205

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668503e+00	 sigma_n : 8.758657e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1206

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719697e+00	 sigma_n : 8.793671e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1207

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796053e+00	 sigma_n : 9.069181e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1208

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541187e+00	 sigma_n : 8.637100e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1209

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559434e+00	 sigma_n : 8.493135e-02
	 number of secondary particules: 997
	 number of fission neutrons: 997

 batch number : 1210

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.936810e+00	 sigma_n : 9.653048e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1211

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.480663e+00	 sigma_n : 7.579412e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1212

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769613e+00	 sigma_n : 9.243974e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1213

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552408e+00	 sigma_n : 8.821927e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 1214

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774481e+00	 sigma_n : 9.206335e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1215

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687016e+00	 sigma_n : 8.817259e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1216

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730656e+00	 sigma_n : 8.844719e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1217

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758396e+00	 sigma_n : 8.722179e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1218

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647664e+00	 sigma_n : 8.551271e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1219

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747317e+00	 sigma_n : 9.397613e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1220

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626054e+00	 sigma_n : 8.588452e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 1221

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.908092e+00	 sigma_n : 1.008631e-01
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1222

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647378e+00	 sigma_n : 8.944015e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1223

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772140e+00	 sigma_n : 9.679260e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1224

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515500e+00	 sigma_n : 7.930748e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1225

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.930684e+00	 sigma_n : 9.385821e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1226

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661348e+00	 sigma_n : 9.120448e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 1227

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555363e+00	 sigma_n : 8.325858e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1228

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543221e+00	 sigma_n : 8.341693e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1229

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703670e+00	 sigma_n : 8.316211e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1230

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625659e+00	 sigma_n : 8.638915e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1231

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.409362e+00	 sigma_n : 7.825759e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1232

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751423e+00	 sigma_n : 9.041447e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1233

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498643e+00	 sigma_n : 8.601773e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1234

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.847349e+00	 sigma_n : 9.026906e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1235

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.480069e+00	 sigma_n : 8.760698e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1236

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697717e+00	 sigma_n : 9.005430e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1237

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727531e+00	 sigma_n : 8.594880e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1238

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626364e+00	 sigma_n : 8.782929e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1239

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606227e+00	 sigma_n : 9.123456e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1240

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712871e+00	 sigma_n : 9.288384e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1241

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.416065e+00	 sigma_n : 8.064573e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1242

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579431e+00	 sigma_n : 9.031940e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1243

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575703e+00	 sigma_n : 8.401380e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 1244

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754246e+00	 sigma_n : 9.278435e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1245

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.509953e+00	 sigma_n : 7.962274e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 1246

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731898e+00	 sigma_n : 9.007716e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1247

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608059e+00	 sigma_n : 8.823939e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1248

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767940e+00	 sigma_n : 8.772114e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1249

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551075e+00	 sigma_n : 8.171110e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1250

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776105e+00	 sigma_n : 9.024854e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 1251

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639033e+00	 sigma_n : 8.662223e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1252

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550218e+00	 sigma_n : 8.641396e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1253

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559894e+00	 sigma_n : 8.786807e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1254

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593376e+00	 sigma_n : 8.069158e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1255

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669903e+00	 sigma_n : 8.946057e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1256

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623894e+00	 sigma_n : 8.567839e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1257

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846154e+00	 sigma_n : 9.636249e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1258

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521076e+00	 sigma_n : 7.995345e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1259

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727683e+00	 sigma_n : 9.060699e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1260

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534529e+00	 sigma_n : 8.381334e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1261

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573674e+00	 sigma_n : 8.469770e-02
	 number of secondary particules: 995
	 number of fission neutrons: 995

 batch number : 1262

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789950e+00	 sigma_n : 9.456853e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1263

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767857e+00	 sigma_n : 8.967671e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1264

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.443656e+00	 sigma_n : 7.768397e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 1265

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763600e+00	 sigma_n : 1.025691e-01
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1266

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631579e+00	 sigma_n : 8.230414e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1267

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696532e+00	 sigma_n : 8.890180e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1268

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537815e+00	 sigma_n : 8.453978e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1269

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.866601e+00	 sigma_n : 9.475908e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1270

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526316e+00	 sigma_n : 8.039405e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1271

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632805e+00	 sigma_n : 8.400579e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1272

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664165e+00	 sigma_n : 8.520339e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1273

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696793e+00	 sigma_n : 9.297145e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1274

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.742248e+00	 sigma_n : 9.659384e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1275

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491340e+00	 sigma_n : 8.339708e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1276

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.869934e+00	 sigma_n : 1.009093e-01
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1277

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555653e+00	 sigma_n : 7.955179e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 1278

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.381613e+00	 sigma_n : 7.621804e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1279

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670113e+00	 sigma_n : 8.631861e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1280

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690991e+00	 sigma_n : 8.872730e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1281

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581633e+00	 sigma_n : 8.553562e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1282

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639020e+00	 sigma_n : 8.167694e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1283

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730392e+00	 sigma_n : 8.570641e-02
	 number of secondary particules: 1002
	 number of fission neutrons: 1002

 batch number : 1284

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.865269e+00	 sigma_n : 9.915290e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1285

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712394e+00	 sigma_n : 8.536853e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1286

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709459e+00	 sigma_n : 8.905330e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1287

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566421e+00	 sigma_n : 8.646191e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 1288

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798010e+00	 sigma_n : 9.333498e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1289

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740634e+00	 sigma_n : 9.882732e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1290

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705448e+00	 sigma_n : 8.874632e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1291

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539927e+00	 sigma_n : 8.729441e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1292

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.879921e+00	 sigma_n : 9.344809e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1293

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698182e+00	 sigma_n : 8.628219e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1294

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682070e+00	 sigma_n : 9.005001e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1295

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694319e+00	 sigma_n : 8.894636e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1296

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522829e+00	 sigma_n : 8.180763e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1297

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668203e+00	 sigma_n : 8.703102e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1298

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607273e+00	 sigma_n : 8.739927e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1299

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767647e+00	 sigma_n : 8.799439e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1300

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600567e+00	 sigma_n : 8.894572e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 1301

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666004e+00	 sigma_n : 8.953963e-02
	 number of secondary particules: 975
	 number of fission neutrons: 975

 batch number : 1302

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.030769e+00	 sigma_n : 1.024168e-01
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1303

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783045e+00	 sigma_n : 9.170116e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1304

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.476024e+00	 sigma_n : 7.981689e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1305

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545624e+00	 sigma_n : 9.198271e-02
	 number of secondary particules: 989
	 number of fission neutrons: 989

 batch number : 1306

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.878665e+00	 sigma_n : 9.328691e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1307

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655300e+00	 sigma_n : 8.834259e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1308

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608577e+00	 sigma_n : 8.846911e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1309

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.919884e+00	 sigma_n : 9.357172e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1310

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594086e+00	 sigma_n : 8.548442e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1311

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572703e+00	 sigma_n : 8.075803e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 1312

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504325e+00	 sigma_n : 8.023290e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1313

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.853394e+00	 sigma_n : 9.549259e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1314

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669278e+00	 sigma_n : 9.195001e-02
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 1315

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.429547e+00	 sigma_n : 7.560239e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1316

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718090e+00	 sigma_n : 8.471177e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1317

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696494e+00	 sigma_n : 9.274072e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1318

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739556e+00	 sigma_n : 8.536522e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 1319

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551161e+00	 sigma_n : 8.361232e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1320

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776577e+00	 sigma_n : 9.103018e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1321

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497824e+00	 sigma_n : 8.386457e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1322

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644307e+00	 sigma_n : 8.785609e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1323

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726519e+00	 sigma_n : 9.745850e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1324

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744758e+00	 sigma_n : 8.748731e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1325

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576481e+00	 sigma_n : 8.801365e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1326

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600000e+00	 sigma_n : 8.416288e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1327

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744639e+00	 sigma_n : 9.750901e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1328

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669452e+00	 sigma_n : 9.015148e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1329

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511790e+00	 sigma_n : 8.436989e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1330

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702381e+00	 sigma_n : 8.986075e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1331

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513004e+00	 sigma_n : 8.191461e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1332

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673913e+00	 sigma_n : 9.111690e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1333

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700478e+00	 sigma_n : 8.947043e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1334

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538534e+00	 sigma_n : 8.303589e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1335

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732883e+00	 sigma_n : 9.051008e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1336

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808824e+00	 sigma_n : 9.039862e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1337

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776727e+00	 sigma_n : 9.197983e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1338

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649676e+00	 sigma_n : 8.163473e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1339

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611940e+00	 sigma_n : 8.416799e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1340

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688584e+00	 sigma_n : 8.719014e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1341

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607502e+00	 sigma_n : 8.560491e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1342

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662594e+00	 sigma_n : 8.738072e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1343

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666365e+00	 sigma_n : 8.894205e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1344

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.495629e+00	 sigma_n : 8.589780e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1345

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588124e+00	 sigma_n : 8.827059e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1346

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645594e+00	 sigma_n : 8.921517e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1347

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682399e+00	 sigma_n : 9.284192e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1348

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.016457e+00	 sigma_n : 9.764673e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 1349

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.444062e+00	 sigma_n : 8.221503e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1350

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707071e+00	 sigma_n : 9.562185e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1351

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657247e+00	 sigma_n : 8.406736e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1352

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681267e+00	 sigma_n : 8.570482e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1353

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628731e+00	 sigma_n : 8.567936e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1354

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801357e+00	 sigma_n : 8.866354e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1355

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696545e+00	 sigma_n : 8.968930e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1356

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779808e+00	 sigma_n : 9.194323e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1357

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591350e+00	 sigma_n : 8.644315e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1358

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557218e+00	 sigma_n : 8.312083e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1359

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743446e+00	 sigma_n : 9.337519e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1360

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.456388e+00	 sigma_n : 8.317219e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1361

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662673e+00	 sigma_n : 8.681576e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1362

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622201e+00	 sigma_n : 8.800501e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1363

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700809e+00	 sigma_n : 9.263824e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1364

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573310e+00	 sigma_n : 8.707901e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1365

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640232e+00	 sigma_n : 8.285252e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1366

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756422e+00	 sigma_n : 9.207481e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1367

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577594e+00	 sigma_n : 8.573794e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1368

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740598e+00	 sigma_n : 9.169635e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1369

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673832e+00	 sigma_n : 9.029165e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1370

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777572e+00	 sigma_n : 9.143578e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1371

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491213e+00	 sigma_n : 8.208567e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1372

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692942e+00	 sigma_n : 8.546488e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1373

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572711e+00	 sigma_n : 8.421098e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1374

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725045e+00	 sigma_n : 8.813045e-02
	 number of secondary particules: 1188
	 number of fission neutrons: 1188

 batch number : 1375

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.400673e+00	 sigma_n : 7.929789e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1376

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.836735e+00	 sigma_n : 9.255310e-02
	 number of secondary particules: 1187
	 number of fission neutrons: 1187

 batch number : 1377

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540017e+00	 sigma_n : 8.762379e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1378

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634736e+00	 sigma_n : 8.819813e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1379

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520143e+00	 sigma_n : 8.177884e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1380

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620557e+00	 sigma_n : 9.147470e-02
	 number of secondary particules: 982
	 number of fission neutrons: 982

 batch number : 1381

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.856415e+00	 sigma_n : 9.504694e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1382

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791985e+00	 sigma_n : 9.551624e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1383

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690432e+00	 sigma_n : 9.030286e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1384

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638966e+00	 sigma_n : 8.370268e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1385

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.856221e+00	 sigma_n : 9.672468e-02
	 number of secondary particules: 1194
	 number of fission neutrons: 1194

 batch number : 1386

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631491e+00	 sigma_n : 8.767622e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 1387

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546994e+00	 sigma_n : 8.140369e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 1388

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.398084e+00	 sigma_n : 8.314601e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1389

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609316e+00	 sigma_n : 8.626790e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1390

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753098e+00	 sigma_n : 9.213899e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1391

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754664e+00	 sigma_n : 8.919689e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1392

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518062e+00	 sigma_n : 8.042620e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1393

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.435897e+00	 sigma_n : 8.070892e-02
	 number of secondary particules: 994
	 number of fission neutrons: 994

 batch number : 1394

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.891348e+00	 sigma_n : 9.838544e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1395

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672269e+00	 sigma_n : 9.017247e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1396

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492524e+00	 sigma_n : 8.402963e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1397

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824248e+00	 sigma_n : 9.672733e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1398

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575506e+00	 sigma_n : 8.330583e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1399

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593488e+00	 sigma_n : 9.018026e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1400

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693702e+00	 sigma_n : 9.560220e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1401

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661165e+00	 sigma_n : 8.995701e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1402

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780769e+00	 sigma_n : 1.054961e-01
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1403

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.806302e+00	 sigma_n : 8.915014e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1404

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591764e+00	 sigma_n : 8.132165e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1405

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523894e+00	 sigma_n : 8.235091e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1406

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683230e+00	 sigma_n : 8.898295e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1407

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745471e+00	 sigma_n : 8.915663e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1408

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.443855e+00	 sigma_n : 8.060312e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1409

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794203e+00	 sigma_n : 1.044751e-01
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1410

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694192e+00	 sigma_n : 8.148426e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1411

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602355e+00	 sigma_n : 8.678060e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1412

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682510e+00	 sigma_n : 8.790637e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1413

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611531e+00	 sigma_n : 8.513444e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1414

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798068e+00	 sigma_n : 9.811764e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1415

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661261e+00	 sigma_n : 8.685642e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1416

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.439286e+00	 sigma_n : 8.317298e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1417

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.914230e+00	 sigma_n : 9.880401e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1418

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.499110e+00	 sigma_n : 7.869497e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1419

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667600e+00	 sigma_n : 9.083630e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1420

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464510e+00	 sigma_n : 8.021106e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1421

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833004e+00	 sigma_n : 9.585528e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1422

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.440400e+00	 sigma_n : 8.172152e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1423

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635560e+00	 sigma_n : 8.882148e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1424

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.934314e+00	 sigma_n : 9.787422e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1425

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714029e+00	 sigma_n : 8.863183e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1426

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611807e+00	 sigma_n : 8.180716e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1427

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649074e+00	 sigma_n : 8.423210e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1428

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.843192e+00	 sigma_n : 9.441316e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1429

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610674e+00	 sigma_n : 9.087578e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1430

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545210e+00	 sigma_n : 7.907668e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1431

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615455e+00	 sigma_n : 8.289142e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1432

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664551e+00	 sigma_n : 8.834060e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1433

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685581e+00	 sigma_n : 8.726312e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1434

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657407e+00	 sigma_n : 8.834551e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1435

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672008e+00	 sigma_n : 8.776979e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1436

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694686e+00	 sigma_n : 9.124241e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1437

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.831767e+00	 sigma_n : 9.676732e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1438

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563115e+00	 sigma_n : 8.523711e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1439

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677903e+00	 sigma_n : 9.073218e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1440

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734165e+00	 sigma_n : 9.151914e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1441

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680776e+00	 sigma_n : 8.907590e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1442

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.496056e+00	 sigma_n : 7.892851e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1443

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699640e+00	 sigma_n : 8.817686e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1444

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676069e+00	 sigma_n : 8.537093e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1445

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701547e+00	 sigma_n : 8.984251e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1446

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626209e+00	 sigma_n : 8.613147e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1447

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539669e+00	 sigma_n : 7.757828e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1448

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679964e+00	 sigma_n : 8.776198e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1449

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736937e+00	 sigma_n : 9.252866e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1450

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697024e+00	 sigma_n : 8.789169e-02
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 1451

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569599e+00	 sigma_n : 8.251786e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1452

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569076e+00	 sigma_n : 8.469682e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1453

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651359e+00	 sigma_n : 8.426468e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1454

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812383e+00	 sigma_n : 9.444430e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 1455

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465157e+00	 sigma_n : 8.393025e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1456

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619615e+00	 sigma_n : 8.785680e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1457

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681523e+00	 sigma_n : 8.307498e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1458

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659517e+00	 sigma_n : 8.469145e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1459

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687161e+00	 sigma_n : 8.763467e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1460

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598684e+00	 sigma_n : 8.582776e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1461

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666358e+00	 sigma_n : 8.573539e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1462

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.410394e+00	 sigma_n : 8.352016e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1463

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803902e+00	 sigma_n : 9.702896e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1464

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.856039e+00	 sigma_n : 9.461110e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1465

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500455e+00	 sigma_n : 7.997854e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 1466

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639604e+00	 sigma_n : 8.861661e-02
	 number of secondary particules: 976
	 number of fission neutrons: 976

 batch number : 1467

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702869e+00	 sigma_n : 9.297425e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 1468

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.832000e+00	 sigma_n : 9.548242e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1469

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746032e+00	 sigma_n : 9.771922e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1470

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759091e+00	 sigma_n : 9.252463e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1471

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594190e+00	 sigma_n : 7.933811e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1472

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523766e+00	 sigma_n : 7.867251e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1473

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684866e+00	 sigma_n : 8.946420e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1474

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719397e+00	 sigma_n : 9.638730e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1475

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673954e+00	 sigma_n : 8.218048e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1476

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507692e+00	 sigma_n : 8.479851e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1477

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543128e+00	 sigma_n : 8.415898e-02
	 number of secondary particules: 955
	 number of fission neutrons: 955

 batch number : 1478

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.870157e+00	 sigma_n : 9.553857e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1479

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660000e+00	 sigma_n : 8.870897e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1480

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794466e+00	 sigma_n : 9.371287e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1481

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767464e+00	 sigma_n : 1.011696e-01
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1482

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682075e+00	 sigma_n : 8.509170e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1483

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794118e+00	 sigma_n : 8.888012e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1484

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651803e+00	 sigma_n : 8.338649e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1485

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666038e+00	 sigma_n : 8.846861e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1486

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724008e+00	 sigma_n : 9.113118e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1487

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663507e+00	 sigma_n : 9.037188e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1488

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579380e+00	 sigma_n : 8.383640e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1489

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693533e+00	 sigma_n : 8.988107e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1490

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.927757e+00	 sigma_n : 9.662365e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 1491

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684764e+00	 sigma_n : 9.040853e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1492

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504409e+00	 sigma_n : 7.829193e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1493

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590827e+00	 sigma_n : 8.242229e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1494

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681574e+00	 sigma_n : 8.784465e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1495

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.319408e+00	 sigma_n : 7.782809e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1496

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740883e+00	 sigma_n : 8.712589e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1497

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.820709e+00	 sigma_n : 9.584397e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1498

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582794e+00	 sigma_n : 7.797744e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1499

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822551e+00	 sigma_n : 9.150651e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 1500

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.431169e+00	 sigma_n : 8.196825e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1501

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770028e+00	 sigma_n : 9.524225e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1502

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522092e+00	 sigma_n : 8.327262e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1503

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745557e+00	 sigma_n : 9.474621e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1504

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706619e+00	 sigma_n : 8.702558e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1505

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.461404e+00	 sigma_n : 7.842082e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 1506

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800201e+00	 sigma_n : 9.391724e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1507

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712223e+00	 sigma_n : 9.189252e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1508

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650097e+00	 sigma_n : 9.016372e-02
	 number of secondary particules: 980
	 number of fission neutrons: 980

 batch number : 1509

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.020408e+00	 sigma_n : 1.024577e-01
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1510

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558477e+00	 sigma_n : 8.480595e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1511

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.830869e+00	 sigma_n : 9.121697e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1512

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571166e+00	 sigma_n : 8.556570e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1513

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555160e+00	 sigma_n : 8.528756e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1514

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.831876e+00	 sigma_n : 9.438683e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1515

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.487478e+00	 sigma_n : 7.967386e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 1516

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.825706e+00	 sigma_n : 9.469051e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1517

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651696e+00	 sigma_n : 8.556080e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1518

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776133e+00	 sigma_n : 9.528502e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1519

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647318e+00	 sigma_n : 8.544303e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 1520

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.509632e+00	 sigma_n : 8.490542e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1521

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714551e+00	 sigma_n : 9.462162e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1522

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579323e+00	 sigma_n : 8.665864e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1523

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640839e+00	 sigma_n : 8.630021e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1524

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468310e+00	 sigma_n : 8.440130e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1525

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592793e+00	 sigma_n : 8.044357e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1526

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687845e+00	 sigma_n : 9.285377e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1527

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724745e+00	 sigma_n : 9.396135e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1528

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.843486e+00	 sigma_n : 9.004758e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1529

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626582e+00	 sigma_n : 9.088447e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1530

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606145e+00	 sigma_n : 8.669960e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1531

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766698e+00	 sigma_n : 9.258107e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 1532

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567216e+00	 sigma_n : 8.910114e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1533

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598353e+00	 sigma_n : 8.956548e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1534

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675165e+00	 sigma_n : 8.991487e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1535

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.861712e+00	 sigma_n : 9.055210e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1536

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528992e+00	 sigma_n : 8.951014e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1537

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810115e+00	 sigma_n : 9.728675e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1538

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745810e+00	 sigma_n : 9.730661e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1539

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673561e+00	 sigma_n : 8.691398e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1540

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578947e+00	 sigma_n : 8.423786e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1541

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715857e+00	 sigma_n : 8.482183e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 1542

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534645e+00	 sigma_n : 8.799688e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1543

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623084e+00	 sigma_n : 8.283039e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1544

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663284e+00	 sigma_n : 8.809123e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1545

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631532e+00	 sigma_n : 8.800697e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1546

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.501832e+00	 sigma_n : 8.536131e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1547

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641546e+00	 sigma_n : 8.401531e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1548

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720153e+00	 sigma_n : 9.350403e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1549

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712835e+00	 sigma_n : 9.281970e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1550

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681308e+00	 sigma_n : 8.778369e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1551

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807904e+00	 sigma_n : 9.337230e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1552

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682102e+00	 sigma_n : 9.219312e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 1553

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533448e+00	 sigma_n : 8.293011e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1554

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585650e+00	 sigma_n : 8.189499e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1555

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656772e+00	 sigma_n : 8.431189e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1556

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666038e+00	 sigma_n : 8.975818e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1557

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578755e+00	 sigma_n : 8.177163e-02
	 number of secondary particules: 978
	 number of fission neutrons: 978

 batch number : 1558

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793456e+00	 sigma_n : 9.223220e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 1559

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.867906e+00	 sigma_n : 9.597315e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1560

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662559e+00	 sigma_n : 8.781983e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1561

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661454e+00	 sigma_n : 9.367807e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1562

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538390e+00	 sigma_n : 8.122609e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1563

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714286e+00	 sigma_n : 8.570502e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1564

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778517e+00	 sigma_n : 8.939305e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1565

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730839e+00	 sigma_n : 9.074052e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1566

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549605e+00	 sigma_n : 8.972043e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1567

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.901434e+00	 sigma_n : 9.594691e-02
	 number of secondary particules: 1176
	 number of fission neutrons: 1176

 batch number : 1568

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580782e+00	 sigma_n : 7.946815e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 1569

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.347639e+00	 sigma_n : 7.501164e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1570

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639962e+00	 sigma_n : 8.630179e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 1571

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766310e+00	 sigma_n : 9.310426e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1572

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540284e+00	 sigma_n : 8.275953e-02
	 number of secondary particules: 981
	 number of fission neutrons: 981

 batch number : 1573

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.997961e+00	 sigma_n : 1.043879e-01
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1574

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597985e+00	 sigma_n : 8.996456e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1575

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.864341e+00	 sigma_n : 9.323487e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1576

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563717e+00	 sigma_n : 8.142268e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1577

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615789e+00	 sigma_n : 8.878607e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1578

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649091e+00	 sigma_n : 8.703985e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1579

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641929e+00	 sigma_n : 8.136299e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1580

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659341e+00	 sigma_n : 8.202297e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1581

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533333e+00	 sigma_n : 8.335547e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1582

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797258e+00	 sigma_n : 9.942621e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1583

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672498e+00	 sigma_n : 9.122251e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1584

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706157e+00	 sigma_n : 9.017757e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1585

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650094e+00	 sigma_n : 9.027672e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1586

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.889756e+00	 sigma_n : 9.773805e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1587

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598390e+00	 sigma_n : 8.230074e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1588

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629428e+00	 sigma_n : 8.689549e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1589

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712687e+00	 sigma_n : 8.895748e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1590

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727273e+00	 sigma_n : 8.928740e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1591

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725704e+00	 sigma_n : 8.699215e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1592

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634011e+00	 sigma_n : 8.722597e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1593

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590824e+00	 sigma_n : 8.293542e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1594

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633394e+00	 sigma_n : 8.396483e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1595

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.928704e+00	 sigma_n : 9.092215e-02
	 number of secondary particules: 1192
	 number of fission neutrons: 1192

 batch number : 1596

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.449664e+00	 sigma_n : 8.249290e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1597

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720848e+00	 sigma_n : 9.482370e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 1598

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581756e+00	 sigma_n : 8.290576e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1599

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619632e+00	 sigma_n : 8.176878e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1600

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594449e+00	 sigma_n : 8.211407e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1601

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589973e+00	 sigma_n : 8.486647e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1602

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.825024e+00	 sigma_n : 9.634750e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1603

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741553e+00	 sigma_n : 9.262658e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1604

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595822e+00	 sigma_n : 7.826846e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1605

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.456700e+00	 sigma_n : 7.835814e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1606

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811321e+00	 sigma_n : 8.968417e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1607

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706912e+00	 sigma_n : 8.563375e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1608

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736549e+00	 sigma_n : 9.196453e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1609

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645161e+00	 sigma_n : 8.769202e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1610

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682584e+00	 sigma_n : 9.189594e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1611

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635601e+00	 sigma_n : 8.934776e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 1612

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.914634e+00	 sigma_n : 9.467951e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1613

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610200e+00	 sigma_n : 8.359464e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1614

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.827402e+00	 sigma_n : 9.212398e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1615

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.432667e+00	 sigma_n : 7.862439e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1616

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824363e+00	 sigma_n : 9.535411e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1617

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591874e+00	 sigma_n : 8.690288e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1618

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682387e+00	 sigma_n : 9.218584e-02
	 number of secondary particules: 1008
	 number of fission neutrons: 1008

 batch number : 1619

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.946375e+00	 sigma_n : 9.920061e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1620

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669138e+00	 sigma_n : 9.094678e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1621

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613165e+00	 sigma_n : 8.431348e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1622

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791506e+00	 sigma_n : 8.913399e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1623

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547085e+00	 sigma_n : 8.614794e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1624

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780784e+00	 sigma_n : 8.668620e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1625

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559641e+00	 sigma_n : 8.555953e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1626

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656109e+00	 sigma_n : 8.836375e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1627

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780935e+00	 sigma_n : 8.765319e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1628

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609225e+00	 sigma_n : 8.407357e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1629

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611967e+00	 sigma_n : 8.806095e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1630

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634328e+00	 sigma_n : 9.048716e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1631

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790414e+00	 sigma_n : 8.796759e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 1632

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.480948e+00	 sigma_n : 8.199295e-02
	 number of secondary particules: 1177
	 number of fission neutrons: 1177

 batch number : 1633

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491079e+00	 sigma_n : 7.824495e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1634

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646520e+00	 sigma_n : 8.456386e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1635

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525350e+00	 sigma_n : 7.956229e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1636

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729654e+00	 sigma_n : 9.022922e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1637

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634862e+00	 sigma_n : 8.554598e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1638

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705825e+00	 sigma_n : 9.062119e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1639

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650899e+00	 sigma_n : 9.273102e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1640

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.415814e+00	 sigma_n : 8.046426e-02
	 number of secondary particules: 955
	 number of fission neutrons: 955

 batch number : 1641

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.841885e+00	 sigma_n : 9.418029e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1642

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.889328e+00	 sigma_n : 9.645919e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1643

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632493e+00	 sigma_n : 8.340370e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 1644

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.298801e+00	 sigma_n : 7.438872e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1645

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794922e+00	 sigma_n : 9.769876e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1646

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668880e+00	 sigma_n : 8.900113e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1647

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559701e+00	 sigma_n : 8.354826e-02
	 number of secondary particules: 988
	 number of fission neutrons: 988

 batch number : 1648

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.925101e+00	 sigma_n : 1.001378e-01
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1649

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606528e+00	 sigma_n : 8.485083e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1650

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671128e+00	 sigma_n : 9.212483e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1651

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812500e+00	 sigma_n : 9.433573e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1652

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670350e+00	 sigma_n : 8.592697e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1653

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770125e+00	 sigma_n : 9.130992e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 1654

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576068e+00	 sigma_n : 8.925406e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1655

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603147e+00	 sigma_n : 9.229202e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1656

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.529360e+00	 sigma_n : 8.261689e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1657

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717614e+00	 sigma_n : 9.179978e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1658

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504837e+00	 sigma_n : 8.387303e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1659

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721042e+00	 sigma_n : 8.720582e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1660

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701621e+00	 sigma_n : 9.107930e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1661

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681687e+00	 sigma_n : 8.442512e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1662

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713327e+00	 sigma_n : 8.807869e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1663

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691262e+00	 sigma_n : 8.951053e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1664

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615754e+00	 sigma_n : 8.678634e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1665

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757430e+00	 sigma_n : 9.058342e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1666

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.508036e+00	 sigma_n : 8.126140e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1667

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692678e+00	 sigma_n : 8.796450e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1668

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773023e+00	 sigma_n : 9.544935e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1669

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605546e+00	 sigma_n : 8.775530e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1670

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514104e+00	 sigma_n : 8.014302e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1671

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614644e+00	 sigma_n : 8.652104e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1672

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797073e+00	 sigma_n : 9.449295e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1673

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.961941e+00	 sigma_n : 9.752721e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174

 batch number : 1674

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540034e+00	 sigma_n : 7.986448e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1675

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543459e+00	 sigma_n : 8.671486e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1676

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593890e+00	 sigma_n : 8.383409e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1677

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.950962e+00	 sigma_n : 1.021829e-01
	 number of secondary particules: 1192
	 number of fission neutrons: 1192

 batch number : 1678

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.417785e+00	 sigma_n : 7.961183e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1679

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677858e+00	 sigma_n : 8.506074e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1680

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.382128e+00	 sigma_n : 8.063606e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1681

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707136e+00	 sigma_n : 9.549607e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1682

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609434e+00	 sigma_n : 8.589635e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1683

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730097e+00	 sigma_n : 9.009441e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1684

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756732e+00	 sigma_n : 9.066660e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1685

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758364e+00	 sigma_n : 9.862535e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1686

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785913e+00	 sigma_n : 8.998058e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1687

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740179e+00	 sigma_n : 9.573851e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1688

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489006e+00	 sigma_n : 8.300028e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1689

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646330e+00	 sigma_n : 8.366777e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1690

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612717e+00	 sigma_n : 9.000735e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 1691

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659000e+00	 sigma_n : 8.486413e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1692

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.826810e+00	 sigma_n : 9.753408e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1693

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.931689e+00	 sigma_n : 9.552294e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1694

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808341e+00	 sigma_n : 9.352810e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1695

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583840e+00	 sigma_n : 8.129416e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1696

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561531e+00	 sigma_n : 8.597000e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1697

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.554140e+00	 sigma_n : 7.886615e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1698

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757062e+00	 sigma_n : 9.040530e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1699

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.742287e+00	 sigma_n : 9.483831e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1700

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663717e+00	 sigma_n : 8.893321e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1701

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558385e+00	 sigma_n : 8.439861e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1702

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604259e+00	 sigma_n : 8.939638e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1703

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604630e+00	 sigma_n : 8.812638e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1704

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669500e+00	 sigma_n : 8.528971e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1705

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735105e+00	 sigma_n : 9.163889e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1706

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650187e+00	 sigma_n : 9.368026e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1707

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592044e+00	 sigma_n : 8.378228e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 1708

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.878698e+00	 sigma_n : 9.201064e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1709

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582960e+00	 sigma_n : 8.248519e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1710

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544423e+00	 sigma_n : 8.330327e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1711

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718961e+00	 sigma_n : 8.784271e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1712

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739209e+00	 sigma_n : 8.982612e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1713

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626571e+00	 sigma_n : 8.777520e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1714

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644506e+00	 sigma_n : 9.253630e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1715

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545368e+00	 sigma_n : 8.810712e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1716

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.895508e+00	 sigma_n : 9.630568e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1717

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546023e+00	 sigma_n : 8.469194e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1718

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785985e+00	 sigma_n : 9.039599e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1719

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631902e+00	 sigma_n : 9.148016e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1720

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626667e+00	 sigma_n : 8.782419e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 1721

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.491438e+00	 sigma_n : 8.107652e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1722

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532913e+00	 sigma_n : 9.107414e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1723

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587523e+00	 sigma_n : 8.496001e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1724

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678881e+00	 sigma_n : 8.716273e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1725

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631376e+00	 sigma_n : 8.593186e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 1726

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731329e+00	 sigma_n : 8.498966e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1727

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.478180e+00	 sigma_n : 8.140122e-02
	 number of secondary particules: 962
	 number of fission neutrons: 962

 batch number : 1728

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708940e+00	 sigma_n : 9.445791e-02
	 number of secondary particules: 950
	 number of fission neutrons: 950

 batch number : 1729

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.890526e+00	 sigma_n : 9.180626e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1730

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635577e+00	 sigma_n : 9.145025e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1731

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772342e+00	 sigma_n : 9.179684e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1732

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598714e+00	 sigma_n : 8.592450e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1733

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563521e+00	 sigma_n : 8.750805e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1734

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663065e+00	 sigma_n : 9.155061e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1735

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647727e+00	 sigma_n : 8.342101e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1736

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698592e+00	 sigma_n : 9.198648e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1737

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653285e+00	 sigma_n : 8.961624e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1738

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782938e+00	 sigma_n : 8.940014e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1739

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577617e+00	 sigma_n : 8.606026e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1740

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774953e+00	 sigma_n : 9.407063e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1741

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739048e+00	 sigma_n : 9.117638e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1742

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770147e+00	 sigma_n : 8.965049e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1743

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658088e+00	 sigma_n : 8.434149e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1744

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614480e+00	 sigma_n : 7.890784e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1745

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.470163e+00	 sigma_n : 8.350255e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1746

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824782e+00	 sigma_n : 1.039947e-01
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1747

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.941068e+00	 sigma_n : 9.517841e-02
	 number of secondary particules: 1189
	 number of fission neutrons: 1189

 batch number : 1748

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.470143e+00	 sigma_n : 7.905634e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1749

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592456e+00	 sigma_n : 8.882784e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1750

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602955e+00	 sigma_n : 8.667506e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1751

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786252e+00	 sigma_n : 9.705757e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1752

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643836e+00	 sigma_n : 8.632556e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1753

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693548e+00	 sigma_n : 9.146047e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1754

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772381e+00	 sigma_n : 9.166349e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1755

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715370e+00	 sigma_n : 9.441065e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1756

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648826e+00	 sigma_n : 9.059647e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1757

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691606e+00	 sigma_n : 9.219880e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1758

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590827e+00	 sigma_n : 8.444027e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1759

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654163e+00	 sigma_n : 8.718878e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1760

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549955e+00	 sigma_n : 8.395871e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1761

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700816e+00	 sigma_n : 8.885774e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1762

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632525e+00	 sigma_n : 8.502204e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1763

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579439e+00	 sigma_n : 8.267760e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1764

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758201e+00	 sigma_n : 1.026268e-01
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1765

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.826940e+00	 sigma_n : 9.245643e-02
	 number of secondary particules: 1204
	 number of fission neutrons: 1204

 batch number : 1766

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531561e+00	 sigma_n : 8.394165e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1767

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675221e+00	 sigma_n : 9.146890e-02
	 number of secondary particules: 1197
	 number of fission neutrons: 1197

 batch number : 1768

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.420217e+00	 sigma_n : 8.514875e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1769

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530521e+00	 sigma_n : 8.216947e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1770

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692829e+00	 sigma_n : 9.287440e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1771

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709961e+00	 sigma_n : 8.995590e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1772

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559809e+00	 sigma_n : 8.547950e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1773

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731870e+00	 sigma_n : 9.026230e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1774

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675117e+00	 sigma_n : 8.750925e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1775

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522181e+00	 sigma_n : 8.306335e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1776

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636620e+00	 sigma_n : 8.875480e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1777

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.959843e+00	 sigma_n : 9.423143e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1778

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561372e+00	 sigma_n : 8.378740e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1779

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787313e+00	 sigma_n : 9.600230e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1780

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540323e+00	 sigma_n : 8.777605e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1781

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698842e+00	 sigma_n : 9.214399e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1782

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809981e+00	 sigma_n : 9.081642e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1783

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713606e+00	 sigma_n : 9.215917e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 1784

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634241e+00	 sigma_n : 8.542593e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1785

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804348e+00	 sigma_n : 9.105800e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1786

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462946e+00	 sigma_n : 8.043340e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 1787

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749503e+00	 sigma_n : 9.676567e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1788

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462810e+00	 sigma_n : 7.978776e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1789

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541930e+00	 sigma_n : 8.465185e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1790

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717412e+00	 sigma_n : 8.934475e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1791

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608897e+00	 sigma_n : 8.767421e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1792

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819057e+00	 sigma_n : 9.385447e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1793

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601802e+00	 sigma_n : 9.060712e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1794

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632283e+00	 sigma_n : 8.260775e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1795

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760113e+00	 sigma_n : 9.167576e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1796

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733149e+00	 sigma_n : 9.676374e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1797

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804408e+00	 sigma_n : 9.922481e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1798

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654859e+00	 sigma_n : 8.770906e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1799

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.425066e+00	 sigma_n : 7.927650e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1800

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756654e+00	 sigma_n : 9.088961e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1801

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.818692e+00	 sigma_n : 8.880602e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 1802

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.413495e+00	 sigma_n : 7.628697e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1803

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673565e+00	 sigma_n : 8.572319e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1804

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711686e+00	 sigma_n : 8.976598e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1805

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596958e+00	 sigma_n : 8.482305e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1806

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689558e+00	 sigma_n : 8.711632e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1807

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612512e+00	 sigma_n : 8.558602e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1808

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719547e+00	 sigma_n : 9.165230e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1809

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685349e+00	 sigma_n : 9.243918e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 1810

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787968e+00	 sigma_n : 8.830324e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1811

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692748e+00	 sigma_n : 9.012796e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1812

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713340e+00	 sigma_n : 9.095547e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1813

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722689e+00	 sigma_n : 9.215707e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1814

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770308e+00	 sigma_n : 8.898170e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1815

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771593e+00	 sigma_n : 9.098509e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1816

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739650e+00	 sigma_n : 8.992192e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1817

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704263e+00	 sigma_n : 8.890501e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1818

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687722e+00	 sigma_n : 8.757816e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1819

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737601e+00	 sigma_n : 9.110360e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 1820

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.318691e+00	 sigma_n : 7.737106e-02
	 number of secondary particules: 971
	 number of fission neutrons: 971

 batch number : 1821

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.867147e+00	 sigma_n : 9.849786e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1822

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609615e+00	 sigma_n : 9.063002e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1823

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717974e+00	 sigma_n : 9.276675e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 1824

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705419e+00	 sigma_n : 9.377658e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1825

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584689e+00	 sigma_n : 8.628127e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 1826

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810039e+00	 sigma_n : 9.703698e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1827

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747637e+00	 sigma_n : 9.531437e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1828

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.827290e+00	 sigma_n : 9.526347e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1829

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745308e+00	 sigma_n : 9.019949e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1830

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576822e+00	 sigma_n : 8.836917e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1831

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516844e+00	 sigma_n : 8.242938e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1832

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552074e+00	 sigma_n : 8.440120e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1833

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758886e+00	 sigma_n : 9.690435e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1834

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582878e+00	 sigma_n : 8.934479e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1835

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693333e+00	 sigma_n : 8.943081e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1836

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638889e+00	 sigma_n : 8.523052e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1837

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717248e+00	 sigma_n : 9.254950e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1838

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719101e+00	 sigma_n : 8.816443e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1839

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677093e+00	 sigma_n : 8.406139e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1840

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.506824e+00	 sigma_n : 8.442418e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1841

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774500e+00	 sigma_n : 9.102519e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1842

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766151e+00	 sigma_n : 8.579804e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1843

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628444e+00	 sigma_n : 8.975468e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1844

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613438e+00	 sigma_n : 8.997110e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1845

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507339e+00	 sigma_n : 8.348139e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1846

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715588e+00	 sigma_n : 9.457178e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 1847

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584890e+00	 sigma_n : 8.225969e-02
	 number of secondary particules: 1208
	 number of fission neutrons: 1208

 batch number : 1848

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507450e+00	 sigma_n : 8.282375e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174

 batch number : 1849

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652470e+00	 sigma_n : 8.513933e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 1850

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568376e+00	 sigma_n : 8.640415e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1851

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812556e+00	 sigma_n : 9.128228e-02
	 number of secondary particules: 1210
	 number of fission neutrons: 1210

 batch number : 1852

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497521e+00	 sigma_n : 8.495621e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1853

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640582e+00	 sigma_n : 8.275031e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1854

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465909e+00	 sigma_n : 8.698092e-02
	 number of secondary particules: 957
	 number of fission neutrons: 957

 batch number : 1855

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.894462e+00	 sigma_n : 9.780863e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 1856

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730847e+00	 sigma_n : 9.100177e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1857

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.818006e+00	 sigma_n : 9.153330e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1858

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688748e+00	 sigma_n : 8.667139e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1859

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562337e+00	 sigma_n : 8.598466e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1860

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542553e+00	 sigma_n : 8.531007e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1861

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720755e+00	 sigma_n : 9.091964e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1862

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.821735e+00	 sigma_n : 9.766289e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1863

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635774e+00	 sigma_n : 8.981950e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1864

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765854e+00	 sigma_n : 8.648037e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1865

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789179e+00	 sigma_n : 9.362694e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1866

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759528e+00	 sigma_n : 8.647640e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1867

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749110e+00	 sigma_n : 8.906652e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 1868

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.371622e+00	 sigma_n : 7.920259e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1869

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.823091e+00	 sigma_n : 8.650917e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1870

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531802e+00	 sigma_n : 7.951026e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1871

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585526e+00	 sigma_n : 8.734199e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 1872

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697791e+00	 sigma_n : 9.284093e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1873

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635681e+00	 sigma_n : 8.901430e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1874

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698473e+00	 sigma_n : 8.898645e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1875

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685904e+00	 sigma_n : 9.261278e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1876

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537234e+00	 sigma_n : 8.309829e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1877

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675875e+00	 sigma_n : 9.106676e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1878

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675431e+00	 sigma_n : 8.709281e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1879

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610124e+00	 sigma_n : 8.811714e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1880

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689908e+00	 sigma_n : 9.212050e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1881

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686501e+00	 sigma_n : 9.407275e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1882

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.409821e+00	 sigma_n : 7.711491e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1883

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627022e+00	 sigma_n : 9.012596e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1884

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630163e+00	 sigma_n : 7.898747e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1885

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.471349e+00	 sigma_n : 8.243124e-02
	 number of secondary particules: 971
	 number of fission neutrons: 971

 batch number : 1886

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728395e+00	 sigma_n : 8.966633e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1887

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.911417e+00	 sigma_n : 1.046142e-01
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1888

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604436e+00	 sigma_n : 8.617889e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1889

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805956e+00	 sigma_n : 8.867358e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1890

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750235e+00	 sigma_n : 8.681049e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1891

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696915e+00	 sigma_n : 8.893610e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1892

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704110e+00	 sigma_n : 8.657196e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1893

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.881555e+00	 sigma_n : 9.291762e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1894

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617174e+00	 sigma_n : 8.794264e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1895

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612758e+00	 sigma_n : 8.414991e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1896

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565801e+00	 sigma_n : 8.553593e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1897

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613531e+00	 sigma_n : 8.823570e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1898

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.826422e+00	 sigma_n : 9.290416e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1899

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735663e+00	 sigma_n : 8.810428e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 1900

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.455326e+00	 sigma_n : 8.026177e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1901

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665108e+00	 sigma_n : 9.018668e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1902

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722800e+00	 sigma_n : 8.531190e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1903

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670152e+00	 sigma_n : 8.552089e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1904

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648166e+00	 sigma_n : 8.310335e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1905

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659351e+00	 sigma_n : 8.903084e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1906

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765258e+00	 sigma_n : 9.312618e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1907

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490283e+00	 sigma_n : 8.335197e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1908

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769953e+00	 sigma_n : 8.854708e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1909

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659011e+00	 sigma_n : 8.636858e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1910

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762635e+00	 sigma_n : 9.048546e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1911

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608544e+00	 sigma_n : 8.465134e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 1912

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.437126e+00	 sigma_n : 7.924168e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1913

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761991e+00	 sigma_n : 9.269680e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 1914

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547186e+00	 sigma_n : 8.075519e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1915

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622862e+00	 sigma_n : 8.674243e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1916

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672321e+00	 sigma_n : 8.670908e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1917

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528169e+00	 sigma_n : 8.231832e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1918

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737628e+00	 sigma_n : 9.020782e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1919

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537975e+00	 sigma_n : 8.249396e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 1920

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783476e+00	 sigma_n : 9.117495e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1921

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511070e+00	 sigma_n : 8.062284e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1922

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674528e+00	 sigma_n : 9.015891e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 batch number : 1923

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785927e+00	 sigma_n : 9.019358e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1924

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.887814e+00	 sigma_n : 9.963311e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1925

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661111e+00	 sigma_n : 8.627526e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1926

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735322e+00	 sigma_n : 9.191049e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1927

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731193e+00	 sigma_n : 9.488231e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1928

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637209e+00	 sigma_n : 9.056916e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1929

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570605e+00	 sigma_n : 8.733146e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1930

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786603e+00	 sigma_n : 9.280033e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1931

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753584e+00	 sigma_n : 8.647571e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 1932

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539258e+00	 sigma_n : 7.667283e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1933

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723818e+00	 sigma_n : 9.003861e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1934

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642086e+00	 sigma_n : 8.020607e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1935

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.422807e+00	 sigma_n : 8.333853e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1936

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.920192e+00	 sigma_n : 9.397316e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1937

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516696e+00	 sigma_n : 7.908270e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1938

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526126e+00	 sigma_n : 8.453444e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1939

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633147e+00	 sigma_n : 8.562734e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 1940

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772239e+00	 sigma_n : 9.399919e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1941

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645068e+00	 sigma_n : 8.659078e-02
	 number of secondary particules: 1002
	 number of fission neutrons: 1002

 batch number : 1942

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.899202e+00	 sigma_n : 9.519252e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1943

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656367e+00	 sigma_n : 8.193851e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1944

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822010e+00	 sigma_n : 9.388777e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1945

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535651e+00	 sigma_n : 8.379296e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1946

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719855e+00	 sigma_n : 9.131961e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1947

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497725e+00	 sigma_n : 7.949002e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1948

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797059e+00	 sigma_n : 9.292442e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1949

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588979e+00	 sigma_n : 8.382006e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1950

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535224e+00	 sigma_n : 7.980673e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1951

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589580e+00	 sigma_n : 8.884599e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1952

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704567e+00	 sigma_n : 9.193185e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1953

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.853953e+00	 sigma_n : 9.637701e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1954

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634043e+00	 sigma_n : 8.813244e-02
	 number of secondary particules: 1203
	 number of fission neutrons: 1203

 batch number : 1955

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497922e+00	 sigma_n : 8.015677e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1956

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521102e+00	 sigma_n : 7.890879e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1957

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684956e+00	 sigma_n : 8.851636e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1958

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565217e+00	 sigma_n : 8.421056e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1959

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.624542e+00	 sigma_n : 8.946658e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1960

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811731e+00	 sigma_n : 9.191273e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1961

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630063e+00	 sigma_n : 8.826213e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1962

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498628e+00	 sigma_n : 8.287292e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1963

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676301e+00	 sigma_n : 8.623807e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1964

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759771e+00	 sigma_n : 9.412372e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 1965

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800198e+00	 sigma_n : 1.002765e-01
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1966

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822809e+00	 sigma_n : 9.448679e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1967

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579982e+00	 sigma_n : 8.256628e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1968

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539497e+00	 sigma_n : 8.836181e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1969

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734360e+00	 sigma_n : 9.431127e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1970

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747706e+00	 sigma_n : 8.866482e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1971

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789328e+00	 sigma_n : 9.248286e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1972

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641392e+00	 sigma_n : 8.339520e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1973

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756951e+00	 sigma_n : 9.440104e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1974

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563124e+00	 sigma_n : 8.716142e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1975

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634280e+00	 sigma_n : 8.841941e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1976

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721668e+00	 sigma_n : 9.015505e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1977

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700089e+00	 sigma_n : 9.169025e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1978

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556344e+00	 sigma_n : 8.392536e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1979

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686924e+00	 sigma_n : 8.691668e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1980

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628410e+00	 sigma_n : 8.842163e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1981

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731969e+00	 sigma_n : 8.828757e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1982

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593750e+00	 sigma_n : 8.636064e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1983

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751371e+00	 sigma_n : 8.763119e-02
	 number of secondary particules: 1179
	 number of fission neutrons: 1179

 batch number : 1984

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536047e+00	 sigma_n : 8.678008e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1985

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668454e+00	 sigma_n : 8.941439e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1986

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540636e+00	 sigma_n : 8.105367e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1987

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561355e+00	 sigma_n : 8.513432e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1988

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707780e+00	 sigma_n : 9.055946e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1989

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710602e+00	 sigma_n : 8.619882e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1990

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631077e+00	 sigma_n : 8.651367e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1991

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643925e+00	 sigma_n : 8.760927e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1992

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708057e+00	 sigma_n : 9.208973e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1993

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.820056e+00	 sigma_n : 9.599528e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1994

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612116e+00	 sigma_n : 8.199499e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1995

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610000e+00	 sigma_n : 8.549192e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1996

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522132e+00	 sigma_n : 8.335211e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1997

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676218e+00	 sigma_n : 8.739769e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1998

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693609e+00	 sigma_n : 9.130089e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1999

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777467e+00	 sigma_n : 8.805724e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 2000

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772118e+00	 sigma_n : 8.722826e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 2001

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675258e+00	 sigma_n : 8.590996e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 2002

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.399145e+00	 sigma_n : 7.464391e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 2003

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748031e+00	 sigma_n : 8.904926e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 2004

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676983e+00	 sigma_n : 8.554310e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 2005

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649123e+00	 sigma_n : 8.634032e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 2006

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735294e+00	 sigma_n : 8.636435e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 2007

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783190e+00	 sigma_n : 9.059143e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 2008

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634935e+00	 sigma_n : 8.799559e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 2009

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728689e+00	 sigma_n : 9.069459e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 2010

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653913e+00	 sigma_n : 8.600683e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 2011

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615248e+00	 sigma_n : 8.527807e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 2012

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638640e+00	 sigma_n : 8.693462e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 2013

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545534e+00	 sigma_n : 8.408679e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 2014

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609621e+00	 sigma_n : 8.476901e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 2015

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.881783e+00	 sigma_n : 9.527192e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 2016

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563536e+00	 sigma_n : 8.239317e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 2017

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681267e+00	 sigma_n : 9.110371e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 2018

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635797e+00	 sigma_n : 8.689528e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 2019

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701452e+00	 sigma_n : 9.268454e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 2020

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824818e+00	 sigma_n : 9.014521e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 2021

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531330e+00	 sigma_n : 8.295649e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 2022

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558371e+00	 sigma_n : 8.598073e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 2023

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698413e+00	 sigma_n : 8.130580e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 2024

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599258e+00	 sigma_n : 8.502336e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 2025

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770245e+00	 sigma_n : 9.379061e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 2026

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626354e+00	 sigma_n : 8.727838e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 2027

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684743e+00	 sigma_n : 8.707453e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 2028

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728094e+00	 sigma_n : 9.296408e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 2029

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.443686e+00	 sigma_n : 7.654563e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 2030

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675398e+00	 sigma_n : 8.884743e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 2031

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612933e+00	 sigma_n : 8.124425e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 2032

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764651e+00	 sigma_n : 9.426616e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 2033

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525365e+00	 sigma_n : 8.928851e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 2034

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597701e+00	 sigma_n : 8.567934e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 2035

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527063e+00	 sigma_n : 8.233641e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 2036

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661001e+00	 sigma_n : 9.190317e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 2037

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753788e+00	 sigma_n : 8.844030e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 2038

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746569e+00	 sigma_n : 9.160090e-02
	 number of secondary particules: 1191
	 number of fission neutrons: 1191

 batch number : 2039

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486986e+00	 sigma_n : 7.953514e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 2040

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502326e+00	 sigma_n : 8.345296e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 2041

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749263e+00	 sigma_n : 9.249021e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 2042

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715370e+00	 sigma_n : 8.947150e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 2043

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.838710e+00	 sigma_n : 9.398115e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 2044

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659440e+00	 sigma_n : 8.845964e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 2045

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778383e+00	 sigma_n : 9.142911e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 2046

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516474e+00	 sigma_n : 8.060489e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 2047

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693107e+00	 sigma_n : 9.164039e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 2048

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797235e+00	 sigma_n : 8.606256e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 2049

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587665e+00	 sigma_n : 8.545491e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 2050

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585192e+00	 sigma_n : 8.517309e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 2051

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807163e+00	 sigma_n : 9.157282e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 2052

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557811e+00	 sigma_n : 8.363604e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 2053

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555751e+00	 sigma_n : 8.165909e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 2054

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720111e+00	 sigma_n : 8.934740e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 2055

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613879e+00	 sigma_n : 8.754665e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 2056

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570896e+00	 sigma_n : 8.377954e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 2057

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721088e+00	 sigma_n : 9.230586e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 2058

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661831e+00	 sigma_n : 8.576521e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 2059

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671147e+00	 sigma_n : 8.327092e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 2060

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.464476e+00	 sigma_n : 8.103377e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 2061

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.844961e+00	 sigma_n : 9.777251e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 2062

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699262e+00	 sigma_n : 9.274445e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 2063

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676290e+00	 sigma_n : 8.938180e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 2064

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564255e+00	 sigma_n : 8.486502e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 2065

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697307e+00	 sigma_n : 8.790764e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 2066

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722066e+00	 sigma_n : 8.966174e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 2067

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590265e+00	 sigma_n : 8.674280e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 2068

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548893e+00	 sigma_n : 8.318921e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 2069

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.891602e+00	 sigma_n : 9.748373e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 2070

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649234e+00	 sigma_n : 8.695311e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 2071

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576087e+00	 sigma_n : 8.795168e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 2072

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607843e+00	 sigma_n : 8.858757e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 2073

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.742354e+00	 sigma_n : 8.915909e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 2074

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582498e+00	 sigma_n : 8.495145e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 2075

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492740e+00	 sigma_n : 8.407053e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 2076

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579882e+00	 sigma_n : 8.540927e-02
	 number of secondary particules: 986
	 number of fission neutrons: 986

 batch number : 2077

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756592e+00	 sigma_n : 8.775707e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 2078

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660415e+00	 sigma_n : 8.230891e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 2079

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736275e+00	 sigma_n : 9.096273e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 2080

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716730e+00	 sigma_n : 9.227165e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 2081

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572344e+00	 sigma_n : 8.876593e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 2082

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548598e+00	 sigma_n : 8.381302e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 2083

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764648e+00	 sigma_n : 9.451707e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 2084

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601483e+00	 sigma_n : 8.565889e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 2085

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669820e+00	 sigma_n : 8.577266e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 2086

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709973e+00	 sigma_n : 8.550915e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 2087

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758152e+00	 sigma_n : 8.850465e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 2088

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684397e+00	 sigma_n : 9.180200e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 2089

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.440241e+00	 sigma_n : 7.510322e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 2090

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613270e+00	 sigma_n : 8.840335e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 2091

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628955e+00	 sigma_n : 8.432199e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 2092

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522901e+00	 sigma_n : 7.981188e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 2093

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.892276e+00	 sigma_n : 9.243493e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 2094

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744382e+00	 sigma_n : 9.457749e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 2095

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609689e+00	 sigma_n : 8.813537e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 2096

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580528e+00	 sigma_n : 8.747542e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 2097

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515349e+00	 sigma_n : 8.455493e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 2098

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627730e+00	 sigma_n : 8.666454e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 2099

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656759e+00	 sigma_n : 9.080403e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 Type and parameters of random generator before batch 2100 : 
	 DRAND48_RANDOM 40521 46627 54517  COUNTER	83318894


 batch number : 2100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778989e+00	 sigma_n : 8.686143e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 KEFF at step  : 2100
 keff = 9.967823e-01 sigma : 8.820871e-04
 number of batch used: 2000


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.256637e+01
*********************************************************


 Mean weight leakage = 5.735958e+02	 sigma = 3.395857e-01	 sigma% = 5.920295e-02


 Edition after batch number : 2100

******************************************************************************
RESPONSE FUNCTION : PRODUCTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	1.252593e+01	8.849345e-02


******************************************************************************
RESPONSE FUNCTION : ABSORPTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	5.384487e+00	7.483530e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	7.209802e+00	5.902650e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE_INSIDE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : NXN EXCESS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	3.314419e-02	1.183900e+00


******************************************************************************
RESPONSE FUNCTION : FLUX TOTAL
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	8.515324e+01	6.062183e-02


******************************************************************************
RESPONSE FUNCTION : ENERGY LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : KEFFS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000

 KSTEP  9.967823e-01	8.849345e-02
 KCOLL  9.964117e-01	7.044901e-02
 KTRACK 9.957296e-01	6.149765e-02

  	  estimators  			  correlations   	  combined values  	  combined sigma%
  	  KSTEP <-> KCOLL  	    	  7.973082e-01  	  9.964105e-01  	  7.044887e-02
  	  KSTEP <-> KTRACK  	    	  6.396704e-01  	  9.957967e-01  	  6.133931e-02
  	  KCOLL <-> KTRACK  	    	  7.871399e-01  	  9.958604e-01  	  6.091115e-02

  	  full combined estimator  9.958602e-01	6.091054e-02



	  KSTEP ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.967263e-01	 sigma = 8.768337e-04	 sigma% = 8.797137e-02


	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.963795e-01	 sigma = 6.981276e-04	 sigma% = 7.006644e-02


	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.956985e-01	 sigma = 6.100928e-04	 sigma% = 6.127285e-02


	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.963692e-01	 sigma = 6.950659e-04	 sigma% = 6.975987e-02


 simulation time (s) : 0


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 35819 45621 5216  COUNTER	83357360


=====================================================================
	NORMAL COMPLETION
=====================================================================
