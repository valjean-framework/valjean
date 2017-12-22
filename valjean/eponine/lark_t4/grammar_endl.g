// SCORE DESCRIPTION
// scoremode : "scoring mode :" + WORD
// scoremode : WORD WORD ":" rusword
// scoremode : NAME NAME ":" NAME
// mesh : "(" NUMBER "," NUMBER "," NUMBER ")" FLOAT FLOAT
scoremode : "scoring" "mode" ":" name _NEWLINE
// scorezone : "scoring" "zone" ":" sentence ":" name name quantitywunit
// scorezone : "scoring" "zone" ":" sentence ":" // name quantity quantity
// !resonmesh : "Results" "on" "a" "mesh"
// scorezone : "scoring" "zone" ":" ( sentence | resonmesh ) ":" name quantity quantity
// scorezone : "scoring" "zone" ":" ( resonmesh | sentence ) ":" // name quantity quantity
scoremesh : "Results" "on" "a" "mesh" ":" _NEWLINE name quantity quantity _NEWLINE
scoreallgeom : "Results" "cumulated" "on" "all" "geometry" _NEWLINE
scoresurf : name+ "volumes" ":" int ("," int)* _NEWLINE ["Surface" "in" "cm2" ":" float _NEWLINE]
scorevol : "Volume" "num" "of" "volume" ":" int _NEWLINE "Volume" "in" "cm3" ":" float _NEWLINE
// scorezone : "scoring" "zone" ":" sentence ":" name quantity quantity
scorezone : "scoring" "zone" ":" ( scoremesh | scoreallgeom | scoresurf | scorevol )
quantitywunit : name "(" name ")" | sigma "(" name ")"
quantity : name | quantitywunit // | name "(" name ")"
scoredesc : scoremode scorezone

// MESH
energyunit : "Energy" "range" "(" "in" NAME ")" ":"  -> unit
eunit : NAME
emax : FLOAT
emin : FLOAT
energyvals : emax "-" emin
// energyvals : FLOAT "-" FLOAT
// energyline : energyunit energyvals
energyperrange : "Energy" "range" "(" "in" eunit ")" ":" emax "-" emin
energyintegrated : energyintegratedreskw ":" -> integratedenergy
energyline : ( energyintegrated | energyperrange ) _NEWLINE
// energyline : "Energy" "range" "(" "in" name ")" ":" FLOAT "-" FLOAT
meshdesc : "(" [int ("," int)*] ")"
// meshdesc : "(" int "," int "," int ")"
// mesh : "(" int "," int "," int ")" float float
mesh : meshdesc float float _NEWLINE
meshvals : mesh+
meshblock : energyline meshvals -> meshblock
listmeshblock : [meshblock ( meshblock)*]  -> listmeshblock

// Entropy
boltzmannentropy : "Boltzmann" "Entropy" "of" "sources" "=" float _NEWLINE -> bentropy
shannonentropy : "Shannon" "Entropy" "of" "sources" "=" float _NEWLINE -> sentropy
summaryentropy : boltzmannentropy shannonentropy

// Save MED files
filecreation : "Creating" "MED" "output" "file" ":" name _NEWLINE
filename : "MED" "mesh" "id" name _NEWLINE
savemed : filecreation filename

// SPECTRUM
spectrumkw : "SPECTRUM" "RESULTS" _NEWLINE
group : name "(" name ")"
spectrumdesc : group name name name _NEWLINE -> spectrumdesc
spectrumbin : float "-" float -> spectrumbin
spectrum : spectrumbin float float float _NEWLINE
spectrumvals : spectrum+
spectrumblock : spectrumkw numfdiscardedbatch spectrumdesc spectrumvals -> spectrumblock

// KEFFS
keffres : name float float _NEWLINE -> keffres
keffvals : keffres+
keffresblock : keffvals -> keffresblock
_correlationdesc : "estimators" "correlations" "combined" "values" "combined" "sigma%" _NEWLINE  //(name|sigma|sigmapc)*
// _correlationdesc : "estimators" (name|sigma|sigmapc)*
// correlationdesc : sentence
correlationestim : name "<->" name -> estimators
correlationvals : ( float | notconverged_kw )+
correlation : correlationestim correlationvals _NEWLINE
correlations : correlation+
correlationblock : _correlationdesc correlations -> correlationblock
fullcombestim : "full" "combined" "estimator" ( float float | notconverged_kw ) -> fullcombestim
defkeffblock : ( keffresblock correlationblock fullcombestim | notconverged_kw ) _NEWLINE
bestresestim : name+ "ESTIMATOR" _NEWLINE
bestresdiscbatch :  "best" "results" "are" "obtained" "with" "discarding" int "batches" _NEWLINE
bestkeff : "keff" "=" float sigma "=" float sigmapc "=" float -> bestkeff
// bestrespestim : ( bestresdiscbatch numbatchused bestkeff | notconverged_kw )
bestrespestim : ( notconverged_kw | bestresdiscbatch numbatchused bestkeff ) _NEWLINE
bestres : bestresestim _MINUSLINE _NEWLINE bestrespestim -> bestres
bestresblock : bestres+
keffresp : energyintegratedreskw _NEWLINE numbatchused _NEWLINE defkeffblock bestresblock

// DEFAULT INTEGRATED RESULT
integratedresline : (numbatchused integratedres | notconverged_kw)  _NEWLINE
defintegratedres : [energyintegratedreskw _NEWLINE] [numfdiscardedbatch] integratedresline
// defintegratedres : [energyintegratedreskw _NEWLINE] [numfdiscardedbatch] ( numbatchused integratedres | notconverged_kw ) _NEWLINE

// GENERALITIES
energyintegratedreskw : "ENERGY" "INTEGRATED" "RESULTS"
// numbatchused : "number" "of" "batches" "used" ":" int float float -> usedbatches
numbatchused : "number" "of" ("batches"|"batch") "used" ":" int -> usedbatches
integratedres : float float -> integratedres
numfdiscardedbatch : "number" "of" "first" "discarded" "batches" ":" int _NEWLINE -> discardedbatchs
notconverged_kw : "NOT" "YET" "CONVERGED" | "Not" "converged" | "not" "converged"

responsefunc : "RESPONSE" "FUNCTION" ":" sentence ["("sentence")"]_NEWLINE
responsename : "RESPONSE" "NAME" ":" [name] _NEWLINE
scorename : "SCORE" "NAME" ":" name _NEWLINE
energysplitname : "ENERGY" "DECOUPAGE" "NAME" ":" name _NEWLINE
particle : ("PARTICULE"|"PARTICLE") ":" sentence _NEWLINE
reactiononnucl : "reaction" "on" "nucleus" ":" name [_NEWLINE] -> reacnucl
temperature : "temperature" ":" int _NEWLINE -> temperature
composition : "composition" ":" name _NEWLINE -> composition
concentration : "concentration" ":" float _NEWLINE -> concentration
reaction : "reaction" "consists" "in" ( name [":"] [_NEWLINE] int | name+ ) _NEWLINE -> reaction
carac : particle | reactiononnucl | temperature | composition | concentration | reaction

responsedesc : responsefunc [responsename] [scorename] [energysplitname] carac*

// responseformat : (listmeshblock | summaryentropy | spectrumblock | defintegratedres)
responseformat : scoredesc | meshblock | summaryentropy | spectrumblock | keffresp | defintegratedres | savemed

// response : responsedesc starline scoremode scorezone listmeshblock [summaryentropy] spectrumblock [defintegratedres]
// numbatchused

// response : starline responsedesc starline [scoredesc] responseformat+
response : starline responsedesc starline responseformat+

// Optional intro
batchnum : "batch" "number" ":" int _NEWLINE
quotasent : "quota" "sampling" "and" name+ ":" _NEWLINE
meannumcollisionspneut : "mean" "number" "of" "collision" "per" "neutron" "history" ":" float "sigma_n" ":" float _NEWLINE
numpartsec : "number" "of" "secondary" "particules" ":" int _NEWLINE
numfissionneut : "number" "of" "fission" "neutrons" ":" int _NEWLINE
keffatstep : "KEFF" "at" "step" ":" int _NEWLINE "keff" "=" float sigma ":" float _NEWLINE

optintro : batchnum quotasent meannumcollisionspneut numpartsec numfissionneut keffatstep [numbatchused _NEWLINE ] starline

// INTRO
// sourceintensity : _WS "RESULTS ARE GIVEN FOR SOURCE INTENSITY :" _WS float
// sourceintensity : _WS "RESULTS" _WS "ARE" _WS "GIVEN" _WS "FOR" _WS "SOURCE" _WS "INTENSITY" _WS ":" _WS float
sourceintensity : "RESULTS" "ARE" "GIVEN" "FOR" "SOURCE" "INTENSITY" ":" float _NEWLINE
// sourceintensity :  "RESULTS ARE GIVEN FOR SOURCE INTENSITY :" float
meanwghtleak : "Mean" "weight" "leakage" "=" float
sigmawgtleak : sigma "=" float -> sigwl
sigmapcwgtleak : sigmapc "=" (float | int) -> sigpcwl
mwl : meanwghtleak sigmawgtleak sigmapcwgtleak _NEWLINE

edbatchnum : "Edition" "after" "batch" "number" ":" int _NEWLINE

intro : [optintro] [_NEWLINE] sourceintensity starline mwl [edbatchnum]

// END OF RESUTLS BLOCK
simtime : "simulation" "time" "(" "s" ")" ":" int _NEWLINE -> simtime
rdmgen_sentkw : "Type" "and" "parameters" sentence ("simulation" | "before" "batch" int)":" _NEWLINE
rdmgenres : name int int int name int
rdmblock : rdmgen_sentkw rdmgenres _NEWLINE
normalcompletion : _EQUALLINE "NORMAL" "COMPLETION" _NEWLINE _EQUALLINE

// conclu : [simtime] [rdmblock]
conclu : simtime | rdmblock

resultsblock : intro response+ conclu*

test : resultsblock+ [normalcompletion]

onlymesh : meshvals



sigma : "sigma"
sigmapc : "sigma%"

!commonword : "on"|"in"|"a"|"an"|"for"|"of"|"batch"|"at"|"ENERGY"|"all"

// scoremode : WORD WORD ":" WORD

// string : STRING
// rusword : WORD? "_" WORD?
// rusword : /[a-zA-Z_]+/
// NAME: /[a-zA-Z_]\w*/
// NAME: /\w+/
sentence : (name | commonword)*
// var : (VAR1 | VAR2)
// VAR1: /[a-zA-Z_]*\/[a-zA-Z_]*/
// VAR2: /[a-zA-Z_][a-zA-Z_]*%/
name: NAME
NAME: /[a-zA-Z_][a-zA-Z0-9_\/%.]*/

starline: _STARLINE // _NEWLINE
_STARLINE: /[*]+[\n]+/
_MINUSLINE: /[-]+/
_EQUALLINE: /[=]+[\n]+/
// _SPACES: /[\n\t\r]+/
// _WS : /[ \t]+/
_NEWLINE : /[\n]+/
// WS : /[ ]/
int: INT
float: FLOAT
// WORD: /[a-zA-Z]+/
// word : WORD

%import common.ESCAPED_STRING   -> STRING
// %import common.SIGNED_NUMBER    -> NUMBER
%import common.FLOAT            -> FLOAT
%import common.SIGNED_INT              -> INT
// %ignore /[\n\t\r]+/
// %import common.WORD
// %import common.WS
// %ignore WS
%import common.WS_INLINE
%ignore WS_INLINE
// %ignore STARLINE
