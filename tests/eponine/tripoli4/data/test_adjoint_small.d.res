
=====================================================================
$Id: t4main.cc,v 2.141 2019/01/04 14:09:00 aj256514 Exp $
 hostname: is232540
 pid: 29419

=====================================================================
$Id: t4main.cc,v 2.141 2019/01/04 14:09:00 aj256514 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 29419

 DATE : Tue Feb 12 16:22:40 2019

 Version is $Name:  $.

=====================================================================

 data filename = test_adjoint_small.d
 catalogname = /home/tripoli4.11/tripoli4.11.0/Env/t4path.ceav512
 execution call = tripoli4 -a -u -s NJOY -c /home/tripoli4.11/tripoli4.11.0/Env/t4path.ceav512 -d test_adjoint_small.d -o test_adjoint_small.d.res 


 dictionary file : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/ceav512.dictionary
 mass file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/mass_rmd.mas95
 Q fission directory : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/Qfission
 electron cross section  directory : /data/tmpuranus2/GALILEE-V0-3.0/PEID/Electron_Photon
 abondance file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/abundance
 own evaluations directory : 


 WARNING
 method name : T4_path
 error message : No such directory for own evaluations




 	 reading geometry : 

 	 checking association of compositions and volumes :  ok 



GEOMETRIE
TITRE TESTADJOINT

TYPE 1 BOITE 10 10 10
TYPE 2 BOITE 5 5 5

VOLU 10 COMBI 1 0 0 0 FINV
VOLU 11 COMBI 2 0 0 0 ECRASE 1 10 FINV

FING

LIMIT
	3
	10 REFLECTION 1
	10 REFLECTION 4
	10 REFLECTION 6
FIN_LIMIT

COMPOSITION
	1
	PONCTUAL 300 M1 3
		U235	7e-3
		U238	9e-2
		H1_H2O	1e-2
FIN_COMPOSITION

GEOMCOMP
	M1  2 10 11
FIN_GEOMCOMP


LIST_SOURCES 3
    SOURCE 
       // COEFF 1.0
       INTENSITE 1.0
       NEUTRON
       PUNCTUAL 0.5 0.5 0.5 
       ANGULAR_DISTRIBUTION ISOTROPIC
       ENERGETIC_DISTRIBUTION
           SPECTRE MONOCINETIQUE 15
       TIME_DISTRIBUTION DIRAC 0
    FIN_SOURCE
    SOURCE 
       // COEFF 1.0
       INTENSITE 1.0
       NEUTRON
       PUNCTUAL 3.5 -3.1 0.2
       ANGULAR_DISTRIBUTION ISOTROPIC
       ENERGETIC_DISTRIBUTION
           SPECTRE MONOCINETIQUE 0.0001 
       TIME_DISTRIBUTION DIRAC 0
    FIN_SOURCE
    SOURCE 
       // COEFF 1.0
       INTENSITE 1.0
       NEUTRON
       PUNCTUAL -4.5 4.2 1.3 
       ANGULAR_DISTRIBUTION ISOTROPIC
       ENERGETIC_DISTRIBUTION
           SPECTRE MONOCINETIQUE 5
       TIME_DISTRIBUTION DIRAC 0
    FIN_SOURCE
FIN_LIST_SOURCES

LIST_DECOUPAGE 1
	DEC_5G 4 1.96400E+01 5.0 1.0 1.10000E-11
FIN_LIST_DECOUPAGE

IFP_SCORES_SUPERHISTORY

    IFP_ADJOINT_FLUX 
	NAME FluxAdj_ang_1
	IFP_CYCLE_LENGTH 2
	CARTESIAN_ANGULAR -5 +5 2 -5 +5 2 -5 +5 2 -3.141592 3.141592 2  0 3.141592 2 
	ENERGY DECOUPAGE DEC_5G 

    IFP_ADJOINT_FLUX
    NAME flux_vol
    IFP_CYCLE_LENGTH 5
    VOLUMES LIST 2 10 11
    ENERGY DECOUPAGE DEC_5G

    IFP_ADJOINT_FLUX 
	NAME FluxAdj_1
	IFP_CYCLE_LENGTH 2
	CARTESIAN -5 +5 2 -5 +5 2 -5 +5 2 
	ENERGY DECOUPAGE DEC_5G 
FIN_IFP_SCORES


SIMULATION
    ADJOINT_CRITIC_SPH      
	DISCARD 0 
	BATCH 	20
	SIZE  	10000
	EDITION 20
	ENERGY_INF NEUTRON 1.1E-10
        ENERGY_SUP NEUTRON 1.96400E+01
	PARTICULES   1 NEUTRON
FIN_SIMULATION



 data reading time (s): 0

 Total concentration of material M1 (1.E24at/cm3) is: 1.070000e-01


 Loading response functions ...
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         NORM = 1.000000e+00   SIMULATION INTENSITY = 1.000000e+00   BIASED SIMULATION INTENSITY = 1.000000e+00

	 initializing source number : 1

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         NORM = 1.000000e+00   SIMULATION INTENSITY = 1.000000e+00   BIASED SIMULATION INTENSITY = 1.000000e+00

	 initializing source number : 2

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         NORM = 1.000000e+00   SIMULATION INTENSITY = 1.000000e+00   BIASED SIMULATION INTENSITY = 1.000000e+00

   SUM OF SIMULATION INTENSITIES = 3.000000e+00

   GLOBAL SIMULATION INTENSITY = 3.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 3.000000e+00


 initialization time (s): 3


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.559186e+01	 sigma_n : 6.758781e-02
	 number of secondary particules: 44893
	 number of fission neutrons: 44010

 simulation time (s) : 3


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.545636e+01	 sigma_n : 6.796049e-02
	 number of secondary particules: 43615
	 number of fission neutrons: 42693

 simulation time (s) : 7


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.545595e+01	 sigma_n : 6.727206e-02
	 number of secondary particules: 44609
	 number of fission neutrons: 43701

 simulation time (s) : 12


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.547755e+01	 sigma_n : 6.790355e-02
	 number of secondary particules: 43529
	 number of fission neutrons: 42618

 simulation time (s) : 16


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.543633e+01	 sigma_n : 6.769208e-02
	 number of secondary particules: 44113
	 number of fission neutrons: 43180

 simulation time (s) : 20


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.542298e+01	 sigma_n : 6.673312e-02
	 number of secondary particules: 45234
	 number of fission neutrons: 44309

 simulation time (s) : 24


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.538339e+01	 sigma_n : 6.728389e-02
	 number of secondary particules: 44099
	 number of fission neutrons: 43244

 simulation time (s) : 27


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.555047e+01	 sigma_n : 6.695592e-02
	 number of secondary particules: 45652
	 number of fission neutrons: 44761

 simulation time (s) : 31


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.552799e+01	 sigma_n : 6.794844e-02
	 number of secondary particules: 44162
	 number of fission neutrons: 43258

 simulation time (s) : 35


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.541955e+01	 sigma_n : 6.772011e-02
	 number of secondary particules: 43698
	 number of fission neutrons: 42804

 simulation time (s) : 39


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.549905e+01	 sigma_n : 6.795318e-02
	 number of secondary particules: 43179
	 number of fission neutrons: 42278

 simulation time (s) : 42


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.538860e+01	 sigma_n : 6.740170e-02
	 number of secondary particules: 44014
	 number of fission neutrons: 43112

 simulation time (s) : 46


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.539381e+01	 sigma_n : 6.752279e-02
	 number of secondary particules: 44122
	 number of fission neutrons: 43219

 simulation time (s) : 49


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.547788e+01	 sigma_n : 6.693176e-02
	 number of secondary particules: 45187
	 number of fission neutrons: 44221

 simulation time (s) : 54


 batch number : 15



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.134119e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.554149e+01	 sigma_n : 6.774328e-02
	 number of secondary particules: 44496
	 number of fission neutrons: 43604

 simulation time (s) : 58


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.541839e+01	 sigma_n : 6.697235e-02
	 number of secondary particules: 44880
	 number of fission neutrons: 43991

 simulation time (s) : 61


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.554859e+01	 sigma_n : 6.752005e-02
	 number of secondary particules: 44330
	 number of fission neutrons: 43424

 simulation time (s) : 65


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.556084e+01	 sigma_n : 6.760317e-02
	 number of secondary particules: 45048
	 number of fission neutrons: 44122

 simulation time (s) : 69


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.554644e+01	 sigma_n : 6.746436e-02
	 number of secondary particules: 44423
	 number of fission neutrons: 43549

 simulation time (s) : 73


 Type and parameters of random generator before batch 20 : 
	 DRAND48_RANDOM 49345 35689 348  COUNTER	170522054


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.553325e+01	 sigma_n : 6.767869e-02
	 number of secondary particules: 44372
	 number of fission neutrons: 43458

 KEFF at step  : 20
 keff = 0.000000e+00 sigma : 0.000000e+00
 number of batch used: 20


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 3.000000e+00
*********************************************************


 Mean weight leakage = 2.056988e+04	 sigma = 6.057607e+01	 sigma% = 2.944891e-01


 Edition after batch number : 20

******************************************************************************
RESPONSE FUNCTION : KEFFS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	20

 Warning
   One of the Keffectives is null and should not be
   Combined Keffectives will not be edited



******************************************************************************

IFP_ADJOINT_CRITICALITY EDITION

******************************************************************************

IFP_ADJOINT_FLUX

SCORE NAME: FluxAdj_ang_1

IFP CYCLE LENGTH = 2

******************************************************************************

            X (min | max)               Y (min | max)               Z (min | max)             Phi (min | max)           Theta (min | max)               E (min | max)   score [a.u.]       sigma_%

-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     6.097e-02     2.729e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     8.640e-02     2.020e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     5.678e-02     1.814e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     7.862e-02     2.139e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     2.394e-01     1.098e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     2.476e-01     1.079e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     2.184e-01     1.015e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     2.246e-01     1.101e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     4.577e-01     1.136e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     0.000e+00     1.571e+00     5.000e+00     1.964e+01     5.480e-01     1.122e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00    -3.142e+00     0.000e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     4.017e-01     1.063e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     3.142e+00     1.571e+00     3.142e+00     5.000e+00     1.964e+01     4.719e-01     1.100e+00

******************************************************************************

IFP_ADJOINT_FLUX

SCORE NAME: flux_vol

IFP CYCLE LENGTH = 5

******************************************************************************

  Vol                  E (min | max)   score [a.u.]       sigma_%

   10     1.100e-11     1.000e+00     5.760e-02     3.557e+00
   11     1.100e-11     1.000e+00     0.000e+00     0.000e+00
   10     1.000e+00     5.000e+00     3.962e-01     1.280e+00
   11     1.000e+00     5.000e+00     0.000e+00     0.000e+00
   10     5.000e+00     1.964e+01     0.000e+00     0.000e+00
   11     5.000e+00     1.964e+01     6.294e-01     1.014e+00

******************************************************************************

IFP_ADJOINT_FLUX

SCORE NAME: FluxAdj_1

IFP CYCLE LENGTH = 2

******************************************************************************

            X (min | max)               Y (min | max)               Z (min | max)               E (min | max)   score [a.u.]       sigma_%

-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     1.100e-11     1.000e+00     2.828e-01     9.804e-01
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     1.100e-11     1.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     1.000e+00     5.000e+00     9.300e-01     5.434e-01
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     1.000e+00     5.000e+00     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00    -5.000e+00     0.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00    -5.000e+00     0.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00    -5.000e+00     0.000e+00     0.000e+00     5.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
-5.000e+00     0.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     5.000e+00     1.964e+01     0.000e+00     0.000e+00
 0.000e+00     5.000e+00     0.000e+00     5.000e+00     0.000e+00     5.000e+00     5.000e+00     1.964e+01     1.879e+00     5.300e-01

******************************************************************************



	  WARNING
	 ----------

	 In FIXED_SOURCES_CRITICITY mode, the keff result
	 is actually an overall multiplication factor (cf User's Guide)



	  KSTEP ESTIMATOR
	 -------------------- 



		  NOT YET CONVERGED



	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 0 batches

	 number of batch used: 20	 keff = 4.360111e+00	 sigma = 1.253197e-02	 sigma% = 2.874232e-01

	 Equivalent Keff: 8.134367e-01



	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 0 batches

	 number of batch used: 20	 keff = 4.358974e+00	 sigma = 1.360887e-02	 sigma% = 3.122035e-01

	 Equivalent Keff: 8.133971e-01



	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 0 batches

	 number of batch used: 20	 keff = 4.361964e+00	 sigma = 1.284406e-02	 sigma% = 2.944559e-01


	 Equivalent Keff: 8.135012e-01


 simulation time (s) : 77


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 21767 18791 8917  COUNTER	179523324


=====================================================================
	NORMAL COMPLETION
=====================================================================
