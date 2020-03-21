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
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = (np.array(np.arange(10)),)
    >>> lcurves = [CurveElements(values=bins[0]*0.5*(icurve+1), bins=bins,
    ...                          legend=str(icurve+1), index=icurve)
    ...            for icurve in range(20)]
    >>> pltit = PlotTemplate(subplots=[SubPlotElements(
    ...     curves=lcurves, axnames=('the x-axis', ''), ptype='1D')])
    >>> from valjean.javert.mpl import MplPlot
    >>> mplplt = MplPlot(pltit)
    >>> fig = mplplt.draw()

Additional subplots can be drawn if required. The style of the curves is fixed
by the index (see :class:`.CurveElements`).

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = (np.array(np.arange(10)),)
    >>> lcurves1 = []
    >>> for icurve in range(3):
    ...     lcurves1.append(CurveElements(
    ...         values=bins[0][1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         bins=bins, legend=str(icurve), index=icurve))
    >>> sbpe1 = SubPlotElements(curves=lcurves1, axnames=('the x-axis', ''))
    >>> lcurves2 = []
    >>> for icurve in range(1, 3):
    ...     lcurves2.append(CurveElements(
    ...         values=lcurves1[icurve].values/lcurves1[0].values, bins=bins,
    ...         legend=str(icurve+1), index=icurve))
    >>> sbpe2 = SubPlotElements(curves=lcurves2,
    ...                         axnames=('the x-axis', 'C/ref'))
    >>> lcurves3 = []
    >>> for icurve in range(1, 3):
    ...     lcurves3.append(CurveElements(
    ...         values=((lcurves1[icurve].values-lcurves1[0].values)
    ...                 /lcurves1[0].values),
    ...         bins=bins, legend=str(icurve+1), index=icurve))
    >>> sbpe3 = SubPlotElements(curves=lcurves3,
    ...                         axnames=('the x-axis', '(C-ref)/ref'))
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3])
    >>> from valjean.javert.mpl import MplPlot
    >>> mplplt = MplPlot(pltit)
    >>> fig = mplplt.draw()

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
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = (np.array(np.arange(10)),)
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins[0]*0.5*(icurve+1),
    ...                                  bins=bins, legend=str(icurve+1),
    ...                                  index=icurve))
    >>> sbpe = SubPlotElements(curves=lcurves, axnames=['the x-axis', ''])
    >>> pltit = PlotTemplate(subplots=[sbpe])
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> mplplt = MplPlot(pltit, style=MplStyle(style='Solarize_Light2'))
    >>> fig = mplplt.draw()

Colors and markers
``````````````````

Colors and markers can also be changed directly:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(np.arange(10))]
    >>> lcurves = []
    >>> for icurve in range(20):
    ...     lcurves.append(CurveElements(values=bins[0]*0.5*(icurve+1),
    ...                                  bins=bins, legend=str(icurve+1),
    ...                                  index=icurve))
    >>> sbpe = SubPlotElements(curves=lcurves, axnames=['the x-axis', ''])
    >>> pltit = PlotTemplate(subplots=[sbpe])
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> style = MplStyle(colors=['b', 'g', 'r', 'y', 'm'],
    ...                  mshape=['X', '+', 'D', '1', 'p', 'v', 'o'],
    ...                  mfill=['top', 'full', 'right', 'none', 'bottom',
    ...                         'left', 'none'])
    >>> mplplt = MplPlot(pltit, style)
    >>> fig = mplplt.draw()


Legends
```````

By default the legend is represented on the top panel (the largest one in 1D)
at the location **Matplotlib** determines. ``LEGENDS`` is a dictionary.
Currently two keys are interpreted:

* ``'all_subplots'``: to plot the legend on all subplots (or panels) of the \
  plot (expected a boolean, default: ``False``)
* ``''legend_kwargs'``: dictionary of keyword arguements to be passed to the \
  legend, for example to change the position of the legend. The keys should \
  correspond to legend keys which list is given in the `legend documentation`_.

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(np.arange(10))]
    >>> lcurves1 = []
    >>> for icurve in range(3):
    ...     lcurves1.append(CurveElements(
    ...         values=bins[0][1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         bins=bins, legend=str(icurve), index=icurve))
    >>> sbpe1 = SubPlotElements(curves=lcurves1, axnames=['the x-axis', ''])
    >>> lcurves2 = []
    >>> for icurve in range(1, 3):
    ...     lcurves2.append(CurveElements(
    ...         values=lcurves1[icurve].values/lcurves1[0].values,
    ...         bins=bins, legend=str(icurve+1)+' vs 0', index=icurve))
    >>> sbpe2 = SubPlotElements(curves=lcurves2,
    ...                         axnames=['the x-axis', 'C/ref'])
    >>> lcurves3 = []
    >>> for icurve in range(1, 3):
    ...     lcurves3.append(CurveElements(
    ...         values=((lcurves1[icurve].values-lcurves1[0].values)
    ...                 /lcurves1[0].values),
    ...         bins=bins, legend=str(icurve+1)+' vs 0', index=icurve))
    >>> sbpe3 = SubPlotElements(curves=lcurves3,
    ...                         axnames=['the x-axis', '(C-ref)/ref'])
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3])
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> style = MplStyle(legends={
    ...     'legend_kwargs': {'loc': 3, 'bbox_to_anchor': (0., 1., 1, 1),
    ...                        'mode': 'expand'}})
    >>> mplplt = MplPlot(pltit, style=style)
    >>> fig = mplplt.draw()

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(np.arange(10))]
    >>> lcurves1 = []
    >>> for icurve in range(3):
    ...     lcurves1.append(CurveElements(
    ...         values=bins[0][1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...         bins=bins, legend=str(icurve), index=icurve))
    >>> sbpe1 = SubPlotElements(curves=lcurves1, axnames=['the x-axis', ''])
    >>> lcurves2 = []
    >>> for icurve in range(1, 3):
    ...     lcurves2.append(CurveElements(
    ...         values=lcurves1[icurve].values/lcurves1[0].values,
    ...         bins=bins, legend=str(icurve+1)+' vs 0', index=icurve))
    >>> sbpe2 = SubPlotElements(curves=lcurves2,
    ...                         axnames=['the x-axis', 'C/ref'])
    >>> lcurves3 = []
    >>> for icurve in range(1, 3):
    ...     lcurves3.append(CurveElements(
    ...         values=((lcurves1[icurve].values-lcurves1[0].values)
    ...                 /lcurves1[0].values),
    ...         bins=bins, legend=str(icurve+1)+' vs 0', index=icurve))
    >>> sbpe3 = SubPlotElements(curves=lcurves3,
    ...                         axnames=['the x-axis', '(C-ref)/ref'])
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3])
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> mplplt = MplPlot(pltit,
    ...                  style=MplStyle(legends={'all_subplots': True}))
    >>> fig = mplplt.draw()


2D plots
--------

To make 2D plots the class :class:`MplPlot2D` has to be used. Principle is the
same as for 1D plots. Three axes are expected.Each curve has its own plot, no
superposition is done. A subplot is then a collection of curves that share the
same axes (names and properties).

The colorbar axis label is set using the third axis name.

There is no real legend, so ``legend`` is used as title of each plot.

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.arange(6), np.arange(17, step=2)]
    >>> axnames = ['x', 'y']
    >>> incvals = np.arange(1, 41).reshape(5, 8)
    >>> decvals = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> lcurves = []
    >>> lcurves.append(CurveElements(
    ...         values=incvals, bins=bins, legend='increase', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=decvals, bins=bins, legend='decrease', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=incvals/decvals, bins=bins, legend='', index=1))
    >>> sbp1 = SubPlotElements(
    ...     curves=lcurves[:-1], axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp2 = SubPlotElements(
    ...     curves=lcurves[2:], axnames=['x', 'y', 'ratio'], ptype='2D')
    >>> pltnd = PlotTemplate(subplots=[sbp1, sbp2])
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltnd)
    >>> fig = mplplt.draw()


Customization
`````````````

Some customizations can be done for each subplot: limits to adapt axes ranges,
logarithmic scale or lines.

Using the previous example:

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(np.arange(10))]
    >>> lcurves1 = [CurveElements(
    ...     values=bins[0][1:]*0.5*(icurve+1) + icurve*(-1)**(icurve),
    ...     bins=bins, legend=str(icurve), index=icurve)
    ...             for icurve in range(3)]
    >>> sbpe1 = SubPlotElements(curves=lcurves1, axnames=['the x-axis', ''])
    >>> lcurves2 = [CurveElements(
    ...     values=lcurves1[icurve].values/lcurves1[0].values, bins=bins,
    ...     legend=str(icurve+1)+' vs 0', index=icurve)
    ...             for icurve in range(1, 3)]
    >>> sbpe2 = SubPlotElements(curves=lcurves2,
    ...                         axnames=['the x-axis', 'C/ref'])
    >>> lcurves3 = [CurveElements(
    ...     values=((lcurves1[icurve].values-lcurves1[0].values)
    ...             /lcurves1[0].values),
    ...     bins=bins, legend=str(icurve+1)+' vs 0', index=icurve)
    ...             for icurve in range(1, 3)]
    >>> sbpe3 = SubPlotElements(curves=lcurves3,
    ...                         axnames=['the x-axis', '(C-ref)/ref'])
    >>> sbpe1.logx, sbpe2.logx, sbpe3.logx = True, True, True
    >>> sbpe1.limits, sbpe2.limits, sbpe3.limits = [(2, 7)], [(2, 7)], [(2, 7)]
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3])
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> mplplt = MplPlot(pltit,
    ...                  style=MplStyle(legends={'all_subplots': True}))
    >>> fig = mplplt.draw()


Customization also works on 2D plots. In addition the colorscale and colormap
can be put in logarithmic scale.

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.arange(6), np.arange(17, step=2)]
    >>> axnames = ['x', 'y']
    >>> incvals = np.arange(1, 41).reshape(5, 8)
    >>> decvals = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> lcurves = []
    >>> lcurves.append(CurveElements(
    ...         values=incvals, bins=bins, legend='increase', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=decvals, bins=bins, legend='decrease', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=incvals/decvals, bins=bins, legend='', index=1))
    >>> sbp1 = SubPlotElements(
    ...     curves=lcurves[:-1], axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp1.logz = False
    >>> sbp2 = SubPlotElements(
    ...     curves=lcurves[2:], axnames=['x', 'y', 'ratio'], ptype='2D')
    >>> sbp2.logz = True
    >>> pltnd = PlotTemplate(subplots=[sbp1, sbp2])
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot2D(pltnd)
    >>> fig = mplplt.draw()

All 'curves' (so 2D plots) in a :class:`~.templates.SubPlotElements` will share
the same properties. If in the previous case somebody would like the second
curve (``legend='decrase'``) in logaritmic scales for y and z-axes for example,
a new :class:`~.templates.SubPlotElements` should be used:

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.arange(6), np.arange(17, step=2)]
    >>> axnames = ['x', 'y']
    >>> incvals = np.arange(1, 41).reshape(5, 8)
    >>> decvals = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> lcurves = []
    >>> lcurves.append(CurveElements(
    ...         values=incvals, bins=bins, legend='increase', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=decvals, bins=bins, legend='decrease', index=0))
    >>> lcurves.append(CurveElements(
    ...         values=incvals/decvals, bins=bins, legend='', index=1))
    >>> sbp1 = SubPlotElements(
    ...     curves=[lcurves[0]], axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp1b = SubPlotElements(
    ...     curves=[lcurves[1]], axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp1b.logy = True
    >>> sbp1b.logz = True
    >>> sbp2 = SubPlotElements(
    ...     curves=[lcurves[2]], axnames=['x', 'y', 'ratio'], ptype='2D')
    >>> sbp2.logz = True
    >>> pltnd = PlotTemplate(subplots=[sbp1, sbp1b, sbp2])
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot2D(pltnd)
    >>> fig = mplplt.draw()


Module API
----------
'''
from itertools import cycle, chain
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mplcol
from .. import LOGGER


class MplStyle:
    '''Class to store style characteristics.'''

    def __init__(self, colors=None, mshape=None, mfill=None, style=None,
                 legends=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of the style.

        The instance attributes are private, but they are exposed via
        properties.
        '''
        self.colors = (['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
                        'C9'] if colors is None else colors)
        self.markers_shape = (['s', 's', 'H', 'H', 'D', 'D', 'o', 'o', 'X',
                               'X', 'h', 'h', 'P', 'P', '8', '8']
                              if mshape is None else mshape)
        self.markers_fill = ['full', 'none'] if mfill is None else mfill
        self.style = 'default' if style is None else style
        self.legends = ({'all_subplots': False, 'position': {}}
                        if legends is None else legends)


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

    def __init__(self, data, style=MplStyle()):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.templates.PlotTemplate`.

        :param PlotTemplate data: the data to convert.

        This class contains only one instance variable: ``mpl_plot`` that can
        be

        * :class:`MplPlot1D` for usual 1D plots
        * :class:`MplPlot2D` for 2D plots

        This choice is done depending on the dimension of
        :class:`~.templates.PlotTemplate`.

        No plot for more than 2 dimensions are done.
        '''
        self.mpl_plot = None
        if not all(s.ptype == data.subplots[0].ptype for s in data.subplots):
            LOGGER.info('No common plots are currently available for '
                        'different kinds of data (1D and 2D for example)')
            return
        if data.subplots[0].ptype == '1D':
            self.mpl_plot = MplPlot1D(data, style)
        elif data.subplots[0].ptype == '2D':
            self.mpl_plot = MplPlot2D(data, style)
        else:
            LOGGER.warning("ptype {} not taken into account. "
                           "Expected ones are ['1D', '2D'].")

    def draw(self):
        '''Draw the plot.'''
        if self.mpl_plot is None:
            return None
        return self.mpl_plot.draw()

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        if self.mpl_plot is not None:
            fig = self.draw()
            self.mpl_plot.save(name)
            plt.close(fig)


class MplPlot1D:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib plot.'''

    def __init__(self, data, style=MplStyle()):
        '''Construct a :class:`MplPlot1D` from the given
        :class:`~.templates.PlotTemplate`.

        :param PlotTemplate data: the data to convert.

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
        self.mpl_style = style
        plt.style.use(self.mpl_style.style)
        ref_fmt = (('k', 'o', 'full') if data.nb_curves > 1
                   else ('b', 'o', 'full'),)
        self.curve_format = chain(ref_fmt,
                                  zip(cycle(self.mpl_style.colors),
                                      cycle(self.mpl_style.markers_shape),
                                      cycle(self.mpl_style.markers_fill)))
        self.data = data
        self.nb_splts = self.data.nb_plots
        self.fig, self.splt = None, None
        self.legend = []

    def draw(self):
        '''Draw method.'''
        if self.data.same_xaxis():
            self.fig, self.splt = plt.subplots(
                self.nb_splts, sharex=True,
                figsize=(6.4, 4.8+1.2*(self.nb_splts-1)),
                gridspec_kw={'height_ratios': [4] + [1]*(self.nb_splts-1),
                             'hspace': 0.05})
        else:
            self.fig, self.splt = plt.subplots(
                self.nb_splts, figsize=(6.4, 6.4+2*(self.nb_splts-1)),
                gridspec_kw={'hspace': 0.4, 'top': 0.95, 'bottom': 0.05,
                             'right': 0.95})
        if self.nb_splts == 1:
            self.splt = [self.splt]
        self.error_plots()
        self.customize_plots()
        return self.fig

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
        LOGGER.debug("in ierror plot for plot %s on subplot %d",
                     curve.legend, iplot)
        splt = self.splt[iplot]
        if curve.bins[0].size == curve.values.size+1:
            steps = splt.errorbar(
                curve.bins[0], np.append(curve.values, [np.nan]),
                linestyle='-', color=data_fmt[0], drawstyle='steps-post')
            markers = splt.errorbar(
                (curve.bins[0][1:] + curve.bins[0][:-1])/2,
                curve.values, yerr=curve.errors,
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2],
                linestyle='')
            self.legend.append(MplLegend((steps, markers), curve.legend, iplot,
                                         curve.index))
        else:
            linesty = '--' if len(self.data.subplots[0].curves) > 1 else ''
            eplt = splt.errorbar(
                curve.bins[0], curve.values, yerr=curve.errors,
                linestyle=linesty, color=data_fmt[0], marker=data_fmt[1],
                fillstyle=data_fmt[2])
            self.legend.append(MplLegend(eplt, curve.legend, iplot,
                                         curve.index))

    def error_plots(self):
        '''Plot errorbar plot (update the pyplot instance) and build the
        legend.

        Remark: datasets are supposed to be already consistent as coming from
        a single test. If we had them manually bins will need to be checked.
        '''
        crvs_by_index = self.data.pack_by_index()
        for crvs, fmt in zip(crvs_by_index.values(), self.curve_format):
            # print("fmt:", fmt)
            for crv, iplt in crvs:
                self.ierror_plot(crv, iplt, fmt)
        self._build_legend()

    def _build_legend(self):  # , labels):
        '''Build the legends from self.legend and add them to the figures.

        An automatic number of columns is calculated, depending on the number
        of curves to be plotted on each subplot. It has been decided to add a
        new columns each 5 curves.

        No legend is printed when only one curve is given.

        :param labels: available y-axis names
        '''
        if all(len(s.curves) == 1 for s in self.data.subplots):
            return
        for iplt, dplt in enumerate(self.data.subplots):
            if iplt == 0 or self.mpl_style.legends.get('all_subplots', False):
                ncol = len(dplt.curves) // 6 + 1
                self.splt[iplt].legend(
                    [lg.handle for lg in self.legend if lg.iplot == iplt],
                    [lg.label for lg in self.legend if lg.iplot == iplt],
                    ncol=ncol,
                    **self.mpl_style.legends.get('legend_kwargs', {}))

    def customize_plots(self):
        '''Customize plots.'''
        for i, (iplt, splt) in enumerate(zip(self.splt, self.data.subplots)):
            if i == self.data.nb_plots-1 or not self.data.same_xaxis():
                iplt.set_xlabel(splt.axnames[0])
            iplt.set_ylabel(splt.axnames[1])
            if splt.limits is not None:
                iplt.set_xlim(*splt.limits[0])
            if splt.logx:
                iplt.set_xscale('log')
            if splt.logy:
                iplt.set_yscale('log')
            if splt.lines:
                xlims, ylims = iplt.get_xlim(), iplt.get_ylim()
                for line in splt.lines:
                    if ('x' in line
                            and line['x'] > xlims[0] and line['x'] < xlims[1]):
                        iplt.axvline(x=line['x'], c='grey', ls='--', lw=0.5)
                    if ('y' in line
                            and line['y'] > ylims[0] and line['y'] < ylims[1]):
                        iplt.axhline(y=line['y'], c='grey', ls='--', lw=0.5)

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        self.fig.savefig(name)


class MplPlot2D:
    '''Convert a :class:`~.templates.PlotTemplate` into a 2D plot.'''

    def __init__(self, data, style=MplStyle()):
        '''Construct a :class:`MplPlot2D` from the given
        :class:`~.templates.PlotTemplate`.

        :param PlotTemplate data: the data to convert.

        **Instance variables:**

        `nb_splts` (:class:`int`)
            number of subplots in the plot, initialised from ``data``

        `fig` (:class:`matplotlib.figure.Figure`)
            **Matplotlib** figure

        `splt` (:class:`matplotlib.axes.Axes` or \
            :class:`tuple` (:class:`~matplotlib.axes.Axes`))
            the subplots on which will be drawn the curves, tuple if more than
            one subplot
        '''
        LOGGER.debug('initialisation of MplPlot2D')
        plt.style.use(style.style)
        self.data = data
        self.nb_splts = self.data.nb_curves
        self.fig, self.splt = None, None

    def draw(self):
        '''Draw method.

        Remark: if the quantity represented is required in logarithmic scale it
        will be done at the histogram declaration and not in the customization
        step.
        '''
        self.fig, self.splt = plt.subplots(
            self.nb_splts,  # sharex=True, sharey=True,
            figsize=(6.4, 6.4+2*(self.nb_splts-1)),
            gridspec_kw={'hspace': 0.4, 'top': 0.95, 'bottom': 0.05,
                         'right': 0.95})
        if self.nb_splts == 1:
            self.splt = [self.splt]
        self.twod_plots()
        self.customize_plots()
        return self.fig

    @staticmethod
    def broadcast_bin_centers(curve):
        '''Calcuate bin centers if edges are given and broadcast all bins:
        build the (x, y) grid for all bins.

        :param CurveElements curve: data to plot
        :param list(numpy.ndarray) lbins: x and y bins corresponding to data
        :rtype: numpy.ndarray
        '''
        bins = []
        for idim, tbin in enumerate(curve.bins):
            shape = ([curve.values.shape[idim]]
                     + [1] * (curve.values.ndim - 1 - idim))
            cbins = ((tbin[1:] + tbin[:-1]) * 0.5
                     if tbin.size == curve.values.shape[idim]+1
                     else tbin)
            bins.append(np.array(cbins).reshape(shape))
        bbins = np.broadcast_arrays(*bins)
        return bbins

    def itwod_plot(self, curve, iplot, axnames, norm):
        '''Draw the 2D distribution on the ith subplot.

        :param CurveElements curve: data to plot
        :param int iplot: number of the subplot
        :param norm: function corresponding to the chosen
            normalisation and scale (linear or logarithmic)
        :type norm: function from :obj:`matplotlib.colors`
        '''
        cbins = self.broadcast_bin_centers(curve)
        h2d = self.splt[iplot].hist2d(
            cbins[0].flatten(), cbins[1].flatten(),
            bins=curve.bins, norm=norm, weights=curve.values.flatten())
        cbar = self.fig.colorbar(h2d[3], ax=self.splt[iplot])
        self.splt[iplot].set_xlabel(axnames[0])
        self.splt[iplot].set_ylabel(axnames[1])
        cbar.set_label(axnames[2])
        if curve.legend:
            self.splt[iplot].set_title(curve.legend)

    def twod_plots(self):
        '''Build 2D plots.'''
        iplot = 0
        for splt in self.data.subplots:
            for crv in splt.curves:
                self.itwod_plot(
                    crv, iplot, splt.axnames,
                    norm=(mplcol.LogNorm() if splt.logz
                          else mplcol.Normalize()))
                iplot += 1

    def customize_plots(self):
        '''Customize plots.'''
        isplt = 0
        for dsplt in self.data.subplots:
            for _ in range(len(dsplt.curves)):
                if dsplt.limits is not None:
                    self.splt[isplt].set_xlim(*dsplt.limits[0])
                    self.splt[isplt].set_ylim(*dsplt.limits[1])
                if dsplt.logx:
                    self.splt[isplt].set_xscale('log')
                if dsplt.logy:
                    self.splt[isplt].set_yscale('log')
                isplt += 1
        plt.subplots_adjust(top=0.95)

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        self.fig.savefig(name)
