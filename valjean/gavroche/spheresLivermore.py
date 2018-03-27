'''VV of Livermore spheres: comparison to experiment and between various
results (change in nuclear data, T4, MCNP, SCALE, ...)'''

from valjean.eponine.parse_t4 import T4Parser
import valjean.eponine.pyparsing_t4.transform as trans
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
        print(responses)
        self.sphere.set_result(responses)
        self.air.set_result(responses)
        spectrum = self.sphere.spectrum['spectrum']
        print(type(spectrum))
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


class Comparison():
    '''Class to compare, using matplotlib, experiment and Tripoli-4 results.'''

    # def __init__(self, charac, jdd_sphere, jdd_air):
    # def __init__(self, charac, jdds):
    def __init__(self):
        # self.charac = charac
        self.exp_res = LivermoreExps()
        self.simu_res = {}
        # for name, jdd in jdds:
        #     print(jdd)
        #     self.simu_res[name] = SpherePlot(jdd[0].replace("SPHAIR", "sphere"),
        #                                      jdd[0].replace("SPHAIR", "air"),
        #                                      jdd[1])
        # self.simu_res = SpherePlot(jdd_sphere, jdd_air)
        # self.norm_simu, self.norm_sig = self.simu_res.normalized_sphere()


    def set_t4_files(self, jdds):
        for name, jdd in jdds:
            print(jdd)
            self.simu_res[name] = SpherePlot(jdd.replace("SPHAIR", "sphere"),
                                             jdd.replace("SPHAIR", "air"))


    def compare_plots(self, charac, responses):
        # experiment bins
        # expbins = self.exp_res.exp_res[self.charac]['time']
        plt.figure(1)
        plt.subplot(111)
        exp2sig = plt.errorbar(self.exp_res.res[charac]['time'],
                               self.exp_res.res[charac]['cntPtimePsource'],
                               yerr=self.exp_res.res[charac]['error']*2,
                               fmt='none', ecolor='orange')
                               # fmt='none', ecolor='orange', elinewidth=3)
        exp1sig = plt.errorbar(self.exp_res.res[charac]['time'],
                               self.exp_res.res[charac]['cntPtimePsource'],
                               yerr=self.exp_res.res[charac]['error'],
                               fmt='none', ecolor='r', ls=':')
        # plt.errorbar(self.exp_res.res[self.charac]['time'],
        #              self.exp_res.res[self.charac]['cntPtimePsource'],
        #              yerr=self.exp_res.res[self.charac]['error']*2,
        #              fmt='none', ecolor='orange')
        # plt.errorbar(self.exp_res.res[self.charac]['time'],
        #              self.exp_res.res[self.charac]['cntPtimePsource'],
        #              yerr=self.exp_res.res[self.charac]['error'],
        #              fmt='none', ecolor='r')
        cols = ['b', 'g', 'm', 'darkviolet']
        simu = []
        labels = []
        for ires, (sname, simres) in enumerate(self.simu_res.items()):
            print(ires)
            print(simres)
            print(sname)
            print(responses[ires], type(responses[ires]), type(eval(responses[ires])))
            # middle of T4 bins
            norm_simu = simres.normalized_sphere(responses[ires])
            tbinle = simres.sphere.spectrum['tbins'][:-1]
            tbinhe = simres.sphere.spectrum['tbins'][1:]
            mtbins = (tbinle+tbinhe)/2*1e9
            print("shape score:", norm_simu[0].ravel()[1:-1].shape)
            # print(norm_simu[1].ravel()[2:-1])
            print("shape sigma:", norm_simu[1].ravel()[1:-1].shape)
            print("shape exp:", self.exp_res.res[charac]['time'].shape)
            print(mtbins[3:-1])
            print(self.exp_res.res[charac]['time'])
            simu.append(plt.errorbar(mtbins[3:-1],
                                     norm_simu[0].ravel()[3:-1]/2,
                                     yerr=norm_simu[1].ravel()[3:-1],
                                     ecolor=cols[ires], color=cols[ires],
                                     label=simres.sphere.name[0]))
            labels.append(sname)
            # plt.errorbar(mtbins[1:-1],
            #              norm_simu[0].ravel()[1:-1]/2,
            #              yerr=norm_simu[1].ravel()[1:-1],
            #              ecolor=cols[ires]))
        plt.xlabel("time bins [ns]")
        plt.yscale("log", nonposy='clip')
        plt.ylim(ymin=5e-5)
        # plt.legend()
        plt.legend([(exp2sig, exp1sig)]+simu, ["experiment"]+labels) # + simu)
        plt.title("{elt}, {mfp} mfp, detector at {deg}°"
                  .format(elt=charac[0].capitalize(),
                          mfp=charac[1], deg=charac[2]))
        plt.show()
