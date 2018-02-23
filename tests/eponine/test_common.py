'''Tests for the :mod:`common <valjean.eponine.common>` module.'''

import numpy as np
from hypothesis import given, note
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


def spectrum_beginning_str(units=False):
    '''Beginning of spectrum block in Tripoli-4 output.
    Possibility to add units.
    '''
    spec_str = ('''\
         SPECTRUM RESULTS
         number of first discarded batches : 0

         group                   score           sigma_%         score/lethargy
''')
    if units:
        spec_str += ('''\
Units:   MeV                     neut.s^-1       %               neut.s^-1
''')
    return spec_str


def spectrum_str(spectrum, ebins, tmuphi_index, units=False):
    '''Print Tripoli-4 output for spectrum in a string to be parsed afterwards.
    Energy, time, µ and φ are available.

    :param numpy.ndarray spectrum: spectrum array from Hypothesis
    :param list ebins: energy bins
    :param tuple(ints) tmuphi_index: time, µ and φ bin
    :param bool units: activate or not printing of units
    :returns: T4 output as a string
    '''
    t4out = []
    t4out.append(spectrum_beginning_str(units))
    for iebin in range(len(ebins)-1):
        index = (0, 0, 0, iebin) + tmuphi_index
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
    '''Build the Trupoli-4 output for spectra.
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
                tmuphi_index = (itbin, imubin, iphibin)
                t4out.append(spectrum_str(spectrum, bins['e'],
                                          tmuphi_index, units))
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
