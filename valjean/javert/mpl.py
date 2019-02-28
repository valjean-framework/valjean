'''This module provides the classes to convert test results to plots using
:mod:`matplotlib.pyplot`.
'''

from collections import OrderedDict
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
from .. import LOGGER


COLORS = ['k', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
MARKERS_SHAPE = ['o', 'o', 's', 's', 'D', 'D', 'H', 'H', 'X', 'X', 'h', 'h',
                 'P', 'P', '8', '8']
MARKERS_FILL = ['full', 'none']


class MplPlot:
    '''Convert a :class:`~.items.PlotItem` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.items.PlotItem`..

        :param data: the data to convert.
        :type data: :class:`~.items.PlotItem`
        '''
        self.plt_format = (cycle(COLORS), cycle(MARKERS_SHAPE),
                           cycle(MARKERS_FILL))
        self.data = data
        self.nb_splts = len(set(c.yname for c in self.data.curves))
        self.fig, self.splt = plt.subplots(
            self.nb_splts, sharex=True,
            figsize=(6.4, 4.8+1.2*(self.nb_splts-1)),
            gridspec_kw={'height_ratios': [4] + [1]*(self.nb_splts-1),
                         'hspace': 0.05})
        self.legend = {'handles': [], 'labels': [], 'iplot': []}
        self.draw()

    def draw(self):
        '''Draw method.'''
        if len(self.data.curves) == 1:
            return self.error_plot()
        return self.multiple_error_plots()

    def error_plot(self):
        '''Draw the plot with error bars.

        WORKS WHEN ONLY ONE CURVE TO DRAW ON GRAPH.
        Line not needed in that case for the case N(bins) = N(vals)
        '''
        LOGGER.debug("in error plot")
        self.splt.set_xlabel(self.data.xname)
        self.splt.set_ylabel(self.data.curves[0].yname)
        if self.data.bins.size == self.data.curves[0].values.size+1:
            steps = self.splt.errorbar(
                self.data.bins,
                np.append(self.data.curves[0].values, [np.nan]),
                fmt='b-', drawstyle='steps-post')
            marker = self.splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                self.data.curves[0].values, yerr=self.data.curves[0].errors,
                fmt='bo')
            plt.legend((steps, marker), self.data.curves[0].label)
        else:
            self.splt.errorbar(self.data.bins, self.data.curves[0].values,
                               yerr=self.data.curves[0].errors,
                               fmt='bo', label=self.data.curves[0].label)
            plt.legend()

    def ierror_plot(self, idata, iplot, data_fmt):
        '''Draw the plot with error bars.

        .. todo::

            Colors are probably not completely adjusted, this will be checked
            when more curves will be given from a single test.
        '''
        LOGGER.debug("in ierror plot for plot %d on subplot %d", idata, iplot)
        splt = self.splt if self.nb_splts == 1 else self.splt[iplot]
        if iplot == self.nb_splts-1:
            splt.set_xlabel(self.data.xname)
        splt.set_ylabel(self.data.curves[idata].yname)
        if self.data.bins.size == self.data.curves[idata].values.size+1:
            steps = splt.errorbar(
                self.data.bins,
                np.append(self.data.curves[idata].values, [np.nan]),
                linestyle='-', color=data_fmt[0], drawstyle='steps-post')
            markers = splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                self.data.curves[idata].values,
                yerr=self.data.curves[idata].errors,
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2],
                linestyle='')
            self.legend['handles'].append((steps, markers))
            self.legend['labels'].append(self.data.curves[idata].label)
            self.legend['iplot'].append(iplot)
        else:
            eplt = splt.errorbar(
                self.data.bins, self.data.curves[idata].values,
                yerr=self.data.curves[idata].errors, linestyle='--',
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2])
            self.legend['handles'].append(eplt)
            self.legend['labels'].append(self.data.curves[idata].label)
            self.legend['iplot'].append(iplot)

    def multiple_error_plots(self):
        '''Plot errorbar plot when more than one curve are available.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        ynames = OrderedDict()
        iplt_format = tuple(next(pf) for pf in self.plt_format)
        if len(self.data.curves) > 10:
            LOGGER.warning("This method only accepts up to 10 sets of data"
                           "on the same plot (color numbering issue).")
            return
        for iplt, yax in enumerate([c.yname for c in self.data.curves]):
            if yax not in ynames:
                ynames[yax] = 0
            else:
                ynames[yax] += 1
                if list(ynames.keys()).index(yax) == 0:
                    iplt_format = tuple(next(pf) for pf in self.plt_format)
            self.ierror_plot(iplt, list(ynames.keys()).index(yax), iplt_format)
        self._build_legend(ynames)

    def _build_legend(self, ynames):
        '''Build the legends from self.legend and add them to the figures.

        :param ynames: available y-axis names
        '''
        if self.nb_splts == 1:
            self.splt.legend(self.legend['handles'], self.legend['labels'])
        else:
            for iyax, nplt in enumerate(ynames.values()):
                if nplt > 0:
                    self.splt[iyax].legend(
                        [h for i, h in enumerate(self.legend['handles'])
                         if self.legend['iplot'][i] == iyax],
                        [l for i, l in enumerate(self.legend['labels'])
                         if self.legend['iplot'][i] == iyax])

    @staticmethod
    def show():
        '''Show the plot in a popup window.'''
        plt.show()

    def save(self, name='fig.png'):
        '''Save the plot under the given name.'''
        self.fig.savefig(name)

    @staticmethod
    def plt():
        '''Return the matplotlib instance.'''
        return plt
