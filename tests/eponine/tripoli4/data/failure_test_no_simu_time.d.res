
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $
 hostname: 
 pid: 10170

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $

 HOSTNAME : 

 PROCESS ID is : 10170

 DATE : Fri Nov 23 18:07:33 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_no_simu_time.d
 catalogname = sblink_t4path.ceav5
 execution call = tripoli4 -a -u -s NJOY -d failure_test_no_simu_time.d -c sblink_t4path.ceav5 -o failure_test_no_simu_time.d.res 


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
// To obtain a result without the "simulation time" keyword, kill the job during its execution.
// Here a simpler way has been chosen, as the test is for parsing: the job run normally, but the end
// of the output has been removed from the line with "simulation time".

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

   SUM OF SIMULATION INTENSITIES = 1.256637e+01

   GLOBAL NORM = 1.000000e+00   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.574000e+00	 sigma_n : 3.024699e-01

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.639000e+00	 sigma_n : 2.097872e-01

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.523000e+00	 sigma_n : 2.032998e-01

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.645000e+00	 sigma_n : 2.023510e-01

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.395000e+00	 sigma_n : 2.058187e-01

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.357000e+00	 sigma_n : 2.048988e-01

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.413000e+00	 sigma_n : 2.029523e-01

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.144000e+00	 sigma_n : 1.958919e-01

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.350000e+00	 sigma_n : 2.024166e-01

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 6.339000e+00	 sigma_n : 2.027343e-01

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 0.000000e+00	 sigma = 0.000000e+00	 sigma% = 0


 Edition after batch number : 10



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

2.000000e+01 - 1.500000e+01	0.000000e+00	0.000000e+00	0.000000e+00
1.500000e+01 - 1.000000e+01	9.721141e-04	5.329505e+01	2.397528e-03
1.000000e+01 - 5.000000e+00	2.440976e-04	1.000000e+02	3.521584e-04
5.000000e+00 - 1.000000e-11	4.631889e-02	1.560832e+01	1.719471e-03

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 10	4.753511e-02	1.539491e+01

