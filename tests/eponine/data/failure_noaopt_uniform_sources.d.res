
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $
 hostname: is232540
 pid: 16421

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 16421

 DATE : Tue Nov 27 09:23:00 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_noaopt_uniform_sources.d
 catalogname = ../spheresLivermore/Env/sblink_t4path.ceav5
 execution call = tripoli4 -u -s NJOY -c ../spheresLivermore/Env/sblink_t4path.ceav5 -d failure_noaopt_uniform_sources.d -o failure_noaopt_uniform_sources.d.res 


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
TITRE, Source spectrum mesurment
// First time and third time bins have 2 non-zero consecutive energy bins while the second one (middle)
// has 4 non-zero energy bins. If run without -a option, we get 2 bins, 4 bins, 2 bins, So the first
// and last energy bins are missing when parsing need to fill the spectrum during the second step,
// this leads to parsing failure.

TYPE 1 BOITE 10. 10. 10.
TYPE 2 SPHERE 0.01

VOLU 1 COMBI 1 0. 0. 0. FINV
VOLU 2 COMBI 2 0. 0. 0. ECRA 1 1 FINV


FING

COMPOSITION
	1
	PONCTUAL 300 vacuum
		1
		H1		1E-10
FIN_COMPOSITION

GEOMCOMP
	vacuum 2 1 2
FIN_GEOMCOMP	

LIST_SOURCE
   2
   NORME 1.

   SOURCE
   NEUTRON
   PONCTUAL 0. 0. 0.
   ANGULAR_DISTRIBUTION ISOTROPIC
   ENERGETIC_DISTRIBUTION SPECTRE BANDE 12.0 7.5
   TIME_DISTRIBUTION UNIFORM 0.5 6.0
   FIN_SOURCE

   SOURCE
   NEUTRON
   PONCTUAL 0. 0. 0.
   ANGULAR_DISTRIBUTION ISOTROPIC
   ENERGETIC_DISTRIBUTION SPECTRE BANDE 17.0 2.0
   TIME_DISTRIBUTION DIRAC 3.0
   FIN_SOURCE

FIN_LIST_SOURCE

LIST_DECOUPAGE
	2
	DEC_ENERGY
	5
	20. 15. 10. 5. 1E-11

	DEC_TIME
	4
    0.0 2.0 4.0 1E35
FIN_LIST_DECOUPAGE

REPONSES
1
COURANT NEUTRON
FIN_REPONSE

SCORE 
1
	1 SURF  CINETIQUE DECOUPAGE DEC_TIME DECOUPAGE DEC_ENERGY  FRONTIERE LIST 1    2 1
FIN_SCORE

SIMULATION
	BATCH 2
	SIZE 10
    PARTICULES 1 NEUTRON 
	EDITION 200
FIN_SIMULATION





 data reading time (s): 0

 Total concentration of material vacuum (1.E24at/cm3) is: 1.000000e-10


 Loading response functions ...
 Constructing score  ...0
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 4.500000e+00

		 Energetic density simulation intensity = 4.500000e+00

		 Angular intensity = 1.256637e+01

		 Time intensity = 5.500000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 3.110177e+02

		 Calculated source definition intensity = 3.110177e+02

	         SIMULATION INTENSITY = 3.110177e+02   BIASED SIMULATION INTENSITY = 3.110177e+02

	 initializing source number : 1

		 Energetic density definition intensity = 1.500000e+01

		 Energetic density simulation intensity = 1.500000e+01

		 Angular intensity = 1.256637e+01

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.884956e+02

		 Calculated source definition intensity = 1.884956e+02

	         SIMULATION INTENSITY = 1.884956e+02   BIASED SIMULATION INTENSITY = 1.884956e+02

   SUM OF SIMULATION INTENSITIES = 4.995132e+02

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

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 2.550000e+02	 sigma = 2.450000e+02	 sigma% = 9.607843e+01



******************************************************************************
RESPONSE FUNCTION : COURANT
RESPONSE NAME : 
ENERGY DECOUPAGE NAME : DEC_ENERGY


 PARTICULE : NEUTRON 
 temperature :0

 composition : none 

 concentration : 1.000000e+00

 reaction consists in tabulated data

******************************************************************************

	 scoring mode : SCORE_SURF
	 scoring zone : 	 Frontier 	 volumes : 2,1


	 TIME STEP NUMBER : 0
	 ------------------------------------
		 time min. = 0.000000e+00
		 time max. = 2.000000e+00

	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.s^-1	 %		 neut.s^-1

1.500000e+01 - 1.000000e+01	8.400000e-02	1.904762e+01	2.071695e-01
1.000000e+01 - 5.000000e+00	4.300000e-02	1.000000e+02	6.203589e-02

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 2	1.270000e-01	2.125984e+01


	 TIME STEP NUMBER : 1
	 ------------------------------------
		 time min. = 2.000000e+00
		 time max. = 4.000000e+00

	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.s^-1	 %		 neut.s^-1

2.000000e+01 - 1.500000e+01	2.300000e-02	1.000000e+02	7.994937e-02
1.500000e+01 - 1.000000e+01	1.760000e-01	4.318182e+01	4.340694e-01
1.000000e+01 - 5.000000e+00	3.830000e-01	3.054830e+01	5.525522e-01
5.000000e+00 - 1.000000e-11	8.800000e-02	1.363636e+01	3.266776e-03

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 2	6.700000e-01	4.477612e+00


	 TIME STEP NUMBER : 2
	 ------------------------------------
		 time min. = 4.000000e+00
		 time max. = 1.000000e+35

	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.s^-1	 %		 neut.s^-1

1.500000e+01 - 1.000000e+01	9.500000e-02	5.263158e+00	2.342988e-01
1.000000e+01 - 5.000000e+00	1.080000e-01	7.407407e+00	1.558111e-01

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 2	2.030000e-01	1.477833e+00



 simulation time (s) : 0


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 64302 35129 38808  COUNTER	3365


=====================================================================
	NORMAL COMPLETION
=====================================================================
