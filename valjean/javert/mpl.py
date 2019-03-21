'''This module provides the classes to convert test results to plots using
:mod:`matplotlib.pyplot`.


:class:`MplPlot` objects take as input :class:`~.templates.PlotTemplate`
containing at least values and bins.

The format, or rendering, of the plot can be set using the rcParams but also
some predefined parameters on which the class cycle like colors, markers shape
and filling.

By default the first color is black and only used for reference. The cycle on
colors excludes the reference color.

Plots can be obtained with the following for example:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = [CurveElements(values=bins*0.5*(icurve+1),
    ...                          label=str(icurve+1),
    ...                          index=icurve)
    ...            for icurve in range(20)]
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
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
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins*0.5*(icurve+1),
    ...                                  label=str(icurve+1), index=icurve))
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert import mpl
    >>> mpl.STYLE = 'Solarize_Light2'
    >>> mplplt = mpl.MplPlot(pltit)


Colors and markers can also be changed directly:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins*0.5*(icurve+1),
    ...                                  label=str(icurve+1), index=icurve))
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
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
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.templates.PlotTemplate`.

        :param data: the data to convert.
        :type data: :class:`~.templates.PlotTemplate`
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
        self.legend = {'handles': [], 'labels': [], 'iplot': [], 'index': []}
        self.draw()

    def draw(self):
        '''Draw method.'''
        return self.error_plots()

    def ierror_plot(self, idata, iplot, data_fmt):
        '''Draw the plot with error bars on the plot (update the plot)

        If only one curve is represented and the bins are given by centers not
        (dashed) line will be represented between points, as soon as at least
        two curves are represented a dashed line join the points for better
        lisibility.

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
            # self.legend['labels'].append(self.data.curves[idata].label)
            # self.legend['iplot'].append(iplot)
            # self.legend['index'].append(self.data.curves[idata].index)
        else:
            linesty = '--' if len(self.data.curves) > 1 else ''
            eplt = splt.errorbar(
                self.data.bins, self.data.curves[idata].values,
                yerr=self.data.curves[idata].errors, linestyle=linesty,
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2])
            self.legend['handles'].append(eplt)
        self.legend['labels'].append(self.data.curves[idata].label)
        self.legend['iplot'].append(iplot)
        self.legend['index'].append(self.data.curves[idata].index)

    def error_plots(self):
        '''Plot errorbar plot (update the pyplot instance) and build the
        legend.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.

        .. todo::

            change logic of color/marker incrementing when reference will
            be given (next PR)
        '''
        ynames = OrderedDict()
        icv_format = (('k', 'o', 'full') if len(self.data.curves) > 1
                      else ('b', 'o', 'full'))
        for icv, curve in enumerate(self.data.curves):
            if curve.yname not in ynames:
                ynames[curve.yname] = 0
            else:
                ynames[curve.yname] += 1
            if curve.index in self.legend['index']:
                prevc = (
                    self.legend['handles'][curve.index][1][0]
                    if self.data.bins.size == curve.values.size+1
                    else self.legend['handles'][curve.index][0])
                icv_format = (prevc.get_color(),
                              prevc.get_marker(),
                              prevc.get_fillstyle())
            else:
                if self.nb_splts != len(self.data.curves) and icv > 0:
                    icv_format = tuple(next(pf) for pf in self.curve_format)
            self.ierror_plot(icv,
                             list(ynames.keys()).index(curve.yname),
                             icv_format)
        self._build_legend(ynames)

    def _build_legend(self, ynames):
        '''Build the legends from self.legend and add them to the figures.

        An automatic number of columns is calculated, depending on the number
        of curves to be plotted on each subplot. It has been decided to add a
        new columns each 5 curves.

        No legend is printed when only one curve is given.

        :param ynames: available y-axis names
        '''
        if len(self.data.curves) == 1:
            return
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

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        self.fig.savefig(name)
