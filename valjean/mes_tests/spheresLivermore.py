'''VV of Livermore spheres: comparison to experiment and between various
results (change in nuclear data, T4, MCNP, SCALE, ...)

.. errbar_: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.errorbar.html
'''

import ast
from collections import namedtuple
import logging
import numpy as np
from valjean.eponine.parse_t4 import T4Parser
import matplotlib.pyplot as plt

Histo = namedtuple('Histo', ['tbins', 'vals', 'sigma'])
Integral = namedtuple('Integral', ['value', 'sigma'])

LOGGER = logging.getLogger('valjean')


class LivermoreSphere():
    '''Class to study Livermore Spheres.'''

    def __init__(self, jdd, short_name, charac=None):
        self.name = (short_name, jdd)
        self.characteristics = charac
        self.parsed_res = T4Parser.parse_jdd(jdd, -1).result
        self.spectrum = None
        self.integrated = None
        # self.add_result(jdd, ast.literal_eval(responses))

    def set_result(self, responses):
        '''Fill results for the considered sphere from given responses.'''
        LOGGER.info("nbre de responses: %d",
                    len(self.parsed_res[-1]['list_responses']))
        if not isinstance(responses, list):
            LOGGER.debug("No response or not a list")
            self.add_default_result()
        else:
            if len(responses) == 1:
                self.add_default_result()
            else:
                if isinstance(responses[0], int):
                    LOGGER.debug("First response is an int")
                    self.add_result_from_ints(responses)
                else:
                    LOGGER.debug("First response should be a string")
                    self.add_result_from_score_names(responses)

    def add_default_result(self):
        '''Get default results for the responses.'''
        LOGGER.debug("in add_default_result")
        spec_resp = self.parsed_res[-1]['list_responses'][0]
        score_res = spec_resp['results']['score_res']
        LOGGER.debug("Check: number of scores = %d", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        LOGGER.debug("KEYS: %s", str(list(self.spectrum.keys())))
        integ_resp = self.parsed_res[-1]['list_responses'][1]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']
        return

    def add_result_from_ints(self, responses):
        '''Get results from index of the responses.'''
        LOGGER.debug("add_result_from_ints")
        allresp = self.parsed_res[-1]['list_responses']
        spec_resp = allresp[responses[0]]
        score_res = spec_resp['results']['score_res']
        LOGGER.debug("Check: number of scores = %d", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        integ_resp = allresp[responses[1]]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']

    def add_result_from_score_names(self, responses):
        '''Get results from the score name.'''
        LOGGER.debug("add_result_from_score_names")
        allresp = self.parsed_res[-1]['list_responses']
        corr_names = dict(
            map(lambda xy: (xy[1]['response_description']['score_name'],
                            xy[0]),
                enumerate(allresp)))
        LOGGER.debug(corr_names)
        spec_resp = allresp[corr_names[responses[0]]]
        score_res = spec_resp['results']['score_res']
        LOGGER.debug("Check: number of scores = %s", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        integ_resp = allresp[corr_names[responses[1]]]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']


class SpherePlot():
    '''Class to build plot for Livermore spheres from one sphere and associated
    air input.
    '''

    def __init__(self, jdd_sphere, jdd_air):
        LOGGER.info("Parsing %s", jdd_sphere)
        self.sphere = LivermoreSphere(jdd_sphere, "Sphere")
        LOGGER.info("Parsing %s", jdd_air)
        self.air = LivermoreSphere(jdd_air, "Air")

    def normalized_sphere(self, responses):
        '''Normalise T4 sphere results to air ones.

        :param list responses: index or str identifiers of response to be
          used. First one = sphere, second one = air.
        :returns: Histo of the normalised sphre (tbins, values, sigma).
        '''
        LOGGER.info("Set sphere results")
        self.sphere.set_result(responses)
        LOGGER.info("Set air results")
        self.air.set_result(responses)
        spectrum = self.sphere.spectrum['spectrum']
        normalization = self.air.integrated['integrated_res']
        norm_spec = spectrum['score']/normalization['score'].ravel()[0]
        norm_spec_sig = spectrum['sigma']*norm_spec/100.
        # removing first and last bins as irrelevant here
        return Histo(self.sphere.spectrum['tbins'][1:-1]*1e9,
                     norm_spec.ravel()[1:-1],
                     norm_spec_sig.ravel()[1:-1])

    def plot_sphere(self):
        '''Test to plot T4 results.'''
        spectrum, spec_err = self.normalized_sphere([0, 1])
        # spectrum = self.sphere.spectrum['spectrum']['score']
        print(spectrum.shape)
        print(spectrum.ravel())
        tbins = np.arange(spectrum.shape[4])
        # print(self.sphere.spectrum['tbins'])
        print("my tbins=", tbins.shape)
        print(self.sphere.spectrum['tbins'].shape)
        # middle of bins
        tbinle = self.sphere.spectrum['tbins'][:-1]
        tbinhe = self.sphere.spectrum['tbins'][1:]
        # print(tbinle)
        # print(tbinhe)
        mtbins = (tbinle+tbinhe)/2
        # print(mtbins)
        print(mtbins.shape)
        print(spectrum.ravel().shape)
        print("mtbins:")
        print(mtbins)
        plt.figure(1)
        plt.subplot(111)
        # plt.hist(tbins[1:-1], bins=mtbins[1:-1],
        #          weights=spectrum.ravel()[1:-1], color='c')
        plt.hist(mtbins[1:-1]*1e9, bins=mtbins[1:-1]*1e9,
                 weights=spectrum.ravel()[1:-1], color='c')
        plt.xlabel("time bins [ns]")
        plt.yscale("log", nonposy='clip')
        # plt.ylim(1e-5)
        plt.figure(2)
        plt.subplot(111)
        plt.errorbar(mtbins[1:-1]*1e9, spectrum.ravel()[1:-1],
                     yerr=spec_err.ravel()[1:-1])
        plt.xlabel("time bins [ns]")
        plt.yscale("log", nonposy='clip')
        plt.show()


class LivermoreExps():
    '''Class to read experimental results from Livermore sphere (same file as
    in fortran tests.
    '''

    def __init__(self, path=("/data/tmplepp/el220326/QualTassadit/RC1/"
                             "MONO/qualtrip_main/elem/post_processing_main/"
                             "s10a11.res.mesure")):
        self.fname = path
        self.res = {}
        self.read_results()
        LOGGER.info("ALL KEYS:\n%s", list(self.res.keys()))

    def read_results(self):
        '''Read experimental results and stored them in dict as
        :obj:`numpy.ndarray`.
        '''
        charac = None
        results = None
        print(self.fname)
        with open(self.fname) as fil:
            for line in fil:
                if "MFP" in line or not line.split():
                    if charac:
                        print(charac)
                        self.save_res(charac, results)
                    charac = None
                    results = None
                    lelts = line.split()
                    charac = lelts[:-1]
                elif "DEGRES" in line:
                    charac.append(line.split()[1])
                # elif "FP=" in line:
                #     charac.append(line.split()[1])
                elif "TEMPS" in line and "TO" in line:
                    results = []
                elif "CNT" in line or "prob" in line or "FP=" in line:
                    continue
                else:
                    elts = line.split()
                    results.append(tuple(map(ast.literal_eval, elts)))

    def save_res(self, charac, results):
        '''Fill the internal dictionary for experimental results.

        ``{charac: results}``,
        with charac a tuple (element, thickness in mfp, detector angle)
        and results a :obj:`numpy.ndarray` with dtype:  ``[('time', int),
        ('cntPtimePsource', float), ('error', float), ('cntCum', float)]``
        '''
        # pylint: disable=no-member
        dtype = np.dtype({
            'names': ['time', 'cntPtimePsource', 'error', 'cntCum'],
            'formats': [np.int32, np.float32, np.float32, np.float32]})
        self.res[tuple(charac)] = np.array(results, dtype=dtype)

    def plot_res(self, charac):
        '''Plot experimental results for charac.

        :param tuple charac: (element, thickness in mfp, detector angle)
        :returns: matplotlib window with the required plot
        '''
        plt.figure(1)
        plt.subplot(111)
        plt.errorbar(self.res[charac]['time'],
                     self.res[charac]['cntPtimePsource'],
                     yerr=self.res[charac]['error'],
                     fmt='none')
        plt.xlabel("time bins [ns]")
        plt.yscale("log", nonposy='clip')
        plt.show()


class MCNPSphere():
    '''Class to read MCNP outputs.
    Par contre pour le moment les seuls que j'ai sont les donnees
    experimentales (que j'ai aussi grace a T4 !).
    '''

    def __init__(self, path, charac):
        self.fname = path
        self.charac = charac
        self.histo = None
        self.integral = None
        self.read_mcnp()

    def read_mcnp(self):
        '''Read MCNP results and fill its histo and integral.

        Time bins are multiplied by 10 to convert shakes to ns (...).
        Results are presented in a table of value sigma value sigma... on N
        lines, where N(values) > N(time bins+1). The value corresponding to the
        (Ntbins+1)th one is the integral, followed by its σ. Values and σ
        :obj:`numpy.ndarray` are cut to Nbins to only keep relevant numbers.

        Remark: ntbins = number of edges and not of bins, so Nbins+1. The
        comment above takes into account the fact that indexes start at 0...
        '''
        nb_tbins = 0
        tbins_block = False
        vals_block = False
        tbins, counts = [], []
        with open(self.fname) as fil:
            for line in fil:
                if line.startswith('tt') or line.startswith('tc'):
                    nb_tbins = line.split()[1]
                    tbins_block = True
                elif line.startswith('vals'):
                    tbins_block = False
                    vals_block = True
                elif line.startswith('tfc'):
                    vals_block = False
                elif tbins_block:
                    tbins += line.split()
                elif vals_block:
                    counts += [float(x) for x in line.split()]
                else:
                    continue
        nbtbins = len(tbins)
        LOGGER.debug("len(tbins) = %d et vals: %d, Ntbins = %s",
                     len(tbins), len(counts), nb_tbins)
        LOGGER.debug(tbins)
        tbins = np.array([float(x) for x in tbins])*10
        sigma = np.array(
            [x for ind, x in enumerate(counts) if ind % 2 != 0])
        counts = np.array(
            [x for ind, x in enumerate(counts) if ind % 2 == 0])
        sigma = sigma*counts
        self.integral = Integral(counts[nbtbins], sigma[nbtbins])
        self.histo = Histo(tbins, counts[:nbtbins], sigma[:nbtbins])


class MCNPrenormalizedSphere():
    '''Class to buld renormalized spheres for MCNP.'''

    def __init__(self, out_sphere, out_air):
        LOGGER.info("Get results for the MCNP sphere")
        self.sphere = MCNPSphere(out_sphere, "Sphere")
        self.air = MCNPSphere(out_air, "Air")
        self.histo = self.normalized_sphere()
        LOGGER.debug("Renormalized counts: %s", str(self.histo.vals))

    def normalized_sphere(self):
        '''Normalize sphere for MCNP results from sphere and air results.
        :returns: Histo named tuple (tbins, vals, sigma)
        '''
        counts = self.sphere.histo.vals/self.air.integral.value
        sigma = self.sphere.histo.sigma/self.air.integral.value
        tbins = self.sphere.histo.tbins
        return Histo(tbins, counts, sigma)


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
        self.splt[0].set_yscale("log", nonposy='clip')
        self.splt[0].set_title("{elt}, {mfp} mfp, detector at {deg}°"
                               .format(elt=self.charac[0].capitalize(),
                                       mfp=self.charac[1],
                                       deg=self.charac[2]))
        self.splt[0].set_ylabel("neutron count rate [1/(ns.source)]")
        self.splt[0].set_ylim(ymin=2e-4)
        self.splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
        self.splt[1].set_xlabel("time bins [ns]")
        self.splt[1].set_ylabel("Ratios")
        # self.splt[1].set_ylim(ymin=0.5, ymax=1.5)
        self.splt[0].legend(self.legend['curves'], self.legend['labels'],
                            markerscale=2, fontsize=12)
        self.splt[1].legend(loc='upper right')

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
        LOGGER.debug("kwargs: %s", kwargs)
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
        LOGGER.debug("kwargs (ratio): %s", kwargs)
        self.splt[1].errorbar(bins, vals, yerr=errors, **kwargs)


class Comparison():
    '''Class to compare, using matplotlib, experiment and Tripoli-4 results.'''
    NORM_FACTOR = 2
    TIME_SHIFT = 0

    def __init__(self):
        self.exp_res = LivermoreExps()
        self.simu_res = {}
        self.mcnp_res = {}

    def set_t4_files(self, jdds):
        '''Set the TRIPOLI-4 files and call parsing.
        This method can be called more than once.

        :param list(tuple) jdds: ``[('NAME', 'path'), ...]``
          ``'NAME'``: identifier of the file (can contain more than one result)
          ``'path'``: path to the file. CAUTION, this is NOT a real path:
          filename is modified. Instead of sphere or air, please use SPHAIR,
          both files will be automatically read and used to build the
          renormalised sphere.
        :returns: nothing, fill the internal dict of T4 results
        '''
        for name, jdd in jdds:
            self.simu_res[name] = SpherePlot(jdd.replace("SPHAIR", "sphere"),
                                             jdd.replace("SPHAIR", "air"))

    def set_mcnp_files(self, jdds):
        '''Set the MCNP files containing the results to be used.
        This method can be used more than once.

        :param list(tuple) jdds: ``[('NAME', 'path', renormalisation), ...]``
          ``'NAME'``: identifier of the file (string)
          ``'path'``: path to the file (norminal material)
          ``renormalisation``: boolean, True if it has to be done (2 files read
          in that case, sphere and air), False if already normalised.
        :returns: nothing, fill the internal dict of MCNP results
        '''
        for name, jdd, renorm in jdds:
            if renorm:
                LOGGER.info("Read MCNP results for sphere %s and air %s_airm",
                            jdd, jdd[:-1])
                self.mcnp_res[name] = MCNPrenormalizedSphere(jdd,
                                                             jdd[:-1]+"_airm")
            else:
                LOGGER.info("Read MCNP results for %s", jdd)
                self.mcnp_res[name] = MCNPSphere(jdd, name)

    def plot_exp(self, charac, cplot):
        '''Plot experimental data points (directly on the subplot as 1 and 2 σ
        error bars are represented).

        :param tuple charac: identification of experimental data
          (see :meth:compare_plots)
        :param CompPlot cplot: current figure and subplots
        :returns: (nothing, updated plot)
        '''
        exp2sig = cplot.splt[0].errorbar(
            self.exp_res.res[charac]['time'],
            self.exp_res.res[charac]['cntPtimePsource'],
            yerr=self.exp_res.res[charac]['error']*2,
            fmt='s', ms=3, ecolor='orange', c='orange')
        exp1sig = cplot.splt[0].errorbar(
            self.exp_res.res[charac]['time'],
            self.exp_res.res[charac]['cntPtimePsource'],
            yerr=self.exp_res.res[charac]['error'],
            fmt='rs', ms=1, ecolor='r')
        LOGGER.debug("[1;31mExp. first t bin: %d[0m",
                     self.exp_res.res[charac]['time'][0])
        cplot.legend['curves'].append((exp2sig, exp1sig))
        cplot.legend['labels'].append("Experiment")
        cplot.legend['flag'].append("exp")
        cplot.nbins['exp'] = self.exp_res.res[charac]['time'].shape[0]

    def plot_t4(self, responses, cplot):
        '''Plot TRIPOLI-4 results.

        :param dict responses: T4 results (see :meth:compare_plots)
        :param CompPlot cplot: current figure and subplots
        :returns: (nothing, updated plot)
        '''
        cols = ['b', 'g', 'm', 'darkviolet', 'orchid', 'darkmagenta',
                'dodgerblue', 'b', 'g', 'm', 'b', 'g', 'm', 'b', 'g', 'm',
                'b', 'g', 'm', 'b', 'g', 'm','b', 'g', 'm', 'b', 'g', 'm']
        LOGGER.info("Number of responses required: %d", len(responses))
        LOGGER.debug("[32mResponses: %s[0m", responses)
        for ires, (sname, simres) in enumerate(self.simu_res.items()):
            LOGGER.info("[94mName of the sample %d: %s[0m", ires, sname)
            if sname not in responses:
                continue
            norm_simu = simres.normalized_sphere(responses[sname])
            # remove first bin edge as 1 edge more than bins (normal)
            mtbins = norm_simu.tbins[1:] - 1
            t4vals = norm_simu.vals/Comparison.NORM_FACTOR
            t4sigma = norm_simu.sigma/Comparison.NORM_FACTOR
            LOGGER.debug("[1;31mT4%s first t bin: %f[0m", sname, mtbins[0])
            resp_args = (responses[sname][2:][0] if len(responses[sname]) > 2
                         else {})
            resp_args.setdefault('fmt', '-')
            resp_args.setdefault('label', sname)
            resp_args.setdefault('slab', sname)
            print(resp_args)
            resp_args.setdefault('c', resp_args.pop('color', cols[ires]))
            resp_args.setdefault('ecolor', resp_args.get('c', cols[ires]))
            LOGGER.debug("T4 plot args:%s", resp_args)
            cplot.add_errorbar_plot(mtbins, t4vals, t4sigma, **resp_args)

    def plot_mcnp(self, mcnp, cplot):
        '''Plot MCNP results.

        :param mcnp: MCNP results (see :meth:compare_plots)
        :type mcnp: dict or list
        :param CompPlot cplot: current figure and subplots
        :returns: (nothing, updated plot)
        '''
        for sname in self.mcnp_res:
            if sname not in mcnp:
                continue
            mtbins = self.mcnp_res[sname].histo.tbins - 1
            mcnp_vals = np.copy(self.mcnp_res[sname].histo.vals)
            mcnp_sigma = np.copy(self.mcnp_res[sname].histo.sigma)
            # isinstance only works the first time with autoreload
            # if isinstance(self.mcnp_res[sname], MCNPrenormalizedSphere):
            if hasattr(self.mcnp_res[sname], 'sphere'):
                LOGGER.debug("Renormalised sphere")
                mcnp_vals /= Comparison.NORM_FACTOR
                mcnp_sigma /= Comparison.NORM_FACTOR
            mcnp_args = mcnp[sname] if isinstance(mcnp, dict) else {}
            mcnp_args.setdefault('c', 'c')
            mcnp_args.setdefault('label', "MCNP")
            mcnp_args.setdefault('slab', "MCNP")
            cplot.add_errorbar_plot(mtbins, mcnp_vals, mcnp_sigma, **mcnp_args)

    def plot_ratios(self, ratios, cplot):
        '''Plot required ratios.

        :param dict(str, list) ratios: list of short labels, then optional dict
                                       for line style (sent as kwargs)
        :param CompPlot cplot: plot on which adding the ratio
        :returns: (nothing: updated plot)
        '''
        for leg, ratio in ratios.items():
            LOGGER.debug("Ratio: %s", leg)
            # sanity check
            if len([fl for fl in ratio if fl in cplot.legend['flag']]) != 2:
                LOGGER.warning("Wrong flag, possibilities are %s:",
                               cplot.legend['flag'])
                continue
            flagn = cplot.legend['flag'].index(ratio[0])
            num = cplot.legend['curves'][flagn].lines[0].get_data()[1]
            flagd = cplot.legend['flag'].index(ratio[1])
            denom = (self.exp_res.res[cplot.charac]['cntPtimePsource']
                     if 'exp' in ratio
                     else cplot.legend['curves'][flagd].lines[0].get_data()[1])
            # check number of bins and buts if necessary
            cutnf, cutnl, cutd = 0, num.shape[0], 0
            binsn = cplot.legend['curves'][flagn].lines[0].get_data()[0]
            binsd = (self.exp_res.res[cplot.charac]['time']
                     if 'exp' in ratio
                     else cplot.legend['curves'][flagd].lines[0].get_data()[0])
            if num.shape != denom.shape:
                LOGGER.debug("Something has to be done for number of bins")
                LOGGER.debug("num: %d, denom: %d",
                             num.shape[0], denom.shape[0])
                if num.shape > denom.shape:
                    LOGGER.debug("tbinN-tbinD = %f", binsn[0]-binsd[0])
                    if np.isclose(binsn[0]-binsd[0], -2):
                        cutnf = num.shape[0] - denom.shape[0]
                    else:
                        cutnl = denom.shape[0]
                else:
                    cutd = denom.shape[0] - num.shape[0]
            # check on first time bin value
            if not np.isclose(binsn[cutnf:][0], binsd[cutd:][0]):
                LOGGER.warning("First time bins are not the same: "
                               "num = %f, denom = %f",
                               binsn[cutnf:][0], binsd[cutd:][0])
            ratio_args = ratio[2] if len(ratio) > 2 else {}
            cplot.add_errorbar_ratio(binsn[cutnf:cutnl],
                                     num[cutnf:cutnl]/denom[cutd:],
                                     0, label=leg, **ratio_args)

    def compare_plots(self, charac, responses, mcnp=None, ratios=None,
                      save_file=None):
        '''Compare plots for Livermore spheres (data from experiment, T4 and
        MCNP possible).

        :param tuple charac: (element, thickness in mfp, detector angle) as
          used to identify experimental data. If a 4th item ``'False'`` is
          added, experimental points won't be drawn.
        :param dict responses: T4 data,
          ``{'NAME': "[RESP_SPECTRUM, RESP_INTEGRAL, opt]"}``.
          ``'NAME'`` = name used to identify the file,
          ``RESP_SPECTRUM, RESP_INTEGRAL`` = identifier of the response, can be
          a string (new jdds) or the response number
          ``opt`` = optional dictionary with kwargs for the plot, label in the
          legend and slab = short label or flag used to identify the plot in
          order to use it in ratios
        :param dict mcnp: MCNP data, ``{'NAME': dict of kwargs}
          If no dict of kwargs is needed (so no specifications on plotting or
          labels), a list can be used, ``['NAME']``.
        :param dict ratios: ``{'LABEL': ['FLAG_NUM', 'FLAG_DENOM', opt]}``
          ``'LABEL'``: label of the ratio (per default in legend)
          ``'FLAG_NUM', 'FLAG_DENOM'``: flag of the numerator and denominator,
          ``'exp'`` can be used for experiment (else ``'Experiment'``), slab is
          used for T4 and MCNP
          ``opt``: optional kwargs for the ratio plot
        mcnp and ratios are optional, responses (to T4 data) can be empty.
        :returns: the plot !
        '''
        complot = CompPlot(charac)
        if charac[-1] is not False:
            self.plot_exp(charac, complot)
        self.plot_t4(responses, complot)
        if mcnp:
            self.plot_mcnp(mcnp, complot)
        if ratios:
            self.plot_ratios(ratios, complot)
        complot.customize_plot()
        if save_file:
            plt.savefig(save_file)
        else:
            plt.show()
