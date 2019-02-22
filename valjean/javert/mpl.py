'''This module provides the classes to convert test results to matplotlib
plots.
'''

import numpy as np
import matplotlib.pyplot as plt
from .. import LOGGER


class Mpl:
    '''I don't know if this will be necessary, cc from Rst.py...'''


class MplPlot:
    '''Convert a :class:`~.items.PlotItem` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.items.PlotItem`..

        :param data: the data to convert.
        :type data: :class:`~.items.PlotItem`
        '''
        self.data = data
        self.nb_splts = (len(set(d.yname for d in self.data))
                         if isinstance(self.data, list)
                         else 1)
        self.fig, self.splt = plt.subplots(
            self.nb_splts, sharex=True,
            figsize=(6.4, 4.8+1.2*(self.nb_splts-1)),
            gridspec_kw={'height_ratios': [4] + [1]*(self.nb_splts-1),
                         'hspace': 0.05})
        self.legend = {'handles': [], 'labels': []}
        self.draw()

    def draw(self):
        '''Draw the plot.'''
        # if self.data.title == 'pie':
        #     return self.pie()
        # if self.data.title == 'scatter':
        #     return self.scatter()
        # if self.data.title == 'plot':
        #     return self.no_error_plot()
        # if self.data.xerrors is None and self.data.yerrors is None:
        #     return self.step_plot()
        if not isinstance(self.data, list):
            return self.error_plot()
        return self.multiple_error_plots()

    def no_error_plot(self):
        '''Draw the plot if no errors are given.'''
        print("in no_error_plot")
        self.splt.set(xlabel=self.data.xname, ylabel=self.data.yname,
                      title=self.data.title)
        return self.splt.plot(self.data.bins, self.data.vals) #, 'bo-')

    def error_plot(self):
        '''Draw the plot with error bars.

        WORKS WHEN ONLY ONE CURVE TO DRAW ON GRAPH.
        Line not needed in that case for the case N(bins) = N(vals)
        '''
        LOGGER.debug("in error plot")
        self.splt.set_xlabel(self.data.xname)
        self.splt.set_ylabel(self.data.yname)
        if self.data.bins.size == self.data.vals.size+1:
            steps = self.splt.errorbar(self.data.bins,
                                       np.append(self.data.vals, [np.nan]),
                                       fmt='b-', drawstyle='steps-post')
            marker = self.splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                self.data.vals, xerr=self.data.xerrors, yerr=self.data.yerrors,
                fmt='bo')
            plt.legend((steps, marker), self.data.label)
        else:
            self.splt.errorbar(self.data.bins, self.data.vals,
                               xerr=self.data.xerrors, yerr=self.data.yerrors,
                               fmt='bo', label=self.data.label)
            plt.legend()

    def ierror_plot(self, idata, iplot):
        '''Draw the plot with error bars.
        '''
        LOGGER.debug("in ierror plot for plot %d on subplot %d", idata, iplot)
        if iplot == self.nb_splts-1:
            self.splt[iplot].set_xlabel(self.data[idata].xname)
        self.splt[iplot].set_ylabel(self.data[idata].yname)
        col = 'C'+str(idata) if iplot == 0 else 'k'
        if self.data[idata].bins.size == self.data[idata].vals.size+1:
            steps = self.splt[iplot].errorbar(
                self.data[idata].bins,
                np.append(self.data[idata].vals, [np.nan]),
                fmt=col+'-', drawstyle='steps-post')
            markers = self.splt[iplot].errorbar(
                (self.data[idata].bins[1:] + self.data[idata].bins[:-1])/2,
                self.data[idata].vals,
                xerr=self.data[idata].xerrors, yerr=self.data[idata].yerrors,
                fmt=col+'o')
            if iplot == 0:
                self.legend['handles'].append((steps, markers))
                self.legend['labels'].append(self.data[idata].label)
        else:
            eplt = self.splt[iplot].errorbar(
                self.data[idata].bins, self.data[idata].vals,
                xerr=self.data[idata].xerrors, yerr=self.data[idata].yerrors,
                fmt=col+'o--')
            if iplot == 0:
                self.legend['handles'].append(eplt)
                self.legend['labels'].append(self.data[idata].label)

    def multiple_error_plots(self):
        '''Plot errorbar plot when more than one curve are available.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        ynames = ()
        if len(self.data) > 10:
            LOGGER.warning("This method only accepts up to 10 sets of data"
                           "on the same plot (color numbering issue).")
            return
        for ipli, pli in enumerate(self.data):
            if pli.yname not in ynames:
                ynames = ynames + (pli.yname,)
            self.ierror_plot(ipli, ynames.index(pli.yname))
        self.splt[0].legend(self.legend['handles'], self.legend['labels'])

    def step_plot(self):
        print("step plot")
        self.splt.set_xlabel(self.data.xname)
        self.splt.set_ylabel(self.data.yname)
        self.splt.set_title(self.data.title)
        return self.splt.errorbar(self.data.bins, self.data.vals) #,
                                  #fmt='bo-', drawstyle='steps-mid')

    def pie(self):
        print('une tarte, enfin un camembert en bon français !')
        return self.splt.pie(self.data.vals)

    def scatter(self):
        print('scatter plot')
        return self.splt.scatter(self.data.bins, self.data.vals)

    @staticmethod
    def show():
        '''Show the plot in a popup window.'''
        plt.show()

    def save(self, name='fig.png'):
        '''Save the plot under the given name.'''
        self.fig.savefig(name)

    @staticmethod
    def plt():
        return plt


class MplPlot2:
    '''Convert a :class:`~.items.FullPlotItem` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.items.PlotItem`..

        :param data: the data to convert.
        :type data: :class:`~.items.FullPlotItem`
        '''
        self.data = data
        self.nb_splts = len(set(self.data.ynames))
        self.fig, self.splt = plt.subplots(
            self.nb_splts, sharex=True,
            figsize=(6.4, 4.8+1.2*(self.nb_splts-1)),
            gridspec_kw={'height_ratios': [4] + [1]*(self.nb_splts-1),
                         'hspace': 0.05})
        self.legend = {'handles': [], 'labels': []}
        self.draw()

    def draw(self):
        '''Draw method.'''
        if len(self.data.values) == 1:
            return self.error_plot()
        return self.multiple_error_plots()

    def error_plot(self):
        '''Draw the plot with error bars.

        WORKS WHEN ONLY ONE CURVE TO DRAW ON GRAPH.
        Line not needed in that case for the case N(bins) = N(vals)
        '''
        LOGGER.debug("in error plot")
        self.splt.set_xlabel(self.data.xname)
        self.splt.set_ylabel(self.data.ynames[0])
        if self.data.bins.size == self.data.values[0].size+1:
            self.splt.errorbar(
                self.data.bins, np.append(self.data.values[0], [np.nan]),
                fmt='b-', drawstyle='steps-post')
            self.splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                self.data.values[0], yerr=self.data.errors[0],
                fmt='bo')
            # plt.legend((steps, marker), self.data.labels[0])
        else:
            self.splt.errorbar(self.data.bins, self.data.values[0],
                               yerr=self.data.errors[0],
                               fmt='bo', label=self.data.labels[0])
            # plt.legend()

    def ierror_plot(self, idata, iplot):
        '''Draw the plot with error bars.
        '''
        LOGGER.debug("in ierror plot for plot %d on subplot %d", idata, iplot)
        splt = self.splt if self.nb_splts == 1 else self.splt[iplot]
        if iplot == self.nb_splts-1:
            splt.set_xlabel(self.data.xname)
        splt.set_ylabel(self.data.ynames[idata])
        col = 'C'+str(idata) if iplot == 0 else 'k'
        if self.data.bins.size == self.data.values[idata].size+1:
            steps = splt.errorbar(
                self.data.bins,
                np.append(self.data.values[idata], [np.nan]),
                fmt=col+'-', drawstyle='steps-post')
            markers = splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                self.data.values[idata],
                yerr=self.data.errors[idata],
                fmt=col+'o')
            if iplot == 0:
                self.legend['handles'].append((steps, markers))
                self.legend['labels'].append(self.data.labels[idata])
        else:
            eplt = splt.errorbar(
                self.data.bins, self.data.values[idata],
                yerr=self.data.errors[idata],
                fmt=col+'o--')
            if iplot == 0:
                self.legend['handles'].append(eplt)
                self.legend['labels'].append(self.data.labels[idata])

    def multiple_error_plots(self):
        '''Plot errorbar plot when more than one curve are available.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        ynames = ()
        if len(self.data.values) > 10:
            LOGGER.warning("This method only accepts up to 10 sets of data"
                           "on the same plot (color numbering issue).")
            return
        for iplt, yax in enumerate(self.data.ynames):
            if yax not in ynames:
                ynames = ynames + (yax,)
            self.ierror_plot(iplt, ynames.index(yax))
        if self.nb_splts == 1:
            self.splt.legend(self.legend['handles'], self.legend['labels'])
        else:
            self.splt[0].legend(self.legend['handles'], self.legend['labels'])

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
