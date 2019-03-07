'''This module provides the classes to convert test results to plots using
:mod:`matplotlib.pyplot`.


:class:`MplPlot` objects take as input :class:`~.items.PlotItem` containing at
minima values and bins.

The format, or rendering, of the plot can be set using the rcParams but also
some predefined parameters on which the class cycle like colors, markers shape
and filling.

Per default the first color is black and only used for reference. The cycle on
colors excludes the reference color.

Plots can be obtained with the following for example:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.items import PlotItem, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins*0.5*(icurve+1),
    ...                                  label=str(icurve+1)))
    >>> pltit = PlotItem(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert.mpl import MplPlot
    >>> mplplt = MplPlot(pltit)

This example also show the default colors and markers used.


It is possible to change the general style of plots using a predefined one
or to use different markers. The predefined styles can be obtained thanks to

>>> import matplotlib.pyplot as plt  # doctest: +SKIP
>>> print(plt.style.available)  # doctest: +SKIP

For example, we can have:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.items import PlotItem, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins*0.5*(icurve+1),
    ...                                  label=str(icurve+1)))
    >>> pltit = PlotItem(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert import mpl
    >>> mpl.STYLE = 'Solarize_Light2'
    >>> mplplt = mpl.MplPlot(pltit)


Colors and markers can also be changed directly:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.items import PlotItem, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins*0.5*(icurve+1),
    ...                                  label=str(icurve+1)))
    >>> pltit = PlotItem(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert import mpl
    >>> mpl.STYLE = 'default'  # needed here as persistent from above
    >>> mpl.COLORS = ['b', 'g', 'r', 'y', 'm']
    >>> mpl.MARKERS_SHAPE = ['X', '+', 'D', '1', 'p', 'v', 'o']
    >>> mpl.MARKERS_FILL = ['top', 'full', 'right', 'none', 'bottom', 'left',
    ...                     'none']
    >>> mplplt = mpl.MplPlot(pltit)

'''
from collections import OrderedDict
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt
from .. import LOGGER


COLORS = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
MARKERS_SHAPE = ['s', 's', 'H', 'H', 'D', 'D', 'o', 'o', 'X', 'X', 'h', 'h',
                 'P', 'P', '8', '8']
MARKERS_FILL = ['full', 'none']
STYLE = 'default'


class MplPlot:
    '''Convert a :class:`~.items.PlotItem` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.items.PlotItem`..

        :param data: the data to convert.
        :type data: :class:`~.items.PlotItem`
        '''
        plt.style.use(STYLE)
        self.curve_format = (cycle(COLORS), cycle(MARKERS_SHAPE),
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

        .. warning::

            WORKS WHEN ONLY ONE CURVE TO DRAW ON GRAPH.

        Line not represented in the case N(bins) = N(vals) (no steps).
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
            if self.data.curves[0].label:
                plt.legend()

    def ierror_plot(self, idata, iplot, data_fmt):
        '''Draw the plot with error bars on the plot (update the plot)

        :param int idata: index of the data curve in the curves list
        :param int iplot: index of the subplot (chosen according y-axis name)
        :param tuple(str) data_fmt: data format tuple,
            i.e. (color, marker shape, marker filling)
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
        '''Plot errorbar plot when more than one curve are available (update
        the pyplot instance). Also build the legend.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        ynames = OrderedDict()
        icv_format = ('k', 'o', 'full')
        for icv, yax in enumerate([c.yname for c in self.data.curves]):
            if yax not in ynames:
                ynames[yax] = 0
            else:
                ynames[yax] += 1
                if list(ynames.keys()).index(yax) == 0:
                    icv_format = tuple(next(pf) for pf in self.curve_format)
            self.ierror_plot(icv, list(ynames.keys()).index(yax), icv_format)
        self._build_legend(ynames)

    def _build_legend(self, ynames):
        '''Build the legends from self.legend and add them to the figures.

        An automatic number of columns is calculated, depending on the number
        of curves to be plotted on each subplot. It has been decided to add a
        new columns each 5 curves.

        :param ynames: available y-axis names
        '''
        if self.nb_splts == 1:
            ncol = len(self.legend['handles']) // 6 + 1
            self.splt.legend(self.legend['handles'],
                             self.legend['labels'],
                             ncol=ncol)
        else:
            for iyax, nplt in enumerate(ynames.values()):
                if nplt > 0:
                    ncol = nplt // 6 + 1
                    self.splt[iyax].legend(
                        [h for i, h in enumerate(self.legend['handles'])
                         if self.legend['iplot'][i] == iyax],
                        [l for i, l in enumerate(self.legend['labels'])
                         if self.legend['iplot'][i] == iyax],
                        ncol=ncol)

    @staticmethod
    def show():
        '''Show the plot in a popup window.'''
        plt.show()

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        self.fig.savefig(name)

    @staticmethod
    def plt():
        '''Return the matplotlib instance.'''
        return plt
