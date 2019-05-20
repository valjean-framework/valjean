'''Module to access in easy way results stored in list of dictionaries.

This module is composed of 2 classes:

  * :class:`ResponseBook` that stores the list of dictionaries and builds an
    :class:`Index` to facilitate selections;
  * :class:`Index` based on :class:`collections.defaultdict` to perform
    selections on the list of dictionaries


The classes :class:`Index` and :class:`ResponseBook` are meant to be general
even if they will be shown and used in our specific case: parsing results from
Tripoli-4.


The :class:`Index` class
------------------------

This class is based on an inheritance from :class:`collections.abc.Mapping`
from :mod:`collections`. It implements a ``defaultdict(defaultdict(set))`` from
:class:`collections.defaultdict`.

:class:`set` contains `int` that corresponds to the index of the dictionary in
the list of dictionaries.

:class:`Index` is not supposed to be used standalone, but called from
:class:`ResponseBook`, but this is still possible.


The :class:`ResponseBook` class
-------------------------------

This class is analogue to a phonebook: it contains an index and the content,
here stored as a list of dictionaries. It commands the index (building and
selections). Examples are shown below.


.. _resp-book-example:

Building the responses book
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's consider a bunch of friends going to the restaurant and ordering their
menus. For each of them the waiter has to remember their name, under
``'consumer'``, their choice of menu under ``'response_function'``, their
drink, what they precisely order as dish under ``'results'`` and optionally the
number corresponding to their choice of dessert. He will represent these orders
as a list of orders, one order being a dictionary.

>>> from valjean.eponine.response_book import ResponseBook
>>> from pprint import pprint
>>> orders = [
... {'response_function': 'menu1', 'consumer': 'Terry', 'drink': 'beer',
...  'results': {'ingredients_res': ['egg', 'bacon']}},
... {'response_function': 'menu2', 'consumer': 'John',
...  'results': [{'ingredients_res': ['egg', 'spam']},
...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
... {'response_function': 'menu1', 'consumer': 'Graham', 'drink': 'coffee',
...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
... {'response_function': 'menu3', 'consumer': 'Eric', 'drink': 'beer',
...  'results': {'ingredients_res': ['sausage'],
...              'side_res': 'baked beans'}},
... {'response_function': 'royal_menu', 'consumer': 'Michael',
...  'drink': 'brandy', 'dessert': 3,
...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
>>> com_rb = ResponseBook(orders)
>>> print(com_rb)
ResponseBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'index', \
'response_function']
                    -> Number of globals: 0


Selection of a given response or of a list of responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Various methods are available to select one order, depending on requirements:

  * get a new ResponseBook:

    >>> sel_rb = com_rb.filter_by(response_function='menu1', drink='beer')
    >>> pprint(sel_rb.responses)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Terry',  'drink': 'beer', 'index': 0, \
'response_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}}]

    * check if a key is present or not:

    >>> 'drink' in sel_rb
    True
    >>> 'dessert' in sel_rb
    False
    >>> 'dessert' in com_rb
    True

    The ``'dessert'`` key has been removed from the ResponseBook issued from
    the selection while it is still present in the original one.

  * get the available keys (sorted to be able to test them in the doctest, else
    list is enough):

    >>> sorted(sel_rb.keys())
    ['consumer', 'drink', 'index', 'response_function']
    >>> sorted(com_rb.keys())
    ['consumer', 'dessert', 'drink', 'index', 'response_function']

  * if the required key doesn't exist a warning is emitted:

    >>> sel_rb = com_rb.filter_by(quantity=5)
    >>> # prints  WARNING     accessor: quantity not a valid key. Possible \
ones are ['consumer', 'dessert', 'drink', 'index', 'response_function']
    >>> 'quantity' in com_rb
    False

  * if the value corresponding to the key doesn't exist another warning is
    emitted:

    >>> sel_rb = com_rb.filter_by(drink='wine')
    >>> # prints  WARNING     accessor: wine is not a valid drink

  * to know the available values corresponding to the keys (without the
    corresponding responses indexes):

    >>> sorted(com_rb.available_values('drink'))
    ['beer', 'brandy', 'coffee']

  * if the key doesn't exist an 'empty generator' is emitted:

    >>> sorted(com_rb.available_values('quantity'))
    []

  * to directly get the responses corresponding to the selection, use the
    method :func:`ResponseBook.select_by`

    >>> sel_rb = com_rb.select_by(consumer='Graham')
    >>> type(sel_rb)
    <class 'list'>
    >>> len(sel_rb)
    1
    >>> pprint(sel_rb)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Graham', 'drink': 'coffee', 'index': 2, \
'response_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}]

  * this also work when more than one response corresponds to the selection:

    >>> sel_rb = com_rb.select_by(drink='beer')
    >>> pprint(sel_rb)  # doctest: +NORMALIZE_WHITESPACE
    [{'consumer': 'Terry', 'drink': 'beer', 'index': 0, \
'response_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}}, \
{'consumer': 'Eric', 'drink': 'beer', 'index': 3, \
'response_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}}]
    >>> len(sel_rb)
    2

  * a *squeeze* option is also available to directly get the response (and not
    a list of responses) when **only one** response corresponds to the
    selection (its default is at False):

    >>> resp = com_rb.select_by(consumer='Graham', squeeze=True)
    >>> pprint(resp)  # doctest: +NORMALIZE_WHITESPACE
    {'consumer': 'Graham', 'drink': 'coffee', 'index': 2, \
'response_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]}

  * squeeze is not possible if more than one result corresponds to the
    required selection

    >>> resps = com_rb.select_by(drink='beer', squeeze=True)
    >>> # prints  WARNING     accessor: Squeeze cannot be applied, more than \
one response corresponds to your choice


Module API
----------
'''

import logging
from collections import defaultdict, Mapping, Container


LOGGER = logging.getLogger('valjean')


def _make_defaultdict_set():
    '''The sole purpose of this function is to give a name to the defaultdict
    factory in :meth:`Index.index`. Without a name, the :class:`Index` class
    cannot be serialized by :mod:`pickle`.
    '''
    return defaultdict(set)


class Index(Mapping):
    '''Class to describe index used in ResponseBook.

    The structure of Index is a ``defaultdict(defaultdict(set))``.  This class
    was derived mainly for pretty-printing purposes.

    Quick example of index (menu for 4 persons, identified by numbers, one has
    no drink):

    >>> from valjean.eponine.response_book import Index
    >>> myindex = Index()
    >>> myindex.index['drink']['beer'] = {1, 4}
    >>> myindex.index['drink']['wine'] = {2}
    >>> myindex.index['menu']['spam'] = {1, 3}
    >>> myindex.index['menu']['egg'] = {2}
    >>> myindex.index['menu']['bacon'] = {4}
    >>> myindex.dump(sort=True)
    "{'drink': {'beer': {1, 4}, 'wine': {2}}, \
'menu': {'bacon': {4}, 'egg': {2}, 'spam': {1, 3}}}"
    >>> 'drink' in myindex
    True
    >>> 'consumer' in myindex
    False
    >>> len(myindex)
    2
    >>> for k in sorted(myindex):
    ...    print(k, sorted(myindex[k].keys()))
    drink ['beer', 'wine']
    menu ['bacon', 'egg', 'spam']

    The :func:`keep_only` method allows to get a sub-Index from a given set of
    ids (int), removing all keys not involved in the corresponding ids:

    >>> myindex.keep_only({2}).dump(sort=True)
    "{'drink': {'wine': {2}}, 'menu': {'egg': {2}}}"
    >>> menu_clients14 = myindex.keep_only({1, 4})
    >>> sorted(menu_clients14.keys()) == ['drink', 'menu']
    True
    >>> list(menu_clients14['drink'].keys()) == ['beer']
    True
    >>> list(menu_clients14['drink'].values()) == [{1, 4}]
    True
    >>> sorted(menu_clients14['menu'].keys()) == ['bacon', 'spam']
    True
    >>> menu_clients14['menu']['spam'] == {1}
    True
    >>> 3 in menu_clients14['menu']['spam']
    False
    >>> menu_client3 = myindex.keep_only({3})
    >>> list(menu_client3.keys()) == ['menu']
    True
    >>> 'drink' in menu_client3
    False

    The key ``'drink'`` has been removed from the last index as 2 did not
    required it.

    If you print an :class:`Index`, it looks like a standard dictionary (``{
    ... }`` instead of ``defaultdict(...)``) but the keys are not sorted:

    >>> print(myindex)
    {...: {...: {...}...}}
    '''

    def __init__(self):
        self.index = defaultdict(_make_defaultdict_set)

    def __str__(self):
        lstr = ["{"]
        for i, (key, dset) in enumerate(list(self.index.items())):
            lstr.append('{0!r}: {{'.format(key))
            for j, (dkey, ind) in enumerate(list(dset.items())):
                lstr.append('{0!r}: {1!r}'.format(dkey, ind))
                if j < len(dset) - 1:
                    lstr.append(', ')
            lstr.append('}')
            if i < len(self.index) - 1:
                lstr.append(', ')
        lstr.append('}')
        return ''.join(lstr)

    def __repr__(self):
        return self.index.__repr__()

    def __getitem__(self, item):
        return self.index.__getitem__(item)

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index)

    def __contains__(self, key):
        return self.index.__contains__(key)

    def keep_only(self, ids):
        '''Get an :class:`Index` containing only the relevant keywords for the
        required set of ids.

        :param set(int) ids: index corresponding to the required elements of
          the list of responses
        :returns: Index only containing the keys involved in the ids
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

    def dump(self, *, sort=False):
        '''Dump the Index.

        If ``sort == False`` (default case), returns :func:`__str__` result,
        else returns sorted Index (alphabetic order for keys).
        '''
        if sort:
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
        return str(self)


class ResponseBook(Container):
    '''Class to perform selections on results.

    This class is based on two objects:

      * the responses, as a list of dictionaries (containing data and metadata)
      * the key corresponding to data in the dictionary (default='results')
      * an index based on responses allowing easy selections on each metadata.

    Initialization parameters:

    :param list(dict) resp: list of responses
    :param str data_key: key in list of responses corresponding to results or
      data, that should not be used in index (as always present and mandatory)

    An additional key is added at the Index construction: ``'index'`` in order
    to keep track of the order of the list and being able to do selection on
    it.

    Examples on development / debugging methods:

    Let's use the example detailled above in
    :ref:`module introduction <resp-book-example>`:

    >>> from valjean.eponine.response_book import ResponseBook
    >>> orders = [
    ... {'response_function': 'menu1', 'consumer': 'Terry', 'drink': 'beer',
    ...  'results': {'ingredients_res': ['egg', 'bacon']}},
    ... {'response_function': 'menu2', 'consumer': 'John',
    ...  'results': [{'ingredients_res': ['egg', 'spam']},
    ...              {'ingredients_res': ['tomato', 'spam', 'bacon']}]},
    ... {'response_function': 'menu1', 'consumer': 'Graham', 'drink': 'coffee',
    ...  'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},
    ... {'response_function': 'menu3', 'consumer': 'Eric', 'drink': 'beer',
    ...  'results': {'ingredients_res': ['sausage'],
    ...              'side_res': 'baked beans'}},
    ... {'response_function': 'royal_menu', 'consumer': 'Michael',
    ...  'drink': 'brandy', 'dessert': 3,
    ...  'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
    >>> com_rb = ResponseBook(orders)

    * possibility to get the response id directly (internally used method):

      >>> ind = com_rb._filter_resp_id_by(drink='coffee')
      >>> isinstance(ind, set)
      True
      >>> print(ind)
      {2}

    * possibility to get the index of the response stripped without rebuilding
      the full ResponseBook:

      >>> ind = com_rb._filter_index_by(response_function='menu1')
      >>> isinstance(ind, Index)
      True
      >>> ind.dump(sort=True)  # doctest: +NORMALIZE_WHITESPACE
      "{'consumer': {'Graham': {2}, 'Terry': {0}}, \
'drink': {'beer': {0}, 'coffee': {2}}, 'index': {0: {0}, 2: {2}}, \
'response_function': {'menu1': {0, 2}}}"

      The 'dessert' key has been stripped from the index:

      >>> 'dessert' in ind
      False

    Debug print is available thanks to :func:`__repr__`:

    >>> small_order = [{'dessert': 1, 'drink': 'beer', 'results': ['spam']}]
    >>> so_rb = ResponseBook(small_order)
    >>> "{0!r}".format(so_rb)
    "<class 'valjean.eponine.response_book.ResponseBook'>, \
(Responses: ..., Index: ...)"
    '''

    def __init__(self, resp, data_key='results', global_vars=None):
        self.responses = resp
        self.data_key = data_key
        self.index = self._build_index()
        LOGGER.debug("Index: %s", self.index)
        self.globals = global_vars if isinstance(global_vars, dict) else {}

    def __eq__(self, other):
        return (self.responses == other.responses
                and self.data_key == other.data_key
                and self.globals == other.globals)

    def __ne__(self, other):
        return not self == other

    def _build_index(self):
        '''Build index from all responses in the list.

        Keys of the sets are keywords used to describe the responses and/or the
        scores (if flat case).

        :param str data_key: key in list of responses corresponding to results
          or data
        :returns: :class:`Index`
        '''
        index = Index()
        for iresp, resp in enumerate(self.responses):
            resp['index'] = iresp
            for key in resp:
                if key != self.data_key:
                    index[key][resp[key]].add(iresp)
        return index

    def __contains__(self, key):
        if key in self.index:
            return True
        return False

    def __len__(self):
        return len(self.responses)

    def is_empty(self):
        '''Check if the ResponseBook is empty or not.

        Empty meaning no responses AND no globals.
        '''
        return not self.responses and not self.globals

    def join(self, other):
        '''Join two ResponseBook.

        This junction is based on the global variables and on the list of
        responses, then the index is rebuilt on the top of it.

        :param ResponseBook other: another ResponseBook
        :rtype: ResponseBook
        '''
        if self.data_key != other.data_key:
            raise ValueError('Same data_key is required to join ResponseBooks')
        if self.globals != other.globals:
            LOGGER.warning('globals will be updated with other values')
        new_glob = self.globals.copy()
        new_glob.update(other.globals)
        new_resps = self.responses + other.responses
        LOGGER.debug("Nb self resps (%d) + Nb other resps (%d) = %d",
                     len(self), len(other), len(new_resps))
        return ResponseBook(new_resps, data_key=self.data_key,
                            global_vars=new_glob)

    def keys(self):
        '''Get the available keys in the index (so in the responses list). As
        usual it returns a generator.
        '''
        return self.index.keys()

    def available_values(self, key):
        '''Get the available keys in the *second* level, i.e. under the given
        external one.

        :param str key: 'external' key (from outer defaultdict)
        :returns: generator with corresponding keys (or empty one)
        '''
        if key in self:
            yield from self.index[key].keys()
        else:
            yield from ()

    def __str__(self):
        return ("{0} object -> Number of responses: {1}, "
                "data key: {2!r}, available metadata keys: {3}\n"
                "{4:>{5}}        -> Number of globals: {6}"
                .format(self.__class__.__name__, len(self.responses),
                        self.data_key, sorted(self.keys()), "",
                        len(self.__class__.__name__), len(self.globals)))

    def __repr__(self):
        return ("{0}, (Responses: {1!r}, Index: {2!r})"
                .format(self.__class__, self.responses, self.index))

    def _filter_resp_id_by(self, **kwargs):
        '''Selection of responses indices according to kwargs criteria.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :return: set of ids
        :rtype: set(int)
        '''
        respids = set(range(len(self.responses)))
        for kwd in kwargs:
            if kwd not in self.index:
                LOGGER.warning("%s not a valid key. Possible ones are %s",
                               kwd, sorted(self.keys()))
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

    def _filter_index_by(self, **kwargs):
        '''Get index corresponding to selection given thanks to keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`Index` (stripped from useless keys)
        '''
        respids = self._filter_resp_id_by(**kwargs)
        return self.index.keep_only(respids)

    def filter_by(self, include=(), exclude=(), **kwargs):
        '''Get a ResponseBook corresponding to selection from keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :param tuple(str) include: metadata keys required in the responses but
          for which the value is not necessarly known
        :param tuple(str) exclude: metadata that should not be present in the
          responses and for which the value is not necessarly known
        :returns: :class:`ResponseBook` (subset of the default one,
          corresponding to the selection)
        '''
        LOGGER.debug("in select_by, kwargs=%s", kwargs)
        sincl, sexcl = set(include), set(exclude)
        respids = self._filter_resp_id_by(**kwargs)
        lresp = [self.responses[i] for i in respids
                 if sincl.issubset(self.responses[i])
                 and not sexcl.intersection(self.responses[i])]
        sub_rb = ResponseBook(lresp)
        return sub_rb

    def select_by(self, *, squeeze=False, include=(), exclude=(), **kwargs):
        '''Get a ResponseBook corresponding to selection from keyword
        arguments.

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :param bool squeeze: named parameter
        :param tuple(str) include: metadata keys required in the responses but
          for which the value is not necessarly known
        :param tuple(str) exclude: metadata that should not be present in the
          responses and for which the value is not necessarly known
        :returns: first element of the list of responses if only one,
          else list of responses matching the requirements
        '''
        respids = self._filter_resp_id_by(**kwargs)
        sincl, sexcl = set(include), set(exclude)
        lresp = [self.responses[i] for i in respids
                 if sincl.issubset(self.responses[i])
                 and not sexcl.intersection(self.responses[i])]
        if squeeze:
            if not lresp:
                LOGGER.warning("No response corresponding to the selection.")
                return None
            if len(lresp) > 1:
                LOGGER.warning("Squeeze cannot be applied, more than one "
                               "response corresponds to your choice")
                return None
            return lresp[0]
        return lresp
