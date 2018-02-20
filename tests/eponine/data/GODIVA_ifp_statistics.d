// Godiva
//
///////////////////////////////////////
//                                   //
//     ENDF/B-VII.0  keff   std      //
//     Experiment :  1.0000 (10)     //
//     MCNP5-1.60 :  0.9995  (5)     //
//                                   //
///////////////////////////////////////

// IFP Kinetics Parameters
//
// Rossi alpha
// measure : -111 ± 2
// T4 (CEAv5.1) : -113 ± 0.57
//
// Beta eff
// measure : 645 ± 13
// T4 (CEAv5.1) : 646 ± 3
//
// Lambda eff
// computed from Beta eff and Rossi alpha : 5.8
// T4 (CEAv5.1) : 5.71 ± 0.0036


GEOMETRIE
TITRE Godiva  Solid Bare HEU sphere  HEU-MET-FAST-001

SURF 1 SPHERE 0. 0. 0. 8.7407
VOLU 1 EQUA 
          MOINS 1 1
FINV // SPHERE HEU

FINGEOM

COMPOSITION 1

//HEU Metal
PUNCTUAL 294 MF 3
U234    4.9184E-04
U235    4.4994E-02
U238    2.4984E-03

FIN_COMPOSITION

GEOMCOMP
MF 1 1

FIN_GEOMCOMP

LIST_SOURCE 1
SOURCE
   COEFF 1.0
NEUTRON
FACTORIZED FRAME SPHERE
     0 0 0
     1 0 0
     0 0 1
VOLU 1 1
GEOMETRIC_DISTRIBUTION
     ANALYTICAL
     FUNCTION = 1 ;
     DOMAIN = 0 < R < 8.7407,
              0 < RTHETA < 3.14159,
              0 < RPHI < 6.28318 ;
ANGULAR_DISTRIBUTION 
   ISOTROPIC
ENERGETIC_DISTRIBUTION
   SPECTRE WATT_SPECTRE
       PARAM 20 1.E-11 1.036 2.29
TIME_DISTRIBUTION DIRAC 0
FIN_SOURCE
FIN_LIST_SOURCE

SIMULATION
	BATCH 200
	SIZE 5000
	EDITION 200
	DISCARD 100
	CRITIC
	KINETIC_PARAMETERS
	BETA_EFFECTIVE
	IFP_KINETIC_PARAMETERS IFP_CYCLE_LENGTH 20
		IFP_CONVERGENCE_STATISTICS
	PARTICLE 1 NEUTRON
FIN_SIMULATION
