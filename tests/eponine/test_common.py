'''Tests for the :mod:`common <valjean.eponine.common>` module.'''

import numpy as np
from hypothesis import given, note, settings, assume
from hypothesis.strategies import (integers, lists, composite, sampled_from,
                                   data, one_of, tuples, shared, floats,
                                   nothing, booleans, just)
from hypothesis.extra.numpy import array_shapes
from hypothesis.extra.numpy import arrays
from hypothesis.extra.numpy import array_dtypes

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
# pylint: disable=no-value-for-parameter
from valjean.eponine.common import (MeshDictBuilder, SpectrumDictBuilder, FTYPE)
import valjean.eponine.pyparsing_t4.grammar as pygram
import valjean.eponine.pyparsing_t4.transform as pytrans

# , ydim=integers(0, 5), zdim=integers(0,3),
@composite
# def mesh(draw, xdim=one_of(integers(0, 5)), **kwargs):
def tmesh(draw, dim=tuples(integers(1, 5), integers(1, 5), integers(1, 3)), **kwargs):
    '''Composite Hypothesis strategy to generate Meshes.'''
    # print("xdim:", xdim)  #, "ydim:", ydim, "zdim:", zdim)
    # lst = draw(lists(xdim, **kwargs))
    shape = draw(dim) #, ydim, zdim)
    print("shape =", shape, "dim =", dim)
    nbins = int(np.prod(shape))
    print(nbins)
    spacebins = []
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                spacebins.append([x, y, z])
    corrfloats = draw(lists(floats(min_value=0), min_size=nbins, max_size=nbins))
    print(corrfloats)
    return spacebins



@composite
def testm(draw, mint=integers()):
    theints = draw(mint)
    print("the ints =", theints)
    s = integers()
    print("s = ", s)
    oint = shared(s)
    print("other int =", oint)
    return (theints, oint)


@composite
def npmesh(draw,
           arr=arrays(dtype=np.dtype([('val', np.float32), ('sig', np.float32)]),
                      shape=array_shapes(min_dims=3, max_dims=3, min_side=1, max_side=3),
                      elements=floats(0, 1))):
    myarray = draw(arr)
    print(myarray.shape)
    return myarray

@composite
def simplenpmesh(draw,
                 arr=arrays(dtype=np.float,
                            shape=array_shapes(min_dims=3, max_dims=3,
                                               min_side=1, max_side=3),
                            elements=floats(0,1))):
    myarray = draw(arr)
    print(myarray.shape)
    return myarray

@composite
def simplenpmeshWdtype(draw,
                       arr=arrays(dtype=np.dtype([('f1', np.float)]),
                                  shape=array_shapes(min_dims=3, max_dims=3,
                                                     min_side=1, max_side=3))):
    myarray = draw(arr)
    print(myarray.shape)
    return myarray

@composite
def npmeshWdtype(draw,
                 arr=arrays(dtype=np.dtype([('val', np.float), ('sig', np.float)]),
                            shape=array_shapes(min_dims=3, max_dims=3,
                                               min_side=1, max_side=3),
                            elements=tuples(floats(0,1), floats(5,20)),
                            fill=nothing())):
    myarray = draw(arr)
    print(myarray.shape)
    return myarray

@composite
def npmeshWdtypenotwork(draw,
                        arr=arrays(dtype=np.dtype([('f1', np.float)]),
                                   shape=array_shapes(min_dims=3, max_dims=3,
                                                      min_side=1, max_side=3),
                                   elements=floats(0,1))):
    myarray = draw(arr)
    print(myarray.shape)
    return myarray

@composite
def npshape(draw,
            shap=array_shapes(min_dims=3, max_dims=3, min_side=1, max_side=3)):
    myshape = draw(shap)
    return myshape

@composite
def meshshape(draw, elts=tuples(integers(1, 2), integers(1, 2), integers(1, 2),
                                integers(1, 5), integers(1, 5),
                                integers(1, 1), integers(1,1))):
    myshape = draw(elts)
    return myshape

@composite
def meshfshape(draw,
               arr=arrays(dtype=np.dtype([('val', np.float), ('sig', np.float)]),
                          shape=npshape(),
                          elements=tuples(floats(0, 1), floats(5, 20)),
                          fill=nothing())):
    myarray = draw(arr)
    return myarray

@composite
def get_shape(draw, max_dims=[3, 3, 3, 5, 5, 1, 1]):
    mytuple = draw(tuples(integers(1, max_dims[0]),   # s0
                          integers(1, max_dims[1]),   # s1
                          integers(1, max_dims[2]),   # s2
                          integers(1, max_dims[3]),   # e
                          integers(1, max_dims[4]),   # t
                          integers(1, max_dims[5]),   # mu
                          integers(1, max_dims[6])))  # phi
    return mytuple

# # not working...
# @composite
# @given(shap=npshape())
# def array_and_bins(draw, shap,
#                    arr=arrays(dtype=np.dtype([('val', np.float), ('sig', np.float)]),
#                               shape=shap,
#                               elements=tuples(floats(0,1), floats(5,20)),
#                               fill=nothing())):
#     myarray = draw(arr)
#     return myarray

@settings(max_examples=5)
@given(array=meshfshape(), sampler=data())
def gen_bins(array, sampler):
    print(array)
    ns0bins = array.shape[0]
    ns1bins = array.shape[1]
    ns2bins = array.shape[2]
    print("shape =", array.shape,
          "ns0 =", ns0bins, "ns1 =", ns1bins, "ns2 =", ns2bins)
    s0bins = sampler.draw(lists(floats(0, 10),
                                min_size=ns0bins+1, max_size=ns0bins+1)
                          .map(sorted))
    s1bins = sampler.draw(lists(floats(0, 10),
                                min_size=ns1bins+1, max_size=ns1bins+1)
                          .map(sorted))
    s2bins = sorted(sampler.draw(lists(floats(0, 10),
                                       min_size=ns2bins+1,
                                       max_size=ns2bins+1)),
                    reverse=True)
    assume(s0bins[0] != s0bins[1])
    assume(s1bins[0] != s1bins[1])
    assume(s2bins[0] != s2bins[1])
    assert len(s0bins) == ns0bins+1
    assert len(s1bins) == array.shape[1]+1
    assert s2bins[0] > s2bins[1]
    # return s0bins

@composite
def array_and_bins(draw, dtype,
                   max_dim=(3, 3, 3, 5, 5, 1, 1),
                   elements=tuples(floats(0, 1.), floats(0., 100.)),
                   reverse=booleans()):
    shape = draw(get_shape(max_dim))
    print("shape:", shape)
    array = draw(arrays(dtype=dtype, shape=shape, elements=elements,
                        fill=nothing()))
    print("array:", array.squeeze())
    bins = {}
    bins['e'] = draw(get_bins(elements=floats(0, 20), nbins=shape[3],
                              revers=reverse))
    # if shape[4] > 1:
    #     print("shape[4] =", shape[4], " > 1 ?")
    bins['t'] = draw(get_bins(elements=floats(0, 10), nbins=shape[4],
                              revers=reverse))
    # if shape[5] > 1:
    bins['mu'] = draw(get_bins(elements=floats(-1., 1.), nbins=shape[5],
                               revers=reverse))
    # if shape[6] > 1:
    bins['phi'] = draw(get_bins(elements=floats(0, 2*np.pi),
                                nbins=shape[6], revers=reverse))
    print(bins)
    return array, bins

@settings(max_examples=5)
# @given(shape=npshape(), sampler=data())
@given(shape=meshshape(), sampler=data())
def check_array_and_bins(shape, sampler):
    array = sampler.draw(arrays(dtype=np.dtype([('tally', np.float),
                                                ('sigma', np.float)]),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(5, 20)),
                                fill=nothing()))
    ebins = sorted(sampler.draw(lists(floats(0, 10),
                                      min_size=shape[3]+1, max_size=shape[3]+1,
                                      unique=True)),
                   reverse=True)
    tbins = sorted(sampler.draw(lists(floats(0, 10),
                                      min_size=shape[4]+1, max_size=shape[4]+1,
                                      unique=True)))
    # if array.shape == (1, 1, 1, 2, 1, 1, 1):
    #     assume(array[0,0,0,0,0,0,0]['tally'] != array[0,0,0,1,0,0,0]['tally'])
    print("shape:", shape)
    print("array:", array.squeeze())
    print("bins:", ebins, tbins)
    assert len(ebins) == array.shape[3]+1
    mesh = MeshDictBuilder(['tally', 'sigma'], shape)
    mesh.bins['e'] = ebins
    mesh.bins['t'] = tbins
    mesh.arrays['default'] = array
    print("mesh arrays['default'] =", mesh.arrays['default'].squeeze())
    print("values:", mesh.arrays['default'][:,:,:,:,0,:]['tally'].squeeze())
    print("values:", mesh.arrays['default'][...,0,:,:]['tally'].squeeze())
    print("avec squeeze:", mesh.arrays['default'][0,0,0,:,0,0]['tally'].squeeze())
    print("avec ravel:", mesh.arrays['default'][0,0,0,:,0,0]['tally'].ravel())
    bf_flip = mesh.arrays['default'][0,0,0,:,0,0]['tally'].ravel()
    print("values:", bf_flip)
    mesh.flip_bins()
    print("bins after flip:")
    print(mesh.bins)
    print("mesh arrays['default'] =", mesh.arrays['default'].squeeze())
    af_flip = mesh.arrays['default'][0,0,0,:,0,0]['tally'].ravel()
    print("values:", af_flip)
    print("type af_flip =", type(af_flip))
    print(shape)
    # if shape[3] > 1:
    #     print("autre sens:", af_flip[::-1])
    assert np.array_equal(af_flip[::-1], bf_flip)


@composite
def get_bins(draw, elements=floats(0, 10), nbins=1, revers=booleans()):
    '''Choose the (energy, time, mu or phi) bins and their order (reversed or
    not) thanks to hypothesis.

    Edges for the bins can be chosen to get more realistic cases.
    '''
    mybins = sorted(draw(lists(elements, min_size=nbins+1,
                               max_size=nbins+1, unique=True)),
                    reverse=draw(revers))
    return mybins

def compare_bin_order(ibins, fbins, irdm, rev_rdm):
    '''Compare bins orders between flipped bins using
    :mod:`valjean.eponine.common` and bins array read in reversed order.
    Modify value of the reversed random index to match the correct element.
    '''
    if ibins[0] > ibins[1]:
        rev_rdm[irdm] = - rev_rdm[irdm] - 1
        assert np.array_equal(fbins, ibins[::-1])

@settings(max_examples=10)
@given(shape=get_shape(max_dims=[3, 3, 3, 5, 5, 1, 1]), sampler=data())
def test_flip_mesh(shape, sampler):
    '''Test flipping mesh.

    Generate with hypothesis a mesh with max dimensions
    [s0, s1, s2, E, t, mu, phi] = [3, 3, 3, 5, 5, 1, 1]
    as no mu or phi bins available for the moment for meshes.

    Generate energy and time binnings. They can be increasing or decreasing
    depending on the value of the boolean chosen by hypothesis in order to
    test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    array = sampler.draw(arrays(dtype=np.dtype([('tally', np.float),
                                                ('sigma', np.float)]),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(5, 20)),
                                fill=nothing()))
    ebins = sampler.draw(get_bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(get_bins(elements=floats(0, 10), nbins=shape[4]))
    mesh = MeshDictBuilder(['tally', 'sigma'], shape)
    mesh.bins['e'] = ebins
    mesh.bins['t'] = tbins
    mesh.arrays['default'] = array
    mesh.flip_bins()
    rdm = sampler.draw(tuples(integers(0, shape[0]-1),
                              integers(0, shape[1]-1),
                              integers(0, shape[2]-1),
                              integers(0, shape[3]-1),
                              integers(0, shape[4]-1)))
    rdm_r = list(rdm)
    compare_bin_order(np.array(ebins), mesh.bins['e'], 3, rdm_r)
    compare_bin_order(np.array(tbins), mesh.bins['t'], 4, rdm_r)
    index = rdm + (0, 0)
    findex = tuple(rdm_r) + (0, 0)
    assert array[index]['tally'] == mesh.arrays['default'][findex]['tally']

@settings(max_examples=5)
@given(shape=get_shape(max_dims=[1, 1, 1, 5, 5, 3, 3]),
       sampler=data())
def test_flip_spectrum(shape, sampler):
    '''Test flipping spectrum.

    Generate with hypothesis a mesh with max dimensions
    [s0, s1, s2, E, t, mu, phi] = [1, 1, 1, 5, 5, 3, 3].

    Generate energy, time, mu and phi angle binnings. They can be increasing or
    decreasing depending on the value of the boolean chosen by hypothesis in
    order to test all combinations.

    Flip bins if necessary and check if they were correctly flipped.
    '''
    array = sampler.draw(
        arrays(dtype=np.dtype([('score', np.float),
                               ('sigma', np.float),
                               ('score/lethargy', np.float)]),
               shape=shape,
               elements=tuples(floats(0, 1), floats(5, 20), floats(0, 1)),
               fill=nothing()))
    ebins = sampler.draw(get_bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(get_bins(elements=floats(0, 10), nbins=shape[4]))
    mubins = sampler.draw(get_bins(elements=floats(-1., 1.), nbins=shape[5]))
    phibins = sampler.draw(get_bins(elements=floats(0, 2*np.pi),
                                    nbins=shape[6]))
    spectrum = SpectrumDictBuilder(['score', 'sigma', 'score/lethargy'], shape)
    spectrum.bins = {'e': ebins, 't': tbins, 'mu': mubins, 'phi': phibins}
    spectrum.arrays['default'] = array
    spectrum.flip_bins()
    rdm = sampler.draw(tuples(integers(0, shape[3]-1),
                              integers(0, shape[4]-1),
                              integers(0, shape[5]-1),
                              integers(0, shape[6]-1)))
    rdm_r = list(rdm)
    compare_bin_order(np.array(ebins), spectrum.bins['e'], 0, rdm_r)
    compare_bin_order(np.array(tbins), spectrum.bins['t'], 1, rdm_r)
    compare_bin_order(np.array(mubins), spectrum.bins['mu'], 2, rdm_r)
    compare_bin_order(np.array(phibins), spectrum.bins['phi'], 3, rdm_r)
    index = (0, 0, 0) + rdm
    findex = (0, 0, 0) + tuple(rdm_r)
    assert array[index]['score'] == spectrum.arrays['default'][findex]['score']

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

@settings(max_examples=10)
@given(shape=get_shape(max_dims=[3, 3, 3, 3, 3, 1, 1]), sampler=data())
def test_print_parse_mesh(shape, sampler):
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
    these dimensions to 3 (from few runs).
    '''
    array = sampler.draw(arrays(dtype=np.dtype([('tally', FTYPE),
                                                ('sigma', FTYPE)]),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(0, 100)),
                                fill=nothing()))
    print("shape:", shape)
    ebins = sampler.draw(get_bins(elements=floats(0, 20), nbins=shape[3]))
    tbins = sampler.draw(get_bins(elements=floats(0, 10), nbins=shape[4]))
    mesh_str = make_mesh_t4_output(array, ebins, tbins)
    pres = pygram.scoreblock.parseString(mesh_str)
    if pres:
        oebins = ebins if ebins[0] < ebins[1] else ebins[::-1]
        otbins = tbins if tbins[0] < tbins[1] else tbins[::-1]
        assert np.allclose(pres[0]['mesh_res']['ebins'], np.array(oebins))
        if len(otbins) > 2:
            assert np.allclose(pres[0]['mesh_res']['tbins'], np.array(otbins))
        assert array.dtype == pres[0]['mesh_res']['mesh'].dtype
        assert array.shape == pres[0]['mesh_res']['mesh'].shape
        if np.array_equal(oebins, ebins) and np.array_equal(otbins, tbins):
            assert np.allclose(array[:]['tally'],
                               pres[0]['mesh_res']['mesh'][:]['tally'])
            assert np.allclose(array[:]['sigma'],
                               pres[0]['mesh_res']['mesh'][:]['sigma'])


def spectrum_score_str():
    '''Example of score preceeding spectrum results, including units.'''
    specscore_str = ('''
         scoring mode : SCORE_SURF
         scoring zone :          Frontier        volumes : 2,1

''')
    return specscore_str


#     '''
#          SPECTRUM RESULTS
#          number of first discarded batches : 0

#          group                   score           sigma_%         score/lethargy
# ''')
#     if units:
#         specscore_str += ('''\
# Units:   MeV                     neut.s^-1       %               neut.s^-1
# ''')
#     print(specscore_str)

def build_spectrum_str(spectrum, ebins, tbin, mubin, phibin, units=False):
    t4out = []
    spec_str =('''\
         SPECTRUM RESULTS
         number of first discarded batches : 0

         group                   score           sigma_%         score/lethargy
''')
    if units:
        spec_str += ('''\
Units:   MeV                     neut.s^-1       %               neut.s^-1
''')
    t4out.append(spec_str)
    for iebin in range(len(ebins)-1):
        index = (0, 0, 0, iebin, tbin, mubin, phibin)
        t4out.append("{0:.6e} - {1:.6e} \t {2:.6e} \t {3:.6e} \t {4:.6e}\n"
                     .format(ebins[iebin], ebins[iebin+1],
                             spectrum[index]['score'],
                             spectrum[index]['sigma'],
                             spectrum[index]['score/lethargy']))
    t4out.append("\n")
    return ''.join(t4out)

def time_step_str(itbin, tbins):
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

def make_spectrum_t4_output(spectrum, bins, units):
    t4out = []
    t4out.append(spectrum_score_str())
    t4out.append("\n")
    print("spectrum shape =", spectrum.shape)
    # if 't' in bins:
    for itbin in range(len(bins['t'])-1):
        if len(bins['t']) > 2:
            t4out.append(time_step_str(itbin, bins['t']))
        for imubin in range(len(bins['mu'])-1):
            if len(bins['mu']) > 2 or len(bins['phi']) > 2:
                t4out.append(mu_angle_str(imubin, bins['mu']))
            for iphibin in range(len(bins['phi'])-1):
                if len(bins['phi']) > 2:
                    t4out.append(phi_angle_str(iphibin, bins['phi']))
                t4out.append(build_spectrum_str(spectrum, bins['e'], itbin, imubin, iphibin, units))
    # else:
    #     t4out.append(build_spectrum_str(spectrum, bins['e'], 0, 0, 0, units))
    return ''.join(t4out)

def reverse_bins(bins):
    rbins = bins
    for key in bins:
        if bins[key][0] > bins[key][1]:
            rbins[key] = bins[key][::-1]
    return rbins

def compare_bins(bins, spectrum_res):
    print("bins:", bins)
    print("spectrum keys =", list(spectrum_res.keys()))
    for key in bins:
        # if len(gen_bins[key]) > 2 or key == 'e':
        # if key == 'e' or key == 't':
        if key+'bins' in spectrum_res:
            assert np.allclose(spectrum_res[key+'bins'],
                               np.array(bins[key]))
        else:
            print("other key:", key)

@settings(max_examples=10)
@given(sampler=data())
def test_print_parse_spectrum(sampler):
    array, bins = sampler.draw(array_and_bins(
        dtype=np.dtype([('score', FTYPE), ('sigma', FTYPE),
                        ('score/lethargy', FTYPE)]),
        max_dim=(1, 1, 1, 3, 3, 2, 2),
        elements=tuples(floats(0, 1), floats(0, 100), floats(0, 1)),
        reverse=just(False)))
    print("array:", array.squeeze(), "bins:", bins)
    units = sampler.draw(booleans())
    spectrum_str = make_spectrum_t4_output(array, bins, units)
    print(spectrum_str)
    pres = pygram.scoreblock.parseString(spectrum_str)
    if pres:
        print("Test bins")
        # obins = reverse_bins(bins)
        # assert np.allclose(pres[0]['spectrum_res']['ebins'],
        #                    np.array(obins['e']))
        # compare_bins(obins, pres[0]['spectrum_res'])
        compare_bins(bins, pres[0]['spectrum_res'])
        # if len(otbins) > 2:
    #         assert np.allclose(pres[0]['mesh_res']['tbins'], np.array(otbins))
        assert array.dtype == pres[0]['spectrum_res']['spectrum'].dtype
        assert array.shape == pres[0]['spectrum_res']['spectrum'].shape
        #     if np.array_equal(oebins, ebins) and np.array_equal(otbins, tbins):
        assert np.allclose(array[:]['score'],
                           pres[0]['spectrum_res']['spectrum'][:]['score'])
        assert np.allclose(array[:]['sigma'],
                           pres[0]['spectrum_res']['spectrum'][:]['sigma'])
        assert np.allclose(array[:]['score/lethargy'],
                           pres[0]['spectrum_res']['spectrum'][:]['score/lethargy'])
@composite
def simplearray(draw,
                arr=arrays(dtype=np.float, shape=3, elements=floats(0,1))):
    thearray = draw(arr)
    return thearray

@composite
def handmadearray(draw,
                  shap=array_shapes(min_dims=3, max_dims=3, min_side=1, max_side=3)):
    myshape = draw(shap)
    mydtype = np.dtype([('val', np.float), ('sig', np.float)])
    myarray = np.empty(myshape, mydtype)
    print(myarray.shape)
    return myarray
