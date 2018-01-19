'''This module provides generic functions to convert parsing outputs in numpy
objects.

Inputs (outputs from parsers) should be python lists or dictionary,
dictionary keys should be the same in all parsers...

..note:: not a standalone code, needs inputs
         To be tested in a more general context.
'''

import sys
import logging
from abc import ABC, abstractmethod
import numpy as np


if "mem" not in sys.argv:
    def profile(func):
        '''No memory profiling if "mem" not in arguments of the command line.
        '''
        return func


LOGGER = logging.getLogger('valjean')
ITYPE = np.int32
FTYPE = np.float32  # pylint: disable=E1101


class DictBuilder(ABC):
    '''Class to build the dictionary for spectrum and mesh results as
    7-dimensions structured arrays.
    7-dimensions are: space (3), energy, time, mu and phi (direction angles)
    '''
    VAR_FLAG = {'t': 'time_step',
                'mu': 'mu_angle_zone',
                'phi': 'phi_angle_zone'}
    VARS = ['s0', 's1', 's2', 'e', 't', 'mu', 'phi']

    def __init__(self, colnames, lnbins):
        try:
            assert len(lnbins) == 7
        except TypeError:
            LOGGER.error("lnbins should the list of number of bins")
            raise TypeError
        except AssertionError:
            LOGGER.error("Number of bins should be 7 (3 space dimensions, "
                         "1 energy, 1 time, 2 direction angles)")
            raise AssertionError
        self.bins = {'e': [], 't': [], 'mu': [], 'phi': []}
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays = {'default': np.empty((lnbins), dtype=dtype)}
        LOGGER.debug("bins: %s", str(self.bins))

    def add_array(self, name, colnames, nbins):
        '''Add a new array to dictionary arrays with key name.
        :param name: name of the new array (integrated_res, etc.)
        :type name: string
        :param colnames: list of the columns names (score, sigma, tally, etc.)
        :type colnames: list/tuple of string
        :param nbins: number of bins in each dimension
        :type nbins: list of int
        '''
        dtype = np.dtype({'names': colnames,
                          'formats': [FTYPE]*len(colnames)})
        self.arrays[name] = np.empty((nbins), dtype=dtype)

    @abstractmethod
    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum or mesh.
        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        '''
        pass

    def _add_last_bin_for_dim(self, data, dim, lastbin):
        '''Add last bin for the dimension dim. Depending on order of the bins
        the last one will be inserted as first bin or added as last bin.
        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        :param dim: dimension where the bin will be added (t, mu, phi)
        :type dim: string
        :param ilastbin: index of the bin in mesh or spectrum containing the
                         missing edge of the bins
        :type ilastbin: int
        '''
        LOGGER.debug("Adding last bin for dim %s, flag = %s",
                     dim, DictBuilder.VAR_FLAG[dim])
        if len(self.bins[dim]) > 1 and self.bins[dim][0] > self.bins[dim][1]:
            self.bins[dim].insert(0, data[0][DictBuilder.VAR_FLAG[dim]][2])
        else:
            self.bins[dim].append(data[lastbin][DictBuilder.VAR_FLAG[dim]][2])

    def add_last_bins(self, data):
        '''Add last bins in energy, time, mu and phi direction angles.
        Based on keywords presence in data.
        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        '''
        self._add_last_energy_bin(data)
        nphibins = len(self.bins['phi']) if self.bins['phi'] else 1
        nmubins = len(self.bins['mu']) if self.bins['mu'] else 1
        # other possibility: if DictBuilder.VAR_FLAG['t'] in data[0]
        if 'time_step' in data[0]:
            self._add_last_bin_for_dim(data, 't', -int(nphibins)*int(nmubins))
        if 'mu_angle_zone' in data[0]:
            self._add_last_bin_for_dim(data, 'mu', -int(nphibins))
        if 'phi_angle_zone' in data[0]:
            self._add_last_bin_for_dim(data, 'phi', -1)

    def _flip_bins_for_dim(self, dim, axis):
        '''Flip bins for dimension dim.
        :param dim: dimension ('e', 't', 'mu', 'phi')
        :type dim: string
        :param axis: axis of the dimension
                     ('e' -> 3, 't' -> 4, 'mu' -> 5, 'phi' -> 6)
        :type axis: int
        '''
        LOGGER.debug("Bins %s avant flip: %s", dim, str(self.bins[dim]))
        self.bins[dim] = self.bins[dim][::-1]
        for key, array in self.arrays.items():
            self.arrays[key] = np.flip(array, axis=axis)
        LOGGER.debug("et apres: %s", str(self.bins[dim]))

    def flip_bins(self):
        '''Flip bins if given in decreasing order in the output listing.
        Depending on the required grid (GRID or DECOUPAGE) energies, times, mu
        and phi can be given from upper edge to lower edge. This is not
        convenient for post-traitements, especially plots. They have to be
        flipped at a moment, here or later, easiest is here, and all results
        will look the same :-).
        '''
        LOGGER.debug("In DictBuilder.flip_bins")
        if self.bins['e'] and self.bins['e'][0] > self.bins['e'][1]:
            self._flip_bins_for_dim('e', 3)
        if self.bins['t'] and self.bins['t'][0] > self.bins['t'][1]:
            self._flip_bins_for_dim('t', 4)
        if self.bins['mu'] and self.bins['mu'][0] > self.bins['mu'][1]:
            self._flip_bins_for_dim('mu', 5)
        if self.bins['phi'] and self.bins['phi'][0] > self.bins['phi'][1]:
            self._flip_bins_for_dim('phi', 6)

    @abstractmethod
    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum or mesh data.
        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        '''
        pass


class MeshDictBuilder(DictBuilder):
    '''Class specific to mesh dictionary -> mainly filling of bins and arrays.
    '''
    itime, imu, iphi = 0, 0, 0

    def _fill_mesh_array(self, meshvals, name, ebin):
        '''Fill mesh array.
        :param meshvals: mesh data for a given energy bin
        :type meshvals: list of mesh results [[[s0, s1, s2], tally, sigma],...]
        :param name: name of the array to be filled ('default',
                     'eintegrated_mesh') for the moment
        :type name: string
        :param ebin: energy bin to fill in the array
        :type ebin: int
        '''
        for smesh in meshvals:
            index = (smesh[0][0], smesh[0][1], smesh[0][2],
                     ebin, self.itime, self.imu, self.iphi)
            self.arrays[name][index] = np.array(tuple(smesh[1:]),
                                                dtype=self.arrays[name].dtype)

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for mesh data.
        Current arrays possibly filled are:
        - default (mandatory)
        - eintegrated_mesh (facultative, integrated over energy, still splitted
                            in space)
        - integrated_res (over energy and space, splitted in time)
        :param data: mesh
        :type data: list of meshes results
        '''
        for ires in data:
            LOGGER.debug("MeshDictBuilder.fill_arrays_bins, "
                         "keys: %s, number of elements: %d",
                         list(ires.keys()), len(ires))
            if 'time_step' in ires:
                self.itime = ires['time_step'][0]
                self.bins['t'].append(ires['time_step'][1])
            for inde, emesh in enumerate(ires['meshes']):
                if 'mesh_energyrange' in emesh:
                    if self.itime == 0:
                        self.bins['e'].append(emesh['mesh_energyrange'][1])
                    self._fill_mesh_array(emesh['mesh_vals'], 'default', inde)
                if 'mesh_energyintegrated' in emesh:
                    LOGGER.debug("Will fill mesh integrated in energy")
                    self._fill_mesh_array(emesh['mesh_vals'],
                                          'eintegrated_mesh', 0)
            if 'integrated_res' in ires:
                iintres = ires['integrated_res']
                index = (0, 0, 0, 0, self.itime, 0, 0)
                self.arrays['integrated_res'][index] = np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype)

    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from mesh data.
        :param data: mesh data
        :type data: list of meshes results
        '''
        lastmesh = data[-1]['meshes']
        lastebin = self.arrays['default'].shape[3]-1
        self.bins['e'].append(lastmesh[lastebin]['mesh_energyrange'][2])


class SpectrumDictBuilder(DictBuilder):
    '''Class specific to spectrum dictionary
    -> mainly filling of bins and arrays.
    '''
    itime, imu, iphi = 0, 0, 0

    def fill_arrays_and_bins(self, data):
        '''Fill arrays and bins for spectrum data.
        Current arrays possibly filled are:
        - default (mandatory)
        - integrated_res (over energy, splitted in time for the moment)
        :param data: mesh or spectrum
        :type data: list of meshes or spectrum results
        '''
        LOGGER.debug("In SpectrumDictBuilder.fill_arrays_and_bins")
        for ispec in data:
            # Fill bins -> caution to not replicate them
            if 'time_step' in ispec:
                self.itime = ispec['time_step'][0]
                self.bins['t'].append(ispec['time_step'][1])
            if 'mu_angle_zone' in ispec:
                self.imu = ispec['mu_angle_zone'][0]
                if self.itime == 0:
                    self.bins['mu'].append(ispec['mu_angle_zone'][1])
            if 'phi_angle_zone' in ispec:
                self.iphi = ispec['phi_angle_zone'][0]
                if self.itime == 0 and self.imu == 0:
                    self.bins['phi'].append(ispec['phi_angle_zone'][1])

            # Fill spectrum values
            for ienergy, ivals in enumerate(ispec['spectrum_vals']):
                if self.itime == 0 and self.imu == 0 and self.iphi == 0:
                    self.bins['e'].append(ivals[0])
                index = (0, 0, 0, ienergy, self.itime, self.imu, self.iphi)
                self.arrays['default'][index] = np.array(
                    tuple(ivals[2:]),
                    dtype=self.arrays['default'].dtype)

            # Fill integrated result if exist
            if 'integrated_res' in ispec:
                iintres = ispec['integrated_res']
                index = (0, 0, 0, 0, self.itime, self.imu, self.iphi)
                self.arrays['integrated_res'][index] = (np.array(
                    (iintres['score'], iintres['sigma']),
                    dtype=self.arrays['integrated_res'].dtype))

    def _add_last_energy_bin(self, data):
        '''Add last bin in energy from spectrum.
        :param data: spectrum data
        :type data: list of spectrum results
        '''
        self.bins['e'].append(data[-1]['spectrum_vals'][-1][1])


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


def convert_spectrum(spectrum, colnames=('score', 'sigma', 'score/lethargy')):
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
    :param colnames: list of the names of the columns.
                    Default = ['score', 'sigma', 'score/lethargy']
    :type colnames: list of strings
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
    vals = SpectrumDictBuilder(colnames,
                               [1, 1, 1, nebins, ntbins, nmubins, nphibins])
    if 'integrated_res' in spectrum[0]:
        vals.add_array('integrated_res', ['score', 'sigma'],
                       [1, 1, 1, 1, ntbins, nmubins, nphibins])
    # Fill spectrum, bins and integrated result if exists
    vals.fill_arrays_and_bins(spectrum)
    vals.add_last_bins(spectrum)
    # Flip bins
    vals.flip_bins()
    # Build dictionary to be returned
    convspec = {'disc_batch': spectrum[0]['disc_batch'],
                'ebins': np.array(vals.bins['e']),
                'spectrum': vals.arrays['default']}
    if 'time_step' in spectrum[0]:
        convspec['tbins'] = np.array(vals.bins['t'])
    if 'mu_angle_zone' in spectrum[0]:
        convspec['mubins'] = np.array(vals.bins['mu'])
    if 'phi_angle_zone' in spectrum[0]:
        convspec['phibins'] = np.array(vals.bins['phi'])
    if 'integrated_res' in spectrum[0]:
        convspec['integrated_res'] = vals.arrays['integrated_res']
        convspec['used_batch'] = spectrum[0]['integrated_res']['used_batch']
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
    maxbins1 = (lastspacebin[1]*ns2bins+lastspacebin[2]+2
                if lastspacebin[0] != 0
                else lastspacebin[2]+2)
    if LOGGER.isEnabledFor(logging.DEBUG):
        if len(meshvals) > maxbins1:
            if meshvals[-int(maxbins1)][0][1] > lastspacebin[1]:
                LOGGER.debug("will use meshvals[-int(maxbins1)] = %s instead "
                             "of lastspacebin = %s",
                             str(meshvals[-int(maxbins1)]), str(lastspacebin))
            else:
                LOGGER.debug("will use lastspacebin = %s instead of "
                             "meshvals[-int(maxbins1)] = %s",
                             lastspacebin, meshvals[-int(maxbins1)])
        else:
            LOGGER.debug("will use lastspacebin = %s as "
                         "len(meshvals) > maxbins1", lastspacebin)
    ns1bins = (meshvals[-int(maxbins1)][0][1]+1
               if (len(meshvals) > maxbins1
                   and meshvals[-int(maxbins1)][0][1] > lastspacebin[1])
               else lastspacebin[1]+1)
    return ns0bins, ns1bins, ns2bins


def get_energy_bins(meshes):
    '''Get the number of energy bins for mesh.
    :param meshes: mesh, list of dictionaries, at least one should have the key
                   'mesh_energyrange'
    :type meshes: list of dictionaries
    '''
    nbebins = 0
    for mesh in meshes:
        if 'mesh_energyrange' in mesh:
            nbebins += 1
    return nbebins


def convert_mesh(meshres):
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
                - 'eintegrated_mesh': 7 dimensions numpy structured array
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  corresponding to mesh integreted on energy (facultative)
                - 'integrated_res': 7 dimensions numpy structured array
                  v[s0,s1,s2,E,t,mu,phi] = (tally, sigma)
                  corresponding to mesh integrated over energy and space
                  facultative, available when time grid is required (so
                  corresponds to integreated results splitted in time)
                - used_batch: number of used batchs (only if integrated result)
    '''
    LOGGER.debug("In convert_mesh_class")
    LOGGER.debug("Number of mesh results: %d", len(meshres))
    LOGGER.debug("keys of meshes: %s", str(list(meshres[0]['meshes'].keys())))
    LOGGER.debug("elts in meshes: %d", len(meshres[0]['meshes']))
    # dimensions/number of bins of space coordinates are given by last bin
    ns0bins, ns1bins, ns2bins = _get_number_of_space_bins(
        meshres[0]['meshes'][0]['mesh_vals'])
    # ntbins supposes for the moment no mu or phi bins
    ntbins = (meshres[-1]['time_step'][0]+1
              if "time_step" in meshres[0]
              else 1)
    nebins = get_energy_bins(meshres[0]['meshes'])
    LOGGER.debug("ns0bins = %d, ns1bins = %d, ns2bins = %d, ntbins = %d, "
                 "nebins = %d", ns0bins, ns1bins, ns2bins, ntbins, nebins)
    # up to now no mesh splitted in mu or phi angle seen, update easy now
    vals = MeshDictBuilder(['tally', 'sigma'],
                           [ns0bins, ns1bins, ns2bins, nebins, ntbins, 1, 1])
    # mesh integrated on energy (normally the last mesh)
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        vals.add_array('eintegrated_mesh', ['tally', 'sigma'],
                       [ns0bins, ns1bins, ns2bins, 1, ntbins, 1, 1])
    # integrated result (space and energy)
    if 'integrated_res' in meshres[0]:
        vals.add_array('integrated_res', ['score', 'sigma'],
                       [1, 1, 1, 1, ntbins, 1, 1])
    # fill arrays, bins, put them in inceasing order
    vals.fill_arrays_and_bins(meshres)
    vals.add_last_bins(meshres)
    vals.flip_bins()
    # build dictionary to be returned
    convmesh = {'eunit': meshres[0]['meshes'][0]['mesh_energyrange'][0],
                'ebins': np.array(vals.bins['e']),
                'mesh': vals.arrays['default']}
    if 'time_step' in meshres[0]:
        convmesh['tbins'] = np.array(vals.bins['t'])
    if 'mesh_energyintegrated' in meshres[0]['meshes'][-1]:
        convmesh['eintegrated_mesh'] = vals.arrays['eintegrated_mesh']
    if 'integrated_res' in meshres[0]:
        convmesh['integrated_res'] = vals.arrays['integrated_res']
        convmesh['used_batch'] = meshres[0]['integrated_res']['used_batch']
    return convmesh


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
    LOGGER.debug("In common.convert_keff_with_matrix")
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


# 17 locals in convert_green_bands instead 15, but helps reading of the method
def convert_green_bands(gbs):  # pylint: disable=R0914
    '''Convert Green bands results in numpy structured array,
    close to time or angle spectra ones.
    :param gbs: Green bands as a list of dictionaries
    :returns: dictionary similar to spectum one
              CAUTION indexes are changed compared to default spectrum results
              - 'ebins': energy bins (size = number of elements +1)
              - 'vals': 6-dimensions numpy structured array
                v[step, sourceNum, u, v, w, E] = (score, sigma, score/lethargy)
                step: bin of energy of source
                u, v, w: coordinates of the source (0, 0, 0 if not given)
              - 'sebins': energy bins for the source
              - 'disc_batch': number of discarded batchs
    '''
    lastsource = gbs[-1]['gb_step_res'][-1]['gb_source']
    hassourcetab = True if len(lastsource) > 1 else False
    spectrum = gbs[0]['gb_step_res'][0]['spectrum_res'][0]
    bins = {'e': [], 'se': []}
    index = (len(gbs),  # number of steps (= number of bins of source energy)
             lastsource[0]+1,  # number of sources
             lastsource[1][0]+1 if hassourcetab else 1,  # number of u bins
             lastsource[1][1]+1 if hassourcetab else 1,  # number of v bins
             lastsource[1][2]+1 if hassourcetab else 1,  # number of w bins
             len(spectrum['spectrum_vals']))  # number of energy bins
    vals = np.empty(index,
                    dtype=np.dtype([('score', FTYPE),
                                    ('sigma', FTYPE),
                                    ('score/lethargy', FTYPE)]))
    # Loop over results to fill them in numpy array
    for ist, gbstep in enumerate(gbs):
        istep = gbstep['gb_step_desc'][0]
        bins['se'].append(gbstep['gb_step_desc'][2])
        for ires, gbres in enumerate(gbstep['gb_step_res']):
            isource = gbres['gb_source']
            if len(gbres['spectrum_res']) > 1:
                LOGGER.warning("[31mMore than one spectrum_res "
                               "while only one foreseen for the moment[0m")
            ispectrum = gbres['spectrum_res'][0]['spectrum_vals']
            for iebin, ivals in enumerate(ispectrum):
                if ist == 0 and ires == 0:
                    bins['e'].append(ivals[0])
                locind = ((istep, isource[0],
                           isource[1][0], isource[1][1], isource[1][2],
                           iebin) if hassourcetab
                          else (istep, isource[0], 0, 0, 0, iebin))
                vals[locind] = np.array(tuple(ivals[2:]), dtype=vals.dtype)
    # Add last bins
    bins['se'].append(gbs[-1]['gb_step_desc'][1])
    bins['e'].append(spectrum['spectrum_vals'][-1][1])
    # No flip bins for the moment, question about order of steps (so energy
    # bins of sources)
    return {'ebins': np.array(bins['e']),
            'vals': vals,
            'sebins': np.array(bins['se']),
            'disc_batch': spectrum['disc_batch']}


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
    LOGGER.debug("Clefs: %s", str(list(res.keys())))
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
