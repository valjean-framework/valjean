'''Module to access Tripoli-4 parsed results and convert them in standard
:class:`Dataset <valjean.eponine.dataset.Dataset>`, easily comparable to other
codes.

This module is composed of 3 classes:

  * :class:`Accessor` that allows to access and select in easier way the
    various elements of the parsing results, using internally the 2 follwing
    classes;
  * :class:`ResponsesBook` that stores the list of dictionaries and builds an
    :class:`Index` to facilitate selections;
  * :class:`Index` based on :class:`defaultdict` to perform selections on the
    list of dictionaries


The classes :class:`Index` and :class:`ResponsesBook` are meant to be general
even if they will be shown and used in our specific case: parsing results from
Tripoli-4.


:class:`Index`
--------------

This class is based on an inheritance from :class:`collections.abc.Mapping`
from :mod:`collections`. It implements a ``defaultdict(defaultdict(set))`` from
:class:`collections.defaultdict`.

:class:`set` contains `int` that correspond to the index of the dictionary in
the list of dictionaries.

:class:`Index` is not supposed to be used standalone, but called from
:class:`ResponsesBook`, but this is still possible.


:class:`ResponsesBook`
----------------------

This class is analogue to a phonebook: it contains an index and the content,
here stored as a list of dictinaries. It commands the index (building and
selections). Examples are shown below.


Building the responses book
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
    ...  'drink': 'brandy', 'dessert': 3,
    ...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
    >>> com_rb = ResponsesBook(commands)
    >>> print(com_rb.index)  # doctest: +NORMALIZE_WHITESPACE
    {'consumer': {'Eric': {3}, 'Graham': {2}, 'John': {1}, 'Michael': {4},\
 'Terry': {0}}, 'dessert': {3: {4}}, 'drink': {'beer': {0, 3}, 'brandy': {4},\
 'coffee': {2}}, 'resp_function': {'menu1': {0, 2}, 'menu2': {1},\
 'menu3': {3}, 'royal_menu': {4}}}

Various methods are available to select responses, depending on requirements:

  * get the index of the response:

  >>> ind = com_rb.select_index_by(resp_function='menu1')
  >>> print(ind)  # doctest: +NORMALIZE_WHITESPACE
  {'consumer': {'Graham': {2}, 'Terry': {0}}, \
'drink': {'beer': {0}, 'coffee': {2}}, 'resp_function': {'menu1': {0, 2}}}

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
  >>> # prints  WARNING     accessor: quantity not a valid key. Possible ones \
are ['consumer', 'dessert', 'drink', 'resp_function']
  >>> print(com_rb.index)
  {'consumer': {'Eric': {3}, 'Graham': {2}, 'John': {1}, 'Michael': {4}, \
'Terry': {0}}, 'dessert': {3: {4}}, 'drink': {'beer': {0, 3}, 'brandy': {4}, \
'coffee': {2}}, 'resp_function': {'menu1': {0, 2}, 'menu2': {1}, 'menu3': {3},\
 'royal_menu': {4}}}

  * if the value corresponding to the key doesn't exist another warning is
        reached:

  >>> sel_rb = com_rb.select_by(drink='wine')
  >>> # prints  WARNING     accessor: wine is not a valid drink

  * selection using squeeze:

  >>> resp = com_rb.select_by_with_squeeze(consumer='Graham', squeeze=True)
  >>> pprint(resp)  # doctest: +NORMALIZE_WHITESPACE
  {'consumer': 'Graham', 'drink': 'coffee', 'resp_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}

  * squeeze is not possible if more than one result corresponds to the
    required selection

  >>> resps = com_rb.select_by_with_squeeze(drink='beer', squeeze=True)
  >>> # prints  WARNING     accessor: Squeeze cannot be applied, more than one\
 response correspond to your choice

  but you can still get them thanks to:

  >>> sel_rb = com_rb.select_responses_by(drink='beer')
  >>> pprint(sel_rb)  # doctest: +NORMALIZE_WHITESPACE
  [{'consumer': 'Terry', 'drink': 'beer', 'resp_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}}, \
{'consumer': 'Eric', 'drink': 'beer', 'resp_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}}]


:class:`Accessor`
-----------------

The :class:`Accessor` class is the real access point to the list of responses
but not only. The result from parsing is its default input. This parsing result
is necessarly a dictionary, i.e. if you get a list of dictionary because you
required to parse more than one batch you'll need to access them thanks to a
loop over the list of batches. Accessor also allows simplified access to other
data like simulation time or number of batch.

For example, let's consider a parsing results that contains the ``commands``
list of dictionaries used above as example for :class:`ResponsesBook`. It will
now be stored under the key ``'list_responses'`` and additional items will be
added to that dictionary for it to look like a default parsing results one.

>>> from valjean.eponine.accessor import Accessor
>>> pres = {'edition_batch_number': 42, 'list_responses': commands}
>>> pprint(pres)  # doctest: +NORMALIZE_WHITESPACE
{'edition_batch_number': 42, 'list_responses':\
 [{'consumer': 'Terry', 'drink': 'beer', 'resp_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}},\
 {'consumer': 'John', 'resp_function': 'menu2', \
'results': [{'ingredients_res': ['egg', 'spam']}, {'ingredients_res': [\
'tomato', 'spam', 'bacon']}]},\
 {'consumer': 'Graham', 'drink': 'coffee', 'resp_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},\
 {'consumer': 'Eric', 'drink': 'beer', 'resp_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}},\
 {'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy', \
'resp_function': 'royal_menu', 'results': {'dish_res': ['lobster thermidor', \
'Mornay sauce']}}]}

Construction accessor and responses book:

>>> t4acc = Accessor(pres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
Found a responses book
>>> print(t4acc.resp_book.index)  # doctest: +NORMALIZE_WHITESPACE
{'consumer': {'Eric': {3}, 'Graham': {2}, 'John': {1}, 'Michael': {4},\
 'Terry': {0}}, 'dessert': {3: {4}}, 'drink': {'beer': {0, 3}, 'brandy': {4},\
 'coffee': {2}}, 'resp_function': {'menu1': {0, 2}, 'menu2': {1},\
 'menu3': {3}, 'royal_menu': {4}}}

Examples of use:

>>> menu_with_dessert = t4acc.get_by(dessert=3)
>>> pprint(menu_with_dessert.responses)  # doctest: +NORMALIZE_WHITESPACE
[{'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy',\
 'resp_function': 'royal_menu', 'results': {'dish_res': ['lobster thermidor',\
 'Mornay sauce']}}]
>>> batch = t4acc.edition_batch_number()
>>> print(batch)
42
>>> simu_time = t4acc.simulation_time()
>>> print(simu_time)
-1

If no list of responses is avalaible (for example in some creation runs):

>>> pres = {'edition_batch_number': 42, 'simulation_time': 4242}
>>> t4acc = Accessor(pres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
... else:
...    print("Did not found a responses book")
Did not found a responses book
>>> t4acc.edition_batch_number()
42
>>> t4acc.simulation_time()
4242
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
        LOGGER.debug("inside __getitem__")
        return self.index.__getitem__(item)

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def __contains__(self, key):
        LOGGER.debug("in __contains__")
        return self.index.__contains__(key)

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

    Initialization parameters:

    :param list(dict) resp: list of responses
    :param str data_key: key in list of responses corresponding to results or
      data, that should not be used in index (as always present and mandatory)
    '''

    def __init__(self, resp, data_key='results'):
        self.responses = resp
        self.index = self.build_index(data_key)
        LOGGER.debug("Index: %s", self.index)

    def build_index(self, data_key='results'):
        '''Build index from all responses in the list.

        Keys of the sets are keywords used to describe the responses and/or the
        scores (if flat case).

        :param str data_key: key in list of responses corresponding to results
          or data
        :returns: :class:`Index`
        '''
        index = Index()
        for iresp, resp in enumerate(self.responses):
            for key in resp:
                if key != data_key:
                    index[key][resp[key]].add(iresp)
        return index

    def select_responses_id_by(self, **kwargs):
        '''Selection of responses indices according to kwargs criteria.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`set(int)`
        '''
        respids = set(range(len(self.responses)))
        for kwd in kwargs:
            if kwd not in self.index:
                LOGGER.warning("%s not a valid key. Possible ones are %s",
                               kwd, sorted(list(self.index.keys())))
                return set()
            if kwargs[kwd] not in self.index[kwd]:
                LOGGER.warning("%s is not a valid %s", kwargs[kwd], kwd)
                return set()
            respids = respids & self.index[kwd][kwargs[kwd]]
        if not respids:
            LOGGER.warning("Wrong selection, response might be not present. "
                           "Also check if requirements are consistent.")
            return set()
        return respids

    def select_index_by(self, **kwargs):
        '''Get index corresponding to selection given thanks to keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`Index` (stripped from useless keys)
        '''
        respids = self.select_responses_id_by(**kwargs)
        return self.index.strip(respids)

    def select_responses_by(self, **kwargs):
        '''Get response corresponding to selection given thanks to keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: list of responses (dict) corresponding to the selection
        '''
        respids = self.select_responses_id_by(**kwargs)
        return [self.responses[i] for i in respids]

    def select_by(self, **kwargs):
        '''Get a ResponsesBook corresponding to selection from keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`ResponsesBook` (subset of the default one,
          corresponding to the selection)
        '''
        LOGGER.debug("in select_by, kwargs=%s", kwargs)
        respids = self.select_responses_id_by(**kwargs)
        lresp = [self.responses[i] for i in respids]
        sub_rb = ResponsesBook(lresp)
        return sub_rb

    def select_by_with_squeeze(self, *, squeeze=False, **kwargs):
        '''Get a ResponsesBook corresponding to selection from keyword
        arguments.

        PAS CONVAINCUE DE CE QUE L'ON VEUT...

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :param bool squeeze: named parameter
        :returns: first element of the list of responses if only one,
          else subset in :class:`ResponsesBook` format
        '''
        respids = self.select_responses_id_by(**kwargs)
        lresp = [self.responses[i] for i in respids]
        sub_rb = ResponsesBook(lresp)
        if squeeze:
            if not lresp:
                LOGGER.warning("No response corresponding to the selection.")
                return None
            if len(lresp) > 1:
                LOGGER.warning("Squeeze cannot be applied, more than one "
                               "response correspond to your choice")
                return None
            return lresp[0]
        return sub_rb


class Accessor:
    '''Class to access T4 results in a friendly way.
    parsed_res = only one batch

    :param list(dict) tparsed_res: result from parsing (for the moment not the
      result from scan, so some things might be missing like initialization
      time)
    '''

    def __init__(self, tparsed_res):  # , merge_score=False):
        self.parsed_res = tparsed_res
        self.resp_book = (ResponsesBook(self.parsed_res['list_responses'])
                          if 'list_responses' in self.parsed_res
                          else None)
        if self.resp_book:
            LOGGER.debug("RESP_BOOK exists")

    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (resp_function, score_name, scoring_zone_id, etc).

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`ResponsesBook` (subset of the default one,
          corresponding to the selection)
        '''
        return self.resp_book.select_by(**kwargs)

    def simulation_time(self):
        '''Return simulation time.'''
        return self.parsed_res.get('simulation_time', -1)

    def edition_batch_number(self):
        '''Return edition batch number.'''
        return self.parsed_res.get('edition_batch_number', '?')
