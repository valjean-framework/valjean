LANG ENGLISH
GEOMETRY
TITLE check balance
  TYPE 1 BOX 4 4 102
  TYPE 2 BOX 1 1 100
  TYPE 3 CYLZ 0.45 49

  VOLU 1 COMBI 1 0 0 0 ENDV

  VOLU 11 COMBI 2 -1 -1 0 SMASH 1 1 ENDV
  VOLU 12 COMBI 2 0 -1 0 SMASH 1 1 ENDV
  VOLU 13 COMBI 2 1 -1 0 SMASH 1 1 ENDV

  VOLU 14 COMBI 2 -1 0 0 SMASH 1 1 ENDV
  VOLU 15 COMBI 2 0 0 0 SMASH 1 1 ENDV
  VOLU 16 COMBI 2 1 0 0 SMASH 1 1 ENDV

  VOLU 17 COMBI 2 -1 1 0 SMASH 1 1 ENDV
  VOLU 18 COMBI 2 0 1 0 SMASH 1 1 ENDV
  VOLU 19 COMBI 2 1 1 0 SMASH 1 1 ENDV

  VOLU 21 COMBI 3 -1 -1 0 SMASH 1 11 ENDV
  VOLU 22 COMBI 3 0 -1 0  SMASH 1 12 ENDV
  VOLU 23 COMBI 3 1 -1 0  SMASH 1 13 ENDV

  VOLU 24 COMBI 3 -1 0 0  SMASH 1 14 ENDV
  VOLU 25 COMBI 3 0 0 0   SMASH 1 15 ENDV
  VOLU 26 COMBI 3 1 0 0   SMASH 1 16 ENDV

  VOLU 27 COMBI 3 -1 1 0  SMASH 1 17 ENDV
  VOLU 28 COMBI 3 0 1 0   SMASH 1 18 ENDV
  VOLU 29 COMBI 3 1 1 0   SMASH 1 19 ENDV

ENDGEOM 

BOUNDARY_CONDITION 12
11 REFLECTION 1
11 REFLECTION 3
12 REFLECTION 3
13 REFLECTION 2
13 REFLECTION 3
14 REFLECTION 1
16 REFLECTION 2
17 REFLECTION 1
17 REFLECTION 4
18 REFLECTION 4
19 REFLECTION 2
19 REFLECTION 4
END_BOUNDARY_CONDITION

COMPOSITION 4

POINT_WISE 624 GAINC 1
ZR90   1.93E-02          

POINT_WISE 300 VIDE 1
O16   1.0E-15

POINT_WISE 574 MODE 2
H1_H2O 4.736E-02       
O16    2.3684E-02        


POINT_WISE 924 fuel_1_1_1 4
U238   2.2694E-02
U235   7.7229E-04
U234   6.6523E-06
O16    4.6945E-02

END_COMPOSITION

GEOMCOMP
  VIDE 1 1
  MODE 9 11 12 13 14 15 16 17 18 19
  fuel_1_1_1 9 21 22 23 24 25 26 27 28 29
END_GEOMCOMP

SOURCES_LIST 1 
   SOURCE 
     PHOTON
     FACTORIZED  FRAME CARTESIAN  0. 0. 0.
                   1. 0. 0.
                   0. 1. 0.
                   0. 0. 1.

     ALL_FISSILE_VOLUMES_INSIDE_MESH

	 GEOMETRIC_DISTRIBUTION  TABULATED  TYPE F_U_V_W
           VAR_U X 2 -1.89312 1.89312
           VAR_V Y 2 -1.89312 1.89312
           VAR_W Z 2 -50  50. 
               F_U 1.   F_V 1. F_W 1.
         ANGULAR_DISTRIBUTION ISOTROPIC
         ENERGETIC_DISTRIBUTION SPECTRUM WATT_SPECTRUM 
         TIME_DISTRIBUTION DIRAC 0.
   END_SOURCES
END_SOURCES_LIST

GRID_LIST 1
  DEC_1G 2 20. 1.E-11
END_GRID_LIST

RESPONSES 3
  NAME edep_g
    DEPOSITED_ENERGY PHOTON
  NAME edep_e
    DEPOSITED_ENERGY ELECTRON
  NAME edep_p
    DEPOSITED_ENERGY POSITRON
END_RESPONSES

SCORE 3
  NAME edep_g_score
    edep_g LOCAL_ENERGY_DEPOSITION GRID DEC_1G VOLUME SUM 18
    11 12 13 14 15 16 17 18 19 21 22 23 24 25 26 27 28 29
  NAME edep_e_score
    edep_e LOCAL_ENERGY_DEPOSITION GRID DEC_1G VOLUME SUM 18
    11 12 13 14 15 16 17 18 19 21 22 23 24 25 26 27 28 29
  NAME edep_p_score
    edep_p LOCAL_ENERGY_DEPOSITION GRID DEC_1G VOLUME SUM 18
    11 12 13 14 15 16 17 18 19 21 22 23 24 25 26 27 28 29
END_SCORE

SIMULATION
  
  EDITION 1
  BATCH 10
  SIZE 1000
  PARTICLE 3
    PHOTON ELECTRON POSITRON
  ELECTRON_PHOTON_BALANCE
  MONITORING 0

END_SIMULATION
