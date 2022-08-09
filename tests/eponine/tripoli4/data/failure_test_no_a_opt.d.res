
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $
 hostname: 
 pid: 6016

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $

 HOSTNAME : 

 PROCESS ID is : 6016

 DATE : Fri Nov 23 17:34:37 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_no_a_opt.d
 catalogname = sblink_t4path.ceav5
 execution call = tripoli4 -u -s NJOY -c sblink_t4path.ceav5 -d failure_test_no_a_opt.d -o failure_test_no_a_opt.d.res 


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
TITRE from prob003 for geometrie, to be run without -a option to remove 0 bins. This will make parsing to fail.

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

LIST_SOURCE 2
 NORME 1

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 12.17
 TIME_DISTRIBUTION DIRAC 0.
 FIN_SOURCE

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 1.33
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
FLUX NEUTRON
FIN_REPONSE

SCORE 
1
	1 SURF  DECOUPAGE DEC_SPECTRE FRONTIER LIST 1  2 1
FIN_SCORE

SIMULATION
	BATCH	10
	SIZE   1000
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

	 initializing source number : 1

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.256637e+01

		 Calculated source definition intensity = 1.256637e+01

	         SIMULATION INTENSITY = 1.256637e+01   BIASED SIMULATION INTENSITY = 1.256637e+01

   SUM OF SIMULATION INTENSITIES = 2.513274e+01

   GLOBAL NORM = 1.000000e+00   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.718000e+00	 sigma_n : 3.373671e-01

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.356000e+00	 sigma_n : 2.700485e-01

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.778000e+00	 sigma_n : 2.474145e-01

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.004000e+00	 sigma_n : 2.468500e-01

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.064000e+00	 sigma_n : 2.686598e-01

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.809000e+00	 sigma_n : 2.328750e-01

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.706000e+00	 sigma_n : 2.487155e-01

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.629000e+00	 sigma_n : 2.504677e-01

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.007000e+00	 sigma_n : 2.512331e-01

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.729000e+00	 sigma_n : 2.562015e-01

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 0.000000e+00	 sigma = 0.000000e+00	 sigma% = 0



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : 
ENERGY DECOUPAGE NAME : DEC_SPECTRE


 PARTICULE : NEUTRON 
******************************************************************************

	 scoring mode : SCORE_SURF
	 scoring zone : 	 Frontier 	 volumes : 2,1


	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.s^-1	 %		 neut.s^-1

1.500000e+01 - 1.000000e+01	3.182656e-04	5.104561e+01	7.849396e-04
5.000000e+00 - 1.000000e-11	7.593331e-02	2.148787e+01	2.818831e-03

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 10	7.625158e-02	2.152358e+01



 simulation time (s) : 0


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 5360 52261 47037  COUNTER	675519


=====================================================================
	NORMAL COMPLETION
=====================================================================
