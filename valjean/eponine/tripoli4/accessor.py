'''
Module to access Tripoli-4 parsed results.

  * :class:`Accessor` that allows to access and select in easier way the
    various elements of the parsing results, using internally the 2 follwing
    classes;


Description of :class:`Accessor`
--------------------------------

The :class:`Accessor` class is the real access point to the list of responses
but not only. The result from parsing is its default input. This parsing result
is necessarly a dictionary, i.e. if you get a list of dictionary because you
required to parse more than one batch you'll need to access them thanks to a
loop over the list of batches. Accessor also allows simplified access to other
data like simulation time or number of batch.

For example, let's consider a parsing results that contains the same ``orders``
as in :mod:`.response_book`, represented as a list of dictionaries. It will be
stored under the key ``'list_responses'`` and additional items will be added to
that dictionary for it to look like a default parsing results one.

>>> from valjean.eponine.tripoli4.accessor import Accessor
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
>>> pres = {'edition_batch_number': 42, 'list_responses': orders}
>>> pprint(pres)  # doctest: +NORMALIZE_WHITESPACE
{'edition_batch_number': 42, 'list_responses':\
 [{'consumer': 'Terry', 'drink': 'beer', 'response_function': 'menu1', \
'results': {'ingredients_res': ['egg', 'bacon']}},\
 {'consumer': 'John', 'response_function': 'menu2', \
'results': [{'ingredients_res': ['egg', 'spam']}, {'ingredients_res': [\
'tomato', 'spam', 'bacon']}]},\
 {'consumer': 'Graham', 'drink': 'coffee', 'response_function': 'menu1', \
'results': [{'ingredients_res': ['spam', 'egg', 'spam']}]},\
 {'consumer': 'Eric', 'drink': 'beer', 'response_function': 'menu3', \
'results': {'ingredients_res': ['sausage'], 'side_res': 'baked beans'}},\
 {'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy', \
'response_function': 'royal_menu', \
'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]}

Construction accessor and responses book:

>>> t4acc = Accessor(pres)
>>> if t4acc.resp_book:
...    print("Found a responses book")
Found a responses book
>>> print(t4acc.resp_book)
ResponseBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'response_function']

Examples of use:

>>> menu_with_dessert = t4acc.get_by(dessert=3)
>>> pprint(menu_with_dessert)  # doctest: +NORMALIZE_WHITESPACE
[{'consumer': 'Michael', 'dessert': 3, 'drink': 'brandy',\
 'response_function': 'royal_menu', \
 'results': {'dish_res': ['lobster thermidor', 'Mornay sauce']}}]
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


For the moment only two keys allow the construction of a responses book:
``'list_responses'`` (default) and ``'ifp_adjoint_crit_edition'``, others
return an error.

>>> pres2 = {'edition_batch_number': 42, 'ifp_adjoint_crit_edition': orders}
>>> t4acc2 = Accessor(pres2, book_type='ifp_adjoint_crit_edition')
>>> print(t4acc2.resp_book)
ResponseBook object -> Number of responses: 5, data key: 'results', \
available metadata keys: ['consumer', 'dessert', 'drink', 'response_function']

>>> pres3 = {'edition_batch_number': 42, 'and_these_are_our_meals': orders}
>>> t4acc3 = Accessor(pres3)
>>> # prints: ERROR     accessor: The required book_type apparently failed, \
... its shape might not be suitable, please check. Currently available and  \
... tested: ('list_responses', 'ifp_adjoint_crit_edition')
>>> print(t4acc3.resp_book)
None


Module API
----------
'''

import logging
from ..response_book import ResponseBook


LOGGER = logging.getLogger('valjean')


class Accessor:
    '''Class to access T4 results in a friendly way.

    This class contains two members:

        * parsed_res = result from parsing for only one batch
        * :class:`.response_book.ResponseBook` corresponding to the list of
            responses if it exists
    '''

    def __init__(self, tparsed_res, book_type='list_responses'):
        '''Create an :class:`Accessor` from a list of responses.

        :param list(dict) tparsed_res: result from parsing (for the moment not
                                       the result from scan, so some things
                                       might be missing like initialization
                                       time)
        '''
        self.parsed_res = tparsed_res
        self.resp_book = (ResponseBook(self.parsed_res[book_type])
                          if book_type in self.parsed_res
                          else None)
        if self.resp_book:
            LOGGER.debug("RESP_BOOK exists")
        else:
            if book_type not in self.parsed_res:
                LOGGER.error("The required book_type apparently failed, "
                             "its shape might not be suitable, please check. "
                             "Currently available and tested: "
                             "('list_responses', 'ifp_adjoint_crit_edition',"
                             "'default_keffs')")

    def get_by(self, **kwargs):
        '''Selection method based on kwargs corresponding to responses / scores
        characteristics (response_function, score_name, scoring_zone_id, etc).

        :param \\**\\kwargs: keyword arguments to specify the required
          response. More than one are allowed.
        :returns: :class:`~valjean.eponine.response_book.ResponseBook`
          (subset of the default one, corresponding to the selection)
        '''
        return self.resp_book.select_by(**kwargs)

    def simulation_time(self):
        '''Return simulation time.'''
        return self.parsed_res.get('simulation_time', -1)

    def edition_batch_number(self):
        '''Return edition batch number.'''
        return self.parsed_res.get('edition_batch_number', '?')
