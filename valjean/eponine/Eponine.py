'''Class calling Lamarque, the parser and transformer,
JDD normally direclty usable in tests.
'''

import sys
import time
# from Larmarque import Lamarque
import scan_t4
from valjean.eponine.lark_t4.larkOnTripoli import OtherTransformer
from lark import Lark
# import pyparsing_org
import valjean.eponine.pyparsing_t4.grammar as pygram
from pprint import pprint
import Enjolras
from pyparsing import ParseResults

# in Eponine, profile is a key of globals
if 'profile' not in globals().keys():
    def profile(f):
        return f


class Eponine():
    '''La classe Eponine'''

    @profile
    def __init__(self,
                 jddname,
                 batch=-1,
                 endflag="simulation time",
                 meshlim=1000):
        self.jdd = jddname
        self.batch = batch
        self.endflag = endflag
        self.meshlim = meshlim
        self.strres = ""
        self.transres = None
        self.normalend = False
        self.inittime = -1
        self.result = None

    @profile
    def getStrRes(self):
        lamres = scan_t4.Scan(self.jdd, self.endflag, self.meshlim)
        self.normalend = lamres.normalend
        if not self.normalend and len(lamres) == 0:
            return False
        if self.batch == 0:
            self.strres = lamres.get_all_batch_results()
        else:
            self.strres = lamres[self.batch]
        # if self.batch == -1:
        #     self.batch = next(reversed(lamres))
        self.inittime = lamres.initialization_time
        lamres.print_statistics()
        # print("self.strres =", self.strres)
        # print("type lamres =", type(lamres))
        # for k in lamres.keys():
        #     print("[38;5;167mClef:", k, "[0m")
        print("[38;5;167mClef:", list(lamres.keys()), "[0m")
        print("[38;5;105mFrom lamres.items()[0m")
        # for k, v in lamres.items():
        #     print("[38;5;36mlamres[", k, "] =", v, "[0m")
        # print("[38;5;105mFrom lamres, only key[0m")
        # for k in lamres:
        #     print(k, "(type =", type(k), ")")
        #     print(lamres[k])
        # print("[38;5;105mFrom lamres.values()[0m")
        # for v in lamres.values():
        #     print("value:", v)
        print("[38;5;105mFrom lamres, key and value[0m")
        # for k, v in lamres:
        #     print(k, v)
        # print(lamres[-1])
        # for k, v in lamres:  # not working !
        #     print("[38;5;178m", k, " = ", v, "[0m")
        # print("Generator:", lamres.last_generator_state)
        # print(lamres)
        # print("len(lamres) =", len(lamres))
        # print("avec __getitem__:", lamres[9950])
        return True

    @profile
    def getTransResWithLark(self):
        ebnf_grammar_file = "grammar_endl.g"
        with open(ebnf_grammar_file) as gf:
            parser = Lark(gf, start='test', parser="lalr",
                          transformer=OtherTransformer())
            res = None
            start_time = time.time()
            try:
                res = parser.parse(self.strres)
            except:
                print("Parsing failed with LALR and transformer")
                print("Message:", sys.exc_info())
            print("[31mTemps:", time.time()-start_time, "[0m")
            if res:
                print(len(res.children))
                # pprint(res.children, depth=1)

    def printResponseDescAndDetails(self, response):
        # pprint(response.asList(),depth=2)
        # pprint(response.asDict(),depth=2)
        if 'compo_details' in response :
            #     print("compo_details as list:")
            #     pprint(response['compo_details'].asList())
            #     print("compo_details as dict:")
            #     pprint(response['compo_details'].asDict())
            print("Dictionnaire dans compo_details")
            for compo in response['compo_details']:
                print(compo)
                # pprint(compo.asDict())

    def printResponseResults(self, response):
        print("Number of results:",len(response['results']))
        for ind,res in enumerate(response['results']) :
            if len(list(res.keys())) != len(res):
                print("[1;31mNot the same number of elts in results and keys:"
                      "#keys =",len(list(res.keys())),
                      "#elts =",len(res),
                      "\nClefs:",list(res.keys()),"[0m")
            print("type response:", type(response))
            if isinstance(response, ParseResults):
                print("Result",ind,"as list:")
                pprint(res.asList(),depth=2)
                print("Result",ind,"as dict:")
                pprint(res.asDict(),depth=2)
            print("Clefs:",list(res.keys()))
            for key in res.keys() :
                if isinstance(res[key],type(res)):
                    if len(res[key]) != len(list(res[key].keys())) :
                        print("[33mMaybe an issue with key:",key,"\n[0m"
                              "len(ires) =",len(res[key]),
                              "nbre de clefs =",len(list(res[key].keys())),
                              ":",list(res[key].keys()))
                        pprint(res[key].asList(),depth=2)
                # if key == "spectrum_res" or key == "ifp_res":
                #     print("[94mImpression de",key,"[0m")
                #     pprint(res[key].asDict(),depth=4)
                #     # print("Type des float:",type(res[key]['spectrum_vals'][0][0][0]))
                #     print("Contenu:",res[key]['spectrum_vals']['vals'][0])
                #     print("Type des float:",type(res[key]['spectrum_vals']['vals'][0][0]))
                # if key == "mesh_res":
                #     print("[94mImpression de",key,
                #           "nbre de mesh:",len(res[key]),"[0m")
                #     for mesh in res[key]:
                #         pprint(mesh.asDict(),depth=3)
                # if key == "keff_res" :
                #     print("[94mImpression de",key,"[0m")
                #     pprint(res[key].asDict(),depth=4)
                # if key == "integrated_res":
                #     print("[94mImpression de",key,"[0m")
                #     pprint(res[key].asDict(),depth=4)
                # if ((key == "time_spectrum"
                #      or key == "angle_spectrum"
                #      or key == "greenband_res")):
                #     print("[94mImpression de",key,"[0m")
                #     pprint(res[key].asDict(),depth=4)
                #     for timestep in res[key]:
                #         pprint(timestep.asDict())
                #         pprint(timestep.asList())

    def printDefaultKeffsResults(self,response):
        print("Default keff block:")
        pprint(response.asList(),depth=2)
        print("as dict:")
        pprint(response.asDict(),depth=2)
        for keff in response:
            for keffkey in list(keff.keys()):
                if "matrix" not in keffkey:
                    print(keffkey,":",keff[keffkey])


    def testResultAsList(self):
        print("[1;35mtestResultAsList[0m")
        print("type result =",type(self.result))
        pprint(self.result.asList(), depth=3)
        print("ou le dernier resultat (type =",type(self.result[-1]),"):")
        # non faisable car result[-1] est un "vrai" dictionnaire
        # result est bien une liste de resultat (editions de batchs)
        # pprint(self.result[-1].asList(), depth=3)

    @profile
    def getTransResWithPyParsing(self):
        start_time = time.time()
        # res = pyparsing_org.mygram.parseString(self.strres)
        # res = ""
        # try:
        self.result = pygram.mygram.parseString(self.strres)
        print("[31mTemps:", time.time()-start_time, "[0m")
        # except:
        #     print("Got exception:", sys.exc_info())
        #     sys.exit()
        if self.result:
            # print("Clefs :",list(self.result.keys()))
            # print(len(self.result))
            # print(self.result, 'type =', type(self.result))
            # print("[35mTYPE(result) =", type(self.result), "[0m")
            # print("Result as dict:")
            # pprint(self.result.asDict(),depth=3)
            # print("Result as list:")
            # pprint(self.result.asList(),depth=3)
            print("[94mInitialization time =", self.inittime, "[0m")
            # self.testResultAsList()
            if isinstance(self.result[-1], type(self.result)):
                print("Result[-1] as dict:")
                pprint(self.result[-1].asDict(),depth=3)
                print("Result[-1] as list:")
                pprint(self.result[-1].asList(),depth=3)
                # print("Clefs de result:",list(self.result[-1].keys()))
                if len(self.result[-1]) != len(list(self.result[-1].keys())) :
                    print("[35mNbre de resultats:",len(self.result[-1]),
                          "nbre de clefs:",len(list(self.result[-1].keys())),
                          "[0m")
                    print("List:")
                    pprint(self.result[-1].asList(),depth=3)
                    print("Dict:")
                    pprint(self.result[-1].asDict(),depth=3)
                print("Source intensity:",self.result[-1]['source_intensity'],
                      "with type",type(self.result[-1]['source_intensity']))
                print("Mean weigt leak:",self.result[-1]['mean_weigt_leak'],
                      "with type",type(self.result[-1]['mean_weigt_leak'][0]))
                # print("Contributing particles:",
                #       self.result[-1]['contributing_particles'])
                # if 'default_keffs' in self.result[-1]:
                #     self.printDefaultKeffsResults(self.result[-1]['default_keffs'])
                # print("Clefs list_response:",
                #       list(self.result[-1]['list_response'][-1].keys()))
                # if len(self.result[-1]['list_response'][-1]) > 4:
                #     print("Nbres elts dans last resp =",
                #           len(self.result[-1]['list_response'][-1]))
                #     pprint(self.result[-1]['list_response'][-1].asList(),depth=2)
                #     pprint(self.result[-1]['list_response'][-1].asDict(),depth=2)
                # pprint(self.result[-1]['list_response'][-1]['results'].asList(),depth=1)
                # print("Nombre de resultats =",
                #       len(self.result[-1]['list_response'][-1]['results']))
            if self.result.asDict() == {} :
                if 'list_responses' in self.result[-1]:
                    for ind,resp in enumerate(self.result[-1]['list_responses']):
                        if len(list(resp.keys())) != len(resp):  # or len(resp) > 4 :
                            print("[1;31mNot the same number of responses and keys:"
                                  "#keys =",len(list(resp.keys())),
                                  "#elts =",len(resp))
                            print("Clefs:",list(resp.keys()),"[0m")
                        # print("[34mClefs:",list(resp.keys()),"[0m")
                        # print("type =", type(resp))
                        # print("[94mtype(list_response)=", type(self.result[-1]['list_response']), "[0m")
                        # pprint(resp['results'], depth=3)
                        # print("Response",ind,
                        #       "  clefs:",list(resp.keys()))
                        # prints to check response description
                        # and response characteristics details
                        # self.printResponseDescAndDetails(resp)
                        # print to check response results
                        if 'results' in resp:
                            continue
                        # self.printResponseResults(resp)
                        else:
                            print("[31mNo results in response -> strange[0m")


                # print("Last response function:",
                #       self.result[-1]['list_response'][-1]['resp_function'])
                # if 'resp_name' in list(self.result[-1]['list_response'][-1].keys()) :
                #     print("Last response name:",
                #       self.result[-1]['list_response'][-1]['resp_name'])
                # pprint(self.result[-1].asDict(), depth=4)
                if 'simulation_time' in self.result[-1]:
                    print("[94mSimulation time =",
                          self.result[-1]['simulation_time'], "[0m")
                elif 'exploitation_time' in self.result[-1]:
                    print("[94mExploitation time =",
                          self.result[-1]['exploitation_time'], "[0m")
                if 'elapsed_time' in self.result[-1]:
                    print("[94mElapsed time =",
                          self.result[-1]['elapsed_time'], "[0m")

            else:
                if 'simulation_time' in self.result:
                    print("[94mSimulation time =",
                          self.result['simulation_time'], "[0m")
                if 'elapsed_time' in self.result:
                    print("[94mElapsed time =",
                          self.result['elapsed_time'], "[0m")
            if not self.normalend:
                print("[1;31mNot normal end but a result, "
                      "something probably to check[0m")
            # pprint(self.result[-1]['list_response'][-1][-1].asDict(),
            #        depth=4)
            # pprint(self.result[-1]['list_response'].asList(), depth=2)
            # pprint(self.result[-1]['list_response'][-1].asList(), depth=3)
            # pprint(self.result[-1]['list_response'][-1].asDict(), depth=2)
            # pprint(self.result[-1]['list_response'][-1][-1].asDict(),
            #        depth=3)
            # pprint(self.result.asList())
            # pprint(self.result.children, depth=1)

    def timeFound(self):
        # if isinstance(self.result[-1], type(self.result)):
        if isinstance(self.result[-1], dict):
            if ('simulation_time' in self.result[-1]
                    or ("PARA" in sys.argv and
                        "elpased time" in self.result[-1])):
                return True
            elif 'exploitation_time' in self.result[-1]:
                return True
            else:
                return False
        else:
            if ('simulation_time' in self.result
                    or ("PARA" in sys.argv and "elpased time" in self.result)):
                return True
            else:
                return False

    def tryPlot(self):
        if self.result:
            enjol = Enjolras.Enjolras(self.result)
            enjol.printResults()
            # enjol.getLastSpectrumResults()
            # enjol.getLastMeshResults()
            # enjol.getLastMeshResEnergyDep()
            enjol.getLastMeshResEnergyDep7coord()


def main(myjdd="", mode="MONO"):
    print(sys.argv)
    if myjdd == "":
        try:
            myjdd = sys.argv[1]
        except IndexError:
            print("Eponine: argument needed (jdd name)")
            exit(-1)

    print(myjdd)

    if len(sys.argv) > 2:
        if "PARA" in sys.argv:
            mode = "PARA"
    print("mode =", mode)

    start_time = time.time()
    rstart_time = start_time
    myendflag = "simulation time"
    # if "exploit" in myjdd:
    if "exp" in myjdd and "verif" not in myjdd:
        myendflag = "exploitation time"
    if mode == "PARA":
        myendflag = "elapsed time"
    # myendflag = "variance of variance"
    print("[1;32mEND FLAG:", myendflag, "[0m")
    epon = Eponine(myjdd, -1, endflag=myendflag, meshlim=2)
    print("scan: reading file, getting tokens:", time.time() - start_time)
    start_time = time.time()
    gotRes = epon.getStrRes()
    with open("jddres.txt", 'w') as fout:
        fout.write(epon.strres)
    print("[33mNormal completion:", epon.normalend, "[0m")
    # if not epon.normalend: return
    if not gotRes:
        return
    print("scan: get string with the result, duration =",
          time.time() - start_time)
    # start_time = time.time()
    # epon.getTransResWithLark()
    # print("Lark: use parser to get the result, duration =",
    # time.time() - start_time)
    # print("Total time:", time.time() - rstart_time)
    start_time = time.time()
    epon.getTransResWithPyParsing()
    # epon.tryPlot()
    print("PyParsing: use parser to get the result, duration =",
          time.time() - start_time)
    print("Total time:", time.time() - rstart_time)
    return epon.timeFound()


if __name__ == "__main__":
    main()
