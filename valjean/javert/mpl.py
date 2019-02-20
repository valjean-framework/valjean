'''This module provides the classes to convert test results to matplotlib
plots.
'''

import numpy as np
import matplotlib.pyplot as plt


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
        self.fig, self.splt = plt.subplots()
        # self.the_plot = self.draw()
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
        return self.error_plot()

    def no_error_plot(self):
        '''Draw the plot if no errors are given.'''
        print("in no_error_plot")
        self.splt.set(xlabel=self.data.xname, ylabel=self.data.yname,
                      title=self.data.title)
        return self.splt.plot(self.data.bins, self.data.vals) #, 'bo-')

    def error_plot(self):
        '''Draw the plot with error bars.'''
        print("in error plot")
        self.splt.set_xlabel(self.data.xname)
        self.splt.set_ylabel(self.data.yname)
        self.splt.set_title(self.data.title)
        # return self.splt.errorbar(self.data.bins, self.data.vals,
        #                           xerr=self.data.xerrors,
        #                           yerr=self.data.yerrors,
        #                           fmt='bo-', drawstyle='steps-post')
        # self.splt.errorbar(self.data.bins[:-1], self.data.vals,
        #                    xerr=self.data.xerrors, yerr=self.data.yerrors,
        #                    fmt='-', c='limegreen', drawstyle='steps-pre',
        #                    label='-last bin, steps-pre')
        self.splt.errorbar(self.data.bins, np.append(self.data.vals, [np.nan]),
                           xerr=self.data.xerrors, yerr=self.data.yerrors,
                           fmt='b-', drawstyle='steps-post',
                           label='+ 0 end vals, steps-post')
        # self.splt.errorbar(self.data.bins[:-1], self.data.vals,
        #                    xerr=self.data.xerrors, yerr=self.data.yerrors,
        #                    fmt='y--', drawstyle='steps-mid',
        #                    label='-last bin, steps-mid')
        # self.splt.errorbar(self.data.bins[:-1], self.data.vals,
        #                    xerr=self.data.xerrors, yerr=self.data.yerrors,
        #                    fmt='r:', drawstyle='steps-post',
        #                    label='- last bin, steps-post')
        self.splt.errorbar((self.data.bins[1:] + self.data.bins[:-1])/2,
                           self.data.vals,
                           xerr=self.data.xerrors, yerr=self.data.yerrors,
                           fmt='bo', label='mid bins, only markers')
        # self.splt.errorbar((self.data.bins[1:] + self.data.bins[:-1])/2,
        #                    self.data.vals,
        #                    xerr=self.data.xerrors, yerr=self.data.yerrors,
        #                    fmt='ms', fillstyle='none', elinewidth=5,
        #                    label='mid bins, with xerror')
        self.splt.legend()

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
