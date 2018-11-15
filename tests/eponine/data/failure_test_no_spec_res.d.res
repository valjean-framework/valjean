
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $
 hostname: is232540
 pid: 25013

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 25013

 DATE : Thu Nov 15 18:27:20 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_no_spec_res.d
 catalogname = ../spheresLivermore/Env/sblink_t4path.ceav5
 execution call = tripoli4 -u -s NJOY -d failure_test_no_spec_res.d -c ../spheresLivermore/Env/sblink_t4path.ceav5 -o failure_test_no_spec_res.d.res 


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
TITRE from prob003 for geometrie

TYPE 1 BOITE 10 10 10
TYPE 2 SPHERE 8

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

LIST_SOURCES 2
 NORME 1

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 12
 TIME_DISTRIBUTION DIRAC 0.
 FIN_SOURCE

 SOURCE
 NEUTRON
 PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION ISOTROPIC
 ENERGETIC_DISTRIBUTION SPECTRE MONOCINETIQUE 1.33
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
	1 TRACK  DECOUPAGE DEC_SPECTRE VOLU LIST 1  1
FIN_SCORE

SIMULATION
	BATCH	10
	SIZE   1000
    PARTICULES   1 NEUTRON 
	ENERGY_INF NEUTRON 1.
	XML_EXPORT
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
	 mean number of collision per neutron history: 8.214000e+00	 sigma_n : 3.718669e-01

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.158000e+00	 sigma_n : 2.451472e-01

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.438000e+00	 sigma_n : 2.435641e-01

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.177000e+00	 sigma_n : 2.627712e-01

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.772000e+00	 sigma_n : 2.512910e-01

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.151000e+00	 sigma_n : 2.610217e-01

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.017000e+00	 sigma_n : 2.620484e-01

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.675000e+00	 sigma_n : 2.469258e-01

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 8.060000e+00	 sigma_n : 2.535521e-01

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 7.926000e+00	 sigma_n : 2.550011e-01

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

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Volume 	 num of volume : 1
	 Volume in cm3: 1.000000e+00


	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 neut.cm.s^-1	 %		 neut.cm.s^-1


	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 10	0.000000e+00	0.000000e+00



 simulation time (s) : 0


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 19115 48483 25479  COUNTER	679536


=====================================================================
	NORMAL COMPLETION
=====================================================================
