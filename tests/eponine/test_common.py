'''Tests for the :mod:`common <valjean.eponine.common>` module.'''

import numpy as np
from hypothesis import given, note, settings, assume
from hypothesis.strategies import (integers, lists, composite, tuples,
                                   floats, nothing, booleans, just, text)
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
                   unique_by=lambda x: '{0:.6e}'.format(abs(x)))),
        reverse=revers)
    arr = np.array(as_list)
    note('nbins=' + str(nbins))
    note('as_list=' + str(as_list))
    note('revers=' + str(revers))
    note('bins=' + str(arr))
    return arr


@given(array_bins=array_and_bins(
    dtype=np.dtype([('tally', np.float), ('sigma', np.float)]),
    max_dim=(3, 3, 3, 5, 5, 1, 1),
    elements=tuples(floats(0, 1), floats(5, 20))))
def test_flip_mesh(array_bins):
    '''Test flipping mesh.

    Generate with hypothesis a mesh with maximum sides
    ``[s0, s1, s2, E, t, mu, phi] = [3, 3, 3, 5, 5, 1, 1]``
    as no mu or phi bins are available for the moment for meshes.

    Generate energy and time binnings. They can be increasing or decreasing
    depending on the value of the boolean chosen by hypothesis in order to
    test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    array, lbins = array_bins
    note('shape = ' + str(array.shape))
    note('content = ' + str(array))
    note(lbins['e'].shape)
    note(lbins['t'].shape)
    incr = dict(map(
        lambda i: (i[0], 1 if len(i[1]) > 1 and i[1][1] > i[1][0] else -1),
        lbins.items()))

    mesh = MeshDictBuilder(['tally', 'sigma'], array.shape)
    mesh.bins['e'] = lbins['e']
    mesh.bins['t'] = lbins['t']
    mesh.arrays['default'] = array
    mesh.flip_bins()
    assert np.all(np.diff(mesh.bins['e']) > 0.0)
    assert np.all(np.diff(mesh.bins['t']) > 0.0)

    for comp in array.dtype.names:
        assert np.array_equal(array[comp],
                              mesh.arrays['default'][comp]
                              [:, :, :, ::incr['e'], ::incr['t'], :, :])


@given(array_bins=array_and_bins(
    dtype=np.dtype([('score', np.float), ('sigma', np.float),
                    ('score/lethargy', np.float)]),
    max_dim=(1, 1, 1, 5, 5, 3, 3),
    elements=tuples(floats(0, 1), floats(5, 20), floats(0, 1))))
def test_flip_spectrum(array_bins):
    '''Test flipping spectrum.

    Generate with hypothesis a mesh with max dimensions
    ``[s0, s1, s2, E, t, mu, phi] = [1, 1, 1, 5, 5, 3, 3]``.

    Generate energy, time, mu and phi angle binnings. They can be increasing or
    decreasing depending on the value of the boolean chosen by hypothesis in
    order to test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    array, lbins = array_bins
    incr = dict(map(
        lambda i: (i[0], 1 if len(i[1]) > 1 and i[1][1] > i[1][0] else -1),
        lbins.items()))

    spectrum = SpectrumDictBuilder(array.dtype.names, array.shape)
    spectrum.bins = {'e': lbins['e'], 't': lbins['t'], 'mu': lbins['mu'],
                     'phi': lbins['phi']}
    spectrum.arrays['default'] = array
    spectrum.flip_bins()

    assert np.all(np.diff(spectrum.bins['e']) > 0.0)
    assert np.all(np.diff(spectrum.bins['t']) > 0.0)
    assert np.all(np.diff(spectrum.bins['mu']) > 0.0)
    assert np.all(np.diff(spectrum.bins['phi']) > 0.0)
    for comp in array.dtype.names:
        assert np.array_equal(
            array[comp],
            spectrum.arrays['default'][comp]
            [:, :, :, ::incr['e'], ::incr['t'], ::incr['mu'], ::incr['phi']])


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


@given(array_bins=array_and_bins(
    dtype=np.dtype([('tally', FTYPE), ('sigma', FTYPE)]),
    max_dim=(3, 3, 3, 3, 3, 1, 1),
    elements=tuples(floats(0, 1), floats(0, 100)),
    reverse=just(False)))
def test_parse_mesh_roundtrip(array_bins):
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
    array, lbins = array_bins
    LOGGER.debug("shape: %s", str(array.shape))
    mesh_str = make_mesh_t4_output(array, lbins['e'], lbins['t'])
    note('mesh output:\n' + mesh_str)
    pres = pygram.scoreblock.parseString(mesh_str)
    assert pres
    parsed_mesh = pres[0]['mesh_res']
    assert np.allclose(parsed_mesh['ebins'], lbins['e'])
    if len(lbins['t']) > 2:
        assert np.allclose(parsed_mesh['tbins'], lbins['t'])
    assert array.dtype == parsed_mesh['mesh'].dtype
    assert array.shape == parsed_mesh['mesh'].shape
    for comp in array.dtype.names:
        assert np.allclose(array[:][comp], parsed_mesh['mesh'][:][comp])


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
    assert pres
    compare_bins(bins, pres[0]['spectrum_res'])
    spectrum = pres[0]['spectrum_res']['spectrum']
    assert array.dtype == spectrum.dtype
    assert array.shape == spectrum.shape
    for comp in array.dtype.names:
        assert np.allclose(array[:][comp], spectrum[:][comp])


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
    shape = draw(shapes(max_dims))
    array = draw(arrays(
        dtype=np.dtype([('score', FTYPE), ('sigma', FTYPE),
                        ('score/lethargy', FTYPE)]),
        shape=shape,
        elements=tuples(floats(0, 1), floats(0, 100), floats(0, 1)),
        fill=nothing()))
    the_bins = {'e': draw(bins(elements=floats(0, 20), nbins=shape[5],
                               reverse=booleans())),
                'se': (draw(bins(elements=floats(0, 20), nbins=shape[0],
                                 reverse=just(False)))
                       if shape[0] == 1
                       else draw(bins(elements=floats(0, 20), nbins=shape[0],
                                      reverse=booleans())))}
    return array, the_bins

@settings(max_examples=100, deadline=300)
@given(array_bins=green_bands(max_dims=(5, 3, 2, 2, 2, 5)),
       disc_batch=integers(0, 5))
def test_parse_greenbands_roundtrip(array_bins, disc_batch):
    r'''Test printing Green bands results as Tripoli-4 output from random
    arrays got from Hypothesis. Other needed quantities are also obtained
    thanks to Hypothesis like steps and sources.

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
    array, bins = array_bins
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
    for comp in array.dtype.names:
        assert np.allclose(gbres['vals'][:][comp], array[:][comp])
    assert gbres['disc_batch'] == disc_batch


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

@settings(max_examples=100)
@given(corrmat=arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0, 0.5)),
       keffmat=arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0.3, 0.7)),
       sigmat=arrays(dtype=FTYPE, shape=(3, 3), elements=floats(0, 0.5)),
       combination=tuples(floats(0.6, 1.4), floats(0, 1)))
def test_parse_keffs_roundtrip(corrmat, keffmat, sigmat, combination):
    r'''Test printing k\ :sub:`eff` results as Tripoli-4 output from Hypothesis
    strategies then parse it and compare results.

    Tests performed:

    * Presence of keff result aftre parsing (success of parsing)
    * keff result is dictionary containing one key: ``'keff_res'``
    * Keys inside dictionary stored under ``'keff_res'`` are OK
    * Equality at rounding (10\ :sup:`-8`) of correlation matrix, k\ :sub:`eff`
      matrix, σ matrix and full combination estimation.

    .. note::

       Only parsing is tested here, not the coherence/consistence of the matrix
       generated by Hypothesis (no-sense combined results for example).
    '''
    # First need to symmetrize the 3 matrix and put correlation diagonal to 1.
    corrmat += corrmat.T
    for ielt in range(3):
        corrmat[ielt][ielt] = 1
    keffmat += keffmat.T
    sigmat += sigmat.T
    # Then test...
    keff_t4_out = keff_t4_genoutput(keffmat, sigmat, corrmat, combination)
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
        keffres['keff_res']['full_comb_estimation']['keff'], combination[0])
    assert np.isclose(
        keffres['keff_res']['full_comb_estimation']['sigma'], combination[1])


@composite
def keff_best_estimation(draw, n_estim):
    r'''Composite Hypothesis strategy to generate best estimation of
    k\ :sub:`eff` for at least 3 estimators.

    Default estimators are: ``['KSTEP', 'KCOLL', 'KTRACK']``.
    ``'MACRO KCOLL'`` can be added to this list as any other estimator whose
    name is composed of cap letters and spaces.

    k\ :sub:`eff`, σ and σ\ :sub:`%` are computed (`float`) as well as the
    number of discarded batches. Required number of batches is set to 100 here.

    :param int n_estim: maximum number of estimators
    :returns: dict as returned by parser
    '''
    n_estim = draw(integers(3, n_estim))
    estimators = ['KSTEP', 'KCOLL', 'KTRACK']
    if n_estim > 3:
        estimators.append("MACRO KCOLL")
        if n_estim > 4:
            estimators.append(draw(text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ ",
                                        min_size=3, max_size=8,
                                        average_size=4)).rstrip())
    disc_batchs = draw(lists(elements=integers(1, 20),
                             min_size=n_estim, max_size=n_estim))
    keffs = draw(lists(elements=floats(0.9, 1.1),
                       min_size=n_estim, max_size=n_estim))
    sigmas = draw(lists(elements=floats(1e-4, 2e-1),
                        min_size=n_estim, max_size=n_estim))
    keff_res = []
    for iestim, _ in enumerate(estimators):
        keff_res.append({'estimator': estimators[iestim],
                         'best_disc_batchs': disc_batchs[iestim],
                         'used_batch': 100 - disc_batchs[iestim],
                         'bestkeffres': {
                             'keff': keffs[iestim],
                             'sigma': sigmas[iestim],
                             'sigma%': sigmas[iestim]/keffs[iestim]*100}})
    return keff_res

def bekeff_t4_output(be_keff):
    r'''Print in a string the best estimation of k\ :sub:`eff` as in Tripoli-4
    outputs.
    '''
    t4out = []
    for bestim in be_keff:
        t4out.append(" "*10 + "{0} ESTIMATOR\n".format(bestim['estimator']))
        t4out.append(" "*9 + "-"*(len(t4out[-1])+4) + "\n\n\n")
        t4out.append(" "*9
                     + "best results are obtained with discarding {} batches"
                     .format(bestim['best_disc_batchs'])
                     + "\n\n")
        t4out.append(" "*9
                     + "number of batch used: {}".format(bestim['used_batch'])
                     + " "*8
                     + "keff = {0:.6e}".format(bestim['bestkeffres']['keff'])
                     + " "*5
                     + "sigma = {0:.6e}".format(bestim['bestkeffres']['sigma'])
                     + " "*5
                     + "sigma% = {0:.6e}"
                     .format(bestim['bestkeffres']['sigma%'])
                     + "\n\n\n")
    return ''.join(t4out)


@settings(max_examples=100)
@given(keff_res=keff_best_estimation(5))
def test_parse_best_keff_roundtrip(keff_res):
    r'''Test printing k\ :sub:`eff` best estimation and optionally k\ :sub:`ij`
    best estimation as Tripoli-4 output in a string.
    '''
    bekeff_t4_out = bekeff_t4_output(keff_res)
    pres = pygram.defkeffblock.parseString(bekeff_t4_out)
    assert pres
    assert len(pres) == 1
    assert len(pres[0]) == len(keff_res)
    assert sorted(list(pres[0][0].keys())) == sorted(list(keff_res[0].keys()))
    for ikeff, bekeff in enumerate(keff_res):
        for key in bekeff:
            if key != 'bestkeffres':
                assert bekeff[key] == pres[0][ikeff][key]
            else:
                for ikey in bekeff[key]:
                    assert np.isclose(bekeff[key][ikey],
                                      pres[0][ikeff][key][ikey])


def kij_t4_output(evals, evecs, matrix):
    r'''Print Tripoli-4 output for k\ :sub:`ij` results in a string to be
    parsed afterwards.

    :param numpy.ndarray evals: eigenvalues (N)
    :param numpy.ndarray evecs: eigenvectors (N×N)
    :param numpy.ndarray matrix: k\ :sub:`ij` matrix (N×N)
    :returns: T4 output as a string
    '''
    t4out = []
    t4out.append(" "*8 + "ENERGY INTEGRATED RESULTS\n\n")
    t4out.append("number of batches used: 80\n\n\n")
    t4out.append(" "*12 + "kij-keff = {0:.6e}\n\n".format(np.real(evals[0])))
    t4out.append(" "*12 + "dominant ratio = {0:.6e}\n\n\n"
                 .format(np.real(evals[1])/np.real(evals[0])))
    t4out.append("eigenvalues (re, im)\n\n")
    for ival in evals:
        t4out.append("{0:.6e}".format(np.real(ival)) + " "*4
                     + "{0:.6e}".format(np.imag(ival)) + "\n")
    t4out.append("\n\n")
    t4out.append("eigenvectors\n\n")
    for ivec in evecs:
        for icoord in ivec:
            t4out.append("{0:.6e}".format(icoord) + " "*4)
        t4out.append("\n")
    t4out.append("\n\n")
    t4out.append("KIJ_MATRIX :\n\n")
    for kij_i in matrix:
        for kij_j in kij_i:
            t4out.append("{0:.6e}".format(kij_j) + " "*4)
        t4out.append("\n")
    t4out.append("\n")
    return ''.join(t4out)

@composite
def kij_results(draw, dimension):
    r'''Composite Hypothesis strategy to generate eigenvalues, eigenvectors and
    k\ :sub:`ij` matrix.

    Construct the complex eigen values from full random real part and partially
    random imaginary part, reprenseting maximum half of the array, rest is
    filled with 0 (inserted at beginning of array). Real part of first
    eigenvalue should be different from 0 to be able to calculate dominant
    ratio.

    Eigenvectors matrix is required to have det = 0. Used eigenvectors are
    normalized. The eigenvectors considered here are the usual ones, i.e.
    *right* eigenvectors (satifying *A*x = λx).

    :param int dimension: max dimension of the squared matrix
    :returns: 3 numpy.ndarray for eigenvalues, eigenvectors and real part of
              the matrix in T4 outputs (alawys real afak)
    '''
    dim = draw(integers(3, dimension))
    rdmim = draw(integers(0, (dim-1)//2))
    eivals = draw(arrays(dtype=FTYPE, shape=(rdmim), elements=floats(0, 1e-3)))
    eivals = np.append(eivals, -eivals)
    eivals = np.insert(eivals, 0, values=[0]*(dim-rdmim*2))
    ervals = draw(arrays(dtype=FTYPE, shape=(dim-rdmim), elements=floats(0, 1),
                         fill=nothing()))
    if rdmim != 0:
        ervals = np.append(ervals, ervals[-rdmim:])
    assume(ervals[0] != 0)
    evals = ervals + 1j*eivals
    evecs = draw(arrays(dtype=FTYPE, shape=(dim, dim), elements=floats(0, 1)))
    assume(np.linalg.det(evecs) != 0)
    nevecs = evecs / np.linalg.norm(evecs, axis=1).reshape(dim, 1)
    assume(np.linalg.det(nevecs) != 0)
    matrix = np.dot(np.dot(nevecs, np.diag(evals)), np.linalg.inv(nevecs))
    kijdict = draw(kij_best_estimation(evals, matrix))
    return evals, evecs, kijdict

@composite
def kij_best_estimation(draw, evals, kijmat):
    r'''Composite Hypothesis strategy to generate additional k\ :sub:`ij`
    elements appearing in Tripoli-4 listing in the k\ :sub:`eff` best
    estimation block.

    Additional elements are:

    * *left* eigenvectors, corresponding to fission source rate (satifying
      x*A* = λx)
    * standard deviation matrix, squared matrix containing positive floats
    * sensibility matrix, squared matrix containing positive floats
    * spacebins, corresponding to columns and rows of all the matrices
      (including k\ :sub:`ij` matrix)

    Spacebins can be volume numbers (so a `numpy.array` of int with (nbins,)
    as shape) or space meshes, each bin being of dimension 3 (space), so a
    `numpy.array` of shape (nbins, 3).

    :param numpy.ndarray evals: eigenvalues of k\ :sub:`ij` matrix
    :param numpy.ndarray kijmat: k\ :sub:`ij` matrix
    :returns: dictionary corresponding to parsing output with keys
              ``['estimator', 'batchs_kept', 'kij-keff', 'nbins', 'spacebins',
              'eigenvector', 'keff_KIJ_matrix', 'keff_StdDev_matrix',
              'keff_sensibility_matrix']``.
    '''
    lvals, levec = np.linalg.eig(kijmat.T)
    assume(np.allclose(np.sort(evals), np.sort(lvals)))
    stddevmat = draw(arrays(
        dtype=FTYPE, shape=kijmat.shape, elements=floats(0, 1)))
    sensibmat = draw(arrays(
        dtype=FTYPE, shape=kijmat.shape, elements=floats(0, 1)))
    ismesh = draw(booleans())
    if ismesh:
        spacebins = draw(lists(elements=tuples(integers(0, kijmat.shape[0]),
                                               integers(0, kijmat.shape[0]),
                                               integers(0, kijmat.shape[0])),
                               min_size=kijmat.shape[0],
                               max_size=kijmat.shape[0],
                               unique=True))
    else:
        spacebins = list(range(kijmat.shape[0]))
    kijdict = {'estimator': 'KIJ',
               'batchs_kept': draw(integers(80, 99)),
               'kij-keff': np.real(evals[0]),
               'nbins': evals.shape[0],
               'spacebins': np.array(spacebins),
               'eigenvector': np.real(levec[:, 0]),
               'keff_KIJ_matrix': np.real(kijmat),
               'keff_StdDev_matrix': stddevmat,
               'keff_sensibility_matrix': sensibmat}
    return kijdict

def matrix_t4_output(matrix, spacebins):
    r'''Print Tripoli-4 output in a string for matrices as in k\ :sub:`ij` case
    in k\ :sub:`eff` best estimation block.

    :param numpy.ndarray matrix: matrix to be printed
    :param numpy.ndarray spacebins: space bins corresponding to columns and
                                    rows the matrix
    :returns: string corresponding to the T4 output.
    '''
    t4out = []
    tabwidth = 16*spacebins.shape[0]
    for spacebin in spacebins:
        if isinstance(spacebin, np.ndarray):
            t4out.append(" {0:<15}".format("({0},{1},{2})".format(*spacebin)))
        else:
            t4out.append(" {0:^15}".format(spacebin))
    t4out.append("\n")
    t4out.append("{0:>24}{0:->{width}}\n".format("", width=tabwidth))
    for ilin, kij_line in enumerate(matrix):
        if isinstance(spacebins[ilin], np.ndarray):
            t4out.append("{0:>9}{1:<15}"
                         .format("", "({0},{1},{2})".format(*spacebins[ilin])))
        else:
            t4out.append("{0:>16}{1:<8}"
                         .format("", spacebins[ilin]))
        for kij_col in kij_line:
            t4out.append("| {0:<14.6e}".format(kij_col))
        t4out.append("|\n")
        t4out.append("{0:>24}{0:->{width}}\n".format("", width=tabwidth))
    return ''.join(t4out)

def kijkeff_t4_output(kijdict):
    r'''Print in a string the k\ :sub:`ij` best estimation of k\ :sub:`eff` as
    in Tripoli-4 output. This includes k\ :sub:`ij` matrix, standard deviation
    matrix and sensibility matrix.

    :param dict kijdict: k\ :sub:`ij` results stored in a dictionary
    :returns: string corresponding to the T4 output
    '''
    t4out = []
    t4out.append("{0:>10}{1} ESTIMATOR\n".format("", kijdict['estimator']))
    t4out.append("{0:>10}{1:->13}\n\n".format("", ""))
    t4out.append("{0:>12}number of last batches kept : {1}\n\n"
                 .format("", kijdict['batchs_kept']))
    t4out.append("{0:>12}kij-keff = {1:.6e}\n\n"
                 .format("", kijdict['kij-keff']))
    t4out.append("{0:>12}EIGENVECTOR :{0:>6}index{0:>6}source rate\n\n"
                 .format(""))
    for ind, ivec in enumerate(kijdict['eigenvector']):
        t4out.append("{0:>33}{1:<8}{2:.6e}\n\n".format("", ind, np.real(ivec)))
    t4out.append("\n")
    t4out.append("{0:>12}K-IJ MATRIX :\n\n".format(""))
    t4out.append("{0:>24}".format(""))
    t4out.append(matrix_t4_output(kijdict['keff_KIJ_matrix'],
                                  kijdict['spacebins']))
    t4out.append("\n\n\n")
    t4out.append("{0:>12}STANDARD DEVIATION MATRIX :\n\n".format(""))
    t4out.append("{0:>24}".format(""))
    t4out.append(matrix_t4_output(kijdict['keff_StdDev_matrix'],
                                  kijdict['spacebins']))
    t4out.append("\n\n\n")
    t4out.append("{0:>12}SENSIBILITY MATRIX :\n\n".format(""))
    t4out.append("{0:>24}".format(""))
    t4out.append(matrix_t4_output(kijdict['keff_sensibility_matrix'],
                                  kijdict['spacebins']))
    t4out.append("\n\n\n")
    return ''.join(t4out)

def extract_list_from_keff_res(keff_res, key):
    r'''Extract list for a given dictionary key in k\ :sub:`eff` result.

    Used for dictionary comparisons, especially when containing
    `numpy.ndarray`.

    :param list keff_res: k\ :sub:`eff` results as a list of dictionaries, it
                          can be a sublist of the initial list (especially when
                          k\ :sub:`ij` results are present)
    :param str key: dictionary key to match
    :returns: list of objects matching the given key
    '''
    return list(map(lambda x: x[key], keff_res))

@settings(max_examples=100)
@given(kij_res=kij_results(5), keff_res=keff_best_estimation(3))
def test_parse_kij_roundtrip(kij_res, keff_res):
    r'''Test printing k\ :sub:`ij` results as Tripoli-4 output from random
    tuples and array got from Hypothesis.

    Eigenvalues are complex in Triploi-4 output, with (afak)
    Sum(Im(eigval)) = 0, so only half of the values are generated randomly,
    other half are opposite.

    Tests performed:

    * Successful parsing (no exception raised)
    * 1 result
    * List of keys contained in the result
    * Equality (at rouding as floats and complex) of

      * Eigenvalues (complex)
      * Eigenvectors
      * Matrix
    '''
    # evals, evecs, matrix = kij_res
    evals, evecs, kijdict = kij_res
    matrix = kijdict['keff_KIJ_matrix']
    kij_t4_out = kij_t4_output(evals, evecs, matrix)
    note(kij_t4_out)
    pres = pygram.kijres.parseString(kij_t4_out)
    assert pres
    assert len(pres) == 1
    assert sorted(list(pres[0].keys())) == ['kij_eigenval', 'kij_eigenvec',
                                            'kij_matrix', 'kijdomratio',
                                            'kijmkeff_res', 'used_batch']
    assert np.allclose(pres[0]['kij_eigenval'], evals)
    assert np.allclose(pres[0]['kij_eigenvec'], evecs)
    assert np.allclose(pres[0]['kij_matrix'], matrix)
    kijkeff_t4_out = bekeff_t4_output(keff_res)
    kijkeff_t4_out = ''.join([kijkeff_t4_out, kijkeff_t4_output(kijdict)])
    pres = pygram.defkeffblock.parseString(kijkeff_t4_out)
    assert pres
    assert len(pres[0]) == len(keff_res+[kijdict]) == 4
    assert (list(map(lambda x: x['estimator'], pres[0]))
            == list(map(lambda x: x['estimator'], keff_res+[kijdict])))
    # test keff_best_estimation
    assert (extract_list_from_keff_res(pres[0][:-1], 'best_disc_batchs')
            == extract_list_from_keff_res(keff_res, 'best_disc_batchs'))
    for num in ['keff', 'sigma', 'sigma%']:
        assert (np.allclose(
            list(map(lambda x, k=num: x['bestkeffres'][k], pres[0][:-1])),
            list(map(lambda x, k=num: x['bestkeffres'][k], keff_res))))
    # test kij estimator
    keys = [tkey for tkey in list(kijdict.keys()) if tkey != 'estimator']
    for key in keys:
        assert np.allclose(pres[0][-1][key], kijdict[key])
