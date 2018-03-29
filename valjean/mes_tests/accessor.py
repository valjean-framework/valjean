'''Access to parsed data and get results in a more friendly way.'''

from valjean.eponine.parse_t4 import T4Parser
import logging

LOGGER = logging.getLogger('valjean')

class Accessor():
    '''Class to access T4 results in a friendly way.'''

    def __init__(self, jdd):
        self.fname = jdd
        self.parsed_res = T4Parser.parse_jdd(jdd, -1).result
        self.tables = self.default_tables()

    def default_tables(self):
        if 'list_responses' not in self.parsed_res[-1]:
            print("T4 listing seems hving no responses in last batch.")
            raise KeyError
        tables = {}
        self._add_to_table_from_res_desc(tables, 'score_name')
        self._add_to_table_from_res_desc(tables, 'resp_name')
        self._add_to_table_from_res_desc(tables, 'resp_function')
        self._add_to_table_from_res_desc(tables, 'energy_split_name')
        # possibility to put it on the call instead of here
        self._check_table(tables)
        return tables

    def _add_to_table_from_res_desc(self, table, keyword):
        allresp = self.parsed_res[-1]['list_responses']
        if keyword in allresp[0]['response_description']:
            table[keyword] = dict(map(
                lambda xy: (xy[1]['response_description'][keyword], xy[0]),
                enumerate(allresp)))
            if len(allresp) != len(table[keyword]):
                LOGGER.warning(
                    "N(resps) != N(%s): '%s' useless to identify responses.",
                    keyword, keyword)

    def _check_table(self, table):
        allresp = self.parsed_res[-1]['list_responses']
        bad_keys = []
        good_keys = []
        for key in table:
            if len(allresp) != len(table[key]):
                bad_keys.append(key)
            else:
                good_keys.append(key)
        LOGGER.warning("Keys %s are useless to identify responses (not 1 to 1)"
                       ", please use %s", bad_keys, good_keys)

    def get_response(self, response):
        print("nbre de responses:", len(self.parsed_res[-1]['list_responses']))
        if isinstance(response, int):
            return self.get_response_from_index(response)
        elif isinstance(response, str):
            return self.get_response_from_name(response)
        print("Not a foreseen type of response:", type(response))
        print("Expected: int or str")
        return None

    def get_response_from_index(self, response):
        return self.parsed_res[-1]['list_responses'][response]

    def get_response_from_name(self, response, name_type='score_name'):
        if name_type not in self.tables:
            print("Please, choose another response type")
            print("Available ones for your response:")
            for name in self.tables:
                print(name, end=" ")
            print()
            raise KeyError
        allresp = self.parsed_res[-1]['list_responses']
        return allresp[self.tables[name_type][response]]

    def get_score(self, response):
        resp = self.get_response(response)
        return resp['results']['score_res']

    def get_spectrum(self, response, scorenum=None):
        score = self.get_score(response)
        if len(score) > 1:
            print("It would be better to specify which score you want "
                  "as more than one exit")
        return score[0]['spectrum_res']

    def get_mesh(self, response):
        score = self.get_score(response)
        if len(score) > 1:
            print("It would be better to specify which score you want "
                  "as more than one exit")
        # only one score exists in that case
        return score[0]['mesh_res']
