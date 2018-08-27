'''Module to access Tripoli-4 parsed results and convert them in standard
:class:`Dataset <valjean.eponine.dataset.Dataset>`, easily comparable to other
codes.
'''

import logging
import pprint
from collections import defaultdict, namedtuple, OrderedDict
from valjean.eponine.dataset import Dataset
from sys import getsizeof

LOGGER = logging.getLogger('valjean')
PP = pprint.PrettyPrinter(indent=4, depth=2)
Response = namedtuple('Response', ['type', 'data'])


def convert_spectrum_as_dataset(fspec_res, res_type='spectrum_res'):
    '''Conversion of spectrum in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    spec_res = fspec_res[res_type]
    dsspec = Dataset.Data(
        spec_res['spectrum']['score'],
        spec_res['spectrum']['sigma'] * spec_res['spectrum']['score'] / 100)
    bins = spec_res.get('bins')
    return Dataset(dsspec, bins, res_type, unit=spec_res['units']['score'])


def convert_mesh_as_dataset(fmesh_res, res_type='mesh_res'):
    '''Conversion of mesh in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    mesh_res = fmesh_res[res_type]
    print(mesh_res['mesh'].dtype)
    dsmesh = Dataset.Data(
        mesh_res['mesh']['score'],
        mesh_res['mesh']['sigma'] * mesh_res['mesh']['score'] / 100)
    bins = mesh_res.get('bins')
    return Dataset(dsmesh, bins, res_type, unit=mesh_res['units']['score'])


def convert_intres_as_dataset(result, res_type):
    '''Conversion of integrated result (or generic score) in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.

    Bins: only possible bin is energy as energy integrated results.
    If other dimensions are not squeezed it is a spectrum so not treated by
    this function.
    '''
    intres = result[res_type] if res_type in result else result
    dsintres = Dataset.Data(intres['score'],
                            intres['sigma'] * intres['score'] / 100)
    unit = intres.get('uscore', 'unknown')
    bins = OrderedDict()
    if 'spectrum_res' in result:
        if unit == 'unknown':
            unit = result['spectrum_res']['units']['score']
        ebins = result['spectrum_res']['bins']['e']
        bins = OrderedDict([('e', ebins[::ebins.shape[0]-1])])
    return Dataset(dsintres, bins, res_type, unit=unit)


def convert_entropy_as_dataset(result, res_type):
    '''Conversion of entropy in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.

    .. todo::

        think if should be coded as generic score or not (no error), this
        may need a change in grammar.

    '''
    print("\x1b[35m", result, "\x1b[0m")
    dsentrop = Dataset.Data(result, 0)
    return Dataset(dsentrop, {}, res_type)


def convert_keff_in_dataset(result, estimator):
    '''Conversion of keff in :class:`Dataset`.'''
    id_estim = result['estimators'].index(estimator)
    print("estimator index =", id_estim)
    print("essai keff =", result['keff_matrix'][id_estim][id_estim])
    dskeff = Dataset.Data(
        result['keff_matrix'][id_estim][id_estim],
        (result['sigma_matrix'][id_estim][id_estim]
         * result['keff_matrix'][id_estim][id_estim] / 100))
    return Dataset(dskeff, {}, 'keff_'+estimator)


def convert_keff_comb_in_dataset(result):
    '''Conversion of keff combination in dataset.'''
    kcomb = result['full_comb_estimation']
    dskeff = Dataset.Data(kcomb['keff'],
                          kcomb['sigma'] * kcomb['keff'] / 100)
    return Dataset(dskeff, {}, 'keff_combination')


def convert_ifp_in_dataset(result):
    '''Convert IFP in dataset...'''
    print(type(result))
    if not isinstance(result, dict):
        print("\x1b[1;31mISSUE !!!\x1b[0m")
        return None
    if 'score' not in result:
        tres = {k: convert_ifp_in_dataset(v) for k, v in result.items()}
        # for res in result.values():
        #     convert_ifp_in_dataset(res)
        return tres
    print("\x1b[1;38mFound np.ndarray !!!\x1b[0m")
    return convert_intres_as_dataset(result, 'ifp')


def convert_data_in_dataset(data, data_type):
    '''Convert data in dataset. OK for IFP sensitivities for the moment.'''
    if data_type not in data:
        LOGGER.warning("Key %s not found in data", data_type)
        return None
    dset = Dataset.Data(
        data[data_type]['score'],
        data[data_type]['sigma'] * data[data_type]['score'] / 100)
    # units and uscore used in sensitivities (calling default res)
    return Dataset(dset, data['bins'], data_type,
                   unit=data.get('units', {}).get('score', 'unknown'))


CONVERT_IN_DATASET = {
    'spectrum_res': convert_spectrum_as_dataset,
    'mesh_res': convert_mesh_as_dataset,
    'shannon_entropy': convert_entropy_as_dataset,
    'boltzmann_entropy': convert_entropy_as_dataset,
    'integrated_res': convert_intres_as_dataset
}


def convert_data(data, data_type):
    '''Test for data conversion using dict or default.'''
    if data_type not in data:
        LOGGER.warning("%s not found in data", data_type)
        return None
    return CONVERT_IN_DATASET.get(data_type, convert_data_in_dataset)(
        data, data_type)


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
        self.flatten()

    def flatten(self):
        '''Method to flatten the list of responses, including scores.'''
        for iresp, resp in enumerate(self.nested):
            if resp['results'].type != 'score_res':
                self.flat.append(resp)
                self.n2f[iresp] = len(self.flat) - 1
                continue
            rmd = {k: v for k, v in resp.items() if k != 'results'}
            for isc, score in enumerate(resp['results'].data):
                smd = {k: v for k, v in score.items() if '_res' not in k}
                smd.update(rmd)
                smd['results'] = Response(
                    resp['results'].type,
                    {k: v for k, v in score.items() if '_res' in k})
                self.flat.append(smd)
                self.n2f[(iresp, isc)] = len(self.flat) - 1

    def nested_indices(self, flat_indices):
        '''Get the indices in nested list corresponding to indices in flat
        list.
        '''
        print(flat_indices)
        print(self.n2f)
        sub_n2f = [k[0] if isinstance(k, tuple) else k
                   for k, v in self.n2f.items() if v in flat_indices]
        return sub_n2f

    def flat_indices(self, nested_index):
        '''Get flat indices from nested ones: return all flat indices for a
        given response for example.
        '''
        flat_ind = {v for k, v in self.n2f.items()
                    if nested_index in [k if isinstance(k, int) else k[0]]}
        print("flat indices:", flat_ind)
        return flat_ind


class IndexResponses:
    '''Class to index T4 responses, or flat ones, or nested ones. If responses
    are nested scores won't be flatten, this is just index. It should still be
    possible to flatten them afterwards.
    '''

    def __init__(self, lcases):
        print("\x1b[35m>>>>>>>> IndexResponses.__init__ <<<<<<<<<<\x1b[0m")
        self.ids = set(range(len(lcases)))
        print("mem lcases:", id(lcases), "lcases:", id(lcases))
        print("taille lcases:", getsizeof(lcases), "lcases:", getsizeof(lcases))
        print(list(lcases[0].keys()))
        self.dsets = {k: defaultdict(set)
                      for icase in lcases
                      for k in icase.keys() if k != 'results'}
        print("\x1b[91mself.dsets =", self.dsets, "\x1b[0m")
        LOGGER.debug("nb cases = %d", len(lcases))
        self._build_index(lcases)
        print(self.dsets)
        print("\x1b[35m>>>>>>>> END IndexResponses.__init__ <<<<<<<<<<\x1b[0m")

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
            LOGGER.warning("Response: %s", resp['resp_function'])
            for key in self.dsets:
                if key not in resp:
                    continue
                if not isinstance(resp[key], list):
                    self.dsets[key][resp[key]].add(iresp)
                else:
                    if isinstance(resp[key][0], dict):
                        theobject = []
                        for kcase in resp[key]:
                            theobject.append(
                                tuple((k, v) for k, v in kcase.items()))
                        theobject = tuple(theobject)
                    else:
                        # MACROSCOPIC RATE for ex
                        theobject = ': '.join(resp[key])
                    LOGGER.debug(theobject)
                    self.dsets[key][theobject].add(iresp)

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


class Accessor:
    '''Class to access T4 results in a friendly way.
    parsed_res = only one batch
    '''

    def __init__(self, tparsed_res):  # , merge_score=False):
        self.parsed_res = tparsed_res
        self.responses = None
        self.indflat = None
        self.indnest = None
        if 'list_responses' in self.parsed_res.keys():
            lresp = self.parsed_res['list_responses']
            print('nbre de responses =', len(lresp), "type =", type(lresp))
            print(list(lresp[0].keys()))
            self.responses = DataResponses(lresp)
            print(id(self.responses.nested))
            print(self.responses.n2f)
            print("\x1b[1mESSAIS\x1b[0m")
            print("-> index from flat:")
            self.indflat = IndexResponses(self.responses.flat)
            print(len(self.indflat))
            print("-> index from nested:")
            self.indnest = IndexResponses(self.responses.nested)
            print(len(self.indnest))
            print("\x1b[1m----------------------\x1b[0m")

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
        return resps[0] if len(resps) == 1 else resps

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
        return res[0] if len(res) == 1 else res

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
            return convert_spectrum_as_dataset(score[zone]['spectrum_res'])
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
        return convert_mesh_as_dataset(score[0]['mesh_res'])

    def get_intres_from_score(self, response, res_type='integrated_res',
                              zone=0):
        '''Get integrated result from response (and score).'''
        score = self.get_score(response)
        assert res_type in score[zone]
        return convert_intres_as_dataset(score[zone][res_type], res_type)

    def get_entropy_from_score(self, response, res_type):
        '''Get entropy from response (and score).'''
        score = self.get_score(response)
        assert res_type in score[0]
        return convert_entropy_as_dataset(score[0][res_type], res_type)

    # reflechir a mettre le nom de la reponse comme titre ici
    def get_generic_score(self, response):
        '''Get generic score from response.'''
        print(list(self.ordered_res.keys()))
        assert response in self.ordered_res
        print(self.ordered_res[response])
        return convert_intres_as_dataset(
            self.ordered_res[response]['results'][1], 'generic_score')

    def get_keff(self, **kwargs):
        '''Get keff (generic response).'''
        print(list(self.ordered_res.keys()))
        assert self.ordered_res['KEFFS']['results'][0] == 'keff_res'
        keffres = self.ordered_res['KEFFS']['results']
        print(keffres)
        print(list(keffres[1].keys()))
        if 'estimator' in kwargs:
            return convert_keff_in_dataset(keffres[1], kwargs['estimator'])
        if 'combination' in kwargs:
            return convert_keff_comb_in_dataset(keffres[1])
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
            print(convert_ifp_in_dataset(ifpres['scores']))
            return convert_ifp_in_dataset(ifpres['scores'])
        return convert_ifp_in_dataset(self.dict_filter(ifpscores, lnames))
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
            return CONVERT_IN_DATASET[res_type](score[zone][res_type],
                                                res_type)
        return self.get_generic_score(response)
