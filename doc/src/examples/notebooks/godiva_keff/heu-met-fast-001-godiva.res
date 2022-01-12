
=====================================================================
$Id$
 hostname: is232540
 pid: 361

=====================================================================
$Id$

 HOSTNAME : is232540

 PROCESS ID is : 361

 DATE : Wed Jan 12 18:21:49 2022

 Version is tripoli4_11_1.

 git version is dba218c0aa0d9c8b8ca51198567c96ee29b5ff73 (CLEAN).

=====================================================================

 data filename = heu-met-fast-001-godiva.t4
 catalogname = /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512
 execution call = tripoli4 -s NJOY -a -c /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512 -d heu-met-fast-001-godiva.t4 -o heu-met-fast-001-godiva.res 


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


// valjean: old_name: cristal/CL12_s001_c01_geo_simple
COMMENT
NEA/NSC/DOC(95)03/II HEU-MET-FAST-001
Bare, Highly Enriched Uranium Sphere (Godiva), geometry_simple
Resultats existes   7
Experience                              1.0000   0.0010
KENO (16g Hansen-Roach)                 0.9995   0.0011
KENO (27g ENDF/B-IV)                    1.0042   0.0009
MCNP (ENDF/B-V)                         0.9968   0.0009
ONEDANT (27g ENDF/B-IV)                 1.0079   0.
MONK6B (UKNDL)                          1.0054   0.0010
KENO (299g ABBN-93)                     0.9977   0.0001
COMMENT

GEOMETRIE
TITRE

TYPE 1  SPHERE 8.7407
VOLU 1  COMBI 1 0 0 0  FINV
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
    1
    PONCTUAL 300  URANIUM   3
        U234  4.9184E-4
        U235  4.4994E-2
        U238  2.4984E-3
FIN_COMPO

GEOMCOMP
    URANIUM   1   1
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

 Total concentration of material URANIUM (1.E24at/cm3) is: 4.798424e-02


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


 initialization time (s): 1


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 4.001000e+00	 sigma_n : 1.015840e-01
	 number of secondary particules: 1461
	 number of fission neutrons: 1461

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622861e+00	 sigma_n : 8.053620e-02
	 number of secondary particules: 1443
	 number of fission neutrons: 1443

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.316701e+00	 sigma_n : 7.204460e-02
	 number of secondary particules: 1242
	 number of fission neutrons: 1242

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538647e+00	 sigma_n : 8.463510e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492228e+00	 sigma_n : 8.270951e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.937383e+00	 sigma_n : 1.010112e-01
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.391267e+00	 sigma_n : 7.794052e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755369e+00	 sigma_n : 8.931651e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592386e+00	 sigma_n : 8.656600e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777223e+00	 sigma_n : 9.334135e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 simulation time (s) : 0


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736031e+00	 sigma_n : 9.205538e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 simulation time (s) : 0


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533953e+00	 sigma_n : 8.050935e-02
	 number of secondary particules: 990
	 number of fission neutrons: 990

 simulation time (s) : 0


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777778e+00	 sigma_n : 9.428042e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 simulation time (s) : 0


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663776e+00	 sigma_n : 9.035424e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 simulation time (s) : 0


 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771947e+00	 sigma_n : 9.024635e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 simulation time (s) : 0


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694184e+00	 sigma_n : 9.338365e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 simulation time (s) : 0


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643264e+00	 sigma_n : 8.637284e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 simulation time (s) : 0


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726592e+00	 sigma_n : 9.044625e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 simulation time (s) : 0


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626642e+00	 sigma_n : 8.208435e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 simulation time (s) : 0


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753515e+00	 sigma_n : 8.850795e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 simulation time (s) : 0


 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.499093e+00	 sigma_n : 8.315408e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760427e+00	 sigma_n : 9.238635e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601098e+00	 sigma_n : 8.334085e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578195e+00	 sigma_n : 8.130938e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600000e+00	 sigma_n : 8.343681e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746556e+00	 sigma_n : 9.586204e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591727e+00	 sigma_n : 8.450647e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699634e+00	 sigma_n : 8.744261e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833808e+00	 sigma_n : 9.282966e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605354e+00	 sigma_n : 9.288221e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638522e+00	 sigma_n : 8.829877e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634361e+00	 sigma_n : 8.419195e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.335052e+00	 sigma_n : 7.432021e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720532e+00	 sigma_n : 9.356745e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707940e+00	 sigma_n : 9.015127e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805634e+00	 sigma_n : 9.405708e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696097e+00	 sigma_n : 9.068114e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 38

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595664e+00	 sigma_n : 8.484227e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 39

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.946026e+00	 sigma_n : 9.738524e-02
	 number of secondary particules: 1167
	 number of fission neutrons: 1167

 batch number : 40

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586975e+00	 sigma_n : 8.496414e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 41

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572566e+00	 sigma_n : 8.704615e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 42

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752650e+00	 sigma_n : 9.612835e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 43

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801928e+00	 sigma_n : 9.058427e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 44

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525597e+00	 sigma_n : 8.262908e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 45

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662662e+00	 sigma_n : 9.442160e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 46

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645191e+00	 sigma_n : 8.915647e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 47

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833652e+00	 sigma_n : 8.801207e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 48

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603402e+00	 sigma_n : 7.934173e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 49

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754735e+00	 sigma_n : 9.240840e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 50

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617594e+00	 sigma_n : 8.541151e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 51

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635023e+00	 sigma_n : 8.774573e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 52

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799235e+00	 sigma_n : 9.463762e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 53

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675373e+00	 sigma_n : 8.330213e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 54

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765101e+00	 sigma_n : 9.344251e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 55

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744318e+00	 sigma_n : 8.996468e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 56

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586392e+00	 sigma_n : 8.707194e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 57

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573959e+00	 sigma_n : 9.132783e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 58

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700278e+00	 sigma_n : 8.821351e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 59

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620557e+00	 sigma_n : 8.085116e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 60

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735043e+00	 sigma_n : 9.058115e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 61

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638532e+00	 sigma_n : 9.126786e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 62

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634758e+00	 sigma_n : 8.702185e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 63

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593346e+00	 sigma_n : 8.423417e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 64

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564338e+00	 sigma_n : 8.097959e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 65

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.778195e+00	 sigma_n : 9.540904e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 66

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559503e+00	 sigma_n : 8.555194e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 67

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.495928e+00	 sigma_n : 8.119375e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 68

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779628e+00	 sigma_n : 9.760541e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 69

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600726e+00	 sigma_n : 8.785240e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 70

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.907619e+00	 sigma_n : 9.593887e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 71

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541251e+00	 sigma_n : 8.127852e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 72

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759470e+00	 sigma_n : 9.344882e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 73

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687321e+00	 sigma_n : 9.013478e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 74

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675373e+00	 sigma_n : 8.905300e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 75

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748811e+00	 sigma_n : 8.867597e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 76

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791478e+00	 sigma_n : 8.865740e-02
	 number of secondary particules: 1222
	 number of fission neutrons: 1222

 batch number : 77

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.442717e+00	 sigma_n : 7.732595e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 78

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773897e+00	 sigma_n : 9.885114e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 79

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591075e+00	 sigma_n : 8.965292e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 80

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688910e+00	 sigma_n : 8.629208e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 81

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711172e+00	 sigma_n : 8.942127e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 82

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676712e+00	 sigma_n : 9.111688e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 83

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689408e+00	 sigma_n : 8.313102e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 84

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553819e+00	 sigma_n : 8.947242e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 85

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707996e+00	 sigma_n : 8.568183e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 86

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622675e+00	 sigma_n : 8.824586e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 87

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667619e+00	 sigma_n : 8.970320e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 88

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.921512e+00	 sigma_n : 1.012085e-01
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 89

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657633e+00	 sigma_n : 8.682238e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 90

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610573e+00	 sigma_n : 8.510344e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 91

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794967e+00	 sigma_n : 8.784827e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 92

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602344e+00	 sigma_n : 8.666756e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 93

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750459e+00	 sigma_n : 9.239872e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 94

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652135e+00	 sigma_n : 8.579418e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 95

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654148e+00	 sigma_n : 8.325384e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 96

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757493e+00	 sigma_n : 9.006576e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 97

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.399830e+00	 sigma_n : 7.907983e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 98

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730419e+00	 sigma_n : 9.523365e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 99

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477586e+00	 sigma_n : 8.131411e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561870e+00	 sigma_n : 8.353647e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 101

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656702e+00	 sigma_n : 8.394069e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 102

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798486e+00	 sigma_n : 9.211011e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 103

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539697e+00	 sigma_n : 7.865030e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 104

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799625e+00	 sigma_n : 8.890478e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 105

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664279e+00	 sigma_n : 8.697142e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 106

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622422e+00	 sigma_n : 8.320898e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 107

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648794e+00	 sigma_n : 9.233025e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 108

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744037e+00	 sigma_n : 9.595656e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 109

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654663e+00	 sigma_n : 8.882228e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 110

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668773e+00	 sigma_n : 9.551256e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 111

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574640e+00	 sigma_n : 8.849814e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 112

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665714e+00	 sigma_n : 8.493423e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 113

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617754e+00	 sigma_n : 8.365966e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 114

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789238e+00	 sigma_n : 9.768010e-02
	 number of secondary particules: 1176
	 number of fission neutrons: 1176

 batch number : 115

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.383830e+00	 sigma_n : 7.587680e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 116

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725338e+00	 sigma_n : 8.835282e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 117

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754537e+00	 sigma_n : 8.855329e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 118

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697138e+00	 sigma_n : 8.918576e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 119

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683186e+00	 sigma_n : 8.470042e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 120

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520463e+00	 sigma_n : 7.978242e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 121

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696203e+00	 sigma_n : 9.058302e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 122

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782337e+00	 sigma_n : 8.770146e-02
	 number of secondary particules: 1185
	 number of fission neutrons: 1185

 batch number : 123

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574684e+00	 sigma_n : 8.080749e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 124

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.457269e+00	 sigma_n : 7.745534e-02
	 number of secondary particules: 994
	 number of fission neutrons: 994

 batch number : 125

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682093e+00	 sigma_n : 8.834407e-02
	 number of secondary particules: 982
	 number of fission neutrons: 982

 batch number : 126

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.902240e+00	 sigma_n : 9.901520e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 127

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.453977e+00	 sigma_n : 8.241506e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 128

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777340e+00	 sigma_n : 8.526043e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 129

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764761e+00	 sigma_n : 8.899227e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 130

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696379e+00	 sigma_n : 8.957239e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 131

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652632e+00	 sigma_n : 8.611725e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 132

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763056e+00	 sigma_n : 9.332541e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 133

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.450313e+00	 sigma_n : 7.885077e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 134

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654649e+00	 sigma_n : 8.061246e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 135

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.484651e+00	 sigma_n : 8.890899e-02
	 number of secondary particules: 942
	 number of fission neutrons: 942

 batch number : 136

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.022293e+00	 sigma_n : 9.676821e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 137

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527596e+00	 sigma_n : 8.091233e-02
	 number of secondary particules: 985
	 number of fission neutrons: 985

 batch number : 138

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.820305e+00	 sigma_n : 9.662495e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 139

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651643e+00	 sigma_n : 8.307131e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 140

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.875984e+00	 sigma_n : 9.555688e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 141

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626838e+00	 sigma_n : 8.935404e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 142

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665414e+00	 sigma_n : 9.083863e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 143

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784986e+00	 sigma_n : 8.866471e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 144

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622727e+00	 sigma_n : 9.201934e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 145

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765455e+00	 sigma_n : 8.692068e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 146

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528765e+00	 sigma_n : 7.959825e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 147

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679853e+00	 sigma_n : 8.619552e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 148

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639450e+00	 sigma_n : 9.494917e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 149

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745686e+00	 sigma_n : 9.569545e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 150

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541114e+00	 sigma_n : 8.860156e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 151

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519856e+00	 sigma_n : 7.848036e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 152

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555759e+00	 sigma_n : 8.218301e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 153

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833500e+00	 sigma_n : 9.902578e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 154

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540271e+00	 sigma_n : 8.111409e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 155

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786744e+00	 sigma_n : 1.016047e-01
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 156

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.834264e+00	 sigma_n : 9.545594e-02
	 number of secondary particules: 1198
	 number of fission neutrons: 1198

 batch number : 157

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570117e+00	 sigma_n : 8.520861e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 158

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600531e+00	 sigma_n : 8.305493e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 159

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621818e+00	 sigma_n : 8.554505e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 160

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668813e+00	 sigma_n : 8.848537e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 161

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626463e+00	 sigma_n : 8.636301e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 162

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723118e+00	 sigma_n : 9.088098e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 163

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596730e+00	 sigma_n : 8.805717e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 164

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593159e+00	 sigma_n : 8.559969e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 165

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551477e+00	 sigma_n : 8.819503e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 166

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602844e+00	 sigma_n : 8.467461e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 167

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.909543e+00	 sigma_n : 9.674468e-02
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 168

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600342e+00	 sigma_n : 8.426783e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 169

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756732e+00	 sigma_n : 9.343837e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 170

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600881e+00	 sigma_n : 8.548750e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 171

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692810e+00	 sigma_n : 8.670908e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 172

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702025e+00	 sigma_n : 8.849205e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 173

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468840e+00	 sigma_n : 7.808023e-02
	 number of secondary particules: 970
	 number of fission neutrons: 970

 batch number : 174

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.917526e+00	 sigma_n : 1.054685e-01
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 175

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746641e+00	 sigma_n : 9.158837e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 176

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682420e+00	 sigma_n : 8.662318e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 177

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614553e+00	 sigma_n : 8.928422e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 178

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703382e+00	 sigma_n : 8.989299e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 179

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.989205e+00	 sigma_n : 9.860921e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 180

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772520e+00	 sigma_n : 8.870548e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 181

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582670e+00	 sigma_n : 8.657451e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 182

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761860e+00	 sigma_n : 9.195727e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 183

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687611e+00	 sigma_n : 9.194294e-02
	 number of secondary particules: 1193
	 number of fission neutrons: 1193

 batch number : 184

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580050e+00	 sigma_n : 8.629011e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 185

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.481795e+00	 sigma_n : 8.710243e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 186

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567084e+00	 sigma_n : 7.820881e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 187

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738205e+00	 sigma_n : 8.654720e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 188

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541854e+00	 sigma_n : 7.673681e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 189

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687384e+00	 sigma_n : 8.972923e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 190

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.406250e+00	 sigma_n : 7.915355e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 191

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.879447e+00	 sigma_n : 9.901765e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 192

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571813e+00	 sigma_n : 8.450805e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 193

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652057e+00	 sigma_n : 8.588577e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 194

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669767e+00	 sigma_n : 8.709442e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 195

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766953e+00	 sigma_n : 9.171016e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 196

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618314e+00	 sigma_n : 7.993350e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 197

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560329e+00	 sigma_n : 8.166965e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 198

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.933460e+00	 sigma_n : 9.331339e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 199

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682992e+00	 sigma_n : 9.092599e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686364e+00	 sigma_n : 9.558366e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 201

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.506849e+00	 sigma_n : 8.427999e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 202

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596878e+00	 sigma_n : 8.328283e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 203

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786517e+00	 sigma_n : 9.163742e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 204

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741993e+00	 sigma_n : 9.166993e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 205

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539373e+00	 sigma_n : 8.244068e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 206

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505068e+00	 sigma_n : 7.802874e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 207

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537625e+00	 sigma_n : 8.582910e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 208

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657870e+00	 sigma_n : 8.946025e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 209

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801869e+00	 sigma_n : 9.654694e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 210

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666078e+00	 sigma_n : 9.165716e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 211

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534452e+00	 sigma_n : 8.462955e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 212

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682023e+00	 sigma_n : 8.936660e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 213

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515817e+00	 sigma_n : 8.315116e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 214

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540390e+00	 sigma_n : 8.092681e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 215

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786187e+00	 sigma_n : 9.270926e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 216

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653775e+00	 sigma_n : 8.687891e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 217

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794626e+00	 sigma_n : 9.351547e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 218

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664783e+00	 sigma_n : 9.356667e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 219

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.894150e+00	 sigma_n : 9.802781e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 220

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489529e+00	 sigma_n : 8.182948e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 221

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717803e+00	 sigma_n : 9.049659e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 222

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784091e+00	 sigma_n : 9.488750e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 223

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719816e+00	 sigma_n : 9.227672e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 224

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603006e+00	 sigma_n : 8.727540e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 225

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635695e+00	 sigma_n : 8.992387e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 226

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629390e+00	 sigma_n : 8.992533e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 227

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651322e+00	 sigma_n : 9.170358e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 228

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.921937e+00	 sigma_n : 9.586576e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 229

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612263e+00	 sigma_n : 8.812782e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 230

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619361e+00	 sigma_n : 8.478720e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 231

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709313e+00	 sigma_n : 8.897568e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 232

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572350e+00	 sigma_n : 8.437734e-02
	 number of secondary particules: 990
	 number of fission neutrons: 990

 batch number : 233

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.904040e+00	 sigma_n : 9.965616e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 234

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571429e+00	 sigma_n : 9.001843e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 235

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814366e+00	 sigma_n : 9.511155e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 236

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645640e+00	 sigma_n : 8.501199e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 237

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571686e+00	 sigma_n : 8.709805e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 238

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656104e+00	 sigma_n : 8.312554e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 239

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697203e+00	 sigma_n : 9.319509e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 240

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732422e+00	 sigma_n : 8.839204e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 241

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748092e+00	 sigma_n : 9.035233e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 242

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682407e+00	 sigma_n : 8.296989e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 243

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.472146e+00	 sigma_n : 8.043783e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 244

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752212e+00	 sigma_n : 9.557020e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 245

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572650e+00	 sigma_n : 8.671464e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 246

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789778e+00	 sigma_n : 9.292127e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 247

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646002e+00	 sigma_n : 8.792705e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 248

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696558e+00	 sigma_n : 8.528635e-02
	 number of secondary particules: 1176
	 number of fission neutrons: 1176

 batch number : 249

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.453231e+00	 sigma_n : 8.073796e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 250

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667595e+00	 sigma_n : 8.575950e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 251

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639854e+00	 sigma_n : 8.562183e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 252

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717351e+00	 sigma_n : 9.137177e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 253

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522059e+00	 sigma_n : 8.159318e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 254

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759568e+00	 sigma_n : 8.796120e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 255

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777563e+00	 sigma_n : 9.157290e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 256

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660940e+00	 sigma_n : 8.554677e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 257

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609626e+00	 sigma_n : 9.127693e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 258

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658287e+00	 sigma_n : 8.661545e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 259

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.440072e+00	 sigma_n : 7.866320e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 260

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745247e+00	 sigma_n : 8.729602e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 261

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667575e+00	 sigma_n : 8.962501e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 262

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728519e+00	 sigma_n : 8.830616e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 263

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707295e+00	 sigma_n : 9.070348e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 264

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477391e+00	 sigma_n : 7.943167e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 265

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659070e+00	 sigma_n : 8.436053e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 266

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700985e+00	 sigma_n : 9.027098e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 267

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691336e+00	 sigma_n : 8.815730e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 268

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734731e+00	 sigma_n : 9.580616e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 269

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678040e+00	 sigma_n : 8.340177e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 270

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562610e+00	 sigma_n : 8.009817e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 271

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776852e+00	 sigma_n : 9.604304e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 272

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.419643e+00	 sigma_n : 7.742406e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 273

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714002e+00	 sigma_n : 8.968132e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 batch number : 274

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572844e+00	 sigma_n : 8.466708e-02
	 number of secondary particules: 998
	 number of fission neutrons: 998

 batch number : 275

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839679e+00	 sigma_n : 9.714669e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 276

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.844231e+00	 sigma_n : 9.194418e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 277

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.429973e+00	 sigma_n : 8.256451e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 278

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692073e+00	 sigma_n : 9.165497e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 279

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775673e+00	 sigma_n : 9.196839e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 280

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.871917e+00	 sigma_n : 9.456845e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 281

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504325e+00	 sigma_n : 7.785460e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 282

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.996132e+00	 sigma_n : 1.025549e-01
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 283

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595027e+00	 sigma_n : 8.439914e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 284

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565336e+00	 sigma_n : 8.435120e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 285

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755329e+00	 sigma_n : 9.464581e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 286

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536823e+00	 sigma_n : 8.552534e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 287

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790763e+00	 sigma_n : 8.851472e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 288

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669319e+00	 sigma_n : 8.821873e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 289

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563208e+00	 sigma_n : 8.223959e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 290

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666973e+00	 sigma_n : 8.317894e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 291

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562558e+00	 sigma_n : 8.567339e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 292

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740883e+00	 sigma_n : 9.056056e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 293

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712052e+00	 sigma_n : 8.872485e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 294

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.416889e+00	 sigma_n : 8.112241e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 295

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734165e+00	 sigma_n : 8.461000e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 296

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674462e+00	 sigma_n : 8.993676e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 297

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673713e+00	 sigma_n : 9.015795e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 298

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645872e+00	 sigma_n : 8.239894e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 299

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756629e+00	 sigma_n : 8.887801e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 300

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745134e+00	 sigma_n : 8.622048e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 301

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563620e+00	 sigma_n : 7.880932e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 302

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775735e+00	 sigma_n : 9.014910e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 303

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723091e+00	 sigma_n : 8.859481e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 304

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607985e+00	 sigma_n : 8.957271e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 305

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.885525e+00	 sigma_n : 9.703185e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 306

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581960e+00	 sigma_n : 8.741841e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 307

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675090e+00	 sigma_n : 9.273025e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 308

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682184e+00	 sigma_n : 7.910310e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 309

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511873e+00	 sigma_n : 8.092203e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 310

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787091e+00	 sigma_n : 8.804358e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 311

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769231e+00	 sigma_n : 9.002633e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 312

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525244e+00	 sigma_n : 8.302983e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 313

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689815e+00	 sigma_n : 8.672724e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 314

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702652e+00	 sigma_n : 9.720454e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 315

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674545e+00	 sigma_n : 9.052876e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 316

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701170e+00	 sigma_n : 9.077953e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 317

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533790e+00	 sigma_n : 8.700953e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 318

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652289e+00	 sigma_n : 9.209484e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 319

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718412e+00	 sigma_n : 8.790589e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 320

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562019e+00	 sigma_n : 8.278604e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 321

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589878e+00	 sigma_n : 8.177763e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 322

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615594e+00	 sigma_n : 8.582346e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 323

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708791e+00	 sigma_n : 8.793039e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 324

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.465158e+00	 sigma_n : 7.894492e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 325

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697630e+00	 sigma_n : 9.013772e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 326

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634076e+00	 sigma_n : 8.645218e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 327

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644153e+00	 sigma_n : 8.594430e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 328

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765641e+00	 sigma_n : 9.273901e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 329

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798442e+00	 sigma_n : 9.194192e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 330

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724907e+00	 sigma_n : 8.416912e-02
	 number of secondary particules: 1178
	 number of fission neutrons: 1178

 batch number : 331

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561121e+00	 sigma_n : 8.347855e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 332

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634812e+00	 sigma_n : 7.888221e-02
	 number of secondary particules: 1192
	 number of fission neutrons: 1192

 batch number : 333

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.466443e+00	 sigma_n : 8.045986e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 334

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504579e+00	 sigma_n : 8.486814e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 335

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792031e+00	 sigma_n : 9.432462e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 336

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773865e+00	 sigma_n : 8.983368e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 337

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.516544e+00	 sigma_n : 8.411509e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 338

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642857e+00	 sigma_n : 8.497135e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 339

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705939e+00	 sigma_n : 8.782421e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 340

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765977e+00	 sigma_n : 9.325839e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 341

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770209e+00	 sigma_n : 8.928594e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 342

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.823638e+00	 sigma_n : 9.011223e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 343

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691689e+00	 sigma_n : 8.851878e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 344

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528201e+00	 sigma_n : 8.064070e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 345

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696768e+00	 sigma_n : 8.919490e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 346

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605072e+00	 sigma_n : 8.963585e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 347

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687791e+00	 sigma_n : 8.868310e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 348

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571429e+00	 sigma_n : 8.120518e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 349

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587018e+00	 sigma_n : 8.040150e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 350

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756335e+00	 sigma_n : 8.842636e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 351

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793072e+00	 sigma_n : 8.977469e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 352

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.514693e+00	 sigma_n : 7.940488e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 353

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748047e+00	 sigma_n : 9.366848e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 354

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693006e+00	 sigma_n : 9.338732e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 355

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564758e+00	 sigma_n : 8.819299e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 356

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719816e+00	 sigma_n : 9.028339e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 357

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.456328e+00	 sigma_n : 7.940488e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 358

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674374e+00	 sigma_n : 8.218211e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 359

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735992e+00	 sigma_n : 9.153056e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 360

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634307e+00	 sigma_n : 8.447768e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 361

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721715e+00	 sigma_n : 8.676222e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 362

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665778e+00	 sigma_n : 8.720579e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 363

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713076e+00	 sigma_n : 8.680020e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 364

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477798e+00	 sigma_n : 8.215061e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 365

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736641e+00	 sigma_n : 9.457974e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 366

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761553e+00	 sigma_n : 9.038098e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 367

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686703e+00	 sigma_n : 8.479302e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 368

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522298e+00	 sigma_n : 8.480297e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 369

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672625e+00	 sigma_n : 9.156092e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 370

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592362e+00	 sigma_n : 8.582087e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 371

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656250e+00	 sigma_n : 8.492350e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 372

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725067e+00	 sigma_n : 9.247456e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 373

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.489344e+00	 sigma_n : 8.212081e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 374

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520699e+00	 sigma_n : 8.473200e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 375

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700193e+00	 sigma_n : 9.455182e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 376

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.544536e+00	 sigma_n : 7.992171e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 377

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655204e+00	 sigma_n : 8.754493e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 378

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630292e+00	 sigma_n : 8.643314e-02
	 number of secondary particules: 1009
	 number of fission neutrons: 1009

 batch number : 379

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764123e+00	 sigma_n : 9.351243e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 380

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674125e+00	 sigma_n : 9.437797e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 381

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684752e+00	 sigma_n : 8.543189e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 382

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737098e+00	 sigma_n : 9.729666e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 383

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727713e+00	 sigma_n : 9.271670e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 384

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599809e+00	 sigma_n : 8.985027e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 385

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694286e+00	 sigma_n : 8.938822e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 386

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669429e+00	 sigma_n : 8.919494e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 387

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.405359e+00	 sigma_n : 7.877063e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 388

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.821839e+00	 sigma_n : 9.652297e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 389

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692669e+00	 sigma_n : 9.115739e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 390

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751812e+00	 sigma_n : 8.677853e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 391

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674336e+00	 sigma_n : 8.842028e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 392

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604692e+00	 sigma_n : 8.482990e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 393

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560000e+00	 sigma_n : 8.439511e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 394

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658341e+00	 sigma_n : 9.316750e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 395

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500434e+00	 sigma_n : 8.402732e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 396

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672207e+00	 sigma_n : 8.448811e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 397

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711069e+00	 sigma_n : 8.494060e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 398

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608325e+00	 sigma_n : 7.657967e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 399

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.830366e+00	 sigma_n : 1.001321e-01
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 400

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713242e+00	 sigma_n : 8.243191e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 401

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.488749e+00	 sigma_n : 7.996485e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 402

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748778e+00	 sigma_n : 8.990344e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 403

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744786e+00	 sigma_n : 8.657743e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 404

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764414e+00	 sigma_n : 9.850954e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 405

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.970674e+00	 sigma_n : 9.710818e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 406

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632969e+00	 sigma_n : 8.646482e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 407

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.884947e+00	 sigma_n : 9.521173e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 408

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534802e+00	 sigma_n : 8.290452e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 409

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628277e+00	 sigma_n : 8.565887e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 410

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762743e+00	 sigma_n : 9.273651e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 411

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561991e+00	 sigma_n : 8.228571e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 412

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719466e+00	 sigma_n : 9.457111e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 413

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771536e+00	 sigma_n : 1.005805e-01
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 414

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595819e+00	 sigma_n : 8.452917e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 415

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675094e+00	 sigma_n : 9.002853e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 416

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743794e+00	 sigma_n : 9.327813e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 417

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584602e+00	 sigma_n : 8.877347e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 418

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737676e+00	 sigma_n : 9.387220e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 419

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502534e+00	 sigma_n : 8.408007e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 420

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590867e+00	 sigma_n : 8.685550e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 421

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609990e+00	 sigma_n : 8.260594e-02
	 number of secondary particules: 979
	 number of fission neutrons: 979

 batch number : 422

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.871297e+00	 sigma_n : 9.762798e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 423

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813453e+00	 sigma_n : 9.211360e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 424

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500868e+00	 sigma_n : 8.061000e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 425

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669733e+00	 sigma_n : 9.494017e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 426

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649770e+00	 sigma_n : 8.670979e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 427

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799438e+00	 sigma_n : 9.479547e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 428

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688494e+00	 sigma_n : 8.926496e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 429

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812559e+00	 sigma_n : 8.514798e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 430

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688300e+00	 sigma_n : 8.860087e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 431

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690634e+00	 sigma_n : 9.350866e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 432

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.845725e+00	 sigma_n : 9.985894e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 433

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.385417e+00	 sigma_n : 7.968253e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 434

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743389e+00	 sigma_n : 8.855481e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 435

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692237e+00	 sigma_n : 9.057958e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 436

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511936e+00	 sigma_n : 8.103590e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 437

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587786e+00	 sigma_n : 8.927891e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 438

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539062e+00	 sigma_n : 8.384593e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 439

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752248e+00	 sigma_n : 9.764744e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 440

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.885057e+00	 sigma_n : 9.427685e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 441

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604651e+00	 sigma_n : 8.246879e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 442

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593357e+00	 sigma_n : 8.764710e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 443

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689128e+00	 sigma_n : 8.528646e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 444

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.393414e+00	 sigma_n : 7.817445e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 445

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709000e+00	 sigma_n : 8.404393e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 446

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.742772e+00	 sigma_n : 9.181197e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 447

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.845180e+00	 sigma_n : 9.486366e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 448

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.835249e+00	 sigma_n : 9.393263e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 449

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520632e+00	 sigma_n : 8.595380e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 450

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674460e+00	 sigma_n : 8.813313e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 451

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.820151e+00	 sigma_n : 9.270902e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 452

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577624e+00	 sigma_n : 8.041518e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 453

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523316e+00	 sigma_n : 8.417397e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 454

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623684e+00	 sigma_n : 8.887209e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 455

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617261e+00	 sigma_n : 8.720646e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 456

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714697e+00	 sigma_n : 8.843087e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 457

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750951e+00	 sigma_n : 9.342676e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 458

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.851429e+00	 sigma_n : 9.217820e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 459

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.624890e+00	 sigma_n : 8.729485e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 460

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678704e+00	 sigma_n : 8.931286e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 461

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.469725e+00	 sigma_n : 7.856891e-02
	 number of secondary particules: 978
	 number of fission neutrons: 978

 batch number : 462

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764826e+00	 sigma_n : 9.331310e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 463

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769009e+00	 sigma_n : 9.237361e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 464

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678309e+00	 sigma_n : 9.088766e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 465

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.832710e+00	 sigma_n : 8.950337e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 466

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762466e+00	 sigma_n : 9.753738e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 467

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675485e+00	 sigma_n : 8.418915e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 468

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539642e+00	 sigma_n : 7.901636e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 469

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545613e+00	 sigma_n : 8.767751e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 470

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674048e+00	 sigma_n : 8.394459e-02
	 number of secondary particules: 1205
	 number of fission neutrons: 1205

 batch number : 471

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521992e+00	 sigma_n : 8.361214e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 472

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533688e+00	 sigma_n : 8.465641e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 473

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719008e+00	 sigma_n : 9.031304e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 474

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593327e+00	 sigma_n : 8.264912e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 475

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725610e+00	 sigma_n : 9.080999e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 476

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513112e+00	 sigma_n : 7.940131e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 477

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.874882e+00	 sigma_n : 9.623189e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 478

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678150e+00	 sigma_n : 9.004179e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 479

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672811e+00	 sigma_n : 8.905082e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 480

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768519e+00	 sigma_n : 8.673240e-02
	 number of secondary particules: 1185
	 number of fission neutrons: 1185

 batch number : 481

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505485e+00	 sigma_n : 8.246878e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 482

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561325e+00	 sigma_n : 8.580110e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 483

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756387e+00	 sigma_n : 8.959628e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 484

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.494465e+00	 sigma_n : 8.531518e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 485

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609037e+00	 sigma_n : 8.756530e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 486

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707602e+00	 sigma_n : 9.117521e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 487

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653021e+00	 sigma_n : 8.844459e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 488

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695695e+00	 sigma_n : 8.678160e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 489

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805582e+00	 sigma_n : 9.557135e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 490

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599809e+00	 sigma_n : 7.981879e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 491

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.912351e+00	 sigma_n : 1.008118e-01
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 492

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.528767e+00	 sigma_n : 8.412041e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 493

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743842e+00	 sigma_n : 8.748617e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 494

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559513e+00	 sigma_n : 8.504703e-02
	 number of secondary particules: 972
	 number of fission neutrons: 972

 batch number : 495

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.969136e+00	 sigma_n : 9.586140e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 496

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667877e+00	 sigma_n : 8.578343e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 497

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576676e+00	 sigma_n : 8.128170e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 498

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704478e+00	 sigma_n : 9.031970e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 499

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751201e+00	 sigma_n : 1.016407e-01
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 500

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691860e+00	 sigma_n : 8.381229e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 501

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729287e+00	 sigma_n : 8.878428e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 502

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727186e+00	 sigma_n : 9.902835e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 503

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767961e+00	 sigma_n : 9.391229e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 504

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718519e+00	 sigma_n : 9.047234e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 505

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682511e+00	 sigma_n : 8.876838e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 506

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524401e+00	 sigma_n : 8.521546e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 507

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571686e+00	 sigma_n : 8.465305e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 508

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729990e+00	 sigma_n : 8.394408e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 509

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676181e+00	 sigma_n : 9.395061e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 510

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652941e+00	 sigma_n : 9.007567e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 511

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.895418e+00	 sigma_n : 9.797302e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 512

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542803e+00	 sigma_n : 8.142022e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 513

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675778e+00	 sigma_n : 8.819732e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 514

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738764e+00	 sigma_n : 8.983268e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 515

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571043e+00	 sigma_n : 8.548613e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 516

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711927e+00	 sigma_n : 8.609017e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 517

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681695e+00	 sigma_n : 8.808794e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 518

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614695e+00	 sigma_n : 8.332884e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 519

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654128e+00	 sigma_n : 9.424250e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 520

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.829622e+00	 sigma_n : 9.089688e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 521

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628253e+00	 sigma_n : 8.694154e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 522

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672558e+00	 sigma_n : 9.349711e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 523

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655955e+00	 sigma_n : 8.658949e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 524

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759013e+00	 sigma_n : 8.728044e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 525

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661751e+00	 sigma_n : 8.834153e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 526

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765043e+00	 sigma_n : 9.409393e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 527

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561607e+00	 sigma_n : 8.151542e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 528

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.867094e+00	 sigma_n : 9.533263e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 529

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732528e+00	 sigma_n : 9.084008e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 530

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486533e+00	 sigma_n : 7.897437e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 531

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566901e+00	 sigma_n : 8.314245e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 532

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575758e+00	 sigma_n : 8.219117e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 533

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715251e+00	 sigma_n : 8.989472e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 534

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.902439e+00	 sigma_n : 1.023832e-01
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 535

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737535e+00	 sigma_n : 9.025374e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 536

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672100e+00	 sigma_n : 8.588138e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 537

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.922303e+00	 sigma_n : 9.906303e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 538

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605753e+00	 sigma_n : 9.056792e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 539

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568083e+00	 sigma_n : 8.263888e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 540

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.403282e+00	 sigma_n : 8.032545e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 541

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700971e+00	 sigma_n : 8.845058e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 542

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750929e+00	 sigma_n : 8.996147e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 543

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731794e+00	 sigma_n : 8.765525e-02
	 number of secondary particules: 1202
	 number of fission neutrons: 1202

 batch number : 544

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505824e+00	 sigma_n : 8.143067e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 545

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608656e+00	 sigma_n : 8.478084e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 546

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700687e+00	 sigma_n : 8.693387e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 547

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.894686e+00	 sigma_n : 9.783498e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 548

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631625e+00	 sigma_n : 8.717828e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 549

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523104e+00	 sigma_n : 8.251651e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 550

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536785e+00	 sigma_n : 8.386345e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 551

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607011e+00	 sigma_n : 8.604896e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 552

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594995e+00	 sigma_n : 8.306725e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 553

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693780e+00	 sigma_n : 8.973007e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 554

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771930e+00	 sigma_n : 9.659555e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 555

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600181e+00	 sigma_n : 8.619492e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 556

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695770e+00	 sigma_n : 9.049495e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 557

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.482639e+00	 sigma_n : 7.942077e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 558

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707407e+00	 sigma_n : 9.262410e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 559

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704331e+00	 sigma_n : 9.103061e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 560

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570152e+00	 sigma_n : 8.373738e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 561

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814085e+00	 sigma_n : 9.073531e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 562

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679476e+00	 sigma_n : 9.454770e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 563

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.455652e+00	 sigma_n : 7.904163e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 564

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513951e+00	 sigma_n : 8.440449e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 565

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.891098e+00	 sigma_n : 9.562111e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 566

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602993e+00	 sigma_n : 8.588197e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 567

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526505e+00	 sigma_n : 8.592370e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 568

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.490446e+00	 sigma_n : 7.837665e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 569

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770413e+00	 sigma_n : 9.417632e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 570

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663004e+00	 sigma_n : 8.853253e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 571

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590459e+00	 sigma_n : 8.251535e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 572

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814326e+00	 sigma_n : 9.183216e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 573

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697974e+00	 sigma_n : 8.702101e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 574

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686673e+00	 sigma_n : 8.605431e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 575

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531117e+00	 sigma_n : 8.171678e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 576

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.444245e+00	 sigma_n : 7.568349e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 577

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.895050e+00	 sigma_n : 9.719332e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 578

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675856e+00	 sigma_n : 9.255001e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 579

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595725e+00	 sigma_n : 8.273205e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 580

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609043e+00	 sigma_n : 8.783887e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 581

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577491e+00	 sigma_n : 8.323058e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 582

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804453e+00	 sigma_n : 9.547938e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 583

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809893e+00	 sigma_n : 8.989063e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 584

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640909e+00	 sigma_n : 8.929443e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 585

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748858e+00	 sigma_n : 9.246456e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 586

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503100e+00	 sigma_n : 7.811162e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 587

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641121e+00	 sigma_n : 8.888162e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 588

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716963e+00	 sigma_n : 9.236901e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 589

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813716e+00	 sigma_n : 9.015245e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 590

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696699e+00	 sigma_n : 8.617141e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 591

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672398e+00	 sigma_n : 8.494929e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 592

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649091e+00	 sigma_n : 8.733397e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 593

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705398e+00	 sigma_n : 8.398707e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 594

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523598e+00	 sigma_n : 8.492799e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 595

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608120e+00	 sigma_n : 8.930120e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 596

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.481778e+00	 sigma_n : 8.773264e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 597

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798077e+00	 sigma_n : 9.150444e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 598

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.721872e+00	 sigma_n : 9.297831e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 599

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722558e+00	 sigma_n : 8.454385e-02
	 number of secondary particules: 1156
	 number of fission neutrons: 1156

 batch number : 600

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604671e+00	 sigma_n : 8.699293e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 601

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.369509e+00	 sigma_n : 7.408836e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 602

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661850e+00	 sigma_n : 9.781262e-02
	 number of secondary particules: 986
	 number of fission neutrons: 986

 batch number : 603

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809331e+00	 sigma_n : 8.713638e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 604

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766329e+00	 sigma_n : 9.319408e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 605

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550265e+00	 sigma_n : 8.284746e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 606

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722222e+00	 sigma_n : 8.847319e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 607

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.475022e+00	 sigma_n : 7.959440e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 608

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533998e+00	 sigma_n : 8.179614e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 609

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790743e+00	 sigma_n : 9.811252e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 610

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633152e+00	 sigma_n : 8.420628e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 611

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776160e+00	 sigma_n : 9.545448e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 612

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709324e+00	 sigma_n : 8.843484e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 613

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715722e+00	 sigma_n : 8.579009e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 614

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.782098e+00	 sigma_n : 9.966882e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 615

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724650e+00	 sigma_n : 9.691770e-02
	 number of secondary particules: 1189
	 number of fission neutrons: 1189

 batch number : 616

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680404e+00	 sigma_n : 9.538840e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 617

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656557e+00	 sigma_n : 9.138349e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 618

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547137e+00	 sigma_n : 8.060881e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 619

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650850e+00	 sigma_n : 8.692864e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 620

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643180e+00	 sigma_n : 8.874287e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 621

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670074e+00	 sigma_n : 8.658570e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 622

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673358e+00	 sigma_n : 8.645888e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 623

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704589e+00	 sigma_n : 8.707500e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 624

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.844380e+00	 sigma_n : 9.044741e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 625

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530045e+00	 sigma_n : 8.134842e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 626

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580794e+00	 sigma_n : 8.376304e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 627

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538244e+00	 sigma_n : 7.865266e-02
	 number of secondary particules: 1022
	 number of fission neutrons: 1022

 batch number : 628

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.874755e+00	 sigma_n : 9.534601e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 629

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592593e+00	 sigma_n : 8.868396e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 630

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684893e+00	 sigma_n : 8.606055e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 631

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726534e+00	 sigma_n : 8.816517e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 632

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510823e+00	 sigma_n : 8.615126e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 633

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680633e+00	 sigma_n : 8.471035e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 634

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654171e+00	 sigma_n : 8.729379e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 635

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761860e+00	 sigma_n : 8.757675e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 636

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804813e+00	 sigma_n : 8.860392e-02
	 number of secondary particules: 1189
	 number of fission neutrons: 1189

 batch number : 637

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.416316e+00	 sigma_n : 7.786864e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 638

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708178e+00	 sigma_n : 9.081805e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 639

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655109e+00	 sigma_n : 8.819816e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 640

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773481e+00	 sigma_n : 9.777366e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 641

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693396e+00	 sigma_n : 8.824466e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 642

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637037e+00	 sigma_n : 8.479927e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 643

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759242e+00	 sigma_n : 8.955871e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 644

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688617e+00	 sigma_n : 9.084149e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 645

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614593e+00	 sigma_n : 8.810917e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 646

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.504464e+00	 sigma_n : 8.332684e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 647

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679630e+00	 sigma_n : 8.907061e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 648

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618732e+00	 sigma_n : 9.342964e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 649

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717670e+00	 sigma_n : 9.081725e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 650

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809570e+00	 sigma_n : 9.592851e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 651

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621101e+00	 sigma_n : 8.379401e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 652

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693490e+00	 sigma_n : 9.192430e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 653

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.446237e+00	 sigma_n : 8.552508e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 654

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791992e+00	 sigma_n : 9.192845e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 655

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735348e+00	 sigma_n : 9.232215e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 656

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796468e+00	 sigma_n : 8.903985e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 657

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492576e+00	 sigma_n : 7.871550e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 658

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.659555e+00	 sigma_n : 8.230118e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 659

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793436e+00	 sigma_n : 8.930558e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 660

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686220e+00	 sigma_n : 9.573170e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 661

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637708e+00	 sigma_n : 8.344338e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 662

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734637e+00	 sigma_n : 9.249593e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 663

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646491e+00	 sigma_n : 8.486018e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 664

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732432e+00	 sigma_n : 8.894001e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 665

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645018e+00	 sigma_n : 8.752374e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 666

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683830e+00	 sigma_n : 9.037209e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 667

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653394e+00	 sigma_n : 7.810637e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 668

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675627e+00	 sigma_n : 8.328185e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 669

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722370e+00	 sigma_n : 8.233971e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 670

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564767e+00	 sigma_n : 8.336214e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 671

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720175e+00	 sigma_n : 9.254906e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 672

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.379019e+00	 sigma_n : 7.710998e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 673

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791667e+00	 sigma_n : 9.191098e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 674

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738593e+00	 sigma_n : 9.369919e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 675

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621145e+00	 sigma_n : 8.843098e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 676

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569258e+00	 sigma_n : 8.796508e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 677

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535912e+00	 sigma_n : 8.252174e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 678

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809065e+00	 sigma_n : 9.673962e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 679

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808333e+00	 sigma_n : 9.875710e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 680

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666972e+00	 sigma_n : 8.191468e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 681

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.552608e+00	 sigma_n : 7.975596e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 682

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629235e+00	 sigma_n : 8.544436e-02
	 number of secondary particules: 981
	 number of fission neutrons: 981

 batch number : 683

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.873598e+00	 sigma_n : 9.857799e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 684

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716891e+00	 sigma_n : 9.009846e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 685

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678737e+00	 sigma_n : 9.355476e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 686

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813886e+00	 sigma_n : 9.137022e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 687

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586815e+00	 sigma_n : 8.527583e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 688

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732727e+00	 sigma_n : 8.972076e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 689

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717605e+00	 sigma_n : 8.638050e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 690

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620264e+00	 sigma_n : 8.962761e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 691

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615315e+00	 sigma_n : 8.800901e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 692

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591781e+00	 sigma_n : 8.337123e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 693

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760653e+00	 sigma_n : 8.997812e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 694

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.400000e+00	 sigma_n : 8.257111e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 695

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819129e+00	 sigma_n : 9.477241e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 696

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696296e+00	 sigma_n : 8.722695e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 697

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582278e+00	 sigma_n : 8.708794e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 698

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650735e+00	 sigma_n : 9.060753e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 699

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609601e+00	 sigma_n : 8.175348e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 700

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648848e+00	 sigma_n : 8.547679e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 701

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736742e+00	 sigma_n : 9.254107e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 702

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635936e+00	 sigma_n : 8.745403e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 703

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.795802e+00	 sigma_n : 9.406274e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 704

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723305e+00	 sigma_n : 8.881694e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 705

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533512e+00	 sigma_n : 8.019871e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 706

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.816248e+00	 sigma_n : 9.706333e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 707

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.838221e+00	 sigma_n : 9.888925e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 708

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634950e+00	 sigma_n : 8.848635e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 709

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862925e+00	 sigma_n : 8.964479e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 710

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649698e+00	 sigma_n : 8.613610e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 711

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670669e+00	 sigma_n : 9.278929e-02
	 number of secondary particules: 1194
	 number of fission neutrons: 1194

 batch number : 712

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.451424e+00	 sigma_n : 8.031203e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 713

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567592e+00	 sigma_n : 8.527167e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 714

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702403e+00	 sigma_n : 8.940944e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 715

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703226e+00	 sigma_n : 8.595900e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 716

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712418e+00	 sigma_n : 8.846993e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 717

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557675e+00	 sigma_n : 8.145520e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 718

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748560e+00	 sigma_n : 8.896913e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 719

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701738e+00	 sigma_n : 8.395528e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 720

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656388e+00	 sigma_n : 8.970844e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 721

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507437e+00	 sigma_n : 7.753801e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 722

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.825441e+00	 sigma_n : 8.892199e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 723

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679487e+00	 sigma_n : 8.750470e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 724

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577187e+00	 sigma_n : 8.374438e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 725

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.513465e+00	 sigma_n : 8.373887e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 726

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671963e+00	 sigma_n : 8.908631e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 727

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635097e+00	 sigma_n : 8.574236e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 728

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781731e+00	 sigma_n : 9.059912e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 729

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532727e+00	 sigma_n : 8.182417e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 730

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603113e+00	 sigma_n : 9.181527e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 731

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757310e+00	 sigma_n : 9.358530e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 732

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546458e+00	 sigma_n : 8.878466e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 733

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688427e+00	 sigma_n : 9.344791e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 734

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696970e+00	 sigma_n : 8.810679e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 735

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707692e+00	 sigma_n : 9.127935e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 736

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658790e+00	 sigma_n : 8.529438e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 737

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566981e+00	 sigma_n : 9.072789e-02
	 number of secondary particules: 991
	 number of fission neutrons: 991

 batch number : 738

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813320e+00	 sigma_n : 9.578070e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 739

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627037e+00	 sigma_n : 8.624520e-02
	 number of secondary particules: 988
	 number of fission neutrons: 988

 batch number : 740

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796559e+00	 sigma_n : 9.324218e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 741

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706220e+00	 sigma_n : 8.940669e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 742

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758157e+00	 sigma_n : 8.904646e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 743

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687791e+00	 sigma_n : 8.657990e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 744

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716682e+00	 sigma_n : 8.816921e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 745

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639699e+00	 sigma_n : 8.402870e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 746

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760496e+00	 sigma_n : 9.390072e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 747

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713649e+00	 sigma_n : 8.952693e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 748

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573814e+00	 sigma_n : 9.039270e-02
	 number of secondary particules: 1166
	 number of fission neutrons: 1166

 batch number : 749

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.415952e+00	 sigma_n : 8.113107e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 750

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665085e+00	 sigma_n : 8.489405e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 751

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822519e+00	 sigma_n : 8.983385e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 752

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594306e+00	 sigma_n : 8.537772e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 753

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566202e+00	 sigma_n : 8.304042e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 754

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632812e+00	 sigma_n : 8.993071e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 755

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652489e+00	 sigma_n : 8.657961e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 756

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657778e+00	 sigma_n : 8.638079e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 757

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473310e+00	 sigma_n : 8.704649e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 758

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649855e+00	 sigma_n : 9.070333e-02
	 number of secondary particules: 990
	 number of fission neutrons: 990

 batch number : 759

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740404e+00	 sigma_n : 8.801193e-02
	 number of secondary particules: 981
	 number of fission neutrons: 981

 batch number : 760

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.952090e+00	 sigma_n : 1.015531e-01
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 761

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811663e+00	 sigma_n : 8.965388e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 762

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732127e+00	 sigma_n : 9.120044e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 763

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798753e+00	 sigma_n : 9.633961e-02
	 number of secondary particules: 1195
	 number of fission neutrons: 1195

 batch number : 764

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.485356e+00	 sigma_n : 8.165950e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 765

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587922e+00	 sigma_n : 8.228432e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 766

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.853568e+00	 sigma_n : 9.572720e-02
	 number of secondary particules: 1176
	 number of fission neutrons: 1176

 batch number : 767

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551871e+00	 sigma_n : 8.136925e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 768

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542525e+00	 sigma_n : 8.113098e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 769

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640267e+00	 sigma_n : 8.776267e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 770

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725621e+00	 sigma_n : 9.515057e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 771

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657063e+00	 sigma_n : 8.446587e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 772

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668255e+00	 sigma_n : 9.625041e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 773

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788168e+00	 sigma_n : 9.054114e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 774

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701192e+00	 sigma_n : 9.050383e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 775

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678742e+00	 sigma_n : 8.655839e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 776

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735075e+00	 sigma_n : 9.015980e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 777

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543783e+00	 sigma_n : 8.549055e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 778

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697084e+00	 sigma_n : 9.142726e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 779

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587406e+00	 sigma_n : 8.518788e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 780

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692381e+00	 sigma_n : 9.457402e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 781

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641602e+00	 sigma_n : 8.346383e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 782

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679924e+00	 sigma_n : 8.762373e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 783

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691392e+00	 sigma_n : 8.879294e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 784

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637104e+00	 sigma_n : 8.370537e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 785

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748428e+00	 sigma_n : 9.482001e-02
	 number of secondary particules: 1206
	 number of fission neutrons: 1206

 batch number : 786

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.334992e+00	 sigma_n : 7.653596e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 787

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.403525e+00	 sigma_n : 7.754541e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 788

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.946850e+00	 sigma_n : 9.444816e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 789

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691424e+00	 sigma_n : 8.585885e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 790

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.894831e+00	 sigma_n : 9.698077e-02
	 number of secondary particules: 1219
	 number of fission neutrons: 1219

 batch number : 791

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.460656e+00	 sigma_n : 8.023986e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 792

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693192e+00	 sigma_n : 8.812205e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 793

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502161e+00	 sigma_n : 8.093517e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 794

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604186e+00	 sigma_n : 8.551709e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 795

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.950094e+00	 sigma_n : 9.963785e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 796

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.691840e+00	 sigma_n : 9.312741e-02
	 number of secondary particules: 1164
	 number of fission neutrons: 1164

 batch number : 797

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596220e+00	 sigma_n : 8.473674e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 798

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764757e+00	 sigma_n : 9.677959e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 799

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661077e+00	 sigma_n : 8.712621e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 800

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.469965e+00	 sigma_n : 8.148064e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 801

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735067e+00	 sigma_n : 9.121630e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 802

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752558e+00	 sigma_n : 9.183071e-02
	 number of secondary particules: 1163
	 number of fission neutrons: 1163

 batch number : 803

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473775e+00	 sigma_n : 8.503500e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 804

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545620e+00	 sigma_n : 8.079261e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 805

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720293e+00	 sigma_n : 8.996700e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 806

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718297e+00	 sigma_n : 8.764199e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 807

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.471681e+00	 sigma_n : 8.297551e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 808

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787172e+00	 sigma_n : 9.355425e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 809

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630897e+00	 sigma_n : 8.786734e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 810

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767331e+00	 sigma_n : 8.748318e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 811

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698029e+00	 sigma_n : 9.171629e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 812

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531797e+00	 sigma_n : 8.632279e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 813

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634634e+00	 sigma_n : 8.394092e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 814

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734787e+00	 sigma_n : 8.788639e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 815

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779676e+00	 sigma_n : 9.582818e-02
	 number of secondary particules: 1189
	 number of fission neutrons: 1189

 batch number : 816

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.405383e+00	 sigma_n : 7.777623e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 817

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540112e+00	 sigma_n : 8.277371e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 818

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610497e+00	 sigma_n : 8.826677e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 819

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669829e+00	 sigma_n : 8.685777e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 820

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.836034e+00	 sigma_n : 9.633187e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 821

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.494801e+00	 sigma_n : 8.410740e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 822

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694823e+00	 sigma_n : 8.382258e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 823

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.433333e+00	 sigma_n : 7.956851e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 824

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756387e+00	 sigma_n : 9.490730e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 825

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545537e+00	 sigma_n : 8.593824e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 826

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701061e+00	 sigma_n : 8.964372e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 827

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772727e+00	 sigma_n : 9.238134e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 828

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724693e+00	 sigma_n : 8.654793e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 829

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783956e+00	 sigma_n : 9.744163e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 830

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.435345e+00	 sigma_n : 7.702881e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 831

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810313e+00	 sigma_n : 8.911212e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 832

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.526690e+00	 sigma_n : 7.596576e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 833

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518386e+00	 sigma_n : 8.142078e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 834

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713327e+00	 sigma_n : 8.900359e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 835

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685328e+00	 sigma_n : 9.295707e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 836

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732809e+00	 sigma_n : 8.804342e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 837

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732750e+00	 sigma_n : 9.244174e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 838

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547507e+00	 sigma_n : 8.186262e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 839

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.924361e+00	 sigma_n : 9.250438e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 840

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613079e+00	 sigma_n : 8.660217e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 841

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.859390e+00	 sigma_n : 9.550605e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 842

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707136e+00	 sigma_n : 9.584653e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 843

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737185e+00	 sigma_n : 8.991695e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 844

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635674e+00	 sigma_n : 8.513423e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 845

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.960159e+00	 sigma_n : 9.848046e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 846

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578237e+00	 sigma_n : 8.887867e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 847

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683791e+00	 sigma_n : 8.509689e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 848

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.470182e+00	 sigma_n : 8.016932e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 849

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.499074e+00	 sigma_n : 8.048099e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 850

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792323e+00	 sigma_n : 9.308330e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 851

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702048e+00	 sigma_n : 8.787396e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 852

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.565574e+00	 sigma_n : 8.261871e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 853

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662226e+00	 sigma_n : 9.082354e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 854

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.835603e+00	 sigma_n : 9.614478e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 855

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589947e+00	 sigma_n : 8.689933e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 856

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462544e+00	 sigma_n : 8.256082e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 857

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729781e+00	 sigma_n : 9.213194e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 858

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723144e+00	 sigma_n : 9.115976e-02
	 number of secondary particules: 1213
	 number of fission neutrons: 1213

 batch number : 859

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.454246e+00	 sigma_n : 8.173987e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 860

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803309e+00	 sigma_n : 9.508202e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 861

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.521102e+00	 sigma_n : 7.861655e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 862

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531953e+00	 sigma_n : 8.738339e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 863

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589840e+00	 sigma_n : 8.173169e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 864

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.861328e+00	 sigma_n : 8.897130e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 865

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616778e+00	 sigma_n : 8.498462e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 866

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662476e+00	 sigma_n : 8.843336e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 867

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.924827e+00	 sigma_n : 9.636521e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 868

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697955e+00	 sigma_n : 9.613808e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 869

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713382e+00	 sigma_n : 9.160798e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 870

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639402e+00	 sigma_n : 8.468113e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 871

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.424978e+00	 sigma_n : 8.603890e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 872

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673786e+00	 sigma_n : 8.430244e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 873

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.939961e+00	 sigma_n : 9.580500e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 874

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599816e+00	 sigma_n : 8.097792e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 875

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623561e+00	 sigma_n : 8.443409e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 876

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644606e+00	 sigma_n : 7.946058e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 877

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740296e+00	 sigma_n : 9.123560e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 878

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.467972e+00	 sigma_n : 7.793042e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 879

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667304e+00	 sigma_n : 8.364813e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 880

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.892611e+00	 sigma_n : 9.799386e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 881

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586547e+00	 sigma_n : 8.321071e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 882

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598743e+00	 sigma_n : 8.631580e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 883

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667271e+00	 sigma_n : 8.985953e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 884

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607537e+00	 sigma_n : 8.921635e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 885

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676910e+00	 sigma_n : 8.845240e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 886

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702371e+00	 sigma_n : 8.828215e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 887

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741410e+00	 sigma_n : 9.437921e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 888

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661682e+00	 sigma_n : 9.223798e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 889

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789276e+00	 sigma_n : 9.947483e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 890

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628942e+00	 sigma_n : 8.900604e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 891

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679210e+00	 sigma_n : 9.176163e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 892

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660559e+00	 sigma_n : 9.389953e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 893

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.928500e+00	 sigma_n : 9.573567e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 894

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671245e+00	 sigma_n : 8.861305e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 895

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783045e+00	 sigma_n : 8.458636e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 896

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619132e+00	 sigma_n : 9.273628e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 897

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473222e+00	 sigma_n : 8.384405e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 898

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.529740e+00	 sigma_n : 8.394015e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 899

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.868918e+00	 sigma_n : 1.021693e-01
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 900

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639456e+00	 sigma_n : 8.688398e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 901

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.859961e+00	 sigma_n : 9.531611e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 902

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667297e+00	 sigma_n : 8.811539e-02
	 number of secondary particules: 1031
	 number of fission neutrons: 1031

 batch number : 903

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.985451e+00	 sigma_n : 9.493487e-02
	 number of secondary particules: 1234
	 number of fission neutrons: 1234

 batch number : 904

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.378444e+00	 sigma_n : 7.589596e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 905

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.444644e+00	 sigma_n : 7.897886e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 906

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.690233e+00	 sigma_n : 8.637583e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 907

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.517179e+00	 sigma_n : 8.505911e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 908

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677064e+00	 sigma_n : 8.731823e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 909

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679962e+00	 sigma_n : 9.319473e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 910

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800943e+00	 sigma_n : 9.973060e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 911

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655477e+00	 sigma_n : 9.207317e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 912

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603996e+00	 sigma_n : 8.503470e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 913

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.482790e+00	 sigma_n : 8.207897e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 914

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767110e+00	 sigma_n : 8.794743e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 915

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664207e+00	 sigma_n : 8.769229e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 916

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.787766e+00	 sigma_n : 9.080259e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 917

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551874e+00	 sigma_n : 8.089417e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 918

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688930e+00	 sigma_n : 8.648911e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 919

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769871e+00	 sigma_n : 9.525919e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 920

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615859e+00	 sigma_n : 9.192643e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 921

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639963e+00	 sigma_n : 8.690043e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 922

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731662e+00	 sigma_n : 8.869982e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 923

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608229e+00	 sigma_n : 8.965713e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 924

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594570e+00	 sigma_n : 8.936482e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 925

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597649e+00	 sigma_n : 8.445951e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 926

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814134e+00	 sigma_n : 9.571397e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 927

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685134e+00	 sigma_n : 8.651916e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 928

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588235e+00	 sigma_n : 8.555145e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 929

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606909e+00	 sigma_n : 8.267830e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 930

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689655e+00	 sigma_n : 9.882925e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 931

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515296e+00	 sigma_n : 8.544991e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 932

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650246e+00	 sigma_n : 8.571029e-02
	 number of secondary particules: 985
	 number of fission neutrons: 985

 batch number : 933

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.812183e+00	 sigma_n : 9.354918e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 934

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798049e+00	 sigma_n : 1.018933e-01
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 935

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583636e+00	 sigma_n : 8.831707e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 936

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.450417e+00	 sigma_n : 8.398888e-02
	 number of secondary particules: 972
	 number of fission neutrons: 972

 batch number : 937

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.930041e+00	 sigma_n : 1.022481e-01
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 938

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.529730e+00	 sigma_n : 8.566931e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 939

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630237e+00	 sigma_n : 9.119759e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 940

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.866795e+00	 sigma_n : 9.343840e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 941

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555249e+00	 sigma_n : 8.457407e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 942

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761576e+00	 sigma_n : 9.123147e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 943

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.898017e+00	 sigma_n : 9.008707e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 944

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.494801e+00	 sigma_n : 7.807382e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 945

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720370e+00	 sigma_n : 8.855077e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 946

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535316e+00	 sigma_n : 8.561061e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 947

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.968658e+00	 sigma_n : 1.027787e-01
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 948

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646113e+00	 sigma_n : 8.613538e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 949

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698398e+00	 sigma_n : 8.904522e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 950

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798670e+00	 sigma_n : 9.116844e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 951

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587873e+00	 sigma_n : 8.375081e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 952

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765138e+00	 sigma_n : 9.011737e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 953

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.406720e+00	 sigma_n : 7.759455e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 954

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781280e+00	 sigma_n : 9.545583e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 955

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598390e+00	 sigma_n : 8.387169e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 956

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578534e+00	 sigma_n : 8.276964e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 957

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672990e+00	 sigma_n : 8.900738e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 958

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610652e+00	 sigma_n : 8.484349e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 959

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654265e+00	 sigma_n : 9.257108e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 960

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622040e+00	 sigma_n : 8.432135e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 961

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761553e+00	 sigma_n : 9.145301e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 962

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744186e+00	 sigma_n : 9.012229e-02
	 number of secondary particules: 1179
	 number of fission neutrons: 1179

 batch number : 963

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.574215e+00	 sigma_n : 8.585853e-02
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 964

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553768e+00	 sigma_n : 8.496293e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 965

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576616e+00	 sigma_n : 8.360516e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 966

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750919e+00	 sigma_n : 9.119457e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 967

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751965e+00	 sigma_n : 9.762329e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 968

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533906e+00	 sigma_n : 8.748136e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 969

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710363e+00	 sigma_n : 9.009087e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 970

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613158e+00	 sigma_n : 8.685984e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 971

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770136e+00	 sigma_n : 9.518894e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 972

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591350e+00	 sigma_n : 9.087546e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 973

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700186e+00	 sigma_n : 9.269314e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 974

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663586e+00	 sigma_n : 9.517769e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 975

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695933e+00	 sigma_n : 9.187498e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 976

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.742173e+00	 sigma_n : 8.673221e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 977

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714811e+00	 sigma_n : 9.044920e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 978

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738934e+00	 sigma_n : 9.250784e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 979

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.453993e+00	 sigma_n : 7.917306e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 980

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571956e+00	 sigma_n : 8.229863e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 981

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715551e+00	 sigma_n : 8.767362e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 982

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.842054e+00	 sigma_n : 9.486500e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 983

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654949e+00	 sigma_n : 9.008423e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 984

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473778e+00	 sigma_n : 8.301589e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 985

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563567e+00	 sigma_n : 8.365635e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 986

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.822134e+00	 sigma_n : 1.010533e-01
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 987

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672711e+00	 sigma_n : 8.667164e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 988

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564906e+00	 sigma_n : 8.049226e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 989

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.569076e+00	 sigma_n : 8.736523e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 990

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596296e+00	 sigma_n : 8.368008e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 991

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797862e+00	 sigma_n : 9.974365e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 992

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717901e+00	 sigma_n : 9.915181e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 993

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.403743e+00	 sigma_n : 8.031951e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 994

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735322e+00	 sigma_n : 8.810490e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 995

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.445958e+00	 sigma_n : 8.051951e-02
	 number of secondary particules: 980
	 number of fission neutrons: 980

 batch number : 996

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.923469e+00	 sigma_n : 9.925228e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 997

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685115e+00	 sigma_n : 8.935117e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 998

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728599e+00	 sigma_n : 9.407363e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 999

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723223e+00	 sigma_n : 9.244597e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1000

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587015e+00	 sigma_n : 8.281272e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1001

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.843511e+00	 sigma_n : 9.634127e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1002

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677596e+00	 sigma_n : 8.931184e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1003

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.848826e+00	 sigma_n : 8.764564e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 1004

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531969e+00	 sigma_n : 8.273384e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 1005

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.461405e+00	 sigma_n : 8.208873e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1006

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534799e+00	 sigma_n : 8.541381e-02
	 number of secondary particules: 996
	 number of fission neutrons: 996

 batch number : 1007

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675703e+00	 sigma_n : 9.195754e-02
	 number of secondary particules: 983
	 number of fission neutrons: 983

 batch number : 1008

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.914547e+00	 sigma_n : 1.043980e-01
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1009

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.447205e+00	 sigma_n : 8.559160e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 1010

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.830009e+00	 sigma_n : 9.277448e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1011

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701333e+00	 sigma_n : 8.615346e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1012

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523508e+00	 sigma_n : 7.770808e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1013

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734674e+00	 sigma_n : 9.239407e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1014

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755251e+00	 sigma_n : 9.175982e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1015

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677187e+00	 sigma_n : 8.376821e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1016

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637590e+00	 sigma_n : 1.004387e-01
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1017

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753976e+00	 sigma_n : 9.209047e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1018

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632877e+00	 sigma_n : 8.577902e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1019

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.419355e+00	 sigma_n : 8.030063e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1020

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668616e+00	 sigma_n : 8.526337e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1021

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685769e+00	 sigma_n : 9.082213e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1022

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.322202e+00	 sigma_n : 7.612534e-02
	 number of secondary particules: 999
	 number of fission neutrons: 999

 batch number : 1023

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676677e+00	 sigma_n : 8.959146e-02
	 number of secondary particules: 987
	 number of fission neutrons: 987

 batch number : 1024

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814590e+00	 sigma_n : 9.596909e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1025

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740494e+00	 sigma_n : 9.524553e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1026

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697955e+00	 sigma_n : 8.816367e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1027

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545455e+00	 sigma_n : 8.515668e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1028

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741121e+00	 sigma_n : 8.708859e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1029

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779048e+00	 sigma_n : 9.832562e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 1030

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710117e+00	 sigma_n : 8.763241e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 1031

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646594e+00	 sigma_n : 8.755923e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 1032

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808867e+00	 sigma_n : 9.704548e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1033

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697719e+00	 sigma_n : 9.362561e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1034

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533875e+00	 sigma_n : 8.593466e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1035

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723035e+00	 sigma_n : 9.022074e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1036

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535111e+00	 sigma_n : 8.648426e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1037

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734375e+00	 sigma_n : 8.691594e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1038

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644960e+00	 sigma_n : 8.847816e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 1039

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527273e+00	 sigma_n : 8.363820e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1040

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518885e+00	 sigma_n : 8.065919e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1041

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677268e+00	 sigma_n : 8.904091e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1042

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750235e+00	 sigma_n : 8.943425e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1043

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646575e+00	 sigma_n : 8.516277e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1044

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602170e+00	 sigma_n : 8.609548e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1045

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781768e+00	 sigma_n : 9.154717e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1046

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557245e+00	 sigma_n : 8.155380e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1047

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723324e+00	 sigma_n : 8.635882e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1048

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625461e+00	 sigma_n : 8.771252e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1049

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774071e+00	 sigma_n : 9.157654e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 Type and parameters of random generator before batch 1050 : 
	 DRAND48_RANDOM 2425 44332 30574  COUNTER	41801054


 batch number : 1050

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596730e+00	 sigma_n : 8.432095e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 KEFF at step  : 1050
 keff = 9.979533e-01 sigma : 1.284318e-03
 number of batch used: 950


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.256637e+01
*********************************************************


 Mean weight leakage = 5.740539e+02	 sigma = 4.958545e-01	 sigma% = 8.637770e-02


 Edition after batch number : 1050

******************************************************************************
RESPONSE FUNCTION : PRODUCTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	1.254065e+01	1.286952e-01


******************************************************************************
RESPONSE FUNCTION : ABSORPTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	5.389025e+00	1.062735e-01


******************************************************************************
RESPONSE FUNCTION : LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	7.216110e+00	8.484649e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE_INSIDE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : NXN EXCESS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	3.314371e-02	1.678533e+00


******************************************************************************
RESPONSE FUNCTION : FLUX TOTAL
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	950	8.514086e+01	8.779111e-02


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

 KSTEP  9.979533e-01	1.286952e-01
 KCOLL  9.969499e-01	9.968725e-02
 KTRACK 9.966923e-01	8.961997e-02

  	  estimators  			  correlations   	  combined values  	  combined sigma%
  	  KSTEP <-> KCOLL  	    	  7.960564e-01  	  9.969028e-01  	  9.962475e-02
  	  KSTEP <-> KTRACK  	    	  6.082494e-01  	  9.968123e-01  	  8.907274e-02
  	  KCOLL <-> KTRACK  	    	  7.819545e-01  	  9.967596e-01  	  8.808034e-02

  	  full combined estimator  9.967475e-01	8.807245e-02



	  KSTEP ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.981901e-01	 sigma = 1.269905e-03	 sigma% = 1.272207e-01


	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.972117e-01	 sigma = 9.842751e-04	 sigma% = 9.870272e-02


	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.970388e-01	 sigma = 8.867979e-04	 sigma% = 8.894316e-02


	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 970	 keff = 9.972501e-01	 sigma = 9.861045e-04	 sigma% = 9.888237e-02


 simulation time (s) : 15


 batch number : 1051

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643592e+00	 sigma_n : 8.427810e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1052

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749038e+00	 sigma_n : 9.003579e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1053

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824645e+00	 sigma_n : 8.995803e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1054

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761773e+00	 sigma_n : 1.017364e-01
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1055

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621671e+00	 sigma_n : 8.587778e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1056

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699057e+00	 sigma_n : 9.301030e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1057

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680462e+00	 sigma_n : 9.218949e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 1058

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.826979e+00	 sigma_n : 9.069753e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1059

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634615e+00	 sigma_n : 9.331102e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1060

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739210e+00	 sigma_n : 9.082520e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1061

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562724e+00	 sigma_n : 8.757175e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1062

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547660e+00	 sigma_n : 8.326054e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1063

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.470370e+00	 sigma_n : 8.125063e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 1064

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.966000e+00	 sigma_n : 1.032449e-01
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1065

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608171e+00	 sigma_n : 8.507074e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1066

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758427e+00	 sigma_n : 9.154327e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1067

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588659e+00	 sigma_n : 8.425777e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1068

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.847786e+00	 sigma_n : 9.057884e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1069

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801630e+00	 sigma_n : 9.548159e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1070

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510898e+00	 sigma_n : 7.858993e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1071

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741121e+00	 sigma_n : 9.890552e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1072

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672575e+00	 sigma_n : 9.455135e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1073

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598579e+00	 sigma_n : 8.519615e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1074

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587456e+00	 sigma_n : 8.385389e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1075

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796703e+00	 sigma_n : 8.883013e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1076

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579279e+00	 sigma_n : 8.387737e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1077

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790112e+00	 sigma_n : 9.341935e-02
	 number of secondary particules: 1191
	 number of fission neutrons: 1191

 batch number : 1078

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.388749e+00	 sigma_n : 7.929286e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1079

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715877e+00	 sigma_n : 9.242362e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1080

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652988e+00	 sigma_n : 8.655476e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 1081

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695279e+00	 sigma_n : 9.269128e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 1082

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572289e+00	 sigma_n : 8.215894e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1083

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679499e+00	 sigma_n : 8.636123e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1084

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646057e+00	 sigma_n : 8.564442e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1085

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636364e+00	 sigma_n : 8.463263e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1086

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486611e+00	 sigma_n : 8.580071e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1087

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846680e+00	 sigma_n : 9.361717e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1088

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.630000e+00	 sigma_n : 8.448317e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1089

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.873585e+00	 sigma_n : 9.598948e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1090

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611311e+00	 sigma_n : 8.555116e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1091

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536542e+00	 sigma_n : 8.486741e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1092

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813477e+00	 sigma_n : 9.674851e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1093

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556767e+00	 sigma_n : 8.538528e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1094

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746667e+00	 sigma_n : 8.722792e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1095

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689655e+00	 sigma_n : 8.895969e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1096

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679159e+00	 sigma_n : 8.610048e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1097

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750220e+00	 sigma_n : 9.088532e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1098

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726201e+00	 sigma_n : 8.926440e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1099

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.890667e+00	 sigma_n : 9.679544e-02
	 number of secondary particules: 1194
	 number of fission neutrons: 1194

 batch number : 1100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530151e+00	 sigma_n : 8.578030e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1101

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614968e+00	 sigma_n : 8.424368e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1102

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.864943e+00	 sigma_n : 9.558165e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1103

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493934e+00	 sigma_n : 8.611188e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1104

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662037e+00	 sigma_n : 8.628360e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1105

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752399e+00	 sigma_n : 9.275363e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1106

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616071e+00	 sigma_n : 8.869322e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1107

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527804e+00	 sigma_n : 7.780596e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1108

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486590e+00	 sigma_n : 8.066252e-02
	 number of secondary particules: 1000
	 number of fission neutrons: 1000

 batch number : 1109

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669000e+00	 sigma_n : 8.983044e-02
	 number of secondary particules: 994
	 number of fission neutrons: 994

 batch number : 1110

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764588e+00	 sigma_n : 8.672002e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1111

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638114e+00	 sigma_n : 8.650246e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1112

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.830409e+00	 sigma_n : 9.572466e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1113

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668555e+00	 sigma_n : 8.974798e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1114

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719739e+00	 sigma_n : 8.699058e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1115

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599821e+00	 sigma_n : 8.126381e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1116

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621962e+00	 sigma_n : 9.216439e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1117

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553522e+00	 sigma_n : 8.022673e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1118

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.802045e+00	 sigma_n : 9.035264e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1119

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.454947e+00	 sigma_n : 7.826694e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1120

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727872e+00	 sigma_n : 9.244878e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1121

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726766e+00	 sigma_n : 8.676421e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1122

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592189e+00	 sigma_n : 8.798656e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1123

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.524790e+00	 sigma_n : 8.399382e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1124

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788086e+00	 sigma_n : 9.570509e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1125

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726246e+00	 sigma_n : 9.157671e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1126

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654356e+00	 sigma_n : 8.728002e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1127

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751916e+00	 sigma_n : 8.893617e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1128

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.868545e+00	 sigma_n : 9.328847e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1129

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572202e+00	 sigma_n : 8.380879e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1130

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653333e+00	 sigma_n : 9.161006e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 1131

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722832e+00	 sigma_n : 9.376001e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1132

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862573e+00	 sigma_n : 9.358049e-02
	 number of secondary particules: 1149
	 number of fission neutrons: 1149

 batch number : 1133

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639687e+00	 sigma_n : 8.946142e-02
	 number of secondary particules: 1168
	 number of fission neutrons: 1168

 batch number : 1134

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.449486e+00	 sigma_n : 8.044565e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1135

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628295e+00	 sigma_n : 8.372338e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1136

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649351e+00	 sigma_n : 8.264269e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1137

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789625e+00	 sigma_n : 9.798706e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1138

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560510e+00	 sigma_n : 8.663345e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1139

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656163e+00	 sigma_n : 9.443679e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1140

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650138e+00	 sigma_n : 8.744371e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1141

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677809e+00	 sigma_n : 8.603175e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1142

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761180e+00	 sigma_n : 8.776886e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1143

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477868e+00	 sigma_n : 8.069338e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 1144

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712871e+00	 sigma_n : 8.990239e-02
	 number of secondary particules: 1003
	 number of fission neutrons: 1003

 batch number : 1145

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796610e+00	 sigma_n : 9.343876e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1146

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578605e+00	 sigma_n : 8.493111e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1147

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622115e+00	 sigma_n : 8.981449e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1148

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803343e+00	 sigma_n : 9.588921e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1149

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577251e+00	 sigma_n : 9.085773e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1150

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768859e+00	 sigma_n : 9.346979e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1151

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790112e+00	 sigma_n : 9.997672e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1152

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616924e+00	 sigma_n : 8.214066e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1153

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739411e+00	 sigma_n : 9.028688e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1154

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645132e+00	 sigma_n : 8.201888e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1155

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717431e+00	 sigma_n : 8.909774e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1156

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.434464e+00	 sigma_n : 7.696372e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1157

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611324e+00	 sigma_n : 8.321596e-02
	 number of secondary particules: 1024
	 number of fission neutrons: 1024

 batch number : 1158

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714844e+00	 sigma_n : 9.015665e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1159

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709125e+00	 sigma_n : 9.357303e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1160

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748120e+00	 sigma_n : 9.340885e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1161

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640845e+00	 sigma_n : 8.737494e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1162

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631050e+00	 sigma_n : 8.828495e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1163

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706753e+00	 sigma_n : 9.159172e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1164

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681091e+00	 sigma_n : 8.791259e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1165

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.823643e+00	 sigma_n : 9.050801e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1166

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746835e+00	 sigma_n : 9.111078e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1167

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542125e+00	 sigma_n : 8.244039e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1168

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770413e+00	 sigma_n : 9.023955e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1169

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.568075e+00	 sigma_n : 8.537415e-02
	 number of secondary particules: 986
	 number of fission neutrons: 986

 batch number : 1170

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.835700e+00	 sigma_n : 9.828265e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1171

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713592e+00	 sigma_n : 8.604229e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1172

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784810e+00	 sigma_n : 9.312225e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1173

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765595e+00	 sigma_n : 9.438219e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1174

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.791513e+00	 sigma_n : 9.236215e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1175

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648720e+00	 sigma_n : 8.543790e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1176

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666667e+00	 sigma_n : 8.824868e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1177

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594995e+00	 sigma_n : 8.641520e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1178

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549719e+00	 sigma_n : 8.096317e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1179

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.867299e+00	 sigma_n : 9.356876e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1180

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541412e+00	 sigma_n : 7.988688e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1181

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720508e+00	 sigma_n : 9.041194e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1182

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546889e+00	 sigma_n : 8.194638e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1183

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805147e+00	 sigma_n : 9.338063e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1184

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.416379e+00	 sigma_n : 7.850527e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1185

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747328e+00	 sigma_n : 9.392695e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1186

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611563e+00	 sigma_n : 9.253176e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1187

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677694e+00	 sigma_n : 8.455347e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1188

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.873092e+00	 sigma_n : 9.447758e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1189

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745201e+00	 sigma_n : 9.305997e-02
	 number of secondary particules: 1169
	 number of fission neutrons: 1169

 batch number : 1190

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570573e+00	 sigma_n : 8.041055e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1191

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547471e+00	 sigma_n : 8.452899e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1192

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644590e+00	 sigma_n : 8.893829e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1193

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.815637e+00	 sigma_n : 9.074549e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1194

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613907e+00	 sigma_n : 8.670599e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1195

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645654e+00	 sigma_n : 8.376092e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1196

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.386617e+00	 sigma_n : 8.494918e-02
	 number of secondary particules: 950
	 number of fission neutrons: 950

 batch number : 1197

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805263e+00	 sigma_n : 9.401698e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1198

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664350e+00	 sigma_n : 8.642417e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1199

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639692e+00	 sigma_n : 8.275274e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1200

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752699e+00	 sigma_n : 9.293628e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1201

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680451e+00	 sigma_n : 8.986233e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1202

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656538e+00	 sigma_n : 8.819294e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1203

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801887e+00	 sigma_n : 9.685487e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1204

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477072e+00	 sigma_n : 8.316752e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1205

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619666e+00	 sigma_n : 8.901807e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1206

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751381e+00	 sigma_n : 8.480800e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1207

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546256e+00	 sigma_n : 8.243907e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1208

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611004e+00	 sigma_n : 8.827856e-02
	 number of secondary particules: 964
	 number of fission neutrons: 964

 batch number : 1209

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.836100e+00	 sigma_n : 9.358287e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 1210

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.871514e+00	 sigma_n : 9.350464e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1211

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617021e+00	 sigma_n : 8.729874e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1212

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.816808e+00	 sigma_n : 9.890622e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1213

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603175e+00	 sigma_n : 8.313254e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1214

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672968e+00	 sigma_n : 9.235653e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1215

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.836142e+00	 sigma_n : 1.027816e-01
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1216

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683422e+00	 sigma_n : 8.742182e-02
	 number of secondary particules: 1185
	 number of fission neutrons: 1185

 batch number : 1217

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.520675e+00	 sigma_n : 7.859918e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1218

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586821e+00	 sigma_n : 8.063363e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1219

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768372e+00	 sigma_n : 8.725119e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1220

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680431e+00	 sigma_n : 9.276770e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1221

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712028e+00	 sigma_n : 9.275440e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 1222

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601916e+00	 sigma_n : 8.730738e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1223

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.825243e+00	 sigma_n : 9.167672e-02
	 number of secondary particules: 1159
	 number of fission neutrons: 1159

 batch number : 1224

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551337e+00	 sigma_n : 8.636467e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1225

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604070e+00	 sigma_n : 9.247820e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1226

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632312e+00	 sigma_n : 8.513030e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1227

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.849624e+00	 sigma_n : 9.636012e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1228

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462817e+00	 sigma_n : 8.333124e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1229

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.545455e+00	 sigma_n : 8.012653e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1230

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675856e+00	 sigma_n : 8.514953e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1231

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.468750e+00	 sigma_n : 8.581306e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1232

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693659e+00	 sigma_n : 9.130349e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1233

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650000e+00	 sigma_n : 8.444692e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1234

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679630e+00	 sigma_n : 9.660399e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1235

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603653e+00	 sigma_n : 8.823312e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1236

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798068e+00	 sigma_n : 9.259079e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1237

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.466241e+00	 sigma_n : 7.950887e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 1238

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697581e+00	 sigma_n : 9.080112e-02
	 number of secondary particules: 1001
	 number of fission neutrons: 1001

 batch number : 1239

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730270e+00	 sigma_n : 8.737013e-02
	 number of secondary particules: 995
	 number of fission neutrons: 995

 batch number : 1240

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614070e+00	 sigma_n : 8.714999e-02
	 number of secondary particules: 987
	 number of fission neutrons: 987

 batch number : 1241

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.891591e+00	 sigma_n : 9.573501e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1242

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613383e+00	 sigma_n : 8.153222e-02
	 number of secondary particules: 1030
	 number of fission neutrons: 1030

 batch number : 1243

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788350e+00	 sigma_n : 9.181070e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1244

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652095e+00	 sigma_n : 8.689589e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1245

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688808e+00	 sigma_n : 9.221614e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1246

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.958055e+00	 sigma_n : 9.838897e-02
	 number of secondary particules: 1184
	 number of fission neutrons: 1184

 batch number : 1247

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.442568e+00	 sigma_n : 8.073641e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1248

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580615e+00	 sigma_n : 8.448025e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1249

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781431e+00	 sigma_n : 8.993140e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1250

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664200e+00	 sigma_n : 8.727743e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1251

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653430e+00	 sigma_n : 8.329011e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1252

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637760e+00	 sigma_n : 8.264127e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1253

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.816530e+00	 sigma_n : 8.789758e-02
	 number of secondary particules: 1179
	 number of fission neutrons: 1179

 batch number : 1254

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573367e+00	 sigma_n : 9.048917e-02
	 number of secondary particules: 1167
	 number of fission neutrons: 1167

 batch number : 1255

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534704e+00	 sigma_n : 7.884206e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1256

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650000e+00	 sigma_n : 9.082243e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 1257

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622625e+00	 sigma_n : 8.787536e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 1258

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.446087e+00	 sigma_n : 7.762586e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1259

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770583e+00	 sigma_n : 8.831160e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1260

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731409e+00	 sigma_n : 8.950306e-02
	 number of secondary particules: 1199
	 number of fission neutrons: 1199

 batch number : 1261

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.270225e+00	 sigma_n : 7.130110e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 1262

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755081e+00	 sigma_n : 8.912892e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1263

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.805061e+00	 sigma_n : 9.451856e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1264

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745717e+00	 sigma_n : 9.701165e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1265

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.539138e+00	 sigma_n : 7.965115e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1266

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717391e+00	 sigma_n : 8.854873e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1267

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730144e+00	 sigma_n : 8.859033e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1268

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662921e+00	 sigma_n : 9.049711e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1269

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706220e+00	 sigma_n : 9.173437e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1270

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612375e+00	 sigma_n : 8.863885e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1271

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711786e+00	 sigma_n : 8.935875e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1272

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.993572e+00	 sigma_n : 1.020412e-01
	 number of secondary particules: 1213
	 number of fission neutrons: 1213

 batch number : 1273

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538335e+00	 sigma_n : 8.619827e-02
	 number of secondary particules: 1203
	 number of fission neutrons: 1203

 batch number : 1274

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.492934e+00	 sigma_n : 8.436832e-02
	 number of secondary particules: 1208
	 number of fission neutrons: 1208

 batch number : 1275

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.426325e+00	 sigma_n : 7.732278e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1276

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614362e+00	 sigma_n : 8.636072e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1277

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561082e+00	 sigma_n : 8.641291e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1278

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601386e+00	 sigma_n : 8.571025e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1279

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797034e+00	 sigma_n : 9.195115e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 1280

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.433043e+00	 sigma_n : 8.147031e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1281

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.766137e+00	 sigma_n : 1.013944e-01
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1282

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776786e+00	 sigma_n : 9.191512e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1283

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.440000e+00	 sigma_n : 7.903841e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1284

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662397e+00	 sigma_n : 8.919873e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1285

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642517e+00	 sigma_n : 8.717729e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1286

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670813e+00	 sigma_n : 8.600997e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1287

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.901811e+00	 sigma_n : 9.593962e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1288

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535777e+00	 sigma_n : 7.891207e-02
	 number of secondary particules: 1128
	 number of fission neutrons: 1128

 batch number : 1289

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644504e+00	 sigma_n : 8.223240e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1290

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.432196e+00	 sigma_n : 7.891306e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1291

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615314e+00	 sigma_n : 8.650312e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1292

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657774e+00	 sigma_n : 8.694947e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1293

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.888158e+00	 sigma_n : 9.044261e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1294

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588496e+00	 sigma_n : 8.477013e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1295

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519678e+00	 sigma_n : 8.235127e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1296

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705128e+00	 sigma_n : 8.651411e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1297

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649956e+00	 sigma_n : 9.084962e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1298

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728030e+00	 sigma_n : 8.850990e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1299

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546248e+00	 sigma_n : 8.057031e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1300

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737615e+00	 sigma_n : 8.774475e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1301

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493404e+00	 sigma_n : 7.908387e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1302

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671790e+00	 sigma_n : 8.549897e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1303

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633827e+00	 sigma_n : 8.478142e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 1304

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621878e+00	 sigma_n : 8.176146e-02
	 number of secondary particules: 1177
	 number of fission neutrons: 1177

 batch number : 1305

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595582e+00	 sigma_n : 8.514012e-02
	 number of secondary particules: 1193
	 number of fission neutrons: 1193

 batch number : 1306

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.531433e+00	 sigma_n : 7.899119e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1307

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.476105e+00	 sigma_n : 8.405037e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1308

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803675e+00	 sigma_n : 8.831652e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1309

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.834608e+00	 sigma_n : 9.296273e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1310

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616500e+00	 sigma_n : 8.368684e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1311

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692308e+00	 sigma_n : 8.999156e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1312

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.589767e+00	 sigma_n : 8.509188e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1313

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533962e+00	 sigma_n : 8.102635e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 1314

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.924797e+00	 sigma_n : 9.552529e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1315

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633392e+00	 sigma_n : 8.953228e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1316

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590150e+00	 sigma_n : 8.624317e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1317

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689464e+00	 sigma_n : 9.049055e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1318

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651978e+00	 sigma_n : 9.110536e-02
	 number of secondary particules: 1142
	 number of fission neutrons: 1142

 batch number : 1319

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600701e+00	 sigma_n : 8.520554e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1320

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687050e+00	 sigma_n : 8.449904e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1321

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629234e+00	 sigma_n : 9.432160e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1322

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682364e+00	 sigma_n : 8.537284e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1323

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685950e+00	 sigma_n : 8.383113e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1324

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617431e+00	 sigma_n : 8.484783e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1325

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635701e+00	 sigma_n : 8.967555e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1326

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728464e+00	 sigma_n : 8.769299e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1327

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743686e+00	 sigma_n : 8.704179e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1328

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.522707e+00	 sigma_n : 8.456297e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1329

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698761e+00	 sigma_n : 9.370407e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1330

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.878352e+00	 sigma_n : 9.208565e-02
	 number of secondary particules: 1108
	 number of fission neutrons: 1108

 batch number : 1331

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559567e+00	 sigma_n : 8.686526e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1332

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.705653e+00	 sigma_n : 8.928261e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1333

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750722e+00	 sigma_n : 8.745394e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1334

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536832e+00	 sigma_n : 8.598641e-02
	 number of secondary particules: 984
	 number of fission neutrons: 984

 batch number : 1335

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753049e+00	 sigma_n : 9.550665e-02
	 number of secondary particules: 1029
	 number of fission neutrons: 1029

 batch number : 1336

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749271e+00	 sigma_n : 9.413308e-02
	 number of secondary particules: 1015
	 number of fission neutrons: 1015

 batch number : 1337

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.905419e+00	 sigma_n : 9.969259e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1338

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698529e+00	 sigma_n : 8.855855e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1339

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652096e+00	 sigma_n : 8.615033e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1340

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839006e+00	 sigma_n : 9.680624e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1341

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462307e+00	 sigma_n : 8.009617e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1342

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628684e+00	 sigma_n : 8.384188e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1343

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716475e+00	 sigma_n : 9.371932e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1344

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765835e+00	 sigma_n : 9.114314e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1345

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671258e+00	 sigma_n : 8.189443e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1346

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714928e+00	 sigma_n : 8.876676e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1347

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576211e+00	 sigma_n : 8.143317e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1348

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555858e+00	 sigma_n : 8.445239e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1349

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.523277e+00	 sigma_n : 8.163498e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 1350

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846766e+00	 sigma_n : 8.860915e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1351

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.802434e+00	 sigma_n : 9.212445e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1352

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551237e+00	 sigma_n : 8.292514e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1353

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749550e+00	 sigma_n : 8.873355e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1354

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613191e+00	 sigma_n : 8.426157e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1355

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.831793e+00	 sigma_n : 9.782599e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1356

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628975e+00	 sigma_n : 9.139428e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1357

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737660e+00	 sigma_n : 8.798043e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1358

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542105e+00	 sigma_n : 7.947281e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1359

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798206e+00	 sigma_n : 8.991276e-02
	 number of secondary particules: 1201
	 number of fission neutrons: 1201

 batch number : 1360

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.476270e+00	 sigma_n : 8.571900e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1361

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665751e+00	 sigma_n : 8.963032e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1362

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669460e+00	 sigma_n : 8.216337e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1363

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670132e+00	 sigma_n : 8.672935e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1364

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667932e+00	 sigma_n : 8.817902e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1365

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765774e+00	 sigma_n : 8.608118e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1366

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666031e+00	 sigma_n : 8.261543e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1367

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685634e+00	 sigma_n : 8.419668e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1368

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774312e+00	 sigma_n : 9.852486e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1369

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601641e+00	 sigma_n : 8.723209e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1370

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783859e+00	 sigma_n : 9.237319e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1371

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640249e+00	 sigma_n : 8.752603e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1372

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.458111e+00	 sigma_n : 8.097229e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1373

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839269e+00	 sigma_n : 9.575275e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1374

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575730e+00	 sigma_n : 8.252725e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1375

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800763e+00	 sigma_n : 9.109803e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1376

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583857e+00	 sigma_n : 8.231828e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1377

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633272e+00	 sigma_n : 8.622462e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1378

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.902111e+00	 sigma_n : 9.770014e-02
	 number of secondary particules: 1170
	 number of fission neutrons: 1170

 batch number : 1379

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534188e+00	 sigma_n : 8.597195e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 1380

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607639e+00	 sigma_n : 8.496738e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1381

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.412869e+00	 sigma_n : 7.526673e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1382

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.754845e+00	 sigma_n : 9.275972e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1383

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809479e+00	 sigma_n : 9.165229e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1384

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701310e+00	 sigma_n : 8.867468e-02
	 number of secondary particules: 1180
	 number of fission neutrons: 1180

 batch number : 1385

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558475e+00	 sigma_n : 8.064056e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 1386

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.295435e+00	 sigma_n : 7.531684e-02
	 number of secondary particules: 988
	 number of fission neutrons: 988

 batch number : 1387

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.786437e+00	 sigma_n : 9.730977e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1388

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.927133e+00	 sigma_n : 9.380130e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1389

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632456e+00	 sigma_n : 8.780605e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1390

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614912e+00	 sigma_n : 8.413747e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 1391

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700000e+00	 sigma_n : 9.042183e-02
	 number of secondary particules: 1187
	 number of fission neutrons: 1187

 batch number : 1392

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.529065e+00	 sigma_n : 8.418768e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1393

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.716790e+00	 sigma_n : 9.345853e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1394

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617174e+00	 sigma_n : 8.471467e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1395

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712971e+00	 sigma_n : 8.562291e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1396

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558875e+00	 sigma_n : 8.270541e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1397

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.839623e+00	 sigma_n : 9.148321e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1398

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633157e+00	 sigma_n : 8.141058e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1399

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797794e+00	 sigma_n : 8.907453e-02
	 number of secondary particules: 1150
	 number of fission neutrons: 1150

 batch number : 1400

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602609e+00	 sigma_n : 8.675650e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1401

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532127e+00	 sigma_n : 8.381122e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1402

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.848859e+00	 sigma_n : 9.535378e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1403

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625445e+00	 sigma_n : 8.738764e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1404

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796831e+00	 sigma_n : 9.082998e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1405

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646617e+00	 sigma_n : 8.606174e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1406

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696031e+00	 sigma_n : 8.274245e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 1407

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723647e+00	 sigma_n : 8.831804e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1408

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.828431e+00	 sigma_n : 9.641027e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1409

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620787e+00	 sigma_n : 8.762373e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1410

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571973e+00	 sigma_n : 8.101105e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1411

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.532181e+00	 sigma_n : 7.906087e-02
	 number of secondary particules: 966
	 number of fission neutrons: 966

 batch number : 1412

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.827122e+00	 sigma_n : 9.562530e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1413

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.902655e+00	 sigma_n : 9.662666e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1414

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665167e+00	 sigma_n : 8.940537e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1415

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642986e+00	 sigma_n : 8.901550e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1416

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653298e+00	 sigma_n : 8.707368e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1417

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.498612e+00	 sigma_n : 8.723396e-02
	 number of secondary particules: 971
	 number of fission neutrons: 971

 batch number : 1418

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.828012e+00	 sigma_n : 8.960471e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1419

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580584e+00	 sigma_n : 8.475220e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1420

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679889e+00	 sigma_n : 8.361568e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1421

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623294e+00	 sigma_n : 8.323467e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1422

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694600e+00	 sigma_n : 8.544661e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1423

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542831e+00	 sigma_n : 8.596652e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1424

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819905e+00	 sigma_n : 9.240997e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1425

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581916e+00	 sigma_n : 8.398062e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1426

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785455e+00	 sigma_n : 9.834164e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1427

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547535e+00	 sigma_n : 8.198002e-02
	 number of secondary particules: 1174
	 number of fission neutrons: 1174

 batch number : 1428

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.427110e+00	 sigma_n : 7.883947e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1429

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664540e+00	 sigma_n : 8.247638e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1430

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606088e+00	 sigma_n : 8.483088e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1431

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762970e+00	 sigma_n : 9.214912e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 1432

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.434856e+00	 sigma_n : 8.490219e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1433

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577243e+00	 sigma_n : 8.136908e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1434

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595588e+00	 sigma_n : 8.499686e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1435

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.611538e+00	 sigma_n : 8.582355e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1436

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733779e+00	 sigma_n : 8.748884e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1437

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581801e+00	 sigma_n : 8.224989e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1438

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727528e+00	 sigma_n : 9.225009e-02
	 number of secondary particules: 1038
	 number of fission neutrons: 1038

 batch number : 1439

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645472e+00	 sigma_n : 8.882928e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 1440

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681818e+00	 sigma_n : 9.484474e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1441

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.833497e+00	 sigma_n : 9.386561e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1442

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728383e+00	 sigma_n : 9.286779e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1443

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606364e+00	 sigma_n : 8.553479e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1444

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562500e+00	 sigma_n : 8.548194e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1445

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725526e+00	 sigma_n : 9.188792e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1446

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587199e+00	 sigma_n : 8.936206e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 1447

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862205e+00	 sigma_n : 1.015125e-01
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1448

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540692e+00	 sigma_n : 8.117736e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 1449

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.836755e+00	 sigma_n : 9.654818e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1450

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635426e+00	 sigma_n : 8.531647e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1451

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639752e+00	 sigma_n : 8.279840e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1452

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719444e+00	 sigma_n : 9.124474e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1453

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684803e+00	 sigma_n : 8.109486e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1454

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.450228e+00	 sigma_n : 7.464679e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 1455

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.831361e+00	 sigma_n : 9.533679e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1456

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785981e+00	 sigma_n : 9.391210e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1457

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662727e+00	 sigma_n : 9.126763e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1458

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570292e+00	 sigma_n : 8.299441e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1459

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612208e+00	 sigma_n : 8.532354e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1460

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671378e+00	 sigma_n : 8.835950e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1461

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.512389e+00	 sigma_n : 8.154011e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1462

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689189e+00	 sigma_n : 9.690874e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 1463

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731683e+00	 sigma_n : 9.206775e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1464

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736337e+00	 sigma_n : 8.950465e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1465

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.837681e+00	 sigma_n : 9.540372e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1466

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620477e+00	 sigma_n : 8.683467e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1467

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.493274e+00	 sigma_n : 7.682325e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1468

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650467e+00	 sigma_n : 9.243561e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1469

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622659e+00	 sigma_n : 8.870622e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 1470

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.818905e+00	 sigma_n : 9.526375e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1471

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693625e+00	 sigma_n : 9.180724e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1472

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558850e+00	 sigma_n : 8.450584e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1473

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810811e+00	 sigma_n : 8.941621e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1474

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696833e+00	 sigma_n : 8.758159e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1475

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735831e+00	 sigma_n : 9.268462e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1476

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689338e+00	 sigma_n : 9.487320e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1477

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560647e+00	 sigma_n : 8.030825e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1478

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602576e+00	 sigma_n : 8.608599e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1479

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746370e+00	 sigma_n : 9.205326e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1480

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650513e+00	 sigma_n : 9.667314e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1481

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651119e+00	 sigma_n : 8.654559e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1482

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711069e+00	 sigma_n : 8.779619e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1483

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603175e+00	 sigma_n : 8.609510e-02
	 number of secondary particules: 1004
	 number of fission neutrons: 1004

 batch number : 1484

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.816733e+00	 sigma_n : 9.373722e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1485

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684803e+00	 sigma_n : 8.794197e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1486

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.896080e+00	 sigma_n : 9.903483e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 1487

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593264e+00	 sigma_n : 8.093068e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1488

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.488189e+00	 sigma_n : 8.331938e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1489

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704587e+00	 sigma_n : 8.611625e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1490

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536258e+00	 sigma_n : 8.029887e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1491

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615804e+00	 sigma_n : 8.970859e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1492

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.813453e+00	 sigma_n : 8.947115e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1493

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584821e+00	 sigma_n : 8.936106e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1494

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792976e+00	 sigma_n : 8.974089e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1495

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.591320e+00	 sigma_n : 8.316754e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1496

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628753e+00	 sigma_n : 8.658467e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1497

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575619e+00	 sigma_n : 9.003770e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1498

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758454e+00	 sigma_n : 9.077057e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1499

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.560224e+00	 sigma_n : 8.533930e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1500

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693050e+00	 sigma_n : 9.311231e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1501

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666981e+00	 sigma_n : 8.539260e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1502

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654751e+00	 sigma_n : 8.761688e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1503

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682023e+00	 sigma_n : 8.854023e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1504

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535558e+00	 sigma_n : 8.603026e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1505

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595324e+00	 sigma_n : 8.151910e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1506

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715207e+00	 sigma_n : 8.849604e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1507

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755218e+00	 sigma_n : 9.773177e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1508

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518353e+00	 sigma_n : 8.467089e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1509

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582437e+00	 sigma_n : 8.490095e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1510

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612758e+00	 sigma_n : 9.099587e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1511

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724611e+00	 sigma_n : 8.817696e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1512

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497786e+00	 sigma_n : 8.541985e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1513

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649485e+00	 sigma_n : 8.596183e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1514

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703978e+00	 sigma_n : 8.719971e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1515

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.401905e+00	 sigma_n : 7.737580e-02
	 number of secondary particules: 949
	 number of fission neutrons: 949

 batch number : 1516

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796628e+00	 sigma_n : 9.425050e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1517

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.916584e+00	 sigma_n : 1.032375e-01
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1518

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668503e+00	 sigma_n : 8.689000e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1519

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632747e+00	 sigma_n : 8.680556e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1520

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700649e+00	 sigma_n : 8.797451e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1521

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570128e+00	 sigma_n : 8.367373e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1522

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.607211e+00	 sigma_n : 8.515162e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1523

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686582e+00	 sigma_n : 8.837538e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1524

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730585e+00	 sigma_n : 8.975515e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1525

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674397e+00	 sigma_n : 8.933994e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1526

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.804408e+00	 sigma_n : 8.545024e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 1527

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.423012e+00	 sigma_n : 8.260137e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1528

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588819e+00	 sigma_n : 8.268314e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1529

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581586e+00	 sigma_n : 8.387829e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1530

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781870e+00	 sigma_n : 9.055953e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1531

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.725879e+00	 sigma_n : 8.723397e-02
	 number of secondary particules: 1175
	 number of fission neutrons: 1175

 batch number : 1532

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.471489e+00	 sigma_n : 8.355609e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1533

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639631e+00	 sigma_n : 8.104954e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1534

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698669e+00	 sigma_n : 9.020927e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1535

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737094e+00	 sigma_n : 8.575687e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1536

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590009e+00	 sigma_n : 8.245654e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1537

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739450e+00	 sigma_n : 9.109426e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1538

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599634e+00	 sigma_n : 8.371819e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1539

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.846082e+00	 sigma_n : 9.286683e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 1540

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.556326e+00	 sigma_n : 8.695600e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1541

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760930e+00	 sigma_n : 9.495324e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1542

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.631673e+00	 sigma_n : 8.886287e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1543

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.497828e+00	 sigma_n : 7.888920e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1544

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683440e+00	 sigma_n : 8.536897e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1545

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616438e+00	 sigma_n : 8.429914e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1546

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.740608e+00	 sigma_n : 8.886036e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1547

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559441e+00	 sigma_n : 8.543349e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 1548

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.500868e+00	 sigma_n : 8.005610e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1549

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.463964e+00	 sigma_n : 7.591369e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1550

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689358e+00	 sigma_n : 9.026656e-02
	 number of secondary particules: 1025
	 number of fission neutrons: 1025

 batch number : 1551

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.840000e+00	 sigma_n : 8.998941e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1552

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658065e+00	 sigma_n : 8.575947e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1553

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534451e+00	 sigma_n : 8.397870e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 1554

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736016e+00	 sigma_n : 9.749385e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1555

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637979e+00	 sigma_n : 9.343413e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1556

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.893023e+00	 sigma_n : 1.005407e-01
	 number of secondary particules: 1181
	 number of fission neutrons: 1181

 batch number : 1557

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.467401e+00	 sigma_n : 7.964528e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1558

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537684e+00	 sigma_n : 8.836421e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1559

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819923e+00	 sigma_n : 9.415958e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1560

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764168e+00	 sigma_n : 8.993328e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 1561

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675347e+00	 sigma_n : 8.723568e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1562

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736185e+00	 sigma_n : 9.845475e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1563

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682218e+00	 sigma_n : 8.679970e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1564

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575293e+00	 sigma_n : 8.415849e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1565

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674908e+00	 sigma_n : 8.784538e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1566

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605263e+00	 sigma_n : 8.647759e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1567

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575838e+00	 sigma_n : 8.607434e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1568

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.790191e+00	 sigma_n : 1.014328e-01
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1569

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566379e+00	 sigma_n : 8.005796e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1570

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.460303e+00	 sigma_n : 7.771304e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1571

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588180e+00	 sigma_n : 8.365116e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1572

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643974e+00	 sigma_n : 8.697151e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1573

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614447e+00	 sigma_n : 8.725036e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1574

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694915e+00	 sigma_n : 8.838919e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1575

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706880e+00	 sigma_n : 9.151897e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1576

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.914365e+00	 sigma_n : 9.447500e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1577

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639138e+00	 sigma_n : 8.535407e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1578

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734940e+00	 sigma_n : 9.388329e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1579

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669384e+00	 sigma_n : 9.000391e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1580

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.862352e+00	 sigma_n : 9.119114e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1581

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637555e+00	 sigma_n : 8.083236e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 1582

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486344e+00	 sigma_n : 7.924946e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1583

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.474978e+00	 sigma_n : 8.163465e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1584

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768431e+00	 sigma_n : 9.190725e-02
	 number of secondary particules: 1122
	 number of fission neutrons: 1122

 batch number : 1585

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.555258e+00	 sigma_n : 8.876896e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1586

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647940e+00	 sigma_n : 8.517704e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1587

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601679e+00	 sigma_n : 9.637089e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1588

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710476e+00	 sigma_n : 9.156135e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1589

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736111e+00	 sigma_n : 8.553518e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1590

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638663e+00	 sigma_n : 8.735799e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1591

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579982e+00	 sigma_n : 8.794786e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1592

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570384e+00	 sigma_n : 7.957724e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 1593

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.803729e+00	 sigma_n : 9.288993e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1594

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636788e+00	 sigma_n : 8.551216e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1595

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761290e+00	 sigma_n : 8.962341e-02
	 number of secondary particules: 1125
	 number of fission neutrons: 1125

 batch number : 1596

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.415111e+00	 sigma_n : 7.612160e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1597

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.773585e+00	 sigma_n : 9.137551e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1598

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651402e+00	 sigma_n : 8.627002e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1599

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.932892e+00	 sigma_n : 9.766192e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1600

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.462081e+00	 sigma_n : 8.101034e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1601

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.763410e+00	 sigma_n : 9.332892e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1602

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653641e+00	 sigma_n : 8.524414e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1603

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486796e+00	 sigma_n : 8.492778e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1604

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698131e+00	 sigma_n : 9.131381e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1605

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.727516e+00	 sigma_n : 8.672422e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1606

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519231e+00	 sigma_n : 8.427817e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1607

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798303e+00	 sigma_n : 9.324659e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1608

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546329e+00	 sigma_n : 8.555687e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1609

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.775785e+00	 sigma_n : 9.143262e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1610

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563700e+00	 sigma_n : 8.759379e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1611

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.503521e+00	 sigma_n : 8.326861e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1612

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652535e+00	 sigma_n : 9.445852e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1613

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546816e+00	 sigma_n : 8.614530e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1614

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688805e+00	 sigma_n : 8.976968e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1615

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738964e+00	 sigma_n : 8.888036e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1616

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.663810e+00	 sigma_n : 9.096616e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1617

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746061e+00	 sigma_n : 8.952498e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 1618

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.537925e+00	 sigma_n : 7.835963e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1619

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.587258e+00	 sigma_n : 9.019358e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1620

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.597083e+00	 sigma_n : 8.825108e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1621

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608096e+00	 sigma_n : 8.376555e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1622

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672115e+00	 sigma_n : 8.464074e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 1623

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809477e+00	 sigma_n : 1.006644e-01
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1624

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769231e+00	 sigma_n : 9.238483e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1625

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645627e+00	 sigma_n : 8.899373e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1626

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551787e+00	 sigma_n : 8.364336e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1627

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735182e+00	 sigma_n : 8.608134e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1628

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692453e+00	 sigma_n : 9.218650e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1629

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.457987e+00	 sigma_n : 7.914892e-02
	 number of secondary particules: 1023
	 number of fission neutrons: 1023

 batch number : 1630

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.868035e+00	 sigma_n : 9.516846e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1631

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685981e+00	 sigma_n : 8.805299e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1632

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781711e+00	 sigma_n : 9.094156e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1633

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718243e+00	 sigma_n : 8.967001e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1634

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651737e+00	 sigma_n : 8.853289e-02
	 number of secondary particules: 1026
	 number of fission neutrons: 1026

 batch number : 1635

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748538e+00	 sigma_n : 9.239170e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1636

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.578807e+00	 sigma_n : 9.080647e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1637

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541176e+00	 sigma_n : 8.999556e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1638

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780331e+00	 sigma_n : 9.048248e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1639

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651943e+00	 sigma_n : 8.996745e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1640

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610063e+00	 sigma_n : 8.490823e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1641

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.722332e+00	 sigma_n : 8.930011e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1642

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810029e+00	 sigma_n : 9.218410e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1643

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645992e+00	 sigma_n : 8.461307e-02
	 number of secondary particules: 993
	 number of fission neutrons: 993

 batch number : 1644

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665660e+00	 sigma_n : 9.002281e-02
	 number of secondary particules: 995
	 number of fission neutrons: 995

 batch number : 1645

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.848241e+00	 sigma_n : 9.781122e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1646

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667917e+00	 sigma_n : 8.794371e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1647

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772305e+00	 sigma_n : 9.347713e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1648

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598935e+00	 sigma_n : 8.717935e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1649

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625795e+00	 sigma_n : 8.998127e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1650

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.967012e+00	 sigma_n : 9.687121e-02
	 number of secondary particules: 1199
	 number of fission neutrons: 1199

 batch number : 1651

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.426188e+00	 sigma_n : 8.086660e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 1652

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702678e+00	 sigma_n : 8.876182e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1653

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.518810e+00	 sigma_n : 8.309729e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1654

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635514e+00	 sigma_n : 8.375499e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1655

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621368e+00	 sigma_n : 8.882950e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1656

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 3.016997e+00	 sigma_n : 1.055808e-01
	 number of secondary particules: 1185
	 number of fission neutrons: 1185

 batch number : 1657

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563713e+00	 sigma_n : 8.218839e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1658

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712747e+00	 sigma_n : 8.855928e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 1659

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627886e+00	 sigma_n : 8.752043e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1660

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.869406e+00	 sigma_n : 9.214074e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1661

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610961e+00	 sigma_n : 8.988112e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1662

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715857e+00	 sigma_n : 9.283987e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1663

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.542986e+00	 sigma_n : 8.043287e-02
	 number of secondary particules: 1013
	 number of fission neutrons: 1013

 batch number : 1664

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728529e+00	 sigma_n : 9.089826e-02
	 number of secondary particules: 1016
	 number of fission neutrons: 1016

 batch number : 1665

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715551e+00	 sigma_n : 8.469190e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1666

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718391e+00	 sigma_n : 9.774425e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1667

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679439e+00	 sigma_n : 9.006809e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 1668

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.851167e+00	 sigma_n : 9.000318e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1669

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801896e+00	 sigma_n : 1.000265e-01
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1670

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584229e+00	 sigma_n : 8.750048e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 1671

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668255e+00	 sigma_n : 8.902343e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 1672

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703777e+00	 sigma_n : 9.115956e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1673

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656104e+00	 sigma_n : 8.410290e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 1674

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642789e+00	 sigma_n : 8.834934e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1675

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.817225e+00	 sigma_n : 9.544278e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1676

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651852e+00	 sigma_n : 7.955386e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1677

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549257e+00	 sigma_n : 8.762048e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1678

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744403e+00	 sigma_n : 9.180261e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1679

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596934e+00	 sigma_n : 8.455339e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1680

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708603e+00	 sigma_n : 9.392414e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1681

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635762e+00	 sigma_n : 8.960900e-02
	 number of secondary particules: 1036
	 number of fission neutrons: 1036

 batch number : 1682

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733591e+00	 sigma_n : 9.419813e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1683

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739962e+00	 sigma_n : 9.437349e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1684

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644737e+00	 sigma_n : 8.974595e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1685

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693234e+00	 sigma_n : 8.968349e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1686

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702655e+00	 sigma_n : 8.621164e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1687

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.814679e+00	 sigma_n : 9.139231e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 1688

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599134e+00	 sigma_n : 8.581438e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1689

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.769731e+00	 sigma_n : 9.024030e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1690

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.694595e+00	 sigma_n : 8.761458e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1691

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.708668e+00	 sigma_n : 8.850249e-02
	 number of secondary particules: 1191
	 number of fission neutrons: 1191

 batch number : 1692

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.408900e+00	 sigma_n : 8.105671e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1693

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551410e+00	 sigma_n : 8.331329e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1694

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604128e+00	 sigma_n : 8.506460e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1695

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592449e+00	 sigma_n : 8.617908e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1696

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703774e+00	 sigma_n : 8.799005e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1697

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.713274e+00	 sigma_n : 8.845106e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 1698

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.588183e+00	 sigma_n : 9.117547e-02
	 number of secondary particules: 1161
	 number of fission neutrons: 1161

 batch number : 1699

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507321e+00	 sigma_n : 8.496438e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1700

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661654e+00	 sigma_n : 8.770555e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1701

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747646e+00	 sigma_n : 8.744645e-02
	 number of secondary particules: 1092
	 number of fission neutrons: 1092

 batch number : 1702

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771978e+00	 sigma_n : 9.372842e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1703

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.711522e+00	 sigma_n : 9.927370e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1704

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655357e+00	 sigma_n : 8.580359e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1705

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.620532e+00	 sigma_n : 8.418987e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1706

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649865e+00	 sigma_n : 8.668547e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1707

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525594e+00	 sigma_n : 7.768785e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1708

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799810e+00	 sigma_n : 9.348106e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1709

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679035e+00	 sigma_n : 8.731274e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 1710

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737336e+00	 sigma_n : 9.289258e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1711

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573013e+00	 sigma_n : 8.142484e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1712

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.761994e+00	 sigma_n : 9.448768e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1713

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753308e+00	 sigma_n : 8.800230e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1714

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755782e+00	 sigma_n : 9.896995e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1715

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580269e+00	 sigma_n : 8.576058e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1716

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510295e+00	 sigma_n : 8.512566e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1717

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.570888e+00	 sigma_n : 8.277978e-02
	 number of secondary particules: 1020
	 number of fission neutrons: 1020

 batch number : 1718

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.809804e+00	 sigma_n : 9.601090e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1719

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744361e+00	 sigma_n : 8.858957e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1720

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665175e+00	 sigma_n : 8.968544e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1721

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.596380e+00	 sigma_n : 8.250450e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1722

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693989e+00	 sigma_n : 8.934582e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 1723

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.550088e+00	 sigma_n : 8.483242e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1724

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641860e+00	 sigma_n : 9.165575e-02
	 number of secondary particules: 1010
	 number of fission neutrons: 1010

 batch number : 1725

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.889109e+00	 sigma_n : 9.819126e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1726

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.828273e+00	 sigma_n : 9.597855e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1727

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541481e+00	 sigma_n : 8.027329e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1728

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621170e+00	 sigma_n : 8.307329e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 1729

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679709e+00	 sigma_n : 8.606015e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1730

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.889673e+00	 sigma_n : 9.382791e-02
	 number of secondary particules: 1206
	 number of fission neutrons: 1206

 batch number : 1731

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.519071e+00	 sigma_n : 8.169541e-02
	 number of secondary particules: 1173
	 number of fission neutrons: 1173

 batch number : 1732

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595908e+00	 sigma_n : 8.517887e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 1733

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511709e+00	 sigma_n : 8.528933e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1734

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707143e+00	 sigma_n : 9.149638e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 1735

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.566119e+00	 sigma_n : 8.632151e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1736

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562989e+00	 sigma_n : 8.280206e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1737

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.878844e+00	 sigma_n : 9.484975e-02
	 number of secondary particules: 1165
	 number of fission neutrons: 1165

 batch number : 1738

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.435193e+00	 sigma_n : 7.778267e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1739

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.828169e+00	 sigma_n : 9.686185e-02
	 number of secondary particules: 1152
	 number of fission neutrons: 1152

 batch number : 1740

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.469618e+00	 sigma_n : 7.892202e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1741

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639963e+00	 sigma_n : 8.727075e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1742

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760338e+00	 sigma_n : 9.677189e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 1743

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622201e+00	 sigma_n : 8.436685e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 1744

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627599e+00	 sigma_n : 8.771049e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1745

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575330e+00	 sigma_n : 8.717762e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1746

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632519e+00	 sigma_n : 8.728679e-02
	 number of secondary particules: 1028
	 number of fission neutrons: 1028

 batch number : 1747

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.700389e+00	 sigma_n : 9.064021e-02
	 number of secondary particules: 993
	 number of fission neutrons: 993

 batch number : 1748

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780463e+00	 sigma_n : 9.656864e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 1749

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.777994e+00	 sigma_n : 9.811434e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1750

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650614e+00	 sigma_n : 9.017491e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1751

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.824811e+00	 sigma_n : 9.111284e-02
	 number of secondary particules: 1153
	 number of fission neutrons: 1153

 batch number : 1752

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.475282e+00	 sigma_n : 8.567444e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1753

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.811553e+00	 sigma_n : 9.405483e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1754

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541958e+00	 sigma_n : 8.475959e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1755

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783439e+00	 sigma_n : 8.641188e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1756

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603896e+00	 sigma_n : 8.635513e-02
	 number of secondary particules: 1078
	 number of fission neutrons: 1078

 batch number : 1757

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.696660e+00	 sigma_n : 9.049466e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1758

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757660e+00	 sigma_n : 8.969770e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1759

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.515044e+00	 sigma_n : 8.334617e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1760

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.745005e+00	 sigma_n : 8.910400e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1761

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728015e+00	 sigma_n : 9.618964e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1762

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.756341e+00	 sigma_n : 8.977154e-02
	 number of secondary particules: 1185
	 number of fission neutrons: 1185

 batch number : 1763

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.460759e+00	 sigma_n : 8.115419e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1764

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598714e+00	 sigma_n : 8.776134e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1765

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.753183e+00	 sigma_n : 8.980935e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1766

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551971e+00	 sigma_n : 8.734836e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1767

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557656e+00	 sigma_n : 8.078874e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1768

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755258e+00	 sigma_n : 9.436416e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1769

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671963e+00	 sigma_n : 9.228693e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1770

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699535e+00	 sigma_n : 9.337293e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1771

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.719466e+00	 sigma_n : 9.066461e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1772

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792877e+00	 sigma_n : 9.126161e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1773

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677686e+00	 sigma_n : 8.437941e-02
	 number of secondary particules: 1098
	 number of fission neutrons: 1098

 batch number : 1774

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664845e+00	 sigma_n : 8.876542e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1775

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639118e+00	 sigma_n : 9.038383e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 1776

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.760870e+00	 sigma_n : 8.593773e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1777

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.649954e+00	 sigma_n : 8.794743e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 1778

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673469e+00	 sigma_n : 8.722055e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1779

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604972e+00	 sigma_n : 8.192015e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1780

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.749301e+00	 sigma_n : 9.208404e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1781

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557435e+00	 sigma_n : 7.881568e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1782

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619262e+00	 sigma_n : 8.326514e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1783

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658318e+00	 sigma_n : 8.596884e-02
	 number of secondary particules: 1147
	 number of fission neutrons: 1147

 batch number : 1784

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.510898e+00	 sigma_n : 8.259242e-02
	 number of secondary particules: 1065
	 number of fission neutrons: 1065

 batch number : 1785

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.774648e+00	 sigma_n : 9.069993e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 1786

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628571e+00	 sigma_n : 8.418191e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1787

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671171e+00	 sigma_n : 9.453407e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 1788

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729828e+00	 sigma_n : 8.915454e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1789

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.541485e+00	 sigma_n : 8.378053e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 1790

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609083e+00	 sigma_n : 8.536264e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1791

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656194e+00	 sigma_n : 8.851028e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 1792

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573490e+00	 sigma_n : 8.551252e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1793

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538191e+00	 sigma_n : 8.266326e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1794

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751678e+00	 sigma_n : 8.969049e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1795

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.796468e+00	 sigma_n : 9.551373e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1796

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592496e+00	 sigma_n : 8.595518e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1797

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699358e+00	 sigma_n : 8.865833e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1798

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584022e+00	 sigma_n : 8.165835e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1799

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768579e+00	 sigma_n : 8.854601e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1800

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651636e+00	 sigma_n : 8.710487e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1801

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.618062e+00	 sigma_n : 8.990544e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1802

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748099e+00	 sigma_n : 8.689372e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1803

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.595260e+00	 sigma_n : 8.290760e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1804

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.794145e+00	 sigma_n : 9.173707e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1805

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612961e+00	 sigma_n : 8.672651e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1806

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.732896e+00	 sigma_n : 9.185528e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 1807

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698252e+00	 sigma_n : 8.337010e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1808

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583183e+00	 sigma_n : 8.498536e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1809

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.798500e+00	 sigma_n : 9.039262e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1810

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.733628e+00	 sigma_n : 8.712838e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1811

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601227e+00	 sigma_n : 8.521549e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 1812

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.535096e+00	 sigma_n : 8.578018e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1813

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567020e+00	 sigma_n : 7.947977e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 1814

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.606589e+00	 sigma_n : 9.303945e-02
	 number of secondary particules: 1017
	 number of fission neutrons: 1017

 batch number : 1815

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.789577e+00	 sigma_n : 8.869730e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 1816

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.783836e+00	 sigma_n : 9.270637e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1817

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799267e+00	 sigma_n : 9.264549e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1818

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636617e+00	 sigma_n : 9.160735e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1819

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660465e+00	 sigma_n : 9.179717e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1820

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.829665e+00	 sigma_n : 9.233627e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1821

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672856e+00	 sigma_n : 8.440505e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1822

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592287e+00	 sigma_n : 7.833718e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1823

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637996e+00	 sigma_n : 8.579889e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 1824

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747967e+00	 sigma_n : 9.215901e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1825

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681979e+00	 sigma_n : 8.352337e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1826

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.709156e+00	 sigma_n : 8.901206e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 1827

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.581642e+00	 sigma_n : 8.196097e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1828

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633969e+00	 sigma_n : 8.812532e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1829

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.771375e+00	 sigma_n : 9.222267e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 1830

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571939e+00	 sigma_n : 8.877723e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1831

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765399e+00	 sigma_n : 9.408093e-02
	 number of secondary particules: 1172
	 number of fission neutrons: 1172

 batch number : 1832

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.554608e+00	 sigma_n : 8.389483e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1833

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.830909e+00	 sigma_n : 8.853804e-02
	 number of secondary particules: 1190
	 number of fission neutrons: 1190

 batch number : 1834

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.404202e+00	 sigma_n : 7.522446e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1835

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573905e+00	 sigma_n : 8.742185e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1836

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682569e+00	 sigma_n : 9.215241e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1837

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634652e+00	 sigma_n : 8.225806e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1838

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670778e+00	 sigma_n : 8.964328e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1839

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.807551e+00	 sigma_n : 9.024704e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1840

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.735371e+00	 sigma_n : 9.096518e-02
	 number of secondary particules: 1191
	 number of fission neutrons: 1191

 batch number : 1841

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655751e+00	 sigma_n : 9.361521e-02
	 number of secondary particules: 1171
	 number of fission neutrons: 1171

 batch number : 1842

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.547395e+00	 sigma_n : 7.863659e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1843

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.507951e+00	 sigma_n : 7.637912e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1844

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.567084e+00	 sigma_n : 8.229973e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1845

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.609865e+00	 sigma_n : 8.610593e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 1846

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759964e+00	 sigma_n : 8.724756e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 1847

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638279e+00	 sigma_n : 8.604668e-02
	 number of secondary particules: 1158
	 number of fission neutrons: 1158

 batch number : 1848

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.327288e+00	 sigma_n : 7.629522e-02
	 number of secondary particules: 1007
	 number of fission neutrons: 1007

 batch number : 1849

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.802383e+00	 sigma_n : 9.524372e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1850

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751423e+00	 sigma_n : 8.920051e-02
	 number of secondary particules: 1121
	 number of fission neutrons: 1121

 batch number : 1851

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.451383e+00	 sigma_n : 7.889861e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1852

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.599038e+00	 sigma_n : 8.730285e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1853

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.572806e+00	 sigma_n : 8.466922e-02
	 number of secondary particules: 982
	 number of fission neutrons: 982

 batch number : 1854

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.779022e+00	 sigma_n : 9.971739e-02
	 number of secondary particules: 987
	 number of fission neutrons: 987

 batch number : 1855

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.872340e+00	 sigma_n : 9.242847e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1856

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.731776e+00	 sigma_n : 8.539941e-02
	 number of secondary particules: 1145
	 number of fission neutrons: 1145

 batch number : 1857

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.477729e+00	 sigma_n : 8.226978e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1858

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.755329e+00	 sigma_n : 9.425441e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1859

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741144e+00	 sigma_n : 9.199316e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1860

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.467657e+00	 sigma_n : 8.900587e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1861

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808448e+00	 sigma_n : 9.521333e-02
	 number of secondary particules: 1062
	 number of fission neutrons: 1062

 batch number : 1862

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793785e+00	 sigma_n : 9.903697e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 1863

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637104e+00	 sigma_n : 8.045973e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1864

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.549360e+00	 sigma_n : 9.193668e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 1865

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684944e+00	 sigma_n : 8.498494e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 1866

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758555e+00	 sigma_n : 9.080483e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1867

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692596e+00	 sigma_n : 8.674712e-02
	 number of secondary particules: 1114
	 number of fission neutrons: 1114

 batch number : 1868

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.739677e+00	 sigma_n : 8.636656e-02
	 number of secondary particules: 1160
	 number of fission neutrons: 1160

 batch number : 1869

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534483e+00	 sigma_n : 8.806454e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1870

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642526e+00	 sigma_n : 7.866601e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1871

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.764313e+00	 sigma_n : 9.542141e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1872

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641527e+00	 sigma_n : 8.960639e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 1873

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.502885e+00	 sigma_n : 8.102534e-02
	 number of secondary particules: 997
	 number of fission neutrons: 997

 batch number : 1874

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.797392e+00	 sigma_n : 9.467688e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 1875

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687081e+00	 sigma_n : 8.355536e-02
	 number of secondary particules: 1076
	 number of fission neutrons: 1076

 batch number : 1876

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665428e+00	 sigma_n : 8.713153e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1877

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573543e+00	 sigma_n : 8.445084e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1878

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637394e+00	 sigma_n : 9.145271e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1879

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617998e+00	 sigma_n : 8.262688e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1880

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.825234e+00	 sigma_n : 9.227963e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1881

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.585323e+00	 sigma_n : 8.747138e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 1882

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744581e+00	 sigma_n : 9.189681e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 1883

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652214e+00	 sigma_n : 8.805151e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1884

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.832703e+00	 sigma_n : 9.543517e-02
	 number of secondary particules: 1146
	 number of fission neutrons: 1146

 batch number : 1885

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.553229e+00	 sigma_n : 9.057682e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1886

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.548094e+00	 sigma_n : 8.503317e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1887

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.625602e+00	 sigma_n : 8.844979e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1888

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.800581e+00	 sigma_n : 9.590296e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1889

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.849432e+00	 sigma_n : 9.750155e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1890

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656113e+00	 sigma_n : 9.155360e-02
	 number of secondary particules: 1136
	 number of fission neutrons: 1136

 batch number : 1891

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613556e+00	 sigma_n : 8.829277e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1892

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643933e+00	 sigma_n : 8.563384e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 1893

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.417183e+00	 sigma_n : 7.536035e-02
	 number of secondary particules: 1021
	 number of fission neutrons: 1021

 batch number : 1894

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695397e+00	 sigma_n : 9.037672e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1895

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.734733e+00	 sigma_n : 8.688010e-02
	 number of secondary particules: 1058
	 number of fission neutrons: 1058

 batch number : 1896

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699433e+00	 sigma_n : 8.447584e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1897

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.577594e+00	 sigma_n : 9.005885e-02
	 number of secondary particules: 1041
	 number of fission neutrons: 1041

 batch number : 1898

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686840e+00	 sigma_n : 9.544177e-02
	 number of secondary particules: 1037
	 number of fission neutrons: 1037

 batch number : 1899

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672131e+00	 sigma_n : 8.910839e-02
	 number of secondary particules: 1052
	 number of fission neutrons: 1052

 batch number : 1900

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.748099e+00	 sigma_n : 9.491302e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1901

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.564195e+00	 sigma_n : 8.946514e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1902

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.557129e+00	 sigma_n : 8.607600e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 1903

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746562e+00	 sigma_n : 8.948680e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 1904

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.768943e+00	 sigma_n : 9.333579e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 1905

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.473316e+00	 sigma_n : 8.405788e-02
	 number of secondary particules: 1089
	 number of fission neutrons: 1089

 batch number : 1906

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687787e+00	 sigma_n : 8.988133e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1907

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608456e+00	 sigma_n : 8.470360e-02
	 number of secondary particules: 1051
	 number of fission neutrons: 1051

 batch number : 1908

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680304e+00	 sigma_n : 8.302307e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 1909

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.750476e+00	 sigma_n : 8.634926e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 1910

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677449e+00	 sigma_n : 8.391566e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 1911

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.672525e+00	 sigma_n : 9.204897e-02
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1912

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.486758e+00	 sigma_n : 8.642443e-02
	 number of secondary particules: 967
	 number of fission neutrons: 967

 batch number : 1913

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.916236e+00	 sigma_n : 9.788473e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1914

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.736590e+00	 sigma_n : 8.869740e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 1915

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530919e+00	 sigma_n : 8.158572e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 1916

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.561261e+00	 sigma_n : 8.163341e-02
	 number of secondary particules: 1064
	 number of fission neutrons: 1064

 batch number : 1917

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656015e+00	 sigma_n : 8.566516e-02
	 number of secondary particules: 1044
	 number of fission neutrons: 1044

 batch number : 1918

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.799808e+00	 sigma_n : 9.757476e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1919

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.707339e+00	 sigma_n : 8.781521e-02
	 number of secondary particules: 1130
	 number of fission neutrons: 1130

 batch number : 1920

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.602655e+00	 sigma_n : 8.332900e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1921

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681308e+00	 sigma_n : 9.200451e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1922

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.540909e+00	 sigma_n : 7.826580e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1923

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.710325e+00	 sigma_n : 9.965417e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1924

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.706831e+00	 sigma_n : 9.040220e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1925

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.586618e+00	 sigma_n : 8.553583e-02
	 number of secondary particules: 1100
	 number of fission neutrons: 1100

 batch number : 1926

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.525455e+00	 sigma_n : 8.875145e-02
	 number of secondary particules: 1056
	 number of fission neutrons: 1056

 batch number : 1927

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712121e+00	 sigma_n : 9.139757e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 1928

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643264e+00	 sigma_n : 8.353038e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 1929

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.648113e+00	 sigma_n : 8.667809e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1930

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.488073e+00	 sigma_n : 8.279183e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1931

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.744860e+00	 sigma_n : 8.733948e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 1932

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582198e+00	 sigma_n : 8.424680e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 1933

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746954e+00	 sigma_n : 9.114811e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1934

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676498e+00	 sigma_n : 8.718182e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1935

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661001e+00	 sigma_n : 8.728077e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1936

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636877e+00	 sigma_n : 8.511190e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1937

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765524e+00	 sigma_n : 9.362416e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1938

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.619444e+00	 sigma_n : 8.121651e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1939

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.876636e+00	 sigma_n : 9.845557e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 1940

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580961e+00	 sigma_n : 8.220384e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1941

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652372e+00	 sigma_n : 9.200334e-02
	 number of secondary particules: 1085
	 number of fission neutrons: 1085

 batch number : 1942

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715207e+00	 sigma_n : 8.841915e-02
	 number of secondary particules: 1141
	 number of fission neutrons: 1141

 batch number : 1943

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583699e+00	 sigma_n : 8.347317e-02
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 1944

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.461338e+00	 sigma_n : 7.854506e-02
	 number of secondary particules: 1059
	 number of fission neutrons: 1059

 batch number : 1945

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765817e+00	 sigma_n : 9.355207e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 1946

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.576165e+00	 sigma_n : 8.457428e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1947

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697822e+00	 sigma_n : 8.853487e-02
	 number of secondary particules: 1090
	 number of fission neutrons: 1090

 batch number : 1948

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614679e+00	 sigma_n : 8.811461e-02
	 number of secondary particules: 1088
	 number of fission neutrons: 1088

 batch number : 1949

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651654e+00	 sigma_n : 8.349597e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1950

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.701097e+00	 sigma_n : 9.584001e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1951

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683040e+00	 sigma_n : 8.434894e-02
	 number of secondary particules: 1048
	 number of fission neutrons: 1048

 batch number : 1952

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665076e+00	 sigma_n : 9.494581e-02
	 number of secondary particules: 1033
	 number of fission neutrons: 1033

 batch number : 1953

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.702807e+00	 sigma_n : 9.128690e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 1954

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657058e+00	 sigma_n : 8.655662e-02
	 number of secondary particules: 1008
	 number of fission neutrons: 1008

 batch number : 1955

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.780754e+00	 sigma_n : 9.729351e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 1956

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657507e+00	 sigma_n : 8.848229e-02
	 number of secondary particules: 980
	 number of fission neutrons: 980

 batch number : 1957

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.747959e+00	 sigma_n : 9.133035e-02
	 number of secondary particules: 991
	 number of fission neutrons: 991

 batch number : 1958

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.808274e+00	 sigma_n : 9.415526e-02
	 number of secondary particules: 1046
	 number of fission neutrons: 1046

 batch number : 1959

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770554e+00	 sigma_n : 8.991389e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 1960

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.592117e+00	 sigma_n : 8.566810e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1961

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.604846e+00	 sigma_n : 8.784611e-02
	 number of secondary particules: 1035
	 number of fission neutrons: 1035

 batch number : 1962

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.785507e+00	 sigma_n : 9.347258e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 1963

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762172e+00	 sigma_n : 9.106232e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 1964

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657066e+00	 sigma_n : 8.722422e-02
	 number of secondary particules: 1148
	 number of fission neutrons: 1148

 batch number : 1965

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.714286e+00	 sigma_n : 8.694656e-02
	 number of secondary particules: 1117
	 number of fission neutrons: 1117

 batch number : 1966

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643688e+00	 sigma_n : 9.249222e-02
	 number of secondary particules: 1131
	 number of fission neutrons: 1131

 batch number : 1967

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562334e+00	 sigma_n : 8.044361e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 1968

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571930e+00	 sigma_n : 8.514362e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1969

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665424e+00	 sigma_n : 8.949538e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 1970

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.752097e+00	 sigma_n : 9.492217e-02
	 number of secondary particules: 1137
	 number of fission neutrons: 1137

 batch number : 1971

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626209e+00	 sigma_n : 8.182611e-02
	 number of secondary particules: 1157
	 number of fission neutrons: 1157

 batch number : 1972

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573034e+00	 sigma_n : 8.650704e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1973

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.759104e+00	 sigma_n : 8.523690e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 1974

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.451967e+00	 sigma_n : 7.656426e-02
	 number of secondary particules: 1006
	 number of fission neutrons: 1006

 batch number : 1975

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.844930e+00	 sigma_n : 1.041070e-01
	 number of secondary particules: 1095
	 number of fission neutrons: 1095

 batch number : 1976

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.551598e+00	 sigma_n : 8.387191e-02
	 number of secondary particules: 1074
	 number of fission neutrons: 1074

 batch number : 1977

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639665e+00	 sigma_n : 9.343949e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 1978

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674033e+00	 sigma_n : 8.931039e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1979

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720293e+00	 sigma_n : 9.156103e-02
	 number of secondary particules: 1144
	 number of fission neutrons: 1144

 batch number : 1980

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546329e+00	 sigma_n : 8.671993e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 1981

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.770344e+00	 sigma_n : 8.594667e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 1982

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.715064e+00	 sigma_n : 8.644425e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 1983

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693431e+00	 sigma_n : 8.501042e-02
	 number of secondary particules: 1071
	 number of fission neutrons: 1071

 batch number : 1984

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.704015e+00	 sigma_n : 9.734457e-02
	 number of secondary particules: 1039
	 number of fission neutrons: 1039

 batch number : 1985

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668912e+00	 sigma_n : 8.989899e-02
	 number of secondary particules: 1094
	 number of fission neutrons: 1094

 batch number : 1986

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603291e+00	 sigma_n : 8.226301e-02
	 number of secondary particules: 1043
	 number of fission neutrons: 1043

 batch number : 1987

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781400e+00	 sigma_n : 9.197716e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 1988

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.738389e+00	 sigma_n : 9.353210e-02
	 number of secondary particules: 1155
	 number of fission neutrons: 1155

 batch number : 1989

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.562771e+00	 sigma_n : 8.778854e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 1990

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741121e+00	 sigma_n : 8.815619e-02
	 number of secondary particules: 1079
	 number of fission neutrons: 1079

 batch number : 1991

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.793327e+00	 sigma_n : 9.286458e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 1992



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.107026e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.582290e+00	 sigma_n : 8.640761e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 1993

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717593e+00	 sigma_n : 8.834369e-02
	 number of secondary particules: 1063
	 number of fission neutrons: 1063

 batch number : 1994

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.718721e+00	 sigma_n : 9.270899e-02
	 number of secondary particules: 1113
	 number of fission neutrons: 1113

 batch number : 1995

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.637916e+00	 sigma_n : 8.415462e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 1996

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654596e+00	 sigma_n : 8.635368e-02
	 number of secondary particules: 1042
	 number of fission neutrons: 1042

 batch number : 1997

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.860845e+00	 sigma_n : 9.556700e-02
	 number of secondary particules: 1115
	 number of fission neutrons: 1115

 batch number : 1998

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.594619e+00	 sigma_n : 8.633692e-02
	 number of secondary particules: 1112
	 number of fission neutrons: 1112

 batch number : 1999

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.459532e+00	 sigma_n : 7.933662e-02
	 number of secondary particules: 1019
	 number of fission neutrons: 1019

 batch number : 2000

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.850834e+00	 sigma_n : 9.719348e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 2001

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669708e+00	 sigma_n : 8.823973e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 2002

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.614535e+00	 sigma_n : 7.949227e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 2003

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689228e+00	 sigma_n : 8.574514e-02
	 number of secondary particules: 1077
	 number of fission neutrons: 1077

 batch number : 2004

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.571031e+00	 sigma_n : 8.504623e-02
	 number of secondary particules: 1027
	 number of fission neutrons: 1027

 batch number : 2005

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.788911e+00	 sigma_n : 9.540293e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 2006

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.608209e+00	 sigma_n : 8.230504e-02
	 number of secondary particules: 1072
	 number of fission neutrons: 1072

 batch number : 2007

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.559701e+00	 sigma_n : 8.397460e-02
	 number of secondary particules: 1005
	 number of fission neutrons: 1005

 batch number : 2008

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.875622e+00	 sigma_n : 9.816584e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 2009

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724858e+00	 sigma_n : 8.795615e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 2010

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634378e+00	 sigma_n : 8.696695e-02
	 number of secondary particules: 1045
	 number of fission neutrons: 1045

 batch number : 2011

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.863158e+00	 sigma_n : 9.256307e-02
	 number of secondary particules: 1140
	 number of fission neutrons: 1140

 batch number : 2012

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622807e+00	 sigma_n : 8.618069e-02
	 number of secondary particules: 1116
	 number of fission neutrons: 1116

 batch number : 2013

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.605735e+00	 sigma_n : 8.760806e-02
	 number of secondary particules: 1096
	 number of fission neutrons: 1096

 batch number : 2014

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.601277e+00	 sigma_n : 8.598387e-02
	 number of secondary particules: 1049
	 number of fission neutrons: 1049

 batch number : 2015

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612965e+00	 sigma_n : 8.555491e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 2016

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629139e+00	 sigma_n : 1.003251e-01
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 2017

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527154e+00	 sigma_n : 8.317855e-02
	 number of secondary particules: 1014
	 number of fission neutrons: 1014

 batch number : 2018

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.898422e+00	 sigma_n : 9.766904e-02
	 number of secondary particules: 1127
	 number of fission neutrons: 1127

 batch number : 2019

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.616681e+00	 sigma_n : 9.075634e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 2020

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.538736e+00	 sigma_n : 8.734632e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 2021

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.767308e+00	 sigma_n : 9.025236e-02
	 number of secondary particules: 1054
	 number of fission neutrons: 1054

 batch number : 2022

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.784630e+00	 sigma_n : 9.103635e-02
	 number of secondary particules: 1060
	 number of fission neutrons: 1060

 batch number : 2023

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781132e+00	 sigma_n : 9.253125e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 batch number : 2024

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634907e+00	 sigma_n : 9.093108e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 2025

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664042e+00	 sigma_n : 8.753170e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 2026

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.600363e+00	 sigma_n : 8.914386e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 2027

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680222e+00	 sigma_n : 9.321635e-02
	 number of secondary particules: 1066
	 number of fission neutrons: 1066

 batch number : 2028

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.612570e+00	 sigma_n : 8.760527e-02
	 number of secondary particules: 1069
	 number of fission neutrons: 1069

 batch number : 2029

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627689e+00	 sigma_n : 8.747367e-02
	 number of secondary particules: 1018
	 number of fission neutrons: 1018

 batch number : 2030

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.970530e+00	 sigma_n : 1.034284e-01
	 number of secondary particules: 1151
	 number of fission neutrons: 1151

 batch number : 2031

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.530843e+00	 sigma_n : 8.629352e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 2032

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573214e+00	 sigma_n : 8.791199e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 2033

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699630e+00	 sigma_n : 8.411385e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 2034

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.558226e+00	 sigma_n : 7.630862e-02
	 number of secondary particules: 1040
	 number of fission neutrons: 1040

 batch number : 2035

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.712500e+00	 sigma_n : 9.034126e-02
	 number of secondary particules: 1097
	 number of fission neutrons: 1097

 batch number : 2036

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636281e+00	 sigma_n : 9.064069e-02
	 number of secondary particules: 1135
	 number of fission neutrons: 1135

 batch number : 2037

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511894e+00	 sigma_n : 8.294769e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 2038

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687904e+00	 sigma_n : 9.160188e-02
	 number of secondary particules: 1075
	 number of fission neutrons: 1075

 batch number : 2039

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.792558e+00	 sigma_n : 9.484911e-02
	 number of secondary particules: 1154
	 number of fission neutrons: 1154

 batch number : 2040

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.580589e+00	 sigma_n : 8.819252e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 2041

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.627843e+00	 sigma_n : 8.645181e-02
	 number of secondary particules: 1081
	 number of fission neutrons: 1081

 batch number : 2042

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.676226e+00	 sigma_n : 9.001947e-02
	 number of secondary particules: 1082
	 number of fission neutrons: 1082

 batch number : 2043

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.757856e+00	 sigma_n : 9.227239e-02
	 number of secondary particules: 1124
	 number of fission neutrons: 1124

 batch number : 2044

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.536477e+00	 sigma_n : 8.200059e-02
	 number of secondary particules: 993
	 number of fission neutrons: 993

 batch number : 2045

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.776435e+00	 sigma_n : 9.099509e-02
	 number of secondary particules: 1083
	 number of fission neutrons: 1083

 batch number : 2046

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.772853e+00	 sigma_n : 9.044689e-02
	 number of secondary particules: 1133
	 number of fission neutrons: 1133

 batch number : 2047

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615181e+00	 sigma_n : 8.533759e-02
	 number of secondary particules: 1143
	 number of fission neutrons: 1143

 batch number : 2048

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.575678e+00	 sigma_n : 8.289356e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 2049

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613987e+00	 sigma_n : 8.996804e-02
	 number of secondary particules: 1067
	 number of fission neutrons: 1067

 batch number : 2050

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.726592e+00	 sigma_n : 8.866285e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 2051

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.590372e+00	 sigma_n : 8.239589e-02
	 number of secondary particules: 1093
	 number of fission neutrons: 1093

 batch number : 2052

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.741080e+00	 sigma_n : 8.852601e-02
	 number of secondary particules: 1119
	 number of fission neutrons: 1119

 batch number : 2053

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.697945e+00	 sigma_n : 9.335020e-02
	 number of secondary particules: 1106
	 number of fission neutrons: 1106

 batch number : 2054

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.751356e+00	 sigma_n : 8.955966e-02
	 number of secondary particules: 1129
	 number of fission neutrons: 1129

 batch number : 2055

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.584588e+00	 sigma_n : 8.494015e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 2056

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.505126e+00	 sigma_n : 8.358507e-02
	 number of secondary particules: 992
	 number of fission neutrons: 992

 batch number : 2057

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765121e+00	 sigma_n : 9.383672e-02
	 number of secondary particules: 1057
	 number of fission neutrons: 1057

 batch number : 2058

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.762535e+00	 sigma_n : 9.254347e-02
	 number of secondary particules: 1084
	 number of fission neutrons: 1084

 batch number : 2059

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.699262e+00	 sigma_n : 8.566885e-02
	 number of secondary particules: 1091
	 number of fission neutrons: 1091

 batch number : 2060

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527956e+00	 sigma_n : 8.130890e-02
	 number of secondary particules: 1047
	 number of fission neutrons: 1047

 batch number : 2061

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.819484e+00	 sigma_n : 9.938295e-02
	 number of secondary particules: 1118
	 number of fission neutrons: 1118

 batch number : 2062

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.435599e+00	 sigma_n : 8.087854e-02
	 number of secondary particules: 1012
	 number of fission neutrons: 1012

 batch number : 2063

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645257e+00	 sigma_n : 9.063997e-02
	 number of secondary particules: 1011
	 number of fission neutrons: 1011

 batch number : 2064

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680514e+00	 sigma_n : 8.738763e-02
	 number of secondary particules: 1032
	 number of fission neutrons: 1032

 batch number : 2065

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730620e+00	 sigma_n : 9.060769e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 2066

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.717143e+00	 sigma_n : 8.858285e-02
	 number of secondary particules: 1120
	 number of fission neutrons: 1120

 batch number : 2067

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638393e+00	 sigma_n : 8.600599e-02
	 number of secondary particules: 1099
	 number of fission neutrons: 1099

 batch number : 2068

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.583258e+00	 sigma_n : 8.331969e-02
	 number of secondary particules: 1070
	 number of fission neutrons: 1070

 batch number : 2069

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.698131e+00	 sigma_n : 8.375314e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 2070

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.801498e+00	 sigma_n : 9.650040e-02
	 number of secondary particules: 1162
	 number of fission neutrons: 1162

 batch number : 2071

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635112e+00	 sigma_n : 8.786511e-02
	 number of secondary particules: 1109
	 number of fission neutrons: 1109

 batch number : 2072

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665464e+00	 sigma_n : 8.948234e-02
	 number of secondary particules: 1068
	 number of fission neutrons: 1068

 batch number : 2073

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743446e+00	 sigma_n : 9.344095e-02
	 number of secondary particules: 1139
	 number of fission neutrons: 1139

 batch number : 2074

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.511853e+00	 sigma_n : 8.012058e-02
	 number of secondary particules: 1053
	 number of fission neutrons: 1053

 batch number : 2075

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.723647e+00	 sigma_n : 9.219865e-02
	 number of secondary particules: 1102
	 number of fission neutrons: 1102

 batch number : 2076

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.650635e+00	 sigma_n : 8.688156e-02
	 number of secondary particules: 1110
	 number of fission neutrons: 1110

 batch number : 2077

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623423e+00	 sigma_n : 8.965441e-02
	 number of secondary particules: 1107
	 number of fission neutrons: 1107

 batch number : 2078

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.729901e+00	 sigma_n : 8.611867e-02
	 number of secondary particules: 1182
	 number of fission neutrons: 1182

 batch number : 2079

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.593909e+00	 sigma_n : 8.356097e-02
	 number of secondary particules: 1138
	 number of fission neutrons: 1138

 batch number : 2080

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.543937e+00	 sigma_n : 8.115721e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 2081

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.633726e+00	 sigma_n : 8.843434e-02
	 number of secondary particules: 1104
	 number of fission neutrons: 1104

 batch number : 2082

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.647645e+00	 sigma_n : 9.227282e-02
	 number of secondary particules: 1111
	 number of fission neutrons: 1111

 batch number : 2083

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.534653e+00	 sigma_n : 8.595093e-02
	 number of secondary particules: 1087
	 number of fission neutrons: 1087

 batch number : 2084

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692732e+00	 sigma_n : 9.389465e-02
	 number of secondary particules: 1126
	 number of fission neutrons: 1126

 batch number : 2085

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.720249e+00	 sigma_n : 8.966696e-02
	 number of secondary particules: 1177
	 number of fission neutrons: 1177

 batch number : 2086

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.533560e+00	 sigma_n : 7.760881e-02
	 number of secondary particules: 1061
	 number of fission neutrons: 1061

 batch number : 2087

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692743e+00	 sigma_n : 8.733296e-02
	 number of secondary particules: 1073
	 number of fission neutrons: 1073

 batch number : 2088

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.758621e+00	 sigma_n : 9.130145e-02
	 number of secondary particules: 1132
	 number of fission neutrons: 1132

 batch number : 2089

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.730565e+00	 sigma_n : 8.981086e-02
	 number of secondary particules: 1134
	 number of fission neutrons: 1134

 batch number : 2090

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.573192e+00	 sigma_n : 8.398017e-02
	 number of secondary particules: 1105
	 number of fission neutrons: 1105

 batch number : 2091

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.579186e+00	 sigma_n : 9.131098e-02
	 number of secondary particules: 1101
	 number of fission neutrons: 1101

 batch number : 2092

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.603088e+00	 sigma_n : 8.395097e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 2093

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.563889e+00	 sigma_n : 7.863434e-02
	 number of secondary particules: 1050
	 number of fission neutrons: 1050

 batch number : 2094

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.765714e+00	 sigma_n : 9.261812e-02
	 number of secondary particules: 1086
	 number of fission neutrons: 1086

 batch number : 2095

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.728361e+00	 sigma_n : 8.950146e-02
	 number of secondary particules: 1103
	 number of fission neutrons: 1103

 batch number : 2096

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.546691e+00	 sigma_n : 8.593044e-02
	 number of secondary particules: 1034
	 number of fission neutrons: 1034

 batch number : 2097

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.810445e+00	 sigma_n : 9.108087e-02
	 number of secondary particules: 1055
	 number of fission neutrons: 1055

 batch number : 2098

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.781043e+00	 sigma_n : 9.568334e-02
	 number of secondary particules: 1080
	 number of fission neutrons: 1080

 batch number : 2099

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.743519e+00	 sigma_n : 9.218025e-02
	 number of secondary particules: 1123
	 number of fission neutrons: 1123

 Type and parameters of random generator before batch 2100 : 
	 DRAND48_RANDOM 9626 7963 14881  COUNTER	83570481


 batch number : 2100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.724844e+00	 sigma_n : 9.043075e-02
	 number of secondary particules: 1186
	 number of fission neutrons: 1186

 KEFF at step  : 2100
 keff = 9.978572e-01 sigma : 8.598928e-04
 number of batch used: 2000


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.256637e+01
*********************************************************


 Mean weight leakage = 5.739424e+02	 sigma = 3.446137e-01	 sigma% = 6.004325e-02


 Edition after batch number : 2100

******************************************************************************
RESPONSE FUNCTION : PRODUCTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	1.253944e+01	8.617393e-02


******************************************************************************
RESPONSE FUNCTION : ABSORPTION
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	5.388176e+00	7.256452e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	7.213412e+00	5.952260e-02


******************************************************************************
RESPONSE FUNCTION : LEAKAGE_INSIDE
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	0.000000e+00	0.000000e+00


******************************************************************************
RESPONSE FUNCTION : NXN EXCESS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	3.293167e-02	1.175415e+00


******************************************************************************
RESPONSE FUNCTION : FLUX TOTAL
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	2000	8.516147e+01	6.048214e-02


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

 KSTEP  9.978572e-01	8.617393e-02
 KCOLL  9.967607e-01	6.823833e-02
 KTRACK 9.968598e-01	6.129656e-02

  	  estimators  			  correlations   	  combined values  	  combined sigma%
  	  KSTEP <-> KCOLL  	    	  7.913696e-01  	  9.967598e-01  	  6.823838e-02
  	  KSTEP <-> KTRACK  	    	  6.204927e-01  	  9.969623e-01  	  6.088962e-02
  	  KCOLL <-> KTRACK  	    	  7.817791e-01  	  9.968340e-01  	  6.025409e-02

  	  full combined estimator  9.968338e-01	6.025408e-02



	  KSTEP ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.979719e-01	 sigma = 8.555105e-04	 sigma% = 8.572491e-02


	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.968883e-01	 sigma = 6.771168e-04	 sigma% = 6.792303e-02


	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.970245e-01	 sigma = 6.089887e-04	 sigma% = 6.108062e-02


	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 80 batches

	 number of batch used: 2020	 keff = 9.969212e-01	 sigma = 6.773017e-04	 sigma% = 6.793934e-02


 simulation time (s) : 30


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 8922 1330 57032  COUNTER	83612785


=====================================================================
	NORMAL COMPLETION
=====================================================================
