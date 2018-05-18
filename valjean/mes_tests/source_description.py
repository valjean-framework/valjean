'''Closer look at sources properties.'''

# pylint: disable=invalid-name

from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def read_file(tfile):
    '''Read the file, each line corresponding to:
    x, y, z, ox, oy, oz, energy, simulation_weight, sid, pid, time, mxs,
    nbcoll, parttype, status, cellid (cf. file *general).'''
    dtype = np.dtype({
        'names': ['x', 'y', 'z', 'ox', 'oy', 'oz', 'energy',
                  'simulation_weight', 'sid', 'pid', 'time', 'mxs', 'nbcoll',
                  'parttype', 'status', 'cellid'],
        'formats': [np.float32] * 16})
    print(dtype)
    table = []
    # nptab = np.empty((1), dtype=dtype)
    lfiles = glob(tfile)
    for tfil in lfiles:
        with open(tfil) as fil:
            for line in fil:
                # print([eval(x) for x in line.split()])
                # table.append([eval(x) for x in line.split()])
                ttupel = [eval(x) for x in line.split()]
                table.append(np.array(tuple(ttupel), dtype=dtype))
    table = np.array(table)
    return table

def draw_plot_for_var(ltable, var, unit=None, nbins=None, const=1, fit=None):
    plt.figure(1)
    n, bins, patches = plt.hist(ltable[:][var]*const, bins=nbins, density=1)
    print(ltable.shape)
    if fit:
        mu, sigma = stats.norm.fit(ltable[:][var]*const)
        print(mu, sigma)
        pdf_hist = stats.norm.pdf(bins, mu, sigma)
        plt.plot(bins, pdf_hist, 'r--', label='Fit')
        pdf_hist4ns = stats.norm.pdf(bins, 0, fit)
        plt.plot(bins, pdf_hist4ns, '--', c='limegreen',
                 label=r'$\sigma$ = {0} ns'.format(fit))
        pdf_hist4ns_fwhm = stats.norm.pdf(bins, 0, fit/(2*np.sqrt(2*np.log(2))))
        plt.plot(bins, pdf_hist4ns_fwhm, '--', c='lightblue',
                 label='FWHM = {0} ns'.format(fit))
    plt.xlabel("{0} [{1}]".format(var, unit))
    plt.legend()
    plt.show()
