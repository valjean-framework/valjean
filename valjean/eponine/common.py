'''This module provides generic functions to convert parsing outputs in numpy
objects.

Inputs (outputs from parsers) should be python lists or dictionary,
dictionary keys should be the same in all parsers...

..note:: not a standalone code, needs inputs
         To be tested in a more general context.
'''

import sys
import logging
import numpy as np


if "mem" not in sys.argv:
    def profile(func):
        return func


LOGGER = logging.getLogger(__name__)
ITYPE = np.int32
FTYPE = np.float32


def _get_number_of_bins(spectrum):
    '''Get number of bins (time, mu and phi angles and energy).
    :param spectrum: input spectrum (full as various levels of list or
    dictionary may be needed.
    :returns: 4 integers
               - nphibins = number of bins in phi angle, default = 1
               - nmubins = number of bins in mu angle, default = 1
               - ntbins = number of bins in time, default = 1
               - nebins = number of bins in energy, no default
    Mu and phi angle are angles relative to the direction of the particle.
    '''
    # complication: time, mu and phi angles are always in that order
    # and only appears when changing value -> complication for number of "bins"
    # all the available coordinates are listed in element 0
    # if more than one loop necessary to get size of each
    nphibins = (spectrum[-1]["phi_angle_zone"][0]+1
                if "phi_angle_zone" in spectrum[0]
                else 1)
    nmubins = (spectrum[-int(nphibins)]["mu_angle_zone"][0]+1
               if "mu_angle_zone" in spectrum[0]
               else 1)
    ntbins = (spectrum[-int(nphibins)*int(nmubins)]["time_step"][0]+1
              if "time_step" in spectrum[0]
              else 1)
    nebins = len(spectrum[0]["spectrum_vals"])
    return nphibins, nmubins, ntbins, nebins


def _fill_spectrum_and_bins(spectrum, valspectrum, valsintres,
                            ebins, tbins, mubins, phibins):
    '''Fill spectrum, bins and integrated result if exists
    :param spectrum: input spectrum (loop over it so everything needed)
    :param valspectrum: 7 dimensions numpy structured array
        v[s0, s1, s2, E, t, mu, phi] = (score, sigma, score/lethargy)
    :param valsintres: 7 dimensions numpy structured array
        v[s0, s1, s2, E, t, mu, phi] = (score, sigma)
    :param ebins: energy bins
    :param tbins: time bins
    :param mubins: mu angle (direction) bins
    :param phibins: phi angle (direction) bins
    '''
    itime, imu, iphi = 0, 0, 0
    for ispec in spectrum:
        # Fill bins -> caution to not replicate them
        if 'time_step' in ispec:
            itime = ispec['time_step'][0]
            tbins.append(ispec['time_step'][1])
        if 'mu_angle_zone' in ispec:
            imu = ispec['mu_angle_zone'][0]
            if itime == 0:
                mubins.append(ispec['mu_angle_zone'][1])
        if 'phi_angle_zone' in ispec:
            iphi = ispec['phi_angle_zone'][0]
            if itime == 0 and imu == 0:
                phibins.append(ispec['phi_angle_zone'][1])

        # Fill spectrum values
        for ienergy, ivals in enumerate(ispec['spectrum_vals']):
            if itime == 0 and imu == 0 and iphi == 0:
                ebins.append(ivals[0])
            index = (0, 0, 0, ienergy, itime, imu, iphi)
            valspectrum[index] = np.array(tuple(ivals[2:]),
                                          dtype=valspectrum.dtype)

        # Fill integrated result if exist
        if 'integrated_res' in ispec:
            iintres = ispec['integrated_res']
            index = (0, 0, 0, 0, itime, imu, iphi)
            valsintres[index] = np.array((iintres['score'], iintres['sigma']),
                                         dtype=valsintres.dtype)


def _add_last_bins(spectrum, ebins, tbins, mubins, phibins):
    '''Add last bin to the bins array.
    :param spectrum: full spectrum to be able to access all elements
    :param ebins: numpy array of energy bins
    :param tbins: numpy array of time bins
    :param mubins: numpy array of mu angle bins
    :param phibins: numpy array of phi angle bins
    :returns: ebins, tbins, mubins and phi bins will be updated with the
              missing edge
    ..note: Few remarks:
      * at that step len(ibins) = number of bins, except when no binning was
        required (for time, mu and phi). The final length of ibins arrays
        should be number of bins + 1 to have all bins edges.
      * the last bin can be put as first or last bin of the array for time, mu
        and phi, depending on required order (increasing or decreasing),
        because first number is always min and second max
      * in energy case, if increasing order: min - max, else max - min, so
        adding last value in last position is always fine.
    '''
    nphibins = len(phibins) if phibins else 1
    nmubins = len(mubins) if mubins else 1
    ebins.append(spectrum[-1]['spectrum_vals'][-1][1])
    if 'time_step' in spectrum[0]:
        if len(tbins) > 1 and tbins[0] > tbins[1]:
            tbins.insert(0, spectrum[0]['time_step'][2])
        else:
            tbins.append(spectrum[-int(nphibins)*int(nmubins)]['time_step'][2])
    if 'mu_angle_zone' in spectrum[0]:
        if len(mubins) > 1 and mubins[0] > mubins[1]:
            mubins.insert(0, spectrum[0]['mu_angle_zone'][2])
        else:
            mubins.append(spectrum[-int(nphibins)]['mu_angle_zone'][2])
    if 'phi_angle_zone' in spectrum[0]:
        if len(phibins) > 1 and phibins[0] > phibins[1]:
            phibins.insert(0, spectrum[0]['phi_angle_zone'][2])
        else:
            phibins.append(spectrum[-1]['phi_angle_zone'][2])


# def _flip_bins(valspectrum, valsintres=None,
#                ebins=None, tbins=None, mubins=None, phibins=None):
def _flip_bins(valslist, ebins=None, tbins=None, mubins=None, phibins=None):
    '''Flip bins if given in decreasing order in the output listing.
    Depending on the required grid (GRID or DECOUPAGE) energies, times, mu and
    phi can be given from upper edge to lower edge. This is not convenient for
    post-traitements, especially plots. They have to be flipped at a moment,
    here or later, easiest is here, and all results will look the same :-).

    :param valspectrum: 7-dim numpy structured array corresponding to spectrum
                        or mesh
    :param valsintres: 7-dim numpy structured array for integrated result (if
                       available)
    :param ebins: energy bins
    :param tbins: time bins
    :param mubins: mu angle bins
    :param phibins: phi angle bins
    :returns: all these objects are modified if necessary in the function

    ..note: array and list modification is not possible directly in a function,
            this is why the '[:]' appear.
    '''
    LOGGER.info("In _flip_bins")
    # arrays and lists are passed as arguments, to get them updated [:] needs
    # to be added (else modification only happens in the function)
    if ebins and ebins[0] > ebins[1]:
        ebins[:] = ebins[::-1]
        for vals in valslist:
            if vals is not None:
                vals[:] = np.flip(vals, axis=3)
    if tbins and tbins[0] > tbins[1]:
        tbins[:] = tbins[::-1]
        for vals in valslist:
            if vals is not None:
                vals[:] = np.flip(vals, axis=4)
    if mubins and mubins[0] > mubins[1]:
        mubins[:] = mubins[::-1]
        for vals in valslist:
            if vals is not None:
                vals[:] = np.flip(vals, axis=5)
    if phibins and phibins[0] > phibins[1]:
        phibins[:] = phibins[::-1]
        for vals in valslist:
            if vals is not None:
                vals[:] = np.flip(vals, axis=6)


def convert_spectrum(spectrum, specols=('score', 'sigma', 'score/lethargy')):
    '''Convert specrtum results in 7D numpy structured array.
    :param spectrum: list of spectra.
                     Accepts time and (direction) angular grids.
    :type spectrum: list
    If more than one grid (time and mu, mu and phi or the three) order is
    always kept in TRIPOLI listings: time -> mu -> phi.
    Phi cannot be used alone. Mu angle is not the same if ANGULAR or 2D_ANGULAR
    grid used (see user guide).
    In the listing, first is not repeated at each step and needs to be
    propagated to the second, third... An other consequence is the repetition
    of the binning for the second (and third) coordinates, so needs additional
    care. The binning is presented as min then max value for each bin, what is
    a different behaviour from energy bins (in spectrum) and conditional
    treatment based on the order of the required grid (increasing or
    decreasing).
    If no time, no mu and phi grids are required, 1 bin is considered for these
    dimensions (so 0e bin in the array) and no binning is given.
    :param specols: list of the names of the columns.
                    Default = ['score', 'sigma', 'score/lethargy']
    :type specols: list of strings
    :returns: dictionary with keys and elements
              - 'spectrum': 7 dimensions numpy structured array with related
                 binnings as numpy arrays
                 v[s0, s1, s2, E, t, mu, phi] = (score, sigma, score/lethargy)
                 s0, s1, s2 = space coordinates (not specified in spectra, so
                 one bin each)
                 E = energy, given in spectrum
                 t = time
                 mu = cos(theta), with theta defined as
                        * normal to surface used in SURF if ANGULAR used
                        * theta in the global frame if 2D_ANGULAR used
                 phi = direction angle in global frame
                        (only used in 2D_ANGULAR grid)
                 sigma is in %
              - 'disc_batchs': number of discarded batchs for the score
              - 'ebins': energy binning
              - 'tbins': time binning if time grid required
              - 'mubins': mu binning if mu grid required
              - 'phibins': phi binning if phi grid required
              - 'integrated_res': 7 dimensions numpy structured array
                 v[s0, s1, s2, E, t, mu, phi] = (score, sigma)
                 same meaning as for spectrum
                 facultative, seen when time required alone and sometimes
                 when neither time nor mu nor phi are required
              - 'used_batch': number of used batchs (only if integrated result)
    '''
    nphibins, nmubins, ntbins, nebins = _get_number_of_bins(spectrum)
    LOGGER.debug("nebins = %d, ntbins = %d, nmubins = %d, nphibins = %d",
                 nebins, ntbins, nmubins, nphibins)
    phibins, mubins, tbins, ebins = [], [], [], []
    # spectrum
    indspectrum = (1, 1, 1, nebins, ntbins, nmubins, nphibins)
    dtspectrum = np.dtype({'names': specols,
                           'formats': [FTYPE]*len(specols)})
    valspectrum = np.empty((indspectrum), dtype=dtspectrum)

    # integrated result (initialized in all cases)
    indintres = (1, 1, 1, 1, ntbins, nmubins, nphibins)
    dtintres = np.dtype([('score', FTYPE), ('sigma', FTYPE)])
    usedbatchs, valsintres = ((spectrum[0]['integrated_res']['used_batch'],
                               np.empty(indintres, dtype=dtintres))
                              if 'integrated_res' in spectrum[0]
                              else (0, None))

    # Fill spectrum, bins and integrated result if exists
    _fill_spectrum_and_bins(spectrum, valspectrum, valsintres,
                            ebins, tbins, mubins, phibins)

    # Add max bin edge (binning dim = N+1, where N = number of bins)
    _add_last_bins(spectrum, ebins, tbins, mubins, phibins)

    # Flip bins if needed (has to be done in bins arrays and in spectrum or
    # integrated result)
    _flip_bins(valspectrum, valsintres, ebins, tbins, mubins, phibins)
    print("ebins after:", ebins)
    print(np.squeeze(valspectrum))

    # Build dictionary to be returned
    convspec = {'disc_batch': spectrum[0]['disc_batch'],
                'ebins': np.array(ebins),
                'spectrum': valspectrum}
    if 'time_step' in spectrum[0]:
        convspec['tbins'] = np.array(tbins)
    if 'mu_angle_zone' in spectrum[0]:
        convspec['mubins'] = np.array(mubins)
    if 'phi_angle_zone' in spectrum[0]:
        convspec['phibins'] = np.array(phibins)
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = valsintres
        convspec['used_batch'] = usedbatchs
    return convspec


def _get_number_of_space_bins(meshvals):
    '''Get number of space bins used in meshes.

    This function is mainly used when meshes are not entirely saved (tests, or
    useless in the considered case). The limit on the number of lines of mesh
    in the listing does not necessarly match a completed mesh dimension.

    :param meshvals: list of meshes, with mesh [[s0, s1, s2] tally sigma]
                     s0, s1 and s2 being the space coordinates
    :returns: 3 integers
                - ns0bins: number of bins in the s0 dimension
                - ns1bins: number of bins in the s1 dimension
                - ns2bins: number of bins in the s2 dimension
    '''
    lastspacebin = meshvals[-1][0]
    ns0bins = lastspacebin[0]+1
    ns2bins = (meshvals[-int(lastspacebin[2]+2)][0][2]+1
               if lastspacebin[2]+1 < len(meshvals)
               else lastspacebin[2]+1)
    ns1bins = (meshvals[-int(ns2bins+1)][0][1]+1
               if (len(meshvals) % (ns0bins*ns2bins) != 0
                   and lastspacebin[1] < meshvals[-int(ns2bins+1)][0][1])
               else lastspacebin[1]+1)
    return ns0bins, ns1bins, ns2bins


def _fill_mesh(npvals, mesh, ebin=0, tbin=0, mubin=0, phibin=0):
    '''Fill the mesh in the numpy array
    :param npvals: numpy array previously initialized
                   7-dimensions structured array
                   v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
    :param mesh: list of mesh elements, one element being
                 [[s0, s1, s2] tally sigma]
    :param ebin: number of energy bin to fill, default = 0
    :param tbin: number of time bin to fill, default = 0
    :param mubin: number of mu angle bin to fill, default = 0
    :param phibin: number of phi angle bin to fill, default = 0
    :returns: updated npvals
    '''
    for smesh in mesh:
        index = (smesh[0][0], smesh[0][1], smesh[0][2],
                 ebin, tbin, mubin, phibin)
        npvals[index] = np.array(tuple(smesh[1:]), dtype=npvals.dtype)
    return npvals


def convert_mesh(mesh):
    '''Convert mesh in 7-dimensions numpy array.
    :param mesh: Each element of the list is one energy range
                 mesh[i]['mesh_energyrange'][j][[s0, s1, s2], tally, sigma]
                 with i number of energy range and j number of space bin
                 (s0, s1, s2)
    :type mesh: list of dictionaries
    :returns: python dictonary with keys
                - eunit: the energy unit (might be modified of other additional
                  variables are needed)
                - ebins: energy bin limits (size = number of elts + 1)
                - vals: numpy structured array of dimension 7
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  s0, s1, s2 = space coordinates,
                               examples: (x, y, z), (r, phi, theta), etc.
                  E = energy
                  t = time
                  mu, phi = direction angles (mu = cos(theta))
    '''
    print("Number of mesh:", len(mesh))
    print("Mesh keys:", list(mesh[0].keys()))
    print(mesh)
    eunit = mesh[0]['mesh_energyrange'][0]
    ebins = []
    dtmesh = np.dtype([('tally', FTYPE), ('sigma', FTYPE)])
    # dimensions/number of bins of space coordinates are given by last bin
    ns0bins, ns1bins, ns2bins = _get_number_of_space_bins(mesh[0]['mesh_vals'])
    LOGGER.info("ns0bins = %d, ns1bins = %d, ns2bins = %d",
                ns0bins, ns1bins, ns2bins)

    # up to now to mesh splitted in time, mu or phi angle seen
    # index = (lastspacebin[0]+1, lastspacebin[1]+1, lastspacebin[2]+1,
    index = (ns0bins, ns1bins, ns2bins, len(mesh), 1, 1, 1)
    vals = np.empty(index, dtype=dtmesh)
    for inde, emesh in enumerate(mesh):
        if emesh['mesh_energyrange'][0] != eunit:
            LOGGER.warning("[31mStrange: different units in energy bins[0m")
        ebins.append(emesh['mesh_energyrange'][1])
        _fill_mesh(vals, emesh['mesh_vals'], inde)
    ebins.append(mesh[-1]['mesh_energyrange'][2])
    _flip_bins(vals, None, ebins, None, None, None)
    print("[38;5;141m", ebins, "[0m")
    return {'eunit': eunit,
            'ebins': np.array(ebins),
            'vals': vals}


def get_energy_bins(meshes):
    nbebins = 0
    for mesh in meshes:
        if 'mesh_energyrange' in mesh:
            nbebins += 1
    return nbebins


def convert_mesh_with_time(meshres):
    '''Convert mesh in 7-dimensions numpy array.
    :param meshres: Mesh result constructed as:
                 [{'time_step': [], 'meshes': [], 'integrated_res': {}}, {}].
                 The list 'meshes' corresponds to mesh results:
                 [{'mesh_energyrange': [], 'mesh_vals': []},
                  {'mesh_energyintegrated':, 'mesh_vals': []}]
                 Each element of the list corresponding to the key 'mesh_vals'
                 is constructed as: [[s0, s1, s2], tally, sigma].
                 Keys 'meshes' and 'mesh_energyrange' should always be there
                 (of course also 'mesh_vals').
    :type meshres: list of dictionaries
    :returns: python dictonary with keys
                - 'mesh': numpy structured array of dimension 7
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  s0, s1, s2 = space coordinates,
                               examples: (x, y, z), (r, phi, theta), etc.
                  E = energy
                  t = time
                  mu, phi = direction angles (mu = cos(theta))
                - 'eunit': the energy unit (might be modified of other
                  additional variables are needed)
                - 'ebins': energy bin limits (size = number of elts + 1)
                - 'tbins': time binning if time grid required
                - 'energy_integrated_mesh': 7 dimensions numpy structured array
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  corresponding to mesh integreted on energy (facultative)
                - 'integrated_res': 7 dimensions numpy structured array
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  corresponding to mesh integrated over energy and space
                  facultative, available when time grid is required (so
                  corresponds to integreated results splitted in time)
                - used_batch: number of used batchs (only if integrated result)
    '''
    LOGGER.info("In convert_mesh_with_time")
    LOGGER.debug("Number of mesh results: %d", len(meshres))
    ebins, tbins = [], []
    dtmesh = np.dtype([('tally', FTYPE), ('sigma', FTYPE)])
    LOGGER.debug("keys of meshes: %s", str(list(meshres[0]['meshes'].keys())))
    LOGGER.debug("elts in meshes: %d", len(meshres[0]['meshes']))
    # dimensions/number of bins of space coordinates are given by last bin
    ns0bins, ns1bins, ns2bins = _get_number_of_space_bins(meshres[0]['meshes'][0]['mesh_vals'])
    ntbins = (meshres[-1]['time_step'][0]+1
              if "time_step" in meshres[0]
              else 1)
    nebins = get_energy_bins(meshres[0]['meshes'])
    # get_energy_bins is much more efficient than combination of sum([])
    # and [].count('bla'), by a factor > 5
    LOGGER.info("ns0bins = %d, ns1bins = %d, ns2bins = %d, ntbins = %d, "
                "nebins = %d", ns0bins, ns1bins, ns2bins, ntbins, nebins)
    # up to now no mesh splitted in mu or phi angle seen, update easy now
    index = (ns0bins, ns1bins, ns2bins, nebins, ntbins, 1, 1)
    vals = np.empty(index, dtype=dtmesh)
    # mesh integrated on energy (normally the last mesh)
    intmeshindex = (ns0bins, ns1bins, ns2bins, 1, ntbins, 1, 1)
    intmeshvals = (np.empty(intmeshindex, dtype=dtmesh)
                   if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]
                   else None)
    # integrated result (space and energy)
    intresindex = (1, 1, 1, 1, ntbins, 1, 1)
    dtintres = np.dtype([('score', FTYPE), ('sigma', FTYPE)])
    usedbatchs, intresvals = ((meshres[0]['integrated_res']['used_batch'],
                               np.empty(intresindex, dtype=dtintres))
                              if 'integrated_res' in meshres[0]
                              else (0, None))
    itime = 0
    for ires in meshres:
        LOGGER.debug("keys: %s, number of elements: %d",
                     list(ires.keys()), len(ires))
        if 'time_step' in ires:
            itime = ires['time_step'][0]
            tbins.append(ires['time_step'][1])
        for inde, emesh in enumerate(ires['meshes']):
            if 'mesh_energyrange' in emesh:
                if itime == 0:
                    ebins.append(emesh['mesh_energyrange'][1])
                    if inde == nebins-1:
                        ebins.append(emesh['mesh_energyrange'][2])
                _fill_mesh(vals, emesh['mesh_vals'], inde, itime)
            if 'mesh_energyintegrated' in emesh:
                LOGGER.debug("Will fill mesh integrated in energy")
                _fill_mesh(intmeshvals, emesh['mesh_vals'], 0, itime)
        if 'integrated_res' in ires:
            iintres = ires['integrated_res']
            index = (0, 0, 0, 0, itime, 0, 0)
            intresvals[index] = np.array((iintres['score'], iintres['sigma']),
                                         dtype=intresvals.dtype)
    if 'time_step' in meshres[0]:
        if len(tbins) > 1 and tbins[0] > tbins[1]:
            tbins.insert(0, meshres[0]['time_step'][2])
        else:
            tbins.append(meshres[-1]['time_step'][2])
    _flip_bins([vals, intmeshvals, intresvals], ebins, tbins, None, None)
    convmesh = {'eunit': meshres[0]['meshes'][0]['mesh_energyrange'][0],
                'ebins': np.array(ebins),
                'mesh': vals}
    if 'time_step' in meshres[0]:
        convmesh['tbins'] = np.array(tbins)
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        convmesh['energy_integrated_mesh'] = intmeshvals
    if 'integrated_res' in meshres[0]:
        convmesh['integrated_res'] = intresvals
        convmesh['used_batch'] = usedbatchs
    return convmesh


def convert_integrated_mesh(mesh):
    '''Convert energy integrated mesh in numpy structured array.
    :param mesh: values as a list
    :returns: numpy structured array of dimension 7
              v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
              s0, s1, s2 = space coordinates (x, y, z), (r, phi, theta), etc.
              E = energy -> fixed at 0 (one bin)
              t = time
              mu, phi = direction angles (mu = cos(theta))
    '''
    dtmesh = np.dtype([('tally', FTYPE), ('sigma', FTYPE)])
    ns0bins, ns1bins, ns2bins = _get_number_of_space_bins(mesh)
    # up to now to mesh splitted in time, mu or phi angle seen
    index = (ns0bins, ns1bins, ns2bins, 1, 1, 1, 1)
    vals = np.empty(index, dtype=dtmesh)
    _fill_mesh(vals, mesh)
    return vals


def convert_integrated_result(result):
    '''Convert the energy integrated result in numpy structured array
    :param result: resultat
    :type result: list
    :returns: numpy structured array with (score, sigma)
    '''
    LOGGER.debug("[38;5;37m%s[0m", str(result))
    dtir = np.dtype([('score', FTYPE), ('sigma', FTYPE)])
    return np.array(tuple(result), dtype=dtir)


def convert_keff_with_matrix(res):
    '''Convert Keff results in numpy matrices.
    :param res: keff results
    :type res: dictionary
    :returns: dictionary containing
                - 'used_batch': number of batchs used to calculate keff values
                - 'estimators': tuple of estimators names
                                (KSTEP, KCOLL, KTRACK)
                - 'full_comb_estimation': numpy structured array (keff, sigma)
                  of the combined value of all estimators
                - 'keff_matrix': numpy (3,3) array containing keff results per
                  estimator in diagonal and combined values (2 estimators) out
                  of diagonal
                - 'correlation_matrix': numpy (3,3) array, symmetric matrix
                   with 1 on diagonal
                - 'sigma_matrix': numpy (3,3) array,
                  containing sigma values in %, values per estimator on
                  diagonal and for combined sigma out of diagonal
    Values in matrices are set to -100.0 if not converged (string
    "Not converged" appearing in the listings). Full combined results keeps the
    string.
    Matrices are ordered following estimators order, so normally
            KSTEP KCOLL KTRACK
    KSTEP
    KCOLL
    KTRACK
    It is possible to convert the numpy array in numpy matrix if matrix methods
    are needed but array is easier to initialized and more general.
    '''
    # not converged cases a tester...
    LOGGER.info("[38;5;56mClefs: %s[0m", str(list(res.keys())))
    if 'not_converged' in res:
        return {'used_batch': res['used_batch'],
                'not_converged': res['not_converged']}

    dtkeff = np.dtype([('keff', FTYPE), ('sigma', FTYPE)])
    fullcombres = (np.array(tuple(res['full_comb_estimation']), dtype=dtkeff)
                   if len(res['full_comb_estimation']) > 1
                   else res['full_comb_estimation'][0])
    keffnames = list(zip(*res['res_per_estimator']))[0]
    nbkeff = len(res['res_per_estimator'])
    keffmat = np.empty([nbkeff, nbkeff])
    corrmat = np.identity(nbkeff)
    sigmat = np.empty([nbkeff, nbkeff])
    for ikeff, keffname in enumerate(keffnames):
        keffmat[ikeff, ikeff] = res['res_per_estimator'][ikeff][1]
        sigmat[ikeff, ikeff] = res['res_per_estimator'][ikeff][2]
        for jcorr in range(len(res['correlation_mat'])):
            lkeff = res['correlation_mat'][jcorr]
            # list needed as type = pyparsing result
            if keffname in lkeff[0]:
                iokeff = keffnames.index(
                    [okeff for okeff in lkeff[0] if okeff != keffname][0])
                keffmat[ikeff, iokeff] = (lkeff[2]
                                          if not isinstance(lkeff[2], str)
                                          else -100.)
                corrmat[ikeff, iokeff] = (lkeff[1]
                                          if not isinstance(lkeff[1], str)
                                          else -100.)
                sigmat[ikeff, iokeff] = (lkeff[3]
                                         if not isinstance(lkeff[3], str)
                                         else -100.)
            else:
                continue
    return {'used_batch': res['used_batch'],
            'estimators': keffnames,
            'full_comb_estimation': fullcombres,
            'keff_matrix': keffmat,
            'correlation_matrix': corrmat,
            'sigma_matrix': sigmat}


def convert_keff(res):
    '''Convert Keff results in dictionary containing numpy objects.
    :param res: keff results (as pyparsing result ? or dictionary)
    :returns: dictionary containing
                - 'used_batch': number of batchs used to calculate keff values
                - 'estimators': tuple of estimators names
                                (KSTEP, KCOLL, KTRACK)
                - 'res_per_estimator': dictionary with estimator as key and
                  numpy structured array as value with dtype (keff, sigma)
                - 'full_comb_estimation': numpy structured array (keff, sigma)
                  of the combined value of all estimators
                - 'correlation_matrix': dictionary with tuple of estimators as
                  key (couple) and numpy structured array as value with dtype
                  (correlations, combined values, combined sigma%).
                  Theses values correspond to all values out of diagonal in
                  matrix representation.
    Values in matrices are set to -100. if not converged
    (string "Not converged" appearing in the listings).
    Full combined results keeps the string.
    '''
    LOGGER.debug("[38;5;56mClefs:%s[0m", str(list(res.keys())))
    usedbatchs = res['used_batch']
    if 'not_converged' in res:
        return {'used_batch': res['used_batch'],
                'not_converged': res['not_converged']}
    keffnames = list(zip(*res['res_per_estimator']))[0]
    keffres = {}
    dtkeff = np.dtype([('keff', FTYPE), ('sigma', FTYPE)])
    for keff in res['res_per_estimator']:
        keffres[keff[0]] = np.array(tuple(keff[1:]), dtype=dtkeff)
    fullcombres = (np.array(tuple(res['full_comb_estimation']), dtype=dtkeff)
                   if len(res['full_comb_estimation']) == 2
                   else res['full_comb_estimation'])
    corrres = {}
    dtcorr = np.dtype([('correlations', FTYPE),
                       ('combined values', FTYPE),
                       ('combined sigma%', FTYPE)])
    for elt in res['correlation_mat']:
        corrval = (elt[1:]
                   if all(isinstance(ielt, FTYPE) for ielt in elt[1:])
                   else [-100. if isinstance(x, str) else x for x in elt[1:]])
        corrres[tuple(elt[0])] = np.array(tuple(corrval), dtype=dtcorr)
    return {'used_batch': usedbatchs,
            'estimators': keffnames,
            'res_per_estimator': keffres,
            'full_comb_estimation': fullcombres,
            'correlation_matrix': corrres}


def convert_green_bands(gbs):
    '''Convert Green bands results in numpy structured array,
    close to time or angle spectra ones.
    :param gbs: Green bands as a list of dictionaries
    :returns: dictionary similar to spectum one
              CAUTION indexes are changed compared to default spectrum results
              - 'ebins': energy bins (size = number of elements +1)
              - 'vals': 6-dimensions numpy structured array
                v[step, sourceNum, u, v, w, E] = (score, sigma, score/lethargy)
                u, v, w: coordinates of the source (0, 0, 0 if not given)
              - 'sebins': energy bins for the source
              - 'disc_batch': number of discarded batchs
    '''
    sebins = []
    nsteps = len(gbs)
    lastsource = gbs[-1]['gb_step_res'][-1]['gb_source']
    hassourcetab = True if len(lastsource) > 1 else False
    nsources = lastsource[0]+1
    nudim = lastsource[1][0]+1 if hassourcetab else 1
    nvdim = lastsource[1][1]+1 if hassourcetab else 1
    nwdim = lastsource[1][2]+1 if hassourcetab else 1
    spectrum = gbs[0]['gb_step_res'][0]['spectrum_res'][0]
    nebins = len(spectrum['spectrum_vals'])
    ebins = []
    discbatchs = spectrum['disc_batch']
    index = (nsteps, nsources, nudim, nvdim, nwdim, nebins)
    dtgb = np.dtype([('score', FTYPE),
                     ('sigma', FTYPE),
                     ('score/lethargy', FTYPE)])
    vals = np.empty(index, dtype=dtgb)
    for ist, gbstep in enumerate(gbs):
        istep = gbstep['gb_step_desc'][0]
        sebins.append(gbstep['gb_step_desc'][2])
        for ires, gbres in enumerate(gbstep['gb_step_res']):
            isource = gbres['gb_source']
            if len(gbres['spectrum_res']) > 1:
                LOGGER.warning("[31mMore than one spectrum_res "
                               "while only one foreseen for the moment[0m")
            ispectrum = gbres['spectrum_res'][0]['spectrum_vals']
            for iebin, ivals in enumerate(ispectrum):
                if ist == 0 and ires == 0:
                    ebins.append(ivals[0])
                locind = ((istep, isource[0],
                           isource[1][0], isource[1][1], isource[1][2],
                           iebin) if hassourcetab
                          else (istep, isource[0], 0, 0, 0, iebin))
                vals[locind] = np.array(tuple(ivals[2:]), dtype=dtgb)
    sebins.append(gbs[-1]['gb_step_desc'][1])
    ebins.append(spectrum['spectrum_vals'][-1][1])
    return {'ebins': np.array(ebins),
            'vals': vals,
            'sebins': np.array(sebins),
            'disc_batch': discbatchs}


def convert_ifp(ifp):
    '''Convert IFP (statistics) result in numpy array.
    :param ifp: list of cycle and associated results
    :returns: numpy structured array of dimension 1
              v[i] = (length, score, sigma)
              with i = index of the cycle length
              length = cycle length
    '''
    dtifp = np.dtype([('length', ITYPE), ('score', FTYPE), ('sigma', FTYPE)])
    vals = np.empty((len(ifp)), dtype=dtifp)
    for ind, ifpcycle in enumerate(ifp):
        vals[ind] = np.array(tuple(ifpcycle), dtype=dtifp)
    return vals


def convert_kij_sources(res):
    '''Convert Kij sources result in python dictionary.
    Kij sources values are converted in a numpy array
    :param res: kij sources as a dictionary
    :type res: dict
    :returns: same dictionary with numpy array for kij sources values
    '''
    kijs = {}
    for key in res:
        if key == 'kij_sources_vals':
            kijs[key] = np.array(res[key])
        else:
            kijs[key] = res[key]
    return kijs


def convert_kij_result(res):
    '''Convert Kij result in numpy objects and return a dictionary.
    :param res: kij result as a dictionary (keys: used_batch, kij_eigenval,
                kij_eigenvec, kij_matrix)
    :type res: dict
    :returns: dictionary containing the same keys but with different types
                 - 'used_batch': number of used batchs (int)
                 - 'kijmkeff_res': kij-keff result (float)
                 - 'kijdomratio': dominant ratio (float)
                 - 'kij_eigenval': eigen values,
                                   numpy array of N complex numbers
                 - 'kij_eigenvec': eigen vectors,
                                   numpy array (N vectors of N elements)
                 - 'kij_matrix': kij matrix,
                                 numpy matrix of N*N
    '''
    # eigen values (re, im) -> store as array of complex
    reegval = np.array(list(zip(*res['kij_eigenval']))[0])
    imegval = np.array(list(zip(*res['kij_eigenval']))[1])
    egvals = reegval + 1j*imegval
    # eigen vectors
    egvecs = np.array(res['kij_eigenvec'])
    # kij matrix
    kijmat = np.matrix(res['kij_matrix'])
    return {'used_batch': res['used_batch'],
            'kijmkeff_res': res['kijmkeff_res'][0],
            'kijdomratio': res['kijmkeff_res'][1],
            'kij_eigenval': egvals,
            'kij_eigenvec': egvecs,
            'kij_matrix': kijmat}


def convert_kij_keff(res):
    '''Convert matrices in numpy array or matrix when estimating Keff from Kij
    :param res: dictionary with key 'estimator' = 'KIJ'
    :returns: dictionary containing
                - 'estimator': name of the estimator -> 'KIJ' (string)
                - 'batchs_kept': number of batchs used t calculate Keff
                                 from KIJ (int)
                - 'kij-keff': kij-keff result (float)
                - 'nbins': number of volumes/mesh elements considered (int)
                - 'spacebins': list of volumes/mesh elements considered
                               (numpy array of
                                  - int for volumes
                                  - (s0, s1, s2) for mesh elements, being ints)
                - 'eigenvector': eigenvector corresponding to best estimation
                                 (numpy array of N elts with N = nbins)
                - 'keff_KIJ_matrix': KIJ matrix for keff best estimation
                                     (numpy matrix N*N)
                - 'keff_StdDev_matrix': standard deviation matrix for keff best
                                        estimation
                                        (numpy matrix N*N)
                - 'keff_sensibility_matrix': sensibility matrix for keff best
                                             estimation
                                             (numpy matrix N*N)
    '''
    LOGGER.info("Clefs: %s", str(list(res.keys())))
    egvec = np.array(list(zip(*res['eigenvector']))[1])
    nbins = res['nb_fissile_vols'] if 'nb_fissile_vols' in res else len(egvec)
    if nbins != len(egvec):
        LOGGER.warning("[31mIssue in number of fissile volumes "
                       "and size of eigenvector[0m")
    # For the moment 2 possibilities seen for space splitting: mesh or volumes
    # in mesh case: meshes are listed in 1st row of matrix (3 elements)
    # in volume case: list of fissile volumes given, equivalent to 1st row of
    # matrix -> only way kept as closer to mesh case
    if isinstance(res['keff_KIJ_matrix'][0][0], list):
        dtspace = np.dtype([('s0', ITYPE), ('s1', ITYPE), ('s2', ITYPE)])
        spacebins = np.empty(len(res['keff_KIJ_matrix'][0]), dtype=dtspace)
        for ielt, spelt in enumerate(res['keff_KIJ_matrix'][0]):
            spacebins[ielt] = np.array(spelt)
    else:
        spacebins = np.array(res['keff_KIJ_matrix'][0])
    if spacebins.size != len(res['keff_KIJ_matrix'][1:]):
        LOGGER.warning("[31mStrange: not the dimension in space mesh and "
                       "matrix, matrix expected to be squared[0m")
    # Fill the 3 matrices
    kijmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_KIJ_matrix'][1:]):
        kijmat[irow] = np.array(tuple(row[1:]))
    stddevmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_StdDev_matrix'][1:]):
        stddevmat[irow] = np.array(tuple(row[1:]))
    sensibmat = np.empty([spacebins.size, spacebins.size])
    for irow, row in enumerate(res['keff_sensibility_matrix'][1:]):
        sensibmat[irow] = np.array(tuple(row[1:]))
    return {'estimator': res['estimator'],
            'batchs_kept': res['batchs_kept'],
            'kij-keff': res['kij-keff'],
            'nbins': nbins,
            'spacebins': spacebins,
            'eigenvector': egvec,
            'keff_KIJ_matrix': np.matrix(kijmat),
            'keff_StdDev_matrix': np.matrix(stddevmat),
            'keff_sensibility_matrix': np.matrix(sensibmat)}
