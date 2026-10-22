from copy import deepcopy
import unittest

from .count_catalog import CountJob,acceptance_schema
from .count_replay import same,validate_result

PIN = '1'*64


class NativeCountDeclarationTests(unittest.TestCase):
    def test_schema_reads_exact_original_writer_and24_controls_without_exec(self):
        source = '''def accept():
    mutations = MUTATIONS
    out = dict(status='PASS',n=7,index=37,scope='conditional',seconds=time.time())
'''.replace('MUTATIONS','['+','.join(f"('control{i}', lambda x: None)" for i in range(24))+']')
        schema = acceptance_schema(source)
        self.assertEqual(schema['n'],7);self.assertEqual(schema['index'],37)
        self.assertEqual(len(schema['controls']),24)
        self.assertEqual(schema['fields'],['index','n','scope','seconds','status'])
        with self.assertRaises(ValueError):acceptance_schema(source.replace("('control23', lambda x: None)","('control22', lambda x: None)"))
        with self.assertRaises(ValueError):acceptance_schema('def accept():\n    out = old_PASS')

    def test_type_exact_comparison_rejects_boolean_or_float_census(self):
        self.assertFalse(same({'n':7},{'n':7.0}))
        self.assertFalse(same({'n':1},{'n':True}))
        self.assertTrue(same({'n':7,'rows':['1/3']},{'rows':['1/3'],'n':7}))


class UnchangedCountAcceptanceBindingTests(unittest.TestCase):
    def setUp(self):
        self.job = CountJob('n7.B0.p37',7,'B0',37,'work/original/capsule',PIN,PIN,PIN,'4097/10000',
                            ('1','11/10'),'work/original/complete.json',PIN)
        prefix = self.job.capsule+'/'
        pins = {prefix+name:PIN for name in ('kernel.py','count_protocol.py','contract.json',
                                             'COUNT_FOREST.json','KERNEL_COPY_MANIFEST.json')}
        self.result = dict(status='PASS_LITERAL',n=7,index=37,scope='Conditional exact same-law contract only.',
            forest_sha256=PIN,contract_sha256=PIN,checker_sha256=PIN,kernel_sha256={'kernel.py':PIN},
            statistics=dict(nodes=8,leaves=8,closed_statuses={'EMPTY_PHASE':8},maximum_score='0',maximum_depth=0),
            negative_controls=[f'control{i}' for i in range(24)],fresh_leaf_evaluations=8,seconds=.125)
        schema = {key:self.result[key] for key in ('status','n','index','scope')}
        schema.update(fields=sorted(self.result),controls=list(self.result['negative_controls']))
        self.inspection = dict(native_schema=schema,source_files_sha256=pins,old_schema_reference=None)

    def validate(self):return validate_result(self.job,self.inspection,self.result)

    def test_old_accepted_file_is_not_required_or_used_as_math_input(self):
        facts = self.validate()
        self.assertEqual(facts['fresh_leaf_evaluations'],8)
        self.assertEqual(facts['all_original_roots'],8)
        self.assertEqual(facts['native_negative_controls'],24)
        self.assertNotIn('all_index_conclusion_verified',facts)

    def test_every_kernel_binding_and24_controls_are_required(self):
        original = deepcopy(self.result)
        for change in (lambda z:z['kernel_sha256'].clear(),lambda z:z['negative_controls'].pop(),
                       lambda z:z.update(checker_sha256='0'*64),lambda z:z.update(forest_sha256='0'*64)):
            self.result = deepcopy(original);change(self.result)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_literal_n_and_full_n_plus_one_root_census(self):
        original = deepcopy(self.result)
        changes = (lambda z:z.update(n=7.0),lambda z:z.update(index=True),
                   lambda z:z['statistics'].update(nodes=7),lambda z:z['statistics'].update(leaves=8.0),
                   lambda z:z.update(fresh_leaf_evaluations=7),
                   lambda z:z['statistics'].update(closed_statuses={'EMPTY_PHASE':7}),
                   lambda z:z['statistics'].update(maximum_score='4097/10000'))
        for change in changes:
            self.result = deepcopy(original);change(self.result)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_optional_reference_can_compare_whole_result_not_replace_execution(self):
        self.inspection['old_schema_reference'] = deepcopy(self.result)
        self.result['seconds'] = 2
        self.validate()
        self.inspection['old_schema_reference']['statistics']['maximum_depth'] = 1
        with self.assertRaises(ValueError):self.validate()


if __name__ == '__main__':unittest.main()
