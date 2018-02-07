'''Tests for the :mod:`common <valjean.eponine.common>` module.'''

import numpy as np
from hypothesis import given, note, settings, assume
from hypothesis.strategies import (integers, lists, composite, sampled_from,
                                   data, one_of, tuples, shared, floats,
                                   nothing, booleans)
from hypothesis.extra.numpy import array_shapes
from hypothesis.extra.numpy import arrays
from hypothesis.extra.numpy import array_dtypes

from ..context import valjean  # noqa: F401, pylint: disable=unused-import

# pylint: disable=wrong-import-order
# pylint: disable=no-value-for-parameter
from valjean.eponine.common import (MeshDictBuilder, SpectrumDictBuilder)

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

@settings(max_examples=5)
# @given(shape=npshape(), sampler=data())
@given(shape=meshshape(), sampler=data())
def array_and_bins(shape, sampler):
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
