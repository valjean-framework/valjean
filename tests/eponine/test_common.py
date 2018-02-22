'''Tests for the :mod:`common <valjean.eponine.common>` module.'''

import numpy as np
from hypothesis import given, note, settings, assume
from hypothesis.strategies import (integers, lists, composite, data, tuples,
                                   floats, nothing, booleans, just)
from hypothesis.extra.numpy import arrays

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
# pylint: disable=no-value-for-parameter
from valjean.eponine.common import (MeshDictBuilder, SpectrumDictBuilder,
                                    FTYPE)
import valjean.eponine.pyparsing_t4.grammar as pygram
from valjean import LOGGER


@composite
def shapes(draw, max_sides=(3, 3, 3, 5, 5, 1, 1)):
    '''Composite Hypothesis strategy to generate *numpy.ndarray* shapes
    taking into account maximum dimensions in space, energy, time, µ and φ
    coordinates.
    '''
    mytuple = draw(tuples(*map(lambda i: integers(1, i), max_sides)))
    return mytuple


@composite
def array_and_bins(draw, dtype,
                   max_dim=(3, 3, 3, 5, 5, 1, 1),
                   elements=tuples(floats(0, 1.), floats(0., 100.)),
                   reverse=booleans()):
    '''Composite Hypothesis strategy to generate shapes, then array and bins
    corresponding.

    :param numpy.dtype dtype: dtype of the future array
    :param tuple max_dim: maximum shape of the future array
    :param strategy elements: tuples of float with edges corresponding to dtype
    :param strategy reverse: boolean strategy to get order of bins
    :returns: numpy.ndarray and dictionary of bins with keys ``['e', 't',
              'mu', 'phi']``
    '''
    shape = draw(shapes(max_dim))
    array = draw(arrays(dtype=dtype, shape=shape, elements=elements,
                        fill=nothing()))
    the_bins = {'e':   draw(bins(elements=floats(0, 20), nbins=shape[3],
                                 reverse=reverse)),
                't':   draw(bins(elements=floats(0, 10), nbins=shape[4],
                                 reverse=reverse)),
                'mu':  draw(bins(elements=floats(-1., 1.), nbins=shape[5],
                                 reverse=reverse)),
                'phi': draw(bins(elements=floats(0, 2*np.pi), nbins=shape[6],
                                 reverse=reverse))}
    return array, the_bins


@composite
def bins(draw, elements=floats(0, 10), nbins=1, reverse=booleans()):
    '''Choose the (energy, time, µ or φ) bins and their order (reversed or not)
    thanks to hypothesis.

    Edges for the bins can be chosen to get more realistic cases.
    '''
    # we require that the bins are unique when converted to the TRIPOLI-4
    # output format; otherwise bins that are sufficiently close together will
    # fail to pass the roundtrip tests
    revers = draw(reverse)
    as_list = sorted(
        draw(lists(elements, min_size=nbins+1, max_size=nbins+1,
                   unique_by=lambda x: '{0:.6e}'.format(abs(x))))
        )
    if revers:
        arr = np.array(reversed(as_list))
    arr = np.array(as_list)
    note('nbins=' + str(nbins))
    note('as_list=' + str(as_list))
    note('revers=' + str(revers))
    note('bins=' + str(arr))
    return arr


def compare_bin_order(ibins, fbins, irdm, rev_rdm):
    '''Compare bins orders between flipped bins using
    :mod:`valjean.eponine.common` and bins array read in reversed order.
    Modify value of the reversed random index to match the correct element.
    '''
    if ibins[0] > ibins[1]:
        rev_rdm[irdm] = - rev_rdm[irdm] - 1
        assert np.array_equal(fbins, ibins[::-1])


@given(shape=shapes(max_sides=[3, 3, 3, 5, 5, 1, 1]), sampler=data())
def test_flip_mesh(shape, sampler):
    '''Test flipping mesh.

    Generate with hypothesis a mesh with maximum sides
    ``[s0, s1, s2, E, t, mu, phi] = [3, 3, 3, 5, 5, 1, 1]``
    as no mu or phi bins are available for the moment for meshes.

    Generate energy and time binnings. They can be increasing or decreasing
    depending on the value of the boolean chosen by hypothesis in order to
    test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    dtype = [('tally', np.float), ('sigma', np.float)]
    array = sampler.draw(arrays(dtype=np.dtype(dtype),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(5, 20)),
                                fill=nothing()))
    note('shape = ' + str(shape))
    note('content = ' + str(array))
    ebins = sampler.draw(bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(bins(elements=floats(0, 10), nbins=shape[4]))
    note(ebins.shape)
    note(tbins.shape)
    e_incr = 1 if len(ebins) > 1 and ebins[1] > ebins[0] else -1
    t_incr = 1 if len(tbins) > 1 and tbins[1] > tbins[0] else -1

    mesh = MeshDictBuilder(['tally', 'sigma'], shape)
    mesh.bins['e'] = ebins
    mesh.bins['t'] = tbins
    mesh.arrays['default'] = array
    mesh.flip_bins()

    assert np.all(np.diff(mesh.bins['e']) > 0.0)
    assert np.all(np.diff(mesh.bins['t']) > 0.0)

    for comp, _ in dtype:
        assert np.array_equal(array[comp],
                              mesh.arrays['default'][comp]
                              [:, :, :, ::e_incr, ::t_incr, :, :])


@given(shape=shapes(max_sides=[1, 1, 1, 5, 5, 3, 3]),
       sampler=data())
def test_flip_spectrum(shape, sampler):
    '''Test flipping spectrum.

    Generate with hypothesis a mesh with max dimensions
    ``[s0, s1, s2, E, t, mu, phi] = [1, 1, 1, 5, 5, 3, 3]``.

    Generate energy, time, mu and phi angle binnings. They can be increasing or
    decreasing depending on the value of the boolean chosen by hypothesis in
    order to test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    dtype = [('score', np.float),
             ('sigma', np.float),
             ('score/lethargy', np.float)]
    array = sampler.draw(
        arrays(dtype=np.dtype(dtype),
               shape=shape,
               elements=tuples(floats(0, 1), floats(5, 20), floats(0, 1)),
               fill=nothing()))
    ebins = sampler.draw(bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(bins(elements=floats(0, 10), nbins=shape[4]))
    mubins = sampler.draw(bins(elements=floats(-1., 1.), nbins=shape[5]))
    phibins = sampler.draw(bins(elements=floats(0, 2*np.pi),
                                nbins=shape[6]))
    e_incr = 1 if len(ebins) > 1 and ebins[1] > ebins[0] else -1
    t_incr = 1 if len(tbins) > 1 and tbins[1] > tbins[0] else -1
    mu_incr = 1 if len(mubins) > 1 and mubins[1] > mubins[0] else -1
    phi_incr = 1 if len(phibins) > 1 and phibins[1] > phibins[0] else -1

    spectrum = SpectrumDictBuilder(['score', 'sigma', 'score/lethargy'], shape)
    spectrum.bins = {'e': ebins, 't': tbins, 'mu': mubins, 'phi': phibins}
    spectrum.arrays['default'] = array
    spectrum.flip_bins()

    assert np.all(np.diff(spectrum.bins['e']) > 0.0)
    assert np.all(np.diff(spectrum.bins['t']) > 0.0)
    assert np.all(np.diff(spectrum.bins['mu']) > 0.0)
    assert np.all(np.diff(spectrum.bins['phi']) > 0.0)
    for comp, _ in dtype:
        assert np.array_equal(
            array[comp],
            spectrum.arrays['default'][comp]
            [:, :, :, ::e_incr, ::t_incr, ::mu_incr, ::phi_incr]
            )


def mesh_score_str():
    '''String to a mesh block in parsing, describing the score.'''
    msc_str = '''
         scoring mode : SCORE_TRACK
         scoring zone :          Results on a mesh:
         Cell             tally           sigma (percent)
    '''
    return msc_str


def build_mesh_t4_output(mesh, ebins, tbin):
    '''Build the Tripoli-4 output for meshes, looping on energy bins and
    printing all mesh results.

    :param numpy.ndarray mesh: mesh from Hypothesis
    :param list ebins: energy bins
    :param int tbin: time bin
    :returns: T4 output as a string
    '''
    t4out = []
    shape = mesh.shape
    for iebin in range(len(ebins)-1):
        t4out.append("Energy range (in MeV): {0:.6e} - {1:.6e}\n"
                     .format(ebins[iebin], ebins[iebin+1]))
        for is0 in range(shape[0]):
            for is1 in range(shape[1]):
                for is2 in range(shape[2]):
                    index = (is0, is1, is2, iebin, tbin, 0, 0)
                    t4out.append("\t({0},{1},{2})\t\t{3:.6e}\t{4:.6e}\n"
                                 .format(is0, is1, is2,
                                         mesh[index]['tally'],
                                         mesh[index]['sigma']))
        t4out.append("\n")
    return ''.join(t4out)


def make_mesh_t4_output(mesh, ebins, tbins):
    '''Build the Tripoli-4 output for meshes from time binning.
    If only one time bin, build the T4 mesh output string directly, else loop
    on tbins and fill the output.

    :param numpy.ndarray mesh: mesh from Hypothesis
    :param list ebins: energy bins
    :param int tbin: time bin
    :returns: T4 output as a string
    '''
    t4out = []
    t4out.append(mesh_score_str())
    t4out.append("\n")
    if len(tbins) < 3:
        t4out.append("\n")
        t4out.append(build_mesh_t4_output(mesh, ebins, 0))
    else:
        for itbin in range(len(tbins)-1):
            mintime = (tbins[itbin] if tbins[itbin] < tbins[itbin+1]
                       else tbins[itbin+1])
            maxtime = (tbins[itbin+1] if tbins[itbin] < tbins[itbin+1]
                       else tbins[itbin])
            time_str = '''
         TIME STEP NUMBER: {0}
         ------------------------------------
                 time min. = {1:.6e}
                 time max. = {2:.6e}
            '''.format(itbin, mintime, maxtime)
            t4out.append(time_str)
            t4out.append("\n")
            t4out.append(build_mesh_t4_output(mesh, ebins, itbin))
    return ''.join(t4out)


@given(shape=shapes(max_sides=[3, 3, 3, 3, 3, 1, 1]), sampler=data())
def test_parse_mesh_roundtrip(shape, sampler):
    '''Test printing mesh as Tripoli-4 output from random arrays got from
    Hypothesis. Also get energy and time bins.

    Check bins equality taking into account rounding using `numpy.allclose`
    instead of `numpy.array_equal`, limit is per default 1e-8. For time bins
    this is only check if more than 1 bin.

    Check array equality on if none of the binnigs are reversed (else a
    MeshDictBuilder object should be build to flip the arrays):

    * Equality of dtypes and shapes in all cases
    * Equality of ``'tally'`` and ``'sigma'`` arrays considered roundings.

    .. note::

       This test can be quite long depending on number of bins in space, energy
       and time. To avoid warning about that with pytest it is easier to limit
       these dimensions to 3 bins (from few runs).
    '''
    array = sampler.draw(arrays(dtype=np.dtype([('tally', FTYPE),
                                                ('sigma', FTYPE)]),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(0, 100)),
                                fill=nothing()))
    LOGGER.debug("shape: %s", str(shape))
    ebins = sampler.draw(bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(bins(elements=floats(0, 10), nbins=shape[4]))
    mesh_str = make_mesh_t4_output(array, ebins, tbins)
    note('mesh output:\n' + mesh_str)
    pres = pygram.scoreblock.parseString(mesh_str)
    if pres:
        oebins = ebins if ebins[0] < ebins[1] else ebins[::-1]
        otbins = tbins if tbins[0] < tbins[1] else tbins[::-1]
        assert np.allclose(pres[0]['mesh_res']['ebins'], oebins)
        if len(otbins) > 2:
            assert np.allclose(pres[0]['mesh_res']['tbins'], otbins)
        assert array.dtype == pres[0]['mesh_res']['mesh'].dtype
        assert array.shape == pres[0]['mesh_res']['mesh'].shape
        if np.array_equal(oebins, ebins) and np.array_equal(otbins, tbins):
            assert np.allclose(array[:]['tally'],
                               pres[0]['mesh_res']['mesh'][:]['tally'])
            assert np.allclose(array[:]['sigma'],
                               pres[0]['mesh_res']['mesh'][:]['sigma'])


def score_str():
    '''Example of score preceeding spectrum results, including units.'''
    specscore_str = ('''
         scoring mode : SCORE_SURF
         scoring zone :          Frontier        volumes : 2,1

''')
    return specscore_str

def spectrum_beginning_str(units=False, disc_batch=0):
    '''Beginning of spectrum block in Tripoli-4 output.
    Possibility to add units.
    '''
    spec_str = ('''\
         SPECTRUM RESULTS
         number of first discarded batches : {0}

'''.format(disc_batch))
    if units:
        spec_str += ('''\
         group                   score           sigma_%         score/lethargy
Units:   MeV                     neut.s^-1       %               neut.s^-1

''')
    else:
        spec_str += ('''\
         group (MeV)             score           sigma_%         score/lethargy

''')
    return spec_str

def spectrum_str(spectrum, ebins, it_index, units=False, disc_batch=0):
    '''Print Tripoli-4 output for spectrum in a string to be parsed afterwards.
    Energy, time, µ and φ are available.

    :param numpy.ndarray spectrum: spectrum array from Hypothesis
    :param list ebins: energy bins
    :param tuple(ints) tmuphi_index: time, µ and φ bin
    :param bool units: activate or not printing of units
    :returns: T4 output as a string
    '''
    t4out = []
    t4out.append(spectrum_beginning_str(units, disc_batch))
    for iebin in range(len(ebins)-1):
        index = it_index[0] + (iebin,)
        if len(it_index) > 1:
            index += it_index[1]
        t4out.append("{0:.6e} - {1:.6e} \t {2:.6e} \t {3:.6e} \t {4:.6e}\n"
                     .format(ebins[iebin], ebins[iebin+1],
                             spectrum[index]['score'],
                             spectrum[index]['sigma'],
                             spectrum[index]['score/lethargy']))
    t4out.append("\n")
    return ''.join(t4out)


def time_step_str(itbin, tbins):
    '''Print the Tripoli-4 output for time step.

    :param int itbin: time bin number
    :param list tbins: edges of time bins
    :returns: T4output as a string
    '''
    t4out = []
    if tbins[itbin] < tbins[itbin+1]:
        mintime = tbins[itbin]
        maxtime = tbins[itbin+1]
    else:
        mintime = tbins[itbin+1]
        maxtime = tbins[itbin]
    t4out.append("          TIME STEP NUMBER : {0}\n".format(itbin))
    t4out.append("          ------------------------------------\n")
    t4out.append("                  time min. = {0:.6e}\n".format(mintime))
    t4out.append("                  time max. = {0:.6e}\n\n".format(maxtime))
    return ''.join(t4out)


def mu_angle_str(imubin, mubins):
    '''Print the Tripoli-4 output for µ angular zone.

    :param int imubin: µ bin number
    :param list mubins: edges of µ bins
    :returns: T4output as a string
    '''
    t4out = []
    if mubins[imubin] < mubins[imubin+1]:
        minmu = mubins[imubin]
        maxmu = mubins[imubin+1]
    else:
        minmu = mubins[imubin+1]
        maxmu = mubins[imubin]
    t4out.append("          MU ANGULAR ZONE : {0}\n".format(imubin))
    t4out.append("          ------------------------------------\n")
    t4out.append("                  mu min. = {0:.6e}\n".format(minmu))
    t4out.append("                  mu max. = {0:.6e}\n\n".format(maxmu))
    return ''.join(t4out)


def phi_angle_str(iphibin, phibins):
    '''Print the Tripoli-4 output for φ angular zone.

    :param int iphibin: φ bin number
    :param list phibins: edges of φ bins
    :returns: T4output as a string
    '''
    t4out = []
    if phibins[iphibin] < phibins[iphibin+1]:
        minphi = phibins[iphibin]
        maxphi = phibins[iphibin+1]
    else:
        minphi = phibins[iphibin+1]
        maxphi = phibins[iphibin]
    t4out.append("                  PHI ANGULAR ZONE : {0}\n"
                 "                  ------------------------------------\n"
                 "                          phi min. = {1:.6e}\n"
                 "                          phi max. = {2:.6e}\n\n"
                 .format(iphibin, minphi, maxphi))
    return ''.join(t4out)


# pylint: disable=redefined-outer-name
def spectrum_t4_output(spectrum, bins, units):
    '''Build the Tripoli-4 output for spectra.
    Loops are done successively on time, µ and φ as it is done in the "real" T4
    outputs. Then the loop on energy bins is called.

    Time, µ and φ bins are always generated. They are only printed in the T4
    output if there are at least 2 bins, except for µ bins when there are more
    than 2 bins in φ (as it is done in "real" outputs).

    :param numpy.ndarray spectrum: spectrum array from Hypothesis
    :param dict bins: dictionary of lists representing binnings. Keys are
                      ``['e', 't', 'mu', 'phi']``.
    '''
    t4out = []
    t4out.append(score_str())
    t4out.append("\n")
    for itbin in range(len(bins['t'])-1):
        if len(bins['t']) > 2:
            t4out.append(time_step_str(itbin, bins['t']))
        for imubin in range(len(bins['mu'])-1):
            if len(bins['mu']) > 2 or len(bins['phi']) > 2:
                t4out.append(mu_angle_str(imubin, bins['mu']))
            for iphibin in range(len(bins['phi'])-1):
                if len(bins['phi']) > 2:
                    t4out.append(phi_angle_str(iphibin, bins['phi']))
                space_index = (0, 0, 0)
                tmuphi_index = (itbin, imubin, iphibin)
                t4out.append(spectrum_str(spectrum, bins['e'],
                                          (space_index, tmuphi_index), units))
    return ''.join(t4out)


def reverse_bins(bins):
    '''Reverse bins if they are in decreasing order.

    :param dict bins: dictionary of bins
    :returns: dict of bins all in increasing order
    '''
    rbins = bins
    for key in bins:
        if bins[key][0] > bins[key][1]:
            rbins[key] = bins[key][::-1]
    return rbins


def compare_bins(bins, spectrum_res):
    '''Compare bins: generated ones versus bins retrieved from spectrum after
    parsing.

    :param dict bins: dictionary of lists representing binnings. Keys are
                      ``['e', 't', 'mu', 'phi']``.
    :param dict spectrum_res: dictionary for spectrum result. Relevant keys for
                              current method: ``['ebins', 'tbins', 'mubins',
                              'phibins']``.

    .. note::

       The loop is done on keys of *bins* and not of *spectrum_res* as there
       are fewer. The 4 binnings always exist in spectrum case, but are only
       used if at least 2 bins are present in time, µ and φ dimensions. They
       always exist for energy.
    '''
    for key in bins:
        if key+'bins' in spectrum_res:
            assert np.allclose(spectrum_res[key+'bins'], bins[key])


@given(array_bins=array_and_bins(dtype=np.dtype([('score', FTYPE),
                                                 ('sigma', FTYPE),
                                                 ('score/lethargy', FTYPE)]),
                                 max_dim=(1, 1, 1, 5, 5, 2, 2),
                                 elements=tuples(floats(0, 1),
                                                 floats(0, 100),
                                                 floats(0, 1)),
                                 reverse=just(False)),
       units=booleans())
def test_parse_spectrum_roundtrip(array_bins, units):
    '''Test printing spectrum as Tripoli-4 output from random arrays got from
    Hypothesis. Also get energy, time, µ and φ angular bins (alwats in
    increasing order for easiness of checks and as the flip is checked in
    another test.

    Check bins equality taking into account rounding using `numpy.allclose`
    instead of `numpy.array_equal`, limit is per default 1e-8. For time, µ and
    φ bins this is only check if more than 1 bin.

    Check array equality:

    * Equality of dtypes and shapes in all cases
    * Equality of ``'score'``, ``'sigma'`` and ``'score/lethargy'`` arrays
      considering roundings.

    .. note::

       This test can be quite long depending on number of bins in energy, time,
       µ or φ. To avoid warning about that with pytest it is easier to limit
       these dimensions to 3 bins (from few runs).
    '''
    array, bins = array_bins
    LOGGER.debug("shape: %s", str(array.shape))
    spectrum_t4out = spectrum_t4_output(array, bins, units)
    pres = pygram.scoreblock.parseString(spectrum_t4out)
    compare_bins(bins, pres[0]['spectrum_res'])
    spectrum = pres[0]['spectrum_res']['spectrum']
    assert array.dtype == spectrum.dtype
    assert array.shape == spectrum.shape
    assert np.allclose(array[:]['score'], spectrum[:]['score'])
    assert np.allclose(array[:]['sigma'], spectrum[:]['sigma'])
    assert np.allclose(array[:]['score/lethargy'],
                       spectrum[:]['score/lethargy'])

def gb_step_str(istep, sebins):
    '''Print the Tripoli-4 output for Green bands steps (source steps in
    energy).

    :param int istep: step number (or source energy bin number)
    :param list sebins: edges of bins of energy of source
    :returns: T4output as a string
    '''
    t4out = []
    if sebins[istep] < sebins[istep+1]:
        minse = sebins[istep]
        maxse = sebins[istep+1]
    else:
        minse = sebins[istep+1]
        maxse = sebins[istep]
    t4out.append(" "*9 + "* SOURCE SPECTRUM STEP NUMBER : {}\n".format(istep))
    t4out.append(" "*9 + "------------------------------------\n")
    t4out.append(" "*17 + "source energy min. = {0:.6e}\n".format(minse))
    t4out.append(" "*17 + "source energy max. = {0:.6e}\n".format(maxse))
    t4out.append("\n")
    return ''.join(t4out)

def gb_with_tab_str(array, bins, disc_batch, istep):
    '''Print Tripoli-4 for Green bands with tabulations.

    :param numpy.ndarray array: green bands data
    :param dict bins: dictionary of lists representing energy bins (source and
                      observed particles).
    :param int disc_batch: number of first discarded batchs.
    :param int istep: current step number
    :returns: T4output as a string
    '''
    t4out = []
    for isource in range(array.shape[1]):
        for utab in range(array.shape[2]):
            for vtab in range(array.shape[3]):
                for wtab in range(array.shape[4]):
                    t4out.append(" "*9 + "SOURCE NUMBER : {0}".format(isource))
                    t4out.append("       SOURCE TABULATION : "
                                 "u = {0}, v = {1}, w = {2}\n"
                                 .format(utab, vtab, wtab))
                    t4out.append(" "*9 + "-"*72 + "\n\n")
                    t4out.append(spectrum_str(
                        array, bins['e'],
                        ((istep, isource, utab, vtab, wtab),),
                        disc_batch=disc_batch))
    return ''.join(t4out)

def gb_without_tab_str(array, bins, disc_batch, istep):
    '''Print Tripoli-4 for Green bands without tabulations, i.e. in case of
    dimensions of ``(u, v, w) = (1, 1, 1)``.

    :param numpy.ndarray array: green bands data
    :param dict bins: dictionary of lists representing energy bins (source and
                      observed particles).
    :param int disc_batch: number of first discarded batchs.
    :param int istep: current step number
    :returns: T4output as a string
    '''
    t4out = []
    for isource in range(array.shape[1]):
        t4out.append(" "*9 + "SOURCE NUMBER : {}\n".format(isource))
        t4out.append(" "*9 + "------------------------------------\n\n")
        t4out.append(spectrum_str(array, bins['e'],
                                  ((istep, isource, 0, 0, 0),),
                                  disc_batch=disc_batch))
        t4out.append("\n")
    return ''.join(t4out)

def gb_t4_output(array, bins, disc_batch):
    '''Build the Tripoli-4 output for Green bands.
    Loops are successively done on steps (equivalent to bins in energy of
    source), sources, tabulation if not (0, 0, 0) and energy bins.

    If tabulation is (0, 0, 0), source tabulation won't be written in the
    output (to match its absence seen some listings).

    :param numpy.ndarray array: green bands data
    :param dict bins: dictionary of lists representing energy bins (source and
                      observed particles).
    :param int disc_batch: number of first discarded batchs.
    :returns: T4output as a string
    '''
    t4out = []
    t4out.append(score_str())  # default score, could be somthing else...
    t4out.append("\n")
    for istep in range(len(bins['se'])-1):
        t4out.append(gb_step_str(istep, bins['se']))
        if array.shape[2:5] == (1, 1, 1):
            t4out.append(gb_without_tab_str(array, bins, disc_batch, istep))
        else:
            t4out.append(gb_with_tab_str(array, bins, disc_batch, istep))
    return ''.join(t4out)

@composite
def green_bands(draw, max_dims=(5, 3, 2, 2, 2, 5)):
    '''Composite Hypothesis strategy to generate dimension to source
    tabulation.

    :param tuple max_dims: maximum dimensions in
                           ``'steps', 'source', 'u', 'v', 'w', 'energy'``

    .. note::

       ``(u, v, w) = (1, 1, 1)`` is a special case as the SOURCE TABULATION is
       not written in the listing in that case, it should always be run, so
       dimensions of ``u``, ``v`` and ``w`` should not be to high.
    '''
    shape = draw(tuples(integers(1, max_dims[0]),  # steps (source energy bins)
                        integers(1, max_dims[1]),  # sources
                        integers(1, max_dims[2]),  # u
                        integers(1, max_dims[3]),  # v
                        integers(1, max_dims[4]),  # w
                        integers(1, max_dims[5]))) # energy bins
    array = draw(arrays(
        dtype=np.dtype([('score', FTYPE), ('sigma', FTYPE),
                        ('score/lethargy', FTYPE)]),
        shape=shape,
        elements=tuples(floats(0, 1), floats(0, 100), floats(0, 1)),
        fill=nothing()))
    bins = {}
    bins['e'] = draw(bins(
        elements=floats(0, 20), nbins=shape[5], revers=booleans()))
    bins['se'] = (draw(bins(elements=floats(0, 20), nbins=shape[0],
                            revers=just(False)))
                  if shape[0] == 1
                  else draw(bins(elements=floats(0, 20), nbins=shape[0],
                                 revers=booleans())))
    return array, bins

@settings(max_examples=20, deadline=300)
@given(sampler=data())
def test_print_parse_green_bands(sampler):
    '''Test printing Green bands results as Tripoli-4 output from random arrays
    got from Hypothesis. Other needed quantities are also obtained thanks to
    Hypothesis like steps and sources.

    Tests performed:

    * Presence of the parsed result
    * Number of Green bands result = 1
    * Keys inside parsed result
    * Keys specific to Green band result (spectrum in energy and energy of
      source + discarded batchs)
    * Equality at 10\ :sup:`-8` of

       * Energy bins
       * Energy bins of source
       * Array representing Green bands (dtype, shape and ``'score'``,
         ``'sigma'`` and ``'score/lethargy'`` arrays)

    * Equality of number of discarded batchs
    '''
    array, bins = sampler.draw(green_bands(max_dims=(5, 3, 2, 2, 2, 5)))
    disc_batch = sampler.draw(integers(0, 5))
    gb_t4_out = gb_t4_output(array, bins, disc_batch)
    pres = pygram.scoreblock.parseString(gb_t4_out)
    assert pres
    assert len(pres) == 1
    assert (sorted(list(pres[0].keys()))
            == ['greenband_res', 'scoring_mode', 'scoring_zone'])
    gbres = pres[0]['greenband_res']
    assert (sorted(list(gbres.keys()))
            == ['disc_batch', 'ebins', 'sebins', 'vals'])
    assert np.allclose(gbres['ebins'], np.array(bins['e']))
    assert np.allclose(gbres['sebins'], np.array(bins['se']))
    assert array.dtype == gbres['vals'].dtype
    assert array.shape == gbres['vals'].shape
    assert np.allclose(gbres['vals'][:]['score'], array[:]['score'])
    assert np.allclose(gbres['vals'][:]['sigma'], array[:]['sigma'])
    assert np.allclose(gbres['vals'][:]['score/lethargy'],
                       array[:]['score/lethargy'])
    assert gbres['disc_batch'] == disc_batch

# @composite
# def keff_matrix():

def keff_t4_genoutput(keffmat, sigmat, corrmat, fcomb):
    '''Pring keff as generic response of Tripoli-4.'''
    t4out = []
    t4out.append(" "*8 + "ENERGY INTEGRATED RESULTS\n\n")
    t4out.append("number of batches used: 80\n\n")
    keffs = ['KSTEP ', 'KCOLL ', 'KTRACK']
    for ikeff in range(3):
        t4out.append(" {0} {1:.6e}    {2:.6e}\n"
                     .format(keffs[ikeff], keffmat[ikeff][ikeff],
                             sigmat[ikeff][ikeff]))
    t4out.append("\n")
    t4out.append(" "*10 + "estimators" + " "*19 + "correlations" + " "*8
                 + "combined values" + " "*5 + "combined sigma%\n")
    for ikeff in range(2):
        for jkeff in range(ikeff+1, 3):
            t4out.append(" "*10
                         + "{0} <-> {1}".format(keffs[ikeff], keffs[jkeff])
                         + " "*12 + "{0:.6e}".format(corrmat[ikeff][jkeff])
                         + " "*8 + "{0:.6e}".format(keffmat[ikeff][jkeff])
                         + " "*8 + "{0:.6e}\n".format(sigmat[ikeff][jkeff]))
    t4out.append("\n")
    t4out.append(" "*10 + "full combined estimator  {0:.6e} {1:.6e}"
                 .format(fcomb[0], fcomb[1]))
    t4out.append("\n")
    return ''.join(t4out)

@settings(max_examples=20)
@given(sampler=data())
def test_print_parse_keffs(sampler):
    '''Test printing k\ :sub:`eff` results as Tripoli-4 output from Hypothesis
    strategies then parse it and compare results.

    Tests performed:

    * Presence of keff result aftre parsing (success of parsing)
    * keff result is dictionary containing one key: ``'keff_res'``
    * Keys inside dictionary stored under ``'keff_res'`` are OK
    * Equality at rounding (10\ :sup:`-8`) of correlation matrix, k\ :sub:`eff`
      matrix, σ matrix and full combination estimation.
    '''
    corrmat = sampler.draw(
        arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0, 0.5)))
    corrmat += corrmat.T
    for ielt in range(3):
        corrmat[ielt][ielt] = 1
    keffmat = sampler.draw(
        arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0.3, 0.7)))
    keffmat += keffmat.T
    sigmat = sampler.draw(
        arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0, 0.5)))
    sigmat += sigmat.T
    fcomb = sampler.draw(tuples(floats(0.6, 1.4), floats(0, 1)))
    keff_t4_out = keff_t4_genoutput(keffmat, sigmat, corrmat, fcomb)
    keffres = pygram.responseblock.parseString(keff_t4_out)
    assert keffres
    assert list(keffres.keys()) == ['keff_res']
    assert (sorted(list(keffres['keff_res'].keys()))
            == ['correlation_matrix', 'estimators', 'full_comb_estimation',
                'keff_matrix', 'sigma_matrix', 'used_batch'])
    assert np.allclose(keffres['keff_res']['correlation_matrix'], corrmat)
    assert np.allclose(keffres['keff_res']['keff_matrix'], keffmat)
    assert np.allclose(keffres['keff_res']['sigma_matrix'], sigmat)
    assert np.isclose(
        keffres['keff_res']['full_comb_estimation']['keff'], fcomb[0])
    assert np.isclose(
        keffres['keff_res']['full_comb_estimation']['sigma'], fcomb[1])

def test_array_from_t4():
    '''Fake test'''
    # test from a real example
    correlation = np.array([[1, 8.220342e-01, 7.417923e-01],
                            [8.220342e-01, 1, 8.338559e-01],
                            [7.417923e-01, 8.338559e-01, 1]])
    keffr = np.array([9.953052e-01, 9.958371e-01, 9.960223e-01])
    sigmar = np.array([1.458369e-01, 1.253360e-01, 1.167335e-01])
    combkeff = np.array([9.957839e-01, 9.959473e-01, 9.959687e-01])
    print("VRAI EXEMPLE")
    print("correlation:\n", correlation)
    print("keffs:", keffr)
    print("sigmas:", sigmar)
    # print("combined keffs ?\n")
    print("keffr * correlation:\n", keffr * correlation)
    # print("keffr @ correlation:\n", keffr @ correlation)
    print("dot(keffr, correlation):\n", np.dot(keffr, correlation))
    print("dot(dot(keffr, correlation), keffr.T):\n",
          np.dot(np.dot(keffr, correlation), keffr.T))
    # print(correlation*correlation.T)
    # print(np.matrix(correlation).I)
    # print(sigmar * correlation * sigmar.T)
    # print(sigmar*sigmar)
    # print((sigmar * correlation * sigmar.T)/sigmar)
    # covmat = np.array([[1.458369e-03, 1.250667e-03, 1.162897e-03],
    #                    [1.250667e-03, 1.253360e-03, 1.149536e-03],
    #                    [1.162897e-03, 1.149536e-03, 1.167335e-03]])
    sig = sigmar/100.*keffr
    print("sig =", sig)
    # print(sigmanop*correlation*sigmanop.T)
    # combsig = np.array([1.250667e-01, 1.162897e-01, 1.149536e-01])
    # print("essai:", (keffr[0] + keffr[1])/2)  #- 2*correlation[0][1]*keffr[0])
    # mydata = np.concatenate((keffr, sigmar)).reshape(3,2, order="F")
    # print(mydata)
    # print(np.cov(mydata))
    # print(np.cov(keffr))
    testmat = np.array([[sig[0]*sig[0], sig[0]*sig[1], sig[0]*sig[2]],
                        [sig[1]*sig[0], sig[1]*sig[1], sig[1]*sig[2]],
                        [sig[2]*sig[0], sig[2]*sig[1], sig[2]*sig[2]]])
    print(testmat)
    sigdiag = np.diag(sig)
    print(sigdiag)
    print("sigdiag-1 =\n", np.linalg.inv(sigdiag))
    print("correlation * sigdiag-1 =\n",
          np.dot(correlation, np.linalg.inv(sigdiag)))
    print("dot(correlation, sigdiag) =\n", np.dot(correlation, sigdiag))
    print("dot(correlation, sig) =\n", np.dot(correlation, sig))
    print("dot(keffr, dot(correlation, sig).T) =\n",
          np.dot(keffr, np.dot(correlation, sig).T))
    print("dot(correlation, sqrt(testmat)) =\n",
          np.dot(correlation, np.sqrt(testmat)))
    combsig = np.array([1.250667e-01, 1.162897e-01, 1.149536e-01])
    combkeff = np.array([9.957839e-01, 9.959473e-01, 9.959687e-01])
    cbsig = combsig/100.*combkeff
    # testmat2 = np.array([[sig[0]**2, cbsig]])
    # kmat = np.array([[keffr[0], combkeff[0], combkeff[1]],
    #                  [combkeff[0], keffr[1], combkeff[2]],
    #                  [combkeff[1], combkeff[2], keffr[2]]])
    # smat = np.array([[sig[0], cbsig[0], cbsig[1]],
    #                  [cbsig[0], sig[1], cbsig[2]],
    #                  [cbsig[1], cbsig[2], sig[2]]])
    # print(np.cov(kmat))
    print("sig*sig.T =\n", sig*sig.T)
    print("dot(sig, sig.T) =\n", np.dot(sig, sig.T))
    print(np.sqrt(sig**2) * correlation)
    print(correlation[0][1]*np.sqrt(sig[0]*sig[1]))
    tmat = np.array([[correlation[0][0]*np.sqrt(sig[0]*sig[0]),
                      correlation[0][1]*np.sqrt(sig[0]*sig[1]),
                      correlation[0][2]*np.sqrt(sig[0]*sig[2])],
                     [correlation[1][0]*np.sqrt(sig[1]*sig[0]),
                      correlation[1][1]*np.sqrt(sig[1]*sig[1]),
                      correlation[1][2]*np.sqrt(sig[1]*sig[2])],
                     [correlation[2][0]*np.sqrt(sig[2]*sig[0]),
                      correlation[2][1]*np.sqrt(sig[2]*sig[1]),
                      correlation[2][2]*np.sqrt(sig[2]*sig[2])]])
    print(tmat)
    covmat = np.array([[correlation[0][0]*sig[0]*sig[0],
                        correlation[0][1]*sig[0]*sig[1],
                        correlation[0][2]*sig[0]*sig[2]],
                       [correlation[1][0]*sig[1]*sig[0],
                        correlation[1][1]*sig[1]*sig[1],
                        correlation[1][2]*sig[1]*sig[2]],
                       [correlation[2][0]*sig[2]*sig[0],
                        correlation[2][1]*sig[2]*sig[1],
                        correlation[2][2]*sig[2]*sig[2]]])
    print(covmat)
    covmat = np.matrix(covmat)
    print(covmat.A1)
    # print("sig.correlation =\n", np.dot(sig, correlation))
    # print("sig*correlation =\n", sig * correlation)
    # print("sig.correlation.sigT =\n", np.dot(np.dot(sig, correlation), sig.T))
    # scts = sig * correlation * sig.T
    # print("sig*correlation*sig.T =\n", scts)
    # print((scts + scts.T)/2)
    sigmat = np.array([[sig[0]*sig[0], sig[0]*sig[1], sig[0]*sig[2]],
                       [sig[1]*sig[0], sig[1]*sig[1], sig[1]*sig[2]],
                       [sig[2]*sig[0], sig[2]*sig[1], sig[2]*sig[2]]])
    print(sigmat)
    print(sigmat[0][1])
    print(sigmat[0, 1])
    print("sig.T * sig =\n", sig.T * sig)
    print("np.dot(sig.T, sig) =\n", np.dot(sig.T, sig))
    print("np.dot(sig, sig.T) =\n", np.dot(sig, sig.T))
    print("sig.dot(sig.T) =\n", sig.dot(sig.T))
    print("sigT.dot(sig) =\n", (sig.T).dot(sig))
    print("np.outer(sig, sig.T) =\n", np.outer(sig, sig.T))
    print("np.outer(sig.T, sig) =\n", np.outer(sig.T, sig))
    print("np.outer(sig, sig) =\n", np.outer(sig, sig))
    assert np.allclose(sigmat, np.outer(sig, sig))
    print("sig * sig.T =\n", sig * sig.T)
    correlation = np.matrix(correlation)
    tcovA1 = correlation.A1 * np.matrix(sigmat).A1
    print("tcovA1 =\n", tcovA1)
    print("outer(corr, sigmat) =\n", np.outer(correlation, sigmat))
    print("outer(corr, sig) =\n", np.outer(correlation, sig))
    print("(corr * sigmat) =\n", correlation *sigmat)
    print("array(corr * sigmat) =\n", np.array(correlation) *sigmat)
    covmat2 = tcovA1.reshape(3, 3)
    print("covmat2 =\n", covmat2)
    print("type covmat:", type(covmat), "covmat2:", type(covmat2))
    print("shape covmat:", covmat.shape, "covmat2:", covmat2.shape)
    print("ndim covmat:", covmat.ndim, "covmat2:", covmat2.ndim)
    assert np.allclose(covmat, covmat2)
    # combined value
    for ikeff in range(2):
        for jkeff in range(ikeff+1, 3):
            print(sig[ikeff], sig[ikeff]**2, covmat2[ikeff][jkeff])
            denom = sig[ikeff]**2 + sig[jkeff]**2 - 2*covmat2[ikeff][jkeff]
            num = ((sig[jkeff]**2 - covmat2[ikeff][jkeff])*keffr[ikeff]
                   + (sig[ikeff]**2 - covmat2[ikeff][jkeff])*keffr[jkeff])
            print("comb({0}, {1}) = {2}".format(ikeff, jkeff, num/denom))
            assert np.isclose(num/denom, combkeff[ikeff+jkeff-1])
            print(sigmat.shape)
            print(sigmat[ikeff, jkeff])
            numscb = sigmat[ikeff, jkeff]**2 - covmat2[ikeff, jkeff]**2
            print("et le sigma =", np.sqrt(numscb/denom))
            assert np.isclose(np.sqrt(numscb/denom), cbsig[ikeff+jkeff-1])
