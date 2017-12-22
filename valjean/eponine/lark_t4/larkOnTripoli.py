#!/usr/bin/env python3

import sys
from lark import Lark
from lark import Transformer, inline_args #, lexer -> needed to check type of Token, see if will be needed or not
import time
import numpy as np
from pprint import pprint


class OtherTransformer(Transformer):
    @inline_args
    def name(self, s,):
        return s[:]
    def sentence(self,s) :
        # print("[31m"+str(s)+"[0m")
        return ' '.join(s)
    def thestarline(self,s):
        return True
    def quantitywunit(self,s) :
        return list(s)
    def quantity(self,s) :
        return s[:]
    def sigma(self,s) :
        return "sigma"
    def sigmapc(self,s) :
        return "sigmapc"
    def meshblock(self,s):
        # print("[94m",str(s),"[0m")
        # print(type(s))
        meshbl = {}
        for elt in s :
            meshbl[elt.data] = elt.children
        return meshbl
    def commonword(self,s) :
        return s[-1].value
    def resonmesh(self,s) :
        # to check type... need to call lexer
        # print(s)
        # print("type:",type(s))
        # if isinstance(s,list) : print("s is a list")
        # print("type:",type(s[-1]))
        # if isinstance(s[-1],lexer.Token) : print("s[-1] is a Token")
        mystr = ""
        # for elt in s :
        #     print(elt.value)
        #     mystr += elt.value
        return ' '.join(elt.value for elt in s)# mystr
    # def test(self,s):
    #     mtest = {}
    #     for elt in s :
    #         if not isinstance(elt,int) :
    #             if elt.data != "starline" :
    #                 mtest[elt.data] = elt.children
    #     return mtest
    def theblock(self,s) :
        return len(s)

    object = dict
    # meshdesc = np.array #fonctionne mais print plus long, enleve pour les tests
    meshdesc = list
    mesh = list

    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False
    emax = inline_args(float)
    emin = inline_args(float)
    eunit = inline_args(str)
    float = inline_args(float)
    int = inline_args(int)


# try:
#     fin = sys.argv[1]
# except:
#     print("No file given, will parse tungstene_extrait.txt")
#     fin = "tungstene_extrait.txt"

# print("[35mWill read",fin,"[0m")
# # ebnf_grammar_file = "ebnf_grammar.g"
# # ebnf_grammar_file = "grammar_spaces.g"
# ebnf_grammar_file = "grammar_endl.g"

# # print("[32mUsing ebdn_grammer.d, parser = Earley[0m")
# # with open(ebnf_grammar_file) as gf :

# #     with open(fin) as tungfile :
# #         tripolitxt = tungfile.read()
# #         parsertrip2 = Lark(gf, start='test')
# #         res = None
# #         start_time = time.time()
# #         try :
# #             res = parsertrip2.parse(tripolitxt)
# #         except : 
# #             print("Parsing failed with Earley")
# #             print("Message:",sys.exc_info())
# #         print("[31mTemps:",time.time()-start_time,"[0m")
# #         if res : 
# #             try : 
# #                 trans = OtherTransformer().transform(res)
# #                 print(len(trans.children))
# #             except :
# #                 print("Tree transformation failed")

# print("[32mUsing ebdn_grammer.d, parser = LALR[0m")
# with open(ebnf_grammar_file) as gf :

#     with open(fin) as tungfile :
#         tripolitxt = tungfile.read()
#         parsertrip2 = Lark(gf, start='test',parser="lalr")
#         res = None
#         start_time = time.time()
#         try :
#             res = parsertrip2.parse(tripolitxt)
#             # print(res.pretty())
#             # print(res)
#         except :
#             print("Parsing failed with LALR, no tree")
#             print("Message:",sys.exc_info())
#         print("[31mTemps:",time.time()-start_time,"[0m")
#         if res : 
#             try : 
#                 trans = OtherTransformer().transform(res)
#             except :
#                 print("Tree transformation failed")
#             print(len(trans.children))
        
# print("[32mUsing ebdn_grammer.d, parser = LALR, with transformer[0m")
# with open(ebnf_grammar_file) as gf :

#     with open(fin) as tungfile :
#         tripolitxt = tungfile.read()
#         parsertrip2 = Lark(gf, start='test',parser="lalr",transformer=OtherTransformer())
#         res = None
#         start_time = time.time()
#         try :
#             res = parsertrip2.parse(tripolitxt)
#         except :
#             print("Parsing failed with LALR and transformer")
#             print("Message:",sys.exc_info())
#         print("[31mTemps:",time.time()-start_time,"[0m")
#         if res : 
#             print(len(res.children))
#             # pprint(res.children,depth=1)
