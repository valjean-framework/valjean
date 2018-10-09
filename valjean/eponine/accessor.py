'''Module to access Tripoli-4 parsed results and convert them in standard
:class:`Dataset <valjean.eponine.dataset.Dataset>`, easily comparable to other
codes.
'''

import logging
import pprint
from collections import defaultdict, Mapping


LOGGER = logging.getLogger('valjean')
PP = pprint.PrettyPrinter(indent=4, depth=2)


def merge_defaultdict(defd1, defd2):
    '''Function to merge 2 dict of defaultdict(set).'''
    mdefd = defd1.copy()
    for key1, val1 in defd2.items():
        if key1 in mdefd:
            for key2, val2 in val1.items():
                mdefd[key1][key2] |= val2
        else:
            mdefd[key1] = val1
    return mdefd


class Index(Mapping):
    '''Class to describe index used in ResponsesBook.

    Default structure of Index is a ``defaultdict(defaultdict(set))``.
    This class was derived mainly for printing purposes.
    '''

    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(set))

    def __str__(self):
        lstr = ["{"]
        for i, (key, dset) in enumerate(sorted(self.index.items())):
            lstr.append('{0!r}: {{'.format(key))
            for j, (dkey, ind) in enumerate(sorted(dset.items(), key=str)):
                lstr.append('{0!r}: {1!r}'.format(dkey, ind))
                if j < len(dset) - 1:
                    lstr.append(', ')
            lstr.append('}')
            if i < len(self.index) - 1:
                lstr.append(', ')
        lstr.append('}')
        return ''.join(lstr)

    def __getitem__(self, item):
        return self.index[item]

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def strip(self, ids):
        '''Get an :class:`Index` containing only the relevant keywords for the
        required set of ids.
        '''
        assert isinstance(ids, set)
        lind = Index()
        if not ids:
            return lind
        for key in self.index:
            for kwd, kset in self.index[key].items():
                tmpset = kset & ids
                if tmpset:
                    lind[key][kwd] = tmpset
        return lind


class ResponsesBook:
    '''Class to perform selections on results.

    This class is based on two objects:

      * the responses, as a list of dictionaries (containing data and metadata)
      * an index based on responses allowing easy selections on each metadata.

    Building the index:

        >>> from valjean.eponine.accessor import ResponsesBook
        >>> from pprint import pprint
        >>> commands = [
        ... {'resp_function': 'menu1', 'consumer': 'Terry', 'drink': 'beer',
        ...  'results': {'ingredients_res': ['egg', 'bacon']}},
        ... {'resp_function': 'menu2', 'consumer': 'John',
        ...  'results': [{'ingredients_res': ['egg', 'spam']},
        ...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
        ... {'resp_function': 'menu1', 'consumer': 'Graham', 'drink': 'coffee',
        ...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
        ... {'resp_function': 'menu3', 'consumer': 'Eric', 'drink': 'beer',
        ...  'results': {'ingredients_res': ['sausage'],
        ...              'side_res': 'baked beans'}},
        ... {'resp_function': 'royal_menu', 'consumer': 'Michael',
        ...  'drink': 'brandy', 'dessert': 'cheesecake',
        ...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
        >>> com_rb = ResponsesBook(commands)
        >>> print(com_rb.index)  # doctest: +NORMALIZE_WHITESPACE
        {'consumer': {'Eric': {3}, 'Graham': {2}, 'John': {1}, 'Michael': {4},\
 'Terry': {0}}, 'dessert': {'cheesecake': {4}},\
 'drink': {'beer': {0, 3}, 'brandy': {4}, 'coffee': {2}},\
 'resp_function': {'menu1': {0, 2}, 'menu2': {1}, 'menu3': {3},\
 'royal_menu': {4}}}

    Various methods are available to select responses, depending on
    requirements:

      * get the index of the response:

      >>> ind = com_rb.select_index_by(resp_function='menu1')
      >>> print(ind)  # doctest: +NORMALIZE_WHITESPACE
      {'consumer': {'Graham': {2}, 'Terry': {0}},\
 'drink': {'beer': {0}, 'coffee': {2}},\
 'resp_function': {'menu1': {0, 2}}}

      * get the response index in the list:

      >>> ind = com_rb.select_responses_id_by(drink='coffee')
      >>> pprint(ind)
      {2}

      * get the response:

      >>> resp = com_rb.select_responses_by(consumer='John')
      >>> pprint(resp)  # doctest: +NORMALIZE_WHITESPACE
      [{'consumer': 'John', 'resp_function': 'menu2', \
'results': [{'ingredients_res': ['egg', 'spam']}, \
{'ingredients_res': ['tomato', 'spam', 'bacon']}]}]

      * get a new ResponsesBook:

      >>> sel_rb = com_rb.select_by(resp_function='menu1', drink='beer')
      >>> print(sel_rb.index)  # doctest: +NORMALIZE_WHITESPACE
      {'consumer': {'Terry': {0}}, 'drink': {'beer': {0}}, \
'resp_function': {'menu1': {0}}}
      >>> pprint(sel_rb.responses)  # doctest: +NORMALIZE_WHITESPACE
      [{'consumer': 'Terry',  'drink': 'beer', 'resp_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}}]

      * if the required key doesn't exist a warning is sent:

      >>> sel_rb = com_rb.select_by(quantity=5)
        WARNING     accessor: quantity not a valid key. Possible ones are \
['consumer', 'dessert', 'drink', 'resp_function']

      * if the value corresponding to the key doesn't exist another warning is
        reached:

      >>> sel_rb = com_rb.select_by(drink='wine')
        WARNING     accessor: wine is not a valid drink

      * selection using squeeze:

      >>> resp = com_rb.select_by_with_squeeze(consumer='Graham', squeeze=True)
      >>> pprint(resp)  # doctest: +NORMALIZE_WHITESPACE
      {'consumer': 'Graham', 'drink': 'coffee', 'resp_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}

      * squeeze is not possible if more than one result corresponds to the
        required selection

      >>> resps = com_rb.select_by_with_squeeze(drink='beer', squeeze=True)
        WARNING     accessor: Squeeze cannot be applied, more than one \
response correspond to your choice

      but you can still get them thanks to:

      >>> sel_rb = com_rb.select_responses_by(drink='beer')
      >>> pprint(sel_rb)  # doctest: +NORMALIZE_WHITESPACE
      [{'consumer': 'Terry', 'drink': 'beer', 'resp_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}}, \
{'consumer': 'Eric', 'drink': 'beer', 'resp_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}}]

    '''

    def __init__(self, resp, data_key='results'):
        self.responses = resp
        self.index = self.build_index(data_key)
        LOGGER.debug("Index: %s", self.index)

    def build_index(self, data_key='results'):
        '''Build index from all responses in the list.

        Keys of the sets are keywords used to describe the responses and/or the
        scores (if flat case).
        '''
        index = Index()
        for iresp, resp in enumerate(self.responses):
            for key in resp:
                if key != data_key:
                    index[key][resp[key]].add(iresp)
        return index

    def select_responses_id_by(self, **kwargs):
        '''Selection of responses indices according to kwargs criteria.'''
        respids = set(range(len(self.responses)))
        for kwd in kwargs:
            if kwd not in list(self.index.keys()):
                LOGGER.warning("%s not a valid key. Possible ones are %s",
                               kwd, sorted(list(self.index.keys())))
                return set()
            if kwargs[kwd] not in self.index[kwd]:
                LOGGER.warning("%s is not a valid %s", kwargs[kwd], kwd)
                return set()
            respids = respids & self.index[kwd][kwargs[kwd]]
        if not respids:
            LOGGER.warning("Wrong selection, response might be not present. "
                           "Also check if requirements are consistant.")
            return set()
        return respids

    def select_index_by(self, **kwargs):
        '''Get index corresponding to selection given thanks to keyword
        arguments.
        '''
        respids = self.select_responses_id_by(**kwargs)
        return self.index.strip(respids)

    def select_responses_by(self, **kwargs):
        '''Get response corresponding to selection given thanks to keyword
        arguments.
        '''
        respids = self.select_responses_id_by(**kwargs)
        return [self.responses[i] for i in respids]

    def select_by(self, **kwargs):
        '''Get a ResponsesBook corresponding to selection from keyword
        arguments.
        '''
        respids = self.select_responses_id_by(**kwargs)
        lresp = [self.responses[i] for i in respids]
        sub_rb = ResponsesBook(lresp)
        return sub_rb

    def select_by_with_squeeze(self, *, squeeze=False, **kwargs):
        '''Get a ResponsesBook corresponding to selection from keyword
        arguments.

        PAS CONVAINCUE DE CE QUE L'ON VEUT...
        '''
        respids = self.select_responses_id_by(**kwargs)
        lresp = [self.responses[i] for i in respids]
        sub_rb = ResponsesBook(lresp)
        if squeeze:
            if len(lresp) > 1:
                LOGGER.warning("Squeeze cannot be applied, more than one "
                               "response correspond to your choice")
                return None
            return lresp[0]
        return sub_rb


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
            LOGGER.debug("RESP_BOOK exists")

    # get_by (but what ?), get_response_by (but we can get a score even by
    # scoring zone), get_score_by ?, get_result_by ?, select_by ?
    # CAUTION: this method can fail if 'list_responses' does not exist in the
    # parsed result
    # OU LE SQUEEZE SEULEMENT LA -> PAS DU RESSORT DE ResponsesBook ?
    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (resp_function, score_name, scoring_zone_id, etc).
        '''
        if kwargs is None:
            return self.resp_book.responses
        return self.resp_book.select_by(**kwargs)

    def simulation_time(self):
        '''Return simulation time.'''
        return self.parsed_res.get('simulation_time', -1)

    def edition_batch_number(self):
        '''Return edition batch number.'''
        return self.parsed_res.get('edition_batch_number', '?')
