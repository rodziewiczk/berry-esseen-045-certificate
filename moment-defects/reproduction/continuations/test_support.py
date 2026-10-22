from copy import deepcopy
from fractions import Fraction as F
import ast
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from . import catalog
from .catalog import Asset,Sources,REGIONS
from .support import controls,validate_outputs
from .support_port import port


PIN = '1'*64


class SupportSourcePortTests(unittest.TestCase):
    def test_only_reference_reader_changes_not_math_or_controls(self):
        source = '''from fractions import Fraction
def receipt(p):
    z = read(p)
    for rel,h in z['files_sha256'].items():
        need(sha(R/rel) == h, 'historical source')
    bind(p)
    return z
def target(n, radius):
    return original_full_target(n, radius)
for n in range(6, 10):
    rows.append(target(n, radius))
changes = [('mutation', lambda x: x.clear())]
validate(rows)
'''
        before = ast.parse(source);after = port(ast.parse(source))
        def nonreceipt(tree):
            return [ast.dump(node,include_attributes=False) for node in tree.body
                    if not (isinstance(node,ast.FunctionDef) and node.name == 'receipt')]
        self.assertEqual(nonreceipt(before),nonreceipt(after))
        self.assertNotEqual(ast.dump(before),ast.dump(after))
        function = next(n for n in after.body if isinstance(n,ast.FunctionDef) and n.name == 'receipt')
        self.assertEqual(len(function.body),1)
        self.assertEqual(function.body[0].value.func.id,'__conditional_parent_read')

    def test_absent_or_ambiguous_reference_function_rejected(self):
        for source in ('pass','def receipt(p): pass\ndef receipt(p): pass',
                       'def receipt(p, other): pass'):
            with self.subTest(source=source),self.assertRaises(ValueError):port(ast.parse(source))

    def test_control_inventory_is_the_original_literal_19(self):
        source = 'changes = ['+','.join(repr((f'control{i}',None)) for i in range(18))+']'
        names = controls(source)
        self.assertEqual(len(names),19);self.assertEqual(names[-1],'duplicate JSON key')
        with self.assertRaises(ValueError):controls('changes = []')


class ArchiveSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.one = self.root/'one.zip';self.two = self.root/'two.zip'
        with zipfile.ZipFile(self.one,'w') as archive:archive.writestr('cutoff6_20261020/test.py',b'original\n')
        with zipfile.ZipFile(self.two,'w') as archive:archive.writestr('cutoff10_20261018/test.py',b'other\n')
        def asset(path,roots):
            return Asset(path.name,path.stat().st_size,hashlib.sha256(path.read_bytes()).hexdigest(),roots)
        self.patches = patch.multiple(catalog,CUTOFF6=asset(self.one,('cutoff6_20261020',)),
            COMBINED=asset(self.two,('cutoff10_20261018',)))
        self.patches.start();self.addCleanup(self.patches.stop)

    def test_exact_member_and_pin_no_entire_extraction(self):
        with Sources(self.one,self.two) as sources:
            self.assertEqual(sources.read('work/cutoff6_20261020/test.py',hashlib.sha256(b'original\n').hexdigest()),b'original\n')
            with self.assertRaises(ValueError):sources.read('work/cutoff6_20261020/test.py',PIN)
            with self.assertRaises(FileNotFoundError):sources.member('work/cutoff6_20261020/absent.py')
        self.assertEqual(sorted(path.name for path in self.root.iterdir()),['one.zip','two.zip'])

    def test_escape_and_wrong_archive_rejected(self):
        with Sources(self.one,self.two) as sources:
            for name in ('../test.py','work/../test.py','work\\test.py','/work/test.py','runs/old.json'):
                with self.subTest(name=name),self.assertRaises(ValueError):sources.member(name)
        self.one.write_bytes(b'changed')
        with self.assertRaises(ValueError):Sources(self.one,self.two)


class NativeOutputInventoryTests(unittest.TestCase):
    def setUp(self):
        self.pins = {'work/original.py':PIN}
        self.controls = [f'native{i}' for i in range(19)]
        rows,interfaces = [],[]
        for n in range(6,10):
            for name,left,right,radius in REGIONS:
                q = '579/5000' if n == 6 else '0'
                proof = dict(n=n,K='0',q_contact=q,support_sign=0,radius=radius,rho_upper=right,
                    ray_rows=[dict(sign=sign,contact_upper='-1') for sign in (-1,1)],
                    gaussian=dict(cells=260,mesh=10,H0='13',tail_upper='1/1000000'))
                rows.append(dict(n=n,region=name,rho=[left,right],radius=radius,q=q,proof=proof))
                interfaces.append(dict(n=n,region=name,rho=[left,right],support=radius,fourier_upper='2/5',target='4097/10000'))
        self.constructed = dict(schema='CONDITIONAL_SUPPORT6_9_36_TARGETS_V1',
            status='CONSTRUCTED_EXACT_SUPPORT_AND_FOURIER_INTERFACES',rows=rows,fourier_interfaces=interfaces,
            published_tail=str(F(3031,10000)*(1+F(323,500)/F(7361,4000))),files_sha256=self.pins)
        self.replayed = dict(status='PASS_FRESH_CONDITIONAL_SUPPORT6_9_AND_COMPLEMENT_JOIN',n=[6,7,8,9],
            cutoff6_proved=False,construction_sha256=PIN,negative_controls=self.controls,
            **{key:deepcopy(self.constructed[key]) for key in ('rows','fourier_interfaces','published_tail','files_sha256')})

    def validate(self):
        return validate_outputs(self.constructed,self.replayed,PIN,self.pins,self.controls)

    def test_complete_inventory_schema_only_not_a_numerical_kernel(self):
        facts = self.validate()
        self.assertEqual(facts['support_targets'],36);self.assertEqual(facts['signed_support_rays'],72)
        self.assertNotIn('all_index_conclusion_verified',facts)

    def test_missing_row_control_wrong_literal_index_and_freshness_promotion_rejected(self):
        changes = (
            lambda r:r['rows'].pop(),lambda r:r['negative_controls'].pop(),
            lambda r:r.update(n=[6,7,8,True]),lambda r:r.update(cutoff6_proved=True),
            lambda r:r.update(construction_sha256='0'*64),lambda r:r['files_sha256'].clear())
        original = deepcopy(self.replayed)
        for change in changes:
            self.replayed = deepcopy(original);change(self.replayed)
            with self.subTest(change=change),self.assertRaises(ValueError):self.validate()

    def test_equal_but_wrong_closed_domain_or_allowance_rejected(self):
        for field,value in (('q','0'),('radius','2'),('rho',['1','1099/1000'])):
            constructed,replayed = deepcopy(self.constructed),deepcopy(self.replayed)
            constructed['rows'][0][field] = value;replayed['rows'][0][field] = value
            with self.subTest(field=field),self.assertRaises(ValueError):
                validate_outputs(constructed,replayed,PIN,self.pins,self.controls)


if __name__ == '__main__':unittest.main()
