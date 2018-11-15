
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $
 hostname: is232540
 pid: 3239

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27 tv232747 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 3239

 DATE : Wed Nov 14 17:35:03 2018

 Version is $Name: tripoli4_11_branch_release-21-09-2018 $.

=====================================================================

 data filename = failure_test_segFault.d
 catalogname = ../spheresLivermore/Env/sblink_t4path.ceav5
 execution call = tripoli4 -a -u -s NJOY -c ../spheresLivermore/Env/sblink_t4path.ceav5 -d failure_test_segFault.d -o failure_test_segFault.d.res 


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



	 WARNING :  running photon without electron and positron
	 possible lack of bremsstrahlung photons


GEOMETRY
TITRE from prob003 for geometrie

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
    PARTICULES   1 PHOTON 
	ENERGY_INF NEUTRON 1.
	XML_EXPORT
FIN_SIMULATION


 FATAL ERROR
 method name : T4_read_data
 error message : there are no source defined for any particle type declared in simulation directive



			error localization in code sources

				file : t4read.cc
				line : 1012
