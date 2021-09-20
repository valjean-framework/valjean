
=====================================================================
$Id: t4main.cc,v 2.73.2.1 2015/10/07 14:12:44 tv232747 Exp $
 hostname: is232540
 pid: 17360

=====================================================================
$Id: t4main.cc,v 2.73.2.1 2015/10/07 14:12:44 tv232747 Exp $

 HOSTNAME : is232540

 PROCESS ID is : 17360

 DATE : Mon Feb 19 09:12:44 2018

 Version is $Name: tripoli4_10_2 $.

=====================================================================

 data filename = input/tungstene.d
 catalogname = /home/tripoli4.10/tripoli4.10.2/Env/t4path.ceav512
 execution call = tripoli4 -s NJOY -a -c /home/tripoli4.10/tripoli4.10.2/Env/t4path.ceav512 -d input/tungstene.d -o output/tungstene.d.res.ceav5 


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


GEOMETRIE
TITRE

SURF 1 SPHERE 0 0 0 100
SURF 2 SPHERE 0 0 0 0.1

VOLU 1 EQUA PLUS 1 2 MOINS 1 1 FINV
VOLU 2 EQUA MOINS 1 2 FINV

FING

COMPOSITION 2
	PONCTUAL  300 MEDIUM	1 W	1.e-6
	PONCTUAL  300 VOID	1 HE	1.e-10
FIN_COMPOSITION


GEOMCOMP
  MEDIUM 1 2
  VOID 1 1
FIN_GEOMCOMP


LIST_DECOUPAGE 1 
  DEC_INTEG4     4 20. 2. 1.99 1.E-11
FIN_LIST_DECOUPAGE

REPONSES 1
	FLUX		PHOTON
FIN_REPONSES


SCORE  1

        1 TRACK DECOUPAGE DEC_INTEG4 EXTENDED_MESH
          STORE_IN_FILE
	  WINDOW
	    	99	0	-1.
		99.9	6.283185	1.
		1	1	17
	  REPERE SPHEREMU
              	0	0	0
                1       0       0
                0       0       1

FIN_SCORE


LIST_SOURCE     1  NORME 1
        SOURCE PHOTON 
	  PONCTUAL  0  0 0
	  ANGULAR_DISTRIBUTION    MONO_DIR 0 0 1
	  ENERGETIC_DISTRIBUTION  SPECTRE MONOCINETIQUE 2
	  TIME_DISTRIBUTION       DIRAC 0.
	  FIN_SOURCE
FIN_LIST_SOURCE



SIMULATION
	PROTECTION
        // BATCH 50 SIZE 20000
	EDITION 1000
        BATCH 1000 SIZE 50000
        PARTICULES 1 PHOTON
	ENERGY_INF PHOTON 1.e-3
FIN_SIMULATION








Total concentration of material MEDIUM (1.E24at/cm3) is: 1.000000e-06
Total concentration of material VOID (1.E24at/cm3) is: 1.000000e-10


 Loading response functions ...
 Constructing score  ...0
 SOURCE INITIALIZATION ...

	 initializing source number : 0

		 Energetic density definition intensity = 1.000000e+00

		 Energetic density simulation intensity = 1.000000e+00

		 Angular intensity = 1.000000e+00

		 Time intensity = 1.000000e+00

		 Geometric intensity = 1.000000e+00

		 Calculated source simulation intensity = 1.000000e+00

		 Calculated source definition intensity = 1.000000e+00

	         SIMULATION INTENSITY = 1.000000e+00   BIASED SIMULATION INTENSITY = 1.000000e+00

   SUM OF SIMULATION INTENSITIES = 1.000000e+00

   GLOBAL NORM = 1.000000e+00   GLOBAL SIMULATION INTENSITY = 1.000000e+00

   BIASED TOTAL SOURCE INTENSITY = 1.000000e+00


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 38

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 39

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 40

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 41

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 42

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 43

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 44

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 45

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 46

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 47

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 48

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 49

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 50

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 51

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 52

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 53

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 54

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 55

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 56

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 57

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 58

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 59

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 60

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 61

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 62

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 63

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 64

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 65

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 66

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 67

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 68

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 69

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 70

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 71

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 72

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 73

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 74

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 75

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 76

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 77

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 78

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 79

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 80

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 81

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 82

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 83

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 84

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 85

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 86

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 87

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 88

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 89

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 90

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 91

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 92

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 93

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 94

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 95

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 96

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 97

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 98

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 99

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 100

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 101

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 102

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 103

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 104

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 105

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 106

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 107

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 108

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 109

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 110

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 111

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 112

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 113

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 114

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 115

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 116

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 117

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 118

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 119

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 120

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 121

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 122

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 123

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 124

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 125

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 126

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 127

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 128

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 129

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 130

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 131

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 132

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 133

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 134

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 135

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 136

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 137

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 138

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 139

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 140

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 141

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 142

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 143

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 144

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 145

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 146

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 147

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 148

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 149

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 150

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 151

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 152

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 153

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 154

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 155

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 156

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 157

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 158

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 159

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 160

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 161

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 162

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 163

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 164

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 165

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 166

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 167

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 168

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 169

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 170

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 171

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 172

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 173

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 174

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 175

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 176

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 177

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 178

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 179

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 180

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 181

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 182

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 183

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 184

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 185

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 186

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 187

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 188

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 189

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 190

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 191

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 192

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 193

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 194

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 195

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 196

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 197

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 198

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 199

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 200

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 201

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 202

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 203

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 204

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 205

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 206

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 207

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 208

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 209

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 210

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 211

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 212

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 213

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 214

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 215

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 216

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 217

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 218

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 219

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 220

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 221

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 222

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 223

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 224

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 225

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 226

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 227

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 228

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 229

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 230

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 231

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 232

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 233

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 234

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 235

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 236

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 237

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 238

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 239

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 240

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 241

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 242

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 243

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 244

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 245

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 246

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 247

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 248

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 249

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 250

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 251

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 252

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 253

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 254

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 255

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 256

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 257

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 258

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 259

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 260

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 261

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 262

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 263

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 264

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 265

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 266

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 267

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 268

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 269

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 270

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 271

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 272

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 273

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 274

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 275

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 276

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 277

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 278

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 279

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 280

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 281

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 282

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 283

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 284

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 285

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 286

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 287

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 288

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 289

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 290

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 291

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 292

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 293

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 294

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 295

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 296

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 297

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 298

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 299

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 300

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 301

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 302

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 303

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 304

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 305

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 306

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 307

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 308

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 309

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 310

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 311

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 312

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 313

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 314

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 315

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 316

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 317

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 318

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 319

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 320

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 321

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 322

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 323

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 324

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 325

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 326

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 327

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 328

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 329

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 330

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 331

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 332

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 333

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 334

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 335

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 336

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 337

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 338

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 339

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 340

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 341

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 342

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 343

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 344

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 345

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 346

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 347

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 348

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 349

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 350

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 351

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 352

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 353

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 354

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 355

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 356

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 357

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 358

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 359

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 360

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 361

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 362

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 363

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 364

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 365

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 366

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 367

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 368

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 369

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 370

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 371

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 372

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 373

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 374

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 375

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 376

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 377

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 378

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 379

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 380

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 381

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 382

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 383

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 384

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 385

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 386

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 387

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 388

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 389

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 390

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 391

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 392

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 393

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 394

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 395

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 396

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 397

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 398

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 399

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 400

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 401

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 402

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 403

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 404

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 405

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 406

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 407

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 408

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 409

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 410

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 411

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 412

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 413

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 414

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 415

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 416

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 417

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 418

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 419

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 420

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 421

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 422

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 423

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 424

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 425

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 426

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 427

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 428

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 429

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 430

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 431

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 432

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 433

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 434

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 435

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 436

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 437

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 438

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 439

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 440

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 441

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 442

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 443

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 444

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 445

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 446

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 447

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 448

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 449

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 450

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 451

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 452

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 453

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 454

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 455

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 456

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 457

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 458

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 459

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 460

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 461

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 462

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 463

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 464

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 465

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 466

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 467

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 468

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 469

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 470

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 471

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 472

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 473

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 474

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 475

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 476

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 477

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 478

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 479

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 480

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 481

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 482

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 483

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 484

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 485

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 486

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 487

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 488

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 489

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 490

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 491

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 492

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 493

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 494

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 495

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 496

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 497

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 498

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 499

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 500

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 501

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 502

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 503

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 504

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 505

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 506

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 507

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 508

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 509

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 510

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 511

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 512

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 513

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 514

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 515

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 516

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 517

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 518

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 519

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 520

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 521

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 522

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 523

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 524

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 525

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 526

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 527

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 528

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 529

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 530

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 531

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 532

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 533

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 534

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 535

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 536

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 537

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 538

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 539

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 540

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 541

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 542

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 543

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 544

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 545

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 546

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 547

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 548

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 549

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 550

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 551

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 552

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 553

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 554

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 555

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 556

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 557

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 558

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 559

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 560

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 561

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 562

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 563

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 564

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 565

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 566

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 567

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 568

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 569

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 570

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 571

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 572

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 573

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 574

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 575

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 576

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 577

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 578

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 579

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 580

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 581

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 582

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 583

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 584

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 585

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 586

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 587

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 588

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 589

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 590

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 591

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 592

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 593

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 594

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 595

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 596

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 597

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 598

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 599

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 600

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 601

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 602

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 603

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 604

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 605

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 606

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 607

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 608

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 609

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 610

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 611

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 612

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 613

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 614

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 615

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 616

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 617

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 618

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 619

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 620

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 621

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 622

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 623

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 624

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 625

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 626

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 627

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 628

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 629

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 630

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 631

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 632

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 633

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 634

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 635

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 636

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 637

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 638

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 639

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 640

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 641

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 642

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 643

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 644

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 645

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 646

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 647

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 648

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 649

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 650

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 651

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 652

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 653

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 654

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 655

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 656

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 657

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 658

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 659

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 660

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 661

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 662

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 663

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 664

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 665

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 666

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 667

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 668

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 669

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 670

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 671

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 672

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 673

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 674

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 675

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 676

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 677

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 678

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 679

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 680

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 681

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 682

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 683

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 684

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 685

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 686

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 687

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 688

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 689

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 690

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 691

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 692

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 693

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 694

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 695

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 696

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 697

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 698

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 699

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 700

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 701

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 702

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 703

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 704

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 705

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 706

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 707

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 708

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 709

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 710

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 711

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 712

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 713

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 714

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 715

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 716

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 717

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 718

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 719

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 720

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 721

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 722

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 723

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 724

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 725

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 726

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 727

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 728

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 729

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 730

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 731

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 732

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 733

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 734

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 735

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 736

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 737

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 738

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 739

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 740

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 741

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 742

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 743

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 744

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 745

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 746

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 747

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 748

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 749

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 750

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 751

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 752

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 753

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 754

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 755

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 756

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 757

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 758

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 759

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 760

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 761

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 762

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 763

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 764

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 765

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 766

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 767

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 768

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 769

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 770

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 771

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 772

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 773

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 774

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 775

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 776

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 777

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 778

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 779

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 780

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 781

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 782

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 783

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 784

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 785

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 786

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 787

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 788

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 789

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 790

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 791

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 792

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 793

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 794

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 795

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 796

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 797

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 798

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 799

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 800

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 801

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 802

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 803

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 804

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 805

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 806

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 807

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 808

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 809

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 810

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 811

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 812

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 813

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 814

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 815

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 816

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 817

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 818

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 819

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 820

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 821

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 822

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 823

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 824

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 825

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 826

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 827

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 828

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 829

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 830

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 831

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 832

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 833

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 834

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 835

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 836

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 837

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 838

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 839

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 840

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 841

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 842

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 843

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 844

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 845

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 846

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 847

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 848

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 849

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 850

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 851

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 852

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 853

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 854

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 855

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 856

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 857

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 858

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 859

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 860

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 861

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 862

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 863

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 864

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 865

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 866

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 867

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 868

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 869

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 870

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 871

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 872

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 873

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 874

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 875

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 876

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 877

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 878

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 879

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 880

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 881

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 882

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 883

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 884

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 885

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 886

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 887

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 888

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 889

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 890

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 891

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 892

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 893

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 894

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 895

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 896

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 897

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 898

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 899

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 900

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 901

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 902

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 903

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 904

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 905

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 906

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 907

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 908

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 909

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 910

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 911

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 912

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 913

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 914

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 915

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 916

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 917

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 918

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 919

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 920

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 921

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 922

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 923

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 924

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 925

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 926

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 927

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 928

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 929

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 930

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 931

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 932

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 933

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 934

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 935

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 936

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 937

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 938

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 939

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 940

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 941

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 942

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 943

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 944

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 945

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 946

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 947

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 948

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 949

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 950

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 951

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 952

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 953

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 954

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 955

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 956

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 957

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 958

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 959

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 960

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 961

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 962

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 963

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 964

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 965

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 966

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 967

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 968

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 969

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 970

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 971

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 972

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 973

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 974

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 975

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 976

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 977

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 978

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 979

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

 batch number : 980

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 981

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 982

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 983

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 984

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 985

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 986

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 987

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 988

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 989

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 990

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 991

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 992

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 993

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 994

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 995

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 996

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 997

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 998

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 batch number : 999

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 0.000000e+00	 sigma_n : 0.000000e+00

 Type and parameters of random generator before batch 1000 : 
	 DRAND48_RANDOM 23167 55754 25329  COUNTER	149701908


 batch number : 1000

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 2.000000e-05	 sigma_n : 2.000000e-05

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.000000e+00
*********************************************************


 Mean weight leakage = 4.995050e+04	 sigma = 4.950000e+01	 sigma% = 9.909811e-02


 Edition after batch number : 1000



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : 
ENERGY DECOUPAGE NAME : DEC_INTEG4


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  tally   	  sigma (percent)


Energy range (in MeV): 2.000000e+01 - 2.000000e+00
	 (0,0,0)	 0.000000e+00	0.000000e+00
	 (0,0,1)	 0.000000e+00	0.000000e+00
	 (0,0,2)	 0.000000e+00	0.000000e+00
	 (0,0,3)	 0.000000e+00	0.000000e+00
	 (0,0,4)	 0.000000e+00	0.000000e+00
	 (0,0,5)	 0.000000e+00	0.000000e+00
	 (0,0,6)	 0.000000e+00	0.000000e+00
	 (0,0,7)	 0.000000e+00	0.000000e+00
	 (0,0,8)	 0.000000e+00	0.000000e+00
	 (0,0,9)	 0.000000e+00	0.000000e+00
	 (0,0,10)	 0.000000e+00	0.000000e+00
	 (0,0,11)	 0.000000e+00	0.000000e+00
	 (0,0,12)	 0.000000e+00	0.000000e+00
	 (0,0,13)	 0.000000e+00	0.000000e+00
	 (0,0,14)	 0.000000e+00	0.000000e+00
	 (0,0,15)	 0.000000e+00	0.000000e+00
	 (0,0,16)	 9.000005e-01	1.442627e-05

Energy range (in MeV): 2.000000e+00 - 1.990000e+00
	 (0,0,0)	 0.000000e+00	0.000000e+00
	 (0,0,1)	 0.000000e+00	0.000000e+00
	 (0,0,2)	 0.000000e+00	0.000000e+00
	 (0,0,3)	 0.000000e+00	0.000000e+00
	 (0,0,4)	 0.000000e+00	0.000000e+00
	 (0,0,5)	 0.000000e+00	0.000000e+00
	 (0,0,6)	 0.000000e+00	0.000000e+00
	 (0,0,9)	 0.000000e+00	0.000000e+00
	 (0,0,10)	 0.000000e+00	0.000000e+00
	 (0,0,11)	 0.000000e+00	0.000000e+00
	 (0,0,12)	 0.000000e+00	0.000000e+00
	 (0,0,13)	 0.000000e+00	0.000000e+00
	 (0,0,14)	 0.000000e+00	0.000000e+00
	 (0,0,15)	 0.000000e+00	0.000000e+00
	 (0,0,16)	 1.654347e-08	1.000000e+02

Energy range (in MeV): 1.990000e+00 - 1.000000e-11
	 (0,0,0)	 3.308814e-08	7.067528e+01
	 (0,0,1)	 4.963272e-08	7.450565e+01
	 (0,0,2)	 3.309082e-08	7.067528e+01
	 (0,0,3)	 1.265943e-07	4.654161e+01
	 (0,0,4)	 2.231006e-08	7.850459e+01
	 (0,0,5)	 0.000000e+00	0.000000e+00
	 (0,0,6)	 6.619889e-08	6.118649e+01
	 (0,0,7)	 1.654347e-08	1.000000e+02
	 (0,0,8)	 3.309055e-08	7.067528e+01
	 (0,0,9)	 4.964644e-08	5.767721e+01
	 (0,0,10)	 5.969109e-08	6.418034e+01
	 (0,0,11)	 5.614107e-08	5.227803e+01
	 (0,0,12)	 3.308739e-08	1.000000e+02
	 (0,0,13)	 3.308763e-08	7.067528e+01
	 (0,0,14)	 6.617754e-08	4.992487e+01
	 (0,0,15)	 3.308816e-08	7.067528e+01
	 (0,0,16)	 2.977867e-07	2.336882e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 3.308814e-08	7.067528e+01
	 (0,0,1)	 4.963272e-08	7.450565e+01
	 (0,0,2)	 3.309082e-08	7.067528e+01
	 (0,0,3)	 1.265943e-07	4.654161e+01
	 (0,0,4)	 2.231006e-08	7.850459e+01
	 (0,0,5)	 0.000000e+00	0.000000e+00
	 (0,0,6)	 6.619889e-08	6.118649e+01
	 (0,0,7)	 1.654347e-08	1.000000e+02
	 (0,0,8)	 3.309055e-08	7.067528e+01
	 (0,0,9)	 4.964644e-08	5.767721e+01
	 (0,0,10)	 5.969109e-08	6.418034e+01
	 (0,0,11)	 5.614107e-08	5.227803e+01
	 (0,0,12)	 3.308739e-08	1.000000e+02
	 (0,0,13)	 3.308763e-08	7.067528e+01
	 (0,0,14)	 6.617754e-08	4.992487e+01
	 (0,0,15)	 3.308816e-08	7.067528e+01
	 (0,0,16)	 9.000008e-01	1.179045e-05

number of batches used: 1000	9.000016e-01	4.579240e-06


 simulation time (s) : 423


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 31740 1563 11498  COUNTER	149851915


=====================================================================
	NORMAL COMPLETION
=====================================================================
