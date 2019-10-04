'''This module define tests for metadata.'''

from ..test import Test, TestResult


class Missing:
    '''Class for missing metadata.'''

    def __str__(self):
        return 'MISSING'


MISSING = Missing()


class TestResultMetadata(TestResult):
    '''Results of metadata comparisons.'''

    def __init__(self, test, dict_res):
        '''Initialisation of TestResultMetadata.'''
        super().__init__(test)
        self.dict_res = dict_res

    def __bool__(self):
        aresp = [all(val.values()) for val in self.dict_res.values()]
        return all(aresp)

    def per_key(self):
        '''Test result sorted by key.'''
        dresp = {key: all(val.values()) for key, val in self.dict_res.items()}
        return dresp

    def only_failed_comparisons(self):
        '''Return only the failed comparisons. Structure is the same as the
        ``dict_res``.'''
        dresp = {key: self.test.all_md[key]
                 for key, val in self.dict_res.items()
                 if not all(val.values())}
        return dresp


class TestMetadata(Test):
    '''A test that compares metadata.

    .. todo::

        Document the parameters...
    '''

    # pylint: disable=too-many-arguments
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
        all_keys = (set(key for md in self.dmd.values() for key in md)
                    .difference(self.exclude))
        # we could write the whole following loop as a nested dict
        # comprehension, but let's not
        cdict = {}
        for key in all_keys:
            cdict[key] = {name: tmd[key] if key in tmd else MISSING
                          for name, tmd in self.dmd.items()}
        return cdict

    def compare_metadata(self):
        '''Metadata are compared with respect to the first one.'''
        bdict = {}
        t0name = sorted(self.dmd)[0]
        for key, kdict in self.all_md.items():
            bdict[key] = {n: v == kdict[t0name] for n, v in kdict.items()}
        return bdict

    def evaluate(self):
        '''Evaluate this test and turn it into a :class:`TestResultMetadata`.
        '''
        return TestResultMetadata(self, self.compare_metadata())
