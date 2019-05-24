'''This module define tests for metadata.'''

from ..test import Test, TestResult


class Missing:
    pass


MISSING = Missing()

class TestResultMetadata(TestResult):
    '''Results of metadata comparisons.'''

    def __init__(self, test, dict_res):  # , comp_md_num, comp_md_names, comp_md_values):
        '''Initialisation of TestResultMetadata.'''
        super().__init__(test)
        self.dict_res = dict_res

    def __bool__(self):
        aresp = []
        for key, val in self.dict_res.items():
            aresp.append(all(val.values()))
            # print(key, aresp[-1])
        return all(aresp)

    def per_key(self):
        '''Test result ordered per key.'''
        dresp = {}
        for key, val in self.dict_res.items():
            dresp[key] = all(val.values())
        return dresp

    def only_failed_comparisons(self):
        '''Return only the failed comparisons. Structure is the same as the
        ``dict_res``.'''
        dresp = {}
        for key, val in self.dict_res.items():
            if not all(val.values()):
                dresp[key] = self.test.all_md[key]
        return dresp


class TestMetadata(Test):
    '''A test that compares metadata.
    '''

    def __init__(self, dmd, name, description='',
                 exclude=('results', 'index', 'score_index', 'response_index',
                          'response_type'),
                 include=None):
        super().__init__(name=name, description=description)
        if not isinstance(dmd, dict):
            raise TypeError('Metadata should be given as a dictionary '
                            'name: dict of metadata')
        self.dmd = dmd
        self.exclude = exclude
        self.include = include if include is not None else []
        self.all_md = self.build_metadata_dict()

    def build_metadata_dict(self):
        '''Build the dictionary of metadata.

        Contains all the metadata for all samples.
        '''
        all_keys = (set().union(*[set(md) for md in self.dmd.values()])
                    .difference(self.exclude))
        cdict = {}
        for key in all_keys:
            for name, tmd in self.dmd.items(): #sorted(self.dmd.items())[1:]:
                if key not in tmd:
                    cdict.setdefault(key, {}).update({name: MISSING})
                else:
                    cdict.setdefault(key, {}).update({name: tmd[key]})
        return cdict

    def compare_metadata(self):
        '''Metadata are compared with respect to the first one.'''
        bdict = {}
        t0name = sorted(self.dmd)[0]
        for key, kdict in self.all_md.items():
            bdict[key] = {_n: _v == kdict[t0name] for _n, _v in kdict.items()}
        return bdict

    def evaluate(self):
        '''Evaluate this test and turn it into a :class:`TestResultMetadata`.
        '''
        return TestResultMetadata(self, self.compare_metadata())
