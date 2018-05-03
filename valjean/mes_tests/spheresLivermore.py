'''VV of Livermore spheres: comparison to experiment and between various
results (change in nuclear data, T4, MCNP, SCALE, ...)'''

from valjean.eponine.parse_t4 import T4Parser
import valjean.eponine.pyparsing_t4.transform as trans
import numpy as np
import ast
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class LivermoreSphere():
    '''Class to study Livermore Spheres.'''

    def __init__(self, jdd, short_name, charac=None):
        self.name = (short_name, jdd)
        self.characteristics = charac
        self.parsed_res = T4Parser.parse_jdd(jdd, -1).result
        self.spectrum = None
        self.integrated = None
        # self.add_result(jdd, ast.literal_eval(responses))

    def set_result(self, response):
        responses = ast.literal_eval(response)
        print("nbre de responses:", len(self.parsed_res[-1]['list_responses']))
        if not isinstance(responses, list):
            print("No response or not a list")
            self.add_default_result()
        else:
            if len(responses) == 1:
                self.add_default_result()
            else:
                if isinstance(responses[0], int):
                    print("First response is an int")
                    self.add_result_from_ints(responses)
                else:
                    print("First response should be a string")
                    self.add_result_from_score_names(responses)

    def add_default_result(self):
        print("in add_default_result")
        spec_resp = self.parsed_res[-1]['list_responses'][0]
        print(list(spec_resp.keys()))
        print(list(spec_resp['response_description'].keys()))
        score_res = spec_resp['results']['score_res']
        print("Check: number of scores =", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        print(list(self.spectrum.keys()))
        integ_resp = self.parsed_res[-1]['list_responses'][1]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']
        # print(self.integrated)
        return

    def add_result_from_ints(self, responses):
        print("add_result_from_ints")
        allresp = self.parsed_res[-1]['list_responses']
        spec_resp = allresp[responses[0]]
        score_res = spec_resp['results']['score_res']
        print("Check: number of scores =", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        integ_resp = allresp[responses[1]]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']

    def add_result_from_score_names(self, responses):
        print("add_result_from_score_names")
        allresp = self.parsed_res[-1]['list_responses']
        corr_names = dict(
            map(lambda xy: (xy[1]['response_description']['score_name'], xy[0]),
                enumerate(allresp)))
        print(corr_names)
        spec_resp = allresp[corr_names[responses[0]]]
        score_res = spec_resp['results']['score_res']
        print("Check: number of scores =", len(score_res))
        self.spectrum = score_res[0]['spectrum_res']
        integ_resp = allresp[corr_names[responses[1]]]
        score1_res = integ_resp['results']['score_res']
        self.integrated = score1_res[0]['spectrum_res']
        print(self.integrated)

class SpherePlot():
    '''Class to build plot for Livermore spheres from one sphere and associated
    air input.
    '''

    def __init__(self, jdd_sphere, jdd_air):
        print("Parsing", jdd_sphere)
        self.sphere = LivermoreSphere(jdd_sphere, "Sphere")  #, responses)
        print("Parsing", jdd_air)
        self.air = LivermoreSphere(jdd_air, "Air")  #, responses)

    def normalized_sphere(self, responses):
        print("Set sphere results")
        self.sphere.set_result(responses)
        print("Set air results")
        self.air.set_result(responses)
        spectrum = self.sphere.spectrum['spectrum']
        # print(type(spectrum))
        normalization = self.air.integrated['integrated_res']
        # print(normalization['score'].ravel()[0])
        norm_spec = spectrum['score']/normalization['score'].ravel()[0]
        # print(spectrum['score'].ravel())
        # print("sigma from spectrum:")
        # print(spectrum['sigma'].ravel())
        # print("sigma from integrated:")
        # print(normalization['sigma'].ravel()[0])
        # print("normalized spectrum")
        # print(norm_spec.ravel())
        testerr = spectrum['sigma']*norm_spec/100.
        # print(testerr.ravel())
        print("shape=", testerr.shape)
        norm_spec_sig = spectrum['sigma']*norm_spec/100.  #/normalization['sigma'].ravel()[0]
        # print(norm_spec)
        # removing first and last bins as irrelevant here
        return (norm_spec.ravel()[1:-1],
                norm_spec_sig.ravel()[1:-1],
                self.sphere.spectrum['tbins'][1:-1]*1e9)

    def plot_sphere(self):
        spectrum, spec_err = self.normalized_sphere()
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
        # print(self.res)
        print("ALL KEYS:")
        print(list(self.res.keys()))

    def read_results(self):
        charac = None
        results = None
        print(self.fname)
        with open(self.fname) as fil:
            for line in fil:
                if "MFP" in line:
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
                    results.append(tuple(map(eval, elts)))

    def save_res(self, charac, results):
        dtype = np.dtype({
            'names': ['time', 'cntPtimePsource', 'error', 'cntCum'],
            'formats': [np.int32, np.float32, np.float32, np.float32]})
        self.res[tuple(charac)] = np.array(results, dtype=dtype)

    def plot_res(self, charac):
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
        self.tbins = []
        self.counts = []
        self.sigma = []
        self.read_mcnp()

    def read_mcnp(self):
        nb_tbins = 0
        tbins_block = False
        vals_block = False
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
                    self.tbins += line.split()
                elif vals_block:
                    self.counts += [float(x) for x in line.split()]
                else:
                    continue
        nbtbins = len(self.tbins)
        print("len(tbins) =", len(self.tbins), "et vals:", len(self.counts))
        print(self.tbins)
        print((len(self.counts)/2)/len(self.tbins))
        # self.tbins = np.array([float(x)-0.2 for x in self.tbins])*10
        self.tbins = np.array([float(x) for x in self.tbins])*10
        self.sigma = np.array(
            [x for ind, x in enumerate(self.counts) if ind%2 != 0])
        self.counts = np.array(
            [x for ind, x in enumerate(self.counts) if ind%2 == 0])
        self.sigma = self.sigma*self.counts
        initial_counts = self.counts
        self.integral = self.counts[nbtbins]
        self.sigma_integral = self.sigma[nbtbins]
        self.counts = self.counts[:nbtbins]
        self.sigma = self.sigma[:nbtbins]
        print("Sum of counts:", np.sum(self.counts), "integral:", self.integral)

class MCNPrenormalizedSphere():
    '''Class to buld renormalized spheres for MCNP.'''

    def __init__(self, out_sphere, out_air):
        print("Get results for the sphere")
        self.sphere = MCNPSphere(out_sphere, "Sphere")
        self.air = MCNPSphere(out_air, "Air")
        self.counts, self.sigma, self.tbins = self.normalized_sphere()
        print("Renormalized counts:", self.counts)

    def normalized_sphere(self):
        counts = self.sphere.counts/self.air.integral
        sigma = self.sphere.sigma/self.air.integral
        tbins = self.sphere.tbins
        return counts, sigma, tbins


class CompPlot():
    '''Comparison plot'''

    def __init__(self, charac):
        self.charac = charac
        self.fig, self.splt = plt.subplots(
            2, sharex=True, figsize=(15, 8),
            gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})
        self.legend = {'curves': [], 'labels': [], 'flag': []}
        self.nbins = {'exp': 0, 't4': 0, 'mcnp': 0}

    def customize_plot(self):
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
        self.splt[1].set_ylim(ymin=0.5, ymax=1.5)
        self.splt[0].legend(self.legend['curves'], self.legend['labels'],
                            markerscale=2, fontsize=12)
        self.splt[1].legend(loc='lower right')

    def add_errorbar_plot(self, bins, vals, errors, label='', slab='',
                          **kwargs):
        # possibility to remove slab and put it in kwargs, but less obvious
        # would need to append labels before curve and pop it
        print("[1mkwargs:", kwargs, "[0m")
        tmp_curve = self.splt[0].errorbar(
            bins, vals, yerr=errors, **kwargs)
        print(tmp_curve)
        print(tmp_curve.lines)
        print(tmp_curve.lines[0].get_drawstyle())
        print(tmp_curve.lines[0])
        print(tmp_curve.lines[2][0])
        self.legend['curves'].append(tmp_curve)
        self.legend['labels'].append(label)
        self.legend['flag'].append(slab)

    def add_errorbar_ratio(self, bins, vals, errors, **kwargs):
        print("[1mkwargs:", kwargs, "[0m")
        self.splt[1].errorbar(bins, vals, yerr=errors, **kwargs)


class Comparison():
    '''Class to compare, using matplotlib, experiment and Tripoli-4 results.'''
    NORM_FACTOR = 2
    TIME_SHIFT = 0

    def __init__(self):
        self.exp_res = LivermoreExps()
        self.simu_res = {}
        self.mcnp_res = {}
        self.charac = None


    def set_t4_files(self, jdds):
        for name, jdd in jdds:
            print(jdd)
            self.simu_res[name] = SpherePlot(jdd.replace("SPHAIR", "sphere"),
                                             jdd.replace("SPHAIR", "air"))


    def set_mcnp_files(self, jdds):
        for name, jdd, renorm in jdds:
            print("Read MCNP results for sphere", jdd,
                  "and air", jdd[:-1]+"_airm")
            if renorm:
                self.mcnp_res[name] = MCNPrenormalizedSphere(jdd,
                                                             jdd[:-1]+"_airm")
            else:
                self.mcnp_res[name] = MCNPSphere(jdd, name)

    def plot_experiment(self, charac, splt, legend):
        exp2sig = splt[0].errorbar(self.exp_res.res[charac]['time'],
                                   self.exp_res.res[charac]['cntPtimePsource'],
                                   yerr=self.exp_res.res[charac]['error']*2,
                                   fmt='s', ms=3, ecolor='orange', c='orange')
        exp1sig = splt[0].errorbar(self.exp_res.res[charac]['time'],
                                   self.exp_res.res[charac]['cntPtimePsource'],
                                   yerr=self.exp_res.res[charac]['error'],
                                   fmt='rs', ms=1, ecolor='r')
        print("[1;31mExp. first t bin:", self.exp_res.res[charac]['time'][0],
              "[0m")
        legend['curves'].append((exp2sig, exp1sig))
        legend['labels'].append("Experiment")

    def plot_t4(self, responses, splt, legend):
        cols = ['b', 'g', 'm', 'darkviolet', 'orchid', 'darkmagenta',
                'dodgerblue']
        nexptbins = self.exp_res.res[self.charac]['time'].shape[0]
        print("Number of responses required:", len(responses))
        print("[32mResponses:", responses, "[0m")
        for ires, (sname, simres) in enumerate(self.simu_res.items()):
            print("[94mName of the sample", ires, ":", sname, "[0m")
            if sname not in responses:
                continue
            # middle of T4 bins
            norm_simu = simres.normalized_sphere(responses[sname])
            # remove first bin edge as 1 edge more than bins (normal)
            mtbins = norm_simu[2][1:] - 1
            t4vals = norm_simu[0]/Comparison.NORM_FACTOR
            t4sigma = norm_simu[1]/Comparison.NORM_FACTOR
            nsimtbins = mtbins.shape[0]
            print("[1;31mT4", sname, "first t bin:", mtbins[0], "[0m")
            marker = '-'
            if len(ast.literal_eval(responses[sname])) > 2:
                marker += ast.literal_eval(responses[sname])[2]
            simu = splt[0].errorbar(mtbins, t4vals, yerr=t4sigma,
                                    ecolor=cols[ires], color=cols[ires],
                                    fmt=marker, ms=3, mfc="none")
            legend['curves'].append(simu)
            legend['labels'].append(sname)
            if "Experiment" in legend['labels']:
                # cut first points of simulation as data 'only' start at 141 ns
                cut = 0
                if nexptbins != nsimtbins:
                    if nexptbins > nsimtbins:
                        cut = nexptbins + nsimtbins
                    else:
                        cut = nsimtbins - nexptbins
                exp_data = legend['curves'][0][1].lines[0].get_data()[1]
                splt[1].errorbar(simu.lines[0].get_data()[0][cut:],
                                 simu.lines[0].get_data()[1][cut:]/exp_data,
                                 ecolor=cols[ires], color=cols[ires])
            print("Integral T4 data =",
                  np.trapz(norm_simu[0].ravel()[cut:-1]/2, dx=2.0))

    def plot_mcnp(self, mcnp, splt, legend):
        for sname in self.mcnp_res:
            if sname not in mcnp:
                continue
            print(type(self.mcnp_res[sname]))
            # print("MCNP tbins:", self.mcnp_res[sname].tbins)
            mtbins = self.mcnp_res[sname].tbins - 1
            mcnp_simu = self.mcnp_res[sname].counts
            mcnp_sigma = self.mcnp_res[sname].sigma
            exp_data = self.exp_res.res[self.charac]['cntPtimePsource']
            print("[1;31mMCNP", sname, "first t bin:", mtbins[0], "[0m")
            # isinstance only works the first time with autoreload
            # if isinstance(self.mcnp_res[sname], MCNPrenormalizedSphere):
            if hasattr(self.mcnp_res[sname], 'sphere'):
                print("Renormalised sphere")
                print(mtbins.shape)
                print(mcnp_simu.shape)
                legend['curves'].append(
                    splt[0].errorbar(mtbins,
                                     mcnp_simu/Comparison.NORM_FACTOR,
                                     yerr=mcnp_sigma/Comparison.NORM_FACTOR,
                                     ecolor='c', fmt='c+'))
                legend['labels'].append("MCNP")
                splt[1].errorbar(mtbins[1:],
                                 mcnp_simu[1:]/Comparison.NORM_FACTOR/exp_data,
                                 yerr=mcnp_sigma[1:]/Comparison.NORM_FACTOR,
                                 ecolor='c', color='c')
            else:
                print("Already normalised sphere")
                col = 'c' if len(mcnp) == 1 else 'darkcyan'
                print(col)
                legend['curves'].append(
                    splt[0].errorbar(mtbins,
                                     mcnp_simu,
                                     yerr=mcnp_sigma,
                                     ecolor=col, color=col))
                splt[1].plot(mtbins[1:],
                             mcnp_simu[1:]/exp_data,
                             color=col,
                             label="default MCNP")
                legend['labels'].append("Default MCNP")
            print("Integral MCNP data =",
                  np.trapz(mcnp_simu, dx=2.0))

    def compare_plots(self, charac, responses, mcnp=None):
        # experiment bins
        print("[31mNbre fichiers:", len(self.simu_res), "[0m")
        self.charac = charac
        fig, splt = plt.subplots(2, sharex=True,
                                 gridspec_kw={'height_ratios': [4, 1],
                                              'hspace': 0.05},
                                 figsize=(15, 8))
        legend = {'curves': [], 'labels': []}
        self.plot_experiment(charac, splt, legend)
        splt[0].set_yscale("log", nonposy='clip')
        splt[0].set_title("{elt}, {mfp} mfp, detector at {deg}°"
                          .format(elt=charac[0].capitalize(),
                                  mfp=charac[1], deg=charac[2]))
        self.plot_t4(responses, splt, legend)
        if mcnp:
            self.plot_mcnp(mcnp, splt, legend)
        print(legend['labels'])
        if "New ceav5" in legend['labels'] and "MCNP" in legend['labels']:
            if ((legend['curves'][legend['labels'].index("New ceav5")].lines[0]
                 .get_data()[1].shape[0]-1 == legend['curves'][legend['labels']
                                                               .index("MCNP")]
                 .lines[0].get_data()[1].shape[0])):
                plt.plot(legend['curves'][legend['labels'].index("New ceav5")]
                         .lines[0].get_data()[0][1:],
                         legend['curves'][legend['labels'].index("New ceav5")]
                         .lines[0].get_data()[1][1:]
                         /legend['curves'][legend['labels'].index("MCNP")]
                         .lines[0].get_data()[1],
                         color='r',
                         label="ratio")
        if "MCNP" in legend['labels'] and "Default MCNP" in legend['labels']:
            plt.plot(self.mcnp_res[mcnp[0]].tbins,
                     legend['curves'][legend['labels'].index("MCNP")]
                     .lines[0].get_data()[1]/
                     legend['curves'][legend['labels'].index("Default MCNP")]
                     .lines[0].get_data()[1],
                     color='blueviolet',
                     label="ratio")
        print("Integral exp data =",
              np.trapz(self.exp_res.res[charac]['cntPtimePsource'], dx=2.0))
        splt[0].legend(legend['curves'], legend['labels'],
                       markerscale=2, fontsize=12)
        splt[0].set_ylabel("neutron count rate [1/(ns.source)]")
        splt[0].set_ylim(ymin=2e-4)
        splt[1].axhline(y=1, ls='--', lw=0.5, color='grey')
        splt[1].set_xlabel("time bins [ns]")
        splt[1].set_ylabel("simu/exp")
        plt.show()

    def new_plot_exp(self, charac, cplot):
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
        print("[1;31mExp. first t bin:", self.exp_res.res[charac]['time'][0],
              "[0m")
        cplot.legend['curves'].append((exp2sig, exp1sig))
        cplot.legend['labels'].append("Experiment")
        cplot.legend['flag'].append("exp")
        cplot.nbins['exp'] = self.exp_res.res[charac]['time'].shape[0]

    def new_plot_t4(self, responses, cplot):
        cols = ['b', 'g', 'm', 'darkviolet', 'orchid', 'darkmagenta',
                'dodgerblue']
        print("Number of responses required:", len(responses))
        print("[32mResponses:", responses, "[0m")
        for ires, (sname, simres) in enumerate(self.simu_res.items()):
            print("[94mName of the sample", ires, ":", sname, "[0m")
            if sname not in responses:
                continue
            norm_simu = simres.normalized_sphere(responses[sname])
            # remove first bin edge as 1 edge more than bins (normal)
            mtbins = norm_simu[2][1:] - 1
            t4vals = norm_simu[0]/Comparison.NORM_FACTOR
            t4sigma = norm_simu[1]/Comparison.NORM_FACTOR
            print("[1;31mT4", sname, "first t bin:", mtbins[0], "[0m")
            resp_args = (ast.literal_eval(responses[sname])[2:][0]
                         if len(ast.literal_eval(responses[sname])) > 2
                         else {})
            resp_args.setdefault('fmt', '-')
            resp_args.setdefault('label', sname)
            resp_args.setdefault('slab', sname)
            resp_args.setdefault('c', resp_args.pop('color', cols[ires]))
            resp_args.setdefault('ecolor', resp_args.get('c', cols[ires]))
            print("[94m", resp_args, "[0m")
            cplot.add_errorbar_plot(mtbins, t4vals, t4sigma, **resp_args)

    def new_plot_ratios(self, ratios, cplot):
        '''Plot required ratios.

        :param dict(str, list(str)) ratios: list of short labels
        :param CompPlot cplot: plot on which adding the ratio
        :returns: (nothing: updated plot)
        '''
        for leg, ratio in ratios.items():
            # sanity check
            if len([fl for fl in ratio if fl in cplot.legend['flag']]) != 2:
                print("Wrong flag, please check, possibilities are",
                      cplot.legend['flag'])
                continue
            numn, denomn = (cplot.legend['labels'][cplot.legend['flag']
                                                   .index(flag)]
                            for flag in ratio[:2])
            print(numn, denomn)
            ilines = [0, 0] if "exp" not in ratio else [0, 1]
            print(list(zip(ratio, ilines)))
            num = (cplot.legend['curves'][cplot.legend['flag'].index(ratio[0])]
                   .lines[0].get_data()[1])
            denom = (self.exp_res.res[cplot.charac]['cntPtimePsource']
                     if 'exp' in ratio
                     else (cplot.legend['curves'][cplot.legend['flag']
                                                 .index(ratio[1])]
                           .lines[0].get_data()[1]))
            cutn, cutd = 0, 0
            if num.shape != denom.shape:
                print("something will have to be done for number of bins")
                print("num:", num.shape, "denom:", denom.shape)
                if num.shape > denom.shape:
                    cutn = num.shape[0] - denom.shape[0]
                else:
                    cutd = denom.shape[0] - num.shape[0]
            binsn = (cplot.legend['curves'][cplot.legend['flag'].index(ratio[0])]
                     .lines[0].get_data()[0])
            binsd = (self.exp_res.res[cplot.charac]['time']
                     if 'exp' in ratio
                     else (cplot.legend['curves'][cplot.legend['flag']
                                                 .index(ratio[1])]
                           .lines[0].get_data()[0]))
            if not np.isclose(binsn[cutn:][0], binsd[cutd:][0]):
                print("Maybe the first time bins are not the same: "
                      "num = {0}, denom = {1}"
                      .format(binsn[cutn:][0], binsd[cutd:][0]))
            ratio_args = ratio[2] if len(ratio) > 2 else {}
            cplot.add_errorbar_ratio(binsn[cutn:], num[cutn:]/denom[cutd:],
                                     0, label=leg, **ratio_args)

    def new_comparison(self, charac, responses, mcnp=None, ratios=None):
        complot = CompPlot(charac)
        if charac[-1] is not False:
            self.new_plot_exp(charac, complot)
        self.new_plot_t4(responses, complot)
        if ratios:
            self.new_plot_ratios(ratios, complot)
        complot.customize_plot()
        plt.show()
