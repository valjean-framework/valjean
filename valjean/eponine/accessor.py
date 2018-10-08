'''Module to access Tripoli-4 parsed results and convert them in standard
:class:`Dataset <valjean.eponine.dataset.Dataset>`, easily comparable to other
codes.

How to flatten a nested structure of lists and dicts ?
------------------------------------------------------

:class:`DataResponses` is used to flatten the nested result from parsing.
Various possibilities exist. Some functions also allow to calculate the
deepness of the structure. Per default the deepness will be calculated on lists
of dicts.

    >>> from valjean.eponine import accessor as acc
    >>> myex1 = [{'k1': 0, 'k2': [0, 1]}, {'k3': 8, 'k1': 5}]
    >>> print(acc.DataResponses.nested_lod_deepness(myex1))
    1
    >>> myex2 = [{'l1': 'ab', 'l2': 4, 'l3': [{'l11': 0, 'l12': [0, 1, 2]}],
    ...           'l4': 'RYUT'}, {'l1': 'fzg', 'l2': 8}]
    >>> print(acc.DataResponses.nested_lod_deepness(myex2))
    2
    >>> myex3 = [{'m1': 4, 'm2': 'ffgo',
    ...           'm3': [{'m11': 'geig', 'm12': 5,
    ...                   'm13': [{'m21': 'fkj', 'm23': [9, 6]}, {'m21': 'e'}],
    ...                   'm14': [0, 2, 4]}]}, {'m1': 7, 'm2': 'dhng'}]
    >>> print(acc.DataResponses.nested_lod_deepness(myex3))
    3
    >>> myex4 = [{'m1': 4, 'm2': 'ffgo',
    ...           'm3': [{'m11': 'geig', 'm12': 5,
    ...                   'm13': [{'m21': 'fkj', 'm23': [9, 6]}, {'m21': 'e'}],
    ...                   'm14': [0, 2, 4]}]},
    ...          {'m1': 7, 'm2': 'dhng',
    ...           'm3': [{'m14': [5, 7, 9],
    ...                   'm13': [{'m21': 'ofhidf', 'm22': 10}]}]}]
    >>> print(acc.DataResponses.nested_lod_deepness(myex4))
    3
    >>> myex5 = [{'bla': {'aff': 4, 'sgdg': 'dfsf'}, 'fge': ['gr', 'gsg']}]
    >>> print(acc.DataResponses.nested_lod_deepness(myex5))
    1
'''

import logging
import pprint
from collections import defaultdict, namedtuple, Sequence, Mapping
import valjean.eponine.data_convertor as dcv

LOGGER = logging.getLogger('valjean')
PP = pprint.PrettyPrinter(indent=4, depth=2)
Response = namedtuple('Response', ['type', 'data'])


def merge_defaultdict(defd1, defd2):
    '''Function to merge 2 dict of defaultdict(set).

    .. todo::

        Think about doing a class for these containers with at least this
        method.
    '''
    mdefd = defd1.copy()
    for key1, val1 in defd2.items():
        if key1 in mdefd:
            for key2, val2 in val1.items():
                mdefd[key1][key2] |= val2
        else:
            mdefd[key1] = val1
    return mdefd


class DataResponses:
    '''Class to represent data from responses, that will be re-modeled in
    Accessor, with better seperation between Data and Metadata.'''

    def __init__(self, data):
        self.nested = data
        self.flat = []
        self.n2f = {}
        LOGGER.debug("DANS DATA_RESPONSES")
        self.nested_to_flat(self.flatten_with_flag, stopflag='_res')
        LOGGER.debug("FLATTEN DONE")
        # self.flatten()

    @classmethod
    def nested_to_flat(cls, meth, **kwargs):
        '''Test of generic method to flatten nested structure.'''
        LOGGER.debug("Will transform nested data in flat ones using %s",
                     '.'.join([cls.__name__, meth.__name__]))
        return meth(**kwargs)

    def flatten_with_flag(self, stopflag=""):
        '''Method to flatten the list of responses, including scores.'''
        for iresp, resp in enumerate(self.nested):
            LOGGER.debug("Keys in list_responses = %s", list(resp.keys()))
            if not self.dict_in_list(resp['results']):
                self.flat.append(resp)
                self.n2f[iresp] = len(self.flat) - 1
                continue
            rmd = {k: v for k, v in resp.items() if k != 'results'}
            LOGGER.debug(type(resp['results']))
            for isc, score in enumerate(resp['results']):
                LOGGER.debug("keys: %s", list(score.keys()))
                smd = {k: v for k, v in score.items() if stopflag not in k}
                smd.update(rmd)
                LOGGER.debug("smd = %s", smd)
                smd['results'] = Response(
                    resp['results'].type,
                    {k: v for k, v in score.items() if stopflag in k})
                self.flat.append(smd)
                self.n2f[(iresp, isc)] = len(self.flat) - 1

    def flatten(self):
        '''Method to flatten the list of responses, including scores.'''
        for iresp, resp in enumerate(self.nested):
            if resp['response_type'] not in ('score_res', 'sensitivity_res'):
                self.flat.append(resp)
                self.n2f[iresp] = len(self.flat) - 1
                continue
            rmd = {k: v for k, v in resp.items() if k != 'results'}
            LOGGER.debug(type(resp['results']))
            for isc, score in enumerate(resp['results']):
                LOGGER.debug("keys: %s", list(score.keys()))
                smd = {k: v for k, v in score.items() if '_res' not in k}
                smd.update(rmd)
                LOGGER.debug("smd = %s", smd)
                smd['results'] = Response(
                    resp['results'].type,
                    {k: v for k, v in score.items() if '_res' in k})
                self.flat.append(smd)
                self.n2f[(iresp, isc)] = len(self.flat) - 1

    def nested_indices(self, flat_indices):
        '''Get the indices in nested list corresponding to indices in flat
        list.
        '''
        LOGGER.debug(flat_indices)
        LOGGER.debug(self.n2f)
        sub_n2f = [k[0] if isinstance(k, tuple) else k
                   for k, v in self.n2f.items() if v in flat_indices]
        return sub_n2f

    def flat_indices(self, nested_index):
        '''Get flat indices from nested ones: return all flat indices for a
        given response for example.
        '''
        flat_ind = {v for k, v in self.n2f.items()
                    if nested_index in [k if isinstance(k, int) else k[0]]}
        LOGGER.debug("flat indices: %s", flat_ind)
        return flat_ind

    @classmethod
    def nested_list_deepness(cls, nested, deep=0):
        '''Calculate deepness of nested structure.'''
        if not isinstance(nested, Sequence) or isinstance(nested, str):
            return deep
        deep += 1
        deep += max([cls.nested_list_deepness(x) for x in nested])
        return deep

    @classmethod
    def dict_in_list(cls, struct):
        '''Return ``True`` if there is a dictionary in a list. External
        object has to be a list.

            >>> from valjean.eponine.accessor import DataResponses as dr
            >>> dr.dict_in_list([0, 1])
            False
            >>> dr.dict_in_list({'spam': 0, 'egg': [0, 7]})
            False
            >>> dr.dict_in_list([{'bacon': 'meat', 'egg': 0}])
            True
        '''
        if ((isinstance(struct, Sequence)
             and any(isinstance(x, Mapping) for x in struct))):
            return True
        return False

    @classmethod
    def nested_lod_deepness(cls, nested):
        '''Calculate deepness of nested structure.'''
        LOGGER.debug("in nested_lod_deepness")
        deep = 0
        if cls.dict_in_list(nested):
            deep += 1
            sdicts = [x for y in nested for x in y.values()
                      if isinstance(y, Mapping) and cls.dict_in_list(x)]
            if sdicts:
                ideep = [cls.nested_lod_deepness(x) for x in sdicts]
                deep += max(ideep)
        return deep

    @classmethod
    def nested_keys(cls, nested):
        '''Return list of list of all keys.'''
        lkeys = []
        if cls.dict_in_list(nested):
            for elt in nested:
                tmpkeys = [x for x in elt if '_res' not in x]
                sdicts = [y for y in elt.values()
                          if isinstance(elt, Mapping) and cls.dict_in_list(y)]
                if sdicts:
                    assert len(sdicts) == 1
                sdkeys = cls.nested_keys(sdicts[0]) if sdicts else []
                if not sdkeys:
                    lkeys.append(tmpkeys)
                else:
                    for sdk in sdkeys:
                        lkeys.append(tmpkeys + sdk)
        return lkeys

    @classmethod
    def flatten_nlod(cls, nested, level=None, prev_md=None, prev_key=""):
        '''md = metadata'''
        flat = []
        n2f = {}
        for ielt, elt in enumerate(nested):
            llev = level.copy() if level else []
            llev.append(ielt)
            if not any(cls.dict_in_list(x) for x in elt.values()):
                # if isinstance(x, Mapping)):
                lelt = {'_'.join([prev_key, k])if prev_key else k: v
                        for k, v in elt.items()}
                if prev_md:
                    lelt.update(prev_md)
                flat.append(lelt)
                n2f[tuple(llev)] = len(flat) - 1
            else:
                rmd = {k: v for k, v in elt.items() if not cls.dict_in_list(v)}
                ndata = {k: v for k, v in elt.items() if cls.dict_in_list(v)}
                for key, dat in ndata.items():
                    tflat, tn2f = cls.flatten_nlod(dat, llev, rmd, key)
                    flat.extend(tflat)
                    n2f.update(tn2f)
        return flat, n2f

    @classmethod
    def flatten_res_dict(cls, nested, dataflag=""):
        '''Method to flatten the list of responses, including scores.'''
        flat = []
        n2f = {}
        for iresp, resp in enumerate(nested):
            if not cls.dict_in_list(resp['results']):
                flat.append(resp)
                n2f[iresp] = len(flat) - 1
                continue
            rmd = {k: v for k, v in resp.items() if k != 'results'}
            for isc, score in enumerate(resp['results']):
                # print("keys:", list(score.keys()))
                smd = {k: v for k, v in score.items() if dataflag not in k}
                smd.update(rmd)
                # print("smd =", smd)
                smd['results'] = {k: v for k, v in score.items()
                                  if dataflag in k}
                flat.append(smd)
                n2f[(iresp, isc)] = len(flat) - 1
        return flat, n2f


class IndexResponses:
    '''Class to index T4 responses, or flat ones, or nested ones. If responses
    are nested scores won't be flatten, this is just index. It should still be
    possible to flatten them afterwards.
    '''

    def __init__(self, lcases):
        LOGGER.debug("\x1b[35m>>>>>> IndexResponses.__init__ <<<<<<<<\x1b[0m")
        self.ids = set(range(len(lcases)))
        LOGGER.debug("mem lcases: %d, lcases: %d", id(lcases), id(lcases))
        LOGGER.debug(list(lcases[0].keys()))
        self.dsets = {k: defaultdict(set)
                      for icase in lcases
                      for k in icase.keys() if k != 'results'}
        LOGGER.debug("\x1b[91mself.dsets = %s\x1b[0m", self.dsets)
        LOGGER.debug("nb cases = %d", len(lcases))
        self._build_index(lcases)
        LOGGER.debug(self.dsets)
        LOGGER.debug("\x1b[35m>>>>> END IndexResponses.__init__ <<<<<<\x1b[0m")

    def _build_index(self, responses):
        '''Build index from all responses in the list.

        Keys of the sets are keywords used to describe the responses and/or the
        scores (if flat case).
        One special case has to be quoted: the 'compo_details' characteristic
        is in the parsed result a list of dictionaries as it can involve more
        than one nucleus or more than one reaction for example. To deal with
        that special case a tuple is built from the list of dict. Sadly it will
        probably be difficult to use. Advice: set the reaction name or the
        nucleus name in the score name.
        '''
        for iresp, resp in enumerate(responses):
            LOGGER.debug("Response %d: %s", iresp, resp['resp_function'])
            for key in self.dsets:
                if key in resp:
                    self.dsets[key][resp[key]].add(iresp)

    def __len__(self):
        return len(self.ids)

    def select_by(self, **kwargs):
        '''Selection of responses indices according to kwargs criteria.

        This selection can only be applied on `int` indices and not on `tuple`
        ones, i.e. it has to be applied on a flat collection.
        '''
        respids = self.ids  # voir si la copie est necessaire
        for kwd in kwargs:
            if kwd not in self.dsets:
                LOGGER.warning("%s not a valid key. Possible ones are %s",
                               kwd, list(self.dsets.keys()))
                return set()
            if kwargs[kwd] not in self.dsets[kwd]:
                LOGGER.warning("%s is not a valid %s", kwargs[kwd], kwd)
                return set()
            respids = respids & self.dsets[kwd][kwargs[kwd]]
        if not respids:
            LOGGER.warning("Wrong selection, response might be not present. "
                           "Also check if requirements are consistant.")
            return set()
        return respids

    def strip_index(self, setids):
        '''Get a sub index containing only the relevant keywords for the
        required subset of ids.
        '''
        if not setids:
            return {}
        tmpdict = {k: defaultdict(set) for k in self.dsets}
        for cat in self.dsets:
            for kwd, kset in self.dsets[cat].items():
                tmpset = kset & setids
                if tmpset:
                    tmpdict[cat][kwd] = tmpset
        return {k: v for k, v in tmpdict.items() if v}

    def get_subindex_from(self, **kwargs):
        '''Get subindex from kwargs.'''
        subset = self.select_by(**kwargs)
        return self.strip_index(subset)


class ResponsesBook:
    """Class to perform selections on results.

    This class is based on two objects:

      * the responses, as a list of dictionaries (containing data and metadata)
      * an index based on responses allowing easy selections on each metadata.

    """

    def __init__(self, resp):
        self.responses = resp
        self.index = self.build_index2()
        LOGGER.warning("Index: %s", self.index)

    def build_index(self):
        dsets = {k: defaultdict(set) for iresp in self.responses
                 for k in iresp if k != 'results'}
        for iresp, resp in enumerate(self.responses):
            LOGGER.debug("Response %d: %s", iresp, resp['resp_function'])
            for key in dsets:
                if key in resp:
                    dsets[key][resp[key]].add(iresp)
        return dsets

    def build_index2(self):
        dsets = {}
        for iresp, resp in enumerate(self.responses):
            for key in resp:
                if key != 'results':
                    (dsets.setdefault(key, {})
                     .setdefault(resp[key], set([iresp])).add(iresp))
        return dsets


class Accessor:
    '''Class to access T4 results in a friendly way.
    parsed_res = only one batch
    '''

    def __init__(self, tparsed_res):  # , merge_score=False):
        self.parsed_res = tparsed_res
        # LOGGER.warning("PARSING RESULT: %s", tparsed_res)
        self.resp_book = (ResponsesBook(self.parsed_res['list_responses'])
                          if 'list_responses' in self.parsed_res
                          else None)
        if self.resp_book:
            print("RESP_BOOK done")
        # self.responses = None
        # self.indflat = None
        # self.indnest = None
        # if 'list_responses' in self.parsed_res.keys():
        #     lresp = self.parsed_res['list_responses']
        #     LOGGER.debug('nbre de responses = %d, type = %s',
        #                  len(lresp), type(lresp))
        #     LOGGER.debug(list(lresp[0].keys()))
        #     self.responses = DataResponses(lresp)
        #     LOGGER.debug(id(self.responses.nested))
        #     LOGGER.debug(self.responses.n2f)
        #     LOGGER.debug("\x1b[1mESSAIS\x1b[0m")
        #     LOGGER.debug("-> index from flat:")
        #     self.indflat = IndexResponses(self.responses.flat)
        #     LOGGER.debug(len(self.indflat))
        #     LOGGER.debug("-> index from nested:")
        #     self.indnest = IndexResponses(self.responses.nested)
        #     LOGGER.debug(len(self.indnest))
        #     LOGGER.debug("\x1b[1m----------------------\x1b[0m")

    # questions on the name of that method: what is the more explicit ?
    # get_by (but what ?), get_response_by (but we can get a score even by
    # scoring zone), get_score_by ?, get_result_by ?, select_by ?
    # CAUTION: this method can fail if 'list_responses' does not exist in the
    # parsed result
    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (resp_function, score_name, scoring_zone_id, etc).

        Its returns or an element or a sublist of the flatten response list.
        If no kwarg is given it will return the full flat list. To get it in
        its nested shape, use ``MY_ACCESSOR.responses.nested``.
        '''
        if kwargs is None:
            return self.responses.flat
        if 'index' in kwargs:
            index = kwargs.pop('index')
            return self.get_from_nested_index(index, **kwargs)
        subids = self.indflat.select_by(**kwargs)
        resps = [self.responses.flat[i] for i in subids]
        return resps

    def get_from_nested_index(self, index, **kwargs):
        '''Get response from nested index, other keyword arguments allowed.'''
        if isinstance(index, tuple):
            res = (self.responses.flat[self.responses.n2f[index]]
                   if index in self.responses.n2f else [])
        else:
            find = self.responses.flat_indices(index)
            if kwargs:
                subids = self.indflat.select_by(**kwargs)
                find &= subids
            res = [self.responses.flat[i] for i in find]
        return res

    def _by_response_description(self, keyword):
        assert 'list_responses' in self.parsed_res.keys()
        tdict = dict(map(
            lambda xy: (xy[1]['response_description'].get(keyword), xy[1]),
            enumerate(self.parsed_res['list_responses'])))
        if None in tdict:
            tdict.pop(None)
        if len(tdict) < len(self.parsed_res['list_responses']):
            LOGGER.warning("Some responses are missing from dictionary,"
                           " probably due to identical %s", keyword)
        return tdict

    def by_score_name(self):
        '''Order responses by score name.'''
        print(list(self.parsed_res.keys()))
        tdict = self._by_response_description('score_name')
        # PP.pprint(tdict)
        self.ordered_res = tdict

    def by_response_function(self):
        '''Order responses by response function.'''
        tdict = self._by_response_description('resp_function')
        # print("\x1b[34m")
        # PP.pprint(tdict)
        # print("\x1b[0m")
        self.ordered_res = tdict

    def by_response_index(self):
        '''Order responses by index.'''
        assert 'list_responses' in self.parsed_res.keys()
        self.ordered_res = dict(enumerate(self.parsed_res['list_responses']))
        # PP.pprint(self.ordered_res)

    def get_score(self, response):
        '''Get score result from given response.'''
        print(type(self.ordered_res[response]))
        print(list(self.ordered_res[response].keys()))
        assert self.ordered_res[response]['results'][0] == 'score_res'
        print(list(self.ordered_res[response]['results'][1][0].keys()))
        return self.ordered_res[response]['results'][1]

    def get_scoring_zones(self, response):
        '''Get the list of scoring zones.'''
        score = self.get_score(response)
        # print(len(score))
        return [x['scoring_zone'] for x in score]

    def get_spectrum_from_score(self, response, zone=0):
        '''Get spectrum from response (and score).'''
        score = self.get_score(response)
        print(hex(id(score)))
        if isinstance(zone, int):
            assert 'spectrum_res' in score[zone]
            return dcv.convert_spectrum_as_dataset(score[zone]['spectrum_res'])
        # score_by_zone = self._by_scoring_zone()
        raise TypeError("Only int are accepted for the moment (index in the "
                        "list of scores = index of the scoring zone)")

    def get_mesh_from_score(self, response):
        '''Get mesh from response (and score).'''
        score = self.get_score(response)
        assert 'mesh_res' in score[0]
        print(list(score[0]['mesh_res']))
        print(score[0]['mesh_res']['mesh'].squeeze())
        print(score[0]['mesh_res']['mesh'].shape)
        return dcv.convert_mesh_as_dataset(score[0]['mesh_res'])

    def get_intres_from_score(self, response, res_type='integrated_res',
                              zone=0):
        '''Get integrated result from response (and score).'''
        score = self.get_score(response)
        assert res_type in score[zone]
        return dcv.convert_intres_as_dataset(score[zone][res_type], res_type)

    def get_entropy_from_score(self, response, res_type):
        '''Get entropy from response (and score).'''
        score = self.get_score(response)
        assert res_type in score[0]
        return dcv.convert_entropy_as_dataset(score[0][res_type], res_type)

    # reflechir a mettre le nom de la reponse comme titre ici
    def get_generic_score(self, response):
        '''Get generic score from response.'''
        print(list(self.ordered_res.keys()))
        assert response in self.ordered_res
        print(self.ordered_res[response])
        return dcv.convert_intres_as_dataset(
            self.ordered_res[response]['results'][1], 'generic_score')

    def get_keff(self, **kwargs):
        '''Get keff (generic response).'''
        print(list(self.ordered_res.keys()))
        assert self.ordered_res['KEFFS']['results'][0] == 'keff_res'
        keffres = self.ordered_res['KEFFS']['results']
        print(keffres)
        print(list(keffres[1].keys()))
        if 'estimator' in kwargs:
            return dcv.convert_keff_in_dataset(keffres[1], kwargs['estimator'])
        if 'combination' in kwargs:
            return dcv.convert_keff_comb_in_dataset(keffres[1])
        if 'matrix' in kwargs:
            return keffres[1].get(kwargs['matrix'])
        print("no kwargs required, returning default result")
        return keffres

    def dict_filter(self, ldict, lkeys):
        '''Dictionary filtration.'''
        print("\x1b[32m>>>>>>>> dict_filter >>>>>>>>>>>\x1b[0m")
        print(lkeys)
        if not lkeys:
            print("Nothing to do, will return the dict as it is")
            # return ldict
            print("\x1b[92m<<<<<<<< dict_filter <<<<<<<<<<<\x1b[0m")
            return ldict
        if lkeys[0] is None:
            for key, val in ldict.items():
                print('\x1b[94m', key, ': self.dict_filter(', val, ', ',
                      lkeys[1:], ')\x1b[0m')
            tdict = {k: self.dict_filter(v, lkeys[1:])
                     for k, v in ldict.items()}
            print("\x1b[35m", tdict, "\x1b[0m")
            # print("TEST atdict")
            # atdict = self.dict_filter(ldict, lkeys[1:])
            # print(atdict)
            return tdict
        print("IN THE ELSE")
        print(ldict[lkeys[0]])
        print("tdict")
        tdict = {lkeys[0]: self.dict_filter(ldict[lkeys[0]], lkeys[1:])}
        print("tlist")
        tlist = self.dict_filter(ldict[lkeys[0]], lkeys[1:])
        print("\x1b[33m", tdict, "\x1b[0m")
        print("\x1b[93m", tlist, "\x1b[0m")
        print("\x1b[32m<<<<<<<< dict_filter <<<<<<<<<<<\x1b[0m")
        return tlist

    def get_ifp(self, response, **kwargs):
        '''Get IFP results.'''
        print(self.ordered_res[response]['results'][0])
        assert self.ordered_res[response]['results'][0] == 'ifp_res'
        print(kwargs)
        ifpres = self.ordered_res[response]['results'][1]
        print(list(ifpres.keys()))
        ifpscores = ifpres['scores'].copy()
        lnames = [kwargs.get(name) for name in ifpres['index']]
        print(ifpres["index"])
        print(lnames)
        print(ifpres)
        if not kwargs:
            print("no kwargs required, will return dict of all scores")
            print(dcv.convert_ifp_in_dataset(ifpres['scores']))
            return dcv.convert_ifp_in_dataset(ifpres['scores'])
        return dcv.convert_ifp_in_dataset(self.dict_filter(ifpscores, lnames))
        # ndict = self.dict_filter(ifpscores, lnames)
        # print("ndict =", ndict)
        # if 'nucleus' in kwargs and ifpres['index'] == ['nucleus']:
        #     print("will return required nucleus if exists")
        #     return convert_intres_as_dataset(
        #        ifpres['scores'][kwargs['nucleus']], 'ifp_'+kwargs['nucleus'])
        # print("keyword arguments not already taken into account")
        # return None

    def get_sensitivity(self, response, **kwargs):
        '''Get IFP results.'''
        LOGGER.debug(">>>>>>>>>>>>> get_sensitivity <<<<<<<<<<<<<<<<<")
        assert self.ordered_res[response]['results'][0] == 'sensitivity_res'
        LOGGER.debug("kargs = %s", str(kwargs))
        ifpres = self.ordered_res[response]['results'][1]
        sdata = None
        # tindex = Index(ifpres)
        # if not kwargs:
        #     sdata = tindex.get_by(nucleus='U235', subtype="DELAYED FISSION_NU",
        #                           data_type='energy_integrated')
        # else:
        #     sdata = tindex.get_by(**kwargs)
        LOGGER.debug(">>>>>>>>>>>> end get_sensitivity <<<<<<<<<<<<<<")
        return sdata

    def get_from_response(self, response, res_type, zone=0):
        '''Generic method to get response.'''
        if self.ordered_res[response]['results'][0] == 'score_res':
            # autre possibilite: kwargs, verification que res_type et zone sont
            # presents
            score = self.get_score(response)
            if res_type not in score[zone]:
                print(list(score[zone].keys()))
                return None
            return dcv.CONVERT_IN_DATASET[res_type](score[zone][res_type],
                                                    res_type)
        return self.get_generic_score(response)
