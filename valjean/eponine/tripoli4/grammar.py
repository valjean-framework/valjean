# Copyright French Alternative Energies and Atomic Energy Commission
# Contributors: Ève le Ménédeu, Davide Mancusi (2021)
# eve.le-menedeu@cea.fr, davide.mancusi@cea.fr
#
# This software is a computer program whose purpose is to analyze and
# post-process numerical simulation results.
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL: http://www.cecill.info.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# pylint: disable=too-many-lines
# pylint: disable=invalid-name
r'''This module provides `pyparsing` grammar for Tripoli-4 output listings.

.. role :: parsing_var(literal)
.. |keff| replace:: k\ :sub:`eff`
.. |kij| replace:: k\ :sub:`ij`
.. _pyparsing: https://pythonhosted.org/pyparsing/

Documentation on the ``pyparsing`` package can be found at `pyparsing`_.

Transformation from ``pyparsing.ParseResults`` to more standard python objects,
including :obj:`numpy` arrays, is done with :mod:`~.transform`, calling
:mod:`~valjean.eponine.tripoli4.common`.

Generalitites
-------------

* This parser only parses the result part of the listing (selection done in
  :mod:`~valjean.eponine.tripoli4.scan`).
* It takes into account all responses in ``qualtrip`` database up to Tripoli-4,
  version 10.2.
* If a response is not taken into account parsing will fail:

  * with a big, ugly message ending by location of the end of successful
    parsing in the result string (possible to print it) → normally where starts
    your new response
  * it seems to end normally, but did not in reality. One of the best checks in
    that case is to test if the ``endflag`` in
    :mod:`~valjean.eponine.tripoli4.scan` was read in the parser, usually not.
    Then the new response probably have to be added.

* A general parser is proposed for use in the file, but other parsers can be
  built from the partial parsers written here
* Numbers are automatically converted to :obj:`numpy` numbers (possibility to
  choose the dtype used for numbers)
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
dictionaries in the ``pyparsing.ParseResults``. Then `parse actions` are used
to standard python or :obj:`numpy` objects. These `parse actions`, called with
``pyparsing.ParserElement.setParseAction``, can be found in :mod:`~.transform`.

Main parsers blocks
```````````````````
The main parsers blocks are defined at the end of the module, named
:parsing_var:`mygram` and :parsing_var:`response`. The default parser is
:parsing_var:`mygram`.

Typically, each result block in the listing should start by the `intro` block,
parsed by :parsing_var:`intro`, and end with at least one `runtime` block,
parsed by :parsing_var:`runtime`. This parts follows the
:mod:`~valjean.eponine.tripoli4.scan`: :obj:`str` starting by
``'RESULTS ARE GIVEN'`` and ending with ``'simulation time'``,
``'exploitation time'`` or ``'elapsed time'``.

Between these blocks can be found the data blocks. The major ones are:

* one or more responses, driven by the keyword ``'RESPONSE FUNCTION'``,
* the editions of IFP adjoint criticality,
* the "default" |keff| block, in most of the cases at the end of the listing,
* the *contributing particles block*, mainly in first pass listings,
* the perturbation block,
* an optional additional `runtime` block.

Main data blocks are described below (results taken into account, main
features).

Response block, parser :parsing_var:`response`
``````````````````````````````````````````````
The core of the listings is the list of responses, including all the required
scores. This big block is constructed as a :obj:`list` of :obj:`dict`, each
one representing a response (key ``'list_responses'`` in the final result).

Response are constructed as:

* response introduction containing its definition, parsed by
  :parsing_var:`respintro`:

  * a description of the response parsed by :parsing_var:`respdesc` including:

    * ``'RESPONSE FUNCTION'`` keyword as mandatory (afaik)
    * ``'RESPONSE NAME'``, ``'SCORE NAME'`` and ``'ENERGY DECOUPAGE NAME'``
      that are present in most of the cases

  * more characteristics of the response, parsed by :parsing_var:`respcarac`,
    like:

    * considered particle (``'PARTICULE'`` in the listing)
    * nucleus on which the reaction happens (if ``'RESPONSE FUNCTION'`` is a
      ``'REACTION'``)
    * temperature
    * compostion of the volumes considered
    * concentration
    * reaction considered (usually given as codes)
    * others like DPA type, required arguments, mode, filters, etc.

* responses themselves, using parser :parsing_var:`responseblock`, are various:

  * responses including *score* description, all included in the
    :parsing_var:`scoreblock` parser. More than one can be present, they are
    grouped in the :parsing_var:`listscoreblock` parser.
    :parsing_var:`scoreblock` parser contains:

    * score description (parser :parsing_var:`scoredesc`) contains the score
      mode (``'TRACK'``, ``'SURF'`` or ``'COLL'``) and the score zone
      (currently taken into account: mesh, results cumulated on all geometry or
      on all sources, Volume, Volume Sum, Frontier, Frontier Sum, Point, Cells
      and Maille)

    * results block, where at least one of these results can be found, are by
      parsed by the following parsers:

      * :parsing_var:`spectrumblock`: spectrum
      * :parsing_var:`meshblock`: mesh
      * :parsing_var:`vovspectrumblock`: spectrum with variance of variance
      * :parsing_var:`entropy`: entropy results (Boltzmann and Shannon
        entropies)
      * :parsing_var:`medfile`: location of optional MED file
      * :parsing_var:`genericscoreblock`: default result integrated over energy
      * :parsing_var:`uncertblock`: uncertainty results
      * :parsing_var:`uncertintegblock`: uncertainties on integrated results
        over energy
      * :parsing_var:`gbblock`: Green bands results

  * |keff| presented as a generic response, possibly transformed in
    :obj:`numpy.matrix` (parser :parsing_var:`keffblock`)
  * |kij| results: matrix, eigenvalues, eigenvectors (parser
    :parsing_var:`kijres`)
  * |kij| sources (parser :parsing_var:`kijsources`)
  * Adjoint related results (parser :parsing_var:`adjointres`): scores ordered
    by precursors and families, by perturbation index, by cycle length or
    sensitivities (this last case is represented in a 3 dimensions
    :obj:`numpy.ndarray`, incident energy, energy ("leaving neutron"),
    direction cosine (µ)). For the moment this is only for IFP method , in
    close future also for Wielandt method
  * default result integrated over energy where no scoring mode and zone are
    precised (parser :parsing_var:`defintegratedres`)
  * perturbation results (parser :parsing_var:`perturbation`)


Other parsers
`````````````
Various other blocks can appear in the Tripoli-4 listing, located at the same
level as the response block. These parsers and the associated dictionary key
(same level as ``'list_responses'``) are:

* :parsing_var:`ifpadjointcriticality`: edition of IFP adjoint criticality, key
  ``'ifp_adjoint_crit_edition'``;
* :parsing_var:`autokeffblock`: "default" |keff| block, containing for example
  the best estimation of |keff| using variable number of discarded batches, key
  ``'keff_auto'``;
* :parsing_var:`contribpartblock`: *contributing particles block*, key
  ``'contributing_particles'``
* :parsing_var:`perturbation`: perturbation results, containing a description
  of the calculation of the perturbation followed by the perturbation result
  presented like a usual response (spectrum, mesh, etc. depending on required
  score), key ``'perturbation'``
* :parsing_var:`runtime`: simulation, exploitation or elapsed time.


.. todo::

    Adjoint results: for the moment only IFP is really parsed. Grammar has
    already more or less adapted to welcome Wielandt method that will have the
    same kind of outputs (renaming as adjoint_res for example). No key is set
    for the moment to specify the method, it can be obtained from the response
    function itself. Adjoint criticality editions are only done for IFP, this
    may change when the same will be available for Wielandt. Some renaming can
    also be needed.

'''

from pyparsing import (Word, Keyword, White, alphas, alphanums,
                       Suppress, Optional, LineEnd, CaselessKeyword,
                       Group, OneOrMore, ZeroOrMore, Forward, originalTextFor,
                       tokenMap, delimitedList, printables, replaceWith)
from pyparsing import pyparsing_common as pyparscom
from . import transform as trans
from .transform import compose2
from .dump import dump_in_logger
from ... import LOGGER

_fnums = pyparscom.fnumber.setParseAction(tokenMap(trans.common.FTYPE))
_inums = pyparscom.number.setParseAction(tokenMap(trans.common.ITYPE))

###################################
#            KEYWORDS             #
###################################

# General keywords
_integratedres_kw = Keyword("INTEGRATED RESULTS")
_numbatchsused_kw = (Keyword("number of")
                     + (Keyword("batches") | Keyword("batch"))
                     + Optional(Keyword("used")))
_numbatchs1stdiscarded_kw = Keyword("number of first discarded batches")
_notconverged_kw = (Keyword("NOT YET CONVERGED")
                    | CaselessKeyword("Not converged"))
_unknown_kw = Keyword("unknown")
_unavailable_kw = Keyword("unavailable")
_units_kw = Keyword("Units:")
_warning_kw = CaselessKeyword("Warning")
_endtable = LineEnd() + LineEnd()

# Introduction keywords
_sourceintensity_kw = Keyword("RESULTS ARE GIVEN FOR SOURCE INTENSITY")
_meanweightleakage_kw = Keyword("Mean weight leakage")
_meanweightleakagein_kw = Keyword("Mean weight leakage inside")
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
_nusplitname_kw = Keyword("DECOUPAGE NAME")
_respfiltered_kw = Keyword("RESPONSE FILTERED BY")
_respfiltcompos_kw = Keyword("COMPOSITIONS")
_particule_kw = Keyword("PARTICULE")
_incparticle_kw = Keyword("INCIDENT PARTICULE")
_noise_equation_kw = Keyword("NOISE EQUATION")
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
_scoremesh_kw = (Keyword("Results on a mesh")
                 .setParseAction(replaceWith('Mesh')))
_scoremeshinfobins_kw = Keyword("(x,y,z)")
_scoreallgeom_kw = (Keyword("Results cumulated on all geometry")
                    .setParseAction(replaceWith('All geometry')))
_scoreallsources_kw = (Keyword("Results cumulated on all sources")
                       .setParseAction(replaceWith('All sources')))
_scorevol_kw = Keyword("Volume")
_scorevolvol_kw = Keyword("num of volume")
_scorevolume_kw = (Keyword("Volume in cm3")
                   | Keyword('Volume in 1.000000e+00 cm3'))
_scorevolumeint_kw = (Keyword("The result is integrated over the volume")
                      | Keyword("The result is integrated in volume")
                      ).setParseAction(replaceWith('volume integrated'))
_scorevolumenotint_kw = (
    Keyword("The volume has been provided by the user "
            "(the user requested a score per unit volume)")
    | Keyword("The volume has been calculated by Tripoli-4 "
              "or provided by the user")).setParseAction(
                  replaceWith('per unit volume'))
_scorevolsum_kw = Keyword("Volume Sum")
_scorevolsumvol_kw = Keyword("num of volumes")
_scorevolumesum_kw = Keyword("Total volume in cm3")
_scorevolumecell_kw = Keyword("Cell volume in cm3")
_scoresurf_kw = Keyword("Frontier")
_scoresurfvol_kw = Keyword("volumes")
_scoresurface_kw = Keyword("Surface in cm2")
_scoresurfaceint_kw = Keyword("The surface area has been provided by the user "
                              "(the user requested a score per unit area)")
_scoresurfacenotint_kw = Keyword("The result is integrated over the surface")
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

# Correspondence table (volumes and their names)
_corresptable_kw = Keyword("Correspondence table between volumes "
                           "ids and names :")
_vol_kw = CaselessKeyword("Volume")

# KEFF keywords
_fullcomb_kw = Keyword("full combined estimator")
_bestresdiscbatchs_kw = Keyword("best results are obtained with discarding")
_correlations_kw = Group(Keyword("estimators")
                         + Keyword("correlations")
                         + Keyword("combined values")
                         + Keyword("combined sigma%"))
_estimator_kw = Keyword("ESTIMATOR")
_equivkeff_kw = Keyword("Equivalent Keff:")
_warn_combkeff_kw = (
    Keyword("One of the Keffectives is null and should not be")
    + Keyword("Combined Keffectives will not be edited"))
_warn_fixsourcekeff_kw = (
    Keyword("In FIXED_SOURCES_CRITICITY mode, the keff result")
    + Keyword("is actually an overall multiplication factor "
              "(cf User's Guide)"))

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
_spscovlethargy_kw = Keyword("score/lethargy")
_spvov_kw = Keyword("vov")
_nuspectrum_kw = Keyword("NU RESULTS")
_nusprange_kw = Keyword("range")
_zaspectrum_kw = Keyword("ZA RESULTS")
_zaspid_kw = Keyword("(Z,A)")
_spscore_kw = Keyword("score")
_spsigma_kw = Keyword("sigma_%")

# Mesh keywords
_energyrange_kw = Keyword("Energy range")

# MED files
_creationmedfile_kw = Keyword("Creating MED output file")
_creationfile_kw = Keyword("# Creating output file")
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
# Perturbation order
_perturborder_kw = Keyword("Scores are ordered by perturbation index:")
# Sensitivities
_sensitivitytypeorder_kw = Keyword("Scores are ordered by type")
_sensitivityindexorder_kw = Keyword("and index:")
_sensitivity_kw = Keyword("SENSITIVITY :")
_sensitivity_energyint_kw = Keyword("Energy integrated S")
_sensitivity_incenergy_kw = Keyword("Incident energy interval in MeV:")
_sensitivity_dircos_kw = Keyword("Direction cosine interval:")

# Variance of variance
_vovstar_kw = Keyword("variance of variance* :")
_sensibtomaxval_kw = Keyword("sensibility to maximum value:")
_vov_kw = Keyword("variance of variance :")

# Greenbands
_gbspectrumstep_kw = Keyword("* SOURCE SPECTRUM STEP NUMBER :")
_gbenergymin_kw = Keyword("source energy min. =")
_gbenergymax_kw = Keyword("source energy max. =")
_gbsourcenum_kw = Keyword("SOURCE NUMBER :")
_gbsourcetab_kw = Keyword("SOURCE TABULATION :")

# KIJ matrix
_kijlefteigenval_kw = Keyword("left_eigenvalues called")
_kijmkeff_kw = Keyword("kij-keff =")
_kijdomratio_kw = Keyword("dominant ratio =")
_kijeigenval_kw = Keyword("eigenvalues (re, im)")
_kijeigenvec_kw = Keyword("eigenvectors")
_kijeigenvecnotprint_kw = Keyword("KIJ eigenvectors not printed, "
                                  "increase maximum dump size if needed")
_kijmatrix_kw = Keyword("KIJ_MATRIX :")
_kijmatrixnotprint_kw = Keyword("KIJ matrix not printed, "
                                "increase maximum dump size if needed")

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

# Adjoint results (IFP for the moment)
# if IFP is changed to Wielandt in _cvgstat_kw when using Wielandt method this
# is the way to get the method name
# convergence statistics
_cvgstat_kw = Keyword("Scores for IFP convergence statistics are ordered "
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
_star_line = Suppress(Word('*'))
_equal_line = Suppress(Word('='))
_minus_line = Suppress(White() + Word('-'))


################################
#           PARSERS            #
################################

# Introduction parser
_sourceintensity = (Suppress(_sourceintensity_kw + ':')
                    + (_fnums | _unavailable_kw)
                    ('source_intensity'))
# unkown -> string not in a list, while list of float per default
_meanweightleakvals = Group(_fnums('score')
                            + Suppress("sigma =") + _fnums('sigma')
                            + Suppress('sigma% =') + _fnums('sigma%'))
_meanweightleak = (Suppress(_meanweightleakage_kw)
                   + (Suppress('=') + _meanweightleakvals('mean_weight_leak')
                      | Suppress(':') + _unknown_kw('mean_weight_leak')))
_meanweightleakin = (
    Suppress(_meanweightleakagein_kw)
    + (Suppress('=') + _meanweightleakvals('mean_weight_leak_inside')
       | Suppress(':') + _unknown_kw('mean_weight_leak_inside')))
_edbatchnum = Suppress(_edbatchnum_kw + ':') + _inums('edition_batch_number')

_meanweightrestartpart = (Suppress(_meanweightrestartpart_kw)
                          + _fnums('mean_weight_restart_particle'))
_introelts = (_meanweightleak | _meanweightleakin | _edbatchnum
              | _meanweightrestartpart)
intro = Group(_sourceintensity + _star_line + OneOrMore(_introelts))('intro')

# Conclusion parser
_simutime = Suppress(_simulationtime_kw + ':') + _fnums('simulation_time')
_exploitime = (Suppress(_exploitationtime_kw + ':')
               + _fnums('exploitation_time'))
_elapsedtime = Suppress(_elapsedtime_kw + ':') + _fnums('elapsed_time')
runtime = Group(_simutime | _elapsedtime | _exploitime)('conclu')

# Response parser
# Description of the response
_respfunc = (Suppress(_respfunction_kw + ':')
             + OneOrMore(Word(printables), stopOn=LineEnd())
             .setParseAction(' '.join)('response_function'))
# warning: order matters hier, LineEnd has to be before Optional(Word)
_respname = (Suppress(_respname_kw + ':')
             + (Suppress(LineEnd())
                | Optional(Word(printables)('response_name'))))
_scorename = (Suppress(_scorename_kw + ":")
              + Optional(Word(printables)('score_name')))
_energysplit = (Suppress(_energysplitname_kw + ':')
                + Word(printables)('energy_split_name'))
_nusplit = (Suppress(_nusplitname_kw + ':')
            + Word(printables)('nu_split_name'))
respdesc = (_respfunc + Optional(_respname) + Optional(_scorename)
            + Optional(_energysplit | _nusplit))

_respfilter = (Suppress(_respfiltered_kw) + _inums('nb_filtered_compos')
               + Suppress(_respfiltcompos_kw + ':')
               + Group(OneOrMore(Word(printables), stopOn=LineEnd()))
               .setParseAction(trans.convert_list_to_tuple)
               ('filtered_compositions'))

_particle = (Suppress(_particule_kw + ':')
             + OneOrMore(Word(alphas+','), stopOn=LineEnd())
             .setParseAction(' '.join)('particle'))
_incparticle = (Suppress(_incparticle_kw + ':')
                + Word(alphas)('incident_particle'))
_noise_equation = (Suppress(_noise_equation_kw + ':')
                   + OneOrMore(Word(alphas), stopOn=LineEnd())
                   .setParseAction(' '.join)('noise_equation'))
# response characteristics written in lower case
_reactiononnucl = (Suppress(_reactiononnucl_kw + ':')
                   + Word(printables)('reaction_on_nucleus'))
_temperature = Suppress(_temperature_kw + ':') + _fnums('temperature')
_composition = (Suppress(_composition_kw + ':')
                + Word(printables)('composition'))
_concentration = Suppress(_concentration_kw + ':') + _fnums('concentration')
_reaction = (Suppress(_reaction_kw)
             + ((Suppress(Word(alphas) + ':')
                 + Group(delimitedList(_inums, delim='+')))
                | OneOrMore(Word(alphas), stopOn=LineEnd())
                .setParseAction(' '.join))
             .setParseAction(trans.convert_list_to_tuple)('reaction'))


# Goal: when more than one reaction are required, keep characteristics grouped
# by particle, reaction, etc.
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
_nuclflags = (OneOrMore(_compodetails).setParseAction(trans.lod_to_dot)
              ('compos_details'))


# other response characteristics
_dpatype = (Suppress(_dpatype_kw)
            + OneOrMore(Word(alphas+'-,'), stopOn=LineEnd())
            .setParseAction(' '.join)('dpa_type'))
_required = (Suppress(_required_kw)
             + OneOrMore(Word(alphanums+'():'), stopOn=LineEnd())
             .setParseAction(' '.join)('required'))
_mode = Suppress(_mode_kw) + Word(alphas)('mode')
_inducedbyint = (Suppress(_inducedbyint_kw)
                 + Group(OneOrMore(_inums))
                 .setParseAction(trans.convert_list_to_tuple)
                 ('induced_by_interation'))
_notinducedbyint = (Suppress("NOT" + _inducedbyint_kw)
                    + Group(OneOrMore(_inums))
                    .setParseAction(trans.convert_list_to_tuple)
                    ('NOT_induced_by_interation'))
_fxptcontrib = (OneOrMore(Word(alphas+'()'),
                          stopOn=_fxptcontrib_kw).setParseAction(' '.join)
                ('fxpt_contribution')
                + Suppress(_fxptcontrib_kw))
_spectrumresp = Suppress(_spectrumresp_kw + ':') + Word(alphas)('spectrum')
_filters = (Suppress(_filters_kw + ':')
            + Group(OneOrMore(_inums))
            .setParseAction(trans.convert_list_to_tuple)
            ('filtered_volumes')
            + Optional(Suppress('With') + Word(alphas+'_')('filter_type')))


respcarac = (_respfilter
             | _particle
             | _incparticle
             | _noise_equation
             | _nuclflags
             | _filters
             | _required
             | _dpatype
             | _mode
             | _inducedbyint
             | _notinducedbyint
             | _fxptcontrib
             | _spectrumresp)

respintro = respdesc + ZeroOrMore(respcarac)

# Responses themselves
# Score description (not needed for KEFF)
scoremode = Suppress(_scoremode_kw + ':') + Word(alphas+'_')('scoring_mode')
# scoring zones
_score_mesh_unit = (Suppress("(in")
                    + Word(alphanums+'.^-+')('unit')
                    + Suppress(')'))
_score_meshinfo_cell_unit = (Suppress(_scoremeshinfobins_kw + '[')
                             + _fnums + Word(alphanums+' .^-+')
                             + Suppress(']'))('cell_unit')
_score_meshinfo_volume = (Suppress(_vol_kw + '[')
                          + _fnums + Word(alphanums+'.^-+')
                          + Suppress(']'))('vol_unit')
_score_meshcols = Suppress(Word(alphas)
                           + Optional(_scoremeshinfobins_kw)
                           + Word(alphas)
                           + Word(alphas+'() '))
_score_meshinfounit_cols = (Suppress(Word(alphas))
                            + _score_meshinfo_cell_unit
                            + _score_meshinfo_volume
                            + Suppress(Word(alphas) + Word(alphas+'() ')))
_score_mesh = (Optional(Suppress(_scorevolume_kw + ':')
                        + _fnums('scoring_zone_volsurf'))
               + Optional(Suppress(_scorevolumecell_kw + ':')
                          + _fnums('scoring_zone_cellvol'))
               + _scoremesh_kw('scoring_zone_type') + Suppress(':')
               + (_score_meshinfounit_cols | _score_meshcols)
               + Optional(_score_mesh_unit))
_score_allgeom = _scoreallgeom_kw('scoring_zone_type')
_score_allsources = _scoreallsources_kw('scoring_zone_type')
_score_vol = (_scorevol_kw('scoring_zone_type')
              + Suppress(_scorevolvol_kw + ':')
              + (_inums | Word(printables))('scoring_zone_id')
              + Suppress(_scorevolume_kw + ':')
              + _fnums('scoring_zone_volsurf')
              + Optional(_scorevolumeint_kw | _scorevolumenotint_kw)
              ('scoring_zone_details'))
_score_vol_sum = ((_scorevolsum_kw('scoring_zone_type')
                   + Suppress(_scorevolsumvol_kw + ':')
                   + Group(delimitedList(_inums, delim='+'))('scoring_zone_id')
                   + Suppress(_scorevolumesum_kw + ':')
                   + _fnums('scoring_zone_volsurf')))
_score_surf = (_scoresurf_kw('scoring_zone_type')
               + Suppress(_scoresurfvol_kw + ':')
               + Group(delimitedList(_inums
                                     | Word(printables, excludeChars=',')))
               ('scoring_zone_id')
               + Optional(Suppress(_scoresurface_kw + ':')
                          + _fnums('scoring_zone_volsurf'))
               + Optional(Suppress(_scoresurfaceint_kw
                                   | _scoresurfacenotint_kw)))
_score_surf_sum = (
    _scoresurfsum_kw('scoring_zone_type')
    + Suppress(_scoresurfsumfront_kw + ':')
    + delimitedList(Group(Suppress('(')
                          + delimitedList(Word(printables, excludeChars=',()')
                                          | _inums)
                          + Suppress(')')), delim='+')('scoring_zone_id')
    + Suppress(_scoresurfacesum_kw + ':')
    + _fnums('scoring_zone_volsurf'))
_score_point = (_scorepoint_kw('scoring_zone_type')
                + Suppress(':')
                + Group(_fnums + Suppress(',')
                        + _fnums + Suppress(',')
                        + _fnums)('scoring_zone_id'))
_cellelt = (Group(Suppress('(') + _inums
                  + Suppress(',') + _inums
                  + OneOrMore(
                      Group(Suppress(',') + _inums
                            + Suppress(',') + _inums
                            + Suppress(',') + _inums))
                  + Suppress(')')))
_score_cell = (_scorecell_kw('scoring_zone_type')
               + Suppress(_scorecelldet_kw)
               + Group(_cellelt
                       + ZeroOrMore(Suppress('+') + _cellelt))
               ('scoring_zone_id'))
_maillelt = (Suppress(_scoremaillevol_kw + ':') + _inums
             + Suppress(_scoremailledepth_kw + ':') + _inums
             + Suppress(_scoremaillecell_kw + ':')
             + OneOrMore(
                 Group(Suppress('(') + _inums
                       + Suppress(',') + _inums
                       + Suppress(',') + _inums + Suppress(')'))))
_score_maille = (_scoremaille_kw('scoring_zone_type')
                 + Group(_maillelt)('scoring_zone_id'))
scorezone = (Suppress(_scorezone_kw+':')
             + (_score_mesh
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
# scoring description = scoring mode + scoring zone
scoredesc = scoremode + scorezone

# Correspondence table (volumes ids and names)
corresptable = (Suppress(_corresptable_kw)
                + OneOrMore(Group(
                    Suppress(_vol_kw + ':')
                    + _inums('volume_id')
                    + Suppress(Keyword('is :'))
                    + Word(printables)('volume_name')), stopOn=_endtable)
                ('correspondence_table'))


# RESPONSE RESULTS


def _set_no_unit_case(toks):
    '''Deal with the "not unit" case'''
    if len(toks) == 1:
        return {'uscore': '', 'usigma': toks[0]}
    LOGGER.warning("more than one unit, please check: %s", toks)
    return None


def _rm_blanks(toks):
    '''Remove leading and trailing spaces (not the ones inside the string)'''
    return toks[0].strip()


# Default integrated result
_numdiscbatch = (Suppress(_numbatchs1stdiscarded_kw + ':')
                 + _inums('discarded_batches'))
_numusedbatch = Suppress(_numbatchsused_kw + ':') + _inums('used_batches')
_integratedres_name = _integratedres_kw | Word(alphas) + _integratedres_kw
_integratedres = _fnums('score') + _fnums('sigma')
_unitsres = (Suppress(_units_kw)
             + (Word('%').setParseAction(_set_no_unit_case)
                | (Word(alphanums+'.^-+ ').setParseAction(_rm_blanks)('uscore')
                   + Word('%')('usigma'))))
# rejection in vov and sensibility cases
_rejection = (Suppress('[')
              + OneOrMore(Word(alphanums+'<>.+-')).setParseAction(' '.join)
              ('rejection')
              + Suppress(']'))
_vovnostar = Suppress(_vov_kw) + Group(_fnums('score'))('vov_res')
_vovstar = Group(
    Suppress(_vovstar_kw) + _fnums('score')
    + Suppress('[') + _fnums('sigma') + Suppress(']')
    + Optional(_rejection))('vovstar_res')
_sensibtomaxval = Group(
    Suppress(_sensibtomaxval_kw) + _fnums('max_val')
    + Optional(_rejection))('sensibility_res')
_vov = (_vovnostar | _vovstar + _sensibtomaxval)
# best result
bestres = (Group(Suppress(_bestresdiscbatchs_kw) + _inums('discarded_batches')
                 + Suppress("batches")
                 + _minus_line
                 + _numusedbatch + _fnums('score') + _fnums('sigma'))
           ('best_result_res'))


integratedres = (Group(Optional(Suppress(_integratedres_name))
                       + Optional(_numdiscbatch)
                       + ((_numusedbatch + _integratedres)
                          | _notconverged_kw('not_converged')))
                 ('integrated_res')
                 + Optional(_vov))

genericscoreblock = (Group(Optional(Suppress(_integratedres_name))
                           + ((_numusedbatch
                               + _integratedres
                               + Optional(_unitsres))
                              | _notconverged_kw('not_converged')))
                     ('generic_res').setParseAction(trans.group_to_dict))


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
_spectrumunits = Group(Suppress(_units_kw)
                       + Word(alphanums+'.^-+%') * 4)('units')
_spectrumbin = _fnums + Suppress('-') + _fnums
_spectrumcols = Suppress((_spgroupwunit_kw | _spgroup_kw)
                         + _spscore_kw
                         + _spsigma_kw
                         + _spscovlethargy_kw)
_spectrumvals = (Group(_spectrumbin + _fnums + _fnums + _fnums)
                 .setFailAction(trans.fail_spectrum))
_spectrum = (Suppress(_spectrum_kw)
             + _numdiscbatch
             + _spectrumcols
             + Optional(_spectrumunits)
             + OneOrMore(_spectrumvals, stopOn=_endtable)('spectrum_vals'))
spectrumblock = (Group(OneOrMore
                       (Group(OneOrMore(_timestep | _muangzone | _phiangzone)
                              + _spectrum
                              + Optional(integratedres)))
                       | Group(_spectrum))('spectrum_res'))


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


# Nu spectrum
_nuspectrumunits = Group(Suppress(_units_kw)
                         + Word(alphanums+'.^-+%') * 3)('units')
_nuspectrumcols = Suppress(_nusprange_kw + _spscore_kw + _spsigma_kw)
_nuspectrumvals = (Group(_spectrumbin + _fnums + _fnums)
                   .setFailAction(trans.fail_spectrum))
_nuspectrum = (Suppress(_nuspectrum_kw)
               + _numdiscbatch
               + _nuspectrumcols
               + Optional(_nuspectrumunits)
               + OneOrMore(_nuspectrumvals, stopOn=_endtable)('spectrum_vals'))
nuspectrumblock = Group(Group(_nuspectrum + integratedres))('nu_spectrum_res')


# ZA spectrum
_zaspectrumunits = Group(Suppress(_units_kw)
                         + Word(alphanums+'.^-+%') * 2)('units')
_zaspectrumcols = Suppress(_zaspid_kw + _spscore_kw + _spsigma_kw)
_zaspectrumbin = (Suppress('(') + _inums + Suppress(',')
                  + _inums + Suppress(')'))
_zaspectrumvals = (Group(_zaspectrumbin + _fnums + _fnums)
                   .setFailAction(trans.fail_spectrum))
_zaspectrum = (Suppress(_zaspectrum_kw)
               + _numdiscbatch
               + _zaspectrumcols
               + Optional(_zaspectrumunits)
               + OneOrMore(_zaspectrumvals, stopOn=_endtable)('spectrum_vals'))
zaspectrumblock = Group(Group(_zaspectrum + integratedres))('za_spectrum_res')


def _printtoks(toks):
    print(toks)


# Entropy
_boltzmannentropy = (Suppress(_boltzmannentropy_kw)
                     + _fnums('boltzmann_entropy_res'))
_shannonentropy = Suppress(_shannonentropy_kw) + _fnums('shannon_entropy_res')
entropy = _boltzmannentropy + _shannonentropy


# Mesh
_mesh_energyrange = (Group(Suppress(_energyrange_kw + "(in") + Word(alphas)
                           + Suppress('):') + _fnums + Suppress('-') + _fnums)
                     ('mesh_energyrange'))
_mesh_energyintegrated = ((Suppress(_integratedres_name) + Suppress(':'))
                          ('mesh_energyintegrated'))
_mesh_energyline = _mesh_energyrange | _mesh_energyintegrated
_meshres = Group(
    _mesh_energyline
    + Group(originalTextFor(
        OneOrMore(Word(printables), stopOn=_endtable)))('mesh_vals')
    + Optional(Group(entropy)('entropy')))
meshblock = Group(OneOrMore(Group(_timestep
                                  + Optional(_score_mesh_unit)
                                  + Group(OneOrMore(_meshres))('meshes')
                                  + Optional(integratedres)))
                  | Group(Group(OneOrMore(_meshres))('meshes')))('mesh_res')


# KIJ matrix
# before keff as KIJ ESTIMATOR used to evaluate KEFF...
# definition de kijdim en variable globale ne fonctionne pas car creee avant
# solution : utiliser forward pour le redefinir !


def _set_kijdim(toks):
    _kijdim = len(toks)
    _kijeigenvec << Group(_fnums * _kijdim)  # pylint: disable=W0106
    _kijmatrix << Group(_fnums * _kijdim)  # pylint: disable=W0106


_kijsum = Group(Optional(Suppress(_kijlefteigenval_kw))
                + Suppress(_kijmkeff_kw) + _fnums
                + Suppress(_kijdomratio_kw) + _fnums)('kijmkeff_res')
_kijeigenval = Group(_fnums + _fnums)
_kijeigenvec = Forward()
_kijmatrix = Forward()
_kijeigenvaltab = (Suppress(_kijeigenval_kw)
                   + (OneOrMore(_kijeigenval).setParseAction(_set_kijdim))
                   ('kij_eigenval'))
_kijeigenvectab = ((Suppress(_kijeigenvec_kw) + (OneOrMore(_kijeigenvec)))
                   | _kijeigenvecnotprint_kw)('kij_eigenvec')
_kijmatrixtab = (Suppress(_kijmatrix_kw)
                 + ((OneOrMore(_kijmatrix)) | _kijmatrixnotprint_kw)
                 ('kij_matrix'))
kijres = (Group(Suppress(_integratedres_name)
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
kijsources = (Group(Suppress(_integratedres_name)
                    + _numusedbatch
                    + Suppress(_kijsources_kw)
                    + Optional(_kijsourcesorder)
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
                 + Suppress(_kijmkeff_kw) + _fnums('kij_mkeff'))

_idline = Forward()
_matline = Forward()
_kijkeffev = OneOrMore(Group(_inums + _fnums)).setParseAction(_define_kij_dim)
_kijkeffevtab = Group(Suppress(_kijkeffevid_kw) + _kijkeffev)('kij_leigenvec')
_defmatrix = _idline + _minus_line + OneOrMore(_matline + _minus_line)
_kijkeffmatrix = (Group(Suppress(_kijkeffmat_kw) + _defmatrix)
                  ('kij_matrix'))
_kijkeffstdmatrix = (Group(Suppress(_kijkeffstddevmat_kw) + _defmatrix)
                     ('kij_stddev_matrix'))
_kijkeffsensibmatrix = (Group(Suppress(_kijkeffsensibilitymat_kw) + _defmatrix)
                        ('kij_sensibility_matrix'))

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
_autokeffres = ((_keffresblock + _correlationblock + _fullcombestimation)
                | _notconverged_kw('not_converged'))
_warnkeff = (Suppress(_warning_kw)
             + _warn_combkeff_kw.setParseAction(' '.join)('warning'))
keffblock = Group(Suppress(_integratedres_name)
                  + _numusedbatch
                  + (_autokeffres | _warnkeff)
                  ).setParseAction(trans.convert_keff)('keff_res')


# Keff as historical response
_bestresestim = (OneOrMore(Word(alphas), stopOn=_estimator_kw)
                 .setParseAction(' '.join)('keff_estimator')
                 + Suppress(_estimator_kw))
_bestresdiscbatch = (Suppress(_bestresdiscbatchs_kw)
                     + _inums('best_disc_batchs')
                     + Suppress("batches"))
_bestkeff = (Suppress(Keyword("keff") + '=') + _fnums('keff')
             + Suppress(Keyword("sigma") + '=') + _fnums('sigma')
             + Suppress(Keyword("sigma%") + '=') + _fnums('sigma%'))
_equivkeff = Suppress(_equivkeff_kw) + _fnums('equivalent_keff')
_bestkeffpestim = (Group(_notconverged_kw('not_converged')
                         | Group(Optional(_bestresdiscbatch)
                                 + _numusedbatch
                                 + _bestkeff
                                 + Optional(_equivkeff))('keff_auto'))
                   ('results'))
_bestreskeff = Group(_bestresestim + _minus_line + _bestkeffpestim)
_warnfixedsources = Group(Suppress(_warning_kw) + _minus_line
                          + _warn_fixsourcekeff_kw('warning'))
_bestresblock = OneOrMore(_bestreskeff, stopOn="KIJ")
autokeffblock = Group(Group(Optional(_warnfixedsources)
                            + _bestresblock
                            + Optional(_kijkeffblock))
                      .setParseAction(trans.convert_keff_auto))('keff_auto')


# MED files
medfile = (Suppress((_creationmedfile_kw | _creationfile_kw) + ':')
           + Word(alphanums+'/_.')('med_file')
           + Suppress(_medmeshid_kw + Word(alphanums+'_.')))


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
gbblock = Group(OneOrMore(_gbstep))('green_bands_res')


# Scores ordered by nuclei and precursor families, IFP outputs
_generic_score = Suppress(':') + _fnums + _fnums
# Nuclei order alone
_scorepernucleus = Group(Word(alphanums) + _generic_score)
_nucleiorder = (Suppress(_nucleiorder_kw)
                + ZeroOrMore(_scorepernucleus)('score_per_nucleus'))
# Families order alone
_scoreperfamily = Group(Suppress("i =") + _inums + _generic_score)
_familyorder = (Suppress(_familiesorder_kw)
                + ZeroOrMore(_scoreperfamily)('score_per_family'))
# Nuclei and families order
_nucleusid = Suppress(_nucleus_kw) + Word(alphanums) + Suppress('.')
_nucleusfam = Group(_nucleusid + _familyorder)
_nuclfamorder = (Suppress(_nucleifamilyorder_kw)
                 + ZeroOrMore(_nucleusfam)('score_per_nucleus_family'))
# Perturbation index order
_scoreperpertuind = Group(Suppress("i =") + _inums + _generic_score)
_perturborder = (Suppress(_perturborder_kw)
                 + ZeroOrMore(_scoreperpertuind)('score_per_perturbation'))
# Convergence statistics
_cvgline = Group(Suppress("L =") + _inums + _generic_score)
_cvgstat = (Suppress(_cvgstat_kw)
            + ZeroOrMore(_cvgline)('score_per_length'))
# results from adjoint calculation
adjointres = (Group(Group(Suppress(_integratedres_name)
                          + _numusedbatch
                          + Group(_nuclfamorder
                                  | _nucleiorder
                                  | _familyorder
                                  | _perturborder
                                  | _cvgstat)('adj_res')
                          + Optional(_unitsres)
                          ).setParseAction(trans.convert_generic_adjoint))
              )('adjoint')
# Convergence statistics
_kingcritline = Group(Suppress("CRITICALITY SOURCE") + _fnums + _fnums)
_kingtimestepline = Group(Suppress("END OF TIME STEP ") + Suppress(_inums)
                          + _fnums + _fnums)
_kingstat = Group(_kingcritline
                  + ZeroOrMore(_kingtimestepline))('kin_generic_res')
kingres = (Group(Suppress(_integratedres_name)
                 + _numusedbatch
                 + _kingstat
                 + Optional(_unitsres)('units')
                 ).setParseAction(trans.convert_generic_kinetic)
           )('kinetic_generic')
# sensitivities
_sensitivityorder = (Suppress(_sensitivitytypeorder_kw)
                     + OneOrMore(Word(alphas + '_,()'),
                                 stopOn=_sensitivityindexorder_kw)
                     .setParseAction(' '.join)
                     + Suppress(_sensitivityindexorder_kw))
_sensitivity_type = (OneOrMore(Word(alphas.upper()), stopOn=_sensitivity_kw)
                     .setParseAction(' '.join)
                     + Suppress(_sensitivity_kw))('typeI')
_sensitivity_index = Group(
    Suppress("i =") + _inums('sensitivity_index') + Suppress(';')
    + Suppress("NUCLEUS :") + Word(alphanums + '_')('sensitivity_nucleus')
    + Suppress(',') + Suppress("TYPE :")
    + Word(alphanums.upper() + '_() ')('sensitivity_reaction'))
_sensitivity_dircos = Group(Suppress(_sensitivity_dircos_kw)
                            + _fnums*2)('direction_cosine')
_sensitivity_energyinc = Group(Suppress(_sensitivity_incenergy_kw)
                               + _fnums*2)('energy_incident')
_sensitivity_cols = (Keyword("E min") + Keyword("E max")
                     + Keyword("S(E)") + Keyword("sigma"))
_sensitivity_vals = Group(_fnums*4)
_sensitivity_energyint = Group(Suppress(_sensitivity_energyint_kw)
                               + _integratedres)
_sensitivity_res = Group(_sensitivity_index('charac')
                         + Group(OneOrMore(Group(
                             ZeroOrMore(_sensitivity_dircos
                                        | _sensitivity_energyinc)
                             + Suppress(_sensitivity_cols)
                             + OneOrMore(_sensitivity_vals)('values'))))
                         ('vals')
                         + _sensitivity_energyint('energy_integrated'))
_sensitivity = (Suppress(_sensitivityorder)
                + (OneOrMore(Group(_sensitivity_type('sensitivity_type')
                                   + OneOrMore(_sensitivity_res)('res')))))
sensitivityres = Group(Group(Optional(Suppress(_integratedres_name))
                             + _numusedbatch
                             + Group(_sensitivity)('sensit_res')
                             + Optional(_unitsres)('units'))
                       .setParseAction(trans.convert_sensitivities)
                       )('sensitivity')


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
_adjcrit_ed_intro = _star_line + Suppress(_ifpadjcriticality_kw) + _star_line
_ifpadjcrit_intro = Group(Word(alphas+'_')('ifp_response')
                          + _scorename
                          + Suppress(_ifpadjcyclelength_kw)
                          + _inums('ifp_cycle_length')
                          + (Optional(_ifpadjnormalizedres_kw
                                      .setParseAction(_rename_norm_kw))
                             ('normalized'))
                          + _star_line)
_ifpadjbinval = Forward()
_ifpadjcoordinate = Word(alphas) + Suppress(_ifpadjminmax_kw)
_ifpadjcoordinates = ((Optional(_ifpadjvol_kw) + OneOrMore(_ifpadjcoordinate))
                      .setParseAction(_define_ifp_adj_table_dim))
_ifpadjcolumns = _ifpadjcoordinates + _ifpadjscore_kw + _spsigma_kw
_ifpadjline = Group(_ifpadjbinval + _fnums + _fnums)
_ifpadjvalues = OneOrMore(_ifpadjline)
_adjcritblock = Group(_ifpadjcrit_intro('ifp_adjoint_criticality_intro')
                      + _ifpadjcolumns('columns')
                      + _ifpadjvalues('values')
                      + _star_line)
ifpadjointcriticality = (Group((_adjcrit_ed_intro + OneOrMore(_adjcritblock))
                               .setParseAction(trans.convert_ifp_adj_crit_ed))
                         ('ifp_adjoint_crit_edition'))

# Perturbations
_perturank = Suppress(_perturank_kw) + _inums('perturbation_rank')
_pertumethod = (Suppress(_pertumethod_kw)
                + OneOrMore(Word(alphas), stopOn=LineEnd())
                .setParseAction(' '.join)('perturbation_method'))
_pertuorder = Suppress(_pertuorder_kw) + _inums('perturbation_order')
_pertutype = Suppress(_pertutype_kw) + Word(alphas)('perturbation_type')
_pertucompo = (Suppress(_pertucompo_kw)
               + Word(alphanums+'_')('perturbation_composition'))
pertu_desc = (Group(Suppress(_perturbation_kw)
                    + _perturank
                    + _pertumethod
                    + Optional(_pertuorder)
                    + _pertutype
                    + _pertucompo)('perturbation_desc'))

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
scoreblock = (Group(scoredesc + (OneOrMore(vovspectrumblock
                                           | spectrumblock
                                           | nuspectrumblock
                                           | zaspectrumblock
                                           | meshblock
                                           | medfile
                                           | integratedres
                                           | bestres
                                           | uncertblock
                                           | uncertintegblock
                                           | gbblock
                                           | corresptable)))
              .setParseAction(trans.convert_score))

listscoreblock = (Group(OneOrMore(scoreblock)
                        .setParseAction(trans.index_elements('score_index')))
                  ('score_res'))

# Response block
responseblock = Group(keffblock
                      | kijres
                      | kijsources
                      | adjointres
                      | kingres
                      | sensitivityres
                      | genericscoreblock
                      | listscoreblock)('results')

response = (Group(_star_line
                  + respintro
                  + _star_line
                  + responseblock)
            .setParseAction(trans.finalize_response_dict))

listresponses = Group(OneOrMore(response).setParseAction(
    compose2(trans.extract_all_metadata,
             trans.index_elements('response_index'))))('list_responses')

perturbation = (OneOrMore(Group(pertu_desc + listresponses)
                          .setParseAction(trans.propagate_all_metadata))
                .setParseAction(trans.index_elements('perturbation_index'))
                ('perturbation'))


################################
#         DEBUG PARSER         #
################################

# debug grammar, to be used with parse_debug (only for parsing development)
t4debug_gram = (OneOrMore((intro
                           + OneOrMore(listresponses | ifpadjointcriticality
                                       | autokeffblock | perturbation
                                       | Suppress(contribpartblock)
                                       | OneOrMore(runtime)))
                          .setParseAction(trans.to_final_dict))
                .setParseAction(dump_in_logger)
                | intro + OneOrMore(runtime)).setFailAction(trans.fail_parsing)


################################
#        GENERAL PARSER        #
################################

t4gram = (OneOrMore((intro
                     + ZeroOrMore(listresponses | ifpadjointcriticality
                                  | autokeffblock | perturbation
                                  | Suppress(contribpartblock))
                     + runtime)
                    .setParseAction(trans.to_final_dict))
          .setParseAction(dump_in_logger)
          ).setFailAction(trans.fail_parsing)
