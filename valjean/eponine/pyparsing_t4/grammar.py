# pylint: disable=too-many-lines
r'''This module provides `pyparsing` grammar for Tripoli-4 output listings.

.. _pyparsing_wiki: http://pyparsing.wikispaces.com/
.. _pyparsing_pip: https://pypi.python.org/pypi/pyparsing/2.2.0
.. |keff| replace:: k\ :sub:`eff`
.. |kij| replace:: k\ :sub:`ij`
.. role :: parsing_var(attr)

Documentation on **pyparsing** package can be found in `pyparsing`_
documentation linked to `pyparsing_pip`_ and on `pyparsing_wiki`_ with
examples.

Transformation from `pyparsing.ParseResults` to more standard python objects,
including `numpy` ones,is done with :mod:`~.transform`, calling
:mod:`common <valjean.eponine.common>`.

Generalitites
-------------

* This parser only parses the result part of the listing (selection done in
  :mod:`scan_t4 <valjean.eponine.scan_t4>`).
* It takes into account all responses in ``qualtrip`` database up to Tripoli-4,
  version 10.2.
* If a response is not taken into account parsing will fail:

  * with a big, ugly message ending by location of the end of successful
    parsing in the result string (possible to print it) → normally where starts
    your new response
  * it seems to end normally, but did not in reality. One of the best checks in
    that case is to test if the ``endflag`` in :mod:`scan_t4
    <valjean.eponine.scan_t4>` was read in the parser, usually not. Then the
    new response probably have to be added.

* A general parser is proposed for use in the file, but other parsers can be
  built from the partial parsers written here
* Numbers are automatically converted to `numpy` numbers (possibility to choose
  the dtype used for numbers)
* Keywords and most of the variables used to build parsers are private


Organisation
------------

This module is divided in 3 parts:

keywords:
  list of all keywords used to parse the listings, this part is
  important as these keywords trigger the parsing
parsers:
  parsers for each part of the listing (introduction, mesh,
  spectra, general responses, |keff|, etc.)
general parser:
  parser to parse the full listing, taking into accout all
  current response (present in V&V)

Keywords are in most of the cases used as flags and suppressed when data are
stored.

A first structure is designed when building the parsers results as lists and
dictionaries in the `pyparsing.ParseResults`. Then "parse actions" are used
to standard python or :obj:`numpy` objects. These *parse actions*, called with
`pyparsing.ParserElement.setParseAction`, can be found in :mod:`~.transform`.

Main parsers blocks
```````````````````
The main parsers blocks are defined at the end of the file, see
``mygram`` and ``response``.

Typically, each result block in the listing should start by the `intro` block
and end with at least one `runtime` block. This parts follows the :mod:`scan_t4
<valjean.eponine.scan_t4>`: `string` starting by ``'RESULTS ARE GIVEN'`` and
ending with ``'simulation time'``, ``'exploitation time'`` or
``'elapsed time'``.

Between these blocks can be found the data blocks. The major ones are:

* one or more responses, driven by the keyword ``'RESPONSE FUNCTION'``,
* the editions of IFP adjoint criticality,
* the "default" |keff| block, in most of the cases at the end of the listing,
* the *contributing particles block*, mainly in first pass listings,
* the perturbation block,
* an optional additional ``runtime`` block.

Main data blocks are described below (results taken into account, main
features).

Response blocks
```````````````
The core of the listings is the list of responses, including all the required
scores. This big block is constructed as a **list** of **dictionaries**, each
one representing a response (key ``'list_responses'`` in the final result).

Response are constructed as:

* response introduction containing its definition:

  * a description of the response, ``respdesc`` including:

    * ``'RESPONSE FUNCTION'`` keyword as mandatory (afak)
    * ``'RESPONSE NAME'``, ``'SCORE NAME'`` and ``'ENERGY DECOUPAGE NAME'``
      that are present in most of the cases

  * more characteristics of the response, stored under `respcarac`,
    like:

    * considered particle (``'PARTICULE'`` in the listing)
    * nucleus on which the reaction happens (if ``'RESPONSE FUNCTION'`` is a
      ``'REACTION'``)
    * temperature
    * compostion of the volumes considered
    * concentration
    * reaction considered (usually given as codes)
    * others like DPA type, required arguments, mode, filters, etc.

* responses themselves, various:

  * responses including *score* description, all included in the ``scoreblock``
    parser (more than one can be present):

    * score description (``scoredesc``) contains the score mode (``'TRACK'``,
      ``'SURF'`` or ``'COLL'``) and the score zone (currently taken into
      account: mesh, results cumulated on all geometry or on all sources,
      Volume, Volume Sum, Frontier, Frontier Sum, Point, Cells and Maille)

    * results block, where at least one of these results can be found:

      * :parsing_var:`spectrumblock`: spectrum
      * :parsing_var:`meshblock`: mesh
      * :parsing_var:`vovspectrumblock`: spectrum with variance of variance
      * :parsing_var:`entropy`: entropy results (Boltzmann and Shannon
        entropies)
      * :parsing_var:`medfile`: location of optional MED file
      * :parsing_var:`defintegratedres`: default result integrated over energy
      * :parsing_var:`uncertblock`: uncertainty results
      * :parsing_var:`uncertintegblock`: uncertainties on integrated results
        over energy
      * :parsing_var:`gbblock`: Green bands results

  * |keff| presented as a generic response, possibly transformed in
    :obj:`numpy.matrix` (:parsing_var:`keffblock`)
  * |kij| results: matrix, eigenvalues, eigenvectors (:parsing_var:`kijres`)
  * |kij| sources (:parsing_var:`kijsources`)
  * ordered results (in nucleus and/or family (:parsing_var:`orderedres`)
  * default result integrated over energy where no scoring mode and zone are
    precised (:parsing_var:`defintegratedres`)
  * IFP results (:parsing_var:`ifpblock`)
  * perturbation results (:parsing_var:`perturbation`)


Other blocks
````````````
Various other blocks can appear in the Tripoli-4 listing, located at the level
of the responses block, identified by the key ``'list_responses'``. Other
possibilities are:

* :parsing_var:`ifpadjointcriticality`: edition of IFP adjoint criticality,
* :parsing_var:`defkeffblock`: "default" |keff| block, containing for example
  the best estimation of |keff| using variable number of discarded batches,
* :parsing_var:`contribpartblock`: *contributing particles block*,
* :parsing_var:`perturbation`: perturbation results, containing a description
  of the calculation of the perturbation followed by the perturbation result
  presented like a usual response (spectrum, mesh, etc. depending on required
  score),
* :parsing_var:`runtime`: simulation, exploitation or elapsed time.

.. _link to grammar: ../../_modules/valjean/eponine/pyparsing_t4/grammar.html

Et le lien vers le code: `link to grammar`_.

.. todo:: need to test with "fake" outputs from Tripoli-4 (to be thought)

'''

import logging
from pyparsing import (Word, Keyword, White, alphas, alphanums,
                       Suppress, Optional, LineEnd, LineStart,
                       Group, OneOrMore, ZeroOrMore, Forward,
                       tokenMap)
from pyparsing import pyparsing_common as pyparscom
from . import transform as trans


LOGGER = logging.getLogger('valjean')

_fnums = pyparscom.fnumber.setParseAction(tokenMap(trans.common.FTYPE))
_inums = pyparscom.number.setParseAction(tokenMap(trans.common.ITYPE))

###################################
#            KEYWORDS             #
###################################

# General keywords
_integratedres_kw = Keyword("ENERGY INTEGRATED RESULTS")
_numbatchsused_kw = (Keyword("number of")
                     + (Keyword("batches") | Keyword("batch"))
                     + Optional(Keyword("used")))
_numbatchs1stdiscarded_kw = Keyword("number of first discarded batches")
_notconverged_kw = (Keyword("NOT YET CONVERGED") | Keyword("Not converged")
                    | Keyword("not converged"))
_unknown_kw = Keyword("unknown")
_unavailable_kw = Keyword("unavailable")
_units_kw = Keyword("Units:")
_endtable = LineEnd() + LineEnd()

# Introduction keywords
_sourceintensity_kw = Keyword("RESULTS ARE GIVEN FOR SOURCE INTENSITY")
_meanweightleakage_kw = Keyword("Mean weight leakage")
_edbatchnum_kw = Keyword("Edition after batch number")
_meanweightrestartpart_kw = Keyword("Mean weight of restarted particles :")

# End of edition keywords
_simulationtime_kw = Keyword("simulation time (s)")
_exploitationtime_kw = Keyword("exploitation time (s)")
_elapsedtime_kw = Keyword("elapsed time (s)")
_rdmgenerator_kw = Keyword("Type and parameters of random generator "
                           "at the end of simulation")
# _rdmgenerator_kw = Keyword("Type and parameters of random generator" +
# ("at the end of simulation"|"after batch"))
_normalcompletion_kw = Keyword("NORMAL COMPLETION")

# Response description keywords
_respfunction_kw = Keyword("RESPONSE FUNCTION")
_respname_kw = Keyword("RESPONSE NAME")
_scorename_kw = Keyword("SCORE NAME")
_energysplitname_kw = Keyword("ENERGY DECOUPAGE NAME")
_particule_kw = Keyword("PARTICULE")
_incparticle_kw = Keyword("INCIDENT PARTICULE")
_reactiononnucl_kw = Keyword("reaction on nucleus")
_temperature_kw = Keyword("temperature")
_composition_kw = Keyword("composition")
_concentration_kw = Keyword("concentration")
_reaction_kw = Keyword("reaction consists in")
_required_kw = Keyword("REQUIRED")
_dpatype_kw = Keyword("DPA TYPE:")
_mode_kw = Keyword("MODE :")
_inducedbyint_kw = Keyword("INDUCED BY INTERACTION :")
_fxptcontrib_kw = Keyword("FXPT CONTRIBUTION")
_spectrumresp_kw = Keyword("SPECTRUM")
_filters_kw = Keyword("Score filtered by volume")

# Scoring description
_scoremode_kw = Keyword("scoring mode")
_scorezone_kw = Keyword("scoring zone")
_scoremesh_kw = Keyword("Results on a mesh")
_scoreallgeom_kw = Keyword("Results cumulated on all geometry")
_scoreallsources_kw = Keyword("Results cumulated on all sources")
_scorevol_kw = Keyword("Volume")
_scorevolvol_kw = Keyword("num of volume")
_scorevolume_kw = Keyword("Volume in cm3")
_scorevolsum_kw = Keyword("Volume Sum")
_scorevolsumvol_kw = Keyword("num of volumes")
_scorevolumesum_kw = Keyword("Total volume in cm3")
_scoresurf_kw = Keyword("Frontier")
_scoresurfvol_kw = Keyword("volumes")
_scoresurface_kw = Keyword("Surface in cm2")
_scoresurfsum_kw = Keyword("Frontier Sum")
_scoresurfsumfront_kw = Keyword("num of frontiers")
_scoresurfacesum_kw = Keyword("Total surface in cm2")
_scorepoint_kw = Keyword("Point")
_scorecell_kw = Keyword("Cells")
_scorecelldet_kw = Keyword("(numvol,depth,imaille,jmaille,kmaille...)")
_scoremaille_kw = Keyword("Maille")
_scoremaillevol_kw = Keyword("num of volume")
_scoremailledepth_kw = Keyword("depth of lattice")
_scoremaillecell_kw = Keyword("num of cell")

# KEFF keywords
_fullcomb_kw = Keyword("full combined estimator")
_bestresdiscbatchs_kw = Keyword("best results are obtained with discarding")
_correlations_kw = Group(Keyword("estimators")
                         + Keyword("correlations")
                         + Keyword("combined values")
                         + Keyword("combined sigma%"))
_estimator_kw = Keyword("ESTIMATOR")
_bestresdiscbatchs_kw = Keyword("best results are obtained with discarding")
_equivkeff_kw = Keyword("Equivalent Keff:")

# Time steps
_timestepnum_kw = Keyword("TIME STEP NUMBER")
_timestepmin_kw = Keyword("time min. =")
_timestepmax_kw = Keyword("time max. =")

# Angular zones
_muangzone_kw = Keyword("MU ANGULAR ZONE :")
_mumin_kw = Keyword("mu min. =")
_mumax_kw = Keyword("mu max. =")
_phiangzone_kw = Keyword("PHI ANGULAR ZONE :")
_phimin_kw = Keyword("phi min. =")
_phimax_kw = Keyword("phi max. =")

# Spectrum keywords
_spectrum_kw = Keyword("SPECTRUM RESULTS")
_spgroupwunit_kw = Keyword("group (MeV)")
_spgroup_kw = Keyword("group")
_spscore_kw = Keyword("score")
_spsigma_kw = Keyword("sigma_%")
_spscovlethargy_kw = Keyword("score/lethargy")
_spvov_kw = Keyword("vov")

# Mesh keywords
_energyrange_kw = Keyword("Energy range")

# MED files
_creationmedfile_kw = Keyword("Creating MED output file")
_medmeshid_kw = Keyword("MED mesh id")

# Entropy
_boltzmannentropy_kw = Keyword("Boltzmann Entropy of sources =")
_shannonentropy_kw = Keyword("Shannon Entropy of sources =")

# Scores ordered by nuclei and precursor families
_nucleiorder_kw = Keyword("Scores for nuclei contributions are ordered "
                          "according to the user list:")
_familiesorder_kw = Keyword("Scores are ordered from family i = 1 to i = MAX:")
_nucleifamilyorder_kw = Keyword("Scores are ordered "
                                "by nuclei and by families:")
_nucleus_kw = Keyword("Nucleus :")

# Variance of variance
_vovstar_kw = Keyword("variance of variance* :")
_sensibtomaxval_kw = Keyword("sensibility to maximum value:")
_vov_kw = Keyword("variance of variance :")
_bestres_kw = Keyword("best results are obtained with discarding")

# Greenbands
_gbspectrumstep_kw = Keyword("* SOURCE SPECTRUM STEP NUMBER :")
_gbenergymin_kw = Keyword("source energy min. =")
_gbenergymax_kw = Keyword("source energy max. =")
_gbsourcenum_kw = Keyword("SOURCE NUMBER :")
_gbsourcetab_kw = Keyword("SOURCE TABULATION :")

# KIJ matrix
_kijmkeff_kw = Keyword("kij-keff =")
_kijdomratio_kw = Keyword("dominant ratio =")
_kijeigenval_kw = Keyword("eigenvalues (re, im)")
_kijeigenvec_kw = Keyword("eigenvectors")
_kijmatrix_kw = Keyword("KIJ_MATRIX :")

# KIJ sources
_kijsources_kw = Keyword("SOURCES VECTOR :")
_kijsourcesorder_kw = Keyword("Sources are ordered following")

# KIJ keff
_kijfissilevol_kw = Keyword("number of fissile volumes :")
_kijlistfissilevol_kw = Keyword("list of fissile volume numbers : ")
_kijbatchs_kw = Keyword("number of last batches kept :")
_kijkeffevid_kw = (Keyword("EIGENVECTOR :") + Keyword("index")
                   + Keyword("source rate"))
_kijkeffmat_kw = Keyword("K-IJ MATRIX :")
_kijkeffstddevmat_kw = Keyword("STANDARD DEVIATION MATRIX :")
_kijkeffsensibilitymat_kw = Keyword("SENSIBILITY MATRIX :")

# IFP results
# convergence statistics
_ifpcvgstat_kw = Keyword("Scores for IFP convergence statistics are ordered "
                         "from cycle length L = 1 to L = MAX:")
# IFP adjoint criticality edition
_ifpadjcriticality_kw = Keyword("IFP_ADJOINT_CRITICALITY EDITION")
_ifpadjcyclelength_kw = Keyword("IFP CYCLE LENGTH =")
_ifpadjnormalizedres_kw = Keyword("RESULTS ARE NORMALIZED")
_ifpadjvol_kw = Keyword("Vol")
_ifpadjminmax_kw = Keyword("(min | max)")
_ifpadjscore_kw = Keyword("score [a.u.]")

# Perturbations
_perturbation_kw = Keyword("================== Perturbation result edition "
                           "======================")
_perturank_kw = Keyword("Perturbation rank =")
_pertumethod_kw = Keyword("Method :")
_pertuorder_kw = Keyword("Order:")
_pertutype_kw = Keyword("Perturbation de type")
_pertucompo_kw = Keyword("Composition :")

# Uncertainties results (linked to perturbations ?)
_uncertres_kw = Keyword("UNCERTAINTY RESULTS")
_uncertgp_kw = Keyword("group (Mev)")
_uncertsig2_kw = Keyword("sigma2(means)")
_uncertmean_kw = Keyword("mean(sigma_n2)")
_uncertsig_kw = Keyword("sigma(sigma_n2)")
_uncertfisher_kw = Keyword("fisher test")
_uncertintegres_kw = Keyword("UNCERTAINTY ON ENERGY INTEGRATED RESULTS")

# Creation jdds
_nbcontribpart_kw = Keyword("NUMBER OF CONTRIBUTING PARTICLES")
_endcontribpart_kw = Keyword("--- end of CONTRIBUTING PARTICLES ---")

# Symbol lines
_star_line = Suppress(LineStart() + Word('*'))
_equal_line = Suppress(LineStart() + Word('='))
_minus_line = Suppress(White() + Word('-'))


################################
#           PARSERS            #
################################

# Introduction parser
_sourceintensity = (Suppress(_sourceintensity_kw + ':')
                    + (_fnums | _unavailable_kw)
                    ('source_intensity'))
# unkown -> string not in a list, while list of float per default
_meanweightleakvals = Group(_fnums('val')
                            + Suppress("sigma =") + _fnums('sigma')
                            + Suppress('sigma% =') + _fnums('sigma%'))
_meanweightleak = (Suppress(_meanweightleakage_kw)
                   + (Suppress('=') + _meanweightleakvals
                      | Suppress(':') + _unknown_kw)('mean_weigt_leak'))
_edbatchnum = Suppress(_edbatchnum_kw + ':') + _inums('edition_batch_number')

_meanweightrestartpart = (Suppress(_meanweightrestartpart_kw)
                          + _fnums('meanwgtrestartpart'))
_introelts = _meanweightleak | _edbatchnum | _meanweightrestartpart
intro = _sourceintensity + _star_line + OneOrMore(_introelts)


# Conclusion parser
_simutime = Suppress(_simulationtime_kw + ':') + _inums('simulation_time')
_exploitime = (Suppress(_exploitationtime_kw + ':')
               + _inums('exploitation_time'))
_elapsedtime = Suppress(_elapsedtime_kw + ':') + _inums('elapsed_time')
runtime = _simutime | _elapsedtime | _exploitime

# Response parser
# Description of the response
_respfunc = (Suppress(_respfunction_kw + ':')
             + OneOrMore(Word(alphanums + '_() =+/:-'), stopOn=LineEnd())
             .setParseAction(''.join)('resp_function'))
# warning: order matters hier, LineEnd has to be before Optional(Word)
_respname = (Suppress(_respname_kw + ':')
             + (Suppress(LineEnd())
                | Optional(Word(alphanums + '_ ')('resp_name'))))
_scorename = (Suppress(_scorename_kw + ":")
              + Word(alphanums + '_ ')('score_name'))
_energysplit = (Suppress(_energysplitname_kw + ':')
                + Word(alphanums + '_ -')('energy_split_name'))
respdesc = (_respfunc + Optional(_respname) + Optional(_scorename)
            + Optional(_energysplit))

_particle = (Suppress(_particule_kw + ':')
             + OneOrMore(Word(alphas+','), stopOn=LineEnd())
             .setParseAction(' '.join)('particle'))
_incparticle = (Suppress(_incparticle_kw + ':')
                + Word(alphas)('incident_particle'))

# response characteristics written in lower case
_reactiononnucl = (Suppress(_reactiononnucl_kw + ':')
                   + Word(alphanums+'_')('reaction_on_nucleus'))
_temperature = Suppress(_temperature_kw + ':') + _fnums('temperature')
_composition = (Suppress(_composition_kw + ':')
                + Word(alphanums + ".e+-_")('composition'))
_concentration = Suppress(_concentration_kw + ':') + _fnums('concentration')
# remark: join with whitespace is not working here, no idea why
#         -> whitespace replaced by _ in the string
_reaction = (Suppress(_reaction_kw)
             + OneOrMore(Word(alphanums+':+'), stopOn=_endtable)
             .setParseAction('_'.join)('reaction'))


def _next_compos(toks):
    if toks.getName() == 'reaction_on_nucleus':
        detail = _temperature | _composition | _concentration | _reaction
    elif toks.getName() == 'temperature':
        detail = _reactiononnucl | _composition | _concentration | _reaction
    elif toks.getName() == 'composition':
        detail = _reactiononnucl | _temperature | _concentration | _reaction
    elif toks.getName() == 'concentration':
        detail = _reactiononnucl | _temperature | _composition | _reaction
    elif toks.getName() == 'reaction':
        detail = _reactiononnucl | _temperature | _composition | _concentration
    else:
        LOGGER.warning("Not a foreseen result name, please check, keeping all")
        detail = (_reactiononnucl | _temperature | _composition
                  | _concentration | _reaction)
    _otherdetails << OneOrMore(detail)  # pylint: disable=W0106


_compodetails = Forward()
_otherdetails = Forward()
_compoptions = (_reactiononnucl
                | _temperature
                | _composition
                | _concentration
                | _reaction).setParseAction(_next_compos)
_compodetails << Group(_compoptions + _otherdetails)  # pylint: disable=W0106
_nuclflags = Group(OneOrMore(_compodetails))('compo_details')


# other response characteristics
_dpatype = (Suppress(_dpatype_kw)
            + OneOrMore(Word(alphas+'-,'), stopOn=LineEnd())
            .setParseAction(' '.join)('dpa_type'))
_required = Group(Suppress(_required_kw)
                  + OneOrMore(Word(alphas)).setParseAction(' '.join)
                  + Suppress(':')
                  + OneOrMore(Word(alphanums+'()'), stopOn=LineEnd())
                  .setParseAction(' '.join))('required')
_mode = Suppress(_mode_kw) + Word(alphas)('mode')
_inducedbyint = (Suppress(_inducedbyint_kw)
                 + Group(OneOrMore(_inums))('induced_by_interation'))
_notinducedbyint = (Suppress("NOT" + _inducedbyint_kw)
                    + Group(OneOrMore(_inums))('NOT_induced_by_interation'))
_fxptcontrib = (OneOrMore(Word(alphas+'()'),
                          stopOn=_fxptcontrib_kw).setParseAction(' '.join)
                + Suppress(_fxptcontrib_kw))('fxpt_contribution')
_spectrumresp = Suppress(_spectrumresp_kw + ':') + Word(alphas)('spectrum')
_filters = (Suppress(_filters_kw + ':')
            + Group(OneOrMore(_inums))('filter_volumes'))

respcarac = (_particle
             | _incparticle
             | _nuclflags
             | _filters
             | _required
             | _dpatype
             | _mode
             | _inducedbyint
             | _notinducedbyint
             | _fxptcontrib
             | _spectrumresp)

respintro = Group(respdesc + ZeroOrMore(respcarac))('response_description')

# Responses themselves
# Score description (not needed for KEFF)
scoremode = Suppress(_scoremode_kw + ':') + Word(alphas+'_')('scoring_mode')
# scoring zones
_score_mesh = (_scoremesh_kw('zone_type')
               + Suppress(':')
               + Group(Word(alphas)
                       + Word(alphas)
                       + Word(alphas+'() '))('column_names')
               + Optional(Suppress("(in")
                          + Word(alphanums+'.^-+')('unit')
                          + Suppress(')')))
_score_allgeom = _scoreallgeom_kw('zone_type')
_score_allsources = _scoreallsources_kw('zone_type')
_score_vol = (_scorevol_kw('zone_type')
              + Suppress(_scorevolvol_kw + ':')
              + _inums('volume_number')
              + Suppress(_scorevolume_kw + ':')
              + _fnums('total_volume_cm3'))
_score_vol_sum = ((_scorevolsum_kw('zone_type')
                   + Suppress(_scorevolsumvol_kw + ':')
                   + Group(_inums
                           + ZeroOrMore(Suppress('+') + _inums))
                   ('volumes_numbers')
                   + Suppress(_scorevolumesum_kw + ':')
                   + _fnums('total_volume_cm3')))
_score_surf = (_scoresurf_kw('zone_type')
               + Suppress(_scoresurfvol_kw + ':')
               + (Group(_inums + Suppress(',') + _inums)
                  | Group(Word(alphanums+'/_') + Suppress(',')
                          + Word(alphanums+'/_')))
               ('volumes_numbers')
               + Optional(Suppress(_scoresurface_kw + ':')
                          + _fnums('total_surface_cm2')))
_score_surf_sum = (_scoresurfsum_kw('zone_type')
                   + Suppress(_scoresurfsumfront_kw + ':')
                   + OneOrMore(Group(Suppress('(')
                                     + _inums + Suppress(',')
                                     + _inums + Suppress(')')
                                     + Optional(Suppress('+'))))
                   ('frontiers_numbers')
                   + Suppress(_scoresurfacesum_kw + ':')
                   + _fnums('total_surface_cm2'))
_score_point = (_scorepoint_kw('zone_type')
                + Suppress(':')
                + Group(_fnums + Suppress(',')
                        + _fnums + Suppress(',')
                        + _fnums)('point_coordinates'))
_cellelt = (Group(Suppress('(') + _inums('vol_num')
                  + Suppress(',') + _inums('depth')
                  + OneOrMore(
                      Group(Suppress(',') + _inums
                            + Suppress(',') + _inums
                            + Suppress(',') + _inums))('cells')
                  + Suppress(')')))
_score_cell = (_scorecell_kw('zone_type')
               + Suppress(_scorecelldet_kw)
               + Group(_cellelt
                       + ZeroOrMore(Suppress('+') + _cellelt))
               ('cell_details'))
_maillelt = (Suppress(_scoremaillevol_kw + ':') + _inums('vol_num')
             + Suppress(_scoremailledepth_kw + ':') + _inums('depth')
             + Suppress(_scoremaillecell_kw + ':')
             + OneOrMore(
                 Group(Suppress('(') + _inums
                       + Suppress(',') + _inums
                       + Suppress(',') + _inums + Suppress(')')))('cells'))
_score_maille = (_scoremaille_kw('zone_type')
                 + Group(_maillelt)('cell_details'))
scorezone = (Group(Suppress(_scorezone_kw+':') +
                   (_score_mesh
                    | _score_allgeom
                    | _score_allsources
                    | _score_vol
                    | _score_surf
                    | _score_surf_sum
                    | _score_vol_sum
                    | _score_point
                    | _score_cell
                    | _score_maille
                    | LineEnd()))
             ('scoring_zone'))
# scoring description = scoring mode + scoring zone
scoredesc = scoremode + scorezone


# RESPONSE RESULTS


def _set_no_unit_case(toks):
    '''Deal with the "not unit" case'''
    if len(toks) == 1:
        return {'uscore': '', 'usigma': toks[0]}
    else:
        LOGGER.warning("more than one unit, please check: %s", str(toks))


def _rm_blanks(toks):
    '''Remove leading and trailing spaces (not the ones inside the string)'''
    return toks[0].strip()


# Default integrated result
_numdiscbatch = (Suppress(_numbatchs1stdiscarded_kw + ':')
                 + _inums('disc_batch'))
_numusedbatch = Suppress(_numbatchsused_kw + ':') + _inums('used_batch')
_integratedres = _fnums('score') + _fnums('sigma')
_unitsres = (Suppress(_units_kw)
             + (Word('%').setParseAction(_set_no_unit_case)
                | (Word(alphanums+'.^-+ ').setParseAction(_rm_blanks)('uscore')
                   + Word('%')('usigma'))))
# rejection in vov and sensibility cases
_rejection = (Suppress('[')
              + OneOrMore(Word(alphanums+'<>.+-')).setParseAction(' '.join)
              + Suppress(']'))
_vovnostar = Suppress(_vov_kw) + _fnums('vov')
_vovstar = Group(Suppress(_vovstar_kw)
                 + _fnums
                 + Suppress('[') + _fnums + Suppress(']')
                 + Optional(_rejection))('vovstar')
_sensibtomaxval = Group(Suppress(_sensibtomaxval_kw)
                        + _fnums
                        + Optional(_rejection))('sensibility_max_val')
_vov = (_vovnostar | _vovstar + _sensibtomaxval)
# best result
_bestres = Group(Suppress(_bestres_kw) + _inums + Suppress("batches")
                 + _minus_line
                 + _numusedbatch + _fnums + _fnums)('bestresult')

defintegratedres = (Group(Optional(Suppress(_integratedres_kw))
                          + Optional(_numdiscbatch)
                          + ((_numusedbatch
                              + _integratedres
                              + Optional(_unitsres)
                              + Optional(_vov)
                              + Optional(_bestres))
                             | _notconverged_kw('not_converged')))
                    ('integrated_res'))


# Time steps
_timestep = Group(Suppress(_timestepnum_kw + ':') + _inums
                  + _minus_line
                  + Suppress(_timestepmin_kw) + _fnums
                  + Suppress(_timestepmax_kw) + _fnums)('time_step')


# Angular zones
_muangzone = Group(Suppress(_muangzone_kw) + _inums
                   + _minus_line
                   + Suppress(_mumin_kw) + _fnums
                   + Suppress(_mumax_kw) + _fnums)('mu_angle_zone')
_phiangzone = Group(Suppress(_phiangzone_kw) + _inums
                    + _minus_line
                    + Suppress(_phimin_kw) + _fnums
                    + Suppress(_phimax_kw) + _fnums)('phi_angle_zone')


# Spectrum
_spectrumcols = Suppress((_spgroupwunit_kw | _spgroup_kw)
                         + _spscore_kw
                         + _spsigma_kw
                         + _spscovlethargy_kw)
_spectrumunits = Group(Suppress(_units_kw)
                       + Word(alphanums+'.^-+%') * 4)('units')
_spectrumbin = _fnums + Suppress('-') + _fnums
_spectrumvals = Group(_spectrumbin + _fnums + _fnums + _fnums)
_spectrum = (Suppress(_spectrum_kw)
             + _numdiscbatch
             + _spectrumcols
             + Optional(_spectrumunits)
             + OneOrMore(_spectrumvals, stopOn=_endtable)('spectrum_vals'))
spectrumblock = Group(OneOrMore
                      (Group(OneOrMore(_timestep | _muangzone | _phiangzone)
                             + _spectrum
                             + Optional(defintegratedres)))
                      | Group(_spectrum))('spectrum_res')


# Spectrum with vov
_vovspectrumcols = Suppress(_spgroupwunit_kw + _spscore_kw + _spsigma_kw
                            + _spscovlethargy_kw + _spvov_kw)
_vovspectrumbin = _fnums + Suppress('-') + _fnums
_vovspectrumvals = Group(_vovspectrumbin + _fnums + _fnums + _fnums + _fnums)
_vovspectrum = (Suppress(_spectrum_kw)
                + _numdiscbatch
                + _vovspectrumcols
                + OneOrMore(_vovspectrumvals, stopOn=_endtable)
                ('spectrum_vals'))
vovspectrumblock = Group(Group(_vovspectrum))('vov_spectrum_res')


def _printtoks(toks):
    print(toks)


# Mesh
_mesh_energyrange = (Group(Suppress(_energyrange_kw + "(in") + Word(alphas)
                           + Suppress('):') + _fnums + Suppress('-') + _fnums)
                     ('mesh_energyrange'))
_mesh_energyintegrated = ((Suppress(_integratedres_kw) + Suppress(':'))
                          ('mesh_energyintegrated'))
_mesh_energyline = _mesh_energyrange | _mesh_energyintegrated
_meshspacecoord = (Suppress('(') + _inums
                   + (Suppress(',') + _inums) * 2
                   + Suppress(')'))
_meshvals = Group(Group(_meshspacecoord) + _fnums + _fnums)
_meshres = Group(_mesh_energyline
                 + Group(OneOrMore(_meshvals))
                 ('mesh_vals'))
meshblock = Group(OneOrMore(Group(_timestep
                                  + Group(OneOrMore(_meshres))('meshes')
                                  + Optional(defintegratedres)))
                  | Group(Group(OneOrMore(_meshres))('meshes')))('mesh_res')


# KIJ matrix
# before keff as KIJ ESTIMATOR used to evaluate KEFF...
# definition de kijdim en variable globale ne fonctionne pas car creee avant
# solution : utiliser forward pour le redefinir !


def _set_kijdim(toks):
    _kijdim = len(toks)
    _kijeigenvec << Group(_fnums * _kijdim)  # pylint: disable=W0106
    _kijmatrix << Group(_fnums * _kijdim)  # pylint: disable=W0106


_kijsum = Group(Suppress(_kijmkeff_kw) + _fnums
                + Suppress(_kijdomratio_kw) + _fnums)('kijmkeff_res')
_kijeigenval = Group(_fnums + _fnums)
_kijeigenvec = Forward()
_kijmatrix = Forward()
_kijeigenvaltab = (Suppress(_kijeigenval_kw)
                   + Group(OneOrMore(_kijeigenval).setParseAction(_set_kijdim))
                   ('kij_eigenval'))
_kijeigenvectab = (Suppress(_kijeigenvec_kw) + Group(OneOrMore(_kijeigenvec))
                   ('kij_eigenvec'))
_kijmatrixtab = (Suppress(_kijmatrix_kw) + Group(OneOrMore(_kijmatrix))
                 ('kij_matrix'))
kijres = (Group(Suppress(_integratedres_kw)
                + _numusedbatch
                + _kijsum
                + _kijeigenvaltab
                + _kijeigenvectab
                + _kijmatrixtab).setParseAction(trans.convert_kij_result)
          ('kij_res'))


# KIJ SOURCES
_kijsourcesorder = (Suppress(_kijsourcesorder_kw)
                    + Word(alphas)('kij_sources_order') + Suppress(':'))
_kijsourcesval = Group(OneOrMore(_fnums))('kij_sources_vals')
kijsources = (Group(Suppress(_integratedres_kw)
                    + _numusedbatch
                    + Suppress(_kijsources_kw)
                    + _kijsourcesorder
                    + _kijsourcesval)
              .setParseAction(trans.convert_kij_sources)('kij_sources'))


# KIJ estimator for keff

def _define_kij_dim(toks):
    LOGGER.debug("KIJ dimension: %d", len(toks))
    _kijdim = len(toks)
    _identifier = (Group(Suppress('(')
                         + _inums + Suppress(',')
                         + _inums + Suppress(',')
                         + _inums + Suppress(')'))
                   | _inums)
    _idline << Group(_identifier * _kijdim)  # pylint: disable=W0106
    _matline << Group(_identifier            # pylint: disable=W0106
                      + Suppress('|')
                      + (_fnums + Suppress('|')) * _kijdim)


def _set_kij_vols(toks):
    _nbvols = int(toks[0])
    _kijlistvol << Group(_inums * _nbvols)  # pylint: disable=W0106


_kijkeffbeg = Word(alphas)('estimator') + Suppress(_estimator_kw) + _minus_line
_kijlistvol = Forward()
_kijfissilevol = ((Suppress(_kijfissilevol_kw) + _inums('nb_fissile_vols'))
                  .setParseAction(_set_kij_vols)
                  + Suppress(_kijlistfissilevol_kw)
                  + _kijlistvol('list_fissile_vols'))
_kijkeffintro = (Optional(_kijfissilevol)
                 + Suppress(_kijbatchs_kw) + _inums('batchs_kept')
                 + Suppress(_kijmkeff_kw) + _fnums('kij-keff'))

_idline = Forward()
_matline = Forward()
_kijkeffev = OneOrMore(Group(_inums + _fnums)).setParseAction(_define_kij_dim)
_kijkeffevtab = Group(Suppress(_kijkeffevid_kw) + _kijkeffev)('eigenvector')
_defmatrix = _idline + _minus_line + OneOrMore(_matline + _minus_line)
_kijkeffmatrix = (Group(Suppress(_kijkeffmat_kw) + _defmatrix)
                  ('keff_KIJ_matrix'))
_kijkeffstdmatrix = (Group(Suppress(_kijkeffstddevmat_kw) + _defmatrix)
                     ('keff_StdDev_matrix'))
_kijkeffsensibmatrix = (Group(Suppress(_kijkeffsensibilitymat_kw) + _defmatrix)
                        ('keff_sensibility_matrix'))

_kijkeffblock = (Group(_kijkeffbeg
                       + _kijkeffintro
                       + _kijkeffevtab
                       + _kijkeffmatrix
                       + _kijkeffstdmatrix
                       + _kijkeffsensibmatrix)
                 .setParseAction(trans.convert_kij_keff))


# Keff as generic response
_keffres = Group(Word(alphas) + _fnums + _fnums)
_keffresblock = Group(OneOrMore(_keffres))('res_per_estimator')
_correlationdesc = Suppress(_correlations_kw)
_correlationestim = Group(Word(alphas) + Suppress('<->') + Word(alphas))
_correlationvals = OneOrMore(_fnums
                             | _notconverged_kw)
_correlation = Group(_correlationestim + _correlationvals)
_correlationblock = (Group(_correlationdesc + OneOrMore(_correlation))
                     ('correlation_mat'))
_fullcombestimation = (Group(Suppress(_fullcomb_kw)
                             + ((_fnums + _fnums) | _notconverged_kw))
                       ('full_comb_estimation'))
_defkeffres = ((_keffresblock + _correlationblock + _fullcombestimation)
               | _notconverged_kw('not_converged'))
keffblock = Group(Suppress(_integratedres_kw)
                  + _numusedbatch
                  + _defkeffres).setParseAction(trans.convert_keff)('keff_res')


# Keff as historical response
_bestresestim = (OneOrMore(Word(alphas), stopOn=_estimator_kw)
                 .setParseAction(' '.join)('estimator')
                 + Suppress(_estimator_kw))
_bestresdiscbatch = (Suppress(_bestresdiscbatchs_kw)
                     + _inums('best_disc_batchs')
                     + Suppress("batches"))
_bestkeff = (Group(Suppress(Keyword("keff") + '=') + _fnums('keff')
                   + Suppress(Keyword("sigma") + '=') + _fnums('sigma')
                   + Suppress(Keyword("sigma%") + '=') + _fnums('sigma%'))
             ('bestkeffres'))
_equivkeff = Suppress(_equivkeff_kw) + _fnums('equivalent_keff')
_bestkeffpestim = (_notconverged_kw
                   | (_bestresdiscbatch
                      + _numusedbatch
                      + _bestkeff
                      + Optional(_equivkeff)))
_bestreskeff = Group(_bestresestim + _minus_line + _bestkeffpestim)
_bestresblock = OneOrMore(_bestreskeff, stopOn="KIJ")
defkeffblock = Group(_bestresblock + Optional(_kijkeffblock))('default_keffs')


# MED files
medfile = (Suppress(_creationmedfile_kw + ':')
           + Word(alphanums+'/_.')('med_file')
           + Suppress(_medmeshid_kw + Word(alphanums+'_.')))


# Entropy
_boltzmannentropy = (Suppress(_boltzmannentropy_kw)
                     + _fnums('boltzmann_entropy'))
_shannonentropy = Suppress(_shannonentropy_kw) + _fnums('shannon_entropy')
entropy = _boltzmannentropy + _shannonentropy


# Scores ordered by nuclei and precursor families
# Nuclei order alone
_scorepernucleus = Group(Word(alphanums)('nucleus') + Suppress(':')
                         + _integratedres)
_nucleiorder = (Suppress(_nucleiorder_kw)
                + OneOrMore(_scorepernucleus)('score_per_nucleus'))
# Families order alone
_scoreperfamily = Group(Suppress("i =")
                        + _inums('family_number') + Suppress(':')
                        + _integratedres)
_familyorder = (Suppress(_familiesorder_kw)
                + OneOrMore(_scoreperfamily)('score_per_family'))
# Nuclei and families order
_nucleusid = _nucleus_kw + Word(alphanums)('nucleus') + Suppress('.')
_nucleusfam = Group(_nucleusid + _familyorder)
_nuclfamoreder = (Suppress(_nucleifamilyorder_kw)
                  + OneOrMore(_nucleusfam)('score_per_nucleus_and_family'))
orderedres = Group(Suppress(_integratedres_kw)
                   + _numusedbatch
                   + (_nucleiorder | _familyorder | _nuclfamoreder)
                   + Optional(_unitsres))('ordered_res')


# Greenbands exploitation
_gbspectrumstep = Suppress(_gbspectrumstep_kw) + _inums
_gbenergymin = Suppress(_gbenergymin_kw) + _fnums
_gbenergymax = Suppress(_gbenergymax_kw) + _fnums
_gbstepdesc = Group(_gbspectrumstep + _minus_line
                    + _gbenergymin + _gbenergymax)('gb_step_desc')
_gbtabulation = (Suppress(_gbsourcetab_kw)
                 + Group(Suppress('u =') + _inums
                         + Suppress(', v =') + _inums
                         + Suppress(', w =') + _inums))
_gbsource = Group(Suppress(_gbsourcenum_kw)
                  + _inums
                  + (_minus_line | (_gbtabulation + _minus_line)))('gb_source')
_gbrespersource = Group(_gbsource + spectrumblock)
_gbstep = Group(_gbstepdesc + Group(OneOrMore(_gbrespersource))('gb_step_res'))
gbblock = Group(OneOrMore(_gbstep))('greenband_res')


# IFP convergence statistics
_ifpline = Group(Suppress("L =") + _inums + Suppress(':') + _fnums + _fnums)
# lines exists only if converged...
ifpblock = (Group(Suppress(_integratedres_kw)
                  + _numusedbatch
                  + Suppress(_ifpcvgstat_kw)
                  + Optional(Group(OneOrMore(_ifpline))
                             .setParseAction(trans.convert_ifp)('ifp_stat'))
                  + Optional(_unitsres))
            ('ifp_res'))


def _rename_norm_kw():
    '''Transform RESULTS ARE NORMALIZED keyword in int (lighter)'''
    return 1


def _define_ifp_adj_table_dim(toks):
    '''Define the format of the IFP adjoint criticality table result:
    coordinates (Vol or space coordinates) are followed by energy.
    '''
    _tabdim = len(toks)
    if "Vol" not in toks[0]:
        _ifpadjbinval << _fnums * 2 * _tabdim  # pylint: disable=W0104
    else:
        # in Vol case: int to identify volume, then E (min | max)
        _ifpadjbinval << _inums + _fnums * 2  # pylint: disable=W0104


# IFP adjoint criticality edition
_ifpadfcrit_intro = (Group(_star_line
                           + Suppress(_ifpadjcriticality_kw)
                           + _star_line
                           + Word(alphas+'_')('ifp_score')
                           + _scorename
                           + Suppress(_ifpadjcyclelength_kw)
                           + _inums('ifp_cycle_length')
                           + (Optional(_ifpadjnormalizedres_kw
                                       .setParseAction(_rename_norm_kw))
                              ('normalized'))
                           + _star_line)
                     ('ifp_adjoint_criticality_intro'))
_ifpadjbinval = Forward()
_ifpadjcoordinate = Word(alphas) + Suppress(_ifpadjminmax_kw)
_ifpadjcoordinates = ((Optional(_ifpadjvol_kw) + OneOrMore(_ifpadjcoordinate))
                      .setParseAction(_define_ifp_adj_table_dim))
_ifpadjcolumns = _ifpadjcoordinates + _ifpadjscore_kw + _spsigma_kw
_ifpadjline = Group(_ifpadjbinval + _fnums + _fnums)
_ifpadjvalues = OneOrMore(_ifpadjline)('values')
ifpadjointcriticality = (Group(_ifpadfcrit_intro
                               + _ifpadjcolumns('columns')
                               + _ifpadjvalues
                               + _star_line)
                         ('ifp_adjoint_crit_edition'))


# Perturbations
_perturank = Suppress(_perturank_kw) + _inums('rank')
_pertumethod = (Suppress(_pertumethod_kw)
                + OneOrMore(Word(alphas), stopOn=LineEnd())('method')
                .setParseAction(' '.join))
_pertuorder = Suppress(_pertuorder_kw) + _inums('order')
_pertutype = Suppress(_pertutype_kw) + Word(alphas)('type')
_pertucompo = Suppress(_pertucompo_kw) + Word(alphanums+'_')('composition')
pertu_desc = (Group(Suppress(_perturbation_kw)
                    + _perturank
                    + _pertumethod
                    + Optional(_pertuorder)
                    + _pertutype
                    + _pertucompo).setParseAction(trans.to_dict)
              ('perturbation_desc'))


# Uncertainties (linked to perturbations ?)
_uncertcols = Suppress(_uncertgp_kw + _uncertsig2_kw
                       + _uncertmean_kw + _uncertsig_kw + _uncertfisher_kw)
_uncertbin = _fnums + Suppress('-') + _fnums
_uncertvals = Group(_uncertbin + _fnums * 4)
_uncertspectrum = (Suppress(_uncertres_kw)
                   + _numdiscbatch
                   + _uncertcols
                   + _minus_line
                   + OneOrMore(_uncertvals, stopOn=_endtable)
                   ('spectrum_vals'))
uncertblock = Group(OneOrMore
                    (Group(OneOrMore(_timestep | _muangzone | _phiangzone)
                           + _uncertspectrum))
                    | Group(_uncertspectrum))('uncert_spectrum_res')

_uncertintegres = (_fnums('sigma2(means)')
                   + _fnums('mean(sigma_n2)')
                   + _fnums('sigma(sigma_n2)')
                   + _fnums('fisher test'))
_uncertintegfullres = _numusedbatch + _uncertintegres
uncertintegblock = Group(Suppress(_uncertintegres_kw)
                         + _numdiscbatch
                         + _uncertintegfullres)('uncert_integrated_res')


# Creation jdds
_nbpartline = Group(Suppress("FILE") + _inums
                    + Suppress(':') + _inums
                    + Suppress("particles"))
contribpartblock = (Group(Suppress(_nbcontribpart_kw)
                          + _minus_line
                          + OneOrMore(_nbpartline)
                          + Suppress(_endcontribpart_kw))
                    ('contributing_particles'))


# Score block
scoreblock = OneOrMore((Group(scoredesc
                              + (OneOrMore(spectrumblock
                                           | meshblock
                                           | vovspectrumblock
                                           | entropy
                                           | medfile
                                           | defintegratedres
                                           | uncertblock
                                           | uncertintegblock
                                           | gbblock)))
                        .setParseAction(trans.convert_score)))('score_res')

# Response block
responseblock = (keffblock
                 | kijres
                 | kijsources
                 | orderedres
                 | defintegratedres
                 | ifpblock
                 | scoreblock)

response = Group(_star_line
                 + respintro
                 + _star_line
                 + Group(responseblock)('results'))

perturbation = (OneOrMore(Group(pertu_desc + response('response')))
                ('perturbation'))

################################
#        GENERAL PARSER        #
################################

# replace group by real dict, need to check if fine or not (risk: list needed)
mygram = (OneOrMore((intro
                     + (Group(OneOrMore(response))('list_responses')
                        | ifpadjointcriticality)
                     + Optional(defkeffblock)
                     + Optional(contribpartblock)
                     + Optional(perturbation)
                     + Optional(OneOrMore(runtime)))
                    .setParseAction(trans.to_dict))
          .setParseAction(trans.print_result)
          | intro + OneOrMore(runtime))
