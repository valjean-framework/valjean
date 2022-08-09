
=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $
 hostname: 
 pid: 7647

=====================================================================
$Id: t4main.cc,v 2.117.2.6 2018/09/21 14:06:27  Exp $

 HOSTNAME : 

 PROCESS ID is : 7647

 DATE : Tue Feb 12 17:21:34 2019

 Version is $Name: tripoli4_11 $.

=====================================================================

 data filename = sensitivity_godiva.d
 catalogname = t4path.ceav512
 execution call = tripoli4 -s NJOY -a -c t4path.ceav512 -d sensitivity_godiva.d -o sensitivity_godiva.d.res 


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


	 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	 WARNING :

		 simulation domain is incomplete while doing a criticality calculation

		 simulation domain is assumed to cover 20. MeV to 1.E-11 MeV
	 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING : The number of discarded batches has been increased by (IFP_CYCLE_LENGTH - 1) due to the IFP method for kinetics parameters and/or perturbations, sensitivities and Diven factor.
          Discard is now 29

// Godiva
//
///////////////////////////////////////
// //
// ENDF/B-VII.0 keff std //
// Experiment : 1.0000 (10) //
// MCNP5-1.60 : 0.9995 (5) //
// //
///////////////////////////////////////

// IFP Kinetics Parameters
//
// Rossi alpha
// measure : \u2212111 ± 2
// T4 (CEAv5.1) : \u2212113 ± 0.57
//
// Beta eff
// measure : 645 ± 13
// T4 (CEAv5.1) : 646 ± 3
//
// Lambda eff
// computed from Beta eff and Rossi alpha : 5.8
// T4 (CEAv5.1) : 5.71 ± 0.0036


GEOMETRIE
TITRE Godiva Solid Bare HEU sphere HEU-MET-FAST-001

	SURF 1 SPHERE 0. 0. 0. 8.7407
	VOLU 1 EQUA
	MOINS 1 1
	FINV // SPHERE HEU

FINGEOM

COMPOSITION 1
	//HEU Metal
	PUNCTUAL 294 MF 3
	U234 4.9184E-04
	U235 4.4994E-02
	U238 2.4984E-03
FIN_COMPOSITION

GEOMCOMP
	MF 1 1
FIN_GEOMCOMP

LIST_DECOUPAGE 3
DEC_2G 3 1.96400E+01 1.0 1.10000E-11
DEC_33G 34
1.964033E+01 1.000000E+01 6.065307E+00 3.678794E+00 2.231302E+00 1.353353E+00 8.208500E-01 4.978707E-01 3.019738E-01 1.831564E-01 1.110900E-01 6.737947E-02 4.086771E-02
2.478752E-02 1.503439E-02 9.118820E-03 5.530844E-03 3.354626E-03 2.034684E-03 1.234098E-03 7.485183E-04 4.539993E-04 3.043248E-04 1.486254E-04 9.166088E-05 6.790405E-05
4.016900E-05 2.260329E-05 1.370959E-05 8.315287E-06 4.000000E-06 5.400000E-07 1.000000E-07 1.000010E-11
DEC_E_3G 4 1.000010E-11 1.234098e-03 3.019738e-01 1.964033E+01
FIN_LIST_DECOUPAGE

LIST_SOURCE 1
 SOURCE
 NORME     1.
 NEUTRON
	PONCTUAL 0 0 0
 ANGULAR_DISTRIBUTION
	ISOTROPIC
 ENERGETIC_DISTRIBUTION
	SPECTRE MONOCINETIQUE 19.0
 TIME_DISTRIBUTION
	DIRAC 0.
 FIN_SOURCE
FIN_LIST_SOURCE

IFP_SENSITIVITY_LIST 
	
	4
	
	NU_FISSION 3
	
	NUCLEUS U235
	PROMPT
	ENERGY DECOUPAGE DEC_33G 

	NUCLEUS U235
	TOTAL
	ENERGY DECOUPAGE DEC_33G 

	NUCLEUS U235
	DELAYED TOTAL
	ENERGY DECOUPAGE DEC_33G 
	
	CHI_FISSION 3
	
	NUCLEUS U235
	PROMPT
	ENERGY DECOUPAGE DEC_E_3G
	INCIDENT_ENERGY DECOUPAGE DEC_2G 
	UNCONSTRAINED_COEFFICIENTS
	
	NUCLEUS U235
	TOTAL
	ENERGY DECOUPAGE DEC_E_3G
	INCIDENT_ENERGY DECOUPAGE DEC_2G 
	UNCONSTRAINED_COEFFICIENTS
	
	NUCLEUS U235
	TOTAL
	ENERGY DECOUPAGE DEC_E_3G
	INCIDENT_ENERGY DECOUPAGE DEC_2G 
	CONSTRAINED_COEFFICIENTS
	
	SCATTERING_TRANSFER_FUNCTION 1
	
	NUCLEUS U238
	REACTION 21
	ENERGY DECOUPAGE DEC_E_3G
	INCIDENT_ENERGY DECOUPAGE DEC_2G 
	COSINUS DECOUPAGE 5 -1.0 -0.5 0.0 0.5 1.0
	CONSTRAINED_COEFFICIENTS
	
	SECTION 1
	
	NUCLEUS U238
	REACTION 52
	ENERGY DECOUPAGE DEC_33G
	
	IFP_CYCLE_LENGTH 10
FIN_IFP_SENSITIVITY_LIST

SIMULATION
	CRITICITE
	DISCARD 20
	BATCH 120
	SIZE 20000
	EDITION 120
	ENERGY_INF NEUTRON 1.E-11
	ENERGY_SUP NEUTRON 1.964033E+01
	PARTICLE 1 NEUTRON
	FORCED_UNIT_BASE_INTERPOL
FIN_SIMULATION



 data reading time (s): 0

 Total concentration of material MF (1.E24at/cm3) is: 4.798424e-02


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

   SUM OF SIMULATION INTENSITIES = 1.000000e+00

   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 1


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1



 WARNING
 method name : get_fission_neutron_prompt_emission
 error message : fission energy is sampled again

2.072744e+01

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.838035e+00	 sigma_n : 1.791528e-02
	 number of secondary particules: 66909
	 number of fission neutrons: 63089

 simulation time (s) : 1


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.659180e+00	 sigma_n : 8.550413e-03
	 number of secondary particules: 40537
	 number of fission neutrons: 40537

 simulation time (s) : 4


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 1.954017e+00	 sigma_n : 1.226828e-02
	 number of secondary particules: 29988
	 number of fission neutrons: 29988

 simulation time (s) : 5


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.240796e+00	 sigma_n : 1.557977e-02
	 number of secondary particules: 25303
	 number of fission neutrons: 25303

 simulation time (s) : 7


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.459234e+00	 sigma_n : 1.759522e-02
	 number of secondary particules: 23587
	 number of fission neutrons: 23587

 simulation time (s) : 8


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.527536e+00	 sigma_n : 1.853918e-02
	 number of secondary particules: 22404
	 number of fission neutrons: 22404

 simulation time (s) : 9


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626004e+00	 sigma_n : 1.929527e-02
	 number of secondary particules: 21976
	 number of fission neutrons: 21976

 simulation time (s) : 11


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.655897e+00	 sigma_n : 1.962546e-02
	 number of secondary particules: 21893
	 number of fission neutrons: 21893

 simulation time (s) : 12


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666164e+00	 sigma_n : 1.957856e-02
	 number of secondary particules: 21949
	 number of fission neutrons: 21949

 simulation time (s) : 13


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642945e+00	 sigma_n : 1.964078e-02
	 number of secondary particules: 21823
	 number of fission neutrons: 21823

 simulation time (s) : 14


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621987e+00	 sigma_n : 1.943809e-02
	 number of secondary particules: 21614
	 number of fission neutrons: 21614

 simulation time (s) : 15


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671787e+00	 sigma_n : 1.972248e-02
	 number of secondary particules: 21605
	 number of fission neutrons: 21605

 simulation time (s) : 16


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.681477e+00	 sigma_n : 1.962288e-02
	 number of secondary particules: 21751
	 number of fission neutrons: 21751

 simulation time (s) : 17


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.645379e+00	 sigma_n : 1.933419e-02
	 number of secondary particules: 21755
	 number of fission neutrons: 21755

 simulation time (s) : 18


 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652999e+00	 sigma_n : 1.925811e-02
	 number of secondary particules: 21775
	 number of fission neutrons: 21775

 simulation time (s) : 20


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.634443e+00	 sigma_n : 1.948521e-02
	 number of secondary particules: 21549
	 number of fission neutrons: 21549

 simulation time (s) : 21


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669312e+00	 sigma_n : 1.962885e-02
	 number of secondary particules: 21616
	 number of fission neutrons: 21616

 simulation time (s) : 22


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.613111e+00	 sigma_n : 1.923363e-02
	 number of secondary particules: 21148
	 number of fission neutrons: 21148

 simulation time (s) : 23


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.746595e+00	 sigma_n : 2.035453e-02
	 number of secondary particules: 21810
	 number of fission neutrons: 21810

 simulation time (s) : 25


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.638377e+00	 sigma_n : 1.937732e-02
	 number of secondary particules: 21573
	 number of fission neutrons: 21573

 simulation time (s) : 26


 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.692718e+00	 sigma_n : 2.016589e-02
	 number of secondary particules: 21728
	 number of fission neutrons: 21728

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656710e+00	 sigma_n : 1.979543e-02
	 number of secondary particules: 21603
	 number of fission neutrons: 21603

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677545e+00	 sigma_n : 1.984385e-02
	 number of secondary particules: 21631
	 number of fission neutrons: 21631

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674819e+00	 sigma_n : 1.986345e-02
	 number of secondary particules: 21822
	 number of fission neutrons: 21822

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687471e+00	 sigma_n : 1.977813e-02
	 number of secondary particules: 22240
	 number of fission neutrons: 22240

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.617761e+00	 sigma_n : 1.899674e-02
	 number of secondary particules: 21630
	 number of fission neutrons: 21630

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682154e+00	 sigma_n : 1.965392e-02
	 number of secondary particules: 21754
	 number of fission neutrons: 21754

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695091e+00	 sigma_n : 1.977957e-02
	 number of secondary particules: 22241
	 number of fission neutrons: 22241

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.623083e+00	 sigma_n : 1.938294e-02
	 number of secondary particules: 21885
	 number of fission neutrons: 21885

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669637e+00	 sigma_n : 1.975171e-02
	 number of secondary particules: 22043
	 number of fission neutrons: 22043

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.629089e+00	 sigma_n : 1.921862e-02
	 number of secondary particules: 21641
	 number of fission neutrons: 21641

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695578e+00	 sigma_n : 1.988382e-02
	 number of secondary particules: 21983
	 number of fission neutrons: 21983

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644544e+00	 sigma_n : 1.935653e-02
	 number of secondary particules: 21675
	 number of fission neutrons: 21675

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.737867e+00	 sigma_n : 1.991006e-02
	 number of secondary particules: 22194
	 number of fission neutrons: 22194

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.642950e+00	 sigma_n : 1.945355e-02
	 number of secondary particules: 21949
	 number of fission neutrons: 21949

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639072e+00	 sigma_n : 1.970314e-02
	 number of secondary particules: 21811
	 number of fission neutrons: 21811

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683875e+00	 sigma_n : 1.987866e-02
	 number of secondary particules: 21813
	 number of fission neutrons: 21813

 batch number : 38

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656535e+00	 sigma_n : 1.971127e-02
	 number of secondary particules: 21503
	 number of fission neutrons: 21503

 batch number : 39

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686555e+00	 sigma_n : 1.988038e-02
	 number of secondary particules: 21662
	 number of fission neutrons: 21662

 batch number : 40

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684424e+00	 sigma_n : 1.985544e-02
	 number of secondary particules: 21904
	 number of fission neutrons: 21904

 batch number : 41

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662862e+00	 sigma_n : 1.940156e-02
	 number of secondary particules: 21893
	 number of fission neutrons: 21893

 batch number : 42

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660835e+00	 sigma_n : 1.969096e-02
	 number of secondary particules: 21904
	 number of fission neutrons: 21904

 batch number : 43

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.598795e+00	 sigma_n : 1.897605e-02
	 number of secondary particules: 21434
	 number of fission neutrons: 21434

 batch number : 44

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.682654e+00	 sigma_n : 1.974916e-02
	 number of secondary particules: 21637
	 number of fission neutrons: 21637

 batch number : 45

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678560e+00	 sigma_n : 1.994653e-02
	 number of secondary particules: 21762
	 number of fission neutrons: 21762

 batch number : 46

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661336e+00	 sigma_n : 1.969545e-02
	 number of secondary particules: 21811
	 number of fission neutrons: 21811

 batch number : 47

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.685526e+00	 sigma_n : 1.984451e-02
	 number of secondary particules: 22109
	 number of fission neutrons: 22109

 batch number : 48

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.636980e+00	 sigma_n : 1.962787e-02
	 number of secondary particules: 21773
	 number of fission neutrons: 21773

 batch number : 49

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684104e+00	 sigma_n : 1.966101e-02
	 number of secondary particules: 21845
	 number of fission neutrons: 21845

 batch number : 50

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.673335e+00	 sigma_n : 1.981177e-02
	 number of secondary particules: 21819
	 number of fission neutrons: 21819

 batch number : 51

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.654750e+00	 sigma_n : 1.929888e-02
	 number of secondary particules: 21861
	 number of fission neutrons: 21861

 batch number : 52

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665889e+00	 sigma_n : 1.953598e-02
	 number of secondary particules: 21740
	 number of fission neutrons: 21740

 batch number : 53

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674149e+00	 sigma_n : 2.008653e-02
	 number of secondary particules: 21796
	 number of fission neutrons: 21796

 batch number : 54

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.656910e+00	 sigma_n : 1.955406e-02
	 number of secondary particules: 21710
	 number of fission neutrons: 21710

 batch number : 55

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687655e+00	 sigma_n : 1.973741e-02
	 number of secondary particules: 21984
	 number of fission neutrons: 21984

 batch number : 56

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662937e+00	 sigma_n : 1.959819e-02
	 number of secondary particules: 22092
	 number of fission neutrons: 22092

 batch number : 57

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644939e+00	 sigma_n : 1.926413e-02
	 number of secondary particules: 21872
	 number of fission neutrons: 21872

 batch number : 58

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680916e+00	 sigma_n : 1.961708e-02
	 number of secondary particules: 21871
	 number of fission neutrons: 21871

 batch number : 59

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678173e+00	 sigma_n : 1.983315e-02
	 number of secondary particules: 21810
	 number of fission neutrons: 21810

 batch number : 60

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660645e+00	 sigma_n : 1.961570e-02
	 number of secondary particules: 21831
	 number of fission neutrons: 21831

 batch number : 61

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.646283e+00	 sigma_n : 1.949121e-02
	 number of secondary particules: 21654
	 number of fission neutrons: 21654

 batch number : 62

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.677150e+00	 sigma_n : 1.943177e-02
	 number of secondary particules: 21862
	 number of fission neutrons: 21862

 batch number : 63

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.670890e+00	 sigma_n : 1.961405e-02
	 number of secondary particules: 21900
	 number of fission neutrons: 21900

 batch number : 64

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.641689e+00	 sigma_n : 1.950224e-02
	 number of secondary particules: 21574
	 number of fission neutrons: 21574

 batch number : 65

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675165e+00	 sigma_n : 1.963239e-02
	 number of secondary particules: 21572
	 number of fission neutrons: 21572

 batch number : 66

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.674810e+00	 sigma_n : 1.936998e-02
	 number of secondary particules: 21700
	 number of fission neutrons: 21700

 batch number : 67

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675714e+00	 sigma_n : 1.979602e-02
	 number of secondary particules: 21699
	 number of fission neutrons: 21699

 batch number : 68

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665837e+00	 sigma_n : 1.971205e-02
	 number of secondary particules: 21787
	 number of fission neutrons: 21787

 batch number : 69

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688774e+00	 sigma_n : 1.980112e-02
	 number of secondary particules: 22065
	 number of fission neutrons: 22065

 batch number : 70

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.664612e+00	 sigma_n : 1.955802e-02
	 number of secondary particules: 22073
	 number of fission neutrons: 22073

 batch number : 71

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.626829e+00	 sigma_n : 1.930297e-02
	 number of secondary particules: 21767
	 number of fission neutrons: 21767

 batch number : 72

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.653558e+00	 sigma_n : 1.987361e-02
	 number of secondary particules: 21537
	 number of fission neutrons: 21537

 batch number : 73

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.669638e+00	 sigma_n : 1.973752e-02
	 number of secondary particules: 21604
	 number of fission neutrons: 21604

 batch number : 74

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668534e+00	 sigma_n : 1.959003e-02
	 number of secondary particules: 21796
	 number of fission neutrons: 21796

 batch number : 75

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.679758e+00	 sigma_n : 1.984803e-02
	 number of secondary particules: 21870
	 number of fission neutrons: 21870

 batch number : 76

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662643e+00	 sigma_n : 1.969699e-02
	 number of secondary particules: 22019
	 number of fission neutrons: 22019

 batch number : 77

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.615832e+00	 sigma_n : 1.924535e-02
	 number of secondary particules: 21816
	 number of fission neutrons: 21816

 batch number : 78

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.667263e+00	 sigma_n : 1.951694e-02
	 number of secondary particules: 21976
	 number of fission neutrons: 21976

 batch number : 79

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.635210e+00	 sigma_n : 1.902524e-02
	 number of secondary particules: 21792
	 number of fission neutrons: 21792

 batch number : 80

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.687394e+00	 sigma_n : 1.960265e-02
	 number of secondary particules: 21947
	 number of fission neutrons: 21947

 batch number : 81

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.628195e+00	 sigma_n : 1.929347e-02
	 number of secondary particules: 21768
	 number of fission neutrons: 21768

 batch number : 82

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.639103e+00	 sigma_n : 1.950450e-02
	 number of secondary particules: 21404
	 number of fission neutrons: 21404

 batch number : 83

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665639e+00	 sigma_n : 1.934804e-02
	 number of secondary particules: 21295
	 number of fission neutrons: 21295

 batch number : 84

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703391e+00	 sigma_n : 2.009271e-02
	 number of secondary particules: 21612
	 number of fission neutrons: 21612

 batch number : 85

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678327e+00	 sigma_n : 1.995911e-02
	 number of secondary particules: 21671
	 number of fission neutrons: 21671

 batch number : 86

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.695399e+00	 sigma_n : 1.968590e-02
	 number of secondary particules: 22017
	 number of fission neutrons: 22017

 batch number : 87

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.621156e+00	 sigma_n : 1.934630e-02
	 number of secondary particules: 21783
	 number of fission neutrons: 21783

 batch number : 88

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.652635e+00	 sigma_n : 1.963698e-02
	 number of secondary particules: 21397
	 number of fission neutrons: 21397

 batch number : 89

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.678164e+00	 sigma_n : 1.992629e-02
	 number of secondary particules: 21672
	 number of fission neutrons: 21672

 batch number : 90

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660945e+00	 sigma_n : 1.944351e-02
	 number of secondary particules: 21577
	 number of fission neutrons: 21577

 batch number : 91

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.660719e+00	 sigma_n : 1.938838e-02
	 number of secondary particules: 21595
	 number of fission neutrons: 21595

 batch number : 92

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.657822e+00	 sigma_n : 1.975850e-02
	 number of secondary particules: 21394
	 number of fission neutrons: 21394

 batch number : 93

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.680705e+00	 sigma_n : 1.991456e-02
	 number of secondary particules: 21483
	 number of fission neutrons: 21483

 batch number : 94

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693153e+00	 sigma_n : 1.996542e-02
	 number of secondary particules: 21851
	 number of fission neutrons: 21851

 batch number : 95

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.632848e+00	 sigma_n : 1.931355e-02
	 number of secondary particules: 21534
	 number of fission neutrons: 21534

 batch number : 96

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703014e+00	 sigma_n : 2.006903e-02
	 number of secondary particules: 21724
	 number of fission neutrons: 21724

 batch number : 97

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675014e+00	 sigma_n : 1.963643e-02
	 number of secondary particules: 21929
	 number of fission neutrons: 21929

 batch number : 98

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.658808e+00	 sigma_n : 1.969222e-02
	 number of secondary particules: 22043
	 number of fission neutrons: 22043

 batch number : 99

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.640294e+00	 sigma_n : 1.935349e-02
	 number of secondary particules: 21818
	 number of fission neutrons: 21818

 batch number : 100

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.643414e+00	 sigma_n : 1.944798e-02
	 number of secondary particules: 21523
	 number of fission neutrons: 21523

 batch number : 101

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.686103e+00	 sigma_n : 1.989579e-02
	 number of secondary particules: 21518
	 number of fission neutrons: 21518

 batch number : 102

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666047e+00	 sigma_n : 1.964826e-02
	 number of secondary particules: 21389
	 number of fission neutrons: 21389

 batch number : 103

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.675628e+00	 sigma_n : 1.939374e-02
	 number of secondary particules: 21519
	 number of fission neutrons: 21519

 batch number : 104

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.684325e+00	 sigma_n : 1.970280e-02
	 number of secondary particules: 21580
	 number of fission neutrons: 21580

 batch number : 105

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.703475e+00	 sigma_n : 1.998859e-02
	 number of secondary particules: 22011
	 number of fission neutrons: 22011

 batch number : 106

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.622961e+00	 sigma_n : 1.944293e-02
	 number of secondary particules: 21748
	 number of fission neutrons: 21748

 batch number : 107

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.689121e+00	 sigma_n : 1.993115e-02
	 number of secondary particules: 21768
	 number of fission neutrons: 21768

 batch number : 108

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.665197e+00	 sigma_n : 1.935870e-02
	 number of secondary particules: 21770
	 number of fission neutrons: 21770

 batch number : 109

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.671214e+00	 sigma_n : 1.991387e-02
	 number of secondary particules: 22070
	 number of fission neutrons: 22070

 batch number : 110

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.610648e+00	 sigma_n : 1.935053e-02
	 number of secondary particules: 21662
	 number of fission neutrons: 21662

 batch number : 111

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.662866e+00	 sigma_n : 1.962918e-02
	 number of secondary particules: 21470
	 number of fission neutrons: 21470

 batch number : 112

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.661854e+00	 sigma_n : 1.970733e-02
	 number of secondary particules: 21702
	 number of fission neutrons: 21702

 batch number : 113

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.666114e+00	 sigma_n : 1.967162e-02
	 number of secondary particules: 21531
	 number of fission neutrons: 21531

 batch number : 114

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.683851e+00	 sigma_n : 1.977176e-02
	 number of secondary particules: 21550
	 number of fission neutrons: 21550

 batch number : 115

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.693039e+00	 sigma_n : 1.992428e-02
	 number of secondary particules: 21853
	 number of fission neutrons: 21853

 batch number : 116

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.644351e+00	 sigma_n : 1.920330e-02
	 number of secondary particules: 21454
	 number of fission neutrons: 21454

 batch number : 117

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688170e+00	 sigma_n : 2.000569e-02
	 number of secondary particules: 21704
	 number of fission neutrons: 21704

 batch number : 118

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.651170e+00	 sigma_n : 1.945457e-02
	 number of secondary particules: 21596
	 number of fission neutrons: 21596

 batch number : 119

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.668272e+00	 sigma_n : 1.983460e-02
	 number of secondary particules: 21605
	 number of fission neutrons: 21605

 Type and parameters of random generator before batch 120 : 
	 DRAND48_RANDOM 11763 17584 22107  COUNTER	95614104


 batch number : 120

  quota sampling and descendant statistics: 
	 mean number of collision per neutron history: 2.688267e+00	 sigma_n : 2.003488e-02
	 number of secondary particules: 21788
	 number of fission neutrons: 21788

 KEFF at step  : 120
 keff = 9.954907e-01 sigma : 8.759187e-04
 number of batch used: 91


*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 1.146834e+04	 sigma = 1.449156e+01	 sigma% = 1.263615e-01


 Edition after batch number : 120

******************************************************************************
RESPONSE FUNCTION : KEFFS
******************************************************************************

	ENERGY INTEGRATED RESULTS

number of batches used:	91

 KSTEP  9.954907e-01	8.798863e-02
 KCOLL  9.959480e-01	6.558671e-02
 KTRACK 9.963401e-01	5.659325e-02

  	  estimators  			  correlations   	  combined values  	  combined sigma%
  	  KSTEP <-> KCOLL  	    	  7.799494e-01  	  9.959777e-01  	  6.548700e-02
  	  KSTEP <-> KTRACK  	    	  5.764322e-01  	  9.962853e-01  	  5.640535e-02
  	  KCOLL <-> KTRACK  	    	  7.398244e-01  	  9.962508e-01  	  5.566981e-02

  	  full combined estimator  9.962563e-01	5.563808e-02

******************************************************************************
RESPONSE FUNCTION : IFP ADJOINT WEIGHTED KEFF SENSITIVITIES
******************************************************************************

number of batches used:	91

Scores are ordered by type (SECTION, FISSION NU, FISSION CHI, SCATTERING KERNEL) and index:

CROSS SECTION SENSITIVITY :

 i = 1; NUCLEUS : U238, TYPE : SECTION CODE 52

 E min          E max              S(E)         sigma

 1.000000e+01  1.964033e+01    -6.780190e-08  8.636793e+00
 6.065307e+00  1.000000e+01    -4.915194e-07  2.242075e+00
 3.678794e+00  6.065307e+00    -2.774741e-06  1.319753e+00
 2.231302e+00  3.678794e+00    -3.118562e-05  9.535413e-01
 1.353353e+00  2.231302e+00    -1.230044e-04  9.728667e-01
 8.208500e-01  1.353353e+00    -2.426141e-04  8.622969e-01
 4.978707e-01  8.208500e-01    -2.620842e-04  1.073108e+00
 3.019738e-01  4.978707e-01    -2.065576e-04  1.176038e+00
 1.831564e-01  3.019738e-01    -1.567810e-04  1.261982e+00
 1.110900e-01  1.831564e-01    -1.236904e-04  1.723180e+00
 6.737947e-02  1.110900e-01    -9.798637e-05  2.450323e+00
 4.086771e-02  6.737947e-02    -6.690441e-05  3.368924e+00
 2.478752e-02  4.086771e-02    -4.155867e-05  4.831845e+00
 1.503439e-02  2.478752e-02    -2.405685e-05  8.495221e+00
 9.118820e-03  1.503439e-02    -1.308073e-05  1.276562e+01
 5.530844e-03  9.118820e-03    -8.290982e-06  1.750029e+01
 3.354626e-03  5.530844e-03    -2.059294e-06  2.701276e+01
 2.034684e-03  3.354626e-03    -1.715775e-06  3.947320e+01
 1.234098e-03  2.034684e-03    -3.219723e-07  4.161982e+01
 7.485183e-04  1.234098e-03    -9.533254e-08  4.825720e+01
 4.539993e-04  7.485183e-04    -1.299663e-07  9.892701e+01
 3.043248e-04  4.539993e-04    -4.426912e-09  6.785122e+01
 1.486254e-04  3.043248e-04    -1.278170e-10  7.659798e+01
 9.166088e-05  1.486254e-04    -8.874634e-10  1.000000e+02
 6.790405e-05  9.166088e-05    0.000000e+00  0.000000e+00
 4.016900e-05  6.790405e-05    0.000000e+00  0.000000e+00
 2.260329e-05  4.016900e-05    -4.009239e-09  1.000000e+02
 1.370959e-05  2.260329e-05    0.000000e+00  0.000000e+00
 8.315287e-06  1.370959e-05    0.000000e+00  0.000000e+00
 4.000000e-06  8.315287e-06    0.000000e+00  0.000000e+00
 5.400000e-07  4.000000e-06    0.000000e+00  0.000000e+00
 1.000000e-07  5.400000e-07    0.000000e+00  0.000000e+00
 1.000010e-11  1.000000e-07    0.000000e+00  0.000000e+00

 Energy integrated S           -1.405461e-03  5.268915e-01

FISSION NU SENSITIVITY :

 i = 1; NUCLEUS : U235, TYPE : PROMPT FISSION_NU

 E min          E max              S(E)         sigma

 1.000000e+01  1.964033e+01    2.261293e-03  7.273311e+00
 6.065307e+00  1.000000e+01    2.596320e-02  1.817401e+00
 3.678794e+00  6.065307e+00    6.947822e-02  1.029877e+00
 2.231302e+00  3.678794e+00    1.378306e-01  7.219090e-01
 1.353353e+00  2.231302e+00    1.590728e-01  7.081952e-01
 8.208500e-01  1.353353e+00    1.485847e-01  7.532150e-01
 4.978707e-01  8.208500e-01    1.319191e-01  8.801869e-01
 3.019738e-01  4.978707e-01    1.097819e-01  8.979149e-01
 1.831564e-01  3.019738e-01    8.033898e-02  1.002520e+00
 1.110900e-01  1.831564e-01    5.135728e-02  1.424095e+00
 6.737947e-02  1.110900e-01    2.946513e-02  1.731180e+00
 4.086771e-02  6.737947e-02    1.561836e-02  2.303123e+00
 2.478752e-02  4.086771e-02    7.393225e-03  3.230650e+00
 1.503439e-02  2.478752e-02    3.721506e-03  5.524336e+00
 9.118820e-03  1.503439e-02    1.917202e-03  8.289492e+00
 5.530844e-03  9.118820e-03    9.028284e-04  1.131267e+01
 3.354626e-03  5.530844e-03    3.476390e-04  1.862893e+01
 2.034684e-03  3.354626e-03    1.848632e-04  1.975834e+01
 1.234098e-03  2.034684e-03    6.643566e-05  2.656571e+01
 7.485183e-04  1.234098e-03    9.024256e-05  3.743554e+01
 4.539993e-04  7.485183e-04    1.075362e-05  6.124436e+01
 3.043248e-04  4.539993e-04    4.770831e-05  4.404031e+01
 1.486254e-04  3.043248e-04    1.548759e-06  7.338289e+01
 9.166088e-05  1.486254e-04    4.072688e-06  1.000000e+02
 6.790405e-05  9.166088e-05    0.000000e+00  0.000000e+00
 4.016900e-05  6.790405e-05    0.000000e+00  0.000000e+00
 2.260329e-05  4.016900e-05    6.499684e-06  1.000000e+02
 1.370959e-05  2.260329e-05    0.000000e+00  0.000000e+00
 8.315287e-06  1.370959e-05    0.000000e+00  0.000000e+00
 4.000000e-06  8.315287e-06    0.000000e+00  0.000000e+00
 5.400000e-07  4.000000e-06    0.000000e+00  0.000000e+00
 1.000000e-07  5.400000e-07    0.000000e+00  0.000000e+00
 1.000010e-11  1.000000e-07    0.000000e+00  0.000000e+00

 Energy integrated S           9.763660e-01  4.015080e-02

 i = 2; NUCLEUS : U235, TYPE : TOTAL FISSION_NU

 E min          E max              S(E)         sigma

 1.000000e+01  1.964033e+01    2.288530e-03  7.198401e+00
 6.065307e+00  1.000000e+01    2.608429e-02  1.803627e+00
 3.678794e+00  6.065307e+00    6.988477e-02  1.055429e+00
 2.231302e+00  3.678794e+00    1.387733e-01  7.125523e-01
 1.353353e+00  2.231302e+00    1.600367e-01  7.000866e-01
 8.208500e-01  1.353353e+00    1.494982e-01  7.440211e-01
 4.978707e-01  8.208500e-01    1.327692e-01  8.756970e-01
 3.019738e-01  4.978707e-01    1.104587e-01  8.814470e-01
 1.831564e-01  3.019738e-01    8.083503e-02  9.959706e-01
 1.110900e-01  1.831564e-01    5.167985e-02  1.408865e+00
 6.737947e-02  1.110900e-01    2.965948e-02  1.707703e+00
 4.086771e-02  6.737947e-02    1.574298e-02  2.301231e+00
 2.478752e-02  4.086771e-02    7.424452e-03  3.231391e+00
 1.503439e-02  2.478752e-02    3.738368e-03  5.559844e+00
 9.118820e-03  1.503439e-02    1.937954e-03  8.264652e+00
 5.530844e-03  9.118820e-03    9.182586e-04  1.155167e+01
 3.354626e-03  5.530844e-03    3.476390e-04  1.862893e+01
 2.034684e-03  3.354626e-03    1.865156e-04  1.966029e+01
 1.234098e-03  2.034684e-03    6.643566e-05  2.656571e+01
 7.485183e-04  1.234098e-03    9.024256e-05  3.743554e+01
 4.539993e-04  7.485183e-04    1.075362e-05  6.124436e+01
 3.043248e-04  4.539993e-04    4.770831e-05  4.404031e+01
 1.486254e-04  3.043248e-04    1.548759e-06  7.338289e+01
 9.166088e-05  1.486254e-04    4.072688e-06  1.000000e+02
 6.790405e-05  9.166088e-05    0.000000e+00  0.000000e+00
 4.016900e-05  6.790405e-05    0.000000e+00  0.000000e+00
 2.260329e-05  4.016900e-05    6.499684e-06  1.000000e+02
 1.370959e-05  2.260329e-05    0.000000e+00  0.000000e+00
 8.315287e-06  1.370959e-05    0.000000e+00  0.000000e+00
 4.000000e-06  8.315287e-06    0.000000e+00  0.000000e+00
 5.400000e-07  4.000000e-06    0.000000e+00  0.000000e+00
 1.000000e-07  5.400000e-07    0.000000e+00  0.000000e+00
 1.000010e-11  1.000000e-07    0.000000e+00  0.000000e+00

 Energy integrated S           9.824915e-01  3.517106e-02

 i = 3; NUCLEUS : U235, TYPE : DELAYED FISSION_NU

 E min          E max              S(E)         sigma

 1.000000e+01  1.964033e+01    2.723700e-05  4.971120e+01
 6.065307e+00  1.000000e+01    1.210869e-04  2.613149e+01
 3.678794e+00  6.065307e+00    4.065491e-04  1.498665e+01
 2.231302e+00  3.678794e+00    9.426979e-04  9.722777e+00
 1.353353e+00  2.231302e+00    9.639592e-04  8.987559e+00
 8.208500e-01  1.353353e+00    9.135065e-04  8.990748e+00
 4.978707e-01  8.208500e-01    8.500996e-04  9.523675e+00
 3.019738e-01  4.978707e-01    6.768391e-04  1.074072e+01
 1.831564e-01  3.019738e-01    4.960452e-04  1.258753e+01
 1.110900e-01  1.831564e-01    3.225721e-04  1.463588e+01
 6.737947e-02  1.110900e-01    1.943511e-04  2.275585e+01
 4.086771e-02  6.737947e-02    1.246158e-04  2.164071e+01
 2.478752e-02  4.086771e-02    3.122726e-05  5.289827e+01
 1.503439e-02  2.478752e-02    1.686175e-05  5.947740e+01
 9.118820e-03  1.503439e-02    2.075202e-05  5.179887e+01
 5.530844e-03  9.118820e-03    1.543017e-05  1.000000e+02
 3.354626e-03  5.530844e-03    0.000000e+00  0.000000e+00
 2.034684e-03  3.354626e-03    1.652386e-06  1.000000e+02
 1.234098e-03  2.034684e-03    0.000000e+00  0.000000e+00
 7.485183e-04  1.234098e-03    0.000000e+00  0.000000e+00
 4.539993e-04  7.485183e-04    0.000000e+00  0.000000e+00
 3.043248e-04  4.539993e-04    0.000000e+00  0.000000e+00
 1.486254e-04  3.043248e-04    0.000000e+00  0.000000e+00
 9.166088e-05  1.486254e-04    0.000000e+00  0.000000e+00
 6.790405e-05  9.166088e-05    0.000000e+00  0.000000e+00
 4.016900e-05  6.790405e-05    0.000000e+00  0.000000e+00
 2.260329e-05  4.016900e-05    0.000000e+00  0.000000e+00
 1.370959e-05  2.260329e-05    0.000000e+00  0.000000e+00
 8.315287e-06  1.370959e-05    0.000000e+00  0.000000e+00
 4.000000e-06  8.315287e-06    0.000000e+00  0.000000e+00
 5.400000e-07  4.000000e-06    0.000000e+00  0.000000e+00
 1.000000e-07  5.400000e-07    0.000000e+00  0.000000e+00
 1.000010e-11  1.000000e-07    0.000000e+00  0.000000e+00

 Energy integrated S           6.125483e-03  3.580850e+00

FISSION CHI SENSITIVITY :

 i = 1; NUCLEUS : U235, TYPE : PROMPT FISSION_CHI


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    1.448747e-05  7.569734e+01
 1.234098e-03  3.019738e-01    3.177550e-02  1.736329e+00
 3.019738e-01  1.964033e+01    4.540558e-01  3.193554e-01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    4.478140e-07  1.000000e+02
 1.234098e-03  3.019738e-01    3.306100e-02  1.544180e+00
 3.019738e-01  1.964033e+01    4.574588e-01  3.173431e-01

 Energy integrated S           9.763660e-01  4.015080e-02

 i = 2; NUCLEUS : U235, TYPE : TOTAL FISSION_CHI


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    1.595512e-05  7.211633e+01
 1.234098e-03  3.019738e-01    3.309612e-02  1.750449e+00
 3.019738e-01  1.964033e+01    4.557081e-01  3.168125e-01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    4.530631e-06  6.141440e+01
 1.234098e-03  3.019738e-01    3.440065e-02  1.527100e+00
 3.019738e-01  1.964033e+01    4.592661e-01  3.178838e-01

 Energy integrated S           9.824915e-01  3.517106e-02

 i = 3; NUCLEUS : U235, TYPE : TOTAL FISSION_CHI (CONSTRAINED)


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    5.931554e-06  1.940790e+02
 1.234098e-03  3.019738e-01    3.326919e-03  1.710512e+01
 3.019738e-01  1.964033e+01    -3.332850e-03  1.701679e+01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    -7.157376e-06  3.893347e+01
 1.234098e-03  3.019738e-01    3.740270e-03  1.378342e+01
 3.019738e-01  1.964033e+01    -3.733113e-03  1.382170e+01

 Energy integrated S           4.051250e-15  6.236159e+01

SCATTERING TRANSFER FUNCTION SENSITIVITY :

 i = 1; NUCLEUS : U238, TYPE : SCATTERING LAW 21 (CONSTRAINED)


 Direction cosine interval: -1.000000e+00 -5.000000e-01


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    0.000000e+00  0.000000e+00
 1.234098e-03  3.019738e-01    0.000000e+00  0.000000e+00
 3.019738e-01  1.964033e+01    3.909188e-04  2.950215e+01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    -1.606999e-06  9.209702e+01
 1.234098e-03  3.019738e-01    6.595875e-04  3.778701e+01
 3.019738e-01  1.964033e+01    2.389396e-04  9.633561e+01

 Direction cosine interval: -5.000000e-01 0.000000e+00


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    0.000000e+00  0.000000e+00
 1.234098e-03  3.019738e-01    0.000000e+00  0.000000e+00
 3.019738e-01  1.964033e+01    6.237023e-04  2.398063e+01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    -2.692976e-06  2.660172e+00
 1.234098e-03  3.019738e-01    1.678727e-03  1.665461e+01
 3.019738e-01  1.964033e+01    -2.881296e-04  7.814455e+01

 Direction cosine interval: 0.000000e+00 5.000000e-01


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    0.000000e+00  0.000000e+00
 1.234098e-03  3.019738e-01    0.000000e+00  0.000000e+00
 3.019738e-01  1.964033e+01    2.452056e-04  6.481580e+01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    -6.873944e-07  4.527914e+00
 1.234098e-03  3.019738e-01    1.056814e-03  3.020798e+01
 3.019738e-01  1.964033e+01    -8.652611e-04  3.008362e+01

 Direction cosine interval: 5.000000e-01 1.000000e+00


 Incident energy interval in MeV: 1.000000e+00 1.964000e+01

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    0.000000e+00  0.000000e+00
 1.234098e-03  3.019738e-01    0.000000e+00  0.000000e+00
 3.019738e-01  1.964033e+01    -1.259827e-03  1.676275e+01

 Incident energy interval in MeV: 1.100000e-11 1.000000e+00

 E min          E max              S(E)         sigma

 1.000010e-11  1.234098e-03    -4.974350e-07  6.117176e+00
 1.234098e-03  3.019738e-01    5.300126e-04  6.247552e+01
 3.019738e-01  1.964033e+01    -3.005206e-03  1.017811e+01

 Energy integrated S           -3.661409e-17  9.339996e+01



	  KSTEP ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 5 batches

	 number of batch used: 115	 keff = 9.956131e-01	 sigma = 8.121986e-04	 sigma% = 8.157773e-02


	  KCOLL ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 6 batches

	 number of batch used: 114	 keff = 9.957839e-01	 sigma = 6.040021e-04	 sigma% = 6.065594e-02


	  KTRACK  ESTIMATOR
	 -------------------- 


 	 best results are obtained with discarding 5 batches

	 number of batch used: 115	 keff = 9.961751e-01	 sigma = 4.986042e-04	 sigma% = 5.005187e-02


	  MACRO KCOLL ESTIMATOR
	 ---------------------------- 


 	 best results are obtained with discarding 5 batches

	 number of batch used: 115	 keff = 9.957877e-01	 sigma = 5.886514e-04	 sigma% = 5.911415e-02


 simulation time (s) : 159


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 20427 28694 30088  COUNTER	96405776


=====================================================================
	NORMAL COMPLETION
=====================================================================
