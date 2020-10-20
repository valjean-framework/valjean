'''This module provides the classes to convert test results to plots using
:mod:`matplotlib.pyplot`.

.. _legend documentation:
    https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.legend.html
.. _matplotlib colors:
    https://matplotlib.org/tutorials/colors/colors.html
.. _matplotlib markers:
    https://matplotlib.org/api/markers_api.html
.. _matplotlib styles:
    https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html

:class:`MplPlot` objects take as input :class:`~.templates.PlotTemplate`
containing curves (:class:`~.templates.CurveElements`) classified by sub-plots
(:class:`~.templates.SubPlotElements`).

The format, or rendering, of the plot can be set using the rcParams but also
some predefined parameters on which the class cycle like colors, markers shape
and filling.

By default the first color is black and is used only once: it is excluded from
the cycle on colors. It is typically reserved for the reference but can be
reused if the first index is used for another curve.

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
    >>> fig, _ = mplplt.draw()

Additional subplots can be drawn if required. The style of the curves is fixed
by the index (see :class:`.CurveElements`).

.. _plot 3 panels:
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
    >>> fig, _ = mplplt.draw()

These examples also show the default style of the plots.


Style setup
-----------

Some style parameters are available in the object :class:`MplStyle`: general
style, colors of markers and lines (expected to be the same for the same
curve), shapes and fills of markers. Legend keyword arguments can also be
given.


General style
`````````````

It is possible to change the general style of plots using a predefined one
or to use different markers. The predefined styles can be seen in `matplotlib
styles`_ or be obtained thanks to

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
    >>> fig, _ = mplplt.draw()

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
    >>> mplplt = MplPlot(pltit , style=style)
    >>> fig, _ = mplplt.draw()


Legends
```````

By default the legend is represented on all panels at the location
**Matplotlib** determines like in `plot 3 panels`_.

If you would prefer to get only one legend for all panels, the
``suppress_legends`` argument in :class:`~.templates.PlotTemplate` should be
used. In that case, only fine for 1D plots, the legend will be placed on the
largest panel by default.

In the style any keyword argument accepted by matplotlib can be given to modify
for example the legend position. This is can be found in the `legend
documentation`_.

The next example show the `plot 3 panels`_ with only one legend which position
and shape have been modified.

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
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3],
    ...                      suppress_legends=True)
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> style = MplStyle(legends={'loc': 3, 'bbox_to_anchor': (0., 1., 1, 1),
    ...                           'mode': 'expand'})
    >>> mplplt = MplPlot(pltit, style=style)
    >>> fig, _ = mplplt.draw()


2D plots
--------

2D plots are also done via the class :class:`MplPlot`. The plot type ``ptype``
in :class:`~.templates.PlotTemplate` should be ``'2D'``. The principle is the
same as for 1D plots. Three axes are expected. Each curve has its own plot, no
superposition is done, so one subplot is expected to contain only one curve.
Each subplot can then have its own properties.

The colorbar axis label is set using the third axis name.

There is no real legend, so ``legend`` is used as title of each plot.

The index is currently not used.

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.arange(6), np.arange(17, step=2)]
    >>> axnames = ['x', 'y']
    >>> incv = np.arange(1, 41).reshape(5, 8)
    >>> decv = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> lsplts = []
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(
    ...         values=incv, bins=bins, legend='increase', index=0)],
    ...     axnames=['x', 'y', 'spam'], ptype='2D'))
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(
    ...         values=decv, bins=bins, legend='decrease', index=0)],
    ...     axnames=['x', 'y', 'spam'], ptype='2D'))
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(
    ...         values=incv/decv, bins=bins, legend='', index=1)],
    ...     axnames=['x', 'y', 'ratio'], ptype='2D'))
    >>> pltnd = PlotTemplate(subplots=lsplts, small_subplots=False)
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltnd)
    >>> fig, _ = mplplt.draw()


.. note::

    Per default, additional subplots are small ones, it is probably better in
    2D case to set the parameter ``small_subplots`` to ``False`` in the
    :class:`~.templates.PlotTemplate`.

.. warning::

    Requesting more than one curve on a subplot will emit a warning but give
    unexpected results (typically only one of the 2D plot will be shown).

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.arange(6), np.arange(17, step=2)]
    >>> axnames = ['x', 'y']
    >>> incv = np.arange(1, 41).reshape(5, 8)
    >>> decv = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> lsplts = []
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(values=incv, bins=bins, legend='increase'),
    ...             CurveElements(values=decv, bins=bins, legend='decrease')],
    ...     axnames=['x', 'y', 'spam'], ptype='2D'))
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(
    ...         values=incv/decv, bins=bins, legend='', index=1)],
    ...     axnames=['x', 'y', 'ratio'], ptype='2D'))
    >>> pltnd = PlotTemplate(subplots=lsplts)
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltnd)
    >>> fig, _ = mplplt.draw()


Customization
-------------

Some customizations can be done for each subplot with the attributes parameter
of :class:`~.templates.SubPlotElements`: limits to adapt axes ranges,
logarithmic scale or lines.

Using the previous 1D example:

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
    >>> sbpe1.attributes.logx = True
    >>> sbpe2.attributes.limits = [(2, 7)]
    >>> sbpe3.attributes.logy = True
    >>> pltit = PlotTemplate(subplots=[sbpe1, sbpe2, sbpe3],
    ...                      small_subplots=False)
    >>> from valjean.javert.mpl import MplPlot, MplStyle
    >>> mplplt = MplPlot(pltit)
    >>> fig, _ = mplplt.draw()


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
    >>> incv = np.arange(1, 41).reshape(5, 8)
    >>> decv = np.arange(1, 41)[::-1].reshape(5, 8)
    >>> sbp1 = SubPlotElements(
    ...     curves=[CurveElements(values=incv, bins=bins, legend='increase')],
    ...     axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp2 = SubPlotElements(
    ...     curves=[CurveElements(values=decv, bins=bins, legend='decrease')],
    ...     axnames=['x', 'y', 'spam'], ptype='2D')
    >>> sbp3 = SubPlotElements(
    ...     curves=[CurveElements(values=incv/decv, bins=bins, legend='i/d')],
    ...     axnames=['x', 'y', 'ratio'], ptype='2D')
    >>> sbp3.attributes.logz = True
    >>> pltnd = PlotTemplate(subplots=[sbp1, sbp2, sbp3], small_subplots=False)
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltnd)
    >>> fig, _ = mplplt.draw()


Strings as bins
---------------

It is possible to use strings as bins both in 1D and 2D plots. If strings are
too long on x-axis they will be represented vertically.

.. plot::
    :include-source:

    >>> from collections import OrderedDict
    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(['spam', 'egg', 'bacon']),
    ...         np.array(['beer', 'wine', 'milk', 'tea with milk and sugar'])]
    >>> axnames = ['x', 'y']
    >>> v2d = np.arange(12).reshape(3, 4)
    >>> v1d = np.arange(4)
    >>> lsplts = []
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(values=v2d, bins=bins, legend='Menus')],
    ...     axnames=['Meat', 'Drink', 'Associations'], ptype='2D'))
    >>> lsplts.append(SubPlotElements(
    ...     curves=[CurveElements(
    ...         values=v1d, bins=bins[1:], legend='', index=1)],
    ...     axnames=['Drink', 'Quantity'], ptype='1D'))
    >>> pltnd = PlotTemplate(subplots=lsplts)
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltnd)
    >>> fig, _ = mplplt.draw()


Pie plot
--------

Pie plots can be done if requested. `ptype` should be equal to `'pie'`. Note
that the number of `axnames` still has to be N dim + 1, so 2. The first one is
the title of the plot, the second one the title of the legend. If the second
string is empty no title will be given to the legend.

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> ingredients = ['egg', 'spam', 'bacon', 'sausage', 'tomato', 'beans']
    >>> proportions = [0.1, 0.3, 0.25, 0.2, 0.05, 0.1]
    >>> curve = CurveElements(values=np.array(proportions),
    ...                       bins=[ingredients], legend='')
    >>> sbplt = SubPlotElements(curves=[curve],
    ...                         axnames=('Python pie', 'Ingredients'),
    ...                         ptype='pie')
    >>> pltpie = PlotTemplate(subplots=[sbplt])
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltpie)
    >>> fig, _ = mplplt.draw()


Bar plots
---------

Bar plots can be used here with strings as labels in x-axis, like category
plots but no errors are expected here. Two kinds of bar plots are available:
side-by-side bars and stacked bars.

.. plot::
    :include-source:

    >>> import numpy as np
    >>> from valjean.javert.templates import (PlotTemplate, CurveElements,
    ...                                       SubPlotElements)
    >>> bins = [np.array(['spam', 'egg', 'bacon'])]
    >>> data = [np.array([1, 3, 4]),  np.array([2, 4, 5]),
    ...         np.array([5, 3, 2]), np.array([2, 3, 1])]
    >>> names = ['Terry', 'John' , 'Graham', 'Eric']
    >>> lcurves = []
    >>> for datum, name in zip(data, names):
    ...     lcurves.append(CurveElements(values=datum, bins=bins, legend=name))
    >>> speb = SubPlotElements(curves=lcurves,
    ...                        axnames=['ingredient', 'quantity'], ptype='bar')
    >>> spebs = SubPlotElements(curves=lcurves,
    ...                         axnames=['ingredient', 'quantity'],
    ...                         ptype='barstack')
    >>> pltbar = PlotTemplate(subplots=[speb, spebs], small_subplots=False)
    >>> from valjean.javert import mpl
    >>> mplplt = mpl.MplPlot(pltbar)
    >>> fig, _ = mplplt.draw()

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

    def __init__(self, style=None, colors=None, mshape=None, mfill=None,
                 legends=None):
        # pylint: disable=too-many-arguments
        '''Initialisation of the style.

        :param style: style from `matplotlib styles`_ or from user one, if
            ``None`` ``'default'`` is used
        :type style: str or None
        :param colors: colors from `matplotlib colors`_, if ``None`` CN are
            used
        :type colors: list(str) or None
        :param mshape: marker shapes from `matplotlib markers`_, if ``None`` a
            default sequence has been determined
        :type mshape: list(str) or None
        :param mfill: marker fill, ``None`` will use an alternance of
            ``'fill'`` and ``'none'``
        :type mfill: list(str) or None
        :param legends: keyword arguments from `legend documentation`_ to be
            passed to legend builder
        :type legends: dict or None

        An additional instance parameter is available and initialised in
        :class:`MplPlot` thanks to :meth:`styles_sequence`, ``fmts``. It builds
        the suite of styles of 1D curves from colors and markers.
        '''
        self.style = 'default' if style is None else style
        self.colors = (['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8',
                        'C9'] if colors is None else colors)
        self.markers_shape = (['s', 's', 'H', 'H', 'D', 'D', 'o', 'o', 'X',
                               'X', 'h', 'h', 'P', 'P', '8', '8']
                              if mshape is None else mshape)
        self.markers_fill = ['full', 'none'] if mfill is None else mfill
        self.legends = {} if legends is None else legends

    def styles_sequence(self, indices):
        '''Define the 1D style suite to be used for the 1D plots.

        :param list(int) indices: list of the curves style index
        :rtype: dict
        :returns: dictionary of curve styles indexed by curve index
        '''
        all_fmts = chain((('k', 'o', 'full'),),
                         zip(cycle(self.colors),
                             cycle(self.markers_shape),
                             cycle(self.markers_fill)))
        return dict(zip(indices, all_fmts))


class MplPlotException(Exception):
    '''Error raised if the plot cannot be made.'''


class MplPlot:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib plot.'''

    PTYPES = ('1D', '2D', 'pie', 'bar', 'barstack')

    def __init__(self, data, *, style=None):
        '''Construct a :class:`MplPlot` from the given
        :class:`~.templates.PlotTemplate`.

        Plots are initialized, drawn and finalized in :math:`draw`. Depending
        on the requested type of the subplots, ``ptype`` a 1D or a 2D plot will
        be done. Internal classes are called to draw each kind of available
        plots.

        Available types of plots are stored in the class variable ``PTYPES``.

        No plot for more than 2 dimensions are done.

        :param PlotTemplate data: the data to convert
        :param MplStyle style: the style to be used in the plot
        '''
        self.data = data
        self.style = MplStyle() if style is None else style
        plt.style.use(self.style.style)

    @staticmethod
    def figure_properties(data):
        '''Define figures properties like figsize or the grid specifications.

        :returns: dictionary of keyword arguments directly used by matplotlib
        :rtype: dict
        '''
        hspace = 0.05 if data.suppress_xaxes else 0.4
        splts_kwargs = {'figsize': (6.4, 6.4+2*(data.nb_plots-1)),
                        'gridspec_kw': {'hspace': hspace}}
        if data.small_subplots:
            splts_kwargs['figsize'] = (6.4, 4.8+1.2*(data.nb_plots-1))
            splts_kwargs['gridspec_kw'] = {
                'height_ratios': [4] + [1]*(data.nb_plots-1), 'hspace': hspace}
        if 'pie' in [s.ptype for s in data.subplots]:
            splts_kwargs = {'figsize': (6.4, 4)}
        return splts_kwargs

    def initialize_figure(self):
        '''Construct the figure and its subplots.

        :rtype: tuple(matplotlib.figure.Figure, list(matplotlib.axes.Axes))
        '''
        fig, splts = plt.subplots(
            self.data.nb_plots, **self.figure_properties(self.data),
            constrained_layout=True)
        if self.data.nb_plots == 1:
            splts = [splts]
        return fig, splts

    def finalize_figure(self, splts):
        '''Finalize the figure.

        If ``suppress_xaxes`` is required in **data**, tick labels and label of
        the x-axis will be deleted on all subplots except the last one.

        If ``suppress_legends`` is required in **data**, legends will be
        deleted on all plots except the first one. If only one curve is
        represented in total legend is also deleted.


        :param list(matplotlib.axes.Axes) splts: the subplots
        '''
        for i, splt in enumerate(splts):
            if i != self.data.nb_plots-1 and self.data.suppress_xaxes:
                plt.setp(splt.get_xticklabels(), visible=False)
                splt.set_xlabel('')
            if ((i != 0 and self.data.suppress_legends)
                    or (sum(len(s.curves) for s in self.data.subplots) == 1
                        and self.data.subplots[i].ptype != 'pie')):
                plt.setp(splt.get_legend(), visible=False)

    def draw(self):
        '''Draw the plot.

        :rtype: tuple(matplotlib.figure.Figure, list(matplotlib.axes.Axes))
        '''
        if any(s.ptype not in MplPlot.PTYPES for s in self.data.subplots):
            raise MplPlotException(
                "ptype from {} not taken into account. Expected ones are {}."
                .format([s.ptype for s in self.data.subplots], self.PTYPES))
        fig, splts = self.initialize_figure()
        fmts = self.style.styles_sequence(self.data.curves_index())
        for splt, sdat in zip(splts, self.data.subplots):
            if sdat.ptype == '1D':
                mpl_plot = _MplPlot1D(sdat, self.style)
            elif sdat.ptype == '2D':
                mpl_plot = _MplPlot2D(sdat, self.style)
            elif sdat.ptype == 'pie':
                mpl_plot = _MplPie(sdat, self.style)
            elif sdat.ptype == 'bar':
                mpl_plot = _MplBar(sdat, self.style)
            elif sdat.ptype == 'barstack':
                mpl_plot = _MplBarStack(sdat, self.style)
            mpl_plot.draw(fig, splt, fmts=fmts)
        self.finalize_figure(splts)
        return fig, splts

    def save(self, name='fig.png'):
        '''Save the plot under the given name.

        :param str name: name of the output file. Expected extensions: png,
            pdf, svg, eps.
        '''
        LOGGER.info('drawing figure %s', name)
        fig, _ = self.draw()
        if fig is not None:
            fig.savefig(name)
            plt.close(fig)


class _MplLegend:
    '''Class to store the legend content.'''

    def __init__(self, handle, label, index):
        '''Initialisation of :class:`_MplLegend`.

        :param handle: curve to be stored (if the curve needs to be drawn in
            twice a tuple should be given)
        :type handle: :obj:`matplotlib.pyplot.errorbar`
            or :obj:`tuple` (:obj:`matplotlib.pyplot.errorbar`)
        :param str label: the curve label
        :param int index: curve index, to identify its style
        '''
        self.handle = handle
        self.label = label
        self.index = index


class _MplPlot1D:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib plot.'''

    def __init__(self, data, style=None):
        '''Construct a :class:`_MplPlot1D` from the given
        :class:`~.templates.SubPlotElements`.

        :param SubPlotElements data: the data to convert.
        :param MplStyle style: style to be used in the subplot
        '''
        self.data = data
        self.mpl_style = MplStyle() if style is None else style
        self.legend = []

    def draw(self, _fig, splt, *_args, fmts, **_kwargs):
        '''Draw method.

        :param matplotlib.figure.Figure _fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        :param dict fmts: curves styles
        '''
        self.error_plots(splt, fmts)
        self.customize_plots(splt)

    def ierror_plot(self, splt, curve, data_fmt):
        '''Draw the plot with error bars on the plot (update the plot)

        :param matplotlib.axes.Axes splt: the current subplot
        :param CurveElements curve: data to plot
        :param tuple(str) data_fmt: format of the curve (color, marker shape,
            marker filling)
        '''
        LOGGER.debug("in ierror plot for plot %s on subplot %d",
                     curve.legend, 0)
        if curve.bins[0].size == curve.values.size+1:
            steps = splt.errorbar(
                curve.bins[0], np.append(curve.values, [np.nan]),
                linestyle='-', color=data_fmt[0], drawstyle='steps-post')
            markers = splt.errorbar(
                (curve.bins[0][1:] + curve.bins[0][:-1])/2,
                curve.values, yerr=curve.errors,
                color=data_fmt[0], marker=data_fmt[1], fillstyle=data_fmt[2],
                linestyle='')
            self.legend.append(_MplLegend((steps, markers), curve.legend,
                                          curve.index))
        else:
            eplt = splt.errorbar(
                curve.bins[0], curve.values, yerr=curve.errors,
                linestyle='--', color=data_fmt[0], marker=data_fmt[1],
                fillstyle=data_fmt[2])
            self.legend.append(_MplLegend(eplt, curve.legend, curve.index))

    def error_plots(self, splt, fmts):
        '''Plot errorbar plot (update the pyplot instance) and build the
        legend.

        :param matplotlib.axes.Axes splt: the current subplot
        :param dict fmts: curves styles
        '''
        for crv in self.data.curves:
            self.ierror_plot(splt, crv, fmts[crv.index])
        self._build_legend(splt)

    def _build_legend(self, splt):
        '''Build the legends and add them to the figures.

        An automatic number of columns is calculated, depending on the number
        of curves to be plotted on the subplot. It has been decided to add a
        new columns each 5 curves.

        :param matplotlib.axes.Axes splt: the current subplot
        '''
        ncol = len(self.data.curves) // 6 + 1
        splt.legend([lg.handle for lg in self.legend],
                    [lg.label for lg in self.legend],
                    ncol=ncol, **self.mpl_style.legends)

    def customize_plots(self, splt):
        '''Customize plots (scale, limits and lines).'''
        splt.set_xlabel(self.data.axnames[0])
        splt.set_ylabel(self.data.axnames[1])
        if self.data.curves[0].bins[0].dtype.kind == 'U':
            bmax = max([len(b) for b in self.data.curves[0].bins[0]])
            if bmax * self.data.curves[0].bins[0].size > 60:
                splt.tick_params(axis='x', rotation=90)
        if self.data.attributes.limits is not None:
            splt.set_xlim(*self.data.attributes.limits[0])
        if self.data.attributes.logx:
            splt.set_xscale('log')
        if self.data.attributes.logy:
            splt.set_yscale('log')
        if self.data.attributes.lines:
            xlims, ylims = splt.get_xlim(), splt.get_ylim()
            for line in self.data.attributes.lines:
                if ('x' in line
                        and line['x'] > xlims[0] and line['x'] < xlims[1]):
                    splt.axvline(x=line['x'], c='grey', ls='--', lw=0.5)
                if ('y' in line
                        and line['y'] > ylims[0] and line['y'] < ylims[1]):
                    splt.axhline(y=line['y'], c='grey', ls='--', lw=0.5)


class _MplPlot2D:
    '''Convert a :class:`~.templates.SubPlotElements` into a 2D plot.'''

    def __init__(self, data, style=None):
        '''Construct a :class:`_MplPlot2D` from the given
        :class:`~.templates.SubPlotElements`.

        :param SubPlotElements data: the data to convert.
        :param MplStyle style: style to be used in the subplot
        '''
        LOGGER.debug('initialisation of MplPlot2D')
        self.data = data
        self.mpl_style = MplStyle() if style is None else style

    def draw(self, fig, splt, *_args, **_kwargs):
        '''Draw method.

        Remark: if the quantity represented is required in logarithmic scale,so
        the z-axis in logarithmic scale, it has to be done at the histogram
        declaration and not in the customization step.

        :param matplotlib.figure.Figure fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        self.twod_plots(fig, splt)
        self.customize_plots(splt)

    @staticmethod
    def broadcast_bin_centers(curve):
        '''Calculate bin centers if edges are given and broadcast all bins:
        build the (x, y) grid for all bins.

        :param CurveElements curve: data to plot
        :rtype: numpy.ndarray
        '''
        bins, rsbins = [], []
        for idim, tbin in enumerate(curve.bins):
            shape = ([curve.values.shape[idim]]
                     + [1] * (curve.values.ndim - 1 - idim))
            cbins = ((tbin[1:] + tbin[:-1]) * 0.5
                     if tbin.size == curve.values.shape[idim]+1
                     else tbin)
            if tbin.dtype.kind == 'U':
                cbins = np.arange(tbin.size)+0.5
                bins.append(np.arange(tbin.size+1))
            else:
                bins.append(tbin)
            rsbins.append(np.array(cbins).reshape(shape))
        bbins = np.broadcast_arrays(*rsbins)
        return bbins, bins

    def itwod_plot(self, fig, splt, curve, axnames, norm):
        # pylint: disable=too-many-arguments
        '''Draw the 2D distribution on the ith subplot.

        :param matplotlib.figure.Figure fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        :param CurveElements curve: data to plot
        :param int iplot: number of the subplot
        :param norm: function corresponding to the chosen
            normalisation and scale (linear or logarithmic)
        :type norm: function from :obj:`matplotlib.colors`
        '''
        cbins, bins = self.broadcast_bin_centers(curve)
        h2d = splt.hist2d(
            cbins[0].flatten(), cbins[1].flatten(),
            bins=bins, norm=norm, weights=curve.values.flatten())
        cbar = fig.colorbar(h2d[3], ax=splt)
        splt.set_xlabel(axnames[0])
        if curve.bins[0].dtype.kind == 'U':
            splt.set_xticks(bins[0][:-1]+0.5)
            splt.set_xticklabels(list(curve.bins[0]))
            bmax = max([len(b) for b in self.data.curves[0].bins[0]])
            if bmax * self.data.curves[0].bins[0].size > 60:
                splt.tick_params(axis='x', rotation=90)
        splt.set_ylabel(axnames[1])
        if curve.bins[1].dtype.kind == 'U':
            splt.set_yticks(bins[1][:-1] + 0.5)
            splt.set_yticklabels(curve.bins[1])
        cbar.set_label(axnames[2])
        if curve.legend:
            splt.set_title(curve.legend)

    def twod_plots(self, fig, splt):
        '''Build 2D plots.

        :param matplotlib.figure.Figure fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        for crv in self.data.curves:
            self.itwod_plot(
                fig, splt, crv, self.data.axnames,
                norm=(mplcol.LogNorm() if self.data.attributes.logz
                      else mplcol.Normalize()))

    def customize_plots(self, splt):
        '''Customize plots (scale and limit).

        :param matplotlib.figure.Figure fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        if self.data.attributes.limits is not None:
            splt.set_xlim(*self.data.attributes.limits[0])
            splt.set_ylim(*self.data.attributes.limits[1])
        if self.data.attributes.logx:
            splt.set_xscale('log')
        if self.data.attributes.logy:
            splt.set_yscale('log')
        if self.data.curves[0].bins[0].dtype.kind == 'U':
            bmax = max([len(b) for b in self.data.curves[0].bins[0]])
            if bmax * self.data.curves[0].bins[0].size > 60:
                splt.tick_params(axis='x', rotation=90)


class _MplPie:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib pie chart.
    '''

    def __init__(self, data, _style=None):
        '''Construct a :class:`_MplPie` from the given
        :class:`~.templates.SubPlotElements`.

        :param SubPlotElements data: the data to convert.
        :param MplStyle style: style to be used in the subplot
        '''
        self.data = data
        self.fig, self.splt = None, None

    def draw(self, _fig, splt, *_args, **_kwargs):
        '''Draw method.

        :param matplotlib.figure.Figure _fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        self.pie_chart(splt)

    def pie_chart(self, splt):
        '''Prepare the pie chart.

        :param matplotlib.axes.Axes splt: the current subplot
        '''
        curve = self.data.curves[0]
        wedges, _, _ = splt.pie(curve.values, autopct='%1.1f%%')
        splt.set_title(self.data.axnames[0])
        splt.legend(wedges, curve.bins[0],
                    loc='center right', bbox_to_anchor=(1.3, 0.5),
                    title=self.data.axnames[1])


class _MplBar:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib bar plot.
    '''

    def __init__(self, data, _style=None):
        '''Construct a :class:`_MplBar` from the given
        :class:`~.templates.SubPlotElements`.

        :param SubPlotElements data: the data to convert.
        :param MplStyle style: style to be used in the subplot
        '''
        self.data = data

    def draw(self, _fig, splt, *_args, **_kwargs):
        '''Draw method.

        :param matplotlib.figure.Figure _fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        self.bar_plot(splt)

    def bar_plot(self, splt):
        '''Prepare the bar plot.'''
        nb_curves = len(self.data.curves)
        width = 0.8 / nb_curves
        x = np.arange(self.data.curves[0].values.size)
        bot = np.zeros_like(self.data.curves[0].values)
        for icrv, curve in enumerate(self.data.curves):
            splt.bar(x + (icrv-(nb_curves-1)/2)*width, curve.values, width,
                     label=curve.legend)
            bot += curve.values
        splt.set_xlabel(self.data.axnames[0])
        splt.set_ylabel(self.data.axnames[1])
        splt.set_xticks(x)
        splt.set_xticklabels(self.data.curves[0].bins[0])
        splt.legend()


class _MplBarStack:
    '''Convert a :class:`~.templates.PlotTemplate` into a matplotlib bar plot.
    '''

    def __init__(self, data, _style=None):
        '''Construct a :class:`_MplBarStack` from the given
        :class:`~.templates.SubPlotElements`.

        :param SubPlotElements data: the data to convert.
        :param MplStyle style: style to be used in the subplot
        '''
        self.data = data

    def draw(self, _fig, splt, *_args, **_kwargs):
        '''Draw method.

        :param matplotlib.figure.Figure _fig: the current figure
        :param matplotlib.axes.Axes splt: the current subplot
        '''
        self.bar_plot(splt)

    def bar_plot(self, splt):
        '''Prepare the bar plot.'''
        nb_curves = len(self.data.curves)
        width = 0.8 / nb_curves
        bot = np.zeros_like(self.data.curves[0].values)
        for curve in self.data.curves:
            splt.bar(self.data.curves[0].bins[0], curve.values,
                     width*nb_curves, label=curve.legend, bottom=bot)
            bot += curve.values
        splt.set_xlabel(self.data.axnames[0])
        splt.set_ylabel(self.data.axnames[1])
        splt.legend()
