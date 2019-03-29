'''This module provides the classes to convert test results to plots using
:mod:`matplotlib.pyplot`.

.. _legend documentation:
    https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html

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

Additional subplots can be drawn if they have different y-axis names (set using
the ``yname`` argument in :class:`.CurveElements`). The style of the curves is
fixed by the index (see :class:`.CurveElements`).

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(3):
    ...     lcurves.append(CurveElements(
    ...         values=bins[1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         label=str(icurve), index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=lcurves[icurve].values/lcurves[0].values,
    ...         yname='C/ref', label=str(icurve+1), index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=((lcurves[icurve].values-lcurves[0].values)
    ...                 /lcurves[0].values),
    ...         yname='(C-ref)/ref', label=str(icurve+1), index=icurve))
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert.mpl import MplPlot
    >>> mplplt = MplPlot(pltit)

These examples also show the default style of the plots.


Style setup
-----------

Some **global** variables are available to customize the plots:

* ``STYLE``: for the general style of the plots
* ``COLORS``: for the list of the colors to be used to represent the curves \
  (they can also be changed by the style)
* ``MARKERS_SHAPE``: for the shape of the markers (a preselection has been \
  done per default)
* ``MARKERS_FILL``: for the fill of the markers, per default an alternance \
  between `full` and `empty` for the same same
* ``LEGENDS``: for the legend customization


General style
`````````````

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

Colors and markers
``````````````````

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


Legends
```````

By default the legend is represented on the top panel (the largest one) at the
location **Matplotlib** determines. ``LEGENDS`` is a dictionary. Currently two
keys are interpreted:

* ``'all_subplots'``: to plot the legend on all subplots (or panels) of the \
  plot (expected a boolean, default: ``False``)
* ``''legend_kwargs'``: dictionary of keyword arguements to be passed to the \
  legend, for example to change the position of the legend. The keys should \
  correspond to legend keys which list is given in the `legend documentation`_.

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(3):
    ...     lcurves.append(CurveElements(
    ...         values=bins[1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         label=str(icurve), index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=lcurves[icurve].values/lcurves[0].values,
    ...         yname='C/ref', label=str(icurve+1)+' vs 0', index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=((lcurves[icurve].values-lcurves[0].values)
    ...                 /lcurves[0].values),
    ...         yname='(C-ref)/ref', label=str(icurve+1)+' vs 0',
    ...         index=icurve))
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert import mpl
    >>> mpl.LEGENDS = {'legend_kwargs': {'loc': 3,
    ...                                  'bbox_to_anchor': (0., 1., 1, 1),
    ...                                  'mode': 'expand'}}
    >>> mplplt = mpl.MplPlot(pltit)

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import PlotTemplate, CurveElements
    >>> bins = np.array(np.arange(10))
    >>> lcurves = []
    >>> for icurve in range(3):
    ...     lcurves.append(CurveElements(
    ...         values=bins[1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         label=str(icurve), index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=lcurves[icurve].values/lcurves[0].values,
    ...         yname='C/ref', label=str(icurve+1)+' vs 0', index=icurve))
    >>> for icurve in range(1, 3):
    ...     lcurves.append(CurveElements(
    ...         values=((lcurves[icurve].values-lcurves[0].values)
    ...                 /lcurves[0].values),
    ...         yname='(C-ref)/ref', label=str(icurve+1)+' vs 0',
    ...         index=icurve))
    >>> pltit = PlotTemplate(bins=bins, curves=lcurves, xname='the x-axis')
    >>> from valjean.javert import mpl
    >>> mpl.LEGENDS = {'all_subplots': True}
    >>> mplplt = mpl.MplPlot(pltit)


Module API
----------
'''
from collections import OrderedDict, defaultdict
from itertools import cycle, chain
import numpy as np
import matplotlib.pyplot as plt
from .. import LOGGER


COLORS = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
MARKERS_SHAPE = ['s', 's', 'H', 'H', 'D', 'D', 'o', 'o', 'X', 'X', 'h', 'h',
                 'P', 'P', '8', '8']
MARKERS_FILL = ['full', 'none']
STYLE = 'default'
LEGENDS = {'all_subplots': False, 'position': {}}


class MplLegend:
    '''Class to store the legend content.'''

    def __init__(self, handle, label, iplot, index):
        '''Initialisation of :class:`MplLegend`.

        :param handle: curve to be stored (if the curve needs to be drawn in
            twice a tuple should be given)
        :type handle: :obj:`matplotlib.pyplot.errorbar`
            or :obj:`tuple` (:obj:`matplotlib.pyplot.errorbar`)
        :param str label: the curve label
        :param int iplot: index of the subplot / panel on which the curve will
            be drawn
        :param int index: curve index, to identify its style
        '''
        self.handle = handle
        self.label = label
        self.iplot = iplot
        self.index = index


class MplPlot:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib plot.'''

    def __init__(self, data):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.templates.PlotTemplate`.

        :param data: the data to convert.
        :type data: :class:`~.templates.PlotTemplate`

        **Instance variables:**

        `curve_format` (:class:`tuple`)
            available formats (colors, markers_shape, markers_fill) for the
            curves. They are determined using the chosen ``STYLE`` and cycling
            on it using :obj:`itertools.cycle`.

        `nb_splts` (:class:`int`)
            number of subplots in the plot, initialised from ``data``

        `fig` (:class:`matplotlib.figure.Figure`)
            **Matplotlib** figure

        `splt` (:class:`matplotlib.axes.Axes` or \
            :class:`tuple` (:class:`~matplotlib.axes.Axes`))
            the subplots on which will be drawn the curves, tuple if more than
            one subplot

        `legend` (:class:`list`)
            list of :class:`MplLegend` (filled when curves are drawn)
        '''
        plt.style.use(STYLE)
        ref_fmt = (('k', 'o', 'full') if len(data.curves) > 1
                   else ('b', 'o', 'full'),)
        self.curve_format = chain(ref_fmt,
                                  zip(cycle(COLORS),
                                      cycle(MARKERS_SHAPE),
                                      cycle(MARKERS_FILL)))
        self.data = data
        self.nb_splts = len(set(c.yname for c in self.data.curves))
        self.fig, self.splt = plt.subplots(
            self.nb_splts, sharex=True,
            figsize=(6.4, 4.8+1.2*(self.nb_splts-1)),
            gridspec_kw={'height_ratios': [4] + [1]*(self.nb_splts-1),
                         'hspace': 0.05})
        self.legend = []
        self.draw()

    def draw(self):
        '''Draw method.'''
        return self.error_plots()

    def ierror_plot(self, curve, iplot, data_fmt):
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
        LOGGER.debug("in ierror plot for plot %d on subplot %d",
                     curve.label, iplot)
        splt = self.splt if self.nb_splts == 1 else self.splt[iplot]
        if iplot == self.nb_splts-1:
            splt.set_xlabel(self.data.xname)
        splt.set_ylabel(curve.yname)
        if self.data.bins.size == curve.values.size+1:
            steps = splt.errorbar(
                self.data.bins, np.append(curve.values, [np.nan]),
                linestyle='-', color=data_fmt[0], drawstyle='steps-post')
            markers = splt.errorbar(
                (self.data.bins[1:] + self.data.bins[:-1])/2,
                curve.values, yerr=curve.errors,
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2],
                linestyle='')
            self.legend.append(MplLegend((steps, markers), curve.label, iplot,
                                         curve.index))
        else:
            linesty = '--' if len(self.data.curves) > 1 else ''
            eplt = splt.errorbar(
                self.data.bins, curve.values, yerr=curve.errors,
                linestyle=linesty, color=data_fmt[0], marker=data_fmt[1],
                fillstyle=data_fmt[2])
            self.legend.append(MplLegend(eplt, curve.label, iplot,
                                         curve.index))

    @staticmethod
    def pack_by_index(curves):
        '''Pack the curves by index.

        :param curves: list of curves to be used
        :type curves: :class:`.CurveElements`
        :returns: :class:`collections.defaultdict` (:class:`list`)
        '''
        ind_dict = defaultdict(list)
        for crv in curves:
            ind_dict[crv.index].append(crv)
        return ind_dict

    @staticmethod
    def sbplts_by_yname(curves):
        '''Associate the subplots to the y-axis names.

        The order is supposed to be fixed by the user earlier. The first
        subplot will always be bigger (values per default).

        :param curves: list of curves to be used
        :type curves: :class:`.CurveElements`
        :returns: :class:`collections.defaultdict` (:class:`list`)
        '''
        sbynames = OrderedDict()
        for crv in curves:
            if crv.yname not in sbynames:
                sbynames[crv.yname] = [1, len(sbynames)]
            else:
                sbynames[crv.yname][0] += 1
        return sbynames

    def error_plots(self):
        '''Plot errorbar plot (update the pyplot instance) and build the
        legend.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        crvs_by_index = self.pack_by_index(self.data.curves)
        sbplts_by_ynames = self.sbplts_by_yname(self.data.curves)
        for crvs, fmt in zip(crvs_by_index.values(), self.curve_format):
            for crv in crvs:
                self.ierror_plot(crv, sbplts_by_ynames[crv.yname][1], fmt)
        self._build_legend(sbplts_by_ynames)

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
            ncol = len(self.legend) // 6 + 1
            self.splt.legend([l.handle for l in self.legend],
                             [l.label for l in self.legend],
                             ncol=ncol, **LEGENDS.get('legend_kwargs', {}))
            return
        for nplt, iyax in ynames.values():
            if nplt > 0 and (LEGENDS.get('all_subplots', False)
                             or iyax == 0):
                ncol = nplt // 6 + 1
                self.splt[iyax].legend(
                    [l.handle for l in self.legend if l.iplot == iyax],
                    [l.label for l in self.legend if l.iplot == iyax],
                    ncol=ncol, **LEGENDS.get('legend_kwargs', {}))
            return

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        self.fig.savefig(name)
