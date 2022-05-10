
=====================================================================
$Id$
 hostname: is232540
 pid: 15954

=====================================================================
$Id$

 HOSTNAME : is232540

 PROCESS ID is : 15954

 DATE : Mon Oct 18 15:19:38 2021

 Version is $Name$.

 git version is d2850256cb52f78f005a540de5f0b8f2a710e041 (CLEAN).

=====================================================================

 data filename = extended_mesh_cartesian_info.t4
 catalogname = /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512
 execution call = tripoli4 -c /home/tripoli4.11/tripoli4.11.1/Env/t4path.ceav512 -s NJOY -a -u -d extended_mesh_cartesian_info.t4 -o extended_mesh_cartesian_info_NEW.res 


 dictionary file : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/ceav512.dictionary
 mass file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/mass_rmd.mas95
 Q fission directory : /data/tmpuranus2/GALILEE-V0-3.0/CEAV512/Qfission
 electron cross section directory : /data/tmpuranus2/GALILEE-V0-3.0/PEID/Electron_Photon
 electron bremsstrahlung cross section directory : /home/tripoli4.11/tripoli4.11.1/AdditionalData/Bremsstrahlung
 abondance file : /data/tmpuranus2/GALILEE-V0-3.0/Standard_data/abundance
 own evaluations directory : 

  reading geometry : 
  checking association of compositions and volumes :  ok 



	 WARNING :  running photon without electron and positron
	 possible lack of bremsstrahlung photons


LANG ENGLISH

GEOMETRY
TITLE Tests for cartesian extended meshes

// world volume
TYPE   1  SPHERE 500.

// target
TYPE   2  BOX 200 200 3

// the world volume
VOLU   1  COMBI 1  0. 0. 0. ENDV

// the unrotated target volume
VOLU   2  COMBI 2  0. 0. 0. FICTIVE ENDV

// the rotated target volume
VOLU   3  ROTATION VOLU 2 1 0 0 45 0 0 0 SMASH 1 1 ENDV

ENDG


//UNITS
//  LENGTH 0.01 dm
//END_UNITS

COMPOSITION 2
	DENSITY 300 silver 1 1
		AG-NAT	1.

	DENSITY 300 VOID 1 1
		AG-NAT	1.

END_COMPOSITION

GEOMCOMP
  VOID      1 1
  silver 1 3
END_GEOMCOMP

SOURCES_LIST
	1
	SOURCE
		PHOTON
		POINT -3.1 0 1
		ANGULAR_DISTRIBUTION ISOTROPIC
		ENERGETIC_DISTRIBUTION SPECTRUM MONOKINETIC 1
		TIME_DISTRIBUTION DIRAC 0.
	END_SOURCE
	
END_SOURCES_LIST


RESPONSES 1
  NAME photon_flux_response FLUX PHOTON
END_RESPONSES

GRID_LIST
1
grid_score
3 0 1 20
END_GRID_LIST

/*
	This data set defines multiple scores for cartesian extended meshes
	
	Each mesh contains a group of scores. Within each mesh, a reference is calculated with a regular window (keyword WINDOW) and with the tracking estimator (TRACK). Then, some functionalities are tested for this group (listed below). Each values should be consistent between scores in the same given mesh (or at least integrated results if specified so).
	Tables of volumes are given after mesh descriptions in order to compare normalized results.

	
	Meshes and score built :
	
	- Mesh 1 : scores 1 to 6 : simple mesh with three cells
		Tested functionalities : STORE_IN_FILE, NORMALIZE, COLL estimator, WINDOW_VARIABLE
		
	- Mesh 2 : scores 7 and 8 : mesh 1 without cylindrical center cell (radius from 0 to 1)
		Tested functionalities : WINDOW_VARIABLE, Mesh recovering with mesh1
	
	- Mesh 3 : scores 9 and 10 : shifted mesh 1
		Tested functionalities : WINDOW_VARIABLE
	
	- Mesh 4 : scores 11 and 12 : rotated mesh 3
		Tested functionalities : WINDOW_VARIABLE
	
	- Mesh 5 : scores 13 to 16 : mesh 4 with angular and height slicing
		Tested functionalities : WINDOW_VARIABLE, COLL estimator
	
	- Mesh 6 : scores 17 and 18 : mesh 5 without center cell
		Tested functionalities : WINDOW_VARIABLE, Mesh recovering with mesh5
		
	- Mesh 7 : scores 19 and 20 : mesh 5 with only center cell (mesh 6 + 7 = mesh 5)
		Tested functionalities : WINDOW_VARIABLE, Mesh recovering with mesh5
	
	- Mesh 8 : score 21 and 22 : they use distinct meshes (regular vs variable) and a different meshing, but they have the same boundary
		Tested functionalities : these two scores should have the same integrated result
		
	- Mesh 9 : score 23 and 24 : use of an irregular meshing to test the NORMALIZE option (previously, meshing was regular)
		Tested functionalities : STORE_IN_FILE, NORMALIZE
		
	- Mesh 10 : score 25 and 26 : comparison between a score on a meshed volume and a score on a volume
		Tested functionalities : these scores should have the same integrated value.
		
	- Mesh 11 : scores 27 and 28 : same as mesh1 with TRIANGLEZ
		Tested functionalities : STORE_IN_FILE, NORMALIZE, TRIANGLEZ
		
	- Mesh 12 : scores 29 to 32 : one is built with negative coordinates, the other with a translation
		Tested functionalities : Negative coordinates, STORE_IN_FILE, NORMALIZE
		
		
		
					           Mesh 1 volumes
							 -----------------
							| Cell  |  Volume | 
							|-------|---------|
							| 0 0 0 |     2.0 |
							| 1 0 0 |     2.0 |
							| 2 0 0 |     2.0 |
					
					
					            Mesh 9 volumes
					         ------------------
							| Cell  |  Volume  |
							|-------|----------|
							| 0 0 0 |     0.02 |
							| 0 0 1 |     0.18 |
							| 0 1 0 |     0.03 |
							| 0 1 1 |     0.27 |
							| 0 2 0 |     0.15 |
							| 0 2 1 |     1.35 |
							| 1 0 0 |     0.04 |
							| 1 0 1 |     0.36 |
							| 1 1 0 |     0.06 |
							| 1 1 1 |     0.54 |
							| 1 2 0 |     0.30 |
							| 1 2 1 |     2.70 |
							
							
							  Mesh 11 volumes
							 -----------------
							| Cell  |  Volume | 
							|-------|---------|
							| 0 0 0 |     1.0 |
							| 0 1 0 |     1.0 |
							| 1 0 0 |     1.0 |
							| 1 1 0 |     1.0 |
							| 2 0 0 |     1.0 |
							| 2 1 0 |     1.0 |
						
*/

SCORES 32

  COMMENT
				SCORE 1

				STORE_IN_FILE
  COMMENT
  
  
  NAME mesh1_reg_track
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 2

				STORE_IN_FILE
				NORMALIZE : compare with score 1
  COMMENT
  
  NAME mesh1_reg_norm
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH 
  STORE_IN_FILE
  NORMALIZE
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 3

				COLL estimator : compare with score 1
  COMMENT
  
  NAME mesh1_reg_coll
  photon_flux_response COLL
  GRID grid_score
  EXTENDED_MESH 
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 4

				STORE_IN_FILE
				WINDOW_VARIABLE : compare to score 1
  COMMENT
  
  NAME mesh1_var_track
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  WINDOW_VARIABLE
  3 1 1
  0 1 1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 5

				STORE_IN_FILE
				NORMALIZE : compare with score 4
  COMMENT
  
  NAME mesh1_var_norm
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  NORMALIZE
  WINDOW_VARIABLE
  3 1 1
  0 1 1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 6

				COLL estimator : compare with score 4
  COMMENT
  
  NAME mesh1_var_coll
  photon_flux_response COLL
  GRID grid_score
  EXTENDED_MESH
  ENTROPY
  WINDOW_VARIABLE
  3 1 1
  0 1 1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 7
				
				Mesh recovering : compare spectrum values to score 1
  COMMENT
  
  NAME mesh2_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH
  ENTROPY
  NORMALIZE
  WINDOW
  1 0 0
  3 2 1
  2 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 8

				WINDOW_VARIABLE : compare to score 7
  COMMENT
  
  NAME mesh2_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  ENTROPY
  WINDOW_VARIABLE
  2 1 1
  1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 9

  COMMENT
  
  NAME mesh3_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  ENTROPY
  NORMALIZE
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 10

				WINDOW_VARIABLE : compare to score 9
  COMMENT
  
  NAME mesh3_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  3 1 1
  0 1 1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 11

  COMMENT
  
  NAME mesh4_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 12

				WINDOW_VARIABLE : compare to score 11
  COMMENT
  
  NAME mesh4_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  3 1 1
  0 1 1 1 2 1 3
  0 1 2
  0 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 13

  COMMENT
  
  NAME mesh5_reg_track
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  0 0 0
  3 2 1
  3 2 2
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 14

				COLL estimator : compare to score 13
  COMMENT
  
  NAME mesh5_reg_coll
  photon_flux_response COLL
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  0 0 0
  3 2 1
  3 2 2
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 15

				WINDOW_VARIABLE : compare to score 13
  COMMENT
  
  NAME mesh5_var_track
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  3 2 2
  0 1 1 1 2 1 3
  0 1 1 1 2
  0 1 0.5 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 16

				COLL estimator : compare to score 15
  COMMENT
  
  NAME mesh5_var_coll
  photon_flux_response COLL
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  3 2 2
  0 1 1 1 2 1 3
  0 1 1 1 2
  0 1 0.5 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 17

				Mesh recovering : compare spectrum values to score 13
  COMMENT
  
  NAME mesh6_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  1 0 0
  3 2 1
  2 2 2
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 18

				WINDOW_VARIABLE : compare to score 17
  COMMENT
  
  NAME mesh6_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  2 2 2
  1 2 3
  0 2 2
  0 2 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 19
				
				Mesh recovering : compare spectrum values to score 13

  COMMENT
  
  NAME mesh7_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  0 0 0
  1 2 1
  1 2 2
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 20

				WINDOW_VARIABLE : compare to score 19
  COMMENT
  
  NAME mesh7_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  1 2 2
  0 1 1
  0 2 2
  0 2 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 21

  COMMENT
  
  NAME mesh8_reg
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  0 0 0
  3 2 1
  3 2 7
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 22

				WINDOW_VARIABLE : compare integrated to score 21
  COMMENT
  
  NAME mesh8_var
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW_VARIABLE
  11 8 2
  0 11 3
  0 8 2
  0 2 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 23

				STORE_IN_FILE
  COMMENT
  
  NAME mesh9
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  WINDOW_VARIABLE
  2 3 2
  0 1 1 1 3
  0 1 0.2 1 0.5 1 2
  0 1 0.1 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 24

				STORE_IN_FILE
				NORMALIZE : compare with score 23
  COMMENT
  
  NAME mesh9_norm
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  NORMALIZE
  WINDOW_VARIABLE
  2 3 2
  0 1 1 1 3
  0 1 0.2 1 0.5 1 2
  0 1 0.1 1 1
  FRAME CARTESIAN
  -0.2 0.2 -1
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 25

  COMMENT
  
  NAME mesh10
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  WINDOW
  -100 -100 -1.5
  100 100 1.5
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 0.7071068 -0.7071068
  0 0.7071068 0.7071068
  
  
  COMMENT
				SCORE 26

				Target volume computation : compare integrated with score 25
  COMMENT
  
  NAME vol10
  photon_flux_response TRACK
  GRID grid_score
  VOLUME LIST 1 3
  
  
  COMMENT
				SCORE 27

				STORE_IN_FILE
				TRIANGLEZ : compare to score 1
  COMMENT
  
  
  NAME mesh11
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  TRIANGLEZ
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 28

				STORE_IN_FILE
				NORMALIZE : compare with score 27
  COMMENT
  
  NAME mesh11_norm
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  TRIANGLEZ
  NORMALIZE
  WINDOW
  0 0 0
  3 2 1
  3 1 1
  FRAME CARTESIAN
  0 0 0
  1 0 0
  0 1 0
  0 0 1
  
  
  COMMENT
				SCORE 29
				
				STORE_IN_FILE

  COMMENT
  
  NAME mesh11.1
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  WINDOW_VARIABLE
  11 8 2
  0 7 1 4 3
  0 5 1.1 3 2
  0 1 0.7 1 1
  FRAME CARTESIAN
  -1 -2 -3
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 30
				STORE_IN_FILE
				Negative coordinates : compare to score 29

  COMMENT
  
  NAME mesh11.2
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  WINDOW_VARIABLE
  11 8 2
  -5 7 -4 4 -2
  -4 5 -2.9 3 -2
  -3 1 -2.3 1 -2
  FRAME CARTESIAN
  0.65965442  4.87351683 -3.01770998
  3 2 1
  -1 4 -5
  -1 1 1
  
  COMMENT
				SCORE 31
				
				STORE_IN_FILE
				NORMALIZE : compare with score 29

  COMMENT
  
  NAME mesh11.1
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  NORMALIZE
  WINDOW_VARIABLE
  11 8 2
  0 7 1 4 3
  0 5 1.1 3 2
  0 1 0.7 1 1
  FRAME CARTESIAN
  -1 -2 -3
  3 2 1
  -1 4 -5
  -1 1 1
  
  
  COMMENT
				SCORE 32
				STORE_IN_FILE
				NORMALIZE :  : compare with score 30
				Negative coordinates : compare to score 31

  COMMENT
  
  NAME mesh11.2
  photon_flux_response TRACK
  GRID grid_score
  EXTENDED_MESH MESH_INFO
  STORE_IN_FILE
  NORMALIZE
  WINDOW_VARIABLE
  11 8 2
  -5 7 -4 4 -2
  -4 5 -2.9 3 -2
  -3 1 -2.3 1 -2
  FRAME CARTESIAN
  0.65965442  4.87351683 -3.01770998
  3 2 1
  -1 4 -5
  -1 1 1
  
  
END_SCORES

SIMULATION
	BATCH 50
	SIZE 1000
        EDITION 50
	PARTICLES 1 PHOTON
	ENERGY_INF PHOTON 1e-3
        MONITORING 0
END_SIMULATION




 data reading time (s): 0
 Concentration (1.000000e+24 at/cm3) of AG107 in silver is: 2.894107e-03
 Concentration (1.000000e+24 at/cm3) of AG109 in silver is: 2.688766e-03

 Total concentration of material silver (1.E24at/cm3) is: 5.582873e-03
 Concentration (1.000000e+24 at/cm3) of AG107 in VOID is: 2.894107e-03
 Concentration (1.000000e+24 at/cm3) of AG109 in VOID is: 2.688766e-03

 Total concentration of material VOID (1.E24at/cm3) is: 5.582873e-03


 Loading response functions ...
 Constructing score  ...0
 Constructing score  ...1
 Constructing score  ...2
 Constructing score  ...3
 Constructing score  ...4
 Constructing score  ...5
 Constructing score  ...6
 Constructing score  ...7
 Constructing score  ...8
 Constructing score  ...9
 Constructing score  ...10
 Constructing score  ...11
 Constructing score  ...12
 Constructing score  ...13
 Constructing score  ...14
 Constructing score  ...15
 Constructing score  ...16
 Constructing score  ...17
 Constructing score  ...18
 Constructing score  ...19
 Constructing score  ...20
 Constructing score  ...21
 Constructing score  ...22
 Constructing score  ...23
 Constructing score  ...24
 Constructing score  ...25
 Constructing score  ...26
 Constructing score  ...27
 Constructing score  ...28
 Constructing score  ...29
 Constructing score  ...30
 Constructing score  ...31
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

   GLOBAL SIMULATION INTENSITY = 1.256637e+01

   BIASED TOTAL SOURCE INTENSITY = 1.256637e+01


 initialization time (s): 0


 Type and parameters of random generator before batch 1 : 
	 DRAND48_RANDOM 123 13 37  COUNTER	0


 batch number : 1

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.977000e+00	 sigma_n : 5.028916e-02

 simulation time (s) : 0


 batch number : 2

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.027000e+00	 sigma_n : 5.246927e-02

 simulation time (s) : 0


 batch number : 3

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.843000e+00	 sigma_n : 4.497081e-02

 simulation time (s) : 0


 batch number : 4

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.945000e+00	 sigma_n : 4.791942e-02

 simulation time (s) : 0


 batch number : 5

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.882000e+00	 sigma_n : 4.722612e-02

 simulation time (s) : 0


 batch number : 6

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.997000e+00	 sigma_n : 5.094690e-02

 simulation time (s) : 0


 batch number : 7

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.933000e+00	 sigma_n : 4.832024e-02

 simulation time (s) : 0


 batch number : 8

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.000000e+00	 sigma_n : 4.968368e-02

 simulation time (s) : 0


 batch number : 9

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.940000e+00	 sigma_n : 4.858766e-02

 simulation time (s) : 0


 batch number : 10

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.901000e+00	 sigma_n : 4.822369e-02

 simulation time (s) : 0


 batch number : 11

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.862000e+00	 sigma_n : 4.535431e-02

 simulation time (s) : 0


 batch number : 12

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.966000e+00	 sigma_n : 5.035255e-02

 simulation time (s) : 0


 batch number : 13

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.937000e+00	 sigma_n : 4.847041e-02

 simulation time (s) : 1


 batch number : 14

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.049000e+00	 sigma_n : 5.123694e-02

 simulation time (s) : 1


 batch number : 15

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.926000e+00	 sigma_n : 4.966881e-02

 simulation time (s) : 1


 batch number : 16

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.942000e+00	 sigma_n : 4.914317e-02

 simulation time (s) : 1


 batch number : 17

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.896000e+00	 sigma_n : 4.871917e-02

 simulation time (s) : 1


 batch number : 18

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.956000e+00	 sigma_n : 4.800384e-02

 simulation time (s) : 1


 batch number : 19

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.880000e+00	 sigma_n : 4.833152e-02

 simulation time (s) : 1


 batch number : 20

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.928000e+00	 sigma_n : 4.695765e-02

 simulation time (s) : 1


 batch number : 21

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.912000e+00	 sigma_n : 4.637247e-02

 batch number : 22

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.053000e+00	 sigma_n : 5.008692e-02

 batch number : 23

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.876000e+00	 sigma_n : 4.605154e-02

 batch number : 24

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.857000e+00	 sigma_n : 4.782089e-02

 batch number : 25

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.865000e+00	 sigma_n : 4.738164e-02

 batch number : 26

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.918000e+00	 sigma_n : 4.818296e-02

 batch number : 27

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.920000e+00	 sigma_n : 4.679519e-02

 batch number : 28

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.834000e+00	 sigma_n : 4.626645e-02

 batch number : 29

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.894000e+00	 sigma_n : 4.838497e-02

 batch number : 30

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.838000e+00	 sigma_n : 4.734974e-02

 batch number : 31

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.862000e+00	 sigma_n : 4.695914e-02

 batch number : 32

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.914000e+00	 sigma_n : 4.813440e-02

 batch number : 33

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.927000e+00	 sigma_n : 4.677455e-02

 batch number : 34

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.977000e+00	 sigma_n : 4.716668e-02

 batch number : 35

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.930000e+00	 sigma_n : 4.772188e-02

 batch number : 36

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.871000e+00	 sigma_n : 4.800691e-02

 batch number : 37

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.960000e+00	 sigma_n : 4.752535e-02

 batch number : 38

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.910000e+00	 sigma_n : 4.730896e-02

 batch number : 39

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.969000e+00	 sigma_n : 4.923884e-02

 batch number : 40

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.033000e+00	 sigma_n : 5.101484e-02

 batch number : 41

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.814000e+00	 sigma_n : 4.480415e-02

 batch number : 42

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.903000e+00	 sigma_n : 4.787361e-02

 batch number : 43

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 4.020000e+00	 sigma_n : 4.955861e-02

 batch number : 44

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.928000e+00	 sigma_n : 4.838551e-02

 batch number : 45

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.993000e+00	 sigma_n : 4.902402e-02

 batch number : 46

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.907000e+00	 sigma_n : 4.650283e-02

 batch number : 47

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.860000e+00	 sigma_n : 4.576565e-02

 batch number : 48

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.940000e+00	 sigma_n : 4.897753e-02

 batch number : 49

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.911000e+00	 sigma_n : 4.809774e-02

 Type and parameters of random generator before batch 50 : 
	 DRAND48_RANDOM 32981 55802 63971  COUNTER	1859018


 batch number : 50

  quota sampling and descendant statistics: 
	 mean number of collision per photon history: 3.893000e+00	 sigma_n : 4.660175e-02

*********************************************************

 RESULTS ARE GIVEN FOR SOURCE INTENSITY : 1.256637e+01
*********************************************************


 Mean weight leakage = 0.000000e+00	 sigma = 0.000000e+00	 sigma% = 0


 Edition after batch number : 50



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_reg_track
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	3.677422e-02	7.958973e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	2.976691e-02	9.062616e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	2.074936e-02	8.792484e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	1.114170e-01	3.811209e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	6.599374e-02	5.429355e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	4.311254e-02	6.872661e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)	2.000000e+00	1.481913e-01	3.680676e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)	2.000000e+00	9.576065e-02	5.090096e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)	2.000000e+00	6.386189e-02	5.237749e+00

number of batches used: 50	3.078138e-01	3.935660e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_reg_norm
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 1.838711e-02	7.958973e+00
	 (1,0,0)	 1.488345e-02	9.062616e+00
	 (2,0,0)	 1.037468e-02	8.792484e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 5.570852e-02	3.811209e+00
	 (1,0,0)	 3.299687e-02	5.429355e+00
	 (2,0,0)	 2.155627e-02	6.872661e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 7.409563e-02	3.680676e+00
	 (1,0,0)	 4.788033e-02	5.090096e+00
	 (2,0,0)	 3.193095e-02	5.237749e+00

number of batches used: 50	5.130230e-02	3.935660e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_reg_coll
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_COLL
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 2.229393e-02	3.080385e+01
	 (1,0,0)	 2.804283e-02	2.521080e+01
	 (2,0,0)	 2.947464e-02	2.692265e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 9.786847e-02	1.984664e+01
	 (1,0,0)	 1.106339e-01	1.842094e+01
	 (2,0,0)	 4.255151e-02	3.194383e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 1.201624e-01	1.763734e+01
	 (1,0,0)	 1.386768e-01	1.518072e+01
	 (2,0,0)	 7.202614e-02	2.197174e+01

number of batches used: 50	3.308653e-01	9.581184e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_var_track
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	3.677422e-02	7.958973e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	2.976691e-02	9.062616e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	2.074936e-02	8.792484e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	1.114170e-01	3.811209e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	6.599374e-02	5.429355e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	4.311254e-02	6.872661e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)	2.000000e+00	1.481913e-01	3.680676e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)	2.000000e+00	9.576065e-02	5.090096e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)	2.000000e+00	6.386189e-02	5.237749e+00

number of batches used: 50	3.078138e-01	3.935660e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_var_norm
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	1.838711e-02	7.958973e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	1.488345e-02	9.062616e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	1.037468e-02	8.792484e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)   	2.000000e+00	5.570852e-02	3.811209e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	3.299687e-02	5.429355e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	2.155627e-02	6.872661e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.5000, 1.0000, 0.5000)	2.000000e+00	7.409563e-02	3.680676e+00
	 (1,0,0)	 (1.5000, 1.0000, 0.5000)	2.000000e+00	4.788033e-02	5.090096e+00
	 (2,0,0)	 (2.5000, 1.0000, 0.5000)	2.000000e+00	3.193095e-02	5.237749e+00

number of batches used: 50	5.130230e-02	3.935660e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh1_var_coll
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_COLL
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 2.229393e-02	3.080385e+01
	 (1,0,0)	 2.804283e-02	2.521080e+01
	 (2,0,0)	 2.947464e-02	2.692265e+01

 	 Boltzmann Entropy of sources = -8.745633e-03
	 Shannon Entropy of sources = 0.000000e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 9.786847e-02	1.984664e+01
	 (1,0,0)	 1.106339e-01	1.842094e+01
	 (2,0,0)	 4.255151e-02	3.194383e+01

 	 Boltzmann Entropy of sources = -8.745633e-03
	 Shannon Entropy of sources = 0.000000e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 1.201624e-01	1.763734e+01
	 (1,0,0)	 1.386768e-01	1.518072e+01
	 (2,0,0)	 7.202614e-02	2.197174e+01


	 INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 50	3.308653e-01	9.581184e+00




******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh2_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 1.488345e-02	9.062616e+00
	 (1,0,0)	 1.037468e-02	8.792484e+00

 	 Boltzmann Entropy of sources = 6.725953e-01
	 Shannon Entropy of sources = 6.762579e-01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 3.299687e-02	5.429355e+00
	 (1,0,0)	 2.155627e-02	6.872661e+00

 	 Boltzmann Entropy of sources = 7.052600e-01
	 Shannon Entropy of sources = 7.085705e-01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 4.788033e-02	5.090096e+00
	 (1,0,0)	 3.193095e-02	5.237749e+00


	 INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 50	7.981127e-02	4.835135e+00




******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh2_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	2.976691e-02	9.062616e+00
	 (1,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	2.074936e-02	8.792484e+00

 	 Boltzmann Entropy of sources = 6.725953e-01
	 Shannon Entropy of sources = 6.762579e-01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (1.5000, 1.0000, 0.5000)   	2.000000e+00	6.599374e-02	5.429355e+00
	 (1,0,0)	 (2.5000, 1.0000, 0.5000)   	2.000000e+00	4.311254e-02	6.872661e+00

 	 Boltzmann Entropy of sources = 7.052600e-01
	 Shannon Entropy of sources = 7.085705e-01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (1.5000, 1.0000, 0.5000)	2.000000e+00	9.576065e-02	5.090096e+00
	 (1,0,0)	 (2.5000, 1.0000, 0.5000)	2.000000e+00	6.386189e-02	5.237749e+00


	 INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 50	1.596225e-01	4.835135e+00




******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh3_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)   	2.000000e+00	1.600693e-02	7.732999e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)   	2.000000e+00	1.277701e-02	8.535164e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)   	2.000000e+00	1.007856e-02	1.128620e+01

 	 Boltzmann Entropy of sources = 1.082958e+00
	 Shannon Entropy of sources = 1.090042e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)   	2.000000e+00	5.227871e-02	5.647931e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)   	2.000000e+00	3.226962e-02	7.226695e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)   	2.000000e+00	1.918532e-02	6.824089e+00

 	 Boltzmann Entropy of sources = 7.006929e-01
	 Shannon Entropy of sources = 7.061098e-01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)	2.000000e+00	6.828564e-02	4.958319e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)	2.000000e+00	4.504663e-02	5.785883e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)	2.000000e+00	2.926387e-02	5.508119e+00


	 INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 50	1.425961e-01	4.737548e+00




******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh3_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)   	2.000000e+00	3.201386e-02	7.732999e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)   	2.000000e+00	2.555402e-02	8.535164e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)   	2.000000e+00	2.015711e-02	1.128620e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)   	2.000000e+00	1.045574e-01	5.647931e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)   	2.000000e+00	6.453924e-02	7.226695e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)   	2.000000e+00	3.837064e-02	6.824089e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.3000, 1.2000, -0.5000)	2.000000e+00	1.365713e-01	4.958319e+00
	 (1,0,0)	 (1.3000, 1.2000, -0.5000)	2.000000e+00	9.009325e-02	5.785883e+00
	 (2,0,0)	 (2.3000, 1.2000, -0.5000)	2.000000e+00	5.852775e-02	5.508119e+00

number of batches used: 50	2.851923e-01	4.737548e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh4_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)   	2.000000e+00	2.932377e-02	8.400853e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)   	2.000000e+00	2.682630e-02	9.319394e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)   	2.000000e+00	2.587425e-02	9.066040e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)   	2.000000e+00	1.065165e-01	5.150208e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)   	2.000000e+00	6.993093e-02	5.983929e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)   	2.000000e+00	5.436565e-02	6.703525e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)	2.000000e+00	1.358403e-01	4.366823e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)	2.000000e+00	9.675724e-02	5.668759e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)	2.000000e+00	8.023990e-02	6.199905e+00

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh4_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)   	2.000000e+00	2.932377e-02	8.400853e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)   	2.000000e+00	2.682630e-02	9.319394e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)   	2.000000e+00	2.587425e-02	9.066040e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)   	2.000000e+00	1.065165e-01	5.150208e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)   	2.000000e+00	6.993093e-02	5.983929e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)   	2.000000e+00	5.436565e-02	6.703525e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.2421, 1.3731, -1.3492)	2.000000e+00	1.358403e-01	4.366823e+00
	 (1,0,0)	 (0.5597, 1.9077, -1.0819)	2.000000e+00	9.675724e-02	5.668759e+00
	 (2,0,0)	 (1.3615, 2.4422, -0.8147)	2.000000e+00	8.023990e-02	6.199905e+00

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh5_reg_track
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	7.957327e-03	1.331149e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	9.288485e-03	1.130690e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	5.645017e-03	1.598130e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.432937e-03	1.587227e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	5.792668e-03	1.741750e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	7.083283e-03	1.295669e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.806759e-03	1.511638e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	7.143593e-03	1.720639e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	5.393458e-03	1.614296e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	8.297195e-03	1.285091e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	6.280542e-03	1.493615e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	5.903058e-03	1.733738e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.731233e-02	7.297279e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	3.249625e-02	6.160459e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	2.075450e-02	9.334904e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	2.595343e-02	8.080734e+00
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	1.579431e-02	9.917677e+00
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	2.285196e-02	1.093410e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	1.517377e-02	9.357983e+00
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	1.611090e-02	1.080480e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.576824e-02	1.519222e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	1.752098e-02	8.583786e+00
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	9.594539e-03	1.224673e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	1.148188e-02	1.096179e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.526965e-02	5.841215e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	4.178473e-02	5.666446e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	2.639951e-02	7.921620e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	3.238637e-02	6.797811e+00
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.158698e-02	9.323244e+00
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	2.993524e-02	9.197875e+00
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	2.198053e-02	8.169055e+00
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.325449e-02	9.941341e+00
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	2.116170e-02	1.242511e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	2.581818e-02	7.677309e+00
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	1.587508e-02	1.023516e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.738494e-02	9.296343e+00

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh5_reg_coll
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_COLL
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	4.756393e-03	5.841807e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	7.820409e-03	4.578678e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	1.778676e-02	4.131170e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.486156e-03	5.867246e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	6.090275e-03	5.230983e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	4.398914e-03	4.974182e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.347297e-03	5.862581e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	5.323936e-03	6.390708e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	4.107957e-03	7.451118e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	6.408686e-03	4.781458e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	1.325570e-02	4.376538e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	7.469426e-03	5.524480e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.978605e-02	3.540684e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	4.255151e-02	3.194383e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	2.127575e-02	4.285714e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	4.255151e-02	2.857143e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	2.553090e-02	3.868590e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	2.127575e-02	4.285714e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	2.978605e-02	3.540684e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	8.510301e-03	6.998542e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	4.255151e-03	1.000000e+02


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.454245e-02	3.079626e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	5.037192e-02	2.692881e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	3.055221e-02	3.220748e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	1.925161e-02	4.129600e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.736603e-02	3.427947e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	4.695042e-02	2.665086e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	3.187820e-02	3.633086e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.659969e-02	3.804498e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	1.687341e-02	4.564950e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	3.619474e-02	3.343681e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	2.176600e-02	3.690513e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.172458e-02	4.961320e+01

number of batches used: 50	3.540713e-01	1.147552e+01



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh5_var_track
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	7.957327e-03	1.331149e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	9.288485e-03	1.130690e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	5.645017e-03	1.598130e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.432937e-03	1.587227e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	5.792668e-03	1.741750e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	7.083283e-03	1.295669e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.806759e-03	1.511638e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	7.143593e-03	1.720639e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	5.393458e-03	1.614296e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	8.297195e-03	1.285091e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	6.280542e-03	1.493615e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	5.903058e-03	1.733738e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.731233e-02	7.297279e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	3.249625e-02	6.160459e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	2.075450e-02	9.334904e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	2.595343e-02	8.080734e+00
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	1.579431e-02	9.917677e+00
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	2.285196e-02	1.093410e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	1.517377e-02	9.357983e+00
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	1.611090e-02	1.080480e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.576824e-02	1.519222e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	1.752098e-02	8.583786e+00
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	9.594539e-03	1.224673e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	1.148188e-02	1.096179e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.526965e-02	5.841215e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	4.178473e-02	5.666446e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	2.639951e-02	7.921620e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	3.238637e-02	6.797811e+00
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.158698e-02	9.323244e+00
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	2.993524e-02	9.197875e+00
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	2.198053e-02	8.169055e+00
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.325449e-02	9.941341e+00
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	2.116170e-02	1.242511e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	2.581818e-02	7.677309e+00
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	1.587508e-02	1.023516e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.738494e-02	9.296343e+00

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh5_var_coll
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_COLL
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	4.756393e-03	5.841807e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	7.820409e-03	4.578678e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	1.778676e-02	4.131170e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.486156e-03	5.867246e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	6.090275e-03	5.230983e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	4.398914e-03	4.974182e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.347297e-03	5.862581e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	5.323936e-03	6.390708e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	4.107957e-03	7.451118e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	6.408686e-03	4.781458e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	1.325570e-02	4.376538e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	7.469426e-03	5.524480e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.978605e-02	3.540684e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	4.255151e-02	3.194383e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	2.127575e-02	4.285714e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	4.255151e-02	2.857143e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	2.553090e-02	3.868590e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	2.127575e-02	4.285714e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.276545e-02	5.654449e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	2.978605e-02	3.540684e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	8.510301e-03	6.998542e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	4.255151e-03	1.000000e+02


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.454245e-02	3.079626e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	5.037192e-02	2.692881e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	3.055221e-02	3.220748e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	1.925161e-02	4.129600e+01
	 (1,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.736603e-02	3.427947e+01
	 (1,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	4.695042e-02	2.665086e+01
	 (1,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	3.187820e-02	3.633086e+01
	 (1,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.659969e-02	3.804498e+01
	 (2,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	1.687341e-02	4.564950e+01
	 (2,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	3.619474e-02	3.343681e+01
	 (2,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	2.176600e-02	3.690513e+01
	 (2,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.172458e-02	4.961320e+01

number of batches used: 50	3.540713e-01	1.147552e+01



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh6_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	5.792668e-03	1.741750e+01
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	7.083283e-03	1.295669e+01
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.806759e-03	1.511638e+01
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	7.143593e-03	1.720639e+01
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	5.393458e-03	1.614296e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	8.297195e-03	1.285091e+01
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	6.280542e-03	1.493615e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	5.903058e-03	1.733738e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	1.579431e-02	9.917677e+00
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	2.285196e-02	1.093410e+01
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	1.517377e-02	9.357983e+00
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	1.611090e-02	1.080480e+01
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.576824e-02	1.519222e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	1.752098e-02	8.583786e+00
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	9.594539e-03	1.224673e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	1.148188e-02	1.096179e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.158698e-02	9.323244e+00
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	2.993524e-02	9.197875e+00
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	2.198053e-02	8.169055e+00
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.325449e-02	9.941341e+00
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	2.116170e-02	1.242511e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	2.581818e-02	7.677309e+00
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	1.587508e-02	1.023516e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.738494e-02	9.296343e+00

number of batches used: 50	1.769971e-01	5.354886e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh6_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	5.792668e-03	1.741750e+01
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	7.083283e-03	1.295669e+01
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	6.806759e-03	1.511638e+01
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	7.143593e-03	1.720639e+01
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	5.393458e-03	1.614296e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	8.297195e-03	1.285091e+01
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	6.280542e-03	1.493615e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	5.903058e-03	1.733738e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)   	5.000000e-01	1.579431e-02	9.917677e+00
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)   	5.000000e-01	2.285196e-02	1.093410e+01
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)   	5.000000e-01	1.517377e-02	9.357983e+00
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)   	5.000000e-01	1.611090e-02	1.080480e+01
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)   	5.000000e-01	1.576824e-02	1.519222e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)   	5.000000e-01	1.752098e-02	8.583786e+00
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)   	5.000000e-01	9.594539e-03	1.224673e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)   	5.000000e-01	1.148188e-02	1.096179e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.7812, 1.4547, -0.8405)	5.000000e-01	2.158698e-02	9.323244e+00
	 (0,0,1)	 (0.4925, 1.7434, -0.5519)	5.000000e-01	2.993524e-02	9.197875e+00
	 (0,1,0)	 (0.6269, 2.0719, -1.6120)	5.000000e-01	2.198053e-02	8.169055e+00
	 (0,1,1)	 (0.3382, 2.3606, -1.3234)	5.000000e-01	2.325449e-02	9.941341e+00
	 (1,0,0)	 (1.5830, 1.9893, -0.5733)	5.000000e-01	2.116170e-02	1.242511e+01
	 (1,0,1)	 (1.2943, 2.2779, -0.2846)	5.000000e-01	2.581818e-02	7.677309e+00
	 (1,1,0)	 (1.4287, 2.6065, -1.3448)	5.000000e-01	1.587508e-02	1.023516e+01
	 (1,1,1)	 (1.1400, 2.8951, -1.0561)	5.000000e-01	1.738494e-02	9.296343e+00

number of batches used: 50	1.769971e-01	5.354886e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh7_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	7.957327e-03	1.331149e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	9.288485e-03	1.130690e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	5.645017e-03	1.598130e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.432937e-03	1.587227e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.731233e-02	7.297279e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	3.249625e-02	6.160459e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	2.075450e-02	9.334904e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	2.595343e-02	8.080734e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.526965e-02	5.841215e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	4.178473e-02	5.666446e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	2.639951e-02	7.921620e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	3.238637e-02	6.797811e+00

number of batches used: 50	1.358403e-01	4.366823e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh7_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	7.957327e-03	1.331149e+01
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	9.288485e-03	1.130690e+01
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	5.645017e-03	1.598130e+01
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	6.432937e-03	1.587227e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)   	5.000000e-01	2.731233e-02	7.297279e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)   	5.000000e-01	3.249625e-02	6.160459e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)   	5.000000e-01	2.075450e-02	9.334904e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)   	5.000000e-01	2.595343e-02	8.080734e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.0206, 0.9202, -1.1078)	5.000000e-01	3.526965e-02	5.841215e+00
	 (0,0,1)	 (-0.3093, 1.2089, -0.8191)	5.000000e-01	4.178473e-02	5.666446e+00
	 (0,1,0)	 (-0.1749, 1.5374, -1.8793)	5.000000e-01	2.639951e-02	7.921620e+00
	 (0,1,1)	 (-0.4636, 1.8261, -1.5906)	5.000000e-01	3.238637e-02	6.797811e+00

number of batches used: 50	1.358403e-01	4.366823e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh8_reg
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.0825, 0.8171, -1.2109)   	1.428571e-01	2.192582e-03	1.518793e+01
	 (0,0,1)	 (0.0000, 0.8996, -1.1284)   	1.428571e-01	1.961883e-03	1.423723e+01
	 (0,0,2)	 (-0.0825, 0.9821, -1.0459)   	1.428571e-01	2.485022e-03	1.666883e+01
	 (0,0,3)	 (-0.1649, 1.0645, -0.9635)   	1.428571e-01	2.568432e-03	1.753888e+01
	 (0,0,4)	 (-0.2474, 1.1470, -0.8810)   	1.428571e-01	2.396764e-03	1.487993e+01
	 (0,0,5)	 (-0.3299, 1.2295, -0.7985)   	1.428571e-01	2.989286e-03	1.633497e+01
	 (0,0,6)	 (-0.4124, 1.3120, -0.7160)   	1.428571e-01	2.651845e-03	1.552797e+01
	 (0,1,0)	 (-0.0718, 1.4343, -1.9824)   	1.428571e-01	2.057799e-03	1.931822e+01
	 (0,1,1)	 (-0.1543, 1.5168, -1.8999)   	1.428571e-01	1.655238e-03	1.828564e+01
	 (0,1,2)	 (-0.2368, 1.5993, -1.8174)   	1.428571e-01	1.281917e-03	2.107233e+01
	 (0,1,3)	 (-0.3192, 1.6818, -1.7350)   	1.428571e-01	1.789534e-03	2.082459e+01
	 (0,1,4)	 (-0.4017, 1.7642, -1.6525)   	1.428571e-01	1.216063e-03	2.682380e+01
	 (0,1,5)	 (-0.4842, 1.8467, -1.5700)   	1.428571e-01	2.015676e-03	2.256208e+01
	 (0,1,6)	 (-0.5667, 1.9292, -1.4875)   	1.428571e-01	2.061727e-03	1.717061e+01
	 (1,0,0)	 (0.8843, 1.3516, -0.9436)   	1.428571e-01	1.669037e-03	2.211096e+01
	 (1,0,1)	 (0.8018, 1.4341, -0.8611)   	1.428571e-01	1.926957e-03	2.656949e+01
	 (1,0,2)	 (0.7193, 1.5166, -0.7787)   	1.428571e-01	1.448031e-03	1.853872e+01
	 (1,0,3)	 (0.6368, 1.5991, -0.6962)   	1.428571e-01	1.526751e-03	1.695556e+01
	 (1,0,4)	 (0.5544, 1.6815, -0.6137)   	1.428571e-01	1.209751e-03	1.920272e+01
	 (1,0,5)	 (0.4719, 1.7640, -0.5312)   	1.428571e-01	2.243405e-03	1.835689e+01
	 (1,0,6)	 (0.3894, 1.8465, -0.4488)   	1.428571e-01	2.852019e-03	1.817194e+01
	 (1,1,0)	 (0.7300, 1.9688, -1.7151)   	1.428571e-01	1.443443e-03	2.180018e+01
	 (1,1,1)	 (0.6475, 2.0513, -1.6327)   	1.428571e-01	2.319682e-03	1.820619e+01
	 (1,1,2)	 (0.5650, 2.1338, -1.5502)   	1.428571e-01	1.906267e-03	1.908181e+01
	 (1,1,3)	 (0.4825, 2.2163, -1.4677)   	1.428571e-01	2.327638e-03	1.938030e+01
	 (1,1,4)	 (0.4001, 2.2988, -1.3852)   	1.428571e-01	2.231169e-03	2.275565e+01
	 (1,1,5)	 (0.3176, 2.3812, -1.3028)   	1.428571e-01	1.848503e-03	2.134765e+01
	 (1,1,6)	 (0.2351, 2.4637, -1.2203)   	1.428571e-01	1.873650e-03	2.301981e+01
	 (2,0,0)	 (1.6861, 1.8862, -0.6764)   	1.428571e-01	1.464581e-03	1.976524e+01
	 (2,0,1)	 (1.6036, 1.9686, -0.5939)   	1.428571e-01	1.554609e-03	2.068810e+01
	 (2,0,2)	 (1.5211, 2.0511, -0.5114)   	1.428571e-01	1.470425e-03	2.207648e+01
	 (2,0,3)	 (1.4386, 2.1336, -0.4289)   	1.428571e-01	1.785369e-03	2.334437e+01
	 (2,0,4)	 (1.3562, 2.2161, -0.3465)   	1.428571e-01	2.211199e-03	1.734236e+01
	 (2,0,5)	 (1.2737, 2.2985, -0.2640)   	1.428571e-01	2.944390e-03	1.718611e+01
	 (2,0,6)	 (1.1912, 2.3810, -0.1815)   	1.428571e-01	2.260079e-03	2.180324e+01
	 (2,1,0)	 (1.5318, 2.5034, -1.4479)   	1.428571e-01	1.766754e-03	1.948061e+01
	 (2,1,1)	 (1.4493, 2.5858, -1.3654)   	1.428571e-01	1.412600e-03	2.089387e+01
	 (2,1,2)	 (1.3668, 2.6683, -1.2829)   	1.428571e-01	2.060047e-03	2.176307e+01
	 (2,1,3)	 (1.2843, 2.7508, -1.2004)   	1.428571e-01	2.136750e-03	2.390223e+01
	 (2,1,4)	 (1.2019, 2.8333, -1.1180)   	1.428571e-01	1.717393e-03	2.188333e+01
	 (2,1,5)	 (1.1194, 2.9158, -1.0355)   	1.428571e-01	1.167006e-03	2.437914e+01
	 (2,1,6)	 (1.0369, 2.9982, -0.9530)   	1.428571e-01	1.923051e-03	2.202962e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.0825, 0.8171, -1.2109)   	1.428571e-01	7.226031e-03	8.564386e+00
	 (0,0,1)	 (0.0000, 0.8996, -1.1284)   	1.428571e-01	7.566557e-03	8.589408e+00
	 (0,0,2)	 (-0.0825, 0.9821, -1.0459)   	1.428571e-01	8.243543e-03	7.298473e+00
	 (0,0,3)	 (-0.1649, 1.0645, -0.9635)   	1.428571e-01	8.707624e-03	6.610636e+00
	 (0,0,4)	 (-0.2474, 1.1470, -0.8810)   	1.428571e-01	8.988794e-03	7.080940e+00
	 (0,0,5)	 (-0.3299, 1.2295, -0.7985)   	1.428571e-01	9.401688e-03	7.302392e+00
	 (0,0,6)	 (-0.4124, 1.3120, -0.7160)   	1.428571e-01	9.674337e-03	6.821357e+00
	 (0,1,0)	 (-0.0718, 1.4343, -1.9824)   	1.428571e-01	5.889503e-03	1.220124e+01
	 (0,1,1)	 (-0.1543, 1.5168, -1.8999)   	1.428571e-01	5.912555e-03	1.016607e+01
	 (0,1,2)	 (-0.2368, 1.5993, -1.8174)   	1.428571e-01	5.895958e-03	1.000436e+01
	 (0,1,3)	 (-0.3192, 1.6818, -1.7350)   	1.428571e-01	6.213302e-03	9.710940e+00
	 (0,1,4)	 (-0.4017, 1.7642, -1.6525)   	1.428571e-01	7.170110e-03	8.911806e+00
	 (0,1,5)	 (-0.4842, 1.8467, -1.5700)   	1.428571e-01	7.823761e-03	9.257360e+00
	 (0,1,6)	 (-0.5667, 1.9292, -1.4875)   	1.428571e-01	7.802742e-03	9.320520e+00
	 (1,0,0)	 (0.8843, 1.3516, -0.9436)   	1.428571e-01	4.379859e-03	1.046716e+01
	 (1,0,1)	 (0.8018, 1.4341, -0.8611)   	1.428571e-01	4.111107e-03	1.142561e+01
	 (1,0,2)	 (0.7193, 1.5166, -0.7787)   	1.428571e-01	4.619108e-03	1.230045e+01
	 (1,0,3)	 (0.6368, 1.5991, -0.6962)   	1.428571e-01	5.538692e-03	1.248135e+01
	 (1,0,4)	 (0.5544, 1.6815, -0.6137)   	1.428571e-01	6.078213e-03	1.376544e+01
	 (1,0,5)	 (0.4719, 1.7640, -0.5312)   	1.428571e-01	6.721206e-03	1.246580e+01
	 (1,0,6)	 (0.3894, 1.8465, -0.4488)   	1.428571e-01	7.198083e-03	1.072916e+01
	 (1,1,0)	 (0.7300, 1.9688, -1.7151)   	1.428571e-01	3.928814e-03	1.237000e+01
	 (1,1,1)	 (0.6475, 2.0513, -1.6327)   	1.428571e-01	4.529825e-03	1.061231e+01
	 (1,1,2)	 (0.5650, 2.1338, -1.5502)   	1.428571e-01	4.596708e-03	1.066320e+01
	 (1,1,3)	 (0.4825, 2.2163, -1.4677)   	1.428571e-01	4.320332e-03	1.252335e+01
	 (1,1,4)	 (0.4001, 2.2988, -1.3852)   	1.428571e-01	4.388308e-03	1.351335e+01
	 (1,1,5)	 (0.3176, 2.3812, -1.3028)   	1.428571e-01	4.593655e-03	1.276122e+01
	 (1,1,6)	 (0.2351, 2.4637, -1.2203)   	1.428571e-01	4.927020e-03	1.159134e+01
	 (2,0,0)	 (1.6861, 1.8862, -0.6764)   	1.428571e-01	3.834713e-03	1.975441e+01
	 (2,0,1)	 (1.6036, 1.9686, -0.5939)   	1.428571e-01	4.481525e-03	1.839701e+01
	 (2,0,2)	 (1.5211, 2.0511, -0.5114)   	1.428571e-01	5.109093e-03	1.420480e+01
	 (2,0,3)	 (1.4386, 2.1336, -0.4289)   	1.428571e-01	4.751439e-03	1.095648e+01
	 (2,0,4)	 (1.3562, 2.2161, -0.3465)   	1.428571e-01	4.936530e-03	9.690045e+00
	 (2,0,5)	 (1.2737, 2.2985, -0.2640)   	1.428571e-01	4.980933e-03	1.139458e+01
	 (2,0,6)	 (1.1912, 2.3810, -0.1815)   	1.428571e-01	5.194992e-03	1.181776e+01
	 (2,1,0)	 (1.5318, 2.5034, -1.4479)   	1.428571e-01	2.589928e-03	1.374168e+01
	 (2,1,1)	 (1.4493, 2.5858, -1.3654)   	1.428571e-01	2.949270e-03	1.275571e+01
	 (2,1,2)	 (1.3668, 2.6683, -1.2829)   	1.428571e-01	2.629299e-03	1.729662e+01
	 (2,1,3)	 (1.2843, 2.7508, -1.2004)   	1.428571e-01	2.784996e-03	1.630281e+01
	 (2,1,4)	 (1.2019, 2.8333, -1.1180)   	1.428571e-01	2.723724e-03	1.566591e+01
	 (2,1,5)	 (1.1194, 2.9158, -1.0355)   	1.428571e-01	3.464051e-03	1.581859e+01
	 (2,1,6)	 (1.0369, 2.9982, -0.9530)   	1.428571e-01	3.935154e-03	1.428635e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.0825, 0.8171, -1.2109)	1.428571e-01	9.418613e-03	7.199338e+00
	 (0,0,1)	 (0.0000, 0.8996, -1.1284)	1.428571e-01	9.528440e-03	6.596123e+00
	 (0,0,2)	 (-0.0825, 0.9821, -1.0459)	1.428571e-01	1.072856e-02	5.921905e+00
	 (0,0,3)	 (-0.1649, 1.0645, -0.9635)	1.428571e-01	1.127606e-02	6.322522e+00
	 (0,0,4)	 (-0.2474, 1.1470, -0.8810)	1.428571e-01	1.138556e-02	6.446364e+00
	 (0,0,5)	 (-0.3299, 1.2295, -0.7985)	1.428571e-01	1.239097e-02	7.405697e+00
	 (0,0,6)	 (-0.4124, 1.3120, -0.7160)	1.428571e-01	1.232618e-02	6.072943e+00
	 (0,1,0)	 (-0.0718, 1.4343, -1.9824)	1.428571e-01	7.947302e-03	1.022301e+01
	 (0,1,1)	 (-0.1543, 1.5168, -1.8999)	1.428571e-01	7.567793e-03	8.286063e+00
	 (0,1,2)	 (-0.2368, 1.5993, -1.8174)	1.428571e-01	7.177875e-03	9.435978e+00
	 (0,1,3)	 (-0.3192, 1.6818, -1.7350)	1.428571e-01	8.002836e-03	9.145696e+00
	 (0,1,4)	 (-0.4017, 1.7642, -1.6525)	1.428571e-01	8.386173e-03	8.702758e+00
	 (0,1,5)	 (-0.4842, 1.8467, -1.5700)	1.428571e-01	9.839437e-03	7.607433e+00
	 (0,1,6)	 (-0.5667, 1.9292, -1.4875)	1.428571e-01	9.864469e-03	7.712842e+00
	 (1,0,0)	 (0.8843, 1.3516, -0.9436)	1.428571e-01	6.048896e-03	1.012443e+01
	 (1,0,1)	 (0.8018, 1.4341, -0.8611)	1.428571e-01	6.038064e-03	1.248649e+01
	 (1,0,2)	 (0.7193, 1.5166, -0.7787)	1.428571e-01	6.067139e-03	1.100378e+01
	 (1,0,3)	 (0.6368, 1.5991, -0.6962)	1.428571e-01	7.065443e-03	1.052442e+01
	 (1,0,4)	 (0.5544, 1.6815, -0.6137)	1.428571e-01	7.287963e-03	1.183087e+01
	 (1,0,5)	 (0.4719, 1.7640, -0.5312)	1.428571e-01	8.964612e-03	1.176344e+01
	 (1,0,6)	 (0.3894, 1.8465, -0.4488)	1.428571e-01	1.005010e-02	8.413438e+00
	 (1,1,0)	 (0.7300, 1.9688, -1.7151)	1.428571e-01	5.372258e-03	1.186383e+01
	 (1,1,1)	 (0.6475, 2.0513, -1.6327)	1.428571e-01	6.849507e-03	1.034365e+01
	 (1,1,2)	 (0.5650, 2.1338, -1.5502)	1.428571e-01	6.502975e-03	8.402136e+00
	 (1,1,3)	 (0.4825, 2.2163, -1.4677)	1.428571e-01	6.647971e-03	9.904126e+00
	 (1,1,4)	 (0.4001, 2.2988, -1.3852)	1.428571e-01	6.619477e-03	1.250791e+01
	 (1,1,5)	 (0.3176, 2.3812, -1.3028)	1.428571e-01	6.442158e-03	1.175061e+01
	 (1,1,6)	 (0.2351, 2.4637, -1.2203)	1.428571e-01	6.800670e-03	1.167380e+01
	 (2,0,0)	 (1.6861, 1.8862, -0.6764)	1.428571e-01	5.299294e-03	1.531086e+01
	 (2,0,1)	 (1.6036, 1.9686, -0.5939)	1.428571e-01	6.036134e-03	1.485382e+01
	 (2,0,2)	 (1.5211, 2.0511, -0.5114)	1.428571e-01	6.579519e-03	1.278872e+01
	 (2,0,3)	 (1.4386, 2.1336, -0.4289)	1.428571e-01	6.536808e-03	1.122444e+01
	 (2,0,4)	 (1.3562, 2.2161, -0.3465)	1.428571e-01	7.147729e-03	8.828064e+00
	 (2,0,5)	 (1.2737, 2.2985, -0.2640)	1.428571e-01	7.925323e-03	9.468192e+00
	 (2,0,6)	 (1.1912, 2.3810, -0.1815)	1.428571e-01	7.455072e-03	1.116471e+01
	 (2,1,0)	 (1.5318, 2.5034, -1.4479)	1.428571e-01	4.356682e-03	1.224560e+01
	 (2,1,1)	 (1.4493, 2.5858, -1.3654)	1.428571e-01	4.361869e-03	1.211265e+01
	 (2,1,2)	 (1.3668, 2.6683, -1.2829)	1.428571e-01	4.689346e-03	1.344085e+01
	 (2,1,3)	 (1.2843, 2.7508, -1.2004)	1.428571e-01	4.921746e-03	1.291648e+01
	 (2,1,4)	 (1.2019, 2.8333, -1.1180)	1.428571e-01	4.441118e-03	1.245430e+01
	 (2,1,5)	 (1.1194, 2.9158, -1.0355)	1.428571e-01	4.631057e-03	1.417029e+01
	 (2,1,6)	 (1.0369, 2.9982, -0.9530)	1.428571e-01	5.858205e-03	1.060987e+01

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh8_var
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-0.2543, 0.4944, -0.9157)   	3.409091e-02	7.247720e-04	3.746076e+01
	 (0,0,1)	 (-0.5430, 0.7831, -0.6270)   	3.409091e-02	6.878578e-04	2.649524e+01
	 (0,1,0)	 (-0.2929, 0.6487, -1.1085)   	3.409091e-02	4.389839e-04	4.207729e+01
	 (0,1,1)	 (-0.5815, 0.9374, -0.8199)   	3.409091e-02	1.193401e-03	2.611498e+01
	 (0,2,0)	 (-0.3314, 0.8030, -1.3014)   	3.409091e-02	5.747063e-04	3.772781e+01
	 (0,2,1)	 (-0.6201, 1.0917, -1.0127)   	3.409091e-02	7.989903e-04	2.851712e+01
	 (0,3,0)	 (-0.3700, 0.9573, -1.4943)   	3.409091e-02	7.718388e-04	3.134332e+01
	 (0,3,1)	 (-0.6587, 1.2460, -1.2056)   	3.409091e-02	7.608169e-04	2.681405e+01
	 (0,4,0)	 (-0.4086, 1.1116, -1.6872)   	3.409091e-02	4.563502e-04	3.651122e+01
	 (0,4,1)	 (-0.6973, 1.4003, -1.3985)   	3.409091e-02	5.191340e-04	3.026113e+01
	 (0,5,0)	 (-0.4472, 1.2659, -1.8801)   	3.409091e-02	6.435190e-04	3.009442e+01
	 (0,5,1)	 (-0.7358, 1.5546, -1.5914)   	3.409091e-02	2.841960e-04	4.363582e+01
	 (0,6,0)	 (-0.4857, 1.4202, -2.0729)   	3.409091e-02	3.634707e-04	3.858973e+01
	 (0,6,1)	 (-0.7744, 1.7089, -1.7843)   	3.409091e-02	5.300150e-04	3.335442e+01
	 (0,7,0)	 (-0.5243, 1.5745, -2.2658)   	3.409091e-02	5.159088e-04	3.729882e+01
	 (0,7,1)	 (-0.8130, 1.8632, -1.9771)   	3.409091e-02	5.336003e-04	3.095942e+01
	 (1,0,0)	 (-0.0356, 0.6402, -0.8428)   	3.409091e-02	7.788578e-04	2.788374e+01
	 (1,0,1)	 (-0.3243, 0.9288, -0.5541)   	3.409091e-02	5.746891e-04	3.022979e+01
	 (1,1,0)	 (-0.0742, 0.7945, -1.0356)   	3.409091e-02	4.490186e-04	3.755046e+01
	 (1,1,1)	 (-0.3629, 1.0831, -0.7470)   	3.409091e-02	4.845291e-04	3.083874e+01
	 (1,2,0)	 (-0.1128, 0.9488, -1.2285)   	3.409091e-02	2.553019e-04	4.279158e+01
	 (1,2,1)	 (-0.4014, 1.2374, -0.9399)   	3.409091e-02	8.128213e-04	2.873875e+01
	 (1,3,0)	 (-0.1514, 1.1031, -1.4214)   	3.409091e-02	5.306619e-04	3.321565e+01
	 (1,3,1)	 (-0.4400, 1.3917, -1.1327)   	3.409091e-02	2.477272e-04	4.074252e+01
	 (1,4,0)	 (-0.1899, 1.2574, -1.6143)   	3.409091e-02	3.143545e-04	4.132069e+01
	 (1,4,1)	 (-0.4786, 1.5460, -1.3256)   	3.409091e-02	4.446674e-04	3.994700e+01
	 (1,5,0)	 (-0.2285, 1.4117, -1.8072)   	3.409091e-02	6.535747e-04	3.302179e+01
	 (1,5,1)	 (-0.5172, 1.7003, -1.5185)   	3.409091e-02	2.937564e-04	3.926167e+01
	 (1,6,0)	 (-0.2671, 1.5660, -2.0000)   	3.409091e-02	3.283781e-04	3.719790e+01
	 (1,6,1)	 (-0.5558, 1.8547, -1.7114)   	3.409091e-02	3.806040e-04	4.261474e+01
	 (1,7,0)	 (-0.3057, 1.7203, -2.1929)   	3.409091e-02	3.603547e-04	3.649499e+01
	 (1,7,1)	 (-0.5943, 2.0090, -1.9042)   	3.409091e-02	6.024987e-04	3.765338e+01
	 (2,0,0)	 (0.1830, 0.7859, -0.7699)   	3.409091e-02	8.910206e-04	2.507951e+01
	 (2,0,1)	 (-0.1056, 1.0746, -0.4812)   	3.409091e-02	5.004723e-04	3.476589e+01
	 (2,1,0)	 (0.1445, 0.9402, -0.9628)   	3.409091e-02	3.167641e-04	4.108394e+01
	 (2,1,1)	 (-0.1442, 1.2289, -0.6741)   	3.409091e-02	5.098635e-04	3.423396e+01
	 (2,2,0)	 (0.1059, 1.0945, -1.1556)   	3.409091e-02	3.113145e-04	4.417649e+01
	 (2,2,1)	 (-0.1828, 1.3832, -0.8670)   	3.409091e-02	7.739180e-04	2.601110e+01
	 (2,3,0)	 (0.0673, 1.2488, -1.3485)   	3.409091e-02	4.567637e-04	3.068960e+01
	 (2,3,1)	 (-0.2214, 1.5375, -1.0598)   	3.409091e-02	4.567060e-04	3.308762e+01
	 (2,4,0)	 (0.0287, 1.4031, -1.5414)   	3.409091e-02	5.058623e-04	3.062477e+01
	 (2,4,1)	 (-0.2599, 1.6918, -1.2527)   	3.409091e-02	2.215220e-04	4.945929e+01
	 (2,5,0)	 (-0.0098, 1.5575, -1.7343)   	3.409091e-02	3.374682e-04	4.188533e+01
	 (2,5,1)	 (-0.2985, 1.8461, -1.4456)   	3.409091e-02	5.221124e-04	3.186246e+01
	 (2,6,0)	 (-0.0484, 1.7118, -1.9272)   	3.409091e-02	1.665417e-04	6.153118e+01
	 (2,6,1)	 (-0.3371, 2.0004, -1.6385)   	3.409091e-02	3.492334e-04	3.639927e+01
	 (2,7,0)	 (-0.0870, 1.8661, -2.1200)   	3.409091e-02	1.026382e-04	6.405447e+01
	 (2,7,1)	 (-0.3757, 2.1547, -1.8314)   	3.409091e-02	5.011283e-04	4.009602e+01
	 (3,0,0)	 (0.4017, 0.9317, -0.6970)   	3.409091e-02	5.547601e-04	3.234420e+01
	 (3,0,1)	 (0.1130, 1.2204, -0.4083)   	3.409091e-02	5.978762e-04	2.918725e+01
	 (3,1,0)	 (0.3631, 1.0860, -0.8899)   	3.409091e-02	4.198930e-04	3.498071e+01
	 (3,1,1)	 (0.0745, 1.3747, -0.6012)   	3.409091e-02	4.776777e-04	3.713550e+01
	 (3,2,0)	 (0.3246, 1.2403, -1.0827)   	3.409091e-02	4.599723e-04	4.211004e+01
	 (3,2,1)	 (0.0359, 1.5290, -0.7941)   	3.409091e-02	6.190160e-04	3.019430e+01
	 (3,3,0)	 (0.2860, 1.3946, -1.2756)   	3.409091e-02	5.474993e-04	3.321966e+01
	 (3,3,1)	 (-0.0027, 1.6833, -0.9870)   	3.409091e-02	3.918183e-04	4.001256e+01
	 (3,4,0)	 (0.2474, 1.5489, -1.4685)   	3.409091e-02	5.769596e-04	3.109981e+01
	 (3,4,1)	 (-0.0413, 1.8376, -1.1798)   	3.409091e-02	4.318768e-04	3.524055e+01
	 (3,5,0)	 (0.2088, 1.7032, -1.6614)   	3.409091e-02	2.950007e-04	4.913246e+01
	 (3,5,1)	 (-0.0798, 1.9919, -1.3727)   	3.409091e-02	6.340674e-04	3.110505e+01
	 (3,6,0)	 (0.1703, 1.8575, -1.8543)   	3.409091e-02	1.790848e-04	5.732926e+01
	 (3,6,1)	 (-0.1184, 2.1462, -1.5656)   	3.409091e-02	6.132408e-04	2.924906e+01
	 (3,7,0)	 (0.1317, 2.0118, -2.0471)   	3.409091e-02	2.930057e-04	4.750135e+01
	 (3,7,1)	 (-0.1570, 2.3005, -1.7585)   	3.409091e-02	3.339185e-04	3.564194e+01
	 (4,0,0)	 (0.6204, 1.0775, -0.6241)   	3.409091e-02	4.391859e-04	3.482875e+01
	 (4,0,1)	 (0.3317, 1.3662, -0.3354)   	3.409091e-02	2.298614e-04	4.055171e+01
	 (4,1,0)	 (0.5818, 1.2318, -0.8170)   	3.409091e-02	2.871008e-04	4.776313e+01
	 (4,1,1)	 (0.2931, 1.5205, -0.5283)   	3.409091e-02	3.964222e-04	3.728136e+01
	 (4,2,0)	 (0.5432, 1.3861, -1.0099)   	3.409091e-02	1.833837e-04	4.442023e+01
	 (4,2,1)	 (0.2546, 1.6748, -0.7212)   	3.409091e-02	2.597240e-04	4.714501e+01
	 (4,3,0)	 (0.5047, 1.5404, -1.2027)   	3.409091e-02	6.728847e-04	3.160875e+01
	 (4,3,1)	 (0.2160, 1.8291, -0.9141)   	3.409091e-02	8.812431e-04	3.068417e+01
	 (4,4,0)	 (0.4661, 1.6947, -1.3956)   	3.409091e-02	5.398983e-04	2.959824e+01
	 (4,4,1)	 (0.1774, 1.9834, -1.1069)   	3.409091e-02	6.984687e-04	2.867730e+01
	 (4,5,0)	 (0.4275, 1.8490, -1.5885)   	3.409091e-02	3.870500e-04	3.989008e+01
	 (4,5,1)	 (0.1388, 2.1377, -1.2998)   	3.409091e-02	4.610976e-04	3.815422e+01
	 (4,6,0)	 (0.3889, 2.0033, -1.7814)   	3.409091e-02	1.851906e-04	4.370068e+01
	 (4,6,1)	 (0.1003, 2.2920, -1.4927)   	3.409091e-02	4.814803e-04	3.232970e+01
	 (4,7,0)	 (0.3504, 2.1576, -1.9743)   	3.409091e-02	1.889454e-04	4.988368e+01
	 (4,7,1)	 (0.0617, 2.4463, -1.6856)   	3.409091e-02	5.712306e-04	3.085606e+01
	 (5,0,0)	 (0.8391, 1.2233, -0.5512)   	3.409092e-02	5.431031e-04	3.373749e+01
	 (5,0,1)	 (0.5504, 1.5119, -0.2625)   	3.409092e-02	9.872847e-04	2.872235e+01
	 (5,1,0)	 (0.8005, 1.3776, -0.7441)   	3.409092e-02	4.402244e-04	4.025030e+01
	 (5,1,1)	 (0.5118, 1.6663, -0.4554)   	3.409092e-02	2.688056e-04	4.114520e+01
	 (5,2,0)	 (0.7619, 1.5319, -0.9370)   	3.409092e-02	3.202876e-04	4.552370e+01
	 (5,2,1)	 (0.4732, 1.8206, -0.6483)   	3.409092e-02	3.140336e-04	4.054299e+01
	 (5,3,0)	 (0.7233, 1.6862, -1.1298)   	3.409092e-02	3.641033e-04	3.832284e+01
	 (5,3,1)	 (0.4346, 1.9749, -0.8412)   	3.409092e-02	3.807514e-04	4.002288e+01
	 (5,4,0)	 (0.6847, 1.8405, -1.3227)   	3.409092e-02	9.740809e-04	2.959046e+01
	 (5,4,1)	 (0.3961, 2.1292, -1.0341)   	3.409092e-02	4.290096e-04	3.967133e+01
	 (5,5,0)	 (0.6462, 1.9948, -1.5156)   	3.409092e-02	4.218795e-04	3.487825e+01
	 (5,5,1)	 (0.3575, 2.2835, -1.2269)   	3.409092e-02	5.666388e-04	3.174764e+01
	 (5,6,0)	 (0.6076, 2.1491, -1.7085)   	3.409092e-02	4.852596e-04	3.647927e+01
	 (5,6,1)	 (0.3189, 2.4378, -1.4198)   	3.409092e-02	3.548812e-04	3.712975e+01
	 (5,7,0)	 (0.5690, 2.3034, -1.9014)   	3.409092e-02	2.942534e-04	4.694024e+01
	 (5,7,1)	 (0.2803, 2.5921, -1.6127)   	3.409092e-02	4.279292e-04	3.555326e+01
	 (6,0,0)	 (1.0577, 1.3691, -0.4783)   	3.409091e-02	5.123663e-04	3.404646e+01
	 (6,0,1)	 (0.7690, 1.6577, -0.1896)   	3.409091e-02	9.855408e-04	2.718250e+01
	 (6,1,0)	 (1.0191, 1.5234, -0.6712)   	3.409091e-02	5.348191e-04	3.582349e+01
	 (6,1,1)	 (0.7305, 1.8120, -0.3825)   	3.409091e-02	2.895946e-04	4.104593e+01
	 (6,2,0)	 (0.9806, 1.6777, -0.8641)   	3.409091e-02	3.962980e-04	4.748349e+01
	 (6,2,1)	 (0.6919, 1.9663, -0.5754)   	3.409091e-02	4.426812e-04	3.635098e+01
	 (6,3,0)	 (0.9420, 1.8320, -1.0570)   	3.409091e-02	2.362557e-04	4.503453e+01
	 (6,3,1)	 (0.6533, 2.1206, -0.7683)   	3.409091e-02	3.741592e-04	3.951969e+01
	 (6,4,0)	 (0.9034, 1.9863, -1.2498)   	3.409091e-02	5.853076e-04	3.277730e+01
	 (6,4,1)	 (0.6147, 2.2749, -0.9612)   	3.409091e-02	4.684971e-04	3.444444e+01
	 (6,5,0)	 (0.8648, 2.1406, -1.4427)   	3.409091e-02	4.281474e-04	3.446604e+01
	 (6,5,1)	 (0.5762, 2.4292, -1.1540)   	3.409091e-02	6.119398e-04	3.500784e+01
	 (6,6,0)	 (0.8263, 2.2949, -1.6356)   	3.409091e-02	6.350008e-04	3.145663e+01
	 (6,6,1)	 (0.5376, 2.5835, -1.3469)   	3.409091e-02	3.053334e-04	4.353074e+01
	 (6,7,0)	 (0.7877, 2.4492, -1.8285)   	3.409091e-02	6.166669e-04	3.199505e+01
	 (6,7,1)	 (0.4990, 2.7379, -1.5398)   	3.409091e-02	4.378355e-04	3.979696e+01
	 (7,0,0)	 (1.2764, 1.5148, -0.4054)   	3.409091e-02	4.457164e-04	3.471101e+01
	 (7,0,1)	 (0.9877, 1.8035, -0.1168)   	3.409091e-02	8.496423e-04	2.514815e+01
	 (7,1,0)	 (1.2378, 1.6691, -0.5983)   	3.409091e-02	7.127052e-04	2.938105e+01
	 (7,1,1)	 (0.9491, 1.9578, -0.3096)   	3.409091e-02	7.538314e-04	2.704978e+01
	 (7,2,0)	 (1.1992, 1.8234, -0.7912)   	3.409091e-02	2.085834e-04	5.317449e+01
	 (7,2,1)	 (0.9106, 2.1121, -0.5025)   	3.409091e-02	4.220699e-04	3.805590e+01
	 (7,3,0)	 (1.1607, 1.9777, -0.9841)   	3.409091e-02	1.075433e-04	5.215894e+01
	 (7,3,1)	 (0.8720, 2.2664, -0.6954)   	3.409091e-02	5.359608e-04	3.582462e+01
	 (7,4,0)	 (1.1221, 2.1320, -1.1769)   	3.409091e-02	4.750200e-04	3.278824e+01
	 (7,4,1)	 (0.8334, 2.4207, -0.8883)   	3.409091e-02	6.829032e-04	3.261053e+01
	 (7,5,0)	 (1.0835, 2.2863, -1.3698)   	3.409091e-02	5.914557e-04	2.831258e+01
	 (7,5,1)	 (0.7948, 2.5750, -1.0812)   	3.409091e-02	7.543389e-04	2.985584e+01
	 (7,6,0)	 (1.0449, 2.4407, -1.5627)   	3.409091e-02	4.955314e-04	3.899905e+01
	 (7,6,1)	 (0.7563, 2.7293, -1.2740)   	3.409091e-02	1.545905e-04	6.183408e+01
	 (7,7,0)	 (1.0064, 2.5950, -1.7556)   	3.409091e-02	5.040328e-04	3.340244e+01
	 (7,7,1)	 (0.7177, 2.8836, -1.4669)   	3.409091e-02	3.224107e-04	4.217357e+01
	 (8,0,0)	 (1.4951, 1.6606, -0.3325)   	3.409091e-02	2.983583e-04	4.844824e+01
	 (8,0,1)	 (1.2064, 1.9493, -0.0439)   	3.409091e-02	5.668118e-04	3.224099e+01
	 (8,1,0)	 (1.4565, 1.8149, -0.5254)   	3.409091e-02	4.104697e-04	3.088437e+01
	 (8,1,1)	 (1.1678, 2.1036, -0.2367)   	3.409091e-02	8.659262e-04	2.501014e+01
	 (8,2,0)	 (1.4179, 1.9692, -0.7183)   	3.409091e-02	4.248173e-04	4.113103e+01
	 (8,2,1)	 (1.1292, 2.2579, -0.4296)   	3.409091e-02	4.214458e-04	4.165393e+01
	 (8,3,0)	 (1.3793, 2.1235, -0.9112)   	3.409091e-02	1.036703e-04	6.114321e+01
	 (8,3,1)	 (1.0907, 2.4122, -0.6225)   	3.409091e-02	6.597621e-04	2.822302e+01
	 (8,4,0)	 (1.3408, 2.2778, -1.1041)   	3.409091e-02	4.282355e-04	3.735271e+01
	 (8,4,1)	 (1.0521, 2.5665, -0.8154)   	3.409091e-02	4.549993e-04	3.513717e+01
	 (8,5,0)	 (1.3022, 2.4321, -1.2969)   	3.409091e-02	6.163503e-04	3.530916e+01
	 (8,5,1)	 (1.0135, 2.7208, -1.0083)   	3.409091e-02	5.406232e-04	3.354448e+01
	 (8,6,0)	 (1.2636, 2.5864, -1.4898)   	3.409091e-02	6.752466e-04	3.339514e+01
	 (8,6,1)	 (0.9749, 2.8751, -1.2011)   	3.409091e-02	2.504910e-04	4.288679e+01
	 (8,7,0)	 (1.2250, 2.7407, -1.6827)   	3.409091e-02	6.209474e-04	3.172686e+01
	 (8,7,1)	 (0.9363, 3.0294, -1.3940)   	3.409091e-02	3.280775e-04	4.322249e+01
	 (9,0,0)	 (1.7137, 1.8064, -0.2597)   	3.409091e-02	3.265384e-04	4.251439e+01
	 (9,0,1)	 (1.4250, 2.0951, 0.0290)   	3.409091e-02	4.278164e-04	3.778683e+01
	 (9,1,0)	 (1.6751, 1.9607, -0.4525)   	3.409091e-02	3.491789e-04	3.799447e+01
	 (9,1,1)	 (1.3865, 2.2494, -0.1639)   	3.409091e-02	6.322659e-04	3.091975e+01
	 (9,2,0)	 (1.6366, 2.1150, -0.6454)   	3.409091e-02	5.534832e-04	3.569312e+01
	 (9,2,1)	 (1.3479, 2.4037, -0.3567)   	3.409091e-02	1.635123e-04	5.579469e+01
	 (9,3,0)	 (1.5980, 2.2693, -0.8383)   	3.409091e-02	1.998509e-04	5.126297e+01
	 (9,3,1)	 (1.3093, 2.5580, -0.5496)   	3.409091e-02	8.017297e-04	3.413208e+01
	 (9,4,0)	 (1.5594, 2.4236, -1.0312)   	3.409091e-02	2.160351e-04	5.047620e+01
	 (9,4,1)	 (1.2707, 2.7123, -0.7425)   	3.409091e-02	4.529406e-04	3.904460e+01
	 (9,5,0)	 (1.5208, 2.5779, -1.2240)   	3.409091e-02	4.464494e-04	3.694986e+01
	 (9,5,1)	 (1.2322, 2.8666, -0.9354)   	3.409091e-02	2.911286e-04	5.881417e+01
	 (9,6,0)	 (1.4823, 2.7322, -1.4169)   	3.409091e-02	2.719645e-04	4.644106e+01
	 (9,6,1)	 (1.1936, 3.0209, -1.1283)   	3.409091e-02	4.124206e-04	4.122225e+01
	 (9,7,0)	 (1.4437, 2.8865, -1.6098)   	3.409091e-02	2.700263e-04	4.947612e+01
	 (9,7,1)	 (1.1550, 3.1752, -1.3211)   	3.409091e-02	2.950586e-04	4.576533e+01
	 (10,0,0)	 (1.9324, 1.9522, -0.1868)   	3.409091e-02	1.428260e-04	6.087205e+01
	 (10,0,1)	 (1.6437, 2.2408, 0.1019)   	3.409091e-02	4.805775e-04	3.443952e+01
	 (10,1,0)	 (1.8938, 2.1065, -0.3796)   	3.409091e-02	5.412592e-04	3.444180e+01
	 (10,1,1)	 (1.6051, 2.3951, -0.0910)   	3.409091e-02	5.625989e-04	2.996435e+01
	 (10,2,0)	 (1.8552, 2.2608, -0.5725)   	3.409091e-02	2.411104e-04	4.183410e+01
	 (10,2,1)	 (1.5666, 2.5494, -0.2838)   	3.409091e-02	4.806579e-04	3.123702e+01
	 (10,3,0)	 (1.8167, 2.4151, -0.7654)   	3.409091e-02	6.652011e-04	2.832338e+01
	 (10,3,1)	 (1.5280, 2.7038, -0.4767)   	3.409091e-02	3.460718e-04	4.004620e+01
	 (10,4,0)	 (1.7781, 2.5694, -0.9583)   	3.409091e-02	4.303288e-04	3.302948e+01
	 (10,4,1)	 (1.4894, 2.8581, -0.6696)   	3.409091e-02	4.798104e-04	4.035042e+01
	 (10,5,0)	 (1.7395, 2.7237, -1.1512)   	3.409091e-02	2.970056e-04	4.256843e+01
	 (10,5,1)	 (1.4508, 3.0124, -0.8625)   	3.409091e-02	2.441587e-04	4.616890e+01
	 (10,6,0)	 (1.7009, 2.8780, -1.3440)   	3.409091e-02	2.793797e-04	4.628773e+01
	 (10,6,1)	 (1.4123, 3.1667, -1.0554)   	3.409091e-02	3.737843e-04	3.593985e+01
	 (10,7,0)	 (1.6624, 3.0323, -1.5369)   	3.409091e-02	2.801563e-04	4.348309e+01
	 (10,7,1)	 (1.3737, 3.3210, -1.2482)   	3.409091e-02	4.319388e-04	3.888065e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-0.2543, 0.4944, -0.9157)   	3.409091e-02	2.691934e-03	1.560378e+01
	 (0,0,1)	 (-0.5430, 0.7831, -0.6270)   	3.409091e-02	3.720784e-03	1.237210e+01
	 (0,1,0)	 (-0.2929, 0.6487, -1.1085)   	3.409091e-02	2.472525e-03	1.596282e+01
	 (0,1,1)	 (-0.5815, 0.9374, -0.8199)   	3.409091e-02	2.711072e-03	1.792662e+01
	 (0,2,0)	 (-0.3314, 0.8030, -1.3014)   	3.409091e-02	1.313054e-03	2.205896e+01
	 (0,2,1)	 (-0.6201, 1.0917, -1.0127)   	3.409091e-02	2.055046e-03	1.769269e+01
	 (0,3,0)	 (-0.3700, 0.9573, -1.4943)   	3.409091e-02	1.464962e-03	2.730348e+01
	 (0,3,1)	 (-0.6587, 1.2460, -1.2056)   	3.409091e-02	2.957793e-03	1.617782e+01
	 (0,4,0)	 (-0.4086, 1.1116, -1.6872)   	3.409091e-02	1.246838e-03	2.242254e+01
	 (0,4,1)	 (-0.6973, 1.4003, -1.3985)   	3.409091e-02	2.040327e-03	1.684545e+01
	 (0,5,0)	 (-0.4472, 1.2659, -1.8801)   	3.409091e-02	1.984295e-03	2.000107e+01
	 (0,5,1)	 (-0.7358, 1.5546, -1.5914)   	3.409091e-02	1.457153e-03	2.551424e+01
	 (0,6,0)	 (-0.4857, 1.4202, -2.0729)   	3.409091e-02	1.587759e-03	2.208787e+01
	 (0,6,1)	 (-0.7744, 1.7089, -1.7843)   	3.409091e-02	1.849354e-03	2.016996e+01
	 (0,7,0)	 (-0.5243, 1.5745, -2.2658)   	3.409091e-02	1.247143e-03	1.999082e+01
	 (0,7,1)	 (-0.8130, 1.8632, -1.9771)   	3.409091e-02	1.920162e-03	1.835113e+01
	 (1,0,0)	 (-0.0356, 0.6402, -0.8428)   	3.409091e-02	2.231761e-03	1.635625e+01
	 (1,0,1)	 (-0.3243, 0.9288, -0.5541)   	3.409091e-02	2.911941e-03	1.457777e+01
	 (1,1,0)	 (-0.0742, 0.7945, -1.0356)   	3.409091e-02	2.354060e-03	1.854544e+01
	 (1,1,1)	 (-0.3629, 1.0831, -0.7470)   	3.409091e-02	2.790904e-03	1.597406e+01
	 (1,2,0)	 (-0.1128, 0.9488, -1.2285)   	3.409091e-02	1.761890e-03	2.097026e+01
	 (1,2,1)	 (-0.4014, 1.2374, -0.9399)   	3.409091e-02	2.119935e-03	1.494015e+01
	 (1,3,0)	 (-0.1514, 1.1031, -1.4214)   	3.409091e-02	1.114456e-03	2.628494e+01
	 (1,3,1)	 (-0.4400, 1.3917, -1.1327)   	3.409091e-02	1.954230e-03	1.558958e+01
	 (1,4,0)	 (-0.1899, 1.2574, -1.6143)   	3.409091e-02	2.009283e-03	2.328222e+01
	 (1,4,1)	 (-0.4786, 1.5460, -1.3256)   	3.409091e-02	2.553577e-03	1.408920e+01
	 (1,5,0)	 (-0.2285, 1.4117, -1.8072)   	3.409091e-02	1.297284e-03	2.258906e+01
	 (1,5,1)	 (-0.5172, 1.7003, -1.5185)   	3.409091e-02	2.011605e-03	1.630775e+01
	 (1,6,0)	 (-0.2671, 1.5660, -2.0000)   	3.409091e-02	1.079900e-03	2.535453e+01
	 (1,6,1)	 (-0.5558, 1.8547, -1.7114)   	3.409091e-02	1.328695e-03	2.428224e+01
	 (1,7,0)	 (-0.3057, 1.7203, -2.1929)   	3.409091e-02	9.941529e-04	2.243105e+01
	 (1,7,1)	 (-0.5943, 2.0090, -1.9042)   	3.409091e-02	1.426683e-03	1.988738e+01
	 (2,0,0)	 (0.1830, 0.7859, -0.7699)   	3.409091e-02	1.803653e-03	1.879893e+01
	 (2,0,1)	 (-0.1056, 1.0746, -0.4812)   	3.409091e-02	1.370190e-03	2.160634e+01
	 (2,1,0)	 (0.1445, 0.9402, -0.9628)   	3.409091e-02	2.091507e-03	1.816831e+01
	 (2,1,1)	 (-0.1442, 1.2289, -0.6741)   	3.409091e-02	1.806169e-03	1.676848e+01
	 (2,2,0)	 (0.1059, 1.0945, -1.1556)   	3.409091e-02	2.081252e-03	1.842402e+01
	 (2,2,1)	 (-0.1828, 1.3832, -0.8670)   	3.409091e-02	2.143130e-03	1.803149e+01
	 (2,3,0)	 (0.0673, 1.2488, -1.3485)   	3.409091e-02	1.405773e-03	2.193084e+01
	 (2,3,1)	 (-0.2214, 1.5375, -1.0598)   	3.409091e-02	1.861146e-03	1.664946e+01
	 (2,4,0)	 (0.0287, 1.4031, -1.5414)   	3.409091e-02	1.255315e-03	2.244083e+01
	 (2,4,1)	 (-0.2599, 1.6918, -1.2527)   	3.409091e-02	2.012370e-03	1.631938e+01
	 (2,5,0)	 (-0.0098, 1.5575, -1.7343)   	3.409091e-02	1.840797e-03	2.232109e+01
	 (2,5,1)	 (-0.2985, 1.8461, -1.4456)   	3.409091e-02	1.985249e-03	1.737016e+01
	 (2,6,0)	 (-0.0484, 1.7118, -1.9272)   	3.409091e-02	1.393446e-03	2.191599e+01
	 (2,6,1)	 (-0.3371, 2.0004, -1.6385)   	3.409091e-02	1.730331e-03	2.002559e+01
	 (2,7,0)	 (-0.0870, 1.8661, -2.1200)   	3.409091e-02	1.146297e-03	2.479923e+01
	 (2,7,1)	 (-0.3757, 2.1547, -1.8314)   	3.409091e-02	1.334091e-03	2.164539e+01
	 (3,0,0)	 (0.4017, 0.9317, -0.6970)   	3.409091e-02	1.171223e-03	2.456522e+01
	 (3,0,1)	 (0.1130, 1.2204, -0.4083)   	3.409091e-02	1.787330e-03	2.050752e+01
	 (3,1,0)	 (0.3631, 1.0860, -0.8899)   	3.409091e-02	1.911831e-03	1.681192e+01
	 (3,1,1)	 (0.0745, 1.3747, -0.6012)   	3.409091e-02	1.663017e-03	2.104376e+01
	 (3,2,0)	 (0.3246, 1.2403, -1.0827)   	3.409091e-02	1.693598e-03	1.830853e+01
	 (3,2,1)	 (0.0359, 1.5290, -0.7941)   	3.409091e-02	1.466892e-03	1.750744e+01
	 (3,3,0)	 (0.2860, 1.3946, -1.2756)   	3.409091e-02	1.911310e-03	1.991011e+01
	 (3,3,1)	 (-0.0027, 1.6833, -0.9870)   	3.409091e-02	1.132384e-03	2.567486e+01
	 (3,4,0)	 (0.2474, 1.5489, -1.4685)   	3.409091e-02	1.261507e-03	1.990203e+01
	 (3,4,1)	 (-0.0413, 1.8376, -1.1798)   	3.409091e-02	1.714970e-03	2.082082e+01
	 (3,5,0)	 (0.2088, 1.7032, -1.6614)   	3.409091e-02	9.982946e-04	2.356844e+01
	 (3,5,1)	 (-0.0798, 1.9919, -1.3727)   	3.409091e-02	1.917183e-03	1.907946e+01
	 (3,6,0)	 (0.1703, 1.8575, -1.8543)   	3.409091e-02	1.781428e-03	1.667865e+01
	 (3,6,1)	 (-0.1184, 2.1462, -1.5656)   	3.409091e-02	1.142607e-03	2.015390e+01
	 (3,7,0)	 (0.1317, 2.0118, -2.0471)   	3.409091e-02	1.223424e-03	2.133025e+01
	 (3,7,1)	 (-0.1570, 2.3005, -1.7585)   	3.409091e-02	1.377895e-03	1.791197e+01
	 (4,0,0)	 (0.6204, 1.0775, -0.6241)   	3.409091e-02	1.182602e-03	2.697055e+01
	 (4,0,1)	 (0.3317, 1.3662, -0.3354)   	3.409091e-02	1.862184e-03	2.537485e+01
	 (4,1,0)	 (0.5818, 1.2318, -0.8170)   	3.409091e-02	8.581186e-04	2.547421e+01
	 (4,1,1)	 (0.2931, 1.5205, -0.5283)   	3.409091e-02	1.595807e-03	2.031014e+01
	 (4,2,0)	 (0.5432, 1.3861, -1.0099)   	3.409091e-02	1.431141e-03	2.009812e+01
	 (4,2,1)	 (0.2546, 1.6748, -0.7212)   	3.409091e-02	1.651098e-03	1.788921e+01
	 (4,3,0)	 (0.5047, 1.5404, -1.2027)   	3.409091e-02	1.088714e-03	2.078327e+01
	 (4,3,1)	 (0.2160, 1.8291, -0.9141)   	3.409091e-02	1.208498e-03	2.029231e+01
	 (4,4,0)	 (0.4661, 1.6947, -1.3956)   	3.409091e-02	1.437839e-03	1.846528e+01
	 (4,4,1)	 (0.1774, 1.9834, -1.1069)   	3.409091e-02	9.853870e-04	2.366946e+01
	 (4,5,0)	 (0.4275, 1.8490, -1.5885)   	3.409091e-02	1.305555e-03	2.083456e+01
	 (4,5,1)	 (0.1388, 2.1377, -1.2998)   	3.409091e-02	1.431427e-03	2.230947e+01
	 (4,6,0)	 (0.3889, 2.0033, -1.7814)   	3.409091e-02	1.181300e-03	1.973431e+01
	 (4,6,1)	 (0.1003, 2.2920, -1.4927)   	3.409091e-02	1.629224e-03	2.232134e+01
	 (4,7,0)	 (0.3504, 2.1576, -1.9743)   	3.409091e-02	1.320070e-03	2.207031e+01
	 (4,7,1)	 (0.0617, 2.4463, -1.6856)   	3.409091e-02	9.239723e-04	2.504648e+01
	 (5,0,0)	 (0.8391, 1.2233, -0.5512)   	3.409092e-02	1.149654e-03	2.905281e+01
	 (5,0,1)	 (0.5504, 1.5119, -0.2625)   	3.409092e-02	1.572204e-03	2.396097e+01
	 (5,1,0)	 (0.8005, 1.3776, -0.7441)   	3.409092e-02	8.963342e-04	2.555601e+01
	 (5,1,1)	 (0.5118, 1.6663, -0.4554)   	3.409092e-02	2.291737e-03	2.014201e+01
	 (5,2,0)	 (0.7619, 1.5319, -0.9370)   	3.409092e-02	9.740582e-04	3.012931e+01
	 (5,2,1)	 (0.4732, 1.8206, -0.6483)   	3.409092e-02	1.271407e-03	2.072125e+01
	 (5,3,0)	 (0.7233, 1.6862, -1.1298)   	3.409092e-02	9.245268e-04	2.576435e+01
	 (5,3,1)	 (0.4346, 1.9749, -0.8412)   	3.409092e-02	1.460373e-03	2.150109e+01
	 (5,4,0)	 (0.6847, 1.8405, -1.3227)   	3.409092e-02	1.101779e-03	2.418817e+01
	 (5,4,1)	 (0.3961, 2.1292, -1.0341)   	3.409092e-02	5.805877e-04	3.241951e+01
	 (5,5,0)	 (0.6462, 1.9948, -1.5156)   	3.409092e-02	7.190216e-04	2.582315e+01
	 (5,5,1)	 (0.3575, 2.2835, -1.2269)   	3.409092e-02	8.707344e-04	2.607013e+01
	 (5,6,0)	 (0.6076, 2.1491, -1.7085)   	3.409092e-02	1.161390e-03	2.233967e+01
	 (5,6,1)	 (0.3189, 2.4378, -1.4198)   	3.409092e-02	1.475615e-03	1.947650e+01
	 (5,7,0)	 (0.5690, 2.3034, -1.9014)   	3.409092e-02	1.140059e-03	2.245621e+01
	 (5,7,1)	 (0.2803, 2.5921, -1.6127)   	3.409092e-02	1.429104e-03	2.381118e+01
	 (6,0,0)	 (1.0577, 1.3691, -0.4783)   	3.409091e-02	1.019410e-03	2.391945e+01
	 (6,0,1)	 (0.7690, 1.6577, -0.1896)   	3.409091e-02	1.566446e-03	2.195972e+01
	 (6,1,0)	 (1.0191, 1.5234, -0.6712)   	3.409091e-02	1.070631e-03	2.720775e+01
	 (6,1,1)	 (0.7305, 1.8120, -0.3825)   	3.409091e-02	1.986344e-03	1.784774e+01
	 (6,2,0)	 (0.9806, 1.6777, -0.8641)   	3.409091e-02	7.785370e-04	2.682476e+01
	 (6,2,1)	 (0.6919, 1.9663, -0.5754)   	3.409091e-02	1.438990e-03	1.933571e+01
	 (6,3,0)	 (0.9420, 1.8320, -1.0570)   	3.409091e-02	9.773215e-04	2.578126e+01
	 (6,3,1)	 (0.6533, 2.1206, -0.7683)   	3.409091e-02	9.536189e-04	2.759550e+01
	 (6,4,0)	 (0.9034, 1.9863, -1.2498)   	3.409091e-02	8.209850e-04	2.588016e+01
	 (6,4,1)	 (0.6147, 2.2749, -0.9612)   	3.409091e-02	9.919626e-04	3.107308e+01
	 (6,5,0)	 (0.8648, 2.1406, -1.4427)   	3.409091e-02	6.866767e-04	3.151274e+01
	 (6,5,1)	 (0.5762, 2.4292, -1.1540)   	3.409091e-02	6.367609e-04	2.978282e+01
	 (6,6,0)	 (0.8263, 2.2949, -1.6356)   	3.409091e-02	7.637064e-04	3.012235e+01
	 (6,6,1)	 (0.5376, 2.5835, -1.3469)   	3.409091e-02	7.980260e-04	2.358591e+01
	 (6,7,0)	 (0.7877, 2.4492, -1.8285)   	3.409091e-02	8.865801e-04	2.465742e+01
	 (6,7,1)	 (0.4990, 2.7379, -1.5398)   	3.409091e-02	1.501326e-03	2.177603e+01
	 (7,0,0)	 (1.2764, 1.5148, -0.4054)   	3.409091e-02	1.194253e-03	2.525546e+01
	 (7,0,1)	 (0.9877, 1.8035, -0.1168)   	3.409091e-02	1.544223e-03	2.211167e+01
	 (7,1,0)	 (1.2378, 1.6691, -0.5983)   	3.409091e-02	8.000778e-04	2.884469e+01
	 (7,1,1)	 (0.9491, 1.9578, -0.3096)   	3.409091e-02	1.294968e-03	2.218341e+01
	 (7,2,0)	 (1.1992, 1.8234, -0.7912)   	3.409091e-02	1.468387e-03	2.451580e+01
	 (7,2,1)	 (0.9106, 2.1121, -0.5025)   	3.409091e-02	1.761865e-03	2.130789e+01
	 (7,3,0)	 (1.1607, 1.9777, -0.9841)   	3.409091e-02	5.924823e-04	2.957320e+01
	 (7,3,1)	 (0.8720, 2.2664, -0.6954)   	3.409091e-02	1.088640e-03	2.542339e+01
	 (7,4,0)	 (1.1221, 2.1320, -1.1769)   	3.409091e-02	1.051853e-03	2.413799e+01
	 (7,4,1)	 (0.8334, 2.4207, -0.8883)   	3.409091e-02	8.759771e-04	2.655002e+01
	 (7,5,0)	 (1.0835, 2.2863, -1.3698)   	3.409091e-02	7.332353e-04	2.616150e+01
	 (7,5,1)	 (0.7948, 2.5750, -1.0812)   	3.409091e-02	7.175491e-04	2.445770e+01
	 (7,6,0)	 (1.0449, 2.4407, -1.5627)   	3.409091e-02	4.764263e-04	3.347342e+01
	 (7,6,1)	 (0.7563, 2.7293, -1.2740)   	3.409091e-02	6.697995e-04	2.707839e+01
	 (7,7,0)	 (1.0064, 2.5950, -1.7556)   	3.409091e-02	7.691903e-04	2.946082e+01
	 (7,7,1)	 (0.7177, 2.8836, -1.4669)   	3.409091e-02	5.911793e-04	2.741911e+01
	 (8,0,0)	 (1.4951, 1.6606, -0.3325)   	3.409091e-02	1.152552e-03	2.338962e+01
	 (8,0,1)	 (1.2064, 1.9493, -0.0439)   	3.409091e-02	1.400907e-03	2.386107e+01
	 (8,1,0)	 (1.4565, 1.8149, -0.5254)   	3.409091e-02	9.520658e-04	2.684617e+01
	 (8,1,1)	 (1.1678, 2.1036, -0.2367)   	3.409091e-02	7.771682e-04	2.345155e+01
	 (8,2,0)	 (1.4179, 1.9692, -0.7183)   	3.409091e-02	1.235756e-03	3.151539e+01
	 (8,2,1)	 (1.1292, 2.2579, -0.4296)   	3.409091e-02	1.853526e-03	1.669705e+01
	 (8,3,0)	 (1.3793, 2.1235, -0.9112)   	3.409091e-02	1.169827e-03	2.175189e+01
	 (8,3,1)	 (1.0907, 2.4122, -0.6225)   	3.409091e-02	1.226184e-03	2.221614e+01
	 (8,4,0)	 (1.3408, 2.2778, -1.1041)   	3.409091e-02	7.239733e-04	2.975281e+01
	 (8,4,1)	 (1.0521, 2.5665, -0.8154)   	3.409091e-02	9.859041e-04	2.324003e+01
	 (8,5,0)	 (1.3022, 2.4321, -1.2969)   	3.409091e-02	9.619894e-04	2.582589e+01
	 (8,5,1)	 (1.0135, 2.7208, -1.0083)   	3.409091e-02	8.531247e-04	2.652268e+01
	 (8,6,0)	 (1.2636, 2.5864, -1.4898)   	3.409091e-02	3.977439e-04	3.858163e+01
	 (8,6,1)	 (0.9749, 2.8751, -1.2011)   	3.409091e-02	5.105281e-04	3.107592e+01
	 (8,7,0)	 (1.2250, 2.7407, -1.6827)   	3.409091e-02	5.853264e-04	3.380104e+01
	 (8,7,1)	 (0.9363, 3.0294, -1.3940)   	3.409091e-02	9.483297e-04	2.377901e+01
	 (9,0,0)	 (1.7137, 1.8064, -0.2597)   	3.409091e-02	1.333990e-03	1.948746e+01
	 (9,0,1)	 (1.4250, 2.0951, 0.0290)   	3.409091e-02	9.021216e-04	2.581272e+01
	 (9,1,0)	 (1.6751, 1.9607, -0.4525)   	3.409091e-02	1.120874e-03	2.341649e+01
	 (9,1,1)	 (1.3865, 2.2494, -0.1639)   	3.409091e-02	9.148182e-04	2.662271e+01
	 (9,2,0)	 (1.6366, 2.1150, -0.6454)   	3.409091e-02	9.698802e-04	3.318273e+01
	 (9,2,1)	 (1.3479, 2.4037, -0.3567)   	3.409091e-02	1.282327e-03	1.957057e+01
	 (9,3,0)	 (1.5980, 2.2693, -0.8383)   	3.409091e-02	1.255443e-03	2.167848e+01
	 (9,3,1)	 (1.3093, 2.5580, -0.5496)   	3.409091e-02	1.548580e-03	2.148476e+01
	 (9,4,0)	 (1.5594, 2.4236, -1.0312)   	3.409091e-02	6.956796e-04	2.830446e+01
	 (9,4,1)	 (1.2707, 2.7123, -0.7425)   	3.409091e-02	9.659590e-04	2.485934e+01
	 (9,5,0)	 (1.5208, 2.5779, -1.2240)   	3.409091e-02	5.761381e-04	3.506953e+01
	 (9,5,1)	 (1.2322, 2.8666, -0.9354)   	3.409091e-02	7.396343e-04	2.718519e+01
	 (9,6,0)	 (1.4823, 2.7322, -1.4169)   	3.409091e-02	7.625698e-04	3.537601e+01
	 (9,6,1)	 (1.1936, 3.0209, -1.1283)   	3.409091e-02	6.373579e-04	2.974844e+01
	 (9,7,0)	 (1.4437, 2.8865, -1.6098)   	3.409091e-02	2.835143e-04	4.352636e+01
	 (9,7,1)	 (1.1550, 3.1752, -1.3211)   	3.409091e-02	8.297678e-04	2.852856e+01
	 (10,0,0)	 (1.9324, 1.9522, -0.1868)   	3.409091e-02	9.897017e-04	2.230907e+01
	 (10,0,1)	 (1.6437, 2.2408, 0.1019)   	3.409091e-02	7.464000e-04	3.029603e+01
	 (10,1,0)	 (1.8938, 2.1065, -0.3796)   	3.409091e-02	1.063001e-03	2.856685e+01
	 (10,1,1)	 (1.6051, 2.3951, -0.0910)   	3.409091e-02	1.136847e-03	2.064042e+01
	 (10,2,0)	 (1.8552, 2.2608, -0.5725)   	3.409091e-02	4.684493e-04	3.154352e+01
	 (10,2,1)	 (1.5666, 2.5494, -0.2838)   	3.409091e-02	7.690764e-04	2.505980e+01
	 (10,3,0)	 (1.8167, 2.4151, -0.7654)   	3.409091e-02	1.282303e-03	1.959732e+01
	 (10,3,1)	 (1.5280, 2.7038, -0.4767)   	3.409091e-02	1.310869e-03	2.055788e+01
	 (10,4,0)	 (1.7781, 2.5694, -0.9583)   	3.409091e-02	8.343123e-04	2.846870e+01
	 (10,4,1)	 (1.4894, 2.8581, -0.6696)   	3.409091e-02	8.964694e-04	2.651428e+01
	 (10,5,0)	 (1.7395, 2.7237, -1.1512)   	3.409091e-02	7.731268e-04	3.314715e+01
	 (10,5,1)	 (1.4508, 3.0124, -0.8625)   	3.409091e-02	9.227369e-04	2.720193e+01
	 (10,6,0)	 (1.7009, 2.8780, -1.3440)   	3.409091e-02	4.941902e-04	3.819864e+01
	 (10,6,1)	 (1.4123, 3.1667, -1.0554)   	3.409091e-02	7.459049e-04	2.866069e+01
	 (10,7,0)	 (1.6624, 3.0323, -1.5369)   	3.409091e-02	5.314081e-04	3.432001e+01
	 (10,7,1)	 (1.3737, 3.3210, -1.2482)   	3.409091e-02	5.996118e-04	2.820745e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-0.2543, 0.4944, -0.9157)	3.409091e-02	3.416707e-03	1.607348e+01
	 (0,0,1)	 (-0.5430, 0.7831, -0.6270)	3.409091e-02	4.408642e-03	1.138781e+01
	 (0,1,0)	 (-0.2929, 0.6487, -1.1085)	3.409091e-02	2.911509e-03	1.598475e+01
	 (0,1,1)	 (-0.5815, 0.9374, -0.8199)	3.409091e-02	3.904474e-03	1.391825e+01
	 (0,2,0)	 (-0.3314, 0.8030, -1.3014)	3.409091e-02	1.887760e-03	1.854679e+01
	 (0,2,1)	 (-0.6201, 1.0917, -1.0127)	3.409091e-02	2.854036e-03	1.547546e+01
	 (0,3,0)	 (-0.3700, 0.9573, -1.4943)	3.409091e-02	2.236801e-03	2.047036e+01
	 (0,3,1)	 (-0.6587, 1.2460, -1.2056)	3.409091e-02	3.718610e-03	1.391707e+01
	 (0,4,0)	 (-0.4086, 1.1116, -1.6872)	3.409091e-02	1.703188e-03	1.717519e+01
	 (0,4,1)	 (-0.6973, 1.4003, -1.3985)	3.409091e-02	2.559461e-03	1.488262e+01
	 (0,5,0)	 (-0.4472, 1.2659, -1.8801)	3.409091e-02	2.627814e-03	1.582433e+01
	 (0,5,1)	 (-0.7358, 1.5546, -1.5914)	3.409091e-02	1.741349e-03	2.424251e+01
	 (0,6,0)	 (-0.4857, 1.4202, -2.0729)	3.409091e-02	1.951230e-03	1.922501e+01
	 (0,6,1)	 (-0.7744, 1.7089, -1.7843)	3.409091e-02	2.379369e-03	1.752400e+01
	 (0,7,0)	 (-0.5243, 1.5745, -2.2658)	3.409091e-02	1.763051e-03	1.734985e+01
	 (0,7,1)	 (-0.8130, 1.8632, -1.9771)	3.409091e-02	2.453763e-03	1.703817e+01
	 (1,0,0)	 (-0.0356, 0.6402, -0.8428)	3.409091e-02	3.010619e-03	1.440413e+01
	 (1,0,1)	 (-0.3243, 0.9288, -0.5541)	3.409091e-02	3.486630e-03	1.349357e+01
	 (1,1,0)	 (-0.0742, 0.7945, -1.0356)	3.409091e-02	2.803079e-03	1.520904e+01
	 (1,1,1)	 (-0.3629, 1.0831, -0.7470)	3.409091e-02	3.275433e-03	1.525467e+01
	 (1,2,0)	 (-0.1128, 0.9488, -1.2285)	3.409091e-02	2.017192e-03	1.957237e+01
	 (1,2,1)	 (-0.4014, 1.2374, -0.9399)	3.409091e-02	2.932757e-03	1.397167e+01
	 (1,3,0)	 (-0.1514, 1.1031, -1.4214)	3.409091e-02	1.645118e-03	1.860584e+01
	 (1,3,1)	 (-0.4400, 1.3917, -1.1327)	3.409091e-02	2.201958e-03	1.343584e+01
	 (1,4,0)	 (-0.1899, 1.2574, -1.6143)	3.409091e-02	2.323637e-03	1.988807e+01
	 (1,4,1)	 (-0.4786, 1.5460, -1.3256)	3.409091e-02	2.998244e-03	1.219605e+01
	 (1,5,0)	 (-0.2285, 1.4117, -1.8072)	3.409091e-02	1.950859e-03	1.750891e+01
	 (1,5,1)	 (-0.5172, 1.7003, -1.5185)	3.409091e-02	2.305362e-03	1.443674e+01
	 (1,6,0)	 (-0.2671, 1.5660, -2.0000)	3.409091e-02	1.408279e-03	2.160544e+01
	 (1,6,1)	 (-0.5558, 1.8547, -1.7114)	3.409091e-02	1.709299e-03	1.980957e+01
	 (1,7,0)	 (-0.3057, 1.7203, -2.1929)	3.409091e-02	1.354508e-03	1.959584e+01
	 (1,7,1)	 (-0.5943, 2.0090, -1.9042)	3.409091e-02	2.029181e-03	1.688574e+01
	 (2,0,0)	 (0.1830, 0.7859, -0.7699)	3.409091e-02	2.694673e-03	1.415490e+01
	 (2,0,1)	 (-0.1056, 1.0746, -0.4812)	3.409091e-02	1.870662e-03	1.892652e+01
	 (2,1,0)	 (0.1445, 0.9402, -0.9628)	3.409091e-02	2.408271e-03	1.616370e+01
	 (2,1,1)	 (-0.1442, 1.2289, -0.6741)	3.409091e-02	2.316032e-03	1.353268e+01
	 (2,2,0)	 (0.1059, 1.0945, -1.1556)	3.409091e-02	2.392566e-03	1.567250e+01
	 (2,2,1)	 (-0.1828, 1.3832, -0.8670)	3.409091e-02	2.917048e-03	1.567977e+01
	 (2,3,0)	 (0.0673, 1.2488, -1.3485)	3.409091e-02	1.862536e-03	1.747843e+01
	 (2,3,1)	 (-0.2214, 1.5375, -1.0598)	3.409091e-02	2.317852e-03	1.513299e+01
	 (2,4,0)	 (0.0287, 1.4031, -1.5414)	3.409091e-02	1.761177e-03	1.700514e+01
	 (2,4,1)	 (-0.2599, 1.6918, -1.2527)	3.409091e-02	2.233892e-03	1.483491e+01
	 (2,5,0)	 (-0.0098, 1.5575, -1.7343)	3.409091e-02	2.178265e-03	2.057861e+01
	 (2,5,1)	 (-0.2985, 1.8461, -1.4456)	3.409091e-02	2.507361e-03	1.396643e+01
	 (2,6,0)	 (-0.0484, 1.7118, -1.9272)	3.409091e-02	1.559987e-03	2.010735e+01
	 (2,6,1)	 (-0.3371, 2.0004, -1.6385)	3.409091e-02	2.079565e-03	1.618682e+01
	 (2,7,0)	 (-0.0870, 1.8661, -2.1200)	3.409091e-02	1.248935e-03	2.274424e+01
	 (2,7,1)	 (-0.3757, 2.1547, -1.8314)	3.409091e-02	1.835219e-03	1.809207e+01
	 (3,0,0)	 (0.4017, 0.9317, -0.6970)	3.409091e-02	1.725983e-03	1.816177e+01
	 (3,0,1)	 (0.1130, 1.2204, -0.4083)	3.409091e-02	2.385206e-03	1.773522e+01
	 (3,1,0)	 (0.3631, 1.0860, -0.8899)	3.409091e-02	2.331724e-03	1.539232e+01
	 (3,1,1)	 (0.0745, 1.3747, -0.6012)	3.409091e-02	2.140695e-03	1.857010e+01
	 (3,2,0)	 (0.3246, 1.2403, -1.0827)	3.409091e-02	2.153570e-03	1.690787e+01
	 (3,2,1)	 (0.0359, 1.5290, -0.7941)	3.409091e-02	2.085908e-03	1.476056e+01
	 (3,3,0)	 (0.2860, 1.3946, -1.2756)	3.409091e-02	2.458809e-03	1.818553e+01
	 (3,3,1)	 (-0.0027, 1.6833, -0.9870)	3.409091e-02	1.524203e-03	2.006654e+01
	 (3,4,0)	 (0.2474, 1.5489, -1.4685)	3.409091e-02	1.838466e-03	1.763014e+01
	 (3,4,1)	 (-0.0413, 1.8376, -1.1798)	3.409091e-02	2.146847e-03	1.939666e+01
	 (3,5,0)	 (0.2088, 1.7032, -1.6614)	3.409091e-02	1.293295e-03	2.097421e+01
	 (3,5,1)	 (-0.0798, 1.9919, -1.3727)	3.409091e-02	2.551250e-03	1.699663e+01
	 (3,6,0)	 (0.1703, 1.8575, -1.8543)	3.409091e-02	1.960513e-03	1.552720e+01
	 (3,6,1)	 (-0.1184, 2.1462, -1.5656)	3.409091e-02	1.755848e-03	1.519394e+01
	 (3,7,0)	 (0.1317, 2.0118, -2.0471)	3.409091e-02	1.516429e-03	1.791313e+01
	 (3,7,1)	 (-0.1570, 2.3005, -1.7585)	3.409091e-02	1.711813e-03	1.466755e+01
	 (4,0,0)	 (0.6204, 1.0775, -0.6241)	3.409091e-02	1.621788e-03	2.269008e+01
	 (4,0,1)	 (0.3317, 1.3662, -0.3354)	3.409091e-02	2.092046e-03	2.509684e+01
	 (4,1,0)	 (0.5818, 1.2318, -0.8170)	3.409091e-02	1.145219e-03	2.443782e+01
	 (4,1,1)	 (0.2931, 1.5205, -0.5283)	3.409091e-02	1.992229e-03	1.710224e+01
	 (4,2,0)	 (0.5432, 1.3861, -1.0099)	3.409091e-02	1.614525e-03	1.873598e+01
	 (4,2,1)	 (0.2546, 1.6748, -0.7212)	3.409091e-02	1.910822e-03	1.631248e+01
	 (4,3,0)	 (0.5047, 1.5404, -1.2027)	3.409091e-02	1.761599e-03	1.838921e+01
	 (4,3,1)	 (0.2160, 1.8291, -0.9141)	3.409091e-02	2.089741e-03	1.722516e+01
	 (4,4,0)	 (0.4661, 1.6947, -1.3956)	3.409091e-02	1.977738e-03	1.624674e+01
	 (4,4,1)	 (0.1774, 1.9834, -1.1069)	3.409091e-02	1.683856e-03	1.651995e+01
	 (4,5,0)	 (0.4275, 1.8490, -1.5885)	3.409091e-02	1.692605e-03	1.762494e+01
	 (4,5,1)	 (0.1388, 2.1377, -1.2998)	3.409091e-02	1.892525e-03	2.123626e+01
	 (4,6,0)	 (0.3889, 2.0033, -1.7814)	3.409091e-02	1.366491e-03	1.758132e+01
	 (4,6,1)	 (0.1003, 2.2920, -1.4927)	3.409091e-02	2.110705e-03	2.048190e+01
	 (4,7,0)	 (0.3504, 2.1576, -1.9743)	3.409091e-02	1.509016e-03	1.924515e+01
	 (4,7,1)	 (0.0617, 2.4463, -1.6856)	3.409091e-02	1.495203e-03	1.892218e+01
	 (5,0,0)	 (0.8391, 1.2233, -0.5512)	3.409092e-02	1.692757e-03	2.421884e+01
	 (5,0,1)	 (0.5504, 1.5119, -0.2625)	3.409092e-02	2.559489e-03	2.036653e+01
	 (5,1,0)	 (0.8005, 1.3776, -0.7441)	3.409092e-02	1.336559e-03	2.017542e+01
	 (5,1,1)	 (0.5118, 1.6663, -0.4554)	3.409092e-02	2.560543e-03	1.824795e+01
	 (5,2,0)	 (0.7619, 1.5319, -0.9370)	3.409092e-02	1.294346e-03	2.613888e+01
	 (5,2,1)	 (0.4732, 1.8206, -0.6483)	3.409092e-02	1.585441e-03	1.822747e+01
	 (5,3,0)	 (0.7233, 1.6862, -1.1298)	3.409092e-02	1.288630e-03	2.024187e+01
	 (5,3,1)	 (0.4346, 1.9749, -0.8412)	3.409092e-02	1.841124e-03	1.982668e+01
	 (5,4,0)	 (0.6847, 1.8405, -1.3227)	3.409092e-02	2.075860e-03	1.870610e+01
	 (5,4,1)	 (0.3961, 2.1292, -1.0341)	3.409092e-02	1.009597e-03	2.409478e+01
	 (5,5,0)	 (0.6462, 1.9948, -1.5156)	3.409092e-02	1.140901e-03	2.253544e+01
	 (5,5,1)	 (0.3575, 2.2835, -1.2269)	3.409092e-02	1.437373e-03	1.933373e+01
	 (5,6,0)	 (0.6076, 2.1491, -1.7085)	3.409092e-02	1.646650e-03	1.879051e+01
	 (5,6,1)	 (0.3189, 2.4378, -1.4198)	3.409092e-02	1.830496e-03	1.988029e+01
	 (5,7,0)	 (0.5690, 2.3034, -1.9014)	3.409092e-02	1.434313e-03	2.050570e+01
	 (5,7,1)	 (0.2803, 2.5921, -1.6127)	3.409092e-02	1.857033e-03	1.944742e+01
	 (6,0,0)	 (1.0577, 1.3691, -0.4783)	3.409091e-02	1.531776e-03	2.139040e+01
	 (6,0,1)	 (0.7690, 1.6577, -0.1896)	3.409091e-02	2.551986e-03	1.823200e+01
	 (6,1,0)	 (1.0191, 1.5234, -0.6712)	3.409091e-02	1.605450e-03	2.249255e+01
	 (6,1,1)	 (0.7305, 1.8120, -0.3825)	3.409091e-02	2.275939e-03	1.637290e+01
	 (6,2,0)	 (0.9806, 1.6777, -0.8641)	3.409091e-02	1.174835e-03	2.232734e+01
	 (6,2,1)	 (0.6919, 1.9663, -0.5754)	3.409091e-02	1.881672e-03	1.731588e+01
	 (6,3,0)	 (0.9420, 1.8320, -1.0570)	3.409091e-02	1.213577e-03	2.327259e+01
	 (6,3,1)	 (0.6533, 2.1206, -0.7683)	3.409091e-02	1.327778e-03	2.171747e+01
	 (6,4,0)	 (0.9034, 1.9863, -1.2498)	3.409091e-02	1.406293e-03	2.077141e+01
	 (6,4,1)	 (0.6147, 2.2749, -0.9612)	3.409091e-02	1.460460e-03	2.435714e+01
	 (6,5,0)	 (0.8648, 2.1406, -1.4427)	3.409091e-02	1.114824e-03	2.502251e+01
	 (6,5,1)	 (0.5762, 2.4292, -1.1540)	3.409091e-02	1.248701e-03	2.056660e+01
	 (6,6,0)	 (0.8263, 2.2949, -1.6356)	3.409091e-02	1.398707e-03	2.250072e+01
	 (6,6,1)	 (0.5376, 2.5835, -1.3469)	3.409091e-02	1.103359e-03	2.044561e+01
	 (6,7,0)	 (0.7877, 2.4492, -1.8285)	3.409091e-02	1.503247e-03	2.010228e+01
	 (6,7,1)	 (0.4990, 2.7379, -1.5398)	3.409091e-02	1.939162e-03	1.987963e+01
	 (7,0,0)	 (1.2764, 1.5148, -0.4054)	3.409091e-02	1.639970e-03	1.962175e+01
	 (7,0,1)	 (0.9877, 1.8035, -0.1168)	3.409091e-02	2.393866e-03	1.889539e+01
	 (7,1,0)	 (1.2378, 1.6691, -0.5983)	3.409091e-02	1.512783e-03	1.976671e+01
	 (7,1,1)	 (0.9491, 1.9578, -0.3096)	3.409091e-02	2.048800e-03	1.824232e+01
	 (7,2,0)	 (1.1992, 1.8234, -0.7912)	3.409091e-02	1.676971e-03	2.144997e+01
	 (7,2,1)	 (0.9106, 2.1121, -0.5025)	3.409091e-02	2.183935e-03	1.874760e+01
	 (7,3,0)	 (1.1607, 1.9777, -0.9841)	3.409091e-02	7.000256e-04	2.547923e+01
	 (7,3,1)	 (0.8720, 2.2664, -0.6954)	3.409091e-02	1.624600e-03	1.963711e+01
	 (7,4,0)	 (1.1221, 2.1320, -1.1769)	3.409091e-02	1.526873e-03	2.025345e+01
	 (7,4,1)	 (0.8334, 2.4207, -0.8883)	3.409091e-02	1.558880e-03	2.038053e+01
	 (7,5,0)	 (1.0835, 2.2863, -1.3698)	3.409091e-02	1.324691e-03	2.066424e+01
	 (7,5,1)	 (0.7948, 2.5750, -1.0812)	3.409091e-02	1.471888e-03	2.034875e+01
	 (7,6,0)	 (1.0449, 2.4407, -1.5627)	3.409091e-02	9.719577e-04	2.658922e+01
	 (7,6,1)	 (0.7563, 2.7293, -1.2740)	3.409091e-02	8.243901e-04	2.458418e+01
	 (7,7,0)	 (1.0064, 2.5950, -1.7556)	3.409091e-02	1.273223e-03	2.056331e+01
	 (7,7,1)	 (0.7177, 2.8836, -1.4669)	3.409091e-02	9.135900e-04	2.186490e+01
	 (8,0,0)	 (1.4951, 1.6606, -0.3325)	3.409091e-02	1.450911e-03	2.260825e+01
	 (8,0,1)	 (1.2064, 1.9493, -0.0439)	3.409091e-02	1.967718e-03	1.983798e+01
	 (8,1,0)	 (1.4565, 1.8149, -0.5254)	3.409091e-02	1.362535e-03	2.117920e+01
	 (8,1,1)	 (1.1678, 2.1036, -0.2367)	3.409091e-02	1.643094e-03	1.880597e+01
	 (8,2,0)	 (1.4179, 1.9692, -0.7183)	3.409091e-02	1.660573e-03	2.505381e+01
	 (8,2,1)	 (1.1292, 2.2579, -0.4296)	3.409091e-02	2.274972e-03	1.488490e+01
	 (8,3,0)	 (1.3793, 2.1235, -0.9112)	3.409091e-02	1.273497e-03	2.007448e+01
	 (8,3,1)	 (1.0907, 2.4122, -0.6225)	3.409091e-02	1.885946e-03	1.653458e+01
	 (8,4,0)	 (1.3408, 2.2778, -1.1041)	3.409091e-02	1.152209e-03	2.620073e+01
	 (8,4,1)	 (1.0521, 2.5665, -0.8154)	3.409091e-02	1.440903e-03	1.997639e+01
	 (8,5,0)	 (1.3022, 2.4321, -1.2969)	3.409091e-02	1.578340e-03	2.510739e+01
	 (8,5,1)	 (1.0135, 2.7208, -1.0083)	3.409091e-02	1.393748e-03	2.027666e+01
	 (8,6,0)	 (1.2636, 2.5864, -1.4898)	3.409091e-02	1.072991e-03	2.538132e+01
	 (8,6,1)	 (0.9749, 2.8751, -1.2011)	3.409091e-02	7.610190e-04	2.745782e+01
	 (8,7,0)	 (1.2250, 2.7407, -1.6827)	3.409091e-02	1.206274e-03	2.403500e+01
	 (8,7,1)	 (0.9363, 3.0294, -1.3940)	3.409091e-02	1.276407e-03	1.896795e+01
	 (9,0,0)	 (1.7137, 1.8064, -0.2597)	3.409091e-02	1.660529e-03	1.582730e+01
	 (9,0,1)	 (1.4250, 2.0951, 0.0290)	3.409091e-02	1.329938e-03	2.168468e+01
	 (9,1,0)	 (1.6751, 1.9607, -0.4525)	3.409091e-02	1.470053e-03	2.068123e+01
	 (9,1,1)	 (1.3865, 2.2494, -0.1639)	3.409091e-02	1.547084e-03	2.284216e+01
	 (9,2,0)	 (1.6366, 2.1150, -0.6454)	3.409091e-02	1.523363e-03	2.791272e+01
	 (9,2,1)	 (1.3479, 2.4037, -0.3567)	3.409091e-02	1.445839e-03	1.825663e+01
	 (9,3,0)	 (1.5980, 2.2693, -0.8383)	3.409091e-02	1.455294e-03	2.154090e+01
	 (9,3,1)	 (1.3093, 2.5580, -0.5496)	3.409091e-02	2.350309e-03	1.984469e+01
	 (9,4,0)	 (1.5594, 2.4236, -1.0312)	3.409091e-02	9.117147e-04	2.462300e+01
	 (9,4,1)	 (1.2707, 2.7123, -0.7425)	3.409091e-02	1.418900e-03	2.114938e+01
	 (9,5,0)	 (1.5208, 2.5779, -1.2240)	3.409091e-02	1.022587e-03	2.623155e+01
	 (9,5,1)	 (1.2322, 2.8666, -0.9354)	3.409091e-02	1.030763e-03	2.597404e+01
	 (9,6,0)	 (1.4823, 2.7322, -1.4169)	3.409091e-02	1.034534e-03	2.964017e+01
	 (9,6,1)	 (1.1936, 3.0209, -1.1283)	3.409091e-02	1.049779e-03	2.555769e+01
	 (9,7,0)	 (1.4437, 2.8865, -1.6098)	3.409091e-02	5.535406e-04	3.193245e+01
	 (9,7,1)	 (1.1550, 3.1752, -1.3211)	3.409091e-02	1.124826e-03	2.452030e+01
	 (10,0,0)	 (1.9324, 1.9522, -0.1868)	3.409091e-02	1.132528e-03	2.102769e+01
	 (10,0,1)	 (1.6437, 2.2408, 0.1019)	3.409091e-02	1.226978e-03	2.060007e+01
	 (10,1,0)	 (1.8938, 2.1065, -0.3796)	3.409091e-02	1.604260e-03	2.138938e+01
	 (10,1,1)	 (1.6051, 2.3951, -0.0910)	3.409091e-02	1.699446e-03	1.836697e+01
	 (10,2,0)	 (1.8552, 2.2608, -0.5725)	3.409091e-02	7.095597e-04	2.812419e+01
	 (10,2,1)	 (1.5666, 2.5494, -0.2838)	3.409091e-02	1.249734e-03	2.043895e+01
	 (10,3,0)	 (1.8167, 2.4151, -0.7654)	3.409091e-02	1.947504e-03	1.701304e+01
	 (10,3,1)	 (1.5280, 2.7038, -0.4767)	3.409091e-02	1.656941e-03	1.756406e+01
	 (10,4,0)	 (1.7781, 2.5694, -0.9583)	3.409091e-02	1.264641e-03	2.249649e+01
	 (10,4,1)	 (1.4894, 2.8581, -0.6696)	3.409091e-02	1.376280e-03	2.300854e+01
	 (10,5,0)	 (1.7395, 2.7237, -1.1512)	3.409091e-02	1.070132e-03	2.592867e+01
	 (10,5,1)	 (1.4508, 3.0124, -0.8625)	3.409091e-02	1.166896e-03	2.232055e+01
	 (10,6,0)	 (1.7009, 2.8780, -1.3440)	3.409091e-02	7.735700e-04	3.066484e+01
	 (10,6,1)	 (1.4123, 3.1667, -1.0554)	3.409091e-02	1.119689e-03	2.175704e+01
	 (10,7,0)	 (1.6624, 3.0323, -1.5369)	3.409091e-02	8.115644e-04	2.690231e+01
	 (10,7,1)	 (1.3737, 3.3210, -1.2482)	3.409091e-02	1.031551e-03	2.084568e+01

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh9
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)   	2.000000e-02	3.548183e-04	2.908689e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)   	1.800000e-01	3.688733e-03	1.614440e+01
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)   	3.000000e-02	6.387578e-04	2.274438e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)   	2.700000e-01	4.433123e-03	1.496963e+01
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)   	1.500000e-01	2.065831e-03	1.535430e+01
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)   	1.350000e+00	1.814250e-02	1.021705e+01
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)   	4.000000e-02	4.262798e-04	2.672816e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)   	3.600000e-01	5.619577e-03	1.541254e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)   	6.000000e-02	7.477164e-04	2.347054e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)   	5.400000e-01	7.972263e-03	1.448405e+01
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)   	3.000000e-01	3.216330e-03	1.375848e+01
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)   	2.700000e+00	3.471839e-02	9.541922e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)   	2.000000e-02	8.654080e-04	1.822471e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)   	1.800000e-01	1.245137e-02	9.165983e+00
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)   	3.000000e-02	1.883653e-03	1.284409e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)   	2.700000e-01	1.832676e-02	8.745180e+00
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)   	1.500000e-01	6.319981e-03	9.460421e+00
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)   	1.350000e+00	6.666933e-02	5.988285e+00
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)   	4.000000e-02	1.004651e-03	1.812488e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)   	3.600000e-01	1.396419e-02	1.278745e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)   	6.000000e-02	1.696827e-03	1.739787e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)   	5.400000e-01	1.967248e-02	1.131499e+01
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)   	3.000000e-01	7.551583e-03	7.976263e+00
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)   	2.700000e+00	8.040685e-02	5.072241e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)	2.000000e-02	1.220226e-03	1.325894e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)	1.800000e-01	1.614011e-02	8.301713e+00
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)	3.000000e-02	2.522410e-03	1.166982e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)	2.700000e-01	2.275988e-02	7.170220e+00
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)	1.500000e-01	8.385812e-03	7.766561e+00
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)	1.350000e+00	8.481183e-02	4.954091e+00
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)	4.000000e-02	1.430931e-03	1.587240e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)	3.600000e-01	1.958377e-02	1.182378e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)	6.000000e-02	2.444544e-03	1.466227e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)	5.400000e-01	2.764474e-02	9.216027e+00
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)	3.000000e-01	1.076791e-02	7.511775e+00
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)	2.700000e+00	1.151252e-01	5.133169e+00

number of batches used: 50	3.128374e-01	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh9_norm
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)   	2.000000e-02	1.774092e-02	2.908689e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)   	1.800000e-01	2.049296e-02	1.614440e+01
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)   	3.000000e-02	2.129193e-02	2.274438e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)   	2.700000e-01	1.641897e-02	1.496963e+01
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)   	1.500000e-01	1.377221e-02	1.535430e+01
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)   	1.350000e+00	1.343889e-02	1.021705e+01
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)   	4.000000e-02	1.065699e-02	2.672816e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)   	3.600000e-01	1.560994e-02	1.541254e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)   	6.000000e-02	1.246194e-02	2.347054e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)   	5.400000e-01	1.476345e-02	1.448405e+01
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)   	3.000000e-01	1.072110e-02	1.375848e+01
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)   	2.700000e+00	1.285866e-02	9.541922e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)   	2.000000e-02	4.327040e-02	1.822471e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)   	1.800000e-01	6.917430e-02	9.165983e+00
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)   	3.000000e-02	6.278842e-02	1.284409e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)   	2.700000e-01	6.787689e-02	8.745180e+00
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)   	1.500000e-01	4.213320e-02	9.460421e+00
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)   	1.350000e+00	4.938469e-02	5.988285e+00
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)   	4.000000e-02	2.511628e-02	1.812488e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)   	3.600000e-01	3.878941e-02	1.278745e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)   	6.000000e-02	2.828046e-02	1.739787e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)   	5.400000e-01	3.643052e-02	1.131499e+01
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)   	3.000000e-01	2.517194e-02	7.976263e+00
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)   	2.700000e+00	2.978032e-02	5.072241e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.1566, 0.5579, -0.9147)	2.000000e-02	6.101131e-02	1.325894e+01
	 (0,0,1)	 (-0.1321, 0.8465, -0.6260)	1.800000e-01	8.966726e-02	8.301713e+00
	 (0,1,0)	 (0.1180, 0.7122, -1.1075)	3.000000e-02	8.408035e-02	1.166982e+01
	 (0,1,1)	 (-0.1707, 1.0008, -0.8189)	2.700000e-01	8.429587e-02	7.170220e+00
	 (0,2,0)	 (-0.0209, 1.2676, -1.8019)	1.500000e-01	5.590541e-02	7.766561e+00
	 (0,2,1)	 (-0.3095, 1.5563, -1.5132)	1.350000e+00	6.282358e-02	4.954091e+00
	 (1,0,0)	 (1.3593, 1.3596, -0.5138)	4.000000e-02	3.577328e-02	1.587240e+01
	 (1,0,1)	 (1.0706, 1.6483, -0.2251)	3.600000e-01	5.439935e-02	1.182378e+01
	 (1,1,0)	 (1.3207, 1.5139, -0.7066)	6.000000e-02	4.074240e-02	1.466227e+01
	 (1,1,1)	 (1.0320, 1.8026, -0.4180)	5.400000e-01	5.119397e-02	9.216027e+00
	 (1,2,0)	 (1.1818, 2.0694, -1.4010)	3.000000e-01	3.589304e-02	7.511775e+00
	 (1,2,1)	 (0.8931, 2.3581, -1.1123)	2.700000e+00	4.263898e-02	5.133169e+00

number of batches used: 50	5.213957e-02	4.050336e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh10
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-66.6667, 0.0000, 0.0000)   	4.000000e+04	1.022103e+00	5.828595e+00
	 (1,0,0)	 (-0.0000, 0.0000, 0.0000)   	4.000000e+04	2.139798e+01	9.941980e-01
	 (2,0,0)	 (66.6667, 0.0000, 0.0000)   	4.000000e+04	5.722098e-01	6.992904e+00

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-66.6667, 0.0000, 0.0000)   	4.000000e+04	2.863082e-01	1.431960e+01
	 (1,0,0)	 (-0.0000, 0.0000, 0.0000)   	4.000000e+04	5.231304e+01	5.450380e-01
	 (2,0,0)	 (66.6667, 0.0000, 0.0000)   	4.000000e+04	1.740504e-01	2.281538e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-66.6667, 0.0000, 0.0000)	4.000000e+04	1.308411e+00	5.757636e+00
	 (1,0,0)	 (-0.0000, 0.0000, 0.0000)	4.000000e+04	7.371101e+01	4.697387e-01
	 (2,0,0)	 (66.6667, 0.0000, 0.0000)	4.000000e+04	7.462602e-01	7.926564e+00

number of batches used: 50	7.576569e+01	5.077725e-01



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : vol10
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Volume 	 num of volume : 3
	 Volume in cm3: 1.000000e+00
	 The result is integrated over the volume


	 SPECTRUM RESULTS
	 number of first discarded batches : 0

	 group			 score		 sigma_% 	 score/lethargy
Units:	 MeV			 phot.cm.s^-1	 %		 phot.cm.s^-1

0.000000e+00 - 1.000000e+00	2.300749e+01	1.013226e+00	2.300749e-34
1.000000e+00 - 2.000000e+01	5.294144e+01	6.055790e-01	1.767229e+01

	 ENERGY INTEGRATED RESULTS

	 number of first discarded batches : 0

number of batches used: 50	7.594892e+01	5.741635e-01




******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)   	1.000000e+00	1.750925e-02	1.073954e+01
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)   	1.000000e+00	1.926480e-02	9.363992e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)   	1.000000e+00	1.467639e-02	1.065213e+01
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)   	1.000000e+00	1.509037e-02	1.030406e+01
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)   	1.000000e+00	1.082683e-02	1.112783e+01
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)   	1.000000e+00	9.922436e-03	1.281470e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)   	1.000000e+00	5.378491e-02	5.193040e+00
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)   	1.000000e+00	5.763190e-02	4.263485e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)   	1.000000e+00	3.325676e-02	6.537223e+00
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)   	1.000000e+00	3.273674e-02	6.783554e+00
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)   	1.000000e+00	2.173995e-02	8.540800e+00
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)   	1.000000e+00	2.137240e-02	8.684120e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)	1.000000e+00	7.129415e-02	4.885158e+00
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)	1.000000e+00	7.689670e-02	4.224267e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)	1.000000e+00	4.793315e-02	5.679995e+00
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)	1.000000e+00	4.782711e-02	6.419868e+00
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)	1.000000e+00	3.256678e-02	7.036063e+00
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)	1.000000e+00	3.129483e-02	6.790425e+00

number of batches used: 50	3.078127e-01	3.935659e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11_norm
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)   	1.000000e+00	1.750925e-02	1.073954e+01
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)   	1.000000e+00	1.926480e-02	9.363992e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)   	1.000000e+00	1.467639e-02	1.065213e+01
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)   	1.000000e+00	1.509037e-02	1.030406e+01
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)   	1.000000e+00	1.082683e-02	1.112783e+01
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)   	1.000000e+00	9.922436e-03	1.281470e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)   	1.000000e+00	5.378491e-02	5.193040e+00
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)   	1.000000e+00	5.763190e-02	4.263485e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)   	1.000000e+00	3.325676e-02	6.537223e+00
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)   	1.000000e+00	3.273674e-02	6.783554e+00
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)   	1.000000e+00	2.173995e-02	8.540800e+00
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)   	1.000000e+00	2.137240e-02	8.684120e+00


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (0.6667, 0.6667, 0.5000)	1.000000e+00	7.129415e-02	4.885158e+00
	 (0,1,0)	 (0.3333, 1.3333, 0.5000)	1.000000e+00	7.689670e-02	4.224267e+00
	 (1,0,0)	 (1.6667, 0.6667, 0.5000)	1.000000e+00	4.793315e-02	5.679995e+00
	 (1,1,0)	 (1.3333, 1.3333, 0.5000)	1.000000e+00	4.782711e-02	6.419868e+00
	 (2,0,0)	 (2.6667, 0.6667, 0.5000)	1.000000e+00	3.256678e-02	7.036063e+00
	 (2,1,0)	 (2.3333, 1.3333, 0.5000)	1.000000e+00	3.129483e-02	6.790425e+00

number of batches used: 50	5.130212e-02	3.935659e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11.1
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.200000e-02	3.225466e-04	3.617305e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428572e-03	3.104121e-04	4.432005e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.200000e-02	3.506636e-04	4.453193e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428572e-03	2.142961e-04	5.112550e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.200000e-02	2.022451e-04	4.585473e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428571e-03	5.217255e-05	5.660908e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.200000e-02	3.112348e-04	4.954102e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428573e-03	2.178622e-04	4.564348e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.200000e-02	4.755207e-04	3.926478e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428573e-03	8.364093e-05	7.004311e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	3.000000e-02	3.709984e-04	4.575814e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285714e-02	1.715882e-04	4.278500e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	5.788212e-04	3.198679e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285715e-02	3.272633e-04	3.762969e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	3.000000e-02	3.124131e-04	4.799082e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285714e-02	2.968930e-04	5.038202e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.200000e-02	3.832580e-04	3.907522e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428572e-03	1.073188e-04	5.964417e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.200000e-02	3.815284e-04	3.735358e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428572e-03	3.117857e-04	3.982563e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.200000e-02	2.156490e-04	5.979685e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428571e-03	3.617746e-04	3.792996e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.200000e-02	1.248954e-04	5.307019e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428573e-03	1.508033e-04	5.218012e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.200000e-02	3.484060e-04	4.220416e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428573e-03	2.666898e-04	4.630070e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	3.000000e-02	3.103271e-04	3.990827e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285714e-02	2.995124e-04	5.012164e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	4.454421e-04	3.478414e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285715e-02	8.174028e-05	8.098106e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	3.000000e-02	3.401142e-04	5.135097e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285714e-02	1.747300e-04	4.996795e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200000e-02	2.728545e-04	4.589398e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428573e-03	9.372151e-05	5.630020e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200000e-02	3.262388e-04	3.807711e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428573e-03	1.724369e-04	5.529559e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200000e-02	1.359586e-04	7.180342e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428572e-03	1.588551e-04	5.914304e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200001e-02	1.556969e-04	7.540861e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428574e-03	1.272886e-04	5.657138e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200001e-02	1.320969e-04	4.312788e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428574e-03	3.905071e-05	7.648402e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000000e-02	6.258109e-04	3.090607e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285714e-02	1.528648e-04	6.537678e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000001e-02	2.880080e-04	3.627353e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285715e-02	9.934134e-05	8.998232e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000000e-02	2.117389e-04	4.398227e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285714e-02	1.217623e-04	6.201179e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.200000e-02	6.724840e-04	4.070791e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428571e-03	3.949797e-04	4.130223e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.200000e-02	4.447781e-04	4.543214e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428571e-03	4.277972e-05	7.243799e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199999e-02	1.330583e-04	7.234355e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428570e-03	1.061319e-04	7.209835e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.200000e-02	3.170467e-04	5.684565e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428572e-03	2.682201e-04	3.762962e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.200000e-02	3.220990e-04	3.655041e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428572e-03	2.195106e-04	4.754021e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999999e-02	2.384305e-04	5.759931e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285714e-02	6.866852e-05	1.000000e+02
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000000e-02	3.312523e-04	3.859416e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285715e-02	1.423619e-05	7.046482e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999999e-02	2.819860e-04	4.596550e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285714e-02	1.344588e-04	5.226729e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.200000e-02	2.288717e-04	4.491969e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428571e-03	1.956231e-04	4.428749e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.200000e-02	4.386464e-04	4.186218e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428571e-03	7.249010e-05	5.933830e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199999e-02	2.149002e-04	4.398073e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428570e-03	1.461553e-04	4.940522e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.200000e-02	4.932483e-04	3.602865e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428572e-03	3.046563e-04	4.070624e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.200000e-02	1.986853e-04	4.470807e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428572e-03	1.423262e-04	5.199149e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999999e-02	3.476883e-04	3.762835e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285714e-02	2.338415e-04	4.967802e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000000e-02	4.728825e-04	4.381844e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285715e-02	1.894241e-04	5.647274e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999999e-02	2.212863e-04	5.120111e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285714e-02	2.070175e-04	4.700642e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.200001e-02	1.579077e-04	4.712529e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428576e-03	1.123754e-04	7.042162e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.200001e-02	2.174682e-04	3.934846e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428576e-03	2.562393e-04	6.045265e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.200001e-02	4.819292e-04	3.419178e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428574e-03	1.649452e-04	5.306615e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.200001e-02	1.809712e-04	5.018849e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428577e-03	2.973376e-04	3.843780e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.200001e-02	4.186382e-04	5.354826e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428577e-03	2.050774e-04	5.349914e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	3.000000e-02	6.089101e-04	3.433412e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285715e-02	2.912442e-04	5.227367e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000002e-02	2.763149e-04	4.375521e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285715e-02	1.134582e-04	7.031223e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	3.000000e-02	3.499192e-04	4.431589e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285715e-02	1.077406e-04	6.087206e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	3.034036e-04	3.475371e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428567e-03	1.175150e-04	7.023487e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	3.879722e-04	3.568600e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428567e-03	7.159956e-05	5.771576e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199999e-02	2.474226e-04	4.314468e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428566e-03	4.498952e-05	5.572427e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	1.467975e-04	5.387191e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428568e-03	3.307589e-04	3.698916e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	1.306490e-04	6.070071e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428568e-03	1.979715e-04	4.802031e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	4.698242e-04	3.408565e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	1.203638e-04	6.220879e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	2.999999e-02	2.857507e-04	4.988764e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	1.263583e-04	5.687034e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	2.333870e-04	6.539304e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	8.088174e-05	8.082311e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700000e-02	1.529913e-03	2.598754e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	7.262721e-04	2.590681e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700000e-02	1.110634e-03	3.066883e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	4.721340e-04	3.227730e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699998e-02	1.115925e-03	2.782239e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.300000e-02	4.147783e-04	3.681481e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	8.548079e-04	3.046476e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300001e-02	3.384207e-04	4.269143e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	8.196356e-04	2.751395e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300001e-02	5.348072e-04	3.117559e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	1.495092e-03	2.515039e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	5.380117e-04	3.275659e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050000e-01	1.239039e-03	2.581697e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500001e-02	6.078904e-04	3.209491e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	8.644307e-04	3.181421e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	4.999188e-04	3.495240e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700000e-02	1.667557e-03	2.118043e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	6.013844e-04	3.457212e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700000e-02	1.171111e-03	2.380435e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	5.961761e-04	4.378290e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699998e-02	1.569532e-03	2.316671e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.300000e-02	3.481217e-04	3.977987e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	9.703476e-04	3.183683e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300001e-02	3.223066e-04	4.536350e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	4.049645e-04	4.159725e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300001e-02	3.936591e-04	4.380680e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	1.047455e-03	3.415442e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	8.451426e-04	3.641603e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050000e-01	8.841203e-04	3.105801e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500001e-02	5.997537e-04	3.647669e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	1.138960e-03	3.063658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	6.929329e-04	3.114409e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700000e-02	7.422970e-04	3.691217e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	2.381050e-04	4.494075e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700000e-02	8.495031e-04	3.033283e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	4.936694e-04	4.446661e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699998e-02	7.846737e-04	3.886316e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.300000e-02	2.776780e-04	3.923499e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	5.201710e-04	3.484225e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300001e-02	4.776983e-04	4.269698e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	6.842682e-04	3.537545e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300001e-02	4.557635e-04	3.919818e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.221400e-03	2.496657e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	2.960195e-04	5.228652e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050000e-01	1.481435e-03	2.480213e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500001e-02	2.055782e-04	5.207639e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	6.410204e-04	2.931283e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	3.796455e-04	3.661476e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700000e-02	5.265121e-04	3.765926e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	1.311645e-04	7.239601e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700000e-02	7.901570e-04	4.333065e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	6.256819e-05	1.000000e+02
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699998e-02	6.399515e-04	4.108902e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.300000e-02	2.472356e-04	4.840226e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	8.689368e-04	2.792007e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300001e-02	1.955957e-04	5.865157e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	9.931249e-04	2.900812e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300001e-02	3.864328e-04	3.618493e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	1.341832e-03	2.691435e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	5.038118e-04	3.775011e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050000e-01	8.102276e-04	3.836535e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500001e-02	4.514617e-04	4.697005e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	9.639995e-04	2.920104e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	5.513123e-04	3.247450e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.200000e-02	3.793872e-04	5.253220e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428572e-03	3.728509e-04	4.064264e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.200000e-02	5.452522e-04	4.423944e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428572e-03	2.899193e-04	4.416259e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.200000e-02	9.351510e-05	7.997083e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428571e-03	3.490100e-04	4.031380e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.200000e-02	6.195091e-04	3.179356e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428573e-03	3.525344e-04	3.552249e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.200000e-02	1.041124e-03	2.623770e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428573e-03	2.872861e-04	4.327676e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	3.000000e-02	8.551419e-04	3.088974e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285714e-02	3.182752e-04	4.440252e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	6.405968e-04	3.693787e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285715e-02	2.964844e-04	4.550164e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	3.000000e-02	6.247445e-04	3.637211e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285714e-02	2.955860e-04	4.075804e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.200000e-02	7.064044e-04	3.696337e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428572e-03	3.923266e-04	3.731428e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.200000e-02	5.318188e-04	4.128373e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428572e-03	2.507417e-04	4.635099e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.200000e-02	6.329868e-04	3.706094e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428571e-03	3.275642e-04	4.039488e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.200000e-02	5.458262e-04	3.348307e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428573e-03	5.849850e-04	3.579098e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.200000e-02	8.234525e-04	3.486695e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428573e-03	2.624996e-04	3.784411e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	3.000000e-02	9.755515e-04	3.372316e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285714e-02	3.860489e-04	3.831310e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	7.615134e-04	3.553133e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285715e-02	6.566411e-04	2.998546e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	3.000000e-02	1.040467e-03	3.269456e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285714e-02	3.263811e-04	4.532530e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200000e-02	9.653489e-04	3.383535e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428573e-03	1.488515e-04	5.157917e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200000e-02	4.358974e-04	4.080250e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428573e-03	3.348554e-04	3.821958e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200000e-02	5.657363e-04	3.810666e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428572e-03	3.636561e-04	4.795753e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200001e-02	6.436770e-04	4.057317e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428574e-03	4.310461e-04	4.227752e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200001e-02	7.486322e-04	3.771594e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428574e-03	1.731664e-04	5.122809e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000000e-02	6.022001e-04	3.974494e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285714e-02	3.863737e-04	4.364021e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000001e-02	5.906927e-04	4.017746e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285715e-02	6.041032e-04	3.284976e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000000e-02	8.663120e-04	3.598444e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285714e-02	3.898603e-04	3.646618e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.200000e-02	8.440479e-04	3.612282e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428571e-03	6.598490e-04	3.280412e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.200000e-02	9.856339e-04	3.245830e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428571e-03	1.802160e-04	6.084665e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199999e-02	4.009712e-04	4.650276e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428570e-03	4.930352e-04	3.580645e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.200000e-02	5.472258e-04	3.816239e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428572e-03	4.049282e-04	3.633119e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.200000e-02	7.275428e-04	3.219321e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428572e-03	4.722822e-04	4.279867e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999999e-02	1.127066e-03	3.484253e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285714e-02	4.175140e-04	3.909064e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000000e-02	8.677115e-04	3.020898e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285715e-02	2.385607e-04	5.861723e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999999e-02	6.040894e-04	4.042766e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285714e-02	1.804720e-04	5.148100e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.200000e-02	1.215350e-03	2.917574e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428571e-03	9.829085e-05	6.504888e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.200000e-02	3.730546e-04	4.707631e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428571e-03	3.736586e-04	3.857866e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199999e-02	5.339535e-04	3.343924e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428570e-03	5.978954e-04	3.675888e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.200000e-02	1.008333e-03	3.302162e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428572e-03	2.705266e-04	4.718757e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.200000e-02	5.639900e-04	3.574767e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428572e-03	6.030646e-04	3.559333e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999999e-02	9.601070e-04	3.011568e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285714e-02	7.084024e-04	2.927330e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000000e-02	1.305398e-03	2.582440e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285715e-02	3.616095e-04	4.343927e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999999e-02	8.116812e-04	3.208197e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285714e-02	3.615491e-04	4.710782e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.200001e-02	4.151236e-04	4.635193e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428576e-03	2.104868e-04	5.215173e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.200001e-02	2.805910e-04	5.212977e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428576e-03	3.719331e-04	3.729751e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.200001e-02	8.862198e-04	2.968932e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428574e-03	4.643361e-04	3.479581e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.200001e-02	7.326557e-04	3.188652e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428577e-03	3.860855e-04	4.049075e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.200001e-02	4.517506e-04	4.129811e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428577e-03	2.527172e-04	4.751101e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	3.000000e-02	7.403929e-04	3.998907e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285715e-02	1.080527e-04	5.196900e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000002e-02	4.582869e-04	4.271978e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285715e-02	3.344522e-04	4.368995e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	3.000000e-02	4.049335e-04	4.011145e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285715e-02	3.733509e-04	4.212680e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	5.505388e-04	3.558487e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428567e-03	2.989785e-04	4.723587e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	5.914074e-04	4.323888e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428567e-03	2.628755e-04	4.287711e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199999e-02	4.664218e-04	3.503775e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428566e-03	5.828830e-04	3.391626e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	8.871543e-04	3.461226e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428568e-03	2.967505e-04	3.740477e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	8.264430e-04	3.895742e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428568e-03	1.723683e-04	6.423370e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	4.864082e-04	4.289295e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	3.621926e-04	4.940336e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	2.999999e-02	4.424454e-04	4.175586e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	4.887344e-04	3.934400e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	5.599161e-04	3.905374e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	4.209173e-04	3.834941e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700000e-02	2.721213e-03	2.079543e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	2.056580e-03	2.057673e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700000e-02	2.754263e-03	2.325618e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	1.262031e-03	2.283922e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699998e-02	2.299164e-03	2.098855e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.300000e-02	1.177007e-03	2.308458e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	2.438346e-03	1.855081e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300001e-02	1.015933e-03	2.019785e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	2.032728e-03	1.865834e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300001e-02	1.351758e-03	2.049967e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	3.021712e-03	1.817959e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	2.005160e-03	2.073321e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050000e-01	3.405492e-03	1.886595e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500001e-02	1.766407e-03	1.630244e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	3.163943e-03	1.702606e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	8.952646e-04	2.778768e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700000e-02	2.039801e-03	2.040244e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	1.447567e-03	1.981223e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700000e-02	3.079102e-03	1.694010e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	1.026819e-03	3.098851e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699998e-02	1.944250e-03	2.188083e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.300000e-02	9.486789e-04	2.402941e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	1.714911e-03	2.112121e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300001e-02	1.302566e-03	1.980196e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	2.365307e-03	1.720463e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300001e-02	5.855701e-04	3.018060e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	2.012633e-03	2.496206e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	9.903391e-04	2.589989e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050000e-01	2.217690e-03	1.938009e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500001e-02	1.420068e-03	2.261760e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	3.254820e-03	1.607658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	9.434752e-04	2.774525e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700000e-02	2.664956e-03	2.000933e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	1.134735e-03	2.361661e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700000e-02	2.399470e-03	1.825632e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	1.009963e-03	2.631115e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699998e-02	2.076239e-03	2.033474e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.300000e-02	1.222666e-03	2.464897e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	1.786257e-03	2.485304e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300001e-02	6.747876e-04	2.971415e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	1.642649e-03	2.438403e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300001e-02	1.053470e-03	2.532010e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	2.083372e-03	2.232778e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	1.728840e-03	2.048711e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050000e-01	2.319633e-03	2.088301e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500001e-02	1.236848e-03	2.191365e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	2.174351e-03	2.015829e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	1.252552e-03	2.077378e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700000e-02	1.590691e-03	2.555205e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	7.147565e-04	3.210127e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700000e-02	1.583928e-03	2.748482e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	7.764484e-04	3.056098e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699998e-02	1.482351e-03	2.107219e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.300000e-02	1.054187e-03	2.412898e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	1.939904e-03	2.396729e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300001e-02	5.800435e-04	3.191541e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.259586e-03	2.434996e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300001e-02	8.797374e-04	2.136641e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	2.435435e-03	1.738522e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	1.287030e-03	2.297326e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050000e-01	2.750412e-03	1.671266e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500001e-02	9.016078e-04	2.345525e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	2.421677e-03	1.653891e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	1.348675e-03	2.426218e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)	2.200000e-02	7.019338e-04	3.811030e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)	9.428572e-03	6.832630e-04	2.929491e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)	2.200000e-02	8.959158e-04	3.461742e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)	9.428572e-03	5.042154e-04	3.356790e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)	2.200000e-02	2.957602e-04	3.997393e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)	9.428571e-03	4.011825e-04	3.518526e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)	2.200000e-02	9.307439e-04	2.512812e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)	9.428573e-03	5.703966e-04	2.693265e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)	2.200000e-02	1.516645e-03	2.294937e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)	9.428573e-03	3.709271e-04	3.607827e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)	3.000000e-02	1.226140e-03	2.465120e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)	1.285714e-02	4.898635e-04	3.145805e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)	3.000001e-02	1.219418e-03	2.401877e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)	1.285715e-02	6.237477e-04	2.749150e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)	3.000000e-02	9.371576e-04	2.851213e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)	1.285714e-02	5.924789e-04	3.080298e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)	2.200000e-02	1.089662e-03	2.925655e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)	9.428572e-03	4.996453e-04	3.088277e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)	2.200000e-02	9.133472e-04	2.687081e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)	9.428572e-03	5.625274e-04	2.865444e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)	2.200000e-02	8.486359e-04	3.029324e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)	9.428571e-03	6.893388e-04	2.712843e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)	2.200000e-02	6.707216e-04	2.800654e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)	9.428573e-03	7.357883e-04	2.928441e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)	2.200000e-02	1.171859e-03	2.712690e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)	9.428573e-03	5.291894e-04	2.837481e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)	3.000000e-02	1.285879e-03	2.715484e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)	1.285714e-02	6.855613e-04	3.087061e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)	3.000001e-02	1.206956e-03	2.652799e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)	1.285715e-02	7.383814e-04	2.773246e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)	3.000000e-02	1.380581e-03	2.629428e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)	1.285714e-02	5.011112e-04	3.289924e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)	2.200000e-02	1.238203e-03	2.698189e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)	9.428573e-03	2.425730e-04	3.712372e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)	2.200000e-02	7.621362e-04	2.876155e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)	9.428573e-03	5.072923e-04	3.335466e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)	2.200000e-02	7.016949e-04	3.276752e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)	9.428572e-03	5.225112e-04	3.675587e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)	2.200001e-02	7.993738e-04	3.491530e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)	9.428574e-03	5.583347e-04	3.551880e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)	2.200001e-02	8.807290e-04	3.405298e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)	9.428574e-03	2.122172e-04	4.340685e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)	3.000000e-02	1.228011e-03	2.511183e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)	1.285714e-02	5.392385e-04	4.472254e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)	3.000001e-02	8.787007e-04	3.214465e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)	1.285715e-02	7.034445e-04	3.353791e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)	3.000000e-02	1.078051e-03	3.035764e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)	1.285714e-02	5.116227e-04	3.727872e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)	2.200000e-02	1.516532e-03	2.536880e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)	9.428571e-03	1.054829e-03	2.376288e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)	2.200000e-02	1.430412e-03	2.496097e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)	9.428571e-03	2.229957e-04	5.047666e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)	2.199999e-02	5.340295e-04	3.831035e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)	9.428570e-03	5.991671e-04	3.324603e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)	2.200000e-02	8.642725e-04	3.232350e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)	9.428572e-03	6.731483e-04	2.610697e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)	2.200000e-02	1.049642e-03	2.658355e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)	9.428572e-03	6.917928e-04	3.566912e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)	2.999999e-02	1.365496e-03	3.257889e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)	1.285714e-02	4.861825e-04	3.573361e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)	3.000000e-02	1.198964e-03	2.965435e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)	1.285715e-02	2.527969e-04	5.526246e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)	2.999999e-02	8.860754e-04	3.478765e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)	1.285714e-02	3.149308e-04	3.697769e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)	2.200000e-02	1.444221e-03	2.538591e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)	9.428571e-03	2.939140e-04	3.537310e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)	2.200000e-02	8.117010e-04	3.069267e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)	9.428571e-03	4.461487e-04	3.394208e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)	2.199999e-02	7.488536e-04	2.765791e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)	9.428570e-03	7.440507e-04	3.198221e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)	2.200000e-02	1.501581e-03	2.411340e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)	9.428572e-03	5.751829e-04	3.397908e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)	2.200000e-02	7.626753e-04	2.935130e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)	9.428572e-03	7.453908e-04	3.280871e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)	2.999999e-02	1.307795e-03	2.350517e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)	1.285714e-02	9.422438e-04	2.728813e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)	3.000000e-02	1.778280e-03	2.520616e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)	1.285715e-02	5.510336e-04	3.312726e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)	2.999999e-02	1.032968e-03	2.875764e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)	1.285714e-02	5.685667e-04	3.310242e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)	2.200001e-02	5.730313e-04	3.485258e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)	9.428576e-03	3.228622e-04	4.079405e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)	2.200001e-02	4.980592e-04	3.251574e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)	9.428576e-03	6.281724e-04	3.157819e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)	2.200001e-02	1.368149e-03	2.111895e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)	9.428574e-03	6.292813e-04	2.781636e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)	2.200001e-02	9.136269e-04	2.658837e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)	9.428577e-03	6.834231e-04	3.092185e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)	2.200001e-02	8.703887e-04	3.212783e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)	9.428577e-03	4.577946e-04	3.407808e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)	3.000000e-02	1.349303e-03	2.490963e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)	1.285715e-02	3.992969e-04	3.963530e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)	3.000002e-02	7.346018e-04	2.975520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)	1.285715e-02	4.479104e-04	3.637258e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)	3.000000e-02	7.548527e-04	2.799137e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)	1.285715e-02	4.810915e-04	3.440496e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)	2.199999e-02	8.539424e-04	2.419289e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)	9.428567e-03	4.164934e-04	3.820737e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)	2.199999e-02	9.793797e-04	2.799911e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)	9.428567e-03	3.344750e-04	3.492235e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)	2.199999e-02	7.138444e-04	2.628499e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)	9.428566e-03	6.278725e-04	3.218399e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)	2.199999e-02	1.033952e-03	2.993575e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)	9.428568e-03	6.275095e-04	2.774062e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)	2.199999e-02	9.570919e-04	3.394352e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)	9.428568e-03	3.703398e-04	3.958061e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)	2.999998e-02	9.562324e-04	2.607352e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)	1.285713e-02	4.825564e-04	4.541647e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)	2.999999e-02	7.281961e-04	3.199825e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)	1.285714e-02	6.150926e-04	3.364403e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)	2.999998e-02	7.933031e-04	3.328183e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)	1.285713e-02	5.017991e-04	3.390154e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)	7.700000e-02	4.251126e-03	1.827077e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)	3.300000e-02	2.782852e-03	1.701871e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)	7.700000e-02	3.864897e-03	1.853236e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)	3.300000e-02	1.734165e-03	1.700961e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)	7.699998e-02	3.415089e-03	1.648371e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)	3.300000e-02	1.591785e-03	1.921661e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)	7.700001e-02	3.293154e-03	1.596589e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)	3.300001e-02	1.354354e-03	1.644011e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)	7.700001e-02	2.852364e-03	1.571765e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)	3.300001e-02	1.886565e-03	1.690459e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)	1.050000e-01	4.516804e-03	1.712823e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)	4.499999e-02	2.543172e-03	1.760660e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)	1.050000e-01	4.644531e-03	1.576799e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)	4.500001e-02	2.374297e-03	1.468623e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)	1.050000e-01	4.028374e-03	1.393376e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)	4.499999e-02	1.395183e-03	2.062348e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)	7.700000e-02	3.707358e-03	1.468222e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)	3.300000e-02	2.048952e-03	1.812821e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)	7.700000e-02	4.250214e-03	1.275647e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)	3.300000e-02	1.622995e-03	2.364726e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)	7.699998e-02	3.513782e-03	1.700193e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)	3.300000e-02	1.296801e-03	2.177296e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)	7.700001e-02	2.685258e-03	1.792084e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)	3.300001e-02	1.624873e-03	1.936937e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)	7.700001e-02	2.770272e-03	1.634813e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)	3.300001e-02	9.792292e-04	2.318915e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)	1.050000e-01	3.060089e-03	2.010487e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)	4.499999e-02	1.835482e-03	2.006298e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)	1.050000e-01	3.101810e-03	1.591733e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)	4.500001e-02	2.019821e-03	1.750121e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)	1.050000e-01	4.393780e-03	1.345880e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)	4.499999e-02	1.636408e-03	1.922996e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)	7.700000e-02	3.407253e-03	1.741765e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)	3.300000e-02	1.372840e-03	2.033251e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)	7.700000e-02	3.248973e-03	1.468493e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)	3.300000e-02	1.503632e-03	2.432258e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)	7.699998e-02	2.860913e-03	1.775665e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)	3.300000e-02	1.500344e-03	2.218969e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)	7.700001e-02	2.306428e-03	2.047046e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)	3.300001e-02	1.152486e-03	2.462349e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)	7.700001e-02	2.326917e-03	2.182929e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)	3.300001e-02	1.509233e-03	2.360243e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)	1.050000e-01	3.304772e-03	1.810748e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)	4.499999e-02	2.024859e-03	1.882671e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)	1.050000e-01	3.801068e-03	1.553997e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)	4.500001e-02	1.442426e-03	2.159771e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)	1.050000e-01	2.815372e-03	1.541747e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)	4.499999e-02	1.632198e-03	1.846952e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)	7.700000e-02	2.117203e-03	1.995610e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)	3.300000e-02	8.459210e-04	2.912318e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)	7.700000e-02	2.374085e-03	2.151152e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)	3.300000e-02	8.390165e-04	2.876304e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)	7.699998e-02	2.122303e-03	1.890128e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)	3.300000e-02	1.301422e-03	2.386451e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)	7.700001e-02	2.808841e-03	1.931230e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)	3.300001e-02	7.756392e-04	2.895671e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)	7.700001e-02	2.252711e-03	1.853566e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)	3.300001e-02	1.266170e-03	1.915776e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)	1.050000e-01	3.777268e-03	1.544692e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)	4.499999e-02	1.790842e-03	1.895238e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)	1.050000e-01	3.560639e-03	1.782824e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)	4.500001e-02	1.353070e-03	2.090744e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)	1.050000e-01	3.385676e-03	1.488840e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)	4.499999e-02	1.899987e-03	2.137258e+01

number of batches used: 50	2.420892e-01	2.895010e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11.2
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.199999e-02	3.225465e-04	3.617305e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428566e-03	3.104120e-04	4.432007e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.199999e-02	3.506635e-04	4.453195e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428566e-03	2.142961e-04	5.112549e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.199997e-02	2.022447e-04	4.585475e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428557e-03	5.217234e-05	5.660912e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.199999e-02	3.112346e-04	4.954103e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428566e-03	2.178622e-04	4.564348e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.199999e-02	4.755203e-04	3.926477e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428566e-03	8.364096e-05	7.004311e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	2.999998e-02	3.709986e-04	4.575814e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285713e-02	1.715874e-04	4.278508e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	5.788210e-04	3.198680e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285714e-02	3.272633e-04	3.762969e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	2.999998e-02	3.124131e-04	4.799082e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285713e-02	2.968926e-04	5.038201e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.199999e-02	3.832580e-04	3.907523e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428566e-03	1.073184e-04	5.964442e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.199999e-02	3.815283e-04	3.735359e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428566e-03	3.117856e-04	3.982563e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.199997e-02	2.156486e-04	5.979688e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428557e-03	3.617741e-04	3.792996e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.199999e-02	1.248954e-04	5.307021e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428566e-03	1.508032e-04	5.218015e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.199999e-02	3.484065e-04	4.220410e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428566e-03	2.666896e-04	4.630073e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	2.999998e-02	3.103267e-04	3.990832e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285713e-02	2.995129e-04	5.012156e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	4.454425e-04	3.478414e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285714e-02	8.174034e-05	8.098104e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	2.999998e-02	3.401140e-04	5.135100e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285713e-02	1.747301e-04	4.996798e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200007e-02	2.728550e-04	4.589396e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428598e-03	9.372221e-05	5.630015e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200007e-02	3.262397e-04	3.807709e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428598e-03	1.724371e-04	5.529557e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200004e-02	1.359590e-04	7.180346e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428588e-03	1.588552e-04	5.914299e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200007e-02	1.556969e-04	7.540861e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428598e-03	1.272889e-04	5.657132e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200007e-02	1.320974e-04	4.312786e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428598e-03	3.905122e-05	7.648363e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000008e-02	6.258124e-04	3.090605e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285718e-02	1.528649e-04	6.537675e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000011e-02	2.880093e-04	3.627351e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285719e-02	9.934154e-05	8.998215e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000008e-02	2.117395e-04	4.398225e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285718e-02	1.217625e-04	6.201182e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.199999e-02	6.724843e-04	4.070789e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428566e-03	3.949800e-04	4.130218e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.199999e-02	4.447780e-04	4.543216e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428566e-03	4.277972e-05	7.243796e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199997e-02	1.330582e-04	7.234356e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428557e-03	1.061320e-04	7.209831e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.199999e-02	3.170473e-04	5.684558e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428566e-03	2.682203e-04	3.762962e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.199999e-02	3.220984e-04	3.655043e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428566e-03	2.195103e-04	4.754023e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999998e-02	2.384300e-04	5.759936e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285713e-02	6.866867e-05	1.000000e+02
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000001e-02	3.312516e-04	3.859418e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285714e-02	1.423611e-05	7.046496e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999998e-02	2.819859e-04	4.596552e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285713e-02	1.344587e-04	5.226729e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.199999e-02	2.288716e-04	4.491969e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428566e-03	1.956225e-04	4.428747e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.199999e-02	4.386463e-04	4.186219e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428566e-03	7.249012e-05	5.933831e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199997e-02	2.149005e-04	4.398069e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428557e-03	1.461551e-04	4.940526e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.199999e-02	4.932480e-04	3.602865e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428566e-03	3.046562e-04	4.070625e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.199999e-02	1.986853e-04	4.470804e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428566e-03	1.423262e-04	5.199147e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999998e-02	3.476892e-04	3.762831e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285713e-02	2.338413e-04	4.967805e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000001e-02	4.728828e-04	4.381843e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285714e-02	1.894241e-04	5.647274e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999998e-02	2.212863e-04	5.120111e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285713e-02	2.070177e-04	4.700643e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.199999e-02	1.579076e-04	4.712528e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428566e-03	1.123754e-04	7.042162e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.199999e-02	2.174681e-04	3.934845e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428566e-03	2.562393e-04	6.045265e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.199997e-02	4.819285e-04	3.419177e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428557e-03	1.649449e-04	5.306618e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.199999e-02	1.809709e-04	5.018856e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428566e-03	2.973371e-04	3.843781e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.199999e-02	4.186379e-04	5.354828e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428566e-03	2.050774e-04	5.349915e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	2.999998e-02	6.089096e-04	3.433411e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285713e-02	2.912440e-04	5.227367e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000001e-02	2.763147e-04	4.375520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285714e-02	1.134582e-04	7.031229e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	2.999998e-02	3.499192e-04	4.431589e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285713e-02	1.077403e-04	6.087208e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	3.034037e-04	3.475370e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428566e-03	1.175150e-04	7.023487e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	3.879723e-04	3.568600e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428566e-03	7.159954e-05	5.771575e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199997e-02	2.474225e-04	4.314468e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428557e-03	4.498930e-05	5.572440e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	1.467976e-04	5.387189e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428566e-03	3.307589e-04	3.698917e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	1.306489e-04	6.070072e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428566e-03	1.979717e-04	4.802029e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	4.698241e-04	3.408565e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	1.203638e-04	6.220882e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	3.000001e-02	2.857509e-04	4.988763e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	1.263583e-04	5.687034e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	2.333870e-04	6.539305e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	8.088170e-05	8.082314e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700001e-02	1.529913e-03	2.598754e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	7.262721e-04	2.590681e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700001e-02	1.110634e-03	3.066883e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	4.721340e-04	3.227731e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699993e-02	1.115924e-03	2.782240e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.299996e-02	4.147778e-04	3.681484e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	8.548080e-04	3.046476e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300000e-02	3.384204e-04	4.269143e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	8.196353e-04	2.751395e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300000e-02	5.348072e-04	3.117560e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	1.495093e-03	2.515039e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	5.380116e-04	3.275659e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050001e-01	1.239039e-03	2.581697e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500002e-02	6.078906e-04	3.209491e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	8.644307e-04	3.181421e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	4.999187e-04	3.495240e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700001e-02	1.667557e-03	2.118043e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	6.013843e-04	3.457212e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700001e-02	1.171112e-03	2.380435e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	5.961760e-04	4.378290e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699993e-02	1.569531e-03	2.316671e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.299996e-02	3.481212e-04	3.977989e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	9.703482e-04	3.183682e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300000e-02	3.223066e-04	4.536348e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	4.049644e-04	4.159724e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300000e-02	3.936591e-04	4.380681e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	1.047456e-03	3.415442e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	8.451424e-04	3.641604e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050001e-01	8.841208e-04	3.105801e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500002e-02	5.997538e-04	3.647668e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	1.138960e-03	3.063658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	6.929328e-04	3.114409e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700001e-02	7.422972e-04	3.691217e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	2.381049e-04	4.494075e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700001e-02	8.495035e-04	3.033282e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	4.936693e-04	4.446662e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699993e-02	7.846732e-04	3.886317e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.299996e-02	2.776776e-04	3.923503e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	5.201711e-04	3.484224e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300000e-02	4.776982e-04	4.269699e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	6.842683e-04	3.537545e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300000e-02	4.557635e-04	3.919818e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.221400e-03	2.496657e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	2.960197e-04	5.228651e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050001e-01	1.481436e-03	2.480213e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500002e-02	2.055782e-04	5.207639e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	6.410205e-04	2.931283e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	3.796454e-04	3.661476e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700001e-02	5.265122e-04	3.765926e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	1.311644e-04	7.239601e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700001e-02	7.901570e-04	4.333065e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	6.256819e-05	1.000000e+02
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699993e-02	6.399512e-04	4.108903e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.299996e-02	2.472353e-04	4.840227e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	8.689366e-04	2.792008e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300000e-02	1.955958e-04	5.865156e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	9.931251e-04	2.900813e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300000e-02	3.864326e-04	3.618493e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	1.341833e-03	2.691435e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	5.038118e-04	3.775011e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050001e-01	8.102281e-04	3.836535e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500002e-02	4.514618e-04	4.697005e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	9.639996e-04	2.920104e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	5.513122e-04	3.247450e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.199999e-02	3.793873e-04	5.253219e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428566e-03	3.728507e-04	4.064265e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.199999e-02	5.452518e-04	4.423946e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428566e-03	2.899192e-04	4.416260e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.199997e-02	9.351494e-05	7.997092e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428557e-03	3.490096e-04	4.031381e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.199999e-02	6.195078e-04	3.179358e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428566e-03	3.525342e-04	3.552252e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.199999e-02	1.041124e-03	2.623770e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428566e-03	2.872859e-04	4.327676e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	2.999998e-02	8.551415e-04	3.088975e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285713e-02	3.182748e-04	4.440252e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	6.405972e-04	3.693786e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285714e-02	2.964842e-04	4.550168e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	2.999998e-02	6.247442e-04	3.637212e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285713e-02	2.955859e-04	4.075804e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.199999e-02	7.064046e-04	3.696337e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428566e-03	3.923268e-04	3.731427e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.199999e-02	5.318195e-04	4.128370e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428566e-03	2.507408e-04	4.635110e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.199997e-02	6.329854e-04	3.706094e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428557e-03	3.275638e-04	4.039490e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.199999e-02	5.458261e-04	3.348307e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428566e-03	5.849842e-04	3.579098e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.199999e-02	8.234504e-04	3.486699e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428566e-03	2.624989e-04	3.784411e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	2.999998e-02	9.755525e-04	3.372315e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285713e-02	3.860480e-04	3.831310e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	7.615137e-04	3.553133e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285714e-02	6.566394e-04	2.998547e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	2.999998e-02	1.040467e-03	3.269455e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285713e-02	3.263810e-04	4.532531e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200007e-02	9.653490e-04	3.383535e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428598e-03	1.488516e-04	5.157916e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200007e-02	4.359086e-04	4.080241e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428598e-03	3.348563e-04	3.821951e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200004e-02	5.657489e-04	3.810570e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428588e-03	3.636558e-04	4.795753e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200007e-02	6.436890e-04	4.057252e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428598e-03	4.310469e-04	4.227742e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200007e-02	7.486344e-04	3.771587e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428598e-03	1.731676e-04	5.122783e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000008e-02	6.022003e-04	3.974493e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285718e-02	3.863746e-04	4.364013e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000011e-02	5.906930e-04	4.017745e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285719e-02	6.041054e-04	3.284967e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000008e-02	8.663121e-04	3.598444e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285718e-02	3.898603e-04	3.646618e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.199999e-02	8.440498e-04	3.612274e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428566e-03	6.598489e-04	3.280412e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.199999e-02	9.856230e-04	3.245849e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428566e-03	1.802159e-04	6.084665e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199997e-02	4.009608e-04	4.650334e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428557e-03	4.930348e-04	3.580646e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.199999e-02	5.472166e-04	3.816293e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428566e-03	4.049281e-04	3.633119e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.199999e-02	7.275428e-04	3.219321e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428566e-03	4.722822e-04	4.279867e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999998e-02	1.127066e-03	3.484253e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285713e-02	4.175138e-04	3.909065e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000001e-02	8.677119e-04	3.020897e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285714e-02	2.385646e-04	5.861737e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999998e-02	6.040894e-04	4.042766e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285713e-02	1.804740e-04	5.148077e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.199999e-02	1.215349e-03	2.917576e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428566e-03	9.829079e-05	6.504889e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.199999e-02	3.730551e-04	4.707628e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428566e-03	3.736594e-04	3.857863e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199997e-02	5.339522e-04	3.343934e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428557e-03	5.978948e-04	3.675890e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.199999e-02	1.008332e-03	3.302165e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428566e-03	2.705265e-04	4.718758e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.199999e-02	5.639909e-04	3.574763e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428566e-03	6.030644e-04	3.559333e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999998e-02	9.601074e-04	3.011570e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285713e-02	7.084024e-04	2.927330e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000001e-02	1.305399e-03	2.582439e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285714e-02	3.616057e-04	4.343941e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999998e-02	8.116819e-04	3.208195e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285713e-02	3.615471e-04	4.710783e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.199999e-02	4.151231e-04	4.635190e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428566e-03	2.104868e-04	5.215172e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.199999e-02	2.805907e-04	5.212981e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428566e-03	3.719326e-04	3.729752e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.199997e-02	8.862181e-04	2.968933e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428557e-03	4.643358e-04	3.479582e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.199999e-02	7.326556e-04	3.188649e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428566e-03	3.860854e-04	4.049075e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.199999e-02	4.517501e-04	4.129812e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428566e-03	2.527171e-04	4.751099e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	2.999998e-02	7.403924e-04	3.998905e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285713e-02	1.080527e-04	5.196898e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000001e-02	4.582866e-04	4.271979e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285714e-02	3.344522e-04	4.368994e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	2.999998e-02	4.049329e-04	4.011144e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285713e-02	3.733508e-04	4.212680e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	5.505389e-04	3.558487e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428566e-03	2.989784e-04	4.723587e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	5.914074e-04	4.323889e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428566e-03	2.628756e-04	4.287711e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199997e-02	4.664214e-04	3.503776e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428557e-03	5.828825e-04	3.391627e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	8.871544e-04	3.461225e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428566e-03	2.967505e-04	3.740477e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	8.264431e-04	3.895742e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428566e-03	1.723685e-04	6.423371e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	4.864084e-04	4.289294e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	3.621924e-04	4.940337e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	3.000001e-02	4.424456e-04	4.175585e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	4.887345e-04	3.934400e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	5.599162e-04	3.905374e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	4.209173e-04	3.834941e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700001e-02	2.721214e-03	2.079543e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	2.056580e-03	2.057673e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700001e-02	2.754263e-03	2.325617e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	1.262031e-03	2.283922e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699993e-02	2.299162e-03	2.098856e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.299996e-02	1.177006e-03	2.308458e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	2.438347e-03	1.855081e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300000e-02	1.015933e-03	2.019785e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	2.032729e-03	1.865835e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300000e-02	1.351758e-03	2.049968e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	3.021712e-03	1.817959e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	2.005159e-03	2.073320e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050001e-01	3.405494e-03	1.886595e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500002e-02	1.766407e-03	1.630244e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	3.163943e-03	1.702606e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	8.952644e-04	2.778768e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700001e-02	2.039802e-03	2.040244e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	1.447567e-03	1.981223e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700001e-02	3.079103e-03	1.694010e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	1.026819e-03	3.098851e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699993e-02	1.944248e-03	2.188084e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.299996e-02	9.486778e-04	2.402943e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	1.714910e-03	2.112121e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300000e-02	1.302566e-03	1.980195e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	2.365308e-03	1.720462e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300000e-02	5.855701e-04	3.018061e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	2.012634e-03	2.496206e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	9.903386e-04	2.589989e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050001e-01	2.217691e-03	1.938009e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500002e-02	1.420068e-03	2.261760e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	3.254820e-03	1.607658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	9.434750e-04	2.774525e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700001e-02	2.664956e-03	2.000933e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	1.134735e-03	2.361661e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700001e-02	2.399470e-03	1.825632e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	1.009963e-03	2.631115e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699993e-02	2.076238e-03	2.033474e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.299996e-02	1.222665e-03	2.464898e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	1.786257e-03	2.485303e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300000e-02	6.747874e-04	2.971415e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	1.642649e-03	2.438404e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300000e-02	1.053470e-03	2.532009e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	2.083373e-03	2.232778e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	1.728839e-03	2.048711e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050001e-01	2.319634e-03	2.088301e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500002e-02	1.236848e-03	2.191364e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	2.174352e-03	2.015829e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	1.252552e-03	2.077378e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700001e-02	1.590691e-03	2.555205e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	7.147567e-04	3.210127e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700001e-02	1.583929e-03	2.748482e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	7.764482e-04	3.056098e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699993e-02	1.482350e-03	2.107219e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.299996e-02	1.054186e-03	2.412899e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	1.939904e-03	2.396728e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300000e-02	5.800434e-04	3.191541e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.259587e-03	2.434996e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300000e-02	8.797371e-04	2.136640e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	2.435435e-03	1.738522e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	1.287030e-03	2.297326e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050001e-01	2.750413e-03	1.671266e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500002e-02	9.016081e-04	2.345525e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	2.421677e-03	1.653891e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	1.348675e-03	2.426218e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)	2.199999e-02	7.019338e-04	3.811030e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)	9.428566e-03	6.832627e-04	2.929492e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)	2.199999e-02	8.959153e-04	3.461742e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)	9.428566e-03	5.042153e-04	3.356790e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)	2.199997e-02	2.957597e-04	3.997396e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)	9.428557e-03	4.011820e-04	3.518528e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)	2.199999e-02	9.307424e-04	2.512814e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)	9.428566e-03	5.703964e-04	2.693267e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)	2.199999e-02	1.516644e-03	2.294936e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)	9.428566e-03	3.709268e-04	3.607827e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)	2.999998e-02	1.226140e-03	2.465120e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)	1.285713e-02	4.898623e-04	3.145808e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)	3.000001e-02	1.219418e-03	2.401877e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)	1.285714e-02	6.237475e-04	2.749151e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)	2.999998e-02	9.371573e-04	2.851214e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)	1.285713e-02	5.924785e-04	3.080298e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)	2.199999e-02	1.089663e-03	2.925655e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)	9.428566e-03	4.996452e-04	3.088279e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)	2.199999e-02	9.133478e-04	2.687080e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)	9.428566e-03	5.625264e-04	2.865448e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)	2.199997e-02	8.486340e-04	3.029325e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)	9.428557e-03	6.893379e-04	2.712844e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)	2.199999e-02	6.707215e-04	2.800654e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)	9.428566e-03	7.357874e-04	2.928441e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)	2.199999e-02	1.171857e-03	2.712691e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)	9.428566e-03	5.291885e-04	2.837483e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)	2.999998e-02	1.285879e-03	2.715485e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)	1.285713e-02	6.855610e-04	3.087059e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)	3.000001e-02	1.206956e-03	2.652799e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)	1.285714e-02	7.383797e-04	2.773246e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)	2.999998e-02	1.380581e-03	2.629428e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)	1.285713e-02	5.011111e-04	3.289925e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)	2.200007e-02	1.238204e-03	2.698188e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)	9.428598e-03	2.425738e-04	3.712368e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)	2.200007e-02	7.621483e-04	2.876152e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)	9.428598e-03	5.072934e-04	3.335461e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)	2.200004e-02	7.017079e-04	3.276683e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)	9.428588e-03	5.225110e-04	3.675585e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)	2.200007e-02	7.993858e-04	3.491484e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)	9.428598e-03	5.583358e-04	3.551872e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)	2.200007e-02	8.807318e-04	3.405292e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)	9.428598e-03	2.122188e-04	4.340659e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)	3.000008e-02	1.228013e-03	2.511182e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)	1.285718e-02	5.392395e-04	4.472247e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)	3.000011e-02	8.787023e-04	3.214464e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)	1.285719e-02	7.034470e-04	3.353782e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)	3.000008e-02	1.078052e-03	3.035763e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)	1.285718e-02	5.116228e-04	3.727873e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)	2.199999e-02	1.516534e-03	2.536876e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)	9.428566e-03	1.054829e-03	2.376286e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)	2.199999e-02	1.430401e-03	2.496108e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)	9.428566e-03	2.229956e-04	5.047666e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)	2.199997e-02	5.340190e-04	3.831070e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)	9.428557e-03	5.991668e-04	3.324604e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)	2.199999e-02	8.642639e-04	3.232347e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)	9.428566e-03	6.731484e-04	2.610697e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)	2.199999e-02	1.049641e-03	2.658356e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)	9.428566e-03	6.917925e-04	3.566913e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)	2.999998e-02	1.365496e-03	3.257889e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)	1.285713e-02	4.861825e-04	3.573361e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)	3.000001e-02	1.198964e-03	2.965435e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)	1.285714e-02	2.528007e-04	5.526265e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)	2.999998e-02	8.860753e-04	3.478765e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)	1.285713e-02	3.149328e-04	3.697760e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)	2.199999e-02	1.444220e-03	2.538593e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)	9.428566e-03	2.939133e-04	3.537310e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)	2.199999e-02	8.117014e-04	3.069267e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)	9.428566e-03	4.461495e-04	3.394206e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)	2.199997e-02	7.488527e-04	2.765796e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)	9.428557e-03	7.440500e-04	3.198223e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)	2.199999e-02	1.501580e-03	2.411342e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)	9.428566e-03	5.751827e-04	3.397909e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)	2.199999e-02	7.626763e-04	2.935126e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)	9.428566e-03	7.453906e-04	3.280871e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)	2.999998e-02	1.307797e-03	2.350517e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)	1.285713e-02	9.422437e-04	2.728813e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)	3.000001e-02	1.778282e-03	2.520615e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)	1.285714e-02	5.510298e-04	3.312732e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)	2.999998e-02	1.032968e-03	2.875762e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)	1.285713e-02	5.685648e-04	3.310240e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)	2.199999e-02	5.730307e-04	3.485256e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)	9.428566e-03	3.228622e-04	4.079405e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)	2.199999e-02	4.980588e-04	3.251575e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)	9.428566e-03	6.281719e-04	3.157820e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)	2.199997e-02	1.368147e-03	2.111895e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)	9.428557e-03	6.292806e-04	2.781637e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)	2.199999e-02	9.136264e-04	2.658835e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)	9.428566e-03	6.834226e-04	3.092186e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)	2.199999e-02	8.703880e-04	3.212784e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)	9.428566e-03	4.577945e-04	3.407808e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)	2.999998e-02	1.349302e-03	2.490962e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)	1.285713e-02	3.992967e-04	3.963530e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)	3.000001e-02	7.346013e-04	2.975520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)	1.285714e-02	4.479104e-04	3.637259e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)	2.999998e-02	7.548520e-04	2.799137e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)	1.285713e-02	4.810911e-04	3.440497e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)	2.199999e-02	8.539426e-04	2.419289e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)	9.428566e-03	4.164934e-04	3.820737e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)	2.199999e-02	9.793797e-04	2.799911e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)	9.428566e-03	3.344751e-04	3.492235e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)	2.199997e-02	7.138439e-04	2.628499e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)	9.428557e-03	6.278718e-04	3.218400e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)	2.199999e-02	1.033952e-03	2.993575e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)	9.428566e-03	6.275094e-04	2.774062e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)	2.199999e-02	9.570920e-04	3.394352e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)	9.428566e-03	3.703402e-04	3.958061e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)	2.999998e-02	9.562325e-04	2.607352e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)	1.285713e-02	4.825562e-04	4.541649e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)	3.000001e-02	7.281966e-04	3.199824e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)	1.285714e-02	6.150928e-04	3.364403e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)	2.999998e-02	7.933032e-04	3.328183e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)	1.285713e-02	5.017990e-04	3.390155e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)	7.700001e-02	4.251127e-03	1.827077e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)	3.300000e-02	2.782852e-03	1.701870e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)	7.700001e-02	3.864898e-03	1.853236e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)	3.300000e-02	1.734165e-03	1.700961e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)	7.699993e-02	3.415087e-03	1.648371e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)	3.299996e-02	1.591784e-03	1.921662e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)	7.700001e-02	3.293155e-03	1.596589e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)	3.300000e-02	1.354353e-03	1.644011e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)	7.700001e-02	2.852364e-03	1.571765e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)	3.300000e-02	1.886565e-03	1.690459e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)	1.050000e-01	4.516805e-03	1.712823e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)	4.499999e-02	2.543171e-03	1.760660e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)	1.050001e-01	4.644533e-03	1.576799e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)	4.500002e-02	2.374298e-03	1.468623e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)	1.050000e-01	4.028374e-03	1.393376e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)	4.499999e-02	1.395183e-03	2.062348e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)	7.700001e-02	3.707359e-03	1.468222e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)	3.300000e-02	2.048951e-03	1.812821e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)	7.700001e-02	4.250214e-03	1.275646e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)	3.300000e-02	1.622994e-03	2.364726e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)	7.699993e-02	3.513780e-03	1.700194e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)	3.299996e-02	1.296799e-03	2.177297e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)	7.700001e-02	2.685258e-03	1.792084e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)	3.300000e-02	1.624873e-03	1.936937e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)	7.700001e-02	2.770272e-03	1.634812e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)	3.300000e-02	9.792292e-04	2.318916e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)	1.050000e-01	3.060089e-03	2.010486e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)	4.499999e-02	1.835481e-03	2.006298e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)	1.050001e-01	3.101812e-03	1.591733e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)	4.500002e-02	2.019822e-03	1.750121e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)	1.050000e-01	4.393780e-03	1.345880e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)	4.499999e-02	1.636408e-03	1.922996e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)	7.700001e-02	3.407254e-03	1.741765e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)	3.300000e-02	1.372840e-03	2.033251e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)	7.700001e-02	3.248974e-03	1.468492e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)	3.300000e-02	1.503632e-03	2.432258e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)	7.699993e-02	2.860911e-03	1.775666e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)	3.299996e-02	1.500343e-03	2.218970e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)	7.700001e-02	2.306429e-03	2.047045e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)	3.300000e-02	1.152486e-03	2.462350e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)	7.700001e-02	2.326917e-03	2.182929e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)	3.300000e-02	1.509233e-03	2.360243e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)	1.050000e-01	3.304772e-03	1.810748e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)	4.499999e-02	2.024859e-03	1.882671e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)	1.050001e-01	3.801069e-03	1.553997e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)	4.500002e-02	1.442426e-03	2.159771e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)	1.050000e-01	2.815372e-03	1.541747e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)	4.499999e-02	1.632197e-03	1.846952e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)	7.700001e-02	2.117203e-03	1.995610e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)	3.300000e-02	8.459211e-04	2.912318e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)	7.700001e-02	2.374086e-03	2.151152e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)	3.300000e-02	8.390164e-04	2.876304e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)	7.699993e-02	2.122301e-03	1.890128e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)	3.299996e-02	1.301421e-03	2.386451e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)	7.700001e-02	2.808840e-03	1.931230e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)	3.300000e-02	7.756392e-04	2.895670e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)	7.700001e-02	2.252712e-03	1.853566e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)	3.300000e-02	1.266170e-03	1.915776e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)	1.050000e-01	3.777268e-03	1.544691e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)	4.499999e-02	1.790841e-03	1.895238e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)	1.050001e-01	3.560641e-03	1.782824e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)	4.500002e-02	1.353070e-03	2.090744e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)	1.050000e-01	3.385677e-03	1.488840e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)	4.499999e-02	1.899987e-03	2.137258e+01

number of batches used: 50	2.420892e-01	2.895010e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11.1
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.200000e-02	1.466121e-02	3.617305e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428572e-03	3.292250e-02	4.432005e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.200000e-02	1.593925e-02	4.453193e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428572e-03	2.272838e-02	5.112550e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.200000e-02	9.192958e-03	4.585473e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428571e-03	5.533452e-03	5.660908e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.200000e-02	1.414704e-02	4.954102e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428573e-03	2.310660e-02	4.564348e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.200000e-02	2.161458e-02	3.926478e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428573e-03	8.871006e-03	7.004311e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	3.000000e-02	1.236662e-02	4.575814e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285714e-02	1.334575e-02	4.278500e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	1.929403e-02	3.198679e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285715e-02	2.545380e-02	3.762969e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	3.000000e-02	1.041377e-02	4.799082e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285714e-02	2.309168e-02	5.038202e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.200000e-02	1.742082e-02	3.907522e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428572e-03	1.138229e-02	5.964417e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.200000e-02	1.734220e-02	3.735358e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428572e-03	3.306818e-02	3.982563e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.200000e-02	9.802230e-03	5.979685e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428571e-03	3.837003e-02	3.792996e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.200000e-02	5.677061e-03	5.307019e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428573e-03	1.599429e-02	5.218012e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.200000e-02	1.583664e-02	4.220416e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428573e-03	2.828528e-02	4.630070e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	3.000000e-02	1.034424e-02	3.990827e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285714e-02	2.329541e-02	5.012164e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	1.484807e-02	3.478414e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285715e-02	6.357575e-03	8.098106e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	3.000000e-02	1.133714e-02	5.135097e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285714e-02	1.359011e-02	4.996795e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200000e-02	1.240247e-02	4.589398e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428573e-03	9.940159e-03	5.630020e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200000e-02	1.482904e-02	3.807711e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428573e-03	1.828876e-02	5.529559e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200000e-02	6.179937e-03	7.180342e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428572e-03	1.684826e-02	5.914304e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200001e-02	7.077129e-03	7.540861e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428574e-03	1.350030e-02	5.657138e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200001e-02	6.004402e-03	4.312788e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428574e-03	4.141740e-03	7.648402e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000000e-02	2.086036e-02	3.090607e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285714e-02	1.188948e-02	6.537678e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000001e-02	9.600263e-03	3.627353e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285715e-02	7.726545e-03	8.998232e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000000e-02	7.057962e-03	4.398227e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285714e-02	9.470403e-03	6.201179e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.200000e-02	3.056746e-02	4.070791e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428571e-03	4.189179e-02	4.130223e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.200000e-02	2.021719e-02	4.543214e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428571e-03	4.537244e-03	7.243799e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199999e-02	6.048107e-03	7.234355e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428570e-03	1.125641e-02	7.209835e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.200000e-02	1.441121e-02	5.684565e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428572e-03	2.844759e-02	3.762962e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.200000e-02	1.464087e-02	3.655041e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428572e-03	2.328142e-02	4.754021e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999999e-02	7.947687e-03	5.759931e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285714e-02	5.340886e-03	1.000000e+02
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000000e-02	1.104174e-02	3.859416e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285715e-02	1.107259e-03	7.046482e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999999e-02	9.399536e-03	4.596550e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285714e-02	1.045791e-02	5.226729e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.200000e-02	1.040326e-02	4.491969e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428571e-03	2.074791e-02	4.428749e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.200000e-02	1.993847e-02	4.186218e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428571e-03	7.688344e-03	5.933830e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199999e-02	9.768192e-03	4.398073e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428570e-03	1.550132e-02	4.940522e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.200000e-02	2.242038e-02	3.602865e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428572e-03	3.231203e-02	4.070624e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.200000e-02	9.031150e-03	4.470807e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428572e-03	1.509520e-02	5.199149e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999999e-02	1.158961e-02	3.762835e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285714e-02	1.818767e-02	4.967802e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000000e-02	1.576275e-02	4.381844e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285715e-02	1.473298e-02	5.647274e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999999e-02	7.376211e-03	5.120111e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285714e-02	1.610136e-02	4.700642e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.200001e-02	7.177622e-03	4.712529e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428576e-03	1.191860e-02	7.042162e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.200001e-02	9.884914e-03	3.934846e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428576e-03	2.717689e-02	6.045265e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.200001e-02	2.190587e-02	3.419178e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428574e-03	1.749419e-02	5.306615e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.200001e-02	8.225958e-03	5.018849e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428577e-03	3.153579e-02	3.843780e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.200001e-02	1.902900e-02	5.354826e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428577e-03	2.175062e-02	5.349914e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	3.000000e-02	2.029700e-02	3.433412e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285715e-02	2.265232e-02	5.227367e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000002e-02	9.210491e-03	4.375521e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285715e-02	8.824525e-03	7.031223e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	3.000000e-02	1.166397e-02	4.431589e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285715e-02	8.379824e-03	6.087206e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	1.379108e-02	3.475371e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428567e-03	1.246371e-02	7.023487e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	1.763511e-02	3.568600e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428567e-03	7.593896e-03	5.771576e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199999e-02	1.124649e-02	4.314468e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428566e-03	4.771618e-03	5.572427e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	6.672616e-03	5.387191e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428568e-03	3.508050e-02	3.698916e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	5.938591e-03	6.070071e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428568e-03	2.099699e-02	4.802031e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	1.566082e-02	3.408565e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	9.361635e-03	6.220879e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	2.999999e-02	9.525027e-03	4.988764e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	9.827866e-03	5.687034e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	7.779572e-03	6.539304e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	6.290806e-03	8.082311e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700000e-02	1.986900e-02	2.598754e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	2.200825e-02	2.590681e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700000e-02	1.442382e-02	3.066883e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	1.430709e-02	3.227730e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699998e-02	1.449253e-02	2.782239e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.300000e-02	1.256904e-02	3.681481e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	1.110140e-02	3.046476e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300001e-02	1.025517e-02	4.269143e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	1.064462e-02	2.751395e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300001e-02	1.620628e-02	3.117559e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	1.423898e-02	2.515039e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	1.195582e-02	3.275659e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050000e-01	1.180037e-02	2.581697e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500001e-02	1.350867e-02	3.209491e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	8.232674e-03	3.181421e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	1.110931e-02	3.495240e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700000e-02	2.165658e-02	2.118043e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	1.822377e-02	3.457212e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700000e-02	1.520924e-02	2.380435e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	1.806594e-02	4.378290e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699998e-02	2.038354e-02	2.316671e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.300000e-02	1.054914e-02	3.977987e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	1.260192e-02	3.183683e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300001e-02	9.766865e-03	4.536350e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	5.259279e-03	4.159725e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300001e-02	1.192906e-02	4.380680e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	9.975768e-03	3.415442e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	1.878095e-02	3.641603e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050000e-01	8.420191e-03	3.105801e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500001e-02	1.332786e-02	3.647669e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	1.084724e-02	3.063658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	1.539851e-02	3.114409e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700000e-02	9.640221e-03	3.691217e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	7.215302e-03	4.494075e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700000e-02	1.103251e-02	3.033283e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	1.495968e-02	4.446661e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699998e-02	1.019057e-02	3.886316e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.300000e-02	8.414487e-03	3.923499e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	6.755467e-03	3.484225e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300001e-02	1.447570e-02	4.269698e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	8.886600e-03	3.537545e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300001e-02	1.381101e-02	3.919818e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.163238e-02	2.496657e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	6.578213e-03	5.228652e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050000e-01	1.410890e-02	2.480213e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500001e-02	4.568404e-03	5.207639e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	6.104958e-03	2.931283e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	8.436568e-03	3.661476e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700000e-02	6.837820e-03	3.765926e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	3.974681e-03	7.239601e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700000e-02	1.026178e-02	4.333065e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	1.896006e-03	1.000000e+02
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699998e-02	8.311061e-03	4.108902e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.300000e-02	7.491988e-03	4.840226e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	1.128489e-02	2.792007e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300001e-02	5.927142e-03	5.865157e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.289772e-02	2.900812e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300001e-02	1.171008e-02	3.618493e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	1.277936e-02	2.691435e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	1.119582e-02	3.775011e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050000e-01	7.716452e-03	3.836535e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500001e-02	1.003248e-02	4.697005e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	9.180949e-03	2.920104e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	1.225139e-02	3.247450e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.200000e-02	1.724488e-02	5.253220e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428572e-03	3.954479e-02	4.064264e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.200000e-02	2.478419e-02	4.423944e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428572e-03	3.074902e-02	4.416259e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.200000e-02	4.250687e-03	7.997083e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428571e-03	3.701621e-02	4.031380e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.200000e-02	2.815950e-02	3.179356e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428573e-03	3.739001e-02	3.552249e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.200000e-02	4.732382e-02	2.623770e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428573e-03	3.046974e-02	4.327676e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	3.000000e-02	2.850474e-02	3.088974e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285714e-02	2.475474e-02	4.440252e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	2.135322e-02	3.693787e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285715e-02	2.305989e-02	4.550164e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	3.000000e-02	2.082482e-02	3.637211e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285714e-02	2.299002e-02	4.075804e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.200000e-02	3.210929e-02	3.696337e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428572e-03	4.161039e-02	3.731428e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.200000e-02	2.417358e-02	4.128373e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428572e-03	2.659382e-02	4.635099e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.200000e-02	2.877213e-02	3.706094e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428571e-03	3.474166e-02	4.039488e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.200000e-02	2.481028e-02	3.348307e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428573e-03	6.204385e-02	3.579098e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.200000e-02	3.742966e-02	3.486695e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428573e-03	2.784086e-02	3.784411e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	3.000000e-02	3.251839e-02	3.372316e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285714e-02	3.002603e-02	3.831310e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	2.538377e-02	3.553133e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285715e-02	5.107207e-02	2.998546e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	3.000000e-02	3.468224e-02	3.269456e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285714e-02	2.538520e-02	4.532530e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200000e-02	4.387949e-02	3.383535e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428573e-03	1.578728e-02	5.157917e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200000e-02	1.981352e-02	4.080250e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428573e-03	3.551496e-02	3.821958e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200000e-02	2.571529e-02	3.810666e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428572e-03	3.856959e-02	4.795753e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200001e-02	2.925804e-02	4.057317e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428574e-03	4.571700e-02	4.227752e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200001e-02	3.402873e-02	3.771594e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428574e-03	1.836613e-02	5.122809e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000000e-02	2.007334e-02	3.974494e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285714e-02	3.005129e-02	4.364021e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000001e-02	1.968975e-02	4.017746e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285715e-02	4.698578e-02	3.284976e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000000e-02	2.887707e-02	3.598444e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285714e-02	3.032247e-02	3.646618e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.200000e-02	3.836582e-02	3.612282e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428571e-03	6.998398e-02	3.280412e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.200000e-02	4.480155e-02	3.245830e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428571e-03	1.911381e-02	6.084665e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199999e-02	1.822597e-02	4.650276e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428570e-03	5.229162e-02	3.580645e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.200000e-02	2.487390e-02	3.816239e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428572e-03	4.294692e-02	3.633119e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.200000e-02	3.307013e-02	3.219321e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428572e-03	5.009053e-02	4.279867e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999999e-02	3.756887e-02	3.484253e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285714e-02	3.247332e-02	3.909064e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000000e-02	2.892371e-02	3.020898e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285715e-02	1.855471e-02	5.861723e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999999e-02	2.013632e-02	4.042766e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285714e-02	1.403672e-02	5.148100e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.200000e-02	5.524317e-02	2.917574e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428571e-03	1.042479e-02	6.504888e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.200000e-02	1.695703e-02	4.707631e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428571e-03	3.963046e-02	3.857866e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199999e-02	2.427062e-02	3.343924e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428570e-03	6.341316e-02	3.675888e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.200000e-02	4.583332e-02	3.302162e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428572e-03	2.869221e-02	4.718757e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.200000e-02	2.563591e-02	3.574767e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428572e-03	6.396140e-02	3.559333e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999999e-02	3.200357e-02	3.011568e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285714e-02	5.509797e-02	2.927330e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000000e-02	4.351325e-02	2.582440e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285715e-02	2.812517e-02	4.343927e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999999e-02	2.705605e-02	3.208197e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285714e-02	2.812050e-02	4.710782e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.200001e-02	1.886925e-02	4.635193e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428576e-03	2.232435e-02	5.215173e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.200001e-02	1.275413e-02	5.212977e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428576e-03	3.944743e-02	3.729751e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.200001e-02	4.028271e-02	2.968932e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428574e-03	4.924776e-02	3.479581e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.200001e-02	3.330252e-02	3.188652e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428577e-03	4.094844e-02	4.049075e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.200001e-02	2.053411e-02	4.129811e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428577e-03	2.680332e-02	4.751101e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	3.000000e-02	2.467976e-02	3.998907e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285715e-02	8.404094e-03	5.196900e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000002e-02	1.527622e-02	4.271978e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285715e-02	2.601293e-02	4.368995e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	3.000000e-02	1.349778e-02	4.011145e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285715e-02	2.903839e-02	4.212680e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	2.502450e-02	3.558487e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428567e-03	3.170985e-02	4.723587e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	2.688217e-02	4.323888e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428567e-03	2.788074e-02	4.287711e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199999e-02	2.120100e-02	3.503775e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428566e-03	6.182096e-02	3.391626e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	4.032521e-02	3.461226e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428568e-03	3.147355e-02	3.740477e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	3.756560e-02	3.895742e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428568e-03	1.828149e-02	6.423370e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	1.621362e-02	4.289295e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	2.817056e-02	4.940336e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	2.999999e-02	1.474818e-02	4.175586e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	3.801268e-02	3.934400e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	1.866388e-02	3.905374e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	3.273803e-02	3.834941e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700000e-02	3.534043e-02	2.079543e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	6.232061e-02	2.057673e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700000e-02	3.576964e-02	2.325618e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	3.824338e-02	2.283922e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699998e-02	2.985928e-02	2.098855e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.300000e-02	3.566688e-02	2.308458e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	3.166683e-02	1.855081e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300001e-02	3.078585e-02	2.019785e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	2.639907e-02	1.865834e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300001e-02	4.096236e-02	2.049967e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	2.877822e-02	1.817959e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	4.455911e-02	2.073321e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050000e-01	3.243325e-02	1.886595e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500001e-02	3.925347e-02	1.630244e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	3.013280e-02	1.702606e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	1.989477e-02	2.778768e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700000e-02	2.649092e-02	2.040244e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	4.386568e-02	1.981223e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700000e-02	3.998834e-02	1.694010e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	3.111571e-02	3.098851e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699998e-02	2.525000e-02	2.188083e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.300000e-02	2.874785e-02	2.402941e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	2.227157e-02	2.112121e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300001e-02	3.947169e-02	1.980196e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	3.071827e-02	1.720463e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300001e-02	1.774454e-02	3.018060e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	1.916794e-02	2.496206e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	2.200754e-02	2.589989e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050000e-01	2.112085e-02	1.938009e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500001e-02	3.155705e-02	2.261760e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	3.099829e-02	1.607658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	2.096612e-02	2.774525e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700000e-02	3.460982e-02	2.000933e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	3.438591e-02	2.361661e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700000e-02	3.116194e-02	1.825632e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	3.060493e-02	2.631115e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699998e-02	2.696415e-02	2.033474e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.300000e-02	3.705050e-02	2.464897e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	2.319814e-02	2.485304e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300001e-02	2.044810e-02	2.971415e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	2.133310e-02	2.438403e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300001e-02	3.192332e-02	2.532010e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.984164e-02	2.232778e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	3.841866e-02	2.048711e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050000e-01	2.209174e-02	2.088301e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500001e-02	2.748550e-02	2.191365e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	2.070811e-02	2.015829e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	2.783450e-02	2.077378e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700000e-02	2.065832e-02	2.555205e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	2.165929e-02	3.210127e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700000e-02	2.057050e-02	2.748482e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	2.352874e-02	3.056098e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699998e-02	1.925132e-02	2.107219e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.300000e-02	3.194506e-02	2.412898e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	2.519355e-02	2.396729e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300001e-02	1.757707e-02	3.191541e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.635826e-02	2.434996e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300001e-02	2.665870e-02	2.136641e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	2.319463e-02	1.738522e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	2.860067e-02	2.297326e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050000e-01	2.619439e-02	1.671266e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500001e-02	2.003572e-02	2.345525e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	2.306359e-02	1.653891e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	2.997056e-02	2.426218e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)	2.200000e-02	3.190608e-02	3.811030e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)	9.428572e-03	7.246729e-02	2.929491e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)	2.200000e-02	4.072345e-02	3.461742e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)	9.428572e-03	5.347739e-02	3.356790e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)	2.200000e-02	1.344365e-02	3.997393e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)	9.428571e-03	4.254966e-02	3.518526e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)	2.200000e-02	4.230654e-02	2.512812e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)	9.428573e-03	6.049660e-02	2.693265e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)	2.200000e-02	6.893839e-02	2.294937e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)	9.428573e-03	3.934074e-02	3.607827e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)	3.000000e-02	4.087135e-02	2.465120e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)	1.285714e-02	3.810049e-02	3.145805e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)	3.000001e-02	4.064725e-02	2.401877e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)	1.285715e-02	4.851369e-02	2.749150e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)	3.000000e-02	3.123859e-02	2.851213e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)	1.285714e-02	4.608170e-02	3.080298e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)	2.200000e-02	4.953011e-02	2.925655e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)	9.428572e-03	5.299268e-02	3.088277e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)	2.200000e-02	4.151578e-02	2.687081e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)	9.428572e-03	5.966200e-02	2.865444e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)	2.200000e-02	3.857436e-02	3.029324e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)	9.428571e-03	7.311169e-02	2.712843e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)	2.200000e-02	3.048734e-02	2.800654e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)	9.428573e-03	7.803814e-02	2.928441e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)	2.200000e-02	5.326629e-02	2.712690e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)	9.428573e-03	5.612614e-02	2.837481e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)	3.000000e-02	4.286263e-02	2.715484e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)	1.285714e-02	5.332144e-02	3.087061e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)	3.000001e-02	4.023184e-02	2.652799e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)	1.285715e-02	5.742964e-02	2.773246e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)	3.000000e-02	4.601938e-02	2.629428e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)	1.285714e-02	3.897532e-02	3.289924e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)	2.200000e-02	5.628197e-02	2.698189e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)	9.428573e-03	2.572744e-02	3.712372e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)	2.200000e-02	3.464255e-02	2.876155e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)	9.428573e-03	5.380372e-02	3.335466e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)	2.200000e-02	3.189522e-02	3.276752e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)	9.428572e-03	5.541785e-02	3.675587e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)	2.200001e-02	3.633517e-02	3.491530e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)	9.428574e-03	5.921730e-02	3.551880e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)	2.200001e-02	4.003313e-02	3.405298e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)	9.428574e-03	2.250787e-02	4.340685e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)	3.000000e-02	4.093370e-02	2.511183e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)	1.285714e-02	4.194077e-02	4.472254e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)	3.000001e-02	2.929001e-02	3.214465e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)	1.285715e-02	5.471233e-02	3.353791e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)	3.000000e-02	3.593503e-02	3.035764e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)	1.285714e-02	3.979287e-02	3.727872e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)	2.200000e-02	6.893328e-02	2.536880e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)	9.428571e-03	1.118758e-01	2.376288e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)	2.200000e-02	6.501874e-02	2.496097e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)	9.428571e-03	2.365106e-02	5.047666e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)	2.199999e-02	2.427408e-02	3.831035e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)	9.428570e-03	6.354803e-02	3.324603e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)	2.200000e-02	3.928511e-02	3.232350e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)	9.428572e-03	7.139451e-02	2.610697e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)	2.200000e-02	4.771099e-02	2.658355e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)	9.428572e-03	7.337196e-02	3.566912e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)	2.999999e-02	4.551656e-02	3.257889e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)	1.285714e-02	3.781420e-02	3.573361e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)	3.000000e-02	3.996545e-02	2.965435e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)	1.285715e-02	1.966197e-02	5.526246e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)	2.999999e-02	2.953585e-02	3.478765e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)	1.285714e-02	2.449462e-02	3.697769e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)	2.200000e-02	6.564643e-02	2.538591e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)	9.428571e-03	3.117270e-02	3.537310e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)	2.200000e-02	3.689550e-02	3.069267e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)	9.428571e-03	4.731880e-02	3.394208e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)	2.199999e-02	3.403881e-02	2.765791e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)	9.428570e-03	7.891449e-02	3.198221e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)	2.200000e-02	6.825370e-02	2.411340e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)	9.428572e-03	6.100424e-02	3.397908e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)	2.200000e-02	3.466706e-02	2.935130e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)	9.428572e-03	7.905660e-02	3.280871e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)	2.999999e-02	4.359319e-02	2.350517e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)	1.285714e-02	7.328565e-02	2.728813e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)	3.000000e-02	5.927599e-02	2.520616e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)	1.285715e-02	4.285816e-02	3.312726e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)	2.999999e-02	3.443226e-02	2.875764e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)	1.285714e-02	4.422186e-02	3.310242e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)	2.200001e-02	2.604687e-02	3.485258e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)	9.428576e-03	3.424294e-02	4.079405e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)	2.200001e-02	2.263905e-02	3.251574e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)	9.428576e-03	6.662432e-02	3.157819e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)	2.200001e-02	6.218858e-02	2.111895e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)	9.428574e-03	6.674194e-02	2.781636e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)	2.200001e-02	4.152848e-02	2.658837e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)	9.428577e-03	7.248423e-02	3.092185e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)	2.200001e-02	3.956310e-02	3.212783e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)	9.428577e-03	4.855395e-02	3.407808e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)	3.000000e-02	4.497676e-02	2.490963e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)	1.285715e-02	3.105642e-02	3.963530e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)	3.000002e-02	2.448671e-02	2.975520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)	1.285715e-02	3.483745e-02	3.637258e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)	3.000000e-02	2.516175e-02	2.799137e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)	1.285715e-02	3.741822e-02	3.440496e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)	2.199999e-02	3.881558e-02	2.419289e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)	9.428567e-03	4.417357e-02	3.820737e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)	2.199999e-02	4.451728e-02	2.799911e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)	9.428567e-03	3.547464e-02	3.492235e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)	2.199999e-02	3.244749e-02	2.628499e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)	9.428566e-03	6.659258e-02	3.218399e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)	2.199999e-02	4.699783e-02	2.993575e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)	9.428568e-03	6.655406e-02	2.774062e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)	2.199999e-02	4.350419e-02	3.394352e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)	9.428568e-03	3.927848e-02	3.958061e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)	2.999998e-02	3.187444e-02	2.607352e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)	1.285713e-02	3.753219e-02	4.541647e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)	2.999999e-02	2.427321e-02	3.199825e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)	1.285714e-02	4.784055e-02	3.364403e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)	2.999998e-02	2.644345e-02	3.328183e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)	1.285713e-02	3.902884e-02	3.390154e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)	7.700000e-02	5.520943e-02	1.827077e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)	3.300000e-02	8.432886e-02	1.701871e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)	7.700000e-02	5.019347e-02	1.853236e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)	3.300000e-02	5.255047e-02	1.700961e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)	7.699998e-02	4.435181e-02	1.648371e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)	3.300000e-02	4.823592e-02	1.921661e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)	7.700001e-02	4.276823e-02	1.596589e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)	3.300001e-02	4.104102e-02	1.644011e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)	7.700001e-02	3.704368e-02	1.571765e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)	3.300001e-02	5.716863e-02	1.690459e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)	1.050000e-01	4.301719e-02	1.712823e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)	4.499999e-02	5.651493e-02	1.760660e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)	1.050000e-01	4.423362e-02	1.576799e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)	4.500001e-02	5.276215e-02	1.468623e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)	1.050000e-01	3.836547e-02	1.393376e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)	4.499999e-02	3.100408e-02	2.062348e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)	7.700000e-02	4.814750e-02	1.468222e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)	3.300000e-02	6.208944e-02	1.812821e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)	7.700000e-02	5.519758e-02	1.275647e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)	3.300000e-02	4.918166e-02	2.364726e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)	7.699998e-02	4.563354e-02	1.700193e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)	3.300000e-02	3.929699e-02	2.177296e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)	7.700001e-02	3.487348e-02	1.792084e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)	3.300001e-02	4.923856e-02	1.936937e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)	7.700001e-02	3.597755e-02	1.634813e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)	3.300001e-02	2.967361e-02	2.318915e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)	1.050000e-01	2.914371e-02	2.010487e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)	4.499999e-02	4.078849e-02	2.006298e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)	1.050000e-01	2.954104e-02	1.591733e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)	4.500001e-02	4.488491e-02	1.750121e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)	1.050000e-01	4.184553e-02	1.345880e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)	4.499999e-02	3.636463e-02	1.922996e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)	7.700000e-02	4.425004e-02	1.741765e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)	3.300000e-02	4.160121e-02	2.033251e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)	7.700000e-02	4.219445e-02	1.468493e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)	3.300000e-02	4.556461e-02	2.432258e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)	7.699998e-02	3.715472e-02	1.775665e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)	3.300000e-02	4.546499e-02	2.218969e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)	7.700001e-02	2.995361e-02	2.047046e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)	3.300001e-02	3.492381e-02	2.462349e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)	7.700001e-02	3.021970e-02	2.182929e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)	3.300001e-02	4.573433e-02	2.360243e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)	1.050000e-01	3.147402e-02	1.810748e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)	4.499999e-02	4.499688e-02	1.882671e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)	1.050000e-01	3.620064e-02	1.553997e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)	4.500001e-02	3.205390e-02	2.159771e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)	1.050000e-01	2.681307e-02	1.541747e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)	4.499999e-02	3.627107e-02	1.846952e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)	7.700000e-02	2.749614e-02	1.995610e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)	3.300000e-02	2.563397e-02	2.912318e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)	7.700000e-02	3.083227e-02	2.151152e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)	3.300000e-02	2.542474e-02	2.876304e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)	7.699998e-02	2.756238e-02	1.890128e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)	3.300000e-02	3.943704e-02	2.386451e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)	7.700001e-02	3.647845e-02	1.931230e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)	3.300001e-02	2.350421e-02	2.895671e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)	7.700001e-02	2.925598e-02	1.853566e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)	3.300001e-02	3.836878e-02	1.915776e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)	1.050000e-01	3.597398e-02	1.544692e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)	4.499999e-02	3.979649e-02	1.895238e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)	1.050000e-01	3.391084e-02	1.782824e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)	4.500001e-02	3.006820e-02	2.090744e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)	1.050000e-01	3.224454e-02	1.488840e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)	4.499999e-02	4.222194e-02	2.137258e+01

number of batches used: 50	4.034821e-02	2.895010e+00



******************************************************************************
RESPONSE FUNCTION : FLUX
RESPONSE NAME : photon_flux_response
SCORE NAME : mesh11.2
ENERGY DECOUPAGE NAME : grid_score


 PARTICULE : PHOTON 
******************************************************************************

	 scoring mode : SCORE_TRACK
	 scoring zone : 
	 Volume in 1.000000e+00 cm3: 6.000000e+00
	 Results on a mesh: 
	 Cell   	  (x,y,z)[1.000000 cm]	 volume[1.000000 cm3]	 tally   	  sigma (percent)

			 (in phot.cm^-2.s^-1)

Energy range (in MeV): 0.000000e+00 - 1.000000e+00
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.199999e-02	1.466121e-02	3.617305e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428566e-03	3.292250e-02	4.432007e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.199999e-02	1.593925e-02	4.453195e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428566e-03	2.272839e-02	5.112549e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.199997e-02	9.192955e-03	4.585475e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428557e-03	5.533439e-03	5.660912e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.199999e-02	1.414703e-02	4.954103e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428566e-03	2.310661e-02	4.564348e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.199999e-02	2.161457e-02	3.926477e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428566e-03	8.871016e-03	7.004311e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	2.999998e-02	1.236663e-02	4.575814e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285713e-02	1.334570e-02	4.278508e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	1.929403e-02	3.198680e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285714e-02	2.545381e-02	3.762969e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	2.999998e-02	1.041378e-02	4.799082e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285713e-02	2.309166e-02	5.038201e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.199999e-02	1.742082e-02	3.907523e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428566e-03	1.138227e-02	5.964442e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.199999e-02	1.734220e-02	3.735359e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428566e-03	3.306819e-02	3.982563e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.199997e-02	9.802223e-03	5.979688e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428557e-03	3.837004e-02	3.792996e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.199999e-02	5.677065e-03	5.307021e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428566e-03	1.599428e-02	5.218015e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.199999e-02	1.583666e-02	4.220410e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428566e-03	2.828528e-02	4.630073e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	2.999998e-02	1.034423e-02	3.990832e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285713e-02	2.329547e-02	5.012156e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	1.484808e-02	3.478414e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285714e-02	6.357582e-03	8.098104e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	2.999998e-02	1.133714e-02	5.135100e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285713e-02	1.359013e-02	4.996798e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200007e-02	1.240246e-02	4.589396e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428598e-03	9.940207e-03	5.630015e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200007e-02	1.482903e-02	3.807709e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428598e-03	1.828873e-02	5.529557e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200004e-02	6.179941e-03	7.180346e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428588e-03	1.684825e-02	5.914299e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200007e-02	7.077109e-03	7.540861e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428598e-03	1.350030e-02	5.657132e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200007e-02	6.004409e-03	4.312786e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428598e-03	4.141784e-03	7.648363e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000008e-02	2.086036e-02	3.090605e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285718e-02	1.188947e-02	6.537675e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000011e-02	9.600276e-03	3.627351e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285719e-02	7.726538e-03	8.998215e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000008e-02	7.057964e-03	4.398225e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285718e-02	9.470395e-03	6.201182e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.199999e-02	3.056747e-02	4.070789e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428566e-03	4.189185e-02	4.130218e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.199999e-02	2.021719e-02	4.543216e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428566e-03	4.537246e-03	7.243796e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199997e-02	6.048109e-03	7.234356e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428557e-03	1.125644e-02	7.209831e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.199999e-02	1.441125e-02	5.684558e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428566e-03	2.844762e-02	3.762962e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.199999e-02	1.464084e-02	3.655043e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428566e-03	2.328141e-02	4.754023e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999998e-02	7.947672e-03	5.759936e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285713e-02	5.340901e-03	1.000000e+02
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000001e-02	1.104172e-02	3.859418e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285714e-02	1.107253e-03	7.046496e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999998e-02	9.399535e-03	4.596552e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285713e-02	1.045791e-02	5.226729e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.199999e-02	1.040326e-02	4.491969e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428566e-03	2.074785e-02	4.428747e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.199999e-02	1.993847e-02	4.186219e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428566e-03	7.688351e-03	5.933831e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199997e-02	9.768217e-03	4.398069e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428557e-03	1.550133e-02	4.940526e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.199999e-02	2.242037e-02	3.602865e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428566e-03	3.231204e-02	4.070625e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.199999e-02	9.031155e-03	4.470804e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428566e-03	1.509521e-02	5.199147e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999998e-02	1.158965e-02	3.762831e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285713e-02	1.818767e-02	4.967805e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000001e-02	1.576276e-02	4.381843e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285714e-02	1.473298e-02	5.647274e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999998e-02	7.376214e-03	5.120111e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285713e-02	1.610139e-02	4.700643e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.199999e-02	7.177621e-03	4.712528e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428566e-03	1.191861e-02	7.042162e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.199999e-02	9.884915e-03	3.934845e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428566e-03	2.717691e-02	6.045265e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.199997e-02	2.190587e-02	3.419177e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428557e-03	1.749418e-02	5.306618e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.199999e-02	8.225951e-03	5.018856e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428566e-03	3.153577e-02	3.843781e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.199999e-02	1.902900e-02	5.354828e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428566e-03	2.175064e-02	5.349915e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	2.999998e-02	2.029700e-02	3.433411e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285713e-02	2.265233e-02	5.227367e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000001e-02	9.210487e-03	4.375520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285714e-02	8.824524e-03	7.031229e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	2.999998e-02	1.166398e-02	4.431589e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285713e-02	8.379808e-03	6.087208e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	1.379108e-02	3.475370e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428566e-03	1.246371e-02	7.023487e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	1.763511e-02	3.568600e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428566e-03	7.593895e-03	5.771575e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199997e-02	1.124649e-02	4.314468e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428557e-03	4.771600e-03	5.572440e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	6.672619e-03	5.387189e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428566e-03	3.508051e-02	3.698917e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	5.938589e-03	6.070072e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428566e-03	2.099701e-02	4.802029e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	1.566081e-02	3.408565e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	9.361634e-03	6.220882e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	3.000001e-02	9.525028e-03	4.988763e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	9.827865e-03	5.687034e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	7.779572e-03	6.539305e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	6.290804e-03	8.082314e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700001e-02	1.986900e-02	2.598754e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	2.200825e-02	2.590681e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700001e-02	1.442382e-02	3.066883e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	1.430709e-02	3.227731e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699993e-02	1.449254e-02	2.782240e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.299996e-02	1.256904e-02	3.681484e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	1.110140e-02	3.046476e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300000e-02	1.025516e-02	4.269143e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	1.064461e-02	2.751395e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300000e-02	1.620628e-02	3.117560e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	1.423898e-02	2.515039e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	1.195582e-02	3.275659e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050001e-01	1.180037e-02	2.581697e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500002e-02	1.350867e-02	3.209491e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	8.232674e-03	3.181421e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	1.110931e-02	3.495240e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700001e-02	2.165658e-02	2.118043e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	1.822377e-02	3.457212e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700001e-02	1.520924e-02	2.380435e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	1.806594e-02	4.378290e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699993e-02	2.038354e-02	2.316671e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.299996e-02	1.054914e-02	3.977989e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	1.260192e-02	3.183682e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300000e-02	9.766867e-03	4.536348e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	5.259277e-03	4.159724e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300000e-02	1.192906e-02	4.380681e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	9.975768e-03	3.415442e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	1.878095e-02	3.641604e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050001e-01	8.420192e-03	3.105801e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500002e-02	1.332786e-02	3.647668e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	1.084724e-02	3.063658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	1.539851e-02	3.114409e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700001e-02	9.640221e-03	3.691217e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	7.215302e-03	4.494075e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700001e-02	1.103251e-02	3.033282e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	1.495968e-02	4.446662e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699993e-02	1.019057e-02	3.886317e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.299996e-02	8.414481e-03	3.923503e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	6.755468e-03	3.484224e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300000e-02	1.447570e-02	4.269699e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	8.886600e-03	3.537545e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300000e-02	1.381102e-02	3.919818e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.163238e-02	2.496657e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	6.578218e-03	5.228651e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050001e-01	1.410890e-02	2.480213e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500002e-02	4.568402e-03	5.207639e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	6.104958e-03	2.931283e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	8.436566e-03	3.661476e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700001e-02	6.837819e-03	3.765926e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	3.974680e-03	7.239601e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700001e-02	1.026178e-02	4.333065e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	1.896006e-03	1.000000e+02
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699993e-02	8.311062e-03	4.108903e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.299996e-02	7.491988e-03	4.840227e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	1.128489e-02	2.792008e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300000e-02	5.927145e-03	5.865156e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.289773e-02	2.900813e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300000e-02	1.171008e-02	3.618493e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	1.277936e-02	2.691435e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	1.119582e-02	3.775011e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050001e-01	7.716453e-03	3.836535e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500002e-02	1.003248e-02	4.697005e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	9.180949e-03	2.920104e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	1.225139e-02	3.247450e+01

Energy range (in MeV): 1.000000e+00 - 2.000000e+01
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)   	2.199999e-02	1.724488e-02	5.253219e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)   	9.428566e-03	3.954479e-02	4.064265e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)   	2.199999e-02	2.478418e-02	4.423946e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)   	9.428566e-03	3.074902e-02	4.416260e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)   	2.199997e-02	4.250685e-03	7.997092e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)   	9.428557e-03	3.701623e-02	4.031381e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)   	2.199999e-02	2.815945e-02	3.179358e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)   	9.428566e-03	3.739001e-02	3.552252e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)   	2.199999e-02	4.732383e-02	2.623770e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)   	9.428566e-03	3.046973e-02	4.327676e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)   	2.999998e-02	2.850473e-02	3.088975e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)   	1.285713e-02	2.475473e-02	4.440252e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)   	3.000001e-02	2.135323e-02	3.693786e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)   	1.285714e-02	2.305988e-02	4.550168e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)   	2.999998e-02	2.082482e-02	3.637212e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)   	1.285713e-02	2.299003e-02	4.075804e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)   	2.199999e-02	3.210931e-02	3.696337e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)   	9.428566e-03	4.161044e-02	3.731427e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)   	2.199999e-02	2.417362e-02	4.128370e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)   	9.428566e-03	2.659373e-02	4.635110e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)   	2.199997e-02	2.877210e-02	3.706094e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)   	9.428557e-03	3.474167e-02	4.039490e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)   	2.199999e-02	2.481028e-02	3.348307e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)   	9.428566e-03	6.204382e-02	3.579098e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)   	2.199999e-02	3.742958e-02	3.486699e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)   	9.428566e-03	2.784081e-02	3.784411e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)   	2.999998e-02	3.251844e-02	3.372315e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)   	1.285713e-02	3.002598e-02	3.831310e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)   	3.000001e-02	2.538378e-02	3.553133e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)   	1.285714e-02	5.107195e-02	2.998547e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)   	2.999998e-02	3.468227e-02	3.269455e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)   	1.285713e-02	2.538521e-02	4.532531e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)   	2.200007e-02	4.387937e-02	3.383535e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)   	9.428598e-03	1.578724e-02	5.157916e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)   	2.200007e-02	1.981397e-02	4.080241e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)   	9.428598e-03	3.551496e-02	3.821951e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)   	2.200004e-02	2.571581e-02	3.810570e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)   	9.428588e-03	3.856949e-02	4.795753e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)   	2.200007e-02	2.925850e-02	4.057252e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)   	9.428598e-03	4.571696e-02	4.227742e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)   	2.200007e-02	3.402873e-02	3.771587e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)   	9.428598e-03	1.836621e-02	5.122783e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)   	3.000008e-02	2.007329e-02	3.974493e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)   	1.285718e-02	3.005128e-02	4.364013e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)   	3.000011e-02	1.968970e-02	4.017745e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)   	1.285719e-02	4.698582e-02	3.284967e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)   	3.000008e-02	2.887699e-02	3.598444e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)   	1.285718e-02	3.032239e-02	3.646618e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)   	2.199999e-02	3.836591e-02	3.612274e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)   	9.428566e-03	6.998401e-02	3.280412e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)   	2.199999e-02	4.480106e-02	3.245849e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)   	9.428566e-03	1.911382e-02	6.084665e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)   	2.199997e-02	1.822552e-02	4.650334e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)   	9.428557e-03	5.229165e-02	3.580646e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)   	2.199999e-02	2.487349e-02	3.816293e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)   	9.428566e-03	4.294695e-02	3.633119e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)   	2.199999e-02	3.307014e-02	3.219321e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)   	9.428566e-03	5.009056e-02	4.279867e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)   	2.999998e-02	3.756889e-02	3.484253e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)   	1.285713e-02	3.247332e-02	3.909065e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)   	3.000001e-02	2.892372e-02	3.020897e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)   	1.285714e-02	1.855502e-02	5.861737e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)   	2.999998e-02	2.013632e-02	4.042766e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)   	1.285713e-02	1.403688e-02	5.148077e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)   	2.199999e-02	5.524313e-02	2.917576e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)   	9.428566e-03	1.042479e-02	6.504889e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)   	2.199999e-02	1.695705e-02	4.707628e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)   	9.428566e-03	3.963056e-02	3.857863e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)   	2.199997e-02	2.427059e-02	3.343934e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)   	9.428557e-03	6.341318e-02	3.675890e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)   	2.199999e-02	4.583328e-02	3.302165e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)   	9.428566e-03	2.869222e-02	4.718758e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)   	2.199999e-02	2.563596e-02	3.574763e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)   	9.428566e-03	6.396141e-02	3.559333e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)   	2.999998e-02	3.200360e-02	3.011570e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)   	1.285713e-02	5.509801e-02	2.927330e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)   	3.000001e-02	4.351328e-02	2.582439e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)   	1.285714e-02	2.812489e-02	4.343941e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)   	2.999998e-02	2.705608e-02	3.208195e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)   	1.285713e-02	2.812035e-02	4.710783e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)   	2.199999e-02	1.886924e-02	4.635190e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)   	9.428566e-03	2.232437e-02	5.215172e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)   	2.199999e-02	1.275413e-02	5.212981e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)   	9.428566e-03	3.944742e-02	3.729752e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)   	2.199997e-02	4.028270e-02	2.968933e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)   	9.428557e-03	4.924781e-02	3.479582e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)   	2.199999e-02	3.330253e-02	3.188649e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)   	9.428566e-03	4.094848e-02	4.049075e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)   	2.199999e-02	2.053410e-02	4.129812e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)   	9.428566e-03	2.680335e-02	4.751099e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)   	2.999998e-02	2.467976e-02	3.998905e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)   	1.285713e-02	8.404108e-03	5.196898e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)   	3.000001e-02	1.527621e-02	4.271979e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)   	1.285714e-02	2.601295e-02	4.368994e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)   	2.999998e-02	1.349777e-02	4.011144e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)   	1.285713e-02	2.903842e-02	4.212680e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)   	2.199999e-02	2.502450e-02	3.558487e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)   	9.428566e-03	3.170985e-02	4.723587e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)   	2.199999e-02	2.688216e-02	4.323889e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)   	9.428566e-03	2.788076e-02	4.287711e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)   	2.199997e-02	2.120100e-02	3.503776e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)   	9.428557e-03	6.182096e-02	3.391627e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)   	2.199999e-02	4.032521e-02	3.461225e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)   	9.428566e-03	3.147356e-02	3.740477e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)   	2.199999e-02	3.756561e-02	3.895742e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)   	9.428566e-03	1.828151e-02	6.423371e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)   	2.999998e-02	1.621362e-02	4.289294e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)   	1.285713e-02	2.817054e-02	4.940337e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)   	3.000001e-02	1.474818e-02	4.175585e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)   	1.285714e-02	3.801268e-02	3.934400e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)   	2.999998e-02	1.866388e-02	3.905374e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)   	1.285713e-02	3.273804e-02	3.834941e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)   	7.700001e-02	3.534044e-02	2.079543e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)   	3.300000e-02	6.232061e-02	2.057673e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)   	7.700001e-02	3.576964e-02	2.325617e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)   	3.300000e-02	3.824338e-02	2.283922e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)   	7.699993e-02	2.985928e-02	2.098856e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)   	3.299996e-02	3.566688e-02	2.308458e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)   	7.700001e-02	3.166684e-02	1.855081e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)   	3.300000e-02	3.078585e-02	2.019785e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)   	7.700001e-02	2.639907e-02	1.865835e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)   	3.300000e-02	4.096236e-02	2.049968e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)   	1.050000e-01	2.877821e-02	1.817959e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)   	4.499999e-02	4.455911e-02	2.073320e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)   	1.050001e-01	3.243325e-02	1.886595e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)   	4.500002e-02	3.925348e-02	1.630244e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)   	1.050000e-01	3.013279e-02	1.702606e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)   	4.499999e-02	1.989477e-02	2.778768e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)   	7.700001e-02	2.649093e-02	2.040244e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)   	3.300000e-02	4.386567e-02	1.981223e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)   	7.700001e-02	3.998834e-02	1.694010e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)   	3.300000e-02	3.111571e-02	3.098851e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)   	7.699993e-02	2.525000e-02	2.188084e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)   	3.299996e-02	2.874785e-02	2.402943e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)   	7.700001e-02	2.227156e-02	2.112121e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)   	3.300000e-02	3.947170e-02	1.980195e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)   	7.700001e-02	3.071828e-02	1.720462e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)   	3.300000e-02	1.774455e-02	3.018061e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)   	1.050000e-01	1.916794e-02	2.496206e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)   	4.499999e-02	2.200753e-02	2.589989e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)   	1.050001e-01	2.112085e-02	1.938009e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)   	4.500002e-02	3.155705e-02	2.261760e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)   	1.050000e-01	3.099829e-02	1.607658e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)   	4.499999e-02	2.096612e-02	2.774525e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)   	7.700001e-02	3.460982e-02	2.000933e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)   	3.300000e-02	3.438591e-02	2.361661e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)   	7.700001e-02	3.116194e-02	1.825632e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)   	3.300000e-02	3.060493e-02	2.631115e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)   	7.699993e-02	2.696415e-02	2.033474e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)   	3.299996e-02	3.705051e-02	2.464898e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)   	7.700001e-02	2.319814e-02	2.485303e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)   	3.300000e-02	2.044810e-02	2.971415e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)   	7.700001e-02	2.133310e-02	2.438404e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)   	3.300000e-02	3.192332e-02	2.532009e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)   	1.050000e-01	1.984164e-02	2.232778e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)   	4.499999e-02	3.841866e-02	2.048711e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)   	1.050001e-01	2.209174e-02	2.088301e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)   	4.500002e-02	2.748550e-02	2.191364e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)   	1.050000e-01	2.070811e-02	2.015829e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)   	4.499999e-02	2.783450e-02	2.077378e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)   	7.700001e-02	2.065832e-02	2.555205e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)   	3.300000e-02	2.165929e-02	3.210127e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)   	7.700001e-02	2.057050e-02	2.748482e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)   	3.300000e-02	2.352873e-02	3.056098e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)   	7.699993e-02	1.925132e-02	2.107219e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)   	3.299996e-02	3.194506e-02	2.412899e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)   	7.700001e-02	2.519355e-02	2.396728e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)   	3.300000e-02	1.757707e-02	3.191541e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)   	7.700001e-02	1.635826e-02	2.434996e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)   	3.300000e-02	2.665870e-02	2.136640e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)   	1.050000e-01	2.319462e-02	1.738522e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)   	4.499999e-02	2.860067e-02	2.297326e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)   	1.050001e-01	2.619439e-02	1.671266e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)   	4.500002e-02	2.003573e-02	2.345525e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)   	1.050000e-01	2.306359e-02	1.653891e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)   	4.499999e-02	2.997056e-02	2.426218e+01


ENERGY INTEGRATED RESULTS :
	 (0,0,0)	 (-1.1618, -1.6919, -2.8637)	2.199999e-02	3.190609e-02	3.811030e+01
	 (0,0,1)	 (-1.4505, -1.4032, -2.5750)	9.428566e-03	7.246729e-02	2.929492e+01
	 (0,1,0)	 (-1.1957, -1.5561, -3.0334)	2.199999e-02	4.072343e-02	3.461742e+01
	 (0,1,1)	 (-1.4844, -1.2674, -2.7448)	9.428566e-03	5.347741e-02	3.356790e+01
	 (0,2,0)	 (-1.2297, -1.4203, -3.2032)	2.199997e-02	1.344364e-02	3.997396e+01
	 (0,2,1)	 (-1.5183, -1.1316, -2.9145)	9.428557e-03	4.254967e-02	3.518528e+01
	 (0,3,0)	 (-1.2636, -1.2845, -3.3729)	2.199999e-02	4.230648e-02	2.512814e+01
	 (0,3,1)	 (-1.5523, -0.9958, -3.0842)	9.428566e-03	6.049662e-02	2.693267e+01
	 (0,4,0)	 (-1.2976, -1.1487, -3.5426)	2.199999e-02	6.893839e-02	2.294936e+01
	 (0,4,1)	 (-1.5862, -0.8600, -3.2540)	9.428566e-03	3.934075e-02	3.607827e+01
	 (0,5,0)	 (-1.3377, -0.9882, -3.7432)	2.999998e-02	4.087136e-02	2.465120e+01
	 (0,5,1)	 (-1.6264, -0.6996, -3.4546)	1.285713e-02	3.810043e-02	3.145808e+01
	 (0,6,0)	 (-1.3840, -0.8031, -3.9747)	3.000001e-02	4.064726e-02	2.401877e+01
	 (0,6,1)	 (-1.6726, -0.5144, -3.6860)	1.285714e-02	4.851369e-02	2.749151e+01
	 (0,7,0)	 (-1.4303, -0.6179, -4.2061)	2.999998e-02	3.123860e-02	2.851214e+01
	 (0,7,1)	 (-1.7189, -0.3292, -3.9175)	1.285713e-02	4.608170e-02	3.080298e+01
	 (1,0,0)	 (-1.0472, -1.6155, -2.8255)	2.199999e-02	4.953013e-02	2.925655e+01
	 (1,0,1)	 (-1.3359, -1.3268, -2.5368)	9.428566e-03	5.299270e-02	3.088279e+01
	 (1,1,0)	 (-1.0812, -1.4797, -2.9953)	2.199999e-02	4.151582e-02	2.687080e+01
	 (1,1,1)	 (-1.3699, -1.1910, -2.7066)	9.428566e-03	5.966192e-02	2.865448e+01
	 (1,2,0)	 (-1.1151, -1.3439, -3.1650)	2.199997e-02	3.857433e-02	3.029325e+01
	 (1,2,1)	 (-1.4038, -1.0552, -2.8763)	9.428557e-03	7.311171e-02	2.712844e+01
	 (1,3,0)	 (-1.1491, -1.2081, -3.3347)	2.199999e-02	3.048735e-02	2.800654e+01
	 (1,3,1)	 (-1.4378, -0.9195, -3.0460)	9.428566e-03	7.803810e-02	2.928441e+01
	 (1,4,0)	 (-1.1830, -1.0723, -3.5045)	2.199999e-02	5.326624e-02	2.712691e+01
	 (1,4,1)	 (-1.4717, -0.7837, -3.2158)	9.428566e-03	5.612609e-02	2.837483e+01
	 (1,5,0)	 (-1.2231, -0.9119, -3.7051)	2.999998e-02	4.286267e-02	2.715485e+01
	 (1,5,1)	 (-1.5118, -0.6232, -3.4164)	1.285713e-02	5.332145e-02	3.087059e+01
	 (1,6,0)	 (-1.2694, -0.7267, -3.9365)	3.000001e-02	4.023186e-02	2.652799e+01
	 (1,6,1)	 (-1.5581, -0.4380, -3.6478)	1.285714e-02	5.742953e-02	2.773246e+01
	 (1,7,0)	 (-1.3157, -0.5415, -4.1680)	2.999998e-02	4.601941e-02	2.629428e+01
	 (1,7,1)	 (-1.6044, -0.2529, -3.8793)	1.285713e-02	3.897534e-02	3.289925e+01
	 (2,0,0)	 (-0.9327, -1.5391, -2.7873)	2.200007e-02	5.628183e-02	2.698188e+01
	 (2,0,1)	 (-1.2214, -1.2505, -2.4987)	9.428598e-03	2.572745e-02	3.712368e+01
	 (2,1,0)	 (-0.9666, -1.4033, -2.9571)	2.200007e-02	3.464300e-02	2.876152e+01
	 (2,1,1)	 (-1.2553, -1.1147, -2.6684)	9.428598e-03	5.380369e-02	3.335461e+01
	 (2,2,0)	 (-1.0006, -1.2676, -3.1268)	2.200004e-02	3.189575e-02	3.276683e+01
	 (2,2,1)	 (-1.2893, -0.9789, -2.8381)	9.428588e-03	5.541774e-02	3.675585e+01
	 (2,3,0)	 (-1.0345, -1.1318, -3.2965)	2.200007e-02	3.633561e-02	3.491484e+01
	 (2,3,1)	 (-1.3232, -0.8431, -3.0079)	9.428598e-03	5.921727e-02	3.551872e+01
	 (2,4,0)	 (-1.0685, -0.9960, -3.4663)	2.200007e-02	4.003314e-02	3.405292e+01
	 (2,4,1)	 (-1.3572, -0.7073, -3.1776)	9.428598e-03	2.250799e-02	4.340659e+01
	 (2,5,0)	 (-1.1086, -0.8355, -3.6669)	3.000008e-02	4.093365e-02	2.511182e+01
	 (2,5,1)	 (-1.3973, -0.5468, -3.3782)	1.285718e-02	4.194075e-02	4.472247e+01
	 (2,6,0)	 (-1.1549, -0.6503, -3.8983)	3.000011e-02	2.928997e-02	3.214464e+01
	 (2,6,1)	 (-1.4436, -0.3617, -3.6097)	1.285719e-02	5.471236e-02	3.353782e+01
	 (2,7,0)	 (-1.2012, -0.4652, -4.1298)	3.000008e-02	3.593495e-02	3.035763e+01
	 (2,7,1)	 (-1.4899, -0.1765, -3.8411)	1.285718e-02	3.979278e-02	3.727873e+01
	 (3,0,0)	 (-0.8182, -1.4628, -2.7492)	2.199999e-02	6.893339e-02	2.536876e+01
	 (3,0,1)	 (-1.1068, -1.1741, -2.4605)	9.428566e-03	1.118759e-01	2.376286e+01
	 (3,1,0)	 (-0.8521, -1.3270, -2.9189)	2.199999e-02	6.501824e-02	2.496108e+01
	 (3,1,1)	 (-1.1408, -1.0383, -2.6302)	9.428566e-03	2.365106e-02	5.047666e+01
	 (3,2,0)	 (-0.8860, -1.1912, -3.0886)	2.199997e-02	2.427363e-02	3.831070e+01
	 (3,2,1)	 (-1.1747, -0.9025, -2.8000)	9.428557e-03	6.354809e-02	3.324604e+01
	 (3,3,0)	 (-0.9200, -1.0554, -3.2584)	2.199999e-02	3.928473e-02	3.232347e+01
	 (3,3,1)	 (-1.2087, -0.7667, -2.9697)	9.428566e-03	7.139456e-02	2.610697e+01
	 (3,4,0)	 (-0.9539, -0.9196, -3.4281)	2.199999e-02	4.771098e-02	2.658356e+01
	 (3,4,1)	 (-1.2426, -0.6309, -3.1394)	9.428566e-03	7.337197e-02	3.566913e+01
	 (3,5,0)	 (-0.9941, -0.7591, -3.6287)	2.999998e-02	4.551656e-02	3.257889e+01
	 (3,5,1)	 (-1.2827, -0.4705, -3.3400)	1.285713e-02	3.781422e-02	3.573361e+01
	 (3,6,0)	 (-1.0404, -0.5740, -3.8601)	3.000001e-02	3.996544e-02	2.965435e+01
	 (3,6,1)	 (-1.3290, -0.2853, -3.5715)	1.285714e-02	1.966227e-02	5.526265e+01
	 (3,7,0)	 (-1.0866, -0.3888, -4.0916)	2.999998e-02	2.953586e-02	3.478765e+01
	 (3,7,1)	 (-1.3753, -0.1001, -3.8029)	1.285713e-02	2.449479e-02	3.697760e+01
	 (4,0,0)	 (-0.7036, -1.3864, -2.7110)	2.199999e-02	6.564639e-02	2.538593e+01
	 (4,0,1)	 (-0.9923, -1.0977, -2.4223)	9.428566e-03	3.117264e-02	3.537310e+01
	 (4,1,0)	 (-0.7376, -1.2506, -2.8807)	2.199999e-02	3.689553e-02	3.069267e+01
	 (4,1,1)	 (-1.0262, -0.9620, -2.5920)	9.428566e-03	4.731891e-02	3.394206e+01
	 (4,2,0)	 (-0.7715, -1.1148, -3.0505)	2.199997e-02	3.403881e-02	2.765796e+01
	 (4,2,1)	 (-1.0602, -0.8262, -2.7618)	9.428557e-03	7.891451e-02	3.198223e+01
	 (4,3,0)	 (-0.8055, -0.9791, -3.2202)	2.199999e-02	6.825365e-02	2.411342e+01
	 (4,3,1)	 (-1.0941, -0.6904, -2.9315)	9.428566e-03	6.100426e-02	3.397909e+01
	 (4,4,0)	 (-0.8394, -0.8433, -3.3899)	2.199999e-02	3.466711e-02	2.935126e+01
	 (4,4,1)	 (-1.1281, -0.5546, -3.1012)	9.428566e-03	7.905662e-02	3.280871e+01
	 (4,5,0)	 (-0.8795, -0.6828, -3.5905)	2.999998e-02	4.359325e-02	2.350517e+01
	 (4,5,1)	 (-1.1682, -0.3941, -3.3018)	1.285713e-02	7.328568e-02	2.728813e+01
	 (4,6,0)	 (-0.9258, -0.4976, -3.8220)	3.000001e-02	5.927604e-02	2.520615e+01
	 (4,6,1)	 (-1.2145, -0.2089, -3.5333)	1.285714e-02	4.285787e-02	3.312732e+01
	 (4,7,0)	 (-0.9721, -0.3125, -4.0534)	2.999998e-02	3.443229e-02	2.875762e+01
	 (4,7,1)	 (-1.2608, -0.0238, -3.7647)	1.285713e-02	4.422174e-02	3.310240e+01
	 (5,0,0)	 (-0.5891, -1.3101, -2.6728)	2.199999e-02	2.604686e-02	3.485256e+01
	 (5,0,1)	 (-0.8777, -1.0214, -2.3841)	9.428566e-03	3.424298e-02	4.079405e+01
	 (5,1,0)	 (-0.6230, -1.1743, -2.8425)	2.199999e-02	2.263904e-02	3.251575e+01
	 (5,1,1)	 (-0.9117, -0.8856, -2.5539)	9.428566e-03	6.662432e-02	3.157820e+01
	 (5,2,0)	 (-0.6570, -1.0385, -3.0123)	2.199997e-02	6.218857e-02	2.111895e+01
	 (5,2,1)	 (-0.9456, -0.7498, -2.7236)	9.428557e-03	6.674199e-02	2.781637e+01
	 (5,3,0)	 (-0.6909, -0.9027, -3.1820)	2.199999e-02	4.152849e-02	2.658835e+01
	 (5,3,1)	 (-0.9796, -0.6140, -2.8933)	9.428566e-03	7.248425e-02	3.092186e+01
	 (5,4,0)	 (-0.7249, -0.7669, -3.3517)	2.199999e-02	3.956310e-02	3.212784e+01
	 (5,4,1)	 (-1.0135, -0.4782, -3.0631)	9.428566e-03	4.855399e-02	3.407808e+01
	 (5,5,0)	 (-0.7650, -0.6064, -3.5523)	2.999998e-02	4.497676e-02	2.490962e+01
	 (5,5,1)	 (-1.0537, -0.3178, -3.2637)	1.285713e-02	3.105644e-02	3.963530e+01
	 (5,6,0)	 (-0.8113, -0.4213, -3.7838)	3.000001e-02	2.448670e-02	2.975520e+01
	 (5,6,1)	 (-1.0999, -0.1326, -3.4951)	1.285714e-02	3.483747e-02	3.637259e+01
	 (5,7,0)	 (-0.8576, -0.2361, -4.0152)	2.999998e-02	2.516175e-02	2.799137e+01
	 (5,7,1)	 (-1.1462, 0.0526, -3.7266)	1.285713e-02	3.741823e-02	3.440497e+01
	 (6,0,0)	 (-0.4745, -1.2337, -2.6346)	2.199999e-02	3.881559e-02	2.419289e+01
	 (6,0,1)	 (-0.7632, -0.9450, -2.3459)	9.428566e-03	4.417356e-02	3.820737e+01
	 (6,1,0)	 (-0.5085, -1.0979, -2.8044)	2.199999e-02	4.451727e-02	2.799911e+01
	 (6,1,1)	 (-0.7972, -0.8092, -2.5157)	9.428566e-03	3.547465e-02	3.492235e+01
	 (6,2,0)	 (-0.5424, -0.9621, -2.9741)	2.199997e-02	3.244749e-02	2.628499e+01
	 (6,2,1)	 (-0.8311, -0.6734, -2.6854)	9.428557e-03	6.659256e-02	3.218400e+01
	 (6,3,0)	 (-0.5764, -0.8263, -3.1438)	2.199999e-02	4.699783e-02	2.993575e+01
	 (6,3,1)	 (-0.8650, -0.5377, -2.8551)	9.428566e-03	6.655407e-02	2.774062e+01
	 (6,4,0)	 (-0.6103, -0.6905, -3.3136)	2.199999e-02	4.350419e-02	3.394352e+01
	 (6,4,1)	 (-0.8990, -0.4019, -3.0249)	9.428566e-03	3.927852e-02	3.958061e+01
	 (6,5,0)	 (-0.6504, -0.5301, -3.5142)	2.999998e-02	3.187444e-02	2.607352e+01
	 (6,5,1)	 (-0.9391, -0.2414, -3.2255)	1.285713e-02	3.753218e-02	4.541649e+01
	 (6,6,0)	 (-0.6967, -0.3449, -3.7456)	3.000001e-02	2.427321e-02	3.199824e+01
	 (6,6,1)	 (-0.9854, -0.0562, -3.4569)	1.285714e-02	4.784054e-02	3.364403e+01
	 (6,7,0)	 (-0.7430, -0.1597, -3.9771)	2.999998e-02	2.644346e-02	3.328183e+01
	 (6,7,1)	 (-1.0317, 0.1289, -3.6884)	1.285713e-02	3.902884e-02	3.390155e+01
	 (7,0,0)	 (-0.2168, -1.0619, -2.5487)	7.700001e-02	5.520944e-02	1.827077e+01
	 (7,0,1)	 (-0.5055, -0.7732, -2.2600)	3.300000e-02	8.432886e-02	1.701870e+01
	 (7,1,0)	 (-0.2508, -0.9261, -2.7185)	7.700001e-02	5.019347e-02	1.853236e+01
	 (7,1,1)	 (-0.5394, -0.6374, -2.4298)	3.300000e-02	5.255047e-02	1.700961e+01
	 (7,2,0)	 (-0.2847, -0.7903, -2.8882)	7.699993e-02	4.435181e-02	1.648371e+01
	 (7,2,1)	 (-0.5734, -0.5016, -2.5995)	3.299996e-02	4.823592e-02	1.921662e+01
	 (7,3,0)	 (-0.3187, -0.6545, -3.0579)	7.700001e-02	4.276824e-02	1.596589e+01
	 (7,3,1)	 (-0.6073, -0.3658, -2.7692)	3.300000e-02	4.104101e-02	1.644011e+01
	 (7,4,0)	 (-0.3526, -0.5187, -3.2277)	7.700001e-02	3.704368e-02	1.571765e+01
	 (7,4,1)	 (-0.6413, -0.2301, -2.9390)	3.300000e-02	5.716864e-02	1.690459e+01
	 (7,5,0)	 (-0.3927, -0.3583, -3.4282)	1.050000e-01	4.301719e-02	1.712823e+01
	 (7,5,1)	 (-0.6814, -0.0696, -3.1396)	4.499999e-02	5.651493e-02	1.760660e+01
	 (7,6,0)	 (-0.4390, -0.1731, -3.6597)	1.050001e-01	4.423362e-02	1.576799e+01
	 (7,6,1)	 (-0.7277, 0.1156, -3.3710)	4.500002e-02	5.276215e-02	1.468623e+01
	 (7,7,0)	 (-0.4853, 0.0121, -3.8912)	1.050000e-01	3.836547e-02	1.393376e+01
	 (7,7,1)	 (-0.7740, 0.3007, -3.6025)	4.499999e-02	3.100408e-02	2.062348e+01
	 (8,0,0)	 (0.1841, -0.7946, -2.4151)	7.700001e-02	4.814751e-02	1.468222e+01
	 (8,0,1)	 (-0.1046, -0.5059, -2.1264)	3.300000e-02	6.208944e-02	1.812821e+01
	 (8,1,0)	 (0.1501, -0.6588, -2.5848)	7.700001e-02	5.519758e-02	1.275646e+01
	 (8,1,1)	 (-0.1385, -0.3702, -2.2961)	3.300000e-02	4.918165e-02	2.364726e+01
	 (8,2,0)	 (0.1162, -0.5230, -2.7546)	7.699993e-02	4.563354e-02	1.700194e+01
	 (8,2,1)	 (-0.1725, -0.2344, -2.4659)	3.299996e-02	3.929699e-02	2.177297e+01
	 (8,3,0)	 (0.0822, -0.3873, -2.9243)	7.700001e-02	3.487348e-02	1.792084e+01
	 (8,3,1)	 (-0.2064, -0.0986, -2.6356)	3.300000e-02	4.923856e-02	1.936937e+01
	 (8,4,0)	 (0.0483, -0.2515, -3.0940)	7.700001e-02	3.597755e-02	1.634812e+01
	 (8,4,1)	 (-0.2404, 0.0372, -2.8053)	3.300000e-02	2.967361e-02	2.318916e+01
	 (8,5,0)	 (0.0082, -0.0910, -3.2946)	1.050000e-01	2.914371e-02	2.010486e+01
	 (8,5,1)	 (-0.2805, 0.1977, -3.0059)	4.499999e-02	4.078848e-02	2.006298e+01
	 (8,6,0)	 (-0.0381, 0.0942, -3.5261)	1.050001e-01	2.954104e-02	1.591733e+01
	 (8,6,1)	 (-0.3268, 0.3828, -3.2374)	4.500002e-02	4.488491e-02	1.750121e+01
	 (8,7,0)	 (-0.0844, 0.2793, -3.7575)	1.050000e-01	4.184553e-02	1.345880e+01
	 (8,7,1)	 (-0.3731, 0.5680, -3.4689)	4.499999e-02	3.636463e-02	1.922996e+01
	 (9,0,0)	 (0.5850, -0.5274, -2.2815)	7.700001e-02	4.425004e-02	1.741765e+01
	 (9,0,1)	 (0.2963, -0.2387, -1.9928)	3.300000e-02	4.160121e-02	2.033251e+01
	 (9,1,0)	 (0.5510, -0.3916, -2.4512)	7.700001e-02	4.219445e-02	1.468492e+01
	 (9,1,1)	 (0.2623, -0.1029, -2.1625)	3.300000e-02	4.556461e-02	2.432258e+01
	 (9,2,0)	 (0.5171, -0.2558, -2.6209)	7.699993e-02	3.715472e-02	1.775666e+01
	 (9,2,1)	 (0.2284, 0.0329, -2.3322)	3.299996e-02	4.546499e-02	2.218970e+01
	 (9,3,0)	 (0.4831, -0.1200, -2.7907)	7.700001e-02	2.995361e-02	2.047045e+01
	 (9,3,1)	 (0.1945, 0.1687, -2.5020)	3.300000e-02	3.492381e-02	2.462350e+01
	 (9,4,0)	 (0.4492, 0.0158, -2.9604)	7.700001e-02	3.021970e-02	2.182929e+01
	 (9,4,1)	 (0.1605, 0.3045, -2.6717)	3.300000e-02	4.573434e-02	2.360243e+01
	 (9,5,0)	 (0.4091, 0.1763, -3.1610)	1.050000e-01	3.147402e-02	1.810748e+01
	 (9,5,1)	 (0.1204, 0.4649, -2.8723)	4.499999e-02	4.499688e-02	1.882671e+01
	 (9,6,0)	 (0.3628, 0.3614, -3.3924)	1.050001e-01	3.620064e-02	1.553997e+01
	 (9,6,1)	 (0.0741, 0.6501, -3.1038)	4.500002e-02	3.205390e-02	2.159771e+01
	 (9,7,0)	 (0.3165, 0.5466, -3.6239)	1.050000e-01	2.681307e-02	1.541747e+01
	 (9,7,1)	 (0.0278, 0.8353, -3.3352)	4.499999e-02	3.627106e-02	1.846952e+01
	 (10,0,0)	 (0.9859, -0.2601, -2.1478)	7.700001e-02	2.749614e-02	1.995610e+01
	 (10,0,1)	 (0.6972, 0.0286, -1.8592)	3.300000e-02	2.563397e-02	2.912318e+01
	 (10,1,0)	 (0.9519, -0.1243, -2.3176)	7.700001e-02	3.083228e-02	2.151152e+01
	 (10,1,1)	 (0.6632, 0.1644, -2.0289)	3.300000e-02	2.542474e-02	2.876304e+01
	 (10,2,0)	 (0.9180, 0.0115, -2.4873)	7.699993e-02	2.756238e-02	1.890128e+01
	 (10,2,1)	 (0.6293, 0.3002, -2.1986)	3.299996e-02	3.943705e-02	2.386451e+01
	 (10,3,0)	 (0.8840, 0.1473, -2.6570)	7.700001e-02	3.647844e-02	1.931230e+01
	 (10,3,1)	 (0.5953, 0.4359, -2.3684)	3.300000e-02	2.350422e-02	2.895670e+01
	 (10,4,0)	 (0.8501, 0.2831, -2.8268)	7.700001e-02	2.925599e-02	1.853566e+01
	 (10,4,1)	 (0.5614, 0.5717, -2.5381)	3.300000e-02	3.836878e-02	1.915776e+01
	 (10,5,0)	 (0.8100, 0.4435, -3.0274)	1.050000e-01	3.597398e-02	1.544691e+01
	 (10,5,1)	 (0.5213, 0.7322, -2.7387)	4.499999e-02	3.979649e-02	1.895238e+01
	 (10,6,0)	 (0.7637, 0.6287, -3.2588)	1.050001e-01	3.391084e-02	1.782824e+01
	 (10,6,1)	 (0.4750, 0.9174, -2.9701)	4.500002e-02	3.006821e-02	2.090744e+01
	 (10,7,0)	 (0.7174, 0.8139, -3.4903)	1.050000e-01	3.224454e-02	1.488840e+01
	 (10,7,1)	 (0.4287, 1.1025, -3.2016)	4.499999e-02	4.222194e-02	2.137258e+01

number of batches used: 50	4.034821e-02	2.895010e+00


 simulation time (s) : 3


 Type and parameters of random generator at the end of simulation: 
	 DRAND48_RANDOM 6549 27792 56097  COUNTER	1896842


=====================================================================
	NORMAL COMPLETION
=====================================================================
