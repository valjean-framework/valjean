'''Module to access Tripoli-4 parsed results and convert them in standard
:class:`Dataset <valjean.eponine.dataset.Dataset>`, easily comparable to other
codes.
'''

import logging
import pprint
from valjean.eponine.dataset import Dataset

LOGGER = logging.getLogger('valjean')
PP = pprint.PrettyPrinter(indent=4, depth=1)


def convert_spectrum_as_dataset(spec_res):
    '''Conversion of spectrum in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    dsspec = Dataset.Data(
        spec_res['spectrum']['score'],
        spec_res['spectrum']['sigma'] * spec_res['spectrum']['score'] / 100)
    bins = {key.replace('bins', ''): val
            for key, val in spec_res.items() if "bins" in key}
    return Dataset(dsspec, bins, 'spectrum', '')


def convert_mesh_as_dataset(mesh_res):
    '''Conversion of mesh in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    print(mesh_res['mesh'].dtype)
    dsmesh = Dataset.Data(
        mesh_res['mesh']['tally'],
        mesh_res['mesh']['sigma'] * mesh_res['mesh']['tally'] / 100)
    bins = {key.replace('bins', ''): val
            for key, val in mesh_res.items() if "bins" in key}
    return Dataset(dsmesh, bins, 'mesh', '')


def convert_intres_as_dataset(result, res_type):
    '''Conversion of integrated result (or generic score) in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.
    '''
    print("\x1b[35m", result, "\x1b[0m")
    dsintres = Dataset.Data(result['score'],
                            result['sigma'] * result['score'] / 100)
    return Dataset(dsintres, {}, res_type, '')


def convert_entropy_as_dataset(result, res_type):
    '''Conversion of entropy in :class:`Dataset
    <valjean.eponine.dataset.Dataset>`.

    .. todo::

        think if should be coded as generic score or not (no error), this
        may need a change in grammar.

    '''
    print("\x1b[35m", result, "\x1b[0m")
    dsentrop = Dataset.Data(result, 0)
    return Dataset(dsentrop, {}, res_type, '')


def convert_keff_in_dataset(result, estimator):
    '''Conversion of keff in :class:`Dataset`.'''
    id_estim = result['estimators'].index(estimator)
    print("estimator index =", id_estim)
    print("essai keff =", result['keff_matrix'][id_estim][id_estim])
    dskeff = Dataset.Data(
        result['keff_matrix'][id_estim][id_estim],
        (result['sigma_matrix'][id_estim][id_estim]
         * result['keff_matrix'][id_estim][id_estim] / 100))
    return Dataset(dskeff, {}, 'keff_'+estimator, '')


def convert_keff_comb_in_dataset(result):
    '''Conversion of keff combination in dataset.'''
    kcomb = result['full_comb_estimation']
    dskeff = Dataset.Data(kcomb['keff'],
                          kcomb['sigma']*kcomb['keff']/100)
    return Dataset(dskeff, {}, 'keff_combination', '')


CONVERT_IN_DATASET = {
    'spectrum_res': convert_spectrum_as_dataset,
    'mesh_res': convert_mesh_as_dataset,
    'shannon_entropy': convert_entropy_as_dataset,
    'boltzmann_entropy': convert_entropy_as_dataset,
    'integrated_res': convert_intres_as_dataset
}


class Accessor:
    '''Class to access T4 results in a friendly way.
    parsed_res = only one batch
    '''

    def __init__(self, tparsed_res):
        self.parsed_res = tparsed_res
        self.ordered_res = None

    def _by_response_description(self, keyword):
        assert 'list_responses' in self.parsed_res.keys()
        tdict = dict(map(
            lambda xy: (xy[1]['response_description'].get(keyword), xy[1]),
            enumerate(self.parsed_res['list_responses'])))
        if len(tdict) < len(self.parsed_res['list_responses']):
            LOGGER.warning("Some responses are missing from dictionary,"
                           " probably due to identical %s", keyword)
        return tdict

    def by_score_name(self):
        '''Order responses by score name.'''
        print(list(self.parsed_res.keys()))
        tdict = self._by_response_description('score_name')
        PP.pprint(tdict)
        self.ordered_res = tdict

    def by_response_function(self):
        '''Order responses by response function.'''
        tdict = self._by_response_description('resp_function')
        print("\x1b[34m")
        PP.pprint(tdict)
        print("\x1b[0m")
        self.ordered_res = tdict

    def by_response_index(self):
        '''Order responses by index.'''
        assert 'list_responses' in self.parsed_res.keys()
        self.ordered_res = dict(enumerate(self.parsed_res['list_responses']))
        PP.pprint(self.ordered_res)

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

    def get_ifp(self, response, **kwargs):
        '''Get IFP results.'''
        assert self.ordered_res[response]['results'][0] == 'ifp_res'
        print(kwargs)
        ifpres = self.ordered_res[response]['results'][1]
        print(ifpres)
        if not kwargs:
            print("no kwargs required, will return dict of all scores")
            return ifpres['scores']
        if 'nucleus' in kwargs and ifpres['index'] == ['nucleus']:
            print("will return required nucleus if exists")
            return convert_intres_as_dataset(
                ifpres['scores'][kwargs['nucleus']], 'ifp_'+kwargs['nucleus'])
        print("keyword arguments not already taken into account")
        return None

    def get_from_response(self, response, res_type, zone=0):
        '''Generic method to get response.'''
        if self.ordered_res[response]['results'][0] == 'score_res':
            # autre possibilite: kwargs, verification que res_type et zone sont
            # presents
            score = self.get_score(response)
            return CONVERT_IN_DATASET[res_type](score[zone][res_type])
        return self.get_generic_score(response)
