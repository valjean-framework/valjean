
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $
 hostname: 
 pid: 10012

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $

 HOSTNAME : 

 PROCESS ID is : 10012

 DATE : Fri Nov 23 18:03:25 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_no_normal_completion.d
 catalogname = sblink_t4path.ceav5
 execution call = tripoli4 -a -u -s NJOY -d failure_test_no_normal_completion.d -c sblink_t4path.ceav5 -o failure_test_no_normal_completion.d.res 


 dictionary file : ceav512.dictionary
 mass file : mass_rmd.mas95
 Q fission directory : Qfission
 electron cross section  directory : Electron_Photon
 abondance file : abundance
 own evaluations directory : 


 WARNING
 method name : T4_path
 error message : No such directory for own evaluations




 	 reading geometry : 

 	 checking association of compositions and volumes :  ok 


GEOMETRY
TITRE from prob003 for geometrie
// test no "NORMAL COMPLETION" in at the end
// To obtain a "no NORMAL COMPLETION" case launch the job and stop it with Ctrl+C
// A partial edition is obtained but not the final result.

TYPE 1 BOITE 10 10 10
TYPE 2 SPHERE 2.5 

VOLU 1 COMBI 1 0 0 0  
FINV

VOLU 2 COMBI 2 0 0 0
ECRASE 1 1
FINV

FINGEOM

COMPOSITION 1
	PONCTUAL 300 VIDE
		1
		HE4		1e-21
FIN_COMPOSITION

GEOMCOMP
   VIDE 2 1 2
FIN_GEOMCOMP

LIST_SOURCES 1
 NORME 1

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 12
 TIME_DISTRIBUTION DIRAC 0.
 FIN_SOURCE
FIN_LIST_SOURCES

LIST_DECOUPAGE
	1
	DEC_SPECTRE
		5
		20. 15. 10. 5. 1.E-11
FIN_LIST_DECOUPAGE

REPONSES
1
 FLUX NEUTRON
FIN_REPONSE

SCORE 
1
	1 TRACK  DECOUPAGE DEC_SPECTRE VOLU LIST 1  2
FIN_SCORE

SIMULATION
	BATCH	100
	SIZE   1000
    PARTICULES   1 NEUTRON 
	ENERGY_INF NEUTRON 1.
FIN_SIMULATION



 data reading time (s): 0



 WARNING
 method name : add_temperature
 error message : no absorption data for a complete nucleus


 Total concentration of material VIDE (1.E24at/cm3) is: 1.000000e-21


 Loading response functions ...
 Constructing score  ...0
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         SIMULATION INTENSITY = 1.256637e+01   BIASED SIMULATION INTENSITY = 1.256637e+01

   SUM OF SIMULATION INTENSITIES = 1.256637e+01

   GLOBAL NORM = 1.000000e+00   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 simulation time (s) : 0


 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 38


*********************************************************

  PARTIAL EDITION (USER SIGNAL)

*********************************************************

 number of batch : 37


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 9.864865e+02	 sigma = 1.351351e+01	 sigma% = 1.369863e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : 
ENERGY DECOUPAGE NAME : DEC_SPECTRE


 PARTICULE : NEUTRON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Volume 	 num of volume : 2
	 Volume in cm3: 1.000000e+00


	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.cm.s^-1	 %		 neut.cm.s^-1

2.000000e+01 - 1.500000e+01	0.000000e+00	0.000000e+00	0.000000e+00
1.500000e+01 - 1.000000e+01	2.500000e+00	0.000000e+00	6.165759e+00
1.000000e+01 - 5.000000e+00	0.000000e+00	0.000000e+00	0.000000e+00
5.000000e+00 - 1.000000e-11	0.000000e+00	0.000000e+00	0.000000e+00

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 37	2.500000e+00	0.000000e+00



 simulation time (s) : 0
