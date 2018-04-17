'''VV of Livermore spheres: comparison to experiment and between various
results (change in nuclear data, T4, MCNP, SCALE, ...)'''

from valjean.eponine.parse_t4 import T4Parser
import valjean.eponine.pyparsing_t4.transform as trans
import numpy as np
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
        # self.add_result(jdd, eval(responses))

    def set_result(self, response):
        responses = eval(response)
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
        self.sphere = LivermoreSphere(jdd_sphere, "Sphere")  #, responses)
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
        return norm_spec, norm_spec_sig

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
        # print("MCNP tbins:", self.tbins)
        # print("MCNP vals:", self.counts)
        print("len(tbins) =", len(self.tbins), "et vals:", len(self.counts))
        print(self.tbins)
        print((len(self.counts)/2)/len(self.tbins))
        self.tbins = np.array([float(x)-0.2 for x in self.tbins])*10
        # ntbins = np.array([])
        # print(self.tbins)
        self.sigma = np.array(
            [x for ind, x in enumerate(self.counts) if ind%2 != 0])
        self.counts = np.array(
            [x for ind, x in enumerate(self.counts) if ind%2 == 0])
        self.sigma = self.sigma*self.counts
        # print(len(self.sigma))
        # print(len(self.counts))
        # print(len(self.counts[136:]), self.counts[136:][2], self.counts[136:][-1])
        # print(len(self.counts[:136]), self.counts[:136][2], self.counts[:136][-1])
        initial_counts = self.counts
        self.counts = self.counts[:136]
        self.sigma = self.sigma[:136]
        print(self.counts[-1], initial_counts[136], initial_counts[136:139], len(initial_counts))
        # print(self.sigma*self.counts, len(self.sigma*self.counts))

class Comparison():
    '''Class to compare, using matplotlib, experiment and Tripoli-4 results.'''

    # def __init__(self, charac, jdd_sphere, jdd_air):
    # def __init__(self, charac, jdds):
    def __init__(self):
        # self.charac = charac
        self.exp_res = LivermoreExps()
        self.simu_res = {}
        self.mcnp_res = {}


    def set_t4_files(self, jdds):
        for name, jdd in jdds:
            print(jdd)
            self.simu_res[name] = SpherePlot(jdd.replace("SPHAIR", "sphere"),
                                             jdd.replace("SPHAIR", "air"))


    def set_mcnp_files(self, jdd, name):
        self.mcnp_res[name] = MCNPSphere(jdd, name)

    def compare_plots(self, charac, responses, mcnp=None):
        # experiment bins
        # expbins = self.exp_res.exp_res[self.charac]['time']
        print("[31mNbre fichiers:", len(self.simu_res), "[0m")
        plt.figure(1)
        gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])
        # 211 -> gs[0], 212 -> gs[1]
        plt.subplot(gs[0])
        exp2sig = plt.errorbar(self.exp_res.res[charac]['time'],
                               self.exp_res.res[charac]['cntPtimePsource'],
                               yerr=self.exp_res.res[charac]['error']*2,
                               fmt='none', ecolor='orange')
                               # fmt='none', ecolor='orange', elinewidth=3)
        exp1sig = plt.errorbar(self.exp_res.res[charac]['time'],
                               self.exp_res.res[charac]['cntPtimePsource'],
                               yerr=self.exp_res.res[charac]['error'],
                               fmt='none', ecolor='r', ls=':')
        legends_curves = [(exp2sig, exp1sig)]
        legends_leg = ["experiment"]
        plt.yscale("log", nonposy='clip')
        # plt.legend()
        plt.title("{elt}, {mfp} mfp, detector at {deg}°"
                  .format(elt=charac[0].capitalize(),
                          mfp=charac[1], deg=charac[2]))
        cols = ['b', 'g', 'm', 'darkviolet', 'orchid', 'darkmagenta',
                'dodgerblue']
        simu = []
        labels = []
        expcut = 3 if charac[2] == '30' else 2
        nexptbins = self.exp_res.res[charac]['time'].shape[0]
        if charac[0] == "BERYLLIUM":
            expcut = 1
        print(responses)
        print("Number of responses required:", len(responses))
        for ires, (sname, simres) in enumerate(self.simu_res.items()):
            # print(ires)
            # print(simres)
            print("[94mName of the sample", ires, ":", sname, "[0m")
            if sname not in responses:
                continue
            # print(responses[sname], type(responses[sname]), type(eval(responses[sname])))
            # middle of T4 bins
            norm_simu = simres.normalized_sphere(responses[sname])
            tbinle = simres.sphere.spectrum['tbins'][:-1]
            tbinhe = simres.sphere.spectrum['tbins'][1:]
            mtbins = (tbinle+tbinhe)/2*1e9
            print("[37mGot sample", sname, "normalized[0m")
            # print("shape score:", norm_simu[0].ravel()[1:-1].shape)
            # # print(norm_simu[1].ravel()[2:-1])
            # print("shape sigma:", norm_simu[1].ravel()[1:-1].shape)
            # print("shape exp:", self.exp_res.res[charac]['time'].shape)
            # print(mtbins[1:-1])
            # print(self.exp_res.res[charac]['time'])
            # print(type(eval(responses[sname])[0]))
            print("[36m", self.exp_res.res[charac]['time'].shape, "[0m")
            print("[36m", norm_simu[0].ravel()[expcut:-1].shape, "[0m")
            print("[36m", mtbins[expcut:-1].shape, "[0m")
            nsimtbins = mtbins[expcut:-1].shape[0]
            if nexptbins != nsimtbins:
                if nexptbins > nsimtbins:
                    expcut = expcut - nexptbins + nsimtbins
                else:
                    expcut = expcut + nsimtbins - nexptbins
            print("[35m", self.exp_res.res[charac]['time'].shape, "[0m")
            print("[35m", norm_simu[0].ravel()[expcut:-1].shape, "[0m")
            print("[35m", mtbins[expcut:-1].shape, "[0m")
            marker = '-'
            print(marker)
            print(responses[sname])
            if len(eval(responses[sname])) > 2:
                marker += eval(responses[sname])[2]
            print(marker)
            # if ((isinstance(eval(responses[sname])[0], str)
            #      and "old" not in sname and "Old" not in sname)):
            #     print("[34m", sname, "[0m")
            #     print(eval(responses[sname])[0])
            plt.subplot(gs[0])
            simu.append(plt.errorbar(mtbins[expcut:-1],
                                     norm_simu[0].ravel()[expcut:-1]/2,
                                     # norm_simu[0].ravel()[3:-1]/2,
                                     yerr=norm_simu[1].ravel()[expcut:-1],
                                     ecolor=cols[ires], color=cols[ires],
                                     fmt=marker, ms=3, mfc="none",
                                     label=simres.sphere.name[0]))
            plt.subplot(gs[1])
            plt.errorbar(mtbins[expcut:-1],
                         norm_simu[0].ravel()[expcut:-1]/2/self.exp_res.res[charac]['cntPtimePsource'],
                         yerr=self.exp_res.res[charac]['error'],
                         ecolor=cols[ires], color=cols[ires],
                         label=simres.sphere.name[0])
            # else:
            #     print("[35m", sname, "[0m")
            #     plt.subplot(gs[0])
            #     simu.append(plt.errorbar(mtbins[1:-1],
            #                              norm_simu[0].ravel()[1:-1]/2,
            #                              yerr=norm_simu[1].ravel()[1:-1],
            #                              ecolor=cols[ires], color=cols[ires],
            #                              label=simres.sphere.name[0]))
            #     plt.subplot(gs[1])
            #     plt.errorbar(mtbins[1:-1],
            #                  norm_simu[0].ravel()[1:-1]/2/self.exp_res.res[charac]['cntPtimePsource'],
            #                  yerr=self.exp_res.res[charac]['error'],
            #                  ecolor=cols[ires], color=cols[ires],
            #                  label=simres.sphere.name[0])
            print("[36mLabels:", labels, "[0m")
            labels.append(sname)
        legends_curves += simu
        legends_leg += labels
        if mcnp:
            plt.subplot(gs[0])
            # print("MCNP bins:", self.mcnp_res[mcnp].tbins,
            #       "nbre:", len(self.mcnp_res[mcnp].tbins))
            # print("Exp bins:", self.exp_res.res[charac]['time'],
            #       "nbre:", len(self.exp_res.res[charac]['time']))
            mcnp_plot = plt.errorbar(self.mcnp_res[mcnp].tbins,
                                     self.mcnp_res[mcnp].counts,
                                     yerr=self.mcnp_res[mcnp].sigma,
                                     ecolor='c', color='c',
                                     label="MCNP")
            # mcnp_plot2 = plt.errorbar(self.exp_res.res[charac]['time']-1,
            #                           self.mcnp_res[mcnp].counts[1:],
            #                           yerr=self.mcnp_res[mcnp].sigma[1:],
            #                           ecolor='y', color='y',
            #                           label="MCNP th bins", fmt="none")
            plt.subplot(gs[1])
            # plt.errorbar(self.exp_res.res[charac]['time']-1,
            #              self.mcnp_res[mcnp].counts[1:]/2/self.exp_res.res[charac]['cntPtimePsource'],
            #              yerr=self.mcnp_res[mcnp].sigma[1:],
            #              ecolor='y', color='y',
            #              label="MCNP")
            plt.errorbar(self.mcnp_res[mcnp].tbins[1:],
                         self.mcnp_res[mcnp].counts[1:]/self.exp_res.res[charac]['cntPtimePsource'],
                         yerr=self.mcnp_res[mcnp].sigma[1:],
                         ecolor='c', color='c',
                         label="MCNP")
            # plt.errorbar(self.mcnp_res[mcnp].tbins[1:],
            #              self.mcnp_res[mcnp].counts[:-1]/2/self.exp_res.res[charac]['cntPtimePsource'],
            #              yerr=self.mcnp_res[mcnp].sigma[:-1],
            #              ecolor='y', color='y',
            #              label="MCNP")
            # print(mcnp_plot)
            # print(type(mcnp_plot))
            # mpl.artist.getp(mcnp_plot)
            # print(mcnp_plot.lines)
            # mpl.artist.getp(mcnp_plot.lines)
            # mpl.artist.getp(mcnp_plot.lines[0])
            # print(mcnp_plot.lines[0].get_data())
            if "New ceav5" in labels:
                plt.errorbar(self.mcnp_res[mcnp].tbins[1:],
                             simu[labels.index("New ceav5")].lines[0].get_data()[1]/self.mcnp_res[mcnp].counts[1:],
                             yerr=self.mcnp_res[mcnp].sigma[1:],
                             ecolor='r', color='r',
                             label="MCNP")
            legends_curves += [mcnp_plot]  # , mcnp_plot2]
            legends_leg += ["MCNP"]  # , "MCNP th bins"]
        plt.subplot(gs[0])
        plt.legend(legends_curves, legends_leg)
        plt.ylabel("neutron count rate [1/(ns.source)]")
        plt.ylim(ymin=1e-4)
        plt.subplot(gs[1])
        plt.grid(axis='y')
        plt.xlabel("time bins [ns]")
        plt.ylabel("simu/exp")
        plt.show()
