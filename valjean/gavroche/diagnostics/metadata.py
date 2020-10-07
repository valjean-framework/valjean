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
        # aitem = [all(val.values()) for val in self.dict_res.values()]
        # return all(aitem)
        return all(v for val in self.dict_res.values() for v in val.values())

    def per_key(self):
        '''Test result sorted by key.'''
        ditem = {key: all(val.values()) for key, val in self.dict_res.items()}
        return ditem

    def only_failed_comparisons(self):
        '''Return only the failed comparisons. Structure is the same as the
        ``dict_res``.'''
        ditem = {key: self.test.all_md[key]
                 for key, val in self.dict_res.items()
                 if not all(val.values())}
        return ditem


class TestMetadata(Test):
    '''A test that compares metadata.

    .. todo::

        Document the parameters...
    '''

    # pylint: disable=too-many-arguments
    def __init__(self, dict_md, name, description='', labels=None,
                 exclude=('results', 'index', 'score_index', 'response_index',
                          'response_type')):
        '''Initialisation of :class:`TestMetadata`.

        :param str name: local name of the test
        :param str description: specific description of the test
        :param dict labels: labels to be used for test classification in
            reports, for example category, input file name, type of result, ...
        :param tuple exclude: a tuple of keys that will not be considered as
            metadata. Default: ``('results', 'index', 'score_index',
            'response_index', 'response_type')``
        '''
        super().__init__(name=name, description=description, labels=labels)
        if not isinstance(dict_md, dict):
            raise TypeError('Metadata should be given as a dictionary '
                            'name: dict of metadata')
        self.dmd = dict_md
        self.exclude = exclude
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

    def data(self):
        '''Generator yielding objects supporting the buffer protocol that (as a
        whole) represent a serialized version of `self`.'''
        yield from super().data()
        yield self.__class__.__name__.encode('utf-8')
        for key, tmd in self.dmd.items():
            yield key.encode('utf-8')
            for mdkey, mdval in tmd.items():
                yield mdkey.encode('utf-8')
                yield mdval.encode('utf-8')
        for key in self.exclude:
            yield key.encode('utf-8')
