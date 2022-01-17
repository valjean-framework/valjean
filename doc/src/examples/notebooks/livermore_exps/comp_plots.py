import matplotlib.pyplot as plt

class CompPlot():
    '''Comparison plot class'''

    def __init__(self, charac):
        self.charac = charac
        self.fig, self.splt = plt.subplots(
            2, sharex=True, figsize=(15, 8),
            gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
        self.legend = {'curves': [], 'labels': [], 'flag': []}
        self.nbins = {'exp': 0, 't4': 0, 'mcnp': 0}

    def customize_plot(self):
        '''Customize plot: axis labels, title, scale and legend.
        '''
        self.splt[0].set_yscale("log", nonpositive='clip')
        self.splt[0].set_title(f'{self.charac[0].capitalize()}, '
                               f'{self.charac[1]} mfp, detector at '
                               f'{self.charac[2]}°')
        # self.splt[0].set_ylabel("N cnt rate [1/(ns.source)]", labelpad=40)
        self.splt[0].set_ylabel("Neutron count rate [1/(ns.source)]")
        self.splt[0].set_ylim(ymin=2e-4)
        self.splt[1].set_ylim(ymin=0.8, ymax=1.2)
        self.splt[1].set_yscale("log", nonpositive='clip')
        # self.splt[1].set_yticks([], minor=True)
        self.splt[1].set_yticklabels([], minor=True)
        self.splt[1].set_yticks([0.8, 1, 1.2])
        # self.splt[1].set_yticks([0.4, 1, 2], minor=True)
        self.splt[1].set_yticklabels(["0.8", "1", "1.2"])
        self.splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
        self.splt[1].set_xlabel("Time [ns]")
        self.splt[1].set_ylabel("C/E")
        self.splt[0].legend(self.legend['curves'], self.legend['labels'],
                            markerscale=2)  #, fontsize=12
        # self.splt[1].legend(loc='lower right')

    def add_errorbar_plot(self, bins, vals, errors, label='', slab='',
                          **kwargs):
        # pylint: disable=too-many-arguments
        '''Add an error bar plot to the figure on subplot 0.

        :param :obj:`numpy.ndarray` bins: x-axis bins
        :param :obj:`numpy.ndarray` vals: values (corresponding to y-axis)
        :param :obj:`numpy.ndarray` errors: y-errors
        :param str label: plot label in the legend, default = ``''``
        :param str slab: plot short label or flag (for ratio), default = ``''``
          but set to label in plotting methods (see :meth:plot_t4 or
          :meth:plot_mcnp)
        :param kwargs: plotting kewords arguments, directly sent ot matplotlib,
          see `errbar`_ for the full list.
        :returns: nothing, plot the curve on subplot[0], save it and its labels
        '''
        # possibility to remove slab and put it in kwargs, but less obvious
        # would need to append labels before curve and pop it
        # print("kwargs: %s", kwargs)
        tmp_curve = self.splt[0].errorbar(
            bins, vals, yerr=errors, **kwargs)
        self.legend['curves'].append(tmp_curve)
        self.legend['labels'].append(label)
        self.legend['flag'].append(slab)

    def add_errorbar_ratio(self, bins, vals, errors, **kwargs):
        '''Add ratio on subplot 1.

        :param :obj:`numpy.ndarray` bins: x-axis bins
        :param :obj:`numpy.ndarray` vals: values (corresponding to y-axis)
        :param :obj:`numpy.ndarray` errors: y-errors
        :param kwargs: plotting kewords arguments, directly sent ot matplotlib,
          see `errbar`_ for the full list.
        :returns: nothing, plot the curve on subplot[1]
        '''
        # print("kwargs (ratio): %s", kwargs)
        self.splt[1].errorbar(bins, vals, yerr=errors, **kwargs)


class ExtendedCompPlot():
    '''Comparison plot class'''

    def __init__(self, charac):
        self.charac = charac
        self.fig, self.splt = plt.subplots(
            3, sharex=True, figsize=(15, 12),
            gridspec_kw={'height_ratios': [4, 1, 1], 'hspace': 0.05})
        self.legend = {'curves': [], 'labels': [], 'flag': []}
        self.nbins = {'exp': 0, 't4': 0, 'mcnp': 0}

    def customize_plot(self):
        '''Customize plot: axis labels, title, scale and legend.
        '''
        self.splt[0].set_yscale("log", nonpositive='clip')
        self.splt[0].set_title(f'{self.charac[0].capitalize()}, '
                               f'{self.charac[1]} mfp, detector at '
                               f'{self.charac[2]}°')
        # self.splt[0].set_ylabel("N cnt rate [1/(ns.source)]", labelpad=40)
        self.splt[0].set_ylabel("Neutron count rate [1/(ns.source)]")
        self.splt[0].set_ylim(ymin=2e-4)
        self.splt[1].set_ylim(ymin=0.8, ymax=1.2)
        self.splt[1].set_yscale("log", nonpositive='clip')
        # self.splt[1].set_yticks([], minor=True)
        self.splt[1].set_yticklabels([], minor=True)
        self.splt[1].set_yticks([0.8, 1, 1.2])
        # self.splt[1].set_yticks([0.4, 1, 2], minor=True)
        self.splt[1].set_yticklabels(["0.8", "1", "1.2"])
        self.splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
        self.splt[1].set_ylabel("C/E")
        # self.splt[2].set_ylim(ymin=0.8, ymax=1.2)
        # self.splt[2].set_yscale("log", nonpositive='clip')
        # self.splt[2].set_yticks([], minor=True)
        # self.splt[2].set_yticklabels([], minor=True)
        # self.splt[2].set_yticks([0.8, 1, 1.2])
        # self.splt[1].set_yticks([0.4, 1, 2], minor=True)
        # self.splt[2].set_yticklabels(["0.8", "1", "1.2"])
        # self.splt[2].axhline(y=1, ls='--', lw=0.5, color='grey')
        self.splt[2].set_xlabel("Time [ns]")
        self.splt[2].set_ylabel(r"t_{\text{Student}}")
        self.splt[2].axhline(y=2.5755, ls='--', lw=0.5, color='red')
        self.splt[2].axhline(y=-2.5755, ls='--', lw=0.5, color='red')
        self.splt[2].axhline(y=1.960, ls='--', lw=0.5, color='green')
        self.splt[2].axhline(y=-1.960, ls='--', lw=0.5, color='green')
        self.splt[0].legend(self.legend['curves'], self.legend['labels'],
                            markerscale=2)  #, fontsize=12
        # self.splt[1].legend(loc='lower right')

    def add_errorbar_plot(self, bins, vals, errors, label='', slab='',
                          **kwargs):
        # pylint: disable=too-many-arguments
        '''Add an error bar plot to the figure on subplot 0.

        :param :obj:`numpy.ndarray` bins: x-axis bins
        :param :obj:`numpy.ndarray` vals: values (corresponding to y-axis)
        :param :obj:`numpy.ndarray` errors: y-errors
        :param str label: plot label in the legend, default = ``''``
        :param str slab: plot short label or flag (for ratio), default = ``''``
          but set to label in plotting methods (see :meth:plot_t4 or
          :meth:plot_mcnp)
        :param kwargs: plotting kewords arguments, directly sent ot matplotlib,
          see `errbar`_ for the full list.
        :returns: nothing, plot the curve on subplot[0], save it and its labels
        '''
        # possibility to remove slab and put it in kwargs, but less obvious
        # would need to append labels before curve and pop it
        # print("kwargs: %s", kwargs)
        tmp_curve = self.splt[0].errorbar(
            bins, vals, yerr=errors, **kwargs)
        self.legend['curves'].append(tmp_curve)
        self.legend['labels'].append(label)
        self.legend['flag'].append(slab)

    def add_errorbar_ratio(self, bins, vals, errors, **kwargs):
        '''Add ratio on subplot 1.

        :param :obj:`numpy.ndarray` bins: x-axis bins
        :param :obj:`numpy.ndarray` vals: values (corresponding to y-axis)
        :param :obj:`numpy.ndarray` errors: y-errors
        :param kwargs: plotting kewords arguments, directly sent ot matplotlib,
          see `errbar`_ for the full list.
        :returns: nothing, plot the curve on subplot[1]
        '''
        # print("kwargs (ratio): %s", kwargs)
        self.splt[1].errorbar(bins, vals, yerr=errors, **kwargs)

    def add_student(self, bins, vals, **kwargs):
        '''Add ratio on subplot 1.

        :param :obj:`numpy.ndarray` bins: x-axis bins
        :param :obj:`numpy.ndarray` vals: values (corresponding to y-axis)
        :param :obj:`numpy.ndarray` errors: y-errors
        :param kwargs: plotting kewords arguments, directly sent ot matplotlib,
          see `errbar`_ for the full list.
        :returns: nothing, plot the curve on subplot[1]
        '''
        # print("kwargs (ratio): %s", kwargs)
        # self.splt[2].hist(vals, bins, **kwargs)
        # self.splt[2].hist(vals, bins=bins, **kwargs)
        self.splt[2].plot(bins, vals, **kwargs)
