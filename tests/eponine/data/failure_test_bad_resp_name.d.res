
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $
 hostname: is232540
 pid: 19580

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 19580

 DATE : Fri Nov 23 09:56:52 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_bad_resp_name.d
 catalogname = ../spheresLivermore/Env/sblink_t4path.ceav5
 execution call = tripoli4 -a -u -s NJOY -c ../spheresLivermore/Env/sblink_t4path.ceav5 -d failure_test_bad_resp_name.d -o failure_test_bad_resp_name.d.res 


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


GEOMETRY
TITRE from prob003 for geometrie, test response name not taken into account (containing character @)

TYPE 1 BOITE 10 10 10
TYPE 2 SPHERE 2.5 

VOLU 1 COMBI 1 0 0 0  
FINV

VOLU 2 COMBI 2 0 0 0
ECRASE 1 1
FINV

FINGEOM

COMPOSITION 1
	PONCTUAL 300 PLOMB
		1
		PB204		1
FIN_COMPOSITION

GEOMCOMP
   PLOMB 2 1 2
FIN_GEOMCOMP

LIST_SOURCE 1
 NORME 1

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 12.17
 TIME_DISTRIBUTION DIRAC 0.
 FIN_SOURCE
FIN_LIST_SOURCE

LIST_DECOUPAGE
	1
	DEC_SPECTRE
		5
		20. 15. 10. 5. 1.E-11
FIN_LIST_DECOUPAGE

REPONSES
1
 NAME flux_@_neutron FLUX NEUTRON
FIN_REPONSE

SCORE 
1
	NAME score flux_@_neutron SURF  DECOUPAGE DEC_SPECTRE FRONTIER LIST 1  2 1
FIN_SCORE

SIMULATION
	BATCH	1
	SIZE   1
    PARTICULES   1 NEUTRON 
	ENERGY_INF NEUTRON 1.
FIN_SIMULATION



 data reading time (s): 0

 Total concentration of material PLOMB (1.E24at/cm3) is: 1.000000e+00


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
	 mean number of collision per neutron history: 6.574000e+00	 sigma_n : 3.024699e-01

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 0.000000e+00	 sigma = 0.000000e+00	 sigma% = 0


 Edition after batch number : 1



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : flux neutron
SCORE NAME : score
ENERGY DECOUPAGE NAME : DEC_SPECTRE


 PARTICULE : NEUTRON 
******************************************************************************

	 scoring mode : SCORE_SURF
	 scoring zone : 	 Frontier 	 volumes : 2,1


	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.s^-1	 %		 neut.s^-1

2.000000e+01 - 1.500000e+01	0.000000e+00	0.000000e+00	0.000000e+00
1.500000e+01 - 1.000000e+01	0.000000e+00	0.000000e+00	0.000000e+00
1.000000e+01 - 5.000000e+00	0.000000e+00	0.000000e+00	0.000000e+00
5.000000e+00 - 1.000000e-11	8.635318e-03	0.000000e+00	3.205642e-04

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 1	8.635318e-03	0.000000e+00



 simulation time (s) : 0


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 41350 7822 46581  COUNTER	31357


=====================================================================
	NORMAL COMPLETION
=====================================================================
