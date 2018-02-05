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
from valjean.eponine.common import MeshDictBuilder

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


@settings(max_examples=10)
# @given(shape=meshshape(), sampler=data())
@given(shape=get_shape(max_dims=[1, 1, 1, 5, 5, 1, 1]), sampler=data())
def test_reversed_energy_and_time_bins(shape, sampler):
    array = sampler.draw(arrays(dtype=np.dtype([('tally', np.float),
                                                ('sigma', np.float)]),
                                shape=shape,
                                elements=tuples(floats(0, 1), floats(5, 20)),
                                fill=nothing()))
    reversed_ebins = sampler.draw(booleans())
    ebins = sorted(sampler.draw(lists(floats(0, 10),
                                      min_size=shape[3]+1, max_size=shape[3]+1,
                                      unique=True)),
                   reverse=reversed_ebins)
    reversed_tbins = sampler.draw(booleans())
    tbins = sorted(sampler.draw(lists(floats(0, 10),
                                      min_size=shape[4]+1, max_size=shape[4]+1,
                                      unique=True)),
                   reverse=reversed_tbins)
    mesh = MeshDictBuilder(['tally', 'sigma'], shape)
    mesh.bins['e'] = ebins
    mesh.bins['t'] = tbins
    mesh.arrays['default'] = array
    mesh.flip_bins()
    rdme = sampler.draw(integers(0, shape[3]-1))
    rdmt = sampler.draw(integers(0, shape[4]-1))
    if reversed_ebins:
        rdme_r = - rdme - 1
        assert np.array_equal(mesh.bins['e'], np.array(ebins)[::-1])
    else:
        rdme_r = rdme
    if reversed_tbins:
        rdmt_r = - rdmt -1
        assert np.array_equal(mesh.bins['t'], np.array(tbins)[::-1])
    else:
        rdmt_r = rdmt
    assert (array[0, 0, 0, rdme, rdmt, 0, 0]['tally']
            == mesh.arrays['default'][0, 0, 0, rdme_r, rdmt_r, 0, 0]['tally'])

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
